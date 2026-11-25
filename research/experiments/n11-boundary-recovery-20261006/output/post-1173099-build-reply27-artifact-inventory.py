#!/usr/bin/env python3
"""Build a hash-checked inventory for the post-1173099 reply27 checkpoint."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
PREFIX = "post-1173099-"
OUTPUT = OUT / "post-1173099-reply27-checkpoint-artifact-hashes-20261009.json"
SHA_CACHE: dict[Path, tuple[int, int, str]] = {}


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


def select_artifacts() -> set[Path]:
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
    selected.add(Path(__file__).resolve())
    for name in (
        "audit_saved_s7_s6_intersection.py",
        "materialize_s6_batch_descent_evidence.py",
        "rank_dual_tight_repair_classes.py",
    ):
        path = EXP / "scripts" / name
        if not path.is_file():
            raise SystemExit(f"missing current evidence helper: {path}")
        selected.add(path.resolve())
    return selected


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite inventory: {OUTPUT}")
    selected = select_artifacts()
    artifacts = [{"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}
                 for path in sorted(selected, key=rel)]

    manifested: dict[str, dict] = {}
    missing: list[str] = []
    mismatched: list[dict] = []
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
                    mismatched.append({"path": raw_path, "expected": expected, "actual": actual,
                                       "referenced_by": rel(artifact)})
                    continue
                manifested[rel(path)] = {"bytes": path.stat().st_size, "sha256": actual}
    attributes = ROOT / ".gitattributes"
    manifested[rel(attributes)] = {"bytes": attributes.stat().st_size, "sha256": sha(attributes)}
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": sorted(set(missing)), "mismatched": mismatched[:30]}, indent=2))

    cache = OUT / "post-1173099-dual-tight-10448351135499552768-0-probe8-merged-s5.cache"
    verdicts: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(cache.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        row = next(csv.reader([line]))
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            raise SystemExit(f"invalid exact s5 cache row {cache}:{line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        previous = verdicts.get(key)
        if previous is not None and previous != verdict:
            raise SystemExit(f"exact s5 cache conflict for {key}: {previous} vs {verdict}")
        verdicts[key] = verdict

    cardinality = json.loads((OUT / "post-1173099-dual-tight-probe8-cardinality.json").read_text(encoding="utf-8"))
    repair = json.loads((OUT / "post-1173099-dual-tight-probe8-repair.json").read_text(encoding="utf-8"))
    rank = json.loads((OUT / "post-1173099-dual-tight-probe8-ranking.json").read_text(encoding="utf-8"))
    probe = json.loads((OUT / "post-1173099-dual-tight-10448351135499552768-0-probe8-summary.json").read_text(encoding="utf-8"))
    class_audit = json.loads((OUT / "post-1173099-dual-tight-10448351135499552768-0-probe8-class-boundary-audit.json").read_text(encoding="utf-8"))
    descent = json.loads((OUT / "post-1173099-dual-tight-10448351135499552768-0-probe8-s6-descent-summary.json").read_text(encoding="utf-8"))
    s7 = json.loads((OUT / "post-1173099-dual-tight-probe8-s6-s7-saved-intersection.json").read_text(encoding="utf-8"))
    if len(verdicts) != 4954 or cardinality.get("cache_entries") != len(verdicts):
        raise SystemExit("exact cache and cardinality totals disagree")
    if cardinality.get("class_status_counts") != {"LOSS": 29, "UNKNOWN": 3129, "WIN": 226}:
        raise SystemExit("unexpected global s4 class status")
    if cardinality.get("secured_vertices") != 113 or cardinality.get("uncovered_vertices") != 6:
        raise SystemExit("unexpected secured/remaining vertex totals")
    if cardinality.get("minimum_additional_classes") != 3 or not cardinality.get("dual_certificate_matches_integer_optimum"):
        raise SystemExit("repair cardinality is not dual-tight")
    if s7.get("saved_exact_s7_key_count") != 0 or s7.get("conflict_count") != 0:
        raise SystemExit("saved-s7 intersection did not remain an empty conflict-free delta")

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    counts = {"WIN": sum(value == 1 for value in verdicts.values()),
              "LOSS": sum(value == 2 for value in verdicts.values())}
    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v1",
        "created_on": "2026-10-09",
        "main_commit_at_inventory": head,
        "checkpoint": {
            "root": [60, 27],
            "exact_s5_cache": {"path": rel(cache), "bytes": cache.stat().st_size, "sha256": sha(cache),
                               "unique_exact_s5": len(verdicts), "win": counts["WIN"],
                               "loss": counts["LOSS"], "conflicts": 0},
            "s4_status": cardinality["class_status_counts"],
            "processed_s4_class": class_audit.get("class", {}).get("key"),
            "processed_s4_boundary": {"canonical_children": class_audit.get("boundary", {}).get("canonical_children"),
                                       "status_counts": class_audit.get("boundary", {}).get("status_counts"),
                                       "status": class_audit.get("boundary", {}).get("status")},
            "processed_s5_probe": probe.get("exact_replay_counts"),
            "processed_s6_boundary": descent.get("complete_canonical_s6_union"),
            "processed_s6_verdicts": descent.get("total_boundary_verdict_counts"),
            "processed_nodes": descent.get("nodes"),
            "saved_s7_intersection": {"s6_unknown": s7.get("s6_unknown_count"),
                                      "canonical_s7_boundary": s7.get("unique_canonical_s7_boundary_count"),
                                      "saved_exact_s7": s7.get("saved_exact_s7_key_count"),
                                      "derived_s6": s7.get("s6_outcomes")},
            "secured_vertices": cardinality["secured_vertices"],
            "remaining_vertices": cardinality["uncovered_vertices"],
            "minimum_additional_classes": cardinality["minimum_additional_classes"],
            "rational_dual": cardinality["rational_dual_total"],
            "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
            "repair_classes": repair["repair_classes"],
            "repair_additive_unknown_s5": repair["repair_additive_unknown_s5"],
            "repair_unique_unknown_s5": repair["repair_unique_unknown_s5"],
            "next_target": rank["next_target"],
            "claim": "Current exact and boundary audit results only; s4 class, {60,27}, and the 11x11 empty board remain UNKNOWN.",
        },
        "artifacts": artifacts,
        "manifested_sources": [{"path": path, **data} for path, data in sorted(manifested.items())],
        "artifact_count": len(artifacts),
        "source_count": len(manifested),
        "missing_sources": [],
        "mismatched_sources": [],
        "byte_preservation": {"gitattributes_path": rel(attributes), "gitattributes_sha256": sha(attributes),
                              "output_tree_text_normalization": "disabled for preserved output bytes"},
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"artifact_count": len(artifacts), "source_count": len(manifested),
                      "missing": 0, "mismatched": 0, "cache": counts,
                      "inventory": rel(OUTPUT), "sha256": sha(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
