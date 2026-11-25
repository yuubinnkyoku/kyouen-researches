// hunt.mjs — forbidden-quartet machinery on the n x n standard kyouen board:
//   - incremental State (add/remove stone, safety violations, uncovered empty cells)
//   - complete local nets around a base configuration (remove-1/add-0, remove-2/add-0,
//     remove-2/add-1 for k -> k-1 targets)
//   - cross-board transplant: all D4 x translation placements of a source witness on a
//     larger host board, with per-placement uncovered-cell reports
//   - stochastic local search (SLS) witness hunt with time budget and restarts
// All arithmetic is exact integer (well below 2^53 for n<=13).
// Changelog: uncovered counter initialized to N (empty board: every cell uncovered).

import { census, quartetList, verifyAgainstAnchors } from './census.mjs';
import { WITNESSES, d4Images } from './witnesses.mjs';

export class Board {
  constructor(n) {
    this.n = n; this.N = n * n;
    this.cen = census(n);
    const issues = verifyAgainstAnchors(this.cen);
    if (issues.length) throw new Error(`anchor mismatch for n=${n}: ${issues.join("; ")}`);
    this.q4 = quartetList(this.cen); // Uint16Array, 4 cells per quartet
    this.F = this.cen.F;
    const deg = new Uint32Array(this.N);
    for (let i = 0; i < this.q4.length; i++) deg[this.q4[i]]++;
    this.qOff = new Uint32Array(this.N + 1);
    for (let c = 0; c < this.N; c++) this.qOff[c + 1] = this.qOff[c] + deg[c];
    this.qList = new Uint32Array(4 * this.F);
    const tmp = this.qOff.slice(0, this.N);
    for (let i = 0; i < this.F; i++) {
      for (let j = 0; j < 4; j++) {
        const c = this.q4[4 * i + j];
        this.qList[tmp[c]++] = i;
      }
    }
  }
}

export class State {
  constructor(board) {
    this.bd = board;
    const { N, F } = board;
    this.cnt = new Uint8Array(F);      // stones per quartet (0..4)
    this.cov = new Uint16Array(N);    // #quartets q containing the cell with cnt[q]>=3
    this.inS = new Uint8Array(N);
    this.viol = 0;
    this.uncovered = N; // an empty board has every cell uncovered
    this.stones = [];
  }
  reset() {
    this.cnt.fill(0); this.cov.fill(0); this.inS.fill(0);
    this.viol = 0; this.uncovered = this.bd.N; this.stones.length = 0;
  }
  size() { return this.stones.length; }
  add(c) {
    const bd = this.bd, q4 = bd.q4;
    if (this.inS[c]) return false;
    if (this.cov[c] === 0) this.uncovered--;
    this.inS[c] = 1;
    this.stones.push(c);
    const qL = bd.qList, off = bd.qOff;
    for (let i = off[c]; i < off[c + 1]; i++) {
      const q = qL[i];
      const cnt = ++this.cnt[q];
      if (cnt === 3) {
        const b = 4 * q;
        for (let j = 0; j < 4; j++) {
          const p = q4[b + j];
          if (++this.cov[p] === 1 && !this.inS[p]) this.uncovered--;
        }
      } else if (cnt === 4) this.viol++;
    }
    return true;
  }
  remove(c) {
    const bd = this.bd, q4 = bd.q4;
    if (!this.inS[c]) return false;
    const qL = bd.qList, off = bd.qOff;
    for (let i = off[c]; i < off[c + 1]; i++) {
      const q = qL[i];
      let cnt = this.cnt[q];
      if (cnt === 4) this.viol--;
      cnt = --this.cnt[q];
      if (cnt === 2) {
        const b = 4 * q;
        for (let j = 0; j < 4; j++) {
          const p = q4[b + j];
          if (--this.cov[p] === 0 && !this.inS[p]) this.uncovered++;
        }
      }
    }
    this.inS[c] = 0;
    const idx = this.stones.indexOf(c);
    if (idx >= 0) this.stones.splice(idx, 1);
    if (this.cov[c] === 0) this.uncovered++;
    return true;
  }
  score() { return this.viol * 1000 + this.uncovered; }
  uncoveredList() {
    const out = [];
    for (let p = 0; p < this.bd.N; p++) if (!this.inS[p] && this.cov[p] === 0) out.push(p);
    return out;
  }
  coords() {
    const n = this.bd.n;
    return this.stones.slice().sort((a, b) => a - b).map((p) => [p % n, (p / n) | 0]);
  }
}

