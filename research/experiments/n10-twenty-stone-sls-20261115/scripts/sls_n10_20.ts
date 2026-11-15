// sls_n10_20.ts - stochastic local search for a safe 20-stone set on 10x10 (K0141).
// Final-generation engine of the 2026-11-15 sandbox runs (census variant).
// Runs as-is in the Vibe TS sandbox (run_typescript); no imports, no I/O.
// Deterministic: fixed PRNG seed + unit budget => bit-reproducible runs.
// E(S) = number of forbidden 4-subsets (concyclic or collinear) inside S; E=0 iff safe.
// Controls: F_10 quad count (expect 54441, K0057), K0035 19-stone witness safety,
// U unique bad quad, U single-swap / bounded 2-swap non-fixability.
const SEED = 0x5EEDC0DE;   // mulberry32 state; each run of the record used a distinct seed
const BUDGET = 5.0e8;       // self-counted hot-loop iteration units (sandbox safety)

async function main() {
  const N = 100;
  const px = new Uint8Array(N), py = new Uint8Array(N), pw = new Uint8Array(N);
  for (let p = 0; p < N; p++) { const x = p % 10, y = (p / 10) | 0; px[p] = x; py[p] = y; pw[p] = x * x + y * y; }
  // forbidden quads: det of difference rows (w,x,y) vs 4th point; 0 iff concyclic-or-collinear
  const qa: number[] = [], qb: number[] = [], qc: number[] = [], qd: number[] = [];
  for (let a = 0; a < N - 3; a++) {
    const wa = pw[a], xa = px[a], ya = py[a];
    for (let b = a + 1; b < N - 2; b++) {
      const bw = pw[b] - wa, bx = px[b] - xa, by = py[b] - ya;
      for (let c = b + 1; c < N - 1; c++) {
        const cw = pw[c] - wa, cx = px[c] - xa, cy = py[c] - ya;
        const A = -bx * cy + by * cx, B = bw * cy - by * cw, C = -bw * cx + bx * cw;
        for (let d = c + 1; d < N; d++) {
          if (A * (pw[d] - wa) + B * (px[d] - xa) + C * (py[d] - ya) === 0) { qa.push(a); qb.push(b); qc.push(c); qd.push(d); }
        }
      }
    }
  }
  const Q = qa.length; // control: must equal 54441 (K0057 F_10)
  // CSR incidence: per cell, list of (quad id, other-3-cells)
  const qStart = new Uint32Array(N + 1);
  for (let i = 0; i < Q; i++) { qStart[qa[i] + 1]++; qStart[qb[i] + 1]++; qStart[qc[i] + 1]++; qStart[qd[i] + 1]++; }
  for (let c = 0; c < N; c++) qStart[c + 1] += qStart[c];
  const M = qStart[N];
  const o1 = new Uint8Array(M), o2 = new Uint8Array(M), o3 = new Uint8Array(M), qid = new Uint32Array(M);
  {
    const cur = qStart.slice(0, N);
    for (let i = 0; i < Q; i++) {
      const cs = [qa[i], qb[i], qc[i], qd[i]];
      for (let j = 0; j < 4; j++) {
        const k = cur[cs[j]]++;
        const others: number[] = [];
        for (let m = 0; m < 4; m++) if (m !== j) others.push(cs[m]);
        o1[k] = others[0]; o2[k] = others[1]; o3[k] = others[2]; qid[k] = i;
      }
    }
  }
  const occ = new Uint8Array(N);
  const stones = new Uint8Array(20);
  let vlist: number[] = [];          // violated quad ids
  const vpos = new Int32Array(Q).fill(-1);
  const addcost = new Int32Array(N); // for empty cells: # quads that become violated if added
  function vrefresh() { vlist = []; vpos.fill(-1); for (let i = 0; i < Q; i++) if (occ[qa[i]] && occ[qb[i]] && occ[qc[i]] && occ[qd[i]]) { vpos[i] = vlist.length; vlist.push(i); } }
  function vadd(i: number) { if (vpos[i] < 0) { vpos[i] = vlist.length; vlist.push(i); } }
  function vdel(i: number) { const p = vpos[i]; if (p >= 0) { const last = vlist.pop()!; vpos[i] = -1; if (p < vlist.length) { vlist[p] = last; vpos[last] = p; } } }
  function recomputeAddcost() {
    addcost.fill(0);
    for (let i = 0; i < Q; i++) {
      const a = qa[i], b = qb[i], c = qc[i], d = qd[i];
      const u = occ[a] + occ[b] + occ[c] + occ[d];
      if (u === 3) { if (!occ[a]) addcost[a]++; else if (!occ[b]) addcost[b]++; else if (!occ[c]) addcost[c]++; else addcost[d]++; }
    }
  }
  let st = SEED;
  function rnd(): number { // mulberry32 (Math.random is op-metered in the sandbox)
    st = (st + 0x6D2B79F5) >>> 0;
    let t = st;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  const Twit = [9, 15, 16, 18, 20, 22, 30, 36, 44, 58, 62, 65, 67, 70, 71, 87, 91, 93, 97]; // K0035 witness
  const U = [2, 6, 16, 18, 21, 25, 32, 35, 40, 59, 62, 67, 74, 77, 78, 80, 81, 83, 97, 99];   // saturation-20261003-extra
  function loadSet(s: number[]) { occ.fill(0); for (let i = 0; i < 20; i++) { occ[s[i]] = 1; stones[i] = s[i]; } vrefresh(); recomputeAddcost(); }
  loadSet(Twit); const cT = vlist.length;   // control: 0
  loadSet(U); const cU = vlist.length; const Ubad = vlist.map(i => [qa[i], qb[i], qc[i], qd[i]]); // control: 1, {25,59,62,83}
  let units = 0;
  let bestE = 1e9, bestSet: number[] = [], totalMoves = 0;
  const e1seen = new Set<string>();
  const e2seen = new Set<string>();
  const e1new: string[] = [];
  let escapes = 0, escapeBudget = 3;
  const corrCells: number[] = [];
  const corr = new Int32Array(N);
  function applySwap(r: number, e: number): number { // remove stone r, add empty e; returns dE
    const si = stones.indexOf(r);
    const rS = qStart[r], rE = qStart[r + 1];
    let cr = 0;
    for (let k = rS; k < rE; k++) {
      const a = o1[k], b = o2[k], c = o3[k];
      const u = occ[a] + occ[b] + occ[c];
      if (u === 3) { vdel(qid[k]); cr++; }
      else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; addcost[x]--; corr[x]++; if (corr[x] === 1) corrCells.push(x); }
    }
    units += rE - rS;
    occ[r] = 0; occ[e] = 1; stones[si] = e;
    let ce = 0;
    const eS = qStart[e], eE = qStart[e + 1];
    for (let k = eS; k < eE; k++) {
      const a = o1[k], b = o2[k], c = o3[k];
      const u = occ[a] + occ[b] + occ[c];
      if (u === 3) { vadd(qid[k]); ce++; }
      else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; addcost[x]++; }
    }
    units += eE - eS;
    for (const t of corrCells) corr[t] = 0;
    corrCells.length = 0;
    return ce - cr;
  }
  function fillCorr(r: number): number { // corr[] = ce correction for S\{r}; returns cr
    const rS = qStart[r], rE = qStart[r + 1];
    let cr = 0;
    for (let k = rS; k < rE; k++) {
      const a = o1[k], b = o2[k], c = o3[k];
      const u = occ[a] + occ[b] + occ[c];
      if (u === 3) cr++;
      else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; corr[x]++; if (corr[x] === 1) corrCells.push(x); }
    }
    units += rE - rS;
    return cr;
  }
  function clearCorr() { for (const t of corrCells) corr[t] = 0; corrCells.length = 0; }
  function bestEmptyCe(): { e: number; ce: number } { // exact ce(x | S\{r}) via corr
    let be = -1, bc = 1e9;
    for (let c = 0; c < N; c++) { if (occ[c]) continue; const v = addcost[c] - corr[c]; if (v < bc) { bc = v; be = c; } }
    return { e: be, ce: bc };
  }
  function snapshot(): number[] { return Array.from(stones).sort((a, b) => a - b); }
  let lastE = -1;
  function note(): number {
    const E = vlist.length;
    if (E < bestE) { bestE = E; bestSet = snapshot(); }
    const key = snapshot().join(",");
    if (E === 1 && !e1seen.has(key)) { e1seen.add(key); e1new.push(key); }
    if (E === 2) e2seen.add(key);
    lastE = E;
    return E;
  }
  function greedyScan(rs: number[]): boolean { // apply best strictly-improving swap among rs x all empties
    let bestD = 1, bR = -1, bE = -1;
    for (const r of rs) {
      if (!occ[r]) continue;
      const cr = fillCorr(r);
      if (cr === 0) { clearCorr(); continue; }
      const b = bestEmptyCe();
      const d = b.ce - cr;
      if (d < bestD) { bestD = d; bR = r; bE = b.e; }
      clearCorr();
    }
    if (bR >= 0 && bestD < 0) { applySwap(bR, bE); return true; }
    return false;
  }
  function e1Handler(): boolean { // single-swap fix, else bounded 2-swap escape
    const snap = snapshot();
    const q = vlist[0];
    const rs = [qa[q], qb[q], qc[q], qd[q]];
    if (greedyScan(rs)) return true;
    if (escapeBudget <= 0 || units > BUDGET * 0.9) return false;
    escapes++; escapeBudget--;
    for (const r of rs) {
      if (!occ[r]) continue;
      const cr = fillCorr(r);
      if (cr === 0) { clearCorr(); continue; }
      const cands: number[] = [];
      for (let c = 0; c < N; c++) { if (occ[c]) continue; const v = addcost[c] - corr[c]; if (v <= 1) cands.push(c); }
      clearCorr();
      for (const e1 of cands) {
        if (units > BUDGET) return false;
        applySwap(r, e1);
        const E2 = vlist.length;
        if (E2 === 0) return true;
        if (E2 <= 2) {
          const rs2: number[] = [];
          for (let i = 0; i < E2; i++) { const q2 = vlist[i]; rs2.push(qa[q2], qb[q2], qc[q2], qd[q2]); }
          if (greedyScan(rs2)) return true;
        }
        loadSet(snap);
      }
    }
    loadSet(snap);
    return false;
  }
  function kickSet(k: number) {
    for (let i = 0; i < k; i++) {
      const si = (rnd() * 20) | 0;
      const r = stones[si];
      let e = (rnd() * N) | 0; let tries = 0;
      while (occ[e] && tries < 32) { e = (rnd() * N) | 0; tries++; }
      if (occ[e]) continue;
      applySwap(r, e);
    }
  }
  function walk(seed: number[], cap: number, T0: number, T1: number) {
    loadSet(seed);
    let E = note();
    if (E === 0) return;
    if (E === 1 && e1Handler()) { note(); return; }
    const lambda = Math.pow(T1 / T0, 1 / (cap / 32));
    let Tcur = T0, sinceBest = 0, localBest = E;
    for (let mv = 0; mv < cap && units < BUDGET; mv++) {
      totalMoves++;
      E = vlist.length;
      if (E === 0) return;
      const rs: number[] = [];
      if (E <= 8) { for (let i = 0; i < E; i++) { const q = vlist[i]; rs.push(qa[q], qb[q], qc[q], qd[q]); } }
      else { for (let s = 0; s < 8; s++) { const q = vlist[(rnd() * E) | 0]; const cs = [qa[q], qb[q], qc[q], qd[q]]; rs.push(cs[(rnd() * 4) | 0]); } }
      let bestD = 1e9, bR = -1, bE = -1;
      for (const r of rs) {
        if (!occ[r]) continue;
        const cr = fillCorr(r);
        if (cr === 0) { clearCorr(); continue; }
        const b = bestEmptyCe();
        const d = b.ce - cr;
        if (d < bestD) { bestD = d; bR = r; bE = b.e; }
        clearCorr();
      }
      if (bR >= 0 && (bestD <= 0 || rnd() < Math.exp(-bestD / Tcur))) applySwap(bR, bE);
      else {
        const r = rs[(rnd() * rs.length) | 0];
        if (!occ[r]) continue;
        let e = (rnd() * N) | 0; let tries = 0;
        while (occ[e] && tries < 32) { e = (rnd() * N) | 0; tries++; }
        if (occ[e]) continue;
        applySwap(r, e);
      }
      if ((mv & 31) === 31) Tcur *= lambda;
      if ((mv & 15) === 15) {
        E = note();
        if (E === 0) return;
        if (E === 1) { if (e1Handler()) { note(); return; } else kickSet(2 + ((rnd() * 3) | 0)); }
        if (E < localBest) { localBest = E; sinceBest = 0; } else sinceBest++;
        if (sinceBest > 32) { kickSet(2 + ((rnd() * 4) | 0)); sinceBest = 0; localBest = vlist.length; }
      }
      if ((mv & 8191) === 8191) { units += 2 * Q; recomputeAddcost(); }
    }
    note();
  }
  function perturb(base: number[], k: number): number[] {
    const s = base.slice();
    for (let i = 0; i < k; i++) {
      const outI = (rnd() * 20) | 0;
      let inP = (rnd() * N) | 0; let tries = 0;
      while (s.includes(inP) && tries < 40) { inP = (rnd() * N) | 0; tries++; }
      s[outI] = inP;
    }
    return s.sort((a, b) => a - b);
  }
  function randomSet(): number[] {
    const s: number[] = [];
    while (s.length < 20) { const p = (rnd() * N) | 0; if (!s.includes(p)) s.push(p); }
    return s.sort((a, b) => a - b);
  }
  const trace: string[] = [];
  walk(U, 12000, 0.7, 0.06);
  trace.push("U: bestE=" + bestE + " E=" + lastE + " mv=" + totalMoves + " u=" + Math.round(units / 1e6) + "M e1=" + e1seen.size + " e2=" + e2seen.size + " esc=" + escapes);
  let ri = 0;
  while (units < BUDGET && bestE > 0 && ri < 40) {
    ri++;
    const m0 = units;
    const seed = (ri % 3 === 0) ? randomSet() : perturb(bestSet, 2 + ((rnd() * 5) | 0));
    walk(seed, 6000, 1.0, 0.06);
    trace.push("r" + ri + ": bestE=" + bestE + " E=" + lastE + " du=" + Math.round((units - m0) / 1e6) + "M e1=" + e1seen.size + " e2=" + e2seen.size + " esc=" + escapes);
  }
  // second-path verification of any witness (full 4x4 determinant, independent expansion)
  let witness: any = null;
  if (bestE === 0) {
    const S = bestSet.map(p => [px[p], py[p]]);
    let bad = 0;
    for (let i = 0; i < 20; i++) for (let j = i + 1; j < 20; j++) for (let k = j + 1; k < 20; k++) for (let l = k + 1; l < 20; l++) {
      const P = [S[i], S[j], S[k], S[l]];
      const m = (r: number, c: number) => { const q = P[r]; return c === 0 ? q[0] * q[0] + q[1] * q[1] : c === 1 ? q[0] : c === 2 ? q[1] : 1; };
      const d3 = (rs: number[], cs: number[]) =>
        m(rs[0], cs[0]) * (m(rs[1], cs[1]) * m(rs[2], cs[2]) - m(rs[1], cs[2]) * m(rs[2], cs[1]))
        - m(rs[0], cs[1]) * (m(rs[1], cs[0]) * m(rs[2], cs[2]) - m(rs[1], cs[2]) * m(rs[2], cs[0]))
        + m(rs[0], cs[2]) * (m(rs[1], cs[0]) * m(rs[2], cs[1]) - m(rs[1], cs[1]) * m(rs[2], cs[0]));
      const det = d3([1, 2, 3], [0, 1, 2]) - d3([0, 2, 3], [0, 1, 2]) + d3([0, 1, 3], [0, 1, 2]) - d3([0, 1, 2], [0, 1, 2]);
      if (det === 0) bad++;
    }
    witness = { cells: bestSet, bad4x4: bad, coords: bestSet.map(p => [px[p], py[p]]) };
  }
  return {
    controls: { Q, ok54441: Q === 54441, cT, cU, Ubad },
    SEED, totalMoves, units, bestE, bestSet,
    e1_count: e1seen.size, e2_count: e2seen.size, e1new: e1new.slice(0, 12),
    e2_examples: Array.from(e2seen).slice(0, 6), escapes, trace, witness
  };
}
main();
