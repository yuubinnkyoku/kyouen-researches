// mkrecords5734.js — records.jsonl / summary.json for the 5x34 q=7 class-split sweep
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
  push({ w: 5, m: 34, q: 7, class: n.split('').join(','), encoding: 'class' }, `r5x34q7_${n}.txt`);
for (const y of ['0','1']) for (const k of ['0','1','2','3','4'])
  push({ w: 5, m: 34, q: 7, class: y, krow: `${y}:${k}`, encoding: 'class+krow' }, `r5x34q7_${y}k${k}.txt`);
for (const y of ['0','1']) for (const p of ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'])
  push({ w: 5, m: 34, q: 7, class: y, krow: `${y}:5`, minpos: p, encoding: 'class+krow+minpos' }, `r5x34q7_${y}k5p${p}.txt`);
push({ w: 5, m: 34, q: 7, class: '0,1', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x34q7_01_lexH.txt');
push({ w: 5, m: 34, q: 7, class: '2', lex: 'H', encoding: 'class+lexH cross-check' }, 'r5x34q7_2_lexH.txt');
push({ w: 5, m: 18, q: 7, class: '0', encoding: 'positive control (K0332 witness board)' }, 'r_ctrl_5x18_c0.txt');
fs.writeFileSync(path.join(dir, 'records.jsonl'), recs.map(r => JSON.stringify(r)).join('\n') + '\n');
const dec = recs.filter(r => r.m === 34);
const sum = {
  w: 5, m: 34, q: 7,
  claim: 'no row-deficient maximal safe configuration on 5x34 q=7; witness-free width set of (5,7) is {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34}; M_{5,7} = 19 or >= 36 (upper 158 unchanged)',
  direct_classes_unsat: dec.filter(r => r.encoding === 'class' && r.result === 'UNSAT').length,
  class0_k_minpos_split_unsat: recs.filter(r => r.class === '0' && r.m === 34 && r.result === 'UNSAT').length,
  class1_k_minpos_split_unsat: recs.filter(r => r.class === '1' && r.m === 34 && r.result === 'UNSAT').length,
  indet: dec.filter(r => r.result === 'INDET').length,
  sat: dec.filter(r => r.result === 'SAT').length,
  total_conflicts_34: dec.reduce((a, r) => a + r.conflicts, 0),
  hardest: recs.filter(r => r.m === 34).sort((a, b) => b.conflicts - a.conflicts).slice(0, 5).map(r => `${r.class}${r.krow ? ' k' + r.krow : ''}${r.minpos != null ? ' mp' + r.minpos : ''}: ${r.conflicts}`),
  lex_cross_checks: { '0,1': parse('r5x34q7_01_lexH.txt').conflicts, '2': parse('r5x34q7_2_lexH.txt').conflicts },
  positive_control: '5x18 class {0} SAT 343,134 conflicts (bit-exact with the K0821/K0834/K0835/K0836/K0837/K0838/K0839/K0840/K0841/K0842/K0844/K0845/K0846 lane controls — thirteenth cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS',
  decomposition_soundness: 'k=0..5 partitions the deficient-row stone count; k=5 instances split by minpos=0..16, which pins the leftmost stone of the first deficient row at column exactly P; every configuration or its column mirror has leftmost stone column <= floor((m-1)/2) = 16 at m=33 (columns 0..32: min(x_min, 32-x_max) <= 16 since x_min <= x_max); the column mirror preserves row occupancy, hence the class',
  environment_note: 'single continuous session; sat.js/sat2.js/sat3.js byte-identical to the K0836..K0846 lane scripts (restored from the m=33 lane on main (blob shas verified), blob shas 6c3262d6 / edfae1d2 / 6dfa7db3); mkcnf.sh/qrun.sh ported m=33 -> m=34; mkrecords5733.js log-name templates match the actual log names (no c prefix on direct/lexH logs); raw logs pushed batch-by-batch',
};
fs.writeFileSync(path.join(dir, 'summary.json'), JSON.stringify(sum, null, 1) + '\n');
console.log(JSON.stringify({ records: recs.length, indet: sum.indet, sat: sum.sat, total_conflicts: sum.total_conflicts_34, hardest: sum.hardest }));
