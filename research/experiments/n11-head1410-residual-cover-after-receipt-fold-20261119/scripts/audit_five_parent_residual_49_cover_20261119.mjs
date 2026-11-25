#!/usr/bin/env node
// Receipt-aware exact cover for the five-parent head-1410 target union.
// Node 22+, no external packages. Run from any directory in the repository.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../");
const EXP = "research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119";
const OUT = path.join(ROOT, EXP, "output");
const PIN = {
  joint: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-cost16-20261118.json", "40581746dc3304bdaff4b1934fd6f1d3d2981ea5"],
  audit: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json", "7cdc7c9ef341b5d9759923b3fc4986231c48895f"],
  head1476: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-cost71e-full-universe-verdict-join-20261118.json", "65d0c7ce0200638a50db5451b11b8cb88ec64b5d"],
  globalFold: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json", "753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc"],
  fold78: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json", "7e6144cc4bc92c34faa14bed3058cde64fb3880e"],
  cost78c: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json", "626409d50d0a7bb1b925ebecbff7dbee9adfa398"],
  cost79c: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79c-inflight-20261118.json", "054923a47ea0387b25f734222c499e60c054109b"],
  cost73j: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73j-inflight-20261117.json", "74fc3417391e30cf4cff9c2ffce059dce529ed86"]
};
function need(ok, message) { if (!ok) throw new Error(message); }
function gitBlobSha(bytes) {
  const blob = Buffer.concat([Buffer.from("blob " + bytes.length), Buffer.from([0]), bytes]);
  return crypto.createHash("sha1").update(blob).digest("hex");
}
function readBytes(name) {
  const [rel, sha] = PIN[name];
  const bytes = fs.readFileSync(path.join(ROOT, rel));
  need(gitBlobSha(bytes) === sha, "input blob mismatch: " + rel);
  return bytes;
}
function readJSON(name) { return JSON.parse(readBytes(name).toString("utf8")); }
function popcount(x) { let n = 0; while (x) { x &= x - 1n; n++; } return n; }
function transform(mask, t) {
  let out = 0n;
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) {
    const x = p % 11, y = Math.floor(p / 11);
    let X, Y;
    if (t === 0) { X=x; Y=y; }
    else if (t === 1) { X=10-y; Y=x; }
    else if (t === 2) { X=10-x; Y=10-y; }
    else if (t === 3) { X=y; Y=10-x; }
    else if (t === 4) { X=10-x; Y=y; }
    else if (t === 5) { X=x; Y=10-y; }
    else if (t === 6) { X=y; Y=x; }
    else { X=10-y; Y=10-x; }
    out |= 1n << BigInt(11 * Y + X);
  }
  return out;
}
function canon(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) {
    const z = transform(mask, t);
    if (best === null || z < best) best = z;
  }
  return best.toString(16).padStart(32, "0");
}
function det3(a, b, c) {
  const [x1,y1]=a, [x2,y2]=b, [x3,y3]=c;
  const q1=BigInt(x1*x1+y1*y1), q2=BigInt(x2*x2+y2*y2), q3=BigInt(x3*x3+y3*y3);
  return q1*BigInt(x2*y3-x3*y2) - q2*BigInt(x1*y3-x3*y1) + q3*BigInt(x1*y2-x2*y1);
}
function det4(a,b,c,d) { return det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d); }

// Edmonds blossom, O(V^3), for an exact maximum matching in a general graph.
function maximumMatching(g) {
  const n=g.length, match=Array(n).fill(-1), p=Array(n), base=Array(n), used=Array(n), blossom=Array(n);
  function lca(a,b) {
    const seen=Array(n).fill(false);
    while (true) { a=base[a]; seen[a]=true; if (match[a]===-1) break; a=p[match[a]]; }
    while (true) { b=base[b]; if (seen[b]) return b; b=p[match[b]]; }
  }
  function markPath(v,b,child) {
    while (base[v]!==b) {
      blossom[base[v]]=true; blossom[base[match[v]]]=true;
      p[v]=child; child=match[v]; v=p[match[v]];
    }
  }
  function findPath(root) {
    used.fill(false); p.fill(-1); for (let i=0;i<n;i++) base[i]=i;
    const q=[root]; used[root]=true;
    for (let qi=0;qi<q.length;qi++) {
      const v=q[qi];
      for (const u of g[v]) {
        if (base[v]===base[u] || match[v]===u) continue;
        if (u===root || (match[u]!==-1 && p[match[u]]!==-1)) {
          const b=lca(v,u); blossom.fill(false); markPath(v,b,u); markPath(u,b,v);
          for (let i=0;i<n;i++) if (blossom[base[i]]) {
            base[i]=b; if (!used[i]) { used[i]=true; q.push(i); }
          }
        } else if (p[u]===-1) {
          p[u]=v;
          if (match[u]===-1) return u;
          const m=match[u]; used[m]=true; q.push(m);
        }
      }
    }
    return -1;
  }
  for (let i=0;i<n;i++) if (match[i]===-1) {
    let v=findPath(i);
    if (v!==-1) while (v!==-1) {
      const pv=p[v], nv=pv===-1 ? -1 : match[pv];
      match[v]=pv; if (pv!==-1) match[pv]=v; v=nv;
    }
  }
  return { size: match.filter(x=>x!==-1).length/2, match };
}

