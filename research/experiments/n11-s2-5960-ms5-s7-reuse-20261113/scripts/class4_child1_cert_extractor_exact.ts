// class4-batch1 certificate extractor (session 7, 2026-11-13) — WIN7 strategy-tree extraction
//
// PURPOSE. Given an S6 child + 7th-stone candidate whose lossAt(root,10)=true verdict is
// already established by the chunk decomposition (output/class4-batch1-chunk-decomposition.json),
// extract the FULL winning strategy tree and serialize it as an n11-terminal-strategy-v1
// certificate (original_first_WIN7 second_to_move_LOSS):
//   line 1: n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS
//   line 2: root <32-hex board>
//   then:   <32-hex board> <winner move>, boards sorted ascending, one row per
//           winner-to-move position reachable from the root under ALL loser defenses.
//
// EXTRACTION (engine v15 inlined verbatim below; rules identical to
// scripts/class4_child1_sweep_engine.ts):
//   extractW(cells, depth, pref): winner to move. Tries legal moves in closeScore order
//     (with 'pref' first when known — the session-6 kill table gives the depth-1 winner
//     reply per loser first-move and cuts the extraction cost by 10-40x at depth 1:
//     m=0 cost 597k nodes blind vs 298k with the whole two-move batch kill-first).
//     The first move m with lossAt(cells+m, depth-1)=true (uncapped) is recorded in the
//     strategy and extractL recurses on ALL loser replies.
//   extractL(cells, depth): loser to move. Expands every legal reply; a position with no
//     legal move is a terminal (loser stuck). Returns false if any reply cannot be
//     refuted within the remaining depth — the run then reports fatal (extraction is
//     self-checking: every recorded row is backed by an uncapped depth-bounded proof).
//
// VERIFICATION (performed separately, see scripts/verify_bit7_win7_cert.ts and
// output/class4-batch1-bit7-certificate.json): the resulting 30,947-row certificate for
// bit=7 (root 00000000020000003800000080080080) was independently verified by a TS port of
// verify_five_terminal_loss7.py (exact Bareiss 4x4 determinant, winner_parity=1) over all
// 50 first-loser-move sub-roots: PASS, and the union of consumed winner states equals the
// full row set exactly. Control: a fresh extraction on the published pilot root
// 00000000000000a03808100000000000 (winner=root mover) passed the same verifier port
// (2,510 rows, terminals [14,16]).
//
// OPERATIONAL LESSON (recorded in the log session 7): never read-modify-write a large rows
// file across runs — tools.file_system read_file truncates (~64KB) and this silently
// dropped rows (the session-3 incident re-occurred in session 7 and was caught by the
// verifier's missing-row check). Write one file per run and merge with sort -u.
//
// CLI (zero dependencies, node --experimental-strip-types):
//   node --experimental-strip-types class4_child1_cert_extractor.ts (continuation
//        backslash omitted: it does not survive the push transport)
//     --child 00000000020000003800000080080000 --bit 7 --moves 10,15,18 --out rows.txt
// Each root first-move m is extracted as extractW(root+m, 9, KILL[m]); pass --moves in
// batches that fit the node budget (~620k nodes per sandbox-class run). Rows are appended
// to --out as "<32hex> <move>" lines (merge batches with sort -u, then prepend the header
// and root lines).

