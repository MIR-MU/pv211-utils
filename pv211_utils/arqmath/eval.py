from typing import Set, Optional

from ..eval import EvaluationBase
from .leaderboard import ArqmathLeaderboard
from .entities import ArqmathJudgementBase
from .irsystem import ArqmathIRSystemBase


class ArqmathEvaluation(EvaluationBase):
    """An information retrieval system evaluation for the answer retrieval task of ARQMath 2020.

    Parameters
    ----------
    system : ARQMathIRSystemBase
        The information retrieval system.
    judgements : set of ArqmathJudgementBase
        Pairs of queries and relevant documents.
    k : int, optional
        Parameter defining evaluation depth. Default is 10.
    leaderboard : ArqmathLeaderboard or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.
    num_workers : int, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is 1.
    """

    def __init__(self, system: ArqmathIRSystemBase, judgements: Set[ArqmathJudgementBase],
                 k: int = 10, leaderboard: Optional[ArqmathLeaderboard] = None,
                 author_name: Optional[str] = None, num_workers: int = 1):
        super().__init__(system, judgements, k, leaderboard, author_name, num_workers)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.1
