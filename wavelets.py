import numpy as np
import pandas as pd
from scipy.signal import cwt, ricker

def wavelet_energy(series: pd.Series, widths=(2,4,8,16,32)) -> pd.DataFrame:
    """Calcula energía por escala usando CWT (Ricker). Devuelve DataFrame con columnas E_scale{w}."""
    x = series.fillna(0).values
    coef = cwt(x, ricker, widths)
    # Energía por escala = promedio de coeficientes^2
    data = {}
    for i, w in enumerate(widths):
        e = (coef[i]**2)
        data[f"E_scale{w}"] = pd.Series(e, index=series.index)
    return pd.DataFrame(data)


def wavelet_scalogram(series: pd.Series, widths=(2,4,8,16,32,64)):
    # Devuelve matriz coeficientes^2 (energía) [len(widths) x T]
    x = series.fillna(0).values
    from scipy.signal import cwt, ricker
    coef = cwt(x, ricker, widths)
    power = coef**2
    return power, list(widths)
