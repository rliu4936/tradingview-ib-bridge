from ibapi.client import *
from ibapi.wrapper import *
import pandas as pd
import numpy as np
import time

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # To store the latest prices
        self.short_window = 5  # Short-term moving average window
        self.long_window = 20  # Long-term moving average window
        self.current_position = 0  # 0 means no position, 1 means long, -1 means short

    def nextValidId(self, orderId: OrderId):
        self.nextOrderId = orderId
        
        # Request Market Data for QQQ
        contract = Contract()
        contract.symbol = "QQQ"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.reqMktData(1, contract, "", False, False, [])
        print("Requesting QQQ market data")
        
    def tickPrice(self, reqId, tickType, price, attrib):
        print("Price:", price)
        if tickType == 4:  # Last price
            self.data.append(price)
            if len(self.data) > self.long_window:
                self.data.pop(0)  # Keep only the necessary amount of data
                self.calculate_moving_average()

    def calculate_moving_average(self):
        # Convert the list to a pandas Series
        prices = pd.Series(self.data)
        
        # Calculate the moving averages
        short_ma = prices.rolling(window=self.short_window).mean().iloc[-1]
        long_ma = prices.rolling(window=self.long_window).mean().iloc[-1]
        
        print(f"Short MA: {short_ma}, Long MA: {long_ma}")

        # Implement crossover logic
        if short_ma > long_ma and self.current_position != 1:
            # Buy signal
            self.place_order("BUY")
            self.current_position = 1
        elif short_ma < long_ma and self.current_position != -1:
            # Sell signal
            self.place_order("SELL")
            self.current_position = -1

    def place_order(self, action):
        # Create a contract object
        contract = Contract()
        contract.symbol = "TQQQ"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Create an order object
        order = Order()
        order.orderId = self.nextOrderId
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = 10  # Adjust your order size as necessary

        # Place the order
        self.placeOrder(order.orderId, contract, order)
        self.nextOrderId += 1  # Increment orderId for future orders
        print(f"Placed {action} order for 10 shares of TQQQ")

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

app = TestApp()
app.connect("127.0.0.1", 7497, 100)
app.run()