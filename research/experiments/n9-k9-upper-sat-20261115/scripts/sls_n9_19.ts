// sls_n9_19.ts - 19-stone SLS probe on 9x9 (2026-11-15).
// Energy E(S) = number of forbidden quads fully inside S (F_9 = 29,152).
// WalkSAT/Metropolis hybrid, CSR incidence, incremental addcost, deterministic mulberry32.
// Call 1 (seed 0x9E3779B9): census control Q=29,152, W9 E=0; 18-stone positive control
//   from perturb(W9,6) refound E=0 in 809 moves; 19-stone run from W9+argmin(addcost):
//   14,059 moves, bestE=3, no E<=2 ever seen.
// Call 2 (seed 0x9E3779B9 ^ 0xA5A5A5A5), source below: multi-restart campaign (2 restarts
//   within budget), 12,875 moves, bestE=3 at W9+{53}; full 1-swap neighborhood (1,178
//   swaps) of the best set contains no E<=2.
// Records: ../output/sls_n9_19_runs_20261115.json
// Heuristic bounded negative evidence only; implies no upper bound on K_9.
async function main() {
  const n = 9, N = 81;
  const px = new Uint8Array(N), py = new Uint8Array(N), pw = new Uint16Array(N);
  for (let p = 0; p < N; p++) { const x = p % n, y = (p / n) | 0; px[p] = x; py[p] = y; pw[p] = x * x + y * y; }
  const qa: number[] = [], qb: number[] = [], qc: number[] = [], qd: number[] = [];
  for (let a = 0; a < N - 3; a++) { const wa = pw[a], xa = px[a], ya = py[a];
    for (let b = a + 1; b < N - 2; b++) { const bw = pw[b] - wa, bx = px[b] - xa, by = py[b] - ya;
      for (let c = b + 1; c < N - 1; c++) { const cw = pw[c] - wa, cx = px[c] - xa, cy = py[c] - ya;
        const c1 = bx * cy - by * cx, c2 = by * cw - bw * cy, c3 = bw * cx - bx * cw;
        for (let d = c + 1; d < N; d++) { if (c1 * (pw[d] - wa) + c2 * (px[d] - xa) + c3 * (py[d] - ya) === 0) { qa.push(a); qb.push(b); qc.push(c); qd.push(d); } } } } }
  const Q = qa.length;
  const qStart = new Uint32Array(N + 1);
  for (let i = 0; i < Q; i++) { qStart[qa[i] + 1]++; qStart[qb[i] + 1]++; qStart[qc[i] + 1]++; qStart[qd[i] + 1]++; }
  for (let c = 0; c < N; c++) qStart[c + 1] += qStart[c];
  const M = qStart[N];
  const o1 = new Uint8Array(M), o2 = new Uint8Array(M), o3 = new Uint8Array(M), qid = new Uint32Array(M);
  { const cur = qStart.slice(0, N);
    for (let i = 0; i < Q; i++) { const cs = [qa[i], qb[i], qc[i], qd[i]];
      for (let j = 0; j < 4; j++) { const k = cur[cs[j]]++; const others: number[] = []; for (let m2 = 0; m2 < 4; m2++) if (m2 !== j) others.push(cs[m2]); o1[k] = others[0]; o2[k] = others[1]; o3[k] = others[2]; qid[k] = i; } } }
  let st = 0x9E3779B9 ^ 0xA5A5A5A5;
  function rnd(): number { st = (st + 0x6D2B79F5) >>> 0; let t = st; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
  const W9 = [5, 6, 8, 9, 11, 18, 24, 31, 44, 47, 50, 52, 54, 55, 70, 73, 75, 79];
  const BUDGET = 4.8e8;
  let units = 0, totalMoves = 0;
  let occ = new Uint8Array(N), stones = new Uint8Array(20);
  let vlist: number[] = []; const vpos = new Int32Array(Q).fill(-1);
  const addcost = new Int32Array(N);
  const corr = new Int32Array(N); const corrCells: number[] = [];
  function vrefresh() { vlist = []; vpos.fill(-1); for (let i = 0; i < Q; i++) if (occ[qa[i]] && occ[qb[i]] && occ[qc[i]] && occ[qd[i]]) { vpos[i] = vlist.length; vlist.push(i); } }
  function vadd(i: number) { if (vpos[i] < 0) { vpos[i] = vlist.length; vlist.push(i); } }
  function vdel(i: number) { const p = vpos[i]; if (p >= 0) { const last = vlist.pop()!; vpos[i] = -1; if (p < vlist.length) { vlist[p] = last; vpos[last] = p; } } }
  function recomputeAddcost() { addcost.fill(0); for (let i = 0; i < Q; i++) { const a = qa[i], b = qb[i], c = qc[i], d = qd[i]; const u = occ[a] + occ[b] + occ[c] + occ[d]; if (u === 3) { if (!occ[a]) addcost[a]++; else if (!occ[b]) addcost[b]++; else if (!occ[c]) addcost[c]++; else addcost[d]++; } } }
  function loadSet(s: number[], K: number) { occ.fill(0); for (let i = 0; i < K; i++) { occ[s[i]] = 1; stones[i] = s[i]; } vrefresh(); recomputeAddcost(); }
  function applySwap(r: number, e: number): number {
    const si = stones.indexOf(r);
    const rS = qStart[r], rE = qStart[r + 1]; let cr = 0;
    for (let k = rS; k < rE; k++) { const a = o1[k], b = o2[k], c = o3[k]; const u = occ[a] + occ[b] + occ[c];
      if (u === 3) { vdel(qid[k]); cr++; } else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; addcost[x]--; corr[x]++; if (corr[x] === 1) corrCells.push(x); } }
    units += rE - rS;
    occ[r] = 0; occ[e] = 1; stones[si] = e;
    let ce = 0; const eS = qStart[e], eE = qStart[e + 1];
    for (let k = eS; k < eE; k++) { const a = o1[k], b = o2[k], c = o3[k]; const u = occ[a] + occ[b] + occ[c];
      if (u === 3) { vadd(qid[k]); ce++; } else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; addcost[x]++; } }
    units += eE - eS;
    for (const t of corrCells) corr[t] = 0; corrCells.length = 0;
    return ce - cr;
  }
  function fillCorr(r: number): number { const rS = qStart[r], rE = qStart[r + 1]; let cr = 0;
    for (let k = rS; k < rE; k++) { const a = o1[k], b = o2[k], c = o3[k]; const u = occ[a] + occ[b] + occ[c];
      if (u === 3) cr++; else if (u === 2) { const x = occ[a] ? (occ[b] ? c : b) : a; corr[x]++; if (corr[x] === 1) corrCells.push(x); } }
    units += rE - rS; return cr; }
  function clearCorr() { for (const t of corrCells) corr[t] = 0; corrCells.length = 0; }
  function bestEmptyCe(): { e: number; ce: number } { let be = -1, bc = 1e9; for (let c = 0; c < N; c++) { if (occ[c]) continue; const v = addcost[c] - corr[c]; if (v < bc) { bc = v; be = c; } } return { e: be, ce: bc }; }
  function snapshot(K: number): number[] { return Array.from(stones.slice(0, K)).sort((a, b) => a - b); }
  let bestE = 1e9, bestSet: number[] = [];
  const e1seen = new Set<string>(), e2seen = new Set<string>();
  function note(K: number): number { const E = vlist.length; if (E < bestE) { bestE = E; bestSet = snapshot(K); }
    if (E === 1 || E === 2) { const key = snapshot(K).join(","); if (E === 1) e1seen.add(key); else e2seen.add(key); } return E; }
  function greedyScan(rs: number[]): boolean { let bestD = 1, bR = -1, bE = -1;
    for (const r of rs) { if (!occ[r]) continue; const cr = fillCorr(r); if (cr === 0) { clearCorr(); continue; }
      const b = bestEmptyCe(); const d = b.ce - cr; if (d < bestD) { bestD = d; bR = r; bE = b.e; } clearCorr(); }
    if (bR >= 0 && bestD < 0) { applySwap(bR, bE); return true; } return false; }
  function kickSet(K: number, k: number) { for (let i = 0; i < k; i++) { const si = (rnd() * K) | 0; const r = stones[si]; let e = (rnd() * N) | 0; let tries = 0; while (occ[e] && tries < 32) { e = (rnd() * N) | 0; tries++; } if (occ[e]) continue; applySwap(r, e); } }
  function walk(K: number, seed: number[], cap: number, T0: number, T1: number): boolean {
    loadSet(seed, K);
    let E = note(K); if (E === 0) return true;
    const lambda = Math.pow(T1 / T0, 32 / cap); let Tcur = T0, sinceBest = 0, localBest = E;
    for (let mv = 0; mv < cap && units < BUDGET; mv++) { totalMoves++;
      E = vlist.length; if (E === 0) { note(K); return true; }
      const rs: number[] = [];
      if (E <= 8) { for (let i = 0; i < E; i++) { const q = vlist[i]; rs.push(qa[q], qb[q], qc[q], qd[q]); } }
      else { for (let s = 0; s < 8; s++) { const q = vlist[(rnd() * E) | 0]; rs.push(qa[q], qb[q], qc[q], qd[q]); const cs = [qa[q], qb[q], qc[q], qd[q]]; rs.push(cs[(rnd() * 4) | 0]); } }
      let bestD = 1e9, bR = -1, bE = -1;
      for (const r of rs) { if (!occ[r]) continue; const cr = fillCorr(r); if (cr === 0) { clearCorr(); continue; }
        const b = bestEmptyCe(); const d = b.ce - cr; if (d < bestD) { bestD = d; bR = r; bE = b.e; } clearCorr(); }
      if (bR >= 0 && (bestD <= 0 || rnd() < Math.exp(-bestD / Tcur))) applySwap(bR, bE);
      else { const r = rs[(rnd() * rs.length) | 0]; if (!occ[r]) continue; let e = (rnd() * N) | 0; let tries = 0; while (occ[e] && tries < 32) { e = (rnd() * N) | 0; tries++; } if (occ[e]) continue; applySwap(r, e); }
      if ((mv & 31) === 31) Tcur *= lambda;
      if ((mv & 15) === 15) { E = note(K); if (E === 0) return true;
        if (E <= 2 && E >= 1) { const rs2: number[] = []; for (let i = 0; i < E; i++) { const q = vlist[i]; rs2.push(qa[q], qb[q], qc[q], qd[q]); } if (greedyScan(rs2)) { note(K); if (vlist.length === 0) return true; } }
        if (E < localBest) { localBest = E; sinceBest = 0; } else sinceBest++;
        if (sinceBest > 48) { kickSet(K, 2 + ((rnd() * 3) | 0)); sinceBest = 0; localBest = vlist.length; } }
    }
    note(K); return false;
  }
  function perturb(base: number[], K: number, k: number): number[] { const s = base.slice(0, K);
    for (let i = 0; i < k; i++) { const outI = (rnd() * K) | 0; let inP = (rnd() * N) | 0; let tries = 0; while (s.includes(inP) && tries < 40) { inP = (rnd() * N) | 0; tries++; } s[outI] = inP; } return s.sort((a, b) => a - b); }
  function randomSet(K: number): number[] { const s: number[] = []; while (s.length < K) { const p = (rnd() * N) | 0; if (!s.includes(p)) s.push(p); } return s.sort((a, b) => a - b); }
  function w9PlusBest(): number[] { loadSet(W9, 18); let be = -1, bc = 1e9; for (let c = 0; c < N; c++) { if (occ[c]) continue; if (addcost[c] < bc) { bc = addcost[c]; be = c; } } return W9.concat([be]).sort((a, b) => a - b); }
  function w9PlusRand(): number[] { const empty = []; for (let c = 0; c < N; c++) if (!W9.includes(c)) empty.push(c); return W9.concat([empty[(rnd() * empty.length) | 0]]).sort((a, b) => a - b); }

  // multi-restart campaign, 19 stones
  let ri = 0;
  while (units < BUDGET && ri < 40 && bestE > 0) { ri++;
    const seed = (ri % 3 === 0) ? randomSet(19) : (ri % 3 === 1 ? w9PlusRand() : perturb(bestE < 1e8 ? bestSet : w9PlusBest(), 19, 2 + ((rnd() * 4) | 0)));
    walk(19, seed, 9000, 1.0, 0.06);
  }
  const campaign = { restarts: ri, bestE, bestSet, moves: totalMoves, units, e1: e1seen.size, e2: e2seen.size };
  // full 1-swap neighborhood scan of bestSet (bounded local evidence)
  let nbBest = 1e9; const nbDetail: number[] = [];
  if (bestE <= 4 && bestSet.length === 19) {
    for (const r of bestSet) for (let e = 0; e < N; e++) {
      if (bestSet.includes(e)) continue;
      const s2 = bestSet.filter(x => x !== r).concat([e]).sort((a, b) => a - b);
      loadSet(s2, 19); const E2 = vlist.length; units += 3000;
      if (E2 < nbBest) nbBest = E2;
      if (E2 <= 2) nbDetail.push(s2.join(",") + ":" + E2);
    }
  }
  return { Q, campaign, nbBest, nbDetail: nbDetail.slice(0, 6), totalUnits: units };
}
main().then(r => console.log(JSON.stringify(r, null, 2)));
