import pandas as pd
import numpy as np

def rolling_corr(x: pd.Series, y: pd.Series, window: int = 30) -> pd.Series:
    # Correlación rolling como indicador de propagación
    df = pd.concat([x, y], axis=1).dropna()
    if df.shape[1] != 2:
        return pd.Series(index=x.index, dtype=float)
    c = df[x.name].rolling(window, min_periods=max(2, window//3)).corr(df[y.name])
    return c.reindex(x.index)
