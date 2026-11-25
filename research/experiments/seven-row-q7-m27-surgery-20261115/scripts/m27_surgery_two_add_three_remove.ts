// (7,7) 7x27 frontier surgery — (|A|=2, |R|=3) complete enumeration machine (2026-11-15).
// Pure TypeScript, deterministic, no I/O. Run in 5 parts via PART (1..5): the flat R-index range
// [lo, hi) = [0,2132), [2132,4264), [4264,6396), [6396,8528), [8528,10660) covers all C(41,3) = 10,660 R.
// (The consolidated 2026-11-15 run used parts [0,4264), [4264,8528), [8528,10660) — same partition of the
//  flat index, identical deterministic results.)
//
// Space: S' = S - R + A, R any 3 seed stones, A any 2 seed-empty cells (A subset of E — re-adding a
//  removed stone is a smaller edit, already enumerated by the two-edit machine), |R| >= |A| automatic,
//  row deficiency automatic (40 < 42 stones => some row <= 5).
// Blocking lemma (proved for |A| <= 2, see ../README.md): T=(26,3) can only be covered via the line y=3
//  (no 4-stone T-curves; k <= 3 T-curves reach at most 5 with 2 additions). With r3_on = |R intersect row3|
//  stones: line eff = 5 - r3_on, needs a_on >= 6 - eff:
//   - r3_on >= 2: needs a_on >= 3 > 2 -> IMPOSSIBLE -> R rejected (370 R).
//   - r3_on = 1: line eff 4, needs a_on = 2 -> BOTH additions on the line (A = 2 line cells, forced).
//     Every u in Ux (non-row-3 uncovered cells) must then be covered by an eff5 circle through u with a
//     line-empty on it, or an eff4 circle through u with >= 2 line-empties — exact iff per-u wholesale.
//     All 3,150 R have an uncoverable u -> rejected (direct-verified 23/23).
//   - r3_on = 0: A = {s in lineSet, z in E} (>= 1 line cell). U3 (row-3 uncovered cells incl. T) are all
//     covered by the line (5+1=6). Ux coverage: u covered iff z on an eff5 curve through u, or s on an
//     eff5 curve through u, or both s,z on an eff4 curve through u (eff6 excluded by u in U; eff <= 3
//     cannot reach 6 with 2 additions). Exact per-u option sets:
//       Z5(u)  = seed-empty cells on eff5 curves through u (z-side),
//       Lin5(u)= line cells on eff5 curves through u (s-side),
//       eff4 aug: line cells on eff4 curves containing z (pair-side).
//     HardU = {u in Ux: Lin5(u) empty and no eff4 through u} -> z in Z5(u) \u {u} (+ self-cover only if
//     u in E; a removed cell with empty Z5(u) is uncoverable -> R rejected). zcand = intersection over
//     HardU — sound superset-free lower bound on valid z. For each z in zcand passing okZ (safety:
//     z on an eff6 curve would make 7), scand = intersection over Need(z) of (Lin5(u) \u aug) — the
//     exact set of s making the pair cover Ux. Safety for |A| = 2 is EXACTLY {okZ each, no shared
//     eff >= 5 curve} (violation needs (6,1) or (5,2) on a seed curve; curves with <= 3 seed stones cap
//     at 5). Survivors brute-verified (safe + maximal + row-deficient).
// Formal candidate count: 10,660 R x (C(22,2) + 22x136) = 10,660 x 3,203 = 34,103,980 pairs.
// Canonical result (2026-11-15): 0 witnesses. Rejections: 370 r3>=2 + 115 wholesale + 3,150 r3=1
//  line-coverage + 4,320 zcand-empty (R-level) + 14,948 z-level okZ + 55,638 z-level coverage
//  (scand-empty). pairsChecked = 0 (no pair survived coverage).
// Targeted direct controls: coverage 36/36, z-okZ 30/30, r3=1 line-coverage 23/23 (independent
//  fresh-enumeration checks on explicit S' = S - R + {s, z}; see CTL section at the bottom).
// Verification lesson recorded in the log: an earlier CTL helper had (a) lines stored as [a,b,c,0]
//  feeding the circle evaluator (missing 7-stone LINE counts — caught by targeted triage: circle-flagged
//  samples agreed, line-flagged samples all mismatched) and (b) coverage checks that admitted removed
//  cells as additions; both were CTL-side defects, the machine held. CTL helpers need their own triage.

