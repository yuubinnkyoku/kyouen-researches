#!/usr/bin/env node
// Independent exact replay of class2 WIN7 certificates, frontier-branch union,
// and the completed raw cost-68c sweep. Run from the repository root.

import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

const OUT = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output";
const DEFAULT_FILES = [
  OUT + "/class2-lane-cost63e-certificates/bit28-root-00000000000000803202200010000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit90-root-00000000040000803202200000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit97-root-00000002000000803202200000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit42-root-00000000000000803202240000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit73-root-00000000000002803202200000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit100-root-00000010000000803202200000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit116-root-00100000000000803202200000000000.cert",
  OUT + "/class2-lane-cost63e-certificates/bit120-root-01000000000000803202200000000000.cert",
  OUT + "/class2-lane-cost65h-certificates/bit7-root-00000000000000803202000000001080.cert",
  OUT + "/class2-lane-cost65h-certificates/bit109-root-00002000000000803202000000001000.cert",
  OUT + "/class2-lane-cost65h-certificates/bit24-root-00000000000000803202000001001000.cert",
  OUT + "/class2-lane-cost65i-certificates/bit7-root-00000000000000803202000000080080.cert",
  OUT + "/class2-lane-cost65i-certificates/bit43-root-00000000000000803202080000080000.cert",
  OUT + "/class2-lane-cost65i-certificates/bit99-root-00000008000000803202000000080000.cert",
  OUT + "/class2-lane-cost67b-certificates/bit17-root-00000000000000803202000020020000.cert",
  OUT + "/class2-lane-cost67b-certificates/bit117-root-00200000000000803202000020000000.cert",
  OUT + "/class2-lane-cost67b-certificates/bit109-root-00002000000000803202000020000000.cert",
  OUT + "/class2-lane-cost65g-certificates/bit44-root-00000000000000803202100000000004.cert",
];

const EXPECTED_GIT_BLOB_SHA = {
  "bit28-root-00000000000000803202200010000000.cert": "02542389e3601f4146ee0cf629422b85c51381d1",
  "bit90-root-00000000040000803202200000000000.cert": "deae67d4507e6f22be732b5de488f063c278c373",
  "bit97-root-00000002000000803202200000000000.cert": "d86a213e1dd8af2fc4f0cefdf1a87a4da9b2534f",
  "bit42-root-00000000000000803202240000000000.cert": "51903c30bbc19242132719f9949c53e5eceec75f",
  "bit73-root-00000000000002803202200000000000.cert": "ac9cdb10bd237f4d8b3d6a43ebef9b2a7eae2bad",
  "bit100-root-00000010000000803202200000000000.cert": "e733c50cbe795734b54d7411c14a5eff687da689",
  "bit116-root-00100000000000803202200000000000.cert": "8e04c068fb21ea45cd85847dc26306d7e22818b0",
  "bit120-root-01000000000000803202200000000000.cert": "63f82e708ae2104de21a93806bdf5189658d83f4",
  "bit7-root-00000000000000803202000000001080.cert": "3a1865e2f1c48d850ef50ec21f39d448b2a31fe9",
  "bit109-root-00002000000000803202000000001000.cert": "9c5036c8e52613c480da152ec13c52df1acbe7c8",
  "bit24-root-00000000000000803202000001001000.cert": "ef38cb0fe14c268ca476a6edec83e6d454d2b0ec",
  "bit7-root-00000000000000803202000000080080.cert": "dc784750262b5f763cba9b42cc1f67b78ecd50c9",
  "bit43-root-00000000000000803202080000080000.cert": "af7215b24e1658b20fab7339cfc8a3e802f5616c",
  "bit99-root-00000008000000803202000000080000.cert": "ec8c4758c858bc56d6ffe532ec8406c83b33b4f7",
  "bit17-root-00000000000000803202000020020000.cert": "f087663046a6b9724d187aa4e6b07a85c7aa467a",
  "bit117-root-00200000000000803202000020000000.cert": "0c55d6b84ac9f4cebb54f6365fbe22912d695478",
  "bit109-root-00002000000000803202000020000000.cert": "3e1450167191cda48fd93c9394ccb2d326b9a2f5",
  "bit44-root-00000000000000803202100000000004.cert": "80bdf6e1d561f8a639cc76b238561470ca067df4",
};

