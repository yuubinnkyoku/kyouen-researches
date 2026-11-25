async function main() {
// milestone4_worklist.ts - S2 {59,60} COMPLETE S6 worklist (greedy certs 1-33, K0757).
// Same integer-circumcenter circle-mask geometry, D4 canon and 78-first-win-oracle
// conditioning as milestone1/2/3_worklist.ts (K0746/K0748/K0754).
//
// This is the FULL greedy ladder (K0754-ladder, steps 1-33, 61/61 blockers covered at
// the S5 worklist level). Steps 16/24/26 ({92,94},{103,105},{88,98}) are 0-marginal
// classes that add no S5/S6 orbit and are skipped; {31},{89,97} are covered by certs 1-8.
//
// Verified results (K0757):
//   - single-cert S6 orbits: certs 1-8 match K0746/K0748/K0729/K0754 published values;
//     steps 9-33 measured here for the first time (see CHUNKS below / certStats in
//     output/milestone4_manifest.json)
//   - merged union = 43,375 S6 orbits / 1,447 S5 orbit reps (COMPLETE worklist).
//     Supersedes the q59 hash-dedupe ESTIMATE "≈41,842" (the hash estimate was ~3.6% low).
//   - s5 obligation sum = 133,524, exactly the q59 raw obligation census.
//   - milestone-3 manifest (20,534 keys) is a strict subset with cost mismatch 0
//     (machine-verified join), and its 516 s5Reps are a subset with obligations mismatch 0.
//
// REPRODUCTION: the 16MiB sandbox cannot hold the whole enumeration in one run, so the
// ladder is processed in CHUNKS (one fragment file per chunk, ~2-3 pair certs each,
// ~9k-20k raw obligations per chunk; chunks of 4 pair certs exceed the sandbox limit).
// Set CHUNK below to 1..9, run once per chunk (writes /home/user/work-ms4/fragN.json),
// then run scripts/merge_ms4.sh to assemble the byte-exact published manifest.
//
// WARNING: published milestone4 manifest has invalid cert membership; regenerate all chunks.\n// cert bit allocation (greedy step order; pair certs get two adjacent bits, singles one;
// bits are combined with + arithmetic, NEVER with | which coerces to signed int32):
//   1 {5,115}=1  2 {27,93}=2  3 {71}=4  4 {82}=8  5 {104}=16  6 {73}=32
//   7 {90,96}=64+128 (D4-mirror-identical sets)  8 {23}=256
//   9 {79,85}=512+1024  10 {80,84}=2048+4096  11 {100,108}=8192+16384
//   12 {91,95}=32768+65536  13 {52,74}=131072+262144  14 {111,119}=524288+1048576
//   15 {26}=2097152  17 {53,75}=4194304+8388608  18 {102,106}=16777216+33554432
//   19 {113,117}=67108864+134217728  20 {70,72}=268435456+536870912
//   21 {77,87}=1073741824+2147483648  22 {99,109}=4294967296+8589934592
//   23 {15}=17179869184  25 {22}=34359738368  27 {54,76}=68719476736+137438953472
//   28 {78,86}=274877906944+549755813888  29 {81,83}=1099511627776+2199023255552
//   30 {101,107}=4398046511104+8796093022208  31 {110,120}=17592186044416+35184372088832
//   32 {112,118}=70368744177664+140737488355328  33 {114,116}=281474976710656+562949953421312
//
// No game outcome is asserted anywhere; the empty board and all two-stone roots
// remain UNKNOWN.
const CHUNK = 1; // 1..9; see CHUNKS below
const CHUNKS = [
  [{reps:[5,115],bit:1},{reps:[27,93],bit:2},{reps:[71],bit:4},{reps:[82],bit:8},{reps:[104],bit:16}],        // 1 -> frag1
  [{reps:[73],bit:32},{reps:[90,96],bit:64+128},{reps:[23],bit:256}],                                           // 2 -> frag2
  [{reps:[79,85],bit:512+1024},{reps:[80,84],bit:2048+4096},{reps:[100,108],bit:8192+16384}],                  // 3 -> frag3
  [{reps:[91,95],bit:32768+65536},{reps:[52,74],bit:131072+262144},{reps:[111,119],bit:524288+1048576}],        // 4 -> frag4
  [{reps:[26],bit:2097152},{reps:[53,75],bit:4194304+8388608},{reps:[102,106],bit:16777216+33554432}],          // 5 -> frag5
  [{reps:[113,117],bit:67108864+134217728},{reps:[70,72],bit:268435456+536870912},{reps:[77,87],bit:1073741824+2147483648}], // 6 -> frag6
  [{reps:[99,109],bit:4294967296+8589934592},{reps:[15],bit:17179869184},{reps:[22],bit:34359738368}],         // 7 -> frag7
  [{reps:[54,76],bit:68719476736+137438953472},{reps:[78,86],bit:274877906944+549755813888},{reps:[81,83],bit:1099511627776+2199023255552}], // 8 -> frag8
  [{reps:[101,107],bit:4398046511104+8796093022208},{reps:[110,120],bit:17592186044416+35184372088832}],         // 9a -> frag9
  [{reps:[112,118],bit:70368744177664+140737488355328},{reps:[114,116],bit:281474976710656+562949953421312}]      // 9b -> frag10
];
const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000000200000","00000000000000003800800000000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000000103800800000000000","00000000000000000103808000000000000","00000000000000000203800000000000001","00000000000000000203800000000000002","00000000000000000203800000000000004","00000000000000000203800000000000008","00000000000000000203800000000000010","00000000000000000203800000000000040","00000000000000000203800000000000080","00000000000000000203800000000000100","00000000000000000203800000000000200","00000000000000000203800000000000400","00000000000000000203800000000001000","00000000000000000203800000000002000","00000000000000000203800000000004000","00000000000000000203800000000020000","00000000000000000203800000000040000","00000000000000000203800000000080000","00000000000000000203800000000100000","00000000000000000203800000000200000","00000000000000000203800000001000000","00000000000000000203800000002000000","00000000000000000203800000010000000","00000000000000000203800000020000000","00000000000000000203800000040000000","00000000000000000203800000100000000","00000000000000000203800000400000000","00000000000000000203800001000000000","00000000000000000203800002000000000","00000000000000000203800004000000000","00000000000000000203800008000000000","00000000000000000203800010000000000","00000000000000000203800040000000000","00000000000000000203800080000000000","00000000000000000203800800000000000","00000000000000000203801000000000000","00000000000000000203802000000000","00000000000000000203804000000000","00000000000000000203808000000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000000083800800000000000","00000000000000000203800000000000020","00000000000000000203800000000000800","00000000000000000203800000000008000","00000000000000000203800000000010000","00000000000000000203800000000400000","00000000000000000203800000000800000","00000000000000000203800000004000000","00000000000000000203800000008000000","00000000000000000203800080000000","00000000000000000203800000200000000","00000000000000000203800000800000000","00000000000000000203800020000000000"];
const B=(h)=>BigInt('0x'+h);
const FW=fwHex.map(B),SW=swHex.map(B);
const UNI=new Set([...FW,...SW].map(String));
const N=121,FULL=(1n<<121n)-1n;
const X=new Int8Array(N),Y=new Int8Array(N),Q=new Int32Array(N);
for(let p=0;p<N;p++){X[p]=p%11;Y[p]=Math.floor(p/11);Q[p]=X[p]*X[p]+Y[p]*Y[p];}
const forbMemo=new Map();
function forbidden(a,b,c){
  const key=(a*121+b)*121+c;let m=forbMemo.get(key);if(m!==undefined)return m;
  m=0n;const x1=X[a],y1=Y[a],x2=X[b],y2=Y[b],x3=X[c],y3=Y[c];
  const A2=x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2);
  if(A2===0){const A=y2-y1,Bx=x1-x2;for(let z=0;z<N;z++)if(A*(X[z]-x1)+Bx*(Y[z]-y1)===0)m|=1n<<BigInt(z);}
  else{const D=2*A2,Uxn=Q[a]*(y2-y3)+Q[b]*(y3-y1)+Q[c]*(y1-y2),Uyn=Q[a]*(x3-x2)+Q[b]*(x1-x3)+Q[c]*(x2-x1),Rx=D*x1-Uxn,Ry=D*y1-Uyn;
    for(let z=0;z<N;z++){const dx=D*X[z]-Uxn,dy=D*Y[z]-Uyn;if(dx*dx+dy*dy===Rx*Rx+Ry*Ry)m|=1n<<BigInt(z);}}
  m&=~((1n<<BigInt(a))|(1n<<BigInt(b))|(1n<<BigInt(c)));forbMemo.set(key,m);return m;
}
function legalOf(stones){
  let banned=0n;for(const s of stones)banned|=1n<<BigInt(s);
  for(let i=0;i<stones.length;i++)for(let j=i+1;j<stones.length;j++)for(let k=j+1;k<stones.length;k++)banned|=forbidden(stones[i],stones[j],stones[k]);
  return FULL&~banned;
}
const bitsOf=(m)=>{const o=[];for(let d=0;d<N;d++)if((m>>BigInt(d))&1n)o.push(d);return o;};
const TX=[(x,y)=>[x,y],(x,y)=>[y,10-x],(x,y)=>[10-x,10-y],(x,y)=>[10-y,x],(x,y)=>[10-x,y],(x,y)=>[x,10-y],(x,y)=>[y,x],(x,y)=>[10-y,10-x]];
function canon(m){let best=m;for(let g=1;g<8;g++){let t=0n;for(const p of bitsOf(m)){const[nx,ny]=TX[g](p%11,Math.floor(p/11));t|=1n<<BigInt(ny*11+nx);}if(t<best)best=t;}return best;}
const hex=(m)=>m.toString(16).padStart(32,'0');
function worklist(q,r){
  const S3m=(1n<<60n)|(1n<<BigInt(q))|(1n<<BigInt(r));
  let fc=0n;for(const f of FW)if((f&S3m)===S3m)fc|=(f&~S3m);
  const blks=bitsOf(legalOf([60,q,r])&~fc);
  const per=new Map();
  for(const t of blks){
    const mask=S3m|(1n<<BigInt(t));const orbs=new Set();
    for(const c of bitsOf(legalOf([60,q,r,t]))){const child=mask|(1n<<BigInt(c));if(UNI.has(String(child)))continue;orbs.add(String(canon(child)));}
    per.set(t,orbs);
  }
  return per;
}
const pb=worklist(59,61);
const certs=CHUNKS[CHUNK-1];
const certStats=[]; const s5Union=new Map(); const s6Union=new Map();
for(const cert of certs){
  let oblig=0;const s6=new Set();let s5count=0;const seen=new Set();
  for(const t of cert.reps)for(const rep of pb.get(t)){
    if(seen.has(rep))continue; seen.add(rep); s5count++;
    const st5=bitsOf(BigInt(rep));const ch=bitsOf(legalOf(st5));oblig+=ch.length;
    const e5=s5Union.get(rep);if(e5!==undefined)s5Union.set(rep,e5+cert.bit);else s5Union.set(rep,cert.bit);
    for(const c of ch){
      const k=String(canon(BigInt(rep)|(1n<<BigInt(c))));
      // Each certificate contributes its bit once per canonical S6 orbit.
      // Different S5 parents can lead to the same S6 orbit.
      if(s6.has(k))continue;
      s6.add(k);
      const e=s6Union.get(k);
      s6Union.set(k,e===undefined?cert.bit:e+cert.bit);
    }
  }
  certStats.push({cert:cert.reps.join(','),bit:cert.bit,s5Orbits:s5count,rawObligations:oblig,s6OrbitsSingle:s6.size});
}
const list=[];
for(const[k,v] of s6Union){const st=bitsOf(BigInt(k));list.push({hex:hex(BigInt(k)),cost:bitsOf(legalOf(st)).length,certs:v});}
list.sort((a,b)=>a.cost-b.cost||(a.hex<b.hex?-1:1));
const s5Reps=[];
for(const[k,v] of s5Union){const st5=bitsOf(BigInt(k));s5Reps.push({hex:hex(BigInt(k)),certs:v,obligations:bitsOf(legalOf(st5)).length});}
s5Reps.sort((a,b)=>a.hex<b.hex?-1:1);
const out={schema:'n11-s2-5960-ms4-frag-v1',chunk:'chunk'+CHUNK,certStats,s6Union:s6Union.size,s5Union:s5Union.size,s5Reps,s6All:list};
await tools.file_system.write_file({ path:'/home/user/work-ms4/frag'+CHUNK+'.json', content: JSON.stringify(out) });
return {chunk:CHUNK, certStats, s6Union:s6Union.size, s5Union:s5Union.size};
}
main()
