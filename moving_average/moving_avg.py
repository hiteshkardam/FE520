# Moving average module

import matplotlib.pyplot as plt
import yfinance as yf


# SMA Calculation
def calculate_sma(prices, window):
    # Empty list with 'None' values
    sma = [None] * (window - 1)
    # Calculate SMA
    for i in range(window - 1, len(prices)):
        sma.append(sum(prices[i - window + 1:i + 1]) / window)
    return sma


# EMA Calculation
def calculate_ema(prices, span):
    # Empty list with First Value
    ema = [prices[0]]
    # Define multiplier
    multiplier = 2 / (span + 1)
    # Calculate EMA
    for price in prices[1:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema


# Plot Moving Averages
def plot_moving_avg(tickers, start_date, end_date):
    # Define subplot grid
    num_tickers = len(tickers)
    # Define number of columns
    num_columns = 2
    # Calculate rows
    num_rows = num_tickers // num_columns + (num_tickers % num_columns > 0)
    # Plotting Canvas
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(8 * num_columns, 3 * num_rows))
    # Flatten
    axs = axs.flatten()

    # Initialize a counter for plotting
    plot_count = 0

    # Fetch data and perform calculations for each ticker
    for ticker in tickers:
        # Download stock data from yfinance
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        print(f"Downloading data for {ticker}")
        # Define window size
        window_size = 20
        # Start plotting
        if not data.empty:
            # Convert to list
            close_prices = data['Close'].tolist()
            if close_prices:
                data['SMA'] = calculate_sma(close_prices, window=20)
                data['EMA'] = calculate_ema(close_prices, span=20)
                # Plot location
                ax = axs[plot_count]
                ax.plot(data.index, data['Close'], label='Close Price')
                ax.plot(data.index, data['SMA'], label=f'{window_size}-Day SMA')
                ax.plot(data.index, data['EMA'], label=f'{window_size}-Day EMA')
                ax.set_title(f"{ticker} Stock Price with {window_size}-Day SMA and EMA", fontsize=10)
                ax.set_xlabel('Date', fontsize=8)
                ax.set_ylabel('Price', fontsize=8)
                ax.legend(fontsize=8)
                plot_count += 1
        else:
            print(f"Data for {ticker} is not available or the ticker is invalid.")

    # Adjust layout and set a main title
    plt.tight_layout()
    plt.suptitle('Stock Price Plots with SMA and EMA')

    # Show plot
    plt.show()
