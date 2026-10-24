#!/usr/bin/env node
'use strict';
// Reuse the terminal-proven gap6 roots in the existing S7 coverage audit.
// All parent/child edges are regenerated; frozen cache verdicts are not trusted.
const fs=require('node:fs'),path=require('node:path');
const {verify:priorAudit}=require('../n11-terminal-s7-fifth-win-union-20261024/audit.js');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
function check(x,msg){if(!x)throw Error(msg);}
function audit(d,{terminal=true}={}){
  const prior=priorAudit({groups:d.groups,oldCert:d.oldCert,loss35:d.loss35,
    direct38:d.direct38,proof38:d.proof38,proof24:d.proof24,
    proof22:d.proof22,fourCert:d.fourCert,fifth:d.fifth});
  check(prior.totalWin8===1210&&prior.totalS7Parents===4971&&
    prior.totalSecuredMoveEdges===9682&&prior.totalSecuredClassEdges===9680&&
    prior.closedS7===6&&prior.minimumUnknownClassGap===18,
    'previous independent terminal coverage baseline changed');
  const c=JSON.parse(d.gap6),gap=g.verify(c,{terminal});
  const old=JSON.parse(d.oldCert),four=JSON.parse(d.fourCert);
  const s9=new Set(d.groups.flatMap(x=>x.trim().split(/\s+/)).concat(old.new_s9_win));
  check(s9.size===120,'old WIN9 root count changed');
  const win8=g.reverse(s9);
  check(win8.size===961,'old WIN9 reverse closure changed');
  const counts=[];
  for(const t of [d.proof38,d.proof24,d.proof22]){
    const roots=t.split(/\r?\n/).filter(x=>x.startsWith('ROOT\t'))
      .map(x=>x.split('\t')).filter(x=>x[2]==='WIN').map(x=>x[1]);
    counts.push(roots.length);
    for(const h of roots)win8.add(h);
  }
  check(counts.join(',')==='38,20,16','direct WIN8 root count changed');
  for(const h of Object.keys(four.s8_witness))win8.add(h);
  for(const line of d.fifth.split(/\r?\n/).filter(x=>x.startsWith('EDGE ')))
    win8.add(line.split(' ')[1]);
  check(win8.size===1210,'previous WIN8 union changed');
  const oldParents=g.reverse(win8);
  check(oldParents.size===4971,'previous WIN8 reverse parents changed');
  const loss8=new Set(d.loss35.trim().split(/\s+/).concat(old.s8_loss));
  check(loss8.size===38,'old LOSS8 count changed');
  const oldLoss7=g.reverse(loss8);
  check(oldLoss7.size===268,'old LOSS7 reverse count changed');
  const newWin8=new Set(gap.win8Keys),newLoss8=gap.loss8Key;
  check(newWin8.size===18&&[...newWin8].every(h=>!win8.has(h)&&!loss8.has(h)),
    'WIN8 overlap or WIN/LOSS conflict');
  check(!loss8.has(newLoss8)&&!win8.has(newLoss8)&&!newWin8.has(newLoss8),
    'LOSS8 overlap or WIN/LOSS conflict');
  const newParents=g.reverse(newWin8),allWin8=new Set([...win8,...newWin8]);
  const allParents=g.reverse(allWin8),allLoss8=new Set([...loss8,newLoss8]);
  const loss7=g.reverse(allLoss8),newLoss7=g.reverse([newLoss8]);
  check(newParents.size===141&&allParents.size===5111&&
    [...newParents].filter(h=>!oldParents.has(h)).length===140,
    'S7 parent expansion changed');
  check(newLoss7.size===8&&[...newLoss7].filter(h=>!oldLoss7.has(h)).length===6&&
    loss7.size===274,'LOSS7 reverse expansion changed');
  let movesAdded=0,classesAdded=0,closedNew=[],minGap=Infinity;
  for(const h of newParents){
    const b=g.board(h,7),moves=g.legal(b),cls=g.children(b);
    const gained=new Set(),covered=new Set();
    for(const p of moves){
      const child=g.key(g.canonical(b|(1n<<BigInt(p))));
      if(allWin8.has(child))covered.add(child);
      if(newWin8.has(child)){
        check(!win8.has(child),'duplicate secured edge');
        gained.add(child);movesAdded++;
      }
    }
    classesAdded+=gained.size;
    if(covered.size===cls.size)closedNew.push(h);
    else if(!loss7.has(h))minGap=Math.min(minGap,cls.size-covered.size);
  }
  check(movesAdded===144&&classesAdded===144&&closedNew.length===0&&
    minGap>=18,'S7 coverage extension changed');
  check(![...loss7].some(h=>prior.certifiedFifthRoot===h),
    'known certified WIN7 now conflicts with LOSS7');
  return {reusedWin8:18,win8Total:allWin8.size,reusedLoss8:1,loss8Total:allLoss8.size,
    additionalLoss7AgainstPrior:6,loss7Total:loss7.size,
    addedS7Parents:140,s7ParentsTotal:allParents.size,
    addedSecuredMoveEdges:movesAdded,securedMoveEdgesTotal:prior.totalSecuredMoveEdges+movesAdded,
    addedSecuredClassEdges:classesAdded,securedClassEdgesTotal:prior.totalSecuredClassEdges+classesAdded,
    closedS7:prior.closedS7,newlyClosedS7:0,
    minimumUnknownClassGap:18,winLossConflicts:0,
    s10TerminalReverified:gap.terminalVerified,s10TerminalStates:gap.terminalStates,
    terminalVerifiedWins:537,terminalVerifiedLosses:43,
    emptyBoard:'UNKNOWN'};
}
module.exports={audit};
if(require.main===module){
  const base=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(base,p),'utf8');
  const d={groups:[
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
    'n11-s8-frontier-13way-20261024/s9-win7.keys'].map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    direct38:read('n11-s7-38-terminal-20261019/s8_38_children.txt'),
    proof38:read('n11-s7-38-terminal-20261019/s8_38_win_proof.tsv'),
    proof24:read('n11-s8-neighbor24-round8-20261020/proof24_optimized.tsv'),
    proof22:read('n11-s8-round9-global78-20261020/round9_proof_optimized.tsv'),
    fourCert:read('n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json'),
    fifth:read('n11-s7-fifth-terminal-20261015/fifth-s7-win-terminal.cert'),
    gap6:read('n11-gap6-terminal-20261019/gap6-terminal-cert.json')};
  console.log(JSON.stringify(audit(d),null,2));
  if(process.env.NEGATIVE==='1'){
    const bad=structuredClone(d),cert=JSON.parse(bad.gap6);
    cert.s8_win_roots.pop();bad.gap6=JSON.stringify(cert);
    let rejected=false;try{audit(bad,{terminal:false});}catch(_){rejected=true;}
    check(rejected,'missing WIN8 root accepted');
    console.error('PASS missing-root mutation rejected');
  }
}