// ---- complete local nets around a base configuration ----
export function localNets(bd, seedCells, targetK) {
  const st = new State(bd);
  for (const c of seedCells) st.add(c);
  if (st.viol !== 0) throw new Error("seed config is not safe");
  if (st.uncovered !== 0) throw new Error("seed config is not maximal");
  const k = st.size();
  const res = { k, targetK, r1a0: [], r2a0: [], r2a1: [], counts: { r1: 0, r2: 0, r2a1cand: 0, r2a1configs: 0 } };
  for (const s of st.stones.slice()) {
    st.remove(s);
    res.counts.r1++;
    if (st.viol === 0 && st.uncovered === 0) res.r1a0.push(st.coords());
    st.add(s);
  }
  const stones = st.stones.slice();
  const scratch = new State(bd);
  for (let a = 0; a < stones.length; a++) {
    for (let b = a + 1; b < stones.length; b++) {
      const rem = stones.slice(); rem.splice(b, 1); rem.splice(a, 1);
      scratch.reset();
      for (const c of rem) scratch.add(c);
      res.counts.r2++;
      if (scratch.viol !== 0) throw new Error("subset of safe config unsafe (bug)");
      if (scratch.uncovered === 0) { res.r2a0.push(scratch.coords()); continue; }
      if (targetK !== k - 1) continue;
      const U = scratch.uncoveredList();
      const seen = new Set();
      const p0 = U[0];
      for (let i = bd.qOff[p0]; i < bd.qOff[p0 + 1]; i++) {
        const q = bd.qList[i];
        if (scratch.cnt[q] !== 2) continue;
        const b4 = 4 * q;
        for (let j = 0; j < 4; j++) {
          const c = bd.q4[b4 + j];
          if (c === p0 || scratch.inS[c]) continue;
          if (seen.has(c)) continue;
          seen.add(c);
          scratch.add(c);
          if (scratch.viol === 0 && scratch.uncovered === 0) res.r2a1.push(scratch.coords());
          scratch.remove(c);
          res.counts.r2a1cand++;
          res.counts.r2a1configs++;
        }
      }
    }
  }
  return res;
}

// ---- cross-board transplant ----
export function transplant(src, bd) {
  const m = src.n, host = bd.n;
  if (m > host) throw new Error("source bigger than host");
  const placements = [];
  const seen = new Set();
  const st = new State(bd);
  for (const img of d4Images(src.coords, m)) {
    const maxX = Math.max(...img.map(c => c[0])), maxY = Math.max(...img.map(c => c[1]));
    for (let dx = 0; dx + maxX < host; dx++) {
      for (let dy = 0; dy + maxY < host; dy++) {
        const cells = img.map(([x, y]) => (x + dx) + host * (y + dy));
        cells.sort((a, b) => a - b);
        const key = cells.join(",");
        if (seen.has(key)) continue;
        seen.add(key);
        st.reset();
        for (const c of cells) st.add(c);
        const unc = st.uncoveredList();
        if (st.viol !== 0) throw new Error(`transplant broke safety (impossible, bug) src=${src.src} m=${m}`);
        placements.push({
          cells,
          uncoveredCount: unc.length,
          uncoveredCells: unc.slice(0, 64).map((p) => [p % host, (p / host) | 0]),
        });
      }
    }
  }
  placements.sort((a, b) => a.uncoveredCount - b.uncoveredCount);
  return placements;
}

