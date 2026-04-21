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

            failures = []
            warnings = []

            for r in results:
                check_name, status, value = r

                # ✅ Missing in target
                if check_name == "missing_in_target":
                    threshold = table.get("threshold_missing_target", 0)

                    if value > threshold:
                        failures.append(f"{check_name}: {value}")
                    elif value > 0:
                        warnings.append(f"{check_name}: {value}")

                # ✅ Missing in source
                elif check_name == "missing_in_source":
                    threshold = table.get("threshold_missing_source", 0)

                    if value > threshold:
                        failures.append(f"{check_name}: {value}")
                    elif value > 0:
                        warnings.append(f"{check_name}: {value}")

                # ✅ Column mismatch
                elif check_name == "column_mismatch":
                    if not table.get("allow_column_mismatch", False):
                        failures.append(f"{check_name}")
                    else:
                        warnings.append(f"{check_name}")

                # ✅ Other validations
                elif status != "PASS":
                    failures.append(f"{check_name}: {value}")

            # ✅ Attach mismatch data
            if mismatch_df is not None and not mismatch_df.empty:
                allure.attach(
                    mismatch_df.to_csv(index=False),
                    name="Mismatch Data",
                    attachment_type=allure.attachment_type.CSV
                )

            # ✅ Attach warnings
            if warnings:
                allure.attach(
                    "\n".join(warnings),
                    name="Warnings",
                    attachment_type=allure.attachment_type.TEXT
                )

            # ✅ Final decision (fail only on critical issues)
            if failures:
                assert False, "Failures:\n" + "\n".join(failures)

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

                    # STRICT MODE
                    if strict:
                        assert status == "PASS", f"{validation_name} failed: {value}"

                    # THRESHOLD MODE
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
                            if status != "PASS":
                                assert False, f"{validation_name} failed: {value}"