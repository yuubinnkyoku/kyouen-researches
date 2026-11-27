// Machine-generates output/w70/calibration.json for the width-70 holes sweep:
// pinned calibrations, positive control, full w69 holes 199/199 reproduction
// cross-check, w70 run1-vs-run2 determinism, fail-closed tamper controls.
// Deterministic, no floating point.
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const main = () => {
  const bases = JSON.parse(fs.readFileSync('output/w70/bases.json', 'utf8'));
  const w68wit = JSON.parse(fs.readFileSync('output/calib/witnesses_68.json', 'utf8'))[0].stones;
  const out = { scope: 'calibration, positive control, w69 reproduction cross-check, determinism and tamper controls for the width-70 holes two-edit sweep', records: [] };
  const rec = (name, obj) => { out.records.push(Object.assign({ check: name }, obj)); };
  // 1. pinned calibration: base53 on 7x57 fresh (published: 1436643/60921/2)
  const b53 = bases.find(b => b.tag === 'pool_base53');
  let r = runCase(new Board(57), b53.stones, { holes: false });
  rec('pin_base53_w57_fresh', { rcc: r.row_capacity_candidates, safe: r.safe_candidates, maximal: r.safe_maximal_row_deficient,
    expected: { rcc: 1436643, safe: 60921, maximal: 2 }, pass: r.row_capacity_candidates === 1436643 && r.safe_candidates === 60921 && r.safe_maximal_row_deficient === 2 });
  // 2. published stats_69 calibration: w68 witness base on width 69 fresh (2141205/199290/0)
  r = runCase(new Board(69), w68wit, { holes: false });
  rec('pin_w68base_w69_fresh', { rcc: r.row_capacity_candidates, safe: r.safe_candidates, maximal: r.safe_maximal_row_deficient,
    expected: { rcc: 2141205, safe: 199290, maximal: 0 }, pass: r.row_capacity_candidates === 2141205 && r.safe_candidates === 199290 && r.safe_maximal_row_deficient === 0 });
  // 3. positive control: w65 bases at width 68 fresh -> exactly 3 producers with exactly 1, all identical to the published w68 witness
  const w65 = bases.filter(b => b.tag === 'w65');
  let producers = 0, identical = 0;
  for (const b of w65) {
    const rr = runCase(new Board(68), b.stones, { holes: false });
    if (rr.safe_maximal_row_deficient === 1) { producers++; if (JSON.stringify(rr.witnesses[0]) === JSON.stringify(w68wit)) identical++; }
  }
  rec('positive_control_w65_w68', { w65_bases: w65.length, producers_with_exactly_1: producers, identical_to_published_w68: identical,
    expected: { producers: 3, identical: 3 }, pass: producers === 3 && identical === 3 });
  // 4. machinery cross-check: full 199/199 reproduction of the published width-69 holes records
  const pub = new Map();
  for (const line of fs.readFileSync('output/calib/published_w69_holes.jsonl', 'utf8').split('\n')) {
    if (!line.trim()) continue;
    const p = JSON.parse(line);
    pub.set(p.idx, [p.tag, p.sig, p.rcc, p.safe, p.shape_errors, p.maximal]);
  }
  const rep = new Map();
  for (const line of fs.readFileSync('output/calib/repro_w69_holes.jsonl', 'utf8').split('\n')) {
    if (!line.trim()) continue;
    const p = JSON.parse(line);
    rep.set(p.idx, [p.tag, p.sig, p.rcc, p.safe, p.shape_errors, p.maximal]);
  }
  let reproMatch = 0;
  for (const [idx, v] of pub) if (String(rep.get(idx)) === String(v)) reproMatch++;
  rec('w69_holes_full_reproduction', { published_records: pub.size, reproduced: rep.size, matches: reproMatch,
    expected: { matches: 199 }, pass: pub.size === 199 && rep.size === 199 && reproMatch === 199 });
  // 5. determinism: w70 holes run1 vs run2, all 199 records identical modulo ms
  const l1 = fs.readFileSync('output/w70/results_holes70_run1.jsonl', 'utf8').split('\n').filter(Boolean).map(JSON.parse);
  const l2 = fs.readFileSync('output/w70/results_holes70_run2.jsonl', 'utf8').split('\n').filter(Boolean).map(JSON.parse);
  let det = 0;
  const strip = (o) => { const c = Object.assign({}, o); delete c.ms; return JSON.stringify(c); };
  if (l1.length === 199 && l2.length === 199) {
    const m2 = new Map(l2.map(o => [strip(o), true]));
    det = l1.filter(o => m2.has(strip(o))).length;
  }
  rec('determinism_w70_run1_vs_run2', { run1_records: l1.length, run2_records: l2.length, identical_records: det,
    expected: { identical: 199 }, pass: det === 199 });
  // 6. tamper controls at width 70: fail-closed expected
  const t1 = b53.stones.map((p, i) => i === 0 ? [p[0] + 1, p[1]] : p.slice());
  let t1res;
  try { runCase(new Board(70), t1, { holes: true }); t1res = 'RAN (unexpected)'; } catch (e) { t1res = 'fail-closed: ' + e.message; }
  const t2 = b53.stones.slice(0, 19);
  let t2res;
  try { runCase(new Board(70), t2, { holes: true }); t2res = 'RAN (unexpected)'; } catch (e) { t2res = 'fail-closed: ' + e.message; }
  rec('tamper_controls_w70', { one_stone_moved: t1res, one_stone_removed: t2res, pass: t1res.startsWith('fail-closed') && t2res.startsWith('fail-closed') });
  // 7. headline aggregate of run1 (bookkeeping)
  let rcc = 0, safe = 0, se = 0, mx = 0;
  for (const o of l1) { rcc += o.rcc; safe += o.safe; se += o.shape_errors; mx += o.maximal; }
  rec('w70_holes_run1_aggregate', { bases: l1.length, row_capacity_candidates: rcc, safe_candidates: safe, shape_errors: se, safe_maximal_row_deficient: mx,
    pass: l1.length === 199 && mx === 0 });
  out.all_pass = out.records.every(r => r.pass);
  fs.writeFileSync('output/w70/calibration.json', JSON.stringify(out, null, 1) + '\n');
  console.log('all_pass', out.all_pass);
};
main();
