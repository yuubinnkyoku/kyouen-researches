// lp_analysis.ts — K0318 triple-budget LP for w=7, q=5..8 with the K0332-style
// Melchior-inversion y-cap and a K0342 chord-energy event audit. Pure TypeScript,
// exact integer arithmetic (all intermediates < 2^53). Reproduces output/analysis.json.
// Run: npx tsx lp_analysis.ts (or any TS runner). No dependencies, no network.

function binom(n: number, k: number): number {
  if (n < 0 || k < 0 || k > n) return 0;
  let r = 1;
  for (let i = 0; i < k; i++) r = (r * (n - i)) / (i + 1);
  return Math.round(r);
}

// K0342 sharp chord energy: E_r = (2r^3-3r^2+4r-3*[r odd])/12, equality on APs.
const E = (r: number) => (2 * r ** 3 - 3 * r * r + 4 * r - (r % 2 ? 3 : 0)) / 12;

// exhaustive integer optimum of H = max{2x+y : d0x+d1y <= Q, 0<=y<=Y}
function H(d0: number, d1: number, Q: number, Y: number) {
  let best = -1, ax = -1, ay = -1;
  for (let y = 0; y <= Y; y++) {
    const rem = Q - d1 * y;
    if (rem < 0) break;
    const x = Math.floor(rem / d0);
    if (x < 0) continue;
    const v = 2 * x + y;
    if (v > best) { best = v; ax = x; ay = y; }
  }
  return { H: best, x: ax, y: ay };
}

function family(w: number, q: number) {
  const t = w - 1, r = q - 1, a = r - 1, N = r * t;
  const Q = binom(N, 3) - t * binom(r, 3);
  const d0 = binom(r, 3), d1 = binom(r - 1, 3);
  const pairFloor = Math.floor(binom(N, 2) / binom(r - 1, 2));
  const e = binom(r - 1, 2) - Math.floor((r - 1) / 2);
  const P = binom(N, 2) - t * binom(r, 2);
  const Yk = e > 0 ? a * Math.min(pairFloor, Math.floor(P / e)) : a * pairFloor;
  // Melchior inversion per-stone cap (exactly-(r-1)-point lines among <= N points)
  const mel = Math.floor((binom(N, 2) - 3) / (binom(r - 1, 2) + (r - 1) - 3));
  const Ym = a * Math.min(mel, e > 0 ? Math.floor(P / e) : Infinity, pairFloor);
  const hOld = H(d0, d1, Q, Yk), hNew = H(d0, d1, Q, Ym);
  return { q, r, N, Q, d0, d1, d1_over_d0: d1 / d0, E_r: E(r), melchior_per_stone: mel,
    Y_k0318: Yk, Y_melchior: Ym, H_old: hOld.H, H_new: hNew.H,
    U_old: r + hOld.H, U_new: r + hNew.H, gain: r + hOld.H - (r + hNew.H) };
}

console.log(JSON.stringify([5, 6, 7, 8].map((q) => family(7, q)), null, 1));
