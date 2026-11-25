// K0568 CNF regeneration control: streaming port of the repo's
// build_k6_cnf.cpp CNF writer (and of audit_port.js --cnf, its JS port).
//
// audit_port.js --cnf builds the whole CNF as one in-memory string, which
// does not fit the sandbox memory budget for the real d=6 family
// (~19.5M clauses).  This script emits the byte-identical stream: the same
// Sinz sequential-counter clauses first (verbatim at_most_k_clauses port),
// then one clause per circuit record of the family files in size order
// 4,5,6,7, each clause "-(v+1) ... 0" with the record's vertex ids.
//
// Equivalence control: on any family directory (including small synthetic
// ones) `audit_port.js --cnf` and this script produce identical files
// (cmp), which pins the byte-level format; the real-family run then only
// differs by the family content, which is itself audited (mine/port cmp).
//
// Usage:
//   node build_k6_cnf_stream.js --cnf K OUT.cnf [--fix0] --family DIR
'use strict';
const fs = require('fs');

const args = process.argv.slice(2);
const cnfIdx = args.indexOf('--cnf');
const K = parseInt(args[cnfIdx + 1], 10);
const cnfPath = args[cnfIdx + 2];
const fix0 = args.includes('--fix0');
const famDir = args[args.indexOf('--family') + 1];
if (K < 7 || K > 64) throw new Error('circuit CNF requires 7 <= K <= 64');

// ---------- verbatim port of at_most_k_clauses ----------
function atMostKClauses(lits, k, nextVar, out) {
  const n = lits.length;
  if (k === 0) { for (const lit of lits) out.push([-lit]); return nextVar; }
  if (k >= n) return nextVar;
  const s = [];
  for (let i = 0; i < n; i++) { s.push([]); for (let j = 0; j < k; j++) s[i].push(nextVar++); }
  out.push([-lits[0], s[0][0]]);
  for (let j = 1; j < k; j++) out.push([-s[0][j]]);
  for (let i = 1; i < n; i++) {
    out.push([-lits[i], s[i][0]]);
    out.push([-s[i - 1][0], s[i][0]]);
    for (let j = 1; j < k; j++) {
      out.push([-s[i - 1][j], s[i][j]]);
      out.push([-lits[i], -s[i - 1][j - 1], s[i][j]]);
    }
    out.push([-lits[i], -s[i - 1][k - 1]]);
  }
  return nextVar;
}

let nextVar = 65;
const counterClauses = [];
{
  const lits = []; for (let i = 0; i < 64; i++) lits.push(i + 1);
  nextVar = atMostKClauses(lits, K, nextVar, counterClauses);
}
{
  const lits = []; for (let i = 0; i < 64; i++) lits.push(-(i + 1));
  nextVar = atMostKClauses(lits, 64 - K, nextVar, counterClauses);
}

let circuits = 0;
for (const s of [4, 5, 6, 7]) {
  const st = fs.statSync(`${famDir}/circuits${s}.bin`);
  if (st.size % 8 !== 0) throw new Error(`circuits${s}.bin size not multiple of 8`);
  circuits += st.size / 8;
}
const total = counterClauses.length + circuits + (fix0 ? 1 : 0);

const fd = fs.openSync(cnfPath, 'w');
const OUTBUF = Buffer.alloc(1 << 20);
let opos = 0;
const flush = () => { if (opos > 0) { fs.writeSync(fd, OUTBUF, 0, opos); opos = 0; } };
const emit = (str) => {
  const b = Buffer.byteLength(str, 'ascii');
  if (opos + b > OUTBUF.length) flush();
  if (b > OUTBUF.length) { fs.writeSync(fd, Buffer.from(str, 'ascii')); return; }
  OUTBUF.write(str, opos, 'ascii'); opos += b;
};

emit(`p cnf ${nextVar - 1} ${total}\n`);
if (fix0) emit('1 0\n');
for (const c of counterClauses) { for (const l of c) emit(l + ' '); emit('0\n'); }
for (const s of [4, 5, 6, 7]) {
  const buf = fs.readFileSync(`${famDir}/circuits${s}.bin`);
  let chunk = '';
  for (let off = 0; off + 8 <= buf.length; off += 8) {
    for (let i = 0; i < s; i++) chunk += -(buf[off + i] + 1) + ' ';
    chunk += '0\n';
    if (chunk.length > (1 << 16)) { emit(chunk); chunk = ''; }
  }
  emit(chunk);
}
flush();
fs.closeSync(fd);
console.log(JSON.stringify({ cnf: cnfPath, vars: nextVar - 1, clauses: total, counter_clauses: counterClauses.length, circuits }));
