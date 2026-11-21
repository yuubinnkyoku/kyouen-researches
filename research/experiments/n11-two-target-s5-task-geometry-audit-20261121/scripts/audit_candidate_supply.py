#!/usr/bin/env python3
"""Independent geometry and ledger audit of the two-target S5 candidate supply."""
import argparse, ast, csv, hashlib, io, json
from itertools import combinations
from pathlib import Path

COMMIT = "d173632fc19a3d9f9abf8e66d0595f4629748bf0"
PINS = {
 "initial_tasks": ("research/experiments/n11-two-target-design-20261010/output/shared-s5-tasks.csv", "366ff5cd673c09694c8b047e76291174e6c91cf4"),
 "initial_classes": ("research/experiments/n11-two-target-design-20261010/output/candidate-classes.csv", "7e87281fb254d8e8ca85894f16ac29e3137e5b3d"),
 "post_tasks": ("research/experiments/n11-two-target-design-20261010/output/post-probe/shared-s5-tasks.csv", "fa4ba4ab8b0f165c90945f7505de29aebb53d3ac"),
 "post_classes": ("research/experiments/n11-two-target-design-20261010/output/post-probe/candidate-classes.csv", "fc1e3bcf85857ec2248ea7311d5be0f556f19291"),
 "base_cache": ("research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-3.cache", "bcdba2d0ae3309e6e80702068ee5a64266f622ff"),
 "merged_cache": ("research/experiments/n11-two-target-design-20261010/output/merged-exact-s5.cache", "5f20fea7993e1faef15b4bfc4219538858a3223a"),
 "quarantine": ("results/n11-s5-evidence-quarantine.json", "6a320237545874ddd841c90be095cccccc46249d"),
}
LOW = (1 << 64) - 1
TRANSFORMS = []
for refl in (False, True):
 for rot in range(4):
  mapping=[]
  for p in range(121):
   x,y=p%11,p//11
   if refl: x=10-x
   for _ in range(rot): x,y=y,10-x
   mapping.append(y*11+x)
  TRANSFORMS.append(mapping)

