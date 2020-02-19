from typing import Iterable, Dict, Tuple, Set

from numpy import mean, sum
from pv211_utils.entities import QueryBase, DocumentBase

from pv211_utils.irsystem import IRSystem
from pv211_utils import loader


def average_precision(query: QueryBase, results: Iterable[DocumentBase],
                      relevant: Set[Tuple[QueryBase, DocumentBase]], num_relevant: Dict[QueryBase, int]) -> float:
    """Average precision of ranked retrieval results for a query.

    Parameters
    ----------
    query : Query
        The query.
    results : list of Documents
        Ranked retrieval results.
    relevant: list of relevant Documents
    num_relevant: number of relevant Documents

    Returns
    -------
    float
        Average precision of ranked retrieval results for the query.

    """
    result_relevances = []
    precisions = []
    for document in results:
        result_relevance = (query, document) in relevant
        result_relevances.append(float(result_relevance))
        if result_relevance:
            precisions.append(mean(result_relevances))
    return sum(precisions) / num_relevant[query]


def mean_average_precision(ir_system_instance: IRSystem, submit_result=True, author_name: str = None) -> float:
    """Mean average precision of the information retrieval system.

    Returns
    -------
    float
        Mean average precision of the information retrieval system.
    """
    queries = loader.load_queries()
    documents = loader.load_documents()
    relevant = loader.load_judgements(queries, documents)

    num_relevant = {}
    for query, _ in relevant:
        if query not in num_relevant:
            num_relevant[query] = 0
        num_relevant[query] += 1

    average_precisions = []
    for query in queries.values():
        results = ir_system_instance.search(query)
        average_precisions.append(average_precision(query, results, relevant, num_relevant))
    result = float(mean(average_precisions))
    print(f'Mean average precision: {result* 100:.3f}% ')

    if submit_result:
        from pv211_utils.gdrive_upload import log_precision_entry
        log_precision_entry(author_name, result)
        # TODO: provide some more info
        print("Submitted!")
    else:
        print("Not submitted.")
