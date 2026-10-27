#!/usr/bin/env node
'use strict';
// Minimal independent terminal replay for the 157 frozen S9 witnesses.
// WIN9 requires every S10 child to be WIN; LOSS9 requires only its
// selected S10 LOSS child. The exhaustive census remains in prove.js.
// Upstream n22/n23 terminal proofs are separately replayed by the CI chain.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=v=>crypto.createHash('sha256').update(v).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const load=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function verify(negative=false){
  const {plan,plan8,by9,candidates}=n22.inventory();
  const {before,loss}=n22.priorProofs();
  const c22=load('../n11-s9-n22-complete-20261027/compact-certificate.json');
  const b22=Buffer.from(c22.witnessBase64,'base64');
  need(b22.length===890&&sha(b22)===c22.witnessSha256,'n22 digest');
  const secured22=new Set([...before,...g.reverse(
    candidates.filter((_,i)=>b22[i]===255))]);
  need(secured22.size===4944,'n22 coverage');
  const choices=[];
  for(const [h,parents] of by9){
    if(parents.size<2||g.children(g.board(h,9)).size!==23)continue;
    const gaps=[...parents].filter(p=>plan8.has(p)&&!secured22.has(p)).length;
    choices.push({h,degree:parents.size,gaps});
  }
  choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||
    (a.h<b.h?-1:a.h>b.h?1:0));
  const positive=choices.filter(x=>x.gaps>0);
  need(choices.length===877&&positive.length===445,'n23 inventory');
  const first=positive.slice(0,256),remaining=positive.slice(256);
  const c23=load('../n11-s9-n23-priority-20261027/compact-certificate.json');
  const b23=Buffer.from(c23.witnessBase64,'base64');
  need(b23.length===256&&sha(b23)===c23.witnessSha256&&
    sha(first.map(x=>x.h).join('\n')+'\n')===c23.selectionSha256,
    'n23 witness integrity');
  const secured23=new Set([...secured22,...g.reverse(
    first.filter((_,i)=>b23[i]===255).map(x=>x.h))]);
  need(secured23.size===5120,'n23 coverage');
  const fresh=remaining.map(x=>({...x,currentGaps:[...by9.get(x.h)]
    .filter(p=>plan8.has(p)&&!secured23.has(p)).length}))
    .filter(x=>x.currentGaps>0);
  fresh.sort((a,b)=>b.currentGaps-a.currentGaps||b.degree-a.degree||
    (a.h<b.h?-1:a.h>b.h?1:0));
  const cert=load('./compact-certificate.json');
  const witness=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-n23-remaining-terminal-v1'&&
    cert.board===11&&cert.emptyBoard==='UNKNOWN'&&
    fresh.length===157&&witness.length===157&&
    witness.toString('base64')===cert.witnessBase64&&
    sha(witness)===cert.witnessSha256&&
    sha(fresh.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256,
    'frozen witness/selection integrity');
  const cache=new Map(),win9=[],loss9=[];
  let obligations=0,edges=0,states=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'terminal geometry mismatch '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  function checkClaim(i,claim){
    const h=fresh[i].h;
    const b=g.board(h,9),kids=g.children(b);
    need(kids.size===23&&same(kids,ind.children4(h)),
      'S9 boundary geometry mismatch '+h);
    const ordered=[...kids].sort();
    if(claim===255){
      for(const leaf of ordered){
        obligations++;
        need(terminal(leaf).win,'false WIN10 leaf '+leaf);
      }
      for(const parent of g.reverse([h])){
        need(g.children(g.board(parent,8)).has(h)&&
          ind.children4(parent).has(h),'false S8 reverse incidence '+h);
      }
      return true;
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<23,'invalid LOSS index');
    obligations++;
    need(!terminal(ordered[claim]).win,'false LOSS10 leaf '+ordered[claim]);
    return false;
  }
  for(let i=0;i<fresh.length;i++){
    if(checkClaim(i,witness[i])){win9.push(fresh[i].h);edges+=23;}
    else loss9.push(fresh[i].h);
  }
  need(win9.length===23&&loss9.length===134&&edges===529&&
    obligations===663,'minimal terminal proof census');
  // Negative controls may visit additional leaves; do not count them as
  // certificate obligations or in the measured positive replay.
  const positiveReplay={obligations,leaves:cache.size,states};
  if(negative){
    const w=witness.indexOf(255),l=witness.findIndex(x=>x!==255);
    need(w>=0&&l>=0,'missing polarity');
    for(const [i,claim] of [[w,0],[l,255]]){
      let rejected=false;
      try{checkClaim(i,claim);}catch(_){rejected=true;}
      need(rejected,'forged terminal polarity accepted');
    }
  }
  const derived=g.reverse(win9);
  need(derived.size===200&&[...derived].every(h=>!loss.has(h)),
    'S8 WIN/LOSS conflict');
  const after=new Set([...secured23,...derived]);
  need(after.size===5292,'proof-only WIN8 census');
  function coverage(proofs){
    let total=0,secured=0;const missing=new Set();
    for(const h of plan)for(const k of g.children(g.board(h,7))){
      total++;if(proofs.has(k))secured++;else missing.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:missing.size};
  }
  const previous=coverage(secured23),updated=coverage(after);
  need(JSON.stringify(previous)===JSON.stringify(cert.previous)&&
    JSON.stringify(updated)===JSON.stringify(cert.updated)&&
    updated.missing===126,'conditional 14-root coverage');
  return {verified:true,method:'minimal terminal witness replay',
    selectedS9:157,win9:23,loss9:134,
    s10Obligations:positiveReplay.obligations,
    uniqueS10Leaves:positiveReplay.leaves,
    terminalStatesPerGeometry:positiveReplay.states,fullChildOccurrences:157*23,
    obligationsAvoided:157*23-positiveReplay.obligations,
    proofOnlyWin8:after.size,unprovedPlanEdges:updated.missing,
    winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)
  console.log(JSON.stringify(verify(process.argv.includes('--negative')),null,2));
module.exports={verify};
