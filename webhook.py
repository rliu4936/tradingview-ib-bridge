from flask import Flask, request, jsonify
from ib_insync import *
import json

# Initialize Flask app
app = Flask(__name__)

# Initialize Interactive Brokers client
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure TWS/Gateway is running and the API is enabled

@app.route('/webhook', methods=['POST'])
def webhook():
    # Receive the TradingView alert data
    data = request.json
    print("Received data:", data)
    
    action = data.get("action")
    ticker = data.get("ticker")
    
    if action == "long":
        place_order(ticker, action='BUY')
    elif action == "exit":
        place_order(ticker, action='SELL')
        
    return jsonify({"status": "success"})

def place_order(symbol, action):
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    
    if action == "BUY":
        order = MarketOrder('BUY', 100)  # Modify quantity as needed
    elif action == "SELL":
        order = MarketOrder('SELL', 100)
        
    trade = ib.placeOrder(contract, order)
    print(f"Placed {action} order for {symbol}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Exposes the server to your local network
