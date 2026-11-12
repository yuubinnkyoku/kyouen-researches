// six_row_one_deficient_runner.ts — 6×m (W=6, q=7) 1行欠損クラス機械
// multi_deficient_runner.ts (5×19, K0747-K0759) の幅6移植版。
// 危険曲線 = 行直線（6石でblock）+ census円（≥7格子点, ≤6石で安全）のみ。
// 非水平直線は6行と≤6点で交わるため7点直線は存在しない（証明）。
// censusはchord法（K0760制御2で6×13の3点外心brute-forceと完全一致済み）。
//
// 本セッション (2026-11-12, q108高速レーン) の実行結果（すべて厳密整数演算）:
//   6×13  DEF_ROWS=[0] S0={0,1,2,3,4}: witnesses >1,006,128（600k node capまで）、
//         sampled 12件すべて verify safe+maximal, rowCounts (5,6,6,6,6,6)。
//   6×16  同S0: 28ノードでwitness 3件・全verify PASS。
//   6×19  同S0: 203,446ノード完走・witness 3件・全verify PASS。
//         最初のwitness rows = [[0,1,2,3,4],[3,9,12,13,14,16],[7,8,13,14,16,17],
//         [1,7,8,10,14,15],[6,8,10,12,13,15],[0,2,7,8,13,15]]（35石）。
//         census不使用の独立検証（石3つ組外心列挙）: 最悪円石数6・未block空点0。
//   6×20  同S0: 300k cap で capped・witness 0（未完・open）。
//   6×22  S0={0,5,10,15,20}: 249,271ノード完走・witness 0（この1代表のみの不在）。
//         同S0={0,1,2,3,4}: 300k cap で capped（open）。
//   ランダムサンプリング (5,6,6,6,6,6) 20k件: m=19..28 で safe 約79-97% だが
//         maximal-safe 0件（m=19でも0 — witnessが存在するのに）。
//         → サンプリングはこのクラスの不在証明に使えない（log参照）。
//
// 実行手順: RUNS を1エントリに絞って run_typescript で単独実行する
// （census再構築 + 300k-600k nodes が sandbox 1回の上限。600k+大きいcensusは
//  process safety deadline 超過。m=19以下のcensus+300k は安定）。
function gcd(a:number,b:number){a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1;}
function censusChordB(H:number,m:number){const kept=new Map<string,any>();const buckets:number[][][][]=[];
for(let y=0;y<H;y++){const bs:number[][][]=Array.from({length:2*m},()=>[]);
for(let a=0;a<m-1;a++)for(let b=a+1;b<m;b++)bs[a+b].push([a,b]);buckets.push(bs);}
for(let y1=0;y1<H-1;y1++)for(let y2=y1+1;y2<H;y2++){const D=y1-y2;
for(let s=1;s<2*m;s++){for(const p1 of buckets[y1][s])for(const p2 of buckets[y2][s]){
const W1=p1[1]-p1[0],W2=p2[1]-p2[0];const num=W2*W2-W1*W1,den=4*D;
const cyN=y1*2*den-(num+D*den),cyD=2*den;const uN=y1*cyD-cyN;const r2N=4*uN*uN+W1*W1*cyD*cyD;
let dd=2*cyD,ux=s*cyD,uy=2*cyN,nr2=r2N;
const g=gcd(gcd(Math.abs(dd),Math.abs(ux)),Math.abs(uy));dd/=g;ux/=g;uy/=g;nr2/=g*g;
if(dd<0){dd=-dd;ux=-ux;uy=-uy;}
const key=dd+','+ux+','+uy+','+nr2;if(kept.has(key))continue;
const list:number[]=[];for(let y=0;y<H;y++){const dy=y*dd-uy;for(let x=0;x<m;x++){const dx=x*dd-ux;if(dx*dx+dy*dy===nr2)list.push(x,y);}}
if(list.length/2>=7)kept.set(key,{size:list.length/2,pts:list});}}}
return [...kept.values()];}
function buildCensus(W:number,M:number){
const circles=censusChordB(W,M);const nC=circles.length;
const tmpOff:number[]=[0];const tmpPts:number[]=[];
for(const c of circles){for(let i=0;i<c.pts.length;i+=2)tmpPts.push(c.pts[i]+M*c.pts[i+1]);tmpOff.push(tmpPts.length);}
return {nC,circOff:Int32Array.from(tmpOff),circPts:Int32Array.from(tmpPts)};
}
// 1つの S0（欠損行Y0の石集合）に対する DFS。stopAtWitnesses 件見つけたら早期終了。
function probe(M:number, S0:number[], cap:number, stopAtWitnesses:number, keepWitnesses:number){
const W=6,DEF_CAP=5,FULL=6,Y0=0;
const N=W*M,xs=new Int32Array(N),ys=new Int32Array(N);
for(let y=0;y<W;y++)for(let x=0;x<M;x++){xs[x+M*y]=x;ys[x+M*y]=y;}
const cen=buildCensus(W,M);const nC=cen.nC,circOff=cen.circOff,circPts=cen.circPts;
const pcCount=new Int32Array(N);
for(let ci=0;ci<nC;ci++)for(let o=circOff[ci];o<circOff[ci+1];o++)pcCount[circPts[o]]++;
const pcOff=new Int32Array(N+1);for(let p=0;p<N;p++)pcOff[p+1]=pcOff[p]+pcCount[p];
const pcArr=new Int32Array(pcOff[N]);const fl=new Int32Array(N);fl.fill(0);
for(let ci=0;ci<nC;ci++)for(let o=circOff[ci];o<circOff[ci+1];o++){const p=circPts[o];pcArr[pcOff[p]+fl[p]]=ci;fl[p]++;}
const rowOff=new Int32Array(W+1);for(let y=0;y<W;y++)rowOff[y+1]=rowOff[y]+M;
const rowArr=new Int32Array(N);{let t=0;for(let y=0;y<W;y++)for(let x=0;x<M;x++)rowArr[t++]=x+M*y;}
const circLen=new Int32Array(nC);for(let ci=0;ci<nC;ci++)circLen[ci]=circOff[ci+1]-circOff[ci];
const isDef=new Uint8Array(W);isDef[Y0]=1;
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
if(row===W){const rows:number[][]=Array.from({length:W},()=>[]);
for(let p=0;p<N;p++)if(forced[p]===1)rows[ys[p]].push(xs[p]);
witnesses++;if(witnessList.length<keepWitnesses)witnessList.push(rows);
if(witnesses>=stopAtWitnesses)return true;return false;}
nodes++;if(nodes>cap){capped=true;return true;}
const need=FULL-rowStone[row];const unk:number[]=[];
for(let o=rowOff[row];o<rowOff[row+1];o++){const q=rowArr[o];if(forced[q]===0)unk.push(q);}
if(unk.length<need)return false;
return fillComb(row,unk,0,need);}
function fillComb(row:number,unk:number[],start:number,need:number){
if(need===0)return fillRows(row+1);
nodes++;if(nodes>cap){capped=true;return true;}
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
nodes++;if(nodes>cap){capped=true;return true;}
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
// census依存の verify（安全性=census円石数≤6・極大性=空点のblock検査）
function verify(rows:number[][]){const stone=new Uint8Array(N);const rowCnt=new Int32Array(W);
for(let y=0;y<W;y++)for(const x of rows[y]){stone[x+M*y]=1;rowCnt[y]++;}
let safe=true;
for(let ci=0;ci<nC;ci++){let c=0;for(let o=circOff[ci];o<circOff[ci+1];o++)if(stone[circPts[o]])c++;if(c>6)safe=false;}
let maximal=true;
for(let p=0;p<N;p++){if(stone[p])continue;const y=ys[p];let cov=rowCnt[y]===6;
if(!cov)for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];let c=0;for(let o=circOff[ci];o<circOff[ci+1];o++)if(stone[circPts[o]])c++;if(c===6){cov=true;break;}}
if(!cov)maximal=false;}
return{safe,maximal,rowCounts:Array.from(rowCnt)};}
const mark=trail.length;let ok=true;
for(const x of S0){if(!forceStone(x+M*Y0)){ok=false;break;}}
if(ok)for(let x=0;x<M;x++)if(!S0.includes(x)){if(!forceEmpty(x+M*Y0)){ok=false;break;}}
if(ok)dfs();undoTo(mark);
const vw=witnessList.map(w=>({rows:w,v:verify(w)}));
return {M,S0,nC,nodes,witnesses,leaves,capped,found:vw.length>0,allVerified:vw.every(x=>x.v.safe&&x.v.maximal),witnessesDetail:vw};}
// census不使用の独立検証（石3つ組外心列挙。7石以上の円は必ず石3つ組を含む）。
function verifyIndependent(M:number, rows:number[][]){
const W=6;const stones:number[]=[];
for(let y=0;y<W;y++)for(const x of rows[y])stones.push(x,y);
const n=stones.length/2;let worst=0;const seen=new Set<string>();
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++){
const x1=stones[2*i],y1=stones[2*i+1],x2=stones[2*j],y2=stones[2*j+1],x3=stones[2*k],y3=stones[2*k+1];
const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2),uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
const key=ux+','+uy+','+d;if(seen.has(key))continue;seen.add(key);
let cnt=0;
for(let idx=0;idx<n;idx++){const dx=stones[2*idx]*d-ux,dy=stones[2*idx+1]*d-uy;const vx=x1*d-ux,vy=y1*d-uy;if(dx*dx+dy*dy===vx*vx+vy*vy)cnt++;}
if(cnt>worst)worst=cnt;}
// 未block空点: 行1-5は6石行直線でblock。行0の空点は「ちょうど6石の石3つ組円」でblock
const stone=new Uint8Array(W*M);for(let y=0;y<W;y++)for(const x of rows[y])stone[x+M*y]=1;
const unblocked:number[]=[];
for(let x=0;x<M;x++){if(stone[x])continue;let cov=false;
for(let i=0;i<n&&!cov;i++)for(let j=i+1;j<n&&!cov;j++)for(let k=j+1;k<n&&!cov;k++){
const x1=stones[2*i],y1=stones[2*i+1],x2=stones[2*j],y2=stones[2*j+1],x3=stones[2*k],y3=stones[2*k+1];
const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2),uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
const px=x*d-ux,py=0*d-uy,qx=x1*d-ux,qy=y1*d-uy;
if(px*px+py*py===qx*qx+qy*qy){let c=0;
for(let idx=0;idx<n;idx++){const dx=stones[2*idx]*d-ux,dy=stones[2*idx+1]*d-uy;if(dx*dx+dy*dy===qx*qx+qy*qy)c++;}
if(c===6)cov=true;}}
if(!cov)unblocked.push(x);}
return {stones:n,worstCircleStones:worst,unblockedCount:unblocked.length};}
async function main(){
// 1実行1エントリ（sandbox上限）。再現する場合は順に書き換えて実行する。
const RUNS:[number,number[],number,number,number][]=[
  // [M, S0, NODE_CAP, STOP_AT_WITNESSES, KEEP]
  [19,[0,1,2,3,4],600000,3,3],
];
const out:any[]=[];
for(const [M,S0,cap,stop,keep] of RUNS){
const r=await probe(M,S0,cap,stop,keep);
if(r.found&&r.witnessesDetail[0]){
r.independent=verifyIndependent(M,r.witnessesDetail[0].rows);}
out.push(r);}
return JSON.stringify(out);
}