// NOTE (2026-11-14 repair): see the CLI block note below about the fs import.
import fs from 'fs';
const NL = String.fromCharCode(10);
const N = 121;
const FULL0 = 0xFFFFFFFF|0, FULL1 = 0xFFFFFFFF|0, FULL2 = 0xFFFFFFFF|0, FULL3 = 0x01FFFFFF|0;
const X = new Int32Array(N), Y = new Int32Array(N), Q = new Int32Array(N);
for (let i = 0; i < N; i++) { X[i]=i%11; Y[i]=(i/11)|0; Q[i]=X[i]*X[i]+Y[i]*Y[i]; }
const FBS = 1<<20, FBM = FBS-1;
let fbtDrops = 0;
const fbKey = new Int32Array(FBS), fbV = new Uint32Array(FBS*4);
let cB0=0,cB1=0,cB2=0,cB3=0;
function fbtOR(a,b,c) {
  const key=(a*121+b)*121+c+1;
  let h=(Math.imul(key,2654435761)>>>0)&FBM;
  for (let n=0;n<96;n++){ const k=fbKey[h];
    if(k===key){ cB0|=fbV[h*4]; cB1|=fbV[h*4+1]; cB2|=fbV[h*4+2]; cB3|=fbV[h*4+3]; return; }
    if(k===0){
      let m0=0,m1=0,m2=0,m3=0;
      const qb=Q[b]-Q[a], xb=X[b]-X[a], yb=Y[b]-Y[a], qc=Q[c]-Q[a], xc=X[c]-X[a], yc=Y[c]-Y[a];
      for(let d=0;d<N;d++){ if(d===a||d===b||d===c)continue;
        const qd=Q[d]-Q[a], xd=X[d]-X[a], yd=Y[d]-Y[a];
        const det=qb*(xc*yd-yc*xd)-xb*(qc*yd-yc*qd)+yb*(qc*xd-xc*qd);
        if(det===0){ const w=d>>>5, bit=1<<(d&31);
          if(w===0)m0|=bit; else if(w===1)m1|=bit; else if(w===2)m2|=bit; else m3|=bit; } }
      fbKey[h]=key; fbV[h*4]=m0; fbV[h*4+1]=m1; fbV[h*4+2]=m2; fbV[h*4+3]=m3;
      cB0|=m0;cB1|=m1;cB2|=m2;cB3|=m3; return; }
    h=(h+1)&FBM; }
  fbtDrops++;
}
const MS=1<<18, MM=MS-1;
const mK0=new Uint32Array(MS),mK1=new Uint32Array(MS),mK2=new Uint32Array(MS),mK3=new Uint32Array(MS);
const mWin=new Uint8Array(MS),mLose=new Uint8Array(MS),mNoWin=new Uint8Array(MS),mNoLose=new Uint8Array(MS),mOcc=new Uint8Array(MS);
let M0=0,M1=0,M2=0,M3=0, B0=0,B1=0,B2=0,B3=0;
let stones: number[] = [];
let nodes=0, CAP=1e9, capped=false, maxTerm=0, minTerm=121;
const wscore=new Int32Array(N);
function mHash(){ return ((Math.imul(M0,73856093)^Math.imul(M1,19349663)^Math.imul(M2,83492791)^Math.imul(M3,39916801))>>>0)&MM; }
function memoFind(){ let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0)return -1;
  if(mK0[h]===M0&&mK1[h]===M1&&mK2[h]===M2&&mK3[h]===M3)return h; h=(h+1)&MM; } return -1; }
function memoEntry(){ let h=mHash(); for(let n=0;n<64;n++){ if(mOcc[h]===0){
  mOcc[h]=1; mK0[h]=M0; mK1[h]=M1; mK2[h]=M2; mK3[h]=M3;
  mWin[h]=255; mLose[h]=255; mNoWin[h]=255; mNoLose[h]=255; return h; }
  if(mK0[h]===M0&&mK1[h]===M1&&mK2[h]===M2&&mK3[h]===M3)return h; h=(h+1)&MM; } return -1; }
function bump(m,sign){ const mx=X[m],my=Y[m];
  for(let dy=-3;dy<=3;dy++){ const ny=my+dy; if(ny<0||ny>10)continue;
    const nxb=Math.max(0,mx-3),nxe=Math.min(10,mx+3);
    for(let nx2=nxb;nx2<=nxe;nx2++){ const dd=Math.max(Math.abs(nx2-mx),Math.abs(dy));
      wscore[ny*11+nx2]+=sign*(4-dd); } } }
function apply(m){ const k=stones.length; cB0=B0;cB1=B1;cB2=B2;cB3=B3;
  for(let i=0;i<k;i++){ const a=stones[i];
    for(let j=i+1;j<k;j++){ const b=stones[j];
      let A,Bb,C; if(m<a){A=m;Bb=a;C=b;} else if(m<b){A=a;Bb=m;C=b;} else {A=a;Bb=b;C=m;}
      fbtOR(A,Bb,C); } }
  const w=m>>>5, bit=1<<(m&31);
  if(w===0)cB0|=bit; else if(w===1)cB1|=bit; else if(w===2)cB2|=bit; else cB3|=bit;
  B0=cB0;B1=cB1;B2=cB2;B3=cB3; stones.push(m);
  if(w===0)M0|=bit; else if(w===1)M1|=bit; else if(w===2)M2|=bit; else M3|=bit;
  bump(m,1); }
