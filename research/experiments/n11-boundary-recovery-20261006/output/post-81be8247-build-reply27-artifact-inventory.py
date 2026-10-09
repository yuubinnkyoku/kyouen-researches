#!/usr/bin/env python3
"""Extend the 049b2284 reply27 inventory with the 81be8247 checkpoint."""
from __future__ import annotations

import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PARENT = OUT / "post-049b2284-reply27-checkpoint-artifact-hashes-20261009.json"
OUTPUT = OUT / "post-81be8247-reply27-checkpoint-artifact-hashes-20261009.json"
PREFIX = "post-81be8247-"
BASE_MAIN = "81be8247e8809fcdbf6aa730adb5d50b2583e9ba"
USED_SOURCES = [
    OUT / "post-81be8247-build-reply27-checkpoint-report.py",
    OUT / "post-81be8247-build-reply27-artifact-inventory.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_adaptive_win_probe.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
    ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
    ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
    ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
    ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
    ROOT / ".local/n11/reply27-probe9/dfpn.exe",
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
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
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"conflicting source/artifact records for {item['path']}")
    table[item["path"]] = item


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
    for item in OUT.glob(f"{PREFIX}*"):
        if item.is_file() and item != OUTPUT:
            new_paths.add(item.resolve())
        elif item.is_dir():
            new_paths.update(path.resolve() for path in item.rglob("*") if path.is_file())
    for path in sorted(new_paths):
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
            elif path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                mismatched.append(item["path"])
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": missing[:20], "mismatched": mismatched[:20]}))

    doc = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-81be8247 dual-tight adaptive probe8 WIN and reoptimized reply27 frontier",
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_inventory": BASE_MAIN,
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
        "main_commit": BASE_MAIN, "sha256": sha(OUTPUT),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
