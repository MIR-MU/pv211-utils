from typing import Set, Optional

from pv211_utils.eval import EvaluationBase
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
    num_workers : int or None, optional
        The number of processes used to compute the mean average precision.
        If None, all available CPUs will be used. Default is 1.

    """
    def __init__(self, system: BeirIRSystemBase, judgements: Set[BeirJudgementBase], num_workers: Optional[int] = 1):
        super().__init__(system, judgements, None, None, num_workers)

    def _get_minimum_mean_average_precision(self) -> float:
        return 0
