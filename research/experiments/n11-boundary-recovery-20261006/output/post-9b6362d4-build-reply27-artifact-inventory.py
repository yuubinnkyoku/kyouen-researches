#!/usr/bin/env python3
"""Verify the aa90bb5b evidence and inventory the 9b6362d4 checkpoint."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIXES = ("post-aa90bb5b-", "post-9b6362d4-")
HISTORICAL_COMMIT = "aa90bb5b914ce9901f24663a4a012cd62b1daf9a"
PREVIOUS = OUT / "post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json"
OUTPUT = OUT / "post-9b6362d4-reply27-checkpoint-artifact-hashes-20261008.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
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


def historical_blob(path_text: str) -> bytes | None:
    normalized = path_text.replace("\\", "/")
    if Path(normalized).is_absolute():
        return None
    result = subprocess.run(
        ["git", "show", f"{HISTORICAL_COMMIT}:{normalized}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def main() -> int:
    if not PREVIOUS.is_file():
        raise SystemExit(f"missing previous checkpoint inventory: {PREVIOUS}")
    old = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    old_hash = sha256_file(PREVIOUS)

    selected: set[Path] = set()
    for child in OUT.iterdir():
        if child.resolve() == OUTPUT.resolve():
            continue
        if child.name.startswith(PREFIXES):
            if child.is_file():
                selected.add(child.resolve())
            elif child.is_dir():
                selected.update(path.resolve() for path in child.rglob("*") if path.is_file())
    selected.add(Path(__file__).resolve())

    artifacts = [
        {"path": relative(path), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in sorted(selected, key=relative)
    ]
    current_sources: dict[str, dict[str, Any]] = {}
    historical_sources: dict[tuple[str, str], dict[str, Any]] = {}
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
                if path.is_file():
                    actual = sha256_file(path)
                    if actual == expected:
                        current_sources[relative(path)] = {
                            "bytes": path.stat().st_size,
                            "sha256": actual,
                        }
                        continue
                else:
                    actual = None
                blob = historical_blob(raw_path)
                if blob is not None and sha256_bytes(blob) == expected:
                    key = (raw_path.replace("\\", "/"), expected)
                    record = historical_sources.setdefault(key, {
                        "path": key[0],
                        "sha256": expected,
                        "bytes": len(blob),
                        "verified_from_git_commit": HISTORICAL_COMMIT,
                        "referenced_by": [],
                    })
                    record["referenced_by"].append(relative(artifact))
                    continue
                if actual is None:
                    missing.append({"path": raw_path, "referenced_by": relative(artifact)})
                else:
                    raise SystemExit(
                        f"SHA-256 mismatch for {raw_path} referenced by {relative(artifact)}; "
                        f"working tree {actual}, historical commit does not match"
                    )

    historical = sorted(
        (dict(record, referenced_by=sorted(set(record["referenced_by"])))
         for record in historical_sources.values()),
        key=lambda row: (row["path"], row["sha256"]),
    )
    attributes = ROOT / ".gitattributes"
    current_sources[relative(attributes)] = {
        "bytes": attributes.stat().st_size,
        "sha256": sha256_file(attributes),
    }
    report = {
        "schema": "reply27-checkpoint-artifact-hashes-v2",
        "created_on": "2026-10-08",
        "main_commit_at_inventory": "9b6362d4cc0f115608bc6c5586cfdb5b509ce521",
        "previous_checkpoint_inventory": {
            "path": relative(PREVIOUS),
            "sha256": old_hash,
            "main_commit": old.get("main_commit_at_dispatch"),
        },
        "latest_class": {
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
            "sha256": "0653c02857e30102c18287bfc2c25e864b6e445238e469747b736c3e4a612516",
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
        "new_preflight": {
            "raw_history_budget": 15000000,
            "remaining_target_keys": 79,
            "target_ready_keys": 79,
            "saved_s6_outcomes": {"UNKNOWN": 79},
            "probe_keys": 8,
            "probe_ready_keys": 8,
            "probe_blocked_keys": 0,
            "probe_conflicts": 0,
            "solver_dispatched": False,
        },
        "byte_preservation": {
            "gitattributes_path": relative(attributes),
            "gitattributes_sha256": sha256_file(attributes),
            "output_tree_text_normalization": "disabled to preserve artifact SHA-256 bytes",
        },
        "artifacts": artifacts,
        "manifested_sources": [
            {"path": path, **metadata} for path, metadata in sorted(current_sources.items())
        ],
        "historical_sources_verified_at_aa90bb5b": historical,
        "missing_sources": missing,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "artifacts": len(artifacts),
        "current_sources": len(current_sources),
        "historical_sources": len(historical),
        "missing": len(missing),
        "inventory": relative(OUTPUT),
        "sha256": sha256_file(OUTPUT),
    }, sort_keys=True))
    if missing:
        raise SystemExit("one or more manifest-attested sources are missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
