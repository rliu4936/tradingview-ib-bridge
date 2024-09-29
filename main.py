from fastapi import FastAPI, HTTPException
from ib_insync import *
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Initialize the Interactive Brokers client
ib = IB()

async def connect_ib():
    """Connect to Interactive Brokers using the asynchronous method."""
    try:
        await ib.connectAsync('127.0.0.1', 7497, clientId=1)
        print("Connected to IB")
    except Exception as e:
        print(f"Error connecting to IB: {e}")

@app.on_event("startup")
async def startup_event():
    """Startup event to connect to IB when FastAPI starts."""
    await connect_ib()

@app.post("/webhook")
async def webhook():
    """Handle incoming webhook requests and place an order asynchronously."""
    try:
        # Check if the IB client is connected, reconnect if not
        if not ib.isConnected():
            print("IB client not connected, attempting to reconnect...")
            await connect_ib()
            if not ib.isConnected():
                raise HTTPException(status_code=500, detail="Unable to connect to IB")

        # Execute the place_order function within the IB event loop using asyncio
        result = await place_order()

        return {"status": result}

    except Exception as e:
        print(f"Error placing order: {e}")
        raise HTTPException(status_code=500, detail="Error placing order")

async def place_order():
    """Place an order using the IB API asynchronously."""
    try:
        # Define a stock contract
        contract = Stock('TQQQ', 'SMART', 'USD')
        await ib.qualifyContractsAsync(contract)  # Use the asynchronous version
        
        # Place a market order
        order = MarketOrder('BUY', 10)  # Example: 10 shares
        trade = ib.placeOrder(contract, order)
        print("Placed a buy order for SQQQ")
        return "Order placed successfully"
    except Exception as e:
        print(f"Error placing order: {e}")
        raise

