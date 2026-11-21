// u_recompute.js — independent reimplementation of the K0318 curve-packing
// stabilization upper bound U_{w,q} straight from the theorem statement
// (research/experiments/fixed-width/reports/curve-packing-fixed-width.md):
//   r = q-1, a = r-1, N = r(w-1)
//   Q  = C(N,3) - (w-1) C(r,3)
//   d0 = C(r,3), d1 = C(r-1,3)
//   Y  = a * floor(C(N,2)/C(r-1,2))                      (base form)
//   with the cross-row point-pair improvement:
//   e  = C(r-1,2) - floor((r-1)/2)
//   P  = C(N,2) - (w-1) C(r,2)
//   Y  = a * min(floor(C(N,2)/C(r-1,2)), floor(P/e))     (e > 0; q >= 5)
//   H  = max { 2x+y : x,y >= 0 integers, d0*x + d1*y <= Q, y <= Y }
//   U  = r + H
// This file shares no code with the K0318 verifier
// curve_packing_fixed_width.py; it is a from-statement reimplementation used
// to cross-check the published thresholds table before resting a closure on it.
'use strict';
const C = (n, k) => (k < 0 || k > n) ? 0 : (k === 0 ? 1 :
  Array.from({ length: k }, (_, i) => n - i).reduce((p, v) => p * v, 1) /
  Array.from({ length: k }, (_, i) => i + 1).reduce((p, v) => p * v, 1));

function packingU(w, q) {
  if (q < 4) throw new Error('theorem states q>=4');
  const r = q - 1, a = r - 1, N = r * (w - 1);
  const Q = C(N, 3) - (w - 1) * C(r, 3);
  const d0 = C(r, 3), d1 = C(r - 1, 3);
  const pairBudget = Math.floor(C(N, 2) / C(r - 1, 2));
  const e = C(r - 1, 2) - Math.floor((r - 1) / 2);
  let Y = a * pairBudget;
  let Yform = 'base';
  if (e > 0) {
    const P = C(N, 2) - (w - 1) * C(r, 2);
    Y = a * Math.min(pairBudget, Math.floor(P / e));
    Yform = 'crossrow';
  }
  // exact integer optimization: enumerate x, take max feasible y
  let best = null;
  const xmax = d0 > 0 ? Math.floor(Q / d0) : 0;
  for (let x = 0; x <= xmax; x++) {
    const rem = Q - d0 * x;
    // y bounded by Y and, if d1>0, floor(rem/d1); if d1==0, y only by Y
    const ymax = Math.min(Y, d1 > 0 ? Math.floor(rem / d1) : Y);
    const y = ymax;                      // objective grows in y; y=ymax optimal per x
    const obj = 2 * x + y;
    if (best === null || obj > best.obj) best = { x, y, obj };
  }
  const H = best.obj;
  return { w, q, r, a, N, Q, d0, d1, e, Y, Yform, H, x: best.x, y: best.y, U: r + H };
}

if (require.main === module) {
  const fs = require('fs');
  const ref = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); // K0318 json
  const out = [];
  let mismatch = 0, total = 0;
  for (const t of ref.thresholds) {
    const mine = packingU(t.w, t.q);
    total++;
    // The (x,y) argmax need not match: the LP has flat directions (several
    // (x,y) attain H). What must match is every bound-relevant quantity:
    // U, Q, Y, d0, d1 and the objective value H = 2x+y.
    const pubH = 2 * t.integer_optimizer[0] + t.integer_optimizer[1];
    const ok = mine.U === t.packing_U && mine.Q === t.Q && mine.Y === t.Y &&
      mine.d0 === t.d0 && mine.d1 === t.d1 && mine.H === pubH;
    if (!ok) mismatch++;
    out.push({ w: t.w, q: t.q, published_U: t.packing_U, published_Q: t.Q,
      published_Y: t.Y, published_opt: t.integer_optimizer,
      recomputed_U: mine.U, recomputed_Q: mine.Q, recomputed_Y: mine.Y,
      recomputed_Yform: mine.Yform, recomputed_e: mine.e,
      recomputed_opt: [mine.x, mine.y], recomputed_H: mine.H, published_H: pubH,
      match: ok });
  }
  const k47 = packingU(4, 7), k46 = packingU(4, 6);
  const summary = {
    schema: 1,
    entries_checked: total, mismatches: mismatch, all_match: mismatch === 0,
    key_values: { U_4_7: k47.U, Q_4_7: k47.Q, Y_4_7: k47.Y, Yform_4_7: k47.Yform,
      opt_4_7: [k47.x, k47.y], H_4_7: k47.H, U_4_6: k46.U, Q_4_6: k46.Q, Y_4_6: k46.Y,
      opt_4_6: [k46.x, k46.y], H_4_6: k46.H },
    entries: out
  };
  fs.writeFileSync(process.argv[3], JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify({ entries_checked: total, mismatches: mismatch,
    U_4_7: k47.U, U_4_6: k46.U, U_4_5: packingU(4, 5).U, U_4_8: packingU(4, 8).U,
    U_3_5: packingU(3, 5).U, U_3_6: packingU(3, 6).U, U_5_7: packingU(5, 7).U }));
  process.exit(mismatch === 0 ? 0 : 1);
}
module.exports = { packingU };
