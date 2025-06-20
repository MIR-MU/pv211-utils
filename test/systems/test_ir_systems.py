import unittest
from test.systems.data_ir_testset import DOCUMENTS, QUERY
from sentence_transformers import CrossEncoder
from sentence_transformers.SentenceTransformer import SentenceTransformer


from pv211_utils.systems.bm25 import BM25PlusSystem
from pv211_utils.systems.bow import BoWSystem
from pv211_utils.systems.ranker import RankerSystem
from pv211_utils.systems.reranker import RerankerSystem
from pv211_utils.systems.retriever import RetrieverSystem
from pv211_utils.systems.tfidf import TfidfSystem
from pv211_utils.preprocessing.text_preprocessing import DocPreprocessing
from pv211_utils.databases.faiss_vector_db import FaissVectorDB


class TestIRSystems(unittest.TestCase):
    def setUp(self):

        reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        retriever_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        faiss = FaissVectorDB()

        self.systems = [
            BM25PlusSystem(DOCUMENTS, DocPreprocessing()),
            BoWSystem(DOCUMENTS, DocPreprocessing()),
            TfidfSystem(DOCUMENTS, DocPreprocessing()),
            RankerSystem(retriever_model, reranker_model, faiss, DOCUMENTS),
            RerankerSystem(retriever_model, reranker_model, DOCUMENTS),
            RetrieverSystem(retriever_model, DOCUMENTS)

        ]

    def test_query_ranking_is_reasonable(self):
        for system in self.systems:
            with self.subTest(system=system.__class__.__name__):
                results = list(system.search(QUERY))
                self.assertGreaterEqual(str(results[0]).count("polar"), 1)
                self.assertIn("climate", str(results[0]))  # Strong indicator it's doc 1
