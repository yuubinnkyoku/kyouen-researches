// (7,7) 7x27 frontier surgery — (3,3) general space, blocking-structure case-split machine (2026-11-15).
// Pure TypeScript, deterministic. Run: node --experimental-strip-types m33_machine.ts <mode> [sub] [chunk]
//   chunk = "lo:hi" (R-index range, default all) for resumable background runs.
// Modes: facts | L3 | L3ctl | G | C
// Progress goes to stderr (one line per 50 R), results JSON to stdout at the end.
//
// Space: S' = S - R + A, |R| = |A| = 3, A subset of E (seed-empty cells; re-adding a removed stone
//  is a smaller edit, already enumerated by the (1,3) machine), R any 3 seed stones. S' has 41
//  stones on 7 rows of 27 => some row <= 5 = q-2: row deficiency automatic (41 < 42).
//
// T-satisfaction (T = (26,3), the only seed-uncovered cell in 7x27), exhaustive modes for |A| = 3:
//  (a) T in A (T is a stone);
//  (b) line y=3 blocks T (line stones 5 - r3_on + a_on = 6 exactly: cover >= 6, safety <= 6);
//  (c) a k=3 T-curve c blocks T (|C intersect R| = 0, all 3 additions on c: 3 + 3 = 6).
//  Curves through T with k >= 4 do not exist (k4 = 0, k5 = line only, k6+ would cover T in the
//  seed), k <= 2 reach at most 2 + 3 = 5 < 6 — so (a),(b),(c) are exhaustive (facts mode asserts).
//
// COMPLETE, DISJOINT A-structure partition (a_on = |A intersect lineE|):
//  L3   : r3_on=2, a_on=3 — A = 3 lineE cells (360 R x C(22,3) = 554,400).        [memo cat.I]
//  L2f1 : r3_on=1, a_on=2 — A = 2 lineE + 1 free (later).                          [memo cat.I]
//  L1f2 : r3_on=0, a_on=1 — A = 1 lineE + 2 free (later).                          [memo cat.I]
//  G1..G6: T in A, a_on <= r3_on (line < 6, T a stone). NOT covered by memo I/II:
//    G1 = r3_on=1,a_on=1: A={T,x,y} | G2 = r3_on=2,a_on=1: A={T,x,y} | G3 = r3_on=2,a_on=2: A={T,t,x}
//    G4 = r3_on=3,a_on=1: A={T,x,y} | G5 = r3_on=3,a_on=2: A={T,t,x} | G6 = r3_on=3,a_on=3: A={T,t1,t2}
//  C0 : T not in A, a_on=0, A subset of empt(c)\line for a k=3 T-curve c, R cap c = 0. [memo cat.II]
//  C1 : T not in A, a_on=1, A = {t'} + 2 cells of empt(c)\line, r3_on >= 1 (r3_on=0 is L1f2).
//  T not in A with a_on <= r3_on and A not inside any admissible empt(c) => T uncovered => no witness.
// Disjointness: G has T in A; L has a_on = 1+r3_on > a_on(G); C has T not in A and a_on <= 1 <= r3_on.
//
// Coverage (exact, |A|=3): u in U covered iff u in A or some census curve gamma with
//  eff(gamma) + |A cap empt(gamma)| >= 6 (eff5 + >=1, eff4 + >=2, eff3 + all 3).
// Safety (exact): no eff6 curve through any addition, no pair on a common eff5, no triple on a
//  common eff4. Census = ALL seed curves with >= 3 stones (k3..k6; seed max = 6).
// Per-slice A-space filtering keeps per-(R,u) option structures small; structures are built lazily
//  in hard-first u order, so rejected R's pay for only 1-3 u's.

type P = [number, number];
const W = 7, M = 27, Q = 7;
const seed: P[] = [[2,0],[7,0],[12,0],[14,0],[18,0],[19,0],[6,1],[10,1],[11,1],[15,1],[16,1],[20,1],[1,2],[8,2],[13,2],[14,2],[17,2],[24,2],[0,3],[2,3],[3,3],[23,3],[25,3],[4,4],[9,4],[11,4],[15,4],[16,4],[20,4],[7,5],[8,5],[17,5],[18,5],[19,5],[23,5],[5,6],[9,6],[10,6],[16,6],[17,6],[21,6]];
const T: P = [26, 3];
const MODE = process.argv[2] ?? "facts";
const SUB = process.argv[3] ?? "";
const CHUNK = process.argv[4] ?? "";
const prog = (s: string) => process.stderr.write(s + "\n");

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
type Curve = { kind: "line" | "circle", a: number[], st: number[], board: number[], empt: number[] };
const onA = (a: number[], x: number, y: number) => a.length === 3 ? a[0]*x+a[1]*y+a[2] === 0 : a[0]*(x*x+y*y)+a[1]*x+a[2]*y+a[3] === 0;

