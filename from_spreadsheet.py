"""
This script gets data from sample Google spreadsheet
"""
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


def get_spreadsheet(url):
    """
    Gets data from some spreadsheet cells
    :param url: spreadsheet url
    :return:
    """
    spreadsheet_id_search = re.compile(r'(?<=spreadsheets/d/).*(?=/edit)')

    spreadsheet_id = re.search(spreadsheet_id_search, url).group()
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.KEY_FILE, config.SCOPE)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(spreadsheet_id).get_worksheet(1)
    result = sheet.get_all_values()[4:]

    return result
