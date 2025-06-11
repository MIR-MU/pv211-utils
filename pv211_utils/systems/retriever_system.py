from typing import Iterable, OrderedDict
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase


class RetrieverSystem(IRSystemBase):
    def __init__(
        self,
        retriever: SentenceTransformer,
        answers: OrderedDict,
        batch_size: int = 32,
        no_query_expansion: int = 0,
        top_k_sentences: int = 3,
    ):
        """
        A system that returns documents ordered by decreasing cosine similarity.

        Parameters
        ----------
        retriever: SentenceTransformer
            retriever model
        answers: OrderedDict
            Possible answers
        batch_size: int
            The batch size used for the computation
        no_query_expansion : int
            Number of query expansion iterations.
        top_k_sentences : int
            Number of top-relevant sentences to extract for query expansion.
        """

        answers_bodies = [str(answer) for _, answer in answers.items()]

        self.answers = list(answers.values())
        self.no_query_expansion = no_query_expansion
        self.top_k_sentences = top_k_sentences
        self.retriever = retriever
        self.retriever.eval()

        with torch.no_grad():
            self.answers_embeddings = self.retriever.encode(
                answers_bodies, convert_to_tensor="pt", batch_size=batch_size
            )

        self.answers_embeddings = self.answers_embeddings.detach().cpu().numpy()

        self.answers_embedding_norm = [
            np.linalg.norm(embedding) for embedding in self.answers_embeddings
        ]

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """Recursively refine the query and retrieve documents.

        Parameters
        ----------
        query: QueryBase
            The initial user query.
        """

        def _compute_similarity(i: int) -> float:
            # compute similarity between query and answer on index i
            dt = np.dot(query_embedding, self.answers_embeddings[i])
            return dt / (query_embedding_norm * self.answers_embedding_norm[i])

        def _extract_top_k_sentences(doc_text, query_text, k):
            sentences = doc_text.split(". ")
            vectorizer = TfidfVectorizer().fit_transform([query_text] + sentences)
            query_vec = vectorizer[0]  # First vector is the query
            sentence_vecs = vectorizer[1:]  # Remaining are sentences

            # Compute cosine similarity
            similarities = (sentence_vecs * query_vec.T).toarray().flatten()
            top_indices = similarities.argsort()[-k:][::-1]

            return " ".join([sentences[i] for i in top_indices])

        query_text = str(query)
        query_embedding = self.retriever.encode(query_text)
        query_embedding_norm = np.linalg.norm(query_embedding)

        used_doc_indices = set()

        for _ in range(self.no_query_expansion):
            similarities = [
                _compute_similarity(i) for i in range(len(self.answers_embeddings))
            ]
            sorted_indices = np.argsort(similarities)[::-1]

            for idx in sorted_indices:
                if idx not in used_doc_indices:
                    break

            used_doc_indices.add(idx)
            top_doc_text = self.answers[idx]

            if isinstance(top_doc_text, DocumentBase):
                top_doc_text = top_doc_text.body

            top_doc_summary = _extract_top_k_sentences(
                top_doc_text, query_text, self.top_k_sentences
            )
            query_text = query_text + " " + top_doc_summary

            query_embedding = self.retriever.encode(query_text)
            query_embedding_norm = np.linalg.norm(query_embedding)

        similarities = [
            _compute_similarity(i) for i in range(len(self.answers_embeddings))
        ]
        sorted_similarities = np.array(similarities).argsort()[::-1]

        for doc in sorted_similarities:
            yield self.answers[doc]
