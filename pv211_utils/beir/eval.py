from typing import Set, Optional

from pv211_utils.eval import EvaluationBase
from .leaderboard import BeirLeaderboard
from .entities import BeirJudgementBase
from .irsystem import BeirIRSystemBase


class BeirEvaluation(EvaluationBase):
    """A Generic information retrieval system evaluation.

    Parameters
    ----------
    system : BeirIRSystemBase
        The information retrieval system.
    judgements : set of BeirJudgementBase
        Pairs of queries and relevant documents.
    leaderboard : BeirLeaderboard or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.
    num_workers : int or None, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is 1.

    """
    def __init__(self, system: BeirIRSystemBase, judgements: Set[BeirJudgementBase],
                 leaderboard: Optional[TrecLeaderboard] = None,
                 author_name: Optional[str] = None, num_workers: Optional[int] = 1):
        super().__init__(system, judgements, leaderboard, author_name, num_workers)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.1
