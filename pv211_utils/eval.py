import abc
from datetime import datetime
from multiprocessing import get_context
from typing import Iterable, Set, Optional
from statistics import mean
import os

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
    num_workers : int or None, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is 1.

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
    num_workers : int or None, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is None.

    """
    _CURRENT_INSTANCE: Optional['EvaluationBase'] = None  # used for sharing state between processes

    def __init__(self, system: IRSystemBase, judgements: Set[JudgementBase],
                 leaderboard: Optional[LeaderboardBase] = None, author_name: Optional[str] = None,
                 num_workers: Optional[int] = 1):
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
        self.num_workers = num_workers

    def _get_num_relevant(self, query: QueryBase) -> int:
        return self.num_relevant[query] if query in self.num_relevant else 0

    def _average_precision(self, query: QueryBase, results: Iterable[DocumentBase]) -> Optional[float]:
        """Average precision of ranked retrieval results for a query.

        Parameters
        ----------
        query : Query
            The query.
        results : list of DocumentBase
            Ranked retrieval results.

        Returns
        -------
        float or None
            Average precision of the ranked retrieval results with respect to the query.
            If no relevance judgements exist for a query, returns None.

        """
        num_relevant = self._get_num_relevant(query)
        if num_relevant == 0:
            return None

        num_retrieved_relevant = 0
        precision = 0.0
        seen_documents = set()
        for document_number, document in enumerate(results):
            if document in seen_documents:
                continue
            seen_documents.add(document)
            if (query, document) in self.judgements:
                num_retrieved_relevant += 1
                precision += float(num_retrieved_relevant) / (document_number + 1)
        return precision / num_relevant

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
        self.__class__._CURRENT_INSTANCE = self
        if self.num_workers == 1:
            result = self.__class__._mean_average_precision_single_process(queries)
        else:
            result = self.__class__._mean_average_precision_multi_process(queries)
        self.__class__._CURRENT_INSTANCE = None
        return result

    @classmethod
    def _mean_average_precision_single_process(cls, queries: Iterable[QueryBase]) -> float:
        average_precisions = []
        for query in queries:
            precision = cls._CURRENT_INSTANCE._average_precision_worker(query)
            if precision is not None:
                average_precisions.append(precision)
        if not average_precisions:
            raise KeyError('None of the queries has any judgements')
        result = mean(average_precisions)
        return result

    @classmethod
    def _mean_average_precision_multi_process(cls, queries: Iterable[QueryBase]) -> float:
        average_precisions = []
        with get_context('fork').Pool(cls._CURRENT_INSTANCE.num_workers) as pool:
            for precision in pool.imap(cls._CURRENT_INSTANCE._average_precision_worker, queries):
                if precision is not None:
                    average_precisions.append(precision)
        if not average_precisions:
            raise KeyError('None of the queries has any judgements')
        result = mean(average_precisions)
        return result

    @classmethod
    def _average_precision_worker(cls, query: QueryBase) -> Optional[float]:
        results = cls._CURRENT_INSTANCE.system.search(query)
        precision = cls._CURRENT_INSTANCE._average_precision(query, results)
        return precision

    @abc.abstractmethod
    def _get_minimum_mean_average_precision(self) -> Optional[float]:
        """Gets the minimum mean average precision required to pass the course project.
        If minimum MAP == 0, then the evaluation will just display the achieved MAP score.

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
        time_before = datetime.now()
        result = self.mean_average_precision(queries)
        time_after = datetime.now()
        map_score = result * 100.0

        minimum_map_score = self._get_minimum_mean_average_precision() * 100
        submit_result = submit_result and self.leaderboard is not None and self.author_name is not None
        if self.leaderboard is None:
            leaderboard_url = None
            competition_end = None

        else:
            leaderboard_url = self.leaderboard.get_public_url()
            competition_end = self.leaderboard.get_competition_end()

        if leaderboard_url is not None:
            leaderboard_text = '[the leaderboard]({})'.format(leaderboard_url)
        else:
            leaderboard_text = 'the leaderboard'

        display(Markdown('Your system achieved **{:.2f}% MAP score**.'.format(map_score)))

        if minimum_map_score == 0:
            pass
        elif map_score < minimum_map_score:
            display(Markdown('You need at least **{:g}%** to pass. 😢'.format(minimum_map_score)))
            display(Markdown('Try playing with the preprocessing of queries and documents! 💡'))
        else:
            display(Markdown('Congratulations, you passed the **{:g}%** minimum! 🥳'.format(minimum_map_score)))

        if submit_result and self.leaderboard is not None:
            self.leaderboard.log_precision_entry(self.author_name, result)
            display(Markdown('Your result has been submitted to {}! 🏆'.format(leaderboard_text)))
        elif not submit_result and self.leaderboard is None:
            pass
        else:
            message = (
                'Set `submit_result = True` and write your name to the `author_name` variable '
                'to submit your result to {}. 🏆\n\nThe best submissions on the '
                'leaderboard will receive *small awards during the semester*, and some '
                '*__seriously big__ awards* after the personal check at the end of the competition '
                '({}). Please be polite, do not spoil the game for the others, and **have fun!** 😉'
            ).format(leaderboard_text, competition_end)
            display(Markdown(message))

        duration = time_after - time_before

        cpu_count = os.cpu_count()
        cpu_count = cpu_count if cpu_count is not None else 1

        if duration.total_seconds() > 900 and self.num_workers == 1 and cpu_count > 1:
            message = (
                'The evaluation is taking a while! ⌚  Put your {} CPUs to use and speed up the '
                'evaluation by passing the `num_workers={}` parameter to `{}`.'
            ).format(cpu_count, cpu_count, self.__class__.__name__)
            display(Markdown(message))
