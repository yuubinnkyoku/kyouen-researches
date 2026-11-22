// decode_model.mjs — extract the stone set from a kissat model output
// ("v <lit> ... 0" lines). Only positives among the N cell variables are stones.
// Fails loudly unless every cell literal occurs exactly once.
// Usage: node decode_model.mjs <n> <k> <model-file> [--shuffle=seed] ; writes witness JSON to stdout
import { readFileSync } from 'node:fs';

const n = parseInt(process.argv[2], 10);
const k = parseInt(process.argv[3], 10);
const modelPath = process.argv[4];
let shuffleSeed = null;
for (const a of process.argv.slice(5)) { const m = a.match(/^--shuffle=([0-9]+)$/); if (m) shuffleSeed = parseInt(m[1], 10) >>> 0; }

const txt = readFileSync(modelPath, 'utf8');
const allLines = txt.split('\n');
const vlines = allLines.filter((l) => l.startsWith('v '));
if (!vlines.length) { console.error('no v lines'); process.exit(1); }
const lits = [];
for (const l of vlines) for (const t of l.slice(2).trim().split(/\s+/)) if (t) lits.push(parseInt(t, 10));
if (lits[lits.length - 1] !== 0) { console.error('model not terminated by 0'); process.exit(1); }
lits.pop();

const N = n * n;
let inv = null, nVars = 0;
if (shuffleSeed !== null) {
  nVars = parseInt(process.env.KYOUEN_NVARS || '0', 10);
  if (!nVars) { console.error('need KYOUEN_NVARS for shuffle'); process.exit(1); }
  let a0 = shuffleSeed >>> 0;
  const r = () => { a0 |= 0; a0 = (a0 + 0x6D2B79F5) | 0; let t = Math.imul(a0 ^ (a0 >>> 15), 1 | a0); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0); };
  const ids = new Int32Array(nVars);
  for (let i = 0; i < nVars; i++) ids[i] = i + 1;
  for (let i = nVars - 1; i > 0; i--) { const j = (r() % (i + 1)); const t = ids[i]; ids[i] = ids[j]; ids[j] = t; }
  inv = new Int32Array(nVars + 1);
  for (let i = 0; i < nVars; i++) inv[ids[i]] = i + 1;
}

const seen = new Uint8Array(N + 1);
const stones = [];
for (const lit of lits) {
  const logical = shuffleSeed !== null ? inv[Math.abs(lit)] : Math.abs(lit);
  if (logical >= 1 && logical <= N) {
    if (seen[logical]) { console.error('duplicate cell literal'); process.exit(1); }
    seen[logical] = 1;
    if (lit > 0) stones.push(logical - 1);
  }
}
for (let i = 1; i <= N; i++) if (!seen[i]) { console.error('missing cell literal ' + i); process.exit(1); }
const coords = stones.map((c) => [c % n, Math.floor(c / n)]).sort((a, b) => a[1] - b[1] || a[0] - b[0]);
const wit = { n, stones: coords, derived_from: { model: modelPath, k, shuffle: shuffleSeed, nLits: lits.length } };
console.log(JSON.stringify(wit));
console.error(JSON.stringify({ n, k, size: stones.length, shuffle: shuffleSeed }));
