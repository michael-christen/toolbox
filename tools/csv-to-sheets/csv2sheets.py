#!/usr/bin/env python
"""Simple script to upload a CSV to a google sheet.

To Use:
    - pip install -r requirements.txt
    - Obtain credentials: https://gspread.readthedocs.io/en/latest/oauth2.html
    - Download them to "credentials.json"
    - Share a sheet you'd like to change to the client_email in the credentials
    - Run this, feeding your csv in

For me to improve:
    - Specify which sheet in the spreadsheet to use
    - Provide better error handling
"""
import argparse
import csv
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class BaseError(Exception):
    pass


class EntryNotFound(BaseError):
    pass



def read_csv(f=None):
    f = f or sys.stdin
    reader = csv.reader(f)
    for row in reader:
        yield row


def get_entry_for_cell(entries, cell, row_offset=0, col_offset=0):
    entry_row = cell.row - 1 - row_offset
    if entry_row >= len(entries) or entry_row < 0:
        raise EntryNotFound()
    row = entries[entry_row]

    entry_col = cell.col - 1 - col_offset
    if entry_col >= len(row) or entry_col < 0:
        raise EntryNotFound()
    return row[entry_col]


def update_sheet(entries, sheet_name):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    gc = gspread.authorize(credentials)
    # TODO: Select custom sheet
    wks = gc.open(sheet_name).sheet1
    cell_list = wks.range(
        1, 1, wks.row_count, wks.col_count,
    )
    for cell in cell_list:
        try:
            cell.value = get_entry_for_cell(entries, cell)
        except EntryNotFound:
            pass
    wks.update_cells(cell_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload csv to spreadsheets.')
    parser.add_argument('sheet_name', help='The spreadsheet name')
    args = parser.parse_args()
    entries = list(read_csv())
    update_sheet(entries, args.sheet_name)