type P = [number, number];
const W = 7, M = 27, Q = 7;
const seed: P[] = [[2,0],[7,0],[12,0],[14,0],[18,0],[19,0],[6,1],[10,1],[11,1],[15,1],[16,1],[20,1],[1,2],[8,2],[13,2],[14,2],[17,2],[24,2],[0,3],[2,3],[3,3],[23,3],[25,3],[4,4],[9,4],[11,4],[15,4],[16,4],[20,4],[7,5],[8,5],[17,5],[18,5],[19,5],[23,5],[5,6],[9,6],[10,6],[16,6],[17,6],[21,6]];
const T: P = [26, 3];
const PART = 1; // 1..5
const RANGES: [number, number][] = [[0,2132],[2132,4264],[4264,6396],[6396,8528],[8528,10660]];

const gcd = (a: number, b: number): number => b ? gcd(b, a % b) : Math.abs(a);
const det3 = (m: number[][]) => m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);
function circle(p1: P, p2: P, p3: P): number[] | null {
  const [x1,y1]=p1,[x2,y2]=p2,[x3,y3]=p3;
  if ((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1) === 0) return null;
  const r1=x1*x1+y1*y1, r2=x2*x2+y2*y2, r3=x3*x3+y3*y3;
  let A = det3([[x1,y1,1],[x2,y2,1],[x3,y3,1]]);
  let B = -det3([[r1,y1,1],[r2,y2,1],[r3,y3,1]]);
  let C = det3([[r1,x1,1],[r2,x2,1],[r3,x3,1]]);
  let D = -det3([[r1,x1,y1],[r2,x2,y2],[r3,x3,y3]]);
  const g = gcd(gcd(gcd(Math.abs(A),Math.abs(B)),Math.abs(C)),Math.abs(D)) || 1;
  A/=g; B/=g; C/=g; D/=g;
  if (A < 0) { A=-A; B=-B; C=-C; D=-D; }
  return [A,B,C,D];
}
function line(p1: P, p2: P): number[] {
  let a = p2[1]-p1[1], b = p1[0]-p2[0], c = p2[0]*p1[1]-p1[0]*p2[1];
  const g = gcd(gcd(Math.abs(a),Math.abs(b)),Math.abs(c)) || 1;
  a/=g; b/=g; c/=g;
  if (a < 0 || (a === 0 && b < 0)) { a=-a; b=-b; c=-c; }
  return [a,b,c];
}
type Curve = {kind: string, a: number[], cnt: number, stIdx: number[], board: number[], empt: number[]};
const onC = (c: Curve, x: number, y: number) => c.kind === "line" ? c.a[0]*x+c.a[1]*y+c.a[2] === 0 : c.a[0]*(x*x+y*y)+c.a[1]*x+c.a[2]*y+c.a[3] === 0;
const n = seed.length;
const stoneKey = new Set(seed.map(p => p[0]*100 + p[1]));
const cells: P[] = [];
const cellIdx = new Map<number, number>();
for (let y = 0; y < W; y++) for (let x = 0; x < M; x++) { cellIdx.set(x*100+y, cells.length); cells.push([x,y]); }
const cmap = new Map<string, Curve>();
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) { const l = line(seed[i], seed[j]); const k = "L"+l.join(","); if (!cmap.has(k)) cmap.set(k, {kind:"line", a:l, cnt:0, stIdx:[], board:[], empt:[]}); }
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k2 = j+1; k2 < n; k2++) { const c = circle(seed[i], seed[j], seed[k2]); if (!c) continue; const k = "C"+c.join(","); if (!cmap.has(k)) cmap.set(k, {kind:"circle", a:c, cnt:0, stIdx:[], board:[], empt:[]}); }
const bigCurves: Curve[] = [];
for (const c of cmap.values()) {
  for (let si = 0; si < n; si++) if (onC(c, seed[si][0], seed[si][1])) c.stIdx.push(si);
  c.cnt = c.stIdx.length;
  if (c.cnt < 4) continue;
  for (let i = 0; i < cells.length; i++) { const cl = cells[i]; if (onC(c, cl[0], cl[1])) { c.board.push(i); if (!stoneKey.has(cl[0]*100+cl[1])) c.empt.push(i); } }
  bigCurves.push(c);
}
const E: P[] = cells.filter(c => !stoneKey.has(c[0]*100+c[1]));
const EidxList = E.map(p => cellIdx.get(p[0]*100+p[1])!);
const Eset = new Set<number>(EidxList);
const lineArr = [cellIdx.get(T[0]*100+T[1])!, ...E.filter(c => c[1] === 3 && !(c[0]===T[0]&&c[1]===T[1])).map(p => cellIdx.get(p[0]*100+p[1])!)];
const lineSet = new Set<number>(lineArr);
const c6through: number[][] = cells.map(() => []);
for (let ci = 0; ci < bigCurves.length; ci++) if (bigCurves[ci].cnt === 6) for (const b of bigCurves[ci].board) c6through[b].push(ci);
const zBig: number[][] = cells.map(() => []);
for (let ci = 0; ci < bigCurves.length; ci++) for (const b of bigCurves[ci].board) zBig[b].push(ci);
const row3stones = new Set<number>();
for (let i = 0; i < n; i++) if (seed[i][1] === 3) row3stones.add(i);
const NC = bigCurves.length;
const effArr = new Int8Array(NC);
const stIdxSorted = bigCurves.map(c => c.stIdx);
const allR: number[][] = [];
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) allR.push([i, j, k]);

