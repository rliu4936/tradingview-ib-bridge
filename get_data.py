from ib_insync import IB, Stock

# Initialize the IB object
ib = IB()

# Connect to IB Gateway or TWS
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the stock contract (AAPL example)
contract = Stock('AAPL', 'SMART', 'USD')

# Request historical data with delayed data enabled
bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='1 Y',  # For example, 1 year of delayed data
    barSizeSetting='1 day',  # Daily bars
    whatToShow='TRADES',  # TRADES, BID, or ASK based on your preference
    useRTH=True,  # Regular trading hours
    formatDate=1,  # Use '1' for formatted dates
    keepUpToDate=False  # Set to False, as real-time updates are not available for delayed data
)

#  [Date, Open, High, Low, Close, Volume]

# Print some example data
print(bars)

# Optionally disconnect
ib.disconnect()
