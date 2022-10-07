from typing import Iterable, OrderedDict

from sentence_transformers.SentenceTransformer import SentenceTransformer
import numpy as np
import torch

from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.irsystem import IRSystemBase


class RetrieverSystem(IRSystemBase):
    def __init__(self, retriever: SentenceTransformer, answers: OrderedDict, batch_size: int = 32):
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
        """

        answers_bodies = [answer.body for _, answer in answers.items()]

        self.answers = list(answers.values())

        self.retriever = retriever
        self.retriever.eval()

        with torch.no_grad():
            self.answers_embeddings = self.retriever.encode(
                answers_bodies, convert_to_tensor='pt', batch_size=batch_size)

        self.answers_embeddings = self.answers_embeddings.detach().cpu().numpy()

        self.answers_embedding_norm = [np.linalg.norm(embedding) for embedding in self.answers_embeddings]

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

        query_embedding = self.retriever.encode(query.body)
        query_embedding_norm = np.linalg.norm(query_embedding)

        similarities = [_compute_similarity(i) for i in range(len(self.answers_embeddings))]

        sorted_similarities = np.array(similarities).argsort()[::-1]

        for doc in sorted_similarities:
            yield self.answers[doc]
