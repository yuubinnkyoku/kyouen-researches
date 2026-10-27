#!/usr/bin/env node
'use strict';
// Certificate-aware, terminal-free planning for the *current* conditional
// 14-root S8 frontier. Potential incidence is never treated as a WIN proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const {source}=require('../n11-s9-n24-priority-20261028/prove.js');
const {selection}=require('./prove.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function popcount(x){
  let n=0;
  while(x){x&=x-1n;n++;}
  return n;
}
function union(rows){let mask=0n;for(const x of rows)mask|=x.mask;return mask;}
function cost(rows){return rows.reduce((s,x)=>s+x.children,0);}
function greedy(options,limit){
  const picked=[],used=new Set();
  let covered=0n;
  while(picked.length<limit){
    const sorted=options.filter(x=>!used.has(x.h)).map(x=>({
      x,increment:popcount(x.mask&~covered)
    })).filter(x=>x.increment>0).sort((a,b)=>
      b.increment-a.increment||a.x.children-b.x.children||
      b.x.degree-a.x.degree||a.x.h.localeCompare(b.x.h));
    if(!sorted.length)break;
    const x=sorted[0].x;
    picked.push(x);used.add(x.h);covered|=x.mask;
  }
  return picked;
}
function improve(options,initial){
  let picked=initial.slice(),baseMask=union(picked),baseCount=popcount(baseMask),
    baseCost=cost(picked),swaps=0;
  // One-for-one exchange; each accepted move strictly improves the
  // lexicographic objective (distinct potential S8 hits, -child count).
  for(let pass=0;pass<4;pass++){
    const chosen=new Set(picked.map(x=>x.h));
    let best=null;
    for(let i=0;i<picked.length;i++){
      const rest=union(picked.filter((_,j)=>i!==j));
      const restCount=popcount(rest);
      for(const candidate of options){
        if(chosen.has(candidate.h))continue;
        const n=restCount+popcount(candidate.mask&~rest);
        const c=baseCost-picked[i].children+candidate.children;
        if(n<baseCount||(n===baseCount&&c>=baseCost))continue;
        if(!best||n>best.count||(n===best.count&&c<best.cost)||
           (n===best.count&&c===best.cost&&candidate.h<best.row.h)){
          best={i,row:candidate,count:n,cost:c};
        }
      }
    }
    if(!best)break;
    picked[best.i]=best.row;baseCount=best.count;baseCost=best.cost;
    baseMask=union(picked);swaps++;
    need(popcount(baseMask)===baseCount,'exchange coverage invariant');
  }
  return {picked,swaps};
}
function selfTest(){
  const rows=[
    {h:'a',mask:15n,children:4,degree:1},
    {h:'b',mask:19n,children:4,degree:1},
    {h:'c',mask:44n,children:4,degree:1}
  ];
  const before=greedy(rows,2);
  need(popcount(union(before))===5,'synthetic greedy regression');
  const after=improve(rows,before);
  need(popcount(union(after.picked))===6,'synthetic exchange regression');
}
function run(){
  selfTest();
  const s=selection(),prior=source();
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'compact-certificate.json'),'utf8'));
  const bytes=Buffer.from(cert.witnessBase64,'base64');
  need(bytes.length===s.selected.length&&
    sha(bytes)===cert.witnessSha256&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256,
    'round-two certificate identity changed');
  const win9=s.selected.filter((_,i)=>bytes[i]===255).map(x=>x.h);
  need(win9.length===1,'round-two WIN9 boundary changed');
  const secured=new Set([...s.secured,...g.reverse(win9)]);
  need(secured.size===5326,'proof-only S8 frontier changed');
  const missing=[...s.plan8].filter(h=>!secured.has(h)).sort();
  need(missing.length===118,'conditional 14-root frontier changed');
  const index=new Map(missing.map((h,i)=>[h,i]));
  const used=new Set([...prior.selected,...s.selected].map(x=>x.h));
  const options=s.options.filter(x=>!used.has(x.h)).map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(options.length>0,'no candidate remains');
  const baseline=greedy(options,32);
  const optimized=improve(options,baseline);
  const baselineMask=union(baseline),newMask=union(optimized.picked);
  need(popcount(newMask)>=popcount(baselineMask),'coverage regression');
  const result={
    scope:'potential S9->S8 incidence, not a terminal verdict',
    emptyBoard:'UNKNOWN',proofOnlyWin8:secured.size,unprovedS8:missing.length,
    eligibleUnprovedS9:options.length,selected:baseline.length,
    baselinePotentialCoverage:popcount(baselineMask),
    optimizedPotentialCoverage:popcount(newMask),
    baselineChildCountCost:cost(baseline),
    optimizedChildCountCost:cost(optimized.picked),
    exchanges:optimized.swaps,
    selectedKeysSha256:sha(optimized.picked.map(x=>x.h).sort().join('\n')+'\n'),
    newlyProvedS8:0,newTwoStoneClosures:0
  };
  console.log(JSON.stringify(result,null,2));
  return result;
}
if(require.main===module)run();
module.exports={run,greedy,improve,popcount,selfTest};
