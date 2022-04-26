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
import numpy as np

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
    time.sleep(3)

historicalData = dataDataframe(tickers, app)

def rsi(DF,n=20):
    df = DF.copy()
    df['delta']=df['Close'] - df['Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean()[n])
            avg_loss.append(df['loss'].rolling(n).mean()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

TI_dict = {}
for ticker in tickers:
    TI_dict[ticker] = rsi(historicalData[ticker],20)
