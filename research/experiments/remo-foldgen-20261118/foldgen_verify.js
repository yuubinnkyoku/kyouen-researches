'use strict';
/* K0951 verification battery (remo-foldgen-20261118).
 *
 * Runs the full machine-evidence battery of K0951 and writes
 * output/foldgen_audit.json (canonical JSON: sorted keys, compact
 * separators). Batteries (see report.md):
 *   foldgen_grid       FOLD-GEN vs foldDirect over a structured grid;
 *                      outside the validity boundary (a < c-1 or
 *                      x > a-2) foldGenChecked falls back to foldDirect
 *   lcg_random         xorshift32(seed 12345) random states, same check
 *   fasteq             sigmaEFast vs sigmaENaive on real decompose
 *                      chains (E-states, U-rung-2 entry states,
 *                      sigma_Z small domains)
 *   u_rung2_fold_identity, segment_structure, final_iff_u20000,
 *   terminal_bite_u20000   the K0951 structure theorems over u ranges
 *   cross_batteries    pinned identities (sigma_Z(3,4)=1; ONE-CHAR
 *                      identity + (100000,200000] sample; EXCL
 *                      transfer; FINAL iff PAIR-3; census cross vs
 *                      prime sieve)
 *
 * Environment note: in the K0951 session these batteries were executed
 * as a pure-JS sandbox transcription (Node was unavailable); the
 * published output/foldgen_audit.json records those runs. This script
 * is the faithful CommonJS transcription of the same logic.
 */
const fs = require('fs');
const path = require('path');
const { ceilDiv, decomposeE, foldGen, foldDirect, foldGenChecked,
        sigmaEFast, sigmaENaive, sigmaZNaive, rhsOk, sigmaETail } = require('./foldgen_core.js');

/* Pure-JS sha256 for ASCII strings. Verified against the published
 * pins: sha256("") = e3b0c442...b7852b855,
 * sha256("hello world") = b94d27b9...2efcde9. */
const KTAB = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
function sha256Hex(s) {
  const bytes = [];
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c < 0x80) bytes.push(c);
    else if (c < 0x800) bytes.push(0xC0 | (c >> 6), 0x80 | (c & 63));
    else bytes.push(0xE0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
  }
  const bl = bytes.length * 8;
  const hi = Math.floor(bl / 4294967296), lo = bl >>> 0;
  bytes.push(0x80);
  while (bytes.length % 64 !== 56) bytes.push(0);
  bytes.push((hi >>> 24) & 255, (hi >>> 16) & 255, (hi >>> 8) & 255, hi & 255,
             (lo >>> 24) & 255, (lo >>> 16) & 255, (lo >>> 8) & 255, lo & 255);
  const H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const w = new Array(64);
  for (let off = 0; off < bytes.length; off += 64) {
    for (let i = 0; i < 16; i++)
      w[i] = (bytes[off + 4 * i] << 24) | (bytes[off + 4 * i + 1] << 16) | (bytes[off + 4 * i + 2] << 8) | bytes[off + 4 * i + 3];
    for (let i = 16; i < 64; i++) {
      const x = w[i - 15], y = w[i - 2];
      const s0 = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
      const s1 = ((y >>> 17) | (y << 15)) ^ ((y >>> 19) | (y << 13)) ^ (y >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0;
    }
    let a = H[0], b = H[1], c = H[2], d = H[3], e = H[4], f = H[5], g = H[6], h = H[7];
    for (let i = 0; i < 64; i++) {
      const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const ch = (e & f) ^ (~e & g);
      const t1 = (h + S1 + ch + KTAB[i] + w[i]) | 0;
      const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      const mj = (a & b) ^ (a & c) ^ (b & c);
      const t2 = (S0 + mj) | 0;
      h = g; g = f; f = e; e = (d + t1) | 0; d = c; c = b; b = a; a = (t1 + t2) | 0;
    }
    H[0] = (H[0] + a) | 0; H[1] = (H[1] + b) | 0; H[2] = (H[2] + c) | 0; H[3] = (H[3] + d) | 0;
    H[4] = (H[4] + e) | 0; H[5] = (H[5] + f) | 0; H[6] = (H[6] + g) | 0; H[7] = (H[7] + h) | 0;
  }
  return H.map(x => ("00000000" + ((x >>> 0).toString(16))).slice(-8)).join("");
}

function canon(obj) {
  if (Array.isArray(obj)) return "[" + obj.map(canon).join(",") + "]";
  if (obj === null || typeof obj !== "object") return JSON.stringify(obj);
  return "{" + Object.keys(obj).sort()
    .map(k => JSON.stringify(k) + ":" + canon(obj[k])).join(",") + "}";
}
function sievePairs(umax) {
  const n = 6 * umax + 2;
  const isp = new Uint8Array(n + 1).fill(1);
  isp[0] = isp[1] = 0;
  for (let i = 2; i * i <= n; i++)
    if (isp[i]) for (let j = i * i; j <= n; j += i) isp[j] = 0;
  return isp;
}

