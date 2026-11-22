// third_impl.js -- third-implementation verifier for the sixth-cost k02 lane.
// Non-df-pn AND/OR minimax with completion-memo (canonical D4 keys), independent of the
// pinned jsreplay.js replica. Game: 11x11 kyouen; a move that completes a forbidden
// quadruple (4 stones on a common circle) is illegal; a player with no legal move loses.
// OR node = even stone count (player A, the fixed first player, to move).
// Value semantics match the pinned corpus: result 1 = A wins, 2 = A loses, 0 UNKNOWN.
//
// Fixed points of the design (vs the buggy first version):
//  - kid enumeration scratch (KIDPOOL) is PER DEPTH. The first version kept one global
//    KID_IMG/KID_M/KID_CB/KID_CNT set; a child's recursion overwrote the parent's
//    not-yet-visited sibling entries with grandkid data, corrupting sibling canonical
//    keys and TT keys, flipping every WIN into a LOSS (losses matched by luck/chance
//    of the same corruption). Root cause; fixed here.
//  - legal masks are derived down the search (parent legal & ~bans(new triples with the
//    added stone) & ~stone) instead of recomputing legalOf per node; --verify-legal=1
//    cross-checks the derivation against a from-scratch legalOf at every node.
//  - canonical-key dedup of children and TT-status priority ordering (replica parity).
//  - slab TT: 2^22 entries, 16-slot bounded probing, verdict-correct fail-closed misses.
// Output: third,<row>,<stones>,<legalIn>,<legalDerived>,<result>,<expansion>,<ttHits>,
//         <wallS>,<lo>,<hi>,<reason>,quads=<n>,ttOverwrites=<n>,memoPower=<n>
'use strict';
const N = 11, V = N * N; // 121 points
const L3TOP = (1 << (V - 96)) - 1; // lane 3 masks points 96..120

// ---- forbidden quadruple: 4 distinct points on a common circle (det == 0) ----
function forbiddenQuad(a, b, c, d) {
  const ax = a % N, ay = (a - ax) / N, bx = b % N, by = (b - bx) / N;
  const cx = c % N, cy = (c - cx) / N, dx = d % N, dy = (d - dx) / N;
  const ra = ax * ax + ay * ay, rb = bx * bx + by * by, rc = cx * cx + cy * cy, rd = dx * dx + dy * dy;
  // 4x4 determinant of rows [x*x+y*y, x, y, 1] via cofactor expansion
  const d00 = rb * (cx * dy - cy * dx) - rc * (bx * dy - by * dx) + rd * (bx * cy - by * cx);
  const d01 = ra * (cx * dy - cy * dx) - rc * (ax * dy - ay * dx) + rd * (ax * cy - ay * cx);
  const d02 = ra * (bx * dy - by * dx) - rb * (ax * dy - ay * dx) + rd * (ax * by - ay * bx);
  const d03 = ra * (bx * cy - by * cx) - rb * (ax * cy - ay * cx) + rc * (ax * by - ay * bx);
  return (d00 - d01 + d02 - d03) === 0;
}

// ---- triple completion table: TBL[((a*V+b)*V+c)*4 + lane] = bitmask of points that
// with a<b<c complete a forbidden quadruple ----
const TBL = new Uint32Array(V * V * V * 4);
let quadCount = 0;
for (let a = 0; a < V; a++)
  for (let b = a + 1; b < V; b++)
    for (let c = b + 1; c < V; c++)
      for (let d = c + 1; d < V; d++)
        if (forbiddenQuad(a, b, c, d)) {
          quadCount++;
          const t1 = ((a * V + b) * V + c) * 4;
          TBL[t1 + (d >> 5)] |= (1 << (d & 31)) >>> 0;
          const t2 = ((a * V + b) * V + d) * 4;
          TBL[t2 + (c >> 5)] |= (1 << (c & 31)) >>> 0;
          const t3 = ((a * V + c) * V + d) * 4;
          TBL[t3 + (b >> 5)] |= (1 << (b & 31)) >>> 0;
          const t4 = ((b * V + c) * V + d) * 4;
          TBL[t4 + (a >> 5)] |= (1 << (a & 31)) >>> 0;
        }

