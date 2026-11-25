#!/usr/bin/env python3
"""Build a fail-closed artifact inventory for the post-11452254 checkpoint."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path.cwd()
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-11452254"
CLASS_PREFIX = PREFIX + "-next-rank1-1585267068834414720-0-"
EXPECTED_MAIN = "11452254b02958ad0cc40925805362d60815f20f"
PARENT_INVENTORY = OUT / "post-9681c588-reply27-checkpoint-artifact-hashes.json"
PARENT_INVENTORY_SHA256 = "41e0e517c388bb24890f77f81a551d3cf2c08afaf2699c70375b6a82780fe2e8"

REPORT = OUT / f"{PREFIX}-reply27-checkpoint-report.json"
SOURCES = OUT / f"{PREFIX}-reply27-checkpoint-source-manifest.json"
INVENTORY = OUT / f"{PREFIX}-reply27-checkpoint-artifact-hashes.json"
S5_SOURCES = OUT / f"{CLASS_PREFIX}sources.json"
S6_SOURCES = OUT / f"{CLASS_PREFIX}s6-descent-sources.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing evidence: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def exact_cache_counts(path: Path) -> Counter:
    counts: Counter = Counter()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) < 5 or fields[0] != "s5verdict":
            raise SystemExit(f"invalid exact S5 cache row in {path}: {line!r}")
        counts[{1: "WIN", 2: "LOSS"}.get(int(fields[4]), "INVALID")] += 1
    return counts


def collect_source_refs(value: object, refs: dict[str, str]) -> None:
    if isinstance(value, dict):
        path, digest = value.get("path"), value.get("sha256")
        if isinstance(path, str) and isinstance(digest, str):
            refs[path] = digest
        artifact_path = value.get("artifact_path")
        if isinstance(artifact_path, str) and isinstance(digest, str):
            refs[artifact_path] = digest
        for key, item in value.items():
            if key.endswith("_path") and isinstance(item, str):
                digest_key = key[:-5] + "_sha256"
                if isinstance(value.get(digest_key), str):
                    refs[item] = value[digest_key]
            collect_source_refs(item, refs)
    elif isinstance(value, list):
        for item in value:
            collect_source_refs(item, refs)


head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
if head != EXPECTED_MAIN:
    raise SystemExit(f"main moved: expected {EXPECTED_MAIN}, found {head}")
if sha256(PARENT_INVENTORY) != PARENT_INVENTORY_SHA256:
    raise SystemExit("parent checkpoint inventory hash mismatch")

base_cache = OUT / "post-9681c588-next98-round4-merged-s5.cache"
merged_cache = OUT / f"{CLASS_PREFIX}merged-s5.cache"
delta_cache = OUT / f"{CLASS_PREFIX}new-exact-s5.cache"
probe = load(OUT / f"{CLASS_PREFIX}summary.json")
merge = load(OUT / f"{CLASS_PREFIX}merge-receipt.json")
boundary = load(OUT / f"{CLASS_PREFIX}post-probe-class-boundary-audit.json")
s6 = load(OUT / f"{CLASS_PREFIX}s6-descent-summary.json")
cardinality = load(OUT / f"{PREFIX}-after-probe-cardinality.json")
repair = load(OUT / f"{PREFIX}-after-probe-repair.json")
ranking = load(OUT / f"{PREFIX}-after-probe-ranking.json")

probe_counts = probe["exact_replay_counts"]
boundary_counts = boundary["boundary"]["status_counts"]
s6_counts = s6["total_boundary_verdict_counts"]
base_counts, merged_counts, delta_counts = (
    exact_cache_counts(base_cache),
    exact_cache_counts(merged_cache),
    exact_cache_counts(delta_cache),
)
normalize = lambda counts: {"LOSS": counts["LOSS"], "WIN": counts["WIN"]}
expected = {
    "probe": {"LOSS": 7, "UNKNOWN": 1, "WIN": 0},
    "s4_boundary": {"LOSS": 12, "UNKNOWN": 92, "WIN": 0},
    "s6_boundary": {"LOSS": 0, "UNKNOWN": 3, "WIN": 82},
    "base_s5": {"LOSS": 5322, "WIN": 145},
    "delta_s5": {"LOSS": 7, "WIN": 0},
    "merged_s5": {"LOSS": 5329, "WIN": 145},
}
actual = {
    "probe": probe_counts,
    "s4_boundary": boundary_counts,
    "s6_boundary": s6_counts,
    "base_s5": normalize(base_counts),
    "delta_s5": normalize(delta_counts),
    "merged_s5": normalize(merged_counts),
}
if actual != expected:
    raise SystemExit(f"checkpoint verdict counts differ: {actual}")
if boundary["boundary"]["canonical_children"] != 104 or boundary["cache"]["conflicts"] != 0:
    raise SystemExit("S4 geometry boundary cardinality/conflict audit failed")
if probe["class_status_from_exact_witness"] != "UNKNOWN":
    raise SystemExit("probe summary has an unexpected class outcome")
if s6["complete_canonical_s6_union"] != 85 or s6["s5_parent_outcomes"] != {"LOSS": 0, "UNKNOWN": 1, "WIN": 0}:
    raise SystemExit("S6 boundary or S5 propagation audit failed")
if s6["reverse_propagated_s5_loss"] != 0 or s6["conflicts"] != 0:
    raise SystemExit("unexpected S6 reverse-loss propagation or cache conflict")
if merge["conflicts"] != 0 or merge["merged_cache"]["rows"] != 5474:
    raise SystemExit("S5 merge receipt mismatch")
if cardinality["secured_vertices"] != 114 or cardinality["uncovered_vertices"] != 5:
    raise SystemExit("cardinality checkpoint mismatch")
if cardinality["minimum_additional_classes"] != 2 or not cardinality["dual_certificate_matches_integer_optimum"]:
    raise SystemExit("integer cover and rational dual are not tight")
if repair["additive_optimum"]["unique_unknown_s5"] != 189:
    raise SystemExit("repair union cardinality mismatch")

sources: dict[str, str] = {}
for path in (S5_SOURCES, S6_SOURCES):
    collect_source_refs(load(path), sources)
verified_sources = []
for relative, expected_hash in sorted(sources.items()):
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"manifested source is missing: {relative}")
    actual_hash = sha256(path)
    if actual_hash != expected_hash:
        raise SystemExit(f"manifested source hash mismatch: {relative}")
    verified_sources.append(
        {"path": relative, "bytes": path.stat().st_size, "sha256": actual_hash}
    )

source_manifest = {
    "schema": "n11-reply27-checkpoint-source-manifest-v1",
    "dispatch_main_commit": EXPECTED_MAIN,
    "root": [60, 27],
    "s5_probe_source_manifest": {
        "path": S5_SOURCES.relative_to(ROOT).as_posix(),
        "sha256": sha256(S5_SOURCES),
    },
    "s6_descent_source_manifest": {
        "path": S6_SOURCES.relative_to(ROOT).as_posix(),
        "sha256": sha256(S6_SOURCES),
    },
    "parent_checkpoint_inventory": {
        "path": PARENT_INVENTORY.relative_to(ROOT).as_posix(),
        "sha256": PARENT_INVENTORY_SHA256,
    },
    "referenced_source_count": len(verified_sources),
    "missing_sources": 0,
    "sha256_mismatches": 0,
    "sources": verified_sources,
}

report = {
    "schema": "n11-reply27-finite-checkpoint-v1",
    "checkpoint_base_main": EXPECTED_MAIN,
    "root": [60, 27],
    "claim": "The processed S4 class remains UNKNOWN; {60,27} and the 11x11 empty board remain UNKNOWN.",
    "processed_class": {
        "key": [1585267068834414720, 0],
        "canonical_s5_children": 104,
        "coverage_vertices": [38, 77, 87],
        "status": "UNKNOWN",
        "exact_s5_boundary": boundary_counts,
        "geometry_audit": boundary["schema"],
    },
    "s5_probe": {
        "scheduled": probe["scheduled_targets"],
        "completed": probe["completed_targets"],
        "budget_per_target": probe["budget_per_target"],
        "verdicts": probe_counts,
        "nodes_all_rows": probe["nodes_all_completed_rows"],
        "nodes_exact": probe["nodes_exact"],
    },
    "s6_descent": {
        "parent_s5": [1585267068834414720, 64],
        "canonical_s6_children": s6["complete_canonical_s6_union"],
        "saved_boundary": s6["saved_s6_boundary_counts"],
        "total_boundary_verdicts": s6_counts,
        "new_exact_s6": s6["new_s6_verdict_counts"],
        "budget_per_target": s6["budget_per_target"],
        "nodes": s6["nodes"],
        "s5_parent_outcome": s6["s5_parent_outcomes"],
        "reverse_propagated_s5_loss": 0,
    },
    "exact_s5_cache": {
        "path": merged_cache.relative_to(ROOT).as_posix(),
        "entries": 5474,
        "WIN": 145,
        "LOSS": 5329,
        "conflict": 0,
        "sha256": sha256(merged_cache),
    },
    "s4_classes": cardinality["class_status_counts"],
    "secured_third_moves": cardinality["secured_vertices"],
    "remaining_third_moves": cardinality["uncovered_vertices"],
    "minimum_additional_classes": cardinality["minimum_additional_classes"],
    "rational_dual": cardinality["rational_dual_total"],
    "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
    "repair": {
        "classes": repair["additive_optimum"]["repair_classes"],
        "distinct_unknown_s5": repair["additive_optimum"]["unique_unknown_s5"],
        "selected": repair["additive_optimum"]["selected"],
    },
    "next_target": ranking["best_target"],
    "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
    "source_manifest": SOURCES.relative_to(ROOT).as_posix(),
    "artifact_inventory": INVENTORY.relative_to(ROOT).as_posix(),
}

write_json(REPORT, report)
write_json(SOURCES, source_manifest)

artifacts = []
for path in sorted(OUT.rglob(f"{PREFIX}*")):
    if not path.is_file() or path == INVENTORY:
        continue
    artifacts.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    )
inventory = {
    "schema": "n11-reply27-checkpoint-artifact-hashes-v1",
    "checkpoint_base_main": EXPECTED_MAIN,
    "artifact_count": len(artifacts),
    "total_bytes": sum(item["bytes"] for item in artifacts),
    "source_manifest": SOURCES.relative_to(ROOT).as_posix(),
    "source_manifest_sha256": sha256(SOURCES),
    "parent_inventory": PARENT_INVENTORY.relative_to(ROOT).as_posix(),
    "parent_inventory_sha256": PARENT_INVENTORY_SHA256,
    "missing_sources": 0,
    "source_sha256_mismatches": 0,
    "artifacts": artifacts,
}
write_json(INVENTORY, inventory)
print(json.dumps({
    "report": REPORT.relative_to(ROOT).as_posix(),
    "source_manifest": SOURCES.relative_to(ROOT).as_posix(),
    "source_count": len(verified_sources),
    "artifact_inventory": INVENTORY.relative_to(ROOT).as_posix(),
    "artifact_count": len(artifacts),
    "inventory_sha256": sha256(INVENTORY),
}, indent=2))
