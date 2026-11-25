#!/usr/bin/env node
// Third independent exact replay of the six cost-76a WIN7 certificates.
// Circle membership uses rational circumcentre numerators; collinear triples
// use an exact line branch, as required by K0001's circle-or-line rule.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const HERE=path.dirname(fileURLToPath(import.meta.url));
const OUT=path.resolve(HERE,"..","output");
const REPO=path.resolve(OUT,"../../../..");
const P="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/";
const read=(rel)=>fs.readFileSync(path.resolve(REPO,rel));
const sha=(b,a)=>createHash(a).update(b).digest("hex");
const gitsha=b=>sha(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b]),"sha1");
const check=(v,m)=>{if(!v)throw new Error(m);};
const pinned=(rel,id)=>{const b=read(rel);check(gitsha(b)===id,"input blob mismatch: "+rel);return b;};

const manifest=JSON.parse(pinned(P+"class2-lane-cost76a-win7-certificates-20261115.json","f3be0e0edfc4ddf5da327dc545de7009926407ef"));
const rawAudit=JSON.parse(pinned(P+"class2-lane-cost76a-sweep-audit-20261115.json","c754fab60060f8e6ae76bf6215e1559810eaa29e"));
const v15=pinned(P+"class2-lane-cost76a-v15-crosscheck-20261115.jsonl","920bb32f6fb18dcff01c5a0084364ddf9cd5a5a5").toString("utf8").trim().split(/\r?\n/).map(JSON.parse);
const topText=pinned(P+"class-frontier-top-candidates-s6-after-cost72b-receipts-20261115.csv","03641c2be60e23d663d7e433969725117cb7eecf").toString("utf8");
const rankText=pinned(P+"class-frontier-s5-ranking-after-cost72b-receipts-20261115.csv","f2ccbf562bfd853d24ad1f345a4c9e7cf46bc28c").toString("utf8");
const claim=JSON.parse(read(P+"class2-lane-cost76a-inflight-20261115.json").toString("utf8"));

const FULL=(1n<<121n)-1n, tripleCache=new Map(), legalCache=new Map();
function circleOrLineMask(a,b,c){
  const key=a+","+b+","+c,old=tripleCache.get(key);if(old!==undefined)return old;
  const ax=a%11,ay=Math.floor(a/11),x2=b%11-ax,y2=Math.floor(b/11)-ay,x3=c%11-ax,y3=Math.floor(c/11)-ay;
  const cross=x2*y3-y2*x3;let mask=0n;
  if(cross===0){
    for(let d=0;d<121;d++){const dx=d%11-ax,dy=Math.floor(d/11)-ay;if(x2*dy-y2*dx===0)mask|=1n<<BigInt(d);}
    tripleCache.set(key,mask);return mask;
  }
  const den=2n*BigInt(cross),s2=BigInt(x2*x2+y2*y2),s3=BigInt(x3*x3+y3*y3);
  const un=s2*BigInt(y3)-s3*BigInt(y2),vn=BigInt(x2)*s3-BigInt(x3)*s2,rhs=un*un+vn*vn;
  for(let d=0;d<121;d++){const dx=BigInt(d%11-ax),dy=BigInt(Math.floor(d/11)-ay),px=dx*den-un,py=dy*den-vn;if(px*px+py*py===rhs)mask|=1n<<BigInt(d);}
  tripleCache.set(key,mask);return mask;
}
function points(mask){const a=[];for(let p=0;p<121;p++)if((mask>>BigInt(p))&1n)a.push(p);return a;}
function legalMask(ps){
  const key=ps.join(","),old=legalCache.get(key);if(old!==undefined)return old;
  let ban=0n;for(const p of ps)ban|=1n<<BigInt(p);
  for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++)for(let k=j+1;k<ps.length;k++)ban|=circleOrLineMask(ps[i],ps[j],ps[k]);
  const m=FULL&~ban;legalCache.set(key,m);return m;
}
function bits(mask){const a=[];for(let p=0;p<121;p++)if((mask>>BigInt(p))&1n)a.push(p);return a;}
function mapPoint(p,s){
  const x=p%11,y=Math.floor(p/11);let a,b;
  switch(s){case 0:a=x;b=y;break;case 1:a=y;b=10-x;break;case 2:a=10-x;b=10-y;break;case 3:a=10-y;b=x;break;case 4:a=10-x;b=y;break;case 5:a=x;b=10-y;break;case 6:a=y;b=x;break;case 7:a=10-y;b=10-x;break;default:throw Error("bad D4");}
  return 11*b+a;
}
function image(mask,s){let z=0n;for(let p=0;p<121;p++)if((mask>>BigInt(p))&1n)z|=1n<<BigInt(mapPoint(p,s));return z;}
function canon(mask){let best=null,sym=-1;for(let s=0;s<8;s++){const z=image(mask,s);if(best===null||z<best){best=z;sym=s;}}return {hex:best.toString(16).padStart(32,"0"),symmetry:sym};}

