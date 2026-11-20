#!/usr/bin/env python3
"""Independent D4 geometry preflight for K1113 and K1114."""
import hashlib, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-residual58-fold16-k1113-geometry-preflight-20261120"
OUT = EXP / "output/geometry-preflight.json"
FOLD14 = ROOT / "research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/output/win8-root9090022-receipt-fold-20261120.json"
K1097 = ROOT / "research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json"
ROOTS = {
 "K1113": ("00000000010000889002000080100000",
  ROOT/"research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/output/win8-cert-extract-verification-20261120.json",
  ROOT/"research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/certs/win8-root-00000000010000889002000080100000-20261120.n11", 4),
 "K1114": ("00000000012000003800080009000000",
  ROOT/"research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/output/win8-cert-extract-verification-20261120.json",
  ROOT/"research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/certs/win8-root-00000000012000003800080009000000-20261120.n11", 3)
}
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pts(m):
 out=[]
 while m:
  b=m&-m; out.append(b.bit_length()-1); m^=b
 return out
T=[]
for t in range(8):
 tab=[]
 for p in range(121):
  x,y=p%11,p//11
  if t==0:X,Y=x,y
  elif t==1:X,Y=10-y,x
  elif t==2:X,Y=10-x,10-y
  elif t==3:X,Y=y,10-x
  elif t==4:X,Y=10-x,y
  elif t==5:X,Y=x,10-y
  elif t==6:X,Y=y,x
  else:X,Y=10-y,10-x
  tab.append(11*Y+X)
 T.append(tab)
def tr(m,t):
 z=0
 for p in pts(m): z|=1<<T[t][p]
 return z
def can(m): return min(tr(m,t) for t in range(8))
def d3(a,b,c):
 x1,y1=a; x2,y2=b; x3,y3=c
 q1=x1*x1+y1*y1; q2=x2*x2+y2*y2; q3=x3*x3+y3*y3
 return q1*(x2*y3-x3*y2)-q2*(x1*y3-x3*y1)+q3*(x1*y2-x2*y1)
def d4(a,b,c,d): return d3(a,b,c)-d3(a,b,d)+d3(a,c,d)-d3(b,c,d)
def bad4(m):
 ps=[(p%11,p//11) for p in pts(m)]
 return sum(d4(*q)==0 for q in itertools.combinations(ps,4))
def geometry(m):
 ps=pts(m)
 a={can(sum(1<<p for p in q)) for q in itertools.combinations(ps,6)}
 b=set()
 for t in range(8):
  im=tr(m,t); ips=pts(im)
  for x,y in itertools.combinations(ips,2): b.add(can(im&~(1<<x)&~(1<<y)))
 return a,b
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def main():
 f=load(FOLD14); k=load(K1097)
 assert f["status"]=="fold-complete"
 residual={int(x,16) for x in f["five_parent_target_after"]["residual_row_hex_after"]}; assert len(residual)==58
 out={"schema":"n11-residual58-fold16-k1113-geometry-preflight-v1",
  "baseline":{"fold14_sha256":h(FOLD14),"residual_rows":58,"k1097_sha256":h(K1097)},"roots":{},"cross_root":{},
  "interpretation_guard":["Geometric preflight only; not a receipt fold.","WIN8-D10 proves only the named eight-stone root game tree.","K1113 fold16 must wait for K1114 fold15 completion and recheck the actual published frontier.","S6 row closure is bookkeeping, not a game-theoretic value.","11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN."]}
 sets={}
 for name,(hx,ap,cp,nclaim) in ROOTS.items():
  a=load(ap); cert=cp.read_bytes(); lines=cert.decode().splitlines(); m=int(hx,16)
  assert a["all_gates_pass"] and a["gate_count"]==19 and a["root"]==hx
  assert len(pts(m))==8 and can(m)==m and bad4(m)==0
  cm=a["recorded"]["certificate"]; assert h(cp)==cm["sha256"] and len(cert)==cm["bytes"] and len(lines)==cm["rows"]+2
  assert lines[0]=="n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS" and lines[1]=="root "+hx
  claims={int(x,16) for x in a["recorded"]["k1086_claimed_coverage_rows"]}; assert len(claims)==nclaim and claims=={int(x,16) for x in a["recorded"]["k1097_footprint_rows"]}
  fp=k["win16_intrinsic_footprints"][hx]; assert fp["intrinsic_equals_claimed"] and {int(x,16) for x in fp["claimed"]}==claims and {int(x,16) for x in fp["intrinsic"]}==claims
  s1,s2=geometry(m); assert len(s1)==28 and s1==s2 and claims<=s1
  hits=s1&residual; assert hits==claims
  sets[name]=s1
  out["roots"][name]={"root":hx,"stones":8,"d4_canonical":True,"unsafe_quadruples":0,
   "certificate":{"bytes":len(cert),"strategy_rows":cm["rows"],"sha256":cm["sha256"],"audit_sha256":h(ap),"audit_gates":19},
   "claimed_rows":sorted(f"{x:032x}" for x in claims),"geometry":{"six_subsets":28,"d4_pair_deletion_operations":224,"canonical_rows":28,"two_methods_equal":True,"rows":sorted(f"{x:032x}" for x in s1)},
   "fold14_residual58":{"hit_count":len(hits),"hits":sorted(f"{x:032x}" for x in hits),"extra_hits":[],"claims_all_open":True},"k1097_footprint_exact":True}
 inter=sets["K1113"]&sets["K1114"]
 c13={int(x,16) for x in out["roots"]["K1113"]["claimed_rows"]}
 c14={int(x,16) for x in out["roots"]["K1114"]["claimed_rows"]}
 assert not inter and not (sets["K1113"]&c14) and not (sets["K1114"]&c13)
 post=residual-c14; remain=sets["K1113"]&post; assert remain==c13
 out["cross_root"]={"geometry_intersection_count":0,"K1113_vs_K1114_claims_intersection_count":0,
  "K1114_vs_K1113_claims_intersection_count":0,
  "conditional_after_fold15_if_only_its_three_preflight_hits_close":{"K1113_open_claim_count":len(remain),"K1113_claims_remaining_open":sorted(f"{x:032x}" for x in remain),"unchanged":True}}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"output":str(OUT.relative_to(ROOT)),"sha256":h(OUT),"residual58":58,"K1113_hits":4,"K1114_hits":3,"cross_root_geometry_overlap":0,"all_checks":"PASS"},sort_keys=True))
if __name__=="__main__": main()
