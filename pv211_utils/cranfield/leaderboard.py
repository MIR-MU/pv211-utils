import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class CranfieldLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2024, 2, 19)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2024, 3, 19)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1K_GnmMTjeacPaUmvjO79abrlqOV8JqvnoxoQICulpAw'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vQga_qzgcLp_IcrOt5xZBq4Pq7jjTwmV6JLMRPwkLwG3K3dm2FrcZT-1GhGItFkNyAxwDaOzzFLOIdu/pubhtml'
        )
