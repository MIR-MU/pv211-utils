from typing import Iterable, OrderedDict
from sklearn.preprocessing import normalize
import torch
from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase
from ..databases.base_vector_db import BaseVectorDB
from sentence_transformers import CrossEncoder
from sentence_transformers.SentenceTransformer import SentenceTransformer


class RankerSystem(IRSystemBase):
    def __init__(
        self,
        retriever: SentenceTransformer,
        reranker: CrossEncoder,
        vector_db: BaseVectorDB,
        answers: OrderedDict[str, DocumentBase],
        no_reranks: int = 12,
        retriever_batch_size: int = 32,
        reranker_batch_size: int = 16,
        no_returns: int = 100
    ):
        """
        A hybrid ranking system that uses dense retrieval followed by cross-encoder reranking
        to return the most relevant documents from a set of answer candidates.

        Args:
            retriever (SentenceTransformer): Model to encode queries and documents into dense vectors.
            reranker (CrossEncoder): Cross-encoder model to rerank top documents using deep pairwise scoring.
            vector_db (BaseVectorDB): Database that supports vector similarity search.
            answers (OrderedDict[str, DocumentBase]): Ordered mapping of answer IDs to documents to be indexed.
            no_reranks (int): Number of top retrieved documents to rerank using the cross-encoder.
            retriever_batch_size (int): Batch size to use during initial embedding of documents.
            reranker_batch_size (int): Batch size to use when scoring pairs with the cross-encoder.
            no_returns (int): Maximum number of documents to retrieve from the vector store per query.
        """
        self.retriever = retriever.eval()
        self.reranker = reranker
        self.vector_db = vector_db
        self.reranker_batch_size = reranker_batch_size
        self.no_reranks = no_reranks
        self.no_returns = no_returns
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.answers = list(answers.values())
        answer_texts = [str(answer) for answer in self.answers]

        # Encode and normalize all answer documents for efficient cosine similarity search
        with torch.no_grad():
            answer_embeddings = self.retriever.encode(
                answer_texts,
                convert_to_tensor=True,
                batch_size=retriever_batch_size,
                device=self.device
            ).cpu().numpy()

        answer_embeddings = normalize(answer_embeddings, axis=1)
        self.vector_db.add(answer_embeddings)

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """
        Performs dense retrieval followed by reranking, and yields documents in descending order of relevance.

        Args:
            query (QueryBase): The user query to search against the stored answers.

        Yields:
            DocumentBase: Ranked answer documents.
        """
        with torch.no_grad():
            query_embedding = self.retriever.encode(
                str(query),
                convert_to_numpy=True,
                device=self.device
            )

        query_embedding = normalize(query_embedding.reshape(1, -1), axis=1)

        retrieved_indices = self.vector_db.search(
            query_embedding[0],
            top_k=min(len(self.answers), self.no_returns)
        )

        rerank_indices = retrieved_indices[:self.no_reranks]
        rerank_docs = [str(self.answers[i]) for i in rerank_indices]
        rerank_pairs = [(str(query), doc) for doc in rerank_docs]

        scores = self.reranker.predict(rerank_pairs, batch_size=self.reranker_batch_size)
        reranked = sorted(zip(rerank_indices, scores), key=lambda x: x[1], reverse=True)

        for idx, _ in reranked:
            yield self.answers[idx]

        for idx in retrieved_indices[self.no_reranks:]:
            yield self.answers[idx]

        seen_ids = set(retrieved_indices)
        for doc_id, doc in self.answers.items():
            if doc_id not in seen_ids:
                yield doc
        