const n = seed.length;
const cells: P[] = [];
for (let y = 0; y < W; y++) for (let x = 0; x < M; x++) cells.push([x, y]);
const NC7 = cells.length; // 189
const cellOf = new Map<number, number>();
for (let i = 0; i < NC7; i++) cellOf.set(cells[i][0]*100+cells[i][1], i);
const stoneCell = seed.map(p => cellOf.get(p[0]*100+p[1])!);
const seedSet = new Set<number>(stoneCell);

const cmap = new Map<string, Curve>();
const putIf = (kind: "line"|"circle", a: number[]) => { const k = (kind === "line" ? "L" : "C") + a.join(","); if (!cmap.has(k)) cmap.set(k, { kind, a, st: [], board: [], empt: [] }); };
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) putIf("line", line(seed[i], seed[j]));
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k2 = j+1; k2 < n; k2++) { const c = circle(seed[i], seed[j], seed[k2]); if (c) putIf("circle", c); }
const curves: Curve[] = [];
for (const c of cmap.values()) {
  for (let si = 0; si < n; si++) if (onA(c.a, seed[si][0], seed[si][1])) c.st.push(si);
  if (c.st.length < 3) continue;
  for (let i = 0; i < NC7; i++) if (onA(c.a, cells[i][0], cells[i][1])) c.board.push(i);
  c.empt = c.board.filter(b => !seedSet.has(b));
  curves.push(c);
}
const NCZ = curves.length;
const curvesThruCell: number[][] = cells.map(() => []);
for (let ci = 0; ci < NCZ; ci++) for (const b of curves[ci].board) curvesThruCell[b].push(ci);
const curvesThruStone: number[][] = seed.map(() => []);
for (let ci = 0; ci < NCZ; ci++) for (const s of curves[ci].st) curvesThruStone[s].push(ci);

const E: number[] = [];
for (let i = 0; i < NC7; i++) if (!seedSet.has(i)) E.push(i);
const eIdx = new Map<number, number>();
E.forEach((c, i) => eIdx.set(c, i));
const NE = E.length; // 148
const lineE: number[] = E.filter(c => cells[c][1] === 3);
const lineESet = new Set<number>(lineE);
const NL = lineE.length; // 22
const tCell = cellOf.get(T[0]*100+T[1])!;
const freeE = E.filter(c => cells[c][1] !== 3);
const row3stones: number[] = [];
for (let si = 0; si < n; si++) if (seed[si][1] === 3) row3stones.push(si);

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
  for (let i = 0; i < m; i++) { if (S2[i][0]===u[0]&&S2[i][1]===u[1]) continue; const l = line(u, S2[i]); let cc = 0; for (const p of S2) if (l[0]*p[0]+l[1]*p[1]+l[2] === 0) cc++; if (cc >= 6) return true; }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { if (S2[i][0]===u[0]&&S2[i][1]===u[1]) continue; if (S2[j][0]===u[0]&&S2[j][1]===u[1]) continue; const c = circle(u, S2[i], S2[j]); if (!c) continue; let cc = 0; for (const p of S2) if (c[0]*(p[0]*p[0]+p[1]*p[1])+c[1]*p[0]+c[2]*p[1]+c[3] === 0) cc++; if (cc >= 6) return true; }
  return false;
}
function S2of(R: number[], A: number[]): P[] {
  const Rset = new Set<number>(R);
  const S2 = seed.filter((_, si) => !Rset.has(si)).map(p => p.slice() as P);
  for (const a of A) S2.push(cells[E[a]].slice() as P);
  return S2;
}
function bruteWitness(R: number[], A: number[]): { witness: boolean, mx: number, unc: number, minRow: number } {
  const S2 = S2of(R, A);
  const mx = bruteMaxCurve(S2);
  let unc = 0;
  for (let i = 0; i < NC7; i++) { if (S2.some(p => p[0]===cells[i][0]&&p[1]===cells[i][1])) continue; if (!directCoveredU(cells[i], S2)) unc++; }
  const rows = [0,0,0,0,0,0,0]; for (const p of S2) rows[p[1]]++;
  return { witness: unc === 0 && mx < Q && Math.min(...rows) <= Q-2, mx, unc, minRow: Math.min(...rows) };
}

