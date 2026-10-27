#!/usr/bin/env node
'use strict';
// A bounded 32-position S9 terminal batch selected by the certificate-aware
// planner. Only complete S10 terminal verdicts are propagated; potential
// incidence, proof numbers and unfinished searches are never WIN/LOSS.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {selection}=require('../n11-s9-n24-round2-20261028/prove.js');
const {run:plan}=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function coverage(roots,secured){
  let total=0,covered=0;const missing=new Set();
  for(const h of roots)for(const k of g.children(g.board(h,7))){
    total++;
    if(secured.has(k))covered++;else missing.add(k);
  }
  return {total,secured:covered,missing:total-covered,distinctMissing:missing.size};
}
function inventory(){
  const p=plan(),s=selection();
  need(p.emptyBoard==='UNKNOWN'&&p.proofOnlyWin8===5326&&
    p.unprovedS8===118&&p.selected===32&&
    p.optimizedPotentialCoverage===64&&p.optimizedChildCountCost===817,
    'planner boundary changed; re-audit before terminal work');
  const c=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n24-round2-20261028/compact-certificate.json'),'utf8'));
  const raw=Buffer.from(c.witnessBase64,'base64');
  need(raw.length===s.selected.length&&sha(raw)===c.witnessSha256&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===c.selectionSha256,
    'upstream round-two certificate mismatch');
  const win9=s.selected.filter((_,i)=>raw[i]===255).map(x=>x.h);
  need(win9.length===1,'upstream WIN9 count changed');
  const secured=new Set([...s.secured,...g.reverse(win9)]);
  need(secured.size===5326&&[...secured].every(h=>!s.loss.has(h)),
    'proof-only S8 WIN/LOSS boundary changed');
  const missing=new Set([...s.plan8].filter(h=>!secured.has(h)));
  need(missing.size===118,'conditional S8 frontier changed');
  const used=new Set([...s.priorSelected,...s.selected].map(x=>x.h));
  const available=new Map(s.options.filter(x=>!used.has(x.h))
    .map(x=>[x.h,x]));
  need(Array.isArray(p.selectedKeys)&&p.selectedKeys.length===32&&
    new Set(p.selectedKeys).size===32,'invalid planner selection');
  need(sha(p.selectedKeys.slice().sort().join('\n')+'\n')===
    p.selectedKeysSha256,'planner selection digest mismatch');
  const selected=p.selectedKeys.map(h=>{
    const row=available.get(h);
    need(row&&row.children>=24&&row.hits.some(k=>missing.has(k)),
      'stale or invalid planned S9 candidate '+h);
    return row;
  });
  const hits=new Set(selected.flatMap(x=>x.hits.filter(h=>missing.has(h))));
  need(hits.size===64&&selected.reduce((n,x)=>n+x.children,0)===817,
    'planner incidence/cost changed');
  return {s,p,selected,secured,missing};
}
function run(){
  const {s,p,selected,secured}=inventory();
  const terminalCache=new Map(),claims=[],wins=[],losses=[];
  let attempted=0,states=0,winEdges=0;
  function terminal(h){
    if(terminalCache.has(h))return terminalCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent S10 terminal disagreement '+h);
    terminalCache.set(h,a);states+=a.states;
    return a;
  }
  function checkClaim(h,index){
    const ordered=[...g.children(g.board(h,9))].sort();
    need(same(new Set(ordered),ind.children4(h)),
      'independent S9 child boundary mismatch '+h);
    if(index===255){
      for(const child of ordered)need(terminal(child).win,
        'forged S9 WIN accepted '+h);
      return true;
    }
    need(Number.isInteger(index)&&index>=0&&index<ordered.length,
      'invalid LOSS witness index');
    need(!terminal(ordered[index]).win,'forged S9 LOSS accepted '+h);
    return false;
  }
  for(const row of selected){
    const kids=g.children(g.board(row.h,9));
    need(kids.size===row.children&&same(kids,ind.children4(row.h)),
      'independent S9 legal-child disagreement '+row.h);
    const ordered=[...kids].sort();
    let witness=255;
    for(let i=0;i<ordered.length;i++){
      attempted++;
      if(!terminal(ordered[i]).win){witness=i;break;}
    }
    claims.push(witness);
    if(witness===255){
      wins.push(row.h);winEdges+=ordered.length;
      for(const parent of g.reverse([row.h]))
        need(g.children(g.board(parent,8)).has(row.h)&&
          ind.children4(parent).has(row.h),
          'independent S8->S9 reverse witness disagreement '+row.h);
    }else losses.push(row.h);
  }
  const derived=g.reverse(wins);
  need([...derived].every(h=>!s.loss.has(h)),
    'S8 WIN/LOSS conflict: do not publish');
  const after=new Set([...secured,...derived]);
  const previous=coverage(s.plan,secured),updated=coverage(s.plan,after);
  need(previous.total===548&&previous.missing===118&&
    updated.missing<=118,'conditional 14-root coverage regression');
  const bytes=Buffer.from(claims);
  const result={
    format:'n11-s9-n24-round3-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    plannerSelectedKeysSha256:p.selectedKeysSha256,
    selected: selected.length,potentiallyCoveredS8:64,
    selectionSha256:sha(selected.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:bytes.toString('base64'),witnessSha256:sha(bytes),
    win9:wins.length,loss9:losses.length,win10Edges:winEdges,
    firstLossSearchObligations:attempted,
    uniqueTerminalLeaves:terminalCache.size,
    terminalStatesPerGeometry:states,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-secured.size,
    proofOnlyWin8Before:secured.size,proofOnlyWin8After:after.size,
    knownLoss8:s.loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0
  };
  const certPath=path.join(__dirname,'compact-certificate.json');
  if(fs.existsSync(certPath)&&!process.argv.includes('--propose')){
    const frozen=JSON.parse(fs.readFileSync(certPath,'utf8'));
    need(JSON.stringify(result)===JSON.stringify(frozen),
      'frozen certificate changed');
    if(process.argv.includes('--negative')){
      const w=claims.indexOf(255),l=claims.findIndex(x=>x!==255);
      if(w>=0){
        let rejected=false;
        try{checkClaim(selected[w].h,0);}catch(_){rejected=true;}
        need(rejected,'forged S9 LOSS was accepted');
      }
      if(l>=0){
        let rejected=false;
        try{checkClaim(selected[l].h,255);}catch(_){rejected=true;}
        need(rejected,'forged S9 WIN was accepted');
      }
    }
    console.log(JSON.stringify({verified:true,...result},null,2));
  }else console.log(JSON.stringify(result,null,2));
  return result;
}
if(require.main===module)run();
module.exports={run,inventory,coverage};