const PUBLISHED_SHA256 = {
  "bit28-root-00000000000000803202200010000000.cert": "795bbf9019fbd78d7d2ad5e548e5eae4fa3658ccfcb4a4a50f3f1886d84390fd",
  "bit90-root-00000000040000803202200000000000.cert": "fc23d153d2d569f6f0b14b26568dc9ab297508094231fe72491b54ee846a6c1d",
  "bit97-root-00000002000000803202200000000000.cert": "b93eca0f90680e251460694eccdb522d88230507828cbe98acfe30518f435ca3",
  "bit42-root-00000000000000803202240000000000.cert": "90c7f7c721fa0eb99f27d2ff5c118e2bb5e6310199784d68d09c8be3c4cb3be3",
  "bit73-root-00000000000002803202200000000000.cert": "992166eb843281da0102f8410f431c3ff52a75f0f0cab215e9ae3006efa473fc",
  "bit100-root-00000010000000803202200000000000.cert": "d05b4b6b1cadfa5d6a29c904aa34ed88cd48168680b4d62d339f48bdfee3e327",
  "bit116-root-00100000000000803202200000000000.cert": "e99a4b55d7859039911ed91f9c669f74b51ab6d21baecf1daeec3f1edc4cb12b",
  "bit120-root-01000000000000803202200000000000.cert": "d12d26a3b68b22e5d3e7fa7bdd893cd58a385494ec74c131adc9042fd58751d8",
  "bit7-root-00000000000000803202000000001080.cert": "f3b21f78a95379a93e354ab92b6a84899b110024d577a2f56924e22063245be7",
  "bit109-root-00002000000000803202000000001000.cert": "67b8f7c4f58ffe8ae58bf6fa4e456d1397f67933a1e2650487b49b2144a6cbf2",
  "bit24-root-00000000000000803202000001001000.cert": "2a311775de0ebffcacb9c723c58c08d8c9a9cf722c02541848a613bf08c37eff",
  "bit7-root-00000000000000803202000000080080.cert": "c011be1a9a71288de3e530e7828d6ff359fd47b0593a856ae3f24857de158e4c",
  "bit43-root-00000000000000803202080000080000.cert": "aa8eb94428dac984faa0ca57d5fdda57c44d69ffdd0e6dce2778fbb16896ec51",
  "bit99-root-00000008000000803202000000080000.cert": "b6600fd4c444a4557bc76b3f135f97b61c918e5908fd0ff8a50d80c5cf5258aa",
  "bit17-root-00000000000000803202000020020000.cert": "563e9c6557e12df35b4bbc2bf0c2dd2f98729a373f81b0ab9f9612522ceda70a",
  "bit117-root-00200000000000803202000020000000.cert": "2c5b60a92c4ec09e7b97e34bff36b076c4b9e56bf7b7b23459d0e14fa9855b56",
  "bit109-root-00002000000000803202000020000000.cert": "7ccc6eee5569db4d29ac4afd82da83103b9d33071b855731a3447b22a37088c0",
};

const N = 121;
const FULL = (1n << 121n) - 1n;
const XY = Array.from({ length: N }, (_, p) => [BigInt(p % 11), BigInt(Math.floor(p / 11))]);
const tripleCache = new Map();

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function det3(a, b, c, d, e, f, g, h, i) {
  return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
}

