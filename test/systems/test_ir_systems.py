# test_ir_systems.py
import unittest
from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer

# Import the new, separated test cases
from test.systems.data_ir_testset import (
    DOCUMENTS,
    TRIVIAL_TEST_CASES,
    ADVANCED_TEST_CASES
)

# Import your systems and utilities
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
        doc_preprocessing = DocPreprocessing()

        self.all_systems = [
            BM25PlusSystem(DOCUMENTS, doc_preprocessing),
            BoWSystem(DOCUMENTS, doc_preprocessing),
            TfidfSystem(DOCUMENTS, doc_preprocessing),
            RankerSystem(retriever_model, reranker_model, faiss, DOCUMENTS),
            RerankerSystem(retriever_model, reranker_model, DOCUMENTS),
            RetrieverSystem(retriever_model, DOCUMENTS)
        ]

        self.doc_text_to_id_map = {doc.text: doc_id for doc_id, doc in DOCUMENTS.items()}

    def test_trivial_ranking_on_all_systems(self):
        """
        Runs 10 trivial tests on ALL systems to ensure a basic
        level of keyword matching is functional.
        """
        for system in self.all_systems:
            for case in TRIVIAL_TEST_CASES:
                with self.subTest(system=system.__class__.__name__, test=case["test_name"]):
                    results = system.search(case["query"])
                    result_ids = [self.doc_text_to_id_map.get(doc.text) for doc in results]

                    required_doc_id = case["expected_doc_in_top_3"]
                    top_3_ids = result_ids[:3]
                    self.assertIn(
                        required_doc_id,
                        top_3_ids,
                        f"Expected '{required_doc_id}' in top 3. Got {top_3_ids}."
                    )

    def test_advanced_ranking_on_capable_systems(self):
        """
        Runs 10 advanced tests only on systems considered more capable
        than basic BoW and BM25.
        """
        capable_systems = [
            s for s in self.all_systems
            if not isinstance(s, (BoWSystem, BM25PlusSystem, TfidfSystem))
        ]

        for system in capable_systems:
            for case in ADVANCED_TEST_CASES:
                with self.subTest(system=system.__class__.__name__, test=case["test_name"]):
                    results = system.search(case["query"])
                    result_ids = [self.doc_text_to_id_map.get(doc.text) for doc in results]

                    if "expected_doc_in_top_3" in case:
                        required_doc_id = case["expected_doc_in_top_3"]
                        top_3_ids = result_ids[:3]
                        self.assertIn(
                            required_doc_id,
                            top_3_ids,
                            f"Expected '{required_doc_id}' in top 3. Got {top_3_ids}."
                        )

                    if "must_include_in_top_5" in case:
                        required_ids = set(case["must_include_in_top_5"])
                        top_5_ids = set(result_ids[:5])
                        self.assertTrue(
                            required_ids.issubset(top_5_ids),
                            f"Not all required docs {required_ids} were in top 5. Got {top_5_ids}."
                        )

                    if "must_exclude" in case:
                        excluded_id = case["must_exclude"]
                        self.assertNotIn(
                            excluded_id,
                            result_ids,
                            f"Excluded doc '{excluded_id}' was found in results."
                        )
