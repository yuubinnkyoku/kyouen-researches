#!/usr/bin/env python3
"""Extend the latest committed reply27 inventory with the d01858aa checkpoint."""
from __future__ import annotations

import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PARENT = OUT / "post-2beb63af-reply27-checkpoint-artifact-hashes-20261009.json"
REPORT = OUT / "post-d01858aa-reply27-checkpoint-report.json"
OUTPUT = OUT / "post-d01858aa-reply27-checkpoint-artifact-hashes.json"
PREFIX = "post-d01858aa-"
BASE_MAIN = "d01858aa1a1d5ba5843b7a71c3a1539359de5889"


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
    if not path.is_file():
        raise SystemExit(f"checkpoint artifact/source missing: {path}")
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


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def add_record(table: dict[str, dict[str, Any]], item: dict[str, Any]) -> None:
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"conflicting inventory records for {item['path']}")
    table[item["path"]] = item


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite checkpoint inventory: {OUTPUT}")
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if (report.get("checkpoint_base_main") != BASE_MAIN
            or report.get("exact_s5_cache", {}).get("conflict") != 0
            or report.get("processed_class", {}).get("status") != "WIN"):
        raise SystemExit("checkpoint report does not bind to the fetched main and verified class WIN")

    artifacts: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    for item in parent["artifacts"]:
        add_record(artifacts, item)
    for item in parent["manifested_sources"]:
        add_record(sources, item)
    add_record(artifacts, record(PARENT))

    new_paths: set[Path] = set()
    for path in OUT.glob(f"{PREFIX}*"):
        if path.is_file() and path != OUTPUT:
            new_paths.add(path.resolve())
        elif path.is_dir():
            new_paths.update(item.resolve() for item in path.rglob("*") if item.is_file())
    raw_root = OUT / "raw"
    if raw_root.is_dir():
        for path in raw_root.glob(f"{PREFIX}*"):
            if path.is_file():
                new_paths.add(path.resolve())
            elif path.is_dir():
                new_paths.update(item.resolve() for item in path.rglob("*") if item.is_file())
    for path in sorted(new_paths):
        add_record(artifacts, record(path))

    source_manifest = OUT / "post-d01858aa-reply27-checkpoint-source-manifest.json"
    source_doc = json.loads(source_manifest.read_text(encoding="utf-8"))
    for item in source_doc["sources"]:
        add_record(sources, item)
    for item in source_doc["evidence_manifests"]:
        add_record(sources, item)

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
                raise SystemExit(f"manifested source is missing: {source_path}")
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
        "checkpoint": "post-d01858aa exact S5 WIN, S6 LOSS reverse merge, and reoptimized dual-tight repair",
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
    OUTPUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "out": rel(OUTPUT), "artifact_count": len(artifacts),
        "source_count": len(sources), "missing": 0, "mismatched": 0,
        "main_commit": BASE_MAIN, "sha256": sha(OUTPUT),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
