import unittest
from typing import Any, Iterable
from collections import OrderedDict

from pv211_utils.evaluation_metrics import (mean_average_precision,
                                            mean_precision,
                                            mean_recall,
                                            normalized_discounted_cumulative_gain,
                                            mean_bpref)
from pv211_utils.entities import QueryBase, DocumentBase
from pv211_utils.irsystem import IRSystemBase


class Query(QueryBase):
    def __init__(self, query_id: int, body: Any):
        super().__init__(query_id, body)


class Document(DocumentBase):
    def __init__(self, document_id: str, body: Any):
        super().__init__(document_id, body)


QUERIES = OrderedDict({1: Query(1, "a"), 2: Query(2, "b")})
DOCUMENTS = {1: Document('1', "a"), 2: Document('2', "b"),
             3: Document('3', "c"), 4: Document('4', "d")}
JUDGEMENTS = {(QUERIES[1], DOCUMENTS[1]), (QUERIES[1], DOCUMENTS[2]),
              (QUERIES[2], DOCUMENTS[4]), (QUERIES[2], DOCUMENTS[3])}


class System(IRSystemBase):
    def __init__(self, doc_order: dict[int, list[int]]) -> None:
        self.doc_order = doc_order

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        for doc_id in self.doc_order[query.query_id]:
            yield DOCUMENTS[doc_id]


class TestEvaluationMetrics(unittest.TestCase):
    def setUp(self) -> None:
        self.system_perfect = System({1: [1, 2, 3, 4], 2: [4, 3, 2, 1]})
        self.system_mediocore_1 = System({1: [1, 4, 3, 2], 2: [4, 1, 2, 3]})
        self.system_mediocore_2 = System({1: [1, 2, 3, 4], 2: [1, 2, 3, 4]})
        self.system_bad = System({1: [3, 4, 1, 2], 2: [2, 1, 4, 3]})

    def test_mean_avarage_precision_perfect(self):
        map = mean_average_precision(self.system_perfect, QUERIES, JUDGEMENTS, 5, 3)

        self.assertEqual(1, map)

    def test_mean_avarage_precision_mediocore(self):
        map_1 = mean_average_precision(self.system_mediocore_1, QUERIES, JUDGEMENTS, 4, 2)
        map_2 = mean_average_precision(self.system_mediocore_2, QUERIES, JUDGEMENTS, 4, 2)

        self.assertAlmostEqual(0.75, map_1)
        self.assertAlmostEqual(0.708333333, map_2)

    def test_mean_avarage_precision_bad(self):
        map_1 = mean_average_precision(self.system_bad, QUERIES, JUDGEMENTS, 4, 1)
        map_2 = mean_average_precision(self.system_bad, QUERIES, JUDGEMENTS, 2, 1)

        self.assertAlmostEqual(0.416666667, map_1)
        self.assertEqual(0, map_2)

    def test_mean_precision_perfect(self):
        mp = mean_precision(self.system_perfect, QUERIES, JUDGEMENTS, 2, 1)

        self.assertEqual(1, mp)

    def test_mean_precision_mediocore(self):
        mp_1 = mean_precision(self.system_mediocore_1, QUERIES, JUDGEMENTS, 2, 2)
        mp_2 = mean_precision(self.system_mediocore_2, QUERIES, JUDGEMENTS, 3, 2)

        self.assertAlmostEqual(0.5, mp_1)
        self.assertAlmostEqual(0.5, mp_2)

    def test_mean_precision_bad(self):
        mp_1 = mean_precision(self.system_bad, QUERIES, JUDGEMENTS, 3, 1)
        mp_2 = mean_precision(self.system_bad, QUERIES, JUDGEMENTS, 2, 1)

        self.assertAlmostEqual(0.3333333333, mp_1)
        self.assertEqual(0, mp_2)

    def test_mean_recall_perfect(self):
        mr = mean_recall(self.system_perfect, QUERIES, JUDGEMENTS, 4, 1)

        self.assertEqual(1, mr)

    def test_mean_recall_mediocore(self):
        mr_1 = mean_recall(self.system_mediocore_1, QUERIES, JUDGEMENTS, 3, 2)
        mr_2 = mean_recall(self.system_mediocore_2, QUERIES, JUDGEMENTS, 2, 2)

        self.assertAlmostEqual(0.5, mr_1)
        self.assertAlmostEqual(0.5, mr_2)

    def test_mean_recall_bad(self):
        mr = mean_recall(self.system_bad, QUERIES, JUDGEMENTS, 2, 1)

        self.assertEqual(0, mr)

    def test_ndcg_perfect(self):
        ndcg = normalized_discounted_cumulative_gain(self.system_perfect, QUERIES, JUDGEMENTS, 4, 1)

        self.assertAlmostEqual(1, ndcg)

    def test_ndcg_mediocore(self):
        ndcg_1 = normalized_discounted_cumulative_gain(self.system_mediocore_1, QUERIES, JUDGEMENTS, 4, 2)
        ndcg_2 = normalized_discounted_cumulative_gain(self.system_mediocore_2, QUERIES, JUDGEMENTS, 4, 2)

        self.assertAlmostEqual(0.877215315338, ndcg_1)
        self.assertAlmostEqual(0.7853208594, ndcg_2)

    def test_ndcg_bad(self):
        ndcg_1 = normalized_discounted_cumulative_gain(self.system_bad, QUERIES, JUDGEMENTS, 3, 1)
        ndcg_2 = normalized_discounted_cumulative_gain(self.system_bad, QUERIES, JUDGEMENTS, 2, 1)

        self.assertAlmostEqual(0.5, ndcg_1)
        self.assertEqual(0, ndcg_2)

    def test_mean_bpref_perfect(self):
        mbpref = mean_bpref(self.system_perfect, QUERIES, JUDGEMENTS, 4, 1)

        self.assertAlmostEqual(1, mbpref)

    def test_mean_bpref_mediocore(self):
        mbpref_1 = mean_bpref(self.system_mediocore_1, QUERIES, JUDGEMENTS, 4, 2)
        mbpref_2 = mean_bpref(self.system_mediocore_2, QUERIES, JUDGEMENTS, 4, 2)

        self.assertAlmostEqual(0.5, mbpref_1)
        self.assertAlmostEqual(0.5, mbpref_2)

    def test_mean_bpref_bad(self):
        mbpref_1 = mean_bpref(self.system_bad, QUERIES, JUDGEMENTS, 3, 1)
        mbpref_2 = mean_bpref(self.system_bad, QUERIES, JUDGEMENTS, 4, 1)

        self.assertAlmostEqual(0, mbpref_1)
        self.assertEqual(0, mbpref_2)
