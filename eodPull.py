#!/usr/bin/python3

# Download set of files from eod website.
# EOD_FILESET_ROOT_DIR should be set.
# See help below.

import os
import requests
import time
import sys
from datetime import datetime
from pathlib import Path


API_URL = "http://www.eoddata.com/stocklist/"
QUERY_INTERVAL_SECONDS = 15
EXCHANGE = "TSX"

FROM_LETTER = 'A'
TO_LETTER = 'Z'

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M")

EOD_FILESET_ROOT_DIR_DEFAULT = os.getcwd() + '/data/eod_listings/'
EOD_FILESET_ROOT_DIR = os.environ.get('EOD_FILESET_ROOT_DIR', EOD_FILESET_ROOT_DIR_DEFAULT)
TARGET_DIR = "%s/%s/%s/" % (EOD_FILESET_ROOT_DIR, EXCHANGE, NOW)

PULL_META = {'target_dir': TARGET_DIR, 'exchange': EXCHANGE, 'date_time': NOW}


def _help():
    help_msg = """
    This script downloads the eod html pages published at eoddata.com and saves them to local disk.
    Pre-set the environment variable EOD_FILESET_ROOT_DIR to specify the target download directory: 
    
        export EOD_FILESET_ROOT_DIR=./data/eod_listings/
    
    Find the downloaded pages in a directory similar to:
    
        ./data/eod_listings/TSX/2020-01-01_16-50/
    
    where the exchange and the download timestamp are used as part of the directory path.
    This script can be called interactively or invoked via:
    
        import eodPull
        eodPull.pull_pages()
    """
    print(help_msg)


def _create_target_dir(target_dir):
    Path(target_dir).mkdir(parents=True, exist_ok=True)


def _pull_pages():

    for letter in [chr(letter) for letter in range(ord(FROM_LETTER), ord(TO_LETTER) + 1)]:
        print("Retrieving listings for companies starting with the letter", letter)

        url = "%s/%s/%s.htm" % (API_URL, EXCHANGE, letter)
        page = requests.get(url)

        file = TARGET_DIR + letter + '.htm'
        with open(file, "w") as fp:
            fp.write(page.text)

        time.sleep(QUERY_INTERVAL_SECONDS)


def pull_pages():
    _create_target_dir(TARGET_DIR)
    _pull_pages()
    return PULL_META


def main():
    pull_pages()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        _help()
        exit(0)

    main()
    print("\n\nNext run:\n")
    print('export EOD_FILESET_DIR="' + TARGET_DIR + '"')
    print("./eodScrape.py\n\n")
