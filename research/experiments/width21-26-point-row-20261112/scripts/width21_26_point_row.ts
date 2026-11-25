// Verifier for: P(w) <= 2*ceil(w/2) - 2 for w = 21..26 (all candidates at the
// k = ceil(w/2) point-row level die at mod 19), and the extended realizability
// exclusion of the surviving candidate point-row sets at w = 19, 20
// (standard form, e = 4D arbitrary integer, R' = A + e^2/16 <= 2e7;
// A = 0 rigorously impossible for every candidate set).
//
// Framework (K0072 / K0767 / K0778; fifth independent implementation):
//   Circle x^2+y^2+Cx+Dy+N=0 on rows 0..w-1. Any double row forces C in Z
// (sum of the two integer roots). Point rows y satisfy
//   s_y^2 = A - 4y^2 - e*y,   A = C^2 - 4N,  e = 4D.
// For any two point rows y, y': e*(y-y') = (s_y'^2 - s_y^2) - 4(y^2 - y'^2) is
// in Z, so with X = e and the fraction denominator g0 of X (g0 = 1 iff X in Z):
// ALL point rows are congruent mod g0 ("g0-counting lemma").
//   X in Z ("standard form"): A in Z (A - X*y1 = s^2 + 4y1^2) and every point
// row satisfies the coef-4 certificate: exists (a,u) mod m with
// a - 4i^2 - u*i in QR0(m) (witness (a,u) = (A, X); QR0 = squares incl. 0;
// free (a,u) is a sound superset for every m, even included).
//   g0 = 2: all point rows same parity (g=2 form): 4*s_y^2 = 4A - 16y^2 - 4Xy
// with 4A, 4X in Z, and (2s_y)^2 is a perfect square, so the coef-16
// certificate a - 16i^2 - u*i in QR0(m) is necessary.
//   g0 >= 3: |point rows| <= ceil(w/g0) <= ceil(26/3) = 9.
// Accounting: P = 2d + s <= 2(d+s), tangents s <= 2 (geometry).
//   P >= 2k-1 (k = ceil(w/2)) -> d+s >= k and d >= k-1 >= 10 >= 8 -> C in Z.
//   Mixed-parity point-row set -> standard form forced (g0 = 2 contradicts
// mixed parity; g0 >= 3 contradicts d+s >= k: 9 < 11 <= k at w=21..26, and
// at w=19,20 ceil(20/3) = 7 < 9 = the d+s needed for P >= 17).
//
// Claims verified here:
//   (1) w=21..26, k=ceil(w/2): the k-subsets of {0..w-1} passing the mod 9 x 11
// certificates are enumerated COMPLETELY by the window masks
//   T(x,y) = {i in 0..w-1 : mask9[x][i%9] && mask11[y][i%11]}
// over all 81*121 (a,u) pairs (free (a,u) absorbs the board translation, so
// shift-0 windows are complete; any passing k-subset is a subset of some T
// with |T| >= k, and |T| <= 14 < 2k so only exact-T and drop-one cases occur).
// Every candidate (11/34/9/22/7/28 distinct sets) FAILS the coef-4
// certificate at mod 19. No same-parity candidate exists; the same-parity
// classes die under coef-16 anyway (class maxima 7..9 < k).
// -> d+s <= k-1 -> P(w) <= 2k-2.
//   (2) k+1 level: 0 candidates at w=21..25 (max |T| = k); at w=26 the single
// 14-row candidate dies at mod 19 (K0776/K0778's 891 shifted windows come
// from the same 9 parameter pairs x 99 shifts).
//   (3) Controls (same machinery): w=17,18 k=9 -> 0 survivors; w=19 k=9 ->
// exactly 2 (S1 = {0,1,4,6,7,12,13,15,18} and its mirror {0,3,5,6,11,12,14,17,18});
// w=20 k=9 -> exactly 8 (4 mirror pairs). Independent full brute force of all
// C(21,11) = 352,716 subsets -> 0 survivors.
//   (4) A = 0 (row-0 tangent) is rigorously impossible for all 8 distinct
// candidate row sets: two rows with equal squarefree part give a finite
// factorization of d = -e (rows 1,4: d = 20; rows 3,12: d = 60; rows 1,16:
// d in {68, 260}), each candidate d failing a remaining row (some row y needs
// d >= 4y); the set {0,1,6,...} has no equal-squarefree pair: rows 1,6 force
// s1^2 = 6m^2 + 20 = 2 mod 3, not a square. Bounded scans d <= 2e6 confirm
// 0 solutions for every set.
//   (5) Standard-form realizability search with e in Z COMPLETE (previous
// coverage in K0778 was e = 4D = 0 mod 4 only), region R' = A + e^2/16 <= 2e7
// fully covered: 0 realizations for each of the 8 sets.
// Row-0 sets sweep (s0, s_ymax) in [0,4472]^2 (any config with R' <= 2e7 has
// s_y <= sqrt(R') and |2y+D| <= sqrt(R'), both <= 4472, and A = s0^2 <= 2e7);
// non-row-0 sets sweep (s_p, s_q) in [0,4600]^2 with A in [0,2e7] and
// A mod 4 in {0,1} (C^2 = A mod 4 needed for N = (C^2 - A)/4 in Z).
// e even is forced for mixed-parity sets (x = (-C +- s_y)/2 integral ->
// s_y = C mod 2 for every point row -> e*(y - y') even).
//   (6) Witness control: A = 9, e = -44 reproduces the 16-point circle
// (2x-11)^2 + (2y-11)^2 = 130 exactly (s = 3,7,9,11,11,9,7,3).
//
// Stages (STAGE): "classify" (1,2,3 + parity16 class maxima; fast),
// "brute21" (full C(21,11) enumeration), "a0" (algebraic checks + d<=2e6
// scans; heavy, ~minutes), "search" (per-set standard-form search; SET in
// s19_S1, s1, s3..s8; each ~2e7 pair iterations), "all" = classify + brute21.

