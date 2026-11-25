#!/usr/bin/env node
'use strict';
// Third direct LOSS8: terminal-only verification with two integer geometries.
// Never uses verdict cache, proof numbers, or incomplete searches.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8'));
function verify(c,full=null){
  need(c.schema==='n11-s8-third-direct-loss-v1'&&c.board===11&&
    c.emptyBoard==='UNKNOWN'&&c.verdict==='LOSS','header');
  const s9=g.children(g.board(c.root,8));
  need(s9.size===39&&c.legal9===39&&same(s9,ind.children4(c.root)),'S9 boundary');
  const incidence=new Map();
  for(const p of s9){
    const a=g.children(g.board(p,9));
    need(same(a,ind.children4(p)),'S10 boundary '+p);
    for(const h of a){if(!incidence.has(h))incidence.set(h,new Set());incidence.get(h).add(p);}
  }
  need(incidence.size===548&&c.distinct10===548&&
    [...incidence.values()].every(x=>x.size===2),'S10 incidence');
  const U=new Set(c.matchingUpperBoundIndependentSet);
  need(U.size===14&&c.matchingUpperBoundIndependentSet.length===14&&
    [...U].every(x=>s9.has(x)),'matching barrier vertices');
  need(c.witnesses.length===21&&c.selectedLoss10===21&&
    c.minimumWitnesses===21,'selected count');
  const selected=new Set(),covered=new Set();let selectedStates=0;
  for(const row of c.witnesses){
    need(incidence.has(row.s10)&&!selected.has(row.s10),'invalid selected leaf');
    selected.add(row.s10);
    const a=g.solve10(row.s10),b=ind.solve4(row.s10);
    need(!a.win&&!b.win&&a.states===b.states&&a.legal===b.legal,
      'false LOSS10 witness '+row.s10);
    need(row.terminalStates===a.states&&row.legalMoves===a.legal,'witness metadata');
    selectedStates+=a.states;
    for(const p of incidence.get(row.s10))covered.add(p);
  }
  need(same(covered,s9)&&selectedStates===7364&&
    c.terminalStatesSelected===7364,'LOSS8 coverage');
  const parents=[...g.reverse([c.root])].sort();
  need(parents.length===8&&JSON.stringify(parents)===JSON.stringify(c.s7Parents),
    'S7 parent closure');
  for(const p of parents)need(g.children(g.board(p,7)).has(c.root)&&
    ind.children4(p).has(c.root),'S7 incidence');
  const out={verified:true,s8:c.root,s8Verdict:'LOSS',legal9:39,
    selectedLoss10:21,terminalStatesSelected:selectedStates,emptyBoard:'UNKNOWN'};
  if(full!==null){
    need(full.schema==='n11-s8-third-full-loss10-closure-v1'&&
      full.board===11&&full.emptyBoard==='UNKNOWN'&&full.root===c.root&&
      full.distinct10===548,'full header');
    const losses=[];let wins=0,states=0;
    for(const h of [...incidence.keys()].sort()){
      const a=g.solve10(h),b=ind.solve4(h);
      need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
        'terminal disagreement '+h);
      states+=a.states;
      if(a.win)wins++;else losses.push(h);
    }
    need(wins===465&&losses.length===83&&states===114792&&
      full.win10===wins&&c.win10===wins&&
      full.loss10===losses.length&&c.loss10===losses.length&&
      full.terminalStatesFull===states&&c.terminalStatesFull===states&&
      JSON.stringify(losses)===JSON.stringify(full.loss10Keys),'full boundary');
    const closure=[...g.reverse(losses)].sort();
    need(closure.length===703&&
      JSON.stringify(closure)===JSON.stringify(full.loss9ParentKeys),
      'LOSS9 parent closure');
    for(const h of losses)for(const p of g.pts(BigInt('0x'+h))){
      const par=g.key(g.canonical(BigInt('0x'+h)^(1n<<BigInt(p))));
      need(g.children(g.board(par,9)).has(h)&&ind.children4(par).has(h),
        'reverse incidence');
    }
    const neighbors=new Set();
    for(const h of losses){
      const pp=incidence.get(h),hit=[...pp].filter(x=>U.has(x));
      need(hit.length<=1,'barrier not independent');
      if(hit.length===1)for(const p of pp)if(!U.has(p))neighbors.add(p);
    }
    need(neighbors.size===11,'barrier neighborhood not 11');
    // 14 independent vertices with only 11 neighbors force matching <=18.
    // Any edge cover of 39 vertices requires >=39-18=21 edges.
    out.fullScan={win10:wins,loss10:losses.length,loss9Parents:closure.length,
      terminalStatesPerGeometry:states,independentSet:14,neighbors:11,
      minimumLoss10Witnesses:21};
  }
  return out;
}
function negative(c,full){
  const changes=[
    x=>x.witnesses.pop(),
    x=>x.witnesses[0].s10=x.witnesses[1].s10,
    x=>x.witnesses[0].terminalStates++,
    x=>x.witnesses[0].legalMoves++,
    x=>x.root='0'.repeat(32),
    x=>x.matchingUpperBoundIndependentSet.pop(),
    x=>x.emptyBoard='WIN'
  ];
  for(const mutate of changes){
    const forged=JSON.parse(JSON.stringify(c));mutate(forged);
    let rejected=false;try{verify(forged,full)}catch(_){rejected=true;}
    need(rejected,'forged certificate accepted');
  }
}
if(require.main===module){
  const c=read('certificate.json');
  const full=process.argv.includes('--full')?read('full_loss_closure.json'):null;
  const result=verify(c,full);
  if(process.argv.includes('--negative'))negative(c,full);
  console.log(JSON.stringify(result,null,2));
}
module.exports={verify,negative};
