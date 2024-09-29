from contextlib import asynccontextmanager
from ib_insync import *
from fastapi import FastAPI, HTTPException, Request

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


async def place_order(action: str, ticker: str, quantity: int):
    """Place an order using the IB API asynchronously."""
    try:
        # Define a stock contract
        contract = Stock("AAPL", 'SMART', 'USD')
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