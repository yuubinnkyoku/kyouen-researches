#!/usr/bin/env python3
"""Bind one-parent S6 history audit into the batch materializer's schema."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parents", type=Path, required=True)
    ap.add_argument("--parent-audit", type=Path, required=True)
    ap.add_argument("--saved-audit", type=Path, required=True)
    ap.add_argument("--saved-full-detail", type=Path, required=True)
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--dispatch-main-commit", required=True)
    ap.add_argument("--budget", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    audit = json.loads(args.parent_audit.read_text(encoding="utf-8"))
    parent_keys = audit.get("parent", {}).get("key")
    entries = audit.get("boundary_entries", [])
    ready = audit.get("direct_dispatch_ready_keys", [])
    blocked = audit.get("same_or_higher_budget_unknown_keys", [])
    if (audit.get("requested_budget") != args.budget or audit.get("conflicts") != 0
            or blocked or audit.get("direct_dispatch_ready_count") != len(ready)
            or audit.get("geometry", {}).get("boundary_child_count") != len(entries)):
        raise SystemExit("per-parent S6 audit is incomplete, blocked, or conflicting")
    if len(parent_keys or []) != 2 or not entries:
        raise SystemExit("expected a complete audited S6 boundary for one S5 parent")

    status_counts = Counter(item["saved_status"] for item in entries)
    per_parent = [{
        "path": rel(args.parent_audit),
        "sha256": sha256(args.parent_audit),
        "boundary_child_count": audit["geometry"]["boundary_child_count"],
    }]
    result = {
        "schema": "n11-s6-history-dispatch-preflight-adapter-v1",
        "dispatch_main_commit": args.dispatch_main_commit,
        "budget": args.budget,
        "parent_targets": {"path": rel(args.parents), "sha256": sha256(args.parents),
                           "keys": [parent_keys]},
        "saved_source_audit": {"path": rel(args.saved_audit), "sha256": sha256(args.saved_audit)},
        "saved_full_detail": {"path": rel(args.saved_full_detail),
                              "sha256": sha256(args.saved_full_detail)},
        "s5_cache": {"path": rel(args.s5_cache), "sha256": sha256(args.s5_cache)},
        "union": {
            "unique_canonical_s6_keys": len(entries),
            "dispatch_ready_unique_keys": len(ready),
            "same_or_higher_budget_unknown_keys": 0,
            "conflicts": 0,
            "saved_status_counts": dict(sorted(status_counts.items())),
        },
        "per_parent_history_audits": per_parent,
        "adapter_source": {"path": rel(Path(__file__)), "sha256": sha256(Path(__file__))},
        "interpretation": "Dispatch preflight only; it assigns no S5/S4 verdict and preserves UNKNOWN.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["union"], sort_keys=True))


if __name__ == "__main__":
    main()
