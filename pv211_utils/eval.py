from typing import Iterable, Tuple, Set
from statistics import mean

from .entities import QueryBase, DocumentBase
from .irsystem import IRSystemBase


def average_precision(query: QueryBase,
                      results: Iterable[DocumentBase],
                      judgements: Set[Tuple[QueryBase, DocumentBase]],
                      num_relevant: int) -> float:
    """Average precision of ranked retrieval results for a query.

    Parameters
    ----------
    query : Query
        The query.
    results : list of DocumentBase
        Ranked retrieval results.
    judgements: set of tuple of (QueryBase, DocumentBase)
        Pairs of queries and relevant documents.
    num_relevant: int
        Number of relevant documents.

    Returns
    -------
    float
        Average precision of the ranked retrieval results with respect to the query.

    """
    result_relevances = []
    precisions = []
    seen_documents = set()
    for document in results:
        if document in seen_documents:
            continue
        else:
            seen_documents.add(document)
        result_relevance = (query, document) in judgements
        result_relevances.append(float(result_relevance))
        if result_relevance:
            precisions.append(mean(result_relevances))
    return float(sum(precisions) / num_relevant)


def mean_average_precision(system: IRSystemBase,
                           queries: Iterable[QueryBase],
                           judgements: Set[Tuple[QueryBase, DocumentBase]]) -> float:
    """The mean average precision of an information retrieval system.

    Parameters
    ----------
    system : IRSystem
        The information retrieval system.
    queries : iterable of QueryBase
        All queries to be submitted to the information retrieval system.
    judgements : set of tuple of (QueryBase, DocumentBase)
        Pairs of queries and relevant documents.

    Returns
    -------
    float
        The mean average precision of the information retrieval system.

    """
    num_relevant = {}
    for query, _ in judgements:
        if query not in num_relevant:
            num_relevant[query] = 0
        num_relevant[query] += 1

    average_precisions = []
    for query in queries:
        results = system.search(query)
        precision = average_precision(query, results, judgements, num_relevant[query])
        average_precisions.append(precision)
    result = float(mean(average_precisions))

    return result
