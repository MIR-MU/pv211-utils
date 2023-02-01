"""The ensembles module provides functions for ensambling of IR systems.

Functions:
---------
inverse_mean_rank(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]
    Ensembling function based on inverse mean rank.
inverse_median_rank(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on inverse median rank.
reciprocal_rank_fusion(QueryBase, Iterable[IRSystemBase], int) -> Iterable[DocumentBase]:
    Ensembling function based on reciprocal rank fusion.
ibc(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on variant of inverse median rank with tie braking.
weighted_ibc(QueryBase, Iterable[IRSystemBase], Iterable[float]) -> Iterable[DocumentBase]:
    Ensembling function based on variant of inverse weighted median rank with tie braking.
"""
from .irsystem import IRSystemBase
from .entities import QueryBase, DocumentBase

from typing import Iterable, Tuple, Optional
from statistics import median, mean
from random import choices


def _weighted_median(elements: list[int], weights: list[float]) -> float:
    total_wights_sum = sum(weights)
    cumulative_weights_sum = 0
    weighted_median = 0
    
    for i in range(len(weights)):
        cumulative_weights_sum += weights[i]

        if cumulative_weights_sum == total_wights_sum / 2 and i + 1 < len(elements):
            weighted_median = (elements[i] + elements[i + 1]) / 2
            break
            
        if cumulative_weights_sum > total_wights_sum / 2:
            weighted_median = elements[i]
            break
    
    return weighted_median 

def _get_ranks(query: QueryBase, systems: Iterable[IRSystemBase]) -> Tuple[dict, int]:
    documents_scores = dict()
    for system in systems:
        rank = 1
        num_documents = 0
        for document in system.search(query):
            if document not in documents_scores:
                documents_scores[document] = []

            documents_scores[document].append(rank)
            rank += 1
            num_documents += 1

    return (documents_scores, num_documents)

def _break_ties(ratings: list, num_documents: int,
                documents_scores: dict, weights : Optional[list] = None) -> list:
    final_ranking = []

    for start_i in range(len(ratings)):
        end_i = start_i + 1
        # find sequence of duplicates
        while end_i < len(ratings) and ratings[start_i][1] == ratings[end_i][1]:
            end_i += 1
        
        # if no duplicates found for current element
        if end_i == start_i + 1:
            final_ranking.append(ratings[start_i][0])
            continue
         
        tied_documents = dict()
        # calculate new rating from randomly chosen ranking from document's list of rankings
        for i in range(start_i, end_i):
            tied_documents[ratings[i][0]] = (num_documents - choices(documents_scores[ratings[i][0]],
                                                                     weights=weights)[0]) / num_documents
        
        final_ranking.extend([doc for doc, _ in sorted(tied_documents.items(),
                                                       key=lambda item: item[1],
                                                       reverse=True)]) 

    return final_ranking

def inverse_mean_rank(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by their inverse mean rank.

    Args:
    ----
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns:
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by inverse mean rank.
    """
    documents_scores, _ = _get_ranks(query, systems)
    
    return [doc for doc, _ in sorted(documents_scores.items(),
                                     key=lambda item: 1 / mean(item[1]),
                                     reverse=True)]

def inverse_median_rank(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by their inverse median rank.

    Args:
    ----
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns:
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by inverse median rank.
    """
    documents_scores, _ = _get_ranks(query, systems)
    
    return [doc for doc, _ in sorted(documents_scores.items(),
                                     key=lambda item: 1 / median(item[1]),
                                     reverse=True)]

def reciprocal_rank_fusion(query: QueryBase,
                           systems: Iterable[IRSystemBase], k: int) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents
    sorted by reciprocal rank fusion formula.

    Args:
    ----
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.
    k : int
        Hyperparameter used in reciprocal rank fusion formula.

    Returns:
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by reciprocal rank fusion formula.
    """
    documents_scores, _ = _get_ranks(query, systems)

    return [doc for doc, _ in sorted(documents_scores.items(),
                                     key=lambda item: sum(map(lambda elem: 1 / (elem + k),
                                                              item[1])),
                                     reverse=True)]
    
def ibc(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by 
    (num_documents - median_rank) / num_documents formula,
    where ties are broken by taking random ranking out of uniformly
    distributed ranks from given document's individual system's ranks.

    Args:
    ----
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns:
    -------
    Iterable[DocumentBase]
        Sorted documents with ties broken.
    """
    documents_scores, num_documents = _get_ranks(query, systems) 
    
    # sort documents by inverse median rank
    ratings = sorted([(doc, (num_documents - median(ranks)) / num_documents)
                      for doc, ranks in documents_scores.items()],
                     key=lambda item: item[1],
                     reverse=True)

    return _break_ties(ratings, num_documents, documents_scores) 
        

def weighted_ibc(query: QueryBase, systems: Iterable[IRSystemBase],
                 weights: list[float]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by
    (num_documents - weighted_median_rank) / num_documents formula,
    where ties are broken by taking random ranking out of ranks from
    given document's individual system's ranks, where the distribution
    is given by weights parameter.

    Args:
    ----
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.
    weights : Iterable[float]
        Weights of systems.

    Returns:
    -------
    Iterable[DocumentBase]
        Sorted documents with ties broken.
    """
    documents_scores, num_documents = _get_ranks(query, systems) 
    
    # sort documents by inverse weighted median rank
    ratings = sorted([(doc, (num_documents - _weighted_median(ranks, weights)) / num_documents) 
                      for doc, ranks in documents_scores.items()],
                     key=lambda item: item[1],
                     reverse=True)
        
    return _break_ties(ratings, num_documents, documents_scores, weights) 