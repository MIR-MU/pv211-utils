from typing import Set, Optional

from ..eval import EvaluationBase
from .leaderboard import TrecLeaderboard
from .entities import TrecJudgementBase
from .irsystem import TrecIRSystemBase


class TrecEvaluation(EvaluationBase):
    """A Trec collection information retrieval system evaluation.

    Parameters
    ----------
    system : TrecIRSystemBase
        The information retrieval system.
    judgements : set of TrecJudgementBase
        Pairs of queries and relevant documents.
    leaderboard : TrecLeaderboard or None, optional
        A leaderboard to which we may later submit evaluation results.
        If None, then evaluation results will not be submitted. Default is None.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard.
        If None, then the result will not be submitted. Default is None.

    """
    def __init__(self, system: TrecIRSystemBase, judgements: Set[TrecJudgementBase],
                 leaderboard: Optional[TrecLeaderboard] = None,
                 author_name: Optional[str] = None):
        super().__init__(system, judgements, leaderboard, author_name)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0.1
