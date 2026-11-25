#!/usr/bin/env python3
"""Copy preserved .local runner inputs/logs into the checkpoint experiment."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path.cwd()
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-11452254"
CLASS = PREFIX + "-next-rank1-1585267068834414720-0-"
MAIN = "11452254b02958ad0cc40925805362d60815f20f"
OLD_SOURCES = OUT / f"{PREFIX}-reply27-checkpoint-source-manifest.json"
OLD_INVENTORY = OUT / f"{PREFIX}-reply27-checkpoint-artifact-hashes.json"
OLD_INVENTORY_SHA256 = "f828692722691d140e0ac55af57603395e8b9ecb672bdd42f509f79b026141ec"

RAW_MANIFEST = OUT / f"{PREFIX}-raw-input-preservation-manifest.json"
REPORT_V2 = OUT / f"{PREFIX}-reply27-checkpoint-report-v2.json"
SOURCES_V2 = OUT / f"{PREFIX}-reply27-checkpoint-source-manifest-v2.json"
INVENTORY_V2 = OUT / f"{PREFIX}-reply27-checkpoint-artifact-hashes-v2.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_new(path: Path, data: object) -> None:
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing evidence: {path}")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() != MAIN:
    raise SystemExit("main moved since the checkpoint dispatch")
if digest(OLD_INVENTORY) != OLD_INVENTORY_SHA256:
    raise SystemExit("the existing checkpoint inventory has changed")
for path in (RAW_MANIFEST, REPORT_V2, SOURCES_V2, INVENTORY_V2):
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing evidence: {path}")

s5_sources = load(OUT / f"{CLASS}sources.json")
s6_sources = load(OUT / f"{CLASS}s6-descent-sources.json")
copies: list[dict] = []

for row in s5_sources["per_target"]:
    archive_path = ROOT / row["archived_raw_copy"]
    for kind in ("input", "log"):
        original = row[kind]
        copies.append({
            "role": f"s5_{kind}",
            "original_path": original["path"],
            "original_sha256": original["sha256"],
            "archive_path": archive_path.parent.joinpath(Path(original["path"]).name).relative_to(ROOT).as_posix(),
        })

for row in s6_sources["raw_sources"]:
    archive_path = ROOT / row["artifact_path"]
    for kind in ("input", "log"):
        source_key = f"{kind}_local_path"
        hash_key = f"{kind}_local_sha256"
        copies.append({
            "role": f"s6_{kind}",
            "original_path": row[source_key],
            "original_sha256": row[hash_key],
            "archive_path": archive_path.parent.joinpath(Path(row[source_key]).name).relative_to(ROOT).as_posix(),
        })

if len(copies) != 184:
    raise SystemExit(f"expected 184 input/log copies, found {len(copies)}")

# Validate every source and destination before writing the first copy.
for row in copies:
    source = ROOT / row["original_path"]
    destination = ROOT / row["archive_path"]
    if not source.is_file():
        raise SystemExit(f"missing preserved source: {row['original_path']}")
    if digest(source) != row["original_sha256"]:
        raise SystemExit(f"source hash mismatch: {row['original_path']}")
    if destination.exists():
        raise SystemExit(f"refusing to overwrite raw artifact: {row['archive_path']}")

archived = []
for row in copies:
    source = ROOT / row["original_path"]
    destination = ROOT / row["archive_path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    actual_hash = digest(destination)
    if actual_hash != row["original_sha256"]:
        raise SystemExit(f"byte-copy verification failed: {row['archive_path']}")
    archived.append({
        **row,
        "bytes": destination.stat().st_size,
        "sha256": actual_hash,
    })

raw_manifest = {
    "schema": "n11-reply27-raw-input-preservation-v1",
    "checkpoint_base_main": MAIN,
    "root": [60, 27],
    "source_files": len(archived),
    "s5_targets": 8,
    "s6_targets": 84,
    "originals_modified": 0,
    "byte_identical": True,
    "files": archived,
}
dump_new(RAW_MANIFEST, raw_manifest)

old_sources = load(OLD_SOURCES)
source_rows = {row["path"]: row for row in old_sources["sources"]}
for row in archived:
    destination = ROOT / row["archive_path"]
    source_rows[row["archive_path"]] = {
        "path": row["archive_path"],
        "bytes": destination.stat().st_size,
        "sha256": row["sha256"],
    }
for path in (RAW_MANIFEST, Path(__file__).resolve()):
    source_rows[path.relative_to(ROOT).as_posix()] = {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }

sources_v2 = {
    "schema": "n11-reply27-checkpoint-source-manifest-v2",
    "checkpoint_base_main": MAIN,
    "root": [60, 27],
    "previous_source_manifest": OLD_SOURCES.relative_to(ROOT).as_posix(),
    "previous_source_manifest_sha256": digest(OLD_SOURCES),
    "raw_input_preservation_manifest": RAW_MANIFEST.relative_to(ROOT).as_posix(),
    "raw_input_preservation_manifest_sha256": digest(RAW_MANIFEST),
    "source_count": len(source_rows),
    "missing_sources": 0,
    "sha256_mismatches": 0,
    "sources": [source_rows[key] for key in sorted(source_rows)],
}
for row in sources_v2["sources"]:
    path = ROOT / row["path"]
    if not path.is_file() or digest(path) != row["sha256"]:
        raise SystemExit(f"v2 source reference failed validation: {row['path']}")
dump_new(SOURCES_V2, sources_v2)

report = load(OUT / f"{PREFIX}-reply27-checkpoint-report.json")
report["raw_input_archive"] = {
    "manifest": RAW_MANIFEST.relative_to(ROOT).as_posix(),
    "files": len(archived),
    "s5_input_and_log_files": 16,
    "s6_input_and_log_files": 168,
    "originals_modified": 0,
    "byte_identical": True,
}
report["source_manifest"] = SOURCES_V2.relative_to(ROOT).as_posix()
report["artifact_inventory"] = INVENTORY_V2.relative_to(ROOT).as_posix()
report["supersedes_report"] = (OUT / f"{PREFIX}-reply27-checkpoint-report.json").relative_to(ROOT).as_posix()
dump_new(REPORT_V2, report)

artifacts = []
for top in sorted(OUT.glob(f"{PREFIX}*")):
    paths = [top] if top.is_file() else [p for p in top.rglob("*") if p.is_file()]
    for path in paths:
        if path == INVENTORY_V2:
            continue
        artifacts.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })

inventory = {
    "schema": "n11-reply27-checkpoint-artifact-hashes-v2",
    "checkpoint_base_main": MAIN,
    "artifact_count": len(artifacts),
    "total_bytes": sum(row["bytes"] for row in artifacts),
    "source_manifest": SOURCES_V2.relative_to(ROOT).as_posix(),
    "source_manifest_sha256": digest(SOURCES_V2),
    "raw_input_preservation_manifest": RAW_MANIFEST.relative_to(ROOT).as_posix(),
    "raw_input_preservation_manifest_sha256": digest(RAW_MANIFEST),
    "previous_inventory": OLD_INVENTORY.relative_to(ROOT).as_posix(),
    "previous_inventory_sha256": OLD_INVENTORY_SHA256,
    "missing_artifacts": 0,
    "artifact_sha256_mismatches": 0,
    "artifacts": artifacts,
}
dump_new(INVENTORY_V2, inventory)
print(json.dumps({
    "preserved_input_log_files": len(archived),
    "source_count": len(source_rows),
    "artifact_count": len(artifacts),
    "report": REPORT_V2.relative_to(ROOT).as_posix(),
    "source_manifest": SOURCES_V2.relative_to(ROOT).as_posix(),
    "inventory": INVENTORY_V2.relative_to(ROOT).as_posix(),
    "inventory_sha256": digest(INVENTORY_V2),
}, ensure_ascii=False, indent=2))
