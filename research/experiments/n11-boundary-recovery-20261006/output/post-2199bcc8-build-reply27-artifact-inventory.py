#!/usr/bin/env python3
"""Build and verify the hash inventory for the post-2199bcc8 reply27 checkpoint."""
from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
PREFIX = "post-2199bcc8-"
OUTPUT = OUT / "post-2199bcc8-reply27-checkpoint-artifact-hashes-20261009.json"
SHA_CACHE: dict[Path, tuple[int, int, str]] = {}
SCRIPTS = EXP / "scripts"
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
FRONTIER = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
USED_SCRIPTS = [
    SCRIPTS / "audit_local_s6_boundary_history.py",
    SCRIPTS / "audit_saved_s6_targets.py",
    SCRIPTS / "augment_s6_source_audit_from_manifest.py",
    SCRIPTS / "complete_s5_via_s6_local.py",
    SCRIPTS / "materialize_s6_boundary.py",
    SCRIPTS / "materialize_s6_descent_evidence_v2.py",
    SCRIPTS / "materialize_s7_witness_evidence.py",
    SCRIPTS / "prepare_s7_witness_probe.py",
    SCRIPTS / "run_s7_witness_probe_local.py",
    SCRIPTS / "verify_s7_witness_parent_win_v2.py",
    FRONTIER / "cache_aware_reply27_cardinality.py",
    FRONTIER / "cache_aware_reply27_cover.py",
    FRONTIER / "refine_cache_aware_reply27_cover.py",
    SCRIPTS / "rank_dual_tight_repair_classes.py",
    EDGE / "dfpn_edge_classes.py",
]


def sha(path: Path) -> str:
    path = path.resolve()
    stat = path.stat()
    cached = SHA_CACHE.get(path)
    if cached is not None and cached[:2] == (stat.st_size, stat.st_mtime_ns):
        return cached[2]
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    result = digest.hexdigest()
    SHA_CACHE[path] = (stat.st_size, stat.st_mtime_ns, result)
    return result


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def resolve(raw: str) -> Path:
    candidate = Path(raw.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def read_json(path: Path) -> Any | None:
    try:
        if path.name.lower().endswith(".json.gz"):
            return json.loads(gzip.decompress(path.read_bytes()))
        if path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, gzip.BadGzipFile):
        return None
    return None


