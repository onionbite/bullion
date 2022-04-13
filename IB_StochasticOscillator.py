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
        

def usTechStk(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
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

tickers = ["FB","AMZN","INTC"]

for ticker in tickers:
    histData(tickers.index(ticker),usTechStk(ticker),"2 D","5 mins")
    time.sleep(3)

def stchO(DF, a=20,b=3):
    df = DF.copy()
    df["C-L"] = df["Close"] - df["Low"].rolling(a).min()
    df["H-L"] = df["High"].rolling(a).max() - df["Low"].rolling(a).min()
    df["%K"] = df["C-L"]/df["H-L"]*100
    df["%D"] = df["%K"].ewm(span=b,min_periods=b).mean()
    return df[["%K","%D"]]

historicalData = dataDataframe(tickers, app)
TI_dict = {}
for ticker in tickers:
    TI_dict[ticker] = stchO(historicalData[ticker],20,3)

    
