// Seeded variant of research/experiments/sa-row-deficient-witnesses-20261114/scripts/sa_machine.js.
// Heuristic search only; witness validity is established by the separate exact Python verifier.
'use strict';
const fs = require('fs');
function gcdN(a,b){a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1;}
function isqrt(n){if(n<0)return -1;let r=Math.floor(Math.sqrt(n));while(r*r>n)r--;while((r+1)*(r+1)<=n)r++;return r;}
function buildCurves(w,m,q){
 const N=w*m,px=new Int32Array(N),py=new Int32Array(N);
 for(let y=0;y<w;y++)for(let x=0;x<m;x++){px[x+m*y]=x;py[x+m*y]=y;}
 const lineKeys=new Set();
 for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){
  let dx=px[j]-px[i],dy=py[j]-py[i],g=gcdN(dx,dy);dx/=g;dy/=g;
  if(dy<0||(dy===0&&dx<0)){dx=-dx;dy=-dy;}
  lineKeys.add(dx+','+dy+','+(px[i]*dy-py[i]*dx));
 }
 const curves=[];
 for(const key of lineKeys){const [dx,dy,c]=key.split(',').map(Number),pts=[];
  for(let i=0;i<N;i++)if(px[i]*dy-py[i]*dx===c)pts.push(i);
  if(pts.length>=q)curves.push(Int32Array.from(pts));
 }
 const keptC=new Set();
 for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)for(let k=j+1;k<N;k++){
  const x1=px[i],y1=py[i],x2=px[j],y2=py[j],x3=px[k],y3=py[k];
  const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
  const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
  const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2),uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
  let dd=d,uu=ux,vv=uy,rr=(x1*d-ux)**2+(y1*d-uy)**2;
  const g=gcdN(gcdN(Math.abs(dd),Math.abs(uu)),Math.abs(vv));dd/=g;uu/=g;vv/=g;rr/=(g*g);
  if(dd<0){dd=-dd;uu=-uu;vv=-vv;}
  const key=dd+','+uu+','+vv+','+rr;if(keptC.has(key))continue;
  const pts=[];
  for(let y=0;y<w;y++){
   const dy=y*dd-vv,rem=rr-dy*dy;if(rem<0)continue;
   const r=isqrt(rem);if(r*r!==rem)continue;
   const dxs=r===0?[0]:[r,-r];
   for(const dx of dxs){const num=dx+uu;if(num%dd!==0)continue;const x=num/dd;if(x>=0&&x<m)pts.push(x+m*y);}
  }
  if(pts.length>=q){keptC.add(key);curves.push(Int32Array.from(pts));}
 }
 const pcCount=new Int32Array(N);for(const c of curves)for(const p of c)pcCount[p]++;
 const pcOff=new Int32Array(N+1);for(let p=0;p<N;p++)pcOff[p+1]=pcOff[p]+pcCount[p];
 const pcArr=new Int32Array(pcOff[N]);{const fl=new Int32Array(N);for(let ci=0;ci<curves.length;ci++)for(const p of curves[ci]){pcArr[pcOff[p]+fl[p]]=ci;fl[p]++;}}
 return {N,curves,pcOff,pcArr,nC:curves.length};
}
function makeSearch(Ctx,q,seed0,sampleK=24){
 const {N,curves,pcOff,pcArr}=Ctx,cnt=new Int32Array(curves.length),stone=new Uint8Array(N),unsafe=new Uint8Array(N);
 let seed=seed0>>>0||1;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x80000000;}
 function addStone(p){stone[p]=1;for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;if(cnt[ci]===q-1){const c=curves[ci];for(let t=0;t<c.length;t++)unsafe[c[t]]=1;}}}
 const free=[];
 function maximalize(){free.length=0;for(let p=0;p<N;p++)if(!stone[p]&&!unsafe[p])free.push(p);
  while(free.length){if(free.length===1){addStone(free[0]);free.length=0;break;}
   const k=Math.min(sampleK,free.length);let bestP=-1,bestSc=-1;
   for(let t=0;t<k;t++){const p=free[Math.floor(rnd()*free.length)];let sc=0;for(let oi=pcOff[p];oi<pcOff[p+1];oi++)if(cnt[pcArr[oi]]===q-2)sc++;sc+=rnd()*0.5;if(sc>bestSc){bestSc=sc;bestP=p;}}
   addStone(bestP);let w2=0;for(let t=0;t<free.length;t++){const f=free[t];if(f===bestP)continue;if(!stone[f]&&!unsafe[f])free[w2++]=f;}free.length=w2;
  }
 }
 function rebuild(){cnt.fill(0);unsafe.fill(0);for(let p=0;p<N;p++)if(stone[p])for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;if(cnt[ci]===q-1)for(const t of curves[ci])unsafe[t]=1;}}
 function list(){const a=[];for(let p=0;p<N;p++)if(stone[p])a.push(p);return a;}
 return {rnd,maximalize,rebuild,list,stone};
}
function run(w,m,q,seed,budgetMs,initial){
 const t0=Date.now(),C=buildCurves(w,m,q),tBuild=Date.now()-t0,S=makeSearch(C,q,seed);
 for(const [x,y] of initial)S.stone[x+m*y]=1;
 S.rebuild();S.maximalize();let cur=S.list().length,best=cur,bestList=S.list();
 let T=2.5,iters=0,accepts=0,rejects=0,lastImprove=0;const prev=new Uint8Array(w*m),full=w*(q-1);
 while(Date.now()-t0<budgetMs){iters++;const st=S.list();const rmax=Math.max(2,Math.floor(st.length*0.3));let r=1+Math.floor(S.rnd()*rmax);if(r>st.length)r=st.length;const ids=new Set();while(ids.size<r)ids.add(Math.floor(S.rnd()*st.length));prev.set(S.stone);for(const i of ids)S.stone[st[i]]=0;S.rebuild();S.maximalize();const cand=S.list().length,d=cand-cur;
  if(d<=0||S.rnd()<Math.exp(-d/T)){cur=cand;accepts++;}else{S.stone.set(prev);S.rebuild();cur=S.list().length;rejects++;if(iters-lastImprove>300000){S.stone.fill(0);for(const p of bestList)S.stone[p]=1;S.rebuild();cur=best;lastImprove=iters;}}
  if(cur<best){best=cur;bestList=S.list();lastImprove=iters;console.log(JSON.stringify({event:'improve',best,iters,ms:Date.now()-t0,stones:bestList.map(p=>[p%m,Math.floor(p/m)])}));}
  if(best<full)break;T*=0.99985;if(T<0.02)T=2.5;
 }
 return {w,m,q,curves:C.nC,buildMs:tBuild,iters,accepts,rejects,ms:Date.now()-t0,best,stones:bestList.map(p=>[p%m,Math.floor(p/m)])};
}
const [w,m,q,seed,budget,initialPath,initialKey]=process.argv.slice(2);
if(!w||!m||!q||!seed||!budget||!initialPath){console.error('usage: node search_seeded.js W M Q SEED BUDGET_MS INITIAL_WITNESS_JSON [KEY]');process.exit(2);}
const raw=JSON.parse(fs.readFileSync(initialPath,'utf8'));
const init=Array.isArray(raw)?raw:(raw.stones||(initialKey?raw[initialKey]:null));
if(!Array.isArray(init))throw new Error('initial witness not found');
console.log(JSON.stringify(run(Number(w),Number(m),Number(q),Number(seed),Number(budget),init)));
