#!/usr/bin/env python3
"""Build the hash inventory for the post-38613e2 reply27 checkpoint."""
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
PREFIXES = ("post-5dfabf84-", "post-38613e2-")
OUTPUT = OUT / "post-38613e2-reply27-checkpoint-artifact-hashes-v3-20261009.json"
SHA_CACHE: dict[Path, tuple[int, int, str]] = {}

SCRIPTS = EXP / "scripts"
USED_SCRIPTS = [
    SCRIPTS / "audit_local_s5_s6_against_saved_corpus.py",
    SCRIPTS / "audit_local_s6_boundary_history.py",
    SCRIPTS / "audit_saved_s6_targets.py",
    SCRIPTS / "audit_dual_tight_s4_boundary.py",
    SCRIPTS / "audit_s5_raw_history.py",
    SCRIPTS / "augment_s6_source_audit_from_manifest.py",
    SCRIPTS / "complete_s5_via_s6_local.py",
    SCRIPTS / "materialize_dual_tight_class_unknowns.py",
    SCRIPTS / "materialize_s6_descent_evidence.py",
    SCRIPTS / "prepare_dual_tight_ready_subset_probe.py",
    SCRIPTS / "run_s7_witness_probe_local.py",
    SCRIPTS / "verify_dual_tight_probe_preflight.py",
    SCRIPTS / "verify_dual_tight_s4_win_from_s6.py",
    SCRIPTS / "verify_raw_history_coverage.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
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


def relative_if_inside(path: Path) -> str | None:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None


def walk(value: Any) -> Iterable[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def read_json(path: Path) -> Any | None:
    try:
        if path.name.lower().endswith(".json.gz"):
            return json.loads(gzip.decompress(path.read_bytes()))
        if path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, gzip.BadGzipFile):
        return None
    return None


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite inventory: {OUTPUT}")
    selected: set[Path] = set()
    superseded = [
        OUT / "post-38613e2-reply27-checkpoint-artifact-hashes-20261009.json",
        OUT / "post-38613e2-reply27-checkpoint-artifact-hashes-v2-20261009.json",
    ]
    superseded_resolved = {path.resolve() for path in superseded}
    for item in OUT.iterdir():
        if item.resolve() == OUTPUT.resolve():
            continue
        # This first-pass inventory is retained below as a historical artifact,
        # but its nested source manifest points to the earlier builder bytes.
        # Audit the current source/artifact set directly instead of recursively
        # treating that superseded inventory as a current source manifest.
        if item.resolve() in superseded_resolved:
            continue
        if item.name.startswith(PREFIXES):
            if item.is_file():
                selected.add(item.resolve())
            elif item.is_dir():
                selected.update(path.resolve() for path in item.rglob("*") if path.is_file())
    raw_root = OUT / "raw"
    if raw_root.is_dir():
        for directory in raw_root.iterdir():
            if directory.is_dir() and directory.name.startswith(PREFIXES):
                selected.update(path.resolve() for path in directory.rglob("*") if path.is_file())
    for path in USED_SCRIPTS:
        if not path.is_file():
            raise SystemExit(f"missing verifier/solver script: {path}")
        selected.add(path.resolve())
    selected.add(Path(__file__).resolve())

    artifacts = [{"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}
                 for path in sorted(selected, key=rel)]
    manifested: dict[str, dict] = {}
    missing: list[str] = []
    mismatched: list[dict] = []
    archival_aliases: list[dict] = []
    known_archival_aliases = {
        "research/experiments/n11-boundary-recovery-20261006/scripts/run_s7_witness_probe_local.py":
            "research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-run_s7_witness_probe_local-at-dispatch.py",
    }
    pair_fields = (
        ("path", "sha256"),
        ("source_path", "source_sha256"),
        ("artifact_path", "sha256"),
        ("source_local_path", "source_local_sha256"),
        ("input_local_path", "input_local_sha256"),
    )
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
                    source_rel = relative_if_inside(path)
                    archived_rel = known_archival_aliases.get(source_rel or "")
                    archived = ROOT / archived_rel if archived_rel else None
                    if archived is not None and archived.is_file() and sha(archived) == expected:
                        archival_aliases.append({
                            "declared_source_path": raw_path,
                            "declared_source_sha256": expected,
                            "current_source_sha256": actual,
                            "preserved_dispatch_snapshot": archived_rel,
                            "preserved_dispatch_snapshot_sha256": sha(archived),
                            "referenced_by": rel(artifact),
                            "reason": "the original mutable helper was changed after dispatch; the byte-identical at-dispatch snapshot is preserved and hash-matches the original manifest",
                        })
                        manifested[archived_rel] = {"bytes": archived.stat().st_size, "sha256": expected}
                    else:
                        mismatched.append({"path": raw_path, "expected": expected, "actual": actual,
                                           "referenced_by": rel(artifact)})
                    continue
                manifested[rel(path)] = {"bytes": path.stat().st_size, "sha256": actual}
    attributes = ROOT / ".gitattributes"
    manifested[rel(attributes)] = {"bytes": attributes.stat().st_size, "sha256": sha(attributes)}
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": sorted(set(missing)), "mismatched": mismatched[:30]}, indent=2))

    out = OUT / "post-38613e2-hard-s5-s6-descent-v2-merged-s5.cache"
    receipt = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-merge-receipt.json").read_text(encoding="utf-8"))
    card = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-cardinality.json").read_text(encoding="utf-8"))
    repair = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-repair.json").read_text(encoding="utf-8"))
    rank = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-ranking.json").read_text(encoding="utf-8"))
    descent = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-summary.json").read_text(encoding="utf-8"))
    class_audit = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-class-boundary-audit.json").read_text(encoding="utf-8"))
    target_raw = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-next-target-raw-history-audit.json").read_text(encoding="utf-8"))
    target_s6 = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-next-target-saved-s6-summary.json").read_text(encoding="utf-8"))
    probe = json.loads((OUT / "post-38613e2-hard-s5-s6-descent-v2-probe8-preflight.json").read_text(encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    cache_lines = [line for line in out.read_text(encoding="utf-8").splitlines()
                   if line and not line.startswith("#")]
    cache_wins = sum(int(line.split(",")[4]) == 1 for line in cache_lines)
    cache_losses = sum(int(line.split(",")[4]) == 2 for line in cache_lines)
    if len(cache_lines) != receipt.get("unique_exact_s5") or cache_wins != receipt.get("win") or cache_losses != receipt.get("loss"):
        raise SystemExit("current cache totals disagree with its merge receipt")
    if card.get("cache_entries") != len(cache_lines):
        raise SystemExit("cardinality cache entry count differs from the current merged cache")
    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v3",
        "created_on": "2026-10-09",
        "main_commit_at_inventory": head,
        "checkpoint": {
            "root": [60, 27],
            "exact_s5_cache": {"path": rel(out), "bytes": out.stat().st_size, "sha256": sha(out),
                               "unique_exact_s5": len(cache_lines), "win": cache_wins, "loss": cache_losses,
                               "conflicts": 0},
            "s4_status": card["class_status_counts"],
            "secured_vertices": card["secured_vertices"],
            "remaining_vertices": card["uncovered_vertices"],
            "minimum_additional_classes": card["minimum_additional_classes"],
            "rational_dual": card["rational_dual_total"],
            "dual_tight": card["dual_certificate_matches_integer_optimum"],
            "repair_classes": repair["repair_classes"],
            "repair_additive_unknown_s5": repair["repair_additive_unknown_s5"],
            "repair_unique_unknown_s5": repair["repair_unique_unknown_s5"],
            "processed_s5_parent": descent["parent_s5"],
            "processed_s5_outcome": descent["s5_outcome_from_complete_s6_boundary"],
            "processed_s6_boundary": descent["complete_canonical_s6_boundary"],
            "processed_s6_verdicts": descent["exact_s6_verdict_counts"],
            "processed_nodes": descent["nodes"],
            "processed_s4_class": class_audit["class"]["key"],
            "processed_s4_boundary": class_audit["boundary"]["canonical_children"],
            "processed_s4_status": class_audit["boundary"]["status"],
            "next_target": rank["next_target"],
            "next_target_raw_history": {
                "csv_files_examined": target_raw["csv_files_examined"],
                "prior_exact_keys": len(target_raw.get("prior_exact", {})),
                "same_or_higher_budget_unknown_rows": len(target_raw.get("prior_unknown_same_budget_or_higher", [])),
                "same_or_higher_budget_unknown_keys": len({tuple(row["key"]) for row in target_raw.get("prior_unknown_same_budget_or_higher", [])}),
                "cache_hits": target_raw.get("current_cache", {}).get("target_exact_intersection"),
                "conflicts": len(target_raw.get("exact_verdict_conflicts", [])),
                "dispatch_ready": len(target_raw.get("dispatch_ready_keys", [])),
                "requested_budget": target_raw.get("requested_budget"),
            },
            "next_target_saved_s6": {
                "parents": target_s6.get("targets", {}).get("parent_count"),
                "outcomes": target_s6.get("targets", {}).get("status_counts"),
                "new_exact": target_s6.get("cache_comparison", {}).get("new_exact"),
                "cache_conflicts": len(target_s6.get("cache_comparison", {}).get("opposite_verdict_conflicts", [])),
            },
            "probe_preflight": {
                "targets": probe.get("target_count"),
                "ready": len(probe.get("ready_keys", [])),
                "blocked": len(probe.get("blocked_same_or_higher_budget_unknown_keys", [])),
                "conflicts": probe.get("raw_history", {}).get("conflicts", 0) + probe.get("saved_s6", {}).get("conflicts", 0),
            },
            "claim": "The evidence proves one s4 class WIN from one complete all-WIN s6 boundary; {60,27} and the empty board remain UNKNOWN.",
        },
        "artifacts": artifacts,
        "superseded_intermediate_outputs": [
            {
                "path": rel(superseded[0]),
                "sha256": sha(superseded[0]),
                "reason": "Preserved first inventory pass. It was emitted before the compact summary fields were corrected and records an earlier builder-script hash; its original builder bytes are not in the source set. The current inventory rehashes artifacts and source files directly.",
                "excluded_from_current_artifact_validation": True,
            },
            {
                "path": rel(superseded[1]),
                "sha256": sha(superseded[1]),
                "reason": "Preserved complete v2 hash inventory. Its builder source contained short scripts-path literals that the repository knowledge layout checker interpreted relative to the output directory. The v3 builder uses checker-compatible path construction, and this inventory rehashes the current artifacts and sources directly.",
                "excluded_from_current_artifact_validation": True,
            },
        ],
        "manifested_sources": [{"path": path, **data} for path, data in sorted(manifested.items())],
        "historical_source_aliases": archival_aliases,
        "artifact_count": len(artifacts),
        "source_count": len(manifested),
        "missing_sources": [],
        "mismatched_sources": [],
        "byte_preservation": {"gitattributes_path": rel(attributes), "gitattributes_sha256": sha(attributes),
                              "output_tree_text_normalization": "disabled for preserved output bytes"},
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"artifact_count": len(artifacts), "source_count": len(manifested),
                      "missing": 0, "mismatched": 0, "inventory": rel(OUTPUT),
                      "sha256": sha(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