// Exact forbidden-point set for a triple:
// - collinear triple: line membership by an integer cross product;
// - otherwise: solve the circle through the triple with 3x3 Cramer determinants.
// No floating point is used.
function forbiddenMask(a, b, c) {
  if (a > b) [a, b] = [b, a];
  if (b > c) [b, c] = [c, b];
  if (a > b) [a, b] = [b, a];
  const key = a * 14641 + b * 121 + c;
  const cached = tripleCache.get(key);
  if (cached !== undefined) return cached;

  const [x1, y1] = XY[a], [x2, y2] = XY[b], [x3, y3] = XY[c];
  const s1 = x1*x1 + y1*y1, s2 = x2*x2 + y2*y2, s3 = x3*x3 + y3*y3;
  const D = det3(x1,y1,1n, x2,y2,1n, x3,y3,1n);
  let mask = 0n;

  if (D === 0n) {
    const dx = x2-x1, dy = y2-y1;
    for (let p=0; p<N; p++) {
      if (p===a || p===b || p===c) continue;
      const [x,y] = XY[p];
      if (dx*(y-y1)-dy*(x-x1)===0n) mask |= 1n << BigInt(p);
    }
  } else {
    const A = det3(-s1,y1,1n, -s2,y2,1n, -s3,y3,1n);
    const B = det3(x1,-s1,1n, x2,-s2,1n, x3,-s3,1n);
    const C = det3(x1,y1,-s1, x2,y2,-s2, x3,y3,-s3);
    for (let p=0; p<N; p++) {
      if (p===a || p===b || p===c) continue;
      const [x,y] = XY[p], s=x*x+y*y;
      if (D*s+A*x+B*y+C===0n) mask |= 1n << BigInt(p);
    }
  }
  tripleCache.set(key,mask);
  return mask;
}

