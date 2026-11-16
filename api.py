import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_URL = "https://www.alphavantage.co/query"


class StockDataError(Exception):
    """Raised when stock data cannot be retrieved or processed."""


def get_api_key():
    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not key:
        raise StockDataError(
            "No API key found. Set ALPHAVANTAGE_API_KEY in your environment "
            "or add it to a local .env file."
        )
    return key


def fetch_stock_data(symbol, function):
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": get_api_key(),
    }
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = "60min"
        params["outputsize"] = "full"
    elif function == "TIME_SERIES_DAILY":
        params["outputsize"] = "full"

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise StockDataError(
            f"Network problem contacting Alpha Vantage: {exc}"
        ) from exc
    except ValueError as exc:
        raise StockDataError(
            "Alpha Vantage returned data that was not valid JSON."
        ) from exc

    if "Error Message" in payload:
        raise StockDataError(
            f"Alpha Vantage rejected the request: {payload['Error Message']}"
        )
    for note_key in ("Note", "Information"):
        if note_key in payload:
            raise StockDataError(f"Alpha Vantage message: {payload[note_key]}")

    for key, value in payload.items():
        if key.startswith(("Time Series", "Weekly", "Monthly")):
            return value
    raise StockDataError("No time series data found in the response.")


def filter_by_date(series, start, end):
    rows = []
    for timestamp, values in series.items():
        day = timestamp[:10]
        if str(start) <= day <= str(end):
            rows.append((timestamp, {
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
            }))
    rows.sort(key=lambda row: row[0])
    if not rows:
        raise StockDataError("No data available for that date range.")
    return rows