// ---- facts ----
if (MODE === "facts") {
  const kOf = (c: Curve) => c.st.length;
  const tCurves = curves.filter(c => c.board.includes(tCell));
  const byK: Record<number, number> = {};
  for (const c of tCurves) byK[kOf(c)] = (byK[kOf(c)] ?? 0) + 1;
  const lineCurve = curves.find(c => c.kind === "line" && c.a[0] === 0 && c.a[1] === 1 && c.a[2] === -3)!;
  let seedUnc = 0; for (let i = 0; i < NC7; i++) { if (seedSet.has(i)) continue; if (!directCoveredU(cells[i], seed.map(p=>p.slice() as P))) seedUnc++; }
  const seedMax = bruteMaxCurve(seed.map(p=>p.slice() as P));
  const kHist: Record<number, number> = {}; for (const c of curves) kHist[kOf(c)] = (kHist[kOf(c)] ?? 0) + 1;
  const facts = { censusCurves: NCZ, k3T: byK[3] ?? 0, k4T: byK[4] ?? 0, k5T: byK[5] ?? 0, k6T: byK[6] ?? 0,
    k5TisLineOnly: tCurves.filter(c => kOf(c) === 5).every(c => c.kind === "line"),
    lineK: kOf(lineCurve), lineEmpt: lineCurve.empt.length, row3Stones: row3stones.length, E: NE, lineE: NL, freeE: freeE.length,
    seedMaxCurve: seedMax, seedUncovered: seedUnc, seedUncoveredIsT: seedUnc === 1 && !directCoveredU(T, seed.map(p=>p.slice() as P)), kHist };
  console.log(JSON.stringify(facts));
  if (facts.k3T !== 22) throw new Error("k3T != 22");
  if (facts.k4T !== 0) throw new Error("k4T != 0");
  if (facts.k5T !== 1 || !facts.k5TisLineOnly) throw new Error("k5 through T must be the line only");
  if (facts.k6T !== 0) throw new Error("k6T != 0");
  if (facts.lineK !== 5) throw new Error("line k != 5");
  if (facts.row3Stones !== 5 || facts.E !== 148 || facts.lineE !== 22) throw new Error("geometry mismatch");
  if (facts.seedMaxCurve !== 6) throw new Error("seed max curve != 6");
  if (!facts.seedUncoveredIsT) throw new Error("seed uncovered is not exactly T");
  console.log("FACTS_OK");
}

// ---- shared machinery ----
function rCombos(filter: (r: number[]) => boolean): number[][] {
  const out: number[][] = [];
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) { const r = [i,j,k]; if (filter(r)) out.push(r); }
  return out;
}
const applyChunk = (Rs: number[][]): number[][] => { if (!CHUNK) return Rs; const [lo, hi] = CHUNK.split(":").map(Number); return Rs.slice(lo, hi); };
const cnt3on = (r: number[]) => r.filter(s => seed[s][1] === 3).length;
interface RState { R: number[]; r3: number; eff: Int16Array; cov6: Uint8Array; U: number[]; Uhard: number[]; s5pairs: Set<number>; s4triples: Set<number>; }
const pairKey = (a: number, b: number) => { const x = Math.min(a,b), y = Math.max(a,b); return x*NE + y; };
const tripKey = (a: number, b: number, c2: number) => { const s = [a,b,c2].sort((x,y)=>x-y); return (s[0]*NE+s[1])*NE+s[2]; };
const staticDiff: number[] = cells.map((_, i) => curvesThruCell[i].length);
function buildRState(R: number[]): RState {
  const r3 = cnt3on(R);
  const rmark = new Int16Array(NCZ);
  for (const s of R) for (const ci of curvesThruStone[s]) rmark[ci]++;
  const eff = new Int16Array(NCZ);
  const cov6 = new Uint8Array(NC7);
  for (let ci = 0; ci < NCZ; ci++) { const c = curves[ci]; eff[ci] = c.st.length - rmark[ci]; if (eff[ci] >= 6) for (const b of c.board) cov6[b] = 1; }
  const Rcell = new Set<number>(R.map(s => stoneCell[s]));
  const U: number[] = [];
  for (let i = 0; i < NC7; i++) { if (seedSet.has(i) && !Rcell.has(i)) continue; if (!cov6[i]) U.push(i); }
  const Uhard = U.slice().sort((a, b) => staticDiff[a] - staticDiff[b]);
  const s5pairs = new Set<number>();
  const s4triples = new Set<number>();
  for (let ci = 0; ci < NCZ; ci++) {
    const c = curves[ci];
    if (eff[ci] === 5) { const es = c.empt.map(e => eIdx.get(e)!); for (let i = 0; i < es.length; i++) for (let j = i+1; j < es.length; j++) s5pairs.add(pairKey(es[i], es[j])); }
    else if (eff[ci] === 4) { const es = c.empt.map(e => eIdx.get(e)!); for (let i = 0; i < es.length; i++) for (let j = i+1; j < es.length; j++) for (let k = j+1; k < es.length; k++) s4triples.add(tripKey(es[i], es[j], es[k])); }
  }
  return { R, r3, eff, cov6, U, Uhard, s5pairs, s4triples };
}
interface ASpace { allowed: Set<number>; pairOK: (a: number, b: number) => boolean; tripleOK: (a: number, b: number, c2: number) => boolean; }
interface UStruct { cov5: Set<number>; pairs: Set<number>; triples: Set<number>; empty: boolean; }
function buildUStruct(st: RState, u: number, sp: ASpace): UStruct {
  const cov5 = new Set<number>(); const pairs = new Set<number>(); const triples = new Set<number>();
  for (const ci of curvesThruCell[u]) {
    const ef = st.eff[ci];
    if (ef < 3 || ef > 5) continue;
    const es = curves[ci].empt.map(e => eIdx.get(e)!).filter(e => sp.allowed.has(e));
    if (ef === 5) { for (const e of es) cov5.add(e); }
    else if (ef === 4) { for (let i = 0; i < es.length; i++) for (let j = i+1; j < es.length; j++) if (sp.pairOK(es[i], es[j])) pairs.add(pairKey(es[i], es[j])); }
    else { for (let i = 0; i < es.length; i++) for (let j = i+1; j < es.length; j++) for (let k = j+1; k < es.length; k++) if (sp.tripleOK(es[i], es[j], es[k])) triples.add(tripKey(es[i], es[j], es[k])); }
  }
  return { cov5, pairs, triples, empty: cov5.size === 0 && pairs.size === 0 && triples.size === 0 };
}
function coversA(us: UStruct, A: number[]): boolean {
  if (us.cov5.has(A[0]) || us.cov5.has(A[1]) || us.cov5.has(A[2])) return true;
  if (us.pairs.has(pairKey(A[0], A[1])) || us.pairs.has(pairKey(A[0], A[2])) || us.pairs.has(pairKey(A[1], A[2]))) return true;
  if (us.triples.has(tripKey(A[0], A[1], A[2]))) return true;
  return false;
}
function safeA(st: RState, A: number[]): 0 | 1 | 2 | 3 {
  for (const a of A) if (st.cov6[E[a]]) return 1;
  if (st.s5pairs.has(pairKey(A[0], A[1])) || st.s5pairs.has(pairKey(A[0], A[2])) || st.s5pairs.has(pairKey(A[1], A[2]))) return 2;
  if (st.s4triples.has(tripKey(A[0], A[1], A[2]))) return 3;
  return 0;
}
interface SliceResult { rejR: number; rejA_cov: number; rejA_saf: number; survivors: number; witnesses: any[]; pairsChecked: number;
  ctl: { covAgree: number, covTaken: number, safAgree: number, safTaken: number } }
