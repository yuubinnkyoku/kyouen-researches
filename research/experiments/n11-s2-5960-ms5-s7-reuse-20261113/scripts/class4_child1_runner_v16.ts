// class4-batch1 child#1 external runner v16 (2026-11-14) — standalone, zero deps.
//
// Purpose: external depth-10 candidate sweeps with per-candidate engine reset.
// v16 keeps the v15 game rules and move ordering, but repairs the transposition-table
// key signedness and negative-bound sentinels. See the 2026-11-14 v16 memo-key log.
//
// Validation of this file's engine (session 5, run in the Vibe sandbox):
//  - pilot d6 control: loss=false, 3,402 nodes (v15 baseline: 5,949)
//  - pilot d8 default AND order: loss=false, 277,393 nodes (matches session-3/4)
//  - pilot d8 close-first AND: loss=false, 193,556 nodes (matches session-4 -30%)
//  - bit=15 on child 00000000020000003800000280000000, d8 close-first:
//    loss=false, 56,791 nodes, terminal [13,15] (v15 baseline: 146,514)
//
// Usage (Node >= 22):
//   node --experimental-strip-types class4_child1_runner_v16.ts (continuation
//        backslash omitted here: it does not survive the push transport)
//        --bits 34,54,88 --depth 10 --cap 950000 --out results.jsonl
//   --andclose 0|1   close-first AND ordering (lossAt children by wscore DESC);
//                   default 1: applied only when depth >= 8 (session-4 finding:
//                   -30% at pilot d8, worse at d6)
//   --nocontrol      skip the pilot d6 control (default: run it, require
//                    loss=false at exactly 3402 nodes, else abort)
//   --child HEX      S6 child hex (default 00000000020000003800000080080000)
//
// Output JSONL lines: {bit, loss, nodes, capped, terminalStoneRange, ms}
//  loss=true  => WIN7-within-depth candidate (certificate rebuild target)
//  loss=false && !capped => no winner win within depth (NOT a refutation)
//  capped => proves nothing either way
const N = 121;
const FULL0 = 0xFFFFFFFF | 0, FULL1 = 0xFFFFFFFF | 0, FULL2 = 0xFFFFFFFF | 0, FULL3 = 0x01FFFFFF | 0;
const X = new Int32Array(N), Y = new Int32Array(N), Q = new Int32Array(N);
for (let i = 0; i < N; i++) { X[i] = i % 11; Y[i] = (i / 11) | 0; Q[i] = X[i] * X[i] + Y[i] * Y[i]; }
function hexCells(hex) {
  const v = BigInt('0x' + hex); const out = [];
  for (let i = 0; i < N; i++) if ((v >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function freshEngine() {
  // per-candidate state; nothing is shared across candidates
  const FBS = 1 << 17, FBM = FBS - 1;
  const fbKey = new Int32Array(FBS), fbV = new Uint32Array(FBS * 4);
  let cB0 = 0, cB1 = 0, cB2 = 0, cB3 = 0;
  const MS = 1 << 18, MM = MS - 1;
  const mK0=new Uint32Array(MS), mK1=new Uint32Array(MS), mK2=new Uint32Array(MS), mK3=new Uint32Array(MS);
  const mWin=new Uint8Array(MS), mLose=new Uint8Array(MS), mNoWin=new Uint8Array(MS), mNoLose=new Uint8Array(MS), mOcc=new Uint8Array(MS);
  let M0=0,M1=0,M2=0,M3=0, B0=0,B1=0,B2=0,B3=0;
  let stones = [];
  let nodes = 0, CAP = 1e9, capped = false, maxTerm = 0, minTerm = 121;
  const wscore = new Int32Array(N);
  let ANDCLOSE = false;
  function fbtOR(a, b, c) {
    const key = (a * 121 + b) * 121 + c + 1;
    let h = (Math.imul(key, 2654435761) >>> 0) & FBM;
    for (let n = 0; n < 48; n++) {
      const k = fbKey[h];
      if (k === key) { cB0 |= fbV[h*4]; cB1 |= fbV[h*4+1]; cB2 |= fbV[h*4+2]; cB3 |= fbV[h*4+3]; return; }
      if (k === 0) {
        let m0=0,m1=0,m2=0,m3=0;
        const qb=Q[b]-Q[a], xb=X[b]-X[a], yb=Y[b]-Y[a], qc=Q[c]-Q[a], xc=X[c]-X[a], yc=Y[c]-Y[a];
        for (let d = 0; d < N; d++) {
          if (d===a||d===b||d===c) continue;
          const qd=Q[d]-Q[a], xd=X[d]-X[a], yd=Y[d]-Y[a];
          const det = qb*(xc*yd-yc*xd) - xb*(qc*yd-yc*qd) + yb*(qc*xd-xc*qd);
          if (det===0) { const w=d>>>5, bit=1<<(d&31);
            if (w===0) m0|=bit; else if (w===1) m1|=bit; else if (w===2) m2|=bit; else m3|=bit; }
        }
        fbKey[h]=key; fbV[h*4]=m0; fbV[h*4+1]=m1; fbV[h*4+2]=m2; fbV[h*4+3]=m3;
        cB0|=m0; cB1|=m1; cB2|=m2; cB3|=m3; return;
      }
      h = (h + 1) & FBM;
    }
  }
  function mHash() { return ((Math.imul(M0,73856093)^Math.imul(M1,19349663)^Math.imul(M2,83492791)^Math.imul(M3,39916801))>>>0)&MM; }
  function memoFind() { let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0)return -1;
    if(mK0[h]===(M0>>>0)&&mK1[h]===(M1>>>0)&&mK2[h]===(M2>>>0)&&mK3[h]===(M3>>>0))return h; h=(h+1)&MM; } return -1; }
  function memoEntry() { let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0){
    mOcc[h]=1; mK0[h]=M0; mK1[h]=M1; mK2[h]=M2; mK3[h]=M3;
    mWin[h]=255; mLose[h]=255; mNoWin[h]=255; mNoLose[h]=255; return h; }
    if(mK0[h]===(M0>>>0)&&mK1[h]===(M1>>>0)&&mK2[h]===(M2>>>0)&&mK3[h]===(M3>>>0))return h; h=(h+1)&MM; } return -1; }
  function bump(m, sign) {
    const mx=X[m], my=Y[m];
    for(let dy=-3;dy<=3;dy++){ const ny=my+dy; if(ny<0||ny>10)continue;
      const nxb=Math.max(0,mx-3), nxe=Math.min(10,mx+3);
      for(let nx2=nxb;nx2<=nxe;nx2++){ const dd=Math.max(Math.abs(nx2-mx),Math.abs(dy));
        wscore[ny*11+nx2]+=sign*(4-dd); } }
  }
  function apply(m) {
    const k=stones.length; cB0=B0; cB1=B1; cB2=B2; cB3=B3;
    for(let i=0;i<k;i++){ const a=stones[i];
      for(let j=i+1;j<k;j++){ const b=stones[j];
        let A,Bb,C; if(m<a){A=m;Bb=a;C=b;} else if(m<b){A=a;Bb=m;C=b;} else {A=a;Bb=b;C=m;}
        fbtOR(A,Bb,C); } }
    const w=m>>>5, bit=1<<(m&31);
    if(w===0)cB0|=bit; else if(w===1)cB1|=bit; else if(w===2)cB2|=bit; else cB3|=bit;
    B0=cB0; B1=cB1; B2=cB2; B3=cB3; stones.push(m);
    if(w===0)M0|=bit; else if(w===1)M1|=bit; else if(w===2)M2|=bit; else M3|=bit;
    bump(m,1);
  }
  function unapply(m) { bump(m,-1); stones.pop(); }
  const winMoves = Array.from({length:80},()=>[]);
  const lossMoves = Array.from({length:80},()=>[]);
  function legalMoves(arr) {
    arr.length = 0;
    let w=FULL0&~B0; while(w){const b=w&-w; arr.push(Math.clz32(b)^31); w^=b;}
    w=FULL1&~B1; while(w){const b=w&-w; arr.push(32+(Math.clz32(b)^31)); w^=b;}
    w=FULL2&~B2; while(w){const b=w&-w; arr.push(64+(Math.clz32(b)^31)); w^=b;}
    w=FULL3&~B3; while(w){const b=w&-w; arr.push(96+(Math.clz32(b)^31)); w^=b;}
    return arr.length;
  }
  function noteTerm() { const s=stones.length; if(s>maxTerm)maxTerm=s; if(s<minTerm)minTerm=s; }
  function winAt(d) {
    if(capped) return false; nodes++;
    if(nodes>CAP){ capped=true; return false; }
    const arr=winMoves[d];
    if(legalMoves(arr)===0) return false;
    if(d===0) return false;
    const e=memoFind();
    if(e>=0){ if(mLose[e]<255) return false; if(mWin[e]<=d) return true;
      if(mNoWin[e]<255 && d<=mNoWin[e]) return false; }
    if(arr.length>1) arr.sort((p,q)=>wscore[q]-wscore[p]);
    for(let i=0;i<arr.length;i++){
      const m=arr[i];
      const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
      apply(m); const r=lossAt(d-1);
      unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
      if(r){ if(!capped){ const h=memoEntry(); if(h>=0&&d<mWin[h]) mWin[h]=d; } return true; }
      if(capped) return false;
    }
    if(!capped){ const h=memoEntry(); if(h>=0&&(mNoWin[h]===255||d>mNoWin[h])) mNoWin[h]=d; }
    return false;
  }
  function lossAt(e) {
    if(capped) return false; nodes++;
    if(nodes>CAP){ capped=true; return false; }
    const arr=lossMoves[e];
    if(legalMoves(arr)===0){ noteTerm(); return true; }
    if(e===0) return false;
    const h0=memoFind();
    if(h0>=0){ if(mLose[h0]<=e) return true; if(mWin[h0]<255) return false;
      if(mNoLose[h0]<255 && e<=mNoLose[h0]) return false; }
    if(ANDCLOSE && arr.length>1) arr.sort((p,q)=>wscore[q]-wscore[p]);
    for(let i=0;i<arr.length;i++){
      const m=arr[i];
      const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
      apply(m); const r=winAt(e-1);
      unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
      if(!r){ if(!capped){ const h=memoEntry(); if(h>=0&&(mNoLose[h]===255||e>mNoLose[h])) mNoLose[h]=e; } return false; }
      if(capped) return false;
    }
    if(!capped){ const h=memoEntry(); if(h>=0&&e<mLose[h]) mLose[h]=e; }
    return true;
  }
  function setRoot(cs) {
    stones=cs.slice(); M0=0;M1=0;M2=0;M3=0; wscore.fill(0);
    for(const c of cs){ const w=c>>>5, bit=1<<(c&31);
      if(w===0)M0|=bit; else if(w===1)M1|=bit; else if(w===2)M2|=bit; else M3|=bit;
      bump(c,1); }
    B0=M0;B1=M1;B2=M2;B3=M3;
    const k=cs.length;
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)for(let l=j+1;l<k;l++){
      cB0=B0;cB1=B1;cB2=B2;cB3=B3; fbtOR(cs[i],cs[j],cs[l]);
      B0=cB0;B1=cB1;B2=cB2;B3=cB3; }
  }
  function solve(cells, depth, nodeCap, andclose) {
    setRoot(cells);
    nodes=0; capped=false; maxTerm=0; minTerm=121; CAP=nodeCap; ANDCLOSE=andclose;
    const loss = lossAt(depth);
    return { loss, nodes, capped, terminalStoneRange: [minTerm, maxTerm] };
  }
  return { solve };
}
const PILOT_CELLS = hexCells('00000000000000003802000008000006');
const CHILD_HEX_DEFAULT = '00000000020000003800000080080000';
function runBatch(cfg) {
  // cfg: { bits:[int], depth, cap, andcloseMode: 0|1, childHex, runControl:bool }
  const results = [];
  const andclose = (d) => cfg.andcloseMode === 1 && d >= 8;
  if (cfg.runControl) {
    const eng = freshEngine();
    const c = eng.solve(PILOT_CELLS.slice(), 6, 1e9, false);
    if (!(c.loss === false && c.nodes === 3402)) {
      throw new Error('PILOT CONTROL FAILED: expected loss=false nodes=3402, got loss=' + c.loss + ' nodes=' + c.nodes + ' — engine unsound, aborting');
    }
    results.push({ control: 'pilot_d6', loss: c.loss, nodes: c.nodes, capped: c.capped });
  }
  const child = hexCells(cfg.childHex || CHILD_HEX_DEFAULT);
  for (const bit of cfg.bits) {
    const eng = freshEngine();
    const t0 = Date.now();
    const r = eng.solve(child.concat([bit]), cfg.depth, cfg.cap, andclose(cfg.depth));
    results.push({ bit, ...r, ms: Date.now() - t0, andclose: andclose(cfg.depth) });
  }
  return results;
}
if (typeof process !== 'undefined' && process.argv && process.argv.length > 2) {
  const args = process.argv.slice(2);
  const get = (k, dflt) => { const i = args.indexOf(k); return i >= 0 ? args[i+1] : dflt; };
  const cfg = {
    bits: (get('--bits', '')).split(',').map(Number).filter(n => !isNaN(n)),
    depth: Number(get('--depth', 10)),
    cap: Number(get('--cap', 950000)),
    andcloseMode: Number(get('--andclose', 1)),
    childHex: get('--child', CHILD_HEX_DEFAULT),
    runControl: !args.includes('--nocontrol'),
  };
  const out = get('--out', null);
  const results = runBatch(cfg);
  // NOTE (2026-11-14 repair): the previously pushed copy of this file was
// transport-corrupted at this line (the two-char backslash-escape newline
// string literals had been decoded into real newlines, making the file
// uncompilable under --experimental-strip-types).
// Repaired to String.fromCharCode(10) literals, which survive the push transport.
const NL = String.fromCharCode(10);
  const lines = results.map(r => JSON.stringify(r)).join(NL) + NL;
  if (out) { const fs = require('fs'); fs.appendFileSync(out, lines); }
  process.stdout.write(lines);
}
