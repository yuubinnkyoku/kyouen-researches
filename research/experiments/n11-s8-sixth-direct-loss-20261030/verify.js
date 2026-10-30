#!/usr/bin/env node
'use strict';
// Sixth direct LOSS8: cross-check independent integer 3x3 and 4x4 geometries.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8'));

function verify(c,full=false){
  need(c.schema==='n11-s8-sixth-direct-loss-v1'&&c.board===11&&
       c.emptyBoard==='UNKNOWN'&&c.verdict==='LOSS','header');
  const root=c.root,s9=g.children(g.board(root,8));
  need(s9.size===32&&c.legal9===32&&same(s9,ind.children4(root)),'S9 boundary');
  const incidence=new Map();
  for(const p of s9){
    const a=g.children(g.board(p,9));
    need(same(a,ind.children4(p)),'S10 boundary '+p);
    for(const h of a){
      if(!incidence.has(h))incidence.set(h,new Set());
      incidence.get(h).add(p);
    }
  }
  need(incidence.size===364&&c.distinct10===364&&
       [...incidence.values()].every(x=>x.size===2),'S10 incidence');
  const selected=new Set(),covered=new Set();let selectedStates=0;
  need(c.witnesses.length===16&&c.selectedLoss10===16,'selected count');
  for(const row of c.witnesses){
    need(incidence.has(row.s10)&&!selected.has(row.s10),'invalid witness');
    selected.add(row.s10);
    const a=g.solve10(row.s10),b=ind.solve4(row.s10);
    need(!a.win&&!b.win&&a.states===b.states&&a.legal===b.legal,
         'false LOSS10 witness '+row.s10);
    need(row.terminalStates===a.states&&row.legalMoves===a.legal,
         'witness metadata');
    selectedStates+=a.states;
    for(const p of incidence.get(row.s10))covered.add(p);
  }
  need(same(covered,s9)&&selectedStates===2517&&
       c.terminalStatesSelected===2517&&c.minimumWitnesses===16,
       'LOSS8 minimum leaf cover');
  const parents=[...g.reverse([root])].sort();
  need(parents.length===8&&JSON.stringify(parents)===JSON.stringify(c.s7Parents),
       'S7 parent closure');
  for(const p of parents){
    need(g.children(g.board(p,7)).has(root)&&ind.children4(p).has(root),
         'S7 incidence');
  }
  let losses=null,wins=null,states=null,closure=null;
  if(full){
    losses=[];wins=0;states=0;
    for(const h of [...incidence.keys()].sort()){
      const a=g.solve10(h),b=ind.solve4(h);
      need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
           'terminal disagreement '+h);
      states+=a.states;
      if(a.win)wins++;else losses.push(h);
    }
    need(wins===c.win10&&wins===284&&losses.length===c.loss10&&
         losses.length===80&&states===c.terminalStatesFull&&
         states===48648,'full terminal boundary');
    need([...selected].every(h=>losses.includes(h)),'witness not LOSS');
    closure=[...g.reverse(losses)].sort();
    const digest=crypto.createHash('sha256')
      .update(closure.join('\n')+'\n').digest('hex');
    need(closure.length===c.loss9ParentClosure&&closure.length===672&&
         digest===c.loss9ParentSha256,'LOSS9 parent closure digest');
    for(const h of losses)for(const p of g.pts(BigInt('0x'+h))){
      const par=g.key(g.canonical(BigInt('0x'+h)^(1n<<BigInt(p))));
      need(g.children(g.board(par,9)).has(h)&&ind.children4(par).has(h),
           'reverse incidence');
    }
  }
  return {result:{verified:true,root,verdict:'LOSS',legal9:s9.size,
    selectedLoss10:selected.size,terminalStatesSelected:selectedStates,
    fullScan:full,loss10:full?losses.length:null,emptyBoard:'UNKNOWN'},
    losses,closure};
}
if(require.main===module){
  const c=read('certificate.json'),full=process.argv.includes('--full');
  console.log(JSON.stringify(verify(c,full).result,null,2));
}
module.exports={verify};
