#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = process.cwd();
const P = {
  resolve: "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json",
  resolver: "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/resolve5.py",
  roots: "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/roots.json",
  sweep: "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json",
  output: "research/experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/output/candidate-supply-scope-audit-20261120.json"
};
const PIN = {
  resolve: "431ce3bf4199b46b18c30ef79f43165da38c9e13",
  resolver: "c910a450f0e70023ebbc1608c3f4de9ef3aeeea1",
  roots: "c6f447431980418f0426ef909835301142f5c432",
  sweep: "49fa9109b68f9226aa7495c8c6c718de996b7980"
};
function need(ok, message) { if (!ok) throw new Error(message); }
function readPinned(rel, expected) {
  const bytes = fs.readFileSync(path.join(ROOT, rel));
  const blob = crypto.createHash("sha1")
    .update(Buffer.concat([Buffer.from("blob " + bytes.length + "\0"), bytes]))
    .digest("hex");
  need(blob === expected, "Git blob pin mismatch: " + rel + " got " + blob);
  return bytes.toString("utf8");
}
const R = JSON.parse(readPinned(P.resolve, PIN.resolve));
const resolverSource = readPinned(P.resolver, PIN.resolver);
const I = JSON.parse(readPinned(P.roots, PIN.roots));
const S = JSON.parse(readPinned(P.sweep, PIN.sweep));
need(resolverSource.includes("for root in fresh_safe"), "resolver no longer selects from fresh_safe");
const popcount = x => { let n = 0; while (x) { x &= x - 1n; n++; } return n; };
const tf = Array.from({ length: 8 }, (_, t) => Array.from({ length: 121 }, (_, p) => {
  const x = p % 11, y = Math.floor(p / 11);
  const z = [[x,y],[10-y,x],[10-x,10-y],[y,10-x],[10-x,y],[x,10-y],[y,x],[10-y,10-x]][t];
  return 11 * z[1] + z[0];
}));
function transform(mask, t) {
  let out = 0n;
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) out |= 1n << BigInt(tf[t][p]);
  return out;
}
function canon(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) { const z = transform(mask, t); if (best === null || z < best) best = z; }
  return best;
}
function bits(mask) {
  const out = [];
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) out.push(p);
  return out;
}
function det3(a,b,c) {
  const [x1,y1] = a, [x2,y2] = b, [x3,y3] = c;
  const q1=x1*x1+y1*y1, q2=x2*x2+y2*y2, q3=x3*x3+y3*y3;
  return q1*(x2*y3-x3*y2)-q2*(x1*y3-x3*y1)+q3*(x1*y2-x2*y1);
}
function det4(a,b,c,d) { return det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d); }
function unsafeCount(mask) {
  const ps = bits(mask).map(p => [p%11, Math.floor(p/11)]);
  let n=0;
  for(let a=0;a<7;a++) for(let b=a+1;b<7;b++) for(let c=b+1;c<7;c++) for(let d=c+1;d<7;d++)
    if(det4(ps[a],ps[b],ps[c],ps[d])===0) n++;
  return n;
}
const residual = new Set(R.base_state.residual_row_hex);
function coverage(mask) {
  const cov = new Set();
  for(let t=0;t<8;t++) {
    const image=transform(mask,t);
    for(const p of bits(image)) {
      const row=canon(image ^ (1n<<BigInt(p))).toString(16).padStart(32,"0");
      if(residual.has(row)) cov.add(row);
    }
  }
  return [...cov].sort();
}
need(R.base_state.residual_rows===78 && residual.size===78, "residual rows");
need(R.expansion.fresh_safe===4728, "fresh-safe count");
need(R.resolve.pair_edges===706 && R.resolve.singleton_eligible_rows===78, "pair/singleton counts");
need(R.resolve.maximum_matching===39 && R.resolve.witness_size===39, "matching count");
need(Object.keys(R.resolve.multi_cover_roots).length===0, "multi-cover count");
need(I.length===39 && S.classification.counted_roots===39, "39-root inputs");
need(S.classification.win7_d10.count===0 && S.classification.refuted_d10.count===39 &&
     S.classification.capped.count===0 && S.classification.ordering_conflicts.count===0, "sweep partition");
