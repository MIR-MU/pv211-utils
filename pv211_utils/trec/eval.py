from typing import Set, Optional

from ..eval import EvaluationBase
from .leaderboard import TrecLeaderboard
from .entities import TrecJudgementBase
from .irsystem import TrecIRSystemBase


class TrecEvaluation(EvaluationBase):
    """A TREC collection information retrieval system evaluation.

    Parameters
    ----------
    system : TrecIRSystemBase
        The information retrieval system.
    judgements : set of TrecJudgementBase
        Pairs of queries and relevant documents.
    k : int, optional
        Parameter defining evaluation depth. Default is 10.
    leaderboard : TrecLeaderboard or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.
    num_workers : int, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is 1.

    """
    def __init__(self, system: TrecIRSystemBase, judgements: Set[TrecJudgementBase],
                 k: int = 10, leaderboard: Optional[TrecLeaderboard] = None,
                 author_name: Optional[str] = None, num_workers: int = 1):
        super().__init__(system, judgements, k, leaderboard, author_name, num_workers)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.135
