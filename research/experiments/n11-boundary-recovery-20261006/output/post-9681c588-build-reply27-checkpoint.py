#!/usr/bin/env python3
"""Build the hash-bound post-9681c588 reply27 checkpoint."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-9681c588-"
BASE_MAIN = "9681c58886aa1e680d4cba1116187b2715df6107"
CLASS = (1152921504741065728, 68719476736)
REPORT = OUT / f"{PREFIX}reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / f"{PREFIX}reply27-checkpoint-source-manifest.json"
INVENTORY = OUT / f"{PREFIX}reply27-checkpoint-artifact-hashes.json"
PARENT_INVENTORY = OUT / "post-2f23fcb8-reply27-checkpoint-artifact-hashes.json"
PARENT_MANIFEST = OUT / "post-2f23fcb8-reply27-checkpoint-source-manifest.json"
BASE_CACHE = OUT / "post-2f23fcb8-next98-after-s6-reverse-merged-s5.cache"
ROUND3_CACHE = OUT / f"{PREFIX}next98-round3-merged-s5.cache"
ROUND4_CACHE = OUT / f"{PREFIX}next98-round4-merged-s5.cache"
ROUND3_DELTA = OUT / f"{PREFIX}next98-round3-exact-s5.cache"
ROUND4_DELTA = OUT / f"{PREFIX}next98-round4-exact-s5.cache"
ROUND3_BOUNDARY = OUT / f"{PREFIX}next98-round3-class-boundary-audit.json"
ROUND4_BOUNDARY = OUT / f"{PREFIX}next98-round4-class-boundary-audit-reverified.json"
WIN_AUDIT = OUT / f"{PREFIX}next98-round4-win-witness-geometry-audit.json"
CARDINALITY = OUT / f"{PREFIX}after-round4-cardinality.json"
REPAIR = OUT / f"{PREFIX}after-round4-repair.json"
RANKING = OUT / f"{PREFIX}after-round4-ranking.json"
ROUND3_SUMMARY = OUT / f"{PREFIX}next98-round3-summary.json"
ROUND4_SUMMARY = OUT / f"{PREFIX}next98-round4-collected-summary.json"
ROUND4_PREFLIGHT = OUT / f"{PREFIX}next98-round4-strict-preflight.json"

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rel(path: Path) -> str:
    try: return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError: return str(path.resolve())

def resolve(value: str) -> Path:
    p = Path(value.replace("\\", "/"))
    return p if p.is_absolute() else ROOT / p

def record(path: Path) -> dict[str, Any]:
    p = path.resolve()
    if not p.is_file(): raise SystemExit(f"missing source/artifact: {p}")
    return {"path": rel(p), "bytes": p.stat().st_size, "sha256": sha(p)}

def add(table: dict[str, dict[str, Any]], item: dict[str, Any]) -> None:
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"conflicting hash records for {item['path']}")
    table[item["path"]] = item

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from walk(child)
    elif isinstance(value, list):
        for child in value: yield from walk(child)

def read_cache(path: Path) -> dict[tuple[int,int],int]:
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for n,row in enumerate(csv.reader(f),1):
            if not row or row[0].lstrip().startswith("#"): continue
            if len(row)!=6 or row[0]!="s5verdict" or int(row[3])!=5:
                raise SystemExit(f"invalid cache row {path}:{n}: {row}")
            key,verdict=(int(row[1]),int(row[2])),int(row[4])
            if verdict not in (1,2) or key in result:
                raise SystemExit(f"non-exact/duplicate cache key {path}:{n}: {key}")
            result[key]=verdict
    return result

def verify_hash(item: dict[str, Any]) -> None:
    p=resolve(item["path"])
    if (not p.is_file() or p.stat().st_size!=item["bytes"] or sha(p)!=item["sha256"]):
        raise SystemExit(f"source hash/size mismatch: {item['path']}")

for p in (PARENT_INVENTORY,PARENT_MANIFEST,BASE_CACHE,ROUND3_CACHE,ROUND4_CACHE,
          ROUND3_DELTA,ROUND4_DELTA,ROUND3_BOUNDARY,ROUND4_BOUNDARY,WIN_AUDIT,
          CARDINALITY,REPAIR,RANKING,ROUND3_SUMMARY,ROUND4_SUMMARY,ROUND4_PREFLIGHT):
    if not p.is_file(): raise SystemExit(f"required evidence missing: {p}")
if any(p.exists() for p in (REPORT,SOURCE_MANIFEST,INVENTORY)):
    raise SystemExit("checkpoint report/manifest/inventory already exists; refusing overwrite")

parent_inv=read_json(PARENT_INVENTORY)
parent_manifest=read_json(PARENT_MANIFEST)
for item in parent_inv["artifacts"] + parent_inv["manifested_sources"]:
    verify_hash(item)
if sha(PARENT_INVENTORY)!=parent_inv.get("inventory_sha256",sha(PARENT_INVENTORY)):
    raise SystemExit("parent inventory hash self-check failed")

base=read_cache(BASE_CACHE)
r3=read_cache(ROUND3_CACHE)
r4=read_cache(ROUND4_CACHE)
d3=read_cache(ROUND3_DELTA)
d4=read_cache(ROUND4_DELTA)
assert len(base)==5452 and Counter(base.values())==Counter({1:144,2:5308})
assert len(d3)==8 and set(d3.values())=={2}
assert len(r3)==5460 and all(r3.get(k)==v for k,v in base.items())
assert len(d4)==7 and Counter(d4.values())==Counter({1:1,2:6})
assert len(r4)==5467 and all(r4.get(k)==v for k,v in r3.items())
assert all(r4.get(k)==v for k,v in d4.items())
assert len(set(d3)&set(base))==0 and len(set(d4)&set(r3))==0
cache_counts=Counter(r4.values())
assert cache_counts==Counter({1:145,2:5322})

b3=read_json(ROUND3_BOUNDARY)
b4=read_json(ROUND4_BOUNDARY)
win=read_json(WIN_AUDIT)
card=read_json(CARDINALITY)
repair=read_json(REPAIR)
rank=read_json(RANKING)
s3=read_json(ROUND3_SUMMARY)
s4=read_json(ROUND4_SUMMARY)
pre=read_json(ROUND4_PREFLIGHT)
assert tuple(b3["class"]["key"])==CLASS and b3["boundary"]["status_counts"]=={"LOSS":39,"UNKNOWN":63,"WIN":0}
assert tuple(b4["class"]["key"])==CLASS and b4["boundary"]["status_counts"]=={"LOSS":45,"UNKNOWN":56,"WIN":1}
assert win["s4_class"]["status"]=="WIN" and win["complete_canonical_s5_boundary"]["children"]==102
w=win["s5_win_witnesses"]
assert len(w)==1 and w[0]["safe_canonical"] and w[0]["legal_s4_parent_incidence"] and w[0]["exact_cache_verdict"]=="WIN"
new_wins=[x for x in win["reply27_parent_class_impacts_from_witness"] if x.get("reachable_from_reply27") and x.get("status_before_probe")=="UNKNOWN" and x.get("status_after_probe")=="WIN"]
assert len(new_wins)==2 and CLASS in [tuple(x["key"]) for x in new_wins]
assert card["cache_entries"]==5467 and card["class_status_counts"]=={"LOSS":30,"UNKNOWN":3101,"WIN":253}
assert card["secured_vertices"]==114 and card["uncovered_vertices"]==5
assert card["minimum_additional_classes"]==2 and card["rational_dual_total"]=="2" and card["dual_certificate_matches_integer_optimum"]
assert repair["additive_optimum"]["repair_classes"]==2 and repair["additive_optimum"]["unique_unknown_s5"]==196
next_target=rank["ranking"][0]
assert tuple(next_target["key"])==(1585267068834414720,0) and next_target["unknown_s5"]==99
assert s3["verdict_counts"]=={"LOSS":8,"UNKNOWN":0,"WIN":0} and s3["nodes_all_completed_rows"]==41232972
assert s4["verdict_counts"]=={"LOSS":6,"UNKNOWN":1,"WIN":1}
assert s4["nodes_exact"]==45466997 and s4["nodes_all_completed_rows"]==60466997
assert pre["saved_s6"]["unknown_parents"]==8 and pre["saved_s6"]["conflicts"]==0
assert pre["raw_history"]["conflicts"]==0 and pre["raw_history"]["same_or_higher_budget_unknown_rows"]==0
unknown_key=tuple(s4["unknown_keys"][0])
assert unknown_key not in r4

report_doc={
 "schema":"n11-reply27-finite-checkpoint-v1",
 "checkpoint_base_main":BASE_MAIN,
 "created_on":datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "root":[60,27],
 "processed_class":{
  "key":list(CLASS),"status":"WIN","geometry_audit_passed":True,"canonical_s5_children":102,
  "boundary_status_counts":{"LOSS":45,"WIN":1,"UNKNOWN":56},"coverage_vertices":[0,10,100,108],
  "s5_win_witness":w[0]["key"],"unexplored_unknown_s5":56,
  "related_reply27_class_also_proved_win":[x["key"] for x in new_wins if tuple(x["key"])!=CLASS]
 },
 "exact_s5_cache":{"path":rel(ROUND4_CACHE),"entries":len(r4),"WIN":cache_counts[1],"LOSS":cache_counts[2],
  "conflict":0,"new_exact_rows_from_main_base":len(r4)-len(base),"sha256":sha(ROUND4_CACHE)},
 "s5_probe":{
  "budget_per_target":15000000,"scheduled_round3":8,"round3_exact_loss":8,"round3_nodes":41232972,
  "scheduled_round4":8,"round4_exact_rows":7,"round4_exact_win":1,"round4_exact_loss":6,
  "round4_unknown_rows":1,"round4_unknown_key":list(unknown_key),
  "round4_exact_nodes":45466997,"round4_all_completed_nodes":60466997,
  "unknown_not_merged_or_retried":True,"summary_paths":[rel(ROUND3_SUMMARY),rel(ROUND4_SUMMARY)]
 },
 "s6_descent":{"new_exact_s6_rows":0,"nodes":0,"derived_s5_parent_loss_rows":0,
  "round4_saved_s6_parents":pre["saved_s6"]["parents"],
  "round4_saved_s6_unknown_parents":pre["saved_s6"]["unknown_parents"],
  "conflicts":pre["saved_s6"]["conflicts"],"unknowns_propagated":False},
 "s6_reverse_propagation":{"new_exact_s6_loss_witnesses":0,"reverse_propagated_s5_loss_rows":0,"verdict_conflicts":0},
 "s4_classes":card["class_status_counts"],
 "secured_third_moves":card["secured_vertices"],"remaining_third_moves":card["uncovered_vertices"],
 "minimum_additional_classes":card["minimum_additional_classes"],"rational_dual":card["rational_dual_total"],
 "dual_tight":card["dual_certificate_matches_integer_optimum"],
 "repair":{"classes":repair["additive_optimum"]["repair_classes"],
  "distinct_unknown_s5":repair["additive_optimum"]["unique_unknown_s5"],
  "selected":repair["additive_optimum"]["selected"]},
 "next_target":next_target,
 "proof_status":{"reply27_root":"UNKNOWN","empty_11x11":"UNKNOWN"},
 "claim":"An exact s5 WIN witness proves this s4 class WIN. The checkpoint advances local class evidence only; it does not classify the root {60,27} or the 11x11 empty board.",
 "source_manifest":rel(SOURCE_MANIFEST),"artifact_inventory":rel(INVENTORY)
}
REPORT.write_text(json.dumps(report_doc,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")

sources={}
for item in parent_manifest["sources"]:
 verify_hash(item); add(sources,item)
add(sources,record(PARENT_INVENTORY))
add(sources,record(PARENT_MANIFEST))
# Bind every new checkpoint output and every source path/hash embedded in its audit JSONs.
current_paths=sorted({p.resolve() for candidate in OUT.glob(f"{PREFIX}*")
                      for p in ([candidate] if candidate.is_file() else candidate.rglob("*"))
                      if p.is_file() and p.resolve()!=INVENTORY.resolve() and p.resolve()!=SOURCE_MANIFEST.resolve()})
for p in current_paths:
 item=record(p); add(sources,item)
 if p.suffix.lower()!=".json": continue
 try: doc=read_json(p)
 except (UnicodeDecodeError,json.JSONDecodeError): continue
 for ref in walk(doc):
  path,digest=ref.get("path"),ref.get("sha256")
  if not isinstance(path,str) or not isinstance(digest,str): continue
  rp=resolve(path)
  rec=record(rp)
  if rec["sha256"]!=digest or (isinstance(ref.get("bytes"),int) and ref["bytes"]!=rec["bytes"]):
   raise SystemExit(f"embedded source hash/size mismatch: {rec['path']}")
  add(sources,rec)
for item in sources.values(): verify_hash(item)

source_doc={
 "schema":"n11-reply27-checkpoint-source-manifest-v1",
 "checkpoint_base_main":BASE_MAIN,
 "parent_source_manifest":{"path":rel(PARENT_MANIFEST),"sha256":sha(PARENT_MANIFEST),"source_count":len(parent_manifest["sources"])},
 "report":record(REPORT),
 "artifact_inventory":rel(INVENTORY),
 "source_count":len(sources),
 "sources":[sources[k] for k in sorted(sources)],
 "claim":"SHA-256 binds the parent checkpoint, all round-3/round-4 raw solver inputs and outputs, exact caches and receipts, complete S4 geometry audits, saved-S6 preflight, and recomputed global cover/repair/ranking. .local source files were copied byte-for-byte and retained."
}
SOURCE_MANIFEST.write_text(json.dumps(source_doc,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")

artifacts=[]
for p in sorted({p.resolve() for candidate in OUT.glob(f"{PREFIX}*")
                 for p in ([candidate] if candidate.is_file() else candidate.rglob("*"))
                 if p.is_file() and p.resolve()!=INVENTORY.resolve()}):
 artifacts.append(record(p))
parent_item={"path":rel(PARENT_INVENTORY),"bytes":PARENT_INVENTORY.stat().st_size,"sha256":sha(PARENT_INVENTORY),
             "artifact_count":parent_inv["artifact_count"],"source_count":parent_inv["source_count"]}
inventory_doc={
 "schema":"n11-reply27-checkpoint-artifact-inventory-v1",
 "checkpoint":"post-9681c588 round-3/round-4 dual-tight WIN checkpoint",
 "created_on":datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "main_commit_at_inventory":BASE_MAIN,
 "parent_inventory":parent_item,
 "artifact_count":len(artifacts),"artifacts":artifacts,
 "source_count":len(sources),"manifested_sources":[sources[k] for k in sorted(sources)],
 "missing_sources":[],"mismatched_sources":[],
 "verification":{"algorithm":"SHA-256","checked_artifacts":len(artifacts),"checked_sources":len(sources),"missing":0,"mismatched":0}
}
INVENTORY.write_text(json.dumps(inventory_doc,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
# Reopen and independently check all newly listed artifact and source records.
saved=read_json(INVENTORY)
for item in saved["artifacts"]+saved["manifested_sources"]: verify_hash(item)
print(json.dumps({"report":rel(REPORT),"source_manifest":rel(SOURCE_MANIFEST),
 "inventory":rel(INVENTORY),"inventory_sha256":sha(INVENTORY),"artifacts":len(artifacts),
 "sources":len(sources),"cache_entries":len(r4),"cache_WIN":cache_counts[1],
 "cache_LOSS":cache_counts[2],"class_statuses":card["class_status_counts"],
 "secured":card["secured_vertices"],"remaining":card["uncovered_vertices"],
 "minimum_classes":card["minimum_additional_classes"],"dual":card["rational_dual_total"],
 "dual_tight":card["dual_certificate_matches_integer_optimum"],"missing":0,"mismatched":0},indent=2))
