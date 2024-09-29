from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from ib_insync import *
import asyncio

# Initialize the Interactive Brokers client
ib = IB()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to IB when FastAPI starts
    try:
        await ib.connectAsync('127.0.0.1', 7497, clientId=1)
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
async def webhook():
    """Handle incoming webhook requests and place an order asynchronously."""
    try:
        # Check if the IB client is connected, reconnect if not
        if not ib.isConnected():
            print("IB client not connected, attempting to reconnect...")
            await ib.connectAsync('127.0.0.1', 7497, clientId=1)
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
        contract = Stock('SQQQ', 'SMART', 'USD')
        await ib.qualifyContractsAsync(contract)  # Use the asynchronous version
        
        # Place a market order
        order = MarketOrder('BUY', 10)  # Example: 10 shares
        trade = ib.placeOrder(contract, order)
        print("Placed a buy order for SQQQ")
        return "Order placed successfully"
    except Exception as e:
        print(f"Error placing order: {e}")
        raise
