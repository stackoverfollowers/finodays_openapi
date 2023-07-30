import json
import logging
import os

from google_api_service_helper import GoogleSpreadsheet
from googleapiclient.errors import HttpError
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)


GOOGLE_CREDENTIALS_FILE_PATH = os.environ.get('GOOGLE_CREDENTIALS_FILE_PATH', 'credentials.json')
SPREADSHEET_ID = os.environ.get('GOOGLE_SPREADSHEET_ID', '1anLwzOo3pKIL02JCteFPE21b8BKCdYY25zksFMVTIwg')


def read_google_credential_keys() -> dict:
    if not os.path.exists(GOOGLE_CREDENTIALS_FILE_PATH):
        raise ValueError("You schould create `credentials.json` in project folder")
    with open(GOOGLE_CREDENTIALS_FILE_PATH) as f:
        return json.load(f)

def main():
    try:
        gs = GoogleSpreadsheet(google_keys=read_google_credential_keys())
        print(gs.get_spreadsheet(SPREADSHEET_ID)['spreadsheets'])
    except HttpError as e:
        message = json.loads(e.content)['error']['message']
        logger.info('Got `%s`', message)
if __name__ == "__main__":
    main()