// ---- D4 image of point p under the 8 dihedral maps ----
const IMGPT = new Uint8Array(8 * V); // IMGPT[j*V+p] = image point
for (let p = 0; p < V; p++) {
  const x = p % N, y = (p - x) / N;
  const maps = [
    [x, y], [N - 1 - x, y], [x, N - 1 - y], [N - 1 - x, N - 1 - y],
    [y, x], [y, N - 1 - x], [N - 1 - y, x], [N - 1 - y, N - 1 - x],
  ];
  for (let j = 0; j < 8; j++) IMGPT[j * V + p] = maps[j][1] * N + maps[j][0];
}
// TBPT[p*32 + j*4 + lane] = bit-set lane word of image j of point p
const TBPT = new Uint32Array(V * 32);
for (let p = 0; p < V; p++)
  for (let j = 0; j < 8; j++) {
    const q = IMGPT[j * V + p];
    TBPT[p * 32 + j * 4 + (q >> 5)] |= (1 << (q & 31)) >>> 0;
  }

function popW(x) { x = x >>> 0; x = x - ((x >>> 1) & 0x55555555); x = (x & 0x33333333) + ((x >>> 2) & 0x33333333); x = (x + (x >>> 4)) & 0x0f0f0f0f; return (x * 0x01010101) >>> 24; }
function pop4(b, i) { return popW(b[i]) + popW(b[i + 1]) + popW(b[i + 2]) + popW(b[i + 3]); }

// ---- slab TT (fail-closed: bounded-probe deep miss = recompute) ----
class Slab {
  constructor(power) {
    this.n = 1 << power; this.mask = this.n - 1;
    this.k0 = new Uint32Array(this.n); this.k1 = new Uint32Array(this.n);
    this.k2 = new Uint32Array(this.n); this.k3 = new Uint32Array(this.n);
    this.v = new Uint8Array(this.n); this.overwrites = 0;
  }
  h(k0, k1, k2, k3) {
    let h = 0x2545f491 >>> 0;
    const xs = [k0, k1, k2, k3];
    for (let i = 0; i < 4; i++) { h = (Math.imul(h, 0x9e3779b1) ^ (xs[i] >>> 0)) >>> 0; h = (h ^ (h >>> 13)) >>> 0; }
    return h & this.mask;
  }
  find(k0, k1, k2, k3) {
    let i = this.h(k0, k1, k2, k3);
    for (let j = 0; j < 16; j++) {
      const ii = (i + j) & this.mask;
      const vv = this.v[ii];
      if (vv === 0) return 0;
      if (this.k0[ii] === k0 && this.k1[ii] === k1 && this.k2[ii] === k2 && this.k3[ii] === k3) return vv;
    }
    return 0; // deep miss (evicted / never stored): recompute (sound)
  }
  store(k0, k1, k2, k3, verdict) {
    let i = this.h(k0, k1, k2, k3);
    for (let j = 0; j < 16; j++) {
      const ii = (i + j) & this.mask;
      if (this.v[ii] === 0) { this.put(ii, k0, k1, k2, k3, verdict); return; }
      if (this.k0[ii] === k0 && this.k1[ii] === k1 && this.k2[ii] === k2 && this.k3[ii] === k3) { this.v[ii] = verdict; return; }
    }
    this.put(i, k0, k1, k2, k3, verdict); this.overwrites++;
  }
  put(i, k0, k1, k2, k3, verdict) { this.k0[i] = k0; this.k1[i] = k1; this.k2[i] = k2; this.k3[i] = k3; this.v[i] = verdict; }
}

// legal moves of a position: occupied point list (any order) + occ lanes.
// NOTE: sorts pts IN PLACE so that the triple table lookups use ascending
// (a<b<c) indices; all callers use pts only as an unordered set afterwards.
function legalOf(pts, occ) {
  pts.sort((a, b) => a - b);
  const danger = [0, 0, 0, 0];
  const k = pts.length;
  for (let i = 0; i < k; i++)
    for (let j = i + 1; j < k; j++)
      for (let l = j + 1; l < k; l++) {
        const base = 4 * ((pts[i] * V + pts[j]) * V + pts[l]);
        danger[0] |= TBL[base]; danger[1] |= TBL[base + 1];
        danger[2] |= TBL[base + 2]; danger[3] |= TBL[base + 3];
      }
  const out = [0, 0, 0, 0];
  for (let w = 0; w < 4; w++) out[w] = ((w === 3 ? L3TOP : 0xffffffff) & ~(occ[w] | danger[w])) >>> 0;
  return out;
}
function occOf(pts) { const occ = [0, 0, 0, 0]; for (const p of pts) occ[p >> 5] |= (1 << (p & 31)) >>> 0; return occ; }

