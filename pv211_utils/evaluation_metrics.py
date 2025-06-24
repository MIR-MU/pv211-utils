"""The evaluation_metrics module provides functions for evaluation of IR systems.

Functions:
---------
mean_average_precision(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean average precision of a system.
mean_precision(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean precision of a system.
mean_recall(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean recall of a system.
normalized_discounted_cumulative_gain(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate normalized discounted cumulative gain of a system.
bpref(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean bpref score of a system.
"""

from .entities import JudgementBase, QueryBase
from .irsystem import IRSystemBase

from typing import Set, OrderedDict
from multiprocessing import Pool, get_context
from functools import partial
from math import log2
import abc


def _judgements_obj_to_id(old_judgements: Set[JudgementBase]) -> Set:
    new_judgements = set()
    for q, d in old_judgements:
        new_judgements.add((q.query_id, d.document_id))

    return new_judgements


def _calc_recall(
    system: IRSystemBase, judgements: Set, k: int, query: QueryBase
) -> float:
    num_relevant = 0
    num_relevant_topk = 0
    current_rank = 1

    for document in system.search(query):
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            if current_rank <= k:
                num_relevant_topk += 1
        current_rank += 1

    if num_relevant > 0:
        recall = num_relevant_topk / num_relevant
    else:
        recall = 1

    return recall


def _calc_precision(
    system: IRSystemBase, judgements: Set, k: int, query: QueryBase
) -> float:
    num_relevant = 0
    precision = 0.0
    current_rank = 1

    for document in system.search(query):
        if current_rank > k:
            break
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
        current_rank += 1

    precision = num_relevant / k

    return precision


def _calc_average_precision(
    system: IRSystemBase, judgements: Set, k: int, query: QueryBase
) -> float:
    num_relevant = 0
    average_precision = 0.0
    current_rank = 1

    for document in system.search(query):
        if current_rank > k:
            break
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            average_precision += num_relevant / current_rank
        current_rank += 1

    average_precision /= num_relevant if num_relevant > 0 else 1

    return average_precision


class calc_map(abc.ABC):
    system = None
    judgements = None
    k = None
    _CURRENT_INSTANCE = None

    @classmethod
    def _calc_average_precision(csl, query: QueryBase) -> float:
        num_relevant = 0
        average_precision = 0.0
        current_rank = 1

        for document in csl._CURRENT_INSTANCE.system.search(query):
            if current_rank > csl._CURRENT_INSTANCE.k:
                break
            if (
                query.query_id,
                document.document_id,
            ) in csl._CURRENT_INSTANCE.judgements:
                num_relevant += 1
                average_precision += num_relevant / current_rank
            current_rank += 1

        average_precision /= num_relevant if num_relevant > 0 else 1

        return average_precision

    def mean_average_precision(
        self,
        system: IRSystemBase,
        queries: OrderedDict,
        judgements: Set[JudgementBase],
        k: int,
        num_processes: int,
    ) -> float:
        """Evaluate system for given queries and judgements with mean average precision
        metric. Where first k documents will be used in evaluation.

        Arguments
        ---------
        system : IRSystemBase
            System to be evaluated.
        queries : OrderedDict
            Queries to be searched.
        judgements : Set[JudgementBase]
            Judgements.
        k : int
            Parameter defining evaluation depth.
        num_processes : int
            Parallelization parameter defining number of processes to be used to run the evaluation.

        Returns
        -------
        float
            Mean average precision score from interval [0, 1].
        """
        map_score = 0.0

        self.system = system
        self.judgements = _judgements_obj_to_id(judgements)
        self.k = k
        self.__class__._CURRENT_INSTANCE = self

        if num_processes == 1:
            for query in list(queries.values()):
                map_score += self.__class__._calc_average_precision(query)
        else:
            with get_context("fork").Pool(processes=num_processes) as process_pool:
                for precision in process_pool.imap(
                    self.__class__._calc_average_precision, list(queries.values())
                ):
                    map_score += precision

        map_score /= len(queries)
        self.__class__._CURRENT_INSTANCE = None
        return map_score


def _calc_ndcg(
    system: IRSystemBase, judgements: Set, k: int, query: QueryBase
) -> float:
    num_relevant = 0
    dcg = 0.0
    current_rank = 1

    for document in system.search(query):
        if current_rank > k:
            break
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            dcg += 1 / log2(current_rank + 1)
        current_rank += 1

    # max to avoid division by 0
    idcg = max(sum([1 / log2(i + 1) for i in range(1, num_relevant + 1)]), 1)

    return dcg / idcg


def _calc_bpref(
    system: IRSystemBase, judgements: Set, k: int, query: QueryBase
) -> float:
    num_relevant = 0
    relevant_doc_ranks = []
    current_rank = 1
    bpref = 0.0

    for document in system.search(query):
        if current_rank > k:
            break
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            relevant_doc_ranks.append(current_rank)
        current_rank += 1

    for i, rank in enumerate(relevant_doc_ranks, start=1):
        bpref += 1 - min(rank - i, num_relevant) / num_relevant

    return (bpref / num_relevant) if num_relevant > 0 else 0


def mean_average_precision(
    system: IRSystemBase,
    queries: OrderedDict,
    judgements: Set[JudgementBase],
    k: int,
    num_processes: int,
) -> float:
    """Evaluate system for given queries and judgements with mean average precision
    metric. Where first k documents will be used in evaluation.

    Arguments
    ---------
    system : IRSystemBase
        System to be evaluated.
    queries : OrderedDict
        Queries to be searched.
    judgements : Set[JudgementBase]
        Judgements.
    k : int
        Parameter defining evaluation depth.
    num_processes : int
        Parallelization parameter defining number of processes to be used to run the evaluation.

    Returns
    -------
    float
        Mean average precision score from interval [0, 1].
    """
    map_score = 0.0

    if num_processes == 1:
        for query in list(queries.values()):
            map_score += _calc_average_precision(
                system, _judgements_obj_to_id(judgements), k, query
            )
    else:
        worker_avg_precision = partial(
            _calc_average_precision, system, _judgements_obj_to_id(judgements), k
        )

        with get_context("fork").Pool(processes=num_processes) as process_pool:
            for precision in process_pool.imap(
                worker_avg_precision, list(queries.values())
            ):
                map_score += precision

    map_score /= len(queries)

    return map_score


