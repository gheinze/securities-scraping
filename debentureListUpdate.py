#!/usr/bin/python3

import pandas as pd
import json
from pandas.io.json import json_normalize
from datetime import datetime
from shutil import copyfile


DELIMITER = "~"

quote_date = "2020-01-24"

quote_file = "./data/eod_listings/TSX/2020-01-24_21-27/TSX~2020-01-24_21-27.quotes.csv"
debenture_file = "../debenture/data/DebtInstrumentsProcessed.json"

#output_json = "debentureList.json"
output_json = debenture_file

output_csv = "debentureList.csv"

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


backup_file = debenture_file + ".bak." + NOW

copyfile(debenture_file, backup_file)


df = pd.read_csv(quote_file, sep="~", header=None, names=['symbol', 'close'], usecols=[0, 2])
quote_dict = df.set_index('symbol')['close'].to_dict()

with open(debenture_file) as f:
    data = json.load(f)

for debenture in data:

    symbol = debenture['symbol']

    try:
        new_price = quote_dict[symbol]
        debenture['lastPrice'] = float(new_price.replace(',',''))
        debenture['lastPriceDate'] = quote_date

        underlying_symbol = debenture['underlyingSymbol']
        if underlying_symbol is not None:
            try:
                new_price = quote_dict[underlying_symbol]
                debenture['underlyingLastPrice'] = float(new_price.replace(',',''))
                debenture['underlyingLastPriceDate'] = quote_date
            except KeyError as e:
                print("No quote available for: ", e)

    except KeyError as e:
        print("No quote available for: ", e)


# print(json.dumps(data))

with open(output_json, 'w') as json_out_file:
    json.dump(data, json_out_file, indent=4)


#df = json_normalize(data, sep="~")
#df.to_csv(output_csv, index=False, sep='~') #, encoding="utf-8"

