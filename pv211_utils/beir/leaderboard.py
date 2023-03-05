import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2023, 3, 22)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2023, 4, 30)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1LVCY6H2iaS05DDwON4YyZ2aWYnFCBYbnZqtpMdn7e6M'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vSnyvgqXDq3XPzGz3eLz_8JPwceou10HiEShI0wJ2A8vlosRZc1QhKZ10aOmmQFitv2yPAyBERD2wwx/pubhtml '
        )
