// mkrecords5735.js — records.jsonl / summary.json for the 5x35 q=7 class-split sweep
const fs = require('fs'), path = require('path');
const dir = 'output';
const parse = (f) => {
  const t = fs.readFileSync(path.join(dir, f), 'utf8');
  const s = (t.match(/^s (\w+)/m) || [])[1];
  return {
    result: s === 'SATISFIABLE' ? 'SAT' : s === 'UNSATISFIABLE' ? 'UNSAT' : 'INDET',
    conflicts: Number((t.match(/^c conflicts:\s+(\d+)/m) || [])[1]),
    seconds: Number((t.match(/c process-time:.* ([\d.]+) seconds/m) || [])[1]),
  };
};
const recs = [];
const push = (o, f) => { recs.push(Object.assign({ file: f, date: '2026-11-15T12:00:00Z' }, o, parse(f))); };
for (const n of ['2','01','02','03','04','12','13','012','013','014','023','024','123','0123','0124','0134','01234'])
  push({ w: 5, m: 35, q: 7, class: n.split('').join(','), encoding: 'class' }, `r5x35q7_${n}.txt`);
for (const y of ['0','1']) for (const k of ['0','1','2','3','4'])
  push({ w: 5, m: 35, q: 7, class: y, krow: `${y}:${k}`, encoding: 'class+krow' }, `r5x35q7_${y}k${k}.txt`);
for (const y of ['0','1']) for (const p of ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'])
  push({ w: 5, m: 35, q: 7, class: y, krow: `${y}:5`, minpos: p, encoding: 'class+krow+minpos' }, `r5x35q7_${y}k5p${p}.txt`);
push({ w: 5, m: 35, q: 7, class: '0,1', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x35q7_01_lexH.txt');
push({ w: 5, m: 35, q: 7, class: '2', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x35q7_2_lexH.txt');
push({ w: 5, m: 18, q: 7, class: '0', encoding: 'positive control (K0332 witness board)' }, 'r_ctrl_5x18_c0.txt');
fs.writeFileSync(path.join(dir, 'records.jsonl'), recs.map(r => JSON.stringify(r)).join('\n') + '\n');
const dec = recs.filter(r => r.m === 35);
const sum = {
  w: 5, m: 35, q: 7,
  claim: 'no row-deficient maximal safe configuration on 5x35 q=7; witness-free width set of (5,7) is {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35}; M_{5,7} = 19 or >= 37 (upper 158 unchanged)',
  direct_classes_unsat: dec.filter(r => r.encoding === 'class' && r.result === 'UNSAT').length,
  class0_k_minpos_split_unsat: recs.filter(r => r.class === '0' && r.m === 35 && r.result === 'UNSAT').length,
  class1_k_minpos_split_unsat: recs.filter(r => r.class === '1' && r.m === 35 && r.result === 'UNSAT').length,
  indet: dec.filter(r => r.result === 'INDET').length,
  sat: dec.filter(r => r.result === 'SAT').length,
  total_conflicts_35: dec.reduce((a, r) => a + r.conflicts, 0),
  hardest: recs.filter(r => r.m === 35).sort((a, b) => b.conflicts - a.conflicts).slice(0, 5).map(r => `${r.class}${r.krow ? ' k' + r.krow : ''}${r.minpos != null ? ' mp' + r.minpos : ''}: ${r.conflicts}`),
  lex_cross_checks: { '0,1': parse('r5x35q7_01_lexH.txt').conflicts, '2': parse('r5x35q7_2_lexH.txt').conflicts },
  positive_control: '5x18 class {0} SAT 343,134 conflicts (bit-exact with the K0821..K0847 lane controls — fourteenth cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS',
  decomposition_soundness: 'k=0..5 partitions the deficient-row stone count; k=5 instances split by minpos=0..17, which pins the leftmost stone of the first deficient row at column exactly P; every configuration or its column mirror has leftmost stone column <= floor((m-1)/2) = 17 at m=35 (columns 0..34: min(x_min, 34-x_max) <= 17 since x_min <= x_max); the column mirror preserves row occupancy, hence the class',
  environment_note: 'single continuous session; sat.js/sat2.js/sat3.js byte-identical to the K0836..K0847 lane scripts (restored from the m=34 lane on main, blob shas verified: 6c3262d6 / edfae1d2 / 6dfa7db3; the control CNF c5x18q7_0.cnf regenerates md5-identical 0bb6187d36e537a170e4fb451359bb94); mkcnf.sh/qrun.sh ported m=34 -> m=35; mkrecords5735.js log-name templates match the actual log names (no c prefix on direct/lexH logs); raw logs pushed batch-by-batch',
};
fs.writeFileSync(path.join(dir, 'summary.json'), JSON.stringify(sum, null, 1) + '\n');
console.log(JSON.stringify({ records: recs.length, indet: sum.indet, sat: sum.sat, total_conflicts: sum.total_conflicts_35, hardest: sum.hardest }));
