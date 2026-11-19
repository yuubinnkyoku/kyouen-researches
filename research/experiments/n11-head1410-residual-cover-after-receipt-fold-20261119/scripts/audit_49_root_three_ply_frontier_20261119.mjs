#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {createHash} from "node:crypto";
import {fileURLToPath} from "node:url";
import {gzipSync} from "node:zlib";
const ROOT=process.cwd(),SCRIPT_FILE=fileURLToPath(import.meta.url);
const SCRIPT_PATH=path.relative(ROOT,SCRIPT_FILE).replaceAll("\\","/");
const MP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json";
const RP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json";
const TP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-two-ply-frontier-20261119.json";
const KP="research/knowledge/items/K0001-complete-call-rules.md";
const CP="research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md";
const OP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-three-ply-frontier-20261119.json.gz";
const OUT=path.join(ROOT,OP);
const MAIN="fa9a985e380fa2ac9037a31971d2e52b5f7abe91";
const PIN={
 mobility:"b35d54a0ced182153802247452a593096a0acf81",
 residual:"a8eaf00bd6494eda50a68e7d06498bed833a7688",
 two_ply:"f631574b5701bd8f441d2c552ba001814246ef69",
 rules:"ef7483e011d72e0048d667313b6c996d3472729f",
 convention:"b097210d0b49d7cf014cc6a554298b1e49e83384"
};
function need(x,s){if(!x)throw Error(s);}
function blobSha(s){const b=Buffer.from(s,"utf8");return createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");}
function read(p,pin){const s=fs.readFileSync(path.join(ROOT,p),"utf8");need(blobSha(s)===pin,"blob SHA-1 mismatch: "+p);return s;}
function bits(m){const a=[];for(let i=0;i<121;i++)if((m>>BigInt(i))&1n)a.push(i);return a;}
const ROW=Array.from({length:121},(_,i)=>{const x=BigInt(i%11),y=BigInt(Math.floor(i/11));return [x*x+y*y,x,y];});
function detC(a,b,c,q){
 const A=ROW[a],B=ROW[b],C=ROW[c],Q=ROW[q];
 const u0=B[0]-A[0],u1=B[1]-A[1],u2=B[2]-A[2];
 const v0=C[0]-A[0],v1=C[1]-A[1],v2=C[2]-A[2];
 const w0=Q[0]-A[0],w1=Q[1]-A[1],w2=Q[2]-A[2];
 return u0*(v1*w2-v2*w1)-u1*(v0*w2-v2*w0)+u2*(v0*w1-v1*w0);
}
function detL(a,b,c,q){
 const A=ROW[a],B=ROW[b],C=ROW[c],Q=ROW[q];
 const u0=B[0]-A[0],u1=B[1]-A[1],u2=B[2]-A[2];
 const v0=C[0]-A[0],v1=C[1]-A[1],v2=C[2]-A[2];
 const w0=Q[0]-A[0],w1=Q[1]-A[1],w2=Q[2]-A[2];
 return u0*v1*w2+u1*v2*w0+u2*v0*w1-u2*v1*w0-u1*v0*w2-u0*v2*w1;
}
const tripleMasks=new Map();
let determinantPointChecks=0;
function tm(a,b,c){
 const s=[a,b,c].sort((x,y)=>x-y),key=(s[0]*121+s[1])*121+s[2];
 if(tripleMasks.has(key))return tripleMasks.get(key);
 let mask=0n;
 for(let q=0;q<121;q++){
  const x=detC(s[0],s[1],s[2],q),y=detL(s[0],s[1],s[2],q);
  determinantPointChecks++;
  need(x===y,"independent determinant expansions disagree");
  if(x===0n)mask|=1n<<BigInt(q);
 }
 tripleMasks.set(key,mask);
 return mask;
}
function pop(m){let n=0;while(m){m&=m-1n;n++;}return n;}
const BIT=Array.from({length:121},(_,i)=>1n<<BigInt(i));
const ALL=(1n<<121n)-1n;
const TRANS=[];
for(let s=0;s<2;s++)for(let fx=0;fx<2;fx++)for(let fy=0;fy<2;fy++){
 const map=[];
 for(let i=0;i<121;i++){
  const x=i%11,y=Math.floor(i/11);let a=s?y:x,b=s?x:y;
  if(fx)a=10-a;if(fy)b=10-b;
  map[i]=a+11*b;
 }
 TRANS.push(map);
}
function canonStones(stones){
 let best=null;
 for(const t of TRANS){
  let m=0n;for(const p of stones)m|=BIT[t[p]];
  if(best===null||m<best)best=m;
 }
 return best;
}
function pairMask(stones,p){
 let m=0n;
 for(let a=0;a<stones.length;a++)for(let b=a+1;b<stones.length;b++)m|=tm(stones[a],stones[b],p);
 return m;
}
const mobility=JSON.parse(read(MP,PIN.mobility));
const residual=JSON.parse(read(RP,PIN.residual));
const twoPly=JSON.parse(read(TP,PIN.two_ply));
const rules=read(KP,PIN.rules),convention=read(CP,PIN.convention);
need(rules.includes("同一円または同一直線上")&&rules.includes("行列式"),"rule text mismatch");
need(convention.includes("det4")&&convention.includes("共線"),"candidate convention mismatch");
need(mobility.mobility.priority_order.length===49,"candidate count");
const witness=new Map(residual.witness.map(x=>[x.root,x.rows]));
const prior=new Map(twoPly.per_root.map(x=>[x.root,x]));
const owners=new Map();
const pairCounts=Array.from({length:49},()=>new Uint32Array(49));
const per=[];
let total9=0,totalRaw10=0,totalD4Memberships=0,terminal9=0,totalWithinRootMerges=0,rootSafetyQuadruples=0;
let minThird=999,maxThird=-1;
const started=Date.now();
for(let i=0;i<mobility.mobility.priority_order.length;i++){
 const item=mobility.mobility.priority_order[i],root=BigInt("0x"+item.root),st=bits(root);
 need(st.length===7,"root stone count");
 need(canonStones(st)===root,"root not D4 canonical");
 const rows=witness.get(item.root);need(rows&&(rows.length===1||rows.length===2),"root witness rows");
 for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)for(let d=c+1;d<7;d++){
  const x=detC(st[a],st[b],st[c],st[d]),y=detL(st[a],st[b],st[c],st[d]);
  need(x===y&&x!==0n,"unsafe 7-stone root");rootSafetyQuadruples++;
 }
 let base=0n;
 for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)base|=tm(st[a],st[b],st[c]);
 const first=[];
 for(let p=0;p<121;p++)if(!(root&BIT[p])&&!(base&BIT[p]))first.push(p);
 need(first.length===item.legal_next_moves,"first-move count mismatch");
 need(first.join(",")===item.legal_bits.join(","),"first-move set mismatch");
 let nine=0,rawTen=0,d4Ten=0,withinMerges=0,thirdAll=0,term=0,lo=999,hi=-1;
 for(const p of first){
  const extraP=pairMask(st,p),occ8=root|BIT[p],st8=st.concat(p),forbid8=base|extraP;
  const legal8=ALL&~(forbid8|occ8);
  for(const q of first){
   if(q<=p||!(legal8&BIT[q]))continue;
   nine++;
   const extraQ=pairMask(st8,q),occ9=occ8|BIT[q];
   const replies=ALL&~(base|extraP|extraQ|occ9);
   const n=pop(replies);thirdAll+=n;
   if(n===0)term++;
   if(n<lo)lo=n;if(n>hi)hi=n;
   for(let r=q+1;r<121;r++){
    if(!(replies&BIT[r]))continue;
    rawTen++;totalRaw10++;
    const key=canonStones(st8.concat(q,r));
    const own=1n<<BigInt(i),old=owners.get(key);
    if(old===undefined){owners.set(key,own);d4Ten++;}
    else if(old&own){withinMerges++;}
    else{
     for(let j=0;j<i;j++)if(old&(1n<<BigInt(j)))pairCounts[j][i]++;
     owners.set(key,old|own);d4Ten++;
    }
   }
  }
 }
 const priorRoot=prior.get(item.root);
 need(priorRoot&&priorRoot.unique_9stone_positions===nine,"two-ply 9-stone crosscheck mismatch");
 need(thirdAll===3*rawTen,"three-order identity mismatch");
 need(rawTen-d4Ten===withinMerges,"within-root D4 merge accounting mismatch");
 need(nine===priorRoot.unique_9stone_positions,"9-stone count mismatch");
 const rec={input_first_ply_rank:i+1,root:item.root,covered_rows:rows,first_moves:first.length,unique_9stone_positions:nine,all_legal_third_moves:thirdAll,raw_10stone_positions:rawTen,d4_10stone_classes:d4Ten,within_root_d4_merges:withinMerges,min_legal_third_moves:lo,max_legal_third_moves:hi,terminal_9stone_positions:term};
 per.push(rec);total9+=nine;totalD4Memberships+=d4Ten;totalWithinRootMerges+=withinMerges;terminal9+=term;
 if(lo<minThird)minThird=lo;if(hi>maxThird)maxThird=hi;
 console.log(JSON.stringify({root:i+1,unique9:nine,raw10:rawTen,d4Classes:d4Ten,withinRootMerges:withinMerges,thirdAll:thirdAll,uniqueTripleMasks:tripleMasks.size,global10Classes:owners.size,elapsedSeconds:Math.round((Date.now()-started)/1000)}));
}
const coverage={};for(const x of per)coverage[x.covered_rows.length]=(coverage[x.covered_rows.length]||0)+1;
const mult={};let memberships=0,shared=0,maxMultiplicity=0;
for(const mask of owners.values()){const n=pop(mask);mult[n]=(mult[n]||0)+1;if(n>1)shared+=n-1;if(n>maxMultiplicity)maxMultiplicity=n;memberships+=n;}
const pairs=[];
for(let a=0;a<49;a++)for(let b=a+1;b<49;b++)if(pairCounts[a][b]){
 pairs.push({roots:[per[a].root,per[b].root],rows:[per[a].covered_rows,per[b].covered_rows],shared_d4_positions:pairCounts[a][b]});
}
pairs.sort((a,b)=>b.shared_d4_positions-a.shared_d4_positions||a.roots[0].localeCompare(b.roots[0]));
need(memberships===totalD4Memberships,"D4 membership sum mismatch");
const duplicateMemberships=memberships-owners.size;
need(duplicateMemberships===shared,"shared membership accounting mismatch");
const withinRootMerges=totalRaw10-totalD4Memberships;
need(withinRootMerges===totalWithinRootMerges,"global within-root merge accounting mismatch");
const rawRank=new Map(per.slice().sort((a,b)=>a.raw_10stone_positions-b.raw_10stone_positions||a.root.localeCompare(b.root)).map((x,i)=>[x.root,i+1]));
const d4Rank=new Map(per.slice().sort((a,b)=>a.d4_10stone_classes-b.d4_10stone_classes||a.root.localeCompare(b.root)).map((x,i)=>[x.root,i+1]));
let rankSqDiff=0,rankChanged=0;
for(const x of per){
 x.rank_by_raw_three_ply_frontier=rawRank.get(x.root);
 x.rank_by_d4_three_ply_frontier=d4Rank.get(x.root);
 x.rank_by_two_ply_frontier=prior.get(x.root).rank_by_two_ply_frontier;
 const delta=x.rank_by_d4_three_ply_frontier-x.rank_by_two_ply_frontier;
 rankSqDiff+=delta*delta;if(delta!==0)rankChanged++;
}
const spearmanTwoToThree=1-6*rankSqDiff/(49*(49*49-1));
const checks=[
 ["49 candidate roots",per.length===49],
 ["48 pair-cover roots and 1 singleton",coverage["2"]===48&&coverage["1"]===1],
 ["73,059 nine-stone positions",total9===73059],
 ["each root matches published two-ply census",per.every(x=>x.unique_9stone_positions===prior.get(x.root).unique_9stone_positions)],
 ["all legal third moves are exactly three per raw 10-stone set",per.every(x=>x.all_legal_third_moves===3*x.raw_10stone_positions)],
 ["within-root D4 merges are exactly counted",per.every(x=>x.raw_10stone_positions-x.d4_10stone_classes===x.within_root_d4_merges)],
 ["all 10-stone D4 memberships are accounted",memberships===totalD4Memberships],
 ["owner multiplicities account for every membership",memberships===totalD4Memberships],
 ["duplicate membership identity",duplicateMemberships===totalD4Memberships-owners.size],
 ["all 49 prior two-ply ranks present",per.every(x=>Number.isInteger(x.rank_by_two_ply_frontier))],
 ["1,715 root safety quadruples",rootSafetyQuadruples===49*35],
 ["all root safety determinants nonzero",rootSafetyQuadruples===49*35],
 ["two determinant expansions agree",determinantPointChecks===tripleMasks.size*121]
];
need(checks.every(x=>x[1]),"final check failed");
const summary={
 roots:per.length,coverage_histogram:coverage,nine_stone_positions:total9,
 all_legal_third_moves:per.reduce((s,x)=>s+x.all_legal_third_moves,0),
 raw_10stone_positions:totalRaw10,total_per_root_d4_classes:totalD4Memberships,
 within_root_d4_merges:withinRootMerges,within_root_d4_merge_rate_percent:Number((100*withinRootMerges/totalRaw10).toFixed(6)),
 global_unique_d4_classes:owners.size,cross_root_duplicate_memberships:duplicateMemberships,
cross_root_duplicate_rate_percent:Number((100*duplicateMemberships/totalD4Memberships).toFixed(6)),
 two_ply_cross_root_duplicate_memberships:twoPly.summary.cross_root_duplicate_memberships,
 two_ply_cross_root_duplicate_rate_percent:twoPly.summary.cross_root_duplicate_rate_percent,
 cross_root_duplicate_rate_multiple_vs_two_ply:Number((Number((100*duplicateMemberships/totalD4Memberships).toFixed(6))/twoPly.summary.cross_root_duplicate_rate_percent).toFixed(6)),
 two_ply_largest_pair_overlap:twoPly.summary.largest_pair_overlap,
 largest_pair_overlap_multiple_vs_two_ply:Number(((pairs[0]?.shared_d4_positions??0)/twoPly.summary.largest_pair_overlap).toFixed(6)),
 spearman_rank_correlation_two_to_three_ply:Number(spearmanTwoToThree.toFixed(6)),
 rank_changed_count:rankChanged,
 multiplicity_histogram:mult,nonempty_root_pair_overlaps:pairs.length,
 largest_pair_overlap:pairs[0]?.shared_d4_positions??0,
 maximum_root_multiplicity:maxMultiplicity,
 terminal_nine_stone_positions:terminal9,min_legal_third_moves:minThird,max_legal_third_moves:maxThird,
 root_safety_quadruples:rootSafetyQuadruples,unique_triples:tripleMasks.size,determinant_point_checks:determinantPointChecks
};
const result={
 schema:"n11-five-parent-49-root-three-ply-frontier-20261119-v1",date:"2026-11-19",
 status:"exact-three-ply-structural-census",analysis_main_head:MAIN,
 source_main_head:mobility.source_main_head,
 reproduction_script:{path:SCRIPT_PATH,git_blob_sha1:blobSha(fs.readFileSync(SCRIPT_FILE,"utf8"))},
 input_pins:{
  mobility:{path:MP,git_blob_sha1:PIN.mobility},
  residual:{path:RP,git_blob_sha1:PIN.residual},
  two_ply:{path:TP,git_blob_sha1:PIN.two_ply},
  rules:{path:KP,git_blob_sha1:PIN.rules},
  convention:{path:CP,git_blob_sha1:PIN.convention}
 },
 determinant:{representation:"BigInt exact determinant on rows [x^2+y^2,x,y,1] after subtracting first row",independent_expansions:["three-term cofactor expansion","six-term Leibniz expansion"],unique_triples:tripleMasks.size,point_checks:determinantPointChecks,all_agree:true},
 summary,per_root:per,pairwise_overlap:pairs,
 checks:checks.map(([name,pass])=>({name,pass})),check_count:checks.length,all_pass:true,
 interpretation_guard:[
  "This is an exact three-ply geometric frontier census, not a DFPN search or a proof-cost measurement.",
  "D4 overlap counts only 10-stone states across these 49 candidate roots; it does not establish deep transposition-table hit rates.",
  "The 49 roots remain candidate receipt roots, not WIN7-D10 certificates.",
  "REFUTED-D10 is not a LOSS proof; standard 11x11 remains UNKNOWN."
 ]
};
fs.mkdirSync(path.dirname(OUT),{recursive:true});
fs.writeFileSync(OUT,gzipSync(Buffer.from(JSON.stringify(result,null,2)+"\n","utf8")));
console.log("FINAL "+JSON.stringify({output:OUT,summary,checks},null,2));

