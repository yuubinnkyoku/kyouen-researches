// K0568 audit, enumerator A: independent implementation (no relation to the
// repo's C++ generator beyond the mathematical definition of the circuit
// family: an affine circuit is an inclusion-minimal affinely dependent vertex
// set).
//
// Oracle: exact integer arithmetic via Bareiss-fraction determinant
// elimination on doubles.  Every intermediate Bareiss value is a minor of a
// 0/1 matrix with at most 7 rows, so |value| <= Hadamard bound 7^3.5 ~ 907
// << 2^53: double arithmetic is exact, no overflow, no rounding.
//  - square case (s = W = dim+1 rows x cols): dependent iff det = 0.
//  - wide case (s < W): dependent iff ALL s x s column submatrices are
//    singular (rank < s); early exit on the first nonsingular minor.
// Minimality logic: affine dependence is hereditary (any superset of a
// dependent set is dependent), so a dependent s-set is a circuit iff none of
// its (s-1)-subsets is dependent.  For s = 4 every dependent 4-set is a
// circuit because the d-dimensional hypercube {0,1}^d contains no 3
// collinear vertices (checked explicitly below for d = 6).
//
// Outputs (when --out DIR is given):
//   circuits{4,5,6,7}.bin  8-byte records, lexicographic order:
//                          first s bytes = ascending vertex ids, rest zero.
//   summary.json           counts + oracle description.
// Combinadic-rank validation: the enumeration counter of every s-subset is
// compared against the combinadic rank of the subset at every leaf for
// sizes 4..6 (size 7 validates the total count instead).
//
// Resumability: this script is designed to survive arbitrary process kills
// (sandbox command timeouts / environment resets).  All state files are
// written atomically (tmp + rename) at checkpoint boundaries; a re-run with
// the same --out resumes exactly where the previous run stopped.  The
// checkpointing only records *where* the lexicographic enumeration stands;
// it does not change any enumeration or filtering semantics.
//   state_small.json  {done, dep, circ, rank_ok}      after each size 4..6
//   depflags{4,5,6}.bin  raw Uint8Array dependency flags (dumps)
//   state7.json       {a, b, dep7, circ7, total}      after each (a,b) row
//   --deadline-ms N   graceful self-stop after the current checkpoint
//
// Usage:
//   node audit_mine.js --dim 6 --out DIR [--deadline-ms N]
//   node audit_mine.js --dim 3|4|5     small-dimension control (no OUT)
'use strict';
const fs = require('fs');

const args = process.argv.slice(2);
const dim = parseInt(args[args.indexOf('--dim') + 1], 10);
const outDirIdx = args.indexOf('--out');
const OUT = outDirIdx >= 0 ? args[outDirIdx + 1] : null;
const dlIdx = args.indexOf('--deadline-ms');
const DEADLINE = dlIdx >= 0 ? Date.now() + parseInt(args[dlIdx + 1], 10) : Infinity;
const N = 1 << dim;
const W = dim + 1;

// ---- augmented rows: [1, x_0 .. x_{d-1}] --------------------------------
const ROW = new Int32Array(N * W);
for (let v = 0; v < N; v++) {
  ROW[v * W] = 1;
  for (let c = 0; c < dim; c++) ROW[v * W + 1 + c] = (v >> c) & 1;
}

// ---- binomials -----------------------------------------------------------
const C = new Array(N + 1);
for (let n = 0; n <= N; n++) {
  C[n] = [1];
  for (let k = 1; k <= 8; k++) C[n][k] = Math.round(C[n][k - 1] * (n - k + 1) / k);
}

// ---- exact oracles -------------------------------------------------------
const SC = new Float64Array(64);

function bareissDet(s) {
  let prev = 1;
  for (let k = 0; k < s; k++) {
    let piv = -1;
    for (let i = k; i < s; i++) if (SC[i * s + k] !== 0) { piv = i; break; }
    if (piv < 0) return 0;
    if (piv !== k) {
      for (let j = k; j < s; j++) { const t = SC[k * s + j]; SC[k * s + j] = SC[piv * s + j]; SC[piv * s + j] = t; }
    }
    const p = SC[k * s + k];
    for (let i = k + 1; i < s; i++) {
      const f = SC[i * s + k];
      if (f === 0) continue;
      for (let j = k + 1; j < s; j++) {
        SC[i * s + j] = (p * SC[i * s + j] - f * SC[k * s + j]) / prev;
      }
    }
    prev = p;
  }
  return SC[(s - 1) * s + (s - 1)];
}

