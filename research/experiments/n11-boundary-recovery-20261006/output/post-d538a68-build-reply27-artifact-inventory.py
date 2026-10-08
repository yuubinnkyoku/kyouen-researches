#!/usr/bin/env python3
"""Hash the reply27 proof checkpoint artifacts and every manifested source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIXES = (
    "post-bdbdea7c-rank1-10412322338480586760-0-",
    "post-d9583782-rank1-10448355533546061824-0-",
    "post-d538a68-",
)
OUTPUT = OUT / "post-d538a68-reply27-checkpoint-artifact-hashes-20261008.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
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


def resolve_path(raw: str) -> Path:
    normalized = raw.replace("\\", "/")
    path = Path(normalized)
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    selected: set[Path] = set()
    for child in OUT.iterdir():
        if child.is_file() and child.name.startswith(PREFIXES):
            selected.add(child.resolve())
        elif child.is_dir() and child.name.startswith(PREFIXES):
            selected.update(path.resolve() for path in child.rglob("*") if path.is_file())
    selected.add(Path(__file__).resolve())
    selected.discard(OUTPUT.resolve())

    artifacts = [{"path": rel(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
                 for path in sorted(selected, key=lambda p: rel(p))]
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
                path = resolve_path(raw_path)
                if not path.is_file():
                    missing.append({"path": raw_path, "referenced_by": rel(artifact)})
                    continue
                actual = sha256(path)
                if actual != expected:
                    raise SystemExit(f"SHA-256 mismatch for {raw_path} referenced by {rel(artifact)}")
                sources[rel(path)] = {"bytes": path.stat().st_size, "sha256": actual}

    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v1",
        "created_on": "2026-10-08",
        "main_commit_at_dispatch": "d538a68a85ece7d90b2b677e18447176acad9906",
        "latest_class": {"key": [10448355533546061824, 0], "status": "WIN",
                         "boundary": {"children": 102, "LOSS": 14, "WIN": 1, "UNKNOWN": 87}},
        "next_target": {"key": [10448351135500075008, 0], "canonical_s5_children": 103,
                        "known_loss": 9, "unknown": 94, "dispatch_ready": 93},
        "exact_s5_cache": {"entries": 4816, "WIN": 118, "LOSS": 4698, "conflict": 0,
                            "path": "research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-merged-s5.cache"},
        "s4_status": {"LOSS": 29, "WIN": 211, "UNKNOWN": 3144,
                      "secured_vertices": 113, "remaining_vertices": 6,
                      "minimum_additional_classes": 3, "rational_dual": "3", "dual_tight": True,
                      "repair_classes": 3, "distinct_unknown_s5": 288},
        "artifacts": artifacts,
        "manifested_sources": [{"path": path, **meta} for path, meta in sorted(sources.items())],
        "missing_manifested_sources": missing,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"artifact_count": len(artifacts), "source_count": len(sources),
                      "missing_sources": len(missing), "inventory": rel(OUTPUT),
                      "inventory_sha256": sha256(OUTPUT)}, sort_keys=True))
    if missing:
        raise SystemExit("one or more manifested source files are missing")


if __name__ == "__main__":
    main()
