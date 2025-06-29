import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2025, 3, 27)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2025, 12, 12)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1WSSqb42JliidyguSAyk0uzXkX1h5S-273yvms83My0Y'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vQZXQfKXkVhkzgCE4JptaFIO07db-J49Vgo5ehRmp3kazb'
            '5uLwLe_ejwQgdHhxGHYdkhb4HgwJxOjwz/pubhtml'
        )
