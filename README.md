# ⚙️ Automation Scripts

**Dev tools • Quality • Speed**

Scripts that standardize workflows, reduce manual steps, and make systems easier to debug.

Built by [Jonathan Pham](https://github.com/jop062) — Data Analytics student at UC San Diego.

---

## 📁 Structure

```
automation-scripts/
├── python/
│   ├── clean_csv.py          # Remove duplicates, fix nulls, standardize columns
│   ├── batch_rename.py       # Rename files in bulk using patterns
│   └── data_profiler.py      # Auto-generate a summary report of any dataset
├── bash/
│   ├── clean_logs.sh         # Archive and purge old log files
│   ├── backup_dir.sh         # Zip and timestamp a directory backup
│   └── sys_check.sh          # Quick system health snapshot
├── javascript/
│   ├── clean_json.js         # Flatten, deduplicate, and validate JSON files
│   └── csv_to_json.js        # Convert CSV files to structured JSON
└── docs/
    └── USAGE.md              # Detailed usage guide for each script
```

---

## 🐍 Python Scripts

| Script | What it does |
|---|---|
| `clean_csv.py` | Removes duplicates, fills or drops nulls, standardizes column names |
| `batch_rename.py` | Renames files in a folder using prefix, suffix, or regex patterns |
| `data_profiler.py` | Profiles any CSV and outputs a readable summary report |

## 🐚 Bash Scripts

| Script | What it does |
|---|---|
| `clean_logs.sh` | Finds and archives log files older than N days |
| `backup_dir.sh` | Creates a timestamped zip backup of any directory |
| `sys_check.sh` | Prints CPU, memory, disk usage, and uptime at a glance |

## 🟨 JavaScript Scripts

| Script | What it does |
|---|---|
| `clean_json.js` | Flattens nested JSON, removes null keys, deduplicates arrays |
| `csv_to_json.js` | Converts any CSV file to clean structured JSON |

---

## 🚀 Quick Start

**Python** (requires Python 3.8+):
```bash
pip install pandas
python python/clean_csv.py --input data.csv --output cleaned.csv
```

**Bash** (macOS/Linux):
```bash
chmod +x bash/clean_logs.sh
./bash/clean_logs.sh --dir /var/logs --days 30
```

**JavaScript** (requires Node.js 16+):
```bash
node javascript/csv_to_json.js --input data.csv --output data.json
```

---

## 🛠️ Requirements

- Python 3.8+ with `pandas`, `tabulate`
- Node.js 16+
- Bash (macOS/Linux/WSL)

---

## 📄 License

MIT — free to use, modify, and share.