function unapply(m){ bump(m,-1); stones.pop(); }
const winMoves = Array.from({length:80},()=>[] as number[]);
const lossMoves = Array.from({length:80},()=>[] as number[]);
function legalMoves(arr){ arr.length=0;
  let w=FULL0&~B0; while(w){const b=w&-w; arr.push(Math.clz32(b)^31); w^=b;}
  w=FULL1&~B1; while(w){const b=w&-w; arr.push(32+(Math.clz32(b)^31)); w^=b;}
  w=FULL2&~B2; while(w){const b=w&-w; arr.push(64+(Math.clz32(b)^31)); w^=b;}
  w=FULL3&~B3; while(w){const b=w&-w; arr.push(96+(Math.clz32(b)^31)); w^=b;}
  return arr.length; }
function noteTerm(){ const s=stones.length; if(s>maxTerm)maxTerm=s; if(s<minTerm)minTerm=s; }
function winAt(d){ if(capped)return false; nodes++;
  if(nodes>CAP){ capped=true; return false; }
  const arr=winMoves[d];
  if(legalMoves(arr)===0) return false;
  if(d===0) return false;
  const e=memoFind();
  if(e>=0){ if(mLose[e]<255) return false; if(mWin[e]<=d) return true;
    if(mNoWin[e]<255 && d<=mNoWin[e]) return false; }
  if(arr.length>1) arr.sort((p,q)=>wscore[q]-wscore[p]);
  for(let i=0;i<arr.length;i++){ const m=arr[i];
    const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
    apply(m); const r=lossAt(d-1);
    unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
    if(r){ if(!capped){ const h=memoEntry(); if(h>=0&&d<mWin[h]) mWin[h]=d; } return true; }
    if(capped) return false; }
  if(!capped){ const h=memoEntry(); if(h>=0&&d>mNoWin[h]) mNoWin[h]=d; }
  return false; }
function lossAt(e){ if(capped)return false; nodes++;
  if(nodes>CAP){ capped=true; return false; }
  const arr=lossMoves[e];
  if(legalMoves(arr)===0){ noteTerm(); return true; }
  if(e===0) return false;
  const h0=memoFind();
  if(h0>=0){ if(mLose[h0]<=e) return true; if(mWin[h0]<255) return false;
    if(mNoLose[h0]<255 && e<=mNoLose[h0]) return false; }
  for(let i=0;i<arr.length;i++){ const m=arr[i];
    const s0=B0,s1=B1,s2=B2,s3=B3,t0=M0,t1=M1,t2=M2,t3=M3;
    apply(m); const r=winAt(e-1);
    unapply(m); B0=s0;B1=s1;B2=s2;B3=s3; M0=t0;M1=t1;M2=t2;M3=t3;
    if(!r){ if(!capped){ const h=memoEntry(); if(h>=0&&e>mNoLose[h]) mNoLose[h]=e; } return false; }
    if(capped) return false; }
  if(!capped){ const h=memoEntry(); if(h>=0&&e<mLose[h]) mLose[h]=e; }
  return true; }
function setRoot(cs){ stones=cs.slice(); M0=0;M1=0;M2=0;M3=0; wscore.fill(0);
  for(const c of cs){ const w=c>>>5, bit=1<<(c&31);
    if(w===0)M0|=bit; else if(w===1)M1|=bit; else if(w===2)M2|=bit; else M3|=bit;
    bump(c,1); }
  B0=M0;B1=M1;B2=M2;B3=M3;
  const k=cs.length;
  for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)for(let l=j+1;l<k;l++){
    cB0=B0;cB1=B1;cB2=B2;cB3=B3; fbtOR(cs[i],cs[j],cs[l]);
    B0=cB0;B1=cB1;B2=cB2;B3=cB3; } }
function hexCells(hex){ const v=BigInt('0x'+hex); const out=[];
  for(let i=0;i<N;i++) if((v>>BigInt(i))&1n) out.push(i); return out; }
