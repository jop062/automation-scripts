# 📖 Usage Guide

Detailed examples for every script in this repo.

---

## 🐍 Python Scripts

### `clean_csv.py`

Cleans a CSV by removing duplicates, standardizing column names, and handling nulls.

```bash
# Basic clean
python python/clean_csv.py --input raw.csv --output clean.csv

# Drop rows with any null values
python python/clean_csv.py --input raw.csv --output clean.csv --drop-nulls

# Fill nulls with 0
python python/clean_csv.py --input raw.csv --output clean.csv --fill-nulls 0

# Fill nulls with "N/A"
python python/clean_csv.py --input raw.csv --output clean.csv --fill-nulls "N/A"
```

**What it fixes:**
- Column names → lowercase with underscores (e.g. `First Name` → `first_name`)
- Duplicate rows → removed
- Leading/trailing whitespace in text → stripped
- Null values → filled or dropped based on your flag

---

### `data_profiler.py`

Generates a full summary report of any CSV dataset.

```bash
# Print report to terminal
python python/data_profiler.py --input data.csv

# Save report to file
python python/data_profiler.py --input data.csv --output report.txt
```

**Report includes:**
- Row and column count
- Duplicate row count
- Null counts and percentages per column
- Mean, std, min, max for numeric columns
- Top 3 most common values for categorical columns

---

### `batch_rename.py`

Renames files in bulk inside a directory.

```bash
# Add prefix
python python/batch_rename.py --dir ./photos --prefix "2024_"

# Add suffix before extension
python python/batch_rename.py --dir ./reports --suffix "_final"

# Replace spaces with underscores
python python/batch_rename.py --dir ./files --replace " " "_"

# Add sequential numbers (001_filename, 002_filename...)
python python/batch_rename.py --dir ./slides --number --start 1

# Convert all filenames to lowercase
python python/batch_rename.py --dir ./data --lowercase

# Preview without making changes
python python/batch_rename.py --dir ./data --prefix "new_" --dry-run
```

---

## 🐚 Bash Scripts

> Make scripts executable first: `chmod +x bash/*.sh`

### `clean_logs.sh`

Archives old log files into a `.tar.gz`.

```bash
# Archive logs older than 30 days
./bash/clean_logs.sh --dir /var/log --days 30

# Archive AND delete originals
./bash/clean_logs.sh --dir ./logs --days 7 --delete

# Preview only (no changes)
./bash/clean_logs.sh --dir ./logs --days 14 --dry-run
```

---

### `backup_dir.sh`

Creates a timestamped zip backup of any directory.

```bash
# Basic backup (saves to ./backups/)
./bash/backup_dir.sh --dir ./my_project

# Custom output location
./bash/backup_dir.sh --dir ./my_project --output /Volumes/Drive/backups

# Keep only last 5 backups (auto-deletes older ones)
./bash/backup_dir.sh --dir ./my_project --keep 5
```

**Output example:** `backups/my_project_20240315_143022.tar.gz`

---

### `sys_check.sh`

Prints a system health snapshot.

```bash
# One-time report
./bash/sys_check.sh

# Live refresh every 5 seconds
./bash/sys_check.sh --watch
```

**Shows:** CPU usage, memory usage, disk usage, uptime, top 5 processes by CPU.

---

## 🟨 JavaScript Scripts

> Requires Node.js 16+

### `csv_to_json.js`

Converts CSV to structured JSON with type inference.

```bash
# Convert and save
node javascript/csv_to_json.js --input data.csv --output data.json

# Pretty-printed JSON
node javascript/csv_to_json.js --input data.csv --output data.json --pretty

# Print to terminal
node javascript/csv_to_json.js --input data.csv
```

**Type inference:**
- Numbers → `number`
- `true`/`false` → `boolean`
- Empty/`null`/`NULL` → `null`
- Everything else → `string`

---

### `clean_json.js`

Cleans, flattens, and deduplicates JSON files.

```bash
# Basic clean (trim strings + deduplicate arrays)
node javascript/clean_json.js --input data.json --output clean.json

# Remove all null/undefined keys
node javascript/clean_json.js --input data.json --output clean.json --remove-nulls

# Flatten nested objects
node javascript/clean_json.js --input data.json --output clean.json --flatten

# All options combined
node javascript/clean_json.js --input data.json --output clean.json --flatten --remove-nulls
```

**Flatten example:**
```json
// Before
{ "user": { "name": "Jon", "age": 22 } }

// After --flatten
{ "user_name": "Jon", "user_age": 22 }
```
