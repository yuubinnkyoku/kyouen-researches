#!/usr/bin/env node
'use strict';
// Re-optimize the conditional 14-root proof-only cover after new 24+ S9 WIN
// witnesses. Short-child LOSS9 certificates do not propagate to S8.
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const {inventory}=require('../n11-s9-short-single-parent-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const s=inventory();
  need(s.secured.size===5317&&s.missing.size===120,'S8 proof-only frontier');
  const {by7}=base.inventory();
  const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
  let excluded=0;
  for(const [s7,cover] of by7){
    const kids=g.children(g.board(s7,7));
    if([...kids].some(h=>s.loss.has(h))){excluded++;continue;}
    const r={s7,cover:[...cover].sort((a,b)=>a-b),
      total:kids.size,secured:[...kids].filter(h=>s.secured.has(h)).length};
    r.cost=r.total-r.secured;
    need(r.cost>=0&&r.cover.length>=1&&r.cover.length<=2,'invalid S7 candidate');
    valid.set(s7,r);
    for(const i of r.cover)if(better(r,single[i]))single[i]=r;
    if(r.cover.length===2){
      const k=r.cover.join(':');
      if(better(r,pairs.get(k)))pairs.set(k,r);
    }
  }
  need(by7.size===853&&excluded===67&&valid.size===786&&
    pairs.size===343&&single.every(Boolean),'conditional option inventory');
  function evaluate(roots){
    need(roots.length===14&&new Set(roots).size===14,'invalid root count');
    let total=0,secured=0;const covered=new Set(),missing=new Set();
    for(const h of roots){
      need(valid.has(h),'invalid S7 root');
      for(const i of valid.get(h).cover)covered.add(i);
      for(const c of g.children(g.board(h,7))){
        total++;if(s.secured.has(c))secured++;else missing.add(c);
      }
    }
    need(covered.size===27,'S6 obligations not covered');
    return {total,secured,missing:total-secured,distinctMissing:missing.size};
  }
  const saved=evaluate(s.plan);
  need(saved.total===548&&saved.secured===428&&saved.missing===120&&
    saved.distinctMissing===120,'saved 14-root cost');
  if(negative){
    let rejected=false;try{evaluate(s.plan.slice(1));}catch(_){rejected=true;}
    need(rejected,'incomplete 14-root plan accepted');
  }
  return {schema:'n11-s5-post-n24-exact-matching-v1',
    proofOnlyWin8:5317,knownLoss8:s.loss.size,
    candidates:by7.size,excluded,allowed:valid.size,
    pairOptions:[...pairs].map(([k,r])=>{
      const [i,j]=k.split(':').map(Number);
      return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
    }).sort((a,b)=>a.i-b.i||a.j-b.j),
    singleOptions:single.map((r,i)=>({i,s7:r.s7,total:r.total,
      secured:r.secured,cost:r.cost})),
    savedPlan:s.plan,saved,newS7Verdicts:0,newS5Verdicts:0,
    twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};