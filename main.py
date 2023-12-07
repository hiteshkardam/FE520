import pandas as pd
import yfinance as yf

# Give user 5 chances to enter correct symbol
max_chances = 5

# Choice for manual input or top 5
choice = int(input("1 to Enter Stock Symbol\
\n2 to Select Top 5 Largest Companies by Market Cap\
\n3 to Exit\
\nEnter: "))

if choice == 1:
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
            except:
                # KeyError is thrown if the ticker doesn't exist
                print(f"Ticker '{stock_symbol}' does not exist.")
        else:
            print("Stock symbol incorrect.")
    else:
        print("Exhausted max tries! Exiting!")
        exit(0)
elif choice == 2:
    # Pass a user-agent as it does not allow us to scrape otherwise
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"}

    # URL to scrape from
    url = "https://stockanalysis.com/list/biggest-companies/"
    dfs = pd.read_html(url, storage_options=headers, index_col="No.")

    # Selecting top 5 from the first table
    usa_top_5 = dfs[0].head(5)
    print(usa_top_5)
else:
    print("Exiting!")
    exit(0)
