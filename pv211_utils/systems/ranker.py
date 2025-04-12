from typing import OrderedDict
import numpy as np
from sklearn.preprocessing import normalize
import torch
from ..entities import DocumentBase
from ..irsystem import IRSystemBase
from ..databases.vectorDB import BaseVectorDB
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
    ):
        self.retriever = retriever
        self.retriever.eval()
        self.reranker = reranker
        self.no_reranks = no_reranks
        self.answers = list(answers.values())
        self.vector_db = vector_db

        answers_bodies = [str(answer) for answer in self.answers]

        with torch.no_grad():
            answers_embeddings = self.retriever.encode(
                answers_bodies,
                convert_to_tensor=True,
                batch_size=retriever_batch_size,
                device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
            ).cpu().numpy()

        # Normalize for cosine similarity
        answers_embeddings = normalize(answers_embeddings, axis=1)
        self.vector_db.add(answers_embeddings)

    def search(self, query):
        with torch.no_grad():
            query_embedding = self.retriever.encode(
                str(query),
                convert_to_numpy=True,
                device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
            )

        # Normalize query
        query_embedding = normalize(query_embedding.reshape(1, -1), axis=1)

        retrieved_indices = self.vector_db.search(query_embedding[0], top_k=min(len(self.answers), 100))

        top_doc_indices = retrieved_indices[:self.no_reranks]
        top_docs = [str(self.answers[i]) for i in top_doc_indices]
        pairs = [(str(query), doc) for doc in top_docs]

        scores = self.reranker.predict(pairs, batch_size=16)
        reranked = sorted(zip(top_doc_indices, scores), key=lambda x: x[1], reverse=True)

        for i, _ in reranked:
            yield self.answers[i]

        for i in retrieved_indices[self.no_reranks:]:
            yield self.answers[i]

        used = set(retrieved_indices)
        for i in range(len(self.answers)):
            if i not in used:
                yield self.answers[i]
