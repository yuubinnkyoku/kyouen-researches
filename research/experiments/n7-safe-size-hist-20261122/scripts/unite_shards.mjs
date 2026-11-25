// unite_shards.mjs — union of first-stone-shard safehist outputs; verifies that
// the shard sums reproduce an independently computed full-run histogram.
// shard i covers first stone cells [lo, hi): every safe set has a unique
// smallest cell, so shards partition all safe sets of size >= 1; size 0 (the
// empty set) is attributed only to the shard with lo == 0.
import * as fs from 'node:fs';
const shardDir = process.argv[2];   // dir with hist_n7_s*.jsonl
const fullPath = process.argv[3];   // full-run output for comparison
const hist = new Map();
const files = fs.readdirSync(shardDir).filter(f => /^hist_n7_s\d+_\d+\.jsonl$/.test(f)).sort();
if (files.length === 0) throw new Error('no shard files');
let ranges = [];
for (const f of files) {
  const lines = fs.readFileSync(shardDir + '/' + f, 'utf8').trimEnd().split('\n');
  const header = JSON.parse(lines[0]);
  const rec = JSON.parse(lines[1]);
  const h = JSON.parse(rec.histogram);
  ranges.push(header.first_stone_range);
  for (const k of Object.keys(h)) {
    if (parseInt(k) === 0) continue;
    hist.set(k, (hist.get(k) ?? 0) + h[k]);
  }
}
hist.set("0", 1);
const full = fs.readFileSync(fullPath, 'utf8').trimEnd().split('\n');
const fullRec = JSON.parse(full[1]);
const H = JSON.parse(fullRec.histogram);
let match = true;
const allKeys = new Set([...Object.keys(H), ...hist.keys()]);
const diffs = [];
for (const k of allKeys) {
  const a = H[k] ?? 0, b = hist.get(k) ?? 0;
  if (a !== b) { match = false; diffs.push({ size: k, full: a, shards: b }); }
}
const total = [...hist.values()].reduce((s, v) => s + v, 0);
console.log(JSON.stringify({ shards: files.length, ranges, union_total: total, full_total: fullRec.total_safe_subsets, total_match: total === fullRec.total_safe_subsets, histogram_match: match, diffs: diffs.slice(0, 20) }));
