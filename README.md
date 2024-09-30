
# FastAPI Interactive Brokers Integration

This project integrates FastAPI with the Interactive Brokers (IB) API to handle webhook requests and place buy/sell orders asynchronously.

## Prerequisites
- Python 3.7+
- `ib_insync` library
- `fastapi` library
- `uvicorn` server
- `ibapi` library (for direct IB API access)
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
   ibapi
   ```

4. Install the `ibapi` library separately (if not included in your `requirements.txt`):
   ```bash
   pip install ibapi
   ```

## Setting up Trader Workstation (TWS)

Ensure that your IB Gateway or TWS is running and accessible on `localhost` at port `7497`:
- Download and install TWS from the [official website](https://www.interactivebrokers.com/en/index.php?f=16040).
- Open IB Gateway/TWS and configure the API settings:
  - Check "Enable ActiveX and Socket Clients"
  - Uncheck "Read-Only API"
  - Set the port to `7497` for paper trading.

## Running the Application

Start the FastAPI server using `uvicorn`:
```bash
uvicorn main:app --reload --port 8000
```
- Replace `main` with your actual script name if it's different.
- Replace `8000` with your preferred port.

## Webhook Endpoint

The server exposes a `/webhook` endpoint that accepts POST requests with the following JSON payload:

### JSON Payload Example
```json
{
    "action": "buy",
    "ticker": "AAPL",
    "quantity": 10
}
```
- `action`: `buy` or `sell`
- `ticker`: The stock symbol (e.g., `AAPL` for Apple)
- `quantity`: The number of shares to trade

### Sample Request
You can test the endpoint using `curl` or tools like Postman:
```bash
curl -X POST "http://127.0.0.1:8000/webhook" -H "Content-Type: application/json" -d '{"action": "buy", "ticker": "AAPL", "quantity": 10}'
```

## Debugging & Troubleshooting

- Check the console output for connection and order placement logs.
- Ensure that your IB Gateway/TWS is running and the port is accessible.

## Shutting Down

To stop the server, press `CTRL + C` in the terminal where `uvicorn` is running.

## License
This project is licensed under the MIT License.