class Budget { constructor(cap, wallCapSec) { this.cap = cap; this.wallCap = wallCapSec * 1000; this.t0 = Date.now(); this.n = 0; } tick() { this.n++; if (this.n > this.cap) throw { code: 'RUNLIMIT', reason: 'cap' }; if ((this.n & 0xffff) === 0 && Date.now() - this.t0 > this.wallCap) throw { code: 'RUNLIMIT', reason: 'wall' }; } }
class DepthGuard extends Error { constructor(d) { super('depth guard ' + d); this.code = 'DEPTH_GUARD'; } }

let TT = null, budget = null, ttHits = 0;
const CIMG_POOL = [];
function cimgPool(depth) { while (CIMG_POOL.length <= depth) CIMG_POOL.push(new Uint32Array(32)); return CIMG_POOL[depth]; }

// canonical key of an image set (32 uint32 words = 8 images x 4 lanes):
// min image under (lane3,lane2,lane1,lane0) lexicographic compare; returns i*4 base
function canonPick(cimgs) {
  let best = 0;
  for (let j = 1; j < 8; j++) {
    const A = best * 4, B = j * 4;
    if (cimgs[B + 3] !== cimgs[A + 3]) { if (cimgs[B + 3] < cimgs[A + 3]) best = j; continue; }
    if (cimgs[B + 2] !== cimgs[A + 2]) { if (cimgs[B + 2] < cimgs[A + 2]) best = j; continue; }
    if (cimgs[B + 1] !== cimgs[A + 1]) { if (cimgs[B + 1] < cimgs[A + 1]) best = j; continue; }
    if (cimgs[B] < cimgs[A]) best = j;
  }
  return best * 4;
}

// kids scratch: ONE SET PER DEPTH (stones). A previous version used a single
// global KID_IMG/KID_* set; the child solve() recursion then overwrote the
// parent's not-yet-visited sibling entries with grandkid data, corrupting
// sibling canonical keys and flipping WINs. Per-depth pools fix this.
const KIDPOOL = [];
function kidPool(stones) {
  while (KIDPOOL.length <= stones)
    KIDPOOL.push({
      m: new Int32Array(V), cnt: new Int32Array(V), cb: new Int32Array(V),
      st: new Uint8Array(V), leg: new Uint32Array(V * 4), win: new Uint32Array(4),
      img: new Uint32Array(V * 32),
    });
  return KIDPOOL[stones];
}
let VERIFY_LEGAL = false;

