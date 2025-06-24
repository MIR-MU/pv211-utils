from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseVectorDB(ABC):
    """
    Vector DB interface for storing and searching embeddings.
    """

    @abstractmethod
    def add(self, embeddings: np.ndarray):
        """Add documents and their embeddings to the database."""
        pass

    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int) -> List[int]:
        """Return top-k most similar documents for the query embedding."""
        pass
