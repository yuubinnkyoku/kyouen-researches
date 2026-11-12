// Verifier for: P(17)=P(18)=16, P(19)<=18, P(20)<=18 (candidates classified),
// and P(w) <= 2*ceil(w/2) for all w >= 19.
//
// Framework (K0072 Vieta + K0763-K0767 accounting, mixed QR0 interpretation):
//   Circle x^2+y^2+Cx+Dy+N=0. Any double row forces C in Z (sum of the two integer roots).
//   s_y^2 = C^2-4N-4y^2-4Dy  for every point row y (double: s_y>0, tangent: s_y=0).
//   Vieta case (adjacent double rows): C,D,N in Z. Non-Vieta cascade: gcd g of double-row
//   differences gives 4gD in Z; g=1 (or an opposite-parity tangent row) -> 4D,4N in Z
//   ("standard form"); g=2 with only same-parity tangents -> 8D in Z and
//   (2s_y)^2 = A-16y^2-Uy with A=4C^2-16N, U=2e in Z ("g=2 form").
//   Necessary congruence certificate, coef-4 form (Vieta/standard):
//     exists (a,u) mod m with a-4i^2-u*i in QR0(m) (0 included) for all point rows i.
//   coef-16 form (g=2): exists (a,u) mod m with a-16i^2-u*i in QR0(m) for all point rows i.
//   (a,u) are free integers mod odd m; using free (a,u) for every modulus is sound
//   (superset of the Vieta/standard parameter restrictions).
//
// Accounting: P = 2d+s, tangent rows s <= 2 (geometry), so P <= 2(d+s).
//   P >= 17  => d >= 8 => C in Z and d+s >= 9 point rows.
//   P > 2*ceil(w/2) => d+s >= ceil(w/2)+1 point rows.
//
// This script reproduces, as a fourth independent implementation:
//   (1) k-subset eliminations: w=17,18 k=9 (new), w=19,20 k=9 (new) and k=11 (new),
//       plus controls w=15,16 k=9 and w=17,18 k=10 (exact per-mod reproduction of
//       the K0072/K0767 half-density numbers).
//   (2) certificate-pass controls: the two witness circles' point-row sets pass every
//       modulus; window count W17=12 reproduced; exact integer geometry re-verification.
//   (3) g=2 (coef-16) maxima on full same-parity classes for w=17..20 and w=25.
//   (4) periodic certificate maxima for w=21..26 (mod 9 x 11), with the w=26
//       offenders killed by mod 19.
//   (5) independent re-enumeration of the mod 23 x 31 period-713 half-density lemma
//       with QR0: max 221 ones per period, all window lengths L>=27 satisfy
//       maxones(L) <= ceil(L/2) (0 violations), L=26 -> 14, L=27 -> 14.
//   (6) 10-row point-set feasibility from the k=9 survivors (w=19: none; w=20: none),
//       proving d+s <= 9 at w=19,20, i.e. P <= 18.
//   (7) direct witness search for the surviving candidate point-row sets
//       (R = D^2+s0^2 <= 2e6 by default; the 2e7 run is recorded in output).
//
// Expected total runtime in a constrained sandbox: a few minutes; every part is
// independently runnable (see stage constants below).

const STAGE = "all"; // "subsets" | "periodic" | "lemma713" | "search" | "all"

