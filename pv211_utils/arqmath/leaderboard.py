import datetime
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2025, 3, 30)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2025, 5, 9)

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1KYCB-cbqk8TZMti8aneJptf4T3E1t1n_9v9UEhRxNSQ'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vSKbu4rZX4yh5tUmg_2NGUNBcXjazw4-F0CunOp5d7sz'
            'bPj88pY7QC0z5zC9cAShcD5FwPz9JCjNsNX/pubhtml'
        )
