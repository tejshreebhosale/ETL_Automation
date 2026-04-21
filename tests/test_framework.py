import json
import pandas as pd
import pytest
from src.validations.validator import run_validations
from utils.logger import get_logger

logger = get_logger()


def load_metadata():
    with open("metadata/tables.json") as f:
        return json.load(f)


@pytest.mark.parametrize("table", load_metadata())
def test_table_validations(table):
    table_name = table["table_name"]
    source = table["source"]

    logger.info(f"Processing table: {table_name}")

    df = pd.read_excel(source)

    results = run_validations(df)

    logger.info(f"{table_name} | Row Count: {results['row_count']}")
    logger.info(f"{table_name} | Null Count: {results['null_count']}")
    logger.info(f"{table_name} | Duplicate Count: {results['duplicate_count']}")

    # Assertions
    if not table.get("allow_empty", False):
        assert results["row_count"] > 0, f"{table_name}: No data found"

    assert results["null_count"] <= table.get("null_threshold", 0), (
        f"{table_name}: Nulls exceed threshold ({results['null_count']})"
    )

    assert results["duplicate_count"] <= table.get("duplicate_threshold", 0), (
        f"{table_name}: Duplicates exceed threshold ({results['duplicate_count']})"
    )