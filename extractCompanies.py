#!/usr/bin/python3

# Run pullTmxListings.bash to get a list of all the securities.
# Then run this to pull out the debentures (".DB") and compare to existing list.


import json

with open('/home/glenn/code/tmx/tmx_listings/listings.json') as f:
  tmxLoad = json.load(f)

with open('/home/glenn/code/debenture/data/DebtInstrumentsProcessed.json') as g:
  knownDebentureLoad = json.load(g)


listings = tmxLoad['results']

tmxDebentures = set()
tmxDebentureDict = {}

for company in listings:
  companySymbol = company['symbol']
  companyName = company['name']
  for instrument in company['instruments']:
    if -1 != instrument['symbol'].find(".DB"):
#      tmxDebentures.add(instrument['symbol'])
      tmxDebentureDict[instrument['symbol']] = {"underlyingSymbol": companySymbol, "underlyingDescription": companyName, "symbol": instrument['symbol'], "description": instrument['name']}


tmxDebentures = set(tmxDebentureDict.keys())

knownDebentures = set()
for debenture in knownDebentureLoad:
  knownDebentures.add(debenture['symbol'])


newDebentures = sorted(tmxDebentures - knownDebentures)
print("TMX debentures not on my list:")
print(newDebentures)
print()

print("My debentures not on TMX list:")
print(sorted(knownDebentures - tmxDebentures))
print()

print("New debenture tuples to add:")
for debenture in tmxDebentureDict:
  detail = tmxDebentureDict[debenture]
  if detail['symbol'] in newDebentures:
    debentureToAdd = {
      "symbol": detail['symbol']
     ,"description": detail['description']
     ,"percentage" : ""
     ,"issueDate" : ""
     ,"maturityDate" : ""
     ,"lastPrice" : ""
     ,"lastPriceDate" : ""
     ,"prospectus" : ""
     ,"underlyingSymbol": detail['underlyingSymbol']
     ,"underlyingLastPrice" : ""
     ,"underlyingLastPriceDate" : ""
     ,"conversionPrice" : ""
     ,"comments" : ""
    }
    print(debentureToAdd)


#print(json.dumps(listings, indent = 4))


