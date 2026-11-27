// jsreplay.js -- Node.js replica of the STANDALONE EXACT REPLAY code path of
// cpp/solvers/kyouen_dfpn_root.cpp at yuubinnkyoku/kyouen-researches commit
// 154f3b7a67 (file SHA-256
// 9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e), the
// source that generated the published two-target-design replay raws.
//
// Reproduced configuration: --n=11 --memo=22 --only=5 --exact-order=count
// --exact-replay=<csv> --exact-replay-budget=<n>, i.e. per replay row:
//   fresh solver (empty 2^22-entry PnTT, PROBE=32), set_root never called
//   (the TT's root guard stays all-ones and cannot match any board mask),
//   deadline 0, exact handoff publish=ALL, exact order = count-asc,
//   no exact-local memo access, no residual options, no shared TT/layer.
//
// Bitboards are 4 unsigned 32-bit lanes [b0,b1,b2,b3] for bits 0..120
// (C++ Bits{lo,hi}: lo = b1*2^32+b0, hi = b3*2^32+b2 with b3 <= (1<<25)-1).
// TT hashing uses limb-exact uint64 arithmetic implementing the C++ mix64.
// Child pn/dn are written but never read on this path (ordering and DFS loop
// read only st/count/key), so the replica omits them; the TT's pn/dn/vis
// fields are likewise never read back during a replay.
//
// Usage: node jsreplay.js --exact-replay=in.csv --exact-replay-budget=2000000
// Output rows match the C++ driver exactly except wall_s.
'use strict';

// ---------------- Bits helpers ----------------
function anyB(b) { return (b[0] | b[1] | b[2] | b[3]) !== 0; }
function eqB(a, b) { return a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3]; }
function lessB(a, b) { // C++ operator< on Bits: (hi, lo) lexicographic
  if (a[3] !== b[3]) return a[3] < b[3];
  if (a[2] !== b[2]) return a[2] < b[2];
  if (a[1] !== b[1]) return a[1] < b[1];
  return a[0] < b[0];
}
function setbitB(b, p) { b[p >> 5] |= (1 << (p & 31)) >>> 0; }
function hasBit(b, p) { return ((b[p >> 5] >>> (p & 31)) & 1) === 1; }
function ctz32(x) { return x === 0 ? 32 : (31 - Math.clz32((x & -x) | 0)); }
function popcountB(b) {
  let n = 0;
  for (let i = 0; i < 4; i++) {
    let x = b[i] >>> 0;
    x = x - ((x >>> 1) & 0x55555555);
    x = (x & 0x33333333) + ((x >>> 2) & 0x33333333);
    x = (x + (x >>> 4)) & 0x0f0f0f0f;
    n += (x * 0x01010101) >>> 24;
  }
  return n;
}
function takeLsbB(b) {
  if ((b[0] | 0) !== 0) { const p = ctz32(b[0] >>> 0); b[0] = (b[0] - 1) & b[0]; return p; }
  if ((b[1] | 0) !== 0) { const p = ctz32(b[1] >>> 0) + 32; b[1] = (b[1] - 1) & b[1]; return p; }
  if ((b[2] | 0) !== 0) { const p = ctz32(b[2] >>> 0) + 64; b[2] = (b[2] - 1) & b[2]; return p; }
  if ((b[3] | 0) !== 0) { const p = ctz32(b[3] >>> 0) + 96; b[3] = (b[3] - 1) & b[3]; return p; }
  throw new Error('take_lsb on empty Bits');
}