const joint=readJSON("joint"), audit=readJSON("audit"), head=readJSON("head1476");
const globalFold=readJSON("globalFold"), fold78=readJSON("fold78");
const c78=readJSON("cost78c"), c79=readJSON("cost79c"), c73=readJSON("cost73j");
need(audit.all_pass===true && audit.check_count===23, "independent 112-row audit must pass");
need(audit.derived.maximum_root_span===2, "candidate max-span must be 2");
need(joint.derived.joint_results.length===31 && joint.all_pass===true && joint.derived.joint_results.every(x=>x.exact===true), "31 subset witnesses must be published and passing");

const targetRows=[...new Set(audit.derived.witness_pairs.flatMap(x=>x.rows))].sort();
need(targetRows.length===112, "five-parent target union must contain 112 rows");
const targetSet=new Set(targetRows);
const globalRows=globalFold.receipts_by_row.map(x=>x.row_hex);
const laterRows=fold78.new_receipt_coverage.receipts_by_row.map(x=>x.row_hex);
const globalHits=targetRows.filter(x=>globalRows.includes(x));
const laterHits=targetRows.filter(x=>laterRows.includes(x));
const closedSet=new Set([...globalHits,...laterHits]);
need(globalHits.length===13 && laterHits.length===2 && closedSet.size===15, "receipt overlap must be 13 + 2 = 15");
const residualRows=targetRows.filter(x=>!closedSet.has(x));
need(residualRows.length===97, "residual target must contain 97 rows");
const residualSet=new Set(residualRows);

// Exact, explicitly enumerated verdict sources. This is not the entire 8,964-entry cache.
const knownRefuted=new Set(), knownWin=new Set();
for (const x of head.candidate_root_universe.matched_roots) {
  if (x.verdict==="REFUTED-D10") knownRefuted.add(x.d4_canon_root);
  else if (x.verdict==="WIN7-D10") knownWin.add(x.d4_canon_root);
}
for (const c of [c78,c79]) {
  for (const x of Object.values(c.transfers||{})) {
    if (x.verdict==="REFUTED-D10") knownRefuted.add(x.root_canon);
    else if (x.verdict==="WIN7-D10") knownWin.add(x.root_canon);
  }
  for (const bit of c.actual_execution.refuted_d10_bits||[])
    knownRefuted.add(canon(BigInt("0x"+c.s6_child)|(1n<<BigInt(bit))));
  for (const bit of c.actual_execution.win7_d10_bits||[])
    knownWin.add(canon(BigInt("0x"+c.s6_child)|(1n<<BigInt(bit))));
}
const c73Wins=new Set(c73.actual_execution.results.win7_d10_bits);
for (const bit of c73.engine_candidate_bits.open_bits) {
  const root=canon(BigInt("0x"+c73.s6_child)|(1n<<BigInt(bit)));
  if (c73Wins.has(bit)) knownWin.add(root); else knownRefuted.add(root);
}
for (const x of Object.values(c73.transfers||{})) {
  if (x.verdict==="REFUTED-D10") knownRefuted.add(x.root_canon);
  else if (x.verdict==="WIN7-D10") knownWin.add(x.root_canon);
}
for (const row of globalFold.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt("0x"+x.root)));
for (const row of fold78.new_receipt_coverage.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt("0x"+x.root)));
for (const x of fold78.new_receipt_coverage.marginal_by_root) knownWin.add(canon(BigInt("0x"+x.root)));
need(knownRefuted.size===236 && knownWin.size===156, "enumerated verdict-source totals changed");

const pool=new Set(audit.derived.witness_pairs.map(x=>canon(BigInt("0x"+x.root))));
for (const subset of joint.derived.joint_results) for (const root of subset.witness_roots) pool.add(canon(BigInt("0x"+root)));
need(pool.size===117, "subset-witness root pool must contain 117 D4 canons");
const poolRefuted=[...pool].filter(x=>knownRefuted.has(x)).sort();
const poolWin=[...pool].filter(x=>knownWin.has(x)).sort();
need(poolRefuted.length===5 && poolWin.length===0, "candidate-pool verdict overlap changed");

