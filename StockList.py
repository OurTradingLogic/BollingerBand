import pandas as pd
import CommonEnum as enum
from requests import get

pd.options.mode.chained_assignment = None

global token_df
url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
d = get(url).json()
token_df = pd.DataFrame.from_dict(d)

def getlistfrom(source):
    all_list = [] #empty list
    if source == enum.ExportFrom.EXCEL:
        all_list = getfromexcel()
    elif source == enum.ExportFrom.JSON:
        all_list = getfromjson()
    return all_list

def getfromjson():
    all_list = [] #empty list
    for index, rows in token_df.iterrows():
        name = rows["name"]
        symbol = rows["symbol"]
        if name + "-EQ" == symbol:
            list = constructlistjson(name, rows["token"], rows["exch_seg"]) 
            all_list.append(list)
    return all_list

def getfromexcel():
    all_list = [] #empty list
    df = pd.read_excel("Untitled.xlsx")
    for index, rows in df.iterrows():    
        ticket = str(rows['symbol'])
        list = constructlistjson(ticket, str(getTokenInfo(ticket)), str(rows['exchange'])) 
        all_list.append(list)
    return all_list

def getTokenInfo(symbol):
    symbol = symbol + "-EQ"
    df_script = token_df.loc[token_df['symbol'] == symbol]
    if not df_script.empty:
        return df_script.iat[0,0]
    else:
        return "0"

def constructorderjson(row, latestprice):
    cjson = {"variety": "NORMAL", 
            "tradingsymbol" : str(row["tradingsymbol"]),
            "symboltoken" : str(row["symboltoken"]),
            "transactiontype": "BUY", 
            "exchange": str(row["exchange"]),
            "ordertype": "MARKET", 
            "producttype": "AMO Delivery",
            "duration": "DAY", 
            "price": str(latestprice), 
            "quantity": "1",
            "triggerprice": "0"}
    return cjson

def constructlistjson(symbol, token, exchange):
    cjson = {"tradingsymbol" : str(symbol),
            "symboltoken" : str(token),
            "exchange": str(exchange)}
    return cjson