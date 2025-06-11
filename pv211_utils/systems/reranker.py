from typing import Iterable, OrderedDict

import numpy as np
import torch
from sentence_transformers import CrossEncoder
from sentence_transformers.SentenceTransformer import SentenceTransformer

from ..entities import DocumentBase, QueryBase
from ..irsystem import IRSystemBase


class RerankerSystem(IRSystemBase):
    def __init__(
        self,
        retriever: SentenceTransformer,
        reranker: CrossEncoder,
        answers: OrderedDict,
        no_reranks: int = 16,
        retriever_batch_size: int = 32,
        reranker_batch_size: int = 8,
    ):
        """
        A system that returns documents ordered by decreasing cosine similarity.

        Parameters
        ----------
        retriever: SentenceTransformer
            Retriever model
        reranker: CrossEncoder
            Reranker model
        answers: OrderedDict
            Possible answers
        no_reranks: int
            Number of documents to rerank
        retriever_batch_size: int
            The retriever batch size for encoding
        reranker_batch_size: int
            The reranker batch size for prediction
        """

        answers_bodies = [str(answer) for _, answer in answers.items()]

        self.answers = list(answers.values())

        self.reranker_batch_size = reranker_batch_size
        self.no_reranks = no_reranks

        self.retriever = retriever
        self.retriever.eval()

        self.reranker = reranker

        with torch.no_grad():
            self.answers_embeddings = self.retriever.encode(
                answers_bodies, convert_to_tensor="pt", batch_size=retriever_batch_size
            )

        self.answers_embeddings = self.answers_embeddings.detach().cpu().numpy()

        self.answers_embedding_norm = [
            np.linalg.norm(embedding) for embedding in self.answers_embeddings
        ]

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """The ranked retrieval results for a query.

        Parameters
        ----------
        query: QueryBase
            A query.
        """

        def _compute_similarity(i: int) -> float:
            # compute similarity between query and answer on index i
            dt = np.dot(query_embedding, self.answers_embeddings[i])
            return dt / (query_embedding_norm * self.answers_embedding_norm[i])

        query_embedding = self.retriever.encode(str(query))
        query_embedding_norm = np.linalg.norm(query_embedding)

        similarities = [
            _compute_similarity(i) for i in range(len(self.answers_embeddings))
        ]
        sorted_similarities = np.array(similarities).argsort()[::-1]

        # rerank top documents returned by retriever
        retriever_top = []
        for i in range(self.no_reranks):
            retriever_top.append(
                [str(query), str(self.answers[sorted_similarities[i]])]
            )

        rerank_predictions = self.reranker.predict(
            retriever_top, batch_size=self.reranker_batch_size
        )
        rerank_predictions = np.array(rerank_predictions).argsort()[::-1]

        # return documents in reranked order
        for doc in rerank_predictions:
            yield self.answers[sorted_similarities[doc]]

        for doc in sorted_similarities[self.no_reranks :]:
            yield self.answers[doc]
