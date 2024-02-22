import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2024, 3, 27)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2024, 5, 7)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1z59ROLx-0AS-Wd6ppmOrXKmx7gZG2SM4KdFgfiwoFPI'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vRc5VbtwD2YUdfTlICSlYwcS8ZjNqkHVJrKgQ2pVBNmUi'
            'Li9lUkTrYde9Mu6fxJTa07LN4VZ2oTs5jZ/pubhtml'
        )
