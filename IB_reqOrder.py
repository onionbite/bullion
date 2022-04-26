#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:49:22 2022

@author: ob
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd
import threading
import time

class TradingApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self,self)
        self.order_df = pd.DataFrame(columns=["PermId","ClientId","OrderId","Account","Symbol","SecType","Exchange",
                                              "Action","OrderType","TotalQty","CashQty","LmtPrice","AuxPrice",
                                              "Status"])
        self.acc_df = pd.DataFrame(columns=["ReqId","Account","Tag","Value","Currency"])
        
        self.pnl_df = pd.DataFrame(columns=["ReqId","DailyPnL","UnrealizedPnL","RealizedPnL"])

    def openOrder(self, orderId, contract, order,orderState):
                 super().openOrder(orderId, contract, order, orderState)
                 dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId, 
                               "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                               "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                               "TotalQty": order.totalQuantity, "CashQty": order.cashQty, "LmtPrice": order.lmtPrice, 
                               "AuxPrice": order.auxPrice, "Status": orderState.status}
                 self.order_df = self.order_df.append(dictionary, ignore_index=True)
                 
    def accountSummary(self, reqId, account, tag, value, currency):
                 super().accountSummary(reqId, account, tag, value, currency)
                 accDic = {"ReqId": reqId, "Account": account,"Tag": tag, "Value": value, "Currency": currency}
                 self.acc_df = self.acc_df.append(accDic, ignore_index=True)
    
    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
                 super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
                 pnlDic = {"ReqId": reqId, "DailyPnL": dailyPnL, "UnrealizedPnL": unrealizedPnL, "RealizedPnL": realizedPnL}
                 self.pnl_df = self.pnl_df.append(pnlDic, ignore_index=True)
                 
def websocket_con():
    app.run() 

app = TradingApp()      
app.connect("127.0.0.1", 7497, clientId=4)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) #ensure that the connection is established

#req profit and loss
app.reqPnL(9001, "DU5476079", "")
time.sleep(5)
pnlInfo = app.pnl_df

#req account summary
#app.reqAccountSummary(9001, "All", "$LEDGER:ALL")
#time.sleep(5)
#accSum = app.acc_df

#req order
#app.reqOpenOrders()
#time.sleep(5) 
#orderInfo = app.order_df

