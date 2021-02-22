#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class LeaderboardBase(abc.ABC):
    @abc.abstractmethod
    def _get_week(self, current_date: datetime.datetime) -> int:
        pass

    @abc.abstractmethod
    def _get_key_path(self) -> str:
        pass

    @abc.abstractmethod
    def _get_spreadsheet_key(self) -> str:
        pass

    def log_precision_entry(self, competitor_name: str, precision: float = 0.0) -> None:
        if precision > 1.0 or precision < 0.0:
            message = 'That precision ({:.2f}%) looks suspicious. Is it real?'
            message = message.format(100.0 * precision)
            raise ValueError(message)

        key_path = self._get_key_path()
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
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
        current_week = 'Week {}'.format(self._get_week(now))
        header_cell = '=CONCAT(D%s;E%s)' % (current_len+1, current_len+1)
        # append entry
        logs_worksheet.append_row(["", current_len, current_time, current_week, competitor_name, precision])
        logs_worksheet.update_cell(current_len+1, 1, header_cell)

        print('{} submitted MAP {:.2f}% to the leaderboard!'.format(competitor_name, 100.0 * precision))
