import abc
from typing import Iterable

from .entities import DocumentBase


class IRSystemBase(abc.ABC):
    """An information retrieval system."""

    @abc.abstractmethod
    def search(self, query) -> Iterable[DocumentBase]:
        pass