function runSlice(Rs: number[][], enumA: (st: RState) => number[][], spFor: () => ASpace, uFilter: (u: number) => boolean, structAssert?: (us: UStruct, u: number) => void): SliceResult {
  const res: SliceResult = { rejR: 0, rejA_cov: 0, rejA_saf: 0, survivors: 0, witnesses: [], pairsChecked: 0,
    ctl: { covAgree: 0, covTaken: 0, safAgree: 0, safTaken: 0 } };
  let covSmp = 0, safSmp = 0;
  Rs.forEach((R, ri) => {
    if (ri % 50 === 0) prog(`R ${ri}/${Rs.length}`);
    const st = buildRState(R);
    const sp = spFor();
    const Us = st.Uhard.filter(uFilter);
    const usCache = new Map<number, UStruct>();
    const getUS = (u: number): UStruct => { let us = usCache.get(u); if (!us) { us = buildUStruct(st, u, sp); if (structAssert) structAssert(us, u); usCache.set(u, us); } return us; };
    let rej = false;
    for (const u of Us) { if (sp.allowed.has(eIdx.get(u)!)) continue; if (getUS(u).empty) { rej = true; break; } }
    if (rej) { res.rejR++; return; }
    const As = enumA(st);
    for (const A of As) {
      res.pairsChecked++;
      const saf = safeA(st, A);
      if (saf !== 0) { res.rejA_saf++; safSmp++; if (res.ctl.safTaken < 10 && safSmp % 211 === 0) { res.ctl.safTaken++; const bw = bruteWitness(R, A); res.ctl.safAgree += bw.mx >= Q ? 1 : 0; } continue; }
      let bad = -1;
      for (const u of Us) { const ea = eIdx.get(u); if (ea !== undefined && (A[0] === ea || A[1] === ea || A[2] === ea)) continue; const us = getUS(u); if (!coversA(us, A)) { bad = u; break; } }
      if (bad >= 0) { res.rejA_cov++; covSmp++; if (res.ctl.covTaken < 12 && covSmp % 173 === 0) { res.ctl.covTaken++; res.ctl.covAgree += directCoveredU(cells[bad], S2of(R, A)) ? 0 : 1; } continue; }
      res.survivors++;
      const bw = bruteWitness(R, A);
      res.witnesses.push({ R, A: A.map(a => cells[E[a]]), brute: bw, witness: bw.witness });
    }
  });
  return res;
}