function solve(pts, stones, imgs, canonBase, legal) {
  // imgs: own Uint32Array(32) images of occupied; canonBase: index of min image in imgs
  // legal: child legal mask passed from parent (root: legalOf once); derivation is
  // legal(parent) & ~bans(new triples with the added stone) & ~stone -- the same set as
  // a from-scratch legalOf; --verify-legal cross-checks this equality.
  const ck0 = imgs[canonBase], ck1 = imgs[canonBase + 1], ck2 = imgs[canonBase + 2], ck3 = imgs[canonBase + 3];
  const memo = TT.find(ck0 >>> 0, ck1 >>> 0, ck2 >>> 0, ck3 >>> 0);
  if (memo !== 0) { ttHits++; return memo; }
  budget.tick();
  if (VERIFY_LEGAL) {
    const lg2 = legalOf(pts.slice(), occOf(pts));
    for (let w = 0; w < 4; w++) if (lg2[w] !== legal[w]) throw new Error('legal derivation mismatch at stones=' + stones);
  }
  const legalCnt = pop4(legal, 0);
  if (legalCnt === 0) {
    const verdict = (stones % 2 === 0) ? 2 : 1;
    TT.store(ck0 >>> 0, ck1 >>> 0, ck2 >>> 0, ck3 >>> 0, verdict);
    return verdict;
  }
  const orNode = (stones % 2 === 0);
  // per-depth kids scratch (recursion-safe)
  const KID = kidPool(stones);
  const KID_M = KID.m, KID_CNT = KID.cnt, KID_CB = KID.cb, KID_IMG = KID.img, KID_LEG = KID.leg;
  const npar = pts.length;
  // enumerate children
  let nkids = 0;
  for (let w = 0; w < 4; w++) {
    let x = legal[w] >>> 0;
    while (x !== 0) {
      const t = x & -x; x ^= t;
      const m = w * 32 + 31 - Math.clz32(t);
      const lane = m >> 5, bit = (1 << (m & 31)) >>> 0;
      // ---- compute child images and canonical base ----
      const dst = KID_IMG, src = imgs, tb = m * 32;
      const imgBase = nkids * 32;
      for (let j = 0; j < 32; j++) dst[imgBase + j] = src[j] | TBPT[tb + j];
      const cb = canonPickFrom(dst, imgBase);
      // dedup by canonical key (same-class children collapse, replica parity)
      const k0 = dst[imgBase + cb] >>> 0, k1 = dst[imgBase + cb + 1] >>> 0;
      const k2 = dst[imgBase + cb + 2] >>> 0, k3 = dst[imgBase + cb + 3] >>> 0;
      {
        let dup = false;
        for (let q2 = 0; q2 < nkids; q2++) {
          const qb = q2 * 32 + KID_CB[q2];
          if (KID_IMG[qb] === k0 && KID_IMG[qb + 1] === k1 && KID_IMG[qb + 2] === k2 && KID_IMG[qb + 3] === k3) { dup = true; break; }
        }
        if (dup) continue;
      }
      // TT-status priority (replica parity: resolved-good first)
      {
        const memoC = TT.find(k0, k1, k2, k3);
        let pri = 1; // open
        if (memoC !== 0) {
          if (orNode) pri = memoC === 1 ? 0 : 2;
          else pri = memoC === 2 ? 0 : 2;
        }
        KID.st[nkids] = pri;
      }
      KID_CB[nkids] = cb;
      KID_M[nkids] = m;
      // derive child legal mask (passed down; root derives once via legalOf)
      const lb = nkids * 4;
      KID_LEG[lb] = legal[0] >>> 0; KID_LEG[lb + 1] = legal[1] >>> 0;
      KID_LEG[lb + 2] = legal[2] >>> 0; KID_LEG[lb + 3] = (legal[3] & L3TOP) >>> 0;
      for (let i = 0; i < npar; i++) {
        const pi = pts[i];
        for (let j = i + 1; j < npar; j++) {
          let A = pi, B = pts[j], C = m;
          if (A > B) { const q = A; A = B; B = q; }
          if (B > C) { const q = B; B = C; C = q; }
          if (A > B) { const q = A; A = B; B = q; }
          const base = 4 * ((A * V + B) * V + C);
          KID_LEG[lb] &= ~TBL[base]; KID_LEG[lb + 1] &= ~TBL[base + 1];
          KID_LEG[lb + 2] &= ~TBL[base + 2]; KID_LEG[lb + 3] &= ~TBL[base + 3];
        }
      }
      KID_LEG[lb + lane] = (KID_LEG[lb + lane] & ~bit) >>> 0;
      KID_CNT[nkids] = popW(KID_LEG[lb]) + popW(KID_LEG[lb + 1]) + popW(KID_LEG[lb + 2]) + popW(KID_LEG[lb + 3]);
      nkids++;
      if (nkids > V) throw new Error('kids overflow');
    }
  }
  // ordering: status pri asc, cnt asc, canon asc, m asc
  const ord = [];
  for (let i = 0; i < nkids; i++) ord.push(i);
  ord.sort((a, b) => {
    const dp = KID.st[a] - KID.st[b]; if (dp) return dp;
    const dc = KID_CNT[a] - KID_CNT[b]; if (dc) return dc;
    const ca = a * 32 + KID_CB[a], cb = b * 32 + KID_CB[b];
    for (let w = 3; w >= 0; w--) {
      const va = KID_IMG[ca + w], vb = KID_IMG[cb + w];
      if (va !== vb) return va < vb ? -1 : 1;
    }
    return KID_M[a] - KID_M[b];
  });
  const WIN = KID.win;
  let verdict = orNode ? 2 : 1;
  for (const idx of ord) {
    const m = KID_M[idx], cb = KID_CB[idx];
    const k0 = KID_IMG[idx * 32 + cb] >>> 0, k1 = KID_IMG[idx * 32 + cb + 1] >>> 0;
    const k2 = KID_IMG[idx * 32 + cb + 2] >>> 0, k3 = KID_IMG[idx * 32 + cb + 3] >>> 0;
    // copy child images into the child's pooled buffer
    const cimg = cimgPool(stones);
    for (let j = 0; j < 32; j++) cimg[j] = KID_IMG[idx * 32 + j];
    WIN[0] = KID_LEG[idx * 4] >>> 0; WIN[1] = KID_LEG[idx * 4 + 1] >>> 0;
    WIN[2] = KID_LEG[idx * 4 + 2] >>> 0; WIN[3] = KID_LEG[idx * 4 + 3] >>> 0;
    const memoC = TT.find(k0, k1, k2, k3);
    let cr;
    if (memoC !== 0) { ttHits++; cr = memoC; }
    else {
      if (stones + 1 > 60) throw new DepthGuard(stones + 1);
      pts.push(m);
      cr = solve(pts, stones + 1, cimg, cb, WIN);
      pts.pop();
    }
    if (orNode && cr === 1) { verdict = 1; TT.store(ck0 >>> 0, ck1 >>> 0, ck2 >>> 0, ck3 >>> 0, verdict); return verdict; }
    if (!orNode && cr === 2) { verdict = 2; TT.store(ck0 >>> 0, ck1 >>> 0, ck2 >>> 0, ck3 >>> 0, verdict); return verdict; }
  }
  TT.store(ck0 >>> 0, ck1 >>> 0, ck2 >>> 0, ck3 >>> 0, verdict);
  return verdict;
}
function canonPickFrom(arr, base) {
  let best = 0;
  for (let j = 1; j < 8; j++) {
    const A = base + best * 4, B = base + j * 4;
    if (arr[B + 3] !== arr[A + 3]) { if (arr[B + 3] < arr[A + 3]) best = j; continue; }
    if (arr[B + 2] !== arr[A + 2]) { if (arr[B + 2] < arr[A + 2]) best = j; continue; }
    if (arr[B + 1] !== arr[A + 1]) { if (arr[B + 1] < arr[A + 1]) best = j; continue; }
    if (arr[B] < arr[A]) best = j;
  }
  return best * 4;
}

