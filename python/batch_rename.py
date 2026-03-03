"""
batch_rename.py
---------------
Renames files in a folder using:
  - Prefix or suffix addition
  - Text find & replace
  - Sequential numbering
  - Lowercase conversion

Usage:
  python batch_rename.py --dir ./files --prefix "2024_"
  python batch_rename.py --dir ./files --suffix "_final"
  python batch_rename.py --dir ./files --replace " " "_"
  python batch_rename.py --dir ./files --number --start 1
  python batch_rename.py --dir ./files --lowercase
"""

import argparse
import os
import sys


def batch_rename(directory, prefix="", suffix="", replace_from=None,
                 replace_to=None, number=False, start=1, lowercase=False, dry_run=False):

    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)

    files = sorted([
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ])

    if not files:
        print("⚠️  No files found in directory.")
        return

    print(f"📂 Found {len(files)} files in: {directory}")
    if dry_run:
        print("🔍 DRY RUN — no files will be renamed\n")

    renamed = 0
    for i, filename in enumerate(files):
        name, ext = os.path.splitext(filename)

        if lowercase:
            name = name.lower()

        if replace_from is not None:
            name = name.replace(replace_from, replace_to or "")

        if number:
            name = f"{str(i + start).zfill(3)}_{name}"

        new_name = f"{prefix}{name}{suffix}{ext}"

        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        if filename == new_name:
            continue

        print(f"   {filename:<40} → {new_name}")

        if not dry_run:
            os.rename(old_path, new_path)
            renamed += 1

    if dry_run:
        print(f"\n✅ Dry run complete. {len(files)} files previewed.")
    else:
        print(f"\n✅ Done. {renamed} files renamed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files in a directory.")
    parser.add_argument("--dir", required=True, help="Target directory")
    parser.add_argument("--prefix", default="", help="Add prefix to filenames")
    parser.add_argument("--suffix", default="", help="Add suffix before extension")
    parser.add_argument("--replace", nargs=2, metavar=("FROM", "TO"), help="Replace text in filenames")
    parser.add_argument("--number", action="store_true", help="Add sequential numbers")
    parser.add_argument("--start", type=int, default=1, help="Starting number (default: 1)")
    parser.add_argument("--lowercase", action="store_true", help="Convert filenames to lowercase")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    args = parser.parse_args()

    replace_from, replace_to = args.replace if args.replace else (None, None)

    batch_rename(
        args.dir, args.prefix, args.suffix,
        replace_from, replace_to,
        args.number, args.start,
        args.lowercase, args.dry_run
    )
