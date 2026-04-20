import pytest
import allure
import json
from src.engine.runner import load_data
from src.validations.validator import validate_all
from src.validations.comparator import compare_data


with open("metadata/tables.json") as f:
    tables = json.load(f)


@pytest.mark.parametrize("table", tables)
def test_elt(table):
    table_name = table.get("table_name")
    table_type = table.get("type", "excel")

    with allure.step(f"Processing table: {table_name}"):

        data = load_data(table, {})

        # 🔁 Comparison
        if table_type == "excel_compare":
            source_df, target_df = data

            results, mismatch_df = compare_data(
                source_df,
                target_df,
                table["primary_key"],
                table.get("tolerance", {})
            )

            for r in results:
                with allure.step(f"{r[0]} check"):
                    assert r[1] == "PASS", f"{r[0]} failed: {r[2]}"

            # 📎 Attach mismatch file
            if not mismatch_df.empty:
                allure.attach(
                    mismatch_df.to_csv(index=False),
                    name="Mismatch Data",
                    attachment_type=allure.attachment_type.CSV
                )

        else:
            df = data
            results = validate_all(df)

            for r in results:
                with allure.step(f"{r['validation']} check"):
                    assert r["status"] == "PASS", f"{r['validation']} failed: {r['value']}"