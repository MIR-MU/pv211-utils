from typing import Iterable, Tuple, Set, Optional

from ..eval import mean_average_precision
from .leaderboard import CranfieldLeaderboard
from .entities import CranfieldQueryBase, CranfieldDocumentBase
from .irsystem import CranfieldIRSystemBase

from IPython.display import display, Markdown


MINIMUM_MAP_SCORE = 35.0
LEADERBOARD_URL = (
    'https://docs.google.com/spreadsheets/d/e/'
    '2PACX-1vRRR4eDkQIWx5FSU08Uj5DciWwxNfHJeLruNR1T0WW9xmSsYl457Zqv5SlA1jfvsYHpsaUw_8P3z1OF/pubhtml'
)


def evaluate(system: CranfieldIRSystemBase,
             queries: Iterable[CranfieldQueryBase],
             judgements: Set[Tuple[CranfieldQueryBase, CranfieldDocumentBase]],
             leaderboard: Optional[CranfieldLeaderboard] = None,
             submit_result: bool = True,
             author_name: Optional[str] = None) -> None:
    """Evaluates an information retrieval system.

    Parameters
    ----------
    system : CranfieldIRSystem
        The information retrieval system.
    queries : iterable of CranfieldQueryBase
        All queries to be submitted to the information retrieval system.
    judgements : set of tuple of (CranfieldQueryBase, CranfieldDocumentBase)
        Pairs of queries and relevant documents.
    leaderboard : CranfieldLoaderboard or None, optional
        A leaderboard to which we may submit the evaluation result.
        If None, then the result will not be submitted. Default is None.
    submit_result : bool, optional
        Whether the evaluation result should be submitted to the leaderboard.
        Default is True.
    author_name : str or None, optional
        The name of the author submitted to the leaderboard when `submit_result` is True.
        If None, then the result will not be submitted. Default is None.

    """

    result = mean_average_precision(system, queries, judgements)
    map_score = result * 100.0
    submit_result = leaderboard is not None and submit_result and author_name is not None

    display(Markdown('Your system achieved **{:.2f}% MAP score**.'.format(map_score)))

    if map_score < MINIMUM_MAP_SCORE:
        display(Markdown('You need at least **{:g}%** to pass. 😢'.format(MINIMUM_MAP_SCORE)))
        display(Markdown('Try playing with the preprocessing of queries and documents! 💡'))
    else:
        display(Markdown('Congratulations, you passed the **{:g}%** minimum! 🥳'.format(MINIMUM_MAP_SCORE)))
        if not submit_result:
            message = (
                'Set `submit_result = True` and write your name to the `author_name` variable '
                'to submit your result to [the leaderboard]({}). 🏆\n\nThe best submissions on the '
                'leaderboard will receive *small awards during the semester*, and some '
                '*__seriously big__ awards* after the personal check at the end of the competition '
                'the 18th of April). Please be polite, do not spoil the game for the others, '
                'and **have fun!** 😉'
            ).format(LEADERBOARD_URL)
            display(Markdown(message))

    if submit_result:
        leaderboard.log_precision_entry(author_name, result)
        display(Markdown('Submitted your result to [the leaderboard]({})! 🏆'.format(LEADERBOARD_URL)))
