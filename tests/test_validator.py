import pandas as pd
from src.validations import validator
from utils.logger import get_logger

logger = get_logger()

def test_null_check():
    """Validate null values from Excel"""
    df = pd.read_excel("data/sample_sales.xlsx")

    result = validator.null_check(df)

    logger.info(f"Null count: {result}")

    assert result > 0, "Expected null values but none found"


def test_duplicate_check():
    """Validate duplicates from Excel"""
    df = pd.read_excel("data/sample_sales.xlsx")

    result = validator.duplicate_check(df)

    logger.info(f"Duplicate count: {result}")

    assert result > 0, "Expected duplicates but none found"