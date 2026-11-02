#!/usr/bin/env python3
"""Safe terminal-gated single-S6 dispatch for the repaired 2096-class cover.

The 2090 cover is invalidated by a complete WIN6 strategy. This module
accepts only the independently checked 2096 repair and removes from its
worklists only K0644 terminal-replayed LOSS7, never historical cache labels.
Worker receipts are UNVERIFIED and cannot establish a game outcome.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import verify_2096_win6_repair as proof
import focus_s7_worker_2090 as historical
import verify_central49_2094_three_swap_descent as geom
import focus_s7_worker_1984 as receipts

SCHEMA = "n11-central49-2096-terminal-gated-focus-v1"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def key(s):
    return f"{s:032x}"


@lru_cache(maxsize=1)
def geometry():
    doc = json.loads(proof.CERT.read_text(encoding="utf-8"))
    proof.audit(doc)  # Replays 1984 WIN6, K0637 LOSS7, and exact 4x4 repair.
    old, _, _ = historical.geometry()  # Historical geometry, not a valid plan.
    result = dict(old)
    for k in doc["removed"]:
        s = int(k, 16)
        need(s in result, "removed S6 absent from source")
        del result[s]
    for k in doc["added"]:
        s = int(k, 16)
        need(s not in result, "added S6 already selected")
        result[s] = geom.four_frontier(s)
    counts = Counter(c for children in result.values() for c in children)
    loss7 = geom.context()[6]
    secured = set(counts) & loss7
    need(len(result) == 46 and len(counts) == 2096
         and sum(counts.values()) == 2989 and len(secured) == 6,
         "2096 repaired frontier changed")
    return result, counts, secured


def freeze():
    frontiers, counts, secured = geometry()
    def score(s):
        pending = frontiers[s] - secured
        return (len(pending), -sum(counts[c] > 1 for c in pending), key(s))
    focus = min(frontiers, key=score)
    children = frontiers[focus]
    certified = sorted(key(c) for c in children & secured)
    unverified = sorted(key(c) for c in children - secured)
    worklists = [unverified[i::4] for i in range(4)]
    need(len(unverified) + len(certified) == len(children)
         and len(set(unverified) | set(certified)) == len(children)
         and len(set().union(*map(set, worklists))) == len(unverified),
         "focused child ownership incomplete or duplicated")
    return {
        "schema": SCHEMA,
        "source_certificate": proof.CERT.name,
        "source_sha256": receipts.file_digest(proof.CERT),
        "selected_s6_sha256": hashlib.sha256(
            "".join(key(s) + "\n" for s in sorted(frontiers)).encode()
        ).hexdigest(),
        "total_distinct_s7": len(counts),
        "terminal_proved_s7_in_cover": len(secured),
        "focus_policy": "fewest_unproved_S7_then_most_shared_then_key",
        "focus_s6": key(focus),
        "focus_s7_children": sorted(key(c) for c in children),
        "certified_loss7": certified,
        "unverified_s7": unverified,
        "worker_loads": list(map(len, worklists)),
        "worker_sha256": [
            receipts.digest(("\n".join(w) + ("\n" if w else "")).encode())
            for w in worklists
        ],
        "worklists": worklists,
        "evidence_level": "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
        "outcomes": UNKNOWN,
    }


def audit_plan(doc):
    need(type(doc) is dict and doc.get("schema") == SCHEMA
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
             "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
         "wrong repaired plan identity or promoted verdict")
    need(doc == freeze(), "frozen 2096 plan differs from independent proof")
    need(max(doc["worker_loads"]) ==
         (len(doc["unverified_s7"]) + 3) // 4,
         "worker count imbalance")


def merge(doc, existing, workers):
    # Direct callers must pass the same independently verified frozen plan.
    audit_plan(doc)
    allowed = set(doc["unverified_s7"])
    owners = {k: wid for wid, keys in enumerate(doc["worklists"])
              for k in keys}
    need(len(owners) == len(allowed) and set(owners) == allowed,
         "incomplete or duplicate ownership")
    files = ([existing] if existing else []) + [p for _, p in workers]
    before = [receipts.file_digest(p) for p in files]
    merged = {}
    stats = {"rows": 0, "unknown_ignored": 0, "repeated_consistent": 0}
    if existing:
        with existing.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, existing, allowed, owners,
                                  None, merged, stats)
    for wid, path in workers:
        with path.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, path, allowed, owners,
                                  wid, merged, stats)
    need(before == [receipts.file_digest(p) for p in files],
         "worker report changed during merge")
    need(not any(verdict == "WIN" for _, verdict in merged.values()),
         "REPLAN_REQUIRED: reported WIN7 needs independent terminal replay")
    return merged, stats


def self_test():
    doc = freeze()
    audit_plan(doc)
    need(doc["total_distinct_s7"] == 2096
         and doc["terminal_proved_s7_in_cover"] == 6
         and len(doc["unverified_s7"]) <= 62
         and sum(doc["worker_loads"]) == len(doc["unverified_s7"]),
         "2096 focused worklist counts changed")
    for mode in ("verdict", "source", "secured", "owner"):
        bad = json.loads(json.dumps(doc))
        if mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "source":
            bad["source_sha256"] = "0" * 64
        elif mode == "secured":
            bad["certified_loss7"].append("0" * 32)
        else:
            bad["worklists"][0].append(bad["worklists"][1][0])
        for action in (lambda: audit_plan(bad),
                       lambda: merge(bad, None, [])):
            try:
                action()
            except (ValueError, KeyError, TypeError):
                pass
            else:
                raise AssertionError("tampered plan accepted: " + mode)
    first = doc["worklists"][0][0]
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder) / "worker.csv"
        good = f"s7workerreport,0,{first},original_first,LOSS,unverified\n"
        p.write_text(good, encoding="utf-8")
        merged, _ = merge(doc, None, [(0, p)])
        need(len(merged) == 1, "valid unverified report rejected")
        p.write_text(good.replace(",LOSS,", ",WIN,"), encoding="utf-8")
        try:
            merge(doc, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("reported WIN failed to stop dispatch")
        outside = next(k for k in sorted(key(c) for c in geometry()[1])
                       if k not in doc["unverified_s7"])
        p.write_text(good.replace(first, outside), encoding="utf-8")
        try:
            merge(doc, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("off-focus report accepted")
    print(json.dumps({
        "self_test": "PASS",
        "focus_s6": doc["focus_s6"],
        "total_distinct_s7": 2096,
        "focus_children": len(doc["focus_s7_children"]),
        "certified_focus_s7": len(doc["certified_loss7"]),
        "unverified_focus_s7": len(doc["unverified_s7"]),
        "worker_loads": doc["worker_loads"],
        "tampered_plan_rejected": 4,
        "bad_receipts_rejected": 2,
        "outcomes": UNKNOWN,
    }, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--plan-out", type=Path)
    p.add_argument("--audit-plan", type=Path)
    p.add_argument("--existing", type=Path)
    p.add_argument("--worker", nargs=2, action="append", default=[],
                   metavar=("ID", "CSV"))
    p.add_argument("--worklist", type=int, choices=range(4))
    p.add_argument("--merged-out", type=Path)
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    need(bool(args.plan_out) != bool(args.audit_plan),
         "choose exactly one of --plan-out and --audit-plan")
    if args.plan_out:
        need(not (args.existing or args.worker or args.merged_out
                  or args.worklist is not None),
             "plan generation cannot consume worker reports")
        doc = freeze()
        receipts.atomic_new(args.plan_out,
                            json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"focus_s6": doc["focus_s6"],
                          "unverified_s7": len(doc["unverified_s7"]),
                          "worker_loads": doc["worker_loads"],
                          "outcomes": UNKNOWN}))
        return
    doc = json.loads(args.audit_plan.read_text(encoding="utf-8"))
    audit_plan(doc)
    workers = []
    for wid, filename in args.worker:
        need(wid in ("0", "1", "2", "3"), "invalid worker ID")
        workers.append((int(wid), Path(filename)))
    merged, stats = merge(doc, args.existing, workers)
    if args.worklist is not None:
        need(not args.worker and not args.merged_out,
             "worklist export cannot consume new reports")
        pending = [k for k in doc["worklists"][args.worklist] if k not in merged]
        if pending:
            sys.stdout.write("\n".join(pending) + "\n")
        return
    if args.merged_out:
        lines = [f"s7workerreport,{wid},{k},original_first,{verdict},unverified"
                 for k, (wid, verdict) in sorted(merged.items())]
        receipts.atomic_new(args.merged_out,
                            "\n".join(lines) + ("\n" if lines else ""))
    print(json.dumps({
        "focus_s6": doc["focus_s6"],
        "terminal_certified_loss7": len(doc["certified_loss7"]),
        "unverified_reported_loss7": len(merged),
        "unreported_s7": len(doc["unverified_s7"]) - len(merged),
        "report_stats": stats, "outcomes": UNKNOWN,
    }))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("N11_2096_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
