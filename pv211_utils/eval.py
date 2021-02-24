from typing import Iterable, Tuple, Set, Optional
from statistics import mean

from .leaderboard import LeaderboardBase
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
                           judgements: Set[Tuple[QueryBase, DocumentBase]],
                           leaderboard: Optional[LeaderboardBase] = None,
                           submit_result: bool = True,
                           author_name: Optional[str] = None) -> float:
    """The mean average precision of an information retrieval system.

    Parameters
    ----------
    system : IRSystem
        The information retrieval system.
    queries : sequence of QueryBase
        All queries to be submitted to the information retrieval system.
    judgements : set of tuple of (QueryBase, DocumentBase)
        Pairs of queries and relevant documents.
    leaderboard : LoaderboardBase or None, optional
        A leaderboard to which we may submit the mean average precision.
        If None, then the mean average precision will not be submitted.
        Default is None.
    submit_result : bool, optional
        Whether the mean average precision should be submitted to the leaderboard.
        Default is True.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard when `submit_result` is True.
        If None, then the mean average precision will not be submitted. Default is None.

    Returns
    -------
    float
        Mean average precision of the information retrieval system.

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

    submit_result = leaderboard is not None and submit_result and author_name is not None
    if submit_result:
        leaderboard.log_precision_entry(author_name, result)

    return result