const pairRoots=new Map(), singleRoots=new Map();
for (const root of pool) {
  if (knownRefuted.has(root) || knownWin.has(root)) continue;
  const mask=BigInt("0x"+root), covered=new Set();
  for (let t=0;t<8;t++) {
    const image=transform(mask,t);
    for (let bit=0;bit<121;bit++) if ((image>>BigInt(bit))&1n) {
      const row=canon(image^(1n<<BigInt(bit)));
      if (residualSet.has(row)) covered.add(row);
    }
  }
  const rows=[...covered].sort();
  if (rows.length===2) {
    const key=rows.join("|"); if (!pairRoots.has(key)) pairRoots.set(key,[]);
    pairRoots.get(key).push(root);
  } else if (rows.length===1) {
    if (!singleRoots.has(rows[0])) singleRoots.set(rows[0],[]);
    singleRoots.get(rows[0]).push(root);
  }
}
const rowIndex=new Map(residualRows.map((x,i)=>[x,i]));
const graph=Array.from({length:residualRows.length},()=>[]);
for (const key of pairRoots.keys()) {
  const [a,b]=key.split("|"), i=rowIndex.get(a), j=rowIndex.get(b);
  graph[i].push(j); graph[j].push(i);
}
for (const edges of graph) edges.sort((a,b)=>a-b);
const matching=maximumMatching(graph);
const unmatched=residualRows.filter((_,i)=>matching.match[i]===-1);
need(pairRoots.size===92 && singleRoots.size===14 && matching.size===48 && unmatched.length===1,
     "residual matching structure changed");
const singletonRow=unmatched[0];
const singletonChoices=(singleRoots.get(singletonRow)||[]).sort();
need(singletonChoices.length>0, "unmatched row needs a singleton candidate root");
const singletonRoot=singletonChoices[0];

const witness=[];
for (let i=0;i<residualRows.length;i++) {
  const j=matching.match[i];
  if (j>i) {
    const key=[residualRows[i],residualRows[j]].sort().join("|");
    witness.push({root:pairRoots.get(key).sort()[0],rows:key.split("|")});
  }
}
witness.push({root:singletonRoot,rows:[singletonRow]});
witness.sort((a,b)=>a.root.localeCompare(b.root));
need(witness.length===49, "witness must contain 49 roots");

const rootChecks=[];
for (const item of witness) {
  const mask=BigInt("0x"+item.root), points=[];
  for (let p=0;p<121;p++) if ((mask>>BigInt(p))&1n) points.push([p%11,Math.floor(p/11)]);
  let unsafe=0;
  for (let a=0;a<7;a++) for (let b=a+1;b<7;b++) for (let c=b+1;c<7;c++) for (let d=c+1;d<7;d++)
    if (det4(points[a],points[b],points[c],points[d])===0n) unsafe++;
  const covered=new Set();
  for (let t=0;t<8;t++) {
    const image=transform(mask,t);
    for (let bit=0;bit<121;bit++) if ((image>>BigInt(bit))&1n) {
      const row=canon(image^(1n<<BigInt(bit)));
      if (targetSet.has(row)) covered.add(row);
    }
  }
  const residualCovered=[...covered].filter(x=>residualSet.has(x)).sort();
  need(popcount(mask)===7 && canon(mask)===item.root && unsafe===0, "unsafe or noncanonical root: "+item.root);
  need(JSON.stringify(residualCovered)===JSON.stringify(item.rows), "root coverage mismatch: "+item.root);
  need(!knownRefuted.has(item.root) && !knownWin.has(item.root), "selected root has a known verdict: "+item.root);
  rootChecks.push({
    root:item.root, stones:7, d4_canonical:true, unsafe_quadruples:unsafe,
    covered_target_rows:[...covered].sort(), covered_residual_rows:residualCovered
  });
}
const rowUse=new Map();
for (const item of witness) for (const row of item.rows) rowUse.set(row,(rowUse.get(row)||0)+1);
need(rowUse.size===97 && residualRows.every(x=>rowUse.get(x)===1), "residual rows are not covered exactly once");
need([...rowUse.keys()].every(x=>residualSet.has(x)), "witness covers a non-residual row");
const lowerBound=Math.ceil(residualRows.length/audit.derived.maximum_root_span);
need(lowerBound===49 && witness.length===lowerBound, "lower bound not attained");

