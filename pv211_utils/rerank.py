import abc
from typing import Iterable

from .entities import QueryBase, DocumentBase


class ReRankBase(abc.ABC):
    """A reranking method for Information Retrieval systems.

    """
    @abc.abstractmethod
    def rerank_top_k(self, query: QueryBase, retrieved_documents: Iterable[DocumentBase], k: int) \
            -> Iterable[DocumentBase]:
        pass
