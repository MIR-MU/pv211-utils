import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class CranfieldLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2026, 2, 19)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2026, 3, 21)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '18L7dZD1GlRvf-RVEXe9WLr5zmI-ItAfehLMMIDf6YyI'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vTC2L20hNdwaeZr1vaTFwfUdGuzxwyccYkWechI_II_PtB74wYA5aMb1kNJDyD_8oTn1gT0Fz6LcZS3/pubhtml'
        )
