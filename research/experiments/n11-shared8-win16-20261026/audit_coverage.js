#!/usr/bin/env node
'use strict';
// Proof-only S8 WIN coverage of the conditional 14-root S7 plan.
// Inherited source verdicts are NOT re-solved here; see their own verifiers.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const union=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const threeLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const ROOT='00020000000000821090200000000020';
const NEW7='00000000000100001000000042401008';
const RECENT_S9='00000100110002001042100000000010';
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8').trim().split(/\s+/);
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
function audit(){
 const before=new Set([...legacy.certifiedWin8(),...union.sourceEdges().keys()]);
 need(before.size===1513,'proof-only S8 WIN baseline changed');
 const recent8=g.reverse([RECENT_S9]);
 need(recent8.size===9,'recent S9 witness geometry changed');
 for(const h of recent8)need(g.children(g.board(h,8)).has(RECENT_S9),'illegal recent S9 witness');
 for(const h of recent8)before.add(h);
 need(before.size===1521,'recent S9 reverse lift changed');
 const new7children=g.children(g.board(NEW7,7));
 need(new7children.size===34,'new independent S7 WIN boundary changed');
 const known=new Set([...before,...new7children]);
 const frozenWin=new Set(read('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt'));
 const frozenLoss=new Set(read('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const loss=new Set([...union.certifiedLoss8(),...threeLoss.source().cert.roots,
  '000000100010a0011000000001004000',
  '00000410000000821080000002000020']);
 need(loss.size===78,'proof-only S8 LOSS baseline changed');
 need(!loss.has(ROOT)&&!frozenLoss.has(ROOT),'WIN/LOSS conflict at new S8');
 need([...known].every(h=>!loss.has(h)),'known proof-only WIN/LOSS conflict');
 const plan=read('n11-s8-pair-break-20261026/s7-plan14.keys');
 need(plan.length===14&&new Set(plan).size===14,'14-root plan altered');
 const occurrences=new Map(),rows=[];
 for(const p of plan){
  const children=g.children(g.board(p,7));
  for(const h of children){
   if(!occurrences.has(h))occurrences.set(h,[]);
   occurrences.get(h).push(p);
  }
  const secured=[...children].filter(h=>known.has(h)).length;
  rows.push({s7:p,legalS8:children.size,securedBefore:secured,
   uncoveredBefore:children.size-secured,
   securedAfter:secured+Number(children.has(ROOT)&&!known.has(ROOT))});
 }
 const edges=rows.reduce((a,r)=>a+r.legalS8,0);
 need(edges===542&&occurrences.size===541,'14-root S8 boundary changed');
 const shared=[...occurrences].filter(([_,v])=>v.length>1);
 need(shared.length===1&&shared[0][0]===ROOT&&shared[0][1].length===2,
      'shared S8 target no longer the unique duplicate');
 const beforeDistinct=[...occurrences.keys()].filter(h=>known.has(h)).length;
 const after=new Set([...known,ROOT]);
 const afterDistinct=[...occurrences.keys()].filter(h=>after.has(h)).length;
 const beforeEdges=rows.reduce((s,r)=>s+r.securedBefore,0);
 const afterEdges=rows.reduce((s,r)=>s+r.securedAfter,0);
 need(afterDistinct-beforeDistinct===Number(!known.has(ROOT))&&
      afterEdges-beforeEdges===2*Number(!known.has(ROOT)),
      'secured proof-only S8 boundary increment inconsistent');
 return {s8:ROOT,alreadyInProofOnlyUnion:known.has(ROOT),inFrozenWinCache:frozenWin.has(ROOT),
  inFrozenLossCache:frozenLoss.has(ROOT),proofOnlyWinBaseline1521:before.size,
  newS7WinBoundary:34,proofOnlyWinUnionBefore:known.size,
  proofOnlyLossUnion:loss.size,
  conditionalS7Roots:plan.length,allS7ToS8Edges:edges,distinctS8:occurrences.size,
  sharedS8:ROOT,sharedS7Parents:shared[0][1],
  securedEdgesBefore:beforeEdges,securedEdgesAfter:afterEdges,
  securedDistinctBefore:beforeDistinct,securedDistinctAfter:afterDistinct,
  uncoveredEdgesAfter:edges-afterEdges,
  uncoveredDistinctAfter:occurrences.size-afterDistinct,
  bestRootAfter:rows.sort((a,b)=>(a.legalS8-a.securedAfter)-(b.legalS8-b.securedAfter)||a.s7.localeCompare(b.s7))[0],
  newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
