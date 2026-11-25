#!/usr/bin/env node
'use strict';
// Bounded second batch of 24+ child S9 terminal proofs. Only S9 candidates
// touching the *current* unproved S8 frontier are considered. No root df-pn.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {source}=require('../n11-s9-n24-priority-20261028/prove.js');
const {inventory}=require('../n11-s9-short-single-parent-20261028/prove.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function selection(){
  const s=inventory(),prior=source();
  need(s.secured.size===5317&&s.missing.size===120,'upstream proof-only boundary');
  const used=new Set(prior.selected.map(x=>x.h));
  const available=s.options.filter(x=>!used.has(x.h)).map(x=>({...x,
    liveHits:x.hits.filter(h=>s.missing.has(h))})).filter(x=>x.liveHits.length);
  const selected=[],covered=new Set();
  while(selected.length<32&&available.length){
    available.sort((a,b)=>{
      const ca=a.liveHits.filter(h=>!covered.has(h)).length;
      const cb=b.liveHits.filter(h=>!covered.has(h)).length;
      return cb-ca||b.liveHits.length-a.liveHits.length||
        a.children-b.children||b.degree-a.degree||
        (a.h<b.h?-1:a.h>b.h?1:0);
    });
    const x=available.shift();
    if(!x.liveHits.some(h=>!covered.has(h)))break;
    selected.push(x);
    for(const h of x.liveHits)covered.add(h);
  }
  need(selected.length===32,'not enough fresh, nonredundant S9 candidates');
  need(selected.every(x=>x.children>=24&&x.liveHits.length>0),'bad candidate');
  return {...s,selected,covered,priorSelected:prior.selected,availableCount:s.options.length-used.size,
    currentCandidateCount:s.options.filter(x=>!used.has(x.h)&&
      x.hits.some(h=>s.missing.has(h))).length};
}
function run(){
  const s=selection(),cache=new Map(),claims=[],wins=[],losses=[];
  let states=0,attempted=0,winEdges=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent S10 terminal disagreement '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  for(const x of s.selected){
    const kids=g.children(g.board(x.h,9));
    need(kids.size===x.children&&same(kids,ind.children4(x.h)),
      'independent S9 child boundary disagreement '+x.h);
    const ordered=[...kids].sort();
    let witness=255;
    for(let i=0;i<ordered.length;i++){
      attempted++;
      if(!terminal(ordered[i]).win){witness=i;break;}
    }
    claims.push(witness);
    if(witness===255){
      wins.push(x.h);winEdges+=ordered.length;
      for(const p of g.reverse([x.h]))
        need(g.children(g.board(p,8)).has(x.h)&&ind.children4(p).has(x.h),
          'independent reverse incidence disagreement '+x.h);
    }else losses.push(x.h);
  }
  const derived=g.reverse(wins);
  need([...derived].every(h=>!s.loss.has(h)),'WIN8/LOSS8 conflict');
  const after=new Set([...s.secured,...derived]);
  const coverage=proofs=>{
    let total=0,secured=0;const absent=new Set();
    for(const h of s.plan)for(const k of g.children(g.board(h,7))){
      total++;if(proofs.has(k))secured++;else absent.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:absent.size};
  };
  const previous=coverage(s.secured),updated=coverage(after);
  need(previous.total===548&&previous.missing===120&&updated.missing<=120,
    'conditional 14-root frontier regression');
  const bytes=Buffer.from(claims);
  const result={format:'n11-s9-n24-round2-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    currentCandidateCount:s.currentCandidateCount,selected:s.selected.length,
    potentiallyCoveredS8:s.covered.size,
    selectionSha256:sha(s.selected.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:bytes.toString('base64'),witnessSha256:sha(bytes),
    win9:wins.length,loss9:losses.length,win10Edges:winEdges,
    firstLossSearchObligations:attempted,uniqueTerminalLeaves:cache.size,
    terminalStatesPerGeometry:states,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-s.secured.size,
    proofOnlyWin8Before:s.secured.size,proofOnlyWin8After:after.size,
    knownLoss8:s.loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0};
  if(process.argv.includes('--propose')){
    console.log(JSON.stringify(result,null,2));return result;
  }
  const frozen=JSON.parse(fs.readFileSync(path.join(__dirname,
    'compact-certificate.json'),'utf8'));
  need(JSON.stringify(result)===JSON.stringify(frozen),'frozen proof changed');
  console.log(JSON.stringify({verified:true,...result},null,2));
  return result;
}
if(require.main===module)run();
module.exports={selection,run};
