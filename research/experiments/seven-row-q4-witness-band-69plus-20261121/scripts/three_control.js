// Control suite for the restricted 3-for-3 engine (enum_three.js) before production use.
// A: known-answer positive - the published w68 witness must be re-discovered when the
//    additions are allowed to refill exactly the removed cells (holes mode), window x>=52.
// B: window negative - the same run with window x>=56 must NOT re-discover it.
// C: unsafe-base guard - a base containing 4 collinear stones must throw.
// D: determinism - control A must return byte-identical JSON on a second run.
// E: fresh-mode info run on the same base/window (production semantics), all outputs
//    brute-verified.
// F: every witness emitted by A/E must pass the independent brute-force verifier.
// Exit code 0 iff all controls pass.
'use strict';
const fs = require('fs');
const path = require('path');
const { Board, runThree, bruteVerify } = require('./enum_three.js');

const pubDir = path.join(__dirname, '..', 'pub');
const w68pub = JSON.parse(fs.readFileSync(path.join(pubDir, 'witnesses_68.json'), 'utf8'))[0].stones;
const w68sorted = w68pub.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]);
const key = (s) => JSON.stringify(s.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
const sameConfig = (a, b) => key(a) === key(b);
const report = { controls: {}, pass: true };

function setPass(name, ok, detail) {
  report.controls[name] = { pass: !!ok, detail };
  if (!ok) report.pass = false;
}

// A: positive known answer via holes mode, W=58, xMin=52.
const b58 = new Board(58);
let resA = runThree(b58, w68pub, { holes: true, xMin: 52, maxWitnesses: 2000 });
const foundA = resA.witnesses.filter(w => sameConfig(w, w68sorted));
setPass('A_positive_refind_x52', foundA.length === 1, {
  counters: { triples: resA.triples_examined, safe: resA.safe_triples, shape: resA.shape_fails, maximal: resA.safe_maximal_row_deficient, ms: resA.ms },
  refound: foundA.length === 1
});

// B: window negative xMin=56 - [52,1] unreachable.
const resB = runThree(b58, w68pub, { holes: true, xMin: 56, maxWitnesses: 2000 });
const foundB = resB.witnesses.filter(w => sameConfig(w, w68sorted));
setPass('B_window_negative_x56', foundB.length === 0, { counters: { triples: resB.triples_examined, safe: resB.safe_triples, maximal: resB.safe_maximal_row_deficient, ms: resB.ms } });

// C: unsafe-base guard (4 collinear on the diagonal, rows within capacity).
const badBase = [
  [0, 0], [7, 0], [8, 0],
  [1, 1], [9, 1], [10, 1],
  [2, 2], [11, 2], [12, 2],
  [3, 3], [13, 3], [14, 3],
  [15, 4], [16, 4], [17, 4],
  [18, 5], [19, 5], [20, 5],
  [21, 6], [22, 6]
];
let threw = false, threwMsg = '';
try { runThree(new Board(30), badBase, { xMin: 0 }); } catch (e) { threw = true; threwMsg = String(e.message); }
setPass('C_unsafe_base_guard', threw && threwMsg === 'unsafe base', { threw, threwMsg });

// D: determinism of a full repeat of A (all fields except wall-clock ms).
const resA2 = runThree(b58, w68pub, { holes: true, xMin: 52, maxWitnesses: 2000 });
const strip = (o) => JSON.stringify({ ...o, ms: 0 });
setPass('D_determinism', strip(resA) === strip(resA2), { ms_first: resA.ms, ms_second: resA2.ms });

// E: fresh-mode run, same base/window (info; every emitted witness brute-verified).
const resE = runThree(b58, w68pub, { holes: false, xMin: 52, maxWitnesses: 2000 });
report.controls['E_fresh_info_x52'] = {
  pass: true,
  detail: { counters: { triples: resE.triples_examined, safe: resE.safe_triples, shape: resE.shape_fails, maximal: resE.safe_maximal_row_deficient, ms: resE.ms } }
};

// F: brute-force verification of all witnesses from A and E.
let allOK = true, badList = [];
for (const w of resA.witnesses.concat(resE.witnesses)) {
  const v = bruteVerify(b58, w);
  if (!(v.safe && v.shape_ok && v.maximal)) { allOK = false; badList.push({ stones: w, issues: v.issues }); }
}
setPass('F_bruteforce_all_witnesses', allOK, { verified: resA.witnesses.length + resE.witnesses.length, bad: badList.slice(0, 3) });

// extra consistency: window monotonicity - every counter of the narrower window (B, x56)
// must not exceed the corresponding counter of the wider window (A, x52).
setPass('G_window_monotonicity',
  resB.triples_examined <= resA.triples_examined &&
  resB.safe_triples <= resA.safe_triples &&
  resB.safe_maximal_row_deficient <= resA.safe_maximal_row_deficient &&
  resB.ms !== undefined, {
  A: { triples: resA.triples_examined, safe: resA.safe_triples, maximal: resA.safe_maximal_row_deficient },
  B: { triples: resB.triples_examined, safe: resB.safe_triples, maximal: resB.safe_maximal_row_deficient }
});
// H: small-window naive exhaustion cross-check (declaration (b)):
//    naive = independent triple loop over (removal triple, addition triple) with every final
//    config judged purely by bruteVerify (4x4 determinant safety + triple-curve maximality),
//    no engine skip masks, no incremental caches. The set of maximal configs must equal the
//    engine's at identical settings, both in holes and fresh mode.
function naiveThree(board, base, xMin, holes) {
  const W = board.W, n = 20;
  const coords = base.map(p => [p[0], p[1]]);
  const occSet = new Set(base.map(p => p[0] + ',' + p[1]));
  const maximals = new Set(); let combos = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const remSet = new Set([i, j, k]);
    const kept = []; for (let z = 0; z < n; z++) if (!remSet.has(z)) kept.push(coords[z]);
    const rcount = new Int32Array(8); for (const p of kept) rcount[p[1]]++;
    const avail = [];
    for (let y = 0; y < 7; y++) if (rcount[y] < 3) for (let x = xMin; x < W; x++) {
      if (!occSet.has(x + ',' + y)) avail.push([x, y]);
    }
    if (holes) for (const z of [i, j, k]) if (coords[z][0] >= xMin && rcount[coords[z][1]] < 3) avail.push([coords[z][0], coords[z][1]]);
    for (let a = 0; a < avail.length; a++) for (let b = a + 1; b < avail.length; b++) for (let c = b + 1; c < avail.length; c++) {
      const final = kept.concat([avail[a], avail[b], avail[c]]);
      combos++;
      const v = bruteVerify(board, final);
      if (v.safe && v.shape_ok && v.maximal) maximals.add(key(final));
    }
  }
  return { combos, maximals };
}
{
  const t0 = Date.now();
  const naiveH = naiveThree(b58, w68pub, 56, true);
  const engineH = runThree(b58, w68pub, { holes: true, xMin: 56, maxWitnesses: 2000 });
  const engineSet = new Set(engineH.witnesses.map(key));
  let same = engineSet.size === naiveH.maximals.size;
  for (const s of engineSet) if (!naiveH.maximals.has(s)) same = false;
  for (const s of naiveH.maximals) if (!engineSet.has(s)) same = false;
  setPass('H_naive_exhaustion_holes_x56', same, { naive_combos: naiveH.combos, naive_maximals: naiveH.maximals.size, engine_maximals: engineH.safe_maximal_row_deficient, ms: Date.now() - t0 });
  const t1 = Date.now();
  const naiveHF = naiveThree(b58, w68pub, 56, false);
  const engineHF = runThree(b58, w68pub, { holes: false, xMin: 56, maxWitnesses: 2000 });
  const engineSetF = new Set(engineHF.witnesses.map(key));
  let sameF = engineSetF.size === naiveHF.maximals.size;
  for (const s of engineSetF) if (!naiveHF.maximals.has(s)) sameF = false;
  for (const s of naiveHF.maximals) if (!engineSetF.has(s)) sameF = false;
  setPass('H_naive_exhaustion_fresh_x56', sameF, { naive_combos: naiveHF.combos, naive_maximals: naiveHF.maximals.size, engine_maximals: engineHF.safe_maximal_row_deficient, ms: Date.now() - t1 });
}

// I: fresh-mode structural invariant - every emitted fresh witness diffuses from its base
// in exactly 3 cells (no 2-for-2 or weaker degeneration is representable).
{
  const bset = new Set(w68pub.map(p => p[0] + ',' + p[1]));
  let ok = true;
  // vacuous here unless fresh witnesses exist; enforced at emission in runThree and on save
  for (const w of resE.witnesses) { const sh = w.filter(p => bset.has(p[0] + ',' + p[1])).length; if (sh !== 17) ok = false; }
  setPass('I_fresh_diff3_invariant', ok, { checked: resE.witnesses.length, note: 'structural: fresh additions exclude all base cells, so |final ∩ base| = 17 by construction; asserted on save in production' });
}
report.w68_published_sorted = w68sorted;
console.log(JSON.stringify(report, null, 1));
process.exit(report.pass ? 0 : 1);
