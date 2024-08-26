import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

def get_crypto_symbols():
    url = f"https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to fetch crypto symbols: {response.status_code}")
        return []

def find_matching_symbol(base, quote):
    symbols = get_crypto_symbols()
    for symbol in symbols:
        if symbol['displaySymbol'] == f"{base}/{quote}":
            return symbol['symbol']
    return None

def get_finnhub_crypto_data(base, quote):
    try:
        symbol = find_matching_symbol(base, quote)
        if not symbol:
            logger.error(f"No matching symbol found for {base}/{quote}")
            return None

        base_url = "https://finnhub.io/api/v1/crypto/candle"
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=30)).timestamp())
        
        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": start_time,
            "to": end_time,
            "token": FINNHUB_API_KEY
        }
        logger.info(f"Fetching Finnhub crypto data for symbol: {symbol}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['s'] == 'ok':
            df = pd.DataFrame({
                'Open': data['o'],
                'High': data['h'],
                'Low': data['l'],
                'Close': data['c'],
                'Volume': data['v']
            }, index=pd.to_datetime(data['t'], unit='s'))
            
            return df
        else:
            logger.error(f"Error fetching Finnhub crypto data: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        logger.error(f"Error fetching Finnhub crypto data: {e}")
        return None

def get_finnhub_forex_data(symbol):
    try:
        base_url = "https://finnhub.io/api/v1/forex/candle"
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=30)).timestamp())
        
        # Convert symbol to OANDA format
        oanda_symbol = f"OANDA:{symbol.replace('/', '_')}"
        
        params = {
            "symbol": oanda_symbol,
            "resolution": "D",
            "from": start_time,
            "to": end_time,
            "token": FINNHUB_API_KEY
        }
        logger.info(f"Fetching Finnhub forex data for symbol: {oanda_symbol}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['s'] == 'ok':
            df = pd.DataFrame({
                'Open': data['o'],
                'High': data['h'],
                'Low': data['l'],
                'Close': data['c'],
                'Volume': data['v']
            }, index=pd.to_datetime(data['t'], unit='s'))
            
            # Round all price columns to 5 decimal places
            price_columns = ['Open', 'High', 'Low', 'Close']
            df[price_columns] = df[price_columns].round(5)
            
            return df
        else:
            logger.error(f"Error fetching Finnhub forex data: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        logger.error(f"Error fetching Finnhub forex data: {e}")
        return None

def get_data(symbol):
    if '-' in symbol:  # Crypto pair
        base, quote = symbol.split('-')
        return get_finnhub_crypto_data(base, quote)
    elif '/' in symbol:  # Forex pair
        return get_finnhub_forex_data(symbol)
    else:  # Other assets (not implemented yet)
        logger.error(f"Data fetching for {symbol} is not implemented yet.")
        return None