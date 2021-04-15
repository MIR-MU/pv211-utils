import abc
from typing import Iterable

from ..irsystem import IRSystemBase
from .entities import ArqmathQueryBase, ArqmathAnswerBase


class ArqmathIRSystemBase(IRSystemBase):
    @abc.abstractmethod
    def search(self, query: ArqmathQueryBase) -> Iterable[ArqmathAnswerBase]:
        pass
