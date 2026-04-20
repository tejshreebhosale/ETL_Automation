import pandas as pd


def has_minimum_rows(df: pd.DataFrame, min_rows: int = 1) -> bool:
    return len(df) >= min_rows

def count_nulls(df: pd.DataFrame) -> int:
    return int(df.isnull().sum().sum())

def count_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())

def null_check(df):
    return df.isnull().sum().sum()

def duplicate_check(df):
    return df.duplicated().sum()

def row_count(df):
    return len(df)

def run_validations(df):
    return {
        "row_count": row_count(df),
        "null_count": null_check(df),
        "duplicate_count": duplicate_check(df),
    }

def validate_all(df):
    results = []

    row_count = len(df)
    results.append({"validation": "row_count", "value": row_count, "status": "PASS" if row_count > 0 else "FAIL"})

    null_count = df.isnull().sum().sum()
    results.append({"validation": "null_check", "value": null_count, "status": "FAIL" if null_count > 0 else "PASS"})

    dup_count = df.duplicated().sum()
    results.append({"validation": "duplicate_check", "value": dup_count, "status": "FAIL" if dup_count > 0 else "PASS"})

    return results