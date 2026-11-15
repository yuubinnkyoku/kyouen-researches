#!/usr/bin/env node
// Cross-lane D4 receipt overlap audit for cost70f, cost70g, and cost71c.
// Pure BigInt geometry; no solver, verdict cache, or certificate payload.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const HERE=path.dirname(fileURLToPath(import.meta.url));
const OUT=path.resolve(HERE,"../output");
const ROOT="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/";
const INPUTS={
 cost70g:"class2-lane-cost70g-win7-certificates-20261115.json",
 cost70f:"class2-lane-cost70f-win7-certificates-20261115.json",
 cost71c:"class2-lane-cost71c-win7-certificates-20261115.json"
};
const EXPECTED_BLOBS={
 cost70g:"f9714f1282b68a1fd046f975c0d0fccb6325735d",
 cost70f:"e7efa6134e19c8e7de1a9cfd7f05a55b564c984d",
 cost71c:"3a09163ccfde2a3ce4e63f61ef31d42688f60b30"
};
const SOURCE_MAIN="8a567006fcdf902a42b493568d02f5c1885e91d1";
function gitBlobSha(buf){return createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");}
function canon(v){
 let best=null;
 for(let t=0;t<8;t++){
  let out=0n;
  for(let i=0;i<121;i++){
   if(((v>>BigInt(i))&1n)===0n)continue;
   const x=i%11,y=Math.floor(i/11);let a=x,b=y;
   if(t===1){a=10-y;b=x;}else if(t===2){a=10-x;b=10-y;}
   else if(t===3){a=y;b=10-x;}else if(t===4){a=10-x;b=y;}
   else if(t===5){a=10-y;b=10-x;}else if(t===6){a=x;b=10-y;}
   else if(t===7){a=y;b=x;}
   out|=1n<<BigInt(b*11+a);
  }
  if(best===null||out<best)best=out;
 }
 return best.toString(16).padStart(32,"0");
}
function popcount(v){let n=0;while(v){v&=v-1n;n++;}return n;}
function certArray(m){return Array.isArray(m.certificates)?m.certificates:Object.values(m.certificates);}
function parseLane(m){
 const certs=certArray(m),childHex=m.s6_child_hex||m.child_hex,child=BigInt("0x"+childHex);
 const roots=new Map(),parents=new Map(),byBit={},checks=[];
 for(const cert of certs){
  const bit=Number(cert.bit),root=BigInt("0x"+cert.root_hex);
  if(root!==(child|(1n<<BigInt(bit))))checks.push("root != child + bit "+bit);
  if(popcount(root)!==7)checks.push("root stone count != 7 at bit "+bit);
  const rc=canon(root);if(cert.d4_canonical_hex&&cert.d4_canonical_hex!==rc)checks.push("D4 root mismatch at bit "+bit);
  if(!roots.has(rc))roots.set(rc,[]);roots.get(rc).push({bit,root_hex:cert.root_hex});
  const lifts=[];
  for(let i=0;i<121;i++)if(((root>>BigInt(i))&1n)!==0n){
   const p=canon(root&~(1n<<BigInt(i)));lifts.push(p);
   if(!parents.has(p))parents.set(p,[]);parents.get(p).push({bit,deleted_bit:i});
  }
  lifts.sort();
  if(cert.parent_lift_orbits&&JSON.stringify([...cert.parent_lift_orbits].sort())!==JSON.stringify(lifts))checks.push("published parent_lift_orbits mismatch at bit "+bit);
  byBit[bit]=lifts;
 }
 return {bits:certs.map(x=>Number(x.bit)).sort((a,b)=>a-b),childCanon:canon(child),roots,parents,byBit,checks};
}
function inter(a,b){return [...a.keys()].filter(x=>b.has(x)).sort();}
function main(){
 const manifests={},blobs={};
 for(const [name,file] of Object.entries(INPUTS)){
  const buf=fs.readFileSync(path.join(OUT,file));
  blobs[name]=gitBlobSha(buf);
  if(blobs[name]!==EXPECTED_BLOBS[name])throw new Error(name+" manifest blob changed: "+blobs[name]);
  manifests[name]=JSON.parse(buf.toString("utf8"));
 }
 const g=parseLane(manifests.cost70g),f=parseLane(manifests.cost70f),c=parseLane(manifests.cost71c);
 const gfR=inter(g.roots,f.roots),gcR=inter(g.roots,c.roots),fcR=inter(f.roots,c.roots);
 const gfP=inter(g.parents,f.parents),gcP=inter(g.parents,c.parents),fcP=inter(f.parents,c.parents);
 const common=gfR[0],same=common?f.byBit[84]:[],extra=gfP.filter(x=>!same.includes(x));
 const checks=[...g.checks,...f.checks,...c.checks];
 if(gfR.length!==1||gcR.length!==0||fcR.length!==0)checks.push("unexpected cross-lane root intersection");
 if(gfP.length!==8||gcP.length!==0||fcP.length!==0)checks.push("unexpected cross-lane parent-lift intersection");
 if(JSON.stringify(f.byBit[84])!==JSON.stringify(g.byBit[29]))checks.push("duplicate-root parent-lift sets differ");
 if(same.length!==7||extra.length!==1)checks.push("overlap decomposition mismatch");
 if(g.roots.size!==g.bits.length||f.roots.size!==f.bits.length||c.roots.size!==c.bits.length)checks.push("duplicate D4 root within a lane");
 if(!f.parents.has(g.childCanon))checks.push("cost70g child not covered by cost70f parent lifts");
 if(!g.parents.has(f.childCanon))checks.push("cost70f child not covered by cost70g parent lifts");
 if(checks.length)throw new Error(checks.join("; "));
 const ur=new Set([...g.roots.keys(),...f.roots.keys(),...c.roots.keys()]);
 const up=new Set([...g.parents.keys(),...f.parents.keys(),...c.parents.keys()]);
 const result={
  schema:"n11-cross-lane-d4-receipt-overlap-20261115-v1",
  date:"2026-11-15",
  source_main:SOURCE_MAIN,
  method:"Pure JavaScript BigInt 121-bit board transforms; all eight D4 symmetries; canonical representative is the minimum 128-bit hexadecimal board. Parent lifts are independently regenerated by deleting each of the seven root stones and D4-canonicalizing the resulting six-stone board. No solver, verdict cache, or certificate payload is read.",
  manifest_inputs:Object.entries(INPUTS).map(([name,file])=>({path:ROOT+file,blob_sha:blobs[name]})),
  lanes:{
   cost70f:{certificate_bits:f.bits,root_d4_orbits:f.roots.size,parent_lift_incidences:f.bits.length*7,unique_parent_lift_orbits:f.parents.size,duplicate_parent_incidences:f.bits.length*7-f.parents.size,child_occurrences:f.parents.get(f.childCanon)?.length||0,published_parent_lift_lists_checked:true},
   cost70g:{certificate_bits:g.bits,root_d4_orbits:g.roots.size,parent_lift_incidences:g.bits.length*7,unique_parent_lift_orbits:g.parents.size,duplicate_parent_incidences:g.bits.length*7-g.parents.size,child_occurrences:g.parents.get(g.childCanon)?.length||0,published_parent_lift_lists_checked:false},
   cost71c:{certificate_bits:c.bits,root_d4_orbits:c.roots.size,parent_lift_incidences:c.bits.length*7,unique_parent_lift_orbits:c.parents.size,duplicate_parent_incidences:c.bits.length*7-c.parents.size,child_occurrences:c.parents.get(c.childCanon)?.length||0,published_parent_lift_lists_checked:false}
  },
  cross_lane:{
   root_orbit_intersections:{
    cost70f_cost70g:gfR.map(k=>({canonical:k,cost70f:f.roots.get(k),cost70g:g.roots.get(k)})),
    cost70f_cost71c:fcR,cost70g_cost71c:gcR
   },
   parent_lift_intersections:{cost70f_cost70g:gfP,cost70f_cost71c:fcP,cost70g_cost71c:gcP},
   cost70f_cost70g_overlap_decomposition:{
    duplicate_root_pair:{cost70f_bit:84,cost70g_bit:29,canonical_root:common,shared_parent_lifts:same},
    additional_shared_parent_lifts:extra
   },
   child_bridge:{
    cost70f_child_canonical:f.childCanon,cost70g_child_canonical:g.childCanon,
    cost70g_child_already_in_cost70f_parent_lifts:f.parents.has(g.childCanon),
    cost70f_child_already_in_cost70g_parent_lifts:g.parents.has(f.childCanon)
   },
   after_cost70f_first:{
    additional_cost70g_root_orbits:g.roots.size-gfR.length,
    additional_cost70g_parent_lift_orbits:g.parents.size-gfP.length
   },
   combined_unique_root_orbits:ur.size,
   combined_unique_parent_lift_orbits:up.size
  },
  controls:{
   cost70f_parent_lift_lists_match_manifest:true,
   all_roots_are_seven_stone_child_plus_claimed_bit:true,
   roots_unique_within_each_lane:true,
   no_cost71c_root_or_parent_overlap_with_cost70f_or_cost70g:true,
   checks
  },
  interpretation_guard:"This is a D4 orbit-overlap audit of published certificate manifests, not a new game-theoretic proof and not a frontier fold. The shared parent-lift counts are raw orbit-set intersections; they are not new manifest-covered S6 counts because some parent orbits may already be covered by the canonical head. The cost70g bit29 root is D4-equivalent to cost70f bit84, so it is a duplicate proof root across lanes, although both certificate files were independently verified in their own manifests. If cost70f is folded first, the cost70g child orbit is already among cost70f's seven-stone-root parent lifts. Standard 11x11 empty board and the two-stone roots remain UNKNOWN."
 };
 fs.writeFileSync(path.join(OUT,"cost70f-70g-71c-cross-lane-d4-overlap-20261115.json"),JSON.stringify(result,null,2)+"\n");
}
main();
