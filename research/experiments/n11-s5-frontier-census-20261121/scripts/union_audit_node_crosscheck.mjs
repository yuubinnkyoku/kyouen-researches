#!/usr/bin/env node
// Independent second implementation (Node.js) cross-checking the published
// global S5 union audit (audit_global_union.py, sha256 417caa5b...).
//
// Purpose: analytical independence for the audit's headline claims
//   zero internal file conflicts, zero global WIN/LOSS conflicts,
//   326 files / 760,504 rows / 5,866 unique keys, 108 backward-only rows.
// Same pinned inputs, independently re-walked and re-parsed (line-splitting
// and field validation instead of the csv module). Fail-closed on pin
// mismatch or parse ambiguity. Reports only; never merges or rehabilitates.
//
// Usage: node scripts/union_audit_node_crosscheck.mjs
// Emits JSON on stdout.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..', '..');
const CURRENT_CHAIN = path.join(ROOT, 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache');
const REGISTRY = path.join(ROOT, 'results/n11-s5-evidence-quarantine.json');
const PIN = {
  current_chain: '60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6',
  quarantine_registry: '81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9',
  published_audit: '7280376d3ace4240b3c360baa84df17661e2e336df9af9d602c171247792d27b',
};

function die(msg) {
  console.error('CROSSCHECK FAIL-CLOSED ABORT: ' + msg);
  process.exit(1);
}
const sha256 = (buf) => createHash('sha256').update(buf).digest('hex');

// --- quarantine registry (duplicate-key-rejecting, schema-checked) ---------
function assertNoDuplicateJsonKeys(text) {
  // minimal scanner: context stack distinguishes objects (property names)
  // from arrays (string values); flags duplicate property names per object
  const stack = []; // elements: { obj: Set<string> | null }
  let cur = null;   // Set of property names when inside an object, else null
  let expectKey = false;
  let i = 0;
  while (i < text.length) {
    const c = text[i];
    if (c === '"') {
      let j = i + 1, s = '';
      while (j < text.length && text[j] !== '"') {
        if (text[j] === '\\') { s += text[j + 1]; j += 2; } else { s += text[j]; j += 1; }
      }
      if (expectKey) {
        if (cur.has(s)) die('duplicate JSON key: ' + s);
        cur.add(s);
      }
      expectKey = false;
      i = j + 1;
      continue;
    }
    if (c === '{') { stack.push(cur); cur = new Set(); expectKey = true; i += 1; continue; }
    if (c === '[') { stack.push(cur); cur = null; expectKey = false; i += 1; continue; }
    if (c === '}' || c === ']') { cur = stack.pop(); expectKey = false; i += 1; continue; }
    if (c === ',') { expectKey = cur !== null; i += 1; continue; }
    if (c === ':') { expectKey = false; i += 1; continue; }
    i += 1;
  }
}
function loadQuarantine() {
  const text = fs.readFileSync(REGISTRY, 'utf8');
  assertNoDuplicateJsonKeys(text);
  let doc;
  try {
    // big integers (> Number.MAX_SAFE_INTEGER) must survive parsing:
    // quote them before JSON.parse so 64-bit keys are not silently rounded
    doc = JSON.parse(text.replace(/([:\[\s,\[])(-?\d{16,})/g, '$1"$2"'));
  } catch (e) { die('registry JSON parse: ' + e.message); }
  if (doc.schema !== 'n11-s5-evidence-quarantine-v1') die('registry schema');
  const seen = new Set();
  const quarantine = new Set();
  for (const row of doc.entries) {
    const [lo, hi] = row.key;
    const loS = String(lo), hiS = String(hi);
    if (!/^-?\d+$/.test(loS) || !/^-?\d+$/.test(hiS)) die('registry key type');
    if (popcountNum(loS) + popcountNum(hiS) !== 5) die('registry key popcount');
    if (BigInt(loS) < 0n || BigInt(loS) >= 2n ** 64n) die('registry key range lo');
    if (BigInt(hiS) < 0n || BigInt(hiS) >= 2n ** 57n) die('registry key range hi');
    const pair = loS + ':' + hiS;
    if (seen.has(pair)) die('duplicate registry key ' + pair);
    seen.add(pair);
    if (row.active === true) quarantine.add(pair);
  }
  return quarantine;
}

// BigInt-based popcount for keys up to 2^64 / 2^57
function popcountNum(x) {
  let b = BigInt(x), n = 0n;
  while (b) { n += b & 1n; b >>= 1n; }
  return Number(n);
}

// --- trust labels (must replicate the published classifier) ----------------
function trustLabel(rel) {
  const name = rel.toLowerCase();
  if (name.includes('derived')) return 'derived';
  for (const t of ['-witness', '-reverse', '-expanded-s6', 's6-', '-s7-', 'model8', 'model-hard']) {
    if (name.includes(t)) return 'model_derived';
  }
  if (['exact', 'merged', 'canonical', 'reconstructed'].some((t) => name.includes(t))) return 'exact_or_merged';
  return 'other';
}

// --- cache parsing (line-splitting impl, no csv module) --------------------
const INT_RE = /^[+-]?\d+$/;
function* iterCacheRows(text) {
  // emulate csv.reader row separation for the corpus (no embedded newlines;
  // quoted-field presence is asserted against below)
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
  for (const line of text.split(/\r\n|\r|\n/)) {
    if (line.includes('"')) die('quoted CSV field encountered (not expected in corpus): ' + line.slice(0, 60));
    yield line.split(',');
  }
}

function walkCacheFiles(dir) {
  const out = [];
  const stack = [dir];
  while (stack.length) {
    const d = stack.pop();
    let entries;
    try { entries = fs.readdirSync(d, { withFileTypes: true }); } catch (e) { die('walk: ' + e.message); }
    for (const e of entries) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) stack.push(p);
      else if (e.isFile() && e.name.endsWith('.cache')) out.push(p);
    }
  }
  out.sort();
  return out;
}

// --- main -------------------------------------------------------------------
const quarantine = loadQuarantine();
const chainBytes = fs.readFileSync(CURRENT_CHAIN);
if (sha256(chainBytes) !== PIN.current_chain) die('current chain pin mismatch');
if (sha256(fs.readFileSync(REGISTRY)) !== PIN.quarantine_registry) die('registry pin mismatch');

const provenance = new Map(); // key "a:b" -> [{rel,label,v}]
const fileRecs = [];
let rowsTotal = 0;
let internalConflicts = 0;
let suspectRows = 0;

for (const abs of walkCacheFiles(path.join(ROOT, 'research'))) {
  const rel = path.relative(ROOT, abs);
  const seenInFile = new Map(); // key -> verdict or 'CONFLICT_INTERNAL'
  let n = 0;
  let stop = false;
  for (const row of iterCacheRows(fs.readFileSync(abs, 'utf8'))) {
    if (row.length === 1 && row[0] === '') continue;          // empty line
    if (row[0].startsWith('#')) continue;                      // comment
    if (row[0] === 'key') continue;                            // header row
    if (row[0] !== 's5verdict') { stop = true; break; }        // end of s5 block
    const okFields = row.length === 6
      && INT_RE.test(row[1]) && INT_RE.test(row[2])
      && INT_RE.test(row[3]) && INT_RE.test(row[4]);
    if (!okFields || Number(row[3]) !== 5 || ![1, 2].includes(Number(row[4]))) {
      suspectRows += 1;
      continue;
    }
    const k = row[1] + ':' + row[2];
    const v = Number(row[4]);
    n += 1;
    if (seenInFile.has(k) && seenInFile.get(k) !== v && seenInFile.get(k) !== 'CONFLICT_INTERNAL') {
      internalConflicts += 1;
      seenInFile.set(k, 'CONFLICT_INTERNAL');
    } else if (!seenInFile.has(k)) {
      seenInFile.set(k, v);
    }
  }
  if (n === 0) continue;
  const label = trustLabel(rel);
  fileRecs.push({ path: rel, label, rows: n, sha256: sha256(fs.readFileSync(abs)) });
  rowsTotal += n;
  for (const [k, v] of seenInFile) {
    if (!provenance.has(k)) provenance.set(k, []);
    provenance.get(k).push([rel, label, v]);
  }
}

// current chain keys
const chain = new Map();
for (const row of iterCacheRows(chainBytes.toString('utf8'))) {
  if (row.length === 1 && row[0] === '') continue;
  if (row[0].startsWith('#')) continue;
  if (row[0] !== 's5verdict') die('unexpected chain row: ' + row.slice(0, 3).join(','));
  chain.set(row[1] + ':' + row[2], Number(row[4]));
}

// global conflicts and union counts
let globalConflicts = 0;
let hasWin = 0;
let lossOnly = 0;
let backwardOnly = [];
const quarantineHits = {};
for (const [k, prov] of provenance) {
  const vals = new Set(prov.map((p) => p[2]));
  if (vals.has('CONFLICT_INTERNAL') || vals.size > 1) globalConflicts += 1;
  const verdicts = prov.map((p) => p[2]).filter((v) => v !== 'CONFLICT_INTERNAL');
  if (verdicts.includes(1)) hasWin += 1;
  if (verdicts.length > 0 && verdicts.every((v) => v === 2)) lossOnly += 1;
  if (quarantine.has(k)) {
    quarantineHits[k] = prov.map(([rel, label, v]) => ({ file: rel, label, verdict: v }));
  }
  if (!chain.has(k) && !quarantine.has(k)) {
    const exactLike = prov.filter(([, label]) => label === 'exact_or_merged');
    if (exactLike.length > 0) {
      backwardOnly.push({
        // raw CSV text parts (string) preserve values above 2^53 exactly
        key: k.split(':'),
        verdict_values: [...new Set(exactLike.map((p) => p[2]))].sort((a, b) => a - b),
        files: [...new Set(exactLike.map((p) => p[0]))].sort(),
      });
    }
  }
}
backwardOnly.sort((a, b) => (BigInt(a.key[0]) < BigInt(b.key[0]) ? -1 : BigInt(a.key[0]) > BigInt(b.key[0]) ? 1 : BigInt(a.key[1]) < BigInt(b.key[1]) ? -1 : 1));

const result = {
  schema: 'n11-s5-union-audit-node-crosscheck-20261121-v1',
  implementation: 'node-v' + process.versions.node + ' (independent line-splitting parser; no csv module)',
  pins_checked: PIN,
  files_scanned: fileRecs.length,
  s5verdict_rows_total: rowsTotal,
  unique_keys: provenance.size,
  internal_file_conflicts: internalConflicts,
  global_conflict_count: globalConflicts,
  suspect_rows_skipped: suspectRows,
  union_counts: { has_WIN_somewhere: hasWin, LOSS_only_everywhere: lossOnly },
  current_chain_rows: chain.size,
  current_chain_win: [...chain.values()].filter((v) => v === 1).length,
  current_chain_loss: [...chain.values()].filter((v) => v === 2).length,
  quarantine_keys_hit: Object.keys(quarantineHits).sort(),
  backward_only_count: backwardOnly.length,
  backward_only_exact_or_merged_rows: backwardOnly,
  guard: 'Cross-check only. Never establishes a verdict, never merges, never rehabilitates. Standard 11x11 empty board and two-stone root {60,27} remain UNKNOWN.',
};

// --- direct comparison against the published audit artifact -----------------
const PUB = path.join(ROOT, 'research/experiments/n11-s5-frontier-census-20261121/output/global-union-audit.json');
const pubBytes = fs.readFileSync(PUB);
const pubSha = sha256(pubBytes);
const pubShaOk = pubSha === PIN.published_audit;
// same 64-bit-safe integer handling as for the registry (big literals as strings)
const pub = JSON.parse(pubBytes.toString('utf8').replace(/([:\[,\s])(-?\d{16,})/g, '$1"$2"'));
const eqBackward = pub.backward_only_count === backwardOnly.length
  && pub.backward_only_exact_or_merged_rows.length === backwardOnly.length
  && pub.backward_only_exact_or_merged_rows.every((r, i) =>
    String(r.key[0]) === backwardOnly[i].key[0] && String(r.key[1]) === backwardOnly[i].key[1]
    && JSON.stringify(r.verdict_values) === JSON.stringify(backwardOnly[i].verdict_values)
    && JSON.stringify(r.files) === JSON.stringify(backwardOnly[i].files));
const pubQkeys = Object.keys(pub.quarantine_keys_in_files).sort();
const qNorm = (hits) => JSON.stringify([...hits].map((h) => [h.file, h.label, h.verdict]).sort());
const qkeysFullMatch = JSON.stringify(pubQkeys) === JSON.stringify(Object.keys(quarantineHits).sort())
  && pubQkeys.every((k) => qNorm(pub.quarantine_keys_in_files[k]) === qNorm(quarantineHits[k]));
const fields = [
  ['files_scanned', pub.files_scanned, fileRecs.length],
  ['s5verdict_rows_total', pub.s5verdict_rows_total, rowsTotal],
  ['unique_keys', pub.unique_keys, provenance.size],
  ['internal_file_conflicts', pub.internal_file_conflicts, internalConflicts],
  ['global_conflict_count', pub.global_conflict_count, globalConflicts],
  ['union_counts.has_WIN_somewhere', pub.union_counts.has_WIN_somewhere, hasWin],
  ['union_counts.LOSS_only_everywhere', pub.union_counts.LOSS_only_everywhere, lossOnly],
  ['current_chain.rows', pub.current_chain.rows, chain.size],
  ['current_chain.win', pub.current_chain.win, result.current_chain_win],
  ['current_chain.loss', pub.current_chain.loss, result.current_chain_loss],
  ['backward_only_count', pub.backward_only_count, backwardOnly.length],
  ['backward_only_rows_full', true, eqBackward],
  ['quarantine_keys_hit', true, qkeysFullMatch],
];
const comparison = {
  published_audit_sha256: pubSha,
  published_audit_sha_pin_ok: pubShaOk,
  fields: fields.map(([name, a, b]) => ({ field: name, published: a, crosscheck: b, match: a === b })),
  all_fields_match: fields.every(([, a, b]) => a === b),
};
if (!pubShaOk) die('published audit sha pin mismatch: ' + pubSha);
result.cross_check_vs_published = comparison;
console.log(JSON.stringify(result, null, 1));
if (!comparison.all_fields_match) {
  console.error('MISMATCHFIELDS ' + JSON.stringify(comparison.fields.filter((f) => !f.match)));
  process.exit(1);
}
