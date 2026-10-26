#!/usr/bin/env node
'use strict';
// Conditional S5 WIN route only. Every selected S7 root remains UNKNOWN.
// All labels are fixed-original-first. Known S8 LOSS is used for exclusion,
// not as a proof of any candidate S7 WIN.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const union=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const threeLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const HERE=__dirname;
const ROOT='00000000000000821080000000000020';
const NEW7='00000000000100001000000042401008';
const FROZEN_SHA='17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e';
const MORE_LOSS=[
 '000000100010a0011000000001004000',
 '00000410000000821080000002000020',
 '00004000000000821080000040400020'
];
const need=(ok,why)=>{if(!ok)throw Error(why);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const children=h=>g.children(BigInt('0x'+h));
const pair=(i,j)=>i+':'+j;
const format=b=>g.key(g.canonical(b));
function bareiss4(pp) {
 const m=pp.map(p=>{const x=p%11,y=Math.floor(p/11);return [x,y,x*x+y*y,1];});
 let sign=1,prev=1;
 for(let k=0;k<3;k++){
  if(!m[k][k]){
   let j=k+1;while(j<4&&!m[j][k])j++;
   if(j===4)return 0;
   [m[k],m[j]]=[m[j],m[k]];sign=-sign;
  }
  const pivot=m[k][k];
  for(let i=k+1;i<4;i++)for(let j=k+1;j<4;j++){
   const v=m[i][j]*pivot-m[i][k]*m[k][j];
   need(v%prev===0,'non-exact Bareiss division');
   m[i][j]=v/prev;
  }
  for(let i=k+1;i<4;i++)m[i][k]=0;
  prev=pivot;
 }
 return sign*m[3][3];
}
function independentChildren(h){
 const b=BigInt('0x'+h),pts=g.pts(b),tri=[],out=new Set();
 for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++)
  for(let k=j+1;k<pts.length;k++)tri.push([pts[i],pts[j],pts[k]]);
 for(let p=0;p<121;p++){
  if((b>>BigInt(p))&1n)continue;
  if(!tri.some(t=>bareiss4([...t,p])===0))
   out.add(format(b|(1n<<BigInt(p))));
 }
 return out;
}
function same(a,b){return a.size===b.size&&[...a].every(x=>b.has(x));}
function inventory(){
 const raw=read('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt');
 need(crypto.createHash('sha256').update(raw).digest('hex')===FROZEN_SHA,
      'frozen S7 WIN inventory changed');
 const frozen=raw.trim().split(/\s+/);
 need(frozen.length===17,'frozen S7 count changed');
 const known6=g.reverse([...frozen,NEW7]);
 const legal6=children(ROOT);
 const missing=[...legal6].filter(h=>!known6.has(h)).sort();
 need(known6.size===110&&legal6.size===32&&missing.length===27,
      'S5 proof-only boundary changed');
 const frozenLoss=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 need(frozenLoss.size===294,'frozen S8 LOSS inventory changed');
 const knownLoss=new Set([...frozenLoss,...union.certifiedLoss8(),
  ...threeLoss.source().cert.roots,...MORE_LOSS]);
 need(knownLoss.size>=337,'S8 LOSS exclusion inventory unexpectedly shrank');
 const by7=new Map();
 for(let i=0;i<missing.length;i++)for(const h of children(missing[i])){
  if(!by7.has(h))by7.set(h,new Set());
  by7.get(h).add(i);
 }
 need(by7.size===853,'S7 candidate census changed');
 return {missing,by7,knownLoss};
}
function audit(negative=false){
 const {missing,by7,knownLoss}=inventory();
 const costs=new Map(),singles=Array(27).fill(Infinity),valid=new Map();
 let rejected=0;
 for(const [h,covered] of by7){
  const s8=children(h);
  if([...s8].some(x=>knownLoss.has(x))){rejected++;continue;}
  valid.set(h,{covered,s8,cost:s8.size});
  for(const i of covered)singles[i]=Math.min(singles[i],s8.size);
  if(covered.size===2){
   const [i,j]=[...covered].sort((a,b)=>a-b),id=pair(i,j);
   costs.set(id,Math.min(costs.get(id)??Infinity,s8.size));
  }
 }
 need(singles.every(Number.isFinite),'uncoverable S6 class');
 const selected=fs.readFileSync(path.join(HERE,'s7-plan14-matching.keys'),'ascii').trim().split(/\s+/);
 const old=keys('n11-s8-plan14-loss8-20261026/s7-plan14-revised.keys');
 function validate(plan){
  need(plan.length===14&&new Set(plan).size===14,'invalid S7 plan cardinality');
  const covered=new Set(),distinct=new Set();
  let edges=0;
  for(const h of plan){
   need(valid.has(h),'candidate absent or refuted: '+h);
   g.board(h,7);
   const row=valid.get(h);
   for(const i of row.covered)covered.add(i);
   edges+=row.cost;
   for(const x of row.s8)distinct.add(x);
  }
  need(covered.size===27,'not all missing S6 classes covered');
  return {edges,distinct:distinct.size,securedClasses:covered.size};
 }
 const current=validate(selected),previous=validate(old);
 need(current.edges===546&&current.distinct===545,'optimized S8 obligations changed');
 need(previous.edges===554&&previous.distinct===553,'previous plan regression');
 for(const h of [ROOT,...missing,...selected]){
  need(same(children(h),independentChildren(h)),
       '3x3/4x4 legal boundary disagreement: '+h);
 }
 if(negative){
  const bad=[selected.slice(1),selected.map((h,i)=>i? h:ROOT),
   selected.map((h,i)=>i? h:'00004000000000821080000040000020')];
  for(const test of bad){
   let rejectedBad=false;try{validate(test);}catch(_){rejectedBad=true;}
   need(rejectedBad,'tampered S7 plan accepted');
  }
 }
 const pairCosts=[...costs].map(([id,cost])=>{
  const [i,j]=id.split(':').map(Number);return {i,j,cost};
 }).sort((a,b)=>a.i-b.i||a.j-b.j);
 return {schema:'n11-s5-conditional-minimum-edge-matching-v1',
  sourceS5:ROOT,uncoveredS6:27,candidateS7:by7.size,
  knownS8LossExclusion:knownLoss.size,rejectedS7:rejected,
  allowedS7:valid.size,pairEdges:pairCosts,singleCosts:singles,
  selectedS7: selected,selectedCost:current.edges,selectedDistinct:current.distinct,
  oldCost:previous.edges,oldDistinct:previous.distinct,
  independentGeometryChecked:1+missing.length+selected.length,
  newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
 const r=audit(process.argv.includes('--negative'));
 console.log(JSON.stringify(r));
}
module.exports={audit};
