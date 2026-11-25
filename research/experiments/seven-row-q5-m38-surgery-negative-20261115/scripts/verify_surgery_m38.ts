async function main() {
  // research/experiments/seven-row-q5-m38-surgery-negative-20261115/scripts/verify_surgery_m38.ts
  // (7,5) 7x38 two-edit surgery of winC (T'=(37,0), q=5, NEED=4): complete six-case
  // final-state enumeration with exact U-set pruning for the two heavy cases,
  // an end-to-end m35 case-b replica control, direct U validation, and skip audits.
  // Pure TS, exact integer arithmetic, no repo code, no census, no SAT.
  type Pt = [number, number];
  const gcd2 = (a: number, b: number): number => { a = Math.abs(a); b = Math.abs(b); while (b > 0) { const t = a % b; a = b; b = t; } return a; };
  const gcd3 = (a: number, b: number, c: number): number => gcd2(gcd2(a, b), c);
  const gcd4 = (a: number, b: number, c: number, d: number): number => gcd2(gcd3(a, b, c), d);
  function lineCurve(p: Pt, q: Pt): any {
    let a = q[1] - p[1], b = p[0] - q[0], c = -a * p[0] - b * p[1];
    const g = gcd3(a, b, c) || 1;
    a /= g; b /= g; c /= g;
    if (a < 0 || (a === 0 && b < 0)) { a = -a; b = -b; c = -c; }
    return { t: "L", a: a, b: b, c: c, k: "L|" + a + "," + b + "," + c };
  }
  function circleCurve(p: Pt, q: Pt, r: Pt): any {
    const A = q[0] - p[0], B = q[1] - p[1], C = r[0] - p[0], D = r[1] - p[1];
    const det = A * D - C * B;
    if (det === 0) return null;
    const R1 = q[0]*q[0] + q[1]*q[1] - p[0]*p[0] - p[1]*p[1];
    const R2 = r[0]*r[0] + r[1]*r[1] - p[0]*p[0] - p[1]*p[1];
    let d1 = -R1 * D + R2 * B, d2 = -A * R2 + C * R1;
    let d3 = -det * (p[0]*p[0] + p[1]*p[1]) - d1 * p[0] - d2 * p[1];
    const g = gcd4(det, d1, d2, d3) || 1;
    let d0 = det / g; d1 /= g; d2 /= g; d3 /= g;
    if (d0 < 0) { d0 = -d0; d1 = -d1; d2 = -d2; d3 = -d3; }
    return { t: "C", d0: d0, d1: d1, d2: d2, d3: d3, k: "C|" + d0 + "," + d1 + "," + d2 + "," + d3 };
  }
  function curveThru(p: Pt, q: Pt, r: Pt): any { const c = circleCurve(p, q, r); return c !== null ? c : lineCurve(p, q); }
  function onCurve(cv: any, x: number, y: number): boolean {
    return cv.t === "L" ? cv.a * x + cv.b * y + cv.c === 0
      : cv.d0 * (x * x + y * y) + cv.d1 * x + cv.d2 * y + cv.d3 === 0;
  }
  function buildTable(stones: Pt[]): Map<string, any> {
    const n = stones.length;
    const map = new Map<string, any>();
    for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) {
      const cv = curveThru(stones[i], stones[j], stones[k]);
      if (!map.has(cv.k)) map.set(cv.k, cv);
    }
    for (const cv of map.values()) { let c = 0; for (const s of stones) if (onCurve(cv, s[0], s[1])) c++; cv.cnt = c; }
    return map;
  }
  function uncoveredAt(stones: Pt[], W: number, need: number): Pt[] {
    const tab = buildTable(stones);
    const nc: any[] = []; for (const cv of tab.values()) if (cv.cnt >= need) nc.push(cv);
    const occ = new Set(stones.map(s => s[0] + "," + s[1]));
    const res: Pt[] = [];
    for (let y = 0; y < 7; y++) for (let x = 0; x < W; x++) {
      if (occ.has(x + "," + y)) continue;
      let b = false;
      for (const cv of nc) if (onCurve(cv, x, y)) { b = true; break; }
      if (!b) res.push([x, y]);
    }
    return res;
  }
  const sortSt = (st: Pt[]): Pt[] => st.slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]);
  const rowsOf = (st: Pt[]): number[] => { const r = [0,0,0,0,0,0,0]; for (const s of st) r[s[1]]++; return r; };
  const WINA: Pt[] = sortSt([[8,0],[18,0],[30,0],[5,1],[24,1],[28,1],[32,1],[0,2],[9,2],[22,2],[28,2],[14,3],[15,3],[21,3],[30,3],[16,4],[26,4],[30,4],[2,4],[3,5],[8,5],[21,5],[22,5],[15,6],[16,6],[18,6],[25,6]]);
  const WINC: Pt[] = sortSt(WINA.filter(s => !(s[0]===8&&s[1]===5) && !(s[0]===16&&s[1]===6)).concat([[24,5],[22,6]] as Pt[]));
  const R: any = {};
  {
    const t1 = buildTable([[0,0],[1,0],[2,0],[3,0],[4,0]]);
    const t2 = buildTable([[5,0],[0,5],[3,4],[4,3],[-5,0]]);
    const t3 = buildTable([[0,0],[1,0],[2,0],[3,0],[10,5]]);
    const mx = (t: Map<string,any>) => Math.max(...[...t.values()].map(c => c.cnt));
    R.controls = { collinear5_detected: mx(t1) === 5, concyclic5_detected: mx(t2) === 5, line4_not5: mx(t3) === 4, circle_dedup: buildTable([[3,0],[0,3],[-3,0],[0,-3]]).size === 1 };
  }
  function makeMachine(BASE: Pt[], W: number, NEED: number, T: Pt) {
    const N = BASE.length;
    const eKey = (p: Pt) => p[0] + "," + p[1];
    const isT = (p: Pt) => p[0] === T[0] && p[1] === T[1];
    const bIdx = new Map<string, number>(); BASE.forEach((s, i) => bIdx.set(s[0] + "," + s[1], i));
    const EMPTY: Pt[] = [];
    for (let y = 0; y < 7; y++) for (let x = 0; x < W; x++) if (!bIdx.has(x + "," + y)) EMPTY.push([x, y]);
    const tab = buildTable(BASE);
    const baseNeed: any[] = [];
    for (const cv of tab.values()) if (cv.cnt >= NEED) { cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; baseNeed.push(cv); }
    const BL: number[][] = EMPTY.map(e => { const l: number[] = []; baseNeed.forEach((cv, ci) => { if (onCurve(cv, e[0], e[1])) l.push(ci); }); return l; });
    const countBase = (cv: any): number => { let c = 0; for (let i = 0; i < N; i++) if (onCurve(cv, BASE[i][0], BASE[i][1])) c++; return c; };
    const dangerCache = new Map<string, any[]>();
    function danger(z: Pt): any[] {
      const zk = eKey(z);
      let d = dangerCache.get(zk);
      if (d) return d;
      const m = new Map<string, any>();
      for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) { const cv = curveThru(z, BASE[i], BASE[j]); if (!m.has(cv.k)) m.set(cv.k, cv); }
      d = [];
      for (const cv of m.values()) { const c = countBase(cv); if (c >= 3) { cv.bc = c; cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; d.push(cv); } }
      dangerCache.set(zk, d);
      return d;
    }
    function stoneCurves(s: number): any[] {
      const m = new Map<string, any>();
      for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) { const cv = curveThru(BASE[s], BASE[i], BASE[j]); if (!m.has(cv.k)) m.set(cv.k, cv); }
      const d: any[] = [];
      for (const cv of m.values()) { const c = countBase(cv); if (c >= 3) { cv.bc = c; cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; d.push(cv); } }
      return d;
    }
    const tnewCache = new Map<string, any[]>();
    function tnew(sp: Pt): any[] {
      const kk = eKey(sp);
      let d = tnewCache.get(kk);
      if (d) return d;
      const m = new Map<string, any>();
      for (let i = 0; i < N; i++) { const cv = curveThru(T, sp, BASE[i]); if (!m.has(cv.k)) m.set(cv.k, cv); }
      d = [];
      for (const cv of m.values()) { const c = countBase(cv); if (c >= 2) { cv.bc = c; cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; d.push(cv); } }
      tnewCache.set(kk, d);
      return d;
    }
    function safeCheck(Rm: number[], P: Pt[]): boolean {
      for (let pi = 0; pi < P.length; pi++) {
        const other = P.length === 2 ? P[1 - pi] : null;
        for (const cv of danger(P[pi])) {
          let r = 0; for (const s of Rm) if (cv.mem[s]) r++;
          if (cv.bc === 4) { if (r === 0) return false; if (r === 1 && other && onCurve(cv, other[0], other[1])) return false; }
          else { if (r === 0 && other && onCurve(cv, other[0], other[1])) return false; }
        }
      }
      return true;
    }
    function removedBlocked(s: number, Rm: number[], P: Pt[]): boolean {
      for (const cv of stoneCurves(s)) {
        let r = 0; for (const x of Rm) if (cv.mem[x]) r++;
        let newOn = 0; for (const sp of P) if (onCurve(cv, sp[0], sp[1])) newOn++;
        if (cv.bc - r + newOn >= NEED) return true;
      }
      return false;
    }
    function tBlocked(Rm: number[], P: Pt[]): boolean {
      for (const sp of P) {
        for (const cv of tnew(sp)) {
          let r = 0; for (const s of Rm) if (cv.mem[s]) r++;
          let cnt = cv.bc - r + 1;
          for (const sp2 of P) if (sp2 !== sp && onCurve(cv, sp2[0], sp2[1])) cnt++;
          if (cnt >= NEED) return true;
        }
      }
      return false;
    }
    function emptyBlocked(ei: number, Rm: number[], P: Pt[]): boolean {
      for (const ci of BL[ei]) { const cv = baseNeed[ci]; let r = 0; for (const s of Rm) if (cv.mem[s]) r++; if (r === 0) return true; }
      const e = EMPTY[ei];
      for (const sp of P) {
        for (let i = 0; i < N; i++) {
          const cv = curveThru(e, sp, BASE[i]);
          let c2 = 1;
          for (let s2 = 0; s2 < N; s2++) if (onCurve(cv, BASE[s2][0], BASE[s2][1])) c2++;
          for (const sp2 of P) if (sp2 !== sp && onCurve(cv, sp2[0], sp2[1])) c2++;
          for (const s of Rm) if (onCurve(cv, BASE[s][0], BASE[s][1])) c2--;
          if (c2 >= NEED) return true;
        }
      }
      return false;
    }
    function maximalCheck(Rm: number[], P: Pt[]): Pt | null {
      for (const s of Rm) if (!removedBlocked(s, Rm, P)) return BASE[s];
      const occ = new Set<string>(); for (const p of P) occ.add(eKey(p));
      if (!occ.has(eKey(T)) && !tBlocked(Rm, P)) return T;
      for (let ei = 0; ei < EMPTY.length; ei++) {
        if (occ.has(eKey(EMPTY[ei]))) continue;
        if (isT(EMPTY[ei])) continue;
        if (!emptyBlocked(ei, Rm, P)) return EMPTY[ei];
      }
      return null;
    }
    return { BASE, N, W, NEED, T, eKey, isT, EMPTY, bIdx, tab, baseNeed, BL, countBase, danger, tnew, safeCheck, maximalCheck, uncoveredAt };
  }
  // ===== control: m35 case-b replica on winA (must rediscover winC) =====
  {
    const M = makeMachine(WINA, 35, 4, [34, 0]);
    const twoKeys = new Map<string, any>();
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) {
      const cv = curveThru(M.T, M.BASE[i], M.BASE[j]);
      if (M.countBase(cv) === 2 && !twoKeys.has(cv.k)) twoKeys.set(cv.k, cv);
    }
    const spPairs: [Pt, Pt][] = []; const seen = new Set<string>();
    for (const cv of twoKeys.values()) {
      const cells = M.EMPTY.filter(e => onCurve(cv, e[0], e[1]) && !M.isT(e));
      for (let i = 0; i < cells.length; i++) for (let j = i+1; j < cells.length; j++) {
        const kk = M.eKey(cells[i]) + "|" + M.eKey(cells[j]);
        if (!seen.has(kk)) { seen.add(kk); spPairs.push([cells[i], cells[j]]); }
      }
    }
    let cand = 0, safe = 0, max = 0; const wits: any[] = [];
    for (const pair of spPairs) for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) {
      cand++;
      if (!M.safeCheck([i, j], [pair[0], pair[1]])) continue;
      safe++;
      if (M.maximalCheck([i, j], [pair[0], pair[1]]) === null) { max++; wits.push({ removed: [M.BASE[i], M.BASE[j]], added: pair }); }
    }
    R.m35_caseb_replica = { spPairs: spPairs.length, candidates: cand, safe: safe, maximal: max, witnesses: wits, expected: { spPairs: 49, candidates: 17199, safe: 594, maximal: 1 } };
  }
  // ===== winC sanity + census on 7x38 =====
  const M = makeMachine(WINC, 38, 4, [37, 0]);
  R.sanity = { n: M.N, rows: rowsOf(WINC), maxCurve: Math.max(...[...M.tab.values()].map(c => c.cnt)), needCurves: M.baseNeed.length, unc37: M.uncoveredAt(WINC, 37, 4), unc38: M.uncoveredAt(WINC, 38, 4) };
  const k3c: any[] = [], k2c: any[] = [], k4p: any[] = [];
  {
    const twoM = new Map<string, any>();
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) { const cv = curveThru(M.T, M.BASE[i], M.BASE[j]); if (!twoM.has(cv.k)) twoM.set(cv.k, cv); }
    for (const cv of twoM.values()) {
      const c = M.countBase(cv);
      if (c >= 4) { k4p.push(cv); continue; }
      const stoneIdx: number[] = [], emptyCells: Pt[] = [], offIdx: number[] = [];
      for (let i = 0; i < M.N; i++) if (onCurve(cv, M.BASE[i][0], M.BASE[i][1])) stoneIdx.push(i); else offIdx.push(i);
      for (const e of M.EMPTY) if (!M.isT(e) && onCurve(cv, e[0], e[1])) emptyCells.push(e);
      (c === 3 ? k3c : k2c).push({ cv, bc: c, stoneIdx, emptyCells, offIdx });
    }
  }
  R.census = { k4plusTcurves: k4p.length, k3Tcurves: k3c.length, k3TcurveCells: k3c.map(r => r.emptyCells.length), k2Tcurves: k2c.length };
  const Uof = (pi: number, pj: number): string[] => {
    const hit = new Uint8Array(M.baseNeed.length);
    M.baseNeed.forEach((cv, ci) => { if (cv.mem[pi] || cv.mem[pj]) hit[ci] = 1; });
    const res = [M.eKey(M.BASE[pi]), M.eKey(M.BASE[pj])];
    for (let ei = 0; ei < M.EMPTY.length; ei++) {
      let covered = false;
      for (const ci of M.BL[ei]) if (!hit[ci]) { covered = true; break; }
      if (!covered) res.push(M.eKey(M.EMPTY[ei]));
    }
    return res;
  };
  {
    const samples: [number, number][] = [[0,1],[3,7],[5,12],[10,20],[2,26],[13,19],[4,9],[15,25],[6,24],[1,14],[8,18],[11,22],[16,23],[17,21],[0,26]];
    let all = true;
    for (const [pi, pj] of samples) {
      const st = M.BASE.filter((s, i) => i !== pi && i !== pj);
      const d = new Set(M.uncoveredAt(st, 38, 4).map(M.eKey)); d.add(M.eKey(M.BASE[pi])); d.add(M.eKey(M.BASE[pj]));
      const p = new Set(Uof(pi, pj));
      let m = 0, x = 0;
      for (const k2v of d) if (!p.has(k2v)) m++;
      for (const k2v of p) if (!d.has(k2v)) x++;
      if (m !== 0 || x !== 0) all = false;
    }
    R.u_validation = { pairsChecked: samples.length, allMatch: all };
  }
  const witnesses: any[] = [];
  function run(name: string, iter: (cb: (Rm: number[], P: Pt[]) => void) => void) {
    let cand = 0, safe = 0, max = 0;
    iter((Rm, P) => {
      cand++;
      if (!M.safeCheck(Rm, P)) return;
      safe++;
      if (M.maximalCheck(Rm, P) === null) { max++; witnesses.push({ case: name, removed: Rm.map(i => M.BASE[i]), added: P }); }
    });
    R[name] = { candidates: cand, safe: safe, maximal: max };
  }
  run("c1a_Toccupancy", cb => {
    for (let s = 0; s < M.N; s++) cb([s], [M.T]);
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) cb([i, j], [M.T]);
  });
  run("c1b_1new_on_k3", cb => {
    for (const rec of k3c) {
      const off = rec.offIdx;
      for (const z of rec.emptyCells) {
        for (const s of off) cb([s], [z]);
        for (let a = 0; a < off.length; a++) for (let b = a+1; b < off.length; b++) cb([off[a], off[b]], [z]);
      }
    }
  });
  run("c2c_2new_on_k3_1curveRemoval", cb => {
    for (const rec of k3c) {
      const cs = rec.emptyCells, off = rec.offIdx;
      for (let a = 0; a < cs.length; a++) for (let b = a+1; b < cs.length; b++)
        for (const csi of rec.stoneIdx) for (const e of off) cb([csi, e], [cs[a], cs[b]]);
    }
  });
  run("c2d_2new_on_k2", cb => {
    for (const rec of k2c) {
      const cs = rec.emptyCells; if (cs.length < 2) continue;
      const off = rec.offIdx;
      for (let a = 0; a < cs.length; a++) for (let b = a+1; b < cs.length; b++)
        for (let i = 0; i < off.length; i++) for (let j = i+1; j < off.length; j++) cb([off[i], off[j]], [cs[a], cs[b]]);
    }
  });
  const ALLCELLS: Pt[] = [];
  for (let y = 0; y < 7; y++) for (let x = 0; x < 38; x++) ALLCELLS.push([x, y]);
  const emptyKeySet = new Set(M.EMPTY.map(M.eKey));
  const coCover = new Map<string, Set<string>>();
  const ensure = (m: Map<string, Set<string>>, k: string) => { let s = m.get(k); if (!s) { s = new Set<string>(); m.set(k, s); } return s; };
  for (const cv of M.tab.values()) {
    if (cv.cnt !== 3 && cv.cnt !== 4) continue;
    const cells = ALLCELLS.filter(c => onCurve(cv, c[0], c[1]));
    for (const e of cells) {
      const s = ensure(coCover, M.eKey(e));
      for (const z of cells) if (z[0] !== e[0] || z[1] !== e[1]) if (emptyKeySet.has(M.eKey(z))) s.add(M.eKey(z));
    }
  }
  const coCoverK2T = new Map<string, Set<string>>();
  for (const rec of k2c) {
    const cv = rec.cv;
    const cells = ALLCELLS.filter(c => onCurve(cv, c[0], c[1]));
    const ec = cells.filter(c => emptyKeySet.has(M.eKey(c)));
    for (const e of cells) {
      const s = ensure(coCoverK2T, M.eKey(e));
      for (const z of ec) if (z[0] !== e[0] || z[1] !== e[1]) s.add(M.eKey(z));
    }
  }
  const row0Empty = M.EMPTY.filter(e => e[1] === 0 && !M.isT(e));
  const J = new Map<string, Map<string, Set<string>>>();
  for (const z1 of row0Empty) {
    const m = new Map<string, any>();
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) { const cv = curveThru(z1, M.BASE[i], M.BASE[j]); if (!m.has(cv.k)) m.set(cv.k, cv); }
    const jm = new Map<string, Set<string>>();
    for (const cv of m.values()) {
      if (M.countBase(cv) !== 2) continue;
      const cells = ALLCELLS.filter(c => onCurve(cv, c[0], c[1]));
      for (const e of cells) {
        const s = ensure(jm, M.eKey(e));
        for (const z of cells) if ((z[0] !== e[0] || z[1] !== e[1]) && emptyKeySet.has(M.eKey(z)) && !(z[0] === z1[0] && z[1] === z1[1])) s.add(M.eKey(z));
      }
    }
    J.set(M.eKey(z1), jm);
  }
  const emptyByKey = new Map<string, Pt>(); M.EMPTY.forEach(e => emptyByKey.set(M.eKey(e), e));
  const lineBaseSet = new Set(k3c.filter(r => r.cv.t === "L").flatMap(r => r.stoneIdx));
  const offLineStones: number[] = [];
  for (let i = 0; i < M.N; i++) if (M.BASE[i][1] !== 0) offLineStones.push(i);
  const offPairs: [number, number][] = [];
  for (let a = 0; a < offLineStones.length; a++) for (let b = a+1; b < offLineStones.length; b++) offPairs.push([offLineStones[a], offLineStones[b]]);
  const offEmpty = M.EMPTY.filter(e => !M.isT(e) && e[1] !== 0);
  function tryCandidate(Rm: number[], P: Pt[], stat: any): void {
    stat.cand++;
    if (!M.safeCheck(Rm, P)) return;
    stat.safe++;
    if (M.maximalCheck(Rm, P) === null) witnesses.push({ case: stat.name, removed: Rm.map(i => M.BASE[i]), added: P });
  }
  {
    const stat: any = { name: "c2a_Toccupancy_z2", pairs: 0, pairsSkippedEmptyIntersection: 0, pairsFreeZ2: 0, cand: 0, safe: 0, maximal: 0 };
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) {
      const U = Uof(i, j);
      const lineIntact = !lineBaseSet.has(i) && !lineBaseSet.has(j);
      const Up = U.filter(e => !(lineIntact && e.endsWith(",0") && !M.bIdx.has(e)));
      let z2cand: string[];
      if (Up.length === 0) { z2cand = M.EMPTY.filter(e => !M.isT(e)).map(M.eKey); stat.pairsFreeZ2++; }
      else {
        let acc: Set<string> | null = null; let emptyI = false;
        for (const e of Up) {
          const s1 = coCover.get(e) || new Set<string>();
          const s2 = coCoverK2T.get(e) || new Set<string>();
          const u = new Set<string>([...s1, ...s2]);
          if (u.size === 0) { emptyI = true; break; }
          if (acc === null) acc = u; else { const nx = new Set<string>(); for (const v of acc) if (u.has(v)) nx.add(v); acc = nx; }
          if (acc.size === 0) { emptyI = true; break; }
        }
        if (emptyI) { stat.pairsSkippedEmptyIntersection++; stat.pairs++; continue; }
        z2cand = [...acc].filter(z => z !== "37,0");
      }
      stat.pairs++;
      for (const zk of z2cand) tryCandidate([i, j], [M.T, emptyByKey.get(zk) as Pt], stat);
    }
    R.c2a = stat;
  }
  {
    const stat: any = { name: "c2b_1onLine_z2", combos: 0, combosSkipped: 0, combosFreeZ2: 0, cand: 0, safe: 0, maximal: 0 };
    for (const [pi, pj] of offPairs) {
      const U = Uof(pi, pj);
      for (const z1 of row0Empty) {
        const dz = M.danger(z1);
        const Up: string[] = [];
        for (const e of U) {
          let covered = false;
          for (const cv of dz) {
            let r = 0; for (const s of [pi, pj]) if (cv.mem[s]) r++;
            if ((cv.bc === 3 && r === 0) || (cv.bc === 4 && r === 1)) {
              const pt = emptyByKey.has(e) ? (emptyByKey.get(e) as Pt) : (M.BASE.find(b => M.eKey(b) === e) as Pt);
              if (onCurve(cv, pt[0], pt[1])) { covered = true; break; }
            }
          }
          if (!covered) Up.push(e);
        }
        stat.combos++;
        let z2cand: string[];
        if (Up.length === 0) { z2cand = offEmpty.map(M.eKey); stat.combosFreeZ2++; }
        else {
          const jm = J.get(M.eKey(z1)) as Map<string, Set<string>>;
          let acc: Set<string> | null = null; let emptyI = false;
          for (const e of Up) {
            const s1 = coCover.get(e) || new Set<string>();
            const s2 = jm.get(e) || new Set<string>();
            const u = new Set<string>([...s1, ...s2]);
            if (u.size === 0) { emptyI = true; break; }
            if (acc === null) acc = u; else { const nx = new Set<string>(); for (const v of acc) if (u.has(v)) nx.add(v); acc = nx; }
            if (acc.size === 0) { emptyI = true; break; }
          }
          if (emptyI) { stat.combosSkipped++; continue; }
          z2cand = [...acc];
        }
        for (const zk of z2cand) tryCandidate([pi, pj], [z1, emptyByKey.get(zk) as Pt], stat);
      }
    }
    R.c2b = stat;
  }
  // ===== skip audits: fully re-enumerate sampled pruned units =====
  {
    const audits: any[] = [];
    const pairSamples = [3, 17, 42, 88, 131, 199, 240, 269];
    for (const p of pairSamples) {
      const [pi, pj] = offPairs[p];
      const U = Uof(pi, pj);
      let found = 0;
      for (let z1i = 0; z1i < row0Empty.length; z1i += 7) {
        const z1 = row0Empty[z1i];
        const dz = M.danger(z1);
        const Up: string[] = [];
        for (const e of U) {
          let covered = false;
          for (const cv of dz) {
            let r = 0; for (const s of [pi, pj]) if (cv.mem[s]) r++;
            if ((cv.bc === 3 && r === 0) || (cv.bc === 4 && r === 1)) {
              const pt = emptyByKey.has(e) ? (emptyByKey.get(e) as Pt) : (M.BASE.find(b => M.eKey(b) === e) as Pt);
              if (onCurve(cv, pt[0], pt[1])) { covered = true; break; }
            }
          }
          if (!covered) Up.push(e);
        }
        if (Up.length === 0) continue;
        const jm = J.get(M.eKey(z1)) as Map<string, Set<string>>;
        let acc: Set<string> | null = null; let emptyI = false;
        for (const e of Up) {
          const s1 = coCover.get(e) || new Set<string>();
          const s2 = jm.get(e) || new Set<string>();
          const u = new Set<string>([...s1, ...s2]);
          if (u.size === 0) { emptyI = true; break; }
          if (acc === null) acc = u; else { const nx = new Set<string>(); for (const v of acc) if (u.has(v)) nx.add(v); acc = nx; }
          if (acc.size === 0) { emptyI = true; break; }
        }
        if (emptyI) {
          let cand = 0, safe = 0, max = 0;
          for (const z2 of offEmpty) {
            cand++;
            if (!M.safeCheck([pi, pj], [z1, z2])) continue;
            safe++;
            if (M.maximalCheck([pi, pj], [z1, z2]) === null) max++;
          }
          audits.push({ pairIdx: p, z1: z1, fullCandidates: cand, safe: safe, maximal: max });
          found++;
        }
        if (found >= 2) break;
      }
    }
    const pairList: [number, number][] = [];
    for (let i = 0; i < M.N; i++) for (let j = i+1; j < M.N; j++) pairList.push([i, j]);
    const c2aAuditPairs = [11, 77, 150, 228, 303, 340];
    for (const p of c2aAuditPairs) {
      const [pi, pj] = pairList[p];
      let cand = 0, safe = 0, max = 0;
      for (const z2 of M.EMPTY) {
        if (M.isT(z2)) continue;
        cand++;
        if (!M.safeCheck([pi, pj], [M.T, z2])) continue;
        safe++;
        if (M.maximalCheck([pi, pj], [M.T, z2]) === null) max++;
      }
      audits.push({ c2aPairIdx: p, fullCandidates: cand, safe: safe, maximal: max });
    }
    R.skip_audits = { audits: audits, allGroundTruthMaximalZero: audits.every((a: any) => a.maximal === 0) };
  }
  const verified: any[] = [];
  for (const w of witnesses) {
    const st = sortSt(M.BASE.filter((s) => !w.removed.some((r: Pt) => r[0] === s[0] && r[1] === s[1])).concat(w.added as Pt[]));
    const tab = buildTable(st);
    const maxC = Math.max(...[...tab.values()].map(c => c.cnt));
    const unc38 = uncoveredAt(st, 38, 4);
    verified.push({ case: w.case, removed: w.removed, added: w.added, n: st.length, rows: rowsOf(st), maxCurve: maxC, maximal_on_7x38: unc38.length === 0 && maxC <= 4, unc38: unc38, unc39_profile: uncoveredAt(st, 39, 4) });
  }
  R.witnesses = verified;
  return R;
}
main();
