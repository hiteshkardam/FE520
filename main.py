# Import Builtin Python Modules
import pandas as pd
import yfinance as yf
import datetime

# Import User Defined Python Modules
from moving_average.moving_avg import plot_moving_avg
from relative_strength_index.rsi import plot_rsi

# List of selected stocks
stocks_list = list()


def ticker_choice():
    # Flag to check if any incorrect symbol given
    enter_again = True

    # Choice for manual input or top 5
    choice = input("1 To Enter Stock Symbols Separated by a White Space\
    \n2 To Fetch Top 'x' Largest Companies by Market Cap\
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
                        yf.Ticker(symbol).info
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
        # While loop flag
        enter_again = True
        # Input for x
        top_x = None
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

        # Scraped Table to Dataframe
        dfs = pd.read_html(url, storage_options=headers, index_col="No.")

        # Selecting top 5 from the first table on page
        usa_top_5 = dfs[0].head(int(top_x))
        # Add to stocks_list
        stocks_list.extend(list(usa_top_5["Symbol"]))
        print("Final selected symbols: ", end="")
        print(*stocks_list, sep=', ', end='.\n')

    else:
        print("Exiting!")
        exit(0)


if __name__ == "__main__":
    start_date = None
    end_date = None

    # Ticker selection
    ticker_choice()

    while True:
        # Plot selection
        choice = input("\n1 To Show 20-Day EMA and SMA Plots\
                        \n2 To Show RSI Plots\
                        \nAny Other Key To Exit\
                        \nEnter: ")

        try:
            # Try converting the string to an integer
            val = int(choice)
            if choice == "1" or choice == "2":
                break
            else:
                print("Exiting!")
                exit(0)
        except:
            print("Exiting!")
            exit(0)

    while True:
        # Dates selection
        start_date = input("Enter Start Date (yyyy-mm-dd): ")
        end_date = input("Enter End Date (yyyy-mm-dd): ")

        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

                if end_date > start_date:
                    print(f"Selected Start Date: {start_date.date()} and End Date: {end_date.date()}")
                    break
                else:
                    print("End Date < Start Date!")
            except:
                print("Please Input Dates in Correct Format!")
        else:
            print("Please Input Dates")

    if choice == "1":
        print("Plotting Moving Average Graphs")
        plot_moving_avg(stocks_list, start_date, end_date)
    elif choice == "2":
        print("Plotting Relative Strength Index Graphs")
        plot_rsi(stocks_list, start_date, end_date)
