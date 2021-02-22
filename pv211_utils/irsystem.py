import abc
from typing import Iterable

from .entities import QueryBase, DocumentBase


class IRSystemBase(abc.ABC):
    """An information retrieval system.

    """
    @abc.abstractmethod
    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        pass
