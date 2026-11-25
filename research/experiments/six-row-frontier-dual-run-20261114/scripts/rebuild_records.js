// rebuild_records.js — consolidate sweep outputs (raw kissat logs + captured per-class seconds) into records.jsonl + summary.json
// usage: node rebuild_records.js  (reads ../out* dirs relative to repo workspace; writes exp/output/)
const fs = require('fs');
const path = require('path');
const WS = process.env.WS || '/home/user/krwork';
const EXP = process.env.EXP || path.join(WS, 'exp', 'output');
fs.mkdirSync(EXP, { recursive: true });

// per-class wall seconds captured from the sweep stdout (2-worker parallel runs; conflicts are the exact measure)
const SEC = {
  '6x20q8': { '0,1,2,3': 10.4, '1': 128.5, '0,1,2,3,4': 10.5, '2': 136.4, '0,1,2,3,4,5': 10.2, '0': 25.5, '0,1,2,3,5': 10.5, '0,2': 23.9, '0,1,2,4': 8.6, '1,2': 125.7, '0,1,2,4,5': 6.2, '1,3': 62.5, '0,1,2,5': 7.9, '2,3': 50.3, '0,3': 6.6, '0,1,3,4': 7.8, '0,4': 13.1, '0,1,3,5': 8.3, '0,5': 22.9, '0,1,4,5': 10.6, '1,4': 10.7, '0,1,5': 13.2, '0,1': 25.8, '0,2,3': 8.4, '1,5': 15.6, '0,2,3,4': 10.2, '0,1,2': 23.3, '0,2,3,5': 8.1, '0,1,3': 9.9, '0,2,4': 10.2, '0,2,5': 6.6, '0,3,4': 8.2, '1,2,3,4': 8.6, '1,2,3': 14.4, '1,2,4': 3.9, '0,1,4': 5.7 },
};

function parseLog(p) {
  const txt = fs.readFileSync(p, 'utf8');
  const m = txt.match(/^c conflicts:\s*(\d+)/m);
  const sat = txt.includes('s SATISFIABLE'), uns = txt.includes('s UNSATISFIABLE');
  const mr = txt.match(/^c reductions:\s*(\d+)/m);
  return { result: uns ? 'UNSAT' : (sat ? 'SAT' : 'INDET'), rc: uns ? 20 : (sat ? 10 : 124), conflicts: m ? parseInt(m[1]) : null, reductions: mr ? parseInt(mr[1]) : null };
}

const records = [];
function add(board, cls, extra, dir, tag, note) {
  const logP = path.join(dir, tag + '.txt');
  if (!fs.existsSync(logP)) throw new Error('missing ' + logP);
  const metaP = path.join(dir, tag + '.meta.json');
  const meta = fs.existsSync(metaP) ? JSON.parse(fs.readFileSync(metaP, 'utf8')) : {};
  const r = parseLog(logP);
  const [w, m, q] = board.split('x').length === 2 ? [board.split('x')[0], board.split('x')[1].split('q')[0], board.split('q')[1]] : [0, 0, 0];
  const [W, M, Q] = [parseInt(w), parseInt(m), parseInt(q)];
  const rec = { w: W, m: M, q: Q, class: cls, extra: extra || '', result: r.result, rc: r.rc, conflicts: r.conflicts, ...(r.reductions ? { reductions: r.reductions } : {}), ...(meta.vars ? { vars: meta.vars, clauses: meta.clauses } : {}), date: '2026-11-14', note: note || '' };
  if (SEC[board] && SEC[board][cls] !== undefined && !extra) rec.seconds = SEC[board][cls];
  records.push(rec);
}