const COLSETS = {};
function colsets(s) {
  if (!COLSETS[s]) {
    const all = [];
    const cur = [];
    (function rec(start) {
      if (cur.length === s) { all.push(cur.slice()); return; }
      for (let j = start; j < W; j++) { cur.push(j); rec(j + 1); cur.pop(); }
    })(0);
    COLSETS[s] = all;
  }
  return COLSETS[s];
}

function dependent(pts, s) {
  if (s === W) {
    for (let i = 0; i < s; i++) {
      const b = pts[i] * W;
      for (let j = 0; j < s; j++) SC[i * s + j] = ROW[b + j];
    }
    return bareissDet(s) === 0;
  }
  for (const cs of colsets(s)) {
    for (let i = 0; i < s; i++) {
      const b = pts[i] * W;
      for (let j = 0; j < s; j++) SC[i * s + j] = ROW[b + cs[j]];
    }
    if (bareissDet(s) !== 0) return false;
  }
  return true;
}

// ---- combinadic rank of a sorted s-subset of {0..N-1} ---------------------
function rankSubset(c, s) {
  let r = 0, prev = -1;
  for (let i = 0; i < s; i++) {
    r += C[N - 1 - prev][s - i] - C[N - c[i]][s - i];
    prev = c[i];
  }
  return r;
}

// ---- d=6 hot paths ---------------------------------------------------------
const M7 = new Float64Array(49);
const M7VS = new Int32Array(7);
function dep7(v0, v1, v2, v3, v4, v5, v6) {
  const vs = M7VS; vs[0] = v0; vs[1] = v1; vs[2] = v2; vs[3] = v3; vs[4] = v4; vs[5] = v5; vs[6] = v6;
  for (let i = 0; i < 7; i++) {
    const b = vs[i] * 7, r = i * 7;
    M7[r] = ROW[b]; M7[r + 1] = ROW[b + 1]; M7[r + 2] = ROW[b + 2]; M7[r + 3] = ROW[b + 3];
    M7[r + 4] = ROW[b + 4]; M7[r + 5] = ROW[b + 5]; M7[r + 6] = ROW[b + 6];
  }
  let prev = 1;
  for (let k = 0; k < 7; k++) {
    let piv = -1;
    for (let i = k; i < 7; i++) if (M7[i * 7 + k] !== 0) { piv = i; break; }
    if (piv < 0) return true;
    if (piv !== k) {
      for (let j = k; j < 7; j++) { const t = M7[k * 7 + j]; M7[k * 7 + j] = M7[piv * 7 + j]; M7[piv * 7 + j] = t; }
    }
    const p = M7[k * 7 + k];
    for (let i = k + 1; i < 7; i++) {
      const f = M7[i * 7 + k];
      if (f === 0) continue;
      const ri = i * 7, rk = k * 7;
      for (let j = k + 1; j < 7; j++) M7[ri + j] = (p * M7[ri + j] - f * M7[rk + j]) / prev;
    }
    prev = p;
  }
  return false;
}
const R6 = new Int32Array(6);
// rank of a 6-subset (u0<...<u5) of {0..63} in lex order of C(64,6)
function rank6(u0, u1, u2, u3, u4, u5) {
  const u = R6; u[0] = u0; u[1] = u1; u[2] = u2; u[3] = u3; u[4] = u4; u[5] = u5;
  let r = 0, prev = -1;
  for (let i = 0; i < 6; i++) {
    r += C[63 - prev][6 - i] - C[64 - u[i]][6 - i];
    prev = u[i];
  }
  return r;
}

// ---- atomic state helpers --------------------------------------------------
function atomicWrite(path, data) {
  const tmp = path + '.tmp';
  fs.writeFileSync(tmp, data);
  fs.renameSync(tmp, path);
}
const exists = (p) => { try { fs.accessSync(p); return true; } catch { return false; } };

