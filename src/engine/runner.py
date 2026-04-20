import json

from src.validations.validator import validate_all
from utils.logger import get_logger

# NEW: connectors
from src.connectors.excel_connector import read_excel
from src.validations.comparator import compare_data
# from src.connectors.db_connector import read_oracle
# from src.connectors.databricks_connector import read_databricks


from src.reporting.dashboard import generate_dashboard
from src.reporting.email_sender import send_email_report

logger = get_logger()


# 🔹 Load config (NEW)
def load_config():
    with open("config/dev.json") as f:
        return json.load(f)


# 🔹 Load data dynamically (NEW)
def load_data(table, config):
    table_type = table.get("type", "excel")

    if table_type == "excel":
        return read_excel(table["source"])

    elif table_type == "excel_compare":
        # Return BOTH datasets (no processing here)
        source_df = read_excel(table["source"])
        target_df = read_excel(table["target"])
        return source_df, target_df

    # elif table_type == "oracle":
    #     if "oracle" not in config:
    #         logger.warning("Oracle config missing, skipping...")
    #         return None
    #     return read_oracle(table["query"], config["oracle"])

    # elif table_type == "databricks":
    #     return read_databricks(table["query"], config["databricks"])

    else:
        raise ValueError(f"Unsupported type: {table_type}")

def run():
    import os
    import pandas as pd

    logger.info("Starting ELT Validation Framework")

    config = load_config()

    with open("metadata/tables.json") as f:
        tables = json.load(f)

    overall_status = True
    summary = []

    for table in tables:
        table_name = table.get("table_name")
        table_type = table.get("type", "excel")

        passed = 0
        failed = 0

        try:
            logger.info(f"Processing table: {table_name}")

            data = load_data(table, config)

            # ============================
            # 🔁 COMPARISON FLOW
            # ============================
            if table_type == "excel_compare":
                source_df, target_df = data

                results, mismatch_df = compare_data(
                    source_df,
                    target_df,
                    table["primary_key"],
                    table.get("tolerance", {})
                )

                for r in results:
                    msg = f"{table_name} | {r[0]} | {r[1]} | {r[2]}"
                    logger.info(msg)
                    print(msg)

                    if r[1] == "PASS":
                        passed += 1
                    else:
                        failed += 1

                # Save mismatch file
                if not mismatch_df.empty:
                    os.makedirs("reports", exist_ok=True)
                    path = f"reports/{table_name}_mismatch.xlsx"
                    mismatch_df.to_excel(path, index=False)
                    print(f"Mismatch file: {path}")

                status = "PASS" if failed == 0 else "FAIL"

            # ============================
            # ✅ VALIDATION FLOW
            # ============================
            else:
                df = data

                if df is None:
                    logger.warning(f"{table_name} skipped")
                    continue

                results = validate_all(df)

                for r in results:
                    msg = f"{table_name} | {r['validation']} | {r['status']} | {r['value']}"
                    logger.info(msg)
                    print(msg)

                    if r["status"] == "PASS":
                        passed += 1
                    else:
                        failed += 1

                status = "PASS" if failed == 0 else "FAIL"

            summary.append({
                "table": table_name,
                "passed": passed,
                "failed": failed,
                "status": status
            })

            if status == "FAIL":
                overall_status = False

        except Exception as e:
            logger.error(f"{table_name} → ERROR: {str(e)}")
            summary.append({
                "table": table_name,
                "passed": 0,
                "failed": 1,
                "status": "ERROR"
            })
            overall_status = False

    # ============================
    # 📊 SUMMARY DASHBOARD
    # ============================
    print("\n========== SUMMARY ==========")

    total_pass = 0
    total_fail = 0

    for s in summary:
        print(f"{s['table']} → {s['status']} (Pass={s['passed']}, Fail={s['failed']})")
        total_pass += s["passed"]
        total_fail += s["failed"]

    print("\nTotal Passed:", total_pass)
    print("Total Failed:", total_fail)

    # Save summary to Excel
    # df_summary = pd.DataFrame(summary)
    # os.makedirs("reports", exist_ok=True)
    # df_summary.to_excel("reports/summary.xlsx", index=False)

    # Save summary to Excel
    df_summary = pd.DataFrame(summary)
    os.makedirs("reports", exist_ok=True)
    df_summary.to_excel("reports/summary.xlsx", index=False)

    # 🔹 Generate HTML Dashboard
    dashboard_path = generate_dashboard(summary)
    print(f"\nDashboard generated: {dashboard_path}")

    # ============================
    # 📧 SEND EMAIL (FINAL STEP)
    # ============================
    from src.reporting.email_sender import send_email_report

    try:
        send_email_report(
            to_email="tejshree.shinde@infobeans.com",
            subject="ELT Validation Report",
            body="Please find attached ETL validation report.",
            attachments=[
                "reports/summary.xlsx",
                "reports/dashboard.html"
            ]
        )
        print("Email sent successfully ✅")
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")


    logger.info("Execution Completed")

    return overall_status