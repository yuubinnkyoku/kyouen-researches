#!/usr/bin/env python3
"""Frozen single-S6 focus for the 1985-class N11 conditional cover.

This dispatches only geometric proof obligations. Worker WIN/LOSS receipts
are UNVERIFIED, never imported into a trusted cache or promoted to a proof.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import verify_central49_three_swap_chain as chain
import focus_s7_worker_1984 as receipts

HERE = Path(__file__).resolve().parent
FINAL_SHA = "f72c587537cbe2239b0f077545dfd14628298d2fe6d7c6b80ac7345ff46b6026"
SCHEMA = "n11-central49-1985-single-s6-focus-v1"
UNKNOWN = {"selected_s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def geometry():
    doc = json.loads(chain.MANIFEST.read_text(encoding="utf-8"))
    chain.audit(doc)  # Replays full source and every swap with independent 4x4 geometry.
    selected = set(chain.baseline.reconstruct())
    for step in doc["steps"]:
        removed = {int(k, 16) for k in step["removed"]}
        added = {int(k, 16) for k in step["added"]}
        need(removed <= selected and not (added & selected), "bad witness replacement")
        selected = (selected - removed) | added
    need(len(selected) == 46 and chain.digest(selected) == FINAL_SHA,
         "selected S6 set changed")
    frontiers = {}
    for key in sorted(selected):
        raw = chain.geom.children(key)
        children = {chain.geom.canonical(c) for c in raw}
        need(len(raw) == len(children), "within-witness S7 duplication")
        frontiers[key] = children
    multiplicity = Counter(c for children in frontiers.values() for c in children)
    need(sum(map(len, frontiers.values())) == 2989
         and len(multiplicity) == 1985, "1985 S7 frontier changed")
    return frontiers, multiplicity


def freeze(focus=None):
    frontiers, multiplicity = geometry()
    def priority(key):
        return (sum(multiplicity[c] == 1 for c in frontiers[key]),
                len(frontiers[key]), key)
    preferred = min(frontiers, key=priority)
    if focus is None:
        focus = preferred
    else:
        need(len(focus) == 32 and all(c in "0123456789abcdef" for c in focus),
             "invalid focus key")
        focus = int(focus, 16)
        need(focus in frontiers, "focus not selected in 1985 cover")
    children = sorted(frontiers[focus])
    worklists = [[f"{k:032x}" for k in children[i::4]] for i in range(4)]
    need(sum(map(len, worklists)) == len(children)
         and len(set().union(*map(set, worklists))) == len(children),
         "duplicate or missing S7 owner")
    return {
        "schema": SCHEMA,
        "source_certificate": chain.MANIFEST.name,
        "source_sha256": receipts.file_digest(chain.MANIFEST),
        "selected_s6_sha256": FINAL_SHA,
        "focus_s6": f"{focus:032x}",
        "focus_policy": ("fewest_unshared_S7_then_total_then_key"
                         if focus == preferred else "explicit_selected_S6"),
        "focus_s7_children": [f"{k:032x}" for k in children],
        "unshared_s7": sum(multiplicity[c] == 1 for c in children),
        "shared_s7": sum(multiplicity[c] > 1 for c in children),
        "worker_loads": list(map(len, worklists)),
        "worker_sha256": [
            receipts.digest(("\n".join(keys) + ("\n" if keys else "")).encode())
            for keys in worklists
        ],
        "worklists": worklists,
        "evidence_level": "CONDITIONAL_GEOMETRY_AND_UNVERIFIED_REPORTS_ONLY",
        "outcomes": UNKNOWN,
    }


def audit_plan(doc):
    need(type(doc) is dict and doc.get("schema") == SCHEMA
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
             "CONDITIONAL_GEOMETRY_AND_UNVERIFIED_REPORTS_ONLY",
         "wrong plan identity or verdict promotion")
    need(doc == freeze(doc.get("focus_s6")),
         "frozen plan differs from independently verified geometry")
    need(max(doc["worker_loads"]) ==
         (len(doc["focus_s7_children"]) + 3) // 4,
         "worker loads are not optimally balanced by count")


def merge(doc, existing, worker_files):
    owners = {key: worker for worker, keys in enumerate(doc["worklists"])
              for key in keys}
    allowed = set(doc["focus_s7_children"])
    need(len(owners) == len(allowed), "duplicate or missing owner")
    files = ([existing] if existing else []) + [p for _, p in worker_files]
    before = [receipts.file_digest(p) for p in files]
    merged = {}
    stats = {"rows": 0, "unknown_ignored": 0, "repeated_consistent": 0}
    if existing:
        with existing.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, existing, allowed, owners,
                                  None, merged, stats)
    for worker, path in worker_files:
        with path.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, path, allowed, owners,
                                  worker, merged, stats)
    need(before == [receipts.file_digest(p) for p in files],
         "report changed while being read")
    need(not any(verdict == "WIN" for _, verdict in merged.values()),
         "REPLAN_REQUIRED: reported original-first WIN7 requires independent replay")
    return merged, stats


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--focus-s6")
    p.add_argument("--plan-out", type=Path)
    p.add_argument("--audit-plan", type=Path)
    p.add_argument("--existing", type=Path)
    p.add_argument("--worker", nargs=2, action="append", default=[],
                   metavar=("ID", "CSV"))
    p.add_argument("--worklist", type=int, choices=range(4))
    p.add_argument("--merged-out", type=Path)
    args = p.parse_args()
    if args.self_test:
        receipts.self_test()  # Generic receipt conflict/owner/atomic-write negatives.
        return
    need(bool(args.plan_out) != bool(args.audit_plan),
         "choose exactly one of --plan-out and --audit-plan")
    if args.plan_out:
        need(not (args.existing or args.worker or args.merged_out
                  or args.worklist is not None), "plan creation cannot consume reports")
        doc = freeze(args.focus_s6)
        receipts.atomic_new(args.plan_out,
                            json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps({"focus_s6": doc["focus_s6"],
                          "unshared_s7": doc["unshared_s7"],
                          "shared_s7": doc["shared_s7"],
                          "worker_loads": doc["worker_loads"],
                          "outcomes": UNKNOWN}))
        return
    doc = json.loads(args.audit_plan.read_text(encoding="utf-8"))
    audit_plan(doc)
    need(args.focus_s6 is None or args.focus_s6 == doc["focus_s6"],
         "requested focus differs from frozen plan")
    worker_files = []
    for wid, filename in args.worker:
        need(wid in ("0", "1", "2", "3"), "invalid worker ID")
        worker_files.append((int(wid), Path(filename)))
    merged, stats = merge(doc, args.existing, worker_files)
    if args.worklist is not None:
        need(not args.worker and not args.merged_out,
             "worklist export cannot consume new reports")
        pending = [key for key in doc["worklists"][args.worklist]
                   if key not in merged]
        if pending:
            sys.stdout.write("\n".join(pending) + "\n")
        return
    if args.merged_out:
        lines = [f"s7workerreport,{wid},{key},original_first,{verdict},unverified"
                 for key, (wid, verdict) in sorted(merged.items())]
        receipts.atomic_new(args.merged_out,
                            "\n".join(lines) + ("\n" if lines else ""))
    print(json.dumps({"focus_s6": doc["focus_s6"],
                      "unverified_loss7_reports": len(merged),
                      "unreported_s7": len(doc["focus_s7_children"]) - len(merged),
                      "report_stats": stats, "outcomes": UNKNOWN}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("N11_1985_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