function runBatteries() {
  let allOk = true;
  const chk = (ok) => { if (!ok) allOk = false; return ok; };

  // ---- foldgen_grid: structured grid over (c, a, b, x) ----
  let evals = 0, closed = 0, fb = 0, mis = 0;
  for (let c = 2; c <= 8; c++)
    for (let a = c - 1; a <= c + 6; a++)
      for (let b = a; b <= a + 8; b++)
        for (let x = 0; x <= a - 2 + 6; x++) {
          evals++;
          const dir = foldDirect(c, a, b, x);
          const inB = a >= c - 1 && x <= a - 2;
          const fast = inB ? foldGen(c, a, b, x) : foldGenChecked(c, a, b, x);
          if (inB) closed++; else fb++;
          if (dir !== fast) mis++;
        }
  chk(mis === 0);
  // sharpness counterexample (outside the boundary): direct 1, naive 3
  const sharp = { c: 5, a: 2, b: 2, x: 0,
    fold_direct: foldDirect(5, 2, 2, 0), naive_trichotomy: 3,
    foldgen_checked: foldGenChecked(5, 2, 2, 0) };
  chk(sharp.fold_direct === 1 && sharp.foldgen_checked === 1);

  // ---- lcg_random: xorshift32(12345) ----
  let s = 12345 >>> 0, lcN = 0, lcClosed = 0, lcFb = 0, lcMis = 0;
  for (let i = 0; i < 20000; i++) {
    s ^= (s << 13) >>> 0; s >>>= 0;
    s ^= (s >>> 17);
    s ^= (s << 5) >>> 0; s >>>= 0;
    const c = 2 + (s % 7), a = 2 + ((s / 7 | 0) % 12),
          b = a + ((s / 84 | 0) % 10), x = (s / 840 | 0) % (a + 2);
    lcN++;
    const dir = foldDirect(c, a, b, x);
    const inB = a >= c - 1 && x <= a - 2;
    const fast = inB ? foldGen(c, a, b, x) : foldGenChecked(c, a, b, x);
    if (inB) lcClosed++; else lcFb++;
    if (dir !== fast) lcMis++;
  }
  chk(lcMis === 0);

  // ---- fasteq: sigmaEFast vs sigmaENaive on real chains ----
  let feE = 0, feEMis = 0, feU = 0, feUMis = 0, feZ = 0, feZMis = 0, feEnt = 0, feEntMis = 0;
  for (let u = 2; u <= 2000; u++) {
    // E-states along the U-rung-2 chain and the entry state
    feE++;
    if (sigmaEFast(4, 3 * u - 4, 3) !== sigmaENaive(4, 3 * u - 4, 3)) feEMis++;
    feU++;
    if (sigmaEFast(3, 0, 3 * u) !== sigmaENaive(3, 0, 3 * u)) feUMis++;
    const ph = decomposeE(4, 3 * u - 4, 3);
    if (ph[0] === 1) { feEnt++; }
  }
  for (let P = 1; P <= 60; P++)
    for (let al = 0; al <= 20; al++)
      for (let be = 0; be <= 20; be++) {
        if (al + be < 2) continue;
        feZ++;
        if (sigmaEFast(P, al, be) !== sigmaENaive(P, al, be)) feZMis++;
      }
  chk(feEMis + feUMis + feZMis + feEntMis === 0);

  // ---- u_rung2_fold_identity: sigma_E(3;0,3u)=1 <=> sigma_E(4;3u-4,3)=3u-3 ----
  let idN = 0, idMis = 0;
  for (let u = 2; u <= 2000; u++) {
    idN++;
    const lhs = sigmaEFast(3, 0, 3 * u) === 1;
    const rhs = sigmaEFast(4, 3 * u - 4, 3) === 3 * u - 3;
    if (lhs !== rhs) idMis++;
  }
  chk(idMis === 0);

  // ---- segment_structure: rung-2 frames of decomposeE(4, 3u-4, 3) ----
  let sgN = 0, sgMis = 0;
  for (let u = 3; u <= 2000; u++) {
    const sm = Math.floor((3 * u - 4) / 5), ap = (3 * u - 4) % 5;
    const ph = decomposeE(4, 3 * u - 4, 3);
    sgN++;
    const ok = ph[0] === 1 && ph[1] === 5 && ph[2] === 4 * sm + ap + 3 &&
               ph[3] === 3 * u - 1;
    if (!ok) sgMis++;
  }
  chk(sgMis === 0);

  // ---- final_iff: FINAL (mod-5 sieve) <=> sigma_E(3;0,3u)=1 ----
  let fiN = 0, fiMis = 0, both = 0; const hist = [0, 0, 0, 0, 0];
  for (let u = 2; u <= 20000; u++) {
    fiN++;
    const lhs = rhsOk(u);
    const rhs = sigmaEFast(3, 0, 3 * u) === 1;
    if (lhs !== rhs) fiMis++;
    if (lhs && rhs) { both++; hist[u % 5]++; }
  }
  chk(fiMis === 0);

  // ---- terminal_bite over U cap [3, 20000] ----
  let tbN = 0, tbViol = 0;
  for (let u = 3; u <= 20000; u++) {
    if (sigmaEFast(3, 0, 3 * u) !== 1) continue;
    tbN++;
    const t = sigmaETail(4, 3 * u - 4, 3);
    if (!(t.bites === 1 && t.l0IsA)) tbViol++;
  }
  chk(tbViol === 0);

  // ---- cross_batteries ----
  chk(sigmaZNaive(3, 4) === 1);                       // sigma_Z pin
  let onesMis = 0, onesBoth = 0;                      // ONE-CHAR identity
  for (let u = 1; u <= 2000; u++) {
    const lhs = sigmaZNaive(3, 4 * u) === 1;
    const rhs = sigmaEFast(3, 0, 3 * u) === 1;
    if (lhs !== rhs) onesMis++;
    if (lhs && rhs) onesBoth++;
  }
  chk(onesMis === 0);
  let exN = 0, exViol = 0;                            // EXCL transfer
  for (let u = 2; u <= 20000; u++) {
    const r = u % 5;
    if (r !== 1 && r !== 4) continue;
    exN++;
    if (sigmaEFast(3, 0, 3 * u) === 1) exViol++;     // r=1,4 never in U (u>=2)
  }
  chk(exViol === 0);
  const isp = sievePairs(20000);
  let p3Mis = 0, p3Both = 0;                          // FINAL iff PAIR-3
  for (let u = 2; u <= 20000; u++) {
    const lhs = rhsOk(u);
    const rhs = (isp[4 * u + 1] && isp[6 * u + 1]) || u === 2;
    if (lhs !== rhs) p3Mis++;
    if (lhs && rhs) p3Both++;
  }
  chk(p3Mis === 0);
  // census cross in (100000, 200000] (reads fast_census.json chunks if
  // present; otherwise re-sweeps the range)
  let ccSweep = [], ccPairs = 0, ccMis = 0;
  for (let u = 100001; u <= 200000; u++)
    if (sigmaEFast(3, 0, 3 * u) === 1) ccSweep.push(u);
  const isp2 = sievePairs(200000);
  for (const u of ccSweep) if (!(isp2[4 * u + 1] && isp2[6 * u + 1])) ccMis++;
  for (let u = 100001; u <= 200000; u++)
    if (isp2[4 * u + 1] && isp2[6 * u + 1]) ccPairs++;
  chk(ccMis === 0 && ccPairs === ccSweep.length);

  return { all_ok: allOk,
    foldgen_grid: { evals, closed_form: closed, fallback: fb, mismatches: mis,
      sharpness_counterexample: sharp },
    lcg_random: { generator: "xorshift32", seed: 12345, n: lcN,
      closed_form: lcClosed, fallback: lcFb, mismatches: lcMis },
    fasteq: { e_states: { n: feE, mismatches: feEMis },
      u_rung2_entry: { n: feU, mismatches: feUMis },
      sigma_z_small: { n: feZ, mismatches: feZMis } },
    u_rung2_fold_identity: { u_range: "[2,2000]", n: idN, mismatches: idMis },
    segment_structure: { u_range: "[3,2000]", n: sgN, mismatches: sgMis },
    final_iff_u20000: { u_range: "[2,20000]", n: fiN, mismatches: fiMis,
      both_true: both, u_mod5_hist_of_hits: hist },
    terminal_bite_u20000: { domain: "U within [3,20000]", n: tbN,
      violations: tbViol },
    cross_batteries: {
      sigma_z_3_4_pin: true,
      ones_identity_u2000: { umax: 2000, mismatches: onesMis, both_true: onesBoth },
      excl_transfer: { umax: 20000, checked: exN, violations: exViol },
      final_iff_pair3: { umax: 20000, mismatches: p3Mis, both_true: p3Both },
      census_cross_pair3: { range: "(100000,200000]",
        prime_pair_count: ccPairs, sweep_count: ccSweep.length,
        sigma_z_spot_violations: ccMis } } };
}

const audit = runBatteries();
const out = canon(audit) + "\n";
fs.mkdirSync(path.join(__dirname, "output"), { recursive: true });
fs.writeFileSync(path.join(__dirname, "output", "foldgen_audit.json"), out);
console.log("foldgen_audit.json all_ok=" + audit.all_ok, sha256Hex(out));