// ---------------- exact uint64 math (scalars only) ----------------
function mulK(ah, al, bh, bl) { // (ah*2^32+al)*(bh*2^32+bl) mod 2^64
  const alh = al >>> 16, all_ = al & 0xffff;
  const blh = bl >>> 16, bll = bl & 0xffff;
  const t = all_ * bll;                 // < 2^32
  const u = alh * bll + all_ * blh;     // < 2^33
  const v = alh * blh;                  // < 2^32
  const sumLow = t + ((u & 0xffff) * 65536);
  const low = sumLow % 4294967296;
  const carry = sumLow >= 4294967296 ? 1 : 0;
  const highFromXL = v + Math.floor(u / 65536) + carry;
  const cross = ((Math.imul(ah, bl) + Math.imul(al, bh)) | 0);
  const crossU = (cross + 4294967296) % 4294967296;
  const high = (highFromXL + crossU) % 4294967296;
  return [high >>> 0, low >>> 0];
}
function mixStep(xh, xl) { // mix64 on a scalar pair; returns [hi, lo]
  // x ^= x>>30   (64-bit: lo=(lo>>>30)|(hi<<2), hi=hi>>>30)
  let s = ((xl >>> 30) | (xh << 2)) >>> 0;
  xl = (xl ^ s) >>> 0;
  xh = (xh ^ (xh >>> 30)) >>> 0;
  // x *= 0xbf58476d1ce4e5b9
  let m = mulK(xh, xl, 0xbf58476d, 0x1ce4e5b9);
  xh = m[0]; xl = m[1];
  // x ^= x>>27
  // x ^= x>>27   (lo=(lo>>>27)|(hi<<5), hi=hi>>>27)
  s = ((xl >>> 27) | (xh << 5)) >>> 0;
  xl = (xl ^ s) >>> 0;
  xh = (xh ^ (xh >>> 27)) >>> 0;
  // x *= 0x94d049bb133111eb
  m = mulK(xh, xl, 0x94d049bb, 0x133111eb);
  xh = m[0]; xl = m[1];
  // x ^= x>>31
  // x ^= x>>31   (lo=(lo>>>31)|(hi<<1), hi=hi>>>31)
  s = ((xl >>> 31) | (xh << 1)) >>> 0;
  xl = (xl ^ s) >>> 0;
  xh = (xh ^ (xh >>> 31)) >>> 0;
  return [xh >>> 0, xl >>> 0];
}
function slotOf(klo0, klo1, khi2, khi3, mask) {
  const prod = mulK(khi3 >>> 0, khi2 >>> 0, 0x9e3779b9, 0x7f4a7c15);
  const xh = (klo1 ^ prod[0]) >>> 0;
  const xl = (klo0 ^ prod[1]) >>> 0;
  const mm = mixStep(xh, xl);
  return mm[1] & mask; // the low 32-bit word carries any mask < 2^32
}

// ---------------- geometry ----------------
const N = 11, V = 121;
const HI_L3 = (1 << 25) - 1; // bits 96..120 live in lane3 bits 0..24

function det3(a00, a01, a02, a10, a11, a12, a20, a21, a22) {
  return a00 * (a11 * a22 - a12 * a21) - a01 * (a10 * a22 - a12 * a20) + a02 * (a10 * a21 - a11 * a20);
}
// forbidden(a,b,c,d): the 4x4 determinant of rows [x^2+y^2, x, y, 1] is zero
// (four concyclic or collinear points). Restricted to [-2^31..2^31-1]:
const FORBIDX = new Int32Array(V * V * V * V >= 0 ? 1 : 1); void FORBIDX;
function forbidden(a, b, c, d) {
  const x0 = a % N, y0 = (a / N) | 0, x1 = b % N, y1 = (b / N) | 0;
  const x2 = c % N, y2 = (c / N) | 0, x3 = d % N, y3 = (d / N) | 0;
  // m0 = [sq, x, y, 1] and the 3x3 minors of rows 1..3 (cofactor expansion
  // along row 0). Row0-pivot matching the C++ expansion-by-column form:
  // det = sum_{col} (-1)^col m0[col] * det(minor removing row0,col)
  // (sign: col%2==0 -> +). The C++ code removes row 0 and column `col`.
  const s0 = x0 * x0 + y0 * y0, s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
  // rows r1..r3: [sq_r, x_r, y_r, 1]
  // col 0: minor of cols [x, y, 1]; col 1: [sq, y, 1]; col 2: [sq, x, 1].. careful
  // expand: det = s0*Min(0) - x0*Min(1) + y0*Min(2) - 1*Min(3)
  // Min(c) = determinant over the 3 rows r1..r3 of the 3 columns of
  // [sq, x, y, 1] excluding column c.
  const M0 = det3(x1, y1, 1, x2, y2, 1, x3, y3, 1);
  const M1 = det3(s1, y1, 1, s2, y2, 1, s3, y3, 1);
  const M2 = det3(s1, x1, 1, s2, x2, 1, s3, x3, 1);
  const M3 = det3(s1, x1, y1, s2, x2, y2, s3, x3, y3);
  const det = s0 * M0 - x0 * M1 + y0 * M2 - M3;
  void s2; void s3;
  return det === 0;
}
function idx3(a, b, c) { return (a * V + b) * V + c; }

