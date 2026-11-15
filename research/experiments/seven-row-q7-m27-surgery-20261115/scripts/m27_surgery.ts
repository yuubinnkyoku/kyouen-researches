// (7,7) 7x27 frontier surgery machines — verified consolidated reproduction script (2026-11-15).
// Pure TypeScript, deterministic, no I/O, no external dependencies.
// Modes:
//   "twoEdit"           - |A|<=2, |R|<=2, |R|>=|A|: complete two-edit surgery (singles + pairs)
//   "oneAddThreeRemove" - |A|=1, |R|=3: (ia) line addition with r_on=0 (R = 3 off-line stones),
//                         (ib) T addition (R = any 3 stones)
//   "lineTriple"        - |A|=3 all on line y=3, |R|=3 (2 row-3 stones + 1 non-row-3): r_on=2,
//                         line = 5-2+3 = 6 blocks T; complete sub-space of the (3,3) case
// Seed: seven-row-q7-witness-search-20261114/output/w7q7_7x26q7_rowY3.witness.json (41 stones, rows 6,6,6,5,6,6,6)
// Canonical outputs of the 2026-11-15 verified runs: ../output/surgery_results.json
// Verification protocol (see ../README.md): two independent implementations agree bit-exact on twoEdit;
// targeted direct verification 470/470 (coverage 410 + safety gate 60/60 direct-brute UNSAFE);
// gates demonstrably fire (okZ 550,320 / safety 90,540 / shared 1,430) — a dead-gate run would mimic a negative.
// Standalone use: set MODE and run; the result object is returned from main().

const MODE: "twoEdit" | "oneAddThreeRemove" | "lineTriple" = "twoEdit";

