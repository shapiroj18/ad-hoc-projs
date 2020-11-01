import csv
import codecs
from datetime import date
import logging
import os
import sys

import psycopg2
from psycopg2 import sql
import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[
        logging.FileHandler("covid_deaths_to_pg.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def my_handler(type, value, tb):
    logger.exceptiOn("Uncaught exception: %s", value)


sys.excepthook = my_handler


FILENAME = f"covid_deaths{date.today()}.csv"
URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/excess-deaths/deaths.csv"
TABLE = "covid_deaths"


def download_csv(filename: str, url: str) -> None:
    logger.info("Starting to download file to: %s", filename)

    r = requests.get(url, stream=True)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.exception("Unable to connect to url %s", url)
        raise

    counter = 0

    with open(filename, "w") as f:
        # requests.Response.iter_lines sometimes returns bytestrings, we can use
        # codecs.iterdecode to create a new iterator that will decode these bytestrings
        response_iter = codecs.iterdecode(r.iter_lines(), "utf-8")

        for row in response_iter:
            f.write(row + "\n")
            counter += 1

    logger.info("Successfully downloaded file of %i rows to %s", counter, filename)


def load_csv_to_postgres(filename: str, table: str) -> None:
    logger.info("Starting to load file %s to Postgres table %s", filename, table)

    try:
        with psycopg2.connect(
            dbname=os.environ["PGDBNAME"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            host=os.environ["PGHOST"],
        ) as conn, conn.cursor() as cursor, open(filename) as f:
            # Ignore the first line, which is the header
            f.readline()
            cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table)))
            cursor.copy_from(f, table, sep=",", null="")
    except psycopg2.Error as e:
        logger.exception(
            "Something went wrong trying to copy file %s to Postgres table %s",
            filename,
            table,
        )
        raise

    logger.info("Successfully loaded file %s to POstgres table %s", filename, table)


def main() -> None:
    download_csv(FILENAME, URL)
    load_csv_to_postgres(FILENAME, TABLE)


if __name__ == "__main__":
    main()
