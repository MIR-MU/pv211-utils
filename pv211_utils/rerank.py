import abc
from typing import Iterable

from .entities import DocumentBase


class ReRankBase(abc.ABC):
    """A reranking method for Information Retrieval systems.

    """
    @abc.abstractmethod
    def rerank_top_k(self, query, retrieved_documents, k: int) \
            -> Iterable[DocumentBase]:
        pass