type P = [number, number];
const W = 7, M = 27, Q = 7;
const seed: P[] = [[2,0],[7,0],[12,0],[14,0],[18,0],[19,0],[6,1],[10,1],[11,1],[15,1],[16,1],[20,1],[1,2],[8,2],[13,2],[14,2],[17,2],[24,2],[0,3],[2,3],[3,3],[23,3],[25,3],[4,4],[9,4],[11,4],[15,4],[16,4],[20,4],[7,5],[8,5],[17,5],[18,5],[19,5],[23,5],[5,6],[9,6],[10,6],[16,6],[17,6],[21,6]];
const T: P = [26, 3];

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
type Curve = {kind: string, a: number[], stones: P[], cnt: number, stIdx: Set<number>, board: number[], empt: number[]};
const onC = (c: Curve, x: number, y: number) => c.kind === "line" ? c.a[0]*x+c.a[1]*y+c.a[2] === 0 : c.a[0]*(x*x+y*y)+c.a[1]*x+c.a[2]*y+c.a[3] === 0;
const n = seed.length;
const stoneKey = new Set(seed.map(p => p[0]*100 + p[1]));
const cells: P[] = [];
const cellIdx = new Map<number, number>();
for (let y = 0; y < W; y++) for (let x = 0; x < M; x++) { cellIdx.set(x*100+y, cells.length); cells.push([x,y]); }
const cmap = new Map<string, Curve>();
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) { const l = line(seed[i], seed[j]); const k = "L"+l.join(","); if (!cmap.has(k)) cmap.set(k, {kind:"line", a:l, stones:[], cnt:0, stIdx:new Set(), board:[], empt:[]}); }
for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k2 = j+1; k2 < n; k2++) { const c = circle(seed[i], seed[j], seed[k2]); if (!c) continue; const k = "C"+c.join(","); if (!cmap.has(k)) cmap.set(k, {kind:"circle", a:c, stones:[], cnt:0, stIdx:new Set(), board:[], empt:[]}); }
const bigCurves: Curve[] = [];
for (const c of cmap.values()) {
  for (let si = 0; si < n; si++) if (onC(c, seed[si][0], seed[si][1])) { c.stones.push(seed[si]); c.stIdx.add(si); }
  c.cnt = c.stones.length;
  if (c.cnt < 4) continue;
  for (let i = 0; i < cells.length; i++) { const cl = cells[i]; if (onC(c, cl[0], cl[1])) { c.board.push(i); if (!stoneKey.has(cl[0]*100+cl[1])) c.empt.push(i); } }
  bigCurves.push(c);
}
const E: P[] = cells.filter(c => !stoneKey.has(c[0]*100+c[1]));
const Eidx = E.map(p => cellIdx.get(p[0]*100+p[1])!);
const lineEmptyNoT: P[] = E.filter(c => c[1] === 3 && !(c[0]===T[0]&&c[1]===T[1])); // 21 cells (twoEdit / oneAddThreeRemove)
const lineEmptyWithT: P[] = E.filter(c => c[1] === 3);                              // 22 cells (lineTriple: T is a legal line addition)
const c6through: number[][] = cells.map(() => []);
const zBig: number[][] = cells.map(() => []);
for (let ci = 0; ci < bigCurves.length; ci++) {
  if (bigCurves[ci].cnt === 6) for (const b of bigCurves[ci].board) c6through[b].push(ci);
  for (const b of bigCurves[ci].board) zBig[b].push(ci);
}
function directCovered(u: P, stones: P[]): boolean {
  const m = stones.length;
  const test = (kind: string, a: number[]) => { let cc = 0; if (kind === "line") { for (const p of stones) if (a[0]*p[0]+a[1]*p[1]+a[2] === 0) cc++; } else { for (const p of stones) if (a[0]*(p[0]*p[0]+p[1]*p[1])+a[1]*p[0]+a[2]*p[1]+a[3] === 0) cc++; } return cc >= 6; };
  for (let i = 0; i < m; i++) { const l = line(u, stones[i]); if (test("line", l)) return true; }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const c = circle(u, stones[i], stones[j]); if (c && test("circle", c)) return true; }
  return false;
}
function bruteVerify(stones: P[]) {
  const ks = new Set(stones.map(p => p[0]*100+p[1]));
  const cm = new Map<string, Curve>();
  const m = stones.length;
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) { const l = line(stones[i], stones[j]); const k = "L"+l.join(","); if (!cm.has(k)) cm.set(k, {kind:"line", a:l, stones:[], cnt:0, stIdx:new Set(), board:[], empt:[]}); }
  for (let i = 0; i < m; i++) for (let j = i+1; j < m; j++) for (let k2 = j+1; k2 < m; k2++) { const c = circle(stones[i], stones[j], stones[k2]); if (!c) continue; const k = "C"+c.join(","); if (!cm.has(k)) cm.set(k, {kind:"circle", a:c, stones:[], cnt:0, stIdx:new Set(), board:[], empt:[]}); }
  let maxCurve = 0;
  for (const c of cm.values()) { let cc = 0; for (const p of stones) if (onC(c, p[0], p[1])) cc++; c.cnt = cc; if (cc > maxCurve) maxCurve = cc; }
  const ge6: Curve[] = []; for (const c of cm.values()) if (c.cnt >= 6) ge6.push(c);
  const unc: P[] = [];
  for (const cell of cells) { if (ks.has(cell[0]*100+cell[1])) continue; if (!ge6.some(c => onC(c, cell[0], cell[1]))) unc.push(cell); }
  const rows = [0,0,0,0,0,0,0]; for (const p of stones) rows[p[1]]++;
  return {safe: maxCurve < Q, maxCurve, uncovered: unc, rows};
}