// ---- driver ---------------------------------------------------------------
function main() {
  const t0 = Date.now();
  const log = (m) => console.log(`[${((Date.now() - t0) / 1000).toFixed(1)}s] ${m}`);

  // idempotent rerun guard
  if (OUT && exists(`${OUT}/summary.json`)) {
    console.log(fs.readFileSync(`${OUT}/summary.json`, 'utf8'));
    return;
  }

  // 0. no 3 collinear vertices (justifies circuit4 == dependent4)
  let collinear3 = 0;
  {
    const p3 = new Int32Array(3);
    for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) for (let c = b + 1; c < N; c++) {
      p3[0] = a; p3[1] = b; p3[2] = c;
      if (dependent(p3, 3)) collinear3++;
    }
  }
  log(`collinear triples: ${collinear3} (expected 0)`);

  const q = Math.min(dim + 1, 7);
  const TOTAL = {}; for (let s = 4; s <= q; s++) TOTAL[s] = C[N][s];
  const dep = {}, circ = {};
  const depFlags = {};
  let rankOk = true;

  if (dim === 6) {
    if (OUT) fs.mkdirSync(OUT, { recursive: true });

    // ---- resume bookkeeping for sizes 4..6 ----
    let smallDone = 0;
    if (OUT && exists(`${OUT}/state_small.json`)) {
      const st = JSON.parse(fs.readFileSync(`${OUT}/state_small.json`, 'utf8'));
      smallDone = st.done; dep[4] = st.dep[4]; dep[5] = st.dep[5]; dep[6] = st.dep[6];
      circ[4] = st.circ[4]; circ[5] = st.circ[5]; circ[6] = st.circ[6];
      rankOk = st.rank_ok;
      for (let s = 4; s <= smallDone; s++) depFlags[s] = fs.readFileSync(`${OUT}/depflags${s}.bin`);
      log(`resuming: sizes 4..${smallDone} already complete`);
    }

    // ---- sizes 4, 5, 6: recursive enumeration, circuits streamed at leaves ----
    for (let s = 4; s <= 6; s++) {
      if (s <= smallDone) continue;
      dep[s] = 0; circ[s] = 0;
      depFlags[s] = new Uint8Array(TOTAL[s]);
      const prevFlags = s > 4 ? depFlags[s - 1] : null;
      let fd = null, wbuf = null, wpos = 0;
      if (OUT) { fd = fs.openSync(`${OUT}/circuits${s}.bin`, 'w'); wbuf = Buffer.alloc(8 * 65536); }
      const flush = () => { if (fd !== null && wpos > 0) { fs.writeSync(fd, wbuf, 0, wpos); wpos = 0; } };
      const p = new Int32Array(s);
      const sub = new Int32Array(s - 1);
      let counter = 0;
      (function enumerate(start, depth) {
        if (depth === s) {
          if (rankSubset(p, s) !== counter) { rankOk = false; throw new Error(`rank mismatch size ${s} at ${counter}`); }
          if (s === 6 && rank6(p[0], p[1], p[2], p[3], p[4], p[5]) !== counter) { rankOk = false; throw new Error(`rank6 mismatch at ${counter}`); }
          if (dependent(p, s)) {
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
              if (fd !== null) {
                for (let i = 0; i < s; i++) wbuf[wpos++] = p[i];
                for (let i = s; i < 8; i++) wbuf[wpos++] = 0;
                if (wpos === wbuf.length) flush();
              }
            }
          }
          counter++;
          return;
        }
        for (let v = start; v < N; v++) { p[depth] = v; enumerate(v + 1, depth + 1); }
      })(0, 0);
      if (counter !== TOTAL[s]) throw new Error(`size ${s}: enumerated ${counter} != ${TOTAL[s]}`);
      flush(); if (fd !== null) fs.closeSync(fd);
      if (OUT) {
        atomicWrite(`${OUT}/depflags${s}.bin`, depFlags[s]);
        const st = { done: s, dep: { 4: dep[4], 5: dep[5], 6: dep[6] }, circ: { 4: circ[4], 5: circ[5], 6: circ[6] }, rank_ok: rankOk };
        atomicWrite(`${OUT}/state_small.json`, JSON.stringify(st));
      }
      log(`size ${s}: dependent ${dep[s]} / ${TOTAL[s]}, circuits ${circ[s]}`);
      if (Date.now() > DEADLINE) {
        log(`deadline reached after size ${s}; state saved, rerun to resume`);
        console.log(JSON.stringify({ status: 'paused', size_done: s }));
        return;
      }
    }

    // ---- size 7: hot nested loops, per-(a,b)-row checkpoints ----------------
    dep[7] = 0; circ[7] = 0;
    let total = 0;
    let a0 = 0, b0 = 1, resume7 = false;
    if (OUT && exists(`${OUT}/state7.json`)) {
      const st = JSON.parse(fs.readFileSync(`${OUT}/state7.json`, 'utf8'));
      a0 = st.a; b0 = st.b; dep[7] = st.dep7; circ[7] = st.circ7; total = st.total;
      resume7 = true;
      log(`resuming size 7 at (a,b)=(${a0},${b0}), total ${total}, circuits ${circ[7]}`);
    }
    const d6 = depFlags[6];
    let fd = null, wbuf = null, wpos = 0;
    if (OUT) {
      fd = fs.openSync(`${OUT}/circuits7.bin`, resume7 ? 'a' : 'w');
      wbuf = Buffer.alloc(8 * 65536);
    }
    const flush = () => { if (fd !== null && wpos > 0) { fs.writeSync(fd, wbuf, 0, wpos); wpos = 0; } };
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
                  if (dep7(a, b, c, d, e, f, g)) {
                    dep[7]++;
                    if (!(d6[rank6(b, c, d, e, f, g)] ||
                          d6[rank6(a, c, d, e, f, g)] ||
                          d6[rank6(a, b, d, e, f, g)] ||
                          d6[rank6(a, b, c, e, f, g)] ||
                          d6[rank6(a, b, c, d, f, g)] ||
                          d6[rank6(a, b, c, d, e, g)] ||
                          d6[rank6(a, b, c, d, e, f)])) {
                      circ[7]++;
                      if (fd !== null) {
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
        }
        // checkpoint at end of each (a,b) row
        let na = a, nb = b + 1;
        if (nb > 58) { na = a + 1; nb = na + 1; }
        if (OUT) {
          flush();
          atomicWrite(`${OUT}/state7.json`, JSON.stringify({ a: na, b: nb, dep7: dep[7], circ7: circ[7], total }));
        }
        if (na % 8 === 0 || Date.now() - rowStart > 2000) {
          log(`row (a=${a},b=${b}): ${(Date.now() - rowStart)}ms, cum total ${total}, dependent ${dep[7]}, circuits7 ${circ[7]}`);
        }
        if (Date.now() > DEADLINE) {
          flush(); if (fd !== null) fs.closeSync(fd);
          log(`deadline reached at (a,b)=(${na},${nb}); state saved, rerun to resume`);
          console.log(JSON.stringify({ status: 'paused', a: na, b: nb, dep7: dep[7], circ7: circ[7], total }));
          return;
        }
      }
    }
    flush(); if (fd !== null) fs.closeSync(fd);
    if (total !== TOTAL[7]) throw new Error(`size 7: enumerated ${total} != ${TOTAL[7]}`);
    log(`size 7: dependent ${dep[7]} / ${TOTAL[7]}, circuits ${circ[7]}`);
    if (OUT) fs.rmSync(`${OUT}/state7.json`, { force: true });
  } else {
    // ---- generic control path for d = 3, 4, 5 ------------------------------
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
          if (dependent(p, s)) {
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
    oracle: 'exact-integer Bareiss elimination (square) / all-minors rank test (wide); no modular arithmetic',
    dim, N, W,
    collinear3,
    rank_validated: rankOk,
    dependent: dep, circuits: circ,
    totals: TOTAL,
    elapsed_ms: Date.now() - t0,
  };
  if (OUT) fs.writeFileSync(`${OUT}/summary.json`, JSON.stringify(res, null, 2) + '\n');
  console.log(JSON.stringify(res));
}
main();
