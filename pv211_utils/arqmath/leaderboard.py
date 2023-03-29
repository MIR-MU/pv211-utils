import datetime
import pkg_resources
from typing import Optional

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class ArqmathLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def get_competition_start(self) -> datetime.date:
        return datetime.date(2023, 3, 22)

    def get_competition_end(self) -> datetime.date:
        return datetime.date(2023, 5, 1)

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1zGUntkeUmE8oFKgM9WdFbN14IPdGJHDbKWXoiec_lmM'
        return spreadsheet_key

    def _format_name(self, name) -> str:
        name_list = name.split(",")
        return name_list[1].strip(" ") + " " + name_list[0]

    def get_public_url(self) -> Optional[str]:
        return (
            'https://docs.google.com/spreadsheets/d/e/2PACX'
            '-1vT9GibzjkZJxdFNdgr666TLDIHD46HfTYSEPeKUN-ErxRIN2HGjUtKyfvf6Xg3MZ6cW4p9qcSmR'
            '-4Rk/pubhtml?gid=0&single=true'
        )
