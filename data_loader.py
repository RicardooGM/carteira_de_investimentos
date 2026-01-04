import yfinance as yf
import pandas as pd
import numpy as np

def load_prices(tickers, start, end):
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False
    )

    # Sempre usar Close
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = tickers

    return prices.dropna(how="all")


def compute_returns(prices, method="log"):
    if method == "log":
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()

    return returns.dropna()

