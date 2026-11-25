#!/usr/bin/env python3
"""Inventory the 9dcb11b6 reply27 saved-s6 integration checkpoint."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-9dcb11b6-"
OUTPUT = OUT / "post-9dcb11b6-reply27-checkpoint-artifact-hashes-20261009.json"
VERIFIER = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_post9dcb_s6_reverse_integration.py"
SUPERSEDED = [
    "research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-exact-s5.cache",
    "research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-exact-s5-merge-receipt.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def resolve(raw: str) -> Path:
    candidate = Path(raw.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    selected: set[Path] = set()
    for child in OUT.iterdir():
        if child.resolve() == OUTPUT.resolve() or not child.name.startswith(PREFIX):
            continue
        if child.is_file():
            selected.add(child.resolve())
        elif child.is_dir():
            selected.update(path.resolve() for path in child.rglob("*") if path.is_file())
    selected.add(Path(__file__).resolve())
    selected.add(VERIFIER.resolve())

    artifacts = [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(selected, key=rel)
    ]
    sources: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    mismatched: list[dict[str, str]] = []
    for artifact in selected:
        if artifact.suffix.lower() != ".json":
            continue
        try:
            payload = json.loads(artifact.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        for item in walk(payload):
            for path_key, hash_key in (("path", "sha256"), ("source_path", "source_sha256")):
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
                sources[rel(path)] = {"bytes": path.stat().st_size, "sha256": actual}
    attributes = ROOT / ".gitattributes"
    sources[rel(attributes)] = {"bytes": attributes.stat().st_size, "sha256": sha(attributes)}
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": sorted(set(missing)), "mismatched": mismatched[:20]}, indent=2))

    current_cache_path = OUT / "post-9dcb11b6-current-exact-s5-v2.cache"
    merge = json.loads((OUT / "post-9dcb11b6-current-exact-s5-v2-merge-receipt.json").read_text(encoding="utf-8"))
    cardinality = json.loads((OUT / "post-9dcb11b6-current-cardinality.json").read_text(encoding="utf-8"))
    repair = json.loads((OUT / "post-9dcb11b6-current-repair.json").read_text(encoding="utf-8"))
    ranking = json.loads((OUT / "post-9dcb11b6-current-ranking.json").read_text(encoding="utf-8"))
    raw = json.loads((OUT / "post-9dcb11b6-rank1-10448351135499567104-0-raw-history-audit.json").read_text(encoding="utf-8"))
    saved = json.loads((OUT / "post-9dcb11b6-rank1-10448351135499567104-0-saved-s6-summary.json").read_text(encoding="utf-8"))
    integration = json.loads((OUT / "post-9dcb11b6-s6-reverse-integration-audit-v2.json").read_text(encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    superseded = [{"path": path, "sha256": sha(ROOT / path),
                   "reason": "Preserved intermediate: it used the 4,863-row cache rather than the manifest-attested 4,871-row local cache; not used in any current status or target computation."}
                  for path in SUPERSEDED]
    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v1",
        "created_on": "2026-10-09",
        "main_commit_at_inventory": head,
        "checkpoint": {
            "root": [60, 27],
            "exact_s5_cache": {"path": rel(current_cache_path), "bytes": current_cache_path.stat().st_size,
                               "sha256": sha(current_cache_path), **merge},
            "s4_status": cardinality["class_status_counts"],
            "secured_vertices": cardinality["secured_vertices"],
            "remaining_vertices": cardinality["uncovered_vertices"],
            "minimum_additional_classes": cardinality["minimum_additional_classes"],
            "rational_dual": cardinality["rational_dual_total"],
            "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
            "repair_classes": repair["repair_classes"],
            "repair_additive_unknown_s5": repair["repair_additive_unknown_s5"],
            "repair_unique_unknown_s5": repair["repair_unique_unknown_s5"],
            "next_target": ranking["next_target"],
            "target_raw_history": {k: raw[k] for k in ("targets", "csv_files_examined", "prior_exact",
                                                       "same_budget_unknown", "cache_hits", "conflicts",
                                                       "dispatch_ready", "requested_budget") if k in raw},
            "target_saved_s6": {"parents": saved.get("parents"), "outcomes": saved.get("outcomes"),
                                "new_exact": saved.get("new_exact"), "cache_conflicts": saved.get("cache_conflicts")},
            "reverse_s6_integration": integration["reverse_geometry"],
        },
        "superseded_intermediate_outputs": superseded,
        "artifacts": artifacts,
        "manifested_sources": [{"path": path, **metadata} for path, metadata in sorted(sources.items())],
        "source_count": len(sources),
        "missing_sources": [],
        "mismatched_sources": [],
        "byte_preservation": {"gitattributes_path": rel(attributes), "gitattributes_sha256": sha(attributes),
                              "output_tree_text_normalization": "disabled to preserve artifact SHA-256 bytes"},
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"artifact_count": len(artifacts), "source_count": len(sources),
                      "missing": 0, "mismatched": 0, "inventory": rel(OUTPUT), "sha256": sha(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
