import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2022, 3, 22)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2022, 5, 2)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1akHS9OSdN0_gu5xThJBSVAMKvUqAWg6sjO6vM6KCxfw'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vSF1I2TKhKqYc7kTxRfza__PTTQjrAtvezuQFm9I_lL3WsPSETE5yuxe8JyiN-7NvFjv4nZ8eCQ9aHg/pubhtml'
        )