function pointsOf(mask) {
  const out=[];
  for(let p=0;p<N;p++) if((mask>>BigInt(p))&1n) out.push(p);
  return out;
}
function popcount(mask) {
  let n=0;
  while(mask){mask&=mask-1n;n++;}
  return n;
}
function occupiedMask(points) {
  let m=0n;
  for(const p of points)m|=1n<<BigInt(p);
  return m;
}
function isSafe(points) {
  const occupied=occupiedMask(points);
  for(let i=0;i<points.length;i++)for(let j=i+1;j<points.length;j++)for(let k=j+1;k<points.length;k++)
    assert((forbiddenMask(points[i],points[j],points[k])&occupied)===0n,"unsafe position");
  return true;
}
function legalMask(points) {
  let banned=occupiedMask(points);
  for(let i=0;i<points.length;i++)for(let j=i+1;j<points.length;j++)for(let k=j+1;k<points.length;k++)
    banned|=forbiddenMask(points[i],points[j],points[k]);
  return FULL&~banned;
}
function gitBlobSha(raw) {
  const header=Buffer.from("blob "+raw.length+"\0","utf8");
  return createHash("sha1").update(Buffer.concat([header,raw])).digest("hex");
}
const D4 = [
  (x,y)=>[x,y],(x,y)=>[10-y,x],(x,y)=>[10-x,10-y],(x,y)=>[y,10-x],
  (x,y)=>[10-x,y],(x,y)=>[10-y,10-x],(x,y)=>[x,10-y],(x,y)=>[y,x],
];
function canonicalD4(mask) {
  let best=null;
  for(const fn of D4){
    let image=0n;
    for(let p=0;p<N;p++)if((mask>>BigInt(p))&1n){
      const [x,y]=fn(p%11,Math.floor(p/11));
      image|=1n<<BigInt(y*11+x);
    }
    const hex=image.toString(16).padStart(32,"0");
    if(best===null||hex<best)best=hex;
  }
  return best;
}
function verifySubroot(strategy,subroot) {
  const seen=new Set(),consumed=[];
  let terminals=0,opponentEdges=0,tmin=99,tmax=0;
  const stack=[[subroot,0]];
  while(stack.length){
    const [board,depth]=stack.pop();
    const hex=board.toString(16).padStart(32,"0");
    if(seen.has(hex))continue;
    seen.add(hex);
    const points=pointsOf(board),options=legalMask(points);
    if(options===0n){
      assert(depth%2===1,"winner-to-move terminal "+hex);
      assert(!strategy.has(hex),"strategy on terminal "+hex);
      terminals++;tmin=Math.min(tmin,points.length);tmax=Math.max(tmax,points.length);
    }else if(depth%2===0){
      const move=strategy.get(hex);
      assert(move!==undefined,"missing winner move "+hex);
      assert((options&(1n<<BigInt(move)))!==0n,"illegal winner move "+hex);
      consumed.push(hex);
      stack.push([board|(1n<<BigInt(move)),depth+1]);
    }else{
      assert(!strategy.has(hex),"strategy on opponent turn "+hex);
      let rest=options;
      while(rest){const bit=rest&-rest;rest-=bit;opponentEdges++;stack.push([board|bit,depth+1]);}
    }
  }
  return {seen:seen.size,consumed,terminals,opponentEdges,terminalRange:[tmin,tmax]};
}
function verifyCertificate(file) {
  const raw=fs.readFileSync(file),content=raw.toString("utf8"),name=path.basename(file);
  const blob=gitBlobSha(raw);
  assert(blob===EXPECTED_GIT_BLOB_SHA[name],"Git blob SHA mismatch: "+name);
  const publishedSha=PUBLISHED_SHA256[name]??null;
  if(publishedSha!==null)
    assert(createHash("sha256").update(raw).digest("hex")===publishedSha,"SHA-256 mismatch: "+name);

  const lines=content.split(/\r?\n/).filter(x=>x.trim().length>0);
  assert(lines[0]==="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS","header: "+name);
  assert(lines[1]?.startsWith("root "),"root line: "+name);
  const rootHex=lines[1].slice(5);
  const match=name.match(/-root-([0-9a-f]{32})\.cert$/);
  assert(match&&match[1]===rootHex,"filename/root mismatch: "+name);
  const root=BigInt("0x"+rootHex);
  assert(root<=FULL,"root outside board");
  let previous="";
  const strategy=new Map();
  for(const line of lines.slice(2)){
    const parts=line.trim().split(/\s+/);
    assert(parts.length===2,"malformed row: "+name);
    const [hex,moveText]=parts;
    assert(/^[0-9a-f]{32}$/.test(hex)&&hex>previous,"bad/sorted/duplicate row: "+name);
    previous=hex;
    assert(/^\d+$/.test(moveText),"bad move: "+name);
    const board=BigInt("0x"+hex),stones=popcount(board),move=Number(moveText);
    assert(board<=FULL&&stones>=8&&stones%2===0,"bad winner-state key: "+hex);
    assert(Number.isInteger(move)&&move>=0&&move<N,"move range: "+name);
    strategy.set(hex,move);
  }

  const rootPoints=pointsOf(root);
  assert(rootPoints.length===7,"root stone count: "+name);
  isSafe(rootPoints);
  const rootOptions=legalMask(rootPoints),mobility=popcount(rootOptions);
  let subroots=0,seenSum=0,terminalVisits=0,opponentEdges=0,tmin=99,tmax=0;
  const consumed=new Set();
  for(let rest=rootOptions;rest;){
    const bit=rest&-rest;rest-=bit;
    const stats=verifySubroot(strategy,root|bit);
    subroots++;seenSum+=stats.seen;terminalVisits+=stats.terminals;opponentEdges+=stats.opponentEdges;
    tmin=Math.min(tmin,stats.terminalRange[0]);tmax=Math.max(tmax,stats.terminalRange[1]);
    for(const key of stats.consumed)consumed.add(key);
  }
  assert(subroots===mobility,"root reply/subroot count: "+name);
  assert(consumed.size===strategy.size,"strategy row union size: "+name);
  for(const key of strategy.keys())assert(consumed.has(key),"unconsumed strategy row: "+key);
  assert(tmin>=13&&tmax<=17,"terminal range: "+name);

  return {
    file,git_blob_sha:blob,published_sha256:publishedSha,bytes:raw.length,root_hex:rootHex,
    d4_canonical_root:canonicalD4(root),strategy_rows:strategy.size,root_mobility:mobility,
    subroots_verified:subroots,subroot_seen_states_sum:seenSum,terminal_visits:terminalVisits,
    opponent_reply_edges:opponentEdges,terminal_range:[tmin,tmax],consumed_rows:consumed.size,
    missing_rows:0,extra_rows:0,pass:true,
  };
}