function cellsHex(cells){ let v=0n;
  for(const c of cells) v|=1n<<BigInt(c);
  return v.toString(16).padStart(32,'0'); }

const rows = new Map<string, number>();
export function extractW(cells: number[], depth: number, pref: number | null): boolean {
  if (capped) return false;
  setRoot(cells);
  const arr: number[] = []; const nm = legalMoves(arr);
  if (nm === 0) return false;
  if (depth === 0) return false;
  let order: number[];
  if (pref != null && arr.includes(pref)) {
    order = [pref].concat(arr.filter(m=>m!==pref).sort((p,q)=>wscore[q]-wscore[p]));
  } else order = arr.slice().sort((p,q)=>wscore[q]-wscore[p]);
  for (const m of order) {
    setRoot(cells.concat([m]).sort((a,b)=>a-b));
    const l = lossAt(depth-1);
    if (l && !capped) {
      rows.set(cellsHex(cells), m);
      return extractL(cells.concat([m]).sort((a,b)=>a-b), depth-1);
    }
    if (capped) return false;
  }
  return false;
}
export function extractL(cells: number[], depth: number): boolean {
  if (capped) return false;
  setRoot(cells);
  const arr: number[] = []; const nm = legalMoves(arr);
  if (nm === 0) { noteTerm(); return true; }
  if (depth === 0) return false;
  for (const m of arr) {
    if (!extractW(cells.concat([m]).sort((a,b)=>a-b), depth-1, null)) return false;
    if (capped) return false;
  }
  return true;
}

// ---- batch driver: extract subtrees for a list of root first-loser-moves ----
export function extractBatch(childHex: string, bit: number, killTable: Record<number, number>, moves: number[]) {
  const base = hexCells(childHex).concat([bit]).sort((a,b)=>a-b);
  const perMove: Record<string, any> = {};
  const out: string[] = [];
  let sum = 0;
  CAP = 1e9;
  for (const m of moves) {
    nodes = 0; capped = false; maxTerm = 0; minTerm = 121;
    const ok = extractW(base.concat([m]).sort((a,b)=>a-b), 9, killTable[m] ?? null);
    const used = nodes; sum += used;
    perMove[m] = { ok, nodes: used, capped, terminalRange: capped ? null : [minTerm, maxTerm] };
    if (!ok || capped) return { perMove, sum, fatal: m, fbt_drops: fbtDrops };
  }
  for (const [k, v] of rows) out.push(k + ' ' + v);
  return { perMove, sum, rows: out, nRows: rows.size, fbt_drops: fbtDrops, fatal: fbtDrops > 0 ? 'fbt_saturation' : undefined };
}

if (typeof process !== 'undefined' && process.argv && process.argv[1] && process.argv[1].endsWith('class4_child1_cert_extractor_exact.ts')) {
  const arg = (name: string, dflt: string) => { const i = process.argv.indexOf('--'+name); return i >= 0 ? process.argv[i+1] : dflt; };
  const KILL_BIT7 = {0:114,8:21,10:81,15:40,18:40,21:40,28:80,32:81,33:18,34:83,38:70,40:18,44:81,45:28,50:18,54:8,66:18,67:80,70:38,72:88,75:50,76:40,78:70,80:28,81:32,82:50,83:8,84:40,86:72,87:70,88:72,90:8,91:8,92:50,93:8,94:28,102:90,104:40,105:18,106:81,108:18,109:70,110:8,112:82,113:81,114:38,116:8,117:8,118:18,120:28};
  const moves = arg('moves','').split(',').filter(s=>s!=='').map(Number);
  const res = extractBatch(arg('child','00000000020000003800000080080000'), Number(arg('bit',7)), KILL_BIT7, moves);
  process.stdout.write(JSON.stringify({ ...res, rows: res.rows ? res.rows.length : undefined }) + NL);
  // NOTE (2026-11-14 repair): this module is ESM (top-level exports), so the CLI
  // block's require('fs') was undefined under --experimental-strip-types and the
  // rows file was silently never written. Also, backslash escape literals do not
  // survive the push transport; use String.fromCharCode(10).
  if (res.rows && arg('out','')) { fs.appendFileSync(arg('out',''), res.rows.join(NL) + NL); }
}
