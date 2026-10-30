#!/usr/bin/env node
'use strict';
// Independent 3x3 integer-geometry check of the existing {60,27} LOSS
// boundary, followed by cross-source WIN4/LOSS4 S3 candidate pruning.
// S5 labels remain solver-trusted: this is NOT a terminal-only proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const SRC={
  frozen:['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache','2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
  corpus:['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache','9887a18c0788d26507be7e8e191c26817634a6b6'],
  proof:['research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json','b52b6e2829f960e93393eac8fb930d415c37ac33'],
  prior:['research/experiments/n11-s5-cross-snapshot-win4-20261031/manifest.json','4640d33e59355799054e69f175b098db075a1136']
};
function need(v,msg){if(!v)throw Error(msg)}
function pinned([file,sha]){
  const b=fs.readFileSync(path.join(ROOT,file));
  const actual=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
  need(actual===sha,'source changed: '+file);
  return b.toString('utf8');
}
const maps=Array.from({length:8},(_,m)=>Array.from({length:121},(_,i)=>{
  const x=i%11,y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][m];
  return 11*v+u;
}));
const hex=n=>n.toString(16).padStart(32,'0');
function points(k){
  need(/^[0-9a-f]{32}$/.test(k),'bad hex key');
  const n=BigInt('0x'+k);need((n>>121n)===0n,'out of board');
  const a=[];for(let i=0;i<121;i++)if((n>>BigInt(i))&1n)a.push(i);
  return a;
}
function canon(p){
  let best=null;
  for(const m of maps){
    let n=0n;for(const i of p)n|=1n<<BigInt(m[i]);
    if(best===null||n<best)best=n;
  }
  return hex(best);
}
// 3x3 determinant of differences [x^2+y^2,x,y]; all integer arithmetic.
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return [x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
       - b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
       + b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function safe(p){
  for(let a=0;a<p.length;a++)for(let b=a+1;b<p.length;b++)
    for(let c=b+1;c<p.length;c++)for(let d=c+1;d<p.length;d++)
      if(det4([p[a],p[b],p[c],p[d]])===0)return false;
  return true;
}
function board(k,n){
  const p=points(k);
  need(p.length===n&&safe(p)&&canon(p)===k,'bad board '+k);
  return p;
}
function children(p){
  const out=new Set();
  for(let i=0;i<121;i++)if(!p.includes(i)&&safe([...p,i]))out.add(canon([...p,i]));
  return out;
}
function parents(k){const p=points(k);return new Set(p.map(x=>canon(p.filter(y=>y!==x))))}
function parseCache(raw){
  const out=new Map();
  for(const line of raw.split(/\r?\n/)){
    if(!line||line.startsWith('#'))continue;
    const f=line.split(',');
    need(f.length===6&&f[0]==='s5verdict'&&f[3]==='5'&&
      (f[4]==='1'||f[4]==='2')&&/^\d+$/.test(f[5]),'malformed S5');
    const lo=BigInt(f[1]),hi=BigInt(f[2]);
    need(lo>=0n&&lo<2n**64n&&hi>=0n&&hi<2n**64n,'bad 64-bit halves');
    const k=hex(lo+(hi<<64n));board(k,5);
    need(!out.has(k),'duplicate S5');out.set(k,+f[4]);
  }
  return out;
}
function parseProof(raw){
  // Preserve 64-bit key halves before JSON.parse rounds large integers.
  // Structured records bind each key to its own witness or S4 boundary.
  const precise=raw.replace(/("(?:key|s4_class)"\s*:\s*\[\s*)(\d+)(\s*,\s*)(\d+)(\s*\])/g,
    '$1"$2"$3"$4"$5');
  const header=JSON.parse(precise);
  need(header.schema==='n11-reply27-root-loss-move-certificate-v1'&&
    header.root_outcome==='LOSS'&&header.legal_root_moves===119&&
    header.distinct_s4_loss_classes_used===32&&
    header.root_canonical===true&&header.all_root_moves_have_s3_loss_witness===true&&
    Array.isArray(header.root_stones)&&header.root_stones.length===2&&
    header.root_stones[0]===60&&header.root_stones[1]===27,
    'proof header or root changed');
  function pairKey(pair){
    need(Array.isArray(pair)&&pair.length===2&&
      pair.every(v=>typeof v==='string'&&/^\d+$/.test(v)),
      'invalid exact 64-bit key pair');
    const lo=BigInt(pair[0]),hi=BigInt(pair[1]);
    need(lo>=0n&&lo<2n**64n&&hi>=0n&&hi<2n**64n,
      'proof key half out of range');
    return hex(lo+(hi<<64n));
  }
  need(Array.isArray(header.used_s4_loss_classes)&&
    header.used_s4_loss_classes.length===32,'S4 class list incomplete');
  const loss4=new Set(),leafCounts=new Map();
  for(const row of header.used_s4_loss_classes){
    const k=pairKey(row.key);
    need(!loss4.has(k),'duplicate S4 LOSS class');
    board(k,4);
    need(Number.isSafeInteger(row.s5_children)&&row.s5_children>0,
      'invalid declared S5 child count');
    loss4.add(k);leafCounts.set(k,row.s5_children);
  }
  need(Array.isArray(header.third_move_witnesses)&&
    header.third_move_witnesses.length===119,'third-move list incomplete');
  const witnesses=header.third_move_witnesses.map(row=>{
    const k=pairKey(row.s4_class);
    need(loss4.has(k),'witness references unlisted S4 LOSS class');
    need(row.s3_is_or===0&&row.s3_stones===3&&
      row.s4_is_or===1&&row.s4_stones===4,
      'witness polarity or layer mismatch');
    need(row.s5_loss_children===leafCounts.get(k),
      'witness S5 child count mismatch');
    return {third:row.root_move,s4:k,fourth:row.s4_reply_move};
  });
  return {loss4,witnesses,leafCounts};
}
function lossBoundary(k,cache){
  const c=children(board(k,4));need(c.size>0,'empty LOSS4 boundary');
  for(const s5 of c)need(cache.get(s5)===2,'LOSS4 child not exact LOSS: '+k+' -> '+s5);
  return c.size;
}
function checkRoot(proof,cache){
  let edges=0;for(const k of proof.loss4){
    const count=lossBoundary(k,cache);
    need(count===proof.leafCounts.get(k),
      'declared S4 S5 boundary count mismatch: '+k);
    edges+=count;
  }
  need(edges===3297,'S4->S5 certificate edges changed');
  const seen=new Set(),used=new Set();
  for(const w of proof.witnesses){
    need(w.third>=0&&w.third<121&&w.third!==27&&w.third!==60&&
      !seen.has(w.third),'bad third move');
    seen.add(w.third);
    const p=[60,27,w.third,w.fourth];
    need(new Set(p).size===4&&safe(p)&&canon(p)===w.s4,'illegal fourth reply');
    need(proof.loss4.has(w.s4),'unverified LOSS4 reply');
    used.add(w.s4);
  }
  need(seen.size===119&&used.size===32,'incomplete S2 LOSS proof');
  return edges;
}
function win4From(keys){
  const out=new Set();for(const k of keys)for(const p of parents(k))out.add(p);
  return out;
}
function s3Index(win4){
  const out=new Map();
  for(const k of win4)for(const p of parents(k)){
    if(!out.has(p))out.set(p,new Set());
    out.get(p).add(k);
  }
  return out;
}
function main(){
  const frozen=parseCache(pinned(SRC.frozen)),corpus=parseCache(pinned(SRC.corpus));
  const rawProof=pinned(SRC.proof),proof=parseProof(rawProof),prior=JSON.parse(pinned(SRC.prior));
  const badWitnessCount=rawProof.replace(/("s5_loss_children":\s*)(\d+)/,
    (_,prefix,n)=>prefix+String(Number(n)+1));
  assert.throws(()=>parseProof(badWitnessCount),/witness S5 child count mismatch/);
  const badClassCount=rawProof.replace(/("s5_children":\s*)(\d+)/,
    (_,prefix,n)=>prefix+String(Number(n)+1));
  assert.throws(()=>parseProof(badClassCount),/witness S5 child count mismatch/);
  const badRoot=rawProof.replace(/("root_stones":\s*\[\s*)60(\s*,\s*27\s*\])/,
    (_,prefix,suffix)=>prefix+'99'+suffix);
  assert.throws(()=>parseProof(badRoot),/proof header or root changed/);
  need(frozen.size===5851&&corpus.size===5700,'cache inventory changed');
  const edges=checkRoot(proof,frozen);
  const old5=[...frozen].filter(([,v])=>v===1).map(([k])=>k);
  const extra5=[...new Set(prior.rows.map(x=>x.win5))].sort();
  need(old5.length===159&&extra5.length===2,'WIN5 inventory');
  for(const k of extra5)need(!frozen.has(k)&&corpus.get(k)===1,'extra WIN5 unsupported');
  const old4=win4From(old5),new4=win4From([...old5,...extra5]);
  const delta=[...new4].filter(k=>!old4.has(k)).sort();
  need(old4.size===549&&new4.size===555&&delta.length===6,'WIN4 coverage');
  need(JSON.stringify(delta)===JSON.stringify(prior.rows.map(x=>x.s4).sort()),
    'new WIN4 keys changed');
  for(const row of prior.rows)need(corpus.get(row.win5)===1&&
    parents(row.win5).has(row.s4),'invalid WIN4 witness');
  for(const k of new4)need(!proof.loss4.has(k),'WIN4/LOSS4 conflict: '+k);
  const before=s3Index(old4),after=s3Index(new4),affected=[];
  for(const [s3,wins] of after){
    const old=before.get(s3)?.size||0;
    if(old===wins.size)continue;
    const legal=children(board(s3,3));
    for(const k of wins)need(legal.has(k),'WIN4 not a legal S3 child');
    const losses=[...legal].filter(k=>proof.loss4.has(k)).sort();
    affected.push({s3,oldWin4:old,newWin4:wins.size,legalS4:legal.size,
      missingWin4:legal.size-wins.size,loss4:losses});
  }
  const excluded=affected.filter(x=>x.loss4.length),viable=affected.filter(x=>!x.loss4.length);
  const expected=[
    ['00000000000000009100000000000000','00000000000000009100000000000001',40,41,55,105],
    ['00000000000000001202000000000000','00000000000000001202000000080000',18,19,113,106],
    ['00000000000000001200000000040000','00000000000000001210000000040000',4,5,117,111],
    ['00000000000000001200000000200000','00000000000000009200000000000800',3,4,118,104]
  ];
  for(const [s3,loss4,old,n,legal,leaves] of expected){
    const row=excluded.find(x=>x.s3===s3);
    need(row&&row.loss4.length===1&&row.loss4[0]===loss4&&
      row.oldWin4===old&&row.newWin4===n&&row.legalS4===legal&&
      lossBoundary(loss4,frozen)===leaves,'LOSS3 exclusion changed: '+s3);
  }
  const gained=affected.reduce((n,x)=>n+x.newWin4-x.oldWin4,0);
  need(before.size===609&&after.size===615&&affected.length===18&&gained===24&&
    excluded.length===4&&viable.length===14&&
    Math.min(...affected.map(x=>x.missingWin4))===14&&
    Math.min(...viable.map(x=>x.missingWin4))===110,'S3 pruning counts changed');
  const bad=new Map(frozen),first=[...children(points(expected[0][1]))][0];
  bad.set(first,1);
  assert.throws(()=>lossBoundary(expected[0][1],bad),/not exact LOSS/);
  assert.throws(()=>lossBoundary(expected[0][1],new Map()),/not exact LOSS/);
  console.log(JSON.stringify({
    schema:'n11-independent-s2-root-and-s3-pruning-v1',
    root:'{60,27} LOSS (existing, solver-trusted)',
    rootThirdMoves:119,verifiedLOSS4:32,verifiedS4S5Edges:edges,
    frozenWIN5:159,combinedWIN5:161,oldWIN4:549,newWIN4:555,
    affectedS3:18,newS3WithWIN4:6,additionalS3WIN4Edges:24,
    alreadyLOSS3:4,remainingCandidates:14,
    minMissingWIN4Before:14,minMissingWIN4After:110,
    emptyBoard:'UNKNOWN',
    trust:'S5 exact labels are solver-trusted, not independently terminal-replayed'
  },null,2));
}
main();
