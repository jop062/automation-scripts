"""
data_profiler.py
----------------
Auto-generates a readable summary report of any CSV dataset including:
  - Shape, column types, null counts
  - Numeric statistics (mean, std, min, max)
  - Top values for categorical columns
  - Duplicate row count

Usage:
  python data_profiler.py --input data.csv
  python data_profiler.py --input data.csv --output report.txt
"""

import argparse
import pandas as pd
import os
import sys
from datetime import datetime


def profile(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)
    lines = []

    def log(text=""):
        lines.append(text)
        print(text)

    log("=" * 60)
    log(f"  DATA PROFILE REPORT")
    log(f"  File    : {input_path}")
    log(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)

    log(f"\n📐 Shape")
    log(f"   Rows    : {df.shape[0]:,}")
    log(f"   Columns : {df.shape[1]}")

    log(f"\n🔁 Duplicates")
    dupes = df.duplicated().sum()
    log(f"   Duplicate rows: {dupes:,} ({dupes/len(df)*100:.1f}%)")

    log(f"\n📋 Columns Overview")
    log(f"   {'Column':<30} {'Type':<12} {'Nulls':<8} {'Null %'}")
    log(f"   {'-'*30} {'-'*12} {'-'*8} {'-'*8}")
    for col in df.columns:
        nulls = df[col].isnull().sum()
        null_pct = nulls / len(df) * 100
        log(f"   {col:<30} {str(df[col].dtype):<12} {nulls:<8} {null_pct:.1f}%")

    log(f"\n📊 Numeric Column Stats")
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        log(f"   {'Column':<25} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
        log(f"   {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
        for col in numeric_cols:
            log(f"   {col:<25} {df[col].mean():>10.2f} {df[col].std():>10.2f} {df[col].min():>10.2f} {df[col].max():>10.2f}")
    else:
        log("   No numeric columns found.")

    log(f"\n🔤 Categorical Column Top Values")
    cat_cols = df.select_dtypes(include="object").columns
    if len(cat_cols) > 0:
        for col in cat_cols:
            top = df[col].value_counts().head(3)
            log(f"   {col}:")
            for val, count in top.items():
                log(f"      {str(val):<30} {count:,} ({count/len(df)*100:.1f}%)")
    else:
        log("   No categorical columns found.")

    log("\n" + "=" * 60)

    if output_path:
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"\n💾 Report saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile a CSV dataset.")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", default=None, help="Optional path to save report as .txt")
    args = parser.parse_args()

    profile(args.input, args.output)