function parseS5Children(csvPath,s5Hex) {
  const map=new Map();
  for(const line of fs.readFileSync(csvPath,"utf8").split(/\r?\n/)){
    if(!line.startsWith(s5Hex+","))continue;
    const parts=line.split(",");
    if(parts.length<3)continue;
    map.set(parts[1],Number(parts[2]));
  }
  return map;
}
function sumMap(map) { return [...map.values()].reduce((a,b)=>a+b,0); }

const files=process.argv.slice(2).length?process.argv.slice(2):DEFAULT_FILES;
const certs=files.map(verifyCertificate);
const canonicalRoots=new Set(certs.map(c=>c.d4_canonical_root));
assert(canonicalRoots.size===certs.length,"D4-equivalent certificate roots found");

const cost63e=JSON.parse(fs.readFileSync(OUT+"/class-frontier-cost63e-warm-recompute-20261114.json","utf8"));
const cost67b=JSON.parse(fs.readFileSync(OUT+"/class-frontier-cost67b-recompute-20261114.json","utf8"));
const baseA=cost63e.controls.after_cost65h_65i,baseB=cost67b.controls.after_cost65h_65i;
for(const key of ["solved_in_manifest","unique_remaining","sum_cost","open_s6","open_cost"])
  assert(baseA[key]===baseB[key],"frontier baselines differ: "+key);
assert(baseA.solved_in_manifest===991&&baseA.unique_remaining===6856&&baseA.sum_cost===540177&&baseA.open_s6===5126&&baseA.open_cost===403900,"unexpected common frontier baseline");

const keysA=[...new Set(Object.values(cost63e.cost63e_warm_addition).flatMap(v=>v.marginal_manifest_hexes))];
const keysB=[...new Set(Object.values(cost67b.cost67b_addition).flatMap(v=>v.marginal_manifest_hexes))];
assert(keysA.length===6&&keysB.length===2,"unexpected marginal-key counts");
assert(keysA.every(k=>!keysB.includes(k)),"parallel frontier marginal sets overlap");
const deltaA={
  solved:cost63e.frontier_after_cost63e_warm.solved_s6_in_manifest-baseA.solved_in_manifest,
  cost:baseA.sum_cost-cost63e.frontier_after_cost63e_warm.sum_remaining_cost,
  open:baseA.open_s6-cost63e.frontier_after_cost63e_warm.s6_needed_by_open_classes,
  openCost:baseA.open_cost-cost63e.frontier_after_cost63e_warm.cost_needed_by_open_classes,
};
const deltaB={
  solved:cost67b.frontier_after_cost67b.solved_s6_in_manifest-baseB.solved_in_manifest,
  cost:baseB.sum_cost-cost67b.frontier_after_cost67b.sum_remaining_cost,
  open:baseB.open_s6-cost67b.frontier_after_cost67b.s6_needed_by_open_classes,
  openCost:baseB.open_cost-cost67b.frontier_after_cost67b.cost_needed_by_open_classes,
};
assert(deltaA.solved===6&&deltaA.cost===432&&deltaA.open===6&&deltaA.openCost===432,"cost63e delta mismatch");
assert(deltaB.solved===2&&deltaB.cost===142&&deltaB.open===2&&deltaB.openCost===142,"cost67b delta mismatch");
const mergedFrontier={
  solved_s6_in_manifest:baseA.solved_in_manifest+keysA.length+keysB.length,
  unique_remaining_s6:baseA.unique_remaining-keysA.length-keysB.length,
  sum_remaining_cost:baseA.sum_cost-deltaA.cost-deltaB.cost,
  s6_needed_by_open_classes:baseA.open_s6-deltaA.open-deltaB.open,
  cost_needed_by_open_classes:baseA.open_cost-deltaA.openCost-deltaB.openCost,
  disjoint_new_manifest_keys:[...keysA,...keysB],
};
assert(mergedFrontier.solved_s6_in_manifest===999&&mergedFrontier.unique_remaining_s6===6848&&mergedFrontier.sum_remaining_cost===539603&&mergedFrontier.s6_needed_by_open_classes===5118&&mergedFrontier.cost_needed_by_open_classes===403326,"merged frontier mismatch");

