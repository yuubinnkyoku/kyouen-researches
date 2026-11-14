#!/usr/bin/env node
// K0823 — side-window sigma(n) = min{w: P(w) >= n}, universal for n <= 34.
//
// Deterministic, no I/O. Embedded inputs:
//   - proved-exact P table w=0..83 (results/fixed-width/pw_circle_point_max.csv
//     w=2..83 as of 2026-11-14, plus P(1)=2, P(0)=0 per K0817)
//   - K0791 published 11050-circle census w=84..106 (expected values)
//
// Checks:
//   1. sigma table = P-table inverse (definition identity).
//   2. witness circle window counts by independent oo-form enumeration
//      (odd reps of 2R', rows (b-1)/2, two-pointer sliding window)
//      vs the CSV witness assignment, and vs K0791's census for w=84..106.
//
// Run: node sigma_p_inverse.js   (prints the JSON also committed as
//      ../output/sigma_table.json; exits 1 on any mismatch)
"use strict";

const isqrt = (n) => { let t = Math.floor(Math.sqrt(n)); while (t * t > n) t--; while ((t + 1) * (t + 1) <= n) t++; return t; };

// proved-exact P table (CSV w=2..83 + K0817 P(0)=0, P(1)=2)
const P = {1: 2, 2: 4, 3: 6, 4: 8, 5: 8, 6: 8, 7: 10, 8: 12, 9: 12, 10: 12, 11: 14, 12: 16,
  13: 16, 14: 16, 15: 16, 16: 16, 17: 16, 18: 16, 19: 16, 20: 16, 21: 16, 22: 18, 23: 20, 24: 20,
  25: 22, 26: 24, 27: 24, 28: 24, 29: 24, 30: 24, 31: 24, 32: 24, 33: 24, 34: 24, 35: 24, 36: 24,
  37: 24, 38: 24, 39: 24, 40: 24, 41: 24, 42: 24, 43: 26, 44: 28, 45: 28, 46: 30, 47: 30, 48: 32};
for (let w = 49; w <= 82; w++) P[w] = 32;
P[83] = 34;
P[0] = 0;

// K0791 published 11050-circle lower-bound census, w=84..106
const K0791 = {84: 34, 85: 34, 86: 34, 87: 36, 88: 36, 89: 36, 90: 36, 91: 36, 92: 36, 93: 36,
  94: 38, 95: 38, 96: 40, 97: 40, 98: 40, 99: 40, 100: 42, 101: 44, 102: 44, 103: 44, 104: 44,
  105: 46, 106: 48};

// oo-form circle (2x-A)^2+(2y-B)^2 = 2Rp (A,B odd): points = odd reps (a,b) of 2Rp,
// rows y = (b+B)/2 -> relative integer rows (b-1)/2, 2 points per row-sign (from +/-a).
function ooCircleRows(Rp) {
  const N = 2 * Rp;
  const rows = new Map();
  const r = isqrt(N);
  for (let a = 1; a <= r; a += 2) {
    const b2 = N - a * a;
    if (b2 <= 0) continue;
    const b = isqrt(b2);
    if (b * b !== b2 || b % 2 !== 1) continue;
    const r1 = (b - 1) / 2, r2 = (-b - 1) / 2;
    rows.set(r1, (rows.get(r1) || 0) + 2);
    rows.set(r2, (rows.get(r2) || 0) + 2);
  }
  return rows;
}

function windowMax(rows, w) {
  const sorted = [...rows.entries()].sort((x, y) => x[0] - y[0]);
  let lo = 0, sum = 0, bs = 0;
  for (let hi = 0; hi < sorted.length; hi++) {
    sum += sorted[hi][1];
    while (sorted[hi][0] - sorted[lo][0] > w - 1) { sum -= sorted[lo][1]; lo++; }
    if (sum > bs) bs = sum;
  }
  return bs;
}

// sigma(n) = min{w: P(w) >= n} (definition identity; P monotone)
const sigma = {};
for (let n = 2; n <= 34; n++) {
  for (let w = 1; w <= 83; w++) { if (P[w] >= n) { sigma[n] = w; break; } }
}
const sigmaK = {};
for (let k = 2; k <= 17; k++) sigmaK[k] = sigma[2 * k];

// witness census per CSV witness assignment
const witnesses = [
  { name: "oo_R10", Rp: 5, csvWs: [2, 3, 4, 5] },
  { name: "oo_R50", Rp: 25, csvWs: [6, 7, 8, 9, 10] },
  { name: "oo_R130", Rp: 65, csvWs: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] },
  { name: "oo_R650", Rp: 325, csvWs: [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42] },
  { name: "oo_R2210", Rp: 1105, csvWs: [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82] },
  { name: "oo_R11050", Rp: 5525, csvWs: [83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106] },
];
const census = {};
let allMatch = true;
for (const wit of witnesses) {
  const rows = ooCircleRows(wit.Rp);
  const total = [...rows.values()].reduce((a, b) => a + b, 0);
  const counts = {}, expected = {};
  let match = true;
  for (const w of wit.csvWs) {
    counts[w] = windowMax(rows, w);
    expected[w] = w <= 83 ? P[w] : K0791[w];
    if (counts[w] !== expected[w]) match = false;
  }
  if (!match) allMatch = false;
  census[wit.name] = { total_points: total, counts, expected, match };
}

// subadditive upper bounds U(w) = min_a P(a)+P(w-a), w=84..90 (K0817)
const U = {};
for (let w = 84; w <= 90; w++) {
  let u = Infinity, arg = null;
  for (let a = 0; a <= w; a++) {
    if (P[a] !== undefined && P[w - a] !== undefined && P[a] + P[w - a] < u) {
      u = P[a] + P[w - a]; arg = [a, w - a];
    }
  }
  U[w] = { upper: u, split: arg };
}

const result = {
  experiment: "sigma-side-window-p-inverse-20261114",
  date: "2026-11-14",
  identity: "sigma(n) = min{w >= 1 : P(w) >= n}  (side window, any position, all circle families)",
  p_source: "results/fixed-width/pw_circle_point_max.csv (w=2..83, all proved-exact) + P(1)=2, P(0)=0 (K0817)",
  sigma: sigma,
  sigma_double_row_k: sigmaK,
  center_window_note: "for n=26..34 the sigma-achieving witness windows contain the circle row-center (52.5 in [34,76] and [0,82]; 12.5 in [0,25]), and match K0785 E-family center-window bestK(13..17)=43,44,46,48,83; hence center-window sigma equals side sigma for n=26..34 (all families). No claim for n<26.",
  closures: [
    "K0791 resume item 2 (sigma_17 direct determination): closed, sigma_17 = 83 universal (K0804 P(82)=32 lower + K0791 witness upper); no sweep extension needed",
    "K0785 old note (side-window sigma_13 open, stale range [36,43]): closed, sigma_13 = 43 universal (K0788 P(42)=24 < 26 + 2210-circle rows 34..76)"
  ],
  open_frontier: {
    sigma_35_36: [84, 87],
    equivalence: "determining sigma(36) is equivalent to determining P(84),P(85),P(86) (level-18 sweep); all-34 implies sigma(36)=87",
    upper_bounds_U_84_90: U
  },
  witness_census: census,
  all_census_match: allMatch,
};
console.log(JSON.stringify(result, null, 2));
if (!allMatch) process.exit(1);
