"""The evaluation_metrics module provides functions for evaluation of IR systems.

Functions:
---------
mean_avarage_precision(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean avarage precision of a system. 
mean_precision(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean precision of a system. 
mean_recall(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate mean recall of a system. 
normalized_discounted_cumulative_gain(IRSystemBase, OrderedDict, Set[JudgementBase], int, int) -> float:
    Calculate normalized discounted cumulative gain of a system. 
"""
from .entities import JudgementBase, QueryBase
from .irsystem import IRSystemBase

from typing import Set, OrderedDict
from multiprocessing import Pool, Manager
from multiprocessing.managers import ValueProxy
from functools import partial
from math import log2


def _judgements_obj_to_id(old_judgements: Set[JudgementBase]) -> Set:
    new_judgements = set()
    for q, d in old_judgements:
        new_judgements.add((q.query_id, d.document_id))

    return new_judgements

def _calc_recall(system: IRSystemBase, judgements: Set, k: int,
                 mr_score_lock, mr_score: ValueProxy, query: QueryBase) -> None:
    num_relevant = 0
    num_relevant_topk = 0
    current_rank = 1

    for document in system.search(query):
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            if current_rank <= k:
                num_relevant_topk += 1
        current_rank += 1

    recall = num_relevant_topk / num_relevant
 
    mr_score_lock.acquire()
    mr_score.value += recall 
    mr_score_lock.release()

def _calc_precision(system: IRSystemBase, judgements: Set, k: int,
                    mp_score_lock, mp_score: ValueProxy, query: QueryBase) -> None:
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
        
    mp_score_lock.acquire()
    mp_score.value += precision
    mp_score_lock.release()

def _calc_avarage_precision(system: IRSystemBase, judgements: Set, k: int,
                            map_score_lock, map_score: ValueProxy, query: QueryBase) -> None:
    num_relevant = 0
    avarage_precision = 0.0
    current_rank = 1

    for document in system.search(query):
        if current_rank > k:
            break
        if (query.query_id, document.document_id) in judgements:
            num_relevant += 1
            avarage_precision += num_relevant / current_rank
        current_rank += 1

    avarage_precision /= num_relevant if num_relevant > 0 else 1
    
    map_score_lock.acquire()
    map_score.value += avarage_precision
    map_score_lock.release()

def _calc_ndcg(system: IRSystemBase, judgements: Set, k: int,
               ndcg_score_lock, ndcg_score: ValueProxy, query: QueryBase) -> None:
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
     
    ndcg_score_lock.acquire()
    ndcg_score.value += dcg / idcg
    ndcg_score_lock.release()
    
def mean_avarage_precision(system: IRSystemBase, queries: OrderedDict,
                           judgements: Set[JudgementBase],
                           k: int, num_processes: int) -> float:
    """Evaluate system for given queries and judgements with mean avarage precision
    metric. Where first k documents will be used in evaluation.

    Args:
    ----
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

    Returns:
    -------
    float
        Mean avarage precision score from interval [0, 1]. 
    """
    manager = Manager() 
    map_score_lock = manager.Lock()
    map_score = manager.Value('f', 0.0)

    worker_avg_precision = partial(_calc_avarage_precision, system,
                                   _judgements_obj_to_id(judgements),
                                   k, map_score_lock, map_score)

    process_pool = Pool(processes=num_processes) 
    process_pool.map(worker_avg_precision, list(queries.values()))
    
    map_score.value /= len(queries)
    
    return map_score.value 

def mean_precision(system: IRSystemBase, queries: OrderedDict,
                   judgements: Set[JudgementBase], k: int, num_processes: int) -> float:
    """Evaluate system for given queries and judgements with mean precision metric.
    Where first k documents will be used in evaluation.

    Args:
    ----
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

    Returns:
    -------
    float
        Mean precision score from interval [0, 1]. 
    """
    manager = Manager() 
    mp_score_lock = manager.Lock()
    mp_score = manager.Value('f', 0.0)

    worker_precision = partial(_calc_precision, system,
                               _judgements_obj_to_id(judgements),
                               k, mp_score_lock, mp_score)

    process_pool = Pool(processes=num_processes) 
    process_pool.map(worker_precision, list(queries.values()))
    
    mp_score.value /= len(queries)
    
    return mp_score.value 

def mean_recall(system: IRSystemBase, queries: OrderedDict, 
                judgements: Set[JudgementBase], k: int, num_processes: int) -> float:
    """Evaluate system for given queries and judgements with mean recall metric.
    Where first k documents will be used in evaluation.

    Args:
    ----
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

    Returns:
    -------
    float
        Mean recall score from interval [0, 1]. 
    """
    manager = Manager() 
    mr_score_lock = manager.Lock()
    mr_score = manager.Value('f', 0.0)

    worker_recall = partial(_calc_recall, system,
                            _judgements_obj_to_id(judgements), 
                            k, mr_score_lock, mr_score)

    process_pool = Pool(processes=num_processes) 
    process_pool.map(worker_recall, list(queries.values()))
    
    mr_score.value /= len(queries)
    
    return mr_score.value 

def normalized_discounted_cumulative_gain(system: IRSystemBase,
                                          queries: OrderedDict,
                                          judgements: Set[JudgementBase],
                                          k: int, num_processes: int) -> float:
    """Evaluate system for given queries and judgements with normalized
    discounted cumulative gain metric. Where first k documents will be used in evaluation.

    Args:
    ----
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

    Returns:
    -------
    float
        Normalized discounted cumulative gain score from interval [0, 1]. 
    """
    manager = Manager() 
    ndcg_score_lock = manager.Lock()
    ndcg_score = manager.Value('f', 0.0)

    worker_ndcg = partial(_calc_ndcg, system,
                          _judgements_obj_to_id(judgements),
                          k, ndcg_score_lock, ndcg_score)

    process_pool = Pool(processes=num_processes) 
    process_pool.map(worker_ndcg, list(queries.values()))
    
    ndcg_score.value /= len(queries)
    
    return ndcg_score.value 