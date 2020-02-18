import abc
from typing import List

from pv211_utils.entities import Query, Document


class IRSystem(abc.ABC):

    @abc.abstractmethod
    def search(self, query: Query) -> List[Document]:
        raise NotImplementedError("Method search() needs to be implemented in subclass")
