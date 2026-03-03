#!/usr/bin/env node
/**
 * csv_to_json.js
 * --------------
 * Converts any CSV file to clean structured JSON.
 * Handles quoted fields, type inference, and empty values.
 *
 * Usage:
 *   node csv_to_json.js --input data.csv --output data.json
 *   node csv_to_json.js --input data.csv --output data.json --pretty
 *   node csv_to_json.js --input data.csv  (prints to stdout)
 */

const fs = require("fs");
const path = require("path");

// ── Parse CLI args ────────────────────────────────────────────
const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] : null;
};
const has = (flag) => args.includes(flag);

const inputPath = get("--input");
const outputPath = get("--output");
const pretty = has("--pretty");

if (!inputPath) {
  console.error("❌ Usage: node csv_to_json.js --input <file.csv> [--output <file.json>] [--pretty]");
  process.exit(1);
}

if (!fs.existsSync(inputPath)) {
  console.error(`❌ File not found: ${inputPath}`);
  process.exit(1);
}

// ── Parse CSV ─────────────────────────────────────────────────
function parseCSV(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = parseLine(lines[0]);

  return lines.slice(1).map((line) => {
    const values = parseLine(line);
    const row = {};
    headers.forEach((header, i) => {
      const raw = values[i] ?? "";
      row[header] = inferType(raw.trim());
    });
    return row;
  });
}

function parseLine(line) {
  const result = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      result.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  result.push(current);
  return result;
}

function inferType(value) {
  if (value === "" || value === "null" || value === "NULL") return null;
  if (value === "true" || value === "TRUE") return true;
  if (value === "false" || value === "FALSE") return false;
  if (!isNaN(value) && value !== "") return Number(value);
  return value;
}

// ── Run ───────────────────────────────────────────────────────
const raw = fs.readFileSync(inputPath, "utf-8");
const data = parseCSV(raw);
const json = JSON.stringify(data, null, pretty ? 2 : 0);

if (outputPath) {
  fs.writeFileSync(outputPath, json, "utf-8");
  console.log(`✅ Converted ${data.length} rows → ${outputPath}`);
} else {
  console.log(json);
}
