#!/bin/bash

# Pull the TMX listings from the TMX website and create a consolodated json file.
# TMX provides a listing page letter by letter.
# See also: https://tsx.com/listings/current-market-statistics
#           excel with sector and data: https://tsx.com/resource/en/571


TMX_API_URL="https://tsx.com/json/company-directory/search/tsx/"
TMX_QUERY_INTERVAL_SECONDS="15s"

NOW=$(date +'%Y-%m-%d_%H-%M')
DOWNLOAD_DIR="./data/tmx_listings/$NOW"

CONCATENATED_LISTINGS_FILE=".listings.json"
LISTINGS_SYMLINK=$DOWNLOAD_DIR/../listings.json

# An example json response for the TMX query:

#{
#    "last_updated": 1577440510,
#    "length": 97,
#    "results": [
#        {
#            "instruments": [
#                {
#                    "name": "A&W Revenue Rylty Un",
#                    "symbol": "AW.UN"
#                }
#            ],
#            "name": "A&W Revenue Royalties Income Fund",
#            "symbol": "AW.UN"
#        },
#        {
#            "instruments": [
#                {
#                    "name": "Aberdeen Asia-Pacifc",
#                    "symbol": "FAP"
#                }
#            ],
#            "name": "Aberdeen Asia-Pacific Income Investment Company Limited",
#            "symbol": "FAP"
#        },



#date -d @1577440510 -Iminute


function prep {
    mkdir -p "$DOWNLOAD_DIR"
}


function pull {

    for letter in {a..z}
    do
        echo "Retrieving listings for companies starting with the letter: $letter"
        curl "$TMX_API_URL$letter" > "$DOWNLOAD_DIR/$letter.json"
        sleep $TMX_QUERY_INTERVAL_SECONDS
    done
}


function concatResults {

    local RESULT="$DOWNLOAD_DIR/$CONCATENATED_LISTINGS_FILE.tmp"

    # concat listings
    sed 's/^.*\"results\"\:\[/\,/; s/]}$//' "$DOWNLOAD_DIR"/*.json > "$RESULT"

    #open json structure and array of objects
    sed -i '1 s/^\,/{\"results\"\:[/' "$RESULT"

    # close array of objects and json structure
    echo "]}" >> "$RESULT"

    mv "$RESULT" "$DOWNLOAD_DIR/$CONCATENATED_LISTINGS_FILE"

    ln -s -f "$DOWNLOAD_DIR/$CONCATENATED_LISTINGS_FILE" "$LISTINGS_SYMLINK"

}



###########
# mainline
###########


prep
pull
concatResults