function verify(spec){
  const parts=spec.storage.parts.map(p=>{const b=read(p.path);check(b.length===p.bytes,"part size "+p.path);check(gitsha(b)===p.git_blob_sha,"part SHA "+p.path);return b;});
  if(parts.length>1){check(parts[0][parts[0].length-1]===10,"split not at LF");check(/^[0-9a-f]{32} \d+\n/.test(parts[1].toString("utf8")),"part2 mid-row");}
  const raw=Buffer.concat(parts);check(raw.length===spec.bytes,"whole size");check(sha(raw,"md5")===spec.md5,"whole md5");check(sha(raw,"sha256")===spec.sha256,"whole sha256");check(gitsha(raw)===spec.whole_git_blob_sha,"whole Git SHA");
  const lines=raw.toString("utf8").split(/\r?\n/);if(lines.at(-1)==="")lines.pop();
  check(lines[0]==="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS","header");
  check(lines[1]==="root "+spec.root_hex,"root");
  const strategy=new Map();let prev="";
  for(const line of lines.slice(2)){const m=line.match(/^([0-9a-f]{32}) (\d+)$/);check(m!==null,"bad row");check(m[1]>prev,"not sorted-unique");prev=m[1];const board=BigInt("0x"+m[1]);check(board<=FULL,"board range");const mv=Number(m[2]);check(Number.isInteger(mv)&&mv>=0&&mv<121,"move range");strategy.set(m[1],mv);}
  check(strategy.size===spec.rows,"row count");
  const root=BigInt("0x"+spec.root_hex),rp=points(root);check(rp.length===7,"root stones");
  check(canon(root).hex===spec.d4_canonical_hex,"root D4");
  for(let i=0;i<7;i++)for(let j=i+1;j<7;j++)for(let k=j+1;k<7;k++){
    const t=(1n<<BigInt(rp[i]))|(1n<<BigInt(rp[j]))|(1n<<BigInt(rp[k]));
    check((circleOrLineMask(rp[i],rp[j],rp[k])&(root&~t))===0n,"unsafe root");
  }
  const rm=bits(legalMask(rp));check(rm.length===spec.root_check.loser_mobility,"root mobility");
  const sr=rawAudit.win_roots.find(x=>x.bit===spec.bit);check(sr&&sr.root_hex===spec.root_hex&&sr.opponent_legal_replies===rm.length&&sr.nodes===spec.v16_sweep_nodes,"sweep anchor");
  const vr=v15.find(x=>x.bit===spec.bit);check(vr&&vr.loss===true&&vr.capped===false&&vr.nodes===spec.v15_anchor_crosscheck.nodes,"v15 anchor");
  const consumed=new Set();let visited=0,winner=0,loser=0,edges=0,term=0,tmin=99,tmax=0;
  for(const first of rm){const stack=[[root|(1n<<BigInt(first)),0]],seen=new Set();while(stack.length){
    const [board,depth]=stack.pop(),hex=board.toString(16).padStart(32,"0");if(seen.has(hex))continue;seen.add(hex);visited++;
    const ps=points(board),opts=legalMask(ps);
    if(opts===0n){check(depth%2===1,"winner terminal");check(!strategy.has(hex),"terminal row");term++;tmin=Math.min(tmin,ps.length);tmax=Math.max(tmax,ps.length);}
    else if(depth%2===0){winner++;const mv=strategy.get(hex);check(mv!==undefined,"missing WIN row");check(((opts>>BigInt(mv))&1n)===1n,"illegal WIN move");consumed.add(hex);stack.push([board|(1n<<BigInt(mv)),depth+1]);}
    else{loser++;check(!strategy.has(hex),"LOSS row present");for(const mv of bits(opts)){edges++;stack.push([board|(1n<<BigInt(mv)),depth+1]);}}
  }}
  let missing=0,extra=0;for(const k of strategy.keys())if(!consumed.has(k))missing++;for(const k of consumed)if(!strategy.has(k))extra++;
  check(missing===0&&extra===0,"consumed union");check(tmin>=13&&tmax<=17,"terminal range");
  check(visited===spec.visited_states_across_subroots&&winner===spec.winner_states&&loser===spec.loser_states&&edges===spec.loser_reply_edges&&term===spec.terminal_count,"manifest replay totals");
  return {bit:spec.bit,root_hex:spec.root_hex,d4_canonical_hex:spec.d4_canonical_hex,bytes:raw.length,rows:strategy.size,mobility:rm.length,subroots:rm.length,visited,winner_states:winner,loser_states:loser,loser_reply_edges:edges,terminal_count:term,terminal_range:[tmin,tmax],union_missing:missing,union_extra:extra,v15_nodes:vr.nodes,v16_sweep_nodes:sr.nodes,whole_git_blob_sha:spec.whole_git_blob_sha};
}
const replay=manifest.certificates.map(verify);
check(new Set(replay.map(x=>x.d4_canonical_hex)).size===6,"root D4 duplicate");
const totals={certificates:replay.length,bytes:replay.reduce((s,x)=>s+x.bytes,0),rows:replay.reduce((s,x)=>s+x.rows,0),subroots:replay.reduce((s,x)=>s+x.subroots,0),visited:replay.reduce((s,x)=>s+x.visited,0),winner_states:replay.reduce((s,x)=>s+x.winner_states,0),loser_states:replay.reduce((s,x)=>s+x.loser_states,0),loser_reply_edges:replay.reduce((s,x)=>s+x.loser_reply_edges,0),terminals:replay.reduce((s,x)=>s+x.terminal_count,0)};
check(totals.rows===manifest.totals.rows&&totals.visited===manifest.totals.visited_states_across_subroots,"manifest totals");

