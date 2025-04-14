from abc import ABC, abstractmethod
from typing import List
import numpy as np
from ..entities import DocumentBase


class BaseVectorDB(ABC):
    """
    Vector DB interface for storing and searching embeddings.
    """
    @abstractmethod
    def add(self, embeddings: np.ndarray):
        """Add documents and their embeddings to the database."""
        pass

    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int = 10) -> List[DocumentBase]:
        """Return top-k most similar documents for the query embedding."""
        pass
