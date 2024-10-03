from contextlib import asynccontextmanager
import random
from ib_insync import *
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

# Initialize the Interactive Brokers client

ib = IB()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to IB when FastAPI starts
    try:
        await ib.connectAsync('127.0.0.1', 7497, clientId=2)
        print("Connected to IB")
    except Exception as e:
        print(f"Error connecting to IB: {e}")
    
    yield  # Allows the application to continue running

    # Shutdown: Disconnect IB when FastAPI shuts down
    if ib.isConnected():
        ib.disconnect()
        print("Disconnected from IB")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming webhook requests and place an order asynchronously."""
    try:
        # Parse the incoming JSON payload
        payload = await request.json()
        action = payload.get("action", "").lower()
        ticker = payload.get("ticker", "")
        quantity = payload.get("quantity", 10)  # Default to 10 shares if not provided

        if action not in ["buy", "sell"]:
            raise HTTPException(status_code=400, detail="Invalid action. Must be 'buy' or 'sell'.")

        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker is required.")

        # Check if the IB client is connected, reconnect if not
        if not ib.isConnected():
            print("IB client not connected, attempting to reconnect...")
            await ib.connectAsync('127.0.0.1', 7497, clientId=1)
            if not ib.isConnected():
                raise HTTPException(status_code=500, detail="Unable to connect to IB")

        # Execute the place_order function within the IB event loop using asyncio
        result = await place_order(action, ticker, quantity)

        return {"status": result}

    except Exception as e:
        print(f"Error processing webhook request: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook request")
    

def generate_realistic_data(num_entries=5, start_price=150):
    data = []
    current_time = datetime.now()
    current_price = start_price  # Start with an initial price
    
    for i in range(num_entries):
        # Generate realistic price changes
        price_change = random.uniform(-2, 2)  # Small change for the next day's open price
        open_price = current_price + price_change
        
        # Simulate close price with some random fluctuation
        close_price = open_price + random.uniform(-1, 1)
        
        # High and low are based on open/close with some fluctuation
        high_price = max(open_price, close_price) + random.uniform(0, 1)
        low_price = min(open_price, close_price) - random.uniform(0, 1)
        
        # Store the candlestick data
        data.append({
            "time": int((current_time + timedelta(days=i)).timestamp()),  # Unix timestamp
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2)
        })
        
        # Update the current price for the next iteration
        current_price = close_price  # The next day's open is based on the previous close
    
    return data

@app.get("/candlestick")
def get_candlestick_data():
    data = generate_realistic_data(50)  # Generate 5 random candlestick data points
    return data



async def place_order(action: str, ticker: str, quantity: int):
    """Place an order using the IB API asynchronously."""
    try:
        # Define a stock contract
        contract = Stock("A", 'SMART', 'USD')
        await ib.qualifyContractsAsync(contract)  # Use the asynchronous version
        
        # Determine order type based on action
        order = MarketOrder('BUY' if action == "buy" else 'SELL', quantity)
        
        # Place the order
        trade = ib.placeOrder(contract, order)
        print(f"Placed a {action} order for {quantity} shares of {ticker}")
        return f"{action.capitalize()} order placed successfully for {quantity} shares of {ticker}"
    except Exception as e:
        print(f"Error placing order: {e}")
        raise HTTPException(status_code=500, detail="Error placing order")
    

