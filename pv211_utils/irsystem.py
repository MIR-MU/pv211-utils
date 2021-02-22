import abc
from typing import Iterable

from .entities import QueryBase, DocumentBase


class IRSystem(abc.ABC):
    @abc.abstractmethod
    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        pass
