#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
const ROOT=process.cwd();
const INPUT="research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json";
const OUTPUT="research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json";
const PIN={blob_sha1:"45744d8255f454eae3e0d59b0e2246df80e98667",sha256:"49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa"};
const need=(ok,msg)=>{if(!ok)throw new Error(msg);};
const bytes=fs.readFileSync(path.join(ROOT,INPUT));
need(createHash("sha256").update(bytes).digest("hex")===PIN.sha256,"input SHA-256 mismatch");
need(createHash("sha1").update(Buffer.concat([Buffer.from("blob "+bytes.length+"\0"),bytes])).digest("hex")===PIN.blob_sha1,"input blob SHA-1 mismatch");
const roots=JSON.parse(bytes.toString("utf8")).witness_full,N=121,ALL=(1n<<121n)-1n,BIT=Array.from({length:N},(_,i)=>1n<<BigInt(i));
const ROW=Array.from({length:N},(_,i)=>{const x=BigInt(i%11),y=BigInt(Math.floor(i/11));return [x*x+y*y,x,y];});
function detC(a,b,c,q){const A=ROW[a],B=ROW[b],C=ROW[c],Q=ROW[q],u0=B[0]-A[0],u1=B[1]-A[1],u2=B[2]-A[2],v0=C[0]-A[0],v1=C[1]-A[1],v2=C[2]-A[2],w0=Q[0]-A[0],w1=Q[1]-A[1],w2=Q[2]-A[2];return u0*(v1*w2-v2*w1)-u1*(v0*w2-v2*w0)+u2*(v0*w1-v1*w0);}
function detL(a,b,c,q){const A=ROW[a],B=ROW[b],C=ROW[c],Q=ROW[q],u0=B[0]-A[0],u1=B[1]-A[1],u2=B[2]-A[2],v0=C[0]-A[0],v1=C[1]-A[1],v2=C[2]-A[2],w0=Q[0]-A[0],w1=Q[1]-A[1],w2=Q[2]-A[2];return u0*v1*w2+u1*v2*w0+u2*v0*w1-u2*v1*w0-u1*v0*w2-u0*v2*w1;}
const memo=new Map();let pointChecks=0;
function triple(a,b,c){const s=[a,b,c].sort((x,y)=>x-y),k=(s[0]*N+s[1])*N+s[2];if(memo.has(k))return memo.get(k);let m=0n;for(let q=0;q<N;q++){const x=detC(s[0],s[1],s[2],q),y=detL(s[0],s[1],s[2],q);pointChecks++;need(x===y,"determinant mismatch");if(x===0n)m|=BIT[q];}memo.set(k,m);return m;}
const T=[];for(let s=0;s<2;s++)for(let fx=0;fx<2;fx++)for(let fy=0;fy<2;fy++){const a=[];for(let i=0;i<N;i++){const x=i%11,y=Math.floor(i/11);let u=s?y:x,v=s?x:y;if(fx)u=10-u;if(fy)v=10-v;a[i]=u+11*v;}T.push(a);}
function bits(m){const a=[];for(let i=0;i<N;i++)if(m&BIT[i])a.push(i);return a;}
function canon(st){let best=null;for(const t of T){let m=0n;for(const p of st)m|=BIT[t[p]];if(best===null||m<best)best=m;}return best.toString(16).padStart(32,"0");}
function pairMask(st,p){let m=0n;for(let a=0;a<st.length;a++)for(let b=a+1;b<st.length;b++)m|=triple(st[a],st[b],p);return m;}
function pop(m){let n=0;while(m){m&=m-1n;n++;}return n;}
const owners=new Map(),pairCounts=Array.from({length:roots.length},()=>new Uint32Array(roots.length)),per=[];
let total9=0,totalRaw10=0,totalD4=0,withinAll=0,terminal9=0,rootQuads=0;
for(let i=0;i<roots.length;i++){
 const item=roots[i],root=BigInt("0x"+item.root),st=bits(root);
 need(item.safe===true&&st.length===7&&canon(st)===item.root,"root identity/safety failure");
 for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)for(let d=c+1;d<7;d++){const x=detC(st[a],st[b],st[c],st[d]),y=detL(st[a],st[b],st[c],st[d]);rootQuads++;need(x===y&&x!==0n,"unsafe root quadruple");}
 let base=0n;for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)base|=triple(st[a],st[b],st[c]);
 const first=bits(ALL&~(base|root));let n9=0,raw=0,d4=0,within=0,third=0,terms=0,min3=999,max3=-1;
 for(const p of first){const ep=pairMask(st,p),occ8=root|BIT[p],st8=st.concat(p),legal8=ALL&~(base|ep|occ8);
  for(const q of first){if(q<=p||!(legal8&BIT[q]))continue;n9++;const eq=pairMask(st8,q),occ9=occ8|BIT[q],replies=ALL&~(base|ep|eq|occ9),n=pop(replies);third+=n;if(n===0)terms++;min3=Math.min(min3,n);max3=Math.max(max3,n);
   for(let r=q+1;r<N;r++)if(replies&BIT[r]){raw++;totalRaw10++;const key=canon(st8.concat(q,r)),old=owners.get(key),own=1n<<BigInt(i);if(old===undefined){owners.set(key,own);d4++;}else if(old&own)within++;else{for(let j=0;j<i;j++)if(old&(1n<<BigInt(j)))pairCounts[j][i]++;owners.set(key,old|own);d4++;}}
  }
 }
 need(third===3*raw&&raw-d4===within,"frontier accounting failure");
 per.push({rank:i+1,root:item.root,rows:item.rows,worker:i%4,first:first.length,n9,third,raw10:raw,d4,within,terminal9:terms,min3,max3});
 total9+=n9;totalD4+=d4;withinAll+=within;terminal9+=terms;
}
const multiplicity={};let duplicateMemberships=0,maxMultiplicity=0;
for(const m of owners.values()){const n=pop(m);multiplicity[n]=(multiplicity[n]||0)+1;if(n>1)duplicateMemberships+=n-1;maxMultiplicity=Math.max(maxMultiplicity,n);}
const overlaps=[];let sameWorker=0,crossWorker=0,pairwiseTotal=0;
for(let i=0;i<roots.length;i++)for(let j=i+1;j<roots.length;j++){const n=pairCounts[i][j];if(n){overlaps.push({a:roots[i].root,b:roots[j].root,shared:n,workerA:i%4,workerB:j%4});pairwiseTotal+=n;if(i%4===j%4)sameWorker+=n;else crossWorker+=n;}}
overlaps.sort((a,b)=>b.shared-a.shared||a.a.localeCompare(b.a)||a.b.localeCompare(b.b));
const workerStats=Array.from({length:4},(_,w)=>{const a=per.filter(x=>x.worker===w);return {worker:w,roots:a.length,n9:a.reduce((s,x)=>s+x.n9,0),raw10:a.reduce((s,x)=>s+x.raw10,0),d4:a.reduce((s,x)=>s+x.d4,0),within:a.reduce((s,x)=>s+x.within,0)};});
const checks=[["36 roots",per.length===36&&rootQuads===1260],["determinant expansions",pointChecks===memo.size*121],["9-stone total",total9===56597],["raw 10-stone total",totalRaw10===733855],["D4 membership total",totalD4===733800],["within-root merges",withinAll===55],["global D4 classes",owners.size===728370],["cross-root duplicates",duplicateMemberships===5430],["worker split",workerStats.every(x=>x.roots===9)],["third move identity",per.every(x=>x.third===3*x.raw10)],["multiplicity",maxMultiplicity===3],["terminal count",terminal9===0]];
need(checks.every(x=>x[1]),"final gate failure");
const result={schema:"n11-residual72-36root-three-ply-overlap-census-20261120-v1",date:"2026-11-20",status:"exact-three-ply-geometric-frontier-census",source:{main_commit:"b8eec25ccc69192d0e9dd4edbe5b1b4b6ce8d82a",path:INPUT,git_blob_sha1:PIN.blob_sha1,sha256:PIN.sha256},method:{board:"11x11",d4:8,determinant:"exact BigInt determinant [x^2+y^2,x,y,1]",expansions:["cofactor","Leibniz"],root_quads:rootQuads,unique_triples:memo.size,point_checks:pointChecks,worker_partition:"roots[W::4]"},summary:{roots:36,first_moves_min:Math.min(...per.map(x=>x.first)),first_moves_max:Math.max(...per.map(x=>x.first)),unique_9stone_positions:total9,all_legal_third_moves:per.reduce((s,x)=>s+x.third,0),raw_10stone_positions:totalRaw10,per_root_d4_memberships:totalD4,within_root_d4_merges:withinAll,global_unique_d4_classes:owners.size,cross_root_duplicate_memberships:duplicateMemberships,cross_root_duplicate_rate_percent:Number((100*duplicateMemberships/totalD4).toFixed(6)),pairwise_overlap_total:pairwiseTotal,overlapping_root_pairs:overlaps.length,multiplicity_histogram:multiplicity,max_root_multiplicity:maxMultiplicity,terminal_9stone_positions:terminal9,min_legal_third_moves:Math.min(...per.map(x=>x.min3)),max_legal_third_moves:Math.max(...per.map(x=>x.max3)),same_worker_pairwise_overlap:sameWorker,cross_worker_pairwise_overlap:crossWorker,cross_worker_share_percent:Number((100*crossWorker/(sameWorker+crossWorker)).toFixed(6))},worker_stats:workerStats,per_root:per,pairwise_overlap:overlaps,checks:checks.map(([name,pass])=>({name,pass})),check_count:checks.length,all_pass:true,interpretation_guard:["Geometric only, not DFPN cost or TT hit rate.","Shared D4 class does not imply an actual TT hit.","REFUTED-D10 is not a LOSS proof.","36 roots are candidates, not WIN certificates."]};
const out=JSON.stringify(result,null,2)+"\n";
fs.mkdirSync(path.dirname(path.join(ROOT,OUTPUT)),{recursive:true});
fs.writeFileSync(path.join(ROOT,OUTPUT),out);
process.stdout.write(JSON.stringify({summary:result.summary,checks:result.checks})+"\n");
