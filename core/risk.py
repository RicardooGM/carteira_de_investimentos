import numpy as np
import pandas as pd

def volatility(returns: pd.DataFrame, periods_per_year=252):
    return returns.std() * np.sqrt(periods_per_year)


def covariance_matrix(returns: pd.DataFrame, periods_per_year=252):
    return returns.cov() * periods_per_year


def correlation_matrix(returns: pd.DataFrame):
    return returns.corr()