const topRows=[];for(const line of topText.split(/\r?\n/)){const m=line.match(/^([0-9a-f]{32}),([0-9a-f]{32}),(\d+),/);if(m)topRows.push({s5:m[1],s6:m[2],cost:Number(m[3])});}
const topByS6=new Map(topRows.map(x=>[x.s6,x]));
const rank=new Map();for(const line of rankText.split(/\r?\n/)){const m=line.match(/^([0-9a-f]{32}),(\d+),(\d+),(\d+)$/);if(m)rank.set(m[1],{classes:+m[2],remaining:+m[3],cost:+m[4]});}
const groups=new Map();let incidences=0;
for(const spec of manifest.certificates){const root=BigInt("0x"+spec.root_hex);for(const removed of points(root)){incidences++;const p=root^(1n<<BigInt(removed)),c=canon(p),mv=mapPoint(removed,c.symmetry);let g=groups.get(c.hex);if(!g){g={hex:c.hex,incidences:[],moves:new Set()};groups.set(c.hex,g);}g.incidences.push({bit:spec.bit,removed});g.moves.add(mv);}}
check(incidences===42&&groups.size===37,"parent lift totals");
const uniqueParentMovePairs=[...groups.values()].reduce((sum,g)=>sum+g.moves.size,0);
check(uniqueParentMovePairs===42,"unique parent-move pair total");
const topParentGroups=[...groups.values()].filter(g=>topRows.some(row=>row.s6===g.hex)).length;
check(topParentGroups===2,"top-candidate parent count");
check(claim.chain_head.startsWith("1188/6659/525437/4929/389160"),"frontier head snapshot");
const groupFor=hex=>groups.get(canon(BigInt("0x"+hex)).hex);
const s5A=manifest.sweep_source.s5_parent_hex,s6A=manifest.sweep_source.s6_child_hex;
const gA=groupFor(s6A),movesA=[...gA.moves].sort((a,b)=>a-b);
check(movesA.join(",")==="11,29,66,80,92,96","shared S6 moves");
const rowA=topByS6.get(canon(BigInt("0x"+s6A)).hex),rankA=rank.get(s5A);
check(rowA&&rowA.s5===s5A&&rowA.cost===76&&rankA.classes===2&&rankA.remaining===4&&rankA.cost===297,"S5 A snapshot");
const legalA=bits(legalMask(points(BigInt("0x"+s6A))));check(legalA.length===76&&movesA.every(x=>legalA.includes(x)),"S6 A legal edges");

