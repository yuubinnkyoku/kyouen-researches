// class4-batch1 child#1 sweep engine v15 (rebuilt 2026-11-13, session 2)
// Reimplementation of the sandbox-only "engine v14" after it was lost with the
// previous sandbox session. Rules match research/experiments/n11-central-19-cover-20261031/
// verify_five_terminal_loss7.py exactly: cell i = bit i of the 128-bit hex key
// (x = i % 11, y = i / 11); a move is legal iff the cell is empty and placing it
// does NOT complete a 4-point cocircular/collinear set with the stones on board
// (3x3 difference determinant == 4x4 Bareiss det == 0); a player with no legal
// move loses. lossAt(e): the player to move at the node loses within e plies;
// winAt(d): the player to move at the node forces a win within d plies.
// All memoised results are depth-bounded facts (proven-win min depth, proven-loss
// min depth, no-win-within max depth, no-loss-within max depth); cap-aborted
// results are never memoised, so capped runs stay sound and simply unproven.
//
// Validation performed at rebuild time (see class4-batch1-progress-audit.json):
//  - child#1 00000000020000003800000080080000: 66 non-degenerate 7th-stone
//    candidates, and all 66 root mobility values match the published table.
//  - pilot 00000000000000003802000008000006: lossAt(6)=false (5,949 nodes),
//    lossAt(8)=false (277,800 nodes) -> matches published d6/d8 fails.
//  - published LOSS7-orientation root 00000000000000a03808100000000000
//    (winner = root mover): winAt(10)=true, terminal stone range [12,16]
//    exactly matches the published verifier stats (12,16).
// Node counts are NOT comparable with the lost v14 numbers (different
// move-ordering details); verdicts and terminal ranges are.
//
// Run inside the Vibe run_typescript sandbox: replace the driver at the bottom
// with the candidate bit / depth / node cap of the current sweep slice.

const N = 121;
const FULL0 = 0xFFFFFFFF | 0, FULL1 = 0xFFFFFFFF | 0, FULL2 = 0xFFFFFFFF | 0, FULL3 = 0x01FFFFFF | 0;
const X = new Int32Array(N), Y = new Int32Array(N), Q = new Int32Array(N);
for (let i = 0; i < N; i++) { X[i] = i % 11; Y[i] = (i / 11) | 0; Q[i] = X[i] * X[i] + Y[i] * Y[i]; }

// fbt triple-ban cache (open addressing). Key packs sorted (a,b,c) as
// (a*121+b)*121+c+1; value is the 4-word forbidden mask of that triple.
const FBS = 1 << 17, FBM = FBS - 1;
const fbKey = new Int32Array(FBS), fbV = new Uint32Array(FBS * 4);
let cB0 = 0, cB1 = 0, cB2 = 0, cB3 = 0;
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

// position memo (open addressing, 4-word key; win/lose/noWin/noLose bounds).
const MS = 1 << 18, MM = MS - 1;
const mK0=new Uint32Array(MS), mK1=new Uint32Array(MS), mK2=new Uint32Array(MS), mK3=new Uint32Array(MS);
const mWin=new Uint8Array(MS), mLose=new Uint8Array(MS), mNoWin=new Uint8Array(MS), mNoLose=new Uint8Array(MS), mOcc=new Uint8Array(MS);
let M0=0,M1=0,M2=0,M3=0, B0=0,B1=0,B2=0,B3=0;
let stones = [];
let nodes = 0, CAP = 1e9, capped = false, maxTerm = 0, minTerm = 121;
const wscore = new Int32Array(N); // closeScore: sum over stones of 4-chebyshev-dist (radius 3)
function mHash() { return ((Math.imul(M0,73856093)^Math.imul(M1,19349663)^Math.imul(M2,83492791)^Math.imul(M3,39916801))>>>0)&MM; }
function memoFind() { let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0)return -1;
  if(mK0[h]===M0&&mK1[h]===M1&&mK2[h]===M2&&mK3[h]===M3)return h; h=(h+1)&MM; } return -1; }
