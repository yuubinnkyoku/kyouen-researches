// two_deficient_pair_runner.ts — 5×m・q=7 複数行欠損（2行 ≤5石・他行ちょうど6石）クラスの
// 極大安全配置完全列挙機械（K0727 blocker-obligation-fill の2行欠損一般化・ハイブリッド設計）。
//
// 設計: 外側ケース = 欠損行 Y0 の石列 S0 の鏡映代表（canonical: k=5..0・辞書順）。
// 内側 = Y0 の空点への blocker 割当 + 欠損行 Y1 の石/空の分岐 + blocker 割当。
// 葉で非欠損行をちょうど6石に fill。
// soundness/completeness: 欠損行の空点の blocker は自分の行（≤5石）でも他の行（点を含まない）
// でもあり得ないため census 円に限る。石/空+blocker の全分岐で欠損行の全点を決定する。
// NODE_CAP は global 累積（ケースごとにリセットしない）。capped ケースは次スライス先頭で再挑戦。
//
// 検証済み制御（2026-11-11、log 参照）:
//  - 全分岐版（Y1 を非欠損にして Y0 の石も分岐）は 5×18 で (5,6,6,6,6) witness を発見
//    （既知2個と異なる第3 witness、独立検証 PASS）→ 石分岐の健全性を確認。
//  - S0 事前決定なしの2行全分岐は爆発（600k ノードで葉なし）→ ハイブリッド設計が必要。
//  - 5×18・pair {0,1}・S0={5,8,12,14,17}: 17,511 ノードで完走・witness 0。
//  - 5×19・pair {0,1}: 平均 ~5.1k ノード/case・最大 28.5k（idx 0..117 を実施・全 witness 0）。
//
// 再利用: M / Y0 / Y1 / START / NODE_CAP を設定してスライス実行。
// ペアクラスは行鏡映 (y→4−y) で {0,1}≡{3,4}, {0,2}≡{2,4}, {1,2}≡{2,3},
// {0,3}≡{1,4}, {1,3}≡{1,3}, {0,4}≡{0,4} の6代表。
function gcd(a: number, b: number): number { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; }

