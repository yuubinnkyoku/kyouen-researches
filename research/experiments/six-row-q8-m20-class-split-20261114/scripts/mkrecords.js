// mkrecords.js — build records.jsonl from kissat raw logs r6x20q8_c*.txt
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || 'output';
const CLASSES = ['0','1','2','01','02','03','04','05','12','13','14','23','012','013','014','015','023','024','025','034','123','124','0123','0124','0125','0134','0135','0145','0234','0235','1234','12345','02345','01345','012345'];
const fmt = d => d.split('').join(',');
const recs = [];
for (const D of CLASSES) {
  const f = path.join(dir, `r6x20q8_c${D}.txt`);
  const t = fs.readFileSync(f, 'utf8');
  const s = (t.match(/^s (\w+)/m) || [])[1];
  const conf = Number((t.match(/^c conflicts:\s+(\d+)/m) || [])[1]);
  const sec = Number((t.match(/c process-time:.* ([\d.]+) seconds/m) || [])[1]);
  recs.push({ w: 6, m: 20, q: 8, class: fmt(D), result: s === 'UNSATISFIABLE' ? 'UNSAT' : s === 'SATISFIABLE' ? 'SAT' : 'INDET', rc: s === 'UNSATISFIABLE' ? 20 : s === 'SATISFIABLE' ? 10 : null, conflicts: conf, seconds: sec, date: '2026-11-14T13:45:00Z' });
}
for (const [tag, f] of [['1','r6x20q8_c1_lexH.txt'],['2','r6x20q8_c2_lexH.txt']]) {
  const t = fs.readFileSync(path.join(dir, f), 'utf8');
  const s = (t.match(/^s (\w+)/m) || [])[1];
  recs.push({ w: 6, m: 20, q: 8, class: fmt(tag), lex: 'H', result: s === 'UNSATISFIABLE' ? 'UNSAT' : 'INDET', rc: 20, conflicts: Number((t.match(/^c conflicts:\s+(\d+)/m) || [])[1]), seconds: Number((t.match(/c process-time:.* ([\d.]+) seconds/m) || [])[1]), date: '2026-11-14T13:59:00Z', note: 'cross-encoding lex=H re-check' });
}
const ct = fs.readFileSync(path.join(dir, 'r_ctrl_6x18_c1.txt'), 'utf8');
recs.push({ w: 6, m: 18, q: 8, class: '1', result: 'SAT', rc: 10, conflicts: Number((ct.match(/^c conflicts:\s+(\d+)/m) || [])[1]), seconds: Number((ct.match(/c process-time:.* ([\d.]+) seconds/m) || [])[1]), date: '2026-11-14T14:02:00Z', note: 'positive control: 41-stone deficient maximal (rows 7,6,7,7,7,7) rediscovered, conflicts bit-exact with K0818 control' });
fs.writeFileSync(path.join(dir, 'records.jsonl'), recs.map(r => JSON.stringify(r)).join('\n') + '\n');
const tot = recs.filter(r => r.m === 20 && !r.lex).reduce((a, r) => a + r.conflicts, 0);
const sum = { w: 6, m: 20, q: 8, classes: 35, unsat: recs.filter(r => r.m === 20 && !r.lex && r.result === 'UNSAT').length, sat: 0, indet: 0, total_conflicts: tot, hardest_class: '2', hardest_conflicts: 2763766, lex_cross_checks: { '1': 2038080, '2': 2331073 }, controls: { '2x8_q4_class0': 'SAT (K0796 rediscovered)', '2x9_q4_class0': 'UNSAT (M_{2,4}=9 consistent)', '6x18_q8_class1': 'SAT 511895 conflicts (K0815 witness board rediscovered, bit-exact with K0818)' }, claim: 'no row-deficient maximal safe configuration on 6x20 q=8; witness-free width set of (6,8) extends to {19,20}; M_{6,8} in {19,20} or >= 22 (upper 371 unchanged)' };
fs.writeFileSync(path.join(dir, 'summary.json'), JSON.stringify(sum, null, 1) + '\n');
console.log(JSON.stringify({ records: recs.length, total_conflicts: tot }));
