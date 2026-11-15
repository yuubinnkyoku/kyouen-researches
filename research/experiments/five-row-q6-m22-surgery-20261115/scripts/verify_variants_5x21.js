#!/usr/bin/env node
// Independent verification of the three CTRL-1 witnesses on 5x21 (q=6)
// using the all-triples census system of c4_census_check.js (method-disjoint
// from surgery.js: different curve construction, direct safe/maximal checks).
//   safe    : no census curve (>=6 in-board points) holds 6 stones
//   maximal : every empty cell lies on a census curve with exactly 5 stones
// Also checks deficiency (<= 24 stones implies a row with <= 4 stones) and
// prints the row counts. Usage: node verify_variants_5x21.js

"use strict";
const W = 5, M = 21, Q = 6, N = W * M;
const px = (i) => i % M, py = (i) => Math.floor(i / M);
function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }

function allTriplesCensus() {
  const curves = new Map();
  const collinear = (x1,y1,x2,y2,x3,y3) => (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1) === 0;
  for (let a = 0; a < N; a++) for (let b = a+1; b < N; b++) for (let c = b+1; c < N; c++) {
    const x1=px(a),y1=py(a),x2=px(b),y2=py(b),x3=px(c),y3=py(c);
    if (collinear(x1,y1,x2,y2,x3,y3)) {
      let A = y2-y1, B = x1-x2, C = A*x1 + B*y1;
      const g = gcdN(gcdN(Math.abs(A),Math.abs(B)),Math.abs(C)); A/=g; B/=g; C/=g;
      if (A < 0 || (A === 0 && B < 0)) { A=-A; B=-B; C=-C; }
      const key = 'L:'+A+','+B+','+C;
      if (!curves.has(key)) curves.set(key, { kind:'line', coef:[A,B,C] });
    } else {
      const A1 = 2*(x2-x1), B1 = 2*(y2-y1), C1 = x2*x2+y2*y2-x1*x1-y1*y1;
      const A2 = 2*(x3-x1), B2 = 2*(y3-y1), C2 = x3*x3+y3*y3-x1*x1-y1*y1;
      const det = A1*B2 - A2*B1;
      if (det === 0) continue;
      const n1 = C1*B2 - C2*B1, n2 = A1*C2 - A2*C1;
      const K = (det*x1 - n1)*(det*x1 - n1) + (det*y1 - n2)*(det*y1 - n2);
      let A = det*det, B = -2*n1*det, C = -2*n2*det, D = n1*n1 + n2*n2 - K;
      const g = gcdN(gcdN(gcdN(Math.abs(A),Math.abs(B)),Math.abs(C)),Math.abs(D));
      A/=g; B/=g; C/=g; D/=g;
      if (A < 0) { A=-A; B=-B; C=-C; D=-D; }
      const key = 'C:'+A+','+B+','+C+','+D;
      if (!curves.has(key)) curves.set(key, { kind:'circle', coef:[A,B,C,D] });
    }
  }
  const keep = [];
  for (const { kind, coef } of curves.values()) {
    const pts = [];
    for (let i = 0; i < N; i++) {
      const x = px(i), y = py(i);
      const on = kind === 'line' ? coef[0]*x + coef[1]*y === coef[2]
        : coef[0]*(x*x+y*y) + coef[1]*x + coef[2]*y + coef[3] === 0;
      if (on) pts.push(i);
    }
    if (pts.length >= Q) keep.push(pts);
  }
  return keep;
}

const census = allTriplesCensus();
const witnesses = [
  ['original (K0815, restored (5,1))', [[1,0],[3,0],[5,0],[7,0],[0,1],[5,1],[7,1],[10,1],[14,1],[3,2],[6,2],[8,2],[10,2],[17,2],[6,3],[7,3],[8,3],[9,3],[14,3],[4,4],[7,4],[9,4],[11,4],[13,4]]],
  ['variant A (swap (10,2)->(11,2))',  [[1,0],[3,0],[5,0],[7,0],[0,1],[5,1],[7,1],[10,1],[14,1],[3,2],[6,2],[8,2],[11,2],[17,2],[6,3],[7,3],[8,3],[9,3],[14,3],[4,4],[7,4],[9,4],[11,4],[13,4]]],
  ['variant B (swap (10,2)->(12,2))',  [[1,0],[3,0],[5,0],[7,0],[0,1],[5,1],[7,1],[10,1],[14,1],[3,2],[6,2],[8,2],[12,2],[17,2],[6,3],[7,3],[8,3],[9,3],[14,3],[4,4],[7,4],[9,4],[11,4],[13,4]]],
];
const out = { board: '5x21', q: 6, censusCurves: census.length, system: 'independent all-triples (method-disjoint from surgery.js)', witnesses: [] };
for (const [name, stones] of witnesses) {
  const occ = new Uint8Array(N);
  for (const [x, y] of stones) occ[y * M + x] = 1;
  let safe = true, maxCurve = 0;
  for (const cv of census) {
    let cnt = 0; for (const p of cv) cnt += occ[p];
    if (cnt > maxCurve) maxCurve = cnt;
    if (cnt >= Q) { safe = false; break; }
  }
  let maximal = true, unblocked = null;
  outer: for (let p = 0; p < N; p++) {
    if (occ[p]) continue;
    for (const cv of census) {
      let on = false, cnt = 0;
      for (const q2 of cv) { if (q2 === p) on = true; cnt += occ[q2]; }
      if (on && cnt === Q - 1) continue outer;
    }
    maximal = false; unblocked = [px(p), py(p)]; break;
  }
  const rowCount = [0,0,0,0,0];
  for (const [, y] of stones) rowCount[y]++;
  out.witnesses.push({ name, stones: stones.length, rows: rowCount, safe, maxCurveStones: safe ? maxCurve : null, maximal, unblocked, verdict: safe && maximal ? 'PASS deficient-maximal witness' : 'FAIL' });
}
console.log(JSON.stringify(out, null, 1));
if (!out.witnesses.every(w => w.verdict.startsWith('PASS'))) process.exit(1);
