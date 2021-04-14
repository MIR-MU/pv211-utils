import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2021, 4, 19)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2021, 5, 2)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1XXR_3UsjUTxQApU5RRce1Zv4G_0uMJXoaEb0GejU868'
        return spreadsheet_key

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/'
            '2PACX-1vQb_L4ZL5vglRMJBMDn334JHL6xfGVXVz-D1YnZduXTZe4Pj_abKSpe_qnu2gkQEBV5jXEgFyge_Jtu/pubhtml'
        )
