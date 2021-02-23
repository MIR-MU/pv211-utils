import abc
from typing import Iterable

from ..irsystem import IRSystemBase
from .entities import TrecQueryBase, TrecDocumentBase


class TrecIRSystemBase(IRSystemBase):
    @abc.abstractmethod
    def search(self, query: TrecQueryBase) -> Iterable[TrecDocumentBase]:
        pass
