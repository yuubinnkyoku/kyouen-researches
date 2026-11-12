// orbit_ms5_worklist.ts - milestone-5: S2 {59,60} / S3 {59,60,61} remaining-work worklist (K0773).
//
// Supersedes the milestone-1..4 concrete-level fc/UNI accounting for S3 {59,60,61} blockers:
// uses the K0675 94-position 5-stone oracle at ORBIT level (all 8 D4 images), which closes
// 102/110 legal S4 children and leaves 8 blockers {5,23,27,31,89,93,97,115} (3 classes,
// K0766). This script rebuilds the remaining S5/S6 work from the oracle records directly:
//
//   - 196 unknown S5 orbits (blockers' children not in the oracle), raw obligations 17,524,
//     of which 479 child instances are already judged in the K0675 sweep (13 LOSS instances).
//   - 10 S5 orbits have a judged LOSS-for-mover child => SECOND_WIN immediately (settled);
//     they contribute no further S6 work (verdict rule: FIRST_WIN <=> ALL children WIN-for-mover).
//   - Reduced S6 worklist: 7,867 orbits / 615,497 S7-legal-edge cost (K0766 crosscheck at the
//     pre-reduction stage: 7,880 / 616,491, exact match from an independent accounting).
//   - The 94 oracle hex keys and the 14 LOSS S6 keys are EMBEDDED from repo s5_verdicts.json
//     (fetch-derived embedding, per the K0766 rule: no hand-transcribed hex constants).
//     Self-asserts: 78 FW + 16 SW, sweep 3,868, loss-in-sweep 14/14.
//
// Outputs (local sandbox FS): ms5_summary.json / ms5_s5_worklist.json / ms5_s6_manifest.csv
// No game outcome is asserted. 11x11 empty board and all two-stone roots remain UNKNOWN.
const fwCanon = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const swCanon = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];
const lossCanon = ["00000000000000083800800000000020","00000000000000083800800000800000","00000000000000801002002000002200","00000000000000801002002000082000","00000000000000801002002020002000","00000000000000083800800010000000","00000000000000203800200000008000","00000000000000203800200080000000","00000000000000203800000008000020","00000000000000203800000008010000","00000000000000203800000000c00000","00000000000000203800000084000000","00000000000000203800020004000000","00000000000000203800000a00000000"];
async function main(){
const fwSet=new Set(fwCanon),swSet=new Set(swCanon),lossSet=new Set(lossCanon);
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
// sweep = S6 children of the 94 oracle positions
const uniKeys=[...fwSet,...swSet];
const sweep=new Set<string>();
for(const k of uniKeys){const m=BigInt('0x'+k);const st5=bitsOf(m);
  for(const cc of bitsOf(legalOf(st5)))sweep.add(hex(canon(m|(1n<<BigInt(cc)))));}
const lossInSweep=[...lossSet].every(k=>sweep.has(k));
const q=59,r=61,S3m=(1n<<60n)|(1n<<BigInt(q))|(1n<<BigInt(r));
function images(m){const out=[];for(let g=0;g<8;g++){let t=0n;for(const p of bitsOf(m)){const[nx,ny]=TX[g](p%11,Math.floor(p/11));t|=1n<<BigInt(ny*11+nx);}out.push(t);}return out;}
let fcOrbit=0n;for(const k of fwSet)for(const im of images(BigInt('0x'+k)))if((im&S3m)===S3m)fcOrbit|=(im&~S3m);
const legal4=bitsOf(legalOf([60,q,r]));
const openT=legal4.filter(t=>!((fcOrbit>>BigInt(t))&1n));
const CLASS_OF={5:1,115:1,27:2,93:2,23:4,31:4,89:4,97:4};
const s5bits=new Map();
for(const t of openT){const mask=S3m|(1n<<BigInt(t));
  for(const cc of bitsOf(legalOf([60,q,r,t]))){const child=mask|(1n<<BigInt(cc));const k=hex(canon(child));
    if(fwSet.has(k)||swSet.has(k))continue;
    s5bits.set(k,(s5bits.get(k)||0)|CLASS_OF[t]);}}
const s5list=[];const reduced=new Map();
let obligRaw=0,obligUnj=0,judgedInst=0,lossInst=0;
for(const [k5,cls] of s5bits){
  const st5=bitsOf(BigInt('0x'+k5));const ch=bitsOf(legalOf(st5));
  let hasLoss=false;
  for(const cc of ch){const k6=hex(canon(BigInt('0x'+k5)|(1n<<BigInt(cc))));
    if(sweep.has(k6)&&lossSet.has(k6)){hasLoss=true;break;}}
  let unj=0,cost=0;
  if(!hasLoss){
    for(const cc of ch){const k6=hex(canon(BigInt('0x'+k5)|(1n<<BigInt(cc))));
      if(sweep.has(k6)){judgedInst++;continue;}
      unj++;const cst=bitsOf(legalOf([...st5,cc])).length;cost+=cst;
      const ex=reduced.get(k6);if(ex)ex.classes|=cls;else reduced.set(k6,{cost:cst,classes:cls});}
  } else {
    for(const cc of ch){const k6=hex(canon(BigInt('0x'+k5)|(1n<<BigInt(cc))));
      if(sweep.has(k6)){judgedInst++;if(lossSet.has(k6))lossInst++;continue;}
      unj++;}
  }
  obligRaw+=ch.length;obligUnj+=unj;
  s5list.push({hex:k5,classes:cls,children:ch.length,unjudgedChildren:unj,hasJudgedLossChild:hasLoss,unjudgedCost:cost});
}
let totalCost=0;const manifest=[];
for(const [k6,v] of reduced){totalCost+=v.cost;manifest.push({hex:k6,cost:v.cost,classes:v.classes});}
manifest.sort((a,b)=>a.cost-b.cost||(a.hex<b.hex?-1:1));
s5list.sort((a,b)=>a.classes-b.classes||(a.hex<b.hex?-1:1));
const settled=s5list.filter(e=>e.hasJudgedLossChild).length;
// crosscheck vs K0766 (pre-reduction union over ALL unknown S5 parents incl. settled)
const allS6=new Set();let allCost=0;
for(const e of s5list){const st5=bitsOf(BigInt('0x'+e.hex));const ch=bitsOf(legalOf(st5));
  for(const cc of ch){const k6=hex(canon(BigInt('0x'+e.hex)|(1n<<BigInt(cc))));
    if(sweep.has(k6))continue;
    if(!allS6.has(k6)){allS6.add(k6);allCost+=bitsOf(legalOf([...st5,cc])).length;}}}
const A={fw:fwSet.size,sw:swSet.size,sweep:sweep.size,loss:lossSet.size,lossInSweep,
  legal4:legal4.length,open:openT,unknownS5:s5bits.size,obligRaw,obligUnj,judgedInst,lossInst,
  settledS5:settled,k0766_crosscheck:{newS6:allS6.size,cost:allCost,expect:[7880,616491]},
  reducedS6:manifest.length,reducedCost:totalCost};
const pass=A.fw===78&&A.sw===16&&A.sweep===3868&&A.loss===14&&A.lossInSweep&&A.legal4===110&&
  A.open.length===8&&A.unknownS5===196&&A.obligRaw===17524&&A.obligUnj===17045&&A.judgedInst===479&&
  A.lossInst===13&&A.settledS5===10&&allS6.size===7880&&allCost===616491&&
  A.reducedS6===7867&&A.reducedCost===615497;
if(!pass)throw new Error('anchor mismatch: '+JSON.stringify(A));
await tools.file_system.write_file({path:'/home/user/ms5-out/ms5_summary.json',content:JSON.stringify(A,null,1)});
await tools.file_system.write_file({path:'/home/user/ms5-out/ms5_s5_worklist.json',content:JSON.stringify({schema:'n11-s2-5960-ms5-s5-v1',entries:s5list})});
await tools.file_system.write_file({path:'/home/user/ms5-out/ms5_s6_manifest.csv',content:'hex,cost,classes\n'+manifest.map(e=>e.hex+','+e.cost+','+e.classes).join('\n')+'\n'});
return {pass,...A};
}
main()