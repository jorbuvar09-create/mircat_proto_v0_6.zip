import pandas as pd
import numpy as np

def liquidity_proxy(price: pd.Series, window: int = 15) -> pd.Series:
    # Proxy muy simple: rango intraventana (high-low) relativo al nivel de precio
    roll_max = price.rolling(window, min_periods=max(2, window//3)).max()
    roll_min = price.rolling(window, min_periods=max(2, window//3)).min()
    rng = (roll_max - roll_min) / price.replace(0, np.nan)
    return rng.fillna(0.0)


def roll_proxy(returns: pd.Series, window: int = 30) -> pd.Series:
    """Proxy de costo de transacción de Roll (simplificado):
    2*sqrt(-autocov(ret, ret_lag1)) cuando la autocov es negativa; si no, 0.
    """
    ret = returns
    lag1 = returns.shift(1)
    cov = (ret.rolling(window).mean() * lag1.rolling(window).mean())  # aproximación simple
    # Mejor: usar cov rolling directamente
    cov = ret.rolling(window).cov(lag1)
    val = (-cov).clip(lower=0)**0.5 * 2
    return val
