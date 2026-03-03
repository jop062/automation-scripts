#!/usr/bin/env node
/**
 * clean_json.js
 * -------------
 * Cleans a JSON file by:
 *   - Removing null/undefined keys
 *   - Flattening nested objects (optional)
 *   - Deduplicating arrays
 *   - Trimming string values
 *
 * Usage:
 *   node clean_json.js --input data.json --output cleaned.json
 *   node clean_json.js --input data.json --output cleaned.json --flatten
 *   node clean_json.js --input data.json --output cleaned.json --remove-nulls
 */

const fs = require("fs");

// ── Parse CLI args ────────────────────────────────────────────
const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };
const has = (flag) => args.includes(flag);

const inputPath = get("--input");
const outputPath = get("--output");
const flatten = has("--flatten");
const removeNulls = has("--remove-nulls");

if (!inputPath || !outputPath) {
  console.error("❌ Usage: node clean_json.js --input <file> --output <file> [--flatten] [--remove-nulls]");
  process.exit(1);
}

if (!fs.existsSync(inputPath)) {
  console.error(`❌ File not found: ${inputPath}`);
  process.exit(1);
}

// ── Helpers ───────────────────────────────────────────────────
function removeNullKeys(obj) {
  if (Array.isArray(obj)) return obj.map(removeNullKeys).filter(v => v !== null && v !== undefined);
  if (typeof obj === "object" && obj !== null) {
    return Object.fromEntries(
      Object.entries(obj)
        .filter(([_, v]) => v !== null && v !== undefined)
        .map(([k, v]) => [k, removeNullKeys(v)])
    );
  }
  return obj;
}

function trimStrings(obj) {
  if (Array.isArray(obj)) return obj.map(trimStrings);
  if (typeof obj === "object" && obj !== null) {
    return Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, trimStrings(v)]));
  }
  if (typeof obj === "string") return obj.trim();
  return obj;
}

function flattenObject(obj, prefix = "") {
  return Object.entries(obj).reduce((acc, [key, val]) => {
    const newKey = prefix ? `${prefix}_${key}` : key;
    if (typeof val === "object" && val !== null && !Array.isArray(val)) {
      Object.assign(acc, flattenObject(val, newKey));
    } else {
      acc[newKey] = val;
    }
    return acc;
  }, {});
}

function deduplicateArrays(obj) {
  if (Array.isArray(obj)) {
    const seen = new Set();
    return obj
      .map(deduplicateArrays)
      .filter(item => {
        const key = JSON.stringify(item);
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
  }
  if (typeof obj === "object" && obj !== null) {
    return Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, deduplicateArrays(v)]));
  }
  return obj;
}

// ── Run ───────────────────────────────────────────────────────
let data = JSON.parse(fs.readFileSync(inputPath, "utf-8"));
const isArray = Array.isArray(data);
const originalCount = isArray ? data.length : 1;

console.log(`📂 Loaded: ${inputPath}`);

data = trimStrings(data);
console.log("✅ Strings trimmed");

data = deduplicateArrays(data);
console.log("✅ Arrays deduplicated");

if (removeNulls) {
  data = removeNullKeys(data);
  console.log("✅ Null keys removed");
}

if (flatten && !isArray) {
  data = flattenObject(data);
  console.log("✅ Object flattened");
} else if (flatten && isArray) {
  data = data.map(item => typeof item === "object" ? flattenObject(item) : item);
  console.log("✅ Array items flattened");
}

const finalCount = isArray ? data.length : 1;
fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), "utf-8");

console.log(`\n📊 Summary:`);
console.log(`   Original items : ${originalCount}`);
console.log(`   Cleaned items  : ${finalCount}`);
console.log(`\n💾 Saved to: ${outputPath}`);
