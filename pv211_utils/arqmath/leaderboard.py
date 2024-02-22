import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2024, 3, 27)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2024, 5, 7)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1ohEA6tcmKKKng0Tx787p112fTWDNgF8O5JMvSF-v0ds'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vQyaxVj3qnJgeSyOnAtUb7VcielyLnw9MZTNC9vTVZm22'
            'aH4TqV-aIx2TjDZ9fXSeKveUJA8cVB23XR/pubhtml'
        )
