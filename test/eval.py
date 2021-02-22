import unittest

from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.eval import average_precision


QUERY_ID = 123
FIRST_RELEVANT_DOCUMENT_ID = 1
SECOND_RELEVANT_DOCUMENT_ID = 2
FIRST_IRRELEVANT_DOCUMENT_ID = 3
SECOND_IRRELEVANT_DOCUMENT_ID = 4


class TestAveragePrecision(unittest.TestCase):
    def setUp(self):
        self.query = QueryBase(QUERY_ID, None)
        self.first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        self.second_relevant_document = DocumentBase(SECOND_RELEVANT_DOCUMENT_ID, None)
        self.first_irrelevant_document = DocumentBase(FIRST_IRRELEVANT_DOCUMENT_ID, None)
        self.second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)

        self.relevant = set([
            (self.query, self.first_relevant_document),
            (self.query, self.second_relevant_document),
        ])
        self.num_relevant = len(self.relevant)

    def test_average_precision_zero(self):
        results = [
            self.first_irrelevant_document,
            self.second_irrelevant_document,
        ]
        precision = average_precision(self.query, results, self.relevant, self.num_relevant)
        self.assertEqual(0.0, precision)

    def test_average_precision_one(self):
        results = [
            self.first_relevant_document,
            self.second_relevant_document,
        ]
        precision = average_precision(self.query, results, self.relevant, self.num_relevant)
        self.assertEqual(1.0, precision)

    def test_average_precision_repeated_documents(self):
        results = [
            self.first_relevant_document,
            self.second_relevant_document,
            self.first_irrelevant_document,
            self.second_irrelevant_document,
            self.first_relevant_document,
            self.second_relevant_document,
        ]
        precision = average_precision(self.query, results, self.relevant, self.num_relevant)
        self.assertEqual(1.0, precision)