function buildCompletionTable() {
  const wob = new Uint32Array(4 * V * V * V);
  let count = 0;
  for (let a = 0; a < V; a++)
    for (let b = a + 1; b < V; b++)
      for (let c = b + 1; c < V; c++)
        for (let d = c + 1; d < V; d++) {
          if (!forbidden(a, b, c, d)) continue;
          count++;
          const q = [a, b, c, d];
          for (let omit = 0; omit < 4; omit++) {
            const t = [];
            for (let j = 0; j < 4; j++) { if (j !== omit) t.push(q[j]); }
            const base = 4 * idx3(t[0], t[1], t[2]); // t ascending
            wob[base + (q[omit] >> 5)] |= (1 << (q[omit] & 31)) >>> 0;
          }
        }
  return { wob, count };
}

/*
 NH note: the tbit builder places the D4 image of point p under transform k
 at flat[(k*V+p)*4 + (tp>>5)] with bit (tp & 31), where
   nx = {x, N-1-x, x, N-1-x, y, N-1-y, y, N-1-y}
   ny = {y, y, N-1-y, N-1-y, x, x, N-1-x, N-1-x}
 matching the C++ build_maps.
*/
function buildTbit() {
  const flat = new Uint32Array(8 * V * 4);
  for (let p = 0; p < V; p++) {
    const x = p % N, y = (p / N) | 0;
    const nx = [x, N - 1 - x, x, N - 1 - x, y, N - 1 - y, y, N - 1 - y];
    const ny = [y, y, N - 1 - y, N - 1 - y, x, x, N - 1 - x, N - 1 - x];
    for (let k = 0; k < 8; k++) {
      const tp = ny[k] * N + nx[k];
      flat[(k * V + p) * 4 + (tp >> 5)] |= (1 << (tp & 31)) >>> 0;
    }
  }
  return flat;
}

// ---------------- PnTT ----------------
const ST_FREE = 0, ST_OPEN = 1, ST_WIN = 2, ST_LOSS = 3;
class PnTT {
  constructor(power) {
    this.n = 1 << power;
    this.mask = this.n - 1;
    this.lo0 = new Uint32Array(this.n); this.lo1 = new Uint32Array(this.n);
    this.hi0 = new Uint32Array(this.n); this.hi1 = new Uint32Array(this.n);
    this.st = new Uint8Array(this.n);
    // set_root never called on this path: root guard stays all-ones.
    this.r0 = 0xffffffff; this.r1 = 0xffffffff; this.r2 = 0xffffffff; this.r3 = 0xffffffff;
  }
  slot(k0, k1, k2, k3) { return slotOf(k0, k1, k2, k3, this.mask); }
  match(i, k0, k1, k2, k3) {
    return this.lo0[i] === k0 && this.lo1[i] === k1 && this.hi0[i] === k2 && this.hi1[i] === k3;
  }
  isRoot(i) { return this.r0 === this.lo0[i] && this.r1 === this.lo1[i] && this.r2 === this.hi0[i] && this.r3 === this.hi1[i]; }
  put(i, k0, k1, k2, k3) {
    this.lo0[i] = k0; this.lo1[i] = k1; this.hi0[i] = k2; this.hi1[i] = k3;
    this.st[i] = ST_OPEN;
  }
  find(k0, k1, k2, k3) {
    let i = this.slot(k0, k1, k2, k3);
    for (let j = 0; j < 32; j++) {
      if (this.st[i] === ST_FREE) return -1;
      if (this.match(i, k0, k1, k2, k3)) return i;
      i = (i + 1) & this.mask;
    }
    return -1;
  }
  acquire(k0, k1, k2, k3) {
    const h = this.slot(k0, k1, k2, k3);
    let i = h, firstOpen = -1;
    for (let j = 0; j < 32; j++) {
      if (this.st[i] === ST_FREE) { this.put(i, k0, k1, k2, k3); return i; }
      if (this.match(i, k0, k1, k2, k3)) return i;
      if (firstOpen < 0 && this.st[i] === ST_OPEN && !this.isRoot(i)) firstOpen = i;
      i = (i + 1) & this.mask;
    }
    if (firstOpen >= 0) { this.put(firstOpen, k0, k1, k2, k3); return firstOpen; }
    if (this.isRoot(h)) {
      for (let j = 0; j < 32; j++) {
        const ii = (h + j) & this.mask;
        if (!this.isRoot(ii)) { this.put(ii, k0, k1, k2, k3); return ii; }
      }
      return -1;
    }
    this.put(h, k0, k1, k2, k3);
    return h;
  }
}

