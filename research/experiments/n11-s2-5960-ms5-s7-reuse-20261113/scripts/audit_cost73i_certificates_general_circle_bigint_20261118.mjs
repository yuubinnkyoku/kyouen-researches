#!/usr/bin/env node
// Independent cost73i WIN7 certificate audit.
// Node 22, standard library only. Uses BigInt generalized-circle equations,
// not the search engine, verdict cache, or 4x4 Bareiss certificate checker.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const HERE=path.dirname(fileURLToPath(import.meta.url));
const OUT=path.resolve(HERE,'../output');
const CERT=path.join(OUT,'class2-lane-cost73i-certificates');
const BASE_MAIN='feef6bf38cb2e4c89401ad920d9894b561c1207b';
const SPECS=[
 {
  "bit": 1,
  "root": "00000000000000403800400008000002",
  "rows": 59184,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800400008000002.cert.part1of2",
    "sha": "ae30232f7df463a4cc592a019cbe553d454582ea"
   },
   {
    "name": "n11_s7_00000000000000403800400008000002.cert.part2of2",
    "sha": "3d1471576adb95813e2f8ae68e73a363b8120606"
   }
  ]
 },
 {
  "bit": 9,
  "root": "00000000000000403800400008000200",
  "rows": 57174,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800400008000200.cert.part1of2",
    "sha": "360c81d25471ff303b613fd6cfed441c66dae376"
   },
   {
    "name": "n11_s7_00000000000000403800400008000200.cert.part2of2",
    "sha": "a0845ff4672bfb76c9e806fa2acb004fa4748844"
   }
  ]
 },
 {
  "bit": 11,
  "root": "00000000000000403800400008000800",
  "rows": 67172,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800400008000800.cert.part1of3",
    "sha": "0a514f9775323801fc769e7a507a99e40527c8bd"
   },
   {
    "name": "n11_s7_00000000000000403800400008000800.cert.part2of3",
    "sha": "3003ae7d9f451c211828afc91edf5ce00b8c3faf"
   },
   {
    "name": "n11_s7_00000000000000403800400008000800.cert.part3of3",
    "sha": "5645fff8cf9289b3b4381aefabedbb6064d2e2f8"
   }
  ]
 },
 {
  "bit": 18,
  "root": "00000000000000403800400008040000",
  "rows": 59794,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800400008040000.cert.part1of2",
    "sha": "8d3d27ad4ab3fb3419638111d7e6d9a92cd491f4"
   },
   {
    "name": "n11_s7_00000000000000403800400008040000.cert.part2of2",
    "sha": "734475ffde7e49c7ad408c7b4869b6f19f7f6342"
   }
  ]
 },
 {
  "bit": 29,
  "root": "00000000000000403800400028000000",
  "rows": 45839,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800400028000000.cert.part1of2",
    "sha": "4781f177079ad3a51d94b673d7ec95f5e8c108e9"
   },
   {
    "name": "n11_s7_00000000000000403800400028000000.cert.part2of2",
    "sha": "2a6bff83000094940de6a90bb6f95a58a403a300"
   }
  ]
 },
 {
  "bit": 38,
  "root": "00000000000000403800404008000000",
  "rows": 49142,
  "parts": [
   {
    "name": "n11_s7_00000000000000403800404008000000.cert.part1of2",
    "sha": "8c8f872b41028e2000ffd55815589ce8d4032a7a"
   },
   {
    "name": "n11_s7_00000000000000403800404008000000.cert.part2of2",
    "sha": "b58c3cf3377657eed63a167ad8616315f2432f4b"
   }
  ]
 },
 {
  "bit": 54,
  "root": "00000000000000403840400008000000",
  "rows": 70562,
  "parts": [
   {
    "name": "n11_s7_00000000000000403840400008000000.cert.part1of3",
    "sha": "8b24087bd3412b5a51cc831909da249bb50019c9"
   },
   {
    "name": "n11_s7_00000000000000403840400008000000.cert.part2of3",
    "sha": "b117ef9a63155ec4d5710929ca7b3ed8d3636087"
   },
   {
    "name": "n11_s7_00000000000000403840400008000000.cert.part3of3",
    "sha": "2a82980fbbae751c908c332b3516830d279a2560"
   }
  ]
 },
 {
  "bit": 82,
  "root": "00000000000400403800400008000000",
  "rows": 26067,
  "parts": [
   {
    "name": "n11_s7_00000000000400403800400008000000.cert",
    "sha": "f0a57ca0b61fbb87db684d325286b76ce1532752"
   }
  ]
 },
 {
  "bit": 97,
  "root": "00000002000000403800400008000000",
  "rows": 47929,
  "parts": [
   {
    "name": "n11_s7_00000002000000403800400008000000.cert.part1of2",
    "sha": "4f5081e4c8f78683d6c1c1a0474e17e00f16703b"
   },
   {
    "name": "n11_s7_00000002000000403800400008000000.cert.part2of2",
    "sha": "c70fb39f4cafc57833d2459c636c70b99b9e0c47"
   }
  ]
 },
 {
  "bit": 100,
  "root": "00000010000000403800400008000000",
  "rows": 47899,
  "parts": [
   {
    "name": "n11_s7_00000010000000403800400008000000.cert.part1of2",
    "sha": "783d8192eaae0dff912c6a5720d5eb140964e9e4"
   },
   {
    "name": "n11_s7_00000010000000403800400008000000.cert.part2of2",
    "sha": "ab05546c3ab59ba311ff35d3e81d9b9fea350a60"
   }
  ]
 },
 {
  "bit": 110,
  "root": "00004000000000403800400008000000",
  "rows": 58241,
  "parts": [
   {
    "name": "n11_s7_00004000000000403800400008000000.cert.part1of2",
    "sha": "24e11db3bcd1655dd398cde89091c6c57dac82ae"
   },
   {
    "name": "n11_s7_00004000000000403800400008000000.cert.part2of2",
    "sha": "a7ea7250c28ee8c2839c487e6828a7e329d0a614"
   }
  ]
 },
 {
  "bit": 111,
  "root": "00008000000000403800400008000000",
  "rows": 60337,
  "parts": [
   {
    "name": "n11_s7_00008000000000403800400008000000.cert.part1of2",
    "sha": "f60a055e226df9e43e2372c316fae36fc31e4af5"
   },
   {
    "name": "n11_s7_00008000000000403800400008000000.cert.part2of2",
    "sha": "e0a9ba3fa1b6d65f6ba1877fa006483c71ed527f"
   }
  ]
 }
];

