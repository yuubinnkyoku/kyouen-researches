// Width-69 (and width-parameterized) fresh/holes 2-for-2 sweep over all published witness bases,
// with 1-for-0 (19-stone direct maximality) checks. Exact integer geometry only.
// Engine: pinned enum_two.js from seven-row-q4-witness-band-60plus-20261121 (byte-identical copy).
// Usage: node sweep69.js <width> <mode fresh|holes|all> <start> <count>
// Auto-resumes: per (width, mode) results file skips already-processed base sigs.
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const BASES = 'input/bases.json';
const resFile = (W, mode) => `output/w${W}/${mode}/results.jsonl`;

function maxCheckOneForZero(board, stones, W) {
  // 19-stone config: remove one stone; require every empty cell of every deficient row (count<3)
  // to lie on a 3-stone line/circle of the remaining config. Returns list of removals yielding maxima.
  const out = [];
  for (let r = 0; r < stones.length; r++) {
    const cfg = stones.slice(); cfg.splice(r, 1);
    const rows = new Array(7).fill(0);
    for (const [x, y] of cfg) rows[y]++;
    const occ = new Set(cfg.map(([x, y]) => x + y * 4096));
    // blocked cells: union of all 3-stone curves (line or circle) among cfg
    const blocked = new Set();
    let shapeOK = true;
    for (let y = 0; y < 7; y++) if (rows[y] > 3) shapeOK = false;
    if (!shapeOK) continue;
    const n = cfg.length;
    let bad = false;
    for (let a = 0; a < n && !bad; a++) for (let b = a + 1; b < n && !bad; b++) for (let c = b + 1; c < n && !bad; c++) {
      const pts = board.key3(cfg[a][0], cfg[a][1], cfg[b][0], cfg[b][1], cfg[c][0], cfg[c][1]);
      if (board.W > 4096) throw new Error('W too big');
      // decode pts index: idx = x + W*y  => re-encode into x,y set
      for (const u of pts) blocked.add((u % board.W) + ':' + ((u / board.W) | 0));
    }
    if (bad) continue;
    for (let y = 0; y < 7 && !bad; y++) {
      if (rows[y] === 3) continue; // saturated row: horizontal line blocks all cells
      for (let x = 0; x < W; x++) {
        if (occ.has(x + ':' + y)) continue;
        if (!blocked.has(x + ':' + y)) { bad = true; break; }
      }
    }
    if (!bad) out.push({ removed: stones[r], stones: cfg.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]) });
  }
  return out;
}

const main = () => {
  const W = Number(process.argv[2]);
  const mode = process.argv[3] || 'fresh';
  const start = Number(process.argv[4] || 0);
  const count = Number(process.argv[5] || 30);
  const bases = JSON.parse(fs.readFileSync(BASES, 'utf8'));
  const dir = `output/w${W}/${mode}`;
  fs.mkdirSync(dir, { recursive: true });
  const RES = resFile(W, mode);
  const done = new Set();
  if (fs.existsSync(RES)) for (const line of fs.readFileSync(RES, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { done.add(JSON.parse(line).sig); } catch (e) {}
  }
  fs.appendFileSync(RES, '');
  let n = 0, witnessHits = 0;
  const t_start = Date.now();
  for (let i = start; i < bases.length && n < count; i++) {
    const b = bases[i];
    const sig = JSON.stringify(b.stones.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
    if (done.has(sig)) continue;
    const holes = mode === 'holes';
    const r = runCase(new Board(W), b.stones, { holes, maxWitnesses: 64 });
    witnessHits += r.safe_maximal_row_deficient;
    const oneForZero = maxCheckOneForZero(new Board(W), b.stones, W);
    const rec = { idx: i, tag: b.tag, sig, holes, rcc: r.row_capacity_candidates, safe: r.safe_candidates, shape_errors: r.shape_errors, maximal: r.safe_maximal_row_deficient, one_for_zero_hits: oneForZero.length, one_for_zero: oneForZero.map(o => o.removed), ms: Date.now() - t_start, witnesses: r.witnesses };
    fs.appendFileSync(RES, JSON.stringify(rec) + '\n');
    done.add(sig); n++;
  }
  console.log(JSON.stringify({ W, mode, processed: n, witnessHits, totalDone: done.size, ofBases: bases.length, wallMsTotal: Date.now() - t_start }));
};
main();