// ---------------- solver ----------------
class GenBuffer {
  constructor() {
    this.n = 0;
    this.ts = []; this.legal = []; this.key = [];
    this.count = new Int32Array(V);
    this.st = new Uint8Array(V);
    for (let i = 0; i < V; i++) {
      this.ts.push(new Uint32Array(32));
      this.legal.push([0, 0, 0, 0]);
      this.key.push([0, 0, 0, 0]);
    }
  }
}
class Solver {
  constructor(memoPower, wob) {
    this.wob = wob;
    this.tbit = buildTbit();
    this.tt = new PnTT(memoPower);
    this.exactNodes = 0;
    this.genPool = []; this.keyRow = []; this.pris = []; this.orderArr = [];
    for (let s = 0; s <= V; s++) {
      this.genPool.push(new GenBuffer());
      this.keyRow.push([0, 0, 0, 0]);
      this.pris.push(new Uint8Array(V));
      const ord = new Array(V);
      for (let i = 0; i < V; i++) ord[i] = i;
      this.orderArr.push(ord);
    }
    // scratch used only inside genInto (no recursion there):
    this.sMoves = [0, 0, 0, 0];
    this.sVerts = new Int32Array(V);
    this.sBans = [0, 0, 0, 0];
    this.sKb = [0, 0, 0, 0];
    this.sOcc = [0, 0, 0, 0];
  }
  canonicalRow(state, out) {
    let best = 0;
    for (let k = 1; k < 8; k++) {
      const A = k * 4, B = best * 4;
      if (state[A + 3] !== state[B + 3]) { if (state[A + 3] < state[B + 3]) best = k; continue; }
      if (state[A + 2] !== state[B + 2]) { if (state[A + 2] < state[B + 2]) best = k; continue; }
      if (state[A + 1] !== state[B + 1]) { if (state[A + 1] < state[B + 1]) best = k; continue; }
      if (state[A] !== state[B]) { if (state[A] < state[B]) best = k; }
    }
    const b = best * 4;
    out[0] = state[b]; out[1] = state[b + 1]; out[2] = state[b + 2]; out[3] = state[b + 3];
  }
  legalFor(occupied) {
    const s = [occupied[0], occupied[1], occupied[2], occupied[3]];
    const verts = [];
    while (anyB(s)) verts.push(takeLsbB(s));
    const danger = [0, 0, 0, 0];
    const k = verts.length;
    const wob = this.wob;
    for (let i = 0; i < k; i++)
      for (let j = i + 1; j < k; j++)
        for (let l = j + 1; l < k; l++) {
          const base = 4 * idx3(verts[i], verts[j], verts[l]);
          danger[0] |= wob[base]; danger[1] |= wob[base + 1];
          danger[2] |= wob[base + 2]; danger[3] |= wob[base + 3];
        }
    const legal = [4294967295, 4294967295, 4294967295, HI_L3];
    for (let i = 0; i < 4; i++) legal[i] = (legal[i] & ~((occupied[i] | danger[i]) >>> 0)) >>> 0;
    return { legal, count: popcountB(legal) };
  }
  genInto(state, stones, legal, gen) {
    const sMoves = this.sMoves;
    sMoves[0] = legal[0] >>> 0; sMoves[1] = legal[1] >>> 0; sMoves[2] = legal[2] >>> 0;
    sMoves[3] = (legal[3] & HI_L3) >>> 0;
    // occupied verts of state.t[0] (shared by added_bans)
    const occ = this.sOcc;
    occ[0] = state[0]; occ[1] = state[1]; occ[2] = state[2]; occ[3] = state[3];
    const verts = this.sVerts;
    let k = 0;
    while (anyB(occ)) verts[k++] = takeLsbB(occ);
    const wob = this.wob, bans = this.sBans, kb = this.sKb, tbit = this.tbit;
    gen.n = 0;
    while ((sMoves[0] | sMoves[1] | sMoves[2] | sMoves[3]) !== 0) {
      const v = takeLsbB(sMoves);
      if (v < 0 || v >= V) throw new Error('gen_into: move index out of range');
      bans[0] = 0; bans[1] = 0; bans[2] = 0; bans[3] = 0;
      for (let i = 0; i < k; i++)
        for (let j = i + 1; j < k; j++) {
          let A = verts[i], B = verts[j], C = v;
          if (A > B) { const t = A; A = B; B = t; }
          if (B > C) { const t = B; B = C; C = t; }
          if (A > B) { const t = A; A = B; B = t; }
          const base = 4 * idx3(A, B, C);
          bans[0] |= wob[base]; bans[1] |= wob[base + 1];
          bans[2] |= wob[base + 2]; bans[3] |= wob[base + 3];
        }
      const lane = v >> 5, bv = (1 << (v & 31)) >>> 0;
      const nl = gen.legal[gen.n];
      nl[0] = (legal[0] & ~bans[0]) >>> 0;
      nl[1] = (legal[1] & ~bans[1]) >>> 0;
      nl[2] = (legal[2] & ~bans[2]) >>> 0;
      nl[3] = ((legal[3] & ~bans[3])>>>0) & HI_L3;
      nl[lane] = (nl[lane] & ~bv) >>> 0;
      nl[3] = (nl[3] & HI_L3) >>> 0;
      const ts = gen.ts[gen.n];
      for (let kk = 0; kk < 8; kk++) {
        const b = kk * 4, t = (kk * V + v) * 4;
        ts[b] = (state[b] | tbit[t]) >>> 0;
        ts[b + 1] = (state[b + 1] | tbit[t + 1]) >>> 0;
        ts[b + 2] = (state[b + 2] | tbit[t + 2]) >>> 0;
        ts[b + 3] = (state[b + 3] | tbit[t + 3]) >>> 0;
      }
      this.canonicalRow(ts, kb);
      const nk = gen.key[gen.n];
      nk[0] = kb[0]; nk[1] = kb[1]; nk[2] = kb[2]; nk[3] = kb[3];
      let dup = false;
      for (let i = 0; i < gen.n; i++) { if (eqB(gen.key[i], nk)) { dup = true; break; } }
      if (dup) continue;
      gen.count[gen.n] = popcountB(nl);
      const cs = stones + 1;
      const s = this.tt.find(nk[0], nk[1], nk[2], nk[3]);
      if (s >= 0) gen.st[gen.n] = this.tt.st[s];
      else if ((nl[0] | nl[1] | nl[2] | nl[3]) === 0) gen.st[gen.n] = (cs % 2 === 0) ? ST_LOSS : ST_WIN;
      else gen.st[gen.n] = ST_OPEN;
      gen.n++;
      if (gen.n >= V) throw new Error('gen_into: child index out of range');
    }
  }
  exactStore(kb, resultWin) { // resultWin: true=WIN, false=LOSS
    const k0 = kb[0], k1 = kb[1], k2 = kb[2], k3 = kb[3];
    const i = this.tt.find(k0, k1, k2, k3);
    if (i >= 0 && this.tt.st[i] >= ST_WIN) {
      const oldWin = this.tt.st[i] === ST_WIN;
      if (oldWin !== resultWin) throw new Error('exact solver contradicts solved TT entry');
      return;
    }
    let slot = i;
    if (slot < 0) {
      slot = this.tt.acquire(k0, k1, k2, k3);
      if (slot < 0) throw new Error('TT full at exact_store');
    }
    this.tt.st[slot] = resultWin ? ST_WIN : ST_LOSS;
  }
  exactProp(state, stones, legal, budget) {
    // returns 0 UNKNOWN / 1 WIN / 2 LOSS
    const kb = this.keyRow[stones];
    this.canonicalRow(state, kb);
    const s = this.tt.find(kb[0], kb[1], kb[2], kb[3]);
    if (s >= 0 && this.tt.st[s] >= ST_WIN) return this.tt.st[s] === ST_WIN ? 1 : 2;
    if (budget.v === 0) return 0;
    budget.v--;
    this.exactNodes++;
    if ((legal[0] | legal[1] | legal[2] | legal[3]) === 0) {
      const r = (stones % 2 === 0) ? 2 : 1;
      this.exactStore(kb, r === 1);
      return r;
    }
    const gen = this.genPool[stones];
    this.genInto(state, stones, legal, gen);
    const n = gen.n;
    const isor = (stones % 2) === 0;
    const pris = this.pris[stones];
    const st = gen.st, cnt = gen.count, key = gen.key;
    if (isor) {
      for (let i = 0; i < n; i++) {
        const x = st[i];
        pris[i] = (x === ST_WIN) ? 0 : ((x === ST_OPEN) ? 1 : 2);
      }
    } else {
      for (let i = 0; i < n; i++) {
        const x = st[i];
        pris[i] = (x === ST_LOSS) ? 0 : ((x === ST_OPEN) ? 1 : 2);
      }
    }
    const order = this.orderArr[stones];
    for (let i = 0; i < n; i++) order[i] = i;
    order.length = n;
    order.sort(function (ia, ib) {
      const pa = pris[ia], pb = pris[ib];
      if (pa !== pb) return pa - pb;
      const ca = cnt[ia], cb = cnt[ib];
      if (ca !== cb) return ca - cb; // count-asc (exact-order=count)
      return lessB(key[ia], key[ib]) ? -1 : 1;
    });
    let unknown = false;
    for (let oi = 0; oi < n; oi++) {
      const i = order[oi];
      let cr;
      const cst = st[i];
      if (cst === ST_WIN) cr = 1;
      else if (cst === ST_LOSS) cr = 2;
      else cr = this.exactProp(gen.ts[i], stones + 1, gen.legal[i], budget);
      if (isor && cr === 1) { this.exactStore(kb, true); return 1; }
      if (!isor && cr === 2) { this.exactStore(kb, false); return 2; }
      if (cr === 0) unknown = true;
    }
    if (unknown) return 0;
    const r = isor ? 2 : 1;
    this.exactStore(kb, r === 1);
    return r;
  }
  exactReplay(lo0, lo1, hi0, hi1, stones, budget) {
    const occ = [lo0 >>> 0, lo1 >>> 0, hi0 >>> 0, hi1 >>> 0];
    const s = [occ[0], occ[1], occ[2], occ[3]];
    const verts = [];
    let k = 0;
    while (anyB(s)) { if (k >= V) throw new Error('bad occupancy'); verts.push(takeLsbB(s)); k++; }
    if (k !== stones) throw new Error('stones mismatch');
    const seen = [0, 0, 0, 0];
    for (const p of verts) { if (p >= V || hasBit(seen, p)) throw new Error('bad root point'); setbitB(seen, p); }
    for (let i = 0; i < k; i++)
      for (let j = i + 1; j < k; j++)
        for (let l = j + 1; l < k; l++)
          for (let m = l + 1; m < k; m++)
            if (forbidden(verts[i], verts[j], verts[l], verts[m])) throw new Error('unsafe root');
    let state = new Uint32Array(32);
    const tmp = new Uint32Array(32);
    for (let i = 0; i < k; i++) {
      const t = (0 * V + verts[i]) * 4;
      for (let kk = 0; kk < 8; kk++) {
        const b = kk * 4, tb = (kk * V + verts[i]) * 4;
        tmp[b] = state[b]; tmp[b + 1] = state[b + 1]; tmp[b + 2] = state[b + 2]; tmp[b + 3] = state[b + 3];
        void t;
        state[b] = (state[b] | this.tbit[tb]) >>> 0;
        state[b + 1] = (state[b + 1] | this.tbit[tb + 1]) >>> 0;
        state[b + 2] = (state[b + 2] | this.tbit[tb + 2]) >>> 0;
        state[b + 3] = (state[b + 3] | this.tbit[tb + 3]) >>> 0;
      }
    }
    const { legal, count } = this.legalFor(occ);
    this.exactNodes = 0;
    const b = { v: budget };
    const r = this.exactProp(state, stones, legal, b);
    return { res: r, nodes: this.exactNodes, legalCount: count };
  }
}

