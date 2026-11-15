#!/usr/bin/env node
// Third independent replay of the six currently published cost-63g WIN7 certificates.
// Uses exact integer rational-circle and collinear-line tests; imports no search engine,
// verdict cache, BigInt verifier, or Bareiss verifier.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../..");
const EXP = resolve(ROOT, "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113");
const CHILD_HEX = "00000000080000801202000000200000";
const SPECS = [
  {
    "bit": 64,
    "root": "00000000080000811202000000200000",
    "rows": 14896,
    "bytes": 537782,
    "blob": "cdc18ca665d9fe4a06a64a474df4e2eca1548375",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit64-root-00000000080000811202000000200000.cert",
    "mobility": 40,
    "visited": 35677,
    "winner": 23038,
    "loser": 7107,
    "edges": 32571,
    "terminals": 5532,
    "d4": "00000000080000811202000000200000",
    "commit": "a20a2a202a42e65e9daa2d42b7ec55bcb04d0aec"
  },
  {
    "bit": 96,
    "root": "00000001080000801202000000200000",
    "rows": 18463,
    "bytes": 664778,
    "blob": "a1299f9e1817d26d1ed742dcd91513e2210b99c3",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit96-root-00000001080000801202000000200000.cert",
    "mobility": 42,
    "visited": 39263,
    "winner": 25385,
    "loser": 7850,
    "edges": 35044,
    "terminals": 6028,
    "d4": "00000000200080003800000001000200",
    "commit": "35ebe9e2e18386a5cb1b2c21d5cb730711db6492"
  },
  {
    "bit": 105,
    "root": "00000200080000801202000000200000",
    "rows": 21430,
    "bytes": 775472,
    "blob": "1cf08f2a488de0a6b0fa5a95aea1dc7679f709f9",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit105-root-00000200080000801202000000200000.cert",
    "mobility": 42,
    "visited": 47020,
    "winner": 30424,
    "loser": 9409,
    "edges": 42798,
    "terminals": 7187,
    "d4": "00000000200080003800200000000200",
    "commit": "b8af904eb14cc63bc54a7a1098d700c07641c8f4"
  },
  {
    "bit": 58,
    "root": "00000000080000801602000000200000",
    "rows": 24030,
    "bytes": 868008,
    "blob": "d2409f6535a964fbea438962f4b50f62d15d1713",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit58-root-00000000080000801602000000200000.cert",
    "mobility": 46,
    "visited": 53818,
    "winner": 34681,
    "loser": 10783,
    "edges": 48635,
    "terminals": 8354,
    "d4": "00000000080000801602000000200000",
    "commit": "c503796ec3d3ae8d1116d3f4618d8a85f9def60d"
  },
  {
    "bit": 62,
    "root": "00000000080000805202000000200000",
    "rows": 23905,
    "bytes": 863816,
    "blob": "14fcb303e63b909bee3cf8035690b8564edbc22a",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit62-root-00000000080000805202000000200000.cert",
    "mobility": 44,
    "visited": 53086,
    "winner": 34400,
    "loser": 10305,
    "edges": 47542,
    "terminals": 8381,
    "d4": "00000000080000805202000000200000",
    "commit": "06180652ff5158edba3c4a85b4fd27703e91c19f"
  },
  {
    "bit": 54,
    "root": "00000000080000801242000000200000",
    "rows": 27156,
    "bytes": 982624,
    "blob": "26d5ae74296e7f0af722890a663f711af1d4ef9d",
    "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-certificates/bit54-root-00000000080000801242000000200000.cert",
    "mobility": 47,
    "visited": 60500,
    "winner": 39135,
    "loser": 12004,
    "edges": 54856,
    "terminals": 9361,
    "d4": "00000000080000801242000000200000",
    "commit": "348f2ad78fa08545b3df470b8a9341007cc99d79"
  }
];
const SWEEP = JSON.parse(readFileSync(resolve(EXP, "output/class2-lane-cost63g-sweep-audit-20261115.json"), "utf8"));
const N = 121, FULL = (1n << 121n) - 1n;
const X = Array.from({ length:N }, (_,i) => i % 11);
const Y = Array.from({ length:N }, (_,i) => Math.floor(i / 11));
const Q = Array.from({ length:N }, (_,i) => X[i]*X[i] + Y[i]*Y[i]);
const tripleCache = new Map(), legalCache = new Map();

