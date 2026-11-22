// dump_quartets.mjs — emit the canonical forbidden-quartet list from the published
// census.mjs machinery (pinned, byte-identical to
// research/experiments/s12-s13-sat-stabilization-20261122/scripts/census.mjs).
// Output: text form "n=<n>\n" + one sorted ascending line "a b c d" per quartet,
// lexicographically sorted overall (same canonical form as forbidgen.py)
// so the sha256 can be compared directly with the independent Python generator.
import { census, quartetList, verifyAgainstAnchors } from '../pinned/census.mjs';
import * as fs from 'node:fs';

const n = parseInt(process.argv[2], 10);
const cen = census(n);
const issues = verifyAgainstAnchors(cen);
const flat = quartetList(cen);
const quarts = [];
for (let i = 0; i < flat.length; i += 4) {
  const q = [flat[i], flat[i + 1], flat[i + 2], flat[i + 3]].sort((a, b) => a - b);
  if (!(q[0] < q[1] && q[1] < q[2] && q[2] < q[3])) throw new Error('quartet not ascending');
  quarts.push(q);
}
quarts.sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2] || a[3] - b[3]);
let text = `n=${n}\n`;
for (const q of quarts) text += q.join(' ') + '\n';
fs.writeFileSync(process.argv[3], text);
console.log(JSON.stringify({
  n, F: cen.F, D: cen.D, C: cen.C,
  lines: cen.lines.length, circles: cen.circles.length,
  anchors_ok: issues.length === 0, issues,
  count: quarts.length,
  sha256_text: (await import('node:crypto')).createHash('sha256').update(text).digest('hex'),
}));
