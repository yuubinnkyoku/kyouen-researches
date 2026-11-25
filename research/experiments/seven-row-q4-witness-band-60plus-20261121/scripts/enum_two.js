// Complete 2-for-2 replacement enumeration for 7-row q=4 deficient-maximal witnesses.
// Exact integer geometry (all values < 2^53), no floating point, no search heuristics.
// Fresh-cell mode is calibrated byte-for-byte against pinned audit_two_swap.cpp:
//   counters row_capacity_candidates / safe_candidates / safe_maximal_row_deficient.
// --holes mode additionally allows refilling the two removed stones' positions.
'use strict';
const fs = require('fs');
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
class Board {
  constructor(W) { this.W = W; this.H = 7; this.N = W * 7; this.cache = new Map(); }
  key3(x1, y1, x2, y2, x3, y3) {
    const d2 = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
    let key;
    if (d2 === 0) {
      let dx = x2 - x1, dy = y2 - y1; const g = gcdN(dx, dy); dx /= g; dy /= g;
      if (dy < 0 || (dy === 0 && dx < 0)) { dx = -dx; dy = -dy; }
      key = 'L' + dx + ',' + dy + ',' + (x1 * dy - y1 * dx);
    } else {
      const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
      const dd0 = 2 * d2, ux0 = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2), uy0 = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
      let dd = dd0, uu = ux0, vv = uy0, rr = (x1 * dd0 - ux0) * (x1 * dd0 - ux0) + (y1 * dd0 - uy0) * (y1 * dd0 - uy0);
      const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
      dd /= g; uu /= g; vv /= g; rr /= g * g;
      if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
      key = 'C' + dd + ',' + uu + ',' + vv + ',' + rr;
    }
    let pts = this.cache.get(key);
    if (!pts) {
      pts = [];
      if (d2 === 0) {
        const dx = Number(key.split(',')[0].slice(1));
      }
      if (d2 === 0) {
        const [dxs, dys, c] = key.slice(1).split(',').map(Number);
        if (dys === 0) { for (let x = 0; x < this.W; x++) pts.push(x + this.W * y1); }
        else { for (let y = 0; y < 7; y++) { const num = c + y * dxs; if (num % dys === 0) { const x = num / dys; if (x >= 0 && x < this.W) pts.push(x + this.W * y); } } }
      } else {
        const [dd, uu, vv, rr] = key.slice(1).split(',').map(Number);
        for (let y = 0; y < 7; y++) { const dy = y * dd - vv, rem = rr - dy * dy; if (rem < 0) continue; const r = isqrt(rem); if (r * r !== rem) continue; const dxl = r === 0 ? [0] : [r, -r]; for (const dx of dxl) { const num = dx + uu; if (num % dd !== 0) continue; const x = num / dd; if (x >= 0 && x < this.W) pts.push(x + this.W * y); } }
      }
      this.cache.set(key, pts);
    }
    return pts;
  }
}
function runCase(board, base, opts) {
  const W = board.W, N = board.N, n = 20, holes = !!opts.holes;
  const occ = new Uint8Array(N), baseRows = new Int32Array(8);
  for (const [x, y] of base) { if (x < 0 || x >= W || y < 0 || y >= 7 || occ[x + W * y]) throw new Error('invalid base'); occ[x + W * y] = 1; baseRows[y]++; }
  for (let y = 0; y < 7; y++) if (baseRows[y] > 3) throw new Error('row capacity');
  const bx = new Int32Array(n), by = new Int32Array(n);
  base.forEach((p, i) => { bx[i] = p[0]; by[i] = p[1]; });
  const f4 = (ax, ay, bx2, by2, cx, cy, dx, dy) => {
    const ux = bx2 - ax, uy = by2 - ay;
    const az = bx2 * bx2 + by2 * by2 - ax * ax - ay * ay;
    const vx = cx - ax, vy = cy - ay, vz = cx * cx + cy * cy - ax * ax - ay * ay;
    const wx = dx - ax, wy = dy - ay, wz = dx * dx + dy * dy - ax * ax - ay * ay;
    return ux * (vy * wz - vz * wy) - uy * (vx * wz - vz * wx) + az * (vx * wy - vy * wx) === 0;
  };
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) for (let d = c + 1; d < n; d++) if (f4(bx[a], by[a], bx[b], by[b], bx[c], by[c], bx[d], by[d])) throw new Error('unsafe base');
  const C = N;
  const badT = new Array(C); for (let i = 0; i < C; i++) badT[i] = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const pts = board.key3(bx[i], by[i], bx[j], by[j], bx[k], by[k]);
    const pk = i * 400 + j * 20 + k;
    for (const u of pts) badT[u].push(pk);
  }
  const badP = new Map(), coverBy = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    for (let u0 = 0; u0 < C; u0++) {
      if (occ[u0]) { if (!holes) continue; }
      const px = u0 % W, py = (u0 / W) | 0;
      const pts = board.key3(px, py, bx[i], by[i], bx[j], by[j]);
      for (const u of pts) {
        if (u === u0) continue;
        if (!holes && occ[u]) continue;
        const kk = u0 < u ? u0 * 1024 + u : u * 1024 + u0;
        let arr = badP.get(kk); if (!arr) { arr = []; badP.set(kk, arr); } arr.push(i * 20 + j);
        const ck = u0 * 1024 + u; let ca = coverBy.get(ck); if (!ca) { ca = []; coverBy.set(ck, ca); } ca.push(i * 20 + j);
      }
    }
  }
  const single = (u, ri, rj) => { const L = badT[u]; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 400) | 0, rest = pk % 400, j = (rest / 20) | 0, k = rest % 20; if (i !== ri && i !== rj && j !== ri && j !== rj && k !== ri && k !== rj) return false; } return true; };
  const pairOK = (u, v, ri, rj) => { const kk = u < v ? u * 1024 + v : v * 1024 + u; const L = badP.get(kk); if (!L) return true; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 20) | 0, j = pk % 20; if (i !== ri && i !== rj && j !== ri && j !== rj) return false; } return true; };
  let rowCapacity = 0, safe = 0, maximal = 0, shapeErr = 0;
  const witnesses = [];
  const maxWit = opts.maxWitnesses || 64;
  const ord = []; for (let x = W - 1; x >= 0; x--) ord.push(x);
  const covU = (p, u, ri, rj) => { const L = coverBy.get(p * 1024 + u); if (!L) return false; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 20) | 0, j = pk % 20; if (i !== ri && i !== rj && j !== ri && j !== rj) return true; } return false; };
  for (let ri = 0; ri < n; ri++) for (let rj = ri + 1; rj < n; rj++) {
    const rc2 = new Int32Array(8); for (let y = 0; y < 8; y++) rc2[y] = baseRows[y]; rc2[by[ri]]--; rc2[by[rj]]--;
    const holeU = [bx[ri] + W * by[ri], bx[rj] + W * by[rj]];
    const avail = [];
    for (let u = 0; u < C; u++) {
      if (!holes && occ[u]) continue;
      if (occ[u] && !(u === holeU[0] || u === holeU[1])) continue;
      if (rc2[(u / W) | 0] < 3) avail.push(u);
    }
    const okS = new Uint8Array(avail.length);
    for (let s = 0; s < avail.length; s++) okS[s] = single(avail[s], ri, rj) ? 1 : 0;
    const rem = []; for (let k = 0; k < n; k++) if (k !== ri && k !== rj) rem.push(k);
    const remBlocked = new Uint8Array(N);
    for (let a = 0; a < 18; a++) for (let b = a + 1; b < 18; b++) for (let c = b + 1; c < 18; c++) {
      const pts = board.key3(bx[rem[a]], by[rem[a]], bx[rem[b]], by[rem[b]], bx[rem[c]], by[rem[c]]);
      for (const u of pts) remBlocked[u] = 1;
    }
    for (let aa = 0; aa < avail.length; aa++) {
      const pu = avail[aa], px = pu % W, py = (pu / W) | 0;
      for (let bb = aa + 1; bb < avail.length; bb++) {
        const qu = avail[bb], qx = qu % W, qy = (qu / W) | 0;
        if (py === qy && rc2[py] > 1) continue;
        rowCapacity++;
        if (!okS[aa] || !okS[bb]) continue;
        if (!pairOK(pu, qu, ri, rj)) continue;
        safe++;
        const cand = [];
        for (const k of rem) cand.push([bx[k], by[k]]);
        cand.push([px, py], [qx, qy]);
        const counts = new Int32Array(8); for (const z of cand) counts[z[1]]++;
        let y0 = -1, shape = true;
        for (let y = 0; y < 7; y++) { if (counts[y] > 3) shape = false; if (counts[y] === 2) { if (y0 !== -1) shape = false; y0 = y; } else if (counts[y] !== 3) shape = false; }
        if (!shape || y0 < 0) { shapeErr++; continue; }
        const rowStones = []; for (const z of cand) if (z[1] === y0) rowStones.push(z[0]);
        let bad = false;
        for (const x of ord) {
          const u = x + W * y0;
          if (rowStones.includes(x)) continue;
          if (remBlocked[u]) continue;
          if (covU(pu, u, ri, rj)) continue;
          if (covU(qu, u, ri, rj)) continue;
          let hit = false;
          for (const k of rem) { const pts = board.key3(px, py, qx, qy, bx[k], by[k]); if (pts.includes(u)) { hit = true; break; } }
          if (!hit) { bad = true; break; }
        }
        if (!bad) { maximal++; if (witnesses.length < maxWit) witnesses.push(cand.sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(p => [p[0], p[1]])); }
      }
    }
  }
  return { width: W, row_capacity_candidates: rowCapacity, safe_candidates: safe, shape_errors: shapeErr, safe_maximal_row_deficient: maximal, witnesses };
}
module.exports = { Board, runCase };
