from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define a stock contract
contract = Stock('SQQQ', 'SMART', 'USD')
ib.qualifyContracts(contract)

# Place a market order
order = MarketOrder('BUY', 10)
trade = ib.placeOrder(contract, order)
print(f"Placed a buy order for AAPL")
