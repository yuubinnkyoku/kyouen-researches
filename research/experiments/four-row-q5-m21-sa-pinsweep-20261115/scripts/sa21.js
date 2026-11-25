#!/usr/bin/env node
'use strict';
//
// sa21.js — (4,m,5) 単一欠損行 (class {0}, k=3) の SA / pin-sweep 参照実装
// four-row-q5-m21-sa-pinsweep-20261115 (高速レーン 2026-11-15)
//
// 使い方:
//   node sa21.js census [--m 21] [--cell 20,0]
//   node sa21.js verify --witness witness.json --m 20
//   node sa21.js sa --bucket p0|p1 [--pins 1:0,6:2,15:2,18:1] [--iters 2000000]
//        [--seed 1] [--repair 10] [--anneal 5]
//   node sa21.js sweepg20 --bucket p0|p1 [--iters 12000] [--seed 1] [--repair 10] [--anneal 5]
//   node sa21.js manifold --bucket p0|p1 --init init.json [--m 21] [--maxstates 5000]
//
// witness.json / init.json: [[x,y], ...] (15点, profile [3,4,4,4])
//
// コア検証 (TS sandbox, 2026-11-15; 第二実装による独立再検証):
//   census 538 円 (5点180/6点340/8点18, 非共線3点組 89,228)。
//   (20,0)/(0,0) を通る >=5点円は各19本、共通は g* の1本のみ
//   (g* = {(0,0),(4,2),(9,3),(11,3),(16,2),(20,0)}, 6点)。
//   m=20 witness は safe・極大 (count-4 円15本 + 満杯行3本)。
//   p1 seed (V 像移植) は U=1・未遮断 (20,0) のみ。
//   p1 seed の U<=1 多様体はサイズ1 (全169隣接が U>=2)。
//   g20-blocker ケース列挙: p1=83 / p0=86 (sandbox 実行記録と一致)。
//
// 設計:
//   cell id = x*4+y。曲線 = 4行 + >=5点円 (非水平線は最大4点なので q=5 に関与
//   しない; 4点円は空セルを持たないため遮断にも関与しない)。
//   安全 = 全曲線の石数 <= 4。blocked(空セル e) = rowCount[y(e)]==4 または cnt4[e]>0。
//   cnt4[e] = e を通る >=5点円で石数4のものの個数 (add/rm の 3<->4 境界で増分更新)。
//   k3 バケット: profile [3,4,4,4]。p0: (0,0) 固定石 / p1: (0,0) 禁止・(1,0) 固定石。
//   U = 行0の未遮断空セル数 (極大 <=> U=0; 行0は3石なので行満杯での遮断は効かない)。
//   safeSwap(a,e): 石 a -> 同行の空セル e (profile 保存)。e を通る円 g のうち
//   a が g 上に無く石数4のものがあれば不可 (a が g 上なら除去で3に落ちて安全)。
//   ※ 2026-11-15 の sandbox 実行は uphill 受理を含む焼きなましだった。
//   本実装は --anneal P (uphill を P% で受理) で再現可能。hill-climb は --anneal 0。

const ROWS = 4;
const id = (x, y) => x * ROWS + y;
const xOf = (c) => c >> 2;
const yOf = (c) => c & 3;
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; };