const scriptRel=path.relative(ROOT,fileURLToPath(import.meta.url)).split(path.sep).join("/");
const scriptSha=gitBlobSha(fs.readFileSync(fileURLToPath(import.meta.url)));
const result={
  schema:"n11-five-parent-receipt-aware-residual-cover-20261119-v1",
  date:"2026-11-19",
  status:"exact-residual-candidate-cover",
  source_main_head:"8af969be132ca709dd79fbc472ec198f55fe53d1",
  input_pins:Object.fromEntries(Object.entries(PIN).map(([k,v])=>[k,{path:v[0],git_blob_sha1:v[1]}])),
  reproduction_script:{path:scriptRel,git_blob_sha1:scriptSha},
  target:{parents:5,rows:112,maximum_candidate_root_span:2},
  receipts:{
    global_fold_rows:globalRows.length,global_fold_target_rows:globalHits.length,global_fold_target_row_hex:globalHits,
    cost78c_79c_fold_rows:laterRows.length,cost78c_79c_target_rows:laterHits.length,cost78c_79c_target_row_hex:laterHits,
    total_closed_target_rows:closed.size,closed_target_rows:[...closedSet].sort(),
    residual_rows:residualRows.length,residual_row_hex:residualRows
  },
  known_verdict_join:{
    known_refuted_roots:knownRefuted.size,known_win_roots:knownWin.size,
    candidate_pool_roots:pool.size,candidate_pool_refuted_roots:poolRefuted,
    candidate_pool_win_roots:poolWin,
    selected_roots_known_refuted:0,selected_roots_known_win:0,
    sources:["head1476 cost71e full-universe join","cost73j completed sweep and confirmation transfers","cost78c completed sweep and confirmation transfers","cost79c completed sweep and confirmation transfers","global receipt fold","cost78c/79c receipt fold"],
    full_8964_per_root_cache_join_complete:false,
    limitation:"The published 8,964-verdict scan is an aggregate index here; this audit joins the explicitly listed sweep/receipt sources, not every raw cache entry."
  },
  matching:{
    subset_witness_root_pool:pool.size,pair_edges:pairRoots.size,singleton_eligible_rows:singleRoots.size,
    maximum_matching:matching.size,unmatched_row:singletonRow,singleton_root:singletonRoot,
    pair_roots:48,singleton_roots:1,minimum_cover_lower_bound:lowerBound,witness_size:witness.length
  },
  witness,root_checks:rootChecks,
  checks:[
    {name:"five-parent target union is 112 rows",pass:targetRows.length===112},
    {name:"receipt folds close exactly 15 target rows",pass:closed.size===15},
    {name:"97 residual rows remain",pass:residualRows.length===97},
    {name:"candidate universe maximum span is 2",pass:audit.derived.maximum_root_span===2},
    {name:"117 subset-witness roots are D4-distinct",pass:pool.size===117},
    {name:"five known-refuted pool roots are excluded",pass:poolRefuted.length===5},
    {name:"no known-WIN pool root is needed",pass:poolWin.length===0},
    {name:"residual graph has 92 pair edges",pass:pairRoots.size===92},
    {name:"maximum matching has 48 pairs",pass:matching.size===48},
    {name:"one unmatched row has a singleton root",pass:unmatched.length===1&&singletonChoices.length>0},
    {name:"49 roots attain the 49 lower bound",pass:witness.length===lowerBound},
    {name:"all 49 roots have seven stones and are D4-canonical",pass:rootChecks.every(x=>x.stones===7&&x.d4_canonical)},
    {name:"all 49 roots have no forbidden quadruple",pass:rootChecks.every(x=>x.unsafe_quadruples===0)},
    {name:"all 97 residual rows are covered exactly once",pass:rowUse.size===97&&residualRows.every(x=>rowUse.get(x)===1)},
    {name:"selected roots have no known verdict conflict",pass:rootChecks.every(x=>!knownRefuted.has(x.root)&&!knownWin.has(x.root))}
  ],
  all_pass:true,
  interpretation_guard:[
    "This is a minimum candidate-root cover for the 97 residual S6 rows, not a set of WIN7-D10 certificates.",
    "The 49 selected roots still require actual sweeps and independently verified certificates.",
    "The known-verdict join is limited to the explicitly pinned sources; the full 8,964 per-root cache is not fully joined here.",
    "REFUTED-D10 is not a LOSS proof.",
    "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  ]
};
need(result.checks.every(x=>x.pass), "one or more checks failed");
fs.mkdirSync(OUT,{recursive:true});
fs.writeFileSync(path.join(OUT,"five-parent-residual-49-cover-20261119.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify({target_rows:112,closed_rows:15,residual_rows:97,pair_edges:92,matching:48,minimum_cover:49,known_refuted:236,known_win:156,selected_roots:49},null,2));
