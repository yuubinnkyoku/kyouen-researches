// Machine-generates output/w69/calibration.json: pinned calibrations, positive
// control (width-68 unique witness via the three w65 bases), determinism
// re-runs and fail-closed tamper controls. Deterministic, no floating point.
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const main = () => {
  const bases = JSON.parse(fs.readFileSync('output/w69/bases.json', 'utf8'));
  const w68wit = JSON.parse(fs.readFileSync('output/w68/witnesses_68.json', 'utf8'))[0].stones;
  const out = { scope: 'calibration, positive control, determinism and tamper controls for the width-69 two-edit sweep', records: [] };
  const rec = (name, obj) => { out.records.push(Object.assign({ check: name }, obj)); };
  // 1. pinned calibration: base53 on 7x57 fresh (published: 1436643/60921/2)
  const b53 = bases.find(b => b.tag === 'pool_base53');
  let r = runCase(new Board(57), b53.stones, { holes: false });
  rec('pin_base53_w57_fresh', { rcc: r.row_capacity_candidates, safe: r.safe_candidates, maximal: r.safe_maximal_row_deficient,
    expected: { rcc: 1436643, safe: 60921, maximal: 2 }, pass: r.row_capacity_candidates === 1436643 && r.safe_candidates === 60921 && r.safe_maximal_row_deficient === 2 });
  // 2. published stats_69 calibration: w68 witness base on width 69 (2141205/199290/0)
  r = runCase(new Board(69), w68wit, { holes: false });
  rec('pin_w68base_w69_fresh', { rcc: r.row_capacity_candidates, safe: r.safe_candidates, maximal: r.safe_maximal_row_deficient,
    expected: { rcc: 2141205, safe: 199290, maximal: 0 }, pass: r.row_capacity_candidates === 2141205 && r.safe_candidates === 199290 && r.safe_maximal_row_deficient === 0 });
  // 3. positive control: w65 bases at width 68 fresh -> exactly 3 with exactly 1, all identical to the published w68 witness
  const w65 = bases.filter(b => b.tag === 'w65');
  let producers = 0, identical = 0;
  for (const b of w65) {
    const rr = runCase(new Board(68), b.stones, { holes: false });
    if (rr.safe_maximal_row_deficient === 1) { producers++; if (JSON.stringify(rr.witnesses[0]) === JSON.stringify(w68wit)) identical++; }
  }
  rec('positive_control_w65_w68', { w65_bases: w65.length, producers_with_exactly_1: producers, identical_to_published_w68: identical,
    expected: { producers: 3, identical: 3 }, pass: producers === 3 && identical === 3 });
  // 4. determinism: re-run 3 fresh records and compare with results.jsonl
  const res = fs.readFileSync('output/w69/results.jsonl', 'utf8').split('\n').filter(Boolean).map(JSON.parse);
  let det = [];
  for (const idx of [0, 50, 100]) {
    const s = res.find(x => x.idx === idx);
    const rr = runCase(new Board(69), bases[idx].stones, { holes: false });
    det.push({ idx, match: rr.row_capacity_candidates === s.rcc && rr.safe_candidates === s.safe && rr.safe_maximal_row_deficient === s.maximal });
  }
  rec('determinism_fresh_rerun', { checks: det, pass: det.every(d => d.match) });
  // 5. tamper controls: fail-closed expected
  const t1 = b53.stones.map((p, i) => i === 0 ? [p[0] + 1, p[1]] : p.slice());
  let t1res;
  try { runCase(new Board(69), t1, { holes: false }); t1res = 'RAN (unexpected)'; } catch (e) { t1res = 'fail-closed: ' + e.message; }
  const t2 = b53.stones.slice(0, 19);
  let t2res;
  try { runCase(new Board(69), t2, { holes: false }); t2res = 'RAN (unexpected)'; } catch (e) { t2res = 'fail-closed: ' + e.message; }
  rec('tamper_controls', { one_stone_moved: t1res, one_stone_removed: t2res, pass: t1res.startsWith('fail-closed') && t2res.startsWith('fail-closed') });
  out.all_pass = out.records.every(r => r.pass);
  fs.writeFileSync('output/w69/calibration.json', JSON.stringify(out, null, 1) + '\n');
  console.log('all_pass', out.all_pass);
};
main();