const SUBROOTS_PIN='958965fc5f1fd151496f371d803d31b52e3411af';
const ROOTCHECK_PIN='e252780689b03679ad3efa3941926a6b6131a75b';
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
 if(partBuffers.length>1)need(/^[0-9a-f]{32} [0-9]+\n/.test(partBuffers[1].toString('ascii')),'part 2 does not start at a strategy-row boundary');
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
 return {bit:spec.bit,root:spec.root,rows:strategy.size,rootMobility:rootMoves.length,rootCanon:canon(root),
  parts:spec.parts.map((p,i)=>({git_blob_sha:p.sha,bytes:partBuffers[i].length})),certificate_bytes:raw.length,
  subroot_count:subroots.length,subrootSeen:subroots.reduce((s,x)=>s+x.seen,0),winnerStates:subroots.reduce((s,x)=>s+x.winnerStates,0),
  loserStates:subroots.reduce((s,x)=>s+x.loserStates,0),opponentEdges:subroots.reduce((s,x)=>s+x.opponentEdges,0),
  terminals:subroots.reduce((s,x)=>s+x.terminals,0),terminal_range:[Math.min(...subroots.map(x=>x.range[0])),Math.max(...subroots.map(x=>x.range[1]))],
  union:{consumed:consumed.size,missing,extra},_subroots:subroots};
}
const start=Date.now(),verified=SPECS.map(verifyOne);
const subPath=path.join(CERT,'bit1-subroots.jsonl'),rootPath=path.join(CERT,'bit1-rootcheck.json');
const subBytes=fs.readFileSync(subPath),rootBytes=fs.readFileSync(rootPath);
need(gitBlobSha(subBytes)===SUBROOTS_PIN,'bit21 subroots metadata blob mismatch');
need(gitBlobSha(rootBytes)===ROOTCHECK_PIN,'bit21 rootcheck metadata blob mismatch');
const pubLines=subBytes.toString('utf8').trim().split(/\r?\n/).map(JSON.parse),pubStats=Object.assign({},...pubLines.map(x=>x.stats));
const expected=Object.entries(pubStats).map(([k,v])=>({move:Number(k.slice(1)),seen:v.seen,terminals:v.terminals,opponentEdges:v.opponentEdges,range:v.range})).sort((a,b)=>a.move-b.move);
const actual=verified[0]._subroots.map(x=>({move:x.move,seen:x.seen,terminals:x.terminals,opponentEdges:x.opponentEdges,range:x.range}));
const same=JSON.stringify(expected)===JSON.stringify(actual),rootcheck=rootBytes.toString('utf8').trim().split(/\r?\n/).map(JSON.parse)[0];
need(rootcheck.stones===7&&rootcheck.loserMobility===verified[0].rootMobility,'bit21 rootcheck mismatch');
need(same&&expected.length===59,'bit1 subroot replay mismatch');
need(new Set(verified.map(x=>x.rootCanon)).size===12,'D4 root collision');
const CANON_EXPECT={"1": "00000000000000403800400008000002", "9": "00000000000000403800400008000200", "11": "00000000000000403800400008000800", "18": "00000000000000403800400008040000", "29": "00000000000000403800400028000000", "38": "00000000000000403800404008000000", "54": "00000000000000403840400008000000", "82": "00000000000000805206000004000000", "97": "00000000020001003810000008000000", "100": "00000000000000801206000004100000", "110": "00000000000000801206000004000400", "111": "00000000000000801206000004200000"};
for(const v of verified)need(v.rootCanon===CANON_EXPECT[String(v.bit)],'root canon disagrees with the independent python census-side canon: bit '+v.bit);
const certificates=verified.map(({_subroots,...x})=>x);
const totals={certificates:12,rows:certificates.reduce((s,x)=>s+x.rows,0),root_replies:certificates.reduce((s,x)=>s+x.rootMobility,0),
 subroot_seen:certificates.reduce((s,x)=>s+x.subrootSeen,0),winner_states:certificates.reduce((s,x)=>s+x.winnerStates,0),
 loser_states:certificates.reduce((s,x)=>s+x.loserStates,0),opponent_edges:certificates.reduce((s,x)=>s+x.opponentEdges,0),
 terminals:certificates.reduce((s,x)=>s+x.terminals,0)};
