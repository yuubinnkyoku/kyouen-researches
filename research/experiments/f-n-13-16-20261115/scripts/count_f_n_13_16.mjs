#!/usr/bin/env node
// count_f_n_13_16.mjs - F_n extension verifier for n=13..16 (2026-11-15).
// Answers batch-08 next-step #1. Verifies recorded values:
//   F_13=252362 D_13=27340 C_13=225022; F_14=383603 D_14=41506 C_14=342097;
//   F_15=565948 D_15=61176 C_15=504772; F_16=816276 D_16=87756 C_16=728520.
// Systems: A = difference-row linear-form scan (classification);
//          B = independent cofactor-expansion determinant scan (total only);
//          lines = constructive direction walk and M(t) closed form (must agree,
//                  and must equal A.collinear and the round4 closed-form D_n).
// Calibration: n=12 must reproduce published F=158426, D=17154.
// Usage: node count_f_n_13_16.mjs [--fast]   (--fast skips system B)
// Deterministic; prints ALL CHECKS PASSED on success.
// Full run scans ~3.7e8 quads per system; expect tens of minutes.
// --fast runs in well under a minute.

function gcd2(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while(b){
      const t = a % b;
      a = b;
      b = t;
    }
    return a || 1;
  }

function C4(s) {
    return s < 4 ? 0 : s * (s - 1) * (s - 2) * (s - 3) / 24;
  }

function systemA(n) {
    const N = n * n;
    const px = new Int16Array(N), py = new Int16Array(N), pw = new Int32Array(N);
    for(let p = 0; p < N; p++){
      const x = p % n, y = p / n | 0;
      px[p] = x;
      py[p] = y;
      pw[p] = x * x + y * y;
    }
    let F = 0, lin = 0;
    for(let a = 0; a < N - 3; a++){
      const wa = pw[a], xa = px[a], ya = py[a];
      for(let b = a + 1; b < N - 2; b++){
        const bw = pw[b] - wa, bx = px[b] - xa, by = py[b] - ya;
        for(let c = b + 1; c < N - 1; c++){
          const cw = pw[c] - wa, cx = px[c] - xa, cy = py[c] - ya;
          const c1 = bx * cy - by * cx, c2 = by * cw - bw * cy, c3 = bw * cx - bx * cw;
          if (c1 === 0) {
            for(let d = c + 1; d < N; d++){
              if (c2 * (px[d] - xa) + c3 * (py[d] - ya) === 0) {
                F++;
                lin++;
              }
            }
          } else {
            for(let d = c + 1; d < N; d++){
              if (c1 * (pw[d] - wa) + c2 * (px[d] - xa) + c3 * (py[d] - ya) === 0) {
                F++;
              }
            }
          }
        }
      }
    }
    return {
      n,
      N,
      F,
      collinear: lin,
      cocircular: F - lin
    };
  }

function systemB(n) {
    const N = n * n;
    const px = new Int16Array(N), py = new Int16Array(N), pw = new Int32Array(N);
    for(let p = 0; p < N; p++){
      const x = p % n, y = p / n | 0;
      px[p] = x;
      py[p] = y;
      pw[p] = x * x + y * y;
    }
    let F = 0;
    for(let p1 = 0; p1 < N - 3; p1++)for(let p2 = p1 + 1; p2 < N - 2; p2++)for(let p3 = p2 + 1; p3 < N - 1; p3++)for(let p4 = p3 + 1; p4 < N; p4++){
      const r1x = px[p2] - px[p1], r1y = py[p2] - py[p1], r1w = pw[p2] - pw[p1];
      const r2x = px[p3] - px[p1], r2y = py[p3] - py[p1], r2w = pw[p3] - pw[p1];
      const r3x = px[p4] - px[p1], r3y = py[p4] - py[p1], r3w = pw[p4] - pw[p1];
      const det = r1x * (r2y * r3w - r2w * r3y) - r1y * (r2x * r3w - r2w * r3x) + r1w * (r2x * r3y - r2y * r3x);
      if (det === 0) F++;
    }
    return {
      n,
      F
    };
  }

