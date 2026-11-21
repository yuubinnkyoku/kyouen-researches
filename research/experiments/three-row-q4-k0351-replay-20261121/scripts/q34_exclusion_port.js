'use strict';
/*
 * Faithful Node.js port of the K0351 engine q34_support_exclusion.cpp
 * (3 x m, q=4: exterior-three cover-existence search, widths 9..68).
 *
 * Port policy: statement-for-statement transliteration of the pinned C++
 * source (sha256 6960331d..., K34 HEAD), including loop order, pruning
 * thresholds, the (k && j < i) symmetry cut and the candidate counters.
 * Masks: unsigned __int128 -> three 32-bit words (m <= 68 -> bits 0..67).
 *
 * Only deliberate representation change: per-candidate cover() inlines the
 * 9-slab merged adjacency gm[] (which depends on (i,j,k) only); this is a
 * pure factorization, not an algorithmic change.
 *
 * Usage: node q34_exclusion_port.js LOW HIGH
 * Output: one JSON line per width: {m, three_sets, cover_exists,
 *         candidates, witnesses, seconds}
 */

function pc(v) {                    // popcount of a 32-bit word
  v = v - ((v >>> 1) & 0x55555555);
  v = (v & 0x33333333) + ((v >>> 2) & 0x33333333);
  v = (v + (v >>> 4)) & 0x0f0f0f0f;
  return (v * 0x01010101) >>> 24;
}
const pc3 = (a, b, c) => pc(a) + pc(b) + pc(c);

// roots(s, p, m): columns of x^2 - s x + p = 0 within [0, m); word triple -> W.
function rootsW(s, p, m, W) {
  const d = s * s - 4 * p;
  if (d < 0) return;
  let r = Math.sqrt(d) | 0;
  while ((r + 1) * (r + 1) <= d) ++r;
  while (r * r > d) --r;
  if (r * r !== d || ((s - r) & 1) !== 0) return;
  const a = (s - r) >> 1, b = (s + r) >> 1;
  if (a >= 0 && a < m) W[a >> 5] |= 1 << (a & 31);
  if (b >= 0 && b < m) W[b >> 5] |= 1 << (b & 31);
}

// triple(pair a, col b, kind, m), exactly as in the C++ source.
function tripleW(as, ap, bcol, kind, m, W) {
  const pb = bcol * (as - bcol);
  let pt;
  if (kind === 0) pt = 2 + 2 * ap - pb;
  else if (kind === 1) pt = 2 + 2 * pb - ap;
  else {
    const nn = ap + pb - 2;
    if ((nn & 1) !== 0) return;
    pt = nn >> 1;
  }
  rootsW(as, pt, m, W);
}

function threes(m) {
  const xs = [], ps = [], pp = [];
  for (let a = 0; a < m; ++a)
    for (let b = a + 1; b < m; ++b)
      for (let c = b + 1; c < m; ++c) {
        xs.push(a, b, c);
        ps.push(a + b, a + c, b + c);
        pp.push(a * b, a * c, b * c);
      }
  return {
    n: (xs.length / 3) | 0,
    x: Int32Array.from(xs), s: Int32Array.from(ps), p: Int32Array.from(pp),
  };
}

