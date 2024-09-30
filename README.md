# FastAPI Interactive Brokers Integration

This project integrates FastAPI with the Interactive Brokers (IB) API to handle webhook requests and place buy/sell orders asynchronously.

## Prerequisites

- Python 3.7+
- `ib_insync` library
- `fastapi` library
- `uvicorn` server
- Ngrok (to expose your local server to the internet)
- An active IB Gateway or Trader Workstation (TWS) running and configured for API access.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Activate the environment (Windows)
   venv\Scripts\activate
   # Activate the environment (macOS/Linux)
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes:

   ```
   fastapi
   uvicorn
   ib_insync
   ```

4. Install Ngrok from the [official website](https://ngrok.com/download) and set it up.

## Setting up Trader Workstation (TWS)

Ensure that your IB Gateway or TWS is running and accessible on `localhost` at port `7497`:

- Download and install TWS from the [official website](https://www.interactivebrokers.com/en/index.php?f=16040).
- Open IB Gateway/TWS and configure the API settings:
  - Check "Enable ActiveX and Socket Clients"
  - Uncheck "Read-Only API"
  - Set the port to `7497` for paper trading.

## Running the Application

You **must** run the FastAPI server on port 80, and expose it to the internet using Ngrok.

### Start the FastAPI Server

```bash
uvicorn main:app --reload --port 80
```

- Replace `main` with your actual script name if it's different.

### Start Ngrok

In a separate terminal window, run:

```bash
ngrok http 80
```

- Ngrok will provide a URL (e.g., `http://abc123.ngrok.io`) that exposes your local server to the internet.

## Setting up Trading Alerts on TradingView

1. Open [TradingView](https://www.tradingview.com/) and log in to your account.
2. Set up your trading chart and indicators as usual.
3. Click the "Alert" button (or right-click on the chart and choose "Add Alert").
4. In the alert configuration window, choose your desired conditions.
5. Set the "Webhook URL" to the Ngrok URL you obtained earlier, with the `/webhook` endpoint, for example:
   ```
   http://abc123.ngrok.io/webhook
   ```
6. For the "Alert Action" message, use a JSON payload like the example below to specify the trading action:
   ```json
   {
     "action": "{{strategy.order.action}}",
     "ticker": "{{ticker}}",
     "price": "{{close}}"
   }
   ```
   Adjust `action`, `ticker`, and `quantity` as needed.

## Webhook Endpoint

The server exposes a `/webhook` endpoint that accepts POST requests with the following JSON payload:

### JSON Payload Example

```json
{
  "action": "buy",
  "ticker": "AAPL",
  "price": "10.0"
}
```

- `action`: `buy` or `sell`
- `ticker`: The stock symbol (e.g., `AAPL` for Apple)
- `price`: The price of shares to trade at

### Sample Request

You can test the endpoint using `curl` or tools like Postman:

```bash
curl -X POST "http://abc123.ngrok.io/webhook" -H "Content-Type: application/json" -d '{"action": "buy", "ticker": "AAPL", "quantity": 10}'
```

## Shutting Down

To stop the server, press `CTRL + C` in the terminal where `uvicorn` and `ngrok` are running.
