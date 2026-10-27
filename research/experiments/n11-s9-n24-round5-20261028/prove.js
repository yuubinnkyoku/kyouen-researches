#!/usr/bin/env node
'use strict';
// N11 conditional fourteen-root: fifth bounded S9 terminal batch.
// Certificate-only S8 coverage; never infer verdicts from potential hits.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const prior=require('../n11-s9-n24-round4-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const count=planner.popcount;
const union=rows=>rows.reduce((m,x)=>m|x.mask,0n);
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
function inventory(){
  // Only completed upstream terminal certificates can enlarge the secured
  // S8 set. A potential S9 incidence never counts as a proof.
  let old,third;const originalLog=console.log;
  try{
    console.log=()=>{};
    old=prior.inventory();
    third=require('../n11-s9-n24-round3-20261028/prove.js').inventory();
  }finally{console.log=originalLog;}
  const s=old.s;
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n24-round4-20261028/compact-certificate.json'),'utf8'));
  const raw=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-n24-round4-terminal-v1'&&
    raw.length===old.selected.length&&sha(raw)===cert.witnessSha256&&
    sha(old.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256,
    'upstream round-four certificate identity changed');
  const win9=old.selected.filter((_,i)=>raw[i]===255).map(x=>x.h);
  need(win9.length===3,'upstream round-four WIN9 boundary');
  const secured=new Set([...old.secured,...g.reverse(win9)]);
  need(secured.size===5371&&[...secured].every(h=>!s.loss.has(h)),
    'proof-only S8 WIN/LOSS conflict');
  const missing=[...s.plan8].filter(h=>!secured.has(h)).sort();
  need(missing.length===108,'conditional fourteen-root frontier changed');
  const index=new Map(missing.map((h,i)=>[h,i]));
  // Include all four earlier rounds, including round three, so an already
  // proven LOSS9 cannot silently be selected for a second terminal search.
  const used=new Set([...s.priorSelected,...s.selected,
    ...third.selected,...old.selected].map(x=>x.h));
  const options=s.options.filter(x=>!used.has(x.h)).map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(options.length>=32,'insufficient eligible S9 candidates');
  const reduced=planner.pruneDominated(options);
  const baseline=planner.greedy(options,32);
  const reducedGreedy=planner.greedy(reduced,32);
  const better=(a,b)=>count(union(a))>count(union(b))||
    (count(union(a))===count(union(b))&&cost(a)<cost(b));
  const initial=better(reducedGreedy,baseline)?reducedGreedy:baseline;
  const optimized=planner.improve(reduced,initial);
  const selected=optimized.picked;
  need(selected.length===32&&new Set(selected.map(x=>x.h)).size===32,
    'planner selected count/uniqueness');
  need(!better(baseline,selected),'candidate plan regressed against baseline');
  const hits=new Set(selected.flatMap(x=>x.hits.filter(h=>index.has(h))));
  need(hits.size===count(union(selected)),'potential hit union mismatch');
  return {s,secured,selected,missing,options,reduced,baseline,optimized,hits,
    plan:{before:108,eligible:options.length,undominated:reduced.length,
      baselineCoverage:count(union(baseline)),coverage:hits.size,
      baselineChildCost:cost(baseline),childCost:cost(selected),
      exchanges:optimized.swaps}};
}
function coverage(roots,secured){
  let total=0,covered=0;const missing=new Set();
  for(const h of roots)for(const k of g.children(g.board(h,7))){
    total++;
    if(secured.has(k))covered++;else missing.add(k);
  }
  return {total,secured:covered,missing:total-covered,distinctMissing:missing.size};
}
function run(){
  const {s,secured,selected,plan}=inventory();
  const certPath=path.join(__dirname,'compact-certificate.json');
  const propose=process.argv.includes('--propose');
  const minimal=process.argv.includes('--minimal');
  const frozen=fs.existsSync(certPath)&&!propose?
    JSON.parse(fs.readFileSync(certPath,'utf8')):null;
  need(!minimal||frozen,'minimal replay requires frozen certificate');
  const frozenBytes=frozen?Buffer.from(frozen.witnessBase64,'base64'):null;
  if(frozen)need(frozenBytes.length===selected.length&&
    sha(frozenBytes)===frozen.witnessSha256&&
    sha(selected.map(x=>x.h).join('\n')+'\n')===frozen.selectionSha256,
    'frozen witness or selection identity mismatch');
  const terminalCache=new Map();
  let states=0,attempted=0,winEdges=0;
  function terminal(h){
    if(terminalCache.has(h))return terminalCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal disagreement '+h);
    terminalCache.set(h,a);states+=a.states;
    return a;
  }
  function verifyClaim(row,claim){
    const kids=g.children(g.board(row.h,9));
    need(kids.size===row.children&&same(kids,ind.children4(row.h)),
      'independent S9 legal children mismatch '+row.h);
    const ordered=[...kids].sort();
    if(claim===255){
      for(const h of ordered)need(terminal(h).win,
        'false WIN9 universal child '+row.h);
      return ordered.length;
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<ordered.length,
      'out-of-range LOSS9 witness');
    need(!terminal(ordered[claim]).win,'false LOSS9 witness '+row.h);
    return 1;
  }
  const claims=[],wins=[];
  for(let j=0;j<selected.length;j++){
    const row=selected[j];
    const kids=g.children(g.board(row.h,9));
    need(kids.size===row.children&&same(kids,ind.children4(row.h)),
      'independent S9 child boundary '+row.h);
    const ordered=[...kids].sort();
    let witness=255;
    if(minimal){
      witness=frozenBytes[j];
      attempted+=verifyClaim(row,witness);
    }else{
      for(let i=0;i<ordered.length;i++){
        attempted++;
        if(!terminal(ordered[i]).win){witness=i;break;}
      }
    }
    claims.push(witness);
    if(witness===255){
      wins.push(row.h);winEdges+=ordered.length;
      for(const parent of g.reverse([row.h]))
        need(g.children(g.board(parent,8)).has(row.h)&&
          ind.children4(parent).has(row.h),
          'independent reverse S8 incidence mismatch '+row.h);
    }
  }
  const derived=g.reverse(wins);
  need([...derived].every(h=>!s.loss.has(h)),
    'S8 WIN/LOSS conflict: reject certificate');
  const after=new Set([...secured,...derived]);
  const previous=coverage(s.plan,secured),updated=coverage(s.plan,after);
  need(previous.total===548&&previous.missing===108&&
    updated.missing<=108,'conditional fourteen-root coverage regression');
  const positiveLeaves=terminalCache.size,positiveStates=states;
  if(minimal&&process.argv.includes('--negative')){
    const wi=claims.indexOf(255),li=claims.findIndex(x=>x!==255);
    if(wi>=0){let rejected=false;try{verifyClaim(selected[wi],0);}
      catch(_){rejected=true;}need(rejected,'forged LOSS9 accepted');}
    if(li>=0){let rejected=false;try{verifyClaim(selected[li],255);}
      catch(_){rejected=true;}need(rejected,'forged WIN9 accepted');}
    let rejected=false;try{verifyClaim(selected[0],254);}
    catch(_){rejected=true;}need(rejected,'out-of-range witness accepted');
  }
  const bytes=Buffer.from(claims);
  const result={format:'n11-s9-n24-round5-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    plan,selected:selected.length,potentiallyCoveredS8:plan.coverage,
    selectionSha256:sha(selected.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:bytes.toString('base64'),witnessSha256:sha(bytes),
    win9:wins.length,loss9:selected.length-wins.length,win10Edges:winEdges,
    firstLossSearchObligations:attempted,
    uniqueTerminalLeaves:positiveLeaves,
    terminalStatesPerGeometry:positiveStates,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-secured.size,
    proofOnlyWin8Before:secured.size,proofOnlyWin8After:after.size,
    knownLoss8:s.loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0};
  if(frozen){
    if(minimal){
      need(frozen.format===result.format&&
        frozen.win9===result.win9&&frozen.loss9===result.loss9&&
        frozen.win10Edges===result.win10Edges&&
        frozen.proofOnlyWin8After===result.proofOnlyWin8After&&
        JSON.stringify(frozen.updated)===JSON.stringify(result.updated),
        'minimal certificate verdict or coverage mismatch');
    }else need(JSON.stringify(result)===JSON.stringify(frozen),
      'full first-loss replay differs from frozen certificate');
  }
  console.log(JSON.stringify({verified:!!frozen,minimal,...result},null,2));
  return result;
}
if(require.main===module)run();
module.exports={run,inventory,coverage};
