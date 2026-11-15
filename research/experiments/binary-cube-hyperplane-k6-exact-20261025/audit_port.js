// K0568 audit, enumerator B: verbatim algorithmic port of the repo's
// build_k6_circuits.cpp generator (commit f3868c53), executed in Node.
//
// The only deliberate substitution: the original eliminates modulo the
// Mersenne prime p = 2^61-1 using __int128 arithmetic, which has no exact
// analogue in ECMAScript doubles.  This port uses p' = 1,000,003 instead.
// Both primes exceed the Hadamard bound 7^3.5 ~ 907 for every minor of the
// 0/1-augmented matrices involved, so modular singularity over p' coincides
// with rational singularity exactly as over p; the substitution cannot
// change any dependence decision (the same argument the repo uses for its
// small-dimension audit primes 1,000,003 / 1,000,033).
//
// Everything else follows the C++ source: the same lexicographic subset
// enumeration, the same "circuit = dependent and no dependent (s-1)-subset"
// filter, the same CNF writer (Sinz sequential counters, counters first,
// then circuit clauses in size order, optional fix0 unit).
//
// Resumability (bookkeeping only; does not change enumeration or filtering
// semantics): all state files are written atomically (tmp+rename) at
// checkpoint boundaries so the run survives sandbox kills and resumes.
//   state_small.json  {done, dep, circ, rank_ok}     after each size 4..6
//   depflags{4,5,6}.bin raw dependency-flag dumps
//   state7.json       {a, b, dep7, circ7, total}      after each (a,b) row
//   --deadline-ms N   graceful self-stop after the current checkpoint
// Sizes 4..6 keep the per-leaf combinadic-rank validation of the original
// driver; the size-7 pass instead validates the total subset count at the
// end (the rank formula itself is validated by sizes 4..6 and by the
// d = 3, 4, 5 control runs).
//
// Usage:
//   node audit_port.js --dim 6 --out DIR [--deadline-ms N]   full d=6 run
//   node audit_port.js --dim 3|4|5                           small-dim control
//   node audit_port.js --cnf K OUT.cnf [--fix0] --family DIR CNF regeneration
'use strict';
const fs = require('fs');

const args = process.argv.slice(2);
const P = 1000003;

