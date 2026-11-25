#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
const ROOT=process.cwd();
const INPUT="research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json";
const OUTPUT="research/experiments/n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json";
const PIN={sha256:"94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",gitBlobSha1:"730bc378f93c0de8a2ac1bf7941941e4d5a24798",bytes:53914};
const GROUPS=[
["00000000000000003800000008003100","00000000000000801202040020001000","00000000000000821082000000001010","00000000000000821082800000000008","00000000000000821083000000000800","00000000000000909002000080001000","00000000000000919002000000100000","00000010000000003820000008001000","00000010000008801202000000000200"],
["00000000000000003800000008001820","00000000000000003800000008540000","00000000000000043800000008900000","00000000000000083800020008100000","00000000000000801202000000089000","00000000000000889002000000100400","00000000000040809002400000100000","00000000010000809002000800100000","00000010000000801202000200000400"],
["00000000000000003800000209000004","000000000000000038000002c8000000","00000000000000003800000409040000","00000000000000043800200009000000","00000000000000801212000001000100","00000000000084003800000048000000","00000000010000809002000040000001","00000000020000801202000200100000","00000000020008003800000009000000"],
["00000000000000043800000008080010","00000000000000103800000028080000","000000000000008012020000008c0000","00000000000000801222000000800200","00000000000000889002000080000001","00000000000000a09002000480000000","00000000000020809042000080000000","00000000000080801202000000800100","00000000010000809002000080000040"]];
const need=(ok,msg)=>{if(!ok)throw new Error(msg);};
const bytes=fs.readFileSync(path.join(ROOT,INPUT));
const sha256=createHash("sha256").update(bytes).digest("hex");
const gitBlobSha1=createHash("sha1").update(Buffer.concat([Buffer.from("blob "+bytes.length+"\0"),bytes])).digest("hex");
need(bytes.length===PIN.bytes&&sha256===PIN.sha256&&gitBlobSha1===PIN.gitBlobSha1,"source pin mismatch");
const data=JSON.parse(bytes.toString("utf8")),roots=data.per_root,edges=data.pairwise_overlap,n=roots.length;
need(n===36&&edges.length===221,"source shape mismatch");
const index=new Map(roots.map((r,i)=>[r.root,i]));
const candidate=Array(n).fill(-1);
for(let w=0;w<4;w++)for(const root of GROUPS[w]){
 need(index.has(root)&&candidate[index.get(root)]===-1,"unknown or duplicated candidate root");
 candidate[index.get(root)]=w;
}
need(candidate.every(w=>w>=0),"candidate assignment incomplete");
const baseline=roots.map(r=>r.worker);
need(baseline.every((w,i)=>w===i%4),"baseline strided assignment changed");
function cross(assign){let score=0,pairs=0;for(const e of edges)if(assign[index.get(e.a)]!==assign[index.get(e.b)]){score+=e.shared;pairs++;}return {score,pairs};}
function loads(assign){const d4=[0,0,0,0],raw10=[0,0,0,0];for(let i=0;i<n;i++){d4[assign[i]]+=roots[i].d4;raw10[assign[i]]+=roots[i].raw10;}return {d4,raw10};}
function spread(a){return (Math.max(...a)-Math.min(...a))/(a.reduce((s,x)=>s+x,0)/a.length);}
const baselineScore=cross(baseline),candidateScore=cross(candidate),baselineLoads=loads(baseline),candidateLoads=loads(candidate);
const totalOverlap=edges.reduce((s,e)=>s+e.shared,0);
let feasibleSwaps=0,improvingSwaps=0,bestNeighbor=candidateScore.score;
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(candidate[i]!==candidate[j]){
 const b=candidate.slice();[b[i],b[j]]=[b[j],b[i]];
 if(spread(loads(b).d4)<=.08){feasibleSwaps++;const s=cross(b).score;if(s<candidateScore.score){improvingSwaps++;bestNeighbor=Math.min(bestNeighbor,s);}}
}
const checks=[
{name:"source blob and SHA pin",pass:bytes.length===PIN.bytes&&sha256===PIN.sha256&&gitBlobSha1===PIN.gitBlobSha1},
{name:"36 roots assigned exactly once",pass:new Set(GROUPS.flat()).size===36&&candidate.every(w=>w>=0)},
{name:"9 roots per worker",pass:GROUPS.every(g=>g.length===9)},
{name:"baseline matches published summary",pass:baselineScore.score===data.summary.cross_worker_pairwise_overlap},
{name:"candidate overlap audited",pass:candidateScore.score===2000},
{name:"pairwise overlap conservation",pass:totalOverlap===5435},
{name:"candidate D4 load spread <=8%",pass:spread(candidateLoads.d4)<=.08},
{name:"candidate raw10 load spread <=8%",pass:spread(candidateLoads.raw10)<=.08},
{name:"no feasible one-swap improvement",pass:improvingSwaps===0}];
need(checks.every(c=>c.pass),"candidate validation failed");
const result={
schema:"n11-residual72-worker-partition-candidate-20261121-v1",
date:"2026-11-21",status:"exploratory-geometric-partition-candidate",
source:{main_commit:"c74dfd0c0b2c8795236e3064153531f5c7452d01",path:INPUT,sha256:PIN.sha256,git_blob_sha1:PIN.gitBlobSha1,bytes:PIN.bytes},
algorithm:{name:"deterministic simulated annealing",seed:"0xD41F11",restarts:10,swaps_per_restart:120000,randomization_swaps_after_first_start:500,balance_constraint:"D4-membership load spread <= 8%",objective:"minimize pairwise 10-stone D4 overlap across workers",temperature:"45 * 0.01^(iteration / 120000) + 0.05",global_optimum:false,search_reproduction_in_script:false},
baseline:{worker_roots:"roots[W::4]",root_counts:[9,9,9,9],cross_worker_pairwise_overlap:baselineScore.score,within_worker_pairwise_overlap:totalOverlap-baselineScore.score,cross_worker_pair_count:baselineScore.pairs,loads:baselineLoads,load_spread_percent:{d4:spread(baselineLoads.d4)*100,raw10:spread(baselineLoads.raw10)*100}},
candidate:{root_groups:GROUPS,root_counts:GROUPS.map(g=>g.length),cross_worker_pairwise_overlap:candidateScore.score,within_worker_pairwise_overlap:totalOverlap-candidateScore.score,cross_worker_pair_count:candidateScore.pairs,loads:candidateLoads,load_spread_percent:{d4:spread(candidateLoads.d4)*100,raw10:spread(candidateLoads.raw10)*100},crossworker_share_of_pairwise_overlap_percent:candidateScore.score/totalOverlap*100},
comparison:{total_pairwise_overlap:totalOverlap,cross_worker_overlap_reduction_percent:(baselineScore.score-candidateScore.score)/baselineScore.score*100,baseline_crossworker_share_percent:baselineScore.score/totalOverlap*100,one_swap_check:{feasible_swaps:feasibleSwaps,improving_swaps:improvingSwaps,best_neighbor_score:bestNeighbor,local_optimum_under_constraint:improvingSwaps===0}},
checks,check_count:checks.length,all_pass:true,
interpretation_guard:["Geometric overlap only; not actual DFPN transposition-table hits.","A shared D4 class does not imply equal search depth or reusable proof boundary.","This is a heuristic partition candidate, not a globally optimal assignment.","Do not change the active 36-root depth-10 sweep assignment before actual TT-hit measurements.","The full 10-stone class-membership regeneration attempt timed out; no exact per-worker class-copy count is claimed."]};
fs.mkdirSync(path.dirname(path.join(ROOT,OUTPUT)),{recursive:true});
fs.writeFileSync(path.join(ROOT,OUTPUT),JSON.stringify(result,null,2)+"\n");
process.stdout.write(JSON.stringify({checks,crossworkerOverlap:baselineScore.score+" -> "+candidateScore.score,feasibleSwaps,improvingSwaps},null,2)+"\n");
