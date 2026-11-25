#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const {audit:previous,ROOTS:OLD_ROOTS}=require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const ROOTS=['00000100910000001042100000000040',
  '00000000000830841040000004010000',
  '00000100100000001042100000004018'];
const STATES=[941,2877,190];
function need(x,m){if(!x)throw Error(m);}
function checkCertificate(c,{terminal=true}={}){
  need(c.format==='n11-s9-three-legacy-terminal-v1'&&c.board===11&&
    c.perspective==='fixed-original-first'&&c.empty_winner==='UNKNOWN'&&
    Array.isArray(c.roots)&&c.roots.length===3,'certificate frame');
  let leaves=0,states=0;
  for(let i=0;i<3;i++){
    const row=c.roots[i];
    need(row.s9_win===ROOTS[i]&&row.states===STATES[i],'root or state count');
    const actual=g.children(g.board(row.s9_win,9)),list=row.s10_win_children;
    need(Array.isArray(list)&&list.length===actual.size&&
      new Set(list).size===actual.size&&list.every(h=>actual.has(h)),
      'incomplete S9 AND boundary '+row.s9_win);
    leaves+=list.length;
    if(terminal){
      let count=0;
      for(const h of list){
        const x=g.solve10(h);
        need(x.win,'false S10 WIN '+h);
        count+=x.states;
      }
      need(count===STATES[i],'terminal state count '+row.s9_win);
      states+=count;
    }
  }
  need(leaves===50&&(!terminal||states===4008),'leaf count or states');
  return {leaves,states:terminal?states:null};
}
function audit(d,{terminal=true}={}){
  const prior=previous(d,{terminal:false});
  need(prior.s8WinTotal===1299&&prior.s7ParentsTotal===5386&&
    prior.securedMovesTotal===10394&&prior.securedClassesTotal===10392&&
    prior.s7Closed===6&&prior.s7LossProven===282&&
    prior.minUnknownClassGap===18,'previous terminal-only baseline changed');
  const proof=checkCertificate(JSON.parse(d.newCert),{terminal});
  const old=JSON.parse(d.oldCert),four=JSON.parse(d.fourCert),gap=JSON.parse(d.gap6);
  const s9=new Set(d.groups.flatMap(x=>x.trim().split(/\s+/))
    .concat(old.new_s9_win,OLD_ROOTS));
  need(s9.size===128&&ROOTS.every(h=>!s9.has(h)),'S9 baseline or overlap');
  const win8=g.reverse(s9);
  for(const txt of [d.proof38,d.proof24,d.proof22])
    for(const line of txt.split(/\r?\n/)){
      if(line.startsWith('ROOT\t')){
        const row=line.split('\t');
        if(row[2]==='WIN')win8.add(row[1]);
      }
    }
  for(const h of Object.keys(four.s8_witness))win8.add(h);
  for(const line of d.fifth.split(/\r?\n/))
    if(line.startsWith('EDGE '))win8.add(line.split(' ')[1]);
  for(const row of gap.s8_win_roots)win8.add(row.root);
  need(win8.size===1299,'WIN8 baseline');
  const loss8=new Set(d.loss35.trim().split(/\s+/).concat(old.s8_loss,
    [gap.s8_loss_root,'00000000000040001000044400830000']));
  need(loss8.size===40,'LOSS8 baseline');
  const derived=g.reverse(ROOTS),fresh=new Set([...derived].filter(h=>!win8.has(h)));
  need(derived.size===27&&fresh.size===27,'new WIN8 overlap');
  need(![...derived].some(h=>loss8.has(h)),'WIN/LOSS conflict');
  for(const h of fresh)
    need(ROOTS.some(root=>g.children(g.board(h,8)).has(root)),
      'missing WIN8 witness');
  const all8=new Set([...win8,...fresh]);
  const old7=g.reverse(win8),all7=g.reverse(all8),loss7=g.reverse(loss8);
  need(old7.size===5386&&all7.size===5492&&loss7.size===282,'S7 parent sets');
  let moves=0,classes=0,addedMoves=0,addedClasses=0,minGap=Infinity;
  const closed=[];
  for(const h of all7){
    const board=g.board(h,7),all=new Set(),covered=new Set(),added=new Set();
    for(const pos of g.legal(board)){
      const child=g.key(g.canonical(board|(1n<<BigInt(pos))));
      all.add(child);
      if(all8.has(child)){moves++;covered.add(child);}
      if(fresh.has(child)){addedMoves++;added.add(child);}
    }
    classes+=covered.size;addedClasses+=added.size;
    if(all.size===covered.size)closed.push(h);
    else if(!loss7.has(h))minGap=Math.min(minGap,all.size-covered.size);
  }
  need(moves===10610&&classes===10608&&addedMoves===216&&
    addedClasses===216,'secured coverage');
  need(closed.length===6&&closed.every(h=>old7.has(h)&&!loss7.has(h))&&
    minGap===18,'S7 closure or unknown gap');
  return {newS9Win:3,newS10WinLeaves:terminal?proof.leaves:null,
    newS10States:proof.states,newS8Win:27,s8WinTotal:all8.size,
    s8LossTotal:loss8.size,newS7Parents:106,s7ParentsTotal:all7.size,
    newSecuredMoves:addedMoves,securedMovesTotal:moves,
    newSecuredClasses:addedClasses,securedClassesTotal:classes,
    closedS7:closed.length,newlyClosedS7:0,knownLossS7:loss7.size,
    minUnknownClassGap:minGap,winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit,checkCertificate,ROOTS};
if(require.main===module){
  const dir=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(dir,p),'utf8');
  const d={
    groups:[
      'n11-s9-win29-lift-20261023/s9-win29.keys',
      'n11-s9-win27-expansion-20261024/s9-win27.keys',
      'n11-s9-win2-followup-20261024/s9-win2.keys',
      'n11-s9-win10-20261024/s9-win10.keys',
      'n11-s9-win7-expansion-20261024/s9-win7.keys',
      'n11-s9-win20-neighbor-20261024/s9-win20.keys',
      'n11-s8-frontier-13way-20261024/s9-win7.keys'].map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    proof38:read('n11-s7-38-terminal-20261019/s8_38_win_proof.tsv'),
    proof24:read('n11-s8-neighbor24-round8-20261020/proof24_optimized.tsv'),
    proof22:read('n11-s8-round9-global78-20261020/round9_proof_optimized.tsv'),
    fourCert:read('n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json'),
    fifth:read('n11-s7-fifth-terminal-20261015/fifth-s7-win-terminal.cert'),
    gap6:read('n11-gap6-terminal-20261019/gap6-terminal-cert.json'),
    target:read('n11-s8-targeted-closure-20261015/s8-loss-terminal.cert'),
    frozenLoss7:read('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt'),
    frozenWin7:read('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'),
    frozenLoss8:read('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'),
    certificates:OLD_ROOTS.map(h=>
      read('n11-s9-batch-terminal-20261018/certificates/s9-win-'+h+'.cert')),
    newCert:read('n11-terminal-s7-three-legacy-s9-union-20261024/certificate.json')
  };
  console.log(JSON.stringify(audit(d),null,2));
  if(process.argv.includes('--negative')){
    const original=JSON.parse(d.newCert);
    const mutations=[
      x=>x.roots[0].s10_win_children.pop(),
      x=>x.roots[1].s10_win_children[1]=x.roots[1].s10_win_children[0],
      x=>x.roots[2].s9_win=x.roots[0].s9_win,
      x=>x.board=10];
    for(const mutate of mutations){
      const x=structuredClone(original);mutate(x);
      let rejected=false;
      try{checkCertificate(x,{terminal:false});}catch(_){rejected=true;}
      need(rejected,'mutated certificate accepted');
    }
    console.error('PASS four malformed certificates rejected');
  }
}
