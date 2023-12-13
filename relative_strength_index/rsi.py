# RSI module

import matplotlib.pyplot as plt
import yfinance as yf

# RSI is a momentum indicator used in technical analysis
# that measures the magnitude of recent price changes
# to evaluate overbought or oversold conditions.


# Function to compute RSI
def compute_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def plot_rsi(tickers, start_date, end_date):
    # Define subplot grid
    num_tickers = len(tickers)
    num_columns = 2
    num_rows = num_tickers // num_columns + (num_tickers % num_columns > 0)
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(8 * num_columns, 3 * num_rows), squeeze=False)

    # Flatten the axs array for easy indexing
    axs = axs.flatten()

    # Fetch data and plot RSI for each ticker
    for i, ticker in enumerate(tickers):
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        print(f"Downloading data for {ticker}")

        data['RSI'] = compute_rsi(data['Close'])

        ax = axs[i]
        ax.plot(data.index, data['RSI'], label=f'{ticker} RSI', linewidth=1)
        ax.axhline(70, color='red', linestyle='--', linewidth=0.5)
        ax.axhline(30, color='green', linestyle='--', linewidth=0.5)
        ax.legend(loc='upper left', fontsize=8)
        ax.set_title(f'{ticker} RSI', fontsize=10)
        ax.set_xlabel('Date', fontsize=8)
        ax.set_ylabel('RSI', fontsize=8)

    # Adjust layout and set a main title
    plt.tight_layout()
    plt.suptitle('Relative Strength Index Graphs')

    # Show plot
    plt.show()