function bruteMaxCurve(stones: P[]): number {
  const m = stones.length;
  const cm = new Map<string, number[]>();
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const l = line(stones[i], stones[j]); const k = "L"+l.join(","); if (!cm.has(k)) cm.set(k, [0].concat(l)); }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) for (let k2 = j+1; k2 < m; k2++) { const c = circle(stones[i], stones[j], stones[k2]); if (!c) continue; const k = "C"+c.join(","); if (!cm.has(k)) cm.set(k, c); }
  let mx = 0;
  for (const a of cm.values()) { let cc = 0; for (const p of stones) if (a[0]*(p[0]*p[0]+p[1]*p[1])+a[1]*p[0]+a[2]*p[1]+a[3] === 0) cc++; if (cc > mx) mx = cc; }
  return mx;
}
function directCoveredU(u: P, S2: P[]): boolean {
  const m = S2.length;
  for (let i = 0; i < m; i++) { const l = line(u, S2[i]); let cc = 0; for (const p of S2) if (l[0]*p[0]+l[1]*p[1]+l[2] === 0) cc++; if (cc >= 6) return true; }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const c = circle(u, S2[i], S2[j]); if (!c) continue; let cc = 0; for (const p of S2) if (c[0]*(p[0]*p[0]+p[1]*p[1])+c[1]*p[0]+c[2]*p[1]+c[3] === 0) cc++; if (cc >= 6) return true; }
  return false;
}
const onArr = (a: number[], x: number, y: number) => a.length === 3 ? a[0]*x+a[1]*y+a[2] === 0 : a[0]*(x*x+y*y)+a[1]*x+a[2]*y+a[3] === 0;
function directCoverableR1(u: P, SR: P[]): boolean {
  const m = SR.length;
  const SRset = new Set(SR.map(p => p[0]*100+p[1]));
  const testCov = (a: number[]): boolean => {
    if (!onArr(a, u[0], u[1])) return false;
    let st = 0, lineE = 0;
    for (const p of SR) if (onArr(a, p[0], p[1])) st++;
    for (let ci2 = 0; ci2 < cells.length; ci2++) { const cl = cells[ci2]; if (SRset.has(cl[0]*100+cl[1])) continue; if (!onArr(a, cl[0], cl[1])) continue; if (lineSet.has(ci2)) lineE++; }
    return st + Math.min(2, lineE) >= 6;
  };
  for (let i = 0; i < m; i++) { const l = line(u, SR[i]); if (testCov(l)) return true; }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const c = circle(u, SR[i], SR[j]); if (c && testCov(c)) return true; }
  return false;
}