// ---- L3 ----
if (MODE === "L3") {
  const Rs = applyChunk(rCombos(r => cnt3on(r) === 2));
  const lineEidx = lineE.map(c => eIdx.get(c)!);
  const allowedSet = new Set<number>(lineEidx);
  const sp: ASpace = { allowed: allowedSet, pairOK: () => true, tripleOK: () => true };
  const enumA = () => { const out: number[][] = []; for (let i = 0; i < NL; i++) for (let j = i+1; j < NL; j++) for (let k = j+1; k < NL; k++) out.push([lineEidx[i], lineEidx[j], lineEidx[k]]); return out; };
  const r = runSlice(Rs, enumA, () => sp, (u) => cells[u][1] !== 3);
  let geoOK = true, geoDetail = "";
  const RsAll = rCombos(x => cnt3on(x) === 2);
  for (let ri = 0; ri < RsAll.length; ri += 23) {
    const st = buildRState(RsAll[ri]);
    for (const u of st.U) { if (cells[u][1] === 3) continue; const us = buildUStruct(st, u, sp); if (us.triples.size > 0) { geoOK = false; geoDetail = `R=${RsAll[ri]} u=${u}`; break; } }
    if (!geoOK) break;
  }
  console.log(JSON.stringify({ mode: "L3", nR: Rs.length, ...r, L3_geometry_m3_empty_on_Ux: geoOK, geoDetail }));
}

// ---- L3ctl: second independent implementation of the L3 wholesale rejection ----
if (MODE === "L3ctl") {
  const NS = Number(SUB || 8);
  const Rs = rCombos(r => cnt3on(r) === 2);
  const lineEidxSet = new Set<number>(lineE);
  const freshCoverable = (u: number, SR: P[]): boolean => {
    const m = SR.length;
    const SRset = new Set<number>(SR.map(p => p[0]*100+p[1]));
    const test = (a: number[]): boolean => {
      if (!onA(a, u[0], u[1])) return false;
      let st = 0, lineEmpty = 0;
      for (const p of SR) if (onA(a, p[0], p[1])) st++;
      for (let x = 0; x < M; x++) { const key = x*100+3; if (SRset.has(key)) continue; if (!onA(a, x, 3)) continue; if (lineEidxSet.has(cellOf.get(key)!)) lineEmpty++; }
      if (st === 5 && lineEmpty >= 1) return true;
      if (st === 4 && lineEmpty >= 2) return true;
      if (st === 3 && lineEmpty >= 3) return true;
      return false;
    };
    for (let i = 0; i < m; i++) { const l = line(u, SR[i]); if (test(l)) return true; }
    for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const c = circle(u, SR[i], SR[j]); if (c && test(c)) return true; }
    return false;
  };
  let agree = 0, disagree = 0, killerConfirmed = 0, killerFailed = 0;
  const killers: any[] = [];
  for (const R of Rs) {
    const st = buildRState(R);
    const Rset = new Set<number>(R);
    const SR = seed.filter((_, si) => !Rset.has(si)).map(p => p.slice() as P);
    const machineUx = st.Uhard.filter(u => cells[u][1] !== 3);
    let freshKiller = -1;
    for (const u of machineUx) { if (!freshCoverable(cells[u], SR)) { freshKiller = u; break; } }
    const machineRej = (() => { const sp = { allowed: new Set<number>(lineE.map(c => eIdx.get(c)!)), pairOK: () => true, tripleOK: () => true } as ASpace; for (const u of st.Uhard) { if (cells[u][1] === 3) continue; if (buildUStruct(st, u, sp).empty) return u; } return -1; })();
    if ((freshKiller >= 0) === (machineRej >= 0)) agree++; else disagree++;
    if (freshKiller >= 0 && machineRej >= 0) { if (!freshCoverable(cells[machineRej], SR)) killerConfirmed++; else { killerFailed++; killers.push({ R, freshKiller, machineRej }); } }
  }
  let uSampleOK = 0;
  for (let i = 0; i < Rs.length; i += Math.max(1, Math.floor(Rs.length / NS))) {
    const R = Rs[i]; const st = buildRState(R); const Rset = new Set<number>(R);
    const SR = seed.filter((_, si) => !Rset.has(si)).map(p => p.slice() as P);
    const freshU = new Set<number>();
    const SRkeys = new Set<number>(SR.map(p => p[0]*100+p[1]));
    for (let c2 = 0; c2 < NC7; c2++) { if (SRkeys.has(cells[c2][0]*100+cells[c2][1])) continue; if (!directCoveredU(cells[c2], SR)) freshU.add(c2); }
    const machineU = new Set<number>(st.U);
    if (freshU.size === machineU.size && [...freshU].every(x => machineU.has(x))) uSampleOK++;
    else throw new Error("full U-set mismatch R=" + JSON.stringify(R));
  }
  console.log(JSON.stringify({ mode: "L3ctl", nR: Rs.length, verdictAgree: agree, disagree, killerConfirmed, killerFailed, uSampleOK, badKillers: killers }));
}

