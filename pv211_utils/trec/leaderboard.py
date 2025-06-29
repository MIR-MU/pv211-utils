import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class TrecLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2022, 3, 22)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2022, 12, 12)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1OCXrOoaR2MPl-5_oSJ6UJK1dXOaU4J4xZo6erg1HOfE'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vTchMTviB7TzYsQcnJnnoB2SUBAJBOfGh3w7gv65Dp95JltM7t1rcAIjubcgG7HT_dDmo4UyFoZQ9gH/pubhtml'
        )
