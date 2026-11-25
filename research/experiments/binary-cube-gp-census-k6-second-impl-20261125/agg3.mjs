// agg3.mjs — aggregate census3.js per-pair lines and compare with the published first
// implementation (r6-results.jsonl of binary-cube-gp-census-k6-20261121) plus the
// derived anchored s_k table. Fail-closed: any mismatch exits non-zero.
//
// usage: node agg3.mjs <mine.jsonl...> <orig.jsonl>
//   all positional args except the last are "my" files; the last is the reference.
import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
const origPath = args.pop();
const mine = new Map();
let linesMine = 0;
for (const p of args) {
  for (const ln of readFileSync(p, "utf8").split("\n")) {
    if (!ln.trim()) continue;
    const o = JSON.parse(ln);
    if (mine.has(o.v2)) { console.error("DUPLICATE v2=" + o.v2 + " in my files"); process.exit(1); }
    mine.set(o.v2, o.counts);
    linesMine++;
  }
}
const orig = new Map();
for (const ln of readFileSync(origPath, "utf8").split("\n")) {
  if (!ln.trim()) continue;
  const o = JSON.parse(ln);
  orig.set(o.v2, o.counts);
}
if (linesMine !== 63 || mine.size !== 63 || orig.size !== 63) {
  console.error("SIZE FAIL mine=" + linesMine + "/" + mine.size + " orig=" + orig.size);
  process.exit(1);
}
let mismatches = 0;
const sum = new Array(11).fill(0);
for (const [v2, c] of orig) {
  const mc = mine.get(v2);
  if (!mc) { console.error("MISSING v2=" + v2); mismatches++; continue; }
  if (JSON.stringify(mc) !== JSON.stringify(c)) {
    console.error("COUNT MISMATCH v2=" + v2, JSON.stringify(mc), "vs", JSON.stringify(c));
    mismatches++;
  }
  for (let k = 0; k < 11; k++) sum[k] += c[k];
}
// derived anchored table (published): [0,63,63,1953,39410,571340,6029142,40050850,53334038,408240,0]
const expectSum = [0,63,63,1953,39410,571340,6029142,40050850,53334038,408240,0];
const sumMine = new Array(11).fill(0);
for (const [, c] of mine) for (let k = 0; k < 11; k++) sumMine[k] += c[k];
const sumTable_ok = JSON.stringify(sumMine) === JSON.stringify(expectSum);
console.log(JSON.stringify({
  pairs: linesMine, perPairMismatches: mismatches, sum: sumMine,
  sumMatchesPublishedSTable: sumTable_ok,
}));
process.exit(mismatches === 0 && sumTable_ok ? 0 : 1);