const claimB=claim.open_parents_at_head_1188.find(x=>x.s5_hex==="00000000000000801202000000000400");
check(claimB&&claimB.remaining_s6_orbits===77&&claimB.remaining_s7_edge_cost===6296&&claimB.lift_stones.join(",")==="56","S5 B snapshot");
const s5B=BigInt("0x"+claimB.s5_hex),reduced=BigInt("0x"+s6A)^(1n<<56n);let symB=-1;
for(let s=0;s<8;s++)if(image(reduced,s)===s5B)symB=s;
check(symB>=0,"S5 B D4 lift");
const s6B=image(BigInt("0x"+s6A),symB),addedB=mapPoint(56,symB),movesB=movesA.map(x=>mapPoint(x,symB)).sort((a,b)=>a-b);
check(s6B===(s5B|(1n<<BigInt(addedB)))&&addedB===64,"S5 B added move");
const legalB=bits(legalMask(points(s6B)));check(legalB.length===76&&movesB.every(x=>legalB.includes(x)),"S6 B legal edges");
const rankB=rank.get(claimB.s5_hex);check(rankB&&rankB.classes===2&&rankB.remaining===77&&rankB.cost===6296,"S5 B ranking");

const s5C="00000000000000801202000000200000",s6C="00000000000000801202000000200400",gC=groupFor(s6C);
const rowC=topByS6.get(canon(BigInt("0x"+s6C)).hex),rankC=rank.get(s5C);
check(gC&&[...gC.moves].join(",")==="64"&&rowC&&rowC.cost===81&&rankC.remaining===41&&rankC.cost===3058,"S5 C snapshot");
check(topRows.filter(x=>x.s5===s5C).length===41,"S5 C top rows");
const s5CM=BigInt("0x"+s5C),s6CM=BigInt("0x"+s6C);check((s5CM|(1n<<10n))===s6CM,"S5 C lift");
check((legalMask(points(s5CM))&(1n<<10n))!==0n,"S5 C added move");
const legalC=bits(legalMask(points(s6CM)));check(legalC.length===81&&legalC.includes(64),"S6 C legal edge");

const result={
  status:"PASS",date:"2026-11-15",method:"exact BigInt rational circumcentre plus exact collinearity branch; no repository verifier/solver/cache or floating point",
  certificate_replay:{certificates:replay,totals,manifest_extraction_nodes:manifest.totals.extraction_nodes,all_roots_D4_distinct:true,all_unions_exact:true},
  edge_lifts:{parent_incidences:incidences,unique_D4_parent_orbits:groups.size,unique_parent_move_pairs:42,duplicate_incidences:5,unclassified_parent_orbits:35,unique_known_open_S6_orbits:2,unique_known_open_S6_edges:7,
    affected_S5_rows:[
      {s5_hex:s5A,remaining_s6_orbits:4,cost_before:297,cost_after_local:291,shared_s6:s6A,covered_moves:movesA,remaining_edges:70},
      {s5_hex:claimB.s5_hex,remaining_s6_orbits:77,cost_before:6296,cost_after_local:6290,shared_s6:s6B.toString(16).padStart(32,"0"),added_bit:addedB,covered_moves:movesB,remaining_edges:70},
      {s5_hex:s5C,remaining_s6_orbits:41,cost_before:3058,cost_after_local:3057,s6_child:s6C,covered_moves:[64],remaining_edges:80}
    ],
    per_S5_cost_reduction_sum:13,unique_S6_edge_reduction:7,S6_closed:0,global_frontier_recomputed:false
  },
  frontier_head_before_fold:"1188/6659/525437/4929/389160",
  interpretation:"Six WIN7 certificates prove six individual seven-stone roots only. The 76-move S6 parent still has 70 uncovered edges; no S6 orbit is closed by the known lifts. Global frontier is not updated until the six receipts are folded and all marginals recomputed. 11x11 remains UNKNOWN."
};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
