#!/bin/bash

# Deprecated: use eodPull.py
# Pull end of day securities quotes HTML pages and save to local disk


API_URL="http://www.eoddata.com/stocklist/TSX/"
QUERY_INTERVAL_SECONDS="15s"

NOW=$(date +'%Y-%m-%d_%H-%M')
DOWNLOAD_DIR="./data/eod_listings/TSX/$NOW"


function prep {
    mkdir -p "$DOWNLOAD_DIR"
}


function pull {

    for letter in {A..Z}
    do
        echo "Retrieving listings for companies starting with the letter: $letter"
        curl "$API_URL$letter.htm" > "$DOWNLOAD_DIR/$letter.htm"
        sleep "$TMX_QUERY_INTERVAL_SECONDS"
    done
}


prep
pull

