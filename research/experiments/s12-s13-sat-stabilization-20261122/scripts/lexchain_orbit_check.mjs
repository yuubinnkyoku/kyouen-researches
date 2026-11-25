// lexchain_orbit_check.mjs — machine verification of the two lex-leader chain
// schemes used by enc_sat2.mjs on the n x n standard kyouen board (q=4).
//
// Schemes (per transform g, per position c, A = stone vector over cells
// 0..N-1 in fixed order, B = g(A) with B_c = A_{g^{-1}(c)}; D4 has 7
// non-identity transforms; d_{-1} = TRUE for both schemes):
//
//   DRAFT chain (enc_sat2.mjs as first emitted on 2026-11-22; archived as
//   enc_sat2_draft_chain.mjs, sha256 recorded in MANIFEST):
//     c=0:  -A_0 v B_0 v d_0 ;  A_0 v -B_0 v d_0 ;  -A_0 v B_0
//     c>=1: -d_{c-1} v -A_c v B_c v d_c ;  -d_{c-1} v A_c v -B_c v d_c ;
//           -d_{c-1} v -A_c v B_c
//
//   FIXED chain (published enc_sat2.mjs, "v2.1"): standard lex-leader with
//   FULL two-way Tseitin prefix-equality chain d_c <=> d_{c-1} AND (A_c = B_c):
//     c=0:  -A_0 v B_0                                  [blocking, unconditional]
//           -d_0 v -A_0 v B_0 ; -d_0 v A_0 v -B_0 ;
//           d_0 v -A_0 v -B_0 ; d_0 v A_0 v B_0         [d_0 <=> (A_0 = B_0)]
//     c>=1: -d_{c-1} v -A_c v B_c                       [blocking]
//           -d_c v d_{c-1} ; -d_c v -A_c v B_c ; -d_c v A_c v -B_c ;
//           -d_{c-1} v -A_c v -B_c v d_c ; -d_{c-1} v A_c v B_c v d_c
//
// Properties verified:
//  P1 Decider correctness: "exists d-chain satisfying the clauses" is decided
//     by the corresponding automaton / (for FIXED) by A <=lex g(A) directly;
//     both validated against exhaustive d-enumeration (all 2^N assignments).
//  P2 DRAFT is not a lex-leader: complete enumeration of all 2^{n^2} vectors
//     for n=3,4 counts members with A <=lex g(A) that the draft chain REJECTS.
//  P3 DRAFT fully blocks some D4 orbits (none of the 8 members accepted by
//     all 7 gates) — complete orbit census for n=3,4. This makes draft-chain
//     UNSAT results unsound as proofs.
//  P4 FIXED implements A <=lex g(A) exactly: complete check for n=3,4 over
//     all vectors and all 7 transforms (both directions of the iff).
//  P5 FIXED keeps every orbit reachable: complete census for n=3,4 (0 fully
//     blocked orbits; the orbit lex-min member passes all 7 gates), plus
//     sampled orbits for n=5..13.
//
// Usage: node lexchain_orbit_check.mjs [--out=result.json] [--sample=N]
import { writeFileSync } from 'node:fs';

const arg = (name, dflt) => { const a = process.argv.find((s) => s.startsWith('--' + name + '=')); return a ? a.split('=')[1] : dflt; };
const OUT = arg('out', null);
const SAMPLE = parseInt(arg('sample', '200'), 10);

const T = (x, y, n) => x + n * y;
const mkGs = (n) => [
  (x, y) => [n - 1 - x, y], (x, y) => [x, n - 1 - y], (x, y) => [n - 1 - x, n - 1 - y],
  (x, y) => [y, x], (x, y) => [n - 1 - y, n - 1 - x], (x, y) => [y, n - 1 - x], (x, y) => [n - 1 - y, x],
].map((f) => { const N = n * n, p = new Int32Array(N); for (let c = 0; c < N; c++) { const x = c % n, y = (c / n) | 0; const [gx, gy] = f(x, y); p[c] = T(gx, gy, n); } return p; });
const imgOf = (A, p) => { const N = A.length, inv = new Int32Array(N); for (let c = 0; c < N; c++) inv[p[c]] = c; const B = new Uint8Array(N); for (let c = 0; c < N; c++) B[c] = A[inv[c]]; return B; };
const lexLe = (A, B) => { for (let c = 0; c < A.length; c++) { if (A[c] !== B[c]) return A[c] < B[c]; } return true; };