const witness = new Map(R.witness_full.map(x=>[x.root,x]));
const roots = new Map(I.map(x=>[x.root,x]));
const records = new Map(S.witness_records.map(x=>[x.root,x]));
const swept = [...S.classification.refuted_d10.roots].sort();
const selectedRows = new Set(), selectedPairs = new Set(), geometry = [];
for(const root of swept) {
  const w=witness.get(root), r=roots.get(root), s=records.get(root);
  need(w && r && s, "root missing from one source");
  const rows=[...w.rows].sort();
  need(rows.length===2 && JSON.stringify(rows)===JSON.stringify([...r.rows].sort()) &&
       JSON.stringify(rows)===JSON.stringify([...s.covered_stranded_rows].sort()), "coverage disagreement");
  const pair=rows.join("|"); need(!selectedPairs.has(pair), "duplicate matching edge"); selectedPairs.add(pair);
  for(const row of rows) { need(!selectedRows.has(row), "matching rows overlap"); selectedRows.add(row); }
  const mask=BigInt("0x"+root), child=BigInt("0x"+r.child);
  need(popcount(mask)===7 && canon(mask)===mask, "root not canonical seven-stone");
  need((child | (1n<<BigInt(r.bit)))===mask, "child/bit reconstruction");
  const unsafe=unsafeCount(mask); need(unsafe===0, "unsafe root");
  need(JSON.stringify(coverage(mask))===JSON.stringify(rows), "D4 deletion coverage");
  need(s.probe_runs.length===2 && new Set(s.probe_runs.map(p=>p.ordering)).size===2 &&
       s.probe_runs.every(p=>p.cap===30000000 && !p.capped && p.loss===false), "probe verdict gate");
  need(s.pilot_control.all_pass && s.pilot_control.nodes===3402, "pilot control");
  geometry.push({root,covered_rows:rows,unsafe_quadruples:unsafe,probe_nodes:s.probe_runs.map(p=>p.nodes)});
}
need(selectedRows.size===78 && [...selectedRows].every(x=>residual.has(x)), "pair cover not exact");
const result = {
  schema:"n11-residual78-witness39-candidate-supply-scope-audit-20261120-v1",
  date:"2026-11-20",
  status:"verified-scope-audit",
  inputs:{
    resolve5_output:{path:P.resolve,git_blob_sha:PIN.resolve},
    resolve5_source:{path:P.resolver,git_blob_sha:PIN.resolver},
    witness_roots:{path:P.roots,git_blob_sha:PIN.roots},
    sweep_result:{path:P.sweep,git_blob_sha:PIN.sweep}
  },
  pre_sweep_candidate_graph:{
    residual_rows:78,fresh_safe_roots:4728,distinct_pair_edges:706,singleton_eligible_rows:78,
    multi_cover_roots:0,selected_matching_roots:39,selected_pair_edges:39,selected_rows:78
  },
  sweep:{
    roots:39,win7_d10:0,refuted_d10:39,capped:0,ordering_conflicts:0,probe_count:78,
    total_nodes:S.controls.nodes_total_all_probes,
    max_single_probe_nodes:Math.max(...S.witness_records.flatMap(x=>x.probe_runs.map(p=>p.nodes))),
    all_pilot_controls_pass:true
  },
  scope_arithmetic:{
    fresh_safe_roots_outside_this_sweep:4689,
    distinct_pair_edges_not_selected_by_this_matching:667,
    singleton_eligible_rows_not_touched_by_this_sweep:78,
    interpretation:"The selected 39-root matching plan was fully consumed. This does not establish exhaustion of the full pre-sweep add-one-stone candidate universe. The other 4,689 fresh-safe roots were outside this sweep; their status against the full 8,964-entry D4 cache is not established here. The 667 unselected pair edges are pre-sweep row-pair relations, not a recomputed post-sweep matching."
  },
  checks:[
    {name:"pinned source blobs",pass:true},
    {name:"resolve5 candidate counts and matching",pass:true},
    {name:"39-root input equals selected witness set",pass:true},
    {name:"sweep partition 0/39/0/0",pass:true},
    {name:"all 39 roots canonical and seven-stone",pass:true},
    {name:"all 39 roots safe by exact determinant",pass:true},
    {name:"all 39 D4 deletion covers match two recorded residual rows",pass:true},
    {name:"39 pairs are disjoint and cover all 78 residual rows",pass:true},
    {name:"all 78 probes uncapped and pilot-controlled",pass:true}
  ],
  geometry_checks:geometry,
  interpretation_guard:[
    "REFUTED-D10 is not a LOSS proof.",
    "The 39-root plan's exhaustion is not global add-one-stone candidate exhaustion.",
    "No post-sweep maximum matching is claimed.",
    "No receipt was created and no S6 row was closed.",
    "The 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  ]
};
const out=path.join(ROOT,P.output);
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify({status:result.status,checks:result.checks.length,roots:result.sweep.roots,
  freshSafe:result.pre_sweep_candidate_graph.fresh_safe_roots,
  outsideSweep:result.scope_arithmetic.fresh_safe_roots_outside_this_sweep,
  pairEdges:result.pre_sweep_candidate_graph.distinct_pair_edges,
  unselectedPairs:result.scope_arithmetic.distinct_pair_edges_not_selected_by_this_matching,
  singletonRowsUntouched:result.scope_arithmetic.singleton_eligible_rows_not_touched_by_this_sweep},null,2));
