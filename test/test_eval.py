import unittest
from typing import List

from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.irsystem import IRSystemBase
from pv211_utils.eval import average_precision, mean_average_precision


AUTHOR_NAME = 'John Doe'

QUERY_ID = 123
FIRST_RELEVANT_DOCUMENT_ID = '1'
SECOND_RELEVANT_DOCUMENT_ID = '2'
FIRST_IRRELEVANT_DOCUMENT_ID = '3'
SECOND_IRRELEVANT_DOCUMENT_ID = '4'


class GoodIRSystem(IRSystemBase):
    def search(self, query: QueryBase) -> List[DocumentBase]:
        first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        second_relevant_document = DocumentBase(SECOND_RELEVANT_DOCUMENT_ID, None)
        return [first_relevant_document, second_relevant_document]


class BadIRSystem(IRSystemBase):
    def search(self, query: QueryBase) -> List[DocumentBase]:
        first_irrelevant_document = DocumentBase(FIRST_IRRELEVANT_DOCUMENT_ID, None)
        second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)
        return [first_irrelevant_document, second_irrelevant_document]


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


class TestMeanAveragePrecision(unittest.TestCase):
    def setUp(self):
        query = QueryBase(QUERY_ID, None)
        self.queries = [query]

        first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        second_relevant_document = DocumentBase(SECOND_RELEVANT_DOCUMENT_ID, None)
        self.judgements = set([
            (query, first_relevant_document),
            (query, second_relevant_document),
        ])

        self.good_irsystem = GoodIRSystem()
        self.bad_irsystem = BadIRSystem()

    def test_mean_average_precision_zero(self):
        precision = mean_average_precision(self.bad_irsystem, self.queries, self.judgements)
        self.assertEqual(0.0, precision)

    def test_mean_average_precision_one(self):
        precision = mean_average_precision(self.good_irsystem, self.queries, self.judgements)
        self.assertEqual(1.0, precision)
