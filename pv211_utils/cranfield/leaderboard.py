import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class CranfieldLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2025, 2, 17)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2025, 3, 26)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1LGm715BA85FMQDbO4inZu1s1Ey93HLkDCFXUYGKjrpA'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vSLY-jk70GJZSZjJYMKxh6CMBl47KDP6OFjrY_zIMUF9YRwTLl_DSU1mXCrBPiHyUxqav0URYtVP2PK/pubhtml'
        )
