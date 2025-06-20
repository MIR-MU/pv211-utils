"""The ensembles module provides functions for ensambling of IR systems.

Functions:
---------
inverse_mean_rank(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on inverse mean rank.
inverse_median_rank(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on inverse median rank.
reciprocal_rank_fusion(QueryBase, Iterable[IRSystemBase], int) -> Iterable[DocumentBase]:
    Ensembling function based on reciprocal rank fusion.
ibc(QueryBase, Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on variant of inverse median rank with tie braking.
weighted_ibc(QueryBase, Iterable[IRSystemBase], Iterable[float]) -> Iterable[DocumentBase]:
    Ensembling function based on variant of inverse weighted median rank with tie braking.
interleave(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    Ensembling function based on interleaving results from systems.

Classes:
-------
rbc:
    Interface for traning and using an ensembling technique, where regression model
    is used to estimate relevance of documents to queries.
"""
from .irsystem import IRSystemBase
from .entities import QueryBase, DocumentBase, JudgementBase

from typing import Iterable, Tuple, Optional, OrderedDict, Set, Any, List
from statistics import median, mean
from random import choices

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

Pipeline = Any


def _judgements_obj_to_id(old_judgements: Set[JudgementBase]) -> Set:
    new_judgements = set()
    for q, d in old_judgements:
        new_judgements.add((q.query_id, d.document_id))

    return new_judgements


def _weighted_median(elements: List[int], weights: List[float]) -> float:
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
    documents_ranks = dict()
    for system in systems:
        rank = 1
        num_documents = 0
        for document in system.search(query):
            if document not in documents_ranks:
                documents_ranks[document] = []

            documents_ranks[document].append(rank)
            rank += 1
            num_documents += 1

    return (documents_ranks, num_documents)


def _break_ties(ratings: list, num_documents: int,
                documents_scores: dict, weights: Optional[list] = None) -> list:
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

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by inverse mean rank.
    """
    documents_ranks, _ = _get_ranks(query, systems)

    return [doc for doc, _ in sorted(documents_ranks.items(),
                                     key=lambda item: 1 / mean(item[1]),
                                     reverse=True)]


def inverse_median_rank(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by their inverse median rank.

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by inverse median rank.
    """
    documents_ranks, _ = _get_ranks(query, systems)

    return [doc for doc, _ in sorted(documents_ranks.items(),
                                     key=lambda item: 1 / median(item[1]),
                                     reverse=True)]


def reciprocal_rank_fusion(query: QueryBase,
                           systems: Iterable[IRSystemBase], k: int) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents
    sorted by reciprocal rank fusion formula.

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.
    k : int
        Hyperparameter used in reciprocal rank fusion formula.

    Returns
    -------
    Iterable[DocumentBase]
        Documents returned by systems sorted by reciprocal rank fusion formula.
    """
    documents_ranks, _ = _get_ranks(query, systems)

    return [doc for doc, _ in sorted(documents_ranks.items(),
                                     key=lambda item: sum(map(lambda elem: 1 / (elem + k),
                                                              item[1])),
                                     reverse=True)]


def ibc(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by
    (num_documents - median_rank) / num_documents formula,
    where ties are broken by taking random ranking out of uniformly
    distributed ranks from given document's individual system's ranks.

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.

    Returns
    -------
    Iterable[DocumentBase]
        Sorted documents with ties broken.
    """
    documents_ranks, num_documents = _get_ranks(query, systems)

    # sort documents by inverse median rank
    ratings = sorted([(doc, (num_documents - median(ranks)) / num_documents)
                      for doc, ranks in documents_ranks.items()],
                     key=lambda item: item[1],
                     reverse=True)

    return _break_ties(ratings, num_documents, documents_ranks)


def weighted_ibc(query: QueryBase, systems: Iterable[IRSystemBase],
                 weights: List[float]) -> Iterable[DocumentBase]:
    """Ensemble systems and for given query return documents sorted by
    (num_documents - weighted_median_rank) / num_documents formula,
    where ties are broken by taking random ranking out of ranks from
    given document's individual system's ranks, where the distribution
    is given by weights parameter.

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of system to be ensembled.
    weights : Iterable[float]
        Weights of systems.

    Returns
    -------
    Iterable[DocumentBase]
        Sorted documents with ties broken.
    """
    documents_ranks, num_documents = _get_ranks(query, systems)

    # sort documents by inverse weighted median rank
    ratings = sorted([(doc, (num_documents - _weighted_median(ranks, weights)) / num_documents)
                      for doc, ranks in documents_ranks.items()],
                     key=lambda item: item[1],
                     reverse=True)

    return _break_ties(ratings, num_documents, documents_ranks, weights)


