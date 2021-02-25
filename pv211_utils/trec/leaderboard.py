import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class TrecLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2021, 3, 1)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2021, 5, 16)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1eiyase14FrSJs24_LjTSdPwOWOdqutDZhnl33ztBycc'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vQ33YdFZtGH6g2bDbkD9aLozLdVVGNuP09sRh-F9d_EY9nWntOrLHSyNATFsXw4v9lw3UA3vOzl5l0s/pubhtml'
        )