async function main() {
  const [PART_LO, PART_HI] = RANGES[PART - 1];
  let rejR3ge2 = 0, rejWh = 0, rejWhHard = 0, rejLineCov = 0, r1pass = 0, rejZcandEmpty = 0;
  let rejScandEmpty = 0, rejSafZ = 0, rejSafS = 0, rejSafShared = 0, pairsChecked = 0, survivors = 0, bruted = 0;
  const witnesses: any[] = [];
  const ctlCovS: {R: number[], z: number, u: number}[] = []; let ctlCovTaken = 0, ctlCovAgree = 0, covSmp = 0;
  const ctlSafS: {R: number[], s: number, z: number}[] = []; let ctlSafTaken = 0, ctlSafAgree = 0, safSmp = 0;
  const ctlZokS: {R: number[], z: number}[] = []; let ctlZokTaken = 0, ctlZokAgree = 0, zsmp = 0;
  const ctlLineS: {R: number[], u: number}[] = []; let ctlLineTaken = 0, ctlLineAgree = 0, lineSmp = 0;
  const isUx = new Uint8Array(cells.length);
  for (let ri = PART_LO; ri < PART_HI && ri < allR.length; ri++) {
    const R = allR[ri];
    let r3 = 0; for (const si of R) if (row3stones.has(si)) r3++;
    if (r3 >= 2) { rejR3ge2++; continue; }
    const Rset = new Set<number>(R);
    for (let ci = 0; ci < NC; ci++) { let r = 0; const st = stIdxSorted[ci]; for (let t = 0; t < st.length; t++) if (Rset.has(st[t])) r++; effArr[ci] = bigCurves[ci].cnt - r; }
    const Rcells = new Set<number>(R.map(si => cellIdx.get(seed[si][0]*100+seed[si][1])!));
    const U: number[] = [];
    for (let ci = 0; ci < cells.length; ci++) {
      const cl = cells[ci]; const key = cl[0]*100+cl[1];
      if (stoneKey.has(key) && !Rcells.has(ci)) continue;
      let cov = false;
      for (const c6 of c6through[ci]) if (effArr[c6] === 6) { cov = true; break; }
      if (!cov) U.push(ci);
    }
    const Ux: number[] = U.filter(u => cells[u][1] !== 3);
    isUx.fill(0); for (const u of Ux) isUx[u] = 1;
    if (r3 === 1) {
      const lineMark = new Set<number>();
      for (let ci = 0; ci < NC; ci++) {
        if (effArr[ci] === 5) { const c = bigCurves[ci]; let hl = false; for (const b of c.empt) if (lineSet.has(b)) { hl = true; break; } if (!hl) continue; for (const b of c.board) if (isUx[b]) lineMark.add(b); }
        else if (effArr[ci] === 4) { const c = bigCurves[ci]; let lc = 0; for (const b of c.empt) if (lineSet.has(b)) { lc++; if (lc >= 2) break; } if (lc < 2) continue; for (const b of c.board) if (isUx[b]) lineMark.add(b); }
      }
      let failU = -1;
      for (const u of Ux) if (!lineMark.has(u)) { failU = u; break; }
      if (failU >= 0) { rejLineCov++; lineSmp++; if (ctlLineS.length < 12 && lineSmp % 127 === 0) ctlLineS.push({R, u: failU}); continue; }
      r1pass++;
      continue;
    }
    const covMark = new Set<number>();
    for (let ci = 0; ci < NC; ci++) {
      const c = bigCurves[ci];
      if (effArr[ci] === 5) {
        if (c.empt.length === 0) continue;
        if (c.empt.length >= 2) { for (const b of c.board) if (isUx[b]) covMark.add(b); }
        else { const e0 = c.empt[0]; for (const b of c.board) if (isUx[b] && b !== e0) covMark.add(b); }
      } else if (effArr[ci] === 4) {
        if (c.empt.length <= 1) continue;
        if (c.empt.length >= 3) { for (const b of c.board) if (isUx[b]) covMark.add(b); }
        else { const e0 = c.empt[0], e1 = c.empt[1]; for (const b of c.board) if (isUx[b] && b !== e0 && b !== e1) covMark.add(b); }
      }
    }
    let kE = 0, rej = false;
    for (const u of Ux) if (!covMark.has(u)) { if (!Eset.has(u)) { rej = true; break; } kE++; }
    if (rej || kE > 2) { rejWh++; continue; }
    const Z5u = new Map<number, Set<number>>();
    const Lin5u = new Map<number, Set<number>>();
    const has4u = new Set<number>();
    const eff4info: {ucells: number[], lineE: number[]}[] = [];
    const zToEff4 = new Map<number, number[]>();
    for (let ci = 0; ci < NC; ci++) {
      const c = bigCurves[ci];
      if (effArr[ci] === 5) {
        if (c.empt.length === 0) continue;
        let anyLine = false; for (const b of c.empt) if (lineSet.has(b)) { anyLine = true; break; }
        for (const b of c.board) {
          if (!isUx[b]) continue;
          let zs = Z5u.get(b); if (!zs) { zs = new Set(); Z5u.set(b, zs); }
          for (const e of c.empt) if (e !== b) zs.add(e);
          if (anyLine) { let ls = Lin5u.get(b); if (!ls) { ls = new Set(); Lin5u.set(b, ls); } for (const e of c.empt) if (lineSet.has(e)) ls.add(e); }
        }
      } else if (effArr[ci] === 4) {
        const uc: number[] = []; for (const b of c.board) if (isUx[b]) uc.push(b);
        if (uc.length === 0) continue;
        const lineE: number[] = []; for (const b of c.empt) if (lineSet.has(b)) lineE.push(b);
        eff4info.push({ucells: uc, lineE});
        const idx = eff4info.length - 1;
        for (const b of c.empt) { let l = zToEff4.get(b); if (!l) { l = []; zToEff4.set(b, l); } l.push(idx); }
        for (const b of uc) has4u.add(b);
      }
    }
    let zcand: Set<number> | null = null;
    let hardRej = false;
    for (const u of Ux) {
      if (!Lin5u.has(u) && !has4u.has(u)) {
        const zs = new Set<number>(Z5u.get(u) ?? []);
        if (Eset.has(u)) zs.add(u);
        else if (zs.size === 0) { hardRej = true; break; }
        if (zcand === null) zcand = zs;
        else { const nx = new Set<number>(); for (const z of zcand) if (zs.has(z)) nx.add(z); zcand = nx; }
        if (zcand.size === 0) break;
      }
    }
    if (hardRej) { rejWhHard++; continue; }
    if (zcand !== null && zcand.size === 0) { rejZcandEmpty++; continue; }
    if (zcand === null) zcand = new Set<number>(EidxList);
    const okZcache = new Map<number, boolean>();
    const okZ = (cell: number): boolean => { let v = okZcache.get(cell); if (v !== undefined) return v; v = true; for (const ci of c6through[cell]) if (effArr[ci] === 6) { v = false; break; } okZcache.set(cell, v); return v; };
    for (const z of zcand) {
      if (!okZ(z)) { rejSafZ++; zsmp++; if (ctlZokS.length < 10 && zsmp % 173 === 0) ctlZokS.push({R, z}); continue; }
      const aug = new Map<number, Set<number>>();
      const e4s = zToEff4.get(z);
      if (e4s) for (const e4i of e4s) { const info = eff4info[e4i]; for (const u of info.ucells) { let s2 = aug.get(u); if (!s2) { s2 = new Set(); aug.set(u, s2); } for (const lc of info.lineE) s2.add(lc); } }
      let scand: Set<number> | null = null;
      let failU = -1;
      for (const u of Ux) {
        if (u === z) continue;
        const zs = Z5u.get(u);
        if (zs && zs.has(z)) continue;
        let sOpts: Set<number> | null = Lin5u.get(u) ?? null;
        const a = aug.get(u);
        if (sOpts === null && a) sOpts = new Set(a);
        else if (sOpts !== null && a) { sOpts = new Set(sOpts); for (const s2 of a) sOpts.add(s2); }
        if (sOpts === null || sOpts.size === 0) { failU = u; break; }
        if (scand === null) scand = sOpts;
        else { const nx = new Set<number>(); for (const s of scand) if (sOpts.has(s)) nx.add(s); scand = nx; }
        if (scand.size === 0) { failU = u; break; }
      }
      if (failU >= 0 || scand === null || scand.size === 0) {
        rejScandEmpty++;
        covSmp++;
        if (ctlCovS.length < 12 && failU >= 0 && covSmp % 211 === 0) ctlCovS.push({R, z, u: failU});
        continue;
      }
      for (const s of scand) {
        if (s === z) continue;
        pairsChecked++;
        if (!okZ(s)) { rejSafS++; safSmp++; if (ctlSafS.length < 8 && safSmp % 53 === 0) ctlSafS.push({R, s, z}); continue; }
        let shared = false;
        for (const ci of zBig[s]) { if (effArr[ci] < 5) continue; const c = bigCurves[ci]; let zOn = false; for (const b of c.board) if (b === z) { zOn = true; break; } if (zOn) { shared = true; break; } }
        if (shared) { rejSafShared++; safSmp++; if (ctlSafS.length < 8 && safSmp % 53 === 0) ctlSafS.push({R, s, z}); continue; }
        survivors++;
        if (bruted < 3) {
          bruted++;
          const Sp = seed.filter((p, si) => !Rset.has(si));
          const S2 = Sp.concat([cells[s], cells[z]]) as P[];
          const mx = bruteMaxCurve(S2);
          let unc = 0;
          for (const cl of cells) { if (S2.some(p => p[0]===cl[0]&&p[1]===cl[1])) continue; if (directCoveredU(cl, S2)) continue; unc++; }
          const rows = [0,0,0,0,0,0,0]; for (const p of S2) rows[p[1]]++;
          if (unc === 0 && mx < Q && Math.min(...rows) <= Q-2) witnesses.push({R, s: cells[s], z: cells[z], rows});
        }
      }
    }
  }
  for (const smp of ctlCovS) {
    const SR = seed.filter((p, si) => !smp.R.includes(si));
    let allBad = true;
    for (const s of lineArr) { if (s === smp.z) continue; const S2 = SR.concat([cells[s], cells[smp.z]]) as P[]; if (directCoveredU(cells[smp.u], S2)) { allBad = false; break; } }
    ctlCovTaken++;
    if (allBad) ctlCovAgree++;
  }
  for (const smp of ctlSafS) { const SR = seed.filter((p, si) => !smp.R.includes(si)); const S2 = SR.concat([cells[smp.s], cells[smp.z]]) as P[]; ctlSafTaken++; if (bruteMaxCurve(S2) >= Q) ctlSafAgree++; }
  for (const smp of ctlZokS) { const SR = seed.filter((p, si) => !smp.R.includes(si)); const S2 = SR.concat([cells[smp.z]]) as P[]; ctlZokTaken++; if (bruteMaxCurve(S2) >= Q) ctlZokAgree++; }
  for (const smp of ctlLineS) { const SR = seed.filter((p, si) => !smp.R.includes(si)); ctlLineTaken++; if (!directCoverableR1(cells[smp.u], SR)) ctlLineAgree++; }
  return {part: PART, range: [PART_LO, PART_HI], rejR3ge2, rejWh, rejWhHard, rejLineCov, r1pass, rejZcandEmpty, rejScandEmpty, rejSafZ, rejSafS, rejSafShared, pairsChecked, survivors, witnesses,
    ctl: {cov: ctlCovAgree + "/" + ctlCovTaken, saf: ctlSafAgree + "/" + ctlSafTaken, zok: ctlZokAgree + "/" + ctlZokTaken, line: ctlLineAgree + "/" + ctlLineTaken}};
}
main();
