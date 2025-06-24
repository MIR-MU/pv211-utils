import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2025, 3, 27)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2025, 5, 7)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = "132bKclRbrO3Bew94MToB29t4ZPIbWLRltajfkO-h9rU"
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            "https://docs.google.com/spreadsheets/d/e/2PACX"
            "-1vSF9CooJQp8chrRh0DkopPCnLWoTKqnt0g6e6V-9lMzy"
            "MOSN8KpeLpu-52Jyjme2vLc2Jdc9h5Mk_pp/pubhtml"
        )