// The second class-2 S5 has the same 15-child baseline in both branches.
const s5="00000000000000803202000000000000";
const p65="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost65h-65i-20261114.csv";
const p63="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost63e-warm-20261114.csv";
const p67="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost67b-20261114.csv";
const childrenBase=parseS5Children(p65,s5),children63=parseS5Children(p63,s5),children67=parseS5Children(p67,s5);
assert(childrenBase.size===15&&sumMap(childrenBase)===1072,"baseline S5 child set mismatch");
assert(children63.size===14&&sumMap(children63)===1001,"cost63e-warm S5 child set mismatch");
assert(children67.size===14&&sumMap(children67)===1005,"cost67b S5 child set mismatch");
const removed63=[...childrenBase.keys()].filter(k=>!children63.has(k));
const removed67=[...childrenBase.keys()].filter(k=>!children67.has(k));
assert(removed63.length===1&&removed67.length===1&&removed63[0]!==removed67[0],"S5 branch removals overlap");
const mergedLocalChildren=[...childrenBase].filter(([k])=>!removed63.includes(k)&&!removed67.includes(k));
assert(mergedLocalChildren.length===13&&mergedLocalChildren.reduce((a,[,v])=>a+v,0)===934,"merged local S5 count/cost mismatch");
assert(removed67[0]==="00000000000000803202000020000000"&&childrenBase.get(removed67[0])===67,"cost67b parent removal mismatch");

// Three cost-67b certificates share one S6 parent; bit 109 also lifts a second manifest parent.
const parentHex="00000000000000803202000020000000",parent=BigInt("0x"+parentHex),parentPoints=pointsOf(parent);
isSafe(parentPoints);
const parentLegal=legalMask(parentPoints);
for(const move of [17,109,117])assert((parentLegal&(1n<<BigInt(move)))!==0n,"illegal cost67b parent move");
for(const [hex,move] of [
  ["00000000000000803202000020020000",17],
  ["00002000000000803202000020000000",109],
  ["00200000000000803202000020000000",117],
])assert(BigInt("0x"+hex)===(parent|(1n<<BigInt(move))),"cost67b root/parent mismatch");
const bit109Root=BigInt("0x00002000000000803202000020000000");
const secondParent=canonicalD4(bit109Root^(1n<<61n));
assert(secondParent==="00000000080000809002000000000800","cost67b second parent lift mismatch");
const frontier63Csv=fs.readFileSync(p63,"utf8");
assert(frontier63Csv.includes(s5+","+parentHex+",67,"),"cost67b parent missing from post-cost63e-warm frontier");
const parent65g="00000000000000803202000000000004";
assert(!childrenBase.has(parent65g),"cost65g bit44 parent unexpectedly remains in the S5 baseline");