def blob_sha1(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
def key(mask): return f"{mask & LOW}:{mask >> 64}"
def parse_key(s):
 lo,hi=map(int,s.split(":"))
 if not (0<=lo<1<<64 and 0<=hi<1<<57): raise ValueError("out-of-range key")
 return lo|(hi<<64)
def canonical(mask):
 pts=[p for p in range(121) if mask>>p&1]
 best=None
 for mapping in TRANSFORMS:
  m=0
  for p in pts: m|=1<<mapping[p]
  if best is None or m<best: best=m
 return best
def det4(p0,p1,p2,p3):
 x0,y0=p0%11,p0//11; s0=x0*x0+y0*y0
 x1,y1=p1%11,p1//11; d1=(x1-x0,y1-y0,x1*x1+y1*y1-s0)
 x2,y2=p2%11,p2//11; d2=(x2-x0,y2-y0,x2*x2+y2*y2-s0)
 x3,y3=p3%11,p3//11; d3=(x3-x0,y3-y0,x3*x3+y3*y3-s0)
 return d1[0]*(d2[1]*d3[2]-d2[2]*d3[1])-d1[1]*(d2[0]*d3[2]-d2[2]*d3[0])+d1[2]*(d2[0]*d3[1]-d2[1]*d3[0])
def read_csv(data):
 return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
def read_cache(data):
 out={}
 for row in csv.reader(io.StringIO(data.decode("utf-8-sig"))):
  if not row or row[0].startswith("#"): continue
  if len(row)!=6 or row[0]!="s5verdict" or int(row[3])!=5 or int(row[4]) not in (1,2): raise ValueError("invalid cache row")
  k=f"{row[1]}:{row[2]}"; v=int(row[4])
  if k in out:
   if out[k]!=v: raise ValueError("cache verdict conflict: "+k)
   raise ValueError("duplicate cache key: "+k)
  out[k]=v
 return out
def class_map(rows): return {r["key"]:r for r in rows}
def counts(values):
 out={}
 for v in values: out[str(v)]=out.get(str(v),0)+1
 def sortkey(k): return (0,int(k)) if k.isdigit() else (1,k)
 return dict(sorted(out.items(),key=lambda x:sortkey(x[0])))
def class_stats(rows):
 active=[r for r in rows if r["status"]=="UNKNOWN"]
 return {"classes":len(rows),"status_counts":counts(r["status"] for r in rows),
  "all_class_unknown_s5_sum":sum(int(r["s5_unknown"]) for r in rows),
  "active_unknown_s5_incidence_sum":sum(int(r["s5_unknown"]) for r in active),
  "loss_s5_sum":sum(int(r["s5_loss"]) for r in rows),
  "win_s5_sum":sum(int(r["s5_win"]) for r in rows)}
def active_quarantine(data):
 doc=json.loads(data.decode("utf-8"))
 if doc.get("schema")!="n11-s5-evidence-quarantine-v1" or not isinstance(doc.get("entries"),list): raise ValueError("invalid quarantine registry")
 seen=set(); active=set()
 for e in doc["entries"]:
  k=tuple(e["key"])
  if k in seen: raise ValueError("duplicate quarantine key")
  seen.add(k)
  if e.get("active") is True: active.add(f"{k[0]}:{k[1]}")
 return active
def verify_tasks(rows, classes, cache, quarantine):
 errors=[]; legal_dist={}; parent_dist={}; hist_budget={}; hist_obs={}; seen=set()
 gates={name:0 for name in ("stone_count","canonical","safe","legal_count_match","parent_coverage_match","cache_absent","quarantine_absent")}
 for r in rows:
  k=r["key"]
  if k in seen: errors.append((k,"duplicate task key"))
  seen.add(k)
  try: m=parse_key(k)
  except Exception as ex: errors.append((k, "key parse "+str(ex))); continue
  pts=[p for p in range(121) if m>>p&1]
  if len(pts)!=5: errors.append((k, "stone count "+str(len(pts)))); continue
  gates["stone_count"]+=1
  if canonical(m)==m: gates["canonical"]+=1
  else: errors.append((k,"noncanonical"))
  safe=not any(det4(*q)==0 for q in combinations(pts,4))
  if safe: gates["safe"]+=1
  else: errors.append((k,"unsafe"))
  legal=0
  for p in range(121):
   if m>>p&1: continue
   if not any(det4(a,b,c,p)==0 for a,b,c in combinations(pts,3)): legal+=1
  if legal==int(r["legal"]): gates["legal_count_match"]+=1
  else: errors.append((k,"legal mismatch "+str(legal)+" != "+r["legal"]))
  parents=sorted(set(key(canonical(m^(1<<p))) for p in pts))
  live=sorted(pk for pk in parents if classes.get(pk,{}).get("status")=="UNKNOWN")
  listed=sorted(ast.literal_eval(r["live_parent_keys"]))
  if len(live)==int(r["live_parents"]) and live==listed: gates["parent_coverage_match"]+=1
  else: errors.append((k,"parent mismatch"))
  if k not in cache: gates["cache_absent"]+=1
  else: errors.append((k,"cached task"))
  if k not in quarantine: gates["quarantine_absent"]+=1
  else: errors.append((k,"quarantined task"))
  legal_dist[str(legal)]=legal_dist.get(str(legal),0)+1
  parent_dist[str(len(live))]=parent_dist.get(str(len(live)),0)+1
  hist_budget[str(r["history_max_unknown_budget"])]=hist_budget.get(str(r["history_max_unknown_budget"]),0)+1
  hist_obs[str(r["historical_observations"])]=hist_obs.get(str(r["historical_observations"]),0)+1
 return {"count":len(rows),"unique_keys":len(seen),"gate_counts":gates,"total_gate_passes":sum(gates.values()),
  "legal_distribution":dict(sorted(legal_dist.items(),key=lambda x:int(x[0]))),"live_parent_distribution":dict(sorted(parent_dist.items(),key=lambda x:int(x[0]))),
  "history_budget_distribution":dict(sorted(hist_budget.items(),key=lambda x:int(x[0]))),"historical_observation_distribution":dict(sorted(hist_obs.items(),key=lambda x:int(x[0]))),"errors":errors}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--root",type=Path,required=True,help="local repository/input root with pinned paths")
 ap.add_argument("--out",type=Path,required=True)
 args=ap.parse_args()
 docs={}
 for name,(path,pin) in PINS.items():
  data=(args.root/path).read_bytes()
  actual=blob_sha1(data)
  if actual!=pin: raise SystemExit(f"pin mismatch {name}: {actual}")
  docs[name]=data
 initial_tasks=read_csv(docs["initial_tasks"]); post_tasks=read_csv(docs["post_tasks"])
 initial_classes=read_csv(docs["initial_classes"]); post_classes=read_csv(docs["post_classes"])
 base_cache=read_cache(docs["base_cache"]); merged_cache=read_cache(docs["merged_cache"])
 quarantine=active_quarantine(docs["quarantine"])
 if set(base_cache)&quarantine or set(merged_cache)&quarantine: raise SystemExit("quarantined key in cache")
 i_map={r["key"]:r for r in initial_tasks}; p_map={r["key"]:r for r in post_tasks}
 i_classes=class_map(initial_classes); p_classes=class_map(post_classes)
 removed=set(i_map)-set(p_map); added=set(p_map)-set(i_map)
 if added: raise SystemExit("unexpected new tasks: "+repr(sorted(added)))
 if not removed: raise SystemExit("no candidate task removed")
 new_cache={k:v for k,v in merged_cache.items() if k not in base_cache}
 if {k:v for k,v in base_cache.items() if k in merged_cache}!=base_cache: raise SystemExit("base cache changed")
 if len(new_cache)!=len(removed) or set(new_cache)!=removed: raise SystemExit("cache/task delta mismatch")
 if any(v!=2 for v in new_cache.values()): raise SystemExit("new cache entries are not all LOSS")
 if any(k in base_cache for k in i_map): raise SystemExit("initial tasks overlap base cache")
 initial_merged_overlap=set(i_map)&set(merged_cache)
 if initial_merged_overlap!=removed: raise SystemExit("initial task/merged cache overlap differs from removed set")
 if any(k in merged_cache for k in p_map): raise SystemExit("post tasks overlap merged cache")
 if any(k in quarantine for k in i_map): raise SystemExit("initial task quarantined")
 if any(k in quarantine for k in p_map): raise SystemExit("post task quarantined")
 updates={}
 for k in removed:
  r=i_map[k]; parents=sorted(ast.literal_eval(r["live_parent_keys"]))
  if int(r["live_parents"])!=2 or len(parents)!=2: raise SystemExit("removed task not 2-parent")
  for pk in parents: updates[pk]=updates.get(pk,0)+1
 if set(i_classes)!=set(p_classes): raise SystemExit("class set changed")
 for k,old in i_classes.items():
  new=p_classes[k]; delta=updates.get(k,0)
  if old["status"]!=new["status"]: raise SystemExit("class status changed "+k)
  if int(new["s5_unknown"])!=int(old["s5_unknown"])-delta: raise SystemExit("unknown delta mismatch "+k)
  if int(new["s5_loss"])!=int(old["s5_loss"])+delta: raise SystemExit("loss delta mismatch "+k)
  if int(new["s5_win"])!=int(old["s5_win"]): raise SystemExit("win delta mismatch "+k)
 audit_i=verify_tasks(initial_tasks,i_classes,base_cache,quarantine)
 audit_p=verify_tasks(post_tasks,p_classes,merged_cache,quarantine)
 if audit_i["errors"] or audit_p["errors"]: raise SystemExit("geometry/task audit failed")
 sha={name:hashlib.sha256(docs[name]).hexdigest() for name in sorted(docs)}
 top=post_tasks[0]; top_parents=sorted(ast.literal_eval(top["live_parent_keys"]))
 parent_detail=[{"key":k,"unknown":int(p_classes[k]["s5_unknown"]),"loss":int(p_classes[k]["s5_loss"]),"win":int(p_classes[k]["s5_win"])} for k in top_parents]
 lowcost_eligible=[r for r in post_tasks if int(r["live_parents"])>=2 and int(r["history_max_unknown_budget"])==0 and int(r["historical_observations"])==0]
 lowcost=sorted(lowcost_eligible,key=lambda r:(int(r["truncated_cost_proxy_nodes"]),r["key"]))[:10]
 out={"schema":"n11-s5-candidate-supply-geometry-audit-v1","source_commit":COMMIT,"input_git_blob_sha1":{n:PINS[n][1] for n in sorted(PINS)},"input_sha256":sha,
  "cache":{"base_entries":len(base_cache),"base_verdicts":counts(["WIN" if v==1 else "LOSS" for v in base_cache.values()]),"merged_entries":len(merged_cache),"merged_verdicts":counts(["WIN" if v==1 else "LOSS" for v in merged_cache.values()]),"new_entries":dict(sorted(new_cache.items())),"initial_task_cache_overlap_merged":len(set(i_map)&set(merged_cache)),"initial_task_cache_overlap_base":0,"post_task_cache_overlap_merged":0},
  "quarantine_active_count":len(quarantine),"quarantine_task_overlap":0,"cache_quarantine_overlap":0,
  "initial_class_stats":class_stats(initial_classes),"post_class_stats":class_stats(post_classes),
  "task_delta":{"initial":len(initial_tasks),"post":len(post_tasks),"removed":sorted(removed),"removed_verdicts":{k:("WIN" if v==1 else "LOSS") for k,v in sorted(new_cache.items())},"parent_updates":dict(sorted(updates.items()))},
  "initial_geometry_audit":audit_i,"post_geometry_audit":audit_p,
  "top_postprobe_candidate":{"key":top["key"],"legal":int(top["legal"]),"live_parent_count":int(top["live_parents"]),"live_parent_keys":top_parents,"parent_detail":parent_detail,"history_max_unknown_budget":int(top["history_max_unknown_budget"]),"historical_observations":int(top["historical_observations"]),"bin_sample_size":int(top["bin_sample_size"]),"bin_win_count":int(top["bin_win_count"]),"bin_loss_count":int(top["bin_loss_count"]),"bin_unknown_count":int(top["bin_unknown_count"]),"truncated_cost_proxy_nodes":int(top["truncated_cost_proxy_nodes"]),"two_parent_no_key_history_count":len(lowcost_eligible),"lowest_proxy_two_parent_no_history_top10":[{"key":r["key"],"legal":int(r["legal"]),"proxy":int(r["truncated_cost_proxy_nodes"]),"samples":int(r["bin_sample_size"]),"win":int(r["bin_win_count"]),"loss":int(r["bin_loss_count"]),"unknown":int(r["bin_unknown_count"])} for r in lowcost]},
  "interpretation_guard":["Exact geometry and candidate-ledger consistency only; no new S5 verdict is generated.","Historical legal-band counts and truncated node proxy are not key-specific cost estimates or probabilities.","REFUTED-D10 is not a LOSS proof; standard 11x11 empty board remains UNKNOWN."],
  "all_gates_pass":True}
 args.out.parent.mkdir(parents=True,exist_ok=True)
 args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+chr(10),encoding="utf-8")
 print(json.dumps({"all_gates_pass":True,"initial_tasks":len(initial_tasks),"post_tasks":len(post_tasks),"initial_geometry":audit_i["count"],"post_geometry":audit_p["count"],"cache_entries_base_merged":[len(base_cache),len(merged_cache)],"removed_keys":sorted(removed),"initial_class_stats":out["initial_class_stats"],"post_class_stats":out["post_class_stats"],"top_candidate":out["top_postprobe_candidate"],"legal_distribution":audit_p["legal_distribution"],"parent_distribution":audit_p["live_parent_distribution"],"audit_path":str(args.out)},ensure_ascii=False,indent=2))
if __name__=="__main__": main()

