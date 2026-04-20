import pandas as pd


def compare_data(source_df, target_df, keys, tolerance_config=None):
    import pandas as pd

    results = []

    # 🔹 Row count
    if len(source_df) == len(target_df):
        results.append(("row_count", "PASS", len(source_df)))
    else:
        results.append(("row_count", "FAIL", f"{len(source_df)} vs {len(target_df)}"))

    # 🔹 Missing records
    merged = source_df.merge(target_df, on=keys, how="outer", indicator=True)

    missing_in_target = merged[merged["_merge"] == "left_only"]
    missing_in_source = merged[merged["_merge"] == "right_only"]

    results.append(("missing_in_target", "FAIL" if len(missing_in_target) > 0 else "PASS", len(missing_in_target)))
    results.append(("missing_in_source", "FAIL" if len(missing_in_source) > 0 else "PASS", len(missing_in_source)))

    # 🔹 Column comparison with tolerance
    tolerance_config = tolerance_config or {}

    merged_full = source_df.merge(target_df, on=keys, suffixes=("_src", "_tgt"))

    mismatches = []

    for col in source_df.columns:
        if col in keys or col not in target_df.columns:
            continue

        src_col = f"{col}_src"
        tgt_col = f"{col}_tgt"

        if col in tolerance_config:
            tol = tolerance_config[col]

            temp = merged_full[
                (
                    abs(merged_full[src_col] - merged_full[tgt_col]) /
                    merged_full[src_col].replace(0, 1)
                ) > tol
            ]
        else:
            temp = merged_full[merged_full[src_col] != merged_full[tgt_col]]

        if not temp.empty:
            temp = temp[keys + [src_col, tgt_col]].copy()
            temp["column"] = col
            mismatches.append(temp)

    if mismatches:
        mismatch_df = pd.concat(mismatches, ignore_index=True)
        results.append(("column_mismatch", "FAIL", len(mismatch_df)))
    else:
        mismatch_df = pd.DataFrame()
        results.append(("column_mismatch", "PASS", 0))

    return results, mismatch_df