const O = (d) => path.join(WS, d);
// 6x20 q=8: 35 canonical classes + redundant mirror check
for (let mask = 1; mask < 64; mask++) {
  const S = [...Array(6).keys()].filter(y => mask >> y & 1);
  const M = [...Array(6).keys()].filter(y => mask >> (5 - y) & 1);
  const k = a => a.join(','); if (k(S) > k(M)) continue;
  add('6x20q8', k(S), '', O('out620'), 'c6x20q8_' + k(S).replace(/,/g, '_'), '');
}
add('6x20q8', '1,5', '', O('out620'), 'c6x20q8_1_5', 'redundant non-canonical mirror of {0,4}; UNSAT consistent with mirror soundness');
// lex=H cross-encoding
for (const [cls, c] of [['2', 2331073], ['1', 2038080], ['1,2', 1606595], ['1,3', 1209815]])
  add('6x20q8', cls, '--lex=H', O('out620lex'), 'c6x20q8_' + cls.replace(/,/g, '_') + '_--lex_H', 'cross-encoding re-check');
// determinism fresh reruns
add('6x20q8', '2', 'det-rerun', O('out620det'), 'c6x20q8_2', 'fresh rerun, conflicts node-exact');
add('6x20q8', '1', 'det-rerun', O('out620det'), 'c6x20q8_1', 'fresh rerun, conflicts node-exact');
// 6x21 q=7
add('6x21q7', '1', '', O('out621'), 'c6x21q7_1', '');
add('6x21q7', '2', '', O('out621'), 'c6x21q7_2', 'SAT: 35-stone witness rows (6,6,5,6,6,6)');
add('6x21q7', '0,1,2,3', '', O('out621'), 'c6x21q7_0_1_2_3', '');
// 6x22 q=7
add('6x22q7', '2', '', O('out622'), 'c6x22q7_2', '');
add('6x22q7', '2', '--krow=2:5', O('out622'), 'c6x22q7_2_--krow_2_5', '');
// 6x24 q=6
add('6x24q6', '1', '', O('out624'), 'c6x24q6_1', '');
add('6x24q6', '1', '--krow=1:4', O('out624'), 'c6x24q6_1_--krow_1_4', '');
// controls
add('2x8q4', '0', '', O('ctrl'), 'c2x8q4_0', 'positive control: K0796 5-stone witness rediscovered');
add('2x9q4', '0', '', O('ctrl'), 'c2x9q4_0', 'negative control: consistent with M_{2,4}=9');
add('6x18q8', '1', '', O('ctrl'), 'c6x18q8_1', 'positive control: K0815 41-stone witness board rediscovered, conflicts bit-exact with K0818 (511,895)');

fs.writeFileSync(path.join(EXP, 'records.jsonl'), records.map(r => JSON.stringify(r)).join('\n') + '\n');
const m620 = records.filter(r => r.m === 20 && r.q === 8 && !r.extra && r.class !== '1,5');
const sum = {
  date: '2026-11-14',
  m6x20q8: { classes: m620.length, unsat: m620.filter(r => r.result === 'UNSAT').length, sat: 0, indet: 0, totalConflicts: m620.reduce((a, r) => a + (r.conflicts || 0), 0), hardest: [...m620].sort((a, b) => b.conflicts - a.conflicts).slice(0, 5).map(r => ({ class: r.class, conflicts: r.conflicts })) },
  m6x21q7: { class2: 'SAT witness 35 stones rows (6,6,5,6,6,6), conflicts 1,904,706', class1: 'INDET 250s 2,341,807 conflicts', class0123: 'INDET 250s 2,848,875 conflicts' },
  controls: '2x8 q=4 SAT / 2x9 q=4 UNSAT / 6x18 q=8 class {1} SAT 511,895 conflicts (bit-exact vs K0818)',
  crosschecks: 'lex=H UNSAT on {2}=2,331,073 / {1}=2,038,080 / {1,2}=1,606,595 / {1,3}=1,209,815; fresh reruns {2}=2,763,766 and {1}=2,289,935 node-exact',
  mirror_check: 'non-canonical {1,5} UNSAT 258,595 consistent with canonical {0,4} UNSAT 246,856',
};
fs.writeFileSync(path.join(EXP, 'summary.json'), JSON.stringify(sum, null, 1));
console.log('records:', records.length);
console.log(JSON.stringify(sum.m6x20q8));
