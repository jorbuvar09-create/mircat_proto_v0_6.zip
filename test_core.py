import pandas as pd
import numpy as np
from pathlib import Path

from modules.data_engine import load_prices
from modules.core import compute_features

def test_load_prices_schema():
    df = load_prices(str(Path("data")/"sample_prices.csv"))
    assert set(["t","price","ret"]).issubset(df.columns)

def test_compute_features_shapes():
    df = load_prices(str(Path("data")/"sample_prices.csv"))
    feat = compute_features(df, win=30)
    # Debe incluir columnas clave
    for col in ["vol_local","burst","liq_proxy","prop_corr","liq_roll"]:
        assert col in feat.columns
    assert len(feat) == len(df)

def test_no_nan_after_fill():
    df = load_prices(str(Path("data")/"sample_prices.csv"))
    feat = compute_features(df, win=30)
    # Permitir NaN en los primeros puntos por rolling, pero no en exceso
    nan_rate = feat.isna().mean().mean()
    assert nan_rate < 0.5  # criterio laxo para prototipo


def test_schema_and_connector():

    from connectors.csv_connector import load_with_schema

    from pathlib import Path

    df = load_with_schema(str(Path("data")/"sample_prices.csv"), str(Path("schemas")/"data_contract.yaml"))

    assert set(["t","price","ret","volume"]).issubset(df.columns)

