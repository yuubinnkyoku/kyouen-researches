'use strict';
// Proof-only union of six independently terminal-verified S9 WIN roots.
// Verdicts are fixed-original-first; this audit does not re-solve S10 leaves.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latestLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const frontier=require('../n11-terminal-s7-frontier-one-union-20261025/audit.js');
const {ROOTS:BATCH8}=require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const {ROOTS:LEGACY3}=require('../n11-terminal-s7-three-legacy-s9-union-20261024/audit.js');
const EXP=path.resolve(__dirname,'..');
const FRONTIER='00000100110002001042100000000010';
const PREFIX='n11-batch-s9-terminal-20261025/';
const GROUPS=[
 'n11-s9-win29-lift-20261023/s9-win29.keys',
 'n11-s9-win27-expansion-20261024/s9-win27.keys',
 'n11-s9-win2-followup-20261024/s9-win2.keys',
 'n11-s9-win10-20261024/s9-win10.keys',
 'n11-s9-win7-expansion-20261024/s9-win7.keys',
 'n11-s9-win20-neighbor-20261024/s9-win20.keys',
 'n11-s8-frontier-13way-20261024/s9-win7.keys'
];
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
function keys(p){
 const rows=read(p).trim().split(/\s+/);
 need(rows.length>0&&rows.every((h,i)=>/^[0-9a-f]{32}$/.test(h)&&
  (i===0||rows[i-1]<h)),'invalid/unsorted keys: '+p);
 return rows;
}
function validateSources(roots,leaves,parents){
 need(roots.length===6&&leaves.length===106&&parents.length===54,
  'incorrect proof manifest sizes');
 need(new Set(roots).size===roots.length&&
  new Set(leaves).size===leaves.length&&
  new Set(parents).size===parents.length,'duplicate proof manifest entry');
 for(const h of roots)g.board(h,9);
 for(const h of leaves)g.board(h,10);
 for(const h of parents)g.board(h,8);
 const actualLeaves=new Set();
 for(const h of roots)
  for(const c of g.children(g.board(h,9)))actualLeaves.add(c);
 need(actualLeaves.size===106&&leaves.every(h=>actualLeaves.has(h)),
  'S9 AND boundary incomplete');
 const actualParents=g.reverse(roots);
 need(actualParents.size===54&&parents.every(h=>actualParents.has(h)),
  'S8 witness parents incomplete');
 for(const h of parents){
  const children=g.children(g.board(h,8));
  need(roots.some(r=>children.has(r)),'S8 parent lacks legal S9 witness: '+h);
 }
 return {s9Roots:roots.length,s10Leaves:actualLeaves.size,s8Parents:actualParents.size};
}
function audit(){
 const roots=keys(PREFIX+'s9-roots.keys');
 const leaves=keys(PREFIX+'s10-win.keys');
 const parents=keys(PREFIX+'s8-win.keys');
 const source=validateSources(roots,leaves,parents);
 const oldCert=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const oldS9=new Set([...GROUPS.flatMap(keys),...oldCert.new_s9_win,
  ...BATCH8,...LEGACY3]);
 need(oldS9.size===131&&!oldS9.has(FRONTIER),'S9 baseline changed');
 oldS9.add(FRONTIER);
 const overlap9=roots.filter(h=>oldS9.has(h));
 need(oldS9.size===132&&overlap9.length===1&&
  overlap9[0]==='00000000040800011000410a00001000',
  'S9 provenance overlap changed');
 const win8=new Set([...legacy.certifiedWin8(),...previous.sourceEdges().keys(),
  ...g.reverse([FRONTIER])]);
 need(win8.size===1521,'previous S8 WIN union changed');
 const old7=g.reverse(win8);
 need(old7.size===6226,'previous S7 parent union changed');
 const loss8=new Set([...previous.certifiedLoss8(),...latestLoss.source().cert.roots]);
 const frozenLoss8=new Set(keys(
  'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 need(loss8.size===76&&frozenLoss8.size===294,'S8 LOSS comparison changed');
 need(parents.every(h=>!loss8.has(h)&&!frozenLoss8.has(h)),
  'S8 WIN/LOSS conflict');
 const added8=new Set(parents.filter(h=>!win8.has(h)));
 need(added8.size===45,'new S8 WIN count changed');
 const affected7=g.reverse(added8);
 const all7=new Set([...old7,...affected7]);
 need(affected7.size===173&&all7.size===6396,
  'S7 parent coverage changed');
 let addedMoves=0,addedClasses=0,minGap=Infinity;
 const closed=[];
 for(const h of affected7){
  const b=g.board(h,7),legalClasses=new Set(),secured=new Set(),fresh=new Set();
  for(const p of g.legal(b)){
   const c=g.key(g.canonical(b|(1n<<BigInt(p))));
   legalClasses.add(c);
   if(win8.has(c)||added8.has(c))secured.add(c);
   if(added8.has(c)){addedMoves++;fresh.add(c);}
  }
  addedClasses+=fresh.size;
  const gap=legalClasses.size-secured.size;
  minGap=Math.min(minGap,gap);
  if(gap===0)closed.push(h);
 }
 need(addedMoves===360&&addedClasses===360&&minGap===34&&closed.length===0,
  'S7 secured edge/gap regression');
 const result={...source,previousS9Win:132,overlappingS9:1,
  addedS9Win:5,totalS9Win:137,previousS8Win:1521,
  overlappingS8:9,addedS8Win:45,totalS8Win:1566,
  previousS7Parents:6226,affectedS7Parents:173,
  addedS7Parents:170,totalS7Parents:6396,
  previousSecuredS7Moves:12170,addedSecuredS7Moves:addedMoves,
  securedS7Moves:12530,previousSecuredS7Classes:12168,
  addedSecuredS7Classes:addedClasses,securedS7Classes:12528,
  minimumUncoveredAmongAffectedS7:minGap,newlyClosedS7:0,
  provenS8Loss:loss8.size,winLossConflicts:0,
  newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN'};
 if(process.argv.includes('--full-baseline')){
  const prior=frontier.audit();
  need(prior.totalS8Win===1521&&prior.totalS7Parents===6226&&
   prior.securedS7Moves===12170&&prior.securedS7Classes===12168,
   'full previous audit mismatch');
 }
 return result;
}
module.exports={audit,validateSources};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
  const r=keys(PREFIX+'s9-roots.keys'),l=keys(PREFIX+'s10-win.keys'),
        p=keys(PREFIX+'s8-win.keys');
  const mutations=[
   ()=>validateSources(r.slice(1),l,p),
   ()=>validateSources(r,l.slice(1),p),
   ()=>validateSources(r,l,p.slice(1)),
   ()=>validateSources(r,[l[0],...l.slice(0,-1)],p)
  ];
  for(const test of mutations){
   let rejected=false;
   try{test();}catch(_){rejected=true;}
   need(rejected,'malformed proof manifest accepted');
  }
  console.error('PASS four proof-manifest mutation rejections');
 }
}