function runWidth(m) {
  const t0 = process.hrtime.bigint();
  const v = threes(m);
  const n = v.n;
  const m81 = 69;              // target-row adjacency width, as in C++

  // ---- z[kind][i*m + c]: blocked-target-mask word triples ---------------
  const z = [];
  for (let kind = 0; kind < 3; ++kind) {
    const zz = new Int32Array(n * m * 3);
    const W = [0, 0, 0];
    for (let i = 0; i < n; ++i) {
      const s0 = v.s[i * 3], s1 = v.s[i * 3 + 1], s2 = v.s[i * 3 + 2];
      const p0 = v.p[i * 3], p1 = v.p[i * 3 + 1], p2 = v.p[i * 3 + 2];
      for (let c = 0; c < m; ++c) {
        W[0] = 0; W[1] = 0; W[2] = 0;
        tripleW(s0, p0, c, kind, m, W);
        tripleW(s1, p1, c, kind, m, W);
        tripleW(s2, p2, c, kind, m, W);
        const o = (i * m + c) * 3;
        zz[o] = W[0]; zz[o + 1] = W[1]; zz[o + 2] = W[2];
      }
    }
    z.push(zz);
  }

  // ---- g[k]: per (b,c) adjacency slabs and support ----------------------
  const g = [];
  for (let k = 0; k < 2; ++k) {
    const middle = (k === 1);
    const adj = new Int32Array(m * m * m81 * 3);
    const sup = new Int32Array(m * m * 3);
    for (let b = 0; b < m; ++b)
      for (let c = 0; c < m; ++c) {
        const slab = (b * m + c) * m81 * 3;
        const soff = (b * m + c) * 3;
        for (let a = 0; a < m; ++a) {
          let num, den;
          if (middle) { num = 2 - a * (b + c) + b * b + c * c; den = b + c - 2 * a; }
          else { num = 2 + a * (2 * b - c) - 2 * b * b + c * c; den = a - 2 * b + c; }
          if (den === 0 || (num % den) !== 0) continue;
          const x = (num / den) | 0;
          if (x < 0 || x >= m || x === a) continue;
          adj[slab + a * 3 + (x >> 5)] |= 1 << (x & 31);
          sup[soff + (a >> 5)] |= 1 << (a & 31);
          sup[soff + (x >> 5)] |= 1 << (x & 31);
        }
      }
    g.push({ adj, sup });
  }

  // full first-m-bit mask, as words (2**k avoids the JS shift-mod-32 pitfall)
  const fullW = [-1, -1, -1];
  if (m <= 32) { fullW[0] = (2 ** m - 1) | 0; fullW[1] = 0; fullW[2] = 0; }
  else if (m <= 64) { fullW[0] = -1; fullW[1] = (2 ** (m - 32) - 1) | 0; fullW[2] = 0; }
  else { fullW[0] = -1; fullW[1] = -1; fullW[2] = (2 ** (m - 64) - 1) | 0; }

  // ---- main pair sweep ---------------------------------------------------
  const found = [false, false];
  const candidates = [0, 0];
  const wA = [[0, 0], [0, 0]];
  const wBx = [[0, 0, 0], [0, 0, 0]];
  const wCx = [[0, 0, 0], [0, 0, 0]];
  const gm = new Int32Array(m81 * 3);
  const nbuf = new Int32Array(m81 * 3);
  const need = [0, 0, 0];
  const bxs = [0, 0, 0], cxs = [0, 0, 0];

  for (let i = 0; i < n; ++i) {
    const bi = i * 3;
    const bx0 = v.x[bi], bx1 = v.x[bi + 1], bx2 = v.x[bi + 2];
    const bs0 = v.s[bi], bs1 = v.s[bi + 1], bs2 = v.s[bi + 2];
    bxs[0] = bx0; bxs[1] = bx1; bxs[2] = bx2;
    for (let j = 0; j < n; ++j) {
      const bj = j * 3;
      const cs0 = v.s[bj], cs1 = v.s[bj + 1], cs2 = v.s[bj + 2];
      // exterior_safe: no circle through 2+2 external stones
      if (bs0 === cs0 || bs0 === cs1 || bs0 === cs2 ||
          bs1 === cs0 || bs1 === cs1 || bs1 === cs2 ||
          bs2 === cs0 || bs2 === cs1 || bs2 === cs2) continue;
      const cx0 = v.x[bj], cx1 = v.x[bj + 1], cx2 = v.x[bj + 2];
      cxs[0] = cx0; cxs[1] = cx1; cxs[2] = cx2;

      for (let k = 0; k < 2; ++k) {
        if (found[k] || (k !== 0 && j < i)) continue;
        // base: 2+1 external circles, union of 6 z slots
        const za = z[k !== 0 ? 2 : 0], zb = z[k !== 0 ? 2 : 1];
        let b0 = 0, b1 = 0, b2 = 0;
        let o = (i * m + cx0) * 3; b0 |= za[o]; b1 |= za[o + 1]; b2 |= za[o + 2];
        o = (i * m + cx1) * 3;     b0 |= za[o]; b1 |= za[o + 1]; b2 |= za[o + 2];
        o = (i * m + cx2) * 3;     b0 |= za[o]; b1 |= za[o + 1]; b2 |= za[o + 2];
        o = (j * m + bx0) * 3;     b0 |= zb[o]; b1 |= zb[o + 1]; b2 |= zb[o + 2];
        o = (j * m + bx1) * 3;     b0 |= zb[o]; b1 |= zb[o + 1]; b2 |= zb[o + 2];
        o = (j * m + bx2) * 3;     b0 |= zb[o]; b1 |= zb[o + 1]; b2 |= zb[o + 2];
        // two closed neighborhoods <= 32 vertices
        if (pc3(b0, b1, b2) < m - 32) continue;
        // support of the 9 cross slabs
        const G = g[k];
        const adj = G.adj, sup = G.sup;
        let s0 = 0, s1 = 0, s2 = 0;
        for (let u = 0; u < 3; ++u)
          for (let w = 0; w < 3; ++w) {
            const so = (bxs[u] * m + cxs[w]) * 3;
            s0 |= sup[so]; s1 |= sup[so + 1]; s2 |= sup[so + 2];
          }
        // with no 2+2-pair circles, each target vertex has <= 6 neighbors
        if (pc3(b0 | s0, b1 | s1, b2 | s2) < m - 14) continue;

        ++candidates[k];

        // ---- cover(base, b=v[i], c=v[j], g[k], m, require_safe=false) ----
        need[0] = fullW[0] & ~b0;
        need[1] = fullW[1] & ~b1;
        need[2] = fullW[2] & ~b2;
        const needPC = pc3(need[0], need[1], need[2]);
        // merged adjacency over the 9 slabs (depends on (i,j,k) only)
        gm.fill(0);
        for (let u = 0; u < 3; ++u)
          for (let w = 0; w < 3; ++w) {
            const so2 = (bxs[u] * m + cxs[w]) * m81 * 3;
            for (let a = 0; a < m; ++a) {
              const q = so2 + a * 3, t = a * 3;
              gm[t] |= adj[q]; gm[t + 1] |= adj[q + 1]; gm[t + 2] |= adj[q + 2];
            }
          }
        // closed neighborhoods and the top-2 gain prune
        let top0 = 0, top1 = 0;
        for (let a = 0; a < m; ++a) {
          let n0 = 0, n1 = 0, n2 = 0;
          if (a < 32) n0 = 1 << a; else if (a < 64) n1 = 1 << (a - 32); else n2 = 1 << (a - 64);
          let x = bs0 - a; if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          x = bs1 - a;     if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          x = bs2 - a;     if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          x = cs0 - a;     if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          x = cs1 - a;     if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          x = cs2 - a;     if (x >= 0 && x < m && x !== a) { if (x < 32) n0 |= 1 << x; else if (x < 64) n1 |= 1 << (x - 32); else n2 |= 1 << (x - 64); }
          const t = a * 3;
          n0 |= gm[t]; n1 |= gm[t + 1]; n2 |= gm[t + 2];
          nbuf[t] = n0; nbuf[t + 1] = n1; nbuf[t + 2] = n2;
          const gain = pc3(n0 & need[0], n1 & need[1], n2 & need[2]);
          if (gain > top0) { top1 = top0; top0 = gain; }
          else if (gain > top1) top1 = gain;
        }
        if (top0 + top1 < needPC) continue;
        // exact 2-neighborhood cover test
        let A = -1, D = -1;
        outer:
        for (let a = 0; a < m; ++a) {
          const wa = a * 3;
          for (let d = a + 1; d < m; ++d) {
            const wd = d * 3;
            const u0 = nbuf[wa] | nbuf[wd];
            const u1 = nbuf[wa + 1] | nbuf[wd + 1];
            const u2 = nbuf[wa + 2] | nbuf[wd + 2];
            if ((need[0] & ~u0) === 0 && (need[1] & ~u1) === 0 && (need[2] & ~u2) === 0) {
              A = a; D = d; break outer;
            }
          }
        }
        if (A >= 0) {
          found[k] = true;
          wA[k][0] = A; wA[k][1] = D;
          wBx[k][0] = bx0; wBx[k][1] = bx1; wBx[k][2] = bx2;
          wCx[k][0] = cx0; wCx[k][1] = cx1; wCx[k][2] = cx2;
        }
      }
    }
    if (found[0] && found[1]) break;
  }

  const seconds = Number(process.hrtime.bigint() - t0) / 1e9;
  return {
    m,
    three_sets: n,
    cover_exists: [found[0] ? 1 : 0, found[1] ? 1 : 0],
    candidates,
    witnesses: [0, 1].map(k => found[k]
      ? { A: [wA[k][0], wA[k][1]], B: [...wBx[k]], C: [...wCx[k]] }
      : null),
    seconds,
  };
}

function main() {
  const low = process.argv.length > 2 ? parseInt(process.argv[2], 10) : 12;
  const high = process.argv.length > 3 ? parseInt(process.argv[3], 10) : low;
  if (low < 9 || high > 68 || low > high) { process.exitCode = 2; return; }
  for (let m = low; m <= high; ++m) {
    const r = runWidth(m);
    process.stdout.write(JSON.stringify(r) + '\n');
    if (typeof process.send !== 'undefined') break; // unused guard
  }
}
main();
