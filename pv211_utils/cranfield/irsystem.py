import abc
from typing import Iterable

from ..irsystem import IRSystemBase
from .entities import CranfieldQueryBase, CranfieldDocumentBase


class CranfieldIRSystemBase(IRSystemBase):
    @abc.abstractmethod
    def search(self, query: CranfieldQueryBase) -> Iterable[CranfieldDocumentBase]:
        pass
