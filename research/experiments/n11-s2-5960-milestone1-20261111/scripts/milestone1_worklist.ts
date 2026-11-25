async function main() {
// milestone1_worklist.ts - S2 {59,60} closure, greedy head certificates {5,115} and {27,93}.
// Plain JS / pure TypeScript-compatible, 78-first-win oracle conditional (K0675).
// Reproduces the K0725/K0729 S6 census exactly (2191 / 2150 / overlap 79 / union 4262)
// and emits the full S6-orbit worklist with per-orbit legal-move cost for external
// solver scheduling. No game outcome is asserted anywhere; the empty board and all
// two-stone roots remain UNKNOWN. The integer-circumcenter circle-mask geometry is
// validated against verify_conditional_s6_cover_46.py reconstruct() invariants
// (94 / 7890 / 7813 / 3868 / {2:3791,3:77}, priority S4 bits {47,59,60,61}).
const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];
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
  const per=[];
  for(const t of blks){
    const mask=S3m|(1n<<BigInt(t));const orbs=new Set();
    for(const c of bitsOf(legalOf([60,q,r,t]))){const child=mask|(1n<<BigInt(c));if(UNI.has(String(child)))continue;orbs.add(String(canon(child)));}
    per.push({t,orbits:orbs});
  }
  return per;
}
const pb=worklist(59,61);
const repsA=[...pb.find(p=>p.t===5).orbits];
const repsB=[...pb.find(p=>p.t===27).orbits];
function census(reps,bit){
  const orbits=new Map();const s5=[];let oblig=0;
  for(const rep of reps){const st5=bitsOf(BigInt(rep));const ch=bitsOf(legalOf(st5));oblig+=ch.length;
    for(const c of ch){const k=String(canon(BigInt(rep)|(1n<<BigInt(c))));
      const e=orbits.get(k);if(e)e.certs|=bit;else orbits.set(k,{cost:0,certs:bit});}
    s5.push({hex:hex(BigInt(rep)),obligations:ch.length});}
  return{orbits,s5,oblig};}
const A=census(repsA,1),Bc=census(repsB,2);
const all=new Map();
for(const[k,v]of A.orbits)all.set(k,{cost:0,certs:v.certs});
for(const[k,v]of Bc.orbits){const e=all.get(k);if(e)e.certs|=v.certs;else all.set(k,{cost:0,certs:v.certs});}
for(const[k,v]of all)v.cost=bitsOf(legalOf(bitsOf(BigInt(k)))).length;
const list=[...all.entries()].map(([k,v])=>({hex:hex(BigInt(k)),cost:v.cost,certs:v.certs}));
list.sort((a,b)=>a.cost-b.cost||(a.hex<b.hex?-1:1));
const s5all=new Map();
A.s5.forEach(s=>s5all.set(s.hex,{certs:1,obligations:s.obligations}));
Bc.s5.forEach(s=>{const e=s5all.get(s.hex);if(e)e.certs|=2;else s5all.set(s.hex,{certs:2,obligations:s.obligations});});
const costs=list.map(l=>l.cost);
const manifest={
  schema:'n11-s2-5960-milestone1-s6-manifest-v1',
  board:11,root_s2:'{59,60}',best_s3:61,
  conditional_on:'78 first-win five-stone oracle (K0675); no game outcome asserted; empty board and two-stone roots UNKNOWN',
  certA:{blockers:[5,115],s5Orbits:repsA.length,rawObligations:A.oblig,s6Orbits:A.orbits.size},
  certB:{blockers:[27,93],s5Orbits:repsB.length,rawObligations:Bc.oblig,s6Orbits:Bc.orbits.size},
  s5CommonOrbits:[...s5all.values()].filter(v=>v.certs===3).length,
  s6Overlap79:[...A.orbits.keys()].filter(k=>Bc.orbits.has(k)).length,
  s6Union:all.size,
  s6CostStats:{min:Math.min(...costs),median:costs.slice().sort((a,b)=>a-b)[Math.floor(costs.length/2)],max:Math.max(...costs),mean:+(costs.reduce((a,b)=>a+b,0)/costs.length).toFixed(2),sumRawS7Edges:costs.reduce((a,b)=>a+b,0)},
  s5Reps:[...s5all.entries()].map(([h,v])=>({hex:h,certs:v.certs,obligations:v.obligations})),
  s6All:list,
  protocol:'verdict = WIN_for_mover iff the 6-stone rep has a legal child classified WIN7 (mover-at-S7 loses). A WIN certificate needs exactly one certified WIN7 child key; a LOSS certificate needs all legal children certified. Merge rule: two workers disagreeing on one canonical key = WIN/LOSS conflict, halt certificate assembly. D4 invariance: certify one rep per orbit only.',
  empty_board:'UNKNOWN'
};
return manifest;
}
