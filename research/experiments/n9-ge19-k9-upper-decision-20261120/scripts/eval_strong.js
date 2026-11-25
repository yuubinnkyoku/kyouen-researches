#!/usr/bin/env node
// eval_strong.js — independent semantic evaluator for the strong CNFs.
// Loads n{N}_ge{K}_strong.cnf + .map.json + a witness cell list, computes every
// aux variable's value from its DEFINITION (not from the generator's clauses):
//   cell var v = p+1 for cell p in 0..NCELL-1
//   fwd[i][j] := (#chosen among cells 1..i) >= j
//   rev[u][j] := (#chosen among the last u cells, i.e. cells NCELL-u+1..NCELL) >= j
//   curve s[cb][i][j] := (#chosen among first i points of that curve, ascending) >= j
// then evaluates ALL clauses of the CNF under this total assignment and reports
// violations. Also independently re-checks witness safety (no 4 co-circular or
// collinear points) via the standard 4x4 determinant over ALL quads, and checks
// the at-least-K unit.
// Usage: node eval_strong.js --cnf=output2/n9_ge18_strong.cnf --cells=5,6,8,...
'use strict';
const fs = require('fs');

const args = {};
for (const a of process.argv.slice(2)) {
  const m = a.match(/^--(cnf|cells|label)=(.*)$/);
  if (m) args[m[1]] = m[2];
}
if (!args.cnf || !args.cells) { console.error('usage: --cnf=... --cells=a,b,... [--label=NAME]'); process.exit(2); }
const label = args.label || args.cnf;
const cells = args.cells.split(',').map(Number).sort((a, b) => a - b);
const cellSet = new Set(cells);
for (const c of cells) if (!Number.isInteger(c) || c < 0 || c > 80) { console.error('bad cell ' + c); process.exit(2); }

// ---- load CNF ----
const raw = fs.readFileSync(args.cnf, 'utf8');
const mapFn = args.cnf.replace(/\.cnf$/, '.map.json');
const M = JSON.parse(fs.readFileSync(mapFn, 'utf8'));
const NCELL = M.NCELL, K = M.K, n = M.n;
if (NCELL !== n * n) { console.error('unexpected NCELL'); process.exit(2); }

// total assignment: var -> 0/1
const val = new Uint8Array(M.nv + 1);
for (let p = 0; p < NCELL; p++) val[p + 1] = cellSet.has(p) ? 1 : 0;

// fwd: a[i][j], i in 1..NCELL, j in 1..min(i,K); prefix counts over cells 1..i
{
  let cnt = 0;
  for (let i = 1; i <= NCELL; i++) {
    cnt += val[i];
    for (let j = 1; j <= Math.min(i, K); j++) {
      const id = M.fwd[i + ',' + j];
      val[id] = cnt >= j ? 1 : 0;
    }
  }
  if (cnt !== cells.length) { console.error('cell count mismatch'); process.exit(2); }
}
// rev: r[u][j], u in 1..NCELL; suffix counts over last u cells
for (let u = 1; u <= NCELL; u++) {
  let cnt = 0;
  for (let p = NCELL - u + 1; p <= NCELL; p++) cnt += val[p];
  for (let j = 1; j <= Math.min(u, K); j++) {
    const id = M.rev[u + ',' + j];
    val[id] = cnt >= j ? 1 : 0;
  }
}
// curves: s[cb][i][j], j in 1..3
for (const cb of M.curves) {
  const pts = cb.points; // ascending cell indices
  let cnt = 0;
  for (let i = 1; i <= pts.length; i++) {
    cnt += cellSet.has(pts[i - 1]) ? 1 : 0;
    for (let j = 1; j <= 3; j++) {
      const id = cb.sIds[i + ',' + j];
      val[id] = cnt >= j ? 1 : 0;
    }
  }
}

// ---- evaluate all clauses ----
let nClauses = 0, sat = 0, viol = [];
const lines = raw.split('\n');
let cur = [];
for (const line of lines) {
  if (line[0] === 'c' || line[0] === 'p') continue;
  for (const tok of line.split(' ')) {
    if (tok === '' || tok === '0') {
      if (tok === '0' && cur.length) {
        nClauses++;
        let ok = false;
        for (const lit of cur) { const v = lit > 0 ? val[lit] : 1 - val[-lit]; if (v) { ok = true; break; } }
        if (ok) sat++; else if (viol.length < 5) viol.push(cur.slice());
        cur = [];
      }
    } else cur.push(parseInt(tok, 10));
  }
}
// 独立の安全性再検査: 全4点組の det4 (integer exact) — forbidden なら witness が不正
const cr = (p) => [p % n, Math.floor(p / n)];
let unsafe = 0;
for (let a = 0; a < NCELL; a++) if (cellSet.has(a))
  for (let b = a + 1; b < NCELL; b++) if (cellSet.has(b))
    for (let c = b + 1; c < NCELL; c++) if (cellSet.has(c))
      for (let d = c + 1; d < NCELL; d++) if (cellSet.has(d)) {
        const [x1, y1] = cr(a), [x2, y2] = cr(b), [x3, y3] = cr(c), [x4, y4] = cr(d);
        // det [[x^2+y^2, x, y, 1], ...]
        const row = (x, y) => [x * x + y * y, x, y, 1];
        const r1 = row(x1, y1), r2 = row(x2, y2), r3 = row(x3, y3), r4 = row(x4, y4);
        // exact 4x4 integer determinant, expansion along the first row
        const det3 = (u) =>
          BigInt(u[0][0]) * (BigInt(u[1][1]) * BigInt(u[2][2]) - BigInt(u[1][2]) * BigInt(u[2][1]))
          - BigInt(u[0][1]) * (BigInt(u[1][0]) * BigInt(u[2][2]) - BigInt(u[1][2]) * BigInt(u[2][0]))
          + BigInt(u[0][2]) * (BigInt(u[1][0]) * BigInt(u[2][1]) - BigInt(u[1][1]) * BigInt(u[2][0]));
        const m = [r1, r2, r3, r4];
        const det =
          BigInt(m[0][0]) * det3([[m[1][1], m[1][2], m[1][3]], [m[2][1], m[2][2], m[2][3]], [m[3][1], m[3][2], m[3][3]]])
          - BigInt(m[0][1]) * det3([[m[1][0], m[1][2], m[1][3]], [m[2][0], m[2][2], m[2][3]], [m[3][0], m[3][2], m[3][3]]])
          + BigInt(m[0][2]) * det3([[m[1][0], m[1][1], m[1][3]], [m[2][0], m[2][1], m[2][3]], [m[3][0], m[3][1], m[3][3]]])
          - BigInt(m[0][3]) * det3([[m[1][0], m[1][1], m[1][2]], [m[2][0], m[2][1], m[2][2]], [m[3][0], m[3][1], m[3][2]]]);
        if (det === 0n) unsafe++;
      }
const result = {
  label, n, K, k_stones: cells.length,
  clauses_seen: nClauses, clauses_map: M.nClauses,
  clauses_sat: sat, clauses_violated: nClauses - sat,
  example_violations: viol,
  independent_safety_check_forbidden_quads: unsafe,
  verdict: (nClauses === M.nClauses && nClauses - sat === 0 && unsafe === 0) ? 'WITNESS-SAT' : 'VIOLATION',
};
console.log(JSON.stringify(result));
process.exit(result.verdict === 'WITNESS-SAT' ? 0 : 1);
