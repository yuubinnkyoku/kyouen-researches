#!/usr/bin/env node
'use strict';
// Re-evaluate all 786 valid S7 options after the round-two S9 proof.
// Frozen S9 witnesses are digest-checked here, terminal-replayed separately.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const {selection}=require('../n11-s9-n24-round2-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const s=selection(),cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n24-round2-20261028/compact-certificate.json'),'utf8'));
  const bytes=Buffer.from(cert.witnessBase64,'base64');
  need(s.secured.size===5317&&s.missing.size===120&&
    cert.selected===s.selected.length&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256&&
    bytes.length===32&&sha(bytes)===cert.witnessSha256&&
    bytes.toString('base64')===cert.witnessBase64&&
    cert.win9===1&&cert.loss9===31,'S9 witness integrity');
  const win9=s.selected.filter((_,i)=>bytes[i]===255).map(x=>x.h);
  need(win9.length===1,'WIN9 count mismatch');
  const secured=new Set([...s.secured,...g.reverse(win9)]);
  need(secured.size===5326&&[...secured].every(h=>!s.loss.has(h)),
    'S8 proof-only frontier/conflict');
  const {by7}=base.inventory();
  const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
  let excluded=0;
  for(const [s7,cover] of by7){
    const kids=g.children(g.board(s7,7));
    if([...kids].some(h=>s.loss.has(h))){excluded++;continue;}
    const r={s7,cover:[...cover].sort((a,b)=>a-b),
      total:kids.size,secured:[...kids].filter(h=>secured.has(h)).length};
    r.cost=r.total-r.secured;
    need(r.cost>=0&&r.cover.length>=1&&r.cover.length<=2,
      'invalid S7 option');
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
    let total=0,securedEdges=0;const covered=new Set(),missing=new Set();
    for(const h of roots){
      need(valid.has(h),'invalid S7 root');
      for(const i of valid.get(h).cover)covered.add(i);
      for(const c of g.children(g.board(h,7))){
        total++;if(secured.has(c))securedEdges++;else missing.add(c);
      }
    }
    need(covered.size===27,'S6 obligations not covered');
    return {total,secured:securedEdges,missing:total-securedEdges,
      distinctMissing:missing.size};
  }
  const saved=evaluate(s.plan);
  need(saved.total===548&&saved.secured===430&&saved.missing===118&&
    saved.distinctMissing===118,'saved 14-root cost');
  if(negative){
    let rejected=false;try{evaluate(s.plan.slice(1));}catch(_){rejected=true;}
    need(rejected,'incomplete 14-root plan accepted');
  }
  return {schema:'n11-s5-post-n24-round2-exact-matching-v1',
    proofOnlyWin8:secured.size,knownLoss8:s.loss.size,
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
if(require.main===module)
  console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
