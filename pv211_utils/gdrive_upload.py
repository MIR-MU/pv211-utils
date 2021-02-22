#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def _get_week(current_date : datetime.datetime,
              competition_end : datetime.datetime = datetime.date(2021, 4, 18)) -> int:
    competition_start_w = datetime.date(2021, 3, 1).isocalendar()[1]
    if current_date.date() > competition_end:
        message = 'Sorry, the competition has ended in {}. No more submissions.'
        message = message.format(competition_end.strftime('%d.%m.%Y %H:%M:%S'))
        raise ValueError(message)
    return current_date.isocalendar()[1] - competition_start_w + 1


def log_precision_entry(competitor_name: str, precision: float = 0.0) -> None:
    if precision > 1.0 or precision < 0.0:
        raise ValueError('That precision (%f) looks suspicious. Is it real?'.format(precision))

    key_path = pkg_resources.resource_filename('pv211_utils', 'data/pv211-leaderboard-b8e892e3e8bb.json')

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    gc = gspread.authorize(credentials)

    now = datetime.datetime.now()
    current_time = now.strftime('%d.%m.%Y %H:%M:%S')

    spreadsheet_key = '1CNeZESOrPxBs3U0FeGtaDPLJQkb2Ubsr0aCvyNIwdtM'
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
    current_week = 'Week {}'.format(_get_week(now))
    header_cell = '=CONCAT(D%s;E%s)' % (current_len+1, current_len+1)
    # append entry
    logs_worksheet.append_row(["", current_len, current_time, current_week, competitor_name, precision])
    logs_worksheet.update_cell(current_len+1, 1, header_cell)

    print('{} submitted MAP {:.2f}% to the leaderboard!'.format(competitor_name, 100.0 * precision))
