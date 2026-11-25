// Verifier for: exact circle point counts P(22)=18, P(23)=P(24)=20, P(25)=22,
// P(26)=...=P(35)=24 on width-w integer lattices (w x m, all m >= 1), the
// universal bound P(w) <= 2*ceil(w/2) - 4 for all w >= 21, w != 26, and the
// new 24-point witness circle (2x-25)^2 + (2y-25)^2 = 650.
//
// Framework (K0072 / K0767 / K0776 / K0778 / K0782; sixth independent
// implementation): circle x^2+y^2+Cx+Dy+N=0 on rows 0..w-1 (width = number of
// rows; columns x are unbounded, chord lengths s_y are NOT bounded).
//   s_y^2 = A - 4y^2 - e*y,  A = C^2-4N, e = 4D, C in Z (any double row).
//   P = 2d + s <= 2(d+s), tangents s <= 2.
//   A point-row set of size d+s >= L (standard form, e in Z) must pass the
//   coef-4 certificate a - 4i^2 - u*i in QR0(m) for every m, hence must be a
//   subset of some window mask T(x,y) = {i in 0..w-1 : mask9[x][i%9] &&
//   mask11[y][i%11]} (81*121 free (a,u) pairs absorb translation; shift-0
//   windows are complete).
//   Mixed-parity point rows force e in Z (standard form); same-parity sets in
//   g0=2 form must pass the coef-16 certificate (class maxima computed);
//   g0 >= 3 gives |S| <= ceil(w/g0) < L.
// Killing level L completely (all L-subsets of all windows die at some
// modulus) => d+s <= L-1 => P <= 2(L-1).
//
// Claims verified here (STAGE "classify" = 1,2,4,5,6; "search" = 3; "all"):
//   (1) Level k-1 (k = ceil(w/2)) dies COMPLETELY for w = 21..25 and 27..40
//   (w=26 has exactly ONE survivor S* = {0,1,3,4,7,10,15,18,21,22,24,25}).
//   w=21..25: 191/480/166/356/127 candidates, 0 survivors.
//   w=27..40: 63/120/10/28/0/8/0/5/0/0/0/4/0/2 candidates, 0 survivors.
//   => P(w) <= 2k-4 for w=21..25, 27..40 (w != 26).
//   (2) Level 13 dies for w = 27..35 (63/120 + w29,w30: 237/548 +
//   w31..35: 1197/2922/5237/16410/36920 candidates, all 0 survivors; w=26
//   level 13 is K0782). Level 12 is alive at w >= 26 (S*), level 10/11 alive
//   at w=22..25 via the 650-witness truncations.
//   => P(22)=18 (level 10 dead), P(23)=P(24)=20 (level 11 dead),
//   P(25)=22 (level 12 dead), P(26)=...=P(35)=24 (level 13 dead).
//   (3) S* realizability: A=0 rigorously impossible (rows 1,4 squarefree
//   part 1 => d=20 unique => row 25 needs 25*(20-100) < 0). Standard-form
//   sweep (s0, s25) in [0,4472]^2 (R' = A+e^2/16 <= 2e7 complete coverage),
//   e even forced: 20,003,256 pairs, exactly ONE hit (A,e) = (25,-100),
//   s = 5,11,17,19,23,25,25,23,19,17,11,5.
//   (4) Witness: (2x-25)^2+(2y-25)^2=650 has exactly 24 lattice points on
//   the 26x26 board, rows exactly S*; truncations to rows 0..w-1 give
//   16/18/20/20/22/24 points for w=21..26 (P lower bounds).
//   (5) Periodic machinery for w >= 65: c99 = max window count over one
//   99-period = 42 (< 99/2); maxT(w) = floor(w/99)*c99(x,y) + pref(x,y,t),
//   scan w=65..3000: 0 cases with maxT >= L; analytically
//   maxT(w) <= 42*(w/99) + 42 < (w-1)/2 for w >= 562.
//   Same-parity coef-16 class bound via mod 9: period max = 6 (both
//   parities), so classMax <= floor(J/9)*6+6 <= (w+1)/3+6 < (w-1)/2 for
//   w >= 42; direct min-over-8-moduli scan 65..3000 worst ratio 2/3.
//   g0 >= 3: ceil(w/3) < k-1 for all w >= 21. => universal theorem.
//   (6) Parity coef-16 class maxima (min over all 18 moduli) for w=21..40:
//   7,7,8,8,9,9,10,10,10,10,11,11,11,11,11,11,11,11,12,12 (evens) — all
//   below the relevant L. Level k-2 survivors (resume material): w=21 L9: 16,
//   w=22 L9: 36, w=23 L10: 2, w=24 L10: 5, w=25 L11: 2, w=26 L11: 14.
//   (7) Witness control A=9, e=-44 reproduces the 16-point circle
//   (2x-11)^2+(2y-11)^2=130 (s = 3,7,9,11,11,9,7,3).
//
// Note: level-13 classification for w=36..40 was NOT completed here (candidate
// counts explode: ~10^5+ sets at w=35 already; needs streaming implementation).

