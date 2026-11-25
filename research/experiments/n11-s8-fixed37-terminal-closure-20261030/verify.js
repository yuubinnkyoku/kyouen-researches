#!/usr/bin/env node
'use strict';
// Independent 3x3 / 4x4 integer-geometry cross-check for all 37 fixed S8 roots.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));

function verify(c,full=false){
  need(c.schema==='n11-fixed14-37-s8-direct-terminal-v1'&&
       c.board===11&&c.emptyBoard==='UNKNOWN','header');
  const audit=read('../n11-s8-complete-child-audit-20261030/incidence.json');
  need(c.rows.length===37&&audit.s8Rows.length===37,'root count');
  let wins=0,losses=0,selected=0,selectedStates=0,fullBoundary=0,fullStates=0;
  const solve=h=>{
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
         'geometry or recursion disagreement '+h);
    return a;
  };
  for(let k=0;k<c.rows.length;k++){
    const [root,verdict,indices]=c.rows[k];
    need(root===audit.s8Rows[k].h,'root mismatch');
    const s9=[...g.children(g.board(root,8))].sort();
    need(s9.length===audit.s8Rows[k].legal9&&
         same(new Set(s9),ind.children4(root)),'S9 boundary '+root);
    const incidence=new Map();
    for(const p of s9){
      const kids=g.children(g.board(p,9));
      need(same(kids,ind.children4(p)),'S10 boundary '+p);
      for(const h of kids){
        if(!incidence.has(h))incidence.set(h,new Set());
        incidence.get(h).add(p);
      }
    }
    const s10=[...incidence.keys()].sort();
    if(verdict==='W'){
      need(Number.isInteger(indices)&&indices>=0&&indices<s9.length,
           'WIN8 witness index');
      const children=g.children(g.board(s9[indices],9));
      need(children.size>0,'empty WIN8 witness boundary');
      for(const h of children){
        need(solve(h).win,'false WIN10 '+h);
        selectedStates+=g.solve10(h).states;selected++;
      }
      wins++;
    }else{
      need(verdict==='L'&&Array.isArray(indices)&&indices.length>0,
           'LOSS8 witness indices');
      const covered=new Set(),seen=new Set();
      for(const i of indices){
        need(Number.isInteger(i)&&i>=0&&i<s10.length&&!seen.has(i),
             'invalid LOSS8 witness index');
        seen.add(i);
        const h=s10[i],a=solve(h);
        need(!a.win,'false LOSS10 '+h);
        selected++;selectedStates+=a.states;
        for(const p of incidence.get(h))covered.add(p);
      }
      need(same(covered,new Set(s9)),'uncovered S9 '+root);
      losses++;
    }
    if(full){
      const verdicts=new Map();
      for(const h of s10){
        const a=solve(h);
        verdicts.set(h,a.win);fullStates+=a.states;
      }
      fullBoundary+=s10.length;
      const hasLoss9=s9.some(p=>[...g.children(g.board(p,9))].every(h=>verdicts.get(h)));
      need(hasLoss9===(verdict==='W'),'full boundary verdict disagreement '+root);
    }
  }
  need(wins===c.win8&&wins===8&&losses===c.loss8&&losses===29,'S8 verdict counts');
  need(selected===c.terminalWitnesses&&selected===612&&
       selectedStates===c.terminalStatesSelected&&selectedStates===92603,
       'terminal witness counts');
  if(full)need(fullBoundary===c.fullScanDistinct10WithMultiplicity&&
       fullBoundary===11884&&fullStates===c.fullScanTerminalStatesWithMultiplicity&&
       fullStates===1625006,'full terminal scan totals');
  return {verified:true,fixedPlanRoots:37,win8:wins,loss8:losses,
          selectedTerminalLeaves:selected,selectedTerminalStates:selectedStates,
          fullScan:full,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
  console.log(JSON.stringify(verify(read('certificate.json'),
      process.argv.includes('--full')),null,2));
}
module.exports={verify};
