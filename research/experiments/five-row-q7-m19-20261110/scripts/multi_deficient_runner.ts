// multi_deficient_runner.ts — 5×19 (W=5, M=19) 複数行欠損クラス完全列挙機械
// two_deficient_pair_runner_flat.ts (K0740/K0741) の DEF_ROWS 汎用化版。
// 欠損行集合 DEF_ROWS（各行 ≤DEF_CAP=5 石）以外の行はちょうど FULL=6 石で line-block。
// アルゴリズム・探索順・ノード計数は pair 版と完全同一（census 95円・S0鏡映代表8,378・
// blocker割当DFS・fillRows・witness検出時はverify()で独立検証）。
//
// 制御1（等価性・PASS）: DEF_ROWS=[0,1] は pair版スライスA1（START=0, 600k）と
//   決定的完全一致（done=117, capped=117, max 28,488 @ idx 39 = 0,1,2,5,16, witness 0, leaves 0, nC=95）。
// 制御2（陽性対照・PASS）: 5×18, DEF_ROWS=[0], S0={0,1,5,13,17} で既知第3 witness
//   [[0,1,5,13,17],[3,6,8,10,12,15],[1,3,6,10,12,15],[2,4,6,9,10,14],[6,7,9,11,12,16]]
//   を17,829ノードで完全再現・verify PASS（safe+maximal, 行占有(5,6,6,6,6), そのS0でwitnesses=1）。
//
// 使い方: P の DEF_ROWS / START / NODE_CAP を書き換えるのみ。
//   5行欠損: DEF_ROWS=[0,1,2,3,4] / 4行欠損: [0,1,2,3] 等 / 3行欠損: [0,1,2] 等。
//   run_typescript の sandbox では NODE_CAP=300000 単独実行が安定
//   （census再構築込み。400k+並列2実行は process safety deadline 超過あり）。
//   円censusは厳密整数演算（(nX−qx·den)²+(nY−qy·den)²==ref）。浮動小数点除算禁止。
function gcd(a:number,b:number){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a||1;}
async function main(){
const P={W:5,M:19,DEF_ROWS:[0,1,2,3,4],DEF_CAP:5,FULL:6,NODE_CAP:300000,START:0};
const {W,M,DEF_ROWS,DEF_CAP,FULL,NODE_CAP,START}=P;
const N=W*M,xs=new Int32Array(N),ys=new Int32Array(N);
for(let y=0;y<W;y++)for(let x=0;x<M;x++){xs[x+M*y]=x;ys[x+M*y]=y;}
let nC=0;const tmpOff:number[]=[0];const tmpPts:number[]=[];
{const seen=new Set<string>();const buf=new Int32Array(16);
for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)for(let k=j+1;k<N;k++){
const ax=xs[i],ay=ys[i],bx=xs[j],by=ys[j],cx=xs[k],cy=ys[k];
const d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by));if(d===0)continue;
const a2=ax*ax+ay*ay,b2=bx*bx+by*by,c2=cx*cx+cy*cy;
const ux=a2*(by-cy)+b2*(cy-ay)+c2*(ay-by),uy=a2*(cx-bx)+b2*(ax-cx)+c2*(bx-ax);
let g=gcd(gcd(Math.abs(d),Math.abs(ux)),Math.abs(uy));if(d<0)g=-g;
const D=d/g,Ux=ux/g,Uy=uy/g,R2n=(ax*D-Ux)**2+(ay*D-Uy)**2,R2d=D*D,g2=gcd(R2n,R2d);
const key=Ux+','+Uy+','+D+','+(R2n/g2)+'/'+(R2d/g2);if(seen.has(key))continue;
let m=0;for(let p=0;p<N;p++){const vx=xs[p]*D-Ux,vy=ys[p]*D-Uy;if(vx*vx+vy*vy===R2n)buf[m++]=p;}
if(m>=7){seen.add(key);for(let q=0;q<m;q++)tmpPts.push(buf[q]);tmpOff.push(tmpPts.length);nC++;}}}
const circOff=Int32Array.from(tmpOff),circPts=Int32Array.from(tmpPts);
const pcCount=new Int32Array(N);
for(let ci=0;ci<nC;ci++)for(let o=circOff[ci];o<circOff[ci+1];o++)pcCount[circPts[o]]++;
const pcOff=new Int32Array(N+1);for(let p=0;p<N;p++)pcOff[p+1]=pcOff[p]+pcCount[p];
const pcArr=new Int32Array(pcOff[N]);const fl=new Int32Array(N);fl.fill(0);
for(let ci=0;ci<nC;ci++)for(let o=circOff[ci];o<circOff[ci+1];o++){const p=circPts[o];pcArr[pcOff[p]+fl[p]]=ci;fl[p]++;}
const rowOff=new Int32Array(W+1);for(let y=0;y<W;y++)rowOff[y+1]=rowOff[y]+M;
const rowArr=new Int32Array(N);{let t=0;for(let y=0;y<W;y++)for(let x=0;x<M;x++)rowArr[t++]=x+M*y;}
const circLen=new Int32Array(nC);for(let ci=0;ci<nC;ci++)circLen[ci]=circOff[ci+1]-circOff[ci];
const isDef=new Uint8Array(W);for(const r of DEF_ROWS)isDef[r]=1;
const Y0=DEF_ROWS[0];
const forced=new Int8Array(N),assigned=new Uint8Array(N),rowStone=new Int8Array(W),circStone=new Int8Array(nC);
const trail:number[]=[];
function push0(t:number,i:number,p:number){trail.push(t,i,p);}
function forceEmpty(p:number){if(forced[p]===1)return false;if(forced[p]===2)return true;push0(0,p,0);forced[p]=2;return true;}
function forceStone(p:number){
if(forced[p]===2)return false;if(forced[p]===1)return true;
push0(0,p,0);forced[p]=1;const y=ys[p];push0(1,y,rowStone[y]);rowStone[y]++;
const rc=isDef[y]?DEF_CAP:FULL;if(rowStone[y]>rc)return false;
if(rowStone[y]===rc){for(let o=rowOff[y];o<rowOff[y+1];o++){const q=rowArr[o];if(forced[q]===0){if(!forceEmpty(q))return false;}}}
for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];push0(2,ci,circStone[ci]);circStone[ci]++;if(circStone[ci]>6)return false;
if(circStone[ci]===6){for(let o=circOff[ci];o<circOff[ci+1];o++){const q=circPts[o];if(q!==p&&forced[q]===0){if(!forceEmpty(q))return false;}}}}
return true;}
function undoTo(mark:number){while(trail.length>mark){const prev=trail.pop()!,idx=trail.pop()!,t=trail.pop()!;
if(t===0)forced[idx]=prev;else if(t===1)rowStone[idx]=prev;else if(t===2)circStone[idx]=prev;else assigned[idx]=prev;}}
let nodes=0,witnesses=0,capped=false,leaves=0;const witnessList:number[][][]=[];
function fillRows(row:number){
while(row<W&&isDef[row])row++;
if(row===W){const rows:number[][]=[[],[],[],[],[]];
for(let p=0;p<N;p++)if(forced[p]===1)rows[ys[p]].push(xs[p]);
witnesses++;if(witnessList.length<12)witnessList.push(rows);return false;}
nodes++;if(nodes>NODE_CAP){capped=true;return true;}
const need=FULL-rowStone[row];const unk:number[]=[];
for(let o=rowOff[row];o<rowOff[row+1];o++){const q=rowArr[o];if(forced[q]===0)unk.push(q);}
if(unk.length<need)return false;
return fillComb(row,unk,0,need);}
function fillComb(row:number,unk:number[],start:number,need:number){
if(need===0)return fillRows(row+1);
nodes++;if(nodes>NODE_CAP){capped=true;return true;}
for(let i=start;i<=unk.length-need;i++){const q=unk[i];const mark=trail.length;
if(forceStone(q)){if(fillComb(row,unk,i+1,need-1))return true;}undoTo(mark);if(capped)return true;}
return false;}
function optionsFor(p:number){const opts:number[]=[];
for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];const len=circLen[ci],st=circOff[ci];
if(len===7){let ok=true;for(let o=st;o<st+len;o++){const q=circPts[o];if(q!==p&&forced[q]===2){ok=false;break;}}if(ok)opts.push(ci);}
else{let e0=0;for(let o=st;o<st+len;o++){const q=circPts[o];if(q===p)continue;if(forced[q]===2)e0++;}if(e0<=1)opts.push(ci);}}
return opts;}
function tryBlocker(p:number,ci:number){
const len=circLen[ci],st=circOff[ci];push0(3,p,assigned[p]);assigned[p]=1;
if(!forceEmpty(p))return false;
if(len===7){for(let o=st;o<st+len;o++){const q=circPts[o];if(q!==p){if(!forceStone(q))return false;}}return dfs();}
let e0=0;const unknowns:number[]=[];
for(let o=st;o<st+len;o++){const q=circPts[o];if(q===p)continue;if(forced[q]===2)e0++;else if(forced[q]===0)unknowns.push(q);}
if(e0>=2)return false;
if(e0===1){for(const q of unknowns){if(!forceStone(q))return false;}return dfs();}
for(const q of unknowns){const mark=trail.length;
if(forceEmpty(q)){let ok=true;for(const r of unknowns){if(r!==q&&!forceStone(r)){ok=false;break;}}if(ok){if(dfs())return true;}}
undoTo(mark);if(capped)return true;}
return false;}
function dfs(){
nodes++;if(nodes>NODE_CAP){capped=true;return true;}
let selPt=-1,selOptCount=-1;const selOptArr:number[]=[];let selCanStone=false;
for(let i=0;i<N;i++){if(!isDef[ys[i]])continue;
if(forced[i]===1)continue;
if(forced[i]===2&&assigned[i])continue;
const optArr=optionsFor(i);
const canStone=forced[i]===0&&rowStone[ys[i]]<DEF_CAP;
if(optArr.length===0){if(!canStone)return false;
if(selOptCount===-1||1<selOptCount){selOptCount=1;selPt=i;selCanStone=true;selOptArr.length=0;}
continue;}
const total=canStone?optArr.length+1:optArr.length;
if(selOptCount===-1||total<selOptCount){selOptCount=total;selPt=i;selCanStone=canStone;
selOptArr.length=0;for(const v of optArr)selOptArr.push(v);}
if(selOptCount===1)break;}
if(selPt===-1){leaves++;return fillRows(0);}
const mark0=trail.length;
if(selCanStone){if(forceStone(selPt)){if(dfs())return true;}undoTo(mark0);if(capped)return true;}
for(const ci of selOptArr){const mark=trail.length;if(tryBlocker(selPt,ci))return true;undoTo(mark);if(capped)return true;}
return false;}
function runCase(s0:number[]){const mark=trail.length;let ok=true;
for(const x of s0){if(!forceStone(x+M*Y0)){ok=false;break;}}
if(ok)for(let x=0;x<M;x++)if(!s0.includes(x)){if(!forceEmpty(x+M*Y0)){ok=false;break;}}
if(ok)dfs();undoTo(mark);}
const allCases:number[][]=[];
function gen(k:number){const cur:number[]=[];const rec=(start:number)=>{
if(cur.length===k){allCases.push([...cur]);return;}
for(let x=start;x<M;x++){cur.push(x);rec(x+1);cur.pop();}};rec(0);}
for(let k=5;k>=0;k--)gen(k);
const mir=(s:number[])=>s.map(x=>M-1-x).sort((a,b)=>a-b);
const reps:number[][]=[];
for(const s of allCases){const m0=mir(s);if(s.join(',')<=m0.join(','))reps.push(s);}
let done=0,idx=START;const perK:Record<number,number>={};
let nextIdx=START;let cappedCase=-1;const lastS0s:string[]=[];let maxCaseNodes=0;
while(idx>=0&&idx<reps.length){const before=nodes;
runCase(reps[idx]);
if(!capped){done++;perK[reps[idx].length]=(perK[reps[idx].length]||0)+1;
const cn=nodes-before;if(cn>maxCaseNodes)maxCaseNodes=cn;nextIdx=idx+1;
if(done<=3||done%20===0)lastS0s.push(idx+':'+reps[idx].join(',')+'('+cn+')');idx=nextIdx;}
else{cappedCase=idx;break;}}
function verify(rows:number[][]){const stone=new Uint8Array(N);const rowCnt=new Int32Array(W);
for(let y=0;y<W;y++)for(const x of rows[y]){stone[x+M*y]=1;rowCnt[y]++;}
let safe=true;
for(let ci=0;ci<nC;ci++){let c=0;for(let o=circOff[ci];o<circOff[ci+1];o++)if(stone[circPts[o]])c++;if(c>6)safe=false;}
let maximal=true;
for(let p=0;p<N;p++){if(stone[p])continue;const y=ys[p];let cov=rowCnt[y]===6;
if(!cov)for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];let c=0;for(let o=circOff[ci];o<circOff[ci+1];o++)if(stone[circPts[o]])c++;if(c===6){cov=true;break;}}
if(!cov)maximal=false;}
return{safe,maximal,rowCounts:Array.from(rowCnt)};}
const vres=witnessList.map(w=>({w,v:verify(w)}));
return{nC,repsTotal:reps.length,done,nextIdx,cappedCase,witnesses,leaves,perK,lastS0s,maxCaseNodes,witnessList:vres.slice(0,3).map(({w,v})=>({rows:w,safe:v.safe,maximal:v.maximal,rowCounts:v.rowCounts})),allVerified:vres.every(({v})=>v.safe&&v.maximal)};}
main();
