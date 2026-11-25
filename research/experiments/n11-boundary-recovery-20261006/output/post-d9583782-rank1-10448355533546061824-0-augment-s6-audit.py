#!/usr/bin/env python3
"""Add the just-verified exact s6 boundary to the hash-attested saved corpus."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
SCRIPTS = EXP / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))

from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical  # noqa: E402
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

BASE = OUT / "post-next17-dual-tight-92-final-saved-s6-sources.json"
NEW_RAW = OUT / "post-bdbdea7c-rank1-10412322338480586760-0-s6-exact-boundary-raw.csv"
NEW_MANIFEST = OUT / "post-bdbdea7c-rank1-10412322338480586760-0-s6-complete-sources.json"
NEW_SUMMARY = OUT / "post-bdbdea7c-rank1-10412322338480586760-0-s6-complete-summary.json"
GEOMETRY = OUT / "post-bdbdea7c-rank1-10412322338480586760-0-s4-win-geometry-audit.json"
OUT_PATH = OUT / "post-d9583782-rank1-10448355533546061824-0-augmented-s6-source-audit.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    old_exact, _ = read_saved_exact_s6(base)
    geometry = json.loads(GEOMETRY.read_text(encoding="utf-8"))
    manifest = json.loads(NEW_MANIFEST.read_text(encoding="utf-8"))
    summary = json.loads(NEW_SUMMARY.read_text(encoding="utf-8"))

    if geometry.get("schema") != "n11-dual-tight-s4-win-from-s6-geometry-audit-v1":
        raise SystemExit("unexpected geometry audit schema")
    witness = geometry.get("s5_win_witness", {})
    if witness.get("child_count") != 83 or witness.get("complete_canonical_s6_boundary") != "all exact WIN":
        raise SystemExit("geometry audit does not attest the complete 83-child exact-WIN boundary")
    boundary_keys = {tuple(row) for row in witness.get("s6_children", [])}
    solver_rows = {tuple(row["key"]): int(row["verdict"]) for row in witness.get("solver_rows", [])}
    if len(boundary_keys) != 83 or solver_rows != {key: 1 for key in boundary_keys}:
        raise SystemExit("geometry audit s6 child list is incomplete or not all exact WIN")
    if summary.get("parent_key") != [10414574138294272008, 0]:
        raise SystemExit("new s6 source manifest names an unexpected parent")
    if summary.get("boundary_s6_canonical_count") != 83 or summary.get("exact_child_count") != 83:
        raise SystemExit("new s6 source manifest has unexpected boundary/exact row counts")
    if summary.get("exact_child_verdicts", {}).get("LOSS") != 0 or summary.get("exact_child_verdicts", {}).get("WIN") != 83:
        raise SystemExit("new s6 source manifest is not 83 exact WIN rows")

    raw_digest = sha256(NEW_RAW)
    geom_sources = {x["path"].replace("\\", "/"): x["sha256"] for x in geometry.get("sources", [])}
    if geom_sources.get(rel(NEW_RAW)) != raw_digest:
        raise SystemExit("geometry audit does not hash-attest the new exact s6 raw file")
    combined_raw = manifest.get("combined_raw", {})
    if combined_raw.get("path", "").replace("\\", "/") != rel(NEW_RAW) or combined_raw.get("sha256") != raw_digest:
        raise SystemExit("s6 source manifest does not hash-attest the new exact s6 raw file")

    new_rows: dict[tuple[int, int], int] = {}
    replay_rows = 0
    for row_num, row in enumerate(csv.reader(NEW_RAW.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
            continue
        if len(row) != 11 or int(row[2]) != 6 or int(row[4]) != 1 or int(row[6]) != 1:
            raise SystemExit(f"expected an exact s6 WIN row at {NEW_RAW}:{row_num}: {row}")
        key = (int(row[9]), int(row[10]))
        if not safe_canonical(key, 6) or tuple(d4_canonical_key(points(key))) != key:
            raise SystemExit(f"new s6 key is not safe and canonical: {key}")
        if int(row[3]) != len(legal_after(set(points(key)))):
            raise SystemExit(f"new s6 legal count mismatch: {key}")
        if solver_rows.get(key) != 1:
            raise SystemExit(f"geometry audit does not verify exact WIN for {key}")
        if key in new_rows and new_rows[key] != 1:
            raise SystemExit(f"conflicting duplicate new s6 key: {key}")
        new_rows[key] = 1
        replay_rows += 1
    if replay_rows != 83 or set(new_rows) != boundary_keys:
        raise SystemExit(f"new s6 raw/geometry mismatch: rows={replay_rows} unique={len(new_rows)}")

    merged = {key: int(value["verdict"]) for key, value in old_exact.items()}
    for key, verdict in new_rows.items():
        previous = merged.get(key)
        if previous in (1, 2) and previous != verdict:
            raise SystemExit(f"exact s6 verdict conflict at {key}: {previous} vs {verdict}")
        merged[key] = verdict

    counts = Counter(merged.values())
    losses = counts[2]
    wins = counts[1]
    unknowns = counts[0]
    augmented = dict(base)
    augmented["schema"] = "n11-saved-s6-source-audit-with-exact-win-boundary-v1"
    augmented["source_basis"] = "hash-validated 38-source saved corpus plus the geometry-verified exact 83-child s6 WIN boundary"
    augmented["source_file_count"] = len(base["sources"]) + 1
    augmented["source_hashes_validated"] = True
    augmented["sources"] = list(base["sources"]) + [{
        "path": rel(NEW_RAW),
        "sha256": raw_digest,
        "s6_replay_rows": replay_rows,
        "normalized_noncanonical_rows": 0,
        "verdict_counts": {"1": replay_rows},
    }]
    augmented["s6"] = {
        "all_s6_exact_rows_geometry_checked": True,
        "exact_conflict_count": 0,
        "unique_canonical_keys": len(merged),
        "unique_loss_keys": losses,
        "unique_win_keys": wins,
        "unknown_only_keys": unknowns,
        "verdict_counts_by_unique_key": {"1": wins, "2": losses},
    }
    augmented["augmentation_provenance"] = {
        "base_audit": {"path": rel(BASE), "sha256": sha256(BASE)},
        "new_exact_s6_raw": {"path": rel(NEW_RAW), "sha256": raw_digest, "unique_rows": len(new_rows)},
        "new_source_manifest": {"path": rel(NEW_MANIFEST), "sha256": sha256(NEW_MANIFEST)},
        "new_summary": {"path": rel(NEW_SUMMARY), "sha256": sha256(NEW_SUMMARY)},
        "geometry_audit": {"path": rel(GEOMETRY), "sha256": sha256(GEOMETRY)},
        "overlap_with_base": len(set(old_exact) & set(new_rows)),
    }
    OUT_PATH.write_text(json.dumps(augmented, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"audit": rel(OUT_PATH), "source_files": len(augmented["sources"]),
                      "unique_s6_keys": len(merged), "WIN": wins, "LOSS": losses,
                      "UNKNOWN_only": unknowns, "new_unique_exact_WIN": len(set(new_rows) - set(old_exact)),
                      "overlap": len(set(old_exact) & set(new_rows)), "conflict": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