// ============ mode: twoEdit ============
function runTwoEdit() {
  const seedCtl = bruteVerify(seed);
  let candS = 0, candP = 0, saf1S = 0, covS = 0, survS = 0, sharedRej = 0, covPRej = 0, survP = 0;
  const survivors: {R: P[], A: P[], S: P[]}[] = [];
  const ctl2 = { tested: false, rejected: false };
  let ctl1Taken = 0, ctl1Agree = 0;
  const special = new Set<number>([T[0]*100+T[1], ...lineEmptyNoT.map(p => p[0]*100+p[1])]);
  const specialIdx: number[] = [];
  for (let i = 0; i < E.length; i++) if (special.has(E[i][0]*100+E[i][1])) specialIdx.push(i);
  const Rsets: P[][] = [];
  for (let i = 0; i < n; i++) Rsets.push([seed[i]]);
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) Rsets.push([seed[i], seed[j]]);
  for (const R of Rsets) {
    const Rset = new Set<number>(R.map(p => seed.findIndex(s => s[0]===p[0]&&s[1]===p[1])));
    const r2 = R.length === 2;
    const effOf = (ci: number) => { const c = bigCurves[ci]; let r = 0; for (const si of c.stIdx) if (Rset.has(si)) r++; return c.cnt - r; };
    const okZ = new Set<number>();
    for (let ei = 0; ei < E.length; ei++) {
      const cellI = Eidx[ei];
      let ok = true;
      for (const ci of c6through[cellI]) { if (effOf(ci) === 6) { ok = false; break; } }
      if (ok) okZ.add(ei);
    }
    const U: number[] = [];
    for (let i = 0; i < cells.length; i++) {
      const cl = cells[i];
      const k = cl[0]*100+cl[1];
      if (stoneKey.has(k) && !R.some(rp => rp[0]*100+rp[1] === k)) continue;
      let cov = false;
      for (const ci of c6through[i]) { if (effOf(ci) === 6) { cov = true; break; } }
      if (!cov) U.push(i);
    }
    const covA = new Map<number, Set<number>>();
    for (let ci = 0; ci < bigCurves.length; ci++) {
      if (effOf(ci) !== 5) continue;
      const c = bigCurves[ci];
      for (const b of c.board) { let s = covA.get(b); if (!s) { s = new Set(); covA.set(b, s); } for (const e of c.empt) s.add(e); }
    }
    const e4cache = new Map<number, Set<number>[]>();
    function e4sets(u: number): Set<number>[] {
      let l = e4cache.get(u); if (l) return l;
      l = [];
      for (const ci of zBig[u]) { if (effOf(ci) === 4) { const c = bigCurves[ci]; const s = new Set<number>(); for (const b of c.empt) s.add(b); l.push(s); } }
      e4cache.set(u, l); return l;
    }
    for (const zEi of specialIdx) {
      candS++;
      const z = E[zEi];
      const zB = Eidx[zEi];
      const isT = z[0]===T[0] && z[1]===T[1];
      if (!okZ.has(zEi)) { saf1S++; continue; }
      let covOk = true;
      for (const u of U) {
        if (u === zB) continue;
        const s = covA.get(u);
        if (!s || !s.has(zB)) { covOk = false; break; }
      }
      if (!covOk) {
        covS++;
        if (isT && R.length === 1 && R[0][0]===0 && R[0][1]===3) { ctl2.tested = true; ctl2.rejected = true; }
        continue;
      }
      const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z]) as P[];
      survivors.push({R, A:[z], S}); survS++;
    }
    if (!r2) continue;
    const hiC = new Map<number, number[]>();
    for (const zEi of specialIdx) {
      const zB = Eidx[zEi];
      const lst: number[] = [];
      for (const ci of zBig[zB]) { const e = effOf(ci); if (e >= 5) lst.push(ci); }
      hiC.set(zEi, lst);
    }
    const okList = [...okZ];
    for (const z1Ei of specialIdx) {
      if (!okZ.has(z1Ei)) continue;
      const z1B = Eidx[z1Ei];
      for (const z2Ei of okList) {
        if (z2Ei <= z1Ei) continue;
        candP++;
        const z2B = Eidx[z2Ei];
        let bad = false;
        for (const ci of hiC.get(z1Ei)!) { const c = bigCurves[ci]; if (onC(c, cells[z2B][0], cells[z2B][1])) { bad = true; break; } }
        if (bad) { sharedRej++; continue; }
        let covOk = true; let failedU: number[] = [];
        for (const u of U) {
          if (u === z1B || u === z2B) continue;
          const s = covA.get(u);
          if (s && (s.has(z1B) || s.has(z2B))) continue;
          let pairCov = false;
          for (const st of e4sets(u)) { if (st.has(z1B) && st.has(z2B)) { pairCov = true; break; } }
          if (!pairCov) { covOk = false; failedU.push(u); break; }
        }
        if (!covOk) {
          covPRej++;
          if (ctl1Taken < 150 && covPRej % 11 === 0) {
            ctl1Taken++;
            const z1 = cells[z1B], z2 = cells[z2B];
            const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z1, z2]) as P[];
            if (!directCovered(cells[failedU[0]], S)) ctl1Agree++;
          }
          continue;
        }
        const z1 = cells[z1B], z2 = cells[z2B];
        const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z1, z2]) as P[];
        survivors.push({R, A:[z1,z2], S}); survP++;
      }
    }
  }
  const verified: typeof survivors = [];
  let bc = 0;
  for (const s of survivors) { if (bc >= 80) break; bc++;
    const v = bruteVerify(s.S);
    if (v.safe && v.uncovered.length === 0 && Math.min(...v.rows) <= Q-2) verified.push(s);
  }
  return {seedCtl: {maxCurve: seedCtl.maxCurve, uncovered: seedCtl.uncovered.map(p => p.join(",")), rows: seedCtl.rows},
    curves: {big: bigCurves.length, c6: bigCurves.filter(c=>c.cnt===6).length, c5: bigCurves.filter(c=>c.cnt===5).length, c4: bigCurves.filter(c=>c.cnt===4).length},
    counts: {candS, candP, saf1S, covS, survS, sharedRej, covPRej, survP}, ctl2, ctl1: {taken: ctl1Taken, agree: ctl1Agree},
    survivors: survivors.length, bruteChecked: bc, verifiedCount: verified.length,
    witnesses: verified.map(v => ({R: v.R, A: v.A, rows: bruteVerify(v.S).rows, stones: v.S}))};
}