// --- deciders ---
function draftOK(A, p) {
  // derived chain semantics: gate open while consecutive decreases; see P1
  const N = A.length, inv = new Int32Array(N); for (let c = 0; c < N; c++) inv[p[c]] = c;
  let open = 1;
  for (let c = 0; c < N; c++) { const a = A[c], b = A[inv[c]];
    if (open && a === 1 && b === 0) return false;
    open = open && a === 0 && b === 1;
  }
  return true;
}
function fixedOK(A, p) {
  // deterministic chain: the full two-way Tseitin pins d_c = d_{c-1} AND (A_c = B_c)
  const N = A.length, inv = new Int32Array(N); for (let c = 0; c < N; c++) inv[p[c]] = c;
  let dprev = 1;
  for (let c = 0; c < N; c++) { const a = A[c], b = A[inv[c]];
    if (dprev && a === 1 && b === 0) return false;
    dprev = dprev && (a === b);
  }
  return true;
}

// --- ground truth: exhaustive d-chain enumeration (small N only) ---
function draftBrute(A, p) {
  const N = A.length, inv = new Int32Array(N); for (let c = 0; c < N; c++) inv[p[c]] = c;
  for (let mask = 0; mask < (1 << N); mask++) {
    const d = (c) => (mask >> c) & 1;
    let ok = true;
    for (let c = 0; c < N && ok; c++) {
      const dp = c === 0 ? 1 : d(c - 1), a = A[c], b = A[inv[c]];
      if (!(dp === 0 || a === 0 || b === 1 || d(c) === 1)) ok = false;   // L1
      if (!(dp === 0 || a === 1 || b === 0 || d(c) === 1)) ok = false;   // L2
      if (!(dp === 0 || a === 0 || b === 1)) ok = false;                // L3
    }
    if (ok) return true;
  }
  return false;
}
function fixedBrute(A, p) {
  const N = A.length, inv = new Int32Array(N); for (let c = 0; c < N; c++) inv[p[c]] = c;
  for (let mask = 0; mask < (1 << N); mask++) {
    const d = (c) => (mask >> c) & 1;
    let ok = true;
    for (let c = 0; c < N && ok; c++) {
      const dp = c === 0 ? 1 : d(c - 1), a = A[c], b = A[inv[c]];
      if (!(dp === 0 || a === 0 || b === 1)) ok = false;                      // blocking
      if (c === 0) {
        if (!(d(0) === 0 || a === 0 || b === 1)) ok = false;                   // d_0 -> a<=b
        if (!(d(0) === 0 || a === 1 || b === 0)) ok = false;                   // d_0 -> b<=a
        if (!(d(0) === 1 || a === 0 || b === 0)) ok = false;                   // (1,1) -> d_0
        if (!(d(0) === 1 || a === 1 || b === 1)) ok = false;                   // (0,0) -> d_0
      } else {
        if (!(d(c) === 0 || dp === 1)) ok = false;                             // d_c -> d_{c-1}
        if (!(d(c) === 0 || a === 0 || b === 1)) ok = false;                   // d_c -> a<=b
        if (!(d(c) === 0 || a === 1 || b === 0)) ok = false;                   // d_c -> b<=a
        if (!(dp === 0 || a === 0 || b === 0 || d(c) === 1)) ok = false;       // open & (1,1) -> d_c
        if (!(dp === 0 || a === 1 || b === 1 || d(c) === 1)) ok = false;       // open & (0,0) -> d_c
      }
    }
    if (ok) return true;
  }
  return false;
}

const res = { p1_decider_vs_d_enumeration: {}, p2_draft_rejects_lexle: {}, p3_draft_fully_blocked_orbits: {}, p4_fixed_is_exact_lexle: {}, p5_fixed_orbit_coverage: {} };
let rngState = 987654321 >>> 0;
const rnd = () => { rngState = (Math.imul(rngState, 1103515245) + 12345) & 0x7fffffff; return rngState >>> 0; };
const randVec = (N) => { const A = new Uint8Array(N); for (let c = 0; c < N; c++) A[c] = rnd() & 1; return A; };

// P1: deciders vs exhaustive d-enumeration on random vectors and their images
{
  let draftMism = 0, fixedMism = 0, checked = 0;
  for (const n of [2, 3, 4]) {
    const N = n * n, gs = mkGs(n);
    for (let t = 0; t < 300; t++) {
      const A = randVec(N);
      for (const p of gs) {
        checked++;
        if (draftOK(A, p) !== draftBrute(A, p)) draftMism++;
        if (fixedOK(A, p) !== fixedBrute(A, p)) fixedMism++;
      }
    }
  }
  res.p1_decider_vs_d_enumeration = { checked_pairs: checked, draft_decider_mismatches: draftMism, fixed_decider_mismatches: fixedMism };
}