function directionWalk(n) {
    const dirs = [];
    const cap = Math.floor((n - 1) / 3);
    for(let a = 1; a <= cap; a++)for(let b = -cap; b <= cap; b++)if (gcd2(a, Math.abs(b)) === 1) dirs.push([
      a,
      b
    ]);
    dirs.push([
      0,
      1
    ]);
    const perDir = {};
    let quads = 0, linesTotal = 0;
    const sizeHist = {};
    for (const [a, b] of dirs){
      const key = a + "," + b;
      const hist = {};
      for(let x = 0; x < n; x++)for(let y = 0; y < n; y++){
        const px0 = x - a, py0 = y - b;
        if (px0 >= 0 && px0 < n && py0 >= 0 && py0 < n) continue;
        let t = 0, cx = x, cy = y;
        while(cx >= 0 && cx < n && cy >= 0 && cy < n){
          t++;
          cx += a;
          cy += b;
        }
        if (t >= 4) {
          hist[t] = (hist[t] || 0) + 1;
          quads += C4(t);
          linesTotal++;
          sizeHist[t] = (sizeHist[t] || 0) + 1;
        }
      }
      if (Object.keys(hist).length) perDir[key] = hist;
    }
    return {
      n,
      perDir,
      linesTotal,
      quads,
      sizeHist
    };
  }

function closedFormLines(n) {
    const cl = (u)=>u > 0 ? u : 0;
    const perDir = {};
    let quads = 0, linesTotal = 0;
    const sizeHist = {};
    const cap = Math.floor((n - 1) / 3);
    for(let a = 1; a <= cap; a++)for(let bb = 0; bb <= cap; bb++){
      if (gcd2(a, bb) !== 1) continue;
      const signs = bb === 0 ? [
        0
      ] : [
        bb,
        -bb
      ];
      for (const b of signs){
        const key = a + "," + b;
        const maxT = Math.floor((n - 1) / Math.max(a, bb)) + 1;
        const M = (t)=>cl(n - (t - 1) * a) * cl(n - (t - 1) * bb) - cl(n - t * a) * cl(n - t * bb);
        const hist = {};
        for(let t = 4; t <= maxT; t++){
          const ex = M(t) - M(t + 1);
          if (ex > 0) hist[t] = ex;
        }
        if (Object.keys(hist).length) {
          perDir[key] = hist;
          for(const t in hist){
            const tt = +t;
            quads += hist[t] * C4(tt);
            linesTotal += hist[t];
            sizeHist[tt] = (sizeHist[tt] || 0) + hist[t];
          }
        }
      }
    }
    if (n >= 4) {
      perDir["0,1"] = {};
      perDir["0,1"][n] = n;
      quads += n * C4(n);
      linesTotal += n;
      sizeHist[n] = (sizeHist[n] || 0) + n;
    }
    return {
      n,
      perDir,
      linesTotal,
      quads,
      sizeHist
    };
  }

function canon(o) {
    const keys = Object.keys(o).sort();
    const r = {};
    for (const k of keys)r[k] = o[k];
    return JSON.stringify(r);
  }

const RECORDS = { 12: { F: 158426, D: 17154 }, 13: { F: 252362, D: 27340 }, 14: { F: 383603, D: 41506 }, 15: { F: 565948, D: 61176 }, 16: { F: 816276, D: 87756 } };
const ok = (cond, msg) => { if (!cond) throw new Error('CHECK FAIL: ' + msg); };
const fast = process.argv.includes('--fast');
for (const n of [12, 13, 14, 15, 16]) {
  const A = systemA(n);
  ok(A.F === RECORDS[n].F && A.collinear === RECORDS[n].D, 'system A totals n=' + n);
  const w = directionWalk(n), f = closedFormLines(n);
  ok(canon(w.perDir) === canon(f.perDir) && w.quads === f.quads && w.linesTotal === f.linesTotal, 'line systems agree n=' + n);
  ok(f.quads === A.collinear, 'closed form D == A.collinear n=' + n);
  console.log('n=' + n + ': F=' + A.F + ' D=' + A.collinear + ' C=' + A.cocircular + ' lines=' + f.linesTotal + ' [A + line systems OK]');
}
if (!fast) {
  for (const n of [13, 14, 15, 16]) {
    const B = systemB(n);
    ok(B.F === RECORDS[n].F, 'system B total n=' + n);
    console.log('n=' + n + ': system B total=' + B.F + ' [OK]');
  }
}
console.log('ALL CHECKS PASSED');