// ============ mode: oneAddThreeRemove ============
function runOneAddThreeRemove() {
  const nonRow3 = seed.filter(p => p[1] !== 3);
  function runCase(Rsets: P[][], zOptions: P[]) {
    let cand = 0, safRej = 0, covRej = 0, surv = 0;
    const survivors: {R: P[], A: P[], S: P[]}[] = [];
    let ctlTaken = 0, ctlAgree = 0;
    let safCtlTaken = 0, safCtlAgree = 0; // targeted direct-brute check of safety-gate rejections
    const zBs = zOptions.map(z => cellIdx.get(z[0]*100+z[1])!);
    for (const R of Rsets) {
      const Rset = new Set<number>(R.map(p => seed.findIndex(s => s[0]===p[0]&&s[1]===p[1])));
      const effOf = (ci: number) => { const c = bigCurves[ci]; let r = 0; for (const si of c.stIdx) if (Rset.has(si)) r++; return c.cnt - r; };
      const U: number[] = [];
      for (let i = 0; i < cells.length; i++) {
        const cl = cells[i]; const k = cl[0]*100+cl[1];
        if (stoneKey.has(k) && !R.some(rp => rp[0]===cl[0]&&rp[1]===cl[1])) continue;
        let cov = false;
        for (const ci of c6through[i]) if (effOf(ci) === 6) { cov = true; break; }
        if (!cov) U.push(i);
      }
      const coverZ = new Map<number, Set<number>>();
      const cz = (u: number): Set<number> => {
        let s = coverZ.get(u); if (s) return s;
        s = new Set<number>();
        for (const ci of zBig[u]) if (effOf(ci) === 5) { const c = bigCurves[ci]; for (const e of c.empt) s.add(e); }
        coverZ.set(u, s); return s;
      };
      for (let zi = 0; zi < zOptions.length; zi++) {
        cand++;
        const zB = zBs[zi];
        let ok = true;
        for (const ci of c6through[zB]) if (effOf(ci) === 6) { ok = false; break; }
        if (!ok) {
          safRej++;
          if (safCtlTaken < 60 && safRej % 1509 === 0) {
            safCtlTaken++;
            const z = zOptions[zi];
            const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z]) as P[];
            const v = bruteVerify(S);
            if (!v.safe) safCtlAgree++;
          }
          continue;
        }
        let covOk = true; let failU = -1;
        for (const u of U) {
          if (u === zB) continue;
          if (!cz(u).has(zB)) { covOk = false; failU = u; break; }
        }
        if (!covOk) {
          covRej++;
          if (ctlTaken < 80 && covRej % 23 === 0) {
            ctlTaken++;
            const z = zOptions[zi];
            const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z]) as P[];
            if (!directCovered(cells[failU], S)) ctlAgree++;
          }
          continue;
        }
        const z = zOptions[zi];
        const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat([z]) as P[];
        survivors.push({R, A:[z], S}); surv++;
      }
    }
    const verified: typeof survivors = [];
    for (const s of survivors) {
      const v = bruteVerify(s.S);
      if (v.safe && v.uncovered.length === 0 && Math.min(...v.rows) <= 5) verified.push(s);
    }
    return {cand, safRej, covRej, surv, ctl: {taken: ctlTaken, agree: ctlAgree},
      safetyGateCtl: {taken: safCtlTaken, agree: safCtlAgree},
      verifiedCount: verified.length, witnesses: verified.map(v => ({R: v.R, A: v.A, rows: bruteVerify(v.S).rows, stones: v.S}))};
  }
  const RsetsA: P[][] = [];
  for (let i = 0; i < nonRow3.length; i++) for (let j = i+1; j < nonRow3.length; j++) for (let k = j+1; k < nonRow3.length; k++) RsetsA.push([nonRow3[i], nonRow3[j], nonRow3[k]]);
  const caseIA = runCase(RsetsA, lineEmptyNoT);
  const RsetsB: P[][] = [];
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) RsetsB.push([seed[i], seed[j], seed[k]]);
  const caseIB = runCase(RsetsB, [T]);
  return {caseIA_Rsets: RsetsA.length, caseIB_Rsets: RsetsB.length, caseIA, caseIB};
}