const result={schema:'n11-cost73i-certificates-bigint-general-circle-audit-20261118-v1',date:'2026-11-18',base_main_before_audit:BASE_MAIN,
 method:'BigInt一般化円方程式（3x3 Cramer係数）で各3石が定める円または退化直線を構成し、121セルを整数評価。探索器・verdict cache・4x4 Bareiss証明書検査器を呼ばず、各rootの全合法な敗者初手からAND/OR木を独立再走査。',
 certificates,totals,bit1_crosscheck:{rootcheck,subroots_published:59,subroots_recomputed:actual.length,all_59_equal:same},
 root_canon_agrees_with_python_census_side_canon:'12/12',
 metadata_pins:{bit1_subroots_git_blob_sha:SUBROOTS_PIN,bit1_rootcheck_git_blob_sha:ROOTCHECK_PIN},
 parser_checks:{header_and_root:true,strictly_sorted_unique_rows:true,all_moves_in_range:true,part_boundary_checked:true},
 all_pass:true,runtime_ms:Date.now()-start,geometry_cache:{triple_masks:tripleCache.size,legal_positions:legalCache.size},
 interpretation_guard:'Twelve individual seven-stone WIN7 roots of the cost-73i sweep row only. REFUTED-D10 is not a LOSS proof; no receipt fold was performed. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'};
const outputPath=path.join(OUT,'class2-lane-cost73i-certificates-third-independent-audit-20261118.json');
fs.writeFileSync(outputPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({all_pass:true,totals,certificates:certificates.map(x=>({bit:x.bit,root:x.root,rows:x.rows,rootMobility:x.rootMobility,union:x.union,terminal_range:x.terminal_range})),bit1_subroots_equal:true,runtime_ms:result.runtime_ms,output:outputPath},null,2));