export function makeRng(seed) {
  let s = seed >>> 0 || 1;
  return function () {
    s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}

// ---- SLS witness hunt ----
export function slsHunt(bd, targetK, seeds, budgetMs, rnd) {
  const t0 = Date.now();
  const best = { score: Infinity, config: null };
  let restarts = 0, moves = 0, evals = 0, found = null;
  const st = new State(bd);
  const N = bd.N;
  function loadSeed(cellsAry) {
    st.reset();
    for (const c of cellsAry) st.add(c);
    while (st.size() < targetK) {
      const c = (rnd() * N) | 0;
      if (!st.inS[c]) st.add(c);
    }
    while (st.size() > targetK) st.remove(st.stones[(rnd() * st.size()) | 0]);
  }
  const candBuf = [];
  function candidateCells(p) {
    candBuf.length = 0;
    for (let i = bd.qOff[p]; i < bd.qOff[p + 1]; i++) {
      const q = bd.qList[i];
      if (st.cnt[q] !== 2) continue;
      const b = 4 * q;
      for (let j = 0; j < 4; j++) {
        const c = bd.q4[b + j];
        if (c !== p && !st.inS[c] && !candBuf.includes(c)) candBuf.push(c);
      }
    }
    return candBuf;
  }
  function bestRemovalDelta() {
    let bestS = Infinity;
    const cands = st.stones.slice();
    for (const s of cands) {
      st.remove(s);
      const s2 = st.score();
      st.add(s);
      evals++;
      if (s2 < bestS) bestS = s2;
    }
    return bestS;
  }
  function removeBestStone() {
    if (st.size() <= targetK) return;
    let bestS = Infinity, bestSs = -1;
    const cands = st.stones.slice();
    for (const s of cands) {
      st.remove(s);
      const s2 = st.score();
      st.add(s);
      evals++;
      if (s2 < bestS || (s2 === bestS && rnd() < 0.5)) { bestS = s2; bestSs = s; }
    }
    st.remove(bestSs);
  }
  function recordBest() {
    const s = st.score();
    if (s < best.score) { best.score = s; best.config = st.coords(); }
  }
  let stall = 0, seedIdx = 0, lastBest = Infinity;
  function doRestart() {
    restarts++;
    stall = 0;
    lastBest = Infinity;
    if (seeds.length && seedIdx < seeds.length - 1) seedIdx++;
    else if (seeds.length) seedIdx = (rnd() * seeds.length) | 0;
    loadSeed(seeds[seedIdx] || []);
    for (let t = 0; t < 2; t++) {
      const c = (rnd() * bd.N) | 0;
      if (!st.inS[c]) { st.add(c); if (st.size() > targetK) st.remove(st.stones[(rnd() * st.size()) | 0]); }
    }
  }
  loadSeed(seeds[0] || []);
  while (Date.now() - t0 < budgetMs) {
    if (st.viol === 0 && st.uncovered === 0) { found = st.coords(); break; }
    moves++;
    const unc = [];
    for (let p = 0; p < N; p++) if (!st.inS[p] && st.cov[p] === 0) unc.push(p);
    if (unc.length === 0) {
      // violations only: swap a stone out of a violating quartet
      const violQs = [];
      for (let q = 0; q < bd.F; q++) { if (st.cnt[q] === 4) { violQs.push(q); if (violQs.length > 32) break; } }
      if (violQs.length === 0) throw new Error("uncovered==0 but viol>0 (bug)");
      const q = violQs[(rnd() * violQs.length) | 0];
      const cells = [bd.q4[4 * q], bd.q4[4 * q + 1], bd.q4[4 * q + 2], bd.q4[4 * q + 3]];
      st.remove(cells[(rnd() * 4) | 0]);
      for (let tries = 0; tries < 64; tries++) {
        const c = (rnd() * N) | 0;
        st.add(c);
        evals++;
        break;
      }
      recordBest();
      if (++stall > 4000) doRestart();
      continue;
    }
    const p = unc[(rnd() * unc.length) | 0];
    candidateCells(p);
    if (candBuf.length === 0 || rnd() < 0.12) {
      const c = (rnd() * N) | 0;
      if (st.inS[c]) { if (++stall > 4000) doRestart(); continue; }
      st.add(c);
      removeBestStone();
      evals++;
      recordBest();
      if (++stall > 4000) doRestart();
      continue;
    }
    let c = candBuf[(rnd() * candBuf.length) | 0];
    if (candBuf.length > 1) {
      let bestScore = Infinity, bestC = c;
      const sample = Math.min(candBuf.length, 4);
      for (let t = 0; t < sample; t++) {
        const cc = candBuf[(rnd() * candBuf.length) | 0];
        st.add(cc);
        const s2 = bestRemovalDelta();
        st.remove(cc);
        evals++;
        if (s2 < bestScore) { bestScore = s2; bestC = cc; }
      }
      c = bestC;
    }
    st.add(c);
    removeBestStone();
    recordBest();
    if (st.score() < lastBest) { lastBest = st.score(); stall = 0; } else stall++;
    if (stall > 4000) doRestart();
  }
  return { found, bestScore: best.score, bestConfig: best.config, moves, evals, restarts, ms: Date.now() - t0 };
}


// ---- SLS v2 witness hunt ----
// Policy: pick a random uncovered cell p; enumerate the exact-1-add candidate set
// (completions of its cnt==2 quartets); for each candidate c compute the true new
// uncovered count by applying add (the state counter is incremental); pick the best;
// add it; remove the best stone EXCLUDING the just-added one (anti-oscillation);
// 12% random perturbation moves; stall-based restarts with random-mix seeds.
export function slsHuntV2(bd, targetK, seeds, budgetMs, rnd, opts) {
  const t0 = Date.now();
  const best = { score: Infinity, config: null };
  let restarts = 0, moves = 0, evals = 0, found = null;
  const st = new State(bd);
  const N = bd.N;
  const stallLimit = opts?.stallLimit || 2500;
  const perturbProb = opts?.perturbProb ?? 0.12;
  function loadSeedRandom() {
    st.reset();
    while (st.size() < targetK) {
      const c = (rnd() * N) | 0;
      st.add(c);
    }
  }
  function loadSeed(cellsAry) {
    st.reset();
    for (const c of cellsAry) st.add(c);
    while (st.size() < targetK) {
      const c = (rnd() * N) | 0;
      if (!st.inS[c]) st.add(c);
    }
    while (st.size() > targetK) st.remove(st.stones[(rnd() * st.size()) | 0]);
  }
  const candBuf = [];
  function candidatesFor(p) {
    candBuf.length = 0;
    for (let i = bd.qOff[p]; i < bd.qOff[p + 1]; i++) {
      const q = bd.qList[i];
      if (st.cnt[q] !== 2) continue;
      const b = 4 * q;
      for (let j = 0; j < 4; j++) {
        const c = bd.q4[b + j];
        if (c !== p && !st.inS[c] && !candBuf.includes(c)) candBuf.push(c);
      }
    }
    return candBuf;
  }
  function recordBest() {
    const s = st.score();
    if (s < best.score) { best.score = s; best.config = st.coords(); }
  }
  function doRestart() {
    restarts++;
    stall = 0;
    if (seeds.length && rnd() < 0.55) {
      loadSeed(seeds[(rnd() * seeds.length) | 0]);
      for (let t = 0; t < 2 + ((rnd() * 3) | 0); t++) {
        const c = (rnd() * N) | 0;
        st.remove(st.stones[(rnd() * st.size()) | 0]); st.add(c);
      }
    } else {
      loadSeedRandom();
    }
  }
  let stall = 0;
  let bestScoreT = Infinity;
  doRestart();
  while (Date.now() - t0 < budgetMs) {
    if (st.viol === 0 && st.uncovered === 0) { found = st.coords(); break; }
    moves++;
    if (rnd() < perturbProb) {
      // perturbation: swap a random stone for a random cell (keep k)
      const outS = st.stones[(rnd() * st.size()) | 0];
      const c = (rnd() * N) | 0;
      st.remove(outS); st.add(c); evals++;
      recordBest();
      if (++stall > stallLimit) doRestart();
      continue;
    }
    if (st.viol > 0) {
      const violQs = [];
      for (let q = 0; q < bd.F; q++) { if (st.cnt[q] === 4) { violQs.push(q); if (violQs.length > 32) break; } }
      if (violQs.length === 0) throw new Error("viol>0 with no violating quartet (bug)");
      const q = violQs[(rnd() * violQs.length) | 0];
      const cells = [bd.q4[4 * q], bd.q4[4 * q + 1], bd.q4[4 * q + 2], bd.q4[4 * q + 3]];
      st.remove(cells[(rnd() * 4) | 0]);
      while (st.size() < targetK) { const c = (rnd() * N) | 0; if (!st.inS[c]) { st.add(c); break; } }
      evals++;
      recordBest();
      if (++stall > stallLimit) doRestart();
      continue;
    }
    const unc = [];
    for (let p = 0; p < N; p++) if (!st.inS[p] && st.cov[p] === 0) unc.push(p);
    if (unc.length === 0) throw new Error("viol==0 and uncovered==0 handled above (bug)");
    const p = unc[(rnd() * unc.length) | 0];
    candidatesFor(p);
    if (candBuf.length === 0) {
      // no 1-add completion for p: perturb two stones cheaply
      const s0 = st.stones[(rnd() * st.size()) | 0];
      st.remove(s0);
      const c = (rnd() * N) | 0;
      if (!st.inS[c]) st.add(c); else st.add(s0);
      evals += 2;
      recordBest();
      if (++stall > stallLimit) doRestart();
      continue;
    }
    // exact-gain candidate selection
    const before = st.uncovered;
    let bestGain = Infinity, bestC = -1, bestSeen = 0;
    const cands = candBuf.slice();
    for (const c of cands) {
      st.add(c); evals++;
      const gain = st.uncovered - before + 1000 * st.viol;
      if (gain < bestGain) { bestGain = gain; bestC = c; }
      st.remove(c);
      evals++;
      if (++bestSeen > 4000) break;
    }
    if (bestC === -1) { doRestart(); continue; }
    st.add(bestC);
    // remove best stone EXCLUDING bestC
    let rs = -1, rsScore = Infinity;
    const cands2 = st.stones.slice();
    for (const s of cands2) {
      if (s === bestC) continue;
      st.remove(s); evals++;
      const s2 = st.score();
      st.add(s); evals++;
      if (s2 < rsScore) { rsScore = s2; rs = s; }
    }
    st.remove(rs);
    recordBest();
    const sc = st.score();
    if (sc < bestScoreT) { bestScoreT = sc; stall = 0; } else stall++;
    if (stall > stallLimit) doRestart();
  }
  return { found, bestScore: best.score, bestConfig: best.config, moves, evals, restarts, ms: Date.now() - t0 };
}


// ---- complete double-swap plateau probe ----
// Given a stone config S on bd (|S| stones, no maximality assumed), enumerate EVERY
// (remove {s1,s2}; add {c1,c2}) quadruple where c1 is an exact-1-add completion of the
// first uncovered cell of S\{s1,s2} and c2 of the first uncovered cell after c1.
// Reports every outcome with uncovered==0 (witness at |S| stones) and the best score
// seen (any double swap is exactly-once enumerated over its own branch order).
export function doubleSwapProbe(bd, cells) {
  const t0 = Date.now();
  const st = new State(bd);
  for (const c of cells) st.add(c);
  const k = st.size();
  let found = [];
  let bestScore = st.score(), bestConfig = st.coords();
  let visited = 0, branches = 0, witnessSmaller = [];
  const stones0 = st.stones.slice();
  for (let a = 0; a < stones0.length; a++) {
    for (let b = a + 1; b < stones0.length; b++) {
      const s1 = stones0[a], s2 = stones0[b];
      st.remove(s1); st.remove(s2);
      branches++;
      // helper closures on the reduced config
      const uncoveredNow = () => {
        for (let p = 0; p < bd.N; p++) if (!st.inS[p] && st.cov[p] === 0) return p;
        return -1;
      };
      const completions = (p) => {
        const out = [];
        for (let i = bd.qOff[p]; i < bd.qOff[p + 1]; i++) {
          const q = bd.qList[i];
          if (st.cnt[q] !== 2) continue;
          const b4 = 4 * q;
          for (let j = 0; j < 4; j++) {
            const c = bd.q4[b4 + j];
            if (c !== p && !st.inS[c] && !out.includes(c)) out.push(c);
          }
        }
        return out;
      };
      let p1 = uncoveredNow();
      if (p1 === -1) { witnessSmaller.push(st.coords()); st.add(s1); st.add(s2); continue; } // k-2 maximal!
      const C1 = completions(p1);
      for (const c1 of C1) {
        st.add(c1);
        if (st.viol === 0) {
          const p2 = uncoveredNow();
          if (p2 === -1) { found.push(st.coords()); } // k-2+1 = k-1 stone witness (bonus)
          else {
            const C2 = completions(p2);
            for (const c2 of C2) {
              st.add(c2);
              visited++;
              if (st.viol === 0 && st.uncovered === 0) found.push(st.coords()); // k-stone witness
              else {
                const sc = st.score();
                if (sc < bestScore) { bestScore = sc; bestConfig = st.coords(); }
              }
              st.remove(c2);
            }
          }
        }
        st.remove(c1);
      }
      st.add(s1); st.add(s2);
      // score bookkeeping on the reduced config too (best double swap = worst case skip)
    }
  }
  return { k, found, witnessSmaller, bestScore, bestConfig, branches, visited, ms: Date.now() - t0 };
}


// ---- COMPLETE double-swap net (full 2-out/2-in enumeration) ----
// For every stone pair {s1,s2} removed: U = uncovered cells of the reduced config
// (k-2 stones; safety inherited). Candidate cells C_ext = union over p in U of
//  - completions of cnt==2 quartets of p, and
//  - the two empty cells of cnt==1 quartets of p (pairs completed by BOTH adds).
// Every unordered pair {c1,c2} in C_ext x C_ext is applied and checked:
// viol==0 && uncovered==0 -> k-stone witness; every single c in the cnt==2
// completion set is also applied alone (k-1-stone witness if fully covering).
// This is a complete scan of {remove 2, add 2} restricted to adds that can
// complete SOME uncovered cell of the reduced config (any witness in the
// 2-out/2-in neighborhood of the input config is found). bestScore tracks the
// best non-witness score over the net.
export function doubleSwapComplete(bd, cells) {
  const t0 = Date.now();
  const st = new State(bd);
  for (const c of cells) st.add(c);
  const k = st.size();
  const N = bd.N;
  const N2 = N; // hide
  const witnesses = [], smaller = [];
  let bestScore = st.score(), bestConfig = st.coords();
  let pairsDone = 0, add1Checked = 0, pairAddChecked = 0;
  const stones0 = st.stones.slice();
  const seen1 = new Set(), seen2 = new Set();
  for (let a = 0; a < stones0.length; a++) {
    for (let b = a + 1; b < stones0.length; b++) {
      const s1 = stones0[a], s2 = stones0[b];
      st.remove(s1); st.remove(s2);
      pairsDone++;
      const U = [];
      for (let p = 0; p < N; p++) if (!st.inS[p] && st.cov[p] === 0) U.push(p);
      if (U.length === 0) { smaller.push(st.coords()); st.add(s1); st.add(s2); continue; }
      const Cext = new Set(), Csingle = new Set();
      for (const p of U) {
        for (let i = bd.qOff[p]; i < bd.qOff[p + 1]; i++) {
          const q = bd.qList[i];
          const cnt = st.cnt[q];
          if (cnt < 1 || cnt > 2) continue;
          const b4 = 4 * q;
          const empt = [];
          for (let j = 0; j < 4; j++) { const c = bd.q4[b4 + j]; if (c !== p && !st.inS[c]) empt.push(c); else if (c !== p && st.inS[c]) {} }
          if (cnt === 2) { if (empt.length === 1) { Cext.add(empt[0]); Csingle.add(empt[0]); } }
          else if (cnt === 1) { if (empt.length === 2) { Cext.add(empt[0]); Cext.add(empt[1]); } } // the pair completes p via the same quartet
        }
      }
      const Clist = [...Cext];
      // 1-add checks (k-1 witnesses)
      for (const c of Csingle) {
        if (st.inS[c]) continue;
        const key = pairsDone * 100000 + c;
        st.add(c); add1Checked++;
        if (st.viol === 0 && st.uncovered === 0) smaller.push(st.coords());
        st.remove(c);
        void key; void seen1;
      }
      // 2-add checks (k witnesses)
      for (let i = 0; i < Clist.length; i++) {
        for (let j = i + 1; j < Clist.length; j++) {
          const c1 = Clist[i], c2 = Clist[j];
          const kk = c1 * N2 + c2;
          if (seen2.has(kk)) continue;
          st.add(c1); st.add(c2); pairAddChecked++;
          if (st.viol === 0 && st.uncovered === 0) witnesses.push(st.coords());
          else {
            const sc = st.score();
            if (sc < bestScore) { bestScore = sc; bestConfig = st.coords(); }
          }
          st.remove(c1); st.remove(c2);
          if (pairAddChecked % 97 === 0) seen2.clear(); // bound memory; collide-check only within a pair-branch
        }
      }
      seen2.clear();
      st.add(s1); st.add(s2);
    }
  }
  return { k, witnesses, smaller, bestScore, bestConfig, pairsDone, add1Checked, pairAddChecked, ms: Date.now() - t0 };
}

// ---- CLI ----
const mode = process.argv[2];
if (mode) {
  const arg = JSON.parse(process.argv[3] || "{}");
  if (mode === "board") {
    const bd = new Board(arg.n);
    console.log(JSON.stringify({ n: arg.n, F: bd.F, D: bd.cen.D, C: bd.cen.C, lines: bd.cen.lines.length, circles: bd.cen.circles.length }));
  } else if (mode === "witnesscheck") {
    const bd = new Board(arg.n);
    const st = new State(bd);
    for (const [x, y] of arg.coords) st.add(x + arg.n * y);
    console.log(JSON.stringify({ n: arg.n, k: st.size(), safe: st.viol === 0, maximal: st.uncovered === 0,
      uncovered: st.uncoveredList().map(p => [p % arg.n, (p / arg.n) | 0]) }));
  } else if (mode === "transplant") {
    const host = arg.host;
    const bd = new Board(host);
    const out = [];
    for (const w of WITNESSES) {
      if (w.n > host) continue;
      if (arg.srcN !== undefined && w.n !== arg.srcN) continue;
      const pl = transplant(w, bd);
      out.push({
        src: w.src, targetN: w.n, host, k: w.coords.length,
        placements: pl.length,
        transferCount: pl.filter(p2 => p2.uncoveredCount === 0).length,
        minUncovered: pl.length ? pl[0].uncoveredCount : null,
        histUncovered: Object.fromEntries([...new Set(pl.map(p2 => p2.uncoveredCount))].sort((a, b) => a - b).map(u => [u, pl.filter(p2 => p2.uncoveredCount === u).length])),
        best: pl.length ? { uncoveredCount: pl[0].uncoveredCount, uncoveredCells: pl[0].uncoveredCells, cells: pl[0].cells.map(c => [c % host, (c / host) | 0]) } : null,
      });
    }
    console.log(JSON.stringify(out));
  } else if (mode === "nets") {
    const bd = new Board(arg.n);
    const w = WITNESSES.find((x) => x.n === arg.n);
    const cells = w.coords.map(([x, y]) => x + arg.n * y);
    const res = localNets(bd, cells, arg.targetK ?? w.coords.length - 1);
    console.log(JSON.stringify({
      n: arg.n, k: res.k, targetK: res.targetK, counts: res.counts,
      r1a0: res.r1a0, r2a0: res.r2a0, r2a1: res.r2a1,
    }));
  } else if (mode === "sls") {
    const bd = new Board(arg.n);
    const rnd = makeRng(arg.seed || 12345);
    const targetK = arg.targetK;
    const seeds = [];
    for (const w of WITNESSES) {
      if (w.n > arg.n) continue;
      if (arg.seedMaxN !== undefined && w.n > arg.seedMaxN) continue;
      const pl = transplant(w, bd);
      for (const p of pl.slice(0, arg.placementsPerSeed || 6)) seeds.push(p.cells);
    }
    const out = [];
    for (let run = 0; run < (arg.runs || 1); run++) {
      const r = slsHunt(bd, targetK, seeds, arg.budgetMs || 20000, rnd);
      out.push({ run, n: arg.n, targetK, ...r, foundCoords: r.found });
      if (r.found) break;
      if (r.bestConfig) seeds.unshift(r.bestConfig.map(([x, y]) => x + arg.n * y));
    }
    console.log(JSON.stringify(out));
  } else if (mode === "sls2") {
    // v2 policy: exact-per-candidate coverage gain, no-self-removal, random-mix restarts
    const bd = new Board(arg.n);
    const rnd = makeRng(arg.seed || 12345);
    const targetK = arg.targetK;
    const seeds = [];
    for (const w of WITNESSES) {
      if (w.n > arg.n) continue;
      if (arg.seedMaxN !== undefined && w.n > arg.seedMaxN) continue;
      const pl = transplant(w, bd);
      for (const p of pl.slice(0, arg.placementsPerSeed || 8)) seeds.push(p.cells);
    }
    const out = [];
    for (let run = 0; run < (arg.runs || 1); run++) {
      const r = slsHuntV2(bd, targetK, seeds, arg.budgetMs || 20000, rnd, arg);
      out.push({ run, n: arg.n, targetK, ...r });
      if (r.found) break;
    }
    console.log(JSON.stringify(out));
  } else if (mode === "probe") {
    const bd = new Board(arg.n);
    const r = doubleSwapProbe(bd, arg.cells.map(([x, y]) => x + arg.n * y));
    console.log(JSON.stringify(r));
  } else if (mode === "probe2") {
    const bd = new Board(arg.n);
    const r = doubleSwapComplete(bd, arg.cells.map(([x, y]) => x + arg.n * y));
    console.log(JSON.stringify(r));
  }
}
