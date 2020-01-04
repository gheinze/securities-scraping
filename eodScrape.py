#!/usr/bin/python3

# Scrape end of day securities quotes from downloaded HTML pages (ex: symbol, close, volume)
# Run as a script: EOD_FILESET_DIR env var must be set
# Run as a module: EOD_FILESET_ROOT_DIR env var must be set
# Outputs a csv of the quotes extracted from the pages
# See help below

import os
import csv
import sys
from bs4 import BeautifulSoup
import eodPull


FROM_LETTER = 'A'
TO_LETTER = 'Z'

columns_of_interest = {0: 'symbol', 1: 'name', 4: 'close', 5: 'volume'}


def _help():
    help_msg = """
    Scrape the end of day data for securities from a directory of downloaded eoddata.com HTML pages.
    The pages can be downloaded via:  eodPull.py
    Pre-set the environment variable EOD_FILESET_DIR to specify the source directory of the
    already downloaded html pages. Specify the exchange and the download time as well. Ex:
    
        export EOD_FILESET_DIR=./data/eod_listings/TSX/2019-12-29_22-37/
        export EOD_EXCHANGE=TSX
        export EOD_DOWNLOAD_TIME=2019-12-29_22-37
        
    The combination of the three environment variables will direct the output of the generated file.
    The result of invoking the script will be a csv file such as:
    
        ./data/eod_listings/TSX/2020-01-01_16-50/TSX~2020-01-01_16-50.quotes.csv

    Alternatively, this script can be run as a module. In this case it will invoke the eodPull.py
    script to download the data and then scrape the data out of these pages. Invoke like this:
    
        export EOD_FILESET_ROOT_DIR=./data/eod_listings/
        import eodScrape
        pull_meata_data = eodScrape.pull_and_scrape_quotes_from_html_pages()
        
    The function will return a dict containing meta data of the pull:
    
        {'target_dir': TARGET_DIR, 'exchange': EXCHANGE, 'date_time': NOW, 'target_file': GENERATED_CSV}
        
    This information can be further used in the process chain to push the csv to a db (eodPushTODb.py).
    """
    print(help_msg)


def _pick_columns_from_row(table_cell_data):
    """
    :param table_cell_data soup list of td table cell text.
    :return: dict: {symbol, eodPrice, volume}
    """

    quote = {}

    for (i, col_datum) in enumerate(table_cell_data):
        if i in columns_of_interest:
            quote[columns_of_interest[i]] = col_datum

    if quote.get(columns_of_interest[0]) is not None:
        return quote

    return None


def _convert_table_row_to_cell_data(html_tr_row):
    """
    :param html_tr_row: an soup table row (<tr>)
    :return: the data in each of the cells (<td>) of the row stripped of whitespace
    """
    cells = html_tr_row.findAll(lambda tag: tag.name == 'td')
    return [ele.text.strip() for ele in cells]


def _write_quotes_to_file(quotes, csv_file):
    """
    :param quotes:
    """

    with open(csv_file, 'w', newline='') as out:
        writer = csv.writer(out, delimiter='~')
        for quote in quotes:
            writer.writerow(quote.values())


def _scrape_quotes_from_html_pages(work_dir):
    """
    Assuming an input directory of html pages named A.htm - Z.htm pulled from eoddata
    :return: list of quotes, each quote being a dict: {symbol, eodPrice, volume}
    """
    quotes = []

    for letter in range(ord(FROM_LETTER), ord(TO_LETTER) + 1):

        file = work_dir + chr(letter) + '.htm'

        with open(file) as fp:

            soup = BeautifulSoup(fp, 'html.parser')
            table = soup.find("table", {"class": "quotes"})
            rows = table.findAll(lambda tag: tag.name == 'tr')

            for row in rows:
                cell_data = _convert_table_row_to_cell_data(row)
                quote = _pick_columns_from_row(cell_data)
                if quote is not None:
                    quotes.append(quote)

    return quotes


def _scrape_and_write(work_dir, target_file):
    quotes = _scrape_quotes_from_html_pages(work_dir)
    _write_quotes_to_file(quotes, target_file)


def _create_csv_file_name(pull_meta):
    return "%s/%s~%s.quotes.csv" % (pull_meta['target_dir'], pull_meta['exchange'], pull_meta['date_time'])


def pull_and_scrape_quotes_from_html_pages():
    pull_meta = eodPull.pull_pages()
    target_file = _create_csv_file_name(pull_meta)
    _scrape_and_write(pull_meta['target_dir'], target_file)
    pull_meta['target_file'] = target_file
    print(pull_meta)
    return pull_meta


def main():
    """
    If run as a standalone script, assume the work dir already exists.
    Extract the work dir from the environment and process.
    :return:
    """

    if len(sys.argv) > 1:
        _help()
        exit(0)

    # export EOD_FILESET_DIR="/home/glenn/code/securities-scraping/data/eod_listings/TSX/2020-01-01_16-50"
    # export EOD_EXCHANGE="TSX"
    # export EOD_DOWNLOAD_TIME="2020-01-01_16-50"

    work_dir = os.environ.get('EOD_FILESET_DIR') + "/"
    exchange = os.environ.get('EOD_EXCHANGE', 'TSX')
    now = os.environ.get('EOD_DOWNLOAD_TIME')

    pull_metadata = {'target_dir': work_dir, 'exchange': exchange, 'date_time': now}

    target_file = _create_csv_file_name(pull_metadata)
    _scrape_and_write(work_dir, target_file)

    print("Created csv:", target_file)


if __name__ == "__main__":
    main()
