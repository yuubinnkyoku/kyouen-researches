// stripsearch_w8.ts — K0830 (7-row) chord-bounded complete-enumeration machine, w=8 port.
// Reference reconstruction (2026-11-15, post-compaction): constants, chunk map,
// case structure and the config verifier are as executed; the executed machine's
// inner anchor-pair loop is not reproduced line-for-line. Recorded aggregates
// (SPF sieve count, per-chunk pairsTested, A-prime tests, found configs) live in
// ../output/stripsearch-w8-umax2100.json and take precedence over this file.
//
// Search target: circles (2x-u)^2 + (2y-2b)^2 = R (u odd) with >= 10 strip points
// (8-row window: rows 0..7, x unbounded; per-row lattice points come in pairs, so
// the strip count is even, and >= 10 is the right threshold for Theorem A: any
// circle with >= 9 in-board points has >= 9, hence >= 10, strip points), with
// doubled chord c_y = 2*t_y <= UMAX on every occupied row.
//
// Why a finite chord bound suffices (lemma L2): for m <= 984, the far case gives
//   c*^2 <= 4.5*(m-1)^2 + 308   =>   c* <= 2085 < 2100;
// the near case gives c*^2 <= (m-1)^2 + 392.

const W = 8;
const UMAX = 2100;          // doubled-chord bound (L2)
const ZLO = -1102502;       // half-range, negative side (axis-centered center parameter)
const ZHI = -2;             // mirror v0 -> 14 - v0 closes the other half
const APRIME_TESTS = 2100;  // symmetric-pair tests at the axis (Case A-prime, chunk 4)

// 4-chunk execution map (pairsTested as recorded):
//   chunk 1:  97,231      chunk 2: 194,959      chunk 3: 294,561
//   chunk 4: 514,699 (+ A-prime 2,100)  ->  all 13 qualifying configs found here
//   totals: Case A 1,101,450 pairs; SPF sieve 1,102,503.
//
// Enumerated result (13 configs):
//   - 9 configs identical to census families F1-F9 (profiles in the JSON),
//   - the K0830 exception circle R = 2353705250 at v0 in {48515, 48517} plus
//     mirrors {-48501, -48503}; 5 double rows, chords {5, 623, 763, 985, 1079};
//     needs m >= 986 for 9 / m >= 1080 for 10 in-board points (K0830-consistent).

// Exact-integer config verifier (re-runnable; used on 2026-11-15 to re-verify
// all 9 family profiles): for each row y, the doubled chord
//   c_y = sqrt(R - (2y - v0)^2)
// must be an odd integer.
function isqrtExact(n: number): number {
  if (n < 0) return -1;
  const r = Math.round(Math.sqrt(n));
  return r * r === n ? r : -1;
}
export function verifyConfig(R: number, v0: number, rows: number[]): { ok: boolean; profile: string } {
  const parts: string[] = [];
  for (const y of rows) {
    const c = isqrtExact(R - (2 * y - v0) * (2 * y - v0));
    if (c < 0 || c % 2 === 0) return { ok: false, profile: parts.join(",") };
    parts.push(y + ":" + c);
  }
  return { ok: true, profile: parts.join(",") };
}

// The 9 census family geometries (verified through verifyConfig):
export const FAMILIES = [
  { name: "F1", R: 50, v0: 7, rows: [0, 1, 3, 4, 6, 7] },
  { name: "F2", R: 50, v0: 5, rows: [0, 2, 3, 5, 6] },
  { name: "F3", R: 50, v0: 9, rows: [1, 2, 4, 5, 7] },
  { name: "F4", R: 130, v0: 11, rows: [0, 1, 2, 4, 7] },
  { name: "F5", R: 130, v0: 3, rows: [0, 3, 5, 6, 7] },
  { name: "F6", R: 170, v0: 1, rows: [0, 1, 4, 6, 7] },
  { name: "F7", R: 170, v0: 13, rows: [0, 1, 3, 6, 7] },
  { name: "F8", R: 650, v0: 25, rows: [0, 1, 3, 4, 7] },
  { name: "F9", R: 650, v0: -11, rows: [0, 3, 4, 6, 7] }
];