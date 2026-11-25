#!/usr/bin/env node
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const output=join(dirname(fileURLToPath(import.meta.url)),"..","output");
const pins={
"class-frontier-cost77a-receipts-recompute-20261115.json":"a2ba7235793b051d80658818a83aa02c5a5d4958",
"class-frontier-cost77b-receipts-recompute-20261115.json":"b648ed068a1b9a04624b4c230e011e6fefeddb01",
"class-frontier-cost77c-receipts-recompute-20261115.json":"7f2badce7132aa7fdf76c9ee0283bd14a9ac9e7b",
"class-frontier-s5-ranking-after-cost77b-receipts-20261115.csv":"aca61cbdb0741ed975efb71a39914ebacbe821c6",
"class-frontier-top-candidates-s6-after-cost77b-receipts-20261115.csv":"9c59ceb9407700be64011c97d49896079f28d21c",
"class2-lane-cost77d-inflight-20261115.json":"676929023e9b67c94054d966f62a524743233987",
"class-frontier-s5-ranking-after-cost77c-receipts-20261115.csv":"9ada5dfc2057d3a340a3c27a8e984498c17118ad",
"class-frontier-top-candidates-s6-after-cost77c-receipts-20261115.csv":"8d5583e03e490042898be459d06e03b4aa2b5c13"
};
function readPinned(name){
 const bytes=readFileSync(join(output,name));
 const head=Buffer.from("blob "+bytes.length+"\0","utf8");
 assert.equal(createHash("sha1").update(head).update(bytes).digest("hex"),pins[name],"changed input "+name);
 return bytes.toString("utf8");
}
function ti(i,t){
 const x=i%11,y=Math.floor(i/11);let X=0,Y=0;
 if(t===0){X=x;Y=y;} if(t===1){X=10-y;Y=x;} if(t===2){X=10-x;Y=10-y;} if(t===3){X=y;Y=10-x;}
 if(t===4){X=10-x;Y=y;} if(t===5){X=10-y;Y=10-x;} if(t===6){X=x;Y=10-y;} if(t===7){X=y;Y=x;}
 return Y*11+X;
}
function transform(hex,t){const v=BigInt("0x"+hex);let z=0n;for(let i=0;i<121;i++)if((v>>BigInt(i))&1n)z|=1n<<BigInt(ti(i,t));return z.toString(16).padStart(32,"0");}
function canonical(hex){return Array.from({length:8},(_,t)=>transform(hex,t)).sort()[0];}
function determinant4(rows){
 const m=rows.map(r=>r.map(BigInt));let sign=1n,prev=1n;
 for(let k=0;k<3;k++){
  let p=k;while(p<4&&m[p][k]===0n)p++;if(p===4)return 0n;
  if(p!==k){[m[p],m[k]]=[m[k],m[p]];sign=-sign;}
  const pivot=m[k][k];
  for(let i=k+1;i<4;i++)for(let j=k+1;j<4;j++){const n=m[i][j]*pivot-m[i][k]*m[k][j];assert.equal(n%prev,0n);m[i][j]=n/prev;}
  for(let i=k+1;i<4;i++)m[i][k]=0n;prev=pivot;
 }
 return sign*m[3][3];
}
function safeN(hex,n){
 const v=BigInt("0x"+hex),pts=[];
 for(let i=0;i<121;i++)if((v>>BigInt(i))&1n)pts.push([i%11,Math.floor(i/11)]);
 assert.equal(pts.length,n);let checked=0;
 for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)for(let d=c+1;d<n;d++){
  const q=[pts[a],pts[b],pts[c],pts[d]].map(([x,y])=>[x,y,x*x+y*y,1]);
  if(determinant4(q)===0n)return {safe:false,checked:checked+1};checked++;
 }
 return {safe:true,checked};
}
function rankMap(lines){
 assert.equal(lines[0],"s5_hex,classes,remaining_s6_orbits,remaining_s7_edge_cost");
 return new Map(lines.slice(1).filter(Boolean).map(line=>{const [h,c,o,cost]=line.split(",");return [h,{classes:+c,orbits:+o,cost:+cost}];}));
}
const A=JSON.parse(readPinned("class-frontier-cost77a-receipts-recompute-20261115.json"));
const B=JSON.parse(readPinned("class-frontier-cost77b-receipts-recompute-20261115.json"));
const C=JSON.parse(readPinned("class-frontier-cost77c-receipts-recompute-20261115.json"));
const D=JSON.parse(readPinned("class2-lane-cost77d-inflight-20261115.json"));
const rankB=readPinned("class-frontier-s5-ranking-after-cost77b-receipts-20261115.csv").trim().split(/\r?\n/);
const topB=readPinned("class-frontier-top-candidates-s6-after-cost77b-receipts-20261115.csv").trim().split(/\r?\n/);
const rankC=readPinned("class-frontier-s5-ranking-after-cost77c-receipts-20261115.csv").trim().split(/\r?\n/);
const topC=readPinned("class-frontier-top-candidates-s6-after-cost77c-receipts-20261115.csv").trim().split(/\r?\n/);
const rootsA=A.cost77a_addition.map(x=>x.root_hex),rootsB=B.cost77b_addition.map(x=>x.root_hex),rootsC=C.cost77c_addition.map(x=>x.root_hex);
assert.equal(new Set([...rootsA,...rootsB,...rootsC].map(canonical)).size,15);
assert.equal(new Set(rootsC.map(canonical)).size,8);
const childC=BigInt("0x"+C.target.s6_child_hex);
for(const r of C.cost77c_addition){assert.equal(BigInt("0x"+r.root_hex),childC|(1n<<BigInt(r.bit)));assert.equal(BigInt("0x"+r.root_hex).toString(2).replace(/0/g,"").length,7);}
const safeC=rootsC.map(h=>safeN(h,7));assert.ok(safeC.every(x=>x.safe&&x.checked===35));
const marg=C.cost77c_addition.flatMap(x=>x.marginal_manifest_hexes);assert.equal(marg.length,4);assert.equal(new Set(marg).size,4);
const lifts=new Set();for(const root of rootsC){const v=BigInt("0x"+root);for(let bit=0;bit<121;bit++)if((v>>BigInt(bit))&1n)lifts.add(canonical((v&~(1n<<BigInt(bit))).toString(16).padStart(32,"0")));}
assert.equal(lifts.size,49);for(const h of marg)assert.ok(lifts.has(canonical(h)));
const bitsC=[];for(let i=0;i<121;i++)if((childC>>BigInt(i))&1n)bitsC.push(i);
const parentsC=bitsC.map(bit=>({bit,hex:canonical((childC&~(1n<<BigInt(bit))).toString(16).padStart(32,"0"))}));
const rmB=rankMap(rankB),openC=parentsC.filter(x=>rmB.has(x.hex)).map(x=>({s5_hex:x.hex,...rmB.get(x.hex)})).sort((a,b)=>a.s5_hex.localeCompare(b.s5_hex));
assert.deepEqual(openC,[
 {s5_hex:"00000000000000003800000009000000",classes:2,orbits:57,cost:4337},
 {s5_hex:"00000000000000801202000000200000",classes:2,orbits:14,cost:1095}
].sort((a,b)=>a.s5_hex.localeCompare(b.s5_hex)));
assert.ok(topB.some(line=>line.startsWith("00000000000000801202000000200000,00000000040000801202000000200000,77,")&&line.includes("c1=0,c2=2,c4=0")));
const before=B.frontier_after_cost77b,after=C.frontier_after_cost77c;
assert.deepEqual({
 solved:after.solved_s6_in_manifest-before.solved_s6_in_manifest,
 remaining_s6:after.unique_remaining_s6-before.unique_remaining_s6,
 remaining_cost:after.sum_remaining_cost-before.sum_remaining_cost,
 open_needed:after.s6_needed_by_open_classes-before.s6_needed_by_open_classes,
 open_cost:after.cost_needed_by_open_classes-before.cost_needed_by_open_classes
},{solved:4,remaining_s6:-4,remaining_cost:-288,open_needed:-4,open_cost:-288});
assert.deepEqual([C.target.candidates,C.target.win7_d10,C.target.refuted_d10,C.target.capped,C.target.candidate_nodes],[77,8,69,0,98545191]);
assert.deepEqual([C.totals.receipts,C.totals.total_marginal,C.totals.total_marginal_in_manifest,C.totals.certificate_rows,C.totals.certificate_bytes,C.totals.certificate_sub_roots,C.totals.child_closed_by_bit],[8,36,4,362362,13055390,457,10]);
const childD=BigInt("0x"+D.s6_child),bitsD=[];for(let i=0;i<121;i++)if((childD>>BigInt(i))&1n)bitsD.push(i);
assert.deepEqual(bitsD,D.child_stones_bit_indices);
const safeChild=safeN(D.s6_child,6);assert.ok(safeChild.safe);assert.equal(safeChild.checked,15);
const legal=[],safeCounts=[];
for(let bit=0;bit<121;bit++)if(!((childD>>BigInt(bit))&1n)){
 const root=(childD|(1n<<BigInt(bit))).toString(16).padStart(32,"0");
 const q=safeN(root,7);if(q.safe){legal.push(bit);safeCounts.push(q.checked);}
}
assert.deepEqual(legal,D.legal_candidates);assert.deepEqual([legal.length,D.candidate_count,D.s6_s7_edge_cost],[77,77,77]);assert.ok(safeCounts.every(n=>n===35));
const stabilizer=[];for(let t=0;t<8;t++)if(transform(D.s6_child,t)===D.s6_child)stabilizer.push(t);assert.equal(stabilizer.length,1);
const seen=new Set(),representatives=[];for(const bit of legal)if(!seen.has(bit)){representatives.push(bit);for(const t of stabilizer)seen.add(ti(bit,t));}assert.equal(representatives.length,77);
for(const prior of [A.target.s6_child_hex,B.target.s6_child_hex,C.target.s6_child_hex])assert.notEqual(canonical(prior),canonical(D.s6_child));
const parentsD=bitsD.map(bit=>({bit,hex:canonical((childD&~(1n<<BigInt(bit))).toString(16).padStart(32,"0"))}));
const rmC=rankMap(rankC),openD=parentsD.filter(x=>rmC.has(x.hex)).map(x=>({s5_hex:x.hex,...rmC.get(x.hex)})).sort((a,b)=>a.s5_hex.localeCompare(b.s5_hex));
assert.deepEqual(openD,[
 {s5_hex:"00000000000000003800400008000000",classes:2,orbits:66,cost:5192},
 {s5_hex:"00000000000000801202000000200000",classes:2,orbits:13,cost:1018}
].sort((a,b)=>a.s5_hex.localeCompare(b.s5_hex)));
assert.equal(parentsD.length-openD.length,4);
assert.ok(topC.some(line=>line.startsWith(D.s5+","+D.s6_child+",77,")&&line.includes("c1=0,c2=2,c4=0")));
assert.deepEqual([D.demand.c1,D.demand.c2,D.demand.c4],[0,2,0]);assert.equal(D.status,"in-flight");
console.log("PASS: 77a/b/c 15 receipt roots D4-distinct; 77c safe roots 8/8, 280 subsets, 49 parent lifts; 77d legal candidates 77/77 exact, 2,695 subsets safe, trivial D4 stabilizer, two open S5 parents match head-1290 ranking.");