function main() {
  const t0 = Date.now();
  const log = (m) => console.log(`[${((Date.now() - t0) / 1000).toFixed(1)}s] ${m}`);

  // ---------- shared helpers ----------
  function buildTables(dim) {
    const N = 1 << dim, W = dim + 1;
    const ROW = new Int32Array(N * W);
    for (let v = 0; v < N; v++) {
      ROW[v * W] = 1;
      for (let c = 0; c < dim; c++) ROW[v * W + 1 + c] = (v >> c) & 1;
    }
    const C = new Array(N + 1);
    for (let n = 0; n <= N; n++) {
      C[n] = [1];
      for (let k = 1; k <= 8; k++) C[n][k] = Math.round(C[n][k - 1] * (n - k + 1) / k);
    }
    return { N, W, ROW, C };
  }

  // their rank_mod: Gaussian elimination without normalisation, mod P.
  function rankModFactory(ROW, W) {
    const A = new Float64Array(64);
    return function rankMod(vs, s) {
      for (let i = 0; i < s; i++) {
        const b = vs[i] * W;
        for (let j = 0; j < W; j++) A[i * W + j] = ROW[b + j];
      }
      let rank = 0;
      for (let j = 0; j < W && rank < s; ++j) {
        let piv = -1;
        for (let i = rank; i < s; i++) if (A[i * W + j] !== 0) { piv = i; break; }
        if (piv < 0) continue;
        if (piv !== rank) {
          for (let k = j; k < W; ++k) { const t = A[rank * W + k]; A[rank * W + k] = A[piv * W + k]; A[piv * W + k] = t; }
        }
        const g = A[rank * W + j];
        for (let i = rank + 1; i < s; ++i) {
          const f = A[i * W + j];
          if (f === 0) continue;
          const ri = i * W, rk = rank * W;
          for (let k = j; k < W; ++k) A[ri + k] = (A[ri + k] * g % P + P - f * A[rk + k] % P) % P;
        }
        ++rank;
      }
      return rank;
    };
  }

  // ---------- CNF writer (verbatim port of at_most_k_clauses) ----------
  function atMostKClauses(lits, k, nextVar, out) {
    const n = lits.length;
    if (k === 0) { for (const lit of lits) out.push([-lit]); return nextVar; }
    if (k >= n) return nextVar;
    const s = [];
    for (let i = 0; i < n; i++) { s.push([]); for (let j = 0; j < k; j++) s[i].push(nextVar++); }
    out.push([-lits[0], s[0][0]]);
    for (let j = 1; j < k; j++) out.push([-s[0][j]]);
    for (let i = 1; i < n; i++) {
      out.push([-lits[i], s[i][0]]);
      out.push([-s[i - 1][0], s[i][0]]);
      for (let j = 1; j < k; j++) {
        out.push([-s[i - 1][j], s[i][j]]);
        out.push([-lits[i], -s[i - 1][j - 1], s[i][j]]);
      }
      out.push([-lits[i], -s[i - 1][k - 1]]);
    }
    return nextVar;
  }

  const cnfIdx = args.indexOf('--cnf');
  if (cnfIdx >= 0) {
    const K = parseInt(args[cnfIdx + 1], 10);
    const cnfPath = args[cnfIdx + 2];
    const fix0 = args.includes('--fix0');
    const famIdx = args.indexOf('--family');
    const famDir = args[famIdx + 1];
    if (K < 7 || K > 64) throw new Error('circuit CNF requires 7 <= K <= 64');
    const circuits = [];
    for (const s of [4, 5, 6, 7]) {
      const buf = fs.readFileSync(`${famDir}/circuits${s}.bin`);
      for (let off = 0; off + 8 <= buf.length; off += 8) {
        const rec = [];
        for (let i = 0; i < s; i++) rec.push(buf[off + i]);
        circuits.push(rec);
      }
    }
    let nextVar = 65;
    const counterClauses = [];
    {
      const lits = []; for (let i = 0; i < 64; i++) lits.push(i + 1);
      nextVar = atMostKClauses(lits, K, nextVar, counterClauses);
    }
    {
      const lits = []; for (let i = 0; i < 64; i++) lits.push(-(i + 1));
      nextVar = atMostKClauses(lits, 64 - K, nextVar, counterClauses);
    }
    const total = counterClauses.length + circuits.length + (fix0 ? 1 : 0);
    const fd = fs.openSync(cnfPath, 'w');
    let chunk = `p cnf ${nextVar - 1} ${total}\n`;
    if (fix0) chunk += '1 0\n';
    for (const c of counterClauses) { for (const l of c) chunk += l + ' '; chunk += '0\n'; }
    for (const c of circuits) { for (const v of c) chunk += -(v + 1) + ' '; chunk += '0\n'; }
    fs.writeSync(fd, chunk);
    fs.closeSync(fd);
    console.log(JSON.stringify({ cnf: cnfPath, vars: nextVar - 1, clauses: total, counter_clauses: counterClauses.length, circuits: circuits.length }));
    return;
  }

  // ---------- enumeration runs ----------
  const dim = parseInt(args[args.indexOf('--dim') + 1], 10);
  const outDirIdx = args.indexOf('--out');
  const OUT = outDirIdx >= 0 ? args[outDirIdx + 1] : null;
  const dlIdx = args.indexOf('--deadline-ms');
  const DEADLINE = dlIdx >= 0 ? Date.now() + parseInt(args[dlIdx + 1], 10) : Infinity;
  const { N, W, ROW, C } = buildTables(dim);
  const rankMod = rankModFactory(ROW, W);

  const q = Math.min(dim + 1, 7);
  const TOTAL = {}; for (let s = 4; s <= q; s++) TOTAL[s] = C[N][s];
  const dep = {}, circ = {};
  const depFlags = {};
  let rankOk = true;

  function rankSubset(c, s) {
    let r = 0, prev = -1;
    for (let i = 0; i < s; i++) {
      r += C[N - 1 - prev][s - i] - C[N - c[i]][s - i];
      prev = c[i];
    }
    return r;
  }

  const exists = (p) => { try { fs.accessSync(p); return true; } catch { return false; } };
  function atomicWrite(path, data) {
    const tmp = path + '.tmp';
    fs.writeFileSync(tmp, data);
    fs.renameSync(tmp, path);
  }

  // idempotent rerun guard
  if (OUT && exists(`${OUT}/summary.json`)) {
    console.log(fs.readFileSync(`${OUT}/summary.json`, 'utf8'));
    return;
  }

  if (dim === 6 && OUT) {
    fs.mkdirSync(OUT, { recursive: true });

    // ---- resume bookkeeping for sizes 4..6 ----
    let smallDone = 0;
    if (exists(`${OUT}/state_small.json`)) {
      const st = JSON.parse(fs.readFileSync(`${OUT}/state_small.json`, 'utf8'));
      smallDone = st.done;
      dep[4] = st.dep[4]; dep[5] = st.dep[5]; dep[6] = st.dep[6];
      circ[4] = st.circ[4]; circ[5] = st.circ[5]; circ[6] = st.circ[6];
      rankOk = st.rank_ok;
      for (let s = 4; s <= smallDone; s++) depFlags[s] = fs.readFileSync(`${OUT}/depflags${s}.bin`);
      log(`resuming: sizes 4..${smallDone} already complete`);
    }

    // ---- sizes 4, 5, 6: original generic passes, circuits streamed at leaves ----
    for (let s = 4; s <= 6; s++) {
      if (s <= smallDone) continue;
      dep[s] = 0; circ[s] = 0;
      depFlags[s] = new Uint8Array(TOTAL[s]);
      const prevFlags = s > 4 ? depFlags[s - 1] : null;
      let fd = fs.openSync(`${OUT}/circuits${s}.bin`, 'w');
      let wbuf = Buffer.alloc(8 * 16384), wpos = 0;
      const flush = () => { if (wpos > 0) { fs.writeSync(fd, wbuf, 0, wpos); wpos = 0; } };
      const p = new Int32Array(s);
      const sub = new Int32Array(s - 1);
      let counter = 0;
      (function enumerate(start, depth) {
        if (depth === s) {
          if (rankSubset(p, s) !== counter) { rankOk = false; throw new Error(`rank mismatch size ${s} at ${counter}`); }
          if (rankMod(p, s) < s) {
            dep[s]++; depFlags[s][counter] = 1;
            let hasDepSub = false;
            if (prevFlags) {
              for (let skip = 0; skip < s; skip++) {
                let t = 0;
                for (let i = 0; i < s; i++) if (i !== skip) sub[t++] = p[i];
                if (prevFlags[rankSubset(sub, s - 1)]) { hasDepSub = true; break; }
              }
            }
            if (!hasDepSub) {
              circ[s]++;
              for (let i = 0; i < s; i++) wbuf[wpos++] = p[i];
              for (let i = s; i < 8; i++) wbuf[wpos++] = 0;
              if (wpos === wbuf.length) flush();
            }
          }
          counter++;
          return;
        }
        for (let v = start; v < N; v++) { p[depth] = v; enumerate(v + 1, depth + 1); }
      })(0, 0);
      if (counter !== TOTAL[s]) throw new Error(`size ${s}: enumerated ${counter} != ${TOTAL[s]}`);
      flush(); fs.closeSync(fd);
      atomicWrite(`${OUT}/depflags${s}.bin`, depFlags[s]);
      const st = { done: s, dep: { 4: dep[4], 5: dep[5], 6: dep[6] }, circ: { 4: circ[4], 5: circ[5], 6: circ[6] }, rank_ok: rankOk };
      atomicWrite(`${OUT}/state_small.json`, JSON.stringify(st));
      log(`size ${s}: dependent ${dep[s]} / ${TOTAL[s]}, circuits ${circ[s]}`);
      if (Date.now() > DEADLINE) {
        log(`deadline reached after size ${s}; state saved, rerun to resume`);
        console.log(JSON.stringify({ status: 'paused', size_done: s }));
        return;
      }
    }

    // ---- size 7: lexicographic nested loops (same order as the generic
    // driver), rank_mod oracle, per-(a,b)-row checkpoints -----------------
    dep[7] = 0; circ[7] = 0;
    let total = 0;
    let a0 = 0, b0 = 1, resume7 = false;
    if (exists(`${OUT}/state7.json`)) {
      const st = JSON.parse(fs.readFileSync(`${OUT}/state7.json`, 'utf8'));
      a0 = st.a; b0 = st.b; dep[7] = st.dep7; circ[7] = st.circ7; total = st.total;
      resume7 = true;
      log(`resuming size 7 at (a,b)=(${a0},${b0}), total ${total}, circuits ${circ[7]}`);
    }
    const d6 = depFlags[6];
    const VS7 = new Int32Array(7);
    const SUB6 = new Int32Array(6);
    let fd = fs.openSync(`${OUT}/circuits7.bin`, resume7 ? 'a' : 'w');
    let wbuf = Buffer.alloc(8 * 65536), wpos = 0;
    const flush = () => { if (wpos > 0) { fs.writeSync(fd, wbuf, 0, wpos); wpos = 0; } };
    for (let a = a0; a <= 57; a++) {
      const bStart = (a === a0) ? b0 : a + 1;
      for (let b = bStart; b <= 58; b++) {
        const rowStart = Date.now();
        for (let c = b + 1; c <= 59; c++) {
          for (let d = c + 1; d <= 60; d++) {
            for (let e = d + 1; e <= 61; e++) {
              for (let f = e + 1; f <= 62; f++) {
                for (let g = f + 1; g <= 63; g++) {
                  total++;
                  VS7[0] = a; VS7[1] = b; VS7[2] = c; VS7[3] = d; VS7[4] = e; VS7[5] = f; VS7[6] = g;
                  if (rankMod(VS7, 7) < 7) {
                    dep[7]++;
                    let hasDepSub = false;
                    SUB6[0] = b; SUB6[1] = c; SUB6[2] = d; SUB6[3] = e; SUB6[4] = f; SUB6[5] = g;
                    if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = c; SUB6[2] = d; SUB6[3] = e; SUB6[4] = f; SUB6[5] = g;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = b; SUB6[2] = d; SUB6[3] = e; SUB6[4] = f; SUB6[5] = g;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = b; SUB6[2] = c; SUB6[3] = e; SUB6[4] = f; SUB6[5] = g;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = b; SUB6[2] = c; SUB6[3] = d; SUB6[4] = f; SUB6[5] = g;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = b; SUB6[2] = c; SUB6[3] = d; SUB6[4] = e; SUB6[5] = g;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      SUB6[0] = a; SUB6[1] = b; SUB6[2] = c; SUB6[3] = d; SUB6[4] = e; SUB6[5] = f;
                      if (d6[rankSubset(SUB6, 6)]) hasDepSub = true;
                    }
                    if (!hasDepSub) {
                      circ[7]++;
                      wbuf[wpos++] = a; wbuf[wpos++] = b; wbuf[wpos++] = c; wbuf[wpos++] = d;
                      wbuf[wpos++] = e; wbuf[wpos++] = f; wbuf[wpos++] = g; wbuf[wpos++] = 0;
                      if (wpos === wbuf.length) flush();
                    }
                  }
                }
              }
            }
          }
        }
        // checkpoint at end of each (a,b) row
        let na = a, nb = b + 1;
        if (nb > 58) { na = a + 1; nb = na + 1; }
        flush();
        atomicWrite(`${OUT}/state7.json`, JSON.stringify({ a: na, b: nb, dep7: dep[7], circ7: circ[7], total }));
        if (a % 8 === 0 || Date.now() - rowStart > 2000) {
          log(`row (a=${a},b=${b}): ${Date.now() - rowStart}ms, cum total ${total}, dependent ${dep[7]}, circuits7 ${circ[7]}`);
        }
        if (Date.now() > DEADLINE) {
          flush(); fs.closeSync(fd);
          log(`deadline reached at (a,b)=(${na},${nb}); state saved, rerun to resume`);
          console.log(JSON.stringify({ status: 'paused', a: na, b: nb, dep7: dep[7], circ7: circ[7], total }));
          return;
        }
      }
    }
    flush(); fs.closeSync(fd);
    if (total !== TOTAL[7]) throw new Error(`size 7: enumerated ${total} != ${TOTAL[7]}`);
    log(`size 7: dependent ${dep[7]} / ${TOTAL[7]}, circuits ${circ[7]}`);
    fs.rmSync(`${OUT}/state7.json`, { force: true });
  } else {
    // ---- generic path for d = 3, 4, 5 (unchanged control) -----------------
    for (let s = 4; s <= q; s++) {
      const depFlagsS = new Uint8Array(TOTAL[s]);
      dep[s] = 0; circ[s] = 0;
      const prevFlags = s > 4 ? depFlags[s - 1] : null;
      const p = new Int32Array(s);
      const sub = new Int32Array(s - 1);
      let counter = 0;
      (function enumerate(start, depth) {
        if (depth === s) {
          if (rankSubset(p, s) !== counter) { rankOk = false; throw new Error(`rank mismatch size ${s} at ${counter}`); }
          if (rankMod(p, s) < s) {
            dep[s]++; depFlagsS[counter] = 1;
            let hasDepSub = false;
            if (prevFlags) {
              for (let skip = 0; skip < s; skip++) {
                let t = 0;
                for (let i = 0; i < s; i++) if (i !== skip) sub[t++] = p[i];
                if (prevFlags[rankSubset(sub, s - 1)]) { hasDepSub = true; break; }
              }
            }
            if (!hasDepSub) circ[s]++;
          }
          counter++;
          return;
        }
        for (let v = start; v < N; v++) { p[depth] = v; enumerate(v + 1, depth + 1); }
      })(0, 0);
      depFlags[s] = depFlagsS;
      log(`size ${s}: dependent ${dep[s]} / ${TOTAL[s]}, circuits ${circ[s]}`);
    }
  }

  const res = {
    oracle: `ported build_k6_circuits.cpp algorithm, modular elimination mod ${P} (original: 2^61-1; equivalence via Hadamard bound)`,
    dim, N, W,
    rank_validated: rankOk,
    dependent: dep, circuits: circ,
    totals: TOTAL,
    elapsed_ms: Date.now() - t0,
  };
  if (OUT) {
    atomicWrite(`${OUT}/summary.json`, JSON.stringify(res, null, 2) + '\n');
  }
  console.log(JSON.stringify(res));
}
main();
