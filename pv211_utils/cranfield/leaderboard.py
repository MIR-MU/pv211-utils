import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class CranfieldLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2023, 2, 13)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2023, 3, 13)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1kDRTDUCPTOi0crgIO_WqctuvCazTmZ4V_EoVSvb6VQI'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vSXuOTclZfHWYxh2rf7hfMeLvcCuE5UsJu7BzteyunhPw3z4YNZjCovjmMB6SnDdgjGyenOgdochaEq/pubhtml'
        )
