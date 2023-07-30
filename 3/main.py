import csv
import datetime
import json
import logging
import os
from typing import Any
from urllib.request import urlopen, Request

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger(__name__)


API_KEY = os.environ.get("GOOGLE_API_KEY")
SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")


def make_get_request(url: str) -> Any:
    with urlopen(Request(url)) as response:
        status_code = response.getcode()
        data = json.loads(response.read().decode("utf-8"))
        if status_code >= 300:
            raise ValueError(data)
        return data


def get_spreadsheet_info(key_id: str, spreadsheet_id: str) -> dict[str, Any]:
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/?key={key_id}"
    )
    return make_get_request(url)


def get_spreadsheet_data(
    key_id: str, spreadsheet_id: str, range: str
) -> list[list[str]]:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchGet?ranges={range}&key={key_id}"
    return make_get_request(url)


def main():
    if API_KEY is None or SPREADSHEET_ID is None:
        raise EnvironmentError(
            "`GOOGLE_API_KEY` or `GOOGLE_SPREADSHEET_ID` is empty"
            "Rerun after setup env variables"
        )
    spreadsheet_info = get_spreadsheet_info(
        key_id=API_KEY, spreadsheet_id=SPREADSHEET_ID
    )
    title = spreadsheet_info["properties"]["title"]
    logger.info("Got spreadsheet with %d sheets", len(spreadsheet_info["sheets"]))
    for sheet_data in spreadsheet_info["sheets"]:
        sheet = sheet_data["properties"]["title"]
        data = get_spreadsheet_data(
            key_id=API_KEY, spreadsheet_id=SPREADSHEET_ID, range=sheet
        )["valueRanges"][0]["values"]
        logger.info("Loaded `%s` sheet", sheet)
        now = datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S")
        with open(f"{now}_{title}_{sheet}.csv", "w+") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        logger.info("Saved  `%s` sheet", sheet)


if __name__ == "__main__":
    main()
