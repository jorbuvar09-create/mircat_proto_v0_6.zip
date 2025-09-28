import pandas as pd
import numpy as np

def parkinson_vol(high: pd.Series, low: pd.Series, window: int = 30) -> pd.Series:
    # Volatilidad de Parkinson (alta-baja), sin anualizar
    # sigma^2 = (1/(4*ln(2))) * mean(ln(H/L)^2) sobre la ventana
    import numpy as np
    ln_hl = np.log((high / low).clip(lower=1e-12))
    pv = (ln_hl**2).rolling(window, min_periods=max(2, window//3)).mean()
    return (pv / (4*np.log(2))).pow(0.5)

def amihud_illiq(returns: pd.Series, volume: pd.Series, window: int = 30) -> pd.Series:
    # Amihud (|ret| / volumen) promedio rolling como proxy de iliquidez
    illiq = (returns.abs() / volume.replace(0, np.nan)).rolling(window, min_periods=max(2, window//3)).mean()
    return illiq