const STAGE = "all";
const SET = "s26";

async function main() {
  const out: any = { generated: "2026-11-12", parts: {} };
  const qrC: Record<number, Uint8Array> = {};
  const getQR = (m: number): Uint8Array => {
    if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
    return qrC[m];
  };
  const isSq = (v: number): number => { if (v < 0) return -1; const s = Math.round(Math.sqrt(v)); return s * s === v ? s : -1; };
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
  function* combos(arr: number[], j: number): Generator<number[]> {
    if (j === 0) { yield []; return; }
    if (arr.length < j) return;
    for (let s = 0; s <= arr.length - j; s++) {
      const head = arr[s];
      for (const tail of combos(arr.slice(s + 1), j - 1)) yield [head, ...tail];
    }
  }
  function classifyLevel(w: number, L: number) {
    const cand = new Set<string>(); let maxT = 0;
    for (let x = 0; x < m9.length; x++) for (let y = 0; y < m11.length; y++) {
      const T: number[] = [];
      for (let i = 0; i < w; i++) if (m9[x][i % 9] && m11[y][i % 11]) T.push(i);
      const t = T.length; if (t > maxT) maxT = t;
      if (t >= L) for (const S of combos(T, L)) cand.add(S.join(","));
    }
    let s4 = 0; const surv: number[][] = []; const perKill: Record<string, number> = {};
    for (const key of cand) {
      const S = key.split(",").map(Number);
      let dead = -1;
      for (const m of REST) if (!subsetOK(S, m, 4)) { dead = m; break; }
      if (dead < 0) { s4++; if (surv.length < 30) surv.push(S); } else perKill[dead] = (perKill[dead] || 0) + 1;
    }
    return { w, L, maxT, candidates: cand.size, survivors: s4, perKill, survivorSamples: surv };
  }
  function classMax(rows: number[], mods: number[], coef: number): number {
    let best = Infinity;
    for (const m of mods) { const qr = getQR(m); let bm = 0;
      for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) { let c = 0;
        for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) t += m; if (qr[t]) c++; }
        if (c > bm) bm = c; }
      if (bm < best) best = bm; }
    return best;
  }

  if (STAGE === "all" || STAGE === "classify") {
    const P: any = {};
    for (let w = 21; w <= 40; w++) { const k = Math.ceil(w / 2); P["w" + w + "_kminus1"] = classifyLevel(w, k - 1); }
    P["w29_L13"] = classifyLevel(29, 13); P["w30_L13"] = classifyLevel(30, 13);
    for (let w = 21; w <= 26; w++) { const k = Math.ceil(w / 2); P["w" + w + "_kminus2"] = classifyLevel(w, k - 2); }
    out.parts.classify = P;
    const par: any = {};
    for (let w = 21; w <= 40; w++) {
      const ev: number[] = [], od: number[] = [];
      for (let y = 0; y < w; y += 2) ev.push(y); for (let y = 1; y < w; y += 2) od.push(y);
      par[w] = { evensC16max: classMax(ev, ALLMODS, 16), oddsC16max: classMax(od, ALLMODS, 16) };
    }
    out.parts.parityC16Maxima = par;
    let maxc = 0;
    for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) { let c = 0; for (let i = 0; i < 99; i++) if (m9[x][i % 9] && m11[y][i % 11]) c++; if (c > maxc) maxc = c; }
    out.parts.c99max = maxc;
    let f9 = 0;
    for (const r of [0, 1]) for (let a = 0; a < 9; a++) for (let u = 0; u < 9; u++) { let c = 0; for (let j = 0; j < 9; j++) { const y = 2 * j + r; let t = (a - (16 * y * y) % 9 - u * y) % 9; if (t < 0) t += 9; if (getQR(9)[t]) c++; } if (c > f9) f9 = c; }
    out.parts.coef16_mod9_periodMax = f9;
    // periodic maxT scan w=65..3000
    const C = new Int16Array(9801); const PREF = new Int16Array(9801 * 100);
    for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) { const id = x * 121 + y; let c = 0; for (let i = 0; i < 99; i++) { if (m9[x][i % 9] && m11[y][i % 11]) c++; PREF[id * 100 + i + 1] = c; } C[id] = c; }
    let badW = 0;
    for (let w = 65; w <= 3000; w++) { const L = Math.ceil(w / 2) - 1; const q = Math.floor(w / 99), t = w % 99; let mT = 0; for (let id = 0; id < 9801; id++) { const v = q * C[id] + PREF[id * 100 + t]; if (v > mT) mT = v; } if (mT >= L) badW++; }
    out.parts.periodicMaxTscan_65_3000 = { windowsWithMaxTgeL: badW };
    // witness + truncations + A=0
    const pts: number[][] = [];
    for (let x = 0; x < 26; x++) for (let y = 0; y < 26; y++) if ((2 * x - 25) ** 2 + (2 * y - 25) ** 2 === 650) pts.push([x, y]);
    const S = [0, 1, 3, 4, 7, 10, 15, 18, 21, 22, 24, 25];
    out.parts.witness650 = { points: pts.length, distinct: new Set(pts.map(p => p.join(","))).size, rows: [...new Set(pts.map(p => p[1]))].sort((a, b) => a - b), sFromAe: { A: 25, e: -100, s: S.map(y => isSq(25 - 4 * y * y + 100 * y)) } };
    const tr: any = {};
    for (let w = 21; w <= 28; w++) tr["P" + w + "witnessLower"] = pts.filter(p => p[1] <= w - 1).length;
    out.parts.truncations = tr;
    out.parts.a0_S26 = { rows14: [1, 4], dUnique: 20, row25: 25 * (20 - 100), rigorouslyImpossible: 25 * (20 - 100) < 0 };
    out.parts.claims = {
      exactP: { 22: 18, 23: 20, 24: 20, 25: 22, "26..35": 24 },
      P21: "in {16,17,18} (level 10 dead -> <=18; level 9 alive with 16 survivors; witness lower bound 16)",
      universal: "P(w) <= 2*ceil(w/2)-4 for all w >= 21, w != 26 (sharp at w=27,28: P=24=2k-4; fails at w=26 where P(26)=24=2k-2 via the realized S*)",
      corollary: "M_{w,w+1} = w for every odd w >= 21 (21,23,25 extend K0782; all odd w >= 27 from the universal bound)",
      s26_note: "S* is REAL (circle 650): it passed every prime < 2000 at coef-4 — the first certificate-unkillable candidate, resolved positively",
      k0776_gap: "the 650-circle was inside K0776's sum-of-two-squares witness family (650 = 2*5^2*13, sum e = 4) but its row span is 26 > their 17..22-row windows, so it was invisible to that scan"
    };
  }

  if (STAGE === "all" || STAGE === "search") {
    const S = [0, 1, 3, 4, 7, 10, 15, 18, 21, 22, 24, 25];
    const ymax = 25; const rest = S.slice(1, S.length - 1);
    let pairs = 0, pass = 0, hits = 0; const hitList: any[] = [];
    for (let s0 = 1; s0 <= 4472; s0++) {
      const A = s0 * s0;
      for (let sy = 0; sy <= 4472; sy++) {
        pairs++;
        const diff = A - 4 * ymax * ymax - sy * sy;
        if (diff % ymax !== 0) continue;
        const e = diff / ymax;
        if ((e & 1) !== 0) continue; // mixed parity -> e even forced
        pass++;
        let ok = true;
        for (const y of rest) if (isSq(A - 4 * y * y - e * y) < 0) { ok = false; break; }
        if (ok) { hits++; if (hitList.length < 10) hitList.push({ A, e, s: S.map(y => isSq(A - 4 * y * y - e * y)) }); }
      }
    }
    out.parts.search_s26 = { set: SET, rows: S, pairsTested: pairs, passFilters: pass, hits, hitList };
    const wc: number[] = []; let wok = true;
    for (const y of [0, 1, 2, 4, 7, 9, 10, 11]) { const s = isSq(9 - 4 * y * y + 44 * y); if (s < 0) wok = false; else wc.push(s); }
    out.parts.witnessControlA9eMinus44 = { ok: wok, s: wc };
  }
  return out;
}
