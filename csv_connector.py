import pandas as pd
from pathlib import Path
import yaml

def load_with_schema(csv_path: str, schema_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    with open(schema_path, 'r') as f:
        schema = yaml.safe_load(f)
    req = schema["entities"]["price_series"]["required_columns"]
    for col in req:
        if col not in df.columns:
            raise ValueError(f"Falta columna requerida: {col}")
    return df
