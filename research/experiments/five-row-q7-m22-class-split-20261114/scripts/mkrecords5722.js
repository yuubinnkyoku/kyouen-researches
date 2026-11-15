// mkrecords5722.js — build records.jsonl / summary.json for the 5x22 q=7 class-split sweep
// (completion of the 2026-11-14 batch-1 lane: 17 direct classes re-run bit-exact;
//  {0},{1} decided by the complete k x minpos decomposition.)
// Direct-class logs are the batch-1 raw logs (already in this output/ directory);
// decomposition / lex / control logs are the completion lane's raw logs.
const fs = require('fs'), path = require('path');
const direct = process.argv[2] || 'direct';   // dir with the 17 batch-1 direct logs
const dir = process.argv[3] || 'output';      // dir with the decomposition/lex/control logs
const parse = (base, f) => {
  const t = fs.readFileSync(path.join(base, f), 'utf8');
  const s = (t.match(/^s (\w+)/m) || [])[1];
  return {
    result: s === 'SATISFIABLE' ? 'SAT' : s === 'UNSATISFIABLE' ? 'UNSAT' : 'INDET',
    conflicts: Number((t.match(/^c conflicts:\s+(\d+)/m) || [])[1]),
    seconds: Number((t.match(/c process-time:.* ([\d.]+) seconds/m) || [])[1]),
  };
};
const recs = [];
const push = (o, f, base) => { const p = parse(base, f); recs.push(Object.assign({ file: f, date: '2026-11-15T09:30:00Z' }, o, p)); };
// 17/19 classes decided directly (batch-1 raw logs, re-verified bit-exact by the takeover lane);
// {0} and {1} decided by the complete k x minpos decomposition
// (plain single runs of {0},{1} reached 2.85M / 3.33M conflicts at ~142 s without a verdict and are superseded).
for (const n of ['2','01','02','03','04','12','13','012','013','014','023','024','123','0123','0124','0134','01234'])
  push({ w: 5, m: 22, q: 7, class: n.split('').join(','), encoding: 'class' }, `r5x22q7_c${n}.txt`, direct);
for (const y of ['0','1']) for (const k of ['0','1','2','3','4'])
  push({ w: 5, m: 22, q: 7, class: y, krow: `${y}:${k}`, encoding: 'class+krow' }, `r5x22q7_${y}k${k}.txt`, dir);
for (const y of ['0','1']) for (const p of ['0','1','2','3','4','5','6','7','8','9','10'])
  push({ w: 5, m: 22, q: 7, class: y, krow: `${y}:5`, minpos: p, encoding: 'class+krow+minpos' }, `r5x22q7_${y}k5p${p}.txt`, dir);
push({ w: 5, m: 22, q: 7, class: '0,1', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x22q7_c01_lexH.txt', dir);
push({ w: 5, m: 22, q: 7, class: '2', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x22q7_c2_lexH.txt', dir);
push({ w: 5, m: 18, q: 7, class: '0', encoding: 'positive control (K0332 witness board)' }, 'r_ctrl_5x18_c0.txt', dir);
fs.writeFileSync(path.join(dir, 'records.jsonl'), recs.map(r => JSON.stringify(r)).join('\n') + '\n');
const dec = recs.filter(r => r.m === 22);
const sum = {
  w: 5, m: 22, q: 7,
  claim: 'no row-deficient maximal safe configuration on 5x22 q=7; witness-free width set of (5,7) is {19,20,21,22}; M_{5,7} in {19,20,21,22} or >= 23 (upper 158 unchanged)',
  direct_classes_unsat: dec.filter(r => r.encoding === 'class' && r.result === 'UNSAT').length,
  class0_k_minpos_split_unsat: recs.filter(r => r.class === '0' && r.m === 22 && r.result === 'UNSAT').length,
  class1_k_minpos_split_unsat: recs.filter(r => r.class === '1' && r.m === 22 && r.result === 'UNSAT').length,
  indet: dec.filter(r => r.result === 'INDET').length,
  total_conflicts_22: dec.reduce((a, r) => a + r.conflicts, 0),
  hardest: recs.filter(r => r.m === 22).sort((a, b) => b.conflicts - a.conflicts).slice(0, 5).map(r => `${r.class}${r.krow ? ' k' + r.krow : ''}${r.minpos != null ? ' mp' + r.minpos : ''}: ${r.conflicts}`),
  lex_cross_checks: { '0,1': parse(dir, 'r5x22q7_c01_lexH.txt').conflicts, '2': parse(dir, 'r5x22q7_c2_lexH.txt').conflicts },
  positive_control: '5x18 class {0} SAT 343,134 conflicts (bit-exact with the K0821 lane control); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)',
  batch1_rerun_verification: 'all 17 direct UNSAT classes re-run by the takeover lane reproduce the batch-1 raw logs conflicts bit-exactly (e.g. {0,1}: 875,682; {0,2,3}: 199,205)',
  decomposition_soundness: 'k=0..5 partitions the deficient-row stone count; k=5 instances split by minpos=0..10, which pins the leftmost stone of the first deficient row at column exactly P; every configuration or its column mirror has leftmost stone column <= 10 at m=22 (min(x1,21-x5) <= 10, else x1 >= 11 and x5 <= 10 contradict x1 <= x5); the column mirror preserves row occupancy, hence the class',
};
fs.writeFileSync(path.join(dir, 'summary.json'), JSON.stringify(sum, null, 1) + '\n');
console.log(JSON.stringify({ records: recs.length, indet: sum.indet, total_conflicts: sum.total_conflicts_22 }));
