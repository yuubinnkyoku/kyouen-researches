#!/usr/bin/env node
'use strict';
// Re-evaluate all 786 valid S7 options after the round-four S9 terminal proof.
// Frozen S9 witnesses are digest-checked here, terminal-replayed separately.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const {selection}=require('../n11-s9-n24-round2-20261028/prove.js');
const {run:plan}=require('../n11-s9-n24-round2-20261028/plan_next.js');
const {inventory:inventory4}=require('../n11-s9-n24-round4-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const s=selection(),p=plan({quiet:true});
  const read=rel=>JSON.parse(fs.readFileSync(path.join(__dirname,rel),'utf8'));
  const c2=read('../n11-s9-n24-round2-20261028/compact-certificate.json');
  const b2=Buffer.from(c2.witnessBase64,'base64');
  need(s.secured.size===5317&&s.missing.size===120&&
    b2.length===32&&sha(b2)===c2.witnessSha256&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===c2.selectionSha256&&
    c2.win9===1&&c2.loss9===31,'round-two upstream certificate integrity');
  const w2=s.selected.filter((_,i)=>b2[i]===255).map(x=>x.h);
  const secured2=new Set([...s.secured,...g.reverse(w2)]);
  need(secured2.size===5326,'round-two S8 proof-only frontier changed');
  const c3=read('../n11-s9-n24-round3-20261028/compact-certificate.json');
  const b3=Buffer.from(c3.witnessBase64,'base64');
  need(p.proofOnlyWin8===5326&&p.unprovedS8===118&&
    p.selectedKeys.length===32&&b3.length===32&&
    sha(b3)===c3.witnessSha256&&
    sha(p.selectedKeys.join('\n')+'\n')===c3.selectionSha256&&
    p.selectedKeysSha256===c3.plannerSelectedKeysSha256&&
    c3.win9===2&&c3.loss9===30,'round-three witness/order integrity');
  const w3=p.selectedKeys.filter((_,i)=>b3[i]===255);
  need(w3.length===2,'round-three WIN9 count mismatch');
  const secured3=new Set([...secured2,...g.reverse(w3)]);
  need(secured3.size===5344&&[...secured3].every(h=>!s.loss.has(h)),
    'round-three S8 WIN/LOSS conflict');
  const p4=inventory4();
  need(p4.secured.size===5344&&
    p4.secured.size===secured3.size&&
    [...secured3].every(h=>p4.secured.has(h)),
    'round-four planner upstream proof boundary');
  const c4=read('../n11-s9-n24-round4-20261028/compact-certificate.json');
  const b4=Buffer.from(c4.witnessBase64,'base64');
  need(c4.format==='n11-s9-n24-round4-terminal-v1'&&
    b4.length===p4.selected.length&&b4.length===32&&
    sha(b4)===c4.witnessSha256&&
    sha(p4.selected.map(x=>x.h).join('\n')+'\n')===c4.selectionSha256&&
    c4.win9===3&&c4.loss9===29&&
    c4.proofOnlyWin8Before===5344&&c4.proofOnlyWin8After===5371,
    'round-four certificate identity');
  const w4=p4.selected.filter((_,i)=>b4[i]===255).map(x=>x.h);
  need(w4.length===3,'round-four WIN9 count mismatch');
  const secured=new Set([...secured3,...g.reverse(w4)]);
  need(secured.size===5371&&[...secured].every(h=>!s.loss.has(h)),
    'round-four S8 WIN/LOSS conflict');
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
  need(saved.total===548&&saved.secured===440&&saved.missing===108&&
    saved.distinctMissing===108,'saved 14-root cost');
  if(negative){
    let rejected=false;try{evaluate(s.plan.slice(1));}catch(_){rejected=true;}
    need(rejected,'incomplete 14-root plan accepted');
  }
  return {schema:'n11-s5-post-n24-round4-exact-matching-v1',
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
