import logging
import os
import json

from google_api_service_helper import GoogleSpreadsheet

SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")
CREDENTIAL_PATH = os.environ.get("CREDENTIAL_PATH", './credentials.json')
SHEET = "Stats"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger(__name__)




def get_credentials() -> dict[str, str]:
    if not os.path.exists('credentials.json'):
        raise ValueError(f'Credential file is not exist. Create on path `{CREDENTIAL_PATH}')
    
    with open(CREDENTIAL_PATH) as f:
        return json.load(f)


def main():
    gs = GoogleSpreadsheet(google_keys=get_credentials())
    try:
        data = gs.get_data(ss_id=SPREADSHEET_ID, range_sheet="Stats")
    except Exception:
        raise ValueError('Check spreadsheet ID and permissions of credential key')
    column = [
        '01.06.2023',
        '22,3',
        '0',
        '-0,7',
        '0',
        '73,1',
        '19,7',
        '10,6',
        '81,3',
    ]
    for i in range(1,len(column)+1):
        data[i].append(column[i-1])
    data[0].insert(3,"")
    column = [
        '01.06.2023',
        '353',
        '0',
        '6',
        '-10',
        '218',
        '132',
        '8'
    ]
    for i in range(1,len(column)+1):
        data[i].insert(3, column[i-1])
    gs.set_data(ss_id=SPREADSHEET_ID, range_sheet="Stats",values=data, major_dimension="ROWS")
    logger.info('Done')


if __name__ == "__main__":
    main()