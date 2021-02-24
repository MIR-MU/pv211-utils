import datetime
import pkg_resources

from ..leaderboard import GoogleSpreadsheetLeaderboardBase


class TrecLeaderboard(GoogleSpreadsheetLeaderboardBase):
    def _get_week(self, current_date: datetime.datetime) -> int:
        competition_start_w = datetime.date(2021, 3, 1).isocalendar()[1]
        competition_end = datetime.date(2021, 5, 16)
        if current_date.date() > competition_end:
            message = 'Sorry, the competition has ended in {}. No more submissions.'
            message = message.format(competition_end.strftime('%d.%m.%Y %H:%M:%S'))
            raise ValueError(message)
        return current_date.isocalendar()[1] - competition_start_w + 1

    def _get_key_path(self) -> str:
        key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')
        return key_path

    def _get_spreadsheet_key(self) -> str:
        spreadsheet_key = '1eiyase14FrSJs24_LjTSdPwOWOdqutDZhnl33ztBycc'
        return spreadsheet_key
