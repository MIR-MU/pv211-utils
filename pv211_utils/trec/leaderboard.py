import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class TrecLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2022, 2, 14)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2022, 5, 12)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1QD-qS18fR0Q137dw_j8k73KwewsmeJsiB4SSzaXhbPs'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vQPMjEwGPte34q6vT0CfT2NzmC6iDilpgG7s1cunr7eG5BY6T1OiHumbnwKrwrvQcj1e8-Pu96PiYc2/pubhtml'
        )
