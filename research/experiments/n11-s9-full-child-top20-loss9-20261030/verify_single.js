#!/usr/bin/env node
'use strict';
// Independently replay the fixed single S9 LOSS witness using 3x3 and 4x4
// integer geometry. Only a terminal LOSS10 child proves this LOSS9 verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
function verify(cert,negative=false){
  const plan=read('post_top20_frontier.json');
  const target=plan.targetS9ChildrenBySmallestS10Boundary[0];
  need(plan.emptyBoard==='UNKNOWN'&&plan.unknown9After===750&&
    plan.unknownEdgesAfter===760&&target.s9===cert.s9,'source plan mismatch');
  need(cert.schema==='n11-fixed14-post-top20-one-s9-terminal-v1'&&
    cert.emptyBoard==='UNKNOWN'&&cert.s9Verdict==='LOSS'&&
    cert.twoStoneRootClosed===false,'certificate header mismatch');
  const a=g.children(g.board(cert.s9,9)),b=ind.children4(cert.s9);
  need(a.size===b.size&&[...a].every(x=>b.has(x))&&
    a.size===cert.s10Children&&a.size===target.legal10,'S9 legal S10 boundary mismatch');
  const ordered=[...a].sort();
  need(cert.testedS10.length===cert.loss10WitnessIndex+1,
    'missing earlier tested S10 children');
  for(let i=0;i<cert.testedS10.length;i++){
    const row=cert.testedS10[i];
    need(row.index===i&&row.s10===ordered[i],'S10 child index mismatch');
    const x=g.solve10(row.s10),y=ind.solve4(row.s10);
    need(x.win===y.win&&x.legal===y.legal&&x.states===y.states&&
      x.win===row.s10Win&&x.legal===row.s10LegalMoves&&
      x.states===row.terminalStates,'terminal replay mismatch '+i);
    need(x.win===(i<cert.loss10WitnessIndex),'not first LOSS10 witness');
  }
  const leaf=BigInt('0x'+ordered[cert.loss10WitnessIndex]);
  const parents=new Set();
  for(const pt of g.pts(leaf)){
    const par=g.key(g.canonical(leaf^(1n<<BigInt(pt))));
    need(g.children(g.board(par,9)).has(ordered[cert.loss10WitnessIndex])&&
      ind.children4(par).has(ordered[cert.loss10WitnessIndex]),
      'invalid LOSS9 parent closure');
    parents.add(par);
  }
  need(parents.has(cert.s9)&&parents.size===cert.loss9ParentClosure&&
    sha([...parents].sort().join('\n')+'\n')===cert.loss9ParentSha256,
    'LOSS9 parent closure digest mismatch');
  if(negative){
    const mutants=[
      c=>c.testedS10[c.loss10WitnessIndex].s10Win=true,
      c=>c.testedS10[c.loss10WitnessIndex].terminalStates++,
      c=>c.testedS10[c.loss10WitnessIndex].s10=c.testedS10[0].s10,
      c=>c.loss10WitnessIndex=255,
      c=>c.loss9ParentSha256='0'.repeat(64),
      c=>c.s9='0'.repeat(32),
    ];
    for(const mutate of mutants){
      const forged=structuredClone(cert);mutate(forged);
      let rejected=false;
      try{verify(forged,false)}catch(_){rejected=true}
      need(rejected,'forged certificate accepted');
    }
  }
  return {verified:true,independentGeometries:2,s9:cert.s9,
    s9Verdict:'LOSS',s10Children:a.size,
    testedS10:cert.testedS10.length,
    loss10WitnessIndex:cert.loss10WitnessIndex,
    loss9ParentClosure:parents.size,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(
  verify(read('single_s9_certificate.json'),process.argv.includes('--negative')),null,2));
module.exports={verify};
