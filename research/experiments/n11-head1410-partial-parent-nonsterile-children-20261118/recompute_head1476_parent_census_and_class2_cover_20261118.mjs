#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const EXP = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118";
const INPUTS = {
  worklist: "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
  census: "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
  ledger: EXP + "/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json"
};
const PINS = {
  worklist: "2fee1d0718547a62e346d35f5858d7913e37c097",
  census: "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
  ledger: "e8785d509e8a11a37c0d03cc450455a14708c34d"
};
const N = 11;
const T = [
  (x,y) => [x,y], (x,y) => [y,N-1-x], (x,y) => [N-1-x,N-1-y], (x,y) => [N-1-y,x],
  (x,y) => [N-1-x,y], (x,y) => [x,N-1-y], (x,y) => [y,x], (x,y) => [N-1-y,N-1-x]
];
const fail = message => { throw new Error(message); };
const gitBlobSha = data => createHash("sha1").update(Buffer.from("blob " + data.length + "\0")).update(data).digest("hex");
function readPinned(name) {
  const data = fs.readFileSync(path.join(ROOT, INPUTS[name]));
  const sha = gitBlobSha(data);
  if (sha !== PINS[name]) fail(name + " Git blob SHA mismatch: " + sha);
  return data;
}
function transform(mask, t) {
  let out = 0n;
  for (let i=0;i<121;i++) if ((mask >> BigInt(i)) & 1n) {
    const q=t(i%N,Math.floor(i/N));
    out |= 1n << BigInt(q[1]*N+q[0]);
  }
  return out;
}
function canon(mask) {
  let best=null;
  for (const t of T) { const v=transform(mask,t); if (best===null || v<best) best=v; }
  return best.toString(16).padStart(32,"0");
}
function bitsOf(mask) {
  const out=[];
  for (let i=0;i<121;i++) if ((mask >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function popcount(mask) {
  let x=mask,n=0;
  while (x) { x &= x-1n; n++; }
  return n;
}
function det3(a,b,c) {
  const x1=a%N,y1=Math.floor(a/N),x2=b%N,y2=Math.floor(b/N),x3=c%N,y3=Math.floor(c/N);
  const A=BigInt(x1*x1+y1*y1),B=BigInt(x1),C=BigInt(y1);
  const D=BigInt(x2*x2+y2*y2),E=BigInt(x2),F=BigInt(y2);
  const G=BigInt(x3*x3+y3*y3),H=BigInt(x3),I=BigInt(y3);
  return A*(E*I-F*H)-B*(D*I-F*G)+C*(D*H-E*G);
}
const det4=(a,b,c,d)=>det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d);
const sumCost=rows=>rows.reduce((s,r)=>s+Number(r.own_candidates_s6_s7_edge_cost),0);
const classify=(rows,sterile)=>{
  if (!rows.length) return "closed";
  const n=rows.filter(r=>sterile.has(r.s6_canonical_hex)).length;
  return n===rows.length ? "all_remaining_sterile" : n===0 ? "no_sterile" : "partial_sterile";
};
const lexLess=(a,b)=>{
  for(let i=0;i<Math.min(a.length,b.length);i++) if(a[i]!==b[i]) return a[i]<b[i];
  return a.length<b.length;
};
function run() {
  const worklistBytes=readPinned("worklist"), censusBytes=readPinned("census"), ledgerBytes=readPinned("ledger");
  const lines=worklistBytes.toString("utf8").trimEnd().split(/\r?\n/);
  const headers=lines[0].split(",").map(x=>x.trim());
  const rows=lines.slice(1).map(line=>{
    const values=line.split(","), out={};
    headers.forEach((h,i)=>out[h]=values[i]?.trim()??"");
    return out;
  });
  const census=JSON.parse(censusBytes.toString("utf8"));
  const ledger=JSON.parse(ledgerBytes.toString("utf8"));
  const parents=census.open_s5_census;
  const sterile=new Set(census.sterile_row_registry.map(x=>x.hex));
  const closedRows=ledger.derived.closed_rows_66, closed=new Set(closedRows);
  const rowByHex=new Map(rows.map(r=>[r.s6_canonical_hex,r]));
  const rowMasks=rows.map(r=>({r,m:BigInt("0x"+r.s6_canonical_hex)}));
  const checks=[];
  const check=(name,ok,detail="")=>checks.push({name,pass:!!ok,detail:typeof detail==="string"?detail:JSON.stringify(detail)});
  check("worklist.rows",rows.length===6438 && rows.every(r=>popcount(BigInt("0x"+r.s6_canonical_hex))===6),rows.length);
  check("worklist.cost",sumCost(rows)===509109,sumCost(rows));
  check("parents.count",parents.length===174,parents.length);
  check("fold.closed",closedRows.length===66 && closed.size===66 && [...closed].every(h=>rowByHex.has(h)),"");
  const records=[];
  let baseRefs=0,baseSterile=0,currentRefs=0,currentSterile=0;
  const baseCounts={all_remaining_sterile:0,partial_sterile:0,no_sterile:0,closed:0};
  const headCounts={all_remaining_sterile:0,partial_sterile:0,no_sterile:0,closed:0};
  for(const p of parents){
    const mask=BigInt("0x"+p.hex), variants=T.map(t=>transform(mask,t));
    const base=[];
    for(const item of rowMasks) if(variants.some(v=>(v&item.m)===v)) base.push(item.r);
    const sbase=base.filter(r=>sterile.has(r.s6_canonical_hex));
    const sbaseHex=sbase.map(r=>r.s6_canonical_hex).sort();
    check("baseline.rows."+p.hex,base.length===p.remaining_s6_orbits,base.length);
    check("baseline.cost."+p.hex,sumCost(base)===p.remaining_s7_edge_cost,sumCost(base));
    check("baseline.sterile."+p.hex,sbase.length===p.sterile_refs_count,sbase.length);
    check("baseline.sterile_exact."+p.hex,JSON.stringify(sbaseHex)===JSON.stringify((p.sterile_refs||[]).map(x=>x.hex).sort()),"");
    const current=base.filter(r=>!closed.has(r.s6_canonical_hex));
    const s=current.filter(r=>sterile.has(r.s6_canonical_hex));
    const n=current.filter(r=>!sterile.has(r.s6_canonical_hex));
    const bc=classify(base,sterile),hc=classify(current,sterile);
    baseCounts[bc]++;headCounts[hc]++;
    baseRefs+=base.length;baseSterile+=sbase.length;currentRefs+=current.length;currentSterile+=s.length;
    const sumField=f=>n.reduce((v,r)=>v+Number(r[f]),0);
    records.push({
      hex:p.hex,classes:p.classes,base_rows:base.length,base_cost:sumCost(base),base_sterile_rows:sbase.length,base_class:bc,
      head1476_rows:current.length,head1476_cost:sumCost(current),head1476_sterile_rows:s.length,
      nonsterile_rows:n.length,nonsterile_cost:sumCost(n),
      open_candidates_after_transfers:sumField("open_candidates_after_transfers"),
      engine_win7_d10:sumField("engine_win7_d10"),engine_refuted_d10:sumField("engine_refuted_d10"),
      transferred_refuted_d10:sumField("transferred_refuted_d10"),head1476_class:hc,
      remaining_rows:current.map(r=>r.s6_canonical_hex).sort()
    });
  }
  check("baseline.census_totals",baseRefs===12274 && baseSterile===91 && baseCounts.all_remaining_sterile===3 && baseCounts.partial_sterile===57 && baseCounts.no_sterile===114,{baseRefs,baseSterile,baseCounts});
  const remaining=rows.filter(r=>!closed.has(r.s6_canonical_hex));
  check("head1476.global",remaining.length===6372 && sumCost(remaining)===504389,{rows:remaining.length,cost:sumCost(remaining)});
  check("head1476.sterile_retained",sterile.size===35 && [...sterile].every(h=>rowByHex.has(h)&&!closed.has(h)),"");
  check("head1476.parent_counts",headCounts.all_remaining_sterile===4 && headCounts.partial_sterile===56 && headCounts.no_sterile===114,headCounts);
  check("head1476.incidences",currentRefs===12143 && currentSterile===91 && currentRefs-currentSterile===12052,{currentRefs,currentSterile});
  const newly=records.filter(p=>p.base_class==="partial_sterile" && p.head1476_class==="all_remaining_sterile");
  check("head1476.newly_full",newly.length===1 && newly[0].hex==="00000000000000801202000040000000",newly);
  const fullParents=records.filter(p=>p.head1476_class==="all_remaining_sterile").sort((a,b)=>a.classes-b.classes||a.head1476_rows-b.head1476_rows);
  const class2=records.filter(p=>p.classes===2 && p.head1476_rows>0 && p.head1476_sterile_rows===0)
    .sort((a,b)=>a.nonsterile_cost-b.nonsterile_cost || a.nonsterile_rows-b.nonsterile_rows || a.hex.localeCompare(b.hex));
  const target=class2[0];
  check("target.best_class2",target.hex==="00000000000000403800000008000000" && target.base_rows===24 && target.base_cost===1704 && target.head1476_rows===11 && target.head1476_cost===806,target);
  const targetRows=target.remaining_rows.map(h=>rowByHex.get(h)).sort((a,b)=>a.s6_canonical_hex.localeCompare(b.s6_canonical_hex));
  const targetHexes=new Set(targetRows.map(r=>r.s6_canonical_hex)), rootMap=new Map(), rowDetails=[];
  for(const r of targetRows){
    const m=BigInt("0x"+r.s6_canonical_hex),stones=bitsOf(m);
    let count=0;
    for(let d=0;d<121;d++){
      if((m>>BigInt(d))&1n) continue;
      let ok=true;
      for(let i=0;i<6&&ok;i++) for(let j=i+1;j<6&&ok;j++) for(let k=j+1;k<6;k++)
        if(det4(stones[i],stones[j],stones[k],d)===0n){ok=false;break;}
      if(ok){
        count++;
        const root=canon(m|(1n<<BigInt(d)));
        if(!rootMap.has(root)) rootMap.set(root,{root,occurrences:[]});
        rootMap.get(root).occurrences.push({row:r.s6_canonical_hex,bit:d});
      }
    }
    const cost=Number(r.own_candidates_s6_s7_edge_cost);
    check("candidate.count."+r.s6_canonical_hex,count===cost,count+" / "+cost);
    check("candidate.open."+r.s6_canonical_hex,Number(r.engine_win7_d10)===0 && Number(r.engine_refuted_d10)===0 &&
      Number(r.transferred_refuted_d10)===0 && Number(r.open_candidates_after_transfers)===cost,"");
    rowDetails.push({hex:r.s6_canonical_hex,candidates:count,open_after_transfers:Number(r.open_candidates_after_transfers)});
  }
  const roots=[...rootMap.values()].sort((a,b)=>a.root.localeCompare(b.root));
  const rowIndex=new Map(targetRows.map((r,i)=>[r.s6_canonical_hex,i]));
  for(const item of roots){
    const mask=BigInt("0x"+item.root),bits=bitsOf(mask),cover=new Set();
    for(const d of bits){
      const sub=mask^(1n<<BigInt(d)),h=canon(sub);
      if(targetHexes.has(h)) cover.add(h);
    }
    item.cover_rows=[...cover].sort();
    item.cover_mask=item.cover_rows.reduce((m,h)=>m|(1<<rowIndex.get(h)),0);
    item.occurrences.sort((a,b)=>a.row.localeCompare(b.row)||a.bit-b.bit);
  }
  const hist={};
  for(const x of roots) hist[x.cover_rows.length]=(hist[x.cover_rows.length]||0)+1;
  const singleton=Array(targetRows.length).fill(0),pairs=new Map();
  for(const x of roots){
    if(x.cover_rows.length===1) singleton[rowIndex.get(x.cover_rows[0])]++;
    else if(x.cover_rows.length===2){
      const ids=x.cover_rows.map(h=>rowIndex.get(h)).sort((a,b)=>a-b),key=ids[0]+":"+ids[1];
      pairs.set(key,(pairs.get(key)||0)+1);
    }
  }
  const full=(1<<targetRows.length)-1,dp=Array(1<<targetRows.length).fill(null);dp[0]={count:0,roots:[]};
  for(const x of roots){
    const old=dp.slice();
    for(let mask=0;mask<=full;mask++) if(old[mask]){
      const next=mask|x.cover_mask;if(next===mask)continue;
      const cand={count:old[mask].count+1,roots:[...old[mask].roots,x.root]},cur=dp[next];
      if(!cur || cand.count<cur.count || (cand.count===cur.count && lexLess(cand.roots,cur.roots))) dp[next]=cand;
    }
  }
  const memo=new Map();
  function countMatch(mask){
    if(mask===0)return 1;
    if(memo.has(mask))return memo.get(mask);
    let first=0;while(((mask>>first)&1)===0)first++;
    let total=0;
    for(let j=first+1;j<targetRows.length;j++) if(mask&(1<<j)){
      const ways=pairs.get(first+":"+j)||0;
      if(ways) total+=ways*countMatch(mask&~(1<<first)&~(1<<j));
    }
    memo.set(mask,total);return total;
  }
  let matchingSum=0,minCoverCount=0;
  for(let i=0;i<targetRows.length;i++){
    const ways=countMatch(full&~(1<<i));matchingSum+=ways;minCoverCount+=singleton[i]*ways;
  }
  const minimum=dp[full];
  check("candidate.occurrences",rowDetails.reduce((s,x)=>s+x.candidates,0)===806,806);
  check("candidate.distinct_roots",roots.length===757,roots.length);
  check("candidate.cover_histogram",hist[1]===708 && hist[2]===49 && Object.keys(hist).length===2,hist);
  check("candidate.minimum_cover",minimum.count===6 && Math.ceil(targetRows.length/2)===6,minimum.count);
  check("candidate.minimum_cover_count",minCoverCount===337020 && matchingSum===5250,{minCoverCount,matchingSum});
  const scheduled=rows.filter(r=>r.category==="win_receipt_scheduled");
  const nonScheduled=rows.filter(r=>r.category!=="win_receipt_scheduled");
  const statusTotals={
    engine_win7_d10:rows.reduce((s,r)=>s+Number(r.engine_win7_d10),0),
    engine_refuted_d10:rows.reduce((s,r)=>s+Number(r.engine_refuted_d10),0),
    transferred_refuted_d10:rows.reduce((s,r)=>s+Number(r.transferred_refuted_d10),0),
    open_candidates_after_transfers:rows.reduce((s,r)=>s+Number(r.open_candidates_after_transfers),0)
  };
  check("candidate.accounting",nonScheduled.every(r=>Number(r.own_candidates_s6_s7_edge_cost)===
    Number(r.engine_win7_d10)+Number(r.engine_refuted_d10)+Number(r.transferred_refuted_d10)+Number(r.open_candidates_after_transfers)) &&
    scheduled.length===9 && sumCost(scheduled)===635 && scheduled.every(r=>
    Number(r.engine_win7_d10)+Number(r.engine_refuted_d10)+Number(r.transferred_refuted_d10)+Number(r.open_candidates_after_transfers)===0),
    {scheduled:scheduled.length,scheduledCost:sumCost(scheduled),statusTotals});
  const cover=minimum.roots.map(root=>{
    const x=rootMap.get(root);return {root,cover_rows:x.cover_rows,occurrences:x.occurrences};
  });
  const output={
    schema:"n11-head1476-parent-census-and-class2-cover-20261118-v1",
    date:"2026-11-18",
    source_main_commit:"aa3af62b6394699d42fe08a62bc8c5032717545a",
    inputs:{worklist:{path:INPUTS.worklist,git_blob_sha1:PINS.worklist},census:{path:INPUTS.census,git_blob_sha1:PINS.census},ledger:{path:INPUTS.ledger,git_blob_sha1:PINS.ledger}},
    method:"Direct D4 parent-transform subset join (not the preceding 5-subset canonical index), followed by subtraction of the 66 globally closed rows. BigInt det4 re-enumeration of the selected 11 S6 rows. Exact 2^11 set-cover DP plus independent singleton/perfect-matching count.",
    head1410:{rows:rows.length,cost:sumCost(rows),parents:parents.length,parent_incidences:baseRefs,sterile_incidences:baseSterile,class_counts:baseCounts},
    head1476:{closed_rows:closed.size,rows:remaining.length,cost:sumCost(remaining),parents:parents.length,parent_incidences:currentRefs,sterile_incidences:currentSterile,effective_incidences:currentRefs-currentSterile,sterile_rows:sterile.size,class_counts:headCounts,fully_sterile_parents:fullParents,newly_fully_sterile_parents:newly},
    class2_own_closable_top12:class2.slice(0,12),
    selected_parent:{hex:target.hex,base_rows:target.base_rows,base_cost:target.base_cost,head1476_rows:target.head1476_rows,head1476_cost:target.head1476_cost,sterile_rows:target.head1476_sterile_rows,open_candidates_after_transfers:target.open_candidates_after_transfers,target_s6_rows:rowDetails},
    candidate_cover:{
      occurrences:806,distinct_d4_roots:roots.length,coverage_histogram:hist,
      pair_edges:pairs.size,singleton_roots:singleton.reduce((a,b)=>a+b,0),
      minimum_roots:minimum.count,lower_bound:6,weighted_perfect_matchings:matchingSum,minimum_cover_sets:minCoverCount,
      lexicographically_first_minimum_cover:cover,
      all_candidate_roots:roots.map(x=>({root:x.root,cover_rows:x.cover_rows,occurrences:x.occurrences}))
    },
    candidate_accounting:{scheduled_rows:scheduled.length,scheduled_cost:sumCost(scheduled),status_totals:statusTotals},
    checks,check_count:checks.length,all_pass:checks.every(x=>x.pass),
    interpretation_guard:"No 7-stone search, new WIN7-D10/REFUTED-D10 verdict, receipt fold, or S5 closure was produced. The six-root set is only a minimum geometric cover if all six later yield valid WIN7-D10 certificates. REFUTED-D10 and STERILE are not LOSS proofs.",
    unknown_status:"Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  };
  const out=process.argv[2] ? path.resolve(process.argv[2]) : path.join(ROOT,EXP,"output/head1476-parent-census-and-class2-cover-20261118.json");
  fs.writeFileSync(out,JSON.stringify(output,null,2)+"\n");
  process.stdout.write(JSON.stringify({out,all_pass:output.all_pass,checks:checks.length,head1476:output.head1476,candidate_cover:{occurrences:806,roots:roots.length,hist,minimum:minimum.count,minimum_cover_sets:minCoverCount,cover},failed:checks.filter(x=>!x.pass)},null,2)+"\n");
  if(!output.all_pass) process.exitCode=1;
}
run();