def mean_precision(
    system: IRSystemBase,
    queries: OrderedDict,
    judgements: Set[JudgementBase],
    k: int,
    num_processes: int,
) -> float:
    """Evaluate system for given queries and judgements with mean precision metric.
    Where first k documents will be used in evaluation.

    Arguments
    ---------
    system : IRSystemBase
        System to be evaluated.
    queries : OrderedDict
        Queries to be searched.
    judgements : Set[JudgementBase]
        Judgements.
    k : int
        Parameter defining evaluation depth.
    num_processes : int
        Parallelization parameter defining number of processes to be used to run the evaluation.

    Returns
    -------
    float
        Mean precision score from interval [0, 1].
    """
    mp_score = 0

    if num_processes == 1:
        for query in list(queries.values()):
            mp_score += _calc_precision(
                system, _judgements_obj_to_id(judgements), k, query
            )
    else:
        worker_precision = partial(
            _calc_precision, system, _judgements_obj_to_id(judgements), k
        )

        with Pool(processes=num_processes) as process_pool:
            for precision in process_pool.imap(
                worker_precision, list(queries.values())
            ):
                mp_score += precision

    return mp_score / len(queries)


def mean_recall(
    system: IRSystemBase,
    queries: OrderedDict,
    judgements: Set[JudgementBase],
    k: int,
    num_processes: int,
) -> float:
    """Evaluate system for given queries and judgements with mean recall metric.
    Where first k documents will be used in evaluation.

    Arguments
    ---------
    system : IRSystemBase
        System to be evaluated.
    queries : OrderedDict
        Queries to be searched.
    judgements : Set[JudgementBase]
        Judgements.
    k : int
        Parameter defining evaluation depth.
    num_processes : int
        Parallelization parameter defining number of processes to be used to run the evaluation.

    Returns
    -------
    float
        Mean recall score from interval [0, 1].
    """
    mr_score = 0
    if num_processes == 1:
        for query in list(queries.values()):
            mr_score += _calc_recall(
                system, _judgements_obj_to_id(judgements), k, query
            )
    else:
        worker_recall = partial(
            _calc_recall, system, _judgements_obj_to_id(judgements), k
        )

        with Pool(processes=num_processes) as process_pool:
            for recall in process_pool.imap(worker_recall, list(queries.values())):
                mr_score += recall

    return mr_score / len(queries)


def normalized_discounted_cumulative_gain(
    system: IRSystemBase,
    queries: OrderedDict,
    judgements: Set[JudgementBase],
    k: int,
    num_processes: int,
) -> float:
    """Evaluate system for given queries and judgements with normalized
    discounted cumulative gain metric. Where first k documents will be used in evaluation.

    Arguments
    ---------
    system : IRSystemBase
        System to be evaluated.
    queries : OrderedDict
        Queries to be searched.
    judgements : Set[JudgementBase]
        Judgements.
    k : int
        Parameter defining evaluation depth.
    num_processes : int
        Parallelization parameter defining number of processes to be used to run the evaluation.

    Returns
    -------
    float
        Normalized discounted cumulative gain score from interval [0, 1].
    """
    ndcg_score = 0

    if num_processes == 1:
        for query in list(queries.values()):
            ndcg_score += _calc_ndcg(
                system, _judgements_obj_to_id(judgements), k, query
            )
    else:
        worker_ndcg = partial(_calc_ndcg, system, _judgements_obj_to_id(judgements), k)

        with Pool(processes=num_processes) as process_pool:
            for dcg in process_pool.imap(worker_ndcg, list(queries.values())):
                ndcg_score += dcg

    return ndcg_score / len(queries)


def mean_bpref(
    system: IRSystemBase,
    queries: OrderedDict,
    judgements: Set[JudgementBase],
    k: int,
    num_processes: int,
) -> float:
    """Evaluate system for given queries and judgements with bpref metric.
    Where first k documents will be used in evaluation.

    Notes
    -----
    Since bpref differentiates between unjudged and irrelevant documents,
    this class only computes bpref for datasets with complete relevant judgements
    that cover exhaustively all pairs of queries and documents. At the time of writing,
    this is only true of the Cranfield dataset. This can only be remediated by changing
    the JudgementBase class to differentiate between unjudged and irrelevant
    documents.

    Arguments
    ---------
    system : IRSystemBase
        System to be evaluated.
    queries : OrderedDict
        Queries to be searched.
    judgements : Set[JudgementBase]
        Judgements.
    k : int
        Parameter defining evaluation depth.
    num_processes : int
        Parallelization parameter defining number of processes to be used to run the evaluation.

    Returns
    -------
    float
        Bpref score from interval [0, 1].
    """
    bpref_score = 0
    if num_processes == 1:
        for query in list(queries.values()):
            bpref_score += _calc_bpref(
                system, _judgements_obj_to_id(judgements), k, query
            )
    else:
        worker_bpref = partial(
            _calc_bpref, system, _judgements_obj_to_id(judgements), k
        )

        with Pool(processes=num_processes) as process_pool:
            for bpref in process_pool.imap(worker_bpref, list(queries.values())):
                bpref_score += bpref

    return bpref_score / len(queries)
