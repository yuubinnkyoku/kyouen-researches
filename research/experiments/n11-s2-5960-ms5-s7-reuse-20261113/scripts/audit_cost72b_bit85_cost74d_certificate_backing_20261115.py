#!/usr/bin/env python3
"""Verify D4 certificate reuse of cost72b bit85 in the cost74d receipt fold."""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
REPO=Path(__file__).resolve().parents[4]
OUT=REPO/"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output"
M5=REPO/"research/experiments/n11-s2-5960-milestone5-20261112/output"
RESULT=OUT/"class2-lane-cost72b-bit85-cost74d-certificate-backed-frontier-audit-20261115.json"
def j(n): return json.loads((OUT/n).read_text(encoding="utf-8"))
def jl(n): return [json.loads(x) for x in (OUT/n).read_text(encoding="utf-8").splitlines() if x.strip()]
def pts(m): return [p for p in range(121) if (m>>p)&1]
def det4(ps):
 a=[]
 for p in ps:
  x,y=p%11,p//11;a.append((x*x+y*y,x,y,1))
 z=0
 for q in itertools.permutations(range(4)):
  inv=sum(q[i]>q[k] for i in range(4) for k in range(i+1,4));t=1
  for i,k in enumerate(q):t*=a[i][k]
  z+=-t if inv&1 else t
 return z
def safe(m,n):
 p=pts(m);assert len(p)==n
 return all(det4(q)!=0 for q in itertools.combinations(p,4))
def tp(p,k):
 x,y=p%11,p//11
 a,b=((x,y),(y,10-x),(10-x,10-y),(10-y,x),(10-x,y),(x,10-y),(y,x),(10-y,10-x))[k]
 return 11*b+a
def tr(m,k):
 z=0
 for p in pts(m):z|=1<<tp(p,k)
 return z
def canon(m):return min(tr(m,k) for k in range(8))
def parents(m):return sorted({f"{canon(m^(1<<p)):032x}" for p in pts(m)})
def main():
 m72=j("class2-lane-cost72b-win7-certificates-20261115.json")
 i72=j("class2-lane-cost72b-inflight-20261115.json")
 i74=j("class2-lane-cost74d-inflight-20261115.json")
 f74=j("class-frontier-cost74d-receipts-recompute-20261115.json")
 v74=jl("class2-lane-cost74d-v15-crosscheck-20261115.jsonl")
 b118=j("class2-lane-cost74d-cert-bit118-record-20261115.json")
 c72,c74=int(i72["s6_child"],16),int(i74["s6_child"],16)
 r72,r74=c72|(1<<85),c74|(1<<91)
 cert=next(x for x in m72["certificates"] if x["bit"]==85)
 a91=next(x for x in v74 if x.get("bit")==91)
 assert cert["root_hex"]==f"{r72:032x}" and cert["verdict"]=="WIN7"
 assert cert["rows"]==40352 and cert["sub_roots_pass"]==cert["sub_roots_total"]==55
 assert cert["union_missing"]==cert["union_extra"]==cert["fbt_drops"]==0
 assert a91["loss"] and a91["nodes"]==5415122 and not a91["capped"]
 data=(REPO/cert["storage"]["parts"][0]["path"]).read_bytes()
 blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert blob==cert["whole_git_blob_sha"]=="c99ef87964f4770e7dab365ea42ad070b8c6495d"
 assert hashlib.md5(data).hexdigest()==cert["md5"] and hashlib.sha256(data).hexdigest()==cert["sha256"]
 assert safe(c72,6) and safe(c74,6) and safe(r72,7) and safe(r74,7)
 assert tr(r72,5)==r74
 canon_hex=f"{canon(r72):032x}"
 assert canon_hex==f"{canon(r74):032x}"=="00000000000080811202000020000000"
 p72,p74=parents(r72),parents(r74);assert p72==p74 and len(p72)==7
 s6=set();rows=0
 for n in range(1,7):
  lines=(M5/f"ms5_s6_manifest_part{n}.csv").read_text(encoding="utf-8").splitlines()
  assert lines[0]=="hex,cost,classes"
  for line in lines[1:]:
   if line:s6.add(f"{canon(int(line.split(',',1)[0],16)):032x}");rows+=1
 assert rows==len(s6)==7867
 addition=f74["cost74d_addition"];new={h for x in addition for h in x["marginal_manifest_hexes"]}
 bit91=next(x for x in addition if x["bit"]==91);bit2=next(x for x in addition if x["bit"]==2);bit118=next(x for x in addition if x["bit"]==118)
 backed=[p for p in p72 if p in new]
 assert bit91["marginal_manifest_hexes"]==["00000000000000809102000002000000","00000000000080003800000028000000"]
 assert "00000000000000809102020000000000" in bit2["marginal_manifest_hexes"]
 assert backed==["00000000000000809102000002000000","00000000000000809102020000000000","00000000000080003800000028000000"]
 assert all(x in s6 for x in backed)
 assert bit118["certified"] and bit118["marginal_in_manifest"]==0
 assert b118["independent_verification"]["verdict"]=="WIN7 certificate independently verified"
 before,after=f74["frontier_before_cost74d"],f74["frontier_after_cost74d"]
 assert before["solved_s6_in_manifest"]==1163 and after["solved_s6_in_manifest"]==1179
 assert after["unique_remaining_s6"]==6668 and after["sum_remaining_cost"]==526075
 assert after["s6_needed_by_open_classes"]==4938 and after["cost_needed_by_open_classes"]==389798
 assert len(addition)==15 and sum(x["marginal_in_manifest"] for x in addition)==16
 assert i74["status"]=="raw-sweep-complete-receipts-folded"
 assert i72["rebase_required"]["baseline_head"]==1179
 result={"schema":"n11-class2-cost72b-bit85-cost74d-certificate-backed-frontier-audit-20261115-v1","date":"2026-11-15","source_main_before_audit":"392197b77610865199e48db68d050a3b61f004ad","frontier_receipts":{"before":before,"after":after,"new_s6_manifest_orbits":16,"receipt_count":15,"marginal_s6_total":sum(x["marginal"] for x in addition)},"cost72b_bit85_certificate":{"root_hex":f"{r72:032x}","rows":cert["rows"],"sub_roots_pass":cert["sub_roots_pass"],"git_blob_sha":blob},"cost74d_bit91_candidate":{"root_hex":f"{r74:032x}","v15_loss":a91["loss"],"v15_nodes":a91["nodes"]},"d4":{"transform_index":5,"coordinate_map":"(x,y)->(x,10-y)","canonical_root_hex":canon_hex,"same_parent_orbits":True},"certificate_backed_new_s6_manifest_orbits":backed,"certificate_backed_delta":len(backed),"certificate_backed_lower_bound":before["solved_s6_in_manifest"]+len(backed),"receipt_frontier":after["solved_s6_in_manifest"],"bit118_local_certificate":{"independently_verified":True,"marginal_in_manifest":0,"rows":b118["strategy_rows"],"sub_roots":b118["subroots_passed"]},"interpretation_guard":"Receipt frontier 1179 is not a count of independently certified S6 positions. Cost72b bit85 backs three of the 16 new S6 manifest orbits, giving a certificate-backed lower bound of 1166 from the 1163 baseline. The other new receipt orbits are not classified by this audit. Fold all 13 cost72b certificates on head 1179 with D4 deduplication. Empty 11x11, two-stone roots, S2, class2 and class4 remain UNKNOWN."}
 RESULT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
