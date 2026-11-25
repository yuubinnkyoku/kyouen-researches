#!/usr/bin/env node
'use strict';
// Fourth direct LOSS8: two independent integer geometries, terminal-only.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8'));

function verify(c,full=false,knownLosses=null){
  need(c.schema==='n11-s8-fourth-direct-loss-v1'&&c.board===11&&
       c.emptyBoard==='UNKNOWN'&&c.verdict==='LOSS','header');
  const s9=g.children(g.board(c.root,8));
  need(s9.size===40&&c.legal9===40&&same(s9,ind.children4(c.root)),
       'S9 boundary');
  const incidence=new Map();
  for(const p of s9){
    const a=g.children(g.board(p,9));
    need(same(a,ind.children4(p)),'S10 boundary '+p);
    for(const h of a){
      if(!incidence.has(h))incidence.set(h,new Set());
      incidence.get(h).add(p);
    }
  }
  need(incidence.size===573&&c.distinct10===573&&
       [...incidence.values()].every(x=>x.size===2),'S10 incidence');
  need(c.witnesses.length===21&&c.selectedLoss10===21,'selected count');
  const selected=new Set(),covered=new Set();let selectedStates=0;
  for(const row of c.witnesses){
    need(incidence.has(row.s10)&&!selected.has(row.s10),'invalid selected leaf');
    selected.add(row.s10);
    const a=g.solve10(row.s10),b=ind.solve4(row.s10);
    need(!a.win&&!b.win&&a.states===b.states&&a.legal===b.legal,
         'false LOSS10 witness '+row.s10);
    need(row.terminalStates===a.states&&row.legalMoves===a.legal,
         'witness metadata');
    selectedStates+=a.states;
    for(const p of incidence.get(row.s10))covered.add(p);
  }
  need(same(covered,s9)&&selectedStates===6070&&
       c.terminalStatesSelected===6070,'LOSS8 coverage');
  const parents=[...g.reverse([c.root])].sort();
  need(parents.length===8&&JSON.stringify(parents)===JSON.stringify(c.s7Parents),
       'S7 parent closure');
  for(const p of parents){
    need(g.children(g.board(p,7)).has(c.root)&&ind.children4(p).has(c.root),
         'S7 incidence');
  }
  let losses=knownLosses,wins=null,states=null;
  if(full){
    losses=[];wins=0;states=0;
    for(const h of [...incidence.keys()].sort()){
      const a=g.solve10(h),b=ind.solve4(h);
      need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
           'terminal disagreement '+h);
      states+=a.states;
      if(a.win)wins++;else losses.push(h);
    }
    need(wins===c.win10&&wins===495&&losses.length===c.loss10&&
         losses.length===78&&states===c.terminalStatesFull&&
         states===110563,'full terminal boundary');
  }
  let closure=null;
  if(losses!==null){
    need(losses.length===c.loss10&&losses.length===78&&
         new Set(losses).size===losses.length&&
         losses.every(x=>incidence.has(x))&&
         [...selected].every(x=>losses.includes(x)),'LOSS10 inventory');
    const removed=new Set(c.matchingBarrierRemovedVertices);
    const isolated=new Set(c.matchingBarrierIsolatedVertices);
    need(removed.size===3&&c.matchingBarrierRemovedVertices.length===3&&
         isolated.size===5&&c.matchingBarrierIsolatedVertices.length===5&&
         [...removed].every(x=>s9.has(x))&&
         [...isolated].every(x=>s9.has(x)&&!removed.has(x)),
         'matching obstruction vertices');
    for(const v of isolated){
      const edges=losses.filter(h=>incidence.get(h).has(v));
      need(edges.length>0,'isolated vertex in LOSS10 graph');
      for(const h of edges){
        need([...incidence.get(h)].filter(x=>x!==v).every(x=>removed.has(x)),
             'matching obstruction invalid '+v);
      }
    }
    // Three deleted vertices isolate five vertices: every matching leaves
    // at least two vertices unmatched, so matching <=19 and edge cover >=21.
    need(c.minimumWitnesses===21,'minimum edge-cover witness count');
    closure=[...g.reverse(losses)].sort();
    const digest=crypto.createHash('sha256')
      .update(closure.join('\n')+'\n').digest('hex');
    need(closure.length===c.loss9ParentClosure&&closure.length===664&&
         digest===c.loss9ParentSha256,'LOSS9 parent closure digest');
    if(full)for(const h of losses)for(const p of g.pts(BigInt('0x'+h))){
      const par=g.key(g.canonical(BigInt('0x'+h)^(1n<<BigInt(p))));
      need(g.children(g.board(par,9)).has(h)&&ind.children4(par).has(h),
           'reverse incidence');
    }
  }
  const out={verified:true,s8:c.root,s8Verdict:'LOSS',legal9:s9.size,
             selectedLoss10:selected.size,terminalStatesSelected:selectedStates,
             emptyBoard:'UNKNOWN'};
  if(full)out.fullScan={win10:wins,loss10:losses.length,loss9Parents:closure.length,
                       states,minimumLoss10Witnesses:21};
  return {result:out,closure,losses};
}

function negative(c,losses){
  const changes=[
    x=>x.witnesses.pop(),
    x=>x.witnesses[0].s10=x.witnesses[1].s10,
    x=>x.witnesses[0].terminalStates++,
    x=>x.witnesses[0].legalMoves++,
    x=>x.root='0'.repeat(32),
    x=>x.matchingBarrierIsolatedVertices.pop(),
    x=>x.matchingBarrierRemovedVertices.pop(),
    x=>x.loss9ParentSha256='0'.repeat(64),
    x=>x.emptyBoard='WIN'
  ];
  for(const mutate of changes){
    const forged=JSON.parse(JSON.stringify(c));mutate(forged);
    let rejected=false;
    try{verify(forged,false,losses)}catch(_){rejected=true;}
    need(rejected,'forged certificate accepted');
  }
}
if(require.main===module){
  const c=read('certificate.json'),full=process.argv.includes('--full');
  const out=verify(c,full);
  if(process.argv.includes('--negative')){
    need(full,'negative barrier tests require --full');
    negative(c,out.losses);
  }
  console.log(JSON.stringify(out.result,null,2));
}
module.exports={verify,negative};
