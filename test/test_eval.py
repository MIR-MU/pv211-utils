import unittest
from typing import List, Set

from pv211_utils.entities import QueryBase, DocumentBase, JudgementBase
from pv211_utils.irsystem import IRSystemBase
from pv211_utils.eval import EvaluationBase


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


class MediocreIRSystem(IRSystemBase):
    def search(self, query: QueryBase) -> List[DocumentBase]:
        first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)
        return [first_relevant_document, second_irrelevant_document]


class BadIRSystem(IRSystemBase):
    def search(self, query: QueryBase) -> List[DocumentBase]:
        first_irrelevant_document = DocumentBase(FIRST_IRRELEVANT_DOCUMENT_ID, None)
        second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)
        return [first_irrelevant_document, second_irrelevant_document]


class Evaluation(EvaluationBase):
    def __init__(self, system: IRSystemBase, judgements: Set[JudgementBase]):
        super().__init__(system, judgements)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.5


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.query = QueryBase(QUERY_ID, None)
        self.queries = [self.query]

        self.first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        self.second_relevant_document = DocumentBase(SECOND_RELEVANT_DOCUMENT_ID, None)
        self.first_irrelevant_document = DocumentBase(FIRST_IRRELEVANT_DOCUMENT_ID, None)
        self.second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)

        judgements = set([
            (self.query, self.first_relevant_document),
            (self.query, self.second_relevant_document),
        ])
        good_system = GoodIRSystem()
        mediocre_system = MediocreIRSystem()
        bad_system = BadIRSystem()

        self.good_evaluation = Evaluation(good_system, judgements)
        self.mediocre_evaluation = Evaluation(mediocre_system, judgements)
        self.bad_evaluation = Evaluation(bad_system, judgements)

    def test_average_precision_zero(self):
        results = [
            self.first_irrelevant_document,
            self.second_irrelevant_document,
        ]
        precision = self.bad_evaluation._average_precision(self.query, results)
        self.assertEqual(0.0, precision)

    def test_average_precision_half(self):
        results = [
            self.first_relevant_document,
            self.second_irrelevant_document,
        ]
        precision = self.mediocre_evaluation._average_precision(self.query, results)
        self.assertEqual(0.5, precision)

    def test_average_precision_one(self):
        results = [
            self.first_relevant_document,
            self.second_relevant_document,
        ]
        precision = self.good_evaluation._average_precision(self.query, results)
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
        precision = self.good_evaluation._average_precision(self.query, results)
        self.assertEqual(1.0, precision)

    def test_mean_average_precision_zero(self):
        mean_average_precision = self.bad_evaluation.mean_average_precision(self.queries)
        self.assertEqual(0.0, mean_average_precision)

    def test_mean_average_precision_half(self):
        mean_average_precision = self.mediocre_evaluation.mean_average_precision(self.queries)
        self.assertEqual(0.5, mean_average_precision)

    def test_mean_average_precision_one(self):
        mean_average_precision = self.good_evaluation.mean_average_precision(self.queries)
        self.assertEqual(1.0, mean_average_precision)