// Independently parse the complete 68-candidate cost-68c raw sweep.
const claimPath=OUT+"/class2-lane-cost68c-inflight-20261114.json";
const claim=JSON.parse(fs.readFileSync(claimPath,"utf8"));
assert(claim.candidate_bits.length===68,"cost68c claim size mismatch");
const raw=[];
for(let batch=1;batch<=9;batch++){
  const p=OUT+"/class2-lane-cost68c-raw-batch"+batch+"-20261114.jsonl";
  for(const line of fs.readFileSync(p,"utf8").split(/\r?\n/))if(line.trim())raw.push(JSON.parse(line));
}
const candidateRows=raw.filter(r=>Number.isInteger(r.bit));
const pilotRows=raw.filter(r=>!Number.isInteger(r.bit));
const bits=candidateRows.map(r=>r.bit);
assert(candidateRows.length===68&&new Set(bits).size===68,"cost68c raw candidate count/uniqueness mismatch");
assert(claim.candidate_bits.every(b=>bits.includes(b))&&bits.every(b=>claim.candidate_bits.includes(b)),"cost68c candidate set differs from claim");
assert(pilotRows.length===9&&pilotRows.every(r=>r.nodes===3402&&r.loss===false&&r.capped===false),"cost68c pilot control mismatch");
const win7Rows=candidateRows.filter(r=>r.loss===true);
const refutedRows=candidateRows.filter(r=>r.loss===false);
const cappedRows=candidateRows.filter(r=>r.capped===true);
const totalNodes=candidateRows.reduce((a,r)=>a+r.nodes,0);
assert(win7Rows.length===5&&refutedRows.length===63&&cappedRows.length===0&&totalNodes===104482623,"cost68c sweep totals mismatch");
assert(win7Rows.map(r=>r.bit).sort((a,b)=>a-b).join(",")==="11,21,24,53,118","cost68c WIN7-D10 bits mismatch");

const totals=certs.reduce((a,r)=>{
  a.certificates++;a.strategy_rows+=r.strategy_rows;a.subroots_verified+=r.subroots_verified;
  a.subroot_seen_states_sum+=r.subroot_seen_states_sum;a.terminal_visits+=r.terminal_visits;
  a.opponent_reply_edges+=r.opponent_reply_edges;return a;
},{certificates:0,strategy_rows:0,subroots_verified:0,subroot_seen_states_sum:0,terminal_visits:0,opponent_reply_edges:0});

process.stdout.write(JSON.stringify({
  schema:"n11-class2-win7-circle-bigint-independent-audit-v2",
  method:"Exact BigInt 3x3 Cramer circle equation; collinear triples use exact line cross-products; all opponent replies expanded; no solver/cache/verifier imports.",
  totals,
  unique_d4_root_classes:canonicalRoots.size,
  certificates:certs,
  merged_frontier:mergedFrontier,
  local_second_class2_s5:{
    s5_hex:s5,baseline:{remaining_s6:childrenBase.size,cost:sumMap(childrenBase)},
    after_cost63e_warm:{remaining_s6:children63.size,cost:sumMap(children63),removed_s6:removed63},
    after_cost67b:{remaining_s6:children67.size,cost:sumMap(children67),removed_s6:removed67},
    after_union:{remaining_s6:mergedLocalChildren.length,cost:mergedLocalChildren.reduce((a,[,v])=>a+v,0)},
  },
  cost67b_parent_lifts:{
    shared_s6_parent:parentHex,legal_moves:[17,109,117],
    second_manifest_parent:secondParent,unique_s6_manifest_orbits_closed:2,
  },
  cost65g_bit44:{
    root:"00000000000000803202100000000004",
    parent_s6:parent65g,
    already_absent_from_remaining_second_class2_children:true,
    new_frontier_closure_counted:0,
  },
  cost68c_raw_sweep:{
    claim_status:claim.status,
    candidates:68,unique_candidates:bits.length,claim_candidate_set_match:true,
    win7_d10_candidates:win7Rows.length,win7_bits:win7Rows.map(r=>r.bit).sort((a,b)=>a-b),
    refuted_d10_candidates:refutedRows.length,capped:cappedRows.length,
    total_nodes:totalNodes,pilot_controls:pilotRows.length,pilot_nodes:3402,
    summary_file_present:fs.existsSync(OUT+"/class2-lane-cost68c-sweep-20261114.json"),
    note:"All 68 raw rows are present and exact, but the claim JSON still says in_flight and the finalized sweep summary is absent. The five loss=true rows are WIN7-D10 candidates, not certificates.",
  },
  interpretation_guard:"WIN7 certificates prove only their individual seven-stone roots. REFUTED-D10 means no WIN7-D10 receipt, not a LOSS proof. S2 {59,60}, two-stone root {49,60}, standard 11x11 empty root, class2 and class4 remain UNKNOWN.",
},null,2)+"\n");
