#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const ROOT=process.cwd(),SCRIPT_FILE=fileURLToPath(import.meta.url);
const SCRIPT_PATH=path.relative(ROOT,SCRIPT_FILE).replaceAll("\\","/");
const MP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json";
const RP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json";
const KP="research/knowledge/items/K0001-complete-call-rules.md",CP="research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md";
const OP="research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-two-ply-frontier-20261119.json";
const MAIN="673eb9078ba311b7dc93140a2d5bc6d8d71b72f0";
const PIN={m:"b35d54a0ced182153802247452a593096a0acf81",r:"a8eaf00bd6494eda50a68e7d06498bed833a7688",k:"ef7483e011d72e0048d667313b6c996d3472729f",c:"b097210d0b49d7cf014cc6a554298b1e49e83384"};
function need(x,s){if(!x)throw Error(s);}
function sha(s){const b=Buffer.from(s,"utf8");return createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");}
function read(p,h){const s=fs.readFileSync(path.join(ROOT,p),"utf8");need(sha(s)===h,"blob SHA "+p);return s;}
function hex(m){return m.toString(16).padStart(32,"0");}
function bits(m){const a=[];for(let i=0;i<121;i++)if((m>>BigInt(i))&1n)a.push(i);return a;}
function row(i){const x=BigInt(i%11),y=BigInt(Math.floor(i/11));return [x*x+y*y,x,y];}
function dc(a,b,c,q){const A=row(a),B=row(b),C=row(c),Q=row(q),u=B.map((v,i)=>v-A[i]),v=C.map((x,i)=>x-A[i]),w=Q.map((x,i)=>x-A[i]);return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]);}
function dl(a,b,c,q){const A=row(a),B=row(b),C=row(c),Q=row(q),u=B.map((v,i)=>v-A[i]),v=C.map((x,i)=>x-A[i]),w=Q.map((x,i)=>x-A[i]);return u[0]*v[1]*w[2]+u[1]*v[2]*w[0]+u[2]*v[0]*w[1]-u[2]*v[1]*w[0]-u[1]*v[0]*w[2]-u[0]*v[2]*w[1];}
const cache=new Map();let detChecks=0;
function tm(a,b,c){const s=[a,b,c].sort((x,y)=>x-y),k=s.join(",");if(cache.has(k))return cache.get(k);let m=0n;for(let q=0;q<121;q++){const x=dc(...s,q),y=dl(...s,q);detChecks++;need(x===y,"determinant mismatch");if(x===0n)m|=1n<<BigInt(q);}cache.set(k,m);return m;}
function pop(m){let n=0;while(m){m&=m-1n;n++;}return n;}
function trans(m,s,fx,fy){let o=0n;for(const i of bits(m)){const x=i%11,y=Math.floor(i/11);let a=s?y:x,b=s?x:y;if(fx)a=10-a;if(fy)b=10-b;o|=1n<<BigInt(a+11*b);}return o;}
function canon(m){let z=null;for(let s=0;s<2;s++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){const v=trans(m,s,x,y);if(z===null||v<z)z=v;}return hex(z);}
const mobility=JSON.parse(read(MP,PIN.m)),residual=JSON.parse(read(RP,PIN.r)),rules=read(KP,PIN.k),convention=read(CP,PIN.c);
need(rules.includes("同一円または同一直線上")&&rules.includes("行列式"),"rule text");
need(convention.includes("det4")&&convention.includes("共線"),"convention text");
const ALL=(1n<<121n)-1n,witness=new Map(residual.witness.map(x=>[x.root,x.rows]));
const per=[],owners=new Map(),hist={};let child=0,total=0,terminal=0;
for(let i=0;i<mobility.mobility.priority_order.length;i++){
 const item=mobility.mobility.priority_order[i],root=BigInt("0x"+item.root),st=bits(root);
 need(st.length===7&&canon(root)===item.root,"root");
 const rows=witness.get(item.root);need(rows&&(rows.length===1||rows.length===2),"rows");
 let base=0n;for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)base|=tm(st[a],st[b],st[c]);
 const first=[];for(let p=0;p<121;p++)if(!((root>>BigInt(p))&1n)&&!((base>>BigInt(p))&1n))first.push(p);
 need(first.join(",")===item.legal_bits.join(","),"first bits");
 const raw=new Set();let second=0,min=999,max=-1,term=0;
 for(const p of first){let extra=0n;for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)extra|=tm(st[a],st[b],p);
  const after=root|(1n<<BigInt(p)),replies=ALL&~(base|extra|after),n=pop(replies);
  second+=n;min=Math.min(min,n);max=Math.max(max,n);if(!n)term++;
  hist[n]=(hist[n]||0)+1;child++;
  for(let q=0;q<121;q++)if((replies>>BigInt(q))&1n)raw.add(hex(after|(1n<<BigInt(q))));
 }
 need(raw.size===second/2,"order identity");
 const cls=new Set([...raw].map(h=>canon(BigInt("0x"+h))));need(cls.size===raw.size,"within-root D4");
 for(const s of cls){if(!owners.has(s))owners.set(s,new Set());owners.get(s).add(i);}
 per.push({input_first_ply_rank:i+1,root:item.root,covered_rows:rows,first_moves:first.length,ordered_second_moves:second,unique_9stone_positions:raw.size,d4_classes:cls.size,within_root_d4_merges:raw.size-cls.size,min_replies:min,max_replies:max,terminal_children:term});
 total+=second;terminal+=term;
}
const coverage={};for(const x of per)coverage[x.covered_rows.length]=(coverage[x.covered_rows.length]||0)+1;
const pm=new Map(),mult={};for(const [state,ids] of owners){const a=[...ids].sort((x,y)=>x-y);mult[a.length]=(mult[a.length]||0)+1;for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){const k=a[i]+":"+a[j];if(!pm.has(k))pm.set(k,[]);pm.get(k).push(state);}}
const pairs=[...pm.entries()].map(([k,states])=>{const [a,b]=k.split(":").map(Number);return {roots:[per[a].root,per[b].root],rows:[per[a].covered_rows,per[b].covered_rows],shared_d4_positions:states.length,states:states.sort()};}).sort((a,b)=>b.shared_d4_positions-a.shared_d4_positions);
const largest=pairs[0],members=per.reduce((s,x)=>s+x.d4_classes,0),unique=owners.size,dups=members-unique;
const maxMult=Math.max(...Object.keys(mult).map(Number)),minReply=Math.min(...per.map(x=>x.min_replies)),maxReply=Math.max(...per.map(x=>x.max_replies)),unordered=total/2;
const ranks=new Map(per.slice().sort((a,b)=>a.unique_9stone_positions-b.unique_9stone_positions||a.root.localeCompare(b.root)).map((x,i)=>[x.root,i+1]));for(const x of per)x.rank_by_two_ply_frontier=ranks.get(x.root);
const checks=[["49 roots",per.length===49],["48 pair roots + 1 singleton",coverage["2"]===48&&coverage["1"]===1],["2,985 eight-stone children",child===2985],["146,118 ordered moves",total===146118],["73,059 nine-stone positions",unordered===73059],["no terminal eight-stone child",terminal===0],["reply range 28..73",minReply===28&&maxReply===73],["no within-root D4 merges",per.every(x=>x.within_root_d4_merges===0)],["72,756 global classes",unique===72756],["303 cross-root duplicates",dups===303],["shared multiplicity exactly two",maxMult===2&&mult["2"]===303],["213 overlapping root pairs",pairs.length===213],["largest overlap 47",largest.shared_d4_positions===47],["28,553 unique triples",cache.size===28553],["3,454,913 checks per expansion",detChecks===28553*121]];
need(checks.every(x=>x[1]),"check failure");
const a=per.find(x=>x.root===largest.roots[0]),b=per.find(x=>x.root===largest.roots[1]);
const summary={roots:per.length,coverage_histogram:coverage,eight_stone_children:child,ordered_second_moves:total,unordered_nine_stone_positions:unordered,total_per_root_frontier_memberships:members,global_unique_d4_classes:unique,cross_root_duplicate_memberships:dups,cross_root_duplicate_rate_percent:Number((100*dups/unordered).toFixed(6)),multiplicity_histogram:mult,nonempty_root_pair_overlaps:pairs.length,largest_pair_overlap:largest.shared_d4_positions,maximum_root_multiplicity:maxMult,terminal_eight_stone_children:terminal,min_replies:minReply,max_replies:maxReply,within_root_d4_merges:per.reduce((s,x)=>s+x.within_root_d4_merges,0)};
const result={schema:"n11-five-parent-49-root-two-ply-frontier-20261119-v1",date:"2026-11-19",status:"exact-two-ply-structural-census",analysis_main_head:MAIN,source_main_head:mobility.source_main_head,input_pins:{mobility:{path:MP,git_blob_sha1:PIN.m},residual:{path:RP,git_blob_sha1:PIN.r},rules:{path:KP,git_blob_sha1:PIN.k},convention:{path:CP,git_blob_sha1:PIN.c}},reproduction_script:{path:SCRIPT_PATH,git_blob_sha1:sha(fs.readFileSync(SCRIPT_FILE,"utf8"))},determinant:{representation:"BigInt exact arithmetic on rows [x^2+y^2,x,y,1], after subtracting the first row",independent_expansions:["three-term cofactor expansion","six-term Leibniz expansion"],unique_triples:cache.size,point_checks_per_expansion:detChecks,all_agree:true},summary,reply_histogram:Object.fromEntries(Object.entries(hist).sort((a,b)=>+a[0]-+b[0])),per_root:per,pairwise_overlap:pairs.map(({states,...x})=>x),largest_pair:{roots:largest.roots,rows:largest.rows,shared_d4_positions:largest.shared_d4_positions,union_d4_positions:a.d4_classes+b.d4_classes-largest.shared_d4_positions,shared_states:largest.states},checks:checks.map(([name,pass])=>({name,pass})),check_count:checks.length,all_pass:true,interpretation_guard:["No candidate root has a one-move terminal child; this does not prove that any root is losing.","The 49 roots remain candidate receipt roots, not WIN7-D10 certificates.","Two-ply frontier counts are not DFPN node counts, run time, or proof cost.","The 303 shared D4 classes measure only this 9-stone frontier; deeper cache benefit may differ.","REFUTED-D10 is not a LOSS proof; standard 11x11 remains UNKNOWN."]};
need(result.all_pass,"not all pass");
fs.mkdirSync(path.dirname(OP),{recursive:true});
fs.writeFileSync(OP,JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify({output:OP,check_count:result.check_count,summary:result.summary},null,2));
