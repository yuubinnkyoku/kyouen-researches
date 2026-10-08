#!/usr/bin/env python3
"""Hash the aa90bb5b reply27 checkpoint and all manifest-attested sources."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-aa90bb5b-"
OUTPUT = OUT / "post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def resolve(raw: str) -> Path:
    candidate = Path(raw.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def main() -> int:
    selected: set[Path] = set()
    for child in OUT.iterdir():
        if child.name.startswith(PREFIX) and child.resolve() != OUTPUT.resolve():
            if child.is_file():
                selected.add(child.resolve())
            elif child.is_dir():
                selected.update(path.resolve() for path in child.rglob("*") if path.is_file())
    selected.add(Path(__file__).resolve())

    artifacts = [
        {"path": relative(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in sorted(selected, key=relative)
    ]
    sources: dict[str, dict[str, Any]] = {}
    missing: list[dict[str, str]] = []
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
                    missing.append({"path": raw_path, "referenced_by": relative(artifact)})
                    continue
                actual = sha256(path)
                if actual != expected:
                    raise SystemExit(f"SHA-256 mismatch for {raw_path} referenced by {relative(artifact)}")
                sources[relative(path)] = {"bytes": path.stat().st_size, "sha256": actual}

    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v1",
        "created_on": "2026-10-08",
        "main_commit_at_dispatch": "aa90bb5b914ce9901f24663a4a012cd62b1daf9a",
        "completed_s6_win_class": {
            "key": [1297036692682702976, 128],
            "witness_s5": [3602879701896396928, 128],
            "boundary_s6": {"children": 83, "WIN": 83, "LOSS": 0, "UNKNOWN": 0},
        },
        "latest_probed_class": {
            "key": [10448351135499567104, 0],
            "canonical_s5_children": 104,
            "LOSS": 25,
            "WIN": 0,
            "UNKNOWN": 79,
        },
        "exact_s5_cache": {
            "path": "research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-merged-s5.cache",
            "entries": 4871,
            "WIN": 121,
            "LOSS": 4750,
            "conflict": 0,
        },
        "s4_status": {
            "LOSS": 29,
            "WIN": 218,
            "UNKNOWN": 3137,
            "secured_vertices": 113,
            "remaining_vertices": 6,
            "minimum_additional_classes": 3,
            "rational_dual": "3",
            "dual_tight": True,
            "repair_classes": 3,
            "distinct_unknown_s5": 275,
        },
        "artifacts": artifacts,
        "manifested_sources": [
            {"path": path, **metadata} for path, metadata in sorted(sources.items())
        ],
        "missing_manifested_sources": missing,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"artifacts": len(artifacts), "sources": len(sources),
                      "missing": len(missing), "inventory": relative(OUTPUT),
                      "sha256": sha256(OUTPUT)}, sort_keys=True))
    if missing:
        raise SystemExit("one or more manifest-attested sources are missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
