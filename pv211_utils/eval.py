import abc
from typing import Iterable, Set, Optional
from statistics import mean

from .entities import QueryBase, DocumentBase, JudgementBase
from .leaderboard import LeaderboardBase
from .irsystem import IRSystemBase

from IPython.display import display, Markdown


class EvaluationBase(abc.ABC):
    """An information retrieval system evaluation.

    Parameters
    ----------
    system : IRSystemBase
        The information retrieval system.
    judgements : set of JudgementsBase
        Pairs of queries and relevant documents.
    leaderboard : LeaderboardBase or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.

    Attributes
    ----------
    system : IRSystem
        The information retrieval system.
    judgements : JudgementsBase
        Pairs of queries and relevant documents.
    num_relevant : dict of (QueryBase, int)
        The number of relevant documents for queries.
    leaderboard : LeaderboardBase or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.

    """
    def __init__(self, system: IRSystemBase, judgements: Set[JudgementBase],
                 leaderboard: Optional[LeaderboardBase] = None, author_name: Optional[str] = None):
        num_relevant = {}
        for query, _ in judgements:
            if query not in num_relevant:
                num_relevant[query] = 0
            num_relevant[query] += 1

        self.system = system
        self.judgements = judgements
        self.num_relevant = num_relevant
        self.leaderboard = leaderboard
        self.author_name = author_name

    def _get_num_relevant(self, query: QueryBase) -> int:
        if query not in self.num_relevant:
            raise KeyError('No relevant documents for {} in self.judgements'.format(query))
        return self.num_relevant[query]

    def _average_precision(self, query: QueryBase, results: Iterable[DocumentBase]) -> float:
        """Average precision of ranked retrieval results for a query.

        Parameters
        ----------
        query : Query
            The query.
        results : list of DocumentBase
            Ranked retrieval results.

        Returns
        -------
        float
            Average precision of the ranked retrieval results with respect to the query.

        """
        num_relevant = 0
        precision = 0.0
        seen_documents = set()
        for document_number, document in enumerate(results):
            if document in seen_documents:
                continue
            seen_documents.add(document)
            if (query, document) in self.judgements:
                num_relevant += 1
                precision += float(num_relevant) / (document_number + 1)
        return precision / self._get_num_relevant(query)

    def mean_average_precision(self, queries: Iterable[QueryBase]) -> float:
        """The mean average precision of the information retrieval system.

        Parameters
        ----------
        queries : iterable of QueryBase
            Queries to be submitted to the information retrieval system.

        Returns
        -------
        float
            The mean average precision of the information retrieval system.

        """
        average_precisions = []
        for query in queries:
            results = self.system.search(query)
            precision = self._average_precision(query, results)
            average_precisions.append(precision)
        return mean(average_precisions)

    @abc.abstractmethod
    def _get_minimum_mean_average_precision(self) -> float:
        """Gets the minimum mean average precision required to pass the course project.

        Returns
        -------
        The minimum mean average precision required to pass the course project.

        """
        pass

    def evaluate(self, queries: Iterable[QueryBase], submit_result: bool = True) -> None:
        """Evaluates the information retrieval system and provides feedback.

        Parameters
        ----------
        queries : iterable of QueryBase
            Queries to be submitted to the information retrieval system.
        submit_result : bool, optional
            Whether the evaluation result should be submitted to the leaderboard.
            Default is True.

        """
        result = self.mean_average_precision(queries)
        map_score = result * 100.0
        minimum_map_score = self._get_minimum_mean_average_precision() * 100
        submit_result = submit_result and self.leaderboard is not None and self.author_name is not None
        leaderboard_url = self.leaderboard.get_public_url()
        if leaderboard_url is not None:
            leaderboard_text = '[the leaderboard]({})'.format(leaderboard_url)
        else:
            leaderboard_text = 'the leaderboard'
        competition_end = self.leaderboard.get_competition_end()

        display(Markdown('Your system achieved **{:.2f}% MAP score**.'.format(map_score)))

        if map_score < minimum_map_score:
            display(Markdown('You need at least **{:g}%** to pass. 😢'.format(minimum_map_score)))
            display(Markdown('Try playing with the preprocessing of queries and documents! 💡'))
        else:
            display(Markdown('Congratulations, you passed the **{:g}%** minimum! 🥳'.format(minimum_map_score)))

        if submit_result:
            self.leaderboard.log_precision_entry(self.author_name, result)
            display(Markdown('Your result has been submitted to {}! 🏆'.format(leaderboard_text)))
        else:
            message = (
                'Set `submit_result = True` and write your name to the `author_name` variable '
                'to submit your result to {}. 🏆\n\nThe best submissions on the '
                'leaderboard will receive *small awards during the semester*, and some '
                '*__seriously big__ awards* after the personal check at the end of the competition '
                '({}). Please be polite, do not spoil the game for the others, and **have fun!** 😉'
            ).format(leaderboard_text, competition_end)
            display(Markdown(message))