function forbiddenByTriple(a,b,c) {
  const key = a*14641 + b*121 + c;
  if (tripleCache.has(key)) return tripleCache.get(key);
  const ux=X[b]-X[a], uy=Y[b]-Y[a], vx=X[c]-X[a], vy=Y[c]-Y[a];
  const D=ux*vy-uy*vx;
  let mask=0n;
  if (D===0) {
    for (let d=0; d<N; d++) {
      if (d===a || d===b || d===c) continue;
      const dx=X[d]-X[a], dy=Y[d]-Y[a];
      if (ux*dy-uy*dx===0) mask |= 1n<<BigInt(d);
    }
  } else {
    const qb=Q[b]-Q[a], qc=Q[c]-Q[a];
    const cxNum=qb*vy-qc*uy, cyNum=ux*qc-vx*qb;
    for (let d=0; d<N; d++) {
      if (d===a || d===b || d===c) continue;
      const dx=X[d]-X[a], dy=Y[d]-Y[a];
      if (D*(Q[d]-Q[a])-cxNum*dx-cyNum*dy===0) mask |= 1n<<BigInt(d);
    }
  }
  tripleCache.set(key,mask);
  return mask;
}
function pointsOf(mask) {
  const out=[];
  for (let i=0;i<N;i++) if ((mask>>BigInt(i))&1n) out.push(i);
  return out;
}
function hexOf(mask) { return mask.toString(16).padStart(32,"0"); }
function legalMask(points) {
  const key=points.map(x=>x.toString(16).padStart(2,"0")).join("");
  if (legalCache.has(key)) return legalCache.get(key);
  let banned=0n;
  for (const p of points) banned |= 1n<<BigInt(p);
  for (let i=0;i<points.length;i++)
    for (let j=i+1;j<points.length;j++)
      for (let k=j+1;k<points.length;k++)
        banned |= forbiddenByTriple(points[i],points[j],points[k]);
  const result=FULL&~banned;
  legalCache.set(key,result);
  return result;
}
function bitsOf(mask) {
  const out=[];
  for (let i=0;i<N;i++) if ((mask>>BigInt(i))&1n) out.push(i);
  return out;
}
function canonicalD4(mask) {
  let best=null;
  for (let t=0;t<8;t++) {
    let v=0n;
    for (const p of pointsOf(mask)) {
      const x=X[p], y=Y[p]; let a,b;
      switch(t) {
        case 0:a=x;b=y;break;
        case 1:a=10-y;b=x;break;
        case 2:a=10-x;b=10-y;break;
        case 3:a=y;b=10-x;break;
        case 4:a=10-x;b=y;break;
        case 5:a=x;b=10-y;break;
        case 6:a=y;b=x;break;
        default:a=10-y;b=10-x;
      }
      v|=1n<<BigInt(b*11+a);
    }
    const h=hexOf(v);
    if (best===null || h<best) best=h;
  }
  return best;
}
function assertRootSafe(points) {
  for (let i=0;i<points.length;i++)
    for (let j=i+1;j<points.length;j++)
      for (let k=j+1;k<points.length;k++) {
        const bad=forbiddenByTriple(points[i],points[j],points[k]);
        for (let z=k+1;z<points.length;z++)
          if ((bad>>BigInt(points[z]))&1n) throw new Error("unsafe root");
      }
}
function verify(spec) {
  const file=readFileSync(resolve(ROOT,spec.path));
  const gitBlobSha=createHash("sha1")
    .update(Buffer.concat([Buffer.from("blob "+file.length+"\0"),file]))
    .digest("hex");
  if (file.length!==spec.bytes || gitBlobSha!==spec.blob) throw new Error("blob/size mismatch bit "+spec.bit);
  const lines=file.toString("utf8").split(/\r?\n/).filter(Boolean);
  if (lines[0]!=="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS") throw new Error("bad header bit "+spec.bit);
  if (lines[1]!=="root "+spec.root) throw new Error("bad root bit "+spec.bit);
  const strategy=new Map(); let previous="";
  for (const line of lines.slice(2)) {
    const m=line.match(/^([0-9a-f]{32})\s+(\d+)$/);
    if (!m || m[1]<=previous) throw new Error("bad/unsorted/duplicate row bit "+spec.bit);
    previous=m[1]; strategy.set(m[1],Number(m[2]));
  }
  if (strategy.size!==spec.rows) throw new Error("row count mismatch bit "+spec.bit);
  const root=BigInt("0x"+spec.root), child=BigInt("0x"+CHILD_HEX);
  if (root!==(child|(1n<<BigInt(spec.bit)))) throw new Error("root != child|bit "+spec.bit);
  const rootPoints=pointsOf(root);
  if (rootPoints.length!==7) throw new Error("root stone count bit "+spec.bit);
  assertRootSafe(rootPoints);
  const replies=bitsOf(legalMask(rootPoints));
  if (replies.length!==spec.mobility) throw new Error("root mobility mismatch bit "+spec.bit);
  const d4=canonicalD4(root);
  if (d4!==spec.d4) throw new Error("D4 root mismatch bit "+spec.bit);
  if (!(SWEEP.root_orbit_check.orbit_map[d4]||[]).includes(spec.bit)) throw new Error("sweep D4 map mismatch bit "+spec.bit);
  const consumed=new Set();
  let visited=0,winner=0,loser=0,edges=0,terminals=0,minTerm=999,maxTerm=0,maxPlies=0;
  for (const reply of replies) {
    const stack=[[root|(1n<<BigInt(reply)),0]], seen=new Set();
    while (stack.length) {
      const [board,depth]=stack.pop(), hex=hexOf(board);
      if (seen.has(hex)) continue;
      seen.add(hex); visited++;
      const pts=pointsOf(board), options=legalMask(pts);
      if (options===0n) {
        if (depth%2!==1 || strategy.has(hex)) throw new Error("bad terminal bit "+spec.bit);
        terminals++; minTerm=Math.min(minTerm,pts.length); maxTerm=Math.max(maxTerm,pts.length);
        maxPlies=Math.max(maxPlies,depth+1); continue;
      }
      if (depth%2===0) {
        winner++;
        const move=strategy.get(hex);
        if (move===undefined || ((options>>BigInt(move))&1n)===0n) throw new Error("missing/illegal winner move bit "+spec.bit);
        consumed.add(hex); stack.push([board|(1n<<BigInt(move)),depth+1]);
      } else {
        loser++;
        if (strategy.has(hex)) throw new Error("row on loser turn bit "+spec.bit);
        for (const move of bitsOf(options)) { edges++; stack.push([board|(1n<<BigInt(move)),depth+1]); }
      }
    }
  }
  const missing=[...strategy.keys()].filter(k=>!consumed.has(k));
  const extra=[...consumed].filter(k=>!strategy.has(k));
  if (missing.length || extra.length || consumed.size!==strategy.size) throw new Error("certificate union mismatch bit "+spec.bit);
  if (minTerm<13 || maxTerm>17 || maxPlies>10) throw new Error("terminal bounds bit "+spec.bit);
  const result={
    bit:spec.bit,root_hex:spec.root,d4_canonical_hex:d4,bytes:file.length,git_blob_sha:gitBlobSha,
    rows:strategy.size,root_mobility:replies.length,sub_roots:replies.length,
    visited_states_across_subroots:visited,winner_states:winner,loser_states:loser,
    loser_reply_edges:edges,terminal_count:terminals,terminal_range:[minTerm,maxTerm],
    max_plies_from_root:maxPlies,union_missing:missing.length,union_extra:extra.length
  };
  for (const [key,expected] of [
    ["visited_states_across_subroots",spec.visited],["winner_states",spec.winner],
    ["loser_states",spec.loser],["loser_reply_edges",spec.edges],["terminal_count",spec.terminals]
  ]) if (result[key]!==expected) throw new Error("count mismatch bit "+spec.bit+" "+key);
  return result;
}

