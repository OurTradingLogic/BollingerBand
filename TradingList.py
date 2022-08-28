from datetime import datetime, timedelta
import YahooAPI as yapi
import BollingerBand as bband
import StockList as slidt
import os

def gettradinglist(source):
    trade_list = [] #empty list
    startdate = datetime.now() - timedelta(days=500)
    enddate = datetime.now()

    alllist = slidt.getlistfrom(source) 
    inte = 1
    intetotal = 0
    for rows in alllist:
        if inte > 11:
            os.system('clear')
            inte = 0

        print(str(intetotal))
        inte = inte + 1
        intetotal = intetotal +1
        ticket = str(rows['tradingsymbol'])

        stock = yapi.get_historic_data(tickers=ticket, start=startdate, end=enddate, interval="1wk")
        if len(stock) > 0:
            stock = stock.set_index('date')

            stock['sma_20'] = bband.sma(stock['close'], 20)
            stock['upper_bb'], stock['lower_bb'] = bband.bb(stock['close'], stock['sma_20'], 20)
            bband.break_out(stock)

            buy_price, sell_price, bb_signal, buy_date, sell_date = bband.implement_bb_strategy(stock, 1)

            if len(buy_date) > 0: 
                temp_last_buy_date = buy_date[len(buy_date)-1]
                last_buy_date = temp_last_buy_date.strftime("%Y-%m-%d")
                temp_date = datetime.now() - timedelta(days=30)
                today_date = temp_date.strftime("%Y-%m-%d")
                
                if last_buy_date > today_date: 
                    new_dict = slidt.constructorderjson(rows, stock['close'][len(stock)-1])                  
                    trade_list.append(new_dict)
    return trade_list