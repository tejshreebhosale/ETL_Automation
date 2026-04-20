import os
from pathlib import Path

import pandas as pd


def ensure_sample_excel(path: str) -> None:
    file_path = Path(path)
    if file_path.exists():
        return

    rows = [
        {"order_id": 1, "amount": 100.0, "customer": "Alpha"},
        {"order_id": 2, "amount": 150.5, "customer": "Beta"},
        {"order_id": 2, "amount": 150.5, "customer": "Beta"},
        {"order_id": 3, "amount": None, "customer": "Gamma"},
        {"order_id": None, "amount": 50.0, "customer": None},
    ]
    df = pd.DataFrame(rows)

    os.makedirs(file_path.parent, exist_ok=True)
    df.to_excel(file_path, index=False)


def read_excel(path: str) -> pd.DataFrame:
    return pd.read_excel(path)


def write_excel(df: pd.DataFrame, path: str) -> None:
    output_path = Path(path)
    os.makedirs(output_path.parent, exist_ok=True)
    df.to_excel(output_path, index=False)
