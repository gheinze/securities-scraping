#!/usr/bin/python3

import psycopg2
import eodScrape
import sys
import os


def _help():
    return """
    ETL. Set your environment with eodConfig.bash
    
        export EOD_FILESET_ROOT_DIR=./data/eod_listings/
        python -c 'import eodPushToDb; eodPushToDb.etl()'
    """


def _get_db_config():
    host = os.environ.get('EOD_DB_HOST')
    database = os.environ.get('EOD_DB')
    user = os.environ.get('EOD_DB_USER')
    password = os.environ.get('EOD_DB_PWD')
    return {'host': host, 'database': database, 'user': user, 'password': password}


def _create_db_connection(host, database, user, password):
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )


def _create_staging_table(cursor) -> None:
    cursor.execute("""
        SET search_path=public;
        DROP TABLE IF EXISTS sm_eod_quotes_staging;
        CREATE UNLOGGED TABLE sm_eod_quotes_staging (
            symbol              TEXT,
            security_descr      TEXT,
            close_price         TEXT,
            volume_traded       TEXT
        );
        COMMIT;
    """)


def _load_staging_table(cursor, src_csv) -> None:
    with open(src_csv, 'r') as f:
        cursor.copy_from(f, 'public.sm_eod_quotes_staging', sep='~')


def _process_staging_table(cursor, exchange, download_date):
    cursor.execute(
        "select sm_load_eod_quotes( %(exchange)s , %(download_date)s )"
        , {'exchange': exchange, 'download_date': download_date}
    )


def load_csv_into_db(csv, exchange, download_date):

    db_config = _get_db_config()

    with _create_db_connection(
            db_config['host'],
            db_config['database'],
            db_config['user'],
            db_config['password']
    ) as connection:

        with connection.cursor() as cursor:
            _create_staging_table(cursor)
            _load_staging_table(cursor, csv)
            _process_staging_table(cursor, exchange, download_date)
            connection.commit()


def etl():
    pull_meta_data = eodScrape.pull_and_scrape_quotes_from_html_pages()
    load_csv_into_db(
        pull_meta_data['target_file'],
        pull_meta_data['exchange'],
        pull_meta_data['date_time']
    )


def main():
    """
    If run as a standalone script, assume the csv already exists.
    Extract config from the environment and process.
    :return:
    """

    if len(sys.argv) > 1:
        _help()
        exit(0)

    csv = os.environ.get('EOD_CSV')
    exchange = os.environ.get('EOD_EXCHANGE', 'TSX')
    date_time = os.environ.get('EOD_DOWNLOAD_TIME')

    load_csv_into_db(csv, exchange, date_time)

    print("Loaded")


if __name__ == "__main__":
    main()
