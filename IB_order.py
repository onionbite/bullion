#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:49:22 2022

@author: ob
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

class TradingApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self,self)

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId,errorCode,errorString))        

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:",orderId)

def websocket_con():
    app.run() 

app = TradingApp()      
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) #ensure that the connection is established

def usTechStk(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract

def limitOrder(direction,quantity,lmt_price):
    order = Order()
    order.action = direction
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmt_price
    return order

def marketOrder(direction,quantity):
    order = Order()
    order.action = direction
    order.orderType = "MKT"
    order.totalQuantity = quantity
    return order

def stopOrder(direction,quantity,stopPrice):
    order = Order()
    order.action = direction
    order.orderType = "STP"
    order.auxPrice = stopPrice
    order.totalQuantity = quantity
    return order

def trailingOrder(direction,quantity,trStop,tr_step=1):
    order = Order()
    order.action = direction
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.auxPrice = tr_step
    order.trailStopPrice = trStop
    return order 


app.reqIds(-1)
orId = app.nextValidOrderId
app.placeOrder(orId,usTechStk("FB"),trailingOrder("BUY",1,1400,2))
time.sleep(5) 

#modify order
#orId = app.nextValidOrderId
#app.placeOrder(orId,usTechStk("FB"),limitOrder("BUY",1,200))
#time.sleep(5) 
#app.cancelOrder(orId)
#app.reqIds(-1) # Function to trigger nextValidId function
#time.sleep(3) 
#orId = app.nextValidOrderId
#app.placeOrder(orId,usTechStk("FB"),limitOrder("BUY",1,150))
#time.sleep(5) 
#app.cancelOrder(orId)