// ============ mode: lineTriple ============
function runLineTriple() {
  const row3: P[] = seed.filter(p => p[1] === 3);
  const nonRow3: P[] = seed.filter(p => p[1] !== 3);
  const Rsets: P[][] = [];
  for (let i = 0; i < 5; i++) for (let j = i+1; j < 5; j++) for (const p of nonRow3) Rsets.push([row3[i], row3[j], p]);
  let candTotal = 0, cand = 0, sharedRej = 0, covRej = 0, surv = 0;
  const survivors: {R: P[], A: P[], S: P[]}[] = [];
  let ctlTaken = 0, ctlAgree = 0;
  for (const R of Rsets) {
    const Rset = new Set<number>(R.map(p => seed.findIndex(s => s[0]===p[0]&&s[1]===p[1])));
    const effOf = (ci: number) => { const c = bigCurves[ci]; let r = 0; for (const si of c.stIdx) if (Rset.has(si)) r++; return c.cnt - r; };
    const okList: number[] = [];
    for (let ei = 0; ei < E.length; ei++) {
      const p = E[ei];
      if (p[1] !== 3) continue;
      const b = Eidx[ei];
      let ok = true;
      for (const ci of c6through[b]) if (effOf(ci) === 6) { ok = false; break; }
      if (ok) okList.push(ei);
    }
    candTotal += 1540; // C(22,3): full triple space per R (before the necessary-condition okZ gate)
    if (okList.length < 3) continue;
    const Uother: number[] = [];
    for (let i = 0; i < cells.length; i++) {
      const cl = cells[i]; const k = cl[0]*100+cl[1];
      if (stoneKey.has(k) && !R.some(rp => rp[0]===cl[0]&&rp[1]===cl[1])) continue;
      if (cl[1] === 3) continue; // row-3 cells are covered by the line (5-2+3=6) in S'
      let cov = false;
      for (const ci of c6through[i]) if (effOf(ci) === 6) { cov = true; break; }
      if (!cov) Uother.push(i);
    }
    const covA = new Map<number, Set<number>>();
    for (let ci = 0; ci < bigCurves.length; ci++) {
      if (effOf(ci) !== 5) continue;
      const c = bigCurves[ci];
      for (const b of c.board) { let s = covA.get(b); if (!s) { s = new Set(); covA.set(b, s); } for (const e of c.empt) s.add(e); }
    }
    const e4cache = new Map<number, Set<number>[]>();
    const e4sets = (u: number): Set<number>[] => {
      let l = e4cache.get(u); if (l) return l;
      l = [];
      for (const ci of zBig[u]) if (effOf(ci) === 4) { const c = bigCurves[ci]; const s = new Set<number>(); for (const b of c.empt) s.add(b); l.push(s); }
      e4cache.set(u, l); return l;
    };
    const hiC = new Map<number, number[]>();
    for (const ei of okList) {
      const b = Eidx[ei]; const lst: number[] = [];
      for (const ci of zBig[b]) if (effOf(ci) >= 5) lst.push(ci);
      hiC.set(ei, lst);
    }
    const K = okList.length;
    for (let a = 0; a < K; a++) for (let b2 = a+1; b2 < K; b2++) for (let c3 = b2+1; c3 < K; c3++) {
      cand++;
      const eis = [okList[a], okList[b2], okList[c3]];
      const bs = eis.map(ei => Eidx[ei]);
      let bad = false;
      for (let pi = 0; pi < 3 && !bad; pi++) {
        for (const ci of hiC.get(eis[pi])!) {
          const c = bigCurves[ci];
          let other = false;
          for (let pj = 0; pj < 3; pj++) if (pj !== pi && onC(c, cells[bs[pj]][0], cells[bs[pj]][1])) { other = true; break; }
          if (other) { bad = true; break; }
        }
      }
      if (bad) { sharedRej++; continue; }
      let covOk = true; let failU = -1;
      for (const u of Uother) {
        if (bs.includes(u)) continue;
        const s = covA.get(u);
        let cov = false;
        if (s) { for (const b3 of bs) if (s.has(b3)) { cov = true; break; } }
        if (!cov) {
          for (const st of e4sets(u)) {
            let cnt = 0;
            for (const b3 of bs) if (st.has(b3)) cnt++;
            if (cnt >= 2) { cov = true; break; }
          }
        }
        if (!cov) { covOk = false; failU = u; break; }
      }
      if (!covOk) {
        covRej++;
        if (ctlTaken < 100 && covRej % 17 === 0) {
          ctlTaken++;
          const A = bs.map(b3 => cells[b3]);
          const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat(A) as P[];
          if (!directCovered(cells[failU], S)) ctlAgree++;
        }
        continue;
      }
      const A = bs.map(b3 => cells[b3]);
      const S = seed.filter(p => !R.some(rp => rp[0]===p[0]&&rp[1]===p[1])).concat(A) as P[];
      survivors.push({R, A, S}); surv++;
    }
  }
  const verified: typeof survivors = [];
  for (const s of survivors) {
    const v = bruteVerify(s.S);
    if (v.safe && v.uncovered.length === 0 && Math.min(...v.rows) <= 5) verified.push(s);
  }
  return {triplesTotal: candTotal, okzGateRejected: candTotal - cand, gatedValid: cand, sharedRej, covRej, surv,
    ctl: {taken: ctlTaken, agree: ctlAgree}, verifiedCount: verified.length,
    witnesses: verified.map(v => ({R: v.R, A: v.A, rows: bruteVerify(v.S).rows, stones: v.S}))};
}

// ============ dispatch ============
async function main() {
  if (MODE === "twoEdit") return {mode: MODE, result: runTwoEdit()};
  if (MODE === "oneAddThreeRemove") return {mode: MODE, result: runOneAddThreeRemove()};
  return {mode: MODE, result: runLineTriple()};
}
main();