const SEED_P1 = [
  [7, 3], [8, 3], [12, 3], [13, 3],
  [4, 2], [5, 2], [6, 2], [14, 2],
  [2, 1], [7, 1], [9, 1], [11, 1],
  [1, 0], [4, 0], [19, 0],
];
function buildCircles(m) {
    const N = m * ROWS;
    const A = [], B = [], C = [], D = [];
    for(let i = 0; i < N; i++)for(let j = i + 1; j < N; j++)for(let k = j + 1; k < N; k++){
      const x1 = xOf(i), y1 = yOf(i), x2 = xOf(j), y2 = yOf(j), x3 = xOf(k), y3 = yOf(k);
      const Dd = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
      if (Dd === 0) continue;
      const r1 = -(x1 * x1 + y1 * y1), r2 = -(x2 * x2 + y2 * y2), r3 = -(x3 * x3 + y3 * y3);
      let U = r1 * (y2 - y3) - y1 * (r2 - r3) + (r2 * y3 - r3 * y2);
      let V = x1 * (r2 - r3) - r1 * (x2 - x3) + (x2 * r3 - x3 * r2);
      let W = x1 * (y2 * r3 - y3 * r2) - y1 * (x2 * r3 - x3 * r2) + r1 * (x2 * y3 - x3 * y2);
      let Dn = Dd;
      if (Dn < 0) {
        Dn = -Dn;
        U = -U;
        V = -V;
        W = -W;
      }
      const g0 = gcd(gcd(Dn, U), gcd(V, W)) || 1;
      A.push(Dn / g0);
      B.push(U / g0);
      C.push(V / g0);
      D.push(W / g0);
    }
    const T = A.length;
    const order = new Array(T);
    for(let i = 0; i < T; i++)order[i] = i;
    order.sort((p, q)=>A[p] - A[q] || B[p] - B[q] || C[p] - C[q] || D[p] - D[q]);
    const circles = [];
    let t = 0;
    while(t < T){
      const i0 = order[t];
      const a0 = A[i0], b0 = B[i0], c0 = C[i0], d0 = D[i0];
      let u = t;
      while(u < T){
        const i = order[u];
        if (A[i] !== a0 || B[i] !== b0 || C[i] !== c0 || D[i] !== d0) break;
        u++;
      }
      const nTrip = u - t;
      if (nTrip >= 10) {
        const pts = [];
        for(let c = 0; c < N; c++)if (a0 * (xOf(c) * xOf(c) + yOf(c) * yOf(c)) + b0 * xOf(c) + c0 * yOf(c) + d0 === 0) pts.push(c);
        const kk = pts.length;
        if (kk * (kk - 1) * (kk - 2) / 6 !== nTrip) throw new Error('census sanity failure');
        circles.push(pts);
      }
      t = u;
    }
    const cellCirc = Array.from({
      length: N
    }, ()=>[]);
    for(let g = 0; g < circles.length; g++)for (const p of circles[g])cellCirc[p].push(g);
    return {
      circles,
      cellCirc,
      triples: T
    };
  }

class State {
    constructor(m, circles, cellCirc){
      this.m = m;
      this.N = m * ROWS;
      this.circles = circles;
      this.cellCirc = cellCirc;
      this.st = new Uint8Array(this.N);
      this.fr = new Uint8Array(this.N);
      this.fe = new Uint8Array(this.N);
      this.rowCnt = [
        0,
        0,
        0,
        0
      ];
      this.cnt = new Int32Array(circles.length);
      this.cnt4 = new Int32Array(this.N);
      this.stones = [];
    }
    add(e) {
      this.st[e] = 1;
      this.stones.push(e);
      this.rowCnt[yOf(e)]++;
      for (const g of this.cellCirc[e])if (++this.cnt[g] === 4) for (const p of this.circles[g])this.cnt4[p]++;
    }
    rm(a) {
      this.st[a] = 0;
      this.stones = this.stones.filter((s)=>s !== a);
      this.rowCnt[yOf(a)]--;
      for (const g of this.cellCirc[a]){
        if (this.cnt[g] === 4) for (const p of this.circles[g])this.cnt4[p]--;
        this.cnt[g]--;
      }
    }
    canAdd(e) {
      return !this.st[e] && !this.fe[e] && this.rowCnt[yOf(e)] < 4 && this.cnt4[e] === 0;
    }
    U() {
      const un = [];
      for(let x = 0; x < this.m; x++){
        const e = id(x, 0);
        if (!this.st[e] && this.cnt4[e] === 0) un.push(e);
      }
      return un;
    }
    safeSwap(a, e) {
      if (a === e || this.st[e] !== 0 || this.st[a] !== 1) return false;
      if (this.fr[a] || this.fe[e]) return false;
      if (yOf(a) !== yOf(e)) return false;
      for (const g of this.cellCirc[e])if (this.cnt[g] === 4 && !this.circles[g].includes(a)) return false;
      return true;
    }
    clone() {
      const s = new State(this.m, this.circles, this.cellCirc);
      s.st = this.st.slice();
      s.fr = this.fr.slice();
      s.fe = this.fe.slice();
      s.rowCnt = this.rowCnt.slice();
      s.cnt = this.cnt.slice();
      s.cnt4 = this.cnt4.slice();
      s.stones = this.stones.slice();
      return s;
    }
  }

function xorshift32(seed) {
    let s = seed >>> 0 || 1;
    return ()=>{
      s ^= s << 13;
      s >>>= 0;
      s ^= s >>> 17;
      s ^= s << 5;
      s >>>= 0;
      return s;
    };
  }

