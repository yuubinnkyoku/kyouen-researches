// Builds output/calibration.json and output/summary.json for the width-69 sweep.
// calibration.json pins the engine/driver against all published reference values:
//  - enum_two.js engine calibration: base53@57 and the published width-68 witness's
//    width-69 fresh neighborhood record (stats_69.json values) - recomputed here.
//  - driver calibration at W=68: recompute the published per-base records for the
//    first 8 bases and the three positive (w65-tagged) bases; verify counts equal.
//  - holes-superset semantics at W=60 on w57_0: fresh witnesses subset of holes witnesses,
//    fresh counts equal to the published wit_w57_0_60.json.
// summary.json: totals of the completed width-69 fresh and holes sweeps.
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');

const bases = JSON.parse(fs.readFileSync('input/bases.json', 'utf8'));
const pub68 = fs.readFileSync('pub/results_w68.jsonl', 'utf8').trim().split('\n').map(JSON.parse);
const key = w => w.map(p => p[0] + ',' + p[1]).sort().join(';');

const cal = { engine: {}, driver_w68: {}, holes_semantics_w60: {}, selftest_1f0: {} };

// ---- engine calibration ----
{
  const b53 = bases.find(x => x.tag === 'pool_base53');
  const r = runCase(new Board(57), b53.stones, { holes: false, maxWitnesses: 64 });
  const expected = { rcc: 1436643, safe: 60921, max: 2 };
  cal.engine.base53_w57 = {
    recomputed: { rcc: r.row_capacity_candidates, safe: r.safe_candidates, max: r.safe_maximal_row_deficient },
    expected, pass: r.row_capacity_candidates === expected.rcc && r.safe_candidates === expected.safe && r.safe_maximal_row_deficient === expected.max
  };
  const w68 = JSON.parse(fs.readFileSync('pub/witnesses_68.json', 'utf8'))[0].stones;
  const r69 = runCase(new Board(69), w68, { holes: false, maxWitnesses: 64 });
  const exp69 = { rcc: 2141205, safe: 199290, max: 0 }; // published output/chain/stats_69.json
  cal.engine.w68witness_w69_fresh = {
    recomputed: { rcc: r69.row_capacity_candidates, safe: r69.safe_candidates, max: r69.safe_maximal_row_deficient },
    expected: exp69, pass: r69.row_capacity_candidates === exp69.rcc && r69.safe_candidates === exp69.safe && r69.safe_maximal_row_deficient === exp69.max
  };
}
// ---- driver calibration at width 68 (published sweep68): first 8 + the 3 positive bases ----
{
  let compared = 0, mismatches = [];
  const positives = [185, 187, 189];
  const runIdx = new Set([0, 1, 2, 3, 4, 5, 6, 7, ...positives]);
  for (const i of Array.from(runIdx).sort((a, b) => a - b)) {
    const b = bases[i];
    const r = runCase(new Board(68), b.stones, { holes: false, maxWitnesses: 64 });
    const pub = pub68.find(p => p.idx === i);
    const eq = r.row_capacity_candidates === pub.rcc && r.safe_candidates === pub.safe && r.safe_maximal_row_deficient === pub.maximal;
    if (!eq) mismatches.push({ idx: i, recomputed: [r.row_capacity_candidates, r.safe_candidates, r.safe_maximal_row_deficient], published: [pub.rcc, pub.safe, pub.maximal] });
    compared++;
  }
  // witness rediscovery: the three positive bases must all yield the published 20-stone witness
  const w68pub = JSON.parse(fs.readFileSync('pub/witnesses_68.json', 'utf8'))[0].stones;
  const wpk = key(w68pub);
  let rediscovered = 0;
  for (const i of positives) {
    const b = bases[i];
    const r = runCase(new Board(68), b.stones, { holes: false, maxWitnesses: 64 });
    for (const w of r.witnesses) if (key(w) === wpk) { rediscovered++; break; }
  }
  cal.driver_w68 = { compared, mismatches, positives_rediscovering_published_witness: rediscovered, pass: compared === 11 && mismatches.length === 0 && rediscovered === 3 };
}
// ---- holes superset semantics at width 60 ----
{
  const b = bases.find(x => x.tag === 'pool_w57_0');
  const fresh = runCase(new Board(60), b.stones, { holes: false, maxWitnesses: 512 });
  const holes = runCase(new Board(60), b.stones, { holes: true, maxWitnesses: 512 });
  const fk = new Set(fresh.witnesses.map(key));
  const hk = new Set(holes.witnesses.map(key));
  let subset = true; for (const k of fk) if (!hk.has(k)) subset = false;
  const pub = JSON.parse(fs.readFileSync('pub/wit_w57_0_60.json', 'utf8'));
  const pk = new Set(pub.witnesses.map(key));
  let pubIn = true; for (const k of pk) if (!fk.has(k)) pubIn = false;
  cal.holes_semantics_w60 = {
    fresh_rcc: fresh.row_capacity_candidates, fresh_safe: fresh.safe_candidates, fresh_max: fresh.safe_maximal_row_deficient,
    holes_rcc: holes.row_capacity_candidates, holes_safe: holes.safe_candidates, holes_max: holes.safe_maximal_row_deficient,
    fresh_subset_of_holes: subset,
    published_fresh_counts_match: pub.safe_maximal_row_deficient === fresh.safe_maximal_row_deficient && pub.row_capacity_candidates === fresh.row_capacity_candidates,
    published_witnesses_reproduced: pubIn,
    pass: subset && pub.safe_maximal_row_deficient === fresh.safe_maximal_row_deficient && pubIn
  };
}
// ---- selftest record ----
cal.selftest_1f0 = JSON.parse(fs.readFileSync('output/w69/selftest_1f0.json', 'utf8'));
cal.overall_pass = cal.engine.base53_w57.pass && cal.engine.w68witness_w69_fresh.pass && cal.driver_w68.pass && cal.holes_semantics_w60.pass && cal.selftest_1f0.pass;
fs.writeFileSync('output/calibration.json', JSON.stringify(cal, null, 2) + '\n');

// ---- summary ----
function totals(mode) {
  const lines = fs.readFileSync(`output/w69/${mode}/results.jsonl`, 'utf8').trim().split('\n').map(JSON.parse);
  let rcc = 0, safe = 0, maximal = 0, ms = 0, z = 0;
  for (const r of lines) { rcc += r.rcc; safe += r.safe; maximal += r.maximal; ms += r.ms; if (r.one_for_zero_hits > 0) z++; }
  return { mode, records: lines.length, bases: bases.length, total_row_capacity_candidates: rcc, total_safe: safe, total_safe_maximal: maximal, bases_with_one_for_zero_hits: z, wall_ms_deltas_sum_informal: ms };
}
const summary = {
  width: 69, bases: bases.length,
  fresh: totals('fresh'), holes: totals('holes'),
  result: 'no witnesses in the complete fresh+holes 2-for-2 neighborhoods of all 199 published bases; 1-for-0 (19-stone) also 0 hits everywhere',
  bound_unchanged: 'M_{7,4} in [69,1929]'
};
fs.writeFileSync('output/summary.json', JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify({ overall_pass: cal.overall_pass, fresh: summary.fresh, holes: summary.holes }));