// ---- G ----
if (MODE === "G") {
  const sub = SUB || "all";
  const tIdx = eIdx.get(tCell)!;
  const lineEidxNoT = lineE.filter(c => c !== tCell).map(c => eIdx.get(c)!);
  const freeIdx = freeE.map(c => eIdx.get(c)!);
  const mkSp = (): ASpace => ({ allowed: new Set<number>([tIdx, ...lineEidxNoT, ...freeIdx]), pairOK: () => true, tripleOK: () => true });
  const out: any = {};
  const runG = (name: string, r3: number[], kind: 0 | 1 | 2) => {
    const Rs = applyChunk(rCombos(r => cnt3on(r) === r3[0]));
    const enumA = (): number[][] => {
      const outA: number[][] = [];
      if (kind === 0) { for (let i = 0; i < freeIdx.length; i++) for (let j = i+1; j < freeIdx.length; j++) outA.push([tIdx, freeIdx[i], freeIdx[j]].sort((a,b)=>a-b)); }
      else if (kind === 1) { for (const t of lineEidxNoT) for (const x of freeIdx) outA.push([tIdx, t, x].sort((a,b)=>a-b)); }
      else { for (let i = 0; i < lineEidxNoT.length; i++) for (let j = i+1; j < lineEidxNoT.length; j++) outA.push([tIdx, lineEidxNoT[i], lineEidxNoT[j]].sort((a,b)=>a-b)); }
      return outA;
    };
    const r = runSlice(Rs, enumA, mkSp, () => true);
    out[name] = { nR: Rs.length, ...r };
  };
  if (sub === "all" || sub === "r3x3") { runG("G6", [3], 2); runG("G5", [3], 1); runG("G4", [3], 0); }
  if (sub === "all" || sub === "r3x2") { runG("G3", [2], 1); runG("G2", [2], 0); }
  if (sub === "all" || sub === "r3x1") { runG("G1", [1], 0); }
  console.log(JSON.stringify(out));
}

