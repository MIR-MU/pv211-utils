#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pkg_resources
import datetime


def _get_week(current_date: datetime.datetime, competition_end=datetime.date(2020, 5, 8)) -> int:
    competition_start_w = datetime.date(2020, 2, 17).isocalendar()[1]
    if current_date.date() > competition_end:
        raise ValueError("Sorry, the competition has ended in %s. No more submissions."
                         % competition_end.strftime("%d.%m.%Y %H:%M:%S"))
    return current_date.isocalendar()[1] - competition_start_w + 1


def log_precision_entry(competitor_name: str, precision: float = 0):
    if precision > 1 or precision < 0:
        raise ValueError("That precision (%s) looks suspicious. Is it real?" % precision)

    key_path = pkg_resources.resource_filename("pv211_utils", "data/pv211-leaderboard-b8e892e3e8bb.json")

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    gc = gspread.authorize(credentials)

    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")

    spreadsheet_key = '1f9P3bn17n2rHGCxBnn3GVr57PF5hMWJEILp06Uq7Jnk'
    spreadsheet = gc.open_by_key(spreadsheet_key)
    logs_worksheet = spreadsheet.worksheet("submissions")
    scores_worksheet = spreadsheet.worksheet("leaderboard")
    if competitor_name not in scores_worksheet.col_values(2):
        raise ValueError("We do not have anyone named '%s' in the leaderboard. Is the spelling correct? "
                         "\nWe expect the name in format '<Surname>, <Name>', like 'Novotný, Vít'"
                         % competitor_name)

    logs_list = logs_worksheet.get_all_values()
    current_len = len(logs_list)
    current_week = "Week %s" % _get_week(now)
    header_cell = '=CONCAT(D%s;E%s)' % (current_len+1, current_len+1)
    # append entry
    logs_worksheet.append_row(["", current_len, current_time, current_week, competitor_name, float(precision)])
    logs_worksheet.update_cell(current_len+1, 1, header_cell)
    return "Alles gutte!"
