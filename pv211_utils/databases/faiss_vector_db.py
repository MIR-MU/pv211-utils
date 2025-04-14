import faiss
import numpy as np
from .base_vector_db import BaseVectorDB


class FaissVectorDB(BaseVectorDB):
    """
    Vector DB implementation using FAISS for efficient similarity search.
    This class uses the FAISS library to create an index for fast nearest neighbor search.
    It supports adding embeddings and searching for the most similar ones.
    """
    def __init__(self):
        self.index = None

    def add(self, embeddings: np.ndarray):
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(embedding_dim)  # Use Inner Product for cosine
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int):
        _, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
        return indices[0].tolist()