// ---- C ----
if (MODE === "C") {
  const sub = SUB || "all";
  const k3T = curves.filter(c => c.st.length === 3 && c.board.includes(tCell));
  const out: any = { nK3T: k3T.length };
  const runC = (name: string, aOn1: boolean) => {
    let rejR = 0, rejA_cov = 0, rejA_saf = 0, survivors = 0, pairsChecked = 0, cRpairs = 0, nCs = 0;
    const witnesses: any[] = [];
    const ctl = { covAgree: 0, covTaken: 0, safAgree: 0, safTaken: 0 };
    let covSmp = 0, safSmp = 0;
    for (let ci = 0; ci < k3T.length; ci++) {
      const c = k3T[ci];
      const cStones = new Set<number>(c.st);
      const tPrime = c.empt.find(e => lineESet.has(e) && e !== tCell);
      if (aOn1 && tPrime === undefined) continue;
      const aCells = c.empt.filter(e => !lineESet.has(e));
      const baseCells = aOn1 ? [tPrime!, ...aCells] : aCells;
      if (baseCells.length < 3) continue;
      nCs++;
      const Rs = applyChunk(rCombos(r => r.every(s => !cStones.has(s)) && (!aOn1 || cnt3on(r) >= 1)));
      prog(`C curve ${ci}: ${Rs.length} R`);
      const baseIdx = baseCells.map(x => eIdx.get(x)!).sort((a,b)=>a-b);
      let ridx = 0;
      for (const R of Rs) {
        if (ridx++ % 200 === 0) prog(`C curve ${ci} R ${ridx}/${Rs.length}`);
        cRpairs++;
        const st = buildRState(R);
        const allowed = new Set<number>(baseIdx);
        const sp: ASpace = { allowed, pairOK: () => true, tripleOK: () => true };
        const enumA = (): number[][] => {
          const outA: number[][] = [];
          if (aOn1) { const tp = eIdx.get(tPrime!)!; const rest = baseIdx.filter(b => b !== tp); for (let i = 0; i < rest.length; i++) for (let j = i+1; j < rest.length; j++) outA.push([tp, rest[i], rest[j]].sort((a,b)=>a-b)); }
          else { for (let i = 0; i < baseIdx.length; i++) for (let j = i+1; j < baseIdx.length; j++) for (let k = j+1; k < baseIdx.length; k++) outA.push([baseIdx[i], baseIdx[j], baseIdx[k]]); }
          return outA;
        };
        const UsAll = st.Uhard.filter(u => u !== tCell && !c.board.includes(u));
        const usCache = new Map<number, UStruct>();
        const getUS = (u: number): UStruct => { let us = usCache.get(u); if (!us) { us = buildUStruct(st, u, sp); usCache.set(u, us); } return us; };
        let rej = false;
        for (const u of UsAll) { if (allowed.has(eIdx.get(u)!)) continue; if (getUS(u).empty) { rej = true; break; } }
        if (rej) { rejR++; continue; }
        const As = enumA();
        for (const A of As) {
          pairsChecked++;
          const saf = safeA(st, A);
          if (saf !== 0) { rejA_saf++; safSmp++; if (ctl.safTaken < 10 && safSmp % 211 === 0) { ctl.safTaken++; const bw = bruteWitness(R, A); ctl.safAgree += bw.mx >= Q ? 1 : 0; } continue; }
          let bad = -1;
          for (const u of UsAll) { const ea = eIdx.get(u); if (ea !== undefined && (A[0] === ea || A[1] === ea || A[2] === ea)) continue; const us = getUS(u); if (!coversA(us, A)) { bad = u; break; } }
          if (bad >= 0) { rejA_cov++; covSmp++; if (ctl.covTaken < 12 && covSmp % 173 === 0) { ctl.covTaken++; ctl.covAgree += directCoveredU(cells[bad], S2of(R, A)) ? 0 : 1; } continue; }
          survivors++;
          const bw = bruteWitness(R, A);
          witnesses.push({ R, c: ci, A: A.map(a => cells[a]), brute: bw, witness: bw.witness });
        }
      }
    }
    out[name] = { nCs, cRpairs, rejR, rejA_cov, rejA_saf, survivors, pairsChecked, witnesses, ctl };
  };
  if (sub === "all" || sub === "C0") runC("C0", false);
  if (sub === "all" || sub === "C1") runC("C1", true);
  console.log(JSON.stringify(out));
}

