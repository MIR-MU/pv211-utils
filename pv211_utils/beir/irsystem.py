import abc
from typing import Iterable

from ..irsystem import IRSystemBase
from .entities import BeirQueryBase, BeirDocumentBase


class BeirIRSystemBase(IRSystemBase):
    @abc.abstractmethod
    def search(self, query: BeirQueryBase) -> Iterable[BeirDocumentBase]:
        pass
