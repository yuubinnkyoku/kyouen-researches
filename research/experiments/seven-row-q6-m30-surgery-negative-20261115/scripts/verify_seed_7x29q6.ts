async function main() {
  // research/experiments/seven-row-q6-m30-surgery-negative-20261115/scripts/verify_seed_7x29q6.ts
  // (7,6) m=29 seed の新規独立検証 + T=(29,3) センサス + T-blocker 手術ケース数の再導出 + 完全性ギャップの定量化
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
  // seed = s7x29q6.witness.json (34 stones, rows [5,5,5,4,5,5,5])
  const S6: Pt[] = [[9,0],[14,0],[19,0],[20,0],[21,0],[2,1],[8,1],[10,1],[13,1],[22,1],[7,2],[10,2],[13,2],[19,2],[22,2],[3,3],[8,3],[11,3],[27,3],[1,4],[5,4],[7,4],[8,4],[14,4],[4,5],[6,5],[19,5],[20,5],[25,5],[7,6],[8,6],[11,6],[17,6],[22,6]];
  const sortSt = (st: Pt[]): Pt[] => st.slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]);
  const rowsOf = (st: Pt[]): number[] => { const r = [0,0,0,0,0,0,0]; for (const s of st) r[s[1]]++; return r; };
  const R: any = {};
  {
    const t1 = buildTable([[0,0],[1,0],[2,0],[3,0],[4,0]]);
    const t2 = buildTable([[5,0],[0,5],[3,4],[4,3],[-5,0]]);
    const t3 = buildTable([[0,0],[1,0],[2,0],[3,0],[10,5]]);
    const mx = (t: Map<string,any>) => Math.max(...[...t.values()].map(c => c.cnt));
    R.controls = { collinear5_detected: mx(t1) === 5, concyclic5_detected: mx(t2) === 5, line4_not5: mx(t3) === 4, circle_dedup: buildTable([[3,0],[0,3],[-3,0],[0,-3]]).size === 1 };
  }
  const stones = sortSt(S6);
  const tab = buildTable(stones);
  const N = stones.length;
  R.seed = { stones: stones, n: N, rows: rowsOf(stones), maxX: Math.max(...stones.map(s => s[0])), safe_maxCurve: Math.max(...[...tab.values()].map(c => c.cnt)), uncovered: {} as any };
  for (const W of [29, 30, 31]) R.seed.uncovered[String(W)] = uncoveredAt(stones, W, 5);
  const T: Pt = [29, 3];
  const countStones = (cv: any): number => { let c = 0; for (const s of stones) if (onCurve(cv, s[0], s[1])) c++; return c; };
  const twoM = new Map<string, any>();
  for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) {
    const cv = curveThru(T, stones[i], stones[j]);
    if (!twoM.has(cv.k)) twoM.set(cv.k, cv);
  }
  const k4: any[] = [], k3: any[] = [], twoStone: any[] = [];
  for (const cv of twoM.values()) {
    const c = countStones(cv);
    if (c === 4) k4.push(cv); else if (c === 3) k3.push(cv); else if (c === 2) twoStone.push(cv);
  }
  R.T_census = { T: T, fourStoneTCurves: k4.map(c => fmt(c)), threeStoneTCurves: k3.length, twoStoneTCurves: twoStone.length };
  const emptyOnBoard = (x: number, y: number, W: number): boolean => x >= 0 && x < W && y >= 0 && y < 7 && !stones.some(s => s[0] === x && s[1] === y);
  const lineCells: Pt[] = [];
  for (let y = 0; y < 7; y++) for (let x = 0; x < 30; x++) if (emptyOnBoard(x, y, 30) && onCurve(k4[0], x, y)) lineCells.push([x, y]);
  R.T_census.fourStoneCurveEmptyCellsOn7x30 = { curve: fmt(k4[0]), count: lineCells.length };
  const k3PairsAll: [Pt, Pt][] = [];
  const seen = new Set<string>();
  for (const cv of k3) {
    const cells: Pt[] = [];
    for (let y = 0; y < 7; y++) for (let x = 0; x < 30; x++) if (emptyOnBoard(x, y, 30) && onCurve(cv, x, y)) cells.push([x, y]);
    for (let i = 0; i < cells.length; i++) for (let j = i+1; j < cells.length; j++) { const kk = cells[i][0]+","+cells[i][1]+"|"+cells[j][0]+","+cells[j][1]; if (!seen.has(kk)) { seen.add(kk); k3PairsAll.push([cells[i], cells[j]]); } }
  }
  const k3PairsExclT = k3PairsAll.filter(pr => !(pr[0][0]===29 && pr[0][1]===3) && !(pr[1][0]===29 && pr[1][1]===3));
  R.T_census.k3SpPairsOn7x30 = { total: k3PairsAll.length, excludingT: k3PairsExclT.length, pairsExcludingT: k3PairsExclT, note: "pairs including T=(29,3) are subsumed by the T-occupancy case" };
  const spCount = lineCells.length;
  const empty30 = 210 - N;
  const pairsN = N * (N - 1) / 2;
  R.enumerated_session_cases = {
    q: 6, NEED_for_maximality: 5,
    TOcc_sp_count: empty30 - 1, TOcc_candidates: (empty30 - 1) * pairsN, TOcc_expected_98175: (empty30 - 1) * pairsN === 98175,
    one_swap_sp_count: spCount, one_swap_candidates: spCount * N, one_swap_expected_884: spCount * N === 884,
    two_remove_one_add_candidates: spCount * pairsN, two_remove_one_add_expected_14586: spCount * pairsN === 14586,
    case_b_sp_pairs: k3PairsExclT.length, case_b_candidates: k3PairsExclT.length * pairsN, case_b_expected_561: k3PairsExclT.length * pairsN === 561,
    enumerated_total: (empty30 - 1) * pairsN + spCount * N + spCount * pairsN + k3PairsExclT.length * pairsN,
    session_result: "0 witnesses in all four cases (session record; not re-run here)",
  };
  // completeness analysis of the (2,2) T-blocked space with T not in P:
  // blocking a curve through T needs post-count >= 5. Base counts: line y=3 has 4, k3 curves have 3, others <= 2.
  //  - line, 1 new stone (other new off-line), 0 line-stone removals: 4+1 = 5  -> SAFE-blocking case NOT in the session list
  //  - line, 2 new stones, 0 removals: 4+2 = 6 = q -> unsafe (structural exclusion)
  //  - line, 2 new stones, exactly 1 line-stone removal: 4-1+2 = 5 -> SAFE-blocking case NOT in the session list
  //  - line, 1 new stone, >=1 removal: 4-1+1 = 4 < 5 -> not blocking
  //  - k3, both new stones, 0 removals: 3+2 = 5 -> case-b (enumerated, 561)
  //  - k3, anything else: < 5 -> not blocking
  const lineExclT = lineCells.filter(c => !(c[0] === 29 && c[1] === 3));
  const offLineEmpty = empty30 - lineCells.length;
  const lineStones = stones.filter(s => s[1] === 3).length;
  const offLineStones = N - lineStones;
  const c2 = (n: number) => n * (n - 1) / 2;
  R.completeness_gap = {
    finding: "the session four cases do NOT cover the full (2,2) T-blocking space: the line-based cases (the q=6 analogue of the (7,5) case-a) are missing",
    line_cells_excluding_T: lineExclT.length,
    off_line_empty_cells: offLineEmpty,
    off_line_stones: offLineStones,
    gap_1new_on_line: lineExclT.length * offLineEmpty * c2(offLineStones),
    gap_2new_on_line_1removal: c2(lineExclT.length) * lineStones * offLineStones,
    gap_total: lineExclT.length * offLineEmpty * c2(offLineStones) + c2(lineExclT.length) * lineStones * offLineStones,
    structural_exclusions: "both-new-on-line with 0 line removals gives 4+2=6=q (unsafe); 1-new-on-line with a line removal gives 4 (not blocking); k3 with 1 new gives 4 (not blocking)",
    status: "newly identified in this session; enumeration is the top next task (about 1.67M candidates; per-candidate safety+maximality needed)",
  };
  return R;
}
main();