function memoEntry() { let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0){
  mOcc[h]=1; mK0[h]=M0; mK1[h]=M1; mK2[h]=M2; mK3[h]=M3;
  mWin[h]=255; mLose[h]=255; mNoWin[h]=255; mNoLose[h]=255; return h; }
  if(mK0[h]===M0&&mK1[h]===M1&&mK2[h]===M2&&mK3[h]===M3)return h; h=(h+1)&MM; } return -1; }
function bump(m, sign) {
  const mx=X[m], my=Y[m];
  for(let dy=-3;dy<=3;dy++){ const ny=my+dy; if(ny<0||ny>10)continue;
    const nxb=Math.max(0,mx-3), nxe=Math.min(10,mx+3);
    for(let nx2=nxb;nx2<=nxe;nx2++){ const dd=Math.max(Math.abs(nx2-mx),Math.abs(dy));
      wscore[ny*11+nx2]+=sign*(4-dd); } }
}
// apply(m): child banned = parent banned | bit(m) | U_{pairs} fbt(pair, m).
// bit(m) MUST be OR-ed into the banned words (v14-class bug: forgetting it lets
// the mover replay the same cell and corrupts the memo with bogus nodes=1 hits).
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
  arr.length = 0; // NOTE: per-depth arrays only; never share one array across levels
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
  if(legalMoves(arr)===0) return false;      // mover stuck: mover loses
  if(d===0) return false;                    // horizon: nothing proven
  const e=memoFind();
  if(e>=0){ if(mLose[e]<255) return false; if(mWin[e]<=d) return true;
    if(mNoWin[e]<255 && d<=mNoWin[e]) return false; }
  if(arr.length>1) arr.sort((p,q)=>wscore[q]-wscore[p]); // closeScore ordering
  for(let i=0;i<arr.length;i++){
    const m=arr[i];
    const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
    apply(m); const r=lossAt(d-1);
    unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
    if(r){ if(!capped){ const h=memoEntry(); if(h>=0&&d<mWin[h]) mWin[h]=d; } return true; }
    if(capped) return false;
  }
  if(!capped){ const h=memoEntry(); if(h>=0&&d>mNoWin[h]) mNoWin[h]=d; }
  return false;
}
function lossAt(e) {
  if(capped) return false; nodes++;
  if(nodes>CAP){ capped=true; return false; }
  const arr=lossMoves[e];
  if(legalMoves(arr)===0){ noteTerm(); return true; } // mover stuck: mover loses
  if(e===0) return false;
  const h0=memoFind();
  if(h0>=0){ if(mLose[h0]<=e) return true; if(mWin[h0]<255) return false;
    if(mNoLose[h0]<255 && e<=mNoLose[h0]) return false; }
  for(let i=0;i<arr.length;i++){
    const m=arr[i];
    const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
    apply(m); const r=winAt(e-1);
    unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
    if(!r){ if(!capped){ const h=memoEntry(); if(h>=0&&e>mNoLose[h]) mNoLose[h]=e; } return false; }
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
  B0=M0;B1=M1;B2=M2;B3=M3; // banned includes the occupied cells themselves
  const k=cs.length;
  for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)for(let l=j+1;l<k;l++){
    cB0=B0;cB1=B1;cB2=B2;cB3=B3; fbtOR(cs[i],cs[j],cs[l]);
    B0=cB0;B1=cB1;B2=cB2;B3=cB3; }
}
function hexCells(hex) {
  const v=BigInt('0x'+hex); const out=[];
  for(let i=0;i<N;i++) if((v>>BigInt(i))&1n) out.push(i);
  return out;
}

// ---- driver (edit per sweep slice) ----
export function solveCandidate(childHex, bit, depth, nodeCap) {
  const child = hexCells(childHex);
  setRoot(child.concat([bit]));       // root mover = the losing side (winner_parity=1 cert)
  nodes=0; capped=false; maxTerm=0; minTerm=121; CAP=nodeCap;
  const loss = lossAt(depth);         // true => winner wins within depth (WIN7 candidate)
  return { bit, loss, nodes, capped, terminalStoneRange: [minTerm, maxTerm] };
}
