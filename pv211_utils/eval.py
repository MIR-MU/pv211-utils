import abc
from datetime import datetime
from typing import Set, Optional, OrderedDict
import os

from .entities import QueryBase, JudgementBase
from .leaderboard import LeaderboardBase
from .irsystem import IRSystemBase
from .evaluation_metrics import mean_average_precision

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
    k : int, optional
        Parameter defining evaluation depth. Default is 10.


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
    k : int, optional
        Parameter defining evaluation depth. Default is 10.

    """
    _CURRENT_INSTANCE: Optional['EvaluationBase'] = None  # used for sharing state between processes

    def __init__(self, system: IRSystemBase, judgements: Set[JudgementBase],
                 leaderboard: Optional[LeaderboardBase] = None, author_name: Optional[str] = None,
                 num_workers: Optional[int] = 1, k: Optional[int] = 10):
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
        self.k = k

    def _get_num_relevant(self, query: QueryBase) -> int:
        return self.num_relevant[query] if query in self.num_relevant else 0

    @abc.abstractmethod
    def _get_minimum_mean_average_precision(self) -> float:
        """Gets the minimum mean average precision required to pass the course project.

        Returns
        -------
        The minimum mean average precision required to pass the course project.

        """
        pass

    def evaluate(self, queries: OrderedDict, submit_result: bool = True) -> None:
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
        result = mean_average_precision(self.system, queries, self.judgements, self.k, self.num_workers)
        time_after = datetime.now()
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

        duration = time_after - time_before

        cpu_count = os.cpu_count()
        cpu_count = cpu_count if cpu_count is not None else 1

        if duration.total_seconds() > 900 and self.num_workers == 1 and cpu_count > 1:
            message = (
                'The evaluation is taking a while! ⌚  Put your {} CPUs to use and speed up the '
                'evaluation by passing the `num_workers={}` parameter to `{}`.'
            ).format(cpu_count, cpu_count, self.__class__.__name__)
            display(Markdown(message))
