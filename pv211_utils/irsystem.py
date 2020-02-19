import abc
from typing import List

from pv211_utils.entities import QueryBase, DocumentBase


class IRSystem(abc.ABC):

    @abc.abstractmethod
    def search(self, query: QueryBase) -> List[DocumentBase]:
        raise NotImplementedError("TODO: fancy stuff goes here: "
                                  "Method search() needs to be implemented in your subclass")
