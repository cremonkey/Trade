import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TWELVEDATA_API_KEY")

def test_symbol(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={api_key}"
    r = requests.get(url)
    print(f"Symbol {symbol}: {r.json()}")

test_symbol("SLV")
test_symbol("SIL") # Global X Silver Miners ETF
test_symbol("SILJ") # Junior Silver Miners