async function main() {
  const W = 5, M = 19;
  const Y0 = 0, Y1 = 1;   // deficient-row pair class {0,1}
  const DEF_CAP = 5, FULL = 6;
  const NODE_CAP = 600_000;
  const START = 0;        // case index (canonical: k=5..0, lex, mirror reps of row-Y0 stones)
  const N = W * M;
  const xs = new Int32Array(N), ys = new Int32Array(N);
  for (let y = 0; y < W; y++) for (let x = 0; x < M; x++) { xs[x + M * y] = x; ys[x + M * y] = y; }
  const circles: number[][] = [];
  { const buf = new Int32Array(16); const circSeen = new Set<string>();
    for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k = j + 1; k < N; k++) {
      const ax = xs[i], ay = ys[i], bx = xs[j], by = ys[j], cx = xs[k], cy = ys[k];
      const d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by));
      if (d === 0) continue;
      const a2 = ax * ax + ay * ay, b2 = bx * bx + by * by, c2 = cx * cx + cy * cy;
      const ux = a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by);
      const uy = a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax);
      let g = gcd(gcd(Math.abs(d), Math.abs(ux)), Math.abs(uy));
      if (d < 0) g = -g;
      const D = d / g, Ux = ux / g, Uy = uy / g;
      const R2n = (ax * D - Ux) ** 2 + (ay * D - Uy) ** 2;
      const R2d = D * D;
      const g2 = gcd(R2n, R2d);
      const key = Ux + ',' + Uy + ',' + D + ',' + (R2n / g2) + '/' + (R2d / g2);
      if (circSeen.has(key)) continue;
      let m = 0;
      for (let p = 0; p < N; p++) { const vx = xs[p] * D - Ux, vy = ys[p] * D - Uy; if (vx * vx + vy * vy === R2n) buf[m++] = p; }
      if (m >= 7) { circSeen.add(key); const c: number[] = []; for (let q = 0; q < m; q++) c.push(buf[q]); circles.push(c); }
    } }
  const nC = circles.length;
  const ptCirc: number[][] = Array.from({ length: N }, () => []);
  for (let ci = 0; ci < nC; ci++) for (const p of circles[ci]) ptCirc[p].push(ci);
  const rowPts: number[][] = [];
  for (let y = 0; y < W; y++) { const r: number[] = []; for (let x = 0; x < M; x++) r.push(x + M * y); rowPts.push(r); }
  const isDef = new Uint8Array(W); isDef[Y0] = 1; isDef[Y1] = 1;
  const forced = new Int8Array(N), assigned = new Uint8Array(N), rowStone = new Int8Array(W), circStone = new Int8Array(nC);
  const trail: number[] = [];
  function push0(type: number, idx: number, prev: number) { trail.push(type, idx, prev); }
  function forceEmpty(p: number): boolean { if (forced[p] === 1) return false; if (forced[p] === 2) return true; push0(0, p, 0); forced[p] = 2; return true; }
  function forceStone(p: number): boolean {
    if (forced[p] === 2) return false;
    if (forced[p] === 1) return true;
    push0(0, p, 0); forced[p] = 1;
    const y = ys[p]; push0(1, y, rowStone[y]); rowStone[y]++;
    const rc = isDef[y] ? DEF_CAP : FULL;
    if (rowStone[y] > rc) return false;
    if (rowStone[y] === rc) { for (const q of rowPts[y]) if (forced[q] === 0) { if (!forceEmpty(q)) return false; } }
    for (const ci of ptCirc[p]) { push0(2, ci, circStone[ci]); circStone[ci]++; if (circStone[ci] > 6) return false;
      if (circStone[ci] === 6) { for (const q of circles[ci]) if (q !== p && forced[q] === 0) { if (!forceEmpty(q)) return false; } } }
    return true;
  }
  function undoTo(mark: number) { while (trail.length > mark) { const prev = trail.pop()!, idx = trail.pop()!, type = trail.pop()!;
    if (type === 0) forced[idx] = prev; else if (type === 1) rowStone[idx] = prev; else if (type === 2) circStone[idx] = prev; else assigned[idx] = prev; } }
  let nodes = 0, witnesses = 0, capped = false, leaves = 0;
  const witnessList: number[][][] = [];
  function fillRows(row: number): boolean {
    while (row < W && isDef[row]) row++;
    if (row === W) { const rows: number[][] = [[], [], [], [], []];
      for (let p = 0; p < N; p++) if (forced[p] === 1) rows[ys[p]].push(xs[p]);
      witnesses++; if (witnessList.length < 10) witnessList.push(rows); return false; }
    nodes++; if (nodes > NODE_CAP) { capped = true; return true; }
    const need = FULL - rowStone[row]; const unk: number[] = [];
    for (const q of rowPts[row]) if (forced[q] === 0) unk.push(q);
    if (unk.length < need) return false;
    return fillComb(row, unk, 0, need);
  }
  function fillComb(row: number, unk: number[], start: number, need: number): boolean {
    if (need === 0) return fillRows(row + 1);
    nodes++; if (nodes > NODE_CAP) { capped = true; return true; }
    for (let i = start; i <= unk.length - need; i++) { const q = unk[i]; const mark = trail.length;
      if (forceStone(q)) { if (fillComb(row, unk, i + 1, need - 1)) return true; } undoTo(mark); if (capped) return true; }
    return false;
  }
  function optionsFor(p: number): number[] {
    const opts: number[] = [];
    for (const ci of ptCirc[p]) { const C = circles[ci];
      if (C.length === 7) { let ok = true; for (const q of C) if (q !== p && forced[q] === 2) { ok = false; break; } if (ok) opts.push(ci); }
      else { let e0 = 0; for (const q of C) { if (q === p) continue; if (forced[q] === 2) e0++; } if (e0 <= 1) opts.push(ci); } }
    return opts;
  }
  function tryBlocker(p: number, ci: number): boolean {
    const C = circles[ci]; push0(3, p, assigned[p]); assigned[p] = 1;
    if (!forceEmpty(p)) return false;
    if (C.length === 7) { for (const q of C) if (q !== p) { if (!forceStone(q)) return false; } return dfs(); }
    let e0 = 0; const unknowns: number[] = [];
    for (const q of C) { if (q === p) continue; if (forced[q] === 2) e0++; else if (forced[q] === 0) unknowns.push(q); }
    if (e0 >= 2) return false;
    if (e0 === 1) { for (const q of unknowns) { if (!forceStone(q)) return false; } return dfs(); }
    for (const q of unknowns) { const mark = trail.length;
      if (forceEmpty(q)) { let ok = true; for (const r of unknowns) { if (r !== q && !forceStone(r)) { ok = false; break; } } if (ok) { if (dfs()) return true; } }
      undoTo(mark); if (capped) return true; }
    return false;
  }
  function dfs(): boolean {
    nodes++; if (nodes > NODE_CAP) { capped = true; return true; }
    let selPt = -1, selOptCount = -1; const selOptArr: number[] = []; let selCanStone = false;
    for (let i = 0; i < N; i++) { if (!isDef[ys[i]]) continue;
      if (forced[i] === 1) continue;
      if (forced[i] === 2 && assigned[i]) continue;
      const optArr = optionsFor(i);
      const canStone = forced[i] === 0 && rowStone[ys[i]] < DEF_CAP;
      if (optArr.length === 0) {
        if (!canStone) return false;
        if (selOptCount === -1 || 1 < selOptCount) { selOptCount = 1; selPt = i; selCanStone = true; selOptArr.length = 0; }
        continue;
      }
      const total = canStone ? optArr.length + 1 : optArr.length;
      if (selOptCount === -1 || total < selOptCount) {
        selOptCount = total; selPt = i; selCanStone = canStone;
        selOptArr.length = 0; for (const v of optArr) selOptArr.push(v);
      }
      if (selOptCount === 1) break;
    }
    if (selPt === -1) { leaves++; return fillRows(0); }
    const mark0 = trail.length;
    if (selCanStone) { if (forceStone(selPt)) { if (dfs()) return true; } undoTo(mark0); if (capped) return true; }
    for (const ci of selOptArr) { const mark = trail.length; if (tryBlocker(selPt, ci)) return true; undoTo(mark); if (capped) return true; }
    return false;
  }
  function runCase(s0: number[]) {
    const mark = trail.length; let ok = true;
    for (const x of s0) { if (!forceStone(x + M * Y0)) { ok = false; break; } }
    if (ok) for (let x = 0; x < M; x++) if (!s0.includes(x)) { if (!forceEmpty(x + M * Y0)) { ok = false; break; } }
    if (ok) dfs(); undoTo(mark);
  }
  const allCases: number[][] = [];
  function gen(k: number) { const cur: number[] = []; const rec = (start: number) => {
    if (cur.length === k) { allCases.push([...cur]); return; }
    for (let x = start; x < M; x++) { cur.push(x); rec(x + 1); cur.pop(); } }; rec(0); }
  for (let k = 5; k >= 0; k--) gen(k);
  const mir = (s: number[]) => s.map(x => M - 1 - x).sort((a, b) => a - b);
  const reps: number[][] = [];
  for (const s of allCases) { const m0 = mir(s); if (s.join(',') <= m0.join(',')) reps.push(s); }
  let done = 0, idx = START; const perK: Record<number, number> = {};
  let nextIdx = START; let cappedCase = -1; const lastS0s: string[] = []; let maxCaseNodes = 0;
  while (idx >= 0 && idx < reps.length) {
    const before = nodes;
    runCase(reps[idx]);
    if (!capped) {
      done++; perK[reps[idx].length] = (perK[reps[idx].length] || 0) + 1;
      const cn = nodes - before; if (cn > maxCaseNodes) maxCaseNodes = cn;
      nextIdx = idx + 1;
      if (done <= 3 || done % 20 === 0) lastS0s.push(idx + ':' + reps[idx].join(',') + '(' + cn + ')');
      idx = nextIdx;
    } else { cappedCase = idx; break; }
  }
  return { nC, repsTotal: reps.length, done, nextIdx, cappedCase, witnesses, leaves, perK, lastS0s, maxCaseNodes, witnessList };
}