function tryRepair(state, un, rng) {
    const e = un[rng() % un.length];
    const cands = state.cellCirc[e].filter((g)=>state.cnt[g] === 3);
    if (!cands.length) return null;
    const g = cands[rng() % cands.length];
    const empt = state.circles[g].filter((p)=>!state.st[p] && p !== e && !state.fe[p]);
    for(let tr = 0; tr < 10 && empt.length; tr++){
      const f = empt[rng() % empt.length];
      const rowSt = state.stones.filter((s)=>yOf(s) === yOf(f) && !state.fr[s] && !state.circles[g].includes(s));
      if (!rowSt.length) continue;
      const a = rowSt[rng() % rowSt.length];
      if (!state.safeSwap(a, f)) continue;
      state.rm(a);
      state.add(f);
      return {
        blocked: e,
        movedTo: f,
        removed: a
      };
    }
    return null;
  }

function saRun(state, iters, seed, opts) {
    const rng = xorshift32(seed);
    const repair = opts && opts.repair || 0;
    const anneal = opts && opts.anneal || 0;
    let cur = state.U().length;
    let best = cur, acc = 0, u1states = 0;
    const u1hist = {};
    for(let it = 0; it < iters; it++){
      const un = state.U();
      if (cur === 1) {
        u1states++;
        const k = xOf(un[0]) + ',' + yOf(un[0]);
        u1hist[k] = (u1hist[k] || 0) + 1;
      }
      if (cur > 0 && repair > 0 && rng() % 100 < repair) {
        const r = tryRepair(state, un, rng);
        if (r) {
          const nu = state.U().length;
          if (nu <= cur) {
            cur = nu;
            acc++;
            if (cur < best) best = cur;
          } else {
            state.rm(r.movedTo);
            state.add(r.removed);
            cur = state.U().length;
          }
          continue;
        }
      }
      const ns = state.stones.length;
      const a = state.stones[rng() % ns];
      if (state.fr[a]) continue;
      const e2 = id(rng() % state.m, yOf(a));
      if (!state.safeSwap(a, e2)) continue;
      state.rm(a);
      state.add(e2);
      const nu = state.U().length;
      if (nu <= cur || rng() % 100 < anneal) {
        cur = nu;
        acc++;
        if (cur < best) best = cur;
      } else {
        state.rm(e2);
        state.add(a);
      }
    }
    return {
      bestU: best,
      accepted: acc,
      iters,
      seed,
      u1states,
      u1hist
    };
  }

function kSubsets(arr, k) {
    const res = [], cur = [];
    const rec = (start)=>{
      if (cur.length === k) {
        res.push(cur.slice());
        return;
      }
      for(let i = start; i < arr.length; i++){
        cur.push(arr[i]);
        rec(i + 1);
        cur.pop();
      }
    };
    rec(0);
    return res;
  }

function enumerateCases(m, circles, bucket) {
    const target = id(m - 1, 0), origin = id(0, 0);
    const cases = [];
    for(let g = 0; g < circles.length; g++){
      const pts = circles[g];
      if (!pts.includes(target)) continue;
      const hasO = pts.includes(origin);
      let rest, k;
      if (bucket === 'p1') {
        rest = pts.filter((p)=>p !== target && p !== origin);
        k = 4;
      } else if (hasO) {
        rest = pts.filter((p)=>p !== target && p !== origin);
        k = 3;
      } else {
        rest = pts.filter((p)=>p !== target);
        k = 4;
      }
      for (const S of kSubsets(rest, k)){
        if (S.filter((p)=>yOf(p) === 0).length > 2) continue;
        cases.push({
          g,
          S
        });
      }
    }
    return cases;
  }

function buildCaseState(m, circles, cellCirc, bucket, S, rng) {
    for(let attempt = 0; attempt < 300; attempt++){
      const st = new State(m, circles, cellCirc);
      if (bucket === 'p0') st.fr[id(0, 0)] = 1;
      else {
        st.fe[id(0, 0)] = 1;
        st.fr[id(1, 0)] = 1;
      }
      const pins = S.slice();
      if (bucket === 'p0') pins.push(id(0, 0));
      else if (!pins.includes(id(1, 0))) pins.push(id(1, 0));
      let ok = true;
      for (const p of pins){
        if (!st.canAdd(p)) {
          ok = false;
          break;
        }
        st.add(p);
        st.fr[p] = 1;
      }
      if (!ok) return null;
      for (const y of [
        1,
        2,
        3,
        0
      ]){
        const cap = y === 0 ? 3 : 4;
        let guard = 0;
        while(st.rowCnt[y] < cap && guard++ < 500){
          const cands = [];
          for(let x = 0; x < m; x++){
            const e = id(x, y);
            if (st.canAdd(e)) cands.push(e);
          }
          if (!cands.length) {
            ok = false;
            break;
          }
          st.add(cands[rng() % cands.length]);
        }
        if (!ok) break;
      }
      if (ok && st.stones.length === 15) return st;
    }
    return null;
  }