// ---- Cctl: second independent implementation of the C0/C1 wholesale rejection ----
if (MODE === "Cctl") {
  const sub = SUB || "all";
  const NS = Number(CHUNK || 6);
  const k3T = curves.filter(c => c.st.length === 3 && c.board.includes(tCell));
  const out: any = { nK3T: k3T.length };
  const runCctl = (name: string, aOn1: boolean) => {
    let cRpairs = 0, agree = 0, disagree = 0, killerConfirmed = 0, killerFailed = 0, uSampleOK = 0, nCs = 0;
    const killers: any[] = [];
    for (let ci = 0; ci < k3T.length; ci++) {
      const c = k3T[ci];
      const cStones = new Set<number>(c.st);
      const cBoard = new Set<number>(c.board);
      const tPrime = c.empt.find(e => lineESet.has(e) && e !== tCell);
      if (aOn1 && tPrime === undefined) continue;
      const aCells = c.empt.filter(e => !lineESet.has(e));
      const baseCells = aOn1 ? [tPrime!, ...aCells] : aCells;
      if (baseCells.length < 3) continue;
      nCs++;
      const baseIdx = baseCells.map(x => eIdx.get(x)!).sort((a,b)=>a-b);
      const allowedSet = new Set<number>(baseIdx);
      const Rs = rCombos(r => r.every(s => !cStones.has(s)) && (!aOn1 || cnt3on(r) >= 1));
      prog(`Cctl curve ${ci}: ${Rs.length} R`);
      const freshCoverable = (u: number, SR: P[]): boolean => {
        const m = SR.length;
        const up = cells[u];
        const test = (a: number[]): boolean => {
          if (!onA(a, up[0], up[1])) return false;
          let st = 0; for (const p of SR) if (onA(a, p[0], p[1])) st++;
          if (st < 3 || st > 5) return false;
          let bc = 0; for (const b of baseIdx) if (onA(a, cells[E[b]][0], cells[E[b]][1])) bc++;
          if (st === 5 && bc >= 1) return true;
          if (st === 4 && bc >= 2) return true;
          if (st === 3 && bc >= 3) return true;
          return false;
        };
        for (let i = 0; i < m; i++) { if (SR[i][0]===up[0]&&SR[i][1]===up[1]) continue; const l = line(up, SR[i]); if (test(l)) return true; }
        for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { if ((SR[i][0]===up[0]&&SR[i][1]===up[1])||(SR[j][0]===up[0]&&SR[j][1]===up[1])) continue; const cc = circle(up, SR[i], SR[j]); if (cc && test(cc)) return true; }
        return false;
      };
      let ri = 0;
      for (const R of Rs) {
        if (ri++ % 200 === 0) prog(`Cctl curve ${ci} R ${ri}/${Rs.length}`);
        cRpairs++;
        const st = buildRState(R);
        const Rset = new Set<number>(R);
        const SR = seed.filter((_, si) => !Rset.has(si)).map(p => p.slice() as P);
        const UsAll = st.Uhard.filter(u => u !== tCell && !cBoard.has(u));
        const machineRej = (() => { const sp = { allowed: allowedSet, pairOK: () => true, tripleOK: () => true } as ASpace; for (const u of UsAll) { if (allowedSet.has(eIdx.get(u)!)) continue; if (buildUStruct(st, u, sp).empty) return u; } return -1; })();
        let freshKiller = -1;
        for (const u of UsAll) { if (allowedSet.has(eIdx.get(u)!)) continue; if (!freshCoverable(u, SR)) { freshKiller = u; break; } }
        if ((freshKiller >= 0) === (machineRej >= 0)) agree++; else disagree++;
        if (freshKiller >= 0 && machineRej >= 0) { if (!freshCoverable(machineRej, SR)) killerConfirmed++; else { killerFailed++; killers.push({ R, ci, freshKiller, machineRej }); } }
      }
      for (let i = 0; i < Rs.length; i += Math.max(1, Math.floor(Rs.length / NS))) {
        const R = Rs[i]; const st = buildRState(R); const Rset = new Set<number>(R);
        const SR = seed.filter((_, si) => !Rset.has(si)).map(p => p.slice() as P);
        const freshU = new Set<number>();
        const SRkeys = new Set<number>(SR.map(p => p[0]*100+p[1]));
        for (let c2 = 0; c2 < NC7; c2++) { if (SRkeys.has(cells[c2][0]*100+cells[c2][1])) continue; if (!directCoveredU(cells[c2], SR)) freshU.add(c2); }
        const machineU = new Set<number>(st.U);
        if (freshU.size === machineU.size && [...freshU].every(x => machineU.has(x))) uSampleOK++;
        else throw new Error("full U-set mismatch curve " + ci + " R=" + JSON.stringify(R));
      }
    }
    out[name] = { nCs, cRpairs, agree, disagree, killerConfirmed, killerFailed, uSampleOK, badKillers: killers };
  };
  if (sub === "all" || sub === "C0") runCctl("C0", false);
  if (sub === "all" || sub === "C1") runCctl("C1", true);
  console.log(JSON.stringify(out));
}

// ---- L2f1: r3_on=1, a_on=2 (2 lineE + 1 free; line = 5-1+2 = 6 => row 3 auto-covered) ----
if (MODE === "L2f1") {
  const lineEidx = lineE.map(c => eIdx.get(c)!);
  const freeIdx = freeE.map(c => eIdx.get(c)!);
  const sp: ASpace = { allowed: new Set<number>([...lineEidx, ...freeIdx]), pairOK: () => true, tripleOK: () => true };
  const Rs = applyChunk(rCombos(r => cnt3on(r) === 1));
  const enumA = (): number[][] => {
    const out: number[][] = [];
    for (let i = 0; i < lineEidx.length; i++) for (let j = i+1; j < lineEidx.length; j++) for (const f of freeIdx) out.push([lineEidx[i], lineEidx[j], f].sort((a,b)=>a-b));
    return out;
  };
  const r = runSlice(Rs, enumA, () => sp, (u) => cells[u][1] !== 3);
  console.log(JSON.stringify({ mode: "L2f1", nR: Rs.length, ...r }));
}

// ---- L1f2: r3_on=0, a_on=1 (1 lineE + 2 free; line = 5+1 = 6 => row 3 auto-covered) ----
if (MODE === "L1f2") {
  const lineEidx = lineE.map(c => eIdx.get(c)!);
  const freeIdx = freeE.map(c => eIdx.get(c)!);
  const sp: ASpace = { allowed: new Set<number>([...lineEidx, ...freeIdx]), pairOK: () => true, tripleOK: () => true };
  const Rs = applyChunk(rCombos(r => cnt3on(r) === 0));
  const enumA = (): number[][] => {
    const out: number[][] = [];
    for (const l of lineEidx) for (let i = 0; i < freeIdx.length; i++) for (let j = i+1; j < freeIdx.length; j++) out.push([l, freeIdx[i], freeIdx[j]].sort((a,b)=>a-b));
    return out;
  };
  const r = runSlice(Rs, enumA, () => sp, (u) => cells[u][1] !== 3);
  console.log(JSON.stringify({ mode: "L1f2", nR: Rs.length, ...r }));
}
