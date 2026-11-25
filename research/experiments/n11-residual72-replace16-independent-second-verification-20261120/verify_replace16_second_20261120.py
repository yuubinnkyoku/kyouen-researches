#!/usr/bin/env python3
"""Independent geometry and ledger audit for the N11 residual-72 replace16 sweep."""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
INPUTS=[
("K1085","research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json","5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e"),
("K1086","research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json","3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced"),
("K1088","research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json","16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724"),
("K1089","research/experiments/n11-residual72-replace16-d10-sweep-20261120/output/replace16-d10-sweep-20261120.json","808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc")]
RUNNER_PATH="research/experiments/n11-residual72-replace16-d10-sweep-20261120/runner_v17.ts"
RUNNER_GIT_BLOB="c132cc6425eee3feaeef1d697dd74f968cfedb59"
def readp(n,p,h):
 raw=(ROOT/p).read_bytes();s=hashlib.sha256(raw).hexdigest()
 if s!=h:raise SystemExit(n+" SHA-256 mismatch: "+s)
 blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
 return json.loads(raw),{"name":n,"path":p,"sha256":s,"git_blob_sha1":blob}
def cells(v):return [i for i in range(121) if (v>>i)&1]
def d4(v):
 out=[]
 for m in range(8):
  a=[]
  for i in cells(v):
   x,y=i%11,i//11
   X,Y=((x,y),(10-y,x),(10-x,10-y),(y,10-x),(10-x,y),(x,10-y),(y,x),(10-y,10-x))[m]
   a.append(Y*11+X)
  out.append(sum(1<<i for i in a))
 return out
def canon(v):return min(format(x,"032x") for x in d4(v))
def det(m):
 if len(m)==1:return m[0][0]
 return sum((-1 if j%2 else 1)*v*det([r[:j]+r[j+1:] for r in m[1:]]) for j,v in enumerate(m[0]))
