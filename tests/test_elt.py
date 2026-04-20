import pytest
import allure
import json
from src.engine.runner import load_data
from src.validations.validator import validate_all
from src.validations.comparator import compare_data


# Load metadata once
with open("metadata/tables.json") as f:
    tables = json.load(f)


@pytest.mark.parametrize("table", tables)
def test_elt(table):

    table_name = table.get("table_name")
    table_type = table.get("type", "excel")

    # Rule controls
    strict = table.get("strict", False)
    null_threshold = table.get("null_threshold", 0)
    duplicate_threshold = table.get("duplicate_threshold", 0)

    with allure.step(f"Processing table: {table_name}"):

        data = load_data(table, {})

        # =========================
        # EXCEL COMPARE LOGIC
        # =========================
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

                    # Fail only when validation fails
                    if r[1] != "PASS":
                        assert False, f"{r[0]} failed: {r[2]}"

            # Attach mismatch data if present
            if mismatch_df is not None and not mismatch_df.empty:
                allure.attach(
                    mismatch_df.to_csv(index=False),
                    name="Mismatch Data",
                    attachment_type=allure.attachment_type.CSV
                )

        # =========================
        # STANDARD EXCEL VALIDATION
        # =========================
        else:

            df = data
            results = validate_all(df)

            for r in results:
                with allure.step(f"{r['validation']} check"):

                    validation_name = r["validation"]
                    status = r["status"]
                    value = r["value"]

                    # STRICT MODE (production-grade validation)
                    if strict:
                        assert status == "PASS", f"{validation_name} failed: {value}"

                    # THRESHOLD MODE (flexible validation)
                    else:

                        if validation_name == "null_check":
                            assert value <= null_threshold, (
                                f"{table_name}: Nulls exceed threshold. Found={value}, Allowed={null_threshold}"
                            )

                        elif validation_name == "duplicate_check":
                            assert value <= duplicate_threshold, (
                                f"{table_name}: Duplicates exceed threshold. Found={value}, Allowed={duplicate_threshold}"
                            )

                        else:
                            # fallback for other validations
                            if status != "PASS":
                                assert False, f"{validation_name} failed: {value}"