function sweepG20(m, bucket, itersPerCase, seed, opts) {
    const cen = buildCircles(m);
    const cases = enumerateCases(m, cen.circles, bucket);
    const rng0 = xorshift32(seed);
    const hist = {};
    const results = [];
    for(let ci = 0; ci < cases.length; ci++){
      const st = buildCaseState(m, cen.circles, cen.cellCirc, bucket, cases[ci].S, rng0);
      if (!st) {
        hist.fail = (hist.fail || 0) + 1;
        results.push({
          ci,
          fail: true
        });
        continue;
      }
      const r = saRun(st, itersPerCase, seed + 1000 + ci, opts);
      hist[r.bestU] = (hist[r.bestU] || 0) + 1;
      results.push({
        ci,
        bestU: r.bestU,
        initU: st.U().length
      });
    }
    return {
      bucket,
      caseCount: cases.length,
      itersPerCase,
      hist,
      results,
      circles: cen.circles
    };
  }

function manifoldBFS(state, maxStates) {
    const keyOf = (s)=>Array.from(s.stones).sort((p, q)=>p - q).join(',');
    const seen = new Set([
      keyOf(state)
    ]);
    const queue = [
      state
    ];
    const nbHist = {};
    let truncated = false;
    while(queue.length){
      const s = queue.shift();
      for (const a of s.stones.slice()){
        if (s.fr[a]) continue;
        for(let x = 0; x < s.m; x++){
          const e = id(x, yOf(a));
          if (!s.safeSwap(a, e)) continue;
          const cl = s.clone();
          cl.rm(a);
          cl.add(e);
          const u = cl.U().length;
          if (u <= 1) {
            const k = keyOf(cl);
            if (!seen.has(k)) {
              if (seen.size >= maxStates) {
                truncated = true;
                break;
              }
              seen.add(k);
              queue.push(cl);
            }
          } else {
            nbHist['u' + u] = (nbHist['u' + u] || 0) + 1;
          }
        }
        if (truncated) break;
      }
      if (truncated) break;
    }
    return {
      size: seen.size,
      truncated,
      neighborHist: nbHist
    };
  }

function verifyWitness(m, pts) {
    const cen = buildCircles(m);
    const st = new State(m, cen.circles, cen.cellCirc);
    for (const p of pts){
      const e = id(p[0], p[1]);
      if (!st.canAdd(e)) return {
        ok: false,
        reason: 'unsafe add at ' + p[0] + ',' + p[1]
      };
      st.add(e);
    }
    const unblocked = [];
    for(let c = 0; c < m * ROWS; c++){
      if (st.st[c]) continue;
      if (st.rowCnt[yOf(c)] === 4 || st.cnt4[c] > 0) continue;
      unblocked.push([
        xOf(c),
        yOf(c)
      ]);
    }
    let c4circles = 0;
    for(let g = 0; g < cen.circles.length; g++)if (st.cnt[g] === 4) c4circles++;
    return {
      ok: unblocked.length === 0,
      safe: true,
      rows: st.rowCnt,
      unblocked,
      count4Circles: c4circles
    };
  }

function buildSeedState(m, circles, cellCirc, bucket) {
    if (bucket === 'p1') {
      const st = new State(m, circles, cellCirc);
      for (const p of SEED_P1){
        const e = id(p[0], p[1]);
        if (!st.canAdd(e)) throw new Error('seed unsafe');
        st.add(e);
      }
      st.fe[id(0, 0)] = 1;
      st.fr[id(1, 0)] = 1;
      return st;
    }
    for (const r of [
      1,
      4,
      19
    ]){
      const s2 = new State(m, circles, cellCirc);
      let ok = true;
      for (const p of SEED_P1){
        if (p[1] === 0 && p[0] === r) continue;
        const e = id(p[0], p[1]);
        if (!s2.canAdd(e)) {
          ok = false;
          break;
        }
        s2.add(e);
      }
      if (ok && s2.canAdd(id(0, 0))) {
        s2.add(id(0, 0));
        s2.fr[id(0, 0)] = 1;
        return s2;
      }
    }
    return null;
  }