module.exports = { Solver, buildCompletionTable, V, N, forbidden, slotOf, mixStep, mulK, popcountB, HI_L3, lessB, eqB, idx3 };

// ---------------- driver ----------------
if (require.main === module) {
  const fs = require('fs');
  let path = '', budget = 1000000, only = '', memo = 22;
  for (let i = 2; i < process.argv.length; i++) {
    const a = process.argv[i];
    if (a.startsWith('--exact-replay=')) path = a.slice(15);
    else if (a.startsWith('--exact-replay-budget=')) budget = parseInt(a.slice(22), 10);
    else if (a.startsWith('--only=')) only = a.slice(7);
    else if (a.startsWith('--memo=')) memo = parseInt(a.slice(7), 10);
    else if (a.startsWith('--n=') || a.startsWith('--exact-order=')) { /* fixed values */ }
    else { console.error('unknown arg: ' + a); process.exit(2); }
  }
  if (!path) { console.error('usage: node jsreplay.js --exact-replay=in.csv --exact-replay-budget=N [--only=v,..] [--memo=22]'); process.exit(1); }
  const onlySet = only === '' ? null : new Set(only.split(',').filter(w => w !== '').map(w => parseInt(w, 10)));
  console.log('# exact replay: order=0 (0=count-asc 1=count-desc 2=key-asc 3=s5-count-desc 4=s5-target92) share_tt=0');
  console.log('# exact replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi');
  const t0wall = Date.now();
  const { wob, count: quads } = buildCompletionTable();
  console.error('# forbidden quadruples: ' + quads);
  let id = 0;
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  for (const line of lines) {
    if (line === '' || line[0] === '#') continue;
    const f = line.split(',');
    if (f.length < 11) continue;
    const stones = parseInt(f[2], 10);
    if (onlySet !== null && !onlySet.has(stones)) continue;
    const loS = f[3], hiS = f[4], legalS = f[5];
    const loB = BigInt(loS), hiB = BigInt(hiS);
    const lo0 = Number(loB & 0xffffffffn), lo1 = Number((loB >> 32n) & 0xffffffffn);
    const hi0 = Number(hiB & 0xffffffffn), hi1 = Number((hiB >> 32n) & 0xffffffffn);
    const rowStart = process.hrtime.bigint();
    const solver = new Solver(Math.min(memo, 22), wob);
    let res = -1, nodes = 0;
    try {
      const r = solver.exactReplay(lo0, lo1, hi0, hi1, stones, budget);
      res = r.res; nodes = r.nodes;
      if (r.legalCount !== parseInt(legalS, 10)) throw new Error('legal count mismatch: derived ' + r.legalCount + ' != input ' + legalS);
    } catch (e) {
      console.log('replay_error,' + id + ',' + stones + ',0,"' + e.message + '"');
      id++;
      continue;
    }
    const rowEnd = process.hrtime.bigint();
    const wallS = Math.trunc(Number(rowEnd - rowStart) / 1e9);
    console.log('replay,' + id + ',' + stones + ',' + legalS + ',' + (stones % 2 === 0 ? 1 : 0) + ',' + budget + ',' + res + ',' + nodes + ',' + wallS + ',' + loS + ',' + hiS);
    id++;
  }
  const wallAll = Math.trunc((Date.now() - t0wall) / 1000);
  console.log('# replay_done rows=' + id + ' wall_s=' + wallAll);
}
