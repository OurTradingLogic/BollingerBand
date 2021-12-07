import yfinance as yf
import pandas as pd 
import numpy as np


def amdentNS(tickers):
    tickersresult = []
    for ticket in tickers:
        tickersresult.append(ticket['tradingsymbol'] + ".NS") 

    return tickersresult   

def get_historic_data2(tickers, start, end, interval):
    tickers_result = amdentNS(tickers)

    data = yf.download(tickers=tickers_result, start=start, end=end, interval=interval)
  
    date = []
    open = []
    high = []
    low = []
    close = []
    prevopen = []
    prevhigh = []
    prevlow = []
    prevclose = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

def get_historic_data(tickers, start, end, interval):
    tickers = tickers + '.NS'
    data = yf.download(tickers=tickers, start=start, end=end, interval=interval)
  
    date = []
    open = []
    high = []
    low = []
    close = []
    prevopen = []
    prevhigh = []
    prevlow = []
    prevclose = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        if np.isnan(row['Close']) and (len(close) > 0): 
            close.append(close[len(close)-1])
        else:
            close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df