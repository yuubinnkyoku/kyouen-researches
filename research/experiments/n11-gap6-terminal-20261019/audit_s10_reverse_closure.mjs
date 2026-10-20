#!/usr/bin/env node
// Exact reverse closure from canonical S10 LOSS verdicts to S8 LOSS,
// with an independent integer-determinant legal-move check.
// Usage: node audit_s10_reverse_closure.mjs S10.tsv S8_LOSS.txt S8_WIN.txt
import fs from 'node:fs';
import crypto from 'node:crypto';

if (process.argv.length !== 5) {
  console.error('usage: node audit_s10_reverse_closure.mjs s10.tsv s8_loss.txt s8_win.txt');
  process.exit(2);
}
const [cachePath, lossPath, winPath] = process.argv.slice(2);
const raw = fs.readFileSync(cachePath, 'utf8');
const cacheSha256 = crypto.createHash('sha256').update(raw).digest('hex');
const hex = m => m.toString(16).padStart(32, '0');
const bit = Array.from({length:121},(_,i)=>1n<<BigInt(i));
const full = (1n<<121n)-1n;
const xyz = Array.from({length:121},(_,i)=>{const x=i%11,y=Math.floor(i/11);return [x,y,x*x+y*y]});
const maps = Array.from({length:8},(_,t)=>Array.from({length:121},(_,i)=>{
  const x=i%11,y=Math.floor(i/11);
  const [xx,yy]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],[10-x,y],[10-y,10-x],[x,10-y],[y,x]][t];
  return 1n<<BigInt(yy*11+xx);
}));
function points(m){const p=[];for(let i=0;i<121;i++)if(m&bit[i])p.push(i);return p}
function canonical(m){const ps=points(m);let best=null;for(let t=0;t<8;t++){
  let v=0n;for(const p of ps)v|=maps[t][p];if(best===null||v<best)best=v;
}return hex(best)}
function parents(m){const ps=points(m), transforms=maps.map(a=>ps.reduce((v,p)=>v|a[p],0n));
  const out=new Set();for(const p of ps){let best=null;for(let t=0;t<8;t++){
    const v=transforms[t]^maps[t][p];if(best===null||v<best)best=v;
  }out.add(hex(best))}return out;
}
function circle(a,b,c,d){
  const A=xyz[a],B=xyz[b],C=xyz[c],D=xyz[d];
  const ux=A[0]-D[0],uy=A[1]-D[1],uz=A[2]-D[2];
  const vx=B[0]-D[0],vy=B[1]-D[1],vz=B[2]-D[2];
  const wx=C[0]-D[0],wy=C[1]-D[1],wz=C[2]-D[2];
  return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)===0;
}
function safe(m){const p=points(m);for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)
 for(let k=j+1;k<p.length;k++)for(let l=k+1;l<p.length;l++)if(circle(p[i],p[j],p[k],p[l]))return false;
 return true;
}
const badMemo=new Map();
function forbiddenByTriple(a,b,c){const key=(a*121+b)*121+c;let r=badMemo.get(key);if(r!==undefined)return r;
 r=0n;for(let d=0;d<121;d++)if(d!==a&&d!==b&&d!==c&&circle(a,b,c,d))r|=bit[d];
 badMemo.set(key,r);return r;
}
function legalBits(m){const ps=points(m);let banned=m;
 for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++)for(let k=j+1;k<ps.length;k++)
   banned|=forbiddenByTriple(ps[i],ps[j],ps[k]);
 return full&~banned;
}
function countBits(m){let n=0;while(m){m&=m-1n;n++}return n}
function loadSet(path){return new Set(fs.readFileSync(path,'utf8').trim().split(/\s+/).filter(Boolean))}
const knownLoss=loadSet(lossPath),knownWin=loadSet(winPath);
for(const p of knownLoss)if(knownWin.has(p))throw Error('S8 WIN/LOSS conflict '+p);
const cache=new Map();for(const line of raw.trim().split(/\r?\n/)){
 const a=line.trim().split(/\s+/);if(a.length<2||!['WIN','LOSS'].includes(a[1])||!/^[0-9a-f]{32}$/.test(a[0]))throw Error('bad cache row '+line);
 if(cache.has(a[0])&&cache.get(a[0])!==a[1])throw Error('S10 WIN/LOSS conflict '+a[0]);
 if(cache.has(a[0]))throw Error('duplicate S10 '+a[0]);cache.set(a[0],a[1]);
}
const loss10=[...cache].filter(([,v])=>v==='LOSS').map(([p])=>BigInt('0x'+p));
for(const m of loss10){if(countBits(m)!==10||canonical(m)!==hex(m)||!safe(m))throw Error('unsafe/noncanonical S10 LOSS '+hex(m))}
const win9=new Set();for(const m of loss10)for(const p of parents(m))win9.add(p);
const coverage=new Map();for(const h of win9)for(const p of parents(BigInt('0x'+h)))coverage.set(p,(coverage.get(p)||0)+1);
const hist={},unknownNear=[],closed=[],minLegal={count:121,position:null};
for(const [h,n] of coverage){const m=BigInt('0x'+h),lb=legalBits(m),total=countBits(lb),missing=total-n;
 if(missing<0)throw Error('coverage exceeds legal children '+h);
 if(total<minLegal.count){minLegal.count=total;minLegal.position=h}
 const kind=knownLoss.has(h)?'LOSS':knownWin.has(h)?'WIN':'UNKNOWN';
 if(missing<=8){hist[missing]??={LOSS:0,WIN:0,UNKNOWN:0};hist[missing][kind]++;
  if(kind==='UNKNOWN')unknownNear.push([h,missing,n,total]);}
 if(missing===0){
  // Independent positive coverage check: every legal S9 child is actually in win9.
  for(let p=0;p<121;p++)if(lb&bit[p])if(!win9.has(canonical(m|bit[p])))throw Error('false closure '+h);
  if(kind==='WIN')throw Error('S8 WIN/LOSS conflict '+h);
  closed.push(h);
 }
}
unknownNear.sort((a,b)=>a[1]-b[1]||b[2]-a[2]||a[0].localeCompare(b[0]));
const closedSet=new Set(closed);
const result={format:'n11-s10-reverse-closure-audit-v1',cache_sha256:cacheSha256,
 s10_total:cache.size,s10_loss:loss10.length,s9_win:win9.size,s8_candidates:coverage.size,
 min_s8_legal:minLegal,near_miss_histogram:hist,closed_s8:closed.length,
 closed_known_loss:closed.filter(h=>knownLoss.has(h)).length,
 closed_unknown:closed.filter(h=>!knownLoss.has(h)),
 known_loss_not_closed:[...knownLoss].filter(h=>!closedSet.has(h)).sort(),
 unknown_near_misses:unknownNear,forbidden_triple_cache_size:badMemo.size};
console.log(JSON.stringify(result,null,2));
