import abc
from typing import Iterable

from ..irsystem import IRSystem
from .entities import CranfieldQueryBase, CranfieldDocumentBase


class CranfieldIRSystem(IRSystem):
    @abc.abstractmethod
    def search(self, query: CranfieldQueryBase) -> Iterable[CranfieldDocumentBase]:
        pass
