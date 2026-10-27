#!/usr/bin/env node
'use strict';
// Targeted S9 terminal proofs for the remaining conditional 14-root S8 frontier.
// Upstream frozen certificates are checked by digest and incidence here; their
// terminal leaves must be independently replayed by their own CI verifiers.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function source(){
  const {plan,plan8,by9,candidates}=n22.inventory();
  const {old9,before,loss}=n22.priorProofs();
  const c22=read('../n11-s9-n22-complete-20261027/compact-certificate.json');
  const b22=Buffer.from(c22.witnessBase64,'base64');
  need(b22.length===candidates.length&&sha(b22)===c22.witnessSha256,'n22 digest');
  const secured22=new Set([...before,...g.reverse(candidates.filter((_,i)=>b22[i]===255))]);
  need(secured22.size===4944,'n22 secured boundary');
  const choices=[];
  for(const [h,parents] of by9){
    if(parents.size<2||g.children(g.board(h,9)).size!==23)continue;
    const gaps=[...parents].filter(p=>plan8.has(p)&&!secured22.has(p)).length;
    choices.push({h,degree:parents.size,gaps});
  }
  choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||(a.h<b.h?-1:a.h>b.h?1:0));
  const positive=choices.filter(x=>x.gaps>0);
  need(choices.length===877&&positive.length===445,'n23 inventory');
  const first=positive.slice(0,256),remaining=positive.slice(256);
  const c23=read('../n11-s9-n23-priority-20261027/compact-certificate.json');
  const b23=Buffer.from(c23.witnessBase64,'base64');
  need(b23.length===256&&sha(b23)===c23.witnessSha256&&
    sha(first.map(x=>x.h).join('\n')+'\n')===c23.selectionSha256,'n23 digest/order');
  const secured23=new Set([...secured22,...g.reverse(first.filter((_,i)=>b23[i]===255).map(x=>x.h))]);
  need(secured23.size===5120,'n23 secured boundary');
  const fresh=remaining.map(x=>({...x,currentGaps:[...by9.get(x.h)]
    .filter(p=>plan8.has(p)&&!secured23.has(p)).length})).filter(x=>x.currentGaps>0);
  fresh.sort((a,b)=>b.currentGaps-a.currentGaps||b.degree-a.degree||(a.h<b.h?-1:a.h>b.h?1:0));
  const c24=read('../n11-s9-n23-remaining-20261027/compact-certificate.json');
  const b24=Buffer.from(c24.witnessBase64,'base64');
  need(fresh.length===157&&b24.length===157&&sha(b24)===c24.witnessSha256&&
    sha(fresh.map(x=>x.h).join('\n')+'\n')===c24.selectionSha256,'remaining n23 digest/order');
  const secured=new Set([...secured23,...g.reverse(fresh.filter((_,i)=>b24[i]===255).map(x=>x.h))]);
  need(secured.size===5292&&[...secured].every(h=>!loss.has(h)),'current proof-only WIN8');
  const missing=new Set([...plan8].filter(h=>!secured.has(h)));
  need(missing.size===126,'conditional S8 frontier is no longer 126');
  const known9=new Set([...old9,...candidates,...first.map(x=>x.h),...fresh.map(x=>x.h)]);
  const options=[],shortOptions=[],hist={};
  for(const [h,parents] of by9){
    if(known9.has(h))continue;
    const hits=[...parents].filter(p=>missing.has(p));
    if(!hits.length)continue;
    const children=g.children(g.board(h,9)).size;
    hist[children]=(hist[children]||0)+1;
    if(children<24){shortOptions.push({h,hits,children,degree:parents.size});continue;}
    options.push({h,hits,children,degree:parents.size});
  }
  need(options.length>0,'no remaining 24+ child candidates');
  const covered=new Set(),selected=[],available=options.slice();
  while(selected.length<32&&available.length){
    available.sort((a,b)=>{
      const ga=a.hits.filter(h=>!covered.has(h)).length;
      const gb=b.hits.filter(h=>!covered.has(h)).length;
      return gb-ga||a.children-b.children||b.degree-a.degree||(a.h<b.h?-1:a.h>b.h?1:0);
    });
    const row=available.shift();
    if(!row.hits.some(h=>!covered.has(h)))break;
    selected.push(row);
    for(const h of row.hits)covered.add(h);
  }
  need(selected.length>0,'greedy selection empty');
  return {plan,plan8,loss,secured,missing,options,shortOptions,hist,selected,covered};
}
function run(){
  const s=source(),cache=new Map(),win9=[],loss9=[],claims=[];
  let states=0,obligations=0,winEdges=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal mismatch '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  function check(h,index){
    const kids=g.children(g.board(h,9));
    need(same(kids,ind.children4(h)),'independent S9 boundary mismatch '+h);
    const ordered=[...kids].sort();
    if(index===255){
      for(const k of ordered){obligations++;need(terminal(k).win,'false WIN9 '+h);}
      return true;
    }
    need(Number.isInteger(index)&&index>=0&&index<ordered.length,'invalid LOSS index');
    obligations++;
    need(!terminal(ordered[index]).win,'false LOSS9 '+h);
    return false;
  }
  for(const row of s.selected){
    const ordered=[...g.children(g.board(row.h,9))].sort();
    need(ordered.length===row.children,'selected S9 child count changed');
    let index=255;
    for(let i=0;i<ordered.length;i++){
      obligations++;
      if(!terminal(ordered[i]).win){index=i;break;}
    }
    if(index===255){
      win9.push(row.h);winEdges+=ordered.length;
      for(const p of g.reverse([row.h]))
        need(g.children(g.board(p,8)).has(row.h)&&ind.children4(p).has(row.h),
          'S8 reverse incidence mismatch '+row.h);
    }else loss9.push(row.h);
    claims.push(index);
  }
  const raw=Buffer.from(claims),derived=g.reverse(win9);
  need([...derived].every(h=>!s.loss.has(h)),'S8 WIN/LOSS conflict');
  const after=new Set([...s.secured,...derived]);
  function coverage(set){
    let total=0,secured=0;const absent=new Set();
    for(const h of s.plan)for(const k of g.children(g.board(h,7))){
      total++;if(set.has(k))secured++;else absent.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:absent.size};
  }
  const previous=coverage(s.secured),updated=coverage(after);
  need(previous.total===548&&previous.missing===126&&updated.missing<=126,
    'conditional 14-root coverage regression');
  const result={format:'n11-s9-n24-targeted-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    candidateCount:s.options.length,childHistogram:s.hist,
    selected:s.selected.length,potentiallyCoveredS8:s.covered.size,
    selectionSha256:sha(s.selected.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:raw.toString('base64'),witnessSha256:sha(raw),
    win9:win9.length,loss9:loss9.length,win10Edges:winEdges,
    terminalObligations:obligations,uniqueTerminalLeaves:cache.size,
    terminalStatesPerGeometry:states,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-s.secured.size,
    proofOnlyWin8Before:s.secured.size,proofOnlyWin8After:after.size,
    knownLoss8:s.loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0};
  if(process.argv.includes('--propose')){
    console.log(JSON.stringify(result,null,2));return result;
  }
  const frozen=read('./compact-certificate.json');
  need(JSON.stringify(frozen)===JSON.stringify(result),'frozen certificate mismatch');
  if(process.argv.includes('--negative')){
    const w=claims.indexOf(255),l=claims.findIndex(x=>x!==255);
    if(w>=0) {
      let rejected=false;try{check(s.selected[w].h,0);}catch(_){rejected=true;}
      need(rejected,'forged LOSS9 accepted');
    }
    if(l>=0) {
      let rejected=false;try{check(s.selected[l].h,255);}catch(_){rejected=true;}
      need(rejected,'forged WIN9 accepted');
    }
  }
  console.log(JSON.stringify({verified:true,...result},null,2));return result;
}
if(require.main===module)run();
module.exports={run,source};