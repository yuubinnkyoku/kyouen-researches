#!/usr/bin/env node
'use strict';
// Independent terminal-only verifier: 3x3 differences vs 4x4 Bareiss.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const same=(a,b)=>a.size===b.size&&[...a].every(k=>b.has(k));
function verify(c,full=null){
  need(c.schema==='n11-s8-second-direct-loss-18-witness-v1'&&c.board===11&&
    c.emptyBoard==='UNKNOWN'&&c.verdict==='LOSS','header');
  const s9=[...g.children(g.board(c.root,8))].sort();
  need(s9.length===35&&c.legal9===35&&same(new Set(s9),ind.children4(c.root)),'S9 boundary');
  const incidence=new Map();
  for(const h of s9){
    const a=g.children(g.board(h,9));
    need(same(a,ind.children4(h)),'independent S10 boundary '+h);
    for(const k of a){if(!incidence.has(k))incidence.set(k,new Set());incidence.get(k).add(h);}
  }
  need(incidence.size===423&&c.distinct10===423&&
    [...incidence.values()].every(x=>x.size===2),'S10 incidence');
  need(c.witnesses.length===18&&c.selectedLoss10===18,'witness count');
  let states=0;const used=new Set(),covered=new Set();
  for(const row of c.witnesses){
    need(incidence.has(row.s10)&&!used.has(row.s10),'invalid witness');
    used.add(row.s10);
    const a=g.solve10(row.s10),b=ind.solve4(row.s10);
    need(!a.win&&!b.win&&a.states===b.states&&a.legal===b.legal,'false LOSS10 '+row.s10);
    need(a.states===row.terminalStates&&a.legal===row.legalMoves,'witness metadata');
    states+=a.states;for(const h of incidence.get(row.s10))covered.add(h);
  }
  need(covered.size===35&&states===2925&&c.terminalStatesPerGeometry===states,'LOSS8 proof coverage');
  const parents=[...g.reverse([c.root])].sort();
  need(parents.length===8&&JSON.stringify(parents)===JSON.stringify(c.s7Parents),'S7 parent closure');
  for(const h of parents)need(g.children(g.board(h,7)).has(c.root)&&
    ind.children4(h).has(c.root),'S7 parent incidence');
  const out={verified:true,s8:c.root,s8Verdict:'LOSS',legal9:35,
    selectedLoss10:18,terminalStatesPerGeometry:states,derivedS7Parents:8,emptyBoard:'UNKNOWN'};
  if(full!==null){
    need(full.schema==='n11-s8-second-full-loss10-closure-v1'&&
      full.board===11&&full.emptyBoard==='UNKNOWN'&&full.root===c.root&&
      full.distinct10===423,'full manifest header');
    let total=0,win=0;const loss=[];
    for(const h of [...incidence.keys()].sort()){
      const a=g.solve10(h),b=ind.solve4(h);
      need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,'S10 disagreement '+h);
      total+=a.states;if(a.win)win++;else loss.push(h);
    }
    need(win===326&&loss.length===97&&total===46329&&
      full.win10===win&&full.loss10===loss.length&&
      full.terminalStatesPerGeometry===total&&
      JSON.stringify(loss)===JSON.stringify(full.loss10Keys),'full LOSS10 list');
    const closure=[...g.reverse(loss)].sort();
    need(closure.length===811&&JSON.stringify(closure)===
      JSON.stringify(full.loss9ParentKeys),'full LOSS9 parent closure');
    for(const h of loss)for(const p of g.pts(BigInt('0x'+h))){
      const par=g.key(g.canonical(BigInt('0x'+h)^(1n<<BigInt(p))));
      need(g.children(g.board(par,9)).has(h),'invalid parent incidence');
    }
    out.fullScan={win10:win,loss10:loss.length,loss9Parents:closure.length,
      terminalStatesPerGeometry:total};
  }
  return out;
}
function negative(c){
  for(const mutate of [
    x=>x.witnesses.pop(),
    x=>x.witnesses[0].s10=x.witnesses[1].s10,
    x=>x.witnesses[0].terminalStates++,
    x=>x.witnesses[0].legalMoves++,
    x=>x.root='0'.repeat(32),
    x=>x.s7Parents.pop(),
    x=>x.emptyBoard='WIN'
  ]){
    const forged=JSON.parse(JSON.stringify(c));mutate(forged);
    let rejected=false;try{verify(forged)}catch(_){rejected=true;}
    need(rejected,'forged certificate accepted');
  }
}
if(require.main===module){
  const c=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
  const full=process.argv.includes('--full')?
    JSON.parse(fs.readFileSync(path.join(__dirname,'full_loss_closure.json'),'utf8')):null;
  const result=verify(c,full);
  if(process.argv.includes('--negative'))negative(c);
  console.log(JSON.stringify(result,null,2));
}
module.exports={verify,negative};
