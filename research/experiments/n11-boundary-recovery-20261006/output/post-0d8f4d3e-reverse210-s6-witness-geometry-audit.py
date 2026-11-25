#!/usr/bin/env python3
"""Verify the committed 210-row reverse S6-to-S5 LOSS delta geometrically."""
from __future__ import annotations
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
sys.path.insert(0, str(EXP / "scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical
from dfpn_edge_classes import d4_canonical_key, legal_after

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()
def read_cache(path: Path, kind: str):
    out = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if kind == "s5":
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
                raise SystemExit(f"invalid s5 exact row {path}:{line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if not safe_canonical(key, 5):
                raise SystemExit(f"unsafe/noncanonical s5 key: {key}")
        else:
            raise AssertionError(kind)
        if key in out and out[key] != verdict:
            raise SystemExit(f"duplicate conflicting s5 key {key} in {path}")
        if key in out:
            raise SystemExit(f"duplicate s5 key {key} in {path}")
        out[key] = verdict
    return out

def main() -> None:
    source_audit = OUT / "post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json"
    delta_path = OUT / "post-0148c177-s6-loss-reverse210-s5-delta.cache"
    base_cache = OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-collection-merged-s5.cache"
    class_key = (10448351135499550722, 0)
    audit_out = OUT / "post-0d8f4d3e-reverse210-s6-witness-geometry-audit.json"
    manifest_out = OUT / "post-0d8f4d3e-reverse210-s6-witness-source-manifest.json"
    if audit_out.exists() or manifest_out.exists():
        raise SystemExit("refusing to overwrite reverse-delta geometry artifacts")
    doc = json.loads(source_audit.read_text(encoding="utf-8"))
    if doc.get("run_status") != "ok" or doc.get("source_hashes_validated") is not True:
        raise SystemExit("saved S6 source audit lacks successful hash validation")
    if doc.get("s6", {}).get("all_s6_exact_rows_geometry_checked") is not True or doc.get("s6", {}).get("exact_conflict_count") != 0:
        raise SystemExit("saved S6 source audit lacks geometry attestation or reports conflicts")
    saved, reports = read_saved_exact_s6(doc)
    if len(reports) != doc.get("source_file_count") or len(saved) != doc["s6"].get("unique_canonical_keys"):
        raise SystemExit("saved S6 source audit did not rehydrate exactly")
    loss_witnesses: dict[tuple[int,int], set[tuple[int,int]]] = defaultdict(set)
    reply27_loss_witnesses: dict[tuple[int,int], set[tuple[int,int]]] = defaultdict(set)
    loss_keys = [key for key, row in saved.items() if row["verdict"] == 2]
    for child in loss_keys:
        child_points = points(child)
        expected_legal = len(legal_after(set(child_points)))
        exact_loss_observations = 0
        for obs in saved[child]["observations"]:
            if obs["legal"] != expected_legal:
                raise SystemExit(f"saved S6 row legal-count mismatch at {child}: {obs}")
            if obs["verdict"] == 2:
                exact_loss_observations += 1
            elif obs["verdict"] not in (0, 1):
                raise SystemExit(f"invalid saved S6 observation verdict at {child}: {obs}")
        if exact_loss_observations == 0:
            raise SystemExit(f"saved S6 LOSS key lacks exact LOSS replay observation: {child}")
        for removed in child_points:
            parent_points = tuple(p for p in child_points if p != removed)
            parent = tuple(d4_canonical_key(parent_points))
            if not safe_canonical(parent, 5):
                raise SystemExit(f"unsafe canonical deletion parent from {child}: {parent}")
            if removed not in legal_after(set(parent_points)):
                raise SystemExit(f"deleted point is not a legal extension: {parent} + {removed}")
            if tuple(d4_canonical_key((*parent_points, removed))) != child:
                raise SystemExit(f"parent/child canonical incidence failure: {parent} -> {child}")
            parent_set = set(points(parent))
            loss_witnesses[parent].add(child)
            if 60 in parent_set and parent_set.intersection({27, 57, 63, 93}):
                reply27_loss_witnesses[parent].add(child)
    delta = read_cache(delta_path, "s5")
    if len(delta) != 210 or set(delta.values()) != {2}:
        raise SystemExit(f"unexpected incoming delta cardinality/verdicts: {len(delta)} {Counter(delta.values())}")
    missing = sorted(k for k in delta if k not in loss_witnesses)
    if missing:
        raise SystemExit(f"incoming LOSS keys lack exact legal S6 LOSS witness: {missing[:10]}")
    current = read_cache(base_cache, "s5")
    conflicts = sorted((k, current[k], value) for k, value in delta.items()
                       if k in current and current[k] != value)
    if conflicts:
        raise SystemExit(f"incoming exact S5 delta conflicts with active cache: {conflicts[:10]}")
    overlap = sorted(k for k in delta if k in current)
    class_audit_path = OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-class-boundary-audit.json"
    class_before = json.loads(class_audit_path.read_text(encoding="utf-8"))
    class_children = {tuple(row["key"]): row.get("verdict") for row in class_before["boundary"]["children"]}
    class_hits = sorted(k for k in delta if k in class_children)
    class_unknown_hits = sorted(k for k in class_hits if class_children[k] is None)
    candidate_missing = sorted(k for k in loss_witnesses if k not in current)
    audit = {
      "schema":"n11-s6-loss-reverse210-s5-geometry-audit-v1",
      "incoming_delta":{"path":relative(delta_path),"sha256":sha(delta_path),"rows":len(delta),"verdicts":{"LOSS":len(delta)}},
      "saved_s6_source_audit":{"path":relative(source_audit),"sha256":sha(source_audit),"source_files_rehydrated":len(reports),"canonical_s6_keys":len(saved),"exact_s6_loss_keys":len(loss_keys),"exact_conflicts":0},
      "geometry":{"every_exact_s6_loss_deletion_parent_enumerated":True,"all_parents_safe_canonical_s5":True,"all_removed_points_legal_extensions":True,"all_reverse_incidence_rechecked":True,"all_loss_parent_candidates":len(loss_witnesses),"reply27_loss_parent_candidates":len(reply27_loss_witnesses),"candidate_s5_without_active_exact_verdict":len(candidate_missing)},
      "delta_coverage":{"incoming_rows_with_exact_s6_loss_witness":len(delta)-len(missing),"missing_witnesses":[],"witnesses":[{"s5_key":list(k),"s6_loss_witnesses":[list(x) for x in sorted(loss_witnesses[k])]} for k in sorted(delta)]},
      "active_cache_comparison":{"path":relative(base_cache),"sha256":sha(base_cache),"rows":len(current),"overlap_same_verdict":len(overlap),"opposite_verdict_conflicts":0},
      "active_class_intersection":{"class_key":list(class_key),"delta_children":len(class_hits),"previously_unknown_children_now_exact_loss":len(class_unknown_hits),"keys":[list(k) for k in class_hits]},
      "claim":"Every incoming s5 LOSS delta row has at least one geometry-checked legal canonical exact S6 LOSS witness from the hash-validated saved corpus. No WIN or UNKNOWN S6 row is propagated."
    }
    audit_out.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    manifest={"schema":"n11-s6-loss-reverse210-source-manifest-v1","sources":[{"path":relative(p),"sha256":sha(p),"bytes":p.stat().st_size} for p in [Path(__file__),source_audit,delta_path,base_cache,class_audit_path]],"saved_s6_source_files":doc.get("sources",[]),"outputs":[{"path":relative(audit_out),"sha256":sha(audit_out),"bytes":audit_out.stat().st_size}],"audit_sha256":sha(audit_out)}
    manifest_out.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"delta_rows":len(delta),"s6_loss_keys":len(loss_keys),"all_loss_parent_candidates":len(loss_witnesses),"reply27_loss_parent_candidates":len(reply27_loss_witnesses),"current_overlap":len(overlap),"conflicts":0,"active_class_loss_hits":len(class_unknown_hits),"audit_sha256":sha(audit_out),"manifest_sha256":sha(manifest_out)},sort_keys=True))
if __name__ == "__main__": main()