if (SWEEP.candidates!==63 || SWEEP.win7_count!==14 || SWEEP.refuted_count!==49 || SWEEP.capped_count!==0 ||
    SWEEP.root_orbit_check.distinct_d4_orbits!==14) {
  throw new Error("cost63g sweep audit changed");
}
for (const spec of SPECS) {
  if (!SWEEP.win7_d10_bits.includes(spec.bit)) throw new Error("bit absent from WIN7 sweep set: " + spec.bit);
}
const results=SPECS.map(verify);
if (new Set(results.map(x=>x.d4_canonical_hex)).size!==results.length) throw new Error("D4 duplicate among six roots");
const parentOrbits=new Map();
for (const r of results) {
  const root=BigInt("0x"+r.root_hex);
  for (const removed of pointsOf(root)) {
    const parent=canonicalD4(root&~(1n<<BigInt(removed)));
    if (!parentOrbits.has(parent)) parentOrbits.set(parent,[]);
    parentOrbits.get(parent).push({bit:r.bit,removed});
  }
}
const childOrbit=canonicalD4(BigInt("0x"+CHILD_HEX));
const childIncidences=parentOrbits.get(childOrbit)||[];
const repeated=[...parentOrbits.entries()].filter(x=>x[1].length>1).map(x=>({parent:x[0],incidences:x[1]}));
if (parentOrbits.size!==37 || childIncidences.length!==6 || repeated.length!==1) throw new Error("parent-lift D4 multiplicity mismatch");