def walk(value: Any) -> Iterable[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite inventory: {OUTPUT}")
    selected: set[Path] = set()
    for item in OUT.iterdir():
        if item.resolve() == OUTPUT.resolve():
            continue
        if item.name.startswith(PREFIX):
            if item.is_file():
                selected.add(item.resolve())
            elif item.is_dir():
                selected.update(path.resolve() for path in item.rglob("*") if path.is_file())
    raw_root = OUT / "raw"
    if raw_root.is_dir():
        for directory in raw_root.iterdir():
            if directory.is_dir() and directory.name.startswith(PREFIX):
                selected.update(path.resolve() for path in directory.rglob("*") if path.is_file())
    for path in USED_SCRIPTS:
        if not path.is_file():
            raise SystemExit(f"missing verifier or materializer: {path}")
        selected.add(path.resolve())
    selected.add(Path(__file__).resolve())

    artifacts = [{"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}
                 for path in sorted(selected, key=rel)]
    pair_fields = (
        ("path", "sha256"),
        ("source_path", "source_sha256"),
        ("artifact_path", "sha256"),
        ("source_local_path", "source_local_sha256"),
        ("input_local_path", "input_local_sha256"),
        ("local_path", "local_sha256"),
        ("input_path", "input_sha256"),
        ("raw_output_path", "raw_output_sha256"),
        ("log_path", "log_sha256"),
    )
    manifested: dict[str, dict] = {}
    missing: list[str] = []
    mismatched: list[dict] = []
    for artifact in selected:
        payload = read_json(artifact)
        if payload is None:
            continue
        for item in walk(payload):
            for path_key, hash_key in pair_fields:
                raw_path, expected = item.get(path_key), item.get(hash_key)
                if not isinstance(raw_path, str) or not isinstance(expected, str) or len(expected) != 64:
                    continue
                path = resolve(raw_path)
                if not path.is_file():
                    missing.append(raw_path)
                    continue
                actual = sha(path)
                if actual != expected:
                    mismatched.append({"path": raw_path, "expected": expected, "actual": actual,
                                       "referenced_by": rel(artifact)})
                    continue
                manifested[rel(path)] = {"bytes": path.stat().st_size, "sha256": actual}
    attributes = ROOT / ".gitattributes"
    manifested[rel(attributes)] = {"bytes": attributes.stat().st_size, "sha256": sha(attributes)}
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": sorted(set(missing)), "mismatched": mismatched[:50]}, indent=2))

    base = OUT / "post-2199bcc8-dual-tight-10448351135499552768-0-probe8-sequential-completed-merged-s5.cache"
    merged = OUT / "post-2199bcc8-s5-10448351135499552768-128-s7-witness-merged-s5.cache"
    cardinality = json.loads((OUT / "post-2199bcc8-repair-after-s7-class-win-cardinality.json").read_text(encoding="utf-8"))
    repair = json.loads((OUT / "post-2199bcc8-repair-after-s7-class-win-refined-repair.json").read_text(encoding="utf-8"))
    ranking = json.loads((OUT / "post-2199bcc8-repair-after-s7-class-win-ranking.json").read_text(encoding="utf-8"))
    s5_audit = json.loads((OUT / "post-2199bcc8-s5-10448351135499552768-128-s7-witness-class-boundary-audit.json").read_text(encoding="utf-8"))
    s6_summary = json.loads((OUT / "post-2199bcc8-s5-10448351135499552768-128-s6-descent-summary.json").read_text(encoding="utf-8"))
    s7_summary = json.loads((OUT / "post-2199bcc8-s5-10448351135499552768-128-s7-witness-summary.json").read_text(encoding="utf-8"))
    cache_lines = [line for line in merged.read_text(encoding="utf-8").splitlines()
                   if line and not line.startswith("#")]
    wins = sum(int(line.split(",")[4]) == 1 for line in cache_lines)
    losses = sum(int(line.split(",")[4]) == 2 for line in cache_lines)
    if (len(cache_lines) != 4962 or wins != 126 or losses != 4836
            or cardinality.get("cache_entries") != len(cache_lines)
            or cardinality.get("class_status_counts") != {"LOSS": 29, "UNKNOWN": 3127, "WIN": 228}
            or cardinality.get("secured_vertices") != 113
            or cardinality.get("uncovered_vertices") != 6
            or cardinality.get("minimum_additional_classes") != 3
            or cardinality.get("rational_dual_total") != "3"
            or cardinality.get("dual_certificate_matches_integer_optimum") is not True
            or repair.get("repair_classes") != 3
            or repair.get("refined_unique_unknown_s5") != 292
            or s5_audit.get("s4_class", {}).get("outcome") != "WIN"
            or s5_audit.get("exact_verdict_conflicts") != 0
            or s6_summary.get("new_s6_verdict_counts") != {"WIN": 84, "LOSS": 0, "UNKNOWN": 3}
            or s7_summary.get("s7_verdict_counts") != {"2": 2}
            or s7_summary.get("s5_outcome") != "WIN"):
        raise SystemExit("checkpoint cache or exact-recurrence summaries disagree")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    attributes_path = ROOT / ".gitattributes"
    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v4",
        "created_on": "2026-10-09",
        "main_commit_at_inventory": head,
        "checkpoint": {
            "root": [60, 27],
            "base_s5_cache": {"path": rel(base), "bytes": base.stat().st_size, "sha256": sha(base),
                              "unique_exact_s5": 4961, "win": 125, "loss": 4836, "conflicts": 0},
            "exact_s5_cache": {"path": rel(merged), "bytes": merged.stat().st_size, "sha256": sha(merged),
                               "unique_exact_s5": len(cache_lines), "win": wins, "loss": losses, "conflicts": 0},
            "s4_status": cardinality["class_status_counts"],
            "secured_vertices": cardinality["secured_vertices"],
            "remaining_vertices": cardinality["uncovered_vertices"],
            "minimum_additional_classes": cardinality["minimum_additional_classes"],
            "rational_dual": cardinality["rational_dual_total"],
            "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
            "repair_classes": repair["repair_classes"],
            "repair_unique_unknown_s5": repair["refined_unique_unknown_s5"],
            "processed_s5_parent": s5_audit["s5_parent"]["key"],
            "processed_s5_outcome": s5_audit["s5_parent"]["outcome"],
            "processed_s5_boundary": s5_audit["s5_parent"]["complete_canonical_s6_boundary"],
            "processed_s6_counts": s6_summary["new_s6_verdict_counts"],
            "processed_s6_nodes": s6_summary["nodes"],
            "processed_s7_loss_witnesses": s7_summary["s7_targets"],
            "processed_s7_nodes": s7_summary["nodes"],
            "processed_s4_class": s5_audit["s4_class"]["key"],
            "processed_s4_boundary": s5_audit["s4_class"]["complete_canonical_s5_boundary"],
            "processed_s4_status": s5_audit["s4_class"]["outcome"],
            "next_target": ranking["next_target"],
            "claim": "One s4 class is WIN by one exact s5 WIN child whose complete s6 boundary is all WIN. {60,27} and the 11x11 empty board remain UNKNOWN.",
        },
        "artifacts": artifacts,
        "manifested_sources": [{"path": path, **data} for path, data in sorted(manifested.items())],
        "artifact_count": len(artifacts),
        "source_count": len(manifested),
        "missing_sources": [],
        "mismatched_sources": [],
        "byte_preservation": {"gitattributes_path": rel(attributes_path),
                              "gitattributes_sha256": sha(attributes_path),
                              "output_tree_text_normalization": "disabled for preserved output bytes"},
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"inventory": rel(OUTPUT), "artifacts": len(artifacts),
                      "manifested_sources": len(manifested), "missing_sources": 0,
                      "mismatched_sources": 0, "sha256": sha(OUTPUT),
                      "main_commit_at_inventory": head}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
