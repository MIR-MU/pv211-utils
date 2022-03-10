import unittest
from typing import List, Set

from pv211_utils.entities import QueryBase, DocumentBase, JudgementBase
from pv211_utils.irsystem import IRSystemBase
from pv211_utils.eval import EvaluationBase


AUTHOR_NAME = 'John Doe'

JUDGED_QUERY_ID = 123
FIRST_RELEVANT_DOCUMENT_ID = '1'
SECOND_RELEVANT_DOCUMENT_ID = '2'
FIRST_IRRELEVANT_DOCUMENT_ID = '3'
SECOND_IRRELEVANT_DOCUMENT_ID = '4'

UNJUDGED_QUERY_ID = 456


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
    def __init__(self, system: IRSystemBase, judgements: Set[JudgementBase], num_workers: int):
        super().__init__(system, judgements, num_workers=num_workers)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.5


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.judged_query = QueryBase(JUDGED_QUERY_ID, None)
        self.unjudged_query = QueryBase(UNJUDGED_QUERY_ID, None)

        self.judged_queries = [self.judged_query]
        self.unjudged_queries = [self.unjudged_query]

        self.first_relevant_document = DocumentBase(FIRST_RELEVANT_DOCUMENT_ID, None)
        self.second_relevant_document = DocumentBase(SECOND_RELEVANT_DOCUMENT_ID, None)
        self.first_irrelevant_document = DocumentBase(FIRST_IRRELEVANT_DOCUMENT_ID, None)
        self.second_irrelevant_document = DocumentBase(SECOND_IRRELEVANT_DOCUMENT_ID, None)

        judgements = set([
            (self.judged_query, self.first_relevant_document),
            (self.judged_query, self.second_relevant_document),
        ])
        good_system = GoodIRSystem()
        mediocre_system = MediocreIRSystem()
        bad_system = BadIRSystem()

        self.good_evaluation_single_process = Evaluation(good_system, judgements, num_workers=1)
        self.mediocre_evaluation_single_process = Evaluation(mediocre_system, judgements, num_workers=1)
        self.bad_evaluation_single_process = Evaluation(bad_system, judgements, num_workers=1)

        self.good_evaluation_multi_process = Evaluation(good_system, judgements, num_workers=2)
        self.mediocre_evaluation_multi_process = Evaluation(mediocre_system, judgements, num_workers=2)
        self.bad_evaluation_multi_process = Evaluation(bad_system, judgements, num_workers=2)

    def test_average_precision_unjudged(self):
        results = [
            self.first_relevant_document,
            self.second_irrelevant_document,
        ]
        precision = self.mediocre_evaluation_single_process._average_precision(self.unjudged_query, results)
        self.assertEqual(None, precision)

    def test_average_precision_zero(self):
        results = [
            self.first_irrelevant_document,
            self.second_irrelevant_document,
        ]
        precision = self.bad_evaluation_single_process._average_precision(self.judged_query, results)
        self.assertEqual(0.0, precision)

    def test_average_precision_half(self):
        results = [
            self.first_relevant_document,
            self.second_irrelevant_document,
        ]
        precision = self.mediocre_evaluation_single_process._average_precision(self.judged_query, results)
        self.assertEqual(0.5, precision)

    def test_average_precision_one(self):
        results = [
            self.first_relevant_document,
            self.second_relevant_document,
        ]
        precision = self.good_evaluation_single_process._average_precision(self.judged_query, results)
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
        precision = self.good_evaluation_single_process._average_precision(self.judged_query, results)
        self.assertEqual(1.0, precision)

    def test_mean_average_precision_unjudged_single_process(self):
        with self.assertRaises(KeyError):
            self.mediocre_evaluation_single_process.mean_average_precision(self.unjudged_queries)

    def test_mean_average_precision_zero_single_process(self):
        mean_average_precision = self.bad_evaluation_single_process.mean_average_precision(self.judged_queries)
        self.assertEqual(0.0, mean_average_precision)

    def test_mean_average_precision_half_single_process(self):
        mean_average_precision = self.mediocre_evaluation_single_process.mean_average_precision(self.judged_queries)
        self.assertEqual(0.5, mean_average_precision)

    def test_mean_average_precision_one_single_process(self):
        mean_average_precision = self.good_evaluation_single_process.mean_average_precision(self.judged_queries)
        self.assertEqual(1.0, mean_average_precision)

    def test_mean_average_precision_unjudged_multi_process(self):
        with self.assertRaises(KeyError):
            self.mediocre_evaluation_multi_process.mean_average_precision(self.unjudged_queries)

    def test_mean_average_precision_zero_multi_process(self):
        mean_average_precision = self.bad_evaluation_multi_process.mean_average_precision(self.judged_queries)
        self.assertEqual(0.0, mean_average_precision)

    def test_mean_average_precision_half_multi_process(self):
        mean_average_precision = self.mediocre_evaluation_multi_process.mean_average_precision(self.judged_queries)
        self.assertEqual(0.5, mean_average_precision)

    def test_mean_average_precision_one_multi_process(self):
        mean_average_precision = self.good_evaluation_multi_process.mean_average_precision(self.judged_queries)
        self.assertEqual(1.0, mean_average_precision)
