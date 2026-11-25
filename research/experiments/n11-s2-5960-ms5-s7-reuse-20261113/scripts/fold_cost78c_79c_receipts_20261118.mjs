#!/usr/bin/env node
// Reproduce the cost78c/cost79c combined receipt fold. Node 22+, no external packages.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {fileURLToPath} from "node:url";
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../../../../");
const EXP="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113";
const OUT=path.join(ROOT,EXP,"output");
const PIN={
worklist:["research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv","2fee1d0718547a62e346d35f5858d7913e37c097"],
ledger:["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json","e8785d509e8a11a37c0d03cc450455a14708c34d"],
census:["research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json","9c251da3138c5cb0516e097be5e5d0427dfaf5f0"],
globalFold:[EXP+"/output/class-frontier-receipt-harvest-global-fold-20261118.json","753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc"],
man78:[EXP+"/output/class2-lane-cost78c-certificates/class2-lane-cost78c-win7-certificates-20261117.json","b7fe519e923c6170e836f71e3f084f73219319d5"],
man79:[EXP+"/output/class2-lane-cost79c-certificates/class2-lane-cost79c-win7-certificates-20261118.json","e904a37665fb77c971ce7f9c64a3c4aa9109da4d"],
claim78:[EXP+"/output/class2-lane-cost78c-inflight-20261117.json","1850832186ba9c8715624094f05d67aa4eb10f0b"],
claim79:[EXP+"/output/class2-lane-cost79c-inflight-20261118.json","ca517b73ffe287def7bf2c215fa4c38a6d15838a"],
bigint78:[EXP+"/output/class2-lane-cost78c-certificates-bigint-independent-reverification-20261117.json","7d97599186e6c76b8566d5f5703d71915224a129"],
bigint79a:[EXP+"/output/class2-lane-cost79c-certificates-third-independent-audit-20261118.json","50190347cbc31fa80bf24f9545466c0f3ad9d6f3"],
bigint79b:[EXP+"/output/class2-lane-cost79c-certificates-third-independent-audit-remaining16-20261118.json","410fb935f855881b5b5e9992b75436483d1b3ef1"],
v13:[EXP+"/output/class2-lane-next-target-presweep-1473-v13-20261118.json","fdb94e31ed2fd83ba8104f65c4f55dd2726c3bd8"],
agreement78:[EXP+"/output/class2-lane-cost78c-census-v12-cross-lane-agreement-20261118.json","e2839050803f398c4844a4ef19543c7bc9231e27"],
audit79:[EXP+"/output/class2-lane-cost79c-raw-batches-1-9-audit-20261118.json","133f223040f62eb3edd9bc2dcfbc400c05a1cef5"]
};
function need(x,m){if(!x)throw new Error(m);}
function read(k){const [rel,sha]=PIN[k],b=fs.readFileSync(path.join(ROOT,rel));const h=Buffer.concat([Buffer.from("blob "+b.length),Buffer.from([0]),b]);need(crypto.createHash("sha1").update(h).digest("hex")===sha,"blob mismatch "+rel);return b;}
function js(k){return JSON.parse(read(k).toString("utf8"));}
const csv=read("worklist").toString("utf8").trim().split(/\r?\n/),cols=csv[0].split(","),ix=cols.indexOf("s6_canonical_hex"),cx=cols.indexOf("own_candidates_s6_s7_edge_cost"),kx=cols.indexOf("category");
need(ix>=0&&cx>=0&&kx>=0,"worklist header");
const work=new Map();for(const line of csv.slice(1)){const a=line.split(",");work.set(a[ix],{cost:Number(a[cx]),category:a[kx]});}
const ledger=js("ledger"),census=js("census"),gf=js("globalFold"),c78=js("claim78"),c79=js("claim79"),m78=js("man78"),m79=js("man79");
const b78=js("bigint78"),b79a=js("bigint79a"),b79b=js("bigint79b"),v13=js("v13"),a78=js("agreement78"),a79=js("audit79");
need(m78.certificates.length===11&&m79.certificates.length===19,"manifest counts");
need(b78.summary.verifier_pass===11&&b78.summary.verifier_fail===0,"78c BigInt");
need(b79a.all_pass&&b79b.all_pass&&Object.keys(b79a.certificates).length===3&&Object.keys(b79b.certificates).length===16,"79c BigInt");
need(a78.agreement==="PASS"&&Object.keys(a78.checks).length===7&&a79.all_pass,"cross-lane audits");
need(v13.cross_checks["sixteen_map_internal_conflicts"]===0&&v13.cross_checks["harvest_vs_sixteen_map_conflicts"]===0,"verdict conflicts");
need(c79.actual_execution.win7_d10_bits.length===20&&c79.actual_execution.refuted_d10_bits.length===59,"79c verdict totals");
const old66=new Set(ledger.derived.closed_rows_66),oldGlobal=new Set(gf.receipts_by_row.map(x=>x.row_hex));
const open=new Map([...work].filter(([h])=>!old66.has(h)&&!oldGlobal.has(h)));
const parents=new Map(census.open_s5_census.map(p=>[p.hex,p]));
const tf=[(x,y)=>[x,y],(x,y)=>[y,10-x],(x,y)=>[10-x,10-y],(x,y)=>[10-y,x],(x,y)=>[10-x,y],(x,y)=>[x,10-y],(x,y)=>[y,x],(x,y)=>[10-y,10-x]];
function d4(m,t){let z=0n;for(let p=0;p<121;p++)if((m>>BigInt(p))&1n){const [x,y]=tf[t](p%11,Math.floor(p/11));z|=1n<<BigInt(11*y+x);}return z;}
function canon(m){let b=null;for(let t=0;t<8;t++){const z=d4(m,t);if(b===null||z<b)b=z;}return b.toString(16).padStart(32,"0");}
function pc(m){let n=0;while(m){m&=m-1n;n++;}return n;}
function bitIndex(m){let i=0;while(m>1n){m>>=1n;i++;}return i;}
const certs=[...m78.certificates.map(c=>({band:"78c",bit:Number(c.bit),root:c.root,canon:c.d4_canon_root,child:c78.s6_child})),...m79.certificates.map(c=>({band:"79c",bit:Number(c.bit),root:c.root,canon:c.d4_canon_root,child:c79.s6_child}))].sort((a,b)=>a.band.localeCompare(b.band)||a.bit-b.bit);
const roots=new Map();
for(const c of certs){const r=BigInt("0x"+c.root),rc=canon(r),mc=String(c.canon).toLowerCase().replace(/^0x/,"").padStart(32,"0");need(pc(r)===7&&rc===mc&&r===(BigInt("0x"+c.child)|(1n<<BigInt(c.bit))),"root mismatch");need(!roots.has(rc),"duplicate D4 root");roots.set(rc,{...c,root:r});}
need(roots.size===30,"root count");
const rowParents=new Map();
for(const [h] of open){const m=BigInt("0x"+h),ps=new Set();for(let q=0;q<121;q++)if((m>>BigInt(q))&1n){const p=canon(m^(1n<<BigInt(q)));if(parents.has(p))ps.add(p);}rowParents.set(h,[...ps].sort());}
function demand(h){const d={c1:0,c2:0,c4:0};for(const p of rowParents.get(h)||[]){const c=parents.get(p).classes;if(c&1)d.c1++;if(c&2)d.c2++;if(c&4)d.c4++;}return d;}
function needed(set){let n=0,c=0;for(const h of set)if(demand(h).c1===0){n++;c+=open.get(h).cost;}return {s6_needed_by_open_classes:n,cost_needed_by_open_classes:c};}
const openCost=[...open.values()].reduce((s,x)=>s+x.cost,0),baseNeed=needed(new Set(open.keys()));
need(open.size===6259&&openCost===495507&&parents.size===174&&baseNeed.s6_needed_by_open_classes===4543&&baseNeed.cost_needed_by_open_classes===360227,"base frontier");
const byRoot=new Map(),byRow=new Map();
for(const [rc,info] of roots){const cov=new Map();for(let t=0;t<8;t++){const sr=d4(info.root,t);for(let q=0;q<121;q++)if((sr>>BigInt(q))&1n){const h=canon(sr^(1n<<BigInt(q)));if(open.has(h)&&!cov.has(h))cov.set(h,{transform:t,extra_bit:q});}}byRoot.set(rc,cov);for(const [h,loc] of cov){if(!byRow.has(h))byRow.set(h,[]);byRow.get(h).push({root:rc,band:info.band,bit:info.bit,transform:loc.transform,extra_bit:loc.extra_bit});}}
const byContain=new Map();
for(const [h] of open){const row=BigInt("0x"+h),matches=[];for(const [rc,info] of roots){for(let t=0;t<8;t++){const sr=d4(info.root,t);if((row&~sr)===0n){const e=sr^row;need(pc(e)===1,"subset difference");matches.push({root:rc,band:info.band,bit:info.bit,transform:t,extra_bit:bitIndex(e)});break;}}}if(matches.length)byContain.set(h,matches);}
const ra=[...byRow.keys()].sort(),rb=[...byContain.keys()].sort();need(JSON.stringify(ra)===JSON.stringify(rb),"D4 row sets");
for(const h of ra){const a=byRow.get(h).map(x=>x.root).sort(),b=byContain.get(h).map(x=>x.root).sort();need(JSON.stringify(a)===JSON.stringify(b),"D4 root-row pairs");}
const closed=new Set([...old66,...oldGlobal]),rootFold=[],marginal={"78c":[],"79c":[]};
for(const rc of roots.keys()){const info=roots.get(rc),cov=byRoot.get(rc),newRows=[...cov.keys()].filter(h=>!closed.has(h)).sort(),cost=newRows.reduce((s,h)=>s+open.get(h).cost,0);for(const h of newRows)closed.add(h);const child=canon(BigInt("0x"+info.child)),rec={band:info.band,bit:info.bit,root:rc,child_row:child,child_row_open_before:open.has(child),child_row_newly_closed:newRows.includes(child),covered_open_rows:[...cov.keys()].sort(),marginal_rows:newRows,marginal:newRows.length,marginal_edge_cost:cost};rootFold.push(rec);marginal[info.band].push({bit:info.bit,marginal:rec.marginal,rows:newRows});}
const rows=ra.map(h=>({row_hex:h,cost:open.get(h).cost,category:open.get(h).category,demand:demand(h),parents:rowParents.get(h)||[],receipts:byContain.get(h).slice().sort((x,y)=>x.band.localeCompare(y.band)||x.bit-y.bit)}));
const totalCost=rows.reduce((s,r)=>s+r.cost,0),pairs=rows.reduce((s,r)=>s+r.receipts.length,0),bandSets={"78c":new Set(),"79c":new Set()};
for(const r of rows)for(const x of r.receipts)bandSets[x.band].add(r.row_hex);
const bandCost={};for(const band of ["78c","79c"])bandCost[band]=[...bandSets[band]].reduce((s,h)=>s+open.get(h).cost,0);
const pairBand={};for(const band of ["78c","79c"])pairBand[band]=rootFold.filter(x=>x.band===band).reduce((s,x)=>s+x.covered_open_rows.length,0);
const afterOpen=new Set(open.keys());for(const r of rows)afterOpen.delete(r.row_hex);
const before=new Map([...parents.keys()].map(p=>[p,{rows:0,cost:0}])),after=new Map([...parents.keys()].map(p=>[p,{rows:0,cost:0}]));
for(const [h] of open)for(const p of rowParents.get(h)||[]){before.get(p).rows++;before.get(p).cost+=open.get(h).cost;}
for(const h of afterOpen)for(const p of rowParents.get(h)||[]){after.get(p).rows++;after.get(p).cost+=open.get(h).cost;}
const affected=new Set(rows.flatMap(r=>r.parents)),parentDeltas=[...affected].sort().map(p=>({parent_hex:p,classes:parents.get(p).classes,rows_before:before.get(p).rows,cost_before:before.get(p).cost,rows_closed:before.get(p).rows-after.get(p).rows,cost_closed:before.get(p).cost-after.get(p).cost,rows_after:after.get(p).rows,cost_after:after.get(p).cost}));
const fully=parentDeltas.filter(p=>p.rows_before>0&&p.rows_after===0),afterNeed=needed(afterOpen);
need(rows.length===19&&totalCost===1542&&pairs===29&&bandSets["78c"].size===5&&bandSets["79c"].size===14&&bandCost["78c"]===387&&bandCost["79c"]===1155&&pairBand["78c"]===15&&pairBand["79c"]===14&&fully.length===1,"fold totals");
const target="00000000000000403800000008000000",td=parentDeltas.find(p=>p.parent_hex===target);
need(td&&td.rows_before===1&&td.rows_after===0&&open.has("00000000000000403800000008000008")&&!open.has("00000000000000c09002000200000000")&&oldGlobal.has("00000000000000c09002000200000000"),"child controls");
const frontier={solved_s6_in_manifest:1608,remaining_s5_orbits:173,unique_remaining_s6:afterOpen.size,sum_remaining_cost:openCost-totalCost,...afterNeed,parent_row_incidence:[...after.values()].reduce((s,x)=>s+x.rows,0)};
const record={schema:"n11-class2-lane-cost78c-79c-combined-receipt-fold-20261118-v1",date:"2026-11-18",status:"fold-complete",source_main_head_before:"62279f626e5f11f58b136861c4c8662e146c3c21",basis_head:gf.frontier_after_receipt_harvest_global_fold,source_blob_pins:Object.fromEntries(Object.entries(PIN).map(([k,v])=>[k,{path:v[0],git_blob_sha1:v[1]}])),certificate_sources:{cost78c:{sweep:"11 WIN7-D10 / 67 REFUTED-D10 / 0 capped",manifest_certificates:11,bigint_independent_verification:"11/11 PASS",cross_lane_agreement:"7/7 PASS"},cost79c:{sweep:"20 WIN7-D10 / 59 REFUTED-D10 / 0 capped",manifest_certificates:19,transferred_win_bit:110,transferred_certificate:"canon-equal to published cost73k bit 87",bigint_third_implementation:"19/19 PASS (3 + 16 split audits)",raw_batch_audit:"19/19 PASS",v15_cross_engine:"14/14 agreement",v13_verdict_conflicts:0}},method:{root_population:"11 cost78c + 19 cost79c published WIN7-D10 certificate roots; cost79c bit110 is not duplicated because its canon-equal cost73k certificate is already in the prior global fold",root_checks:"all 30 roots have 7 stones, match their manifest D4 canon, and equal child | (1 << win_bit); 30 distinct D4 canons",independent_cover_algorithms:["root -> all 8 D4 images -> delete each of 7 stones -> canonicalize the resulting S6 row","each open S6 row -> all 30 roots -> all 8 D4 images -> direct one-stone subset test"],conflict_control:"cost78c cross-lane agreement PASS; cost79c v13 sixteen-map and harvest cross-conflict counts are both zero",fold_order:"cost78c bits ascending, then cost79c bits ascending; per-root marginal is measured against the previously closed row set"},root_checks:{roots:30,distinct_d4_canons:30,all_7_stones:true,all_manifest_canons_match:true,all_child_plus_bit:true,duplicate_canons:0},new_receipt_coverage:{unique_s6_rows:19,total_row_root_pairs:29,closed_edge_cost:1542,rows_with_multiple_receipts:rows.filter(r=>r.receipts.length>1).length,by_band:{cost78c:{certificates:11,new_rows:5,new_edge_cost:387,root_row_pairs:15,marginal_by_bit:marginal["78c"]},cost79c:{certificates:19,new_rows:14,new_edge_cost:1155,root_row_pairs:14,roots_with_no_new_open_row:rootFold.filter(x=>x.band==="79c"&&x.covered_open_rows.length===0).length,marginal_by_bit:marginal["79c"]}},marginal_by_root:rootFold,receipts_by_row:rows},parent_deltas:parentDeltas,parent_closure:{fully_closed_count:1,fully_closed:fully,affected_parents:affected.size,parent_row_incidence_touched:rows.reduce((s,r)=>s+r.parents.length,0)},frontier_after:frontier,controls:{base_frontier_recomputed:[open.size,openCost,baseNeed.s6_needed_by_open_classes,baseNeed.cost_needed_by_open_classes],base_frontier_matches_global_fold:true,two_cover_algorithms_same_19_rows:true,two_cover_algorithms_same_29_root_row_witnesses:true,cost78c_child_was_open:true,cost79c_child_was_already_closed_by_global_fold:true,first_fully_receipt_closed_s5_parent:target,target_parent_rows_before_after:[1,0],target_parent_cost_before_after:[78,0]},interpretation_guard:["This is certificate-receipt and manifest-coverage bookkeeping only; no new engine verdict was created in this fold.","WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone root.","REFUTED-D10 is not a LOSS proof.","The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."]};
fs.writeFileSync(path.join(OUT,"class-frontier-cost78c-79c-receipts-recompute-20261118.json"),JSON.stringify(record,null,2)+"\n");
console.log(JSON.stringify({rows:rows.length,cost:totalCost,pairs,frontier},null,2));