// ---- driver ----
if (require.main === module) {
  const arg = (n, d) => { const p = '--' + n + '='; for (let i = 2; i < process.argv.length; i++) if (process.argv[i].startsWith(p)) return process.argv[i].slice(p.length); return d; };
  const lo = BigInt(arg('lo', '-1')), hi = BigInt(arg('hi', '-1'));
  const stones = parseInt(arg('stones', '5'), 10), legalIn = parseInt(arg('legal', '-1'), 10);
  const row = arg('row', 'r0'), cap = parseInt(arg('cap', '300000000'), 10);
  const wallCap = parseInt(arg('wallcap', '2700'), 10), power = parseInt(arg('memo-power', '22'), 10);
  const t0 = Date.now();
  const bits = [];
  {
    let x = lo; for (let i = 0; i < 64; i++) { if (x & 1n) bits.push(i); x >>= 1n; }
    let y = hi; for (let i = 0; i < 57; i++) { if (y & 1n) bits.push(i + 64); y >>= 1n; }
  }
  const fail = (msg) => { console.log('third,' + row + ',' + stones + ',' + legalIn + ',,GATE_FAIL,' + JSON.stringify(msg)); process.exit(1); };
  if (lo < 0n || hi < 0n) fail('missing lo/hi');
  if (new Set(bits).size !== bits.length) fail('duplicate point');
  for (const b of bits) if (b < 0 || b >= V) fail('point out of range');
  if (bits.length !== stones) fail('stone count mismatch: bits=' + bits.length + ' declared=' + stones);
  bits.sort((a, b) => a - b);
  for (let i = 0; i < bits.length; i++)
    for (let j = i + 1; j < bits.length; j++)
      for (let l = j + 1; l < bits.length; l++)
        for (let m = l + 1; m < bits.length; m++)
          if (forbiddenQuad(bits[i], bits[j], bits[l], bits[m])) fail('unsafe root (forbidden quadruple)');
  const legal = legalOf(bits, occOf(bits));
  const legalDerived = pop4(legal, 0);
  if (legalIn >= 0 && legalDerived !== legalIn) fail('legal count mismatch: derived=' + legalDerived + ' declared=' + legalIn);
  // root images
  const imgs = new Uint32Array(32);
  for (const p of bits) for (let j = 0; j < 32; j++) imgs[j] |= TBPT[p * 32 + j];
  const canonBase = canonPickFrom(imgs, 0);
  TT = new Slab(power);
  budget = new Budget(cap, wallCap);
  VERIFY_LEGAL = arg('verify-legal', '0') === '1';
  let result = 0, reason = 'clean';
  try {
    result = solve(bits, stones, imgs, canonBase, legal);
  } catch (e) {
    if (e && e.code === 'RUNLIMIT') { result = 0; reason = 'runlimit:' + e.reason; }
    else if (e && e.code === 'DEPTH_GUARD') { result = 0; reason = 'depth_guard'; }
    else throw e;
  }
  const wallS = (Date.now() - t0) / 1000;
  console.log('third,' + row + ',' + stones + ',' + legalIn + ',' + legalDerived + ',' + result + ',' + budget.n + ',' + ttHits + ',' + wallS.toFixed(2) + ',' + lo.toString() + ',' + hi.toString() + ',' + reason + ',quads=' + quadCount + ',ttOverwrites=' + TT.overwrites + ',memoPower=' + power);
}
module.exports = { forbiddenQuad, quadCount, legalOf, pop4, occOf };
