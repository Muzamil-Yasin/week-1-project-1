"""
csv_stats.py — Read a CSV and calculate basic stats (mean, median, mode)
Usage (Windows PowerShell or CMD):
  py csv_stats.py --csv data.csv --columns age,salary

If you omit --columns, the script will automatically compute stats for all numeric columns.
Outputs a CSV summary at ./output/stats_summary.csv
"""

import argparse
import os
import sys
import pandas as pd

def compute_stats(df, columns=None):
    # If no columns provided, auto-detect numeric columns
    if not columns:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found. Provide --columns with numeric column names.")
        columns = numeric_cols

    rows = []
    for col in columns:
        if col not in df.columns:
            print(f"[WARN] Column '{col}' not found in CSV. Skipping.")
            continue

        # Convert to numeric if possible (coerce errors to NaN)
        s = pd.to_numeric(df[col], errors="coerce")

        # Drop missing values for stats
        s_nonnull = s.dropna()

        if s_nonnull.empty:
            print(f"[WARN] Column '{col}' has no numeric values after cleaning. Skipping.")
            continue

        mean_val = s_nonnull.mean()
        median_val = s_nonnull.median()

        # Mode can have multiple values; join as comma-separated string
        modes = s_nonnull.mode().tolist()
        mode_str = ", ".join(str(m) for m in modes)

        rows.append({
            "column": col,
            "count_non_null": int(s_nonnull.count()),
            "mean": float(mean_val),
            "median": float(median_val),
            "mode": mode_str
        })

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser(description="Compute basic stats from a CSV.")
    parser.add_argument("--csv", default="data.csv", help="Path to CSV file (default: data.csv)")
    parser.add_argument("--columns", default="", help="Comma-separated column names (optional)")
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"[ERROR] CSV not found at: {args.csv}")
        sys.exit(1)

    try:
        df = pd.read_csv(args.csv)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        sys.exit(1)

    columns = [c.strip() for c in args.columns.split(",") if c.strip()] if args.columns else None

    try:
        summary = compute_stats(df, columns)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if summary.empty:
        print("[INFO] No stats were computed. Check your column names or data types.")
        sys.exit(0)

    # Save to ./output/stats_summary.csv
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "stats_summary.csv")
    summary.to_csv(out_path, index=False)

    # Pretty-print to console
    print("\n=== Basic Stats (mean, median, mode) ===")
    print(summary.to_string(index=False))
    print(f"\nSaved summary to: {out_path}")

if __name__ == "__main__":
    main()
