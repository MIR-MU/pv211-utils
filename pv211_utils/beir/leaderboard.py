import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2023, 3, 22)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2023, 5, 1)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1YC0A9-XCd7p18rE37RI8edTOGeSlsAtQWnaPiS8GPOw'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSLYKoYcsTgyTp2T'
            '-pNgW2heZrwvmBVKAgWAAG_vELv8kgnxHffnJ-IKt5huAacvO7r-zKWOgSiqWFU/pubhtml?gid=0&single=true'
        )