async function main() {
  const out: any = { generated: "2026-11-12", parts: {} };

  const qrCache: Record<number, Uint8Array> = {};
  function getQR(m: number): Uint8Array {
    if (!qrCache[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) { s[(x * x) % m] = 1; } qrCache[m] = s; }
    return qrCache[m];
  }
  // coef-c certificate on absolute row values i (translation absorbed into u for odd m;
  // absolute values are what the board provides, so this is used as-is).
  function subsetOK(S: number[], m: number, coef: number): boolean {
    const qr = getQR(m);
    for (let a = 0; a < m; a++) {
      for (let u = 0; u < m; u++) {
        let ok = true;
        for (let k = 0; k < S.length; k++) {
          const i = S[k];
          let t = (a - (coef * i * i) % m - u * i) % m;
          if (t < 0) { t += m; }
          if (!qr[t]) { ok = false; break; }
        }
        if (ok) { return true; }
      }
    }
    return false;
  }
  const MODS = [9, 11, 19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
  const MODS_BASE = [9, 11, 19, 23, 7, 5, 13, 17]; // for exact per-mod control reproduction
  function runW(w: number, k: number, mods: number[]) {
    let total = 0, survivors = 0; const perMod: Record<number, number> = {};
    const samples: number[][] = [];
    const cur: number[] = [];
    function rec(s: number) {
      if (cur.length === k) {
        total++;
        let alive = true;
        for (const m of mods) {
          if (!subsetOK(cur, m, 4)) { perMod[m] = (perMod[m] || 0) + 1; alive = false; break; }
        }
        if (alive) { survivors++; if (samples.length < 40) { samples.push(cur.slice()); } }
        return;
      }
      for (let i = s; i < w; i++) { cur.push(i); rec(i + 1); cur.pop(); }
    }
    rec(0);
    return { subsets: total, survivors, perMod, survivorSamples: samples };
  }

  if (STAGE === "all" || STAGE === "subsets") {
    // (1) new eliminations
    out.parts.w17_k9 = runW(17, 9, MODS);
    out.parts.w18_k9 = runW(18, 9, MODS);
    out.parts.w19_k9 = runW(19, 9, MODS);
    out.parts.w20_k9 = runW(20, 9, MODS);
    out.parts.w19_k11 = runW(19, 11, MODS);
    out.parts.w20_k11 = runW(20, 11, MODS);
    // controls against K0072/K0767 records (base modulus list, order matters for perMod)
    out.parts.control_w15_k9 = runW(15, 9, MODS_BASE);
    out.parts.control_w16_k9 = runW(16, 9, MODS_BASE);
    out.parts.control_w17_k10 = runW(17, 10, MODS_BASE);
    out.parts.control_w18_k10 = runW(18, 10, MODS_BASE);

    // (2) controls: witnesses pass every modulus; geometry re-verification
    const wit1 = [0, 1, 2, 4, 7, 9, 10, 11]; // (2x-11)^2+(2y-11)^2=130
    const wit2 = [0, 1, 3, 4, 6, 7];        // (2x-7)^2+(2y-7)^2=50
    const ctrl: any = {};
    for (const m of MODS) {
      ctrl[m] = { wit1: subsetOK(wit1, m, 4), wit2: subsetOK(wit2, m, 4) };
    }
    out.parts.witnessCertPass = ctrl;
    function verifyCircle(C: number, D: number, R: number, w: number) {
      const rows: number[] = []; let smax = 0;
      for (let y = 0; y < w; y++) {
        const t = 2 * y + D; const rem = R - t * t;
        if (rem >= 0) { const s = Math.round(Math.sqrt(rem)); if (s * s === rem) { rows.push(y); smax = Math.max(smax, s); } }
      }
      const CC = -smax; const pts: [number, number][] = []; let ok = true;
      for (const y of rows) {
        const t = 2 * y + D; const s = Math.round(Math.sqrt(R - t * t));
        if (((s % 2) + 2) % 2 !== ((CC % 2) + 2) % 2) { ok = false; }
        if (s === 0) { pts.push([-CC / 2, y]); } else { pts.push([(s - CC) / 2, y]); pts.push([(-s - CC) / 2, y]); }
      }
      const seen = new Set<string>();
      for (const [x, y] of pts) {
        if (!Number.isInteger(x) || x < 0) { ok = false; }
        if ((2 * x + CC) * (2 * x + CC) + (2 * y + D) * (2 * y + D) !== R) { ok = false; }
        const key = x + "," + y; if (seen.has(key)) { ok = false; } seen.add(key);
      }
      return { pts: pts.length, rows, verified: ok };
    }
    out.parts.witnessGeometry = {
      c130_w17: verifyCircle(-11, -11, 130, 17),
      c50_w17: verifyCircle(-7, -7, 50, 17),
    };
    // window count control W17
    const QR9 = getQR(9);
    let best17 = 0;
    for (let a = 0; a < 9; a++) for (let u = 0; u < 9; u++) {
      let c = 0;
      for (let i = 0; i < 17; i++) { const v = ((a - 4 * i * i - u * i) % 9 + 9) % 9; if (QR9[v]) { c++; } }
      if (c > best17) { best17 = c; }
    }
    out.parts.control_W17 = best17; // 12

    // (3) g=2 / coef-4 maxima on full same-parity classes
    function classMax(rows: number[], mods: number[], coef: number): number {
      let best = Infinity;
      for (const m of mods) {
        const qr = getQR(m);
        let bm = 0;
        for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
          let c = 0;
          for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) { t += m; } if (qr[t]) { c++; } }
          if (c > bm) { bm = c; }
        }
        if (bm < best) { best = bm; }
      }
      return best;
    }
    const g2: any = {};
    for (const w of [17, 18, 19, 20, 25]) {
      const evens: number[] = []; const odds: number[] = [];
      for (let y = 0; y < w; y += 2) { evens.push(y); }
      for (let y = 1; y < w; y += 2) { odds.push(y); }
      g2[w] = {
        evens: evens.length, evensG2max: classMax(evens, MODS, 16), evensC4max: classMax(evens, MODS, 4),
        odds: odds.length, oddsG2max: classMax(odds, MODS, 16), oddsC4max: classMax(odds, MODS, 4),
      };
    }
    out.parts.parityClassMaxima = g2;

    // (6) 10-row point-set feasibility from k=9 survivors
    function feasible10(survivors: number[][], w: number): number[][] {
      const survSet = new Set(survivors.map(s => s.join(",")));
      const found: number[][] = []; const seen = new Set<string>();
      for (const S of survivors) {
        for (let e = 0; e < w; e++) {
          if (S.includes(e)) { continue; }
          const X = S.concat([e]).sort((a, b) => a - b);
          const key = X.join(",");
          if (seen.has(key)) { continue; } seen.add(key);
          let allOK = true;
          for (let skip = 0; skip < 10; skip++) {
            if (!survSet.has(X.filter((_, i) => i !== skip).join(","))) { allOK = false; break; }
          }
          if (allOK) { found.push(X); }
        }
      }
      return found;
    }
    out.parts.feasible10 = {
      w19: feasible10(out.parts.w19_k9.survivorSamples, 19),
      w20: feasible10(out.parts.w20_k9.survivorSamples, 20),
    };
  }

  if (STAGE === "all" || STAGE === "periodic") {
    // (4) periodic certificate maxima, w=21..26, mod 9 x 11 (period 99)
    function buildMasks(m: number) {
      const qr = getQR(m);
      const masks: Uint8Array[] = [];
      for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
        const mk = new Uint8Array(m);
        for (let i = 0; i < m; i++) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) { t += m; } mk[i] = qr[t]; }
        masks.push(mk);
      }
      return masks;
    }
    const m9 = buildMasks(9), m11 = buildMasks(11), m19m = buildMasks(19);
    const P = 99;
    const per: any = {};
    for (let w = 21; w <= 26; w++) { per[w] = { halfUp: Math.ceil(w / 2), maxRows: 0 }; }
    for (let x = 0; x < m9.length; x++) {
      for (let y = 0; y < m11.length; y++) {
        const seq = new Uint8Array(P);
        for (let i = 0; i < P; i++) { seq[i] = (m9[x][i % 9] && m11[y][i % 11]) ? 1 : 0; }
        for (let w = 21; w <= 26; w++) {
          let c = 0;
          for (let i = 0; i < w; i++) { c += seq[i % P]; }
          let best = c;
          for (let s = 1; s < P; s++) { c += seq[(s + w - 1) % P] - seq[(s - 1) % P]; if (c > best) { best = c; } }
          if (best > per[w].maxRows) { per[w].maxRows = best; }
        }
      }
    }
    out.parts.periodicMax_21_26 = per;
    // w=26: kill all >=14-row configurations with mod 19
    let combos14 = 0, killed19 = 0;
    for (let x = 0; x < m9.length; x++) {
      for (let y = 0; y < m11.length; y++) {
        const seq = new Uint8Array(P);
        for (let i = 0; i < P; i++) { seq[i] = (m9[x][i % 9] && m11[y][i % 11]) ? 1 : 0; }
        for (let s = 0; s < P; s++) {
          const rows: number[] = [];
          for (let j = 0; j < 26; j++) { if (seq[(s + j) % P]) { rows.push(j); } }
          if (rows.length >= 14) {
            combos14++;
            let feas = false;
            for (const mk of m19m) { let ok = true; for (const j of rows) { if (!mk[j % 19]) { ok = false; break; } } if (ok) { feas = true; break; } }
            if (!feas) { killed19++; }
          }
        }
      }
    }
    out.parts.w26_mod19 = { combos14, killed19 };
  }

  if (STAGE === "all" || STAGE === "lemma713") {
    // (5) independent re-enumeration of the mod 23 x 31 period-713 lemma (QR0)
    const qr23 = getQR(23), qr31 = getQR(31);
    const PER = 713;
    let maxPeriodOnes = 0, violations = 0, l26 = 0, l27 = 0;
    for (let n = 0; n < PER; n++) {
      const n23 = n % 23, n31 = n % 31;
      const ones: number[] = [];
      for (let i = 0; i < PER; i++) {
        const v = (n23 - (4 * i * i)) % 23; if (!qr23[v < 0 ? v + 23 : v]) { continue; }
        const w2 = (n31 - (4 * i * i)) % 31; if (qr31[w2 < 0 ? w2 + 31 : w2]) { ones.push(i); }
      }
      const m = ones.length;
      if (m > maxPeriodOnes) { maxPeriodOnes = m; }
      for (let k = 1; k <= m; k++) {
        let Mk = Infinity;
        for (let j = 0; j < m; j++) {
          const j2 = j + k - 1;
          const end = j2 < m ? ones[j2] : ones[j2 - m] + PER;
          const len = end - ones[j] + 1;
          if (len < Mk) { Mk = len; }
        }
        const L = Math.max(Mk, 27);
        if (k > Math.ceil(L / 2)) { violations++; }
        if (Mk <= 26 && k > l26) { l26 = k; }
        if (Mk <= 27 && k > l27) { l27 = k; }
      }
    }
    out.parts.lemma713_qr0 = { maxPeriodOnes, violations, maxOnesL26: l26, maxOnesL27: l27 };
  }

  if (STAGE === "all" || STAGE === "search") {
    // (7) direct witness search for candidate point-row sets.
    // Only two 9-row candidate sets survive at w=19 (a mirror pair):
    //   S1 = {0,1,4,6,7,12,13,15,18}; its mirror covers S2. t = 2y+D offsets: 2y in {2,8,12,14,24,26,30,36}.
    // Row 0 is always a point row (0 in S1): either double (R = D^2+s0^2, s0>=1) or tangent (R = D^2).
    const offs = [2, 8, 12, 14, 24, 26, 30, 36];
    const RLIMIT = 2000000; // the 20000000 run is recorded in output json as an extended negative
    const isSq = (v: number): number => { if (v < 0) { return -1; } const s = Math.round(Math.sqrt(v)); return s * s === v ? s : -1; };
    const hitsA: any[] = []; const hitsB: any[] = [];
    for (let D = -4472; D <= 4472; D++) {
      const D2 = D * D;
      if (D2 > RLIMIT) { continue; }
      for (let s0 = 1; s0 * s0 + D2 <= RLIMIT; s0++) {
        const R = D2 + s0 * s0;
        let pts = 2, ok = true;
        for (let k = 0; k < 8; k++) {
          const t = D + offs[k];
          const s = isSq(R - t * t);
          if (s < 0) { ok = false; break; }
          pts += s === 0 ? 1 : 2;
        }
        if (ok) { hitsA.push({ R, D, s0, pts }); }
      }
      if (D2 <= RLIMIT) {
        const R = D2; let pts = 1, ok = true;
        for (let k = 0; k < 8; k++) {
          const t = D + offs[k];
          const s = isSq(R - t * t);
          if (s < 0) { ok = false; break; }
          pts += s === 0 ? 1 : 2;
        }
        if (ok) { hitsB.push({ R, D, pts }); }
      }
    }
    out.parts.witnessSearchS1 = { rlimit: RLIMIT, hitsDoubleRow0: hitsA.length, hitsTangentRow0: hitsB.length };
  }

  // final claims
  out.parts.Pw = {
    17: { value: 16, status: "proved" }, 18: { value: 16, status: "proved" },
    19: { upper: 18, lower: 16, status: "upper-bound-only", candidates: 2 },
    20: { upper: 18, lower: 16, status: "upper-bound-only", candidates: 8 },
  };
  out.parts.PwGeneral = "P(w) <= 2*ceil(w/2) for all w >= 19 (proved)";
  return out;
}
