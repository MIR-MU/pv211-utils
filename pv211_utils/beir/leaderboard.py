import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class BeirLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2026, 3, 30)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2026, 5, 9)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1EoZCyJCDCMEt9IlNNJ4WbVZipIRiBlrIKmAakf2HQKg'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vQu0OM5HKnA5n_ZYoeJH0WKzIz_qA3lbU4LFXRraRcLtG0'
            'nft35tOhdUQ5og1-JlHD1JpFN93vkuqbZ/pubhtml'
        )
