import pandas as pd
import yfinance as yf
from requests import HTTPError

# Give user 5 chances to enter correct symbol
max_chances = 5

# Take inputs until you get a correct symbol 5 max tries
while max_chances != 0:
    # Decrement chance
    max_chances -= 1

    # Input
    stock_symbol = input("Enter stock symbol: ")
    if stock_symbol.isalnum():
        try:
            stock_ticker = yf.Ticker(stock_symbol)
            # Attempt to access the 'info' attribute
            info = stock_ticker.info
            # If no error, the ticker exists
            print(f"Ticker '{stock_symbol}' exists.")
            print(f"Company name: {info['longName']}") if "longName" in info.keys()\
                else print(f"Company symbol: {info['symbol']}")
            break
        except HTTPError:
            # KeyError is thrown if the ticker doesn't exist
            print(f"Ticker '{stock_symbol}' does not exist.")
    else:
        print("Stock symbol incorrect.")
else:
    print("Exhausted max tries! Exiting!")
    exit(0)
