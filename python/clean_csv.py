"""
clean_csv.py
------------
Cleans a CSV file by:
  - Removing duplicate rows
  - Dropping or filling null values
  - Standardizing column names (lowercase, underscores)
  - Stripping whitespace from string columns

Usage:
  python clean_csv.py --input data.csv --output cleaned.csv
  python clean_csv.py --input data.csv --output cleaned.csv --fill-nulls 0
  python clean_csv.py --input data.csv --output cleaned.csv --drop-nulls
"""

import argparse
import pandas as pd
import os
import sys


def standardize_columns(df):
    """Lowercase column names and replace spaces with underscores."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    return df


def strip_whitespace(df):
    """Strip leading/trailing whitespace from all string columns."""
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
    return df


def clean_csv(input_path, output_path, fill_value=None, drop_nulls=False):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    print(f"📂 Loading: {input_path}")
    df = pd.read_csv(input_path)

    original_rows = len(df)
    original_cols = list(df.columns)

    # Standardize columns
    df = standardize_columns(df)
    print(f"✅ Columns standardized: {original_cols} → {list(df.columns)}")

    # Strip whitespace
    df = strip_whitespace(df)
    print(f"✅ Whitespace stripped from string columns")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    removed_dupes = before - len(df)
    print(f"✅ Duplicates removed: {removed_dupes} rows dropped")

    # Handle nulls
    null_count = df.isnull().sum().sum()
    if drop_nulls:
        df = df.dropna()
        print(f"✅ Null rows dropped: {null_count} nulls removed")
    elif fill_value is not None:
        df = df.fillna(fill_value)
        print(f"✅ Nulls filled with: '{fill_value}'")
    else:
        print(f"⚠️  Nulls remaining: {null_count} (use --drop-nulls or --fill-nulls to handle)")

    # Save output
    df.to_csv(output_path, index=False)
    print(f"\n📊 Summary:")
    print(f"   Original rows : {original_rows}")
    print(f"   Cleaned rows  : {len(df)}")
    print(f"   Columns       : {len(df.columns)}")
    print(f"\n💾 Saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean a CSV file.")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    parser.add_argument("--fill-nulls", default=None, help="Value to fill nulls with")
    parser.add_argument("--drop-nulls", action="store_true", help="Drop rows with nulls")
    args = parser.parse_args()

    clean_csv(args.input, args.output, args.fill_nulls, args.drop_nulls)
