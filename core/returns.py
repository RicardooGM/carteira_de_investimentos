import numpy as np
import pandas as pd

def compute_returns(prices: pd.DataFrame, method="log"):
    """
    method:
        - 'log' : log-returns
        - 'simple' : simple returns
    """
    if method == "log":
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()

    return returns.dropna()


def annualized_return(returns: pd.DataFrame, periods_per_year=252):
    return returns.mean() * periods_per_year





