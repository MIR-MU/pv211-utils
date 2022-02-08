import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class CranfieldLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2022, 2, 8)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2022, 3, 14)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1TFE4RAx_kjaAkwhSRudel17kPunzD-C6BuNeZYzuzFk'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vT0FoFzCptIYKDsbcv8LebhZDe_20GFeBAPmS-VyImlWbqET0T7I2iWy59p9SHbUe3LX1yJMhALPcCY/pubhtml'
        )