// P2-P5: complete enumeration for n=3,4; sampled for n=5..13
{
  for (const n of [3, 4]) {
    const N = n * n, gs = mkGs(n);
    const seen = new Set();
    let orbits = 0, draftBlocked = 0, fixedBlocked = 0;
    let draftRejectedLexLe = 0, fixedAcceptedNotLexLe = 0, fixedRejectedLexLe = 0;
    let lexminBlockedDraft = 0, lexminChecked = 0;
    for (let m = 0; m < 1 << N; m++) {
      const A = new Uint8Array(N); for (let c = 0; c < N; c++) A[c] = (m >> c) & 1;
      const key = A.join('');
      if (seen.has(key)) continue;
      const members = [A];
      for (const p of gs) { const I = new Uint8Array(N); for (let c = 0; c < N; c++) I[p[c]] = A[c]; const k = I.join(''); if (!seen.has(k)) members.push(I); }
      for (const M of members) seen.add(M.join(''));
      orbits++;
      // per-member, per-gate language checks (P2, P4)
      for (const M of members) {
        for (const p of gs) {
          const B = imgOf(M, p);
          const dr = draftOK(M, p), fx = fixedOK(M, p), le = lexLe(M, B);
          if (le && !dr) draftRejectedLexLe++;
          if (!le && fx) fixedAcceptedNotLexLe++;
          if (le && !fx) fixedRejectedLexLe++;
        }
      }
      // orbit census (P3, P5)
      let anyDraft = false, anyFixed = false;
      for (const M of members) {
        if (gs.every((p) => draftOK(M, p))) anyDraft = true;
        if (gs.every((p) => fixedOK(M, p))) anyFixed = true;
      }
      if (!anyDraft) draftBlocked++;
      if (!anyFixed) fixedBlocked++;
      // orbit lex-min member: draft blocks it? fixed accepts it? (P3/P5 sharpening)
      let minKey = null; for (const M of members) { const k = M.join(''); if (minKey === null || k < minKey) minKey = k; }
      const minM = members.find((M) => M.join('') === minKey);
      lexminChecked++;
      if (!gs.every((p) => draftOK(minM, p))) lexminBlockedDraft++;
    }
    res.p2_draft_rejects_lexle['n' + n] = { vectors_with_A_lexle_gA_rejected_by_draft: draftRejectedLexLe };
    res.p3_draft_fully_blocked_orbits['n' + n] = { orbits, fully_blocked_by_draft: draftBlocked, lexmin_members_blocked_by_draft: lexminBlockedDraft };
    res.p4_fixed_is_exact_lexle['n' + n] = {
      rejected_despite_lexle: fixedRejectedLexLe,
      accepted_despite_not_lexle: fixedAcceptedNotLexLe,
      verdict: (fixedRejectedLexLe === 0 && fixedAcceptedNotLexLe === 0) ? 'FIXED == exact A<=lex g(A)' : 'MISMATCH',
    };
    res.p5_fixed_orbit_coverage['n' + n] = { orbits, fully_blocked_by_fixed: fixedBlocked, verdict: fixedBlocked === 0 ? 'all orbits reachable' : 'ORBITS LOST' };
  }
  // sampled n = 5..13
  for (const n of [5, 6, 7, 8, 9, 10, 11, 12, 13]) {
    const N = n * n, gs = mkGs(n);
    let bad = 0, lexminBad = 0;
    for (let t = 0; t < SAMPLE; t++) {
      const A = randVec(N);
      // P4 direction check on random vectors and images
      for (const p of gs) {
        const B = imgOf(A, p), le = lexLe(A, B);
        if (le !== fixedOK(A, p)) bad++;
      }
      // P5: orbit lex-min passes all gates
      const members = [A];
      for (const p of gs) { const I = new Uint8Array(N); for (let c = 0; c < N; c++) I[p[c]] = A[c]; members.push(I); }
      let minKey = null; for (const M of members) { const k = M.join(''); if (minKey === null || k < minKey) minKey = k; }
      const minM = members.find((M) => M.join('') === minKey);
      if (!gs.every((p) => fixedOK(minM, p))) lexminBad++;
    }
    res.p4_fixed_is_exact_lexle['n' + n + '_sampled'] = { samples: SAMPLE, mismatches: bad };
    res.p5_fixed_orbit_coverage['n' + n + '_sampled'] = { samples: SAMPLE, lexmin_members_rejected_by_all_gates: lexminBad };
  }
}
const json = JSON.stringify(res, null, 1);
console.log(json);
if (OUT) writeFileSync(OUT, json + '\n');
