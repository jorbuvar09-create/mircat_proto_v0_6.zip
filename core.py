import pandas as pd
import numpy as np
from .volatility import rolling_volatility, burst_index
from .liquidity import liquidity_proxy
from .wavelets import wavelet_energy, wavelet_scalogram
from .liquidity import roll_proxy
from .liquidity_advanced import parkinson_vol, amihud_illiq

from .propagation import rolling_corr

def micro_windows(df: pd.DataFrame, win: int = 30, step: int = 15):
    # Genera índices de microtramos (ventanas deslizantes)
    idx = []
    i = 0
    n = len(df)
    while i + win <= n:
        idx.append((i, i+win))
        i += step
    return idx

def compute_features(df: pd.DataFrame, win: int = 30):
    feat = pd.DataFrame(index=df.index.copy())
    feat["vol_local"] = rolling_volatility(df["ret"], window=win)
    feat["burst"] = burst_index(df["ret"], window=win)
    feat["liq_proxy"] = liquidity_proxy(df["price"], window=max(5, win//2))
    # "Propagación" ficticia: correlación del retorno con su lag (autocorr rolling)
    feat["ret_lag1"] = df["ret"].shift(1)
    feat["prop_corr"] = rolling_corr(df["ret"].rename("ret"),
                                     feat["ret_lag1"].rename("ret_lag1"),
                                     window=win)


    # Energía wavelet multi-escala sobre retornos

    wdf = wavelet_energy(df["ret"].fillna(0))

    for c in wdf.columns:

        feat[c] = wdf[c]

    # Liquidez adicional: Roll proxy

    feat["liq_roll"] = roll_proxy(df["ret"], window=max(5, win//2))

    # Volatilidad de Parkinson y Amihud illiquidity

    if "high" in df.columns and "low" in df.columns:

        feat["parkinson"] = parkinson_vol(df["high"], df["low"], window=max(5, win//2))

    if "volume" in df.columns:

        feat["amihud"] = amihud_illiq(df["ret"], df["volume"], window=max(5, win//2))



    return feat

def classify_microtramo(feat_row: pd.Series,
                        thr_burst: float = 1.5,
                        thr_liq: float = 0.01,
                        thr_prop: float = 0.2):
    # Clasificación simple basada en umbrales
    if pd.isna(feat_row).any():
        return "indeterminado"
    burst = feat_row.get("burst", 0.0)
    liq = feat_row.get("liq_proxy", 0.0)
    prop = abs(feat_row.get("prop_corr", 0.0))
    # Reglas: si hay simultáneamente alta burst + baja liquidez + alta propagación → pre-ruptura
    if (burst >= thr_burst) and (liq >= thr_liq) and (prop >= thr_prop):
        return "pre-ruptura"
    if (burst >= thr_burst) or (liq >= thr_liq) or (prop >= thr_prop):
        return "benigno"
    return "normal"
