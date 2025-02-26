import abc
from typing import Optional
import datetime
import pkg_resources

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class LeaderboardBase(abc.ABC):
    """A leaderboard with information retrieval system results.

    """
    @abc.abstractmethod
    def log_precision_entry(self, author_name: str, mean_average_precision: float) -> None:
        """Logs mean average precision of an author to the leaderboard.

        Parameters
        ----------
        author_name : str
            The name of the information retrieval system author.
        mean_average_precision : float
            The mean average precision.
        """
        pass

    @abc.abstractmethod
    def get_competition_start(self) -> datetime.date:
        """Gets the starting date of the competition.

        Returns
        -------
        datetime.date
            The starting date of the competition.

        """
        pass

    @abc.abstractmethod
    def get_competition_end(self) -> datetime.date:
        """Gets the end date of the competition.

        Returns
        -------
        datetime.date
            The end date of the competition.

        """
        pass

    def get_week(self, current_date: datetime.date) -> int:
        """Gets the current week of the competition.

        Parameters
        ----------
        current_date : datetime.date
            The current date.

        Returns
        -------
        int
            The current week of the competition.

        """
        competition_start = self.get_competition_start()
        competition_end = self.get_competition_end()
        if current_date > competition_end:
            message = 'Sorry, the competition has ended in {}. No more submissions.'
            message = message.format(competition_end.strftime('%d.%m.%Y %H:%M:%S'))
            raise ValueError(message)
        week = current_date.isocalendar()[1] - competition_start.isocalendar()[1] + 1
        return week

    def get_public_url(self) -> Optional[str]:
        """Gets the public URL of the leaderboard.

        Returns
        -------
        str or None
            The public URL of the leaderboard. If None, then there is no public URL.

        """
        return None


class GoogleSpreadsheetLeaderboardBase(LeaderboardBase):

    def _get_key_path(self) -> str:
        key_json_h = open(pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-config.jsonb')).read()
        key_json = json.loads(bytes.fromhex(key_json_h).decode('utf-8'))
        return key_json

    @abc.abstractmethod
    def _get_spreadsheet_key(self) -> str:
        pass

    def log_precision_entry(self, competitor_name: str, precision: float) -> None:
        if precision > 1.0 or precision < 0.0:
            message = 'That precision ({:.2f}%) looks suspicious. Is it real?'
            message = message.format(100.0 * precision)
            raise ValueError(message)

        key_str = self._get_key_path()
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_str, scope)
        gc = gspread.authorize(credentials)

        now = datetime.datetime.now()
        current_time = now.strftime('%d.%m.%Y %H:%M:%S')

        spreadsheet_key = self._get_spreadsheet_key()
        spreadsheet = gc.open_by_key(spreadsheet_key)
        logs_worksheet = spreadsheet.worksheet("submissions")
        scores_worksheet = spreadsheet.worksheet("leaderboard")
        if competitor_name not in scores_worksheet.col_values(2):
            message = "We do not have anyone named '{}' in the leaderboard. Is the spelling correct?"
            message += "\nWe expect the name in format '<Surname>, <Name>', like 'Novotný, Vít'"
            message = message.format(competitor_name)
            raise ValueError(message)

        logs_list = logs_worksheet.get_all_values()
        current_len = len(logs_list)
        current_week = 'Week {}'.format(self.get_week(now.date()))
        header_cell = '=CONCAT(D%s;E%s)' % (current_len+1, current_len+1)
        # append entry
        logs_worksheet.append_row(["", current_len, current_time, current_week, competitor_name, precision])
        logs_worksheet.update_cell(current_len+1, 1, header_cell)
