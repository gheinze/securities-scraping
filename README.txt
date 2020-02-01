Process 1: Examine TMX Instruments

       ./pullTmxListings.bash
       ./showDebentureDiff.py


    A. Pull the TMX Instruments from the TMX web site

       ./pullTmxListings.bash

       No environment variables need to be set. Creates a .data/tmx_listings/listings.json file
       which contains the download companies/instruments. The raw data for the download is
       in a time-stamped subdirectory.


    B. Compare my Debenture List to those pulled

       ./showDebentureDiff.py

       No data is mofified. Delta dumped to display.
       Assumes the location of the debenture file to be at:
       ../debenture/data/DebtInstrumentsProcessed.json

       and the downloaded instruments to be at:
       ./data/tmx_listings/listings.json



Process 2: Download End Of Day (eod) quotes and push them into a db

       . ./eodConfig.bash
       export EOD_FILESET_ROOT_DIR=./data/eod_listings/
       python -c 'import eodPushToDb; eodPushToDb.etl()'



Process 3: Update my Debenture List json file with new quotes using EOD data

       This is still a work in progress. i

       vi debentureListUpdate.py

       set quote date and quote file
       run

       open java process to push to Google Sheets

