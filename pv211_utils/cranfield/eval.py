from typing import Set, Optional

from ..eval import EvaluationBase
from .leaderboard import CranfieldLeaderboard
from .entities import CranfieldJudgementBase
from .irsystem import CranfieldIRSystemBase


class CranfieldEvaluation(EvaluationBase):
    """A Cranfield collection information retrieval system evaluation.

    Parameters
    ----------
    system : CranfieldIRSystemBase
        The information retrieval system.
    judgements : set of CranfieldJudgementBase
        Pairs of queries and relevant documents.
    leaderboard : CranfieldLeaderboard or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.

    """
    def __init__(self, system: CranfieldIRSystemBase, judgements: Set[CranfieldJudgementBase],
                 leaderboard: Optional[CranfieldLeaderboard] = None,
                 author_name: Optional[str] = None):
        super().__init__(system, judgements, leaderboard, author_name)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.22
