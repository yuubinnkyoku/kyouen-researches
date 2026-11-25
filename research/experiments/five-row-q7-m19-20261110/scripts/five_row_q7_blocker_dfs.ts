// five_row_q7_blocker_dfs.ts — blocker-obligation-fill DFS machine for M_{5,7} (5×m, q=7)
// Reproduces (run in the Vibe sandbox via run_typescript):
//   1. 5×18 witness reproduction with S0={5,8,12,14,17} (49,162 nodes, exact repo witness rows)
//   2. New 5×18 witness (2nd, mirror-inequivalent)
//   3. 5×19 S0={5,8,12,14,17} nonexistence (769 nodes, 0 witnesses)
//   4. Campaign slice for 5×19 class {0}: canonical case order, resumable via nextIdx
// Usage: set MODE / START / NODE_CAP, then run. Circle key = center AND radius, with
// (Ux,Uy,D) gcd-normalized, then R2n/R2d gcd-normalized SEPARATELY (joint normalization
// is scale-dependent and wrong). Node budget per run_typescript call: ~400k DFS nodes.

function gcd(a: number, b: number): number { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; }

async function main() {
  // ---- configuration ----
  const W = 5;                    // rows
  const M = 19;                   // columns (use 18 for witness reproduction)
  const MODE = 'campaign';        // 'single' (S0 given) | 'campaign' (class-{0} slice)
  const SINGLE_S0 = [5, 8, 12, 14, 17];
  const START = 262;              // campaign resume index (cases 0..START-1 already done)
  const NODE_CAP = 400_000;
  const Y0 = 0, CAP = 5;         // deficient row 0, cap 5 stones; other rows exactly 6
  // -----------------------
  const N = W * M;
  const xs = new Int32Array(N), ys = new Int32Array(N);
  for (let y = 0; y < W; y++) for (let x = 0; x < M; x++) { xs[x + M * y] = x; ys[x + M * y] = y; }
  // census of circles with >= 7 grid points (5×19: 95; 5×18: 84)
  const circles: number[][] = [];
  {
    const buf = new Int32Array(16);
    const circSeen = new Set<string>();
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
      for (let p = 0; p < N; p++) {
        const vx = xs[p] * D - Ux, vy = ys[p] * D - Uy;
        if (vx * vx + vy * vy === R2n) buf[m++] = p;
      }
      if (m >= 7) { circSeen.add(key); const c: number[] = []; for (let q = 0; q < m; q++) c.push(buf[q]); circles.push(c); }
    }
  }
  const nC = circles.length;
  const ptCirc: number[][] = Array.from({ length: N }, () => []);
  for (let ci = 0; ci < nC; ci++) for (const p of circles[ci]) ptCirc[p].push(ci);
  const rowPts: number[][] = [];
  for (let y = 0; y < W; y++) { const r: number[] = []; for (let x = 0; x < M; x++) r.push(x + M * y); rowPts.push(r); }
  const forced = new Int8Array(N);   // 0 unknown, 1 stone, 2 empty
  const assigned = new Uint8Array(N);
  const rowStone = new Int8Array(W);
  const circStone = new Int8Array(nC);
  const trail: number[] = [];
  function push0(type: number, idx: number, prev: number) { trail.push(type, idx, prev); }
  function forceStone(p: number): boolean {
    if (forced[p] === 2) return false;
    if (forced[p] === 1) return true;
    push0(0, p, 0); forced[p] = 1;
    const y = ys[p];
    push0(1, y, rowStone[y]); rowStone[y]++;
    const rc = y === Y0 ? CAP : 6;
    if (rowStone[y] > rc) return false;
    if (rowStone[y] === rc) {
      for (const q of rowPts[y]) if (forced[q] === 0) { if (!forceEmpty(q)) return false; }
    }
    for (const ci of ptCirc[p]) {
      push0(2, ci, circStone[ci]); circStone[ci]++;
      if (circStone[ci] > 6) return false;
      if (circStone[ci] === 6) {
        for (const q of circles[ci]) if (q !== p && forced[q] === 0) { if (!forceEmpty(q)) return false; }
      }
    }
    return true;
  }
  function forceEmpty(p: number): boolean {
    if (forced[p] === 1) return false;
    if (forced[p] === 2) return true;
    push0(0, p, 0); forced[p] = 2;
    return true;
  }
  function undoTo(mark: number) {
    while (trail.length > mark) {
      const prev = trail.pop()!, idx = trail.pop()!, type = trail.pop()!;
      if (type === 0) forced[idx] = prev;
      else if (type === 1) rowStone[idx] = prev;
      else if (type === 2) circStone[idx] = prev;
      else assigned[idx] = prev;
    }
  }
  let nodes = 0, witnesses = 0, capped = false, leaves = 0;
  const witnessList: number[][][] = [];
  function fillRows(row: number): boolean {
    if (row === Y0) return fillRows(row + 1);
    if (row === W) {
      const rows: number[][] = [[], [], [], [], []];
      for (let p = 0; p < N; p++) if (forced[p] === 1) rows[ys[p]].push(xs[p]);
      witnesses++;
      if (witnessList.length < 20) witnessList.push(rows);
      return false;
    }
    nodes++;
    if (nodes > NODE_CAP) { capped = true; return true; }
    const need = 6 - rowStone[row];
    const unk: number[] = [];
    for (const q of rowPts[row]) if (forced[q] === 0) unk.push(q);
    if (unk.length < need) return false;
    return fillComb(row, unk, 0, need);
  }
  function fillComb(row: number, unk: number[], start: number, need: number): boolean {
    if (need === 0) return fillRows(row + 1);
    nodes++;
    if (nodes > NODE_CAP) { capped = true; return true; }
    for (let i = start; i <= unk.length - need; i++) {
      const q = unk[i];
      const mark = trail.length;
      if (forceStone(q)) { if (fillComb(row, unk, i + 1, need - 1)) return true; }
      undoTo(mark);
      if (capped) return true;
    }
    return false;
  }
  function tryBlocker(p: number, ci: number): boolean {
    const C = circles[ci];
    push0(3, p, assigned[p]); assigned[p] = 1;
    if (C.length === 7) {
      for (const q of C) if (q !== p) { if (!forceStone(q)) return false; }
      return dfs();
    }
    let e0 = 0; const unknowns: number[] = [];
    for (const q of C) {
      if (q === p) continue;
      if (forced[q] === 2) e0++;
      else if (forced[q] === 0) unknowns.push(q);
    }
    if (e0 >= 2) return false;
    if (e0 === 1) {
      for (const q of unknowns) { if (!forceStone(q)) return false; }
      return dfs();
    }
    for (const q of unknowns) {
      const mark = trail.length;
      if (forceEmpty(q)) {
        let ok = true;
        for (const r of unknowns) { if (r !== q && !forceStone(r)) { ok = false; break; } }
        if (ok) { if (dfs()) return true; }
      }
      undoTo(mark);
      if (capped) return true;
    }
    return false;
  }
  function optionsFor(p: number): number[] {
    const opts: number[] = [];
    for (const ci of ptCirc[p]) {
      const C = circles[ci];
      if (C.length === 7) {
        let ok = true;
        for (const q of C) if (q !== p && forced[q] === 2) { ok = false; break; }
        if (ok) opts.push(ci);
      } else {
        let e0 = 0;
        for (const q of C) { if (q === p) continue; if (forced[q] === 2) e0++; }
        if (e0 <= 1) opts.push(ci);
      }
    }
    return opts;
  }
  function dfs(): boolean {
    nodes++;
    if (nodes > NODE_CAP) { capped = true; return true; }
    let selPt = -1, selOptCount = -1;
    const selOptArr: number[] = [];
    for (let i = 0; i < N; i++) {
      if (ys[i] !== Y0) continue;
      if (forced[i] === 1) continue;
      if (forced[i] === 2 && assigned[i]) continue;
      const optArr = optionsFor(i);
      if (optArr.length === 0) return false;
      if (selOptCount === -1 || optArr.length < selOptCount) {
        selOptCount = optArr.length; selPt = i;
        selOptArr.length = 0; for (const v of optArr) selOptArr.push(v);
      }
      if (selOptCount === 1) break;
    }
    if (selPt === -1) { leaves++; return fillRows(0); }
    for (const ci of selOptArr) {
      const mark = trail.length;
      if (tryBlocker(selPt, ci)) return true;
      undoTo(mark);
      if (capped) return true;
    }
    return false;
  }
  function runCase(s0: number[]) {
    const mark = trail.length;
    let ok = true;
    for (const x of s0) { if (!forceStone(x + M * Y0)) { ok = false; break; } }
    if (ok) for (let x = 0; x < M; x++) if (!s0.includes(x)) { if (!forceEmpty(x + M * Y0)) { ok = false; break; } }
    if (ok) dfs();
    undoTo(mark);
  }
  if (MODE === 'single') {
    runCase(SINGLE_S0);
    return { nC, nodes, leaves, witnesses, witnessList };
  }
  // campaign: canonical case order k=5..0, lex within k, mirror reps only
  const allCases: number[][] = [];
  function gen(k: number) {
    const cur: number[] = [];
    const rec = (start: number) => {
      if (cur.length === k) { allCases.push([...cur]); return; }
      for (let x = start; x < M; x++) { cur.push(x); rec(x + 1); cur.pop(); }
    };
    rec(0);
  }
  for (let k = 5; k >= 0; k--) gen(k);
  const mir = (s: number[]) => s.map(x => M - 1 - x).sort((a, b) => a - b);
  const reps: number[][] = [];
  for (const s of allCases) {
    const m0 = mir(s);
    if (s.join(',') <= m0.join(',')) reps.push(s);
  }
  let done = 0, idx = START;
  const perKDone: Record<number, number> = {};
  for (; idx < reps.length; idx++) {
    runCase(reps[idx]);
    if (!capped) { done++; perKDone[reps[idx].length] = (perKDone[reps[idx].length] || 0) + 1; }
    else break;
  }
  return { nC, repsTotal: reps.length, done, nextIdx: START + done, capped, nodes, leaves, witnesses, witnessList, perKDone };
}
// main() is invoked by the sandbox runner; result includes witnesses (row lists) and nextIdx.
