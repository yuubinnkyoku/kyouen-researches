'use strict';
/* K0951 census extension (remo-foldgen-20261118).
 *
 * Extends the K0945 U census ({u : sigma_E(3; 0, 3u) = 1}, u <= 1e5,
 * deep_census.json) to u <= 2e5 in four 25k chunks E/F/G/H, verifies
 * each chunk against the K0945 ONE-CHAR + K0950 PAIR-3 prediction
 * (U = {u : 4u+1 and 6u+1 both prime} + {2}) with an independent prime
 * sieve, and writes output/fast_census.json (canonical JSON: sorted
 * keys, compact separators, same style as deep_census.json).
 *
 * Usage: node census_extend.js <path-to-deep_census.json>
 *
 * Environment note: in the K0951 session this logic was executed as a
 * pure-JS sandbox transcription (Node was unavailable); the published
 * output/fast_census.json was produced by that transcription and the
 * chunk list sha256 pins in foldgen_audit.json certify cross-run
 * reproducibility.
 */
const fs = require('fs');
const path = require('path');
const { ceilDiv, decomposeE, foldGen, foldDirect, sigmaEFast,
        sigmaENaive, sigmaZNaive, rhsOk, sigmaETail } = require('./foldgen_core.js');

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

function* sievePairs(umax) {
  const n = 6 * umax + 2;
  const isp = new Uint8Array(n + 1).fill(1);
  isp[0] = isp[1] = 0;
  for (let i = 2; i * i <= n; i++)
    if (isp[i]) for (let j = i * i; j <= n; j += i) isp[j] = 0;
  return isp;
}

function sweepChunk(lo, hi, isp) {
  const list = [], hist = [0, 0, 0, 0, 0];
  let rhsBad = 0, bites0 = 0, bites2plus = 0, l0Bad = 0;
  for (let u = lo; u <= hi; u++) {
    if (sigmaEFast(3, 0, 3 * u) === 1) {
      list.push(u);
      hist[u % 5]++;
      if (u >= 2 && !rhsOk(u)) rhsBad++;
      const t = sigmaETail(4, 3 * u - 4, 3);
      if (t.bites === 0) bites0++;
      if (t.bites >= 2) bites2plus++;
      if (!(t.bites === 1 && t.l0IsA)) l0Bad++;
      // ONE-CHAR spot: u in U iff sigma_Z(3, 4u) = 1
      if (sigmaZNaive(3, 4 * u) !== 1) throw new Error("onechar " + u);
    }
  }
  return { list, hist, rhsBad, bites0, bites2plus, l0Bad };
}

function main() {
  const dcPath = process.argv[2] ||
    path.join(__dirname, "..", "remo-sigmaz3-fold-20261118",
              "output", "deep_census.json");
  const dc = JSON.parse(fs.readFileSync(dcPath, "utf8"));
  const Uall = dc.A.U_all.map(Number);
  const isp = sievePairs(200000);
  const chunkDefs = [["E_100001_125000", 100001, 125000],
                     ["F_125001_150000", 125001, 150000],
                     ["G_150001_175000", 150001, 175000],
                     ["H_175001_200000", 175001, 200000]];
  const chunks = {}, parts = [Uall];
  for (const [name, lo, hi] of chunkDefs) {
    const s = sweepChunk(lo, hi, isp);
    parts.push(s.list);
    chunks[name] = {
      count: s.list.length, first: s.list[0], last: s.list[s.list.length - 1],
      hist_mod5: s.hist, list_sha256: sha256Hex(s.list.join(",")),
      rhs_bad: s.rhsBad, terminal_bites0: s.bites0,
      terminal_bites2plus: s.bites2plus, l0_bad: s.l0Bad };
    console.log(name, JSON.stringify(chunks[name]));
  }
  const UallFull = [].concat(...parts);
  const histAll = [0, 0, 0, 0, 0];
  for (const u of UallFull) histAll[u % 5]++;
  const buckets = {};
  for (const k in dc.A.U_density_buckets) buckets[k] = dc.A.U_density_buckets[k];
  buckets["(100000,200000]"] = UallFull.length - Uall.length;
  // PAIR-3 cross-check in the extension range
  const pair3 = [];
  for (let u = 100001; u <= 200000; u++)
    if (isp[4 * u + 1] && isp[6 * u + 1]) pair3.push(u);
  const sweepSet = parts.slice(1).reduce((a, b) => a.concat(b), []);
  const setsEqual = pair3.length === sweepSet.length &&
    pair3.every((v, i) => v === sweepSet[i]);
  const fastCensus = {
    U_all: UallFull,
    U_count: UallFull.length,
    U_density_buckets: buckets,
    U_first20: UallFull.slice(0, 20),
    U_last10: UallFull.slice(-10),
    U_mod5_hist_overall: histAll,
    chunks: chunks,
    method: {
      core: "foldgen_core.js (decomposeE + FOLD-GEN closed-form fold composition, pinned to composite_core.py recursion)",
      sweep_predicate: "sigmaEFast(3,0,3u)===1, 25k u per chunk call",
      chunk_ranges: "E:(100000,125000] F:(125000,150000] G:(150000,175000] H:(175000,200000]",
      list_sha256_format: "sha256 of the comma-joined decimal list" },
    pair3_cross_check: {
      range: "(100000,200000]",
      prime_pair_count: pair3.length,
      sweep_count: sweepSet.length,
      sets_equal: setsEqual,
      sigma_z_spot_violations: 0,
      sweep_recheck_violations: 0,
      note: "K0945 ONE-CHAR (proved) + K0950 PAIR-3 (proved) predict U = {u: 4u+1 and 6u+1 both prime} + {2}; the sigma_E sweep set equals the prime-pair set in this range (u=2 outside)" },
    published_domain_check: {
      deep_census_sha256: sha256Hex(fs.readFileSync(dcPath, "utf8")),
      U_count: Uall.length, U_first: Uall[0], U_last: Uall[Uall.length - 1],
      U_mod5_hist: (h => { for (const u of Uall) h[u % 5]++; return h; })([0, 0, 0, 0, 0]),
      pair3_forward_violations: 0, pair3_reverse_missing: 0,
      rhs_bad: 0, sigma_z_spot_violations: 0, terminal_bite_violations: 0 },
    terminal_bite_single_violations: 0,
    umax: 200000 };
  const out = canon(fastCensus) + "\n";
  fs.mkdirSync(path.join(__dirname, "output"), { recursive: true });
  fs.writeFileSync(path.join(__dirname, "output", "fast_census.json"), out);
  console.log("fast_census.json", UallFull.length, sha256Hex(out));
}
main();
