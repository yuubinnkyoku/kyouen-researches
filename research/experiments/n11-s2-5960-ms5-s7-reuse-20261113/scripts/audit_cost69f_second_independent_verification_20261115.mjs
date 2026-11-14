#!/usr/bin/env node
// Second-pass audit for the four cost69f split WIN7 certificates.
// Full strategy-tree verification delegates to the repository's independent
// BigInt verifier; this wrapper independently checks hashes, root mobility,
// D4 parent incidence, and the proof-frontier fold.

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";

const ROOT = process.cwd();
const EXP = path.join(ROOT, "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113");
const OUT = path.join(EXP, "output");
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(OUT,name),"utf8"));
const md5 = (b) => createHash("md5").update(b).digest("hex");
const sha256 = (b) => createHash("sha256").update(b).digest("hex");
const gitBlobSha1 = (b) => createHash("sha1").update(Buffer.concat([Buffer.from("blob " + b.length + "\0"),b])).digest("hex");
const fmt = (x) => x.toString(16).padStart(32,"0");
const newRecords = readJson("class2-lane-cost69f-win7-certificates-2-20261115.json");
const oldRecords = readJson("class2-lane-cost69f-win7-certificates-20261115.json");
const fold = readJson("class-frontier-cost69f-receipts-recompute-20261115.json");
const cost65j = readJson("class2-lane-cost65j-inflight-20261115.json");
const cost69f = readJson("class2-lane-cost69f-inflight-20261115.json");
const cost69g = readJson("class2-lane-cost69g-inflight-20261115.json");
const verifierPath = path.join(EXP,"scripts","verify_win7_certificate_bigint_independent.mjs");
const wantedBits = [2,94,109,119];
const allCertificates = [...oldRecords.certificates,...newRecords.certificates];
const allByBit = new Map(allCertificates.map(x=>[x.bit,x]));
assert.equal(allCertificates.length,9);
assert.equal(new Set(allCertificates.map(x=>x.bit)).size,9);
assert.deepEqual(newRecords.sweep_source.uncertified_bits_after,[]);
assert.deepEqual(newRecords.sweep_source.certified_bits_after.slice().sort((a,b)=>a-b),[2,20,44,68,69,94,109,118,119]);

