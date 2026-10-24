#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const {audit:priorAudit}=require('../n11-terminal-s7-targeted-loss-union-20261024/audit.js');
const ROOTS=[
'00000000000000203802000000304020','00000000000000821080000002140024',
'00000000000000c21080040020100020','00000000000101001401010102000080',
'00000000021080401004041000000004','00000000100010841200000010050000',
'00000100100002001042100000800010','00000180100000001042100000004080'];
const COUNTS=[16,20,20,21,17,24,10,15],STATES=[1410,2273,2095,2686,1520,5336,89,426];
function need(ok,msg){if(!ok)throw Error(msg);}
function checkCertificate(raw,i,{terminal=true}={}){
  const h=ROOTS[i],lines=raw.trim().split(/\r?\n/);
  need(lines[0]==='# n11-S9-WIN-terminal-v1'&&lines[1]==='BOARD 11'&&
    lines[2]==='S9 '+h&&lines[3]==='S10_WIN_LEAVES '+COUNTS[i]&&
    lines.at(-1)==='END'&&lines.length===COUNTS[i]+5,'certificate frame '+h);
  const actual=g.children(g.board(h,9));
  const leaves=lines.slice(4,-1).map(s=>{
    need(/^LEAF [0-9a-f]{32}$/.test(s),'bad leaf');
    const v=s.slice(5);g.board(v,10);return v;
  });
  need(leaves.length===actual.size&&new Set(leaves).size===actual.size&&
    leaves.every(x=>actual.has(x)),'incomplete S9 AND boundary '+h);
  let states=0;
  if(terminal){
    for(const leaf of leaves){
      const v=g.solve10(leaf);need(v.win,'false S10 WIN '+leaf);states+=v.states;
    }
    need(states===STATES[i],'terminal states changed '+h);
  }
  return {leaves,states};
}
function audit(d,{terminal=true}={}){
  const prior=priorAudit(d,{terminal:false});
  need(prior.provenWin8Total===1228&&prior.provenLoss8Total===40&&
    prior.provenLoss7Total===282&&prior.provenClosedS7===6&&
    prior.winLossConflicts===0,'previous terminal-only baseline changed');
  const results=ROOTS.map((_,i)=>checkCertificate(d.certificates[i],i,{terminal}));
  const leaves=new Set(results.flatMap(x=>x.leaves));
  const states=results.reduce((a,x)=>a+x.states,0);
  need(leaves.size===143&&(!terminal||states===15835),'S10 union changed');
  const old=JSON.parse(d.oldCert),four=JSON.parse(d.fourCert),gap=JSON.parse(d.gap6);
  const s9=new Set(d.groups.flatMap(x=>x.trim().split(/\s+/)).concat(old.new_s9_win));
  need(s9.size===120&&ROOTS.every(h=>!s9.has(h)),'S9 baseline overlap');
  const win8=g.reverse(s9);
  for(const txt of [d.proof38,d.proof24,d.proof22])
    for(const line of txt.split(/\r?\n/)){
      if(!line.startsWith('ROOT\t'))continue;
      const row=line.split('\t');if(row[2]==='WIN')win8.add(row[1]);
    }
  for(const h of Object.keys(four.s8_witness))win8.add(h);
  for(const line of d.fifth.split(/\r?\n/))
    if(line.startsWith('EDGE '))win8.add(line.split(' ')[1]);
  for(const row of gap.s8_win_roots)win8.add(row.root);
  need(win8.size===1228,'WIN8 baseline changed');
  const loss8=new Set(d.loss35.trim().split(/\s+/).concat(
    old.s8_loss,[gap.s8_loss_root,'00000000000040001000044400830000']));
  need(loss8.size===40,'LOSS8 baseline changed');
  const derived=g.reverse(ROOTS),fresh=new Set([...derived].filter(h=>!win8.has(h)));
  need(derived.size===72&&fresh.size===71,'WIN8 delta changed');
  need(![...derived].some(h=>loss8.has(h)),'WIN/LOSS conflict');
  for(const h of fresh)
    need(ROOTS.some(root=>g.children(g.board(h,8)).has(root)),'missing WIN8 witness');
  const all8=new Set([...win8,...fresh]);
  const old7=g.reverse(win8),new7=g.reverse(fresh),all7=g.reverse(all8),loss7=g.reverse(loss8);
  need(old7.size===5111&&new7.size===287&&all7.size===5386&&loss7.size===282,
    'S7 parent counts changed');
  let moves=0,classes=0,addedMoves=0,addedClasses=0,minGap=Infinity;
  const closed=[];
  for(const h of all7){
    const b=g.board(h,7),all=new Set(),covered=new Set(),added=new Set();
    for(const p of g.legal(b)){
      const child=g.key(g.canonical(b|(1n<<BigInt(p))));
      all.add(child);
      if(all8.has(child)){moves++;covered.add(child);}
      if(fresh.has(child)){addedMoves++;added.add(child);}
    }
    classes+=covered.size;addedClasses+=added.size;
    if(all.size===covered.size)closed.push(h);
    else if(!loss7.has(h))minGap=Math.min(minGap,all.size-covered.size);
  }
  need(moves===10394&&classes===10392&&addedMoves===568&&addedClasses===568,
    'secured coverage changed');
  need(closed.length===6&&closed.every(h=>old7.has(h)&&!loss7.has(h))&&minGap===18,
    'S7 closure/gap changed');
  return {s9WinRootsAdded:8,s10WinLeaves:terminal?143:0,
    s10States:terminal?states:null,s8WinAdded:71,s8WinTotal:all8.size,
    s8LossTotal:loss8.size,s7ParentsAdded:275,s7ParentsTotal:all7.size,
    securedMovesAdded:addedMoves,securedMovesTotal:moves,
    securedClassesAdded:addedClasses,securedClassesTotal:classes,
    s7Closed:closed.length,s7NewlyClosed:0,s7LossProven:loss7.size,
    minUnknownClassGap:minGap,polarityConflicts:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit,checkCertificate,ROOTS};
if(require.main===module){
  const base=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(base,p),'utf8');
  const d={
    groups:[
      'n11-s9-win29-lift-20261023/s9-win29.keys',
      'n11-s9-win27-expansion-20261024/s9-win27.keys',
      'n11-s9-win2-followup-20261024/s9-win2.keys',
      'n11-s9-win10-20261024/s9-win10.keys',
      'n11-s9-win7-expansion-20261024/s9-win7.keys',
      'n11-s9-win20-neighbor-20261024/s9-win20.keys',
      'n11-s8-frontier-13way-20261024/s9-win7.keys'
    ].map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    direct38:read('n11-s7-38-terminal-20261019/s8_38_children.txt'),
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
    certificates:ROOTS.map(r=>read('n11-s9-batch-terminal-20261018/certificates/s9-win-'+r+'.cert'))
  };
  console.log(JSON.stringify(audit(d),null,2));
  if(process.argv.includes('--negative')){
    const s=d.certificates[0],mutations=[
      s.replace(/^LEAF [0-9a-f]{32}\n/m,''),
      s.replace(/^(LEAF [0-9a-f]{32})\nLEAF [0-9a-f]{32}/m,'$1\n$1'),
      s.replace('BOARD 11','BOARD 10'),
      s.replace('S9 '+ROOTS[0],'S9 '+ROOTS[1])];
    for(const changed of mutations){
      let rejected=false;
      try{checkCertificate(changed,0,{terminal:false});}catch(_){rejected=true;}
      need(rejected,'mutated certificate accepted');
    }
    console.error('PASS four malformed certificates rejected');
  }
}
