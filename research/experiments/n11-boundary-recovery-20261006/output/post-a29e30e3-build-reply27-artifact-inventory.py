#!/usr/bin/env python3
"""Build a hash-checked reply27 checkpoint extending the 0d8f4d3e inventory."""
from __future__ import annotations

import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PARENT = OUT / "post-0d8f4d3e-reply27-checkpoint-artifact-hashes.json"
OUTPUT = OUT / "post-a29e30e3-reply27-checkpoint-artifact-hashes-20261009.json"
PREFIX = "post-a29e30e3-"
MAIN_COMMIT = "a29e30e300f0050f0f7c1fe1de465e258483bdce"
USED_SOURCES = [
    ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-a29e30e3-build-reply27-checkpoint-report.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-a29e30e3-adapt-s6-history-preflight.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-a29e30e3-build-win-parent-projection.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_s5_via_s6_local.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/materialize_s6_descent_evidence.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/materialize_s6_descent_evidence_v2.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s6_boundary_history.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win_from_s6.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
    ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
    ROOT / ".local/n11/reply27-probe9/dfpn.exe",
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def resolve(value: str) -> Path:
    path = Path(value.replace("\\", "/"))
    return path if path.is_absolute() else ROOT / path


def record(path: Path) -> dict[str, Any]:
    path = path.resolve()
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


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


def add_record(table: dict[str, dict], item: dict) -> None:
    path = item["path"]
    old = table.get(path)
    if old is not None and old != item:
        raise SystemExit(f"conflicting source/artifact records for {path}")
    table[path] = item


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite checkpoint inventory: {OUTPUT}")
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    artifacts: dict[str, dict] = {}
    sources: dict[str, dict] = {}
    for item in parent["artifacts"]:
        add_record(artifacts, item)
    for item in parent["manifested_sources"]:
        add_record(sources, item)
    add_record(artifacts, record(PARENT))

    new_paths: set[Path] = set()
    for item in OUT.iterdir():
        if item.name.startswith(PREFIX):
            if item.is_file():
                new_paths.add(item.resolve())
            elif item.is_dir():
                new_paths.update(path.resolve() for path in item.rglob("*") if path.is_file())
    raw_root = OUT / "raw"
    if raw_root.is_dir():
        for item in raw_root.iterdir():
            if item.name.startswith(PREFIX):
                new_paths.update(path.resolve() for path in item.rglob("*") if path.is_file())
    for path in sorted(new_paths):
        if not path.is_file():
            raise SystemExit(f"checkpoint artifact missing: {path}")
        add_record(artifacts, record(path))

    for path in USED_SOURCES:
        if not path.is_file():
            raise SystemExit(f"used source missing: {path}")
        add_record(sources, record(path))

    for artifact_path in sorted(new_paths):
        if artifact_path.suffix.lower() not in {".json", ".gz"}:
            continue
        document = read_json(artifact_path)
        if document is None:
            continue
        for item in walk(document):
            source_path = item.get("path") or item.get("artifact_path")
            digest = item.get("sha256")
            if not isinstance(source_path, str) or not isinstance(digest, str):
                continue
            path = resolve(source_path)
            if not path.is_file():
                continue
            source_record = record(path)
            if source_record["sha256"] != digest:
                raise SystemExit(f"manifested source SHA mismatch: {source_record['path']}")
            if isinstance(item.get("bytes"), int) and source_record["bytes"] != item["bytes"]:
                raise SystemExit(f"manifested source byte-count mismatch: {source_record['path']}")
            add_record(sources, source_record)

    missing: list[str] = []
    mismatched: list[str] = []
    for table in (artifacts, sources):
        for item in table.values():
            path = resolve(item["path"])
            if not path.is_file():
                missing.append(item["path"])
                continue
            if path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                mismatched.append(item["path"])
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": missing[:20], "mismatched": mismatched[:20]}))

    doc = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-a29e30e3 complete canonical S6 batch materialization, exact S5 WIN witness, and reoptimized reply27 frontier",
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_inventory": MAIN_COMMIT,
        "parent_inventory": {
            "path": rel(PARENT), "sha256": sha(PARENT),
            "artifact_count": parent["artifact_count"], "source_count": parent["source_count"],
        },
        "artifact_count": len(artifacts),
        "artifacts": [artifacts[key] for key in sorted(artifacts)],
        "source_count": len(sources),
        "manifested_sources": [sources[key] for key in sorted(sources)],
        "missing_sources": missing,
        "mismatched_sources": mismatched,
        "verification": {
            "algorithm": "SHA-256", "checked_artifacts": len(artifacts),
            "checked_sources": len(sources), "missing": 0, "mismatched": 0,
        },
    }
    OUTPUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "out": rel(OUTPUT), "artifact_count": len(artifacts),
        "source_count": len(sources), "missing": 0, "mismatched": 0,
        "main_commit": MAIN_COMMIT, "sha256": sha(OUTPUT),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
