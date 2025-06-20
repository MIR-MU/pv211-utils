import unittest
from collections import OrderedDict
from typing import List

from pv211_utils.systems.bow import BoWSystem
from pv211_utils.entities import DocumentBase, QueryBase
from pv211_utils.preprocessing import DocPreprocessingBase


class DummyDocument(DocumentBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


class DummyQuery(QueryBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


class DummyPreprocessor(DocPreprocessingBase):
    def __call__(self, text: str) -> List[str]:
        return text.lower().split()


class TestBoWSystem(unittest.TestCase):
    def setUp(self):
        self.documents = OrderedDict({
            "1": DummyDocument("the cat sat on the mat"),
            "2": DummyDocument("the dog sat on the mat"),
            "3": DummyDocument("the cat chased the mouse"),
        })
        self.preprocessor = DummyPreprocessor()
        self.system = BoWSystem(self.documents, self.preprocessor)

    def test_dictionary_contains_expected_terms(self):
        token_ids = self.system.dictionary.token2id
        self.assertIn("cat", token_ids)
        self.assertIn("mat", token_ids)
        self.assertEqual(len(self.system.index_to_document), 3)

    def test_search_returns_relevant_documents(self):
        query = DummyQuery("cat mat")
        results = list(self.system.search(query))

        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[0], DummyDocument)
        self.assertEqual(str(results[0]), "the cat sat on the mat")

