import pandas as pd
import yfinance as yf

# List of selected stocks
stocks_list = list()

# Flag to check if any incorrect symbol given
enter_again = True

# Choice for manual input or top 5
choice = input("1 To Enter Stock Symbols Separated by a White Space\
\n2 To Select Current Top 'x' Largest Companies by Market Cap\
\nAny Other Key To Exit\
\nEnter: ")

if choice == "1":
    # Input
    while enter_again:
        stock_symbols = input("Enter Stock Symbols: ")
        if stock_symbols:
            incorrect_symbols = False
            for symbol in stock_symbols.split(" "):
                try:
                    # Attempt to access the 'info' attribute
                    info = yf.Ticker(symbol).info
                    stocks_list.append(symbol) if symbol not in stocks_list else None
                except:
                    # Error is thrown if the ticker doesn't exist
                    print(f"Ticker '{symbol}' does not exist.")
                    incorrect_symbols = True

            if incorrect_symbols:
                # Inform user to re-enter stock symbols
                print("Current selected symbols: ", end="")
                print(*stocks_list, sep=", ")
                print("Please re-enter the incorrect stock symbols.")
            else:
                # All symbols are correct, prepare to exit the loop
                enter_again = False
        else:
            # No more symbols to enter, prepare to exit the loop
            enter_again = False

    # After exiting the loop, print the final set of valid stock symbols, if it exists
    if stocks_list:
        print("Final selected symbols: ", end="")
        print(*stocks_list, sep=', ', end='.\n')
    else:
        print("No symbols selected. Exiting!")
        exit(0)
elif choice == "2":
    enter_again = True
    while enter_again:
        top_x = input(f"Enter The Count of Top Companies to Select ('x'): ")
        if top_x.isnumeric():
            enter_again = False
        elif not top_x:
            print("No symbols selected. Exiting!")
            exit(0)
        else:
            print("Wrong Input!")

    # URL to scrape data from
    url = "https://stockanalysis.com/list/biggest-companies/"

    # Pass a user-agent as it does not allow us to scrape otherwise
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"}

    dfs = pd.read_html(url, storage_options=headers, index_col="No.")

    # Selecting top 5 from the first table on page
    usa_top_5 = dfs[0].head(int(top_x))
    stocks_list.extend(list(usa_top_5["Symbol"]))
    print("Final selected symbols: ", end="")
    print(*stocks_list, sep=', ', end='.\n')

else:
    print("Exiting!")
    exit(0)