const result={
  schema:"n11-cost63g-six-published-rational-independent-audit-v1",
  date:"2026-11-15",
  scope:"The first six of fourteen published WIN7-D10 certificate roots (bits 64,96,105,58,62,54); the other eight were not yet published at audit time.",
  method:"Exact integer rational-circumcenter equation for noncollinear triples and exact cross-product line test for collinear triples; no floating point, no search engine, no verdict cache, no existing verifier imported.",
  sweep_audit:"class2-lane-cost63g-sweep-audit-20261115.json",
  certificates:results,
  aggregate:{
    certificates:results.length,
    rows:results.reduce((s,x)=>s+x.rows,0),
    sub_roots:results.reduce((s,x)=>s+x.sub_roots,0),
    visited_states_across_subroots:results.reduce((s,x)=>s+x.visited_states_across_subroots,0),
    winner_states:results.reduce((s,x)=>s+x.winner_states,0),
    loser_states:results.reduce((s,x)=>s+x.loser_states,0),
    loser_reply_edges:results.reduce((s,x)=>s+x.loser_reply_edges,0),
    terminal_count:results.reduce((s,x)=>s+x.terminal_count,0)
  },
  parent_lifts:{
    deletion_edges:42,
    unique_d4_parent_orbits:parentOrbits.size,
    shared_child_orbit:childOrbit,
    shared_child_incidences:childIncidences,
    repeated_parent_orbits:repeated
  },
  frontier_impact_at_audit:{
    contribution:0,
    current_chain_head:"1199/6648/524616/4918/388339",
    sweep_claim_base_head:"1195/6652/524884/4922/388607",
    receipt_fold_status:"pending",
    rebase_required_before_fold:true
  },
  interpretation_guard:"These six certificates prove only the six individual seven-stone roots WIN within ten plies. They do not close the six-stone child or either five-stone parent until receipts are folded on the current 1199 head. The other eight WIN7 certificates were not yet published at audit time. The standard 11x11 empty board, both two-stone roots, S2, class2 and class4 remain UNKNOWN."
};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