def safe(v):
 pts=[[i%11,i//11,(i%11)**2+(i//11)**2,1] for i in cells(v)]
 return all(det(list(g))!=0 for g in itertools.combinations(pts,4))
def main():
 docs={};info=[]
 for n,p,h in INPUTS:docs[n.lower()],x=readp(n,p,h);info.append(x)
 a,b,c,d=(docs[x] for x in ("k1085","k1086","k1088","k1089"))
 raw=(ROOT/RUNNER_PATH).read_bytes();runner=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
 checks=[]
 def gate(n,ok,detail):checks.append({"name":n,"pass":bool(ok),"detail":detail})
 pins={n.lower():h for n,p,h in INPUTS}
 gate("input-sha256-pins",all(x["sha256"]==pins[x["name"].lower()] for x in info) and d["inputs"]["k1085_sha256"]==pins["k1085"] and d["inputs"]["k1086_sha256"]==pins["k1086"] and d["inputs"]["k1088_sha256"]==pins["k1088"],{"k1085":info[0]["sha256"],"k1086":info[1]["sha256"],"k1088":info[2]["sha256"],"k1089":info[3]["sha256"]})
 gate("runner-v17-git-blob-pin",runner==RUNNER_GIT_BLOB==d["runner_git_blob"],{"expected":RUNNER_GIT_BLOB,"actual":runner})
 rows=[int(x,16) for x in a["base_state"]["residual_row_hex"]];rs={canon(x) for x in rows}
 wr=[x["root"] for x in b["classification"]["win8_d10_candidates"]];rr=[x["root"] for x in b["classification"]["refuted_d10_facts"]]
 ws={canon(int(y,16)) for r in wr for y in b["per_root"][r]["covered_rows"]};ref={canon(int(y,16)) for r in rr for y in b["per_root"][r]["covered_rows"]}
 gate("k1085-base-has-72-unique-six-stone-rows",len(rows)==72 and len(rs)==72 and all(x.bit_count()==6 for x in rows),{"count":72,"unique":len(rs)})
 gate("k1086-partition-is-7-win-16-refuted",len(wr)==7 and len(rr)==16,{"win":len(wr),"refuted":len(rr)})
 gate("k1086-win-and-refuted-rows-disjoint",not(ws&ref),{"winRows":len(ws),"refutedRows":len(ref)})
 gate("k1086-claimed-rows-partition-k1085-base",len(ws)==23 and len(ref)==49 and ws|ref==rs and len(ws|ref)==72,{"win":len(ws),"refuted":len(ref),"union":len(ws|ref)})
 residual={canon(int(x,16)) for x in c["exclusion"]["residual49_rows"]}
 gate("k1088-residual49-equals-k1086-refuted-footprints",len(residual)==49 and residual==ref,{"k1088":len(residual),"k1086":len(ref)})
 sel=c["scope1_refsolve_residual49"]["greedy_selection"];swept=list(d["per_root"])
 gate("k1088-plan-and-k1089-sweep-root-sets-match",len(sel)==16 and len(swept)==16 and set(x["root"] for x in sel)==set(swept),{"planned":len(sel),"swept":len(swept)})
 bc,bs,bv,br,bp=[],[],[],[],[];counts={}
 for item in sel:
  rh=item["root"];root=int(rh,16);rec=d["per_root"].get(rh)
  if canon(root)!=rh:bc.append(rh)
  if root.bit_count()!=8 or not safe(root):bs.append(rh)
  if rec is None or set(rec["covered_rows"])!=set(item["covered_rows"]):br.append(rh)
  for y in item["covered_rows"]:
   row=int(y,16);key=canon(row);counts[key]=counts.get(key,0)+1
   if row.bit_count()!=6 or key not in residual:br.append(y)
   if not any((row&image)==row for image in d4(root)):bv.append(y)
  if rec:
   for order in ("andclose0","andclose1"):
    z=rec["probes"].get(order)
    if z is None or z["capped"] or z["ordering"]!=order or not isinstance(z["nodes"],int) or z["nodes"]<=0 or len(z["terminalStoneRange"])!=2:bp.append(rh)
   if rec["probes"]["andclose0"]["loss"]!=rec["probes"]["andclose1"]["loss"]:bp.append(rh)
 gate("replacement-roots-are-16-safe-eight-stone-canonical",not bc and not bs and not br,{"badCanonical":len(bc),"badSafe":len(bs),"badRows":len(br),"quadruplesChecked":1120})
 gate("replacement-claims-match-k1088-plan",not br,{"badClaims":len(br)})
 mult=[x for x in residual if counts.get(x)!=1]
 gate("all-49-rows-covered-exactly-once-by-subset-of-a-d4-image",not bv and not mult and len(counts)==49,{"badCoverage":len(bv),"badMultiplicity":len(mult),"covered":len(counts)})
 gains={}
 for x in sel:gains[str(x["gained_rows"])]=gains.get(str(x["gained_rows"]),0)+1
 gate("replacement-gains-histogram-reproduces",gains=={"2":2,"3":11,"4":3} and not c["scope1_refsolve_residual49"]["leftover_rows"],{"gainsHist":gains,"leftover":len(c["scope1_refsolve_residual49"]["leftover_rows"])})
 gate("all-32-published-probes-uncapped-and-order-consistent",not bp,{"probes":32,"bad":len(bp)})
 cw=[r for r,v in d["per_root"].items() if v["probes"]["andclose0"]["loss"] is True];cr=[r for r,v in d["per_root"].items() if v["probes"]["andclose0"]["loss"] is False]
 wl=[x["root"] for x in d["classification"]["win8_d10_candidates"]];rl=[x["root"] for x in d["classification"]["refuted_d10_facts"]]
 nodes=sum(v["probes"]["andclose0"]["nodes"]+v["probes"]["andclose1"]["nodes"] for v in d["per_root"].values());mx=max(z["nodes"] for v in d["per_root"].values() for z in v["probes"].values())
 ranges=[z["terminalStoneRange"] for v in d["per_root"].values() for z in v["probes"].values()];tr=[min(x[0] for x in ranges),max(x[1] for x in ranges)]
 gate("k1089-classification-and-node-ledger-reproduce",set(wl)==set(cw) and set(rl)==set(cr) and len(wl)==3 and len(rl)==13 and nodes==6339079==d["classification"]["nodes_total"] and mx==878391 and d["classification"]["capped_probes"]==0 and d["classification"]["error_probes"]==0 and not d["classification"]["unresolved"] and tr==[12,18],{"wins":3,"refuted":13,"nodes":nodes,"maxNode":mx,"capped":0,"errors":0,"terminalRange":tr})
 gate("all-72-base-rows-are-quadruple-free",all(safe(x) for x in rows),{"rows":72,"quadruplesChecked":1080})
 source=len(d["gates"])==13 and all(x["pass"] for x in d["gates"]) and d["targets"]["replacement_roots"]==16 and d["targets"]["probes_planned"]==32 and d["replacement_plan_geometry_independent_rederivation"]["claimed_pairs_ok"]==49 and d["replacement_plan_geometry_independent_rederivation"]["d4_min_canonical_roots"]==16 and d["replacement_plan_geometry_independent_rederivation"]["quad_free_roots"]==16 and d["residual49_rederivation"]["partition"]["disjoint"] and d["residual49_rederivation"]["partition"]["union_is_residual72"]
 gate("k1089-source-gates-and-target-contract-pass",source,{"sourceGates":13,"failed":0,"targetRoots":16,"plannedProbes":32,"pairsOk":49})
 audit={"schema":"n11-residual72-replace16-independent-second-verification-v1","date":"2026-11-20","inputs":info,"runner":{"path":RUNNER_PATH,"git_blob_sha1":runner},"checks":checks,"summary":{"base_rows":72,"refuted_residual_rows":49,"replacement_roots":16,"probes":32,"win8_d10_candidates":3,"refuted_d10_facts":13,"nodes_total":nodes,"max_probe_nodes":mx,"quadruple_checks_roots":1120,"quadruple_checks_rows":1080},"interpretation_guard":["この監査はK1089の公開済み根・行の幾何と32 probe記録の整合性を独立照合したもので、DFPNエンジンを再実行したものではない。","WIN8-D10 candidateは証明書ではなく、receipt foldもS6行の閉鎖も行っていない。","REFUTED-D10はLOSS証明ではない。","標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。"]}
 if not all(x["pass"] for x in checks):raise SystemExit(json.dumps({"failed":[x for x in checks if not x["pass"]]},ensure_ascii=False,indent=2))
 out=ROOT/"research/experiments/n11-residual72-replace16-independent-second-verification-20261120/output/audit.json";out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079")
if __name__=="__main__":main()