def interleave(query: QueryBase, systems: Iterable[IRSystemBase]) -> Iterable[DocumentBase]:
    """
    Ensemble systems and for a given query return documents interleaved in round-robin fashion.

    This method cycles through each system in order and yields one document from each at a time,
    preserving the system ordering.

    Arguments
    ---------
    query : QueryBase
        Query to be searched.
    systems : Iterable[IRSystemBase]
        List of systems to be interleaved.

    Returns
    -------
    Iterable[DocumentBase]
        Interleaved documents from all systems.
    """
    iterators = [iter(system.search(query)) for system in systems]
    exhausted = [False] * len(iterators)
    seen_doc_ids = set()

    while not all(exhausted):
        for i, it in enumerate(iterators):
            if exhausted[i]:
                continue

            try:
                doc = next(it)

                if doc.document_id not in seen_doc_ids:
                    seen_doc_ids.add(doc.document_id)
                    yield doc

            except StopIteration:
                exhausted[i] = True


class Rbc():
    """Class for rbc ensembling algorithm, where (by default) a linear regression model is trained to predict
    relevance of documents for given queries. This model is then used (in search method) to estimate documents'
    relevance for new queries.

    The training set is constructed from list of document score tuples and document judgement labels.
    The document score tuple consists of scores for each system calculated as (num_documets - rank) / num_documents.


    Methods:
    -------
    search(QueryBase) -> Iterable[DocumentBase]:
        Returns documents sorted by predicted relevance for given query.
    """

    def __init__(self, systems: Iterable[IRSystemBase], train_queries: OrderedDict,
                 train_judgements: Set[JudgementBase], pipeline: Optional[Pipeline] = None) -> None:
        """Construct the rbc object and fit the model.

        Arguments
        ---------
        systems : Iterable[IRSystemBase]
            List of system to be ensembled.
        train_queries : OrderedDict
            Queries used in training of the regression model.
        train_judgements : Set[JudgementBase]
            Judgements used in training of the regression model.
        pipeline : Optional[Pipeline], optional
            Pipeline to be fitted and used in relevance predictions.
            Defaults to linear regression with standard scaler.
        """
        self._systems = systems
        self._train_queries = train_queries
        self._train_judgements = _judgements_obj_to_id(train_judgements)
        self._pipeline = self._fit_model(pipeline)

    def _create_dataset(self, create_labels, queries: OrderedDict) -> Tuple[List[DocumentBase],
                                                                            List[List[float]],
                                                                            List[int]]:
        documents, X, Y = [], [], []
        # build the dataset of document scores given by systems, labeled by relevance judgement
        for query_id, query in queries.items():
            documents_ranks, num_documents = _get_ranks(query, self._systems)

            # calculate document scores from their ranks
            for doc, ranks in documents_ranks.items():
                documents.append(doc)
                document_scores = []

                for rank in ranks:
                    document_scores.append((num_documents - rank) / num_documents)

                # add list of document's scores given by systems to dataset
                X.append(document_scores)

                if create_labels:
                    # add 1/0 if relevant/irrelevant into dataset labels
                    Y.append(int((query_id, doc.document_id) in self._train_judgements))

        return documents, X, Y

    def _fit_model(self, pipeline):
        if pipeline is None:
            pipeline = make_pipeline(
                StandardScaler(copy=False),
                LinearRegression()
            )

        _, X, Y = self._create_dataset(create_labels=True,
                                       queries=self._train_queries)
        pipeline.fit(X, Y)

        return pipeline

    def search(self, query: QueryBase) -> Iterable[DocumentBase]:
        """Returns documents sorted by predicted relevance for given query.

        Arguments
        ---------
        query : QueryBase
            Query to be searched.

        Returns
        -------
        Iterable[DocumentBase]:
            Documents sorted by predicted relevance for given query.
        """
        documents, X, _ = self._create_dataset(create_labels=False,
                                               queries=OrderedDict({query.query_id: query}))
        scores = self._pipeline.predict(X)

        return [doc for doc, _ in sorted(zip(documents, scores),
                                         key=lambda item: item[1],
                                         reverse=True)]
