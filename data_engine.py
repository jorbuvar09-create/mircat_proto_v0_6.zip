import pandas as pd
from pathlib import Path

def load_prices(csv_path: str) -> pd.DataFrame:
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")
    df = pd.read_csv(p)
    # Validación mínima
    expected = {"t", "price", "ret"}
    if not expected.issubset(df.columns):
        raise ValueError(f"Columnas esperadas {expected}, encontradas {set(df.columns)}")
    return df
