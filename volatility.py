import pandas as pd
import numpy as np

def rolling_volatility(returns: pd.Series, window: int = 30) -> pd.Series:
    # Volatilidad local (desv. estándar rolling). Escala anual (supuesto 252*días).
    ann = np.sqrt(252)
    return returns.rolling(window, min_periods=max(2, window//3)).std() * ann

def burst_index(returns: pd.Series, window: int = 30) -> pd.Series:
    # Índice simple de "burst": |ret| relativo a su media rolling
    mu = returns.rolling(window, min_periods=max(2, window//3)).mean()
    sd = returns.rolling(window, min_periods=max(2, window//3)).std()
    z = (returns - mu) / (sd.replace(0, np.nan))
    return z.abs()
