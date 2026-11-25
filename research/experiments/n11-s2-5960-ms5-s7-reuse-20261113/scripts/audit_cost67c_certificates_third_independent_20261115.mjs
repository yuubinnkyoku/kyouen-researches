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

const manifest=JSON.parse(pinned(P+"class2-lane-cost67c-win7-certificates-20261115.json","8b3082c0da4d251e9ea3b4a30e7cab6f804b9711"));
const sweep=JSON.parse(pinned(P+"class2-lane-cost67c-sweep-audit-20261115.json","bc550429f32a3795a4288108f614cacbfcbefed9"));
const v15=pinned(P+"class2-lane-cost67c-v15-crosscheck-20261115.jsonl","790e2008b15af86d8ad1628c893c14291a233e0c").toString("utf8").trim().split(/\r?\n/).map(JSON.parse);
const topText=pinned(P+"class-frontier-top-candidates-s6-after-cost63g-receipts-20261115.csv","77c12f798e9aa3341d1aa1e4e3481e955ebd51f6").toString("utf8");
const rankText=pinned(P+"class-frontier-s5-ranking-after-cost63g-receipts-20261115.csv","15eb7f9684bb715bcfa2090dc989e92b4c9b4989").toString("utf8");
const claim=JSON.parse(pinned(P+"class2-lane-cost67c-inflight-20261115.json","728f929d999fba6d0bed8e037b573d528f99616e").toString("utf8"));

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
  check(spec.verdict==="WIN7"&&spec.fbt_drops===0&&spec.rows_sorted_unique===true,"certificate metadata");
  const parts=spec.storage.parts.map(p=>{const b=read(p.path);check(b.length===p.bytes&&gitsha(b)===p.git_blob_sha,"part bytes/blob");return b;});
  check(parts.length===2&&parts[0][parts[0].length-1]===10&&/^[0-9a-f]{32} \d+\n/.test(parts[1].toString("utf8")),"part split");
  const raw=Buffer.concat(parts);
  check(raw.length===spec.bytes&&sha(raw,"md5")===spec.md5&&sha(raw,"sha256")===spec.sha256&&gitsha(raw)===spec.whole_git_blob_sha,"whole certificate hashes");
  const lines=raw.toString("utf8").split(/\r?\n/);if(lines.at(-1)==="")lines.pop();
  check(lines[0]==="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"&&lines[1]==="root "+spec.root_hex,"header/root");
  const strategy=new Map();let prev="";
  for(const line of lines.slice(2)){const m=line.match(/^([0-9a-f]{32}) (\d+)$/);check(m&&m[1]>prev,"strategy row order");prev=m[1];strategy.set(m[1],Number(m[2]));}
  check(strategy.size===spec.rows,"strategy rows");
  const root=BigInt("0x"+spec.root_hex),rp=points(root);check(rp.length===7&&root===(BigInt("0x"+spec.child_hex)|(1n<<BigInt(spec.bit))),"root identity");
  check(canon(root).hex===spec.d4_canonical_hex,"root D4");
  for(let i=0;i<7;i++)for(let j=i+1;j<7;j++)for(let k=j+1;k<7;k++){
    const tri=(1n<<BigInt(rp[i]))|(1n<<BigInt(rp[j]))|(1n<<BigInt(rp[k]));
    check((circleOrLineMask(rp[i],rp[j],rp[k])&(root&~tri))===0n,"unsafe root");
  }
  const rm=bits(legalMask(rp));check(rm.length===53&&rm.length===spec.root_check.loser_mobility&&rm.length===spec.sub_roots_total,"root mobility");
  check(rm.length===spec.loser_first_moves.length&&rm.every((x,i)=>x===spec.loser_first_moves[i]),"all root first moves");
  check(sweep.win7_d10_bits.includes(spec.bit)&&(sweep.root_orbit_check.orbit_map[spec.d4_canonical_hex]||[]).includes(spec.bit),"sweep anchor");
  check(sweep.root_orbit_check.root_mobility_bareiss[String(spec.bit)]===rm.length,"Bareiss mobility");
  const v=v15.find(x=>x.bit===spec.bit);check(v&&v.loss===true&&v.capped===false&&v.nodes===spec.v15_anchor_crosscheck.nodes,"v15 anchor");
  const stack=rm.map(m=>[root|(1n<<BigInt(m)),0]),seen=new Set(),consumed=new Set();
  let visited=0,winner=0,loser=0,edges=0,term=0,tmin=99,tmax=0;
  while(stack.length){
    const [board,depth]=stack.pop(),hex=board.toString(16).padStart(32,"0");if(seen.has(hex))continue;seen.add(hex);visited++;
    const opts=legalMask(points(board)),moves=bits(opts),ps=points(board);
    if(!moves.length){check(depth%2===1&&!strategy.has(hex),"terminal parity/row");term++;tmin=Math.min(tmin,ps.length);tmax=Math.max(tmax,ps.length);}
    else if(depth%2===0){winner++;const mv=strategy.get(hex);check(mv!==undefined&&((opts>>BigInt(mv))&1n)===1n,"WIN strategy");consumed.add(hex);stack.push([board|(1n<<BigInt(mv)),depth+1]);}
    else{loser++;check(!strategy.has(hex),"LOSS strategy row");edges+=moves.length;for(const mv of moves)stack.push([board|(1n<<BigInt(mv)),depth+1]);}
  }
  let missing=0,extra=0;for(const h of strategy.keys())if(!consumed.has(h))missing++;for(const h of consumed)if(!strategy.has(h))extra++;
  check(!missing&&!extra&&tmin===13&&tmax===17,"strategy union/terminal range");
  const parents=rp.map(p=>canon(root&~(1n<<BigInt(p))).hex).sort();
  check(parents.length===7&&new Set(parents).size===7&&JSON.stringify(parents)===JSON.stringify([...spec.d4_parent_orbits].sort()),"parent lifts");
  return {bit:spec.bit,root_hex:spec.root_hex,d4_canonical_hex:spec.d4_canonical_hex,rows:strategy.size,root_mobility:rm.length,unique_dag_states:visited,winner_states:winner,loser_states:loser,loser_reply_edges:edges,terminal_states:term,terminal_range:[tmin,tmax],missing,extra,parent_orbits:parents};
}
const replay=Object.values(manifest.certificates).map(verify).sort((a,b)=>a.bit-b.bit);
check(replay.length===2&&new Set(replay.map(x=>x.d4_canonical_hex)).size===2,"two distinct roots");
const totals={certificates:2,rows:replay.reduce((s,x)=>s+x.rows,0),unique_dag_states:replay.reduce((s,x)=>s+x.unique_dag_states,0),winner_states:replay.reduce((s,x)=>s+x.winner_states,0),loser_states:replay.reduce((s,x)=>s+x.loser_states,0),loser_reply_edges:replay.reduce((s,x)=>s+x.loser_reply_edges,0),terminal_states:replay.reduce((s,x)=>s+x.terminal_states,0),sub_roots:replay.reduce((s,x)=>s+x.root_mobility,0)};
check(totals.rows===manifest.totals.rows&&totals.sub_roots===manifest.totals.sub_roots,"manifest totals");
const pins=["6b30ad1b224ead35ffc999e1358e2451446adeeb","8aff65fa2942e7be2ee1adf08ffea6a21a4a02c3","203b0fbd071bfe5f4da8a6cd34fcf3a65670df23","1ec608cc12842bd4472a3039fcc0514494e1960c","e2aad9cef9f9a4af3bc659043631558408b6672b","acc1a8b3869a9917be7dd1b55574c756b59b0351"];
const s6=new Map();for(let i=0;i<pins.length;i++){const tx=pinned("research/experiments/n11-s2-5960-milestone5-20261112/output/ms5_s6_manifest_part"+(i+1)+".csv",pins[i]).toString("utf8");for(const line of tx.trim().split(/\r?\n/)){if(!line||line.startsWith("hex,"))continue;const [h,c,k]=line.split(",");check(!s6.has(h),"duplicate S6");s6.set(h,{cost:+c,classes:k});}}
check(s6.size===7867,"S6 manifest size");
const pmap=new Map();for(const c of replay)for(const h of c.parent_orbits){if(!pmap.has(h))pmap.set(h,[]);pmap.get(h).push(c.bit);}
check(pmap.size===13,"parent orbit count");
const parents=[...pmap.entries()].sort((a,b)=>a[0].localeCompare(b[0])).map(([hex,bits])=>({hex,bits,worklist:s6.get(hex)||null}));
const inWork=parents.filter(x=>x.worklist),outWork=parents.filter(x=>!x.worklist);check(inWork.length===7&&outWork.length===6,"worklist hits");
const rank=new Map();for(const line of rankText.split(/\r?\n/)){const m=line.match(/^([0-9a-f]{32}),(\d+),(\d+),(\d+)$/);if(m)rank.set(m[1],{classes:+m[2],remaining_s6_orbits:+m[3],remaining_s7_edge_cost:+m[4]});}
const top=[];for(const line of topText.split(/\r?\n/)){const m=line.match(/^([0-9a-f]{32}),([0-9a-f]{32}),(\d+),/);if(m)top.push({s5_hex:m[1],s6_hex:m[2],cost:+m[3]});}
const childHex=manifest.child_hex,child=BigInt("0x"+childHex);check(canon(child).hex===childHex&&s6.has(childHex)&&s6.get(childHex).cost===67&&s6.get(childHex).classes==="6","child manifest");
const cm=bits(legalMask(points(child)));check(cm.includes(64)&&cm.includes(96),"child legal moves");
const open=points(child).map(p=>canon(child&~(1n<<BigInt(p))).hex).filter(h=>rank.has(h)).sort();
check(open.length===2&&open.includes(manifest.lift_parents.class2_parent1.hex)&&open.includes(manifest.lift_parents.class4_s5_parent.hex),"open S5 parents");
const topChild=top.filter(x=>x.s6_hex===childHex);check(topChild.length===1&&topChild[0].s5_hex===manifest.lift_parents.class2_parent1.hex&&topChild[0].cost===67,"top child row");
check(!top.some(x=>x.s6_hex===childHex&&x.s5_hex===manifest.lift_parents.class4_s5_parent.hex),"class4 not in top subset");
check(claim.s6_child===childHex&&claim.chain_head_at_claim.startsWith("1216/6631/523382/4901/387105")&&claim.demand.c2===1&&claim.demand.c4===1,"claim snapshot");
check(claim.demand_verification.includes("remaining row of both open parents"),"claim remaining incidence");
for(const r of claim.open_parents_at_head_1216){const a=rank.get(r.s5_hex);check(a&&a.classes===r.classes_bitmask&&a.remaining_s6_orbits===r.remaining_s6_orbits&&a.remaining_s7_edge_cost===r.remaining_s7_edge_cost,"claim rank row");}
const wins=replay.filter(x=>x.root_hex===(child|(1n<<BigInt(x.bit))).toString(16).padStart(32,"0")).map(x=>x.bit).sort((a,b)=>a-b);check(wins.join(",")==="64,96","two child winning moves");
const result={schema:"n11-class2-cost67c-third-independent-certificate-audit-20261115-v1",date:"2026-11-15",status:"PASS",method:"独立なBigInt有理中心分子＋共線分岐。浮動小数点、探索器、既存証明書検査器を使わず、全AND/OR戦略木を再走査。",
baseline:{main_at_audit_start:"2f05130ff7deb5535ea76366ded18523346e097f",frontier_head:"1216/6631/523382/4901/387105"},
certificates:replay,totals,
parent_lift:{parent_incidences:14,unique_s6_parent_orbits:13,shared_parent_orbits:[...pmap.entries()].filter(([,b])=>b.length>1).map(([hex,bits])=>({hex,bits})),s6_manifest_rows:7867,worklist_membership_hits:7,worklist_parents:inWork,not_in_worklist:outWork.map(x=>x.hex)},
child_s6:{hex:childHex,proven_win:true,winning_moves_to_distinct_second_to_move_loss_roots:wins,open_s5_parents:open.map(h=>({s5_hex:h,...rank.get(h)})),top_candidate_rows:topChild,class2_remaining_row_directly_listed:true,class4_parent_is_open_but_child_row_not_in_top_candidate_subset:true,claim_reports_child_remaining_in_both_open_parents:true},
frontier:{head_before_fold:"1216/6631/523382/4901/387105",fold_pending:true,official_head_after_audit:"1216/6631/523382/4901/387105",official_solved_s6_in_manifest_change:0,remaining_s5_orbits:175,note:"receipt fold未実施。子S6のWINは証明されたが全親liftと未解決S6集合の交差は未確定のため公式frontierは更新しない。"},
interpretation_guard:"各証明書は個別7石rootのWINを深さ10以内で証明する。二石root {49,60}/{59,60}、S2 {59,60}、class2、class4、標準11×11空盤の勝敗はUNKNOWN."};
fs.writeFileSync(path.join(OUT,"cost67c-third-independent-certificate-audit-20261115.json"),JSON.stringify(result,null,2)+"\n");
console.log("COST67C_THIRD_INDEPENDENT_AUDIT_PASS certs=2 rows="+totals.rows+" parentOrbits=13 worklist=7 childMoves=64,96 fold=PENDING");
