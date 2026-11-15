async function main() {
  // research/experiments/seven-row-q5-m37-surgery-20261115/scripts/verify_and_campaign.ts
  // (7,5) 7x37 witness winC の独立検証 + 2編集surgery軽量ケース（A/F/b/b2a1）の完全再列挙
  // 純TS・完全整数演算・repoコード不使用・census不使用・SAT不使用
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
  const fmt = (cv: any) => cv.t === "L" ? cv.a + "x+" + cv.b + "y+" + cv.c + "=0" : cv.d0 + "(x^2+y^2)+" + cv.d1 + "x+" + cv.d2 + "y+" + cv.d3 + "=0";
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
  const rowsOf = (st: Pt[]): number[] => { const r = [0,0,0,0,0,0,0]; for (const s of st) r[s[1]]++; return r; };
  const sortSt = (st: Pt[]): Pt[] => st.slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]);

  const WINA: Pt[] = sortSt([[8,0],[18,0],[30,0],[5,1],[24,1],[28,1],[32,1],[0,2],[9,2],[22,2],[28,2],[14,3],[15,3],[21,3],[30,3],[16,4],[26,4],[30,4],[2,4],[3,5],[8,5],[21,5],[22,5],[15,6],[16,6],[18,6],[25,6]]);
  const WINC: Pt[] = sortSt(WINA.filter(s => !(s[0]===8&&s[1]===5) && !(s[0]===16&&s[1]===6)).concat([[24,5],[22,6]] as Pt[]));
  const BASE33: Pt[] = sortSt(WINA.filter(s => !(s[0]===8&&s[1]===5) && !(s[0]===2&&s[1]===4)).concat([[25,5],[20,4]] as Pt[]));

  const R: any = {};
  {
    const t1 = buildTable([[0,0],[1,0],[2,0],[3,0],[4,0]]);
    const t2 = buildTable([[5,0],[0,5],[3,4],[4,3],[-5,0]]);
    const t3 = buildTable([[0,0],[1,0],[2,0],[3,0],[10,5]]);
    const mx = (t: Map<string,any>) => Math.max(...[...t.values()].map(c => c.cnt));
    R.controls = { collinear5_detected: mx(t1) === 5, concyclic5_detected: mx(t2) === 5, line4_not5: mx(t3) === 4, circle_dedup: buildTable([[3,0],[0,3],[-3,0],[0,-3]]).size === 1 };
  }
  const tabC = buildTable(WINC); const needC: any[] = []; for (const cv of tabC.values()) if (cv.cnt >= 4) needC.push(cv);
  R.winC = {
    stones: WINC, n: WINC.length, rows: rowsOf(WINC), maxX: Math.max(...WINC.map(s => s[0])),
    surgeryFromWinA: "winA - (8,5) - (16,6) + (24,5) + (22,6)",
    safe_maxCurve: Math.max(...[...tabC.values()].map(c => c.cnt)), needCurves: needC.length,
    uncovered: {} as any,
    T34_blockers: needC.filter(cv => onCurve(cv, 34, 0)).map(fmt),
  };
  for (const W of [33,34,35,36,37,38]) R.winC.uncovered[String(W)] = uncoveredAt(WINC, W, 4);
  R.base33 = { safe: Math.max(...[...buildTable(BASE33).values()].map(c => c.cnt)), unc33: uncoveredAt(BASE33, 33, 4), unc34: uncoveredAt(BASE33, 34, 4) };
  R.winA = { safe: Math.max(...[...buildTable(WINA).values()].map(c => c.cnt)), unc34: uncoveredAt(WINA, 34, 4), unc35: uncoveredAt(WINA, 35, 4) };

  const W = 35, Q = 5, NEED = 4;
  const T: Pt = [34, 0];
  const BASE = WINA;
  const N = BASE.length;
  const bIdx = new Map<string, number>(); BASE.forEach((s, i) => bIdx.set(s[0] + "," + s[1], i));
  const EMPTY: Pt[] = [];
  for (let y = 0; y < 7; y++) for (let x = 0; x < W; x++) if (!bIdx.has(x + "," + y)) EMPTY.push([x, y]);
  const eKey = (p: Pt) => p[0] + "," + p[1];
  const isT = (p: Pt) => p[0] === 34 && p[1] === 0;
  const baseTable = buildTable(BASE);
  const baseNeed: any[] = [];
  for (const cv of baseTable.values()) if (cv.cnt >= NEED) { cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; baseNeed.push(cv); }
  const BL: number[][] = EMPTY.map(e => { const l: number[] = []; baseNeed.forEach((cv, ci) => { if (onCurve(cv, e[0], e[1])) l.push(ci); }); return l; });
  const k3: any[] = [];
  for (const cv of baseTable.values()) if (onCurve(cv, T[0], T[1]) && cv.cnt === 3) { cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; k3.push(cv); }
  const tCells3set = new Set<string>();
  for (const cv of k3) for (const e of EMPTY) if (onCurve(cv, e[0], e[1])) tCells3set.add(eKey(e));
  const tCells3: Pt[] = [...tCells3set].map(s => s.split(",").map(Number) as Pt);
  const countBase = (cv: any): number => { let c = 0; for (let i = 0; i < N; i++) if (onCurve(cv, BASE[i][0], BASE[i][1])) c++; return c; };
  const twoKeys = new Map<string, any>();
  for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) {
    const cv = curveThru(T, BASE[i], BASE[j]);
    if (countBase(cv) === 2 && !twoKeys.has(cv.k)) twoKeys.set(cv.k, cv);
  }
  const spPairs: [Pt, Pt][] = []; const seen = new Set<string>();
  for (const cv of twoKeys.values()) {
    const cells = EMPTY.filter(e => onCurve(cv, e[0], e[1]) && !isT(e));
    for (let i = 0; i < cells.length; i++) for (let j = i+1; j < cells.length; j++) {
      const kk = eKey(cells[i]) + "|" + eKey(cells[j]);
      if (!seen.has(kk)) { seen.add(kk); spPairs.push([cells[i], cells[j]]); }
    }
  }
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
  const stCache: (any[] | undefined)[] = new Array(N).fill(undefined);
  function stoneCurves(s: number): any[] {
    let d = stCache[s];
    if (d) return d;
    const m = new Map<string, any>();
    for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) { const cv = curveThru(BASE[s], BASE[i], BASE[j]); if (!m.has(cv.k)) m.set(cv.k, cv); }
    d = [];
    for (const cv of m.values()) { const c = countBase(cv); if (c >= 3) { cv.bc = c; cv.mem = new Uint8Array(N); for (let i = 0; i < N; i++) cv.mem[i] = onCurve(cv, BASE[i][0], BASE[i][1]) ? 1 : 0; d.push(cv); } }
    stCache[s] = d;
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
    if (!occ.has("34,0") && !tBlocked(Rm, P)) return T;
    for (let ei = 0; ei < EMPTY.length; ei++) {
      if (occ.has(eKey(EMPTY[ei]))) continue;
      if (isT(EMPTY[ei])) continue;
      if (!emptyBlocked(ei, Rm, P)) return EMPTY[ei];
    }
    return null;
  }
  const cases: any = {};
  function run(name: string, iter: (cb: (Rm: number[], P: Pt[]) => void) => void) {
    let cand = 0, safe = 0, max = 0; const witnesses: any[] = [];
    iter((Rm, P) => {
      cand++;
      if (!safeCheck(Rm, P)) return;
      safe++;
      const fail = maximalCheck(Rm, P);
      if (fail === null) { max++; if (witnesses.length < 10) witnesses.push({ removed: Rm.map(i => BASE[i]), added: P }); }
    });
    cases[name] = { candidates: cand, safe: safe, maximal: max, witnesses: witnesses };
  }
  run("A_1swap", cb => { const sps = [T].concat(tCells3); for (const sp of sps) for (let s = 0; s < N; s++) cb([s], [sp]); });
  run("F_2r1a", cb => { const sps = [T].concat(tCells3); for (const sp of sps) for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) cb([i, j], [sp]); });
  run("b_2stoneTcurve", cb => { for (const pair of spPairs) for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) cb([i, j], [pair[0], pair[1]]); });
  run("b2a1_3stoneTcurve", cb => {
    for (const cv of k3) {
      const kCells = EMPTY.filter(e => onCurve(cv, e[0], e[1]));
      const kStones: number[] = [], nonK: number[] = [];
      for (let i = 0; i < N; i++) (cv.mem[i] ? kStones : nonK).push(i);
      for (let a = 0; a < kCells.length; a++) for (let b2 = a+1; b2 < kCells.length; b2++)
        for (const s1 of kStones) for (const s2 of nonK) cb([s1, s2], [kCells[a], kCells[b2]]);
    }
  });
  R.campaign = {
    seed: "winA (7x34 witness) on board 7x35, T=(34,0), q=5, NEED=4",
    census: { baseNeedCurves: baseNeed.length, k3Tcurves: k3.length, tCells3: tCells3.length, twoStoneTCurves: twoKeys.size, spPairsOn2stoneTCurves: spPairs.length, emptyCells: EMPTY.length },
    cases: cases,
  };
  return R;
}
main();
