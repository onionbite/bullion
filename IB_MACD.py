# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd

class TradingApp(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.data = {}     

    def historicalData(self, reqId, bar):
        if reqId not in self.data:    
            self.data[reqId] = [{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}]
        else:
            self.data[reqId].append({"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})
        
        print("redID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId,bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume))
        

def usTechStk(symbol,sec_type="CASH",currency="MXN",exchange="IDEALPRO"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract

def histData(req_num,contract,duration,candle_size):
    #request contract detail
    app.reqHistoricalData(reqId=req_num, 
                          contract=contract, 
                          endDateTime='', 
                          durationStr=duration, 
                          barSizeSetting=candle_size, 
                          whatToShow="MIDPOINT", 
                          useRTH=1, 
                          formatDate=1, 
                          keepUpToDate=0, 
                          chartOptions=[])
    
def websocket_con():
    app.run()
    
app = TradingApp()
app.connect(host="127.0.0.1",port=7497, clientId=1)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)

def dataDataframe(symbols,tradeapp):
    df_data = {}
    for sym in symbols: 
        df_data[sym] = pd.DataFrame(data=tradeapp.data[symbols.index(sym)]) 
        df_data[sym].set_index("Date",inplace=True)
    return df_data

tickers = ["USD","GBP","EUR"]

for ticker in tickers:
    histData(tickers.index(ticker),usTechStk(ticker),"2 D","5 mins")
    time.sleep(5)

historicalData = dataDataframe(tickers, app)

def MACD(DF, a=12,b=26,c=9):
    df = DF.copy()
#MACD SMA
    #df["MA_fast"] = df["Close"].rolling(a).mean()
    #df["MA_slow"] = df["Close"].rolling(b).mean()
    #df["MACD"] = df["MA_fast"] - df["MA_slow"]
    #df["Signal"] = df["MACD"].rolling(c).mean()
#MACD EMA
    df["MA_fast"] = df["Close"].ewm(span=a, min_periods=a).mean()
    df["MA_slow"] = df["Close"].ewm(span=b, min_periods=b).mean()
    df["MACD"] = df["MA_fast"] - df["MA_slow"]
    df["Signal"] = df["MACD"].ewm(span=c, min_periods=c).mean()
    return df


macd_df = MACD(historicalData["GBP"],12,26,9)
