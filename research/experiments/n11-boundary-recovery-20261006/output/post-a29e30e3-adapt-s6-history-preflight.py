#!/usr/bin/env python3
"""Adapt a hash-bound legacy S6 preflight to the v2 evidence materializer schema.

This is a schema adapter only. It checks each referenced input/hash and copies
no verdicts or solver outcomes into a different form.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(value: str) -> Path:
    path = Path(value.replace("\\", "/"))
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def require_source(document: dict, path: Path) -> dict:
    expected = next((item for item in document.get("sources", [])
                     if resolve(item["path"]).resolve() == path.resolve()), None)
    if expected is None or not path.is_file() or digest(path) != expected.get("sha256"):
        raise SystemExit(f"legacy preflight does not hash-bind source: {path}")
    if expected.get("bytes") is not None and expected["bytes"] != path.stat().st_size:
        raise SystemExit(f"legacy preflight byte count differs: {path}")
    return expected


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--legacy-history", type=Path, required=True)
    ap.add_argument("--target-manifest", type=Path, required=True)
    ap.add_argument("--parents", type=Path, required=True)
    ap.add_argument("--batch-summary", type=Path, required=True)
    ap.add_argument("--saved-audit", type=Path, required=True)
    ap.add_argument("--saved-full-detail", type=Path, required=True)
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--dispatch-main-commit", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite adapted preflight: {args.out}")

    old = json.loads(args.legacy_history.read_text(encoding="utf-8"))
    manifest = json.loads(args.target_manifest.read_text(encoding="utf-8"))
    batch = json.loads(args.batch_summary.read_text(encoding="utf-8"))
    require_source(old, args.target_manifest)
    require_source(manifest, args.parents)
    require_source(manifest, args.s5_cache)
    require_source(manifest, args.saved_full_detail)
    require_source(manifest, args.saved_audit)
    if (batch.get("schema") != "n11-complete-s5-via-s6-local-v1"
            or batch.get("parents_sha256") != digest(args.parents)
            or batch.get("saved_audit_sha256") != digest(args.saved_audit)
            or batch.get("budget") != old.get("requested_s6_budget")
            or len(batch.get("parents", [])) != old.get("parent_count")
            or len(old.get("parents", [])) != old.get("parent_count")):
        raise SystemExit("batch summary and legacy S6 preflight do not match")
    if (old.get("conflicts") != 0
            or old.get("same_or_higher_budget_unknown_s6_keys") != 0
            or old.get("local_new_exact_s6_rows_requiring_reuse") != 0):
        raise SystemExit("legacy S6 preflight contains a conflict or blocked history")
    if (manifest.get("canonical_s5_unknown_targets") != old.get("parent_count")
            or old.get("s6_boundary_union") <= 0
            or old.get("parent_child_incidences") != batch.get("parent_child_relations")):
        raise SystemExit("legacy preflight geometry cardinalities differ from batch summary")

    per_parent = []
    for record in old["parents"]:
        audit_path = resolve(record["audit"]["path"])
        if not audit_path.is_file() or digest(audit_path) != record["audit"]["sha256"]:
            raise SystemExit(f"per-parent history audit missing/hash mismatch: {audit_path}")
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        key = record.get("key")
        if (audit.get("requested_budget") != old.get("requested_s6_budget")
                or audit.get("conflicts") != 0
                or audit.get("same_or_higher_budget_unknown_keys")
                or audit.get("parent", {}).get("key") != key
                or audit.get("geometry", {}).get("boundary_child_count") != record.get("boundary_children")):
            raise SystemExit(f"per-parent history audit disagrees with preflight: {key}")
        per_parent.append({
            "path": rel(audit_path),
            "sha256": record["audit"]["sha256"],
            "boundary_child_count": record["boundary_children"],
        })

    adapted = {
        "schema": "n11-reply27-local-s6-history-preflight-adapted-v1",
        "adaptation_claim": "Legacy preflight fields were schema-mapped after SHA-256 checks; no verdicts were added or changed.",
        "dispatch_main_commit": args.dispatch_main_commit,
        "budget": old["requested_s6_budget"],
        "parent_targets": {"path": rel(args.parents), "sha256": digest(args.parents)},
        "saved_source_audit": {"path": rel(args.saved_audit), "sha256": digest(args.saved_audit)},
        "saved_full_detail": {"path": rel(args.saved_full_detail), "sha256": digest(args.saved_full_detail)},
        "s5_cache": {"path": rel(args.s5_cache), "sha256": digest(args.s5_cache)},
        "union": {
            "unique_canonical_s6_keys": old["s6_boundary_union"],
            "dispatch_ready_unique_keys": old["direct_dispatch_ready_unique_s6_keys"],
            "same_or_higher_budget_unknown_keys": old["same_or_higher_budget_unknown_s6_keys"],
            "conflicts": old["conflicts"],
            "saved_status_counts": old["saved_s6_verdict_counts_over_unique_union"],
        },
        "parent_child_incidences": old["parent_child_incidences"],
        "parent_count": old["parent_count"],
        "parent_outcomes_before_dispatch": old["parent_outcomes"],
        "per_parent_history_audits": per_parent,
        "adapted_sources": [
            {"path": rel(path), "sha256": digest(path), "bytes": path.stat().st_size}
            for path in (args.legacy_history, args.target_manifest, args.parents,
                         args.batch_summary, args.saved_audit, args.saved_full_detail,
                         args.s5_cache)
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(adapted, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"out": rel(args.out), "parents": len(per_parent),
                      "s6_union": adapted["union"]["unique_canonical_s6_keys"],
                      "same_budget_unknowns": adapted["union"]["same_or_higher_budget_unknown_keys"],
                      "conflicts": adapted["union"]["conflicts"],
                      "sha256": digest(args.out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
