from flask import Flask, request, jsonify
from ib_insync import *
import json
import logging
import threading
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Initialize Interactive Brokers client
ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure TWS/Gateway is running and the API is enabled
except Exception as e:
    print(f"Error connecting to IB: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Try to parse the JSON data manually
        try:
            data = request.get_json(force=True)  # This forces the parsing of JSON even without the correct header
        except Exception as e:
            logger.error(f"Error parsing JSON data: {e}")
            return jsonify({"error": "Invalid JSON format"}), 400
        
        if not data:
            logger.error("No data received")
            return jsonify({"error": "No data received"}), 400

        logger.info(f"Received data: {data}")
        
        action = data.get("action")
        ticker = data.get("ticker")
        
        # Execute the place_order function in the IB event loop using asyncio
        if action == "long":
            asyncio.run_coroutine_threadsafe(run_place_order(ticker, 'BUY'), ib.asyncioLoop)
        elif action == "exit":
            asyncio.run_coroutine_threadsafe(run_place_order(ticker, 'SELL'), ib.asyncioLoop)
        else:
            logger.error("Invalid action received")
            return jsonify({"error": "Invalid action received"}), 400
        
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

async def run_place_order(symbol, action):
    try:
        contract = Stock(symbol, 'SMART', 'USD')
        await ib.qualifyContractsAsync(contract)  # Use the async version of qualifyContracts
        
        if action == "BUY":
            order = MarketOrder('BUY', 100)  # Modify quantity as needed
        elif action == "SELL":
            order = MarketOrder('SELL', 100)
        
        trade = ib.placeOrder(contract, order)
        logger.info(f"Placed {action} order for {symbol}")
    except Exception as e:
        logger.error(f"Error placing order: {e}")

def start_flask_app():
    app.run(host='0.0.0.0', port=80)

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()

# Start the IB event loop
ib.run()
