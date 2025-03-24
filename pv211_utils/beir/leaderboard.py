import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2025, 3, 26)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2025, 5, 7)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1WSSqb42JliidyguSAyk0uzXkX1h5S-273yvms83My0Y'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vQZXQfKXkVhkzgCE4JptaFIO07db-J49Vgo5ehRmp3kazb'
            '5uLwLe_ejwQgdHhxGHYdkhb4HgwJxOjwz/pubhtml'
        )