function parseArgs(argv) {
  const opt = { cmd: argv[0] || '' };
  for (let i = 1; i + 1 <= argv.length; i += 2) opt[argv[i].replace(/^--/, '')] = argv[i + 1];
  return opt;
}

function main() {
  const fs = require('fs');
  const opt = parseArgs(process.argv.slice(2));
  const m = Number(opt.m || 21);
  if (opt.cmd === 'census') {
    const cen = buildCircles(m);
    const hist = {};
    for (const p of cen.circles) hist[p.length] = (hist[p.length] || 0) + 1;
    console.log(JSON.stringify({ m: m, circles: cen.circles.length, byPoints: hist, triples: cen.triples }));
    if (opt.cell) {
      const cc = opt.cell.split(',').map(Number);
      const c = id(cc[0], cc[1]);
      const thr = cen.circles.filter((p) => p.includes(c)).map((p) => p.map((q) => [xOf(q), yOf(q)]));
      console.log(JSON.stringify({ cell: cc, through: thr.length, circles: thr }));
    }
  } else if (opt.cmd === 'verify') {
    const pts = JSON.parse(fs.readFileSync(opt.witness, 'utf8'));
    console.log(JSON.stringify(verifyWitness(Number(opt.m || 20), pts)));
  } else if (opt.cmd === 'sa') {
    const bucket = opt.bucket || 'p1';
    const cen = buildCircles(m);
    let st;
    if (opt.pins) {
      const rng = xorshift32(Number(opt.seed || 1));
      const S = opt.pins.split(',').map((t) => { const xy = t.split(':').map(Number); return id(xy[0], xy[1]); });
      st = buildCaseState(m, cen.circles, cen.cellCirc, bucket, S, rng);
      if (!st) { console.log(JSON.stringify({ error: 'case state build failed (pins infeasible)' })); return; }
    } else {
      st = buildSeedState(m, cen.circles, cen.cellCirc, bucket);
      if (!st) { console.log(JSON.stringify({ error: 'seed build failed' })); return; }
    }
    const r = saRun(st, Number(opt.iters || 2000000), Number(opt.seed || 1),
      { repair: Number(opt.repair || 0), anneal: Number(opt.anneal || 0) });
    console.log(JSON.stringify({ bucket: bucket, pins: opt.pins || null, initU: st.U().length, result: r }));
  } else if (opt.cmd === 'sweepg20') {
    const r = sweepG20(m, opt.bucket || 'p1', Number(opt.iters || 12000), Number(opt.seed || 1),
      { repair: Number(opt.repair || 10), anneal: Number(opt.anneal || 5) });
    let bestCi = -1, bestU = 99;
    for (const res of r.results) if (!res.fail && res.bestU < bestU) { bestU = res.bestU; bestCi = res.ci; }
    const casesArr = enumerateCases(m, r.circles, r.bucket);
    const best = bestCi >= 0 ? {
      ci: bestCi, bestU: bestU,
      circle: r.circles[casesArr[bestCi].g].map((q) => [xOf(q), yOf(q)]),
      pins: casesArr[bestCi].S.map((q) => [xOf(q), yOf(q)]),
    } : null;
    console.log(JSON.stringify({ bucket: r.bucket, caseCount: r.caseCount, itersPerCase: r.itersPerCase, hist: r.hist, best: best, results: r.results }));
  } else if (opt.cmd === 'manifold') {
    const bucket = opt.bucket || 'p1';
    const cen = buildCircles(m);
    const pts = JSON.parse(fs.readFileSync(opt.init, 'utf8'));
    const st = new State(m, cen.circles, cen.cellCirc);
    for (const p of pts) { const e = id(p[0], p[1]); if (!st.canAdd(e)) throw new Error('init unsafe'); st.add(e); }
    if (bucket === 'p0') st.fr[id(0, 0)] = 1; else { st.fe[id(0, 0)] = 1; st.fr[id(1, 0)] = 1; }
    const u0 = st.U().length;
    if (u0 > 1) { console.log(JSON.stringify({ error: 'init U > 1', u0: u0 })); return; }
    console.log(JSON.stringify({ bucket: bucket, initU: u0, manifold: manifoldBFS(st, Number(opt.maxstates || 5000)) }));
  } else {
    console.error('usage: sa21.js census|verify|sa|sweepg20|manifold ... (see header comment)');
    process.exit(2);
  }
}
main();