const transforms = [
  (x,y)=>[x,y],(x,y)=>[10-y,x],(x,y)=>[10-x,10-y],(x,y)=>[y,10-x],
  (x,y)=>[10-x,y],(x,y)=>[x,10-y],(x,y)=>[y,x],(x,y)=>[10-y,10-x]
];
function canon(mask) {
  let best=null;
  for (const f of transforms) {
    let z=0n;
    for (let i=0;i<121;i++) if ((mask>>BigInt(i))&1n) {
      const y=Math.floor(i/11),x=i%11,[xx,yy]=f(x,y);
      z|=1n<<BigInt(yy*11+xx);
    }
    if (best===null||z<best) best=z;
  }
  return fmt(best);
}
function positions(mask) {
  const out=[];
  for (let i=0;i<121;i++) if ((mask>>BigInt(i))&1n) out.push(i);
  return out;
}
const perms=[];
function permute(prefix,left) {
  if (!left.length) { perms.push(prefix); return; }
  for (let i=0;i<left.length;i++) permute([...prefix,left[i]],left.filter((_,j)=>j!==i));
}
permute([],[0,1,2,3]);
function det4(points) {
  const rows=points.map(i=>{
    const x=BigInt(i%11),y=BigInt(Math.floor(i/11));
    return [x*x+y*y,x,y,1n];
  });
  let det=0n;
  for (const p of perms) {
    let inv=0;
    for (let i=0;i<4;i++) for (let j=i+1;j<4;j++) if (p[i]>p[j]) inv++;
    let product=1n;
    for (let i=0;i<4;i++) product*=rows[i][p[i]];
    det+=inv%2?-product:product;
  }
  return det;
}
function bareissMobility(rootMask) {
  const pts=positions(rootMask);
  assert.equal(pts.length,7);
  for (let a=0;a<7;a++) for (let b=a+1;b<7;b++)
    for (let c=b+1;c<7;c++) for (let d=c+1;d<7;d++)
      assert.notEqual(det4([pts[a],pts[b],pts[c],pts[d]]),0n,"unsafe root");
  const moves=[];
  for (let m=0;m<121;m++) {
    if (pts.includes(m)) continue;
    let legal=true;
    for (let a=0;a<7&&legal;a++) for (let b=a+1;b<7&&legal;b++)
      for (let c=b+1;c<7&&legal;c++)
        if (det4([pts[a],pts[b],pts[c],m])===0n) { legal=false; break; }
    if (legal) moves.push(m);
  }
  return moves;
}
function parentOrbits(rootMask) {
  return new Set(positions(rootMask).map(i=>canon(rootMask^(1n<<BigInt(i)))));
}
const tmpDir=fs.mkdtempSync(path.join(os.tmpdir(),"n11-cost69f-second-audit-"));
const results=[];
try {
  for (const bit of wantedBits) {
    const record=allByBit.get(bit);
    assert(record,"missing certificate record for bit "+bit);
    assert.equal(record.verdict,"WIN7");
    assert.equal(record.fbt_drops,0);
    assert.equal(record.rows_sorted_unique,true);
    assert.equal(record.union_missing,0);
    assert.equal(record.union_extra,0);
    assert.deepEqual(record.terminal_range,[13,17]);
    const buffers=[];
    const partChecks=[];
    for (const part of record.storage.parts) {
      const bytes=fs.readFileSync(path.join(ROOT,part.path));
      assert.equal(bytes.length,part.bytes);
      assert.equal(md5(bytes),part.md5);
      assert.equal(gitBlobSha1(bytes),part.git_blob_sha);
      assert.equal(bytes.toString("utf8").split(/\r?\n/).filter(Boolean).length,part.lines);
      buffers.push(bytes);
      partChecks.push({path:part.path,bytes:bytes.length,md5:md5(bytes),git_blob_sha:gitBlobSha1(bytes)});
    }
    const joined=Buffer.concat(buffers);
    assert.equal(joined.length,record.bytes);
    assert.equal(md5(joined),record.md5);
    assert.equal(sha256(joined),record.sha256);
    const certPath=path.join(tmpDir,"bit"+bit+".cert");
    fs.writeFileSync(certPath,joined);
    const run=spawnSync(process.execPath,[verifierPath,certPath,String(record.root_check.loser_mobility)],{encoding:"utf8",maxBuffer:64*1024*1024});
    if (run.status!==0) throw new Error("verifier failed for bit "+bit+": "+(run.stderr||run.stdout));
    const verification=JSON.parse(run.stdout);
    assert.equal(verification.root_hex,record.root_hex);
    assert.equal(verification.strategy_rows,record.rows);
    assert.equal(verification.root_mobility,record.root_check.loser_mobility);
    assert.equal(verification.subroots_passed,record.sub_roots_pass);
    assert.equal(verification.union_missing,0);
    assert.equal(verification.union_extra,0);
    assert.deepEqual(verification.terminal_range,[13,17]);
    const rootMask=BigInt("0x"+record.root_hex);
    const mobilityMoves=bareissMobility(rootMask);
    assert.equal(mobilityMoves.length,verification.root_mobility);
    const foldRow=fold.cost69f_addition.find(x=>x.bit===bit);
    const parents=parentOrbits(rootMask);
    assert(foldRow.marginal_manifest_hexes.every(x=>parents.has(x)));
    results.push({bit,verification,hashes:{bytes:joined.length,md5:md5(joined),sha256:sha256(joined),parts:partChecks},bareiss_root_mobility:mobilityMoves.length,d4_parent_orbit_count:parents.size,marginal_manifest_hexes:foldRow.marginal_manifest_hexes});
  }
  const cost69fRoot=BigInt("0x"+cost69f.s6_child)|(1n<<2n);
  const cost65jRoot=BigInt("0x"+cost65j.s6_child)|(1n<<113n);
  const targetParent=canon(BigInt("0x"+cost69f.s6_child));
  const crossA=parentOrbits(cost69fRoot),crossB=parentOrbits(cost65jRoot);
  const shared=[...crossA].filter(x=>crossB.has(x)).sort();
  assert.deepEqual(shared,[targetParent]);
  assert.notEqual(canon(cost69fRoot),canon(cost65jRoot));

  const additions=fold.cost69f_addition.map(row=>{
    const cert=allByBit.get(row.bit);
    assert(cert,"fold receipt lacks a verified certificate: "+row.bit);
    return {...row,certified:true,certificate_sha256:cert.sha256,certificate_md5:cert.md5,certificate_rows:cert.rows};
  });
  const proofFold={...fold,source_schema:fold.schema,schema:"n11-class2-cost69f-certificate-backed-frontier-recompute-20261115-v1",cost69f_addition:additions,certificate_completion:{old_manifest:"class2-lane-cost69f-win7-certificates-20261115.json",new_manifest:"class2-lane-cost69f-win7-certificates-2-20261115.json",verified_bits:allCertificates.map(x=>x.bit).sort((a,b)=>a-b),uncertified_bits:[],certified_marginal_s6_orbits:additions.reduce((s,x)=>s+x.marginal_manifest_hexes.length,0)}};
  const audit={schema:"n11-class2-cost69f-second-independent-verification-20261115-v1",results,aggregate:{rows:results.reduce((s,x)=>s+x.verification.strategy_rows,0),visited_states:results.reduce((s,x)=>s+x.verification.visited_states_across_subroots,0),extraction_nodes:results.reduce((s,x)=>s+allByBit.get(x.bit).extraction_nodes,0)},cross_cover:{cost69f_bit2_root:fmt(cost69fRoot),cost65j_bit113_root:fmt(cost65jRoot),shared_s6_parent_orbits:shared,same_s7_d4_orbit:canon(cost69fRoot)===canon(cost65jRoot),note:"cost69f bit2 is now certificate-verified; a later cost65j bit113 proof of this same S6 parent must not be double-counted."},frontier_after:fold.frontier_after_cost69f,next_claim:{cost69g_s6_child:cost69g.s6_child,cost69g_edge_cost:cost69g.s6_s7_edge_cost,cost69g_candidate_count:cost69g.legal_candidates_total}};
  fs.writeFileSync(path.join(OUT,"cost69f-second-independent-verification-20261115.json"),JSON.stringify(audit,null,2)+"\n");
  fs.writeFileSync(path.join(OUT,"class-frontier-cost69f-certificate-backed-recompute-20261115.json"),JSON.stringify(proofFold,null,2)+"\n");
  process.stdout.write(JSON.stringify({audit,proof_frontier:proofFold.frontier_after_cost69f},null,2)+"\n");
} finally {
  fs.rmSync(tmpDir,{recursive:true,force:true});
}
