# TradingView-IB Bridge

A webhook bridge that connects TradingView alerts to Interactive Brokers for automated trade execution. TradingView strategy signals are received via a FastAPI webhook server and forwarded as live orders to IB Gateway/TWS.

## Architecture

```
TradingView Alert ──> Ngrok ──> FastAPI Webhook Server ──> Interactive Brokers API
```

- **Backend**: FastAPI server with async IB connection management via `ib_insync`
- **Frontend**: React app using `lightweight-charts` to display candlestick data from the backend
- **Strategy**: Included PineScript moving average crossover strategy that generates buy/sell signals

## Project Structure

```
backend/
  main.py               # FastAPI server with webhook handler and IB order execution
  get_data.py            # Historical data fetcher from IB
  ib_insync_simple.py    # Standalone IB order placement example
  ma_cross.pinescript    # Moving average crossover TradingView strategy
  alert.json             # TradingView webhook alert JSON template
frontend/
  lightweight-charts-app/ # React app for candlestick chart visualization
```

## Prerequisites

- Python 3.7+
- Node.js (for the frontend)
- [IB Gateway or Trader Workstation (TWS)](https://www.interactivebrokers.com/en/trading/tws.php) running with API access enabled
- [Ngrok](https://ngrok.com/) for exposing the local server to TradingView webhooks

## Setup

### 1. Install Backend Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn ib_insync
```

### 2. Configure IB Gateway/TWS

- Enable **ActiveX and Socket Clients** in API settings
- Disable **Read-Only API**
- Set socket port to `7497` (paper trading) or `7496` (live)

### 3. Start the Server

```bash
cd backend
uvicorn main:app --reload --port 80
```

### 4. Expose via Ngrok

```bash
ngrok http 80
```

### 5. Configure TradingView Alerts

Set the webhook URL in your TradingView alert to your Ngrok URL:

```
https://<your-domain>.ngrok-free.app/webhook
```

Use this JSON payload in the alert message:

```json
{
  "action": "{{strategy.order.action}}",
  "ticker": "{{ticker}}",
  "quantity": 10
}
```

### 6. Start the Frontend (Optional)

```bash
cd frontend/lightweight-charts-app
npm install
npm start
```

## Webhook API

**POST** `/webhook`

| Field      | Type   | Description                          |
|------------|--------|--------------------------------------|
| `action`   | string | `buy` or `sell`                      |
| `ticker`   | string | Stock symbol (e.g., `AAPL`)          |
| `quantity` | int    | Number of shares (default: 10)       |

Example:

```bash
curl -X POST http://localhost:80/webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "buy", "ticker": "AAPL", "quantity": 10}'
```

## Tech Stack

- **FastAPI** - Async web framework for the webhook server
- **ib_insync** - Async Python wrapper for the Interactive Brokers API
- **React** - Frontend UI
- **Lightweight Charts** - TradingView's charting library for candlestick visualization
- **Ngrok** - Tunnel for exposing the local server to the internet