const STAGE = "all";
const SET = "s19_S1";

async function main() {
  const out: any = { generated: "2026-11-12", parts: {} };
  const qrC: Record<number, Uint8Array> = {};
  const getQR = (m: number): Uint8Array => {
    if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
    return qrC[m];
  };
  function subsetOK(S: number[], m: number, coef: number): boolean {
    const qr = getQR(m);
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      let ok = true;
      for (let k = 0; k < S.length; k++) {
        const i = S[k]; let t = (a - (coef * i * i) % m - u * i) % m; if (t < 0) t += m;
        if (!qr[t]) { ok = false; break; }
      }
      if (ok) return true;
    }
    return false;
  }
  function buildMasks(m: number): Uint8Array[] {
    const qr = getQR(m); const masks: Uint8Array[] = [];
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      const mk = new Uint8Array(m);
      for (let i = 0; i < m; i++) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) t += m; mk[i] = qr[t]; }
      masks.push(mk);
    }
    return masks;
  }
  const m9 = buildMasks(9), m11 = buildMasks(11);
  const REST = [19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
  const ALLMODS = [9, 11].concat(REST);
  const isSq = (v: number): number => { if (v < 0) return -1; const s = Math.round(Math.sqrt(v)); return s * s === v ? s : -1; };

  function windowClassify(w: number, k: number) {
    const cand = new Set<string>(); let maxT = 0; const hist: Record<number, number> = {};
    for (let x = 0; x < m9.length; x++) for (let y = 0; y < m11.length; y++) {
      const T: number[] = [];
      for (let i = 0; i < w; i++) if (m9[x][i % 9] && m11[y][i % 11]) T.push(i);
      const t = T.length; hist[t] = (hist[t] || 0) + 1; if (t > maxT) maxT = t;
      if (t === k) cand.add(T.join(","));
      else if (t > k) for (let d = 0; d < t; d++) cand.add(T.filter((_, ix) => ix !== d).join(","));
    }
    let s4 = 0, s16 = 0, sameParityBoth = 0; const perKill: Record<string, number> = {}; const samples: number[][] = [];
    for (const key of cand) {
      const S = key.split(",").map(Number);
      let alive = true;
      for (const m of REST) if (!subsetOK(S, m, 4)) { perKill[m] = (perKill[m] || 0) + 1; alive = false; break; }
      if (alive) { s4++; if (samples.length < 20) samples.push(S); continue; }
      if (S.every(v => v % 2 === S[0] % 2)) {
        let a2 = true;
        for (const m of ALLMODS) if (!subsetOK(S, m, 16)) { a2 = false; break; }
        if (a2) s16++; else sameParityBoth++;
      }
    }
    return { w, k, maxT,
      histTop: (() => { const h: any = {}; for (const t in hist) if (+t >= k - 1) h[t] = hist[t]; return h; })(),
      candidates: cand.size, survivorsCoef4: s4, survivorsG2Only: s16,
      killedSameParityBothForms: sameParityBoth, perKill, samples };
  }

  if (STAGE === "all" || STAGE === "classify") {
    for (let w = 21; w <= 26; w++) {
      const k = Math.ceil(w / 2);
      out.parts["w" + w + "_k" + k] = windowClassify(w, k);
      out.parts["w" + w + "_k" + (k + 1)] = windowClassify(w, k + 1);
    }
    for (const w of [17, 18, 19, 20]) out.parts["control_w" + w + "_k9"] = windowClassify(w, 9);
    function classMax(rows: number[], mods: number[], coef: number): number {
      let best = Infinity;
      for (const m of mods) { const qr = getQR(m); let bm = 0;
        for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) { let c = 0;
          for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) t += m; if (qr[t]) c++; }
          if (c > bm) bm = c; }
        if (bm < best) best = bm; }
      return best;
    }
    const par: any = {};
    for (let w = 21; w <= 26; w++) {
      const ev: number[] = [], od: number[] = [];
      for (let y = 0; y < w; y += 2) ev.push(y); for (let y = 1; y < w; y += 2) od.push(y);
      par[w] = { evens: ev.length, evensC16max: classMax(ev, ALLMODS, 16), odds: od.length, oddsC16max: classMax(od, ALLMODS, 16) };
    }
    out.parts.parityClassC16Maxima = par;
  }

  if (STAGE === "all" || STAGE === "brute21") {
    let total = 0, surv = 0; const cur: number[] = [];
    (function rec(s: number) {
      if (cur.length === 11) { total++;
        let alive = true;
        for (const m of ALLMODS) if (!subsetOK(cur, m, 4)) { alive = false; break; }
        if (alive) surv++;
        return; }
      for (let i = s; i < 21; i++) { cur.push(i); rec(i + 1); cur.pop(); }
    })(0);
    out.parts.brute21_k11 = { total, survivors: surv };
  }

  // The 8 distinct candidate row sets. w=19 survivors: {s19_S1, s1};
  // w=20 survivors: {s1, s19_S1(=s2), s3, s4, s5, s6, s7, s8} (4 mirror pairs:
  // (s19_S1,s7), (s1,s8), (s3,s4), (s5,s6)); s1 realizes both its w=19 and
  // w=20 candidacies with the same row set, so 8 distinct sets in total.
  const SETS: Record<string, number[]> = {
    s19_S1: [0, 1, 4, 6, 7, 12, 13, 15, 18],
    s1: [0, 3, 5, 6, 11, 12, 14, 17, 18],
    s3: [0, 1, 3, 4, 7, 12, 15, 18, 19],
    s4: [0, 1, 4, 7, 12, 15, 16, 18, 19],
    s5: [0, 1, 4, 6, 7, 12, 13, 18, 19],
    s6: [0, 1, 6, 7, 12, 13, 15, 18, 19],
    s7: [1, 4, 6, 7, 12, 13, 15, 18, 19],
    s8: [1, 2, 5, 7, 8, 13, 14, 16, 19],
  };

  if (STAGE === "a0") {
    // A=0: s_y^2 = y(d - 4y), d = -e. Rows with equal squarefree part g
    // (y = g h^2) force d - 4y = g n^2, so g(n_a^2 - n_b^2) = 4(y_b - y_a):
    // finitely many d, each of which must fail some remaining row.
    function sqfree(y: number): number { let g = 1; let v = y; for (let p = 2; p * p <= v; p++) { let c = 0; while (v % p === 0) { v /= p; c++; } if (c % 2) g *= p; } return g * v; }
    const a0: any = {};
    for (const key of Object.keys(SETS)) {
      const rows = SETS[key].filter(y => y > 0);
      a0[key] = { provedByFiniteFactorization: false };
      let proved = false;
      for (let a = 0; a < rows.length && !proved; a++) for (let b = a + 1; b < rows.length && !proved; b++) {
        const ga = sqfree(rows[a]), gb = sqfree(rows[b]);
        if (ga !== gb) continue;
        const D = 4 * (rows[b] - rows[a]) / ga; // (na - nb)(na + nb) = D
        const dcands: number[] = [];
        for (let f = 1; f * f <= D; f++) if (D % f === 0) {
          const f2 = D / f; if ((f + f2) % 2 !== 0) continue;
          const na = (f + f2) / 2; const nb2 = na * na - D;
          const nb = Math.round(Math.sqrt(Math.max(0, nb2)));
          if (nb * nb !== nb2) continue;
          const d1 = 4 * rows[a] + ga * na * na, d2 = 4 * rows[b] + ga * nb * nb;
          if (d1 === d2) dcands.push(d1);
        }
        if (dcands.length > 0) {
          let allDead = true;
          for (const d of dcands) { let ok = true; for (const y of rows) if (isSq(y * (d - 4 * y)) < 0) { ok = false; break; } if (ok) allDead = false; }
          if (allDead) { proved = true; a0[key] = { pair: [rows[a], rows[b]], dCandidates: dcands, provedByFiniteFactorization: true }; }
        }
      }
      if (!proved && key === "s6") {
        a0[key] = { argument: "rows 1,6: s6^2 = 6(d-24) -> 6|s6 -> d = 24+6m^2; s1^2 = d-4 = 6m^2+20 = 2 mod 3 (not a square)", provedByFiniteFactorization: false, provedByMod3: true };
      }
      let sols = 0;
      for (let d = 0; d <= 2000000; d++) { let ok = true; for (const y of rows) if (isSq(y * (d - 4 * y)) < 0) { ok = false; break; } if (ok) sols++; }
      a0[key].scanSolutions_d_le_2e6 = sols;
    }
    out.parts.a0_exclusion = a0;
  }

  if (STAGE === "search") {
    const AMAX = 20000000;
    const S = SETS[SET];
    let pairs = 0, pass = 0, hits = 0; const hitList: any[] = [];
    if (S[0] === 0) {
      const ymax = S[S.length - 1]; const rest = S.slice(1, S.length - 1);
      for (let s0 = 1; s0 <= 4472; s0++) { const A = s0 * s0;
        for (let sy = 0; sy <= 4472; sy++) { pairs++;
          const diff = A - 4 * ymax * ymax - sy * sy;
          if (diff % ymax !== 0) continue;
          const e = diff / ymax;
          if ((e & 1) !== 0) continue; // mixed-parity set: e even forced
          pass++;
          let ok = true;
          for (const y of rest) if (isSq(A - 4 * y * y - e * y) < 0) { ok = false; break; }
          if (ok) { hits++; if (hitList.length < 10) hitList.push({ A, e }); }
        } }
    } else {
      const p = S[0], q = S[S.length - 1]; const rest = S.slice(1, S.length - 1);
      const dqp = q - p, c = -4 * (q * q - p * p); const SMAX = 4600;
      for (let sp = 0; sp <= SMAX; sp++) { const sp2 = sp * sp;
        for (let sq = 0; sq <= SMAX; sq++) { pairs++;
          const num = c - (sq * sq - sp2);
          if (num % dqp !== 0) continue;
          const e = num / dqp;
          if ((e & 1) !== 0) continue;
          const A = sp2 + 4 * p * p + e * p;
          if (A < 0 || A > AMAX || (A & 3) > 1) continue;
          pass++;
          let ok = true;
          for (const y of rest) if (isSq(A - 4 * y * y - e * y) < 0) { ok = false; break; }
          if (ok) { hits++; if (hitList.length < 10) hitList.push({ A, e }); }
        } }
    }
    out.parts.search = { set: SET, rows: S, pairsTested: pairs, passFilters: pass, hits, hitList };
    const wc: number[] = []; let wok = true;
    for (const y of [0, 1, 2, 4, 7, 9, 10, 11]) { const s = isSq(9 - 4 * y * y + 44 * y); if (s < 0) wok = false; else wc.push(s); }
    out.parts.witnessControlA9eMinus44 = { ok: wok, s: wc };
  }

  if (STAGE !== "search") {
    out.parts.claims = {
      Pw: { 21: "<=20", 22: "<=20", 23: "<=22", 24: "<=22", 25: "<=24", 26: "<=24" },
      general: "P(w) <= 2*ceil(w/2) - 2 for w = 21..26 (proved; sharpens K0776/K0778 P(w) <= 2*ceil(w/2))",
      corollaryNewQ: { 21: [22], 23: [24], 25: [26] },
      realizability: "all 8 distinct candidate row sets (w=19,20): A=0 impossible (rigorous); standard-form realizations excluded for R' = A + e^2/16 <= 2e7 with e in Z complete (K0778 covered e = 0 mod 4 only)",
    };
  }
  return out;
}
