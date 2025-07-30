import requests
import pandas as pd
from datetime import datetime
import json

API_URL = "https://api.awattar.de/v1/marketdata"
FALLBACK_FILE = "data/last_prices.json"

def fetch_market_prices(timezone):
    """
    Fetches latest hourly electricity prices from the Awattar API.
    Returns a dictionary with success status and JSON-serializable data.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()['data']
        if not data:
            return {'success': False, 'error': "API returned no data."}

        df = pd.DataFrame(data)

        # Process data
        df['price_eur_kwh'] = df['marketprice'] / 1000
        df['start_time'] = pd.to_datetime(df['start_timestamp'], unit='ms', utc=True)

        # Sort by time and select future prices
        df = df.sort_values('start_time').reset_index(drop=True)
        now_utc = datetime.utcnow().replace(tzinfo=pd.Timestamp.utcnow().tz)
        df = df[df['start_time'] >= now_utc].copy()

        if df.empty:
            return {'success': False, 'error': "No future price data available."}

        # Create a list of dictionaries that is safe for JSON serialization.
        # Convert Timestamp objects to ISO format strings.
        prices_for_store = [{
            'start_time': ts.isoformat(),
            'price_eur_kwh': price
        } for ts, price in zip(df['start_time'], df['price_eur_kwh'])]

        return {
            'success': True,
            'prices': prices_for_store, # This is a JSON-serializable list of dicts
            'timestamp': datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
        }

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f"Network error: {e}"}
    except (KeyError, ValueError) as e:
        return {'success': False, 'error': f"Data processing error: {e}"}

def save_fallback_data(api_data):
    """Saves the successfully fetched data to a local JSON file."""
    try:
        with open(FALLBACK_FILE, 'w') as f:
            # The data is already serializable, so we can dump it directly.
            json.dump(api_data, f)
    except IOError:
        pass

def get_fallback_data():
    """Reads the last known data from the local JSON file."""
    try:
        with open(FALLBACK_FILE, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return None