import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.drop_duplicates().copy()
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce").fillna(0.0)
    cleaned["order_id"] = cleaned["order_id"].fillna("unknown")
    cleaned["customer"] = cleaned["customer"].fillna("unknown")
    cleaned["total_amount"] = cleaned["amount"] * 1.1
    return cleaned
