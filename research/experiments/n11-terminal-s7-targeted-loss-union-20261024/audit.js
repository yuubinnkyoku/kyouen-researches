'use strict';
// Cache-free terminal recheck of the existing 17-leaf S8 LOSS certificate,
// followed by a certificate-only reverse-coverage audit.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const {audit:priorAudit}=require('../n11-terminal-s7-gap6-union-20261024/audit.js');
function need(x,msg){if(!x)throw Error(msg);}
function verifyTarget(text,{terminal=true}={}){
  need(text.startsWith('# n11-S8-LOSS-global-terminal-v1\n'),'wrong certificate version');
  const lines=text.trim().split(/\r?\n/).filter(x=>x&&!x.startsWith('#'));
  need(lines.length===20&&lines[0]==='BOARD 11'&&lines[19]==='END','bad certificate frame');
  need(/^ROOT [0-9a-f]{32}$/.test(lines[1]),'bad root');
  const root=lines[1].slice(5),obligations=g.children(g.board(root,8));
  need(obligations.size===31,'wrong S9 obligation count');
  const leaves=lines.slice(2,19).map(x=>{
    need(/^LEAF [0-9a-f]{32}$/.test(x),'bad leaf');return x.slice(5);
  });
  const selected=new Set(leaves),boundary=new Set();
  need(selected.size===17,'missing or duplicate leaf');
  for(const h of obligations){
    const children=g.children(g.board(h,9));
    need([...children].some(k=>selected.has(k)),'uncovered S9 obligation');
    for(const k of children)boundary.add(k);
  }
  for(const h of leaves){g.board(h,10);need(boundary.has(h),'unreachable S10 leaf');}
  let states=0;
  if(terminal){
    for(const h of leaves){
      const v=g.solve10(h);need(!v.win,'false S10 LOSS: '+h);states+=v.states;
    }
    need(states===12241,'terminal states changed');
  }
  const parents=g.reverse([root]);
  need(parents.size===8,'wrong S7 parent count');
  return {root,parents,obligations:obligations.size,leaves:leaves.length,
    terminalVerified:terminal?17:0,terminalStates:terminal?states:null};
}
function audit(d,{terminal=true}={}){
  const prior=priorAudit(d,{terminal:false});
  need(prior.win8Total===1228&&prior.loss8Total===39&&
    prior.loss7Total===274&&prior.s7ParentsTotal===5111&&
    prior.securedMoveEdgesTotal===9826&&prior.closedS7===6&&
    prior.minimumUnknownClassGap===18&&prior.winLossConflicts===0,
    'previous certified baseline changed');
  const t=verifyTarget(d.target,{terminal});
  const old=JSON.parse(d.oldCert),gap=JSON.parse(d.gap6);
  const loss8=new Set(d.loss35.trim().split(/\s+/).concat(old.s8_loss,[gap.s8_loss_root]));
  need(loss8.size===39&&!loss8.has(t.root),'LOSS8 overlap');
  const old7=g.reverse(loss8),all7=new Set([...old7,...t.parents]);
  need(old7.size===274&&all7.size===282,'LOSS7 reverse union changed');
  const s9=new Set(d.groups.flatMap(x=>x.trim().split(/\s+/)).concat(old.new_s9_win));
  need(s9.size===120,'WIN9 baseline changed');
  const win8=g.reverse(s9);
  for(const proof of [d.proof38,d.proof24,d.proof22])
    for(const line of proof.split(/\r?\n/)){
      if(!line.startsWith('ROOT\t'))continue;
      const row=line.split('\t');if(row[2]==='WIN')win8.add(row[1]);
    }
  for(const h of Object.keys(JSON.parse(d.fourCert).s8_witness))win8.add(h);
  for(const line of d.fifth.split(/\r?\n/))
    if(line.startsWith('EDGE '))win8.add(line.split(' ')[1]);
  for(const row of gap.s8_win_roots)win8.add(row.root);
  need(win8.size===1228&&!win8.has(t.root),'WIN8/LOSS8 conflict');
  const frozenLoss7=new Set(d.frozenLoss7.trim().split(/\s+/));
  const frozenWin7=new Set(d.frozenWin7.trim().split(/\s+/));
  const frozenLoss8=new Set(d.frozenLoss8.trim().split(/\s+/));
  need(frozenLoss7.size===2232&&frozenWin7.size===17&&
    frozenLoss8.size===294&&frozenLoss8.has(t.root),'frozen comparison changed');
  for(const h of t.parents){
    need(frozenLoss7.has(h)&&!frozenWin7.has(h),'frozen S7 polarity conflict');
    need(![...g.children(g.board(h,7))].every(k=>win8.has(k)),
      'closed WIN7/LOSS7 conflict');
  }
  const six=g.reverse(t.parents);
  let gained=0,oldEdges=0,minGap=Infinity,maxCoverage=0,closed=0;
  for(const h of six){
    const cls=g.children(g.board(h,6));
    const a=[...cls].filter(k=>old7.has(k)).length;
    const b=[...cls].filter(k=>t.parents.has(k)).length;
    gained+=b;oldEdges+=a;
    maxCoverage=Math.max(maxCoverage,a+b);
    minGap=Math.min(minGap,cls.size-a-b);
    if(a+b===cls.size)closed++;
  }
  need(six.size===28&&gained===56&&oldEdges===0&&minGap===49&&
    maxCoverage===2&&closed===0,'S6 coverage changed');
  return {reusedLoss8:1,provenLoss8Total:40,s9Obligations:t.obligations,
    terminalLossLeavesReverified:t.terminalVerified,terminalStates:t.terminalStates,
    newIndependentLoss7Witnesses:8,provenLoss7Total:282,
    newVerdictsAgainstFrozenCache:0,affectedS6Parents:28,
    addedS6ToS7ClassEdges:gained,previousEdgesAtTheseS6Parents:oldEdges,
    minimumUncoveredS7ClassesAtS6:minGap,newlyClosedS6:closed,
    provenWin8Total:win8.size,provenClosedS7:prior.closedS7,
    winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
module.exports={verifyTarget,audit};
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
    frozenLoss8:read('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt')
  };
  console.log(JSON.stringify(audit(d),null,2));
  if(process.env.NEGATIVE==='1'){
    const lines=d.target.trimEnd().split('\n'),i=lines.findIndex(x=>x.startsWith('LEAF '));
    const mutations=[
      lines.filter((_,j)=>i!==j).join('\n')+'\n',
      lines.map((x,j)=>j===i+1?lines[i]:x).join('\n')+'\n',
      d.target.replace('BOARD 11','BOARD 10'),
      d.target.replace('ROOT 00000000000040001000044400830000',
        'ROOT 00000000000040001000044400830001')
    ];
    for(const altered of mutations){
      let rejected=false;
      try{verifyTarget(altered,{terminal:false});}catch(_){rejected=true;}
      need(rejected,'mutated certificate accepted');
    }
    console.error('PASS four certificate mutations rejected');
  }
}
