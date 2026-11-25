#!/usr/bin/env node
// Independent cost79c WIN7 certificate audit, remaining sixteen roots.
// Node 22, standard library only. Uses BigInt generalized-circle equations,
// not the search engine, verdict cache, or 4x4 Bareiss certificate checker.
// Same verification logic as audit_cost79c_certificates_general_circle_bigint_20261118.mjs
// (the parallel-lane verifier for bits [1,2,21]); this script covers the remaining
// sixteen published WIN7 roots bits [17,26,28,29,30,31,47,58,62,91,96,100,109,113,117,120]
// and additionally replays the published per-bit subroots and rootcheck metadata.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const HERE=path.dirname(fileURLToPath(import.meta.url));
const OUT=path.resolve(HERE,'../output');
const CERT=path.join(OUT,'class2-lane-cost79c-certificates');
const BASE_MAIN='99ebd380c0ef3adbc45dadfb3ce82d2556b3920b';
const SPECS=[
 {bit:17,root:'00000000000000c09002000200020000',rows:74600,d4:'00000000000000c09002000200020000',parts:[
  {name:'n11_s7_00000000000000c09002000200020000.cert.part1of3',sha:'0ca2f096cac1223307070f1c4fc4eb8c0ef82ce8'},
  {name:'n11_s7_00000000000000c09002000200020000.cert.part2of3',sha:'ffd40388aff819c9ab43ad5c6e7339aaed692f0a'},
  {name:'n11_s7_00000000000000c09002000200020000.cert.part3of3',sha:'699a34e9ba4d015ec61f5be8e35e2adcb31de89f'}]},
 {bit:26,root:'00000000000000c09002000204000000',rows:59195,d4:'00000000000000c09002000204000000',parts:[
  {name:'n11_s7_00000000000000c09002000204000000.cert.part1of2',sha:'56a7c0c8e12b0bd9ad31e8f2cef88ad44d50e9bc'},
  {name:'n11_s7_00000000000000c09002000204000000.cert.part2of2',sha:'396eb7b76e31483238df6e55b7e2f3131b7e896e'}]},
 {bit:28,root:'00000000000000c09002000210000000',rows:61126,d4:'00000000000000c09002000210000000',parts:[
  {name:'n11_s7_00000000000000c09002000210000000.cert.part1of2',sha:'43e614091cbc05cb963acfedafe52167b35401d4'},
  {name:'n11_s7_00000000000000c09002000210000000.cert.part2of2',sha:'cac377bb326aad3f5ee444dbccad890faaf5460b'}]},
 {bit:29,root:'00000000000000c09002000220000000',rows:58957,d4:'00000000000000c09002000220000000',parts:[
  {name:'n11_s7_00000000000000c09002000220000000.cert.part1of2',sha:'a2da8d0eaa00be5dcbf80c1c1eac8443d939584b'},
  {name:'n11_s7_00000000000000c09002000220000000.cert.part2of2',sha:'b7584c43d26c9943863555644eee6dadafb32de7'}]},
 {bit:30,root:'00000000000000c09002000240000000',rows:35813,d4:'00000000000000c09002000240000000',parts:[
  {name:'n11_s7_00000000000000c09002000240000000.cert.part1of2',sha:'30c0fdcf34ad53394986aae64ba007025fd7d967'},
  {name:'n11_s7_00000000000000c09002000240000000.cert.part2of2',sha:'ceae1f5bbd02619310cd7f41f08884cf87b27c90'}]},
 {bit:31,root:'00000000000000c09002000280000000',rows:41791,d4:'00000000000000c09002000280000000',parts:[
  {name:'n11_s7_00000000000000c09002000280000000.cert.part1of2',sha:'fe416625ead11b8b9233fea107cd536706a3eb04'},
  {name:'n11_s7_00000000000000c09002000280000000.cert.part2of2',sha:'e029b6662543604db8baf1a4a93936cdd2ab1303'}]},
 {bit:47,root:'00000000000000c09002800200000000',rows:65560,d4:'00000000000000c09002800200000000',parts:[
  {name:'n11_s7_00000000000000c09002800200000000.cert.part1of2',sha:'e13b7ed4f7712fe05bd0745409e599dce1a94216'},
  {name:'n11_s7_00000000000000c09002800200000000.cert.part2of2',sha:'b5249671630035bede49a80beab9f1ba2a23a234'}]},
 {bit:58,root:'00000000000000c09402000200000000',rows:39363,d4:'00000000000000c09402000200000000',parts:[
  {name:'n11_s7_00000000000000c09402000200000000.cert.part1of2',sha:'202b07e24395110d609f09693132cd7b23c08ee4'},
  {name:'n11_s7_00000000000000c09402000200000000.cert.part2of2',sha:'1e075390f54670f884fde02ee33dd13457132b97'}]},
 {bit:62,root:'00000000000000c0d002000200000000',rows:60432,d4:'00000000000000c0d002000200000000',parts:[
  {name:'n11_s7_00000000000000c0d002000200000000.cert.part1of2',sha:'ec0fd189aae6635616140e934187ea282291571b'},
  {name:'n11_s7_00000000000000c0d002000200000000.cert.part2of2',sha:'12f50badbff21410ea36344aa04e6502a175c4f3'}]},
 {bit:91,root:'00000000080000c09002000200000000',rows:48379,d4:'00000000000020809003000002000000',parts:[
  {name:'n11_s7_00000000080000c09002000200000000.cert.part1of2',sha:'4c86a5d511dd347aed72f0cfa1f860560f9ef157'},
  {name:'n11_s7_00000000080000c09002000200000000.cert.part2of2',sha:'d30787a2d9ddf9e71a93320b208f45d2e9bcb803'}]},
 {bit:96,root:'00000001000000c09002000200000000',rows:64333,d4:'00000000000020809003000040000000',parts:[
  {name:'n11_s7_00000001000000c09002000200000000.cert.part1of2',sha:'5443b26a34cac8273d1c5976d25b3ce1df1b47b6'},
  {name:'n11_s7_00000001000000c09002000200000000.cert.part2of2',sha:'99344221c755134569bf0d8399905d191cdcd9cc'}]},
 {bit:100,root:'00000010000000c09002000200000000',rows:54360,d4:'00000000000020809003000000001000',parts:[
  {name:'n11_s7_00000010000000c09002000200000000.cert.part1of2',sha:'5ce198f9278623db2c3934918466a21239d60542'},
  {name:'n11_s7_00000010000000c09002000200000000.cert.part2of2',sha:'a820917fdb7368c197fa8ff61e220311379260ca'}]},
 {bit:109,root:'00002000000000c09002000200000000',rows:56579,d4:'00000000000020809003000000200000',parts:[
  {name:'n11_s7_00002000000000c09002000200000000.cert.part1of2',sha:'f5da90088725fd88e1886f78e88dab9b3144c680'},
  {name:'n11_s7_00002000000000c09002000200000000.cert.part2of2',sha:'89f7616805a90a2d49044636c759f33a4e9ca9dc'}]},
 {bit:113,root:'00020000000000c09002000200000000',rows:57273,d4:'00000000000020809003000000000008',parts:[
  {name:'n11_s7_00020000000000c09002000200000000.cert.part1of2',sha:'d69f5aeae23e8d27e6a2b7e76a9d7b441121eb4b'},
  {name:'n11_s7_00020000000000c09002000200000000.cert.part2of2',sha:'5f0ee5a269f786c29e271957cde50b64c9992a7d'}]},
 {bit:117,root:'00200000000000c09002000200000000',rows:80970,d4:'00000000000020809003000000000080',parts:[
  {name:'n11_s7_00200000000000c09002000200000000.cert.part1of3',sha:'d3948c04b50409f6d6a4280cc41b961596e6599b'},
  {name:'n11_s7_00200000000000c09002000200000000.cert.part2of3',sha:'a6bb5b001e66ef4e6cb3060cf4c90470a784f5ae'},
  {name:'n11_s7_00200000000000c09002000200000000.cert.part3of3',sha:'17cc17b6b8b5b29785f12f5a0033b497904b82ce'}]},
 {bit:120,root:'01000000000000c09002000200000000',rows:74776,d4:'00000000000020809003000000000400',parts:[
  {name:'n11_s7_01000000000000c09002000200000000.cert.part1of3',sha:'8b84cfcb2f5b16bd750889077cc6731f9225eb23'},
  {name:'n11_s7_01000000000000c09002000200000000.cert.part2of3',sha:'56807ca9799b6f3fa6f553ff8c7573e06e47ab7b'},
  {name:'n11_s7_01000000000000c09002000200000000.cert.part3of3',sha:'6a8b09baf9c2146575131b782dc386cb0229e0e3'}]},
];
const META_PINS={
 17:{subroots:'faab0a2c54141e88ab4a94b2dd9654fd8712174e',rootcheck:'e6f72460a9f5580cf7b5bc45ceb19db60b67d314'},
 26:{subroots:'e857566cffcc0604ca2a867cca245553f0881423',rootcheck:'4c4aa2486b853421858f2cc0058549cdd9994ea1'},
 28:{subroots:'5d6bf03661a43c4d42fbab7902337a6adb29a0f5',rootcheck:'d541cc7bc2f788d0503c87c6e980bd9a1b2dac9c'},
 29:{subroots:'0fa61303949a8d01464f56cf2d6310c5455f19cf',rootcheck:'0f9d0791c2c13493bbc933355def00a5d5878acc'},
 30:{subroots:'90b7e46bdd8d0ec7885ec434b76c4dd5a5c06d84',rootcheck:'9418474c8a480407b425edf8562bc46435aca76e'},
 31:{subroots:'de7f16563114e9f6f034fa59fc636d2b83b8321f',rootcheck:'738e591916a9d0a50d9ccff4358e1e034523bef8'},
 47:{subroots:'ad755e7fa3aade7bb354e03a40ec3d69329d726c',rootcheck:'6a7000d42f7915dac29a08dbfbc97e57a55c15ae'},
 58:{subroots:'f268c70d68e47c8593f620ff219699ad57d42212',rootcheck:'4da1cfaebc6468d3c995def7b305973d9dd19abb'},
 62:{subroots:'cf796d6c276cc2b0ced1323f363bfa4e19110844',rootcheck:'b2c4ca1d7257245a0f9038362b42bac97e7dcd2a'},
 91:{subroots:'7b07a807f12b19d06af1fcdc89eea9556f95cdd6',rootcheck:'08ef409d431a66683a4af644b20362d007991db3'},
 96:{subroots:'993f4517be446d5015d753a2402abf339a436366',rootcheck:'5a4e3843cb6c2ca076b289e49d0412c4079939e6'},
 100:{subroots:'0cfed0c2e3f05b6b0271c7fb18cdd9758d5d003e',rootcheck:'e278009edaef739f95fa89c3d046c524ddd84000'},
 109:{subroots:'c84f14b1e1a174fb7d92ed921b594fa5600bc625',rootcheck:'7ac41a95bf4482c76786382bd67e8e8b4961d5ca'},
 113:{subroots:'a7d633160385b529b214038aad6a940393fa119d',rootcheck:'12f9b116512197bdeaca0f546612b46e5c610c5e'},
 117:{subroots:'61418245cc2ac424779a7e92f1edfc1a47a6fda4',rootcheck:'41d3e4cef5920a4728f1fb71d50f92b064e7c94b'},
 120:{subroots:'fb5f8c9c3847254e1e8fa67fb4e0a650f5607fb8',rootcheck:'b5c433ad826b07ea08063514f46347b5b6ce6484'},
};
const FULL=(1n<<121n)-1n, BIT=Array.from({length:121},(_,i)=>1n<<BigInt(i));
const tripleCache=new Map(),legalCache=new Map();
function need(ok,msg){if(!ok)throw new Error(msg);}
function det3(m){return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function bitIndex(bit){let v=bit,shift=0;while((v&0xffffffffn)===0n){v>>=32n;shift+=32;}return shift+31-Math.clz32(Number(v&0xffffffffn));}
function points(mask){const out=[];while(mask){const low=mask&-mask;out.push(bitIndex(low));mask-=low;}return out;}
function gitBlobSha(buf){return createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');}
function fbt(a,b,c){
 const s=[a,b,c].sort((x,y)=>x-y);a=s[0];b=s[1];c=s[2];
 const key=a*14641+b*121+c,old=tripleCache.get(key);if(old!==undefined)return old;
 const x1=a%11,y1=Math.floor(a/11),x2=b%11,y2=Math.floor(b/11),x3=c%11,y3=Math.floor(c/11);
 const dx2=x2-x1,dy2=y2-y1,dx3=x3-x1,dy3=y3-y1,cross=dx2*dy3-dy2*dx3;
 let A=0n,B=0n,C=0n,D=0n;
 if(cross===0){const g=gcd(BigInt(dy2),BigInt(dx2));B=BigInt(dy2)/g;C=-BigInt(dx2)/g;D=-(B*BigInt(x1)+C*BigInt(y1));}
 else{
  const X=[BigInt(x1),BigInt(x2),BigInt(x3)],Y=[BigInt(y1),BigInt(y2),BigInt(y3)],S=X.map((x,i)=>x*x+Y[i]*Y[i]);
  A=det3([[X[0],Y[0],1n],[X[1],Y[1],1n],[X[2],Y[2],1n]]);
  B=det3([[-S[0],Y[0],1n],[-S[1],Y[1],1n],[-S[2],Y[2],1n]]);
  C=det3([[X[0],-S[0],1n],[X[1],-S[1],1n],[X[2],-S[2],1n]]);
  D=det3([[X[0],Y[0],-S[0]],[X[1],Y[1],-S[1]],[X[2],Y[2],-S[2]]]);
 }
 let g=gcd(gcd(A,B),gcd(C,D));if(g){A/=g;B/=g;C/=g;D/=g;}
 if(A<0n||(A===0n&&(B<0n||(B===0n&&C<0n)))){A=-A;B=-B;C=-C;D=-D;}
 let mask=0n;
 for(let p=0;p<121;p++){const x=BigInt(p%11),y=BigInt(Math.floor(p/11));if(A*(x*x+y*y)+B*x+C*y+D===0n)mask|=BIT[p];}
 tripleCache.set(key,mask);return mask;
}
function legal(board){
 const key=board.toString(16).padStart(32,'0'),old=legalCache.get(key);if(old!==undefined)return old;
 const ps=points(board);let banned=board;
 for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++)for(let k=j+1;k<ps.length;k++)banned|=fbt(ps[i],ps[j],ps[k]);
 const opts=FULL&~banned;legalCache.set(key,opts);return opts;
}
function canon(mask){
 let best=null;
 for(let s=0;s<8;s++){let z=0n;for(const p of points(mask)){const x=p%11,y=Math.floor(p/11);let a,b;
  switch(s){case 0:a=x;b=y;break;case 1:a=y;b=10-x;break;case 2:a=10-x;b=10-y;break;case 3:a=10-y;b=x;break;case 4:a=10-x;b=y;break;case 5:a=x;b=10-y;break;case 6:a=y;b=x;break;default:a=10-y;b=10-x;}
  z|=BIT[11*b+a];}if(best===null||z<best)best=z;}
 return best.toString(16).padStart(32,'0');
}
function parseCert(raw,root,expectedRows){
 const lines=raw.toString('ascii').split(/\r?\n/);if(lines[lines.length-1]==='')lines.pop();
 need(lines[0]==='n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS','bad certificate header');
 need(lines[1]==='root '+root,'bad certificate root');
 const strategy=new Map();let prev='';
 for(const line of lines.slice(2)){const m=line.match(/^([0-9a-f]{32}) ([0-9]+)$/);need(!!m,'bad strategy row');
  need(m[1]>prev,'unsorted or duplicate strategy row');prev=m[1];
  const board=BigInt('0x'+m[1]),move=Number(m[2]);need(board<=FULL,'board out of range');need(move>=0&&move<121,'move out of range');strategy.set(m[1],move);}
 need(strategy.size===expectedRows,'strategy row count mismatch');return strategy;
}
function verifyOne(spec){
 const partBuffers=spec.parts.map(p=>{const b=fs.readFileSync(path.join(CERT,p.name));need(gitBlobSha(b)===p.sha,'Git blob SHA mismatch: '+p.name);return b;});
 need(partBuffers[0][partBuffers[0].length-1]===10,'part 1 is not line terminated');
 for(let i=1;i<partBuffers.length;i++)need(/^[0-9a-f]{32} [0-9]+\n/.test(partBuffers[i].toString('ascii')),'part '+(i+1)+' does not start at a strategy-row boundary');
 const raw=Buffer.concat(partBuffers),strategy=parseCert(raw,spec.root,spec.rows),root=BigInt('0x'+spec.root),rp=points(root);
 need(rp.length===7,'root must have seven stones');
 for(let i=0;i<rp.length;i++)for(let j=i+1;j<rp.length;j++)for(let k=j+1;k<rp.length;k++){
  const others=root&~BIT[rp[i]]&~BIT[rp[j]]&~BIT[rp[k]];need((fbt(rp[i],rp[j],rp[k])&others)===0n,'unsafe root');
 }
 const rootMoves=points(legal(root));need(rootMoves.length>0,'root has no legal loser move');
 const consumed=new Set(),subroots=[];
 for(const move of rootMoves){
  const stack=[[root|BIT[move],0]],seen=new Set(),terminalStones=[];let winnerStates=0,loserStates=0,opponentEdges=0;
  while(stack.length){const [board,depth]=stack.pop(),key=board.toString(16).padStart(32,'0');if(seen.has(key))continue;seen.add(key);
   const opts=legal(board),ps=points(board);
   if(opts===0n){need(depth%2===1,'winner is stuck');need(!strategy.has(key),'terminal has strategy row');terminalStones.push(ps.length);}
   else if(depth%2===0){const move2=strategy.get(key);need(move2!==undefined,'missing winner strategy row '+key);need((opts&BIT[move2])!==0n,'illegal winner move '+key);consumed.add(key);winnerStates++;stack.push([board|BIT[move2],depth+1]);}
   else{need(!strategy.has(key),'strategy row on loser turn '+key);loserStates++;let q=opts;while(q){const low=q&-q;q-=low;opponentEdges++;stack.push([board|low,depth+1]);}}
  }
  need(terminalStones.length>0,'no terminal under subroot');const lo=Math.min(...terminalStones),hi=Math.max(...terminalStones);
  need(lo>=13&&hi<=17,'terminal stone range outside [13,17]');
  subroots.push({move,seen:seen.size,winnerStates,loserStates,terminals:terminalStones.length,opponentEdges,range:[lo,hi]});
 }
 let missing=0,extra=0;for(const k of strategy.keys())if(!consumed.has(k))missing++;for(const k of consumed)if(!strategy.has(k))extra++;
 need(missing===0&&extra===0,'strategy union mismatch');
 const rc=canon(root);need(rc===spec.d4,'D4 canon mismatch: '+rc+' vs manifest '+spec.d4);
 return {bit:spec.bit,root:spec.root,rows:strategy.size,rootMobility:rootMoves.length,rootCanon:rc,
  parts:spec.parts.map((p,i)=>({git_blob_sha:p.sha,bytes:partBuffers[i].length})),certificate_bytes:raw.length,
  subroot_count:subroots.length,subrootSeen:subroots.reduce((s,x)=>s+x.seen,0),winnerStates:subroots.reduce((s,x)=>s+x.winnerStates,0),
  loserStates:subroots.reduce((s,x)=>s+x.loserStates,0),opponentEdges:subroots.reduce((s,x)=>s+x.opponentEdges,0),
  terminals:subroots.reduce((s,x)=>s+x.terminals,0),terminal_range:[Math.min(...subroots.map(x=>x.range[0])),Math.max(...subroots.map(x=>x.range[1]))],
  union:{consumed:consumed.size,missing,extra},_subroots:subroots};
}
const start=Date.now(),verified=SPECS.map(verifyOne);
// published per-bit subroots + rootcheck metadata replay (all sixteen bits)
const crosschecks=[];
for(const spec of SPECS){
 const pins=META_PINS[spec.bit];
 const subBytes=fs.readFileSync(path.join(CERT,'bit'+spec.bit+'-subroots.jsonl'));
 const rootBytes=fs.readFileSync(path.join(CERT,'bit'+spec.bit+'-rootcheck.json'));
 need(gitBlobSha(subBytes)===pins.subroots,'bit'+spec.bit+' subroots metadata blob mismatch');
 need(gitBlobSha(rootBytes)===pins.rootcheck,'bit'+spec.bit+' rootcheck metadata blob mismatch');
 const pubLines=subBytes.toString('utf8').trim().split(/\r?\n/).map(JSON.parse);
 need(pubLines.every(l=>l.rows===spec.rows),'bit'+spec.bit+' subroots rows mismatch');
 const pubStats=Object.assign({},...pubLines.map(x=>x.stats));
 const expected=Object.entries(pubStats).map(([k,v])=>({move:Number(k.slice(1)),seen:v.seen,terminals:v.terminals,opponentEdges:v.opponentEdges,range:v.range})).sort((a,b)=>a.move-b.move);
 const v=verified.find(x=>x.bit===spec.bit);
 const actual=v._subroots.map(x=>({move:x.move,seen:x.seen,terminals:x.terminals,opponentEdges:x.opponentEdges,range:x.range}));
 const same=JSON.stringify(expected)===JSON.stringify(actual);
 const rootcheck=rootBytes.toString('utf8').trim().split(/\r?\n/).map(JSON.parse)[0];
 need(rootcheck.stones===7&&rootcheck.loserMobility===v.rootMobility,'bit'+spec.bit+' rootcheck mismatch');
 need(same&&expected.length===v.subroot_count,'bit'+spec.bit+' subroot replay mismatch');
 crosschecks.push({bit:spec.bit,subroots_published:expected.length,subroots_recomputed:actual.length,all_equal:same,rootcheck_stones:rootcheck.stones,rootcheck_loserMobility:rootcheck.loserMobility});
}
need(new Set(verified.map(x=>x.rootCanon)).size===16,'D4 root collision among the sixteen');
const certificates=verified.map(({_subroots,...x})=>x);
const totals={certificates:16,rows:certificates.reduce((s,x)=>s+x.rows,0),root_replies:certificates.reduce((s,x)=>s+x.rootMobility,0),
 subroot_seen:certificates.reduce((s,x)=>s+x.subrootSeen,0),winner_states:certificates.reduce((s,x)=>s+x.winnerStates,0),
 loser_states:certificates.reduce((s,x)=>s+x.loserStates,0),opponent_edges:certificates.reduce((s,x)=>s+x.opponentEdges,0),
 terminals:certificates.reduce((s,x)=>s+x.terminals,0)};
const result={schema:'n11-cost79c-certificates-bigint-general-circle-audit-remaining16-20261118-v1',date:'2026-11-18',base_main_before_audit:BASE_MAIN,
 method:'BigInt general-circle equations (3x3 Cramer coefficients) build the circle or degenerate line through each triple of stones and integer-evaluate all 121 cells; the search engine, verdict cache and 4x4 Bareiss certificate checker are never called; every legal loser first move is enumerated per root and the full AND/OR tree re-walked independently. Same verification logic as the parallel-lane bits [1,2,21] audit; extended here with a published-subroots/rootcheck metadata replay on all sixteen bits and a manifest d4_canon_root equality check per bit.',
 certificates,totals,subroot_crosschecks:crosschecks,
 metadata_pins:Object.fromEntries(SPECS.map(s=>[s.bit,META_PINS[s.bit]])),
 parser_checks:{header_and_root:true,strictly_sorted_unique_rows:true,all_moves_in_range:true,part_boundary_checked:true},
 all_pass:true,runtime_ms:Date.now()-start,geometry_cache:{triple_masks:tripleCache.size,legal_positions:legalCache.size},
 interpretation_guard:'Sixteen individual seven-stone WIN7 roots only (the remaining cost79c certificates after the parallel-lane audit of bits [1,2,21]). REFUTED-D10 is not a LOSS proof; no receipt fold was performed. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'};
const outputPath=path.join(OUT,'class2-lane-cost79c-certificates-third-independent-audit-remaining16-20261118.json');
fs.writeFileSync(outputPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({all_pass:true,totals,certificates:certificates.map(x=>({bit:x.bit,root:x.root,rows:x.rows,rootMobility:x.rootMobility,union:x.union,terminal_range:x.terminal_range})),subroot_crosschecks_all_equal:crosschecks.every(c=>c.all_equal),runtime_ms:result.runtime_ms,output:outputPath},null,2));
