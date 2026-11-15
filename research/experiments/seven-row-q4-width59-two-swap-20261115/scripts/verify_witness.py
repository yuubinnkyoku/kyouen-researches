#!/usr/bin/env python3
"""Independent exact verifier using normalized integer line/circle equations."""
from itertools import combinations
from math import gcd
import json
from pathlib import Path
BASE=[(21,0),(23,0),(26,0),(18,1),(27,1),(39,1),(14,2),(28,2),(46,2),(25,3),(30,3),(39,3),(18,4),(36,4),(43,4),(13,5),(27,5),(35,5),(14,6),(42,6)]
CASES=[{"name":"A","width":57,"removed_indices":[2,4],"added":[(24,0),(13,1)]},{"name":"B","width":59,"removed_indices":[7,13],"added":[(56,2),(7,4)]}]
def norm_line(p,q):
 x1,y1=p;x2,y2=q;a,b,c=y2-y1,x1-x2,x2*y1-x1*y2
 g=gcd(gcd(abs(a),abs(b)),abs(c))
 if g:a,b,c=a//g,b//g,c//g
 if a<0 or (a==0 and b<0):a,b,c=-a,-b,-c
 return a,b,c
def norm_circle(p,q,r):
 x1,y1=p;x2,y2=q;x3,y3=r;s1=x1*x1+y1*y1;s2=x2*x2+y2*y2;s3=x3*x3+y3*y3
 det=x1*(y2-y3)-y1*(x2-x3)+(x2*y3-x3*y2)
 if det==0:return None
 B=s1*(y2-y3)-y1*(s2-s3)+(s2*y3-s3*y2)
 C=x1*(s2-s3)-s1*(x2-x3)+(x2*s3-x3*s2)
 D=x1*(y2*s3-y3*s2)-y1*(x2*s3-x3*s2)+s1*(x2*y3-x3*y2)
 a,b,c,d=det,-B,-C,-D;g=gcd(gcd(gcd(abs(a),abs(b)),abs(c)),abs(d))
 if g:a,b,c,d=a//g,b//g,c//g,d//g
 if a<0:a,b,c,d=-a,-b,-c,-d
 return a,b,c,d
def on_line(co,p):
 a,b,c=co;x,y=p;return a*x+b*y+c==0
def on_circle(co,p):
 a,b,c,d=co;x,y=p;return a*(x*x+y*y)+b*x+c*y+d==0
def verify(case,keep=False):
 w=case["width"];s=[p for i,p in enumerate(BASE) if i not in case["removed_indices"]]+list(case["added"])
 assert len(s)==20 and len(set(s))==20 and all(0<=x<w and 0<=y<7 for x,y in s)
 rows=[sum(y==r for x,y in s) for r in range(7)];assert rows==[3,3,3,3,3,3,2]
 lines={norm_line(p,q) for p,q in combinations(s,2)}
 lm={c:[p for p in s if on_line(c,p)] for c in lines}
 circles={c for tri in combinations(s,3) if (c:=norm_circle(*tri)) is not None}
 cm={c:[p for p in s if on_circle(c,p)] for c in circles}
 ml=max(map(len,lm.values()));mc=max(map(len,cm.values()));assert ml<=3 and mc<=3
 occ=set(s);blocked=[];special={}
 for x in range(w):
  p=(x,6)
  if p in occ:continue
  hit=None
  for kind,mp,test in (("line",lm,on_line),("circle",cm,on_circle)):
   for co,members in mp.items():
    if len(members)>=3 and test(co,p):hit={"kind":kind,"equation":list(co),"triple":[list(z) for z in members[:3]]};break
   if hit is not None:break
  assert hit is not None,f"uncovered {(x,6)}"
  blocked.append(x)
  if x in (57,58):special[str(x)]=hit
 nxt=(w,6);next_blocked=any(len(m)>=3 and on_line(c,nxt) for c,m in lm.items()) or any(len(m)>=3 and on_circle(c,nxt) for c,m in cm.items())
 out={"name":case["name"],"board":{"width":w,"height":7,"q":4},"construction":{"base_width":53,"removed_indices":case["removed_indices"],"removed":[list(BASE[i]) for i in case["removed_indices"]],"added":[list(p) for p in case["added"]]},"stones":[list(p) for p in s],"row_counts":rows,"safety":{"method":"normalized integer line/circle equations; no floating point","distinct_lines":len(lines),"distinct_circles":len(circles),"max_line_points":ml,"max_circle_points":mc,"safe":True},"maximality":{"deficient_row":6,"empty_points":len(blocked),"all_blocked":True,"rows_0_to_5_blocked_by_horizontal_three":True},"next_column":{"cell":list(nxt),"blocked":next_blocked}}
 if keep:out["maximality"]["blocked_x_values"]=blocked;out["maximality"]["special_blockers"]=special
 return out
def main():
 a=verify(CASES[0]);b=verify(CASES[1],True)
 assert b["maximality"]["special_blockers"]["57"]["kind"]=="line" and b["maximality"]["special_blockers"]["57"]["equation"]==[1,-6,-21]
 assert b["maximality"]["special_blockers"]["58"]["kind"]=="circle" and b["maximality"]["special_blockers"]["58"]["equation"]==[3,-307,611,3940]
 assert not b["next_column"]["blocked"]
 out={"scope":"exact finite witness verification; no nonexistence claim at width 60","verified_witnesses":[a,b]}
 d=Path(__file__).resolve().parents[1]/"output";d.mkdir(parents=True,exist_ok=True)
 (d/"verification.json").write_text(json.dumps(out,separators=(",",":"))+"\n")
 (d/"witness_7x59.json").write_text(json.dumps(b,separators=(",",":"))+"\n")
 print(json.dumps({"verified":[{"name":v["name"],"width":v["board"]["width"],"safe":v["safety"]["safe"],"max_line":v["safety"]["max_line_points"],"max_circle":v["safety"]["max_circle_points"],"empty_deficient_cells":v["maximality"]["empty_points"],"uncovered":0,"next_column_blocked":v["next_column"]["blocked"]} for v in (a,b)]},indent=2))
if __name__=="__main__":main()