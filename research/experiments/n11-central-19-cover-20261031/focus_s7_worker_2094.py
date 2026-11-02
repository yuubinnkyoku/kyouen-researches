#!/usr/bin/env python3
"""Current 2094-class central49 focus with terminal-gated S7 worker receipts.

Rebuild the certified 2154 source and both independently audited three-swaps.
No worker receipt is treated as a game verdict. WIN reports require replanning.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import verify_central49_2094_three_swap_descent as proof
import focus_s7_worker_2154 as old

HERE = Path(__file__).resolve().parent
SCHEMA = "n11-central49-2094-terminal-gated-focus-v1"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def key(s):
    return f"{s:032x}"


@lru_cache(maxsize=1)
def geometry():
    manifest = json.loads(proof.CERT.read_text(encoding="utf-8"))
    audit = proof.audit(manifest)  # Includes five complete terminal replays.
    need(audit["final_s7_classes"] == 2094 and
         audit["secured_terminal_loss7"] == 6,
         "independent 2094 audit changed")
    selected, _, _, _, _, _, loss7, source_frontiers = proof.context()
    frontiers = dict(source_frontiers)
    for step in manifest["steps"]:
        removed = {int(k, 16) for k in step["removed"]}
        added = {int(k, 16) for k in step["added"]}
        need(removed <= selected and not (added & selected),
             "invalid three-swap in work distributor")
        selected = (selected - removed) | added
        for s in removed:
            del frontiers[s]
        for s in added:
            frontiers[s] = proof.four_frontier(s)
    multiplicity = Counter(k for kids in frontiers.values() for k in kids)
    secured = set(multiplicity) & loss7
    need(len(selected) == len(frontiers) == 46
         and len(multiplicity) == 2094
         and sum(multiplicity.values()) == 2987
         and len(secured) == 6,
         "2094 focus geometry changed")
    return frontiers, multiplicity, secured


def freeze(focus=None):
    frontiers, multiplicity, secured = geometry()
    def priority(s):
        children = frontiers[s]
        return (-len(children & secured),
                sum(multiplicity[c] == 1 for c in children - secured),
                len(children - secured), s)
    preferred = min(frontiers, key=priority)
    if focus is None:
        focus = preferred
        policy = "most_certified_then_fewest_unshared_unknown_then_key"
    else:
        need(type(focus) is str and len(focus) == 32
             and all(c in "0123456789abcdef" for c in focus),
             "invalid focus S6 key")
        focus = int(focus, 16)
        need(focus in frontiers, "focus not in current 2094 selection")
        policy = ("most_certified_then_fewest_unshared_unknown_then_key"
                  if focus == preferred else "explicit_selected_s6")
    children = frontiers[focus]
    certified = sorted(children & secured)
    pending = sorted(children - secured)
    worklists = [[key(c) for c in pending[i::4]] for i in range(4)]
    need(sum(map(len, worklists)) == len(pending)
         and len(set().union(*map(set, worklists))) == len(pending),
         "incomplete or duplicated worker ownership")
    return {
        "schema": SCHEMA,
        "source_certificate": proof.CERT.name,
        "source_sha256": old.receipts.file_digest(proof.CERT),
        "selected_s6_sha256": proof.digest(frontiers),
        "selected_s6_count": 46,
        "total_distinct_s7": len(multiplicity),
        "terminal_certified_s7_in_cover": len(secured),
        "focus_s6": key(focus),
        "focus_policy": policy,
        "focus_s7_children": [key(c) for c in sorted(children)],
        "certified_loss7": [key(c) for c in certified],
        "unverified_s7": [key(c) for c in pending],
        "unshared_unverified_s7": sum(multiplicity[c] == 1 for c in pending),
        "worker_loads": list(map(len, worklists)),
        "worker_sha256": [old.receipts.digest(
            ("\n".join(keys) + ("\n" if keys else "")).encode())
            for keys in worklists],
        "worklists": worklists,
        "terminal_provenance": "K0637_SHA256_5_REPLAYED_K0644_23_PARENT_LIFT",
        "evidence_level": "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
        "outcomes": UNKNOWN,
    }


def audit_plan(doc):
    need(type(doc) is dict and doc.get("schema") == SCHEMA
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
         "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
         "wrong focus identity or unproved verdict")
    need(doc == freeze(doc.get("focus_s6")),
         "frozen worklist differs from independent 2094 evidence")
    need(max(doc["worker_loads"]) ==
         (len(doc["unverified_s7"]) + 3) // 4,
         "unbalanced worklist")


def merge(doc, existing, workers):
    # Reuse the already audited receipt parser, atomic writer and
    # owner/conflict checks; it is parameterized by the frozen worklist.
    return old.merge(doc, existing, workers)


def self_test():
    plan = freeze()
    audit_plan(plan)
    need(plan["focus_s6"] == "00000000000000203808000000000040"
         and len(plan["focus_s7_children"]) == 64
         and len(plan["certified_loss7"]) == 2
         and len(plan["unverified_s7"]) == 62
         and plan["worker_loads"] == [16, 16, 15, 15],
         "focused 2094 obligation count changed")
    for mode in ("verdict", "secured", "owner", "source"):
        bad = json.loads(json.dumps(plan))
        if mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "secured":
            bad["certified_loss7"].pop()
        elif mode == "owner":
            bad["worklists"][0].append(bad["worklists"][1][0])
        else:
            bad["source_sha256"] = "0" * 64
        try:
            audit_plan(bad)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("tampered plan accepted: " + mode)
    first = plan["worklists"][0][0]
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder) / "worker.csv"
        good = f"s7workerreport,0,{first},original_first,LOSS,unverified\n"
        p.write_text(good)
        merged, _ = merge(plan, None, [(0, p)])
        need(len(merged) == 1, "valid unverified receipt rejected")
        p.write_text(good.replace(",LOSS,", ",WIN,"))
        try:
            merge(plan, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("reported WIN failed to stop dispatch")
        p.write_text(good.replace(first, plan["certified_loss7"][0]))
        try:
            merge(plan, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("certified child redispatched")
    print(json.dumps({"self_test": "PASS",
                      "focus_s6": plan["focus_s6"],
                      "total_children": 64, "certified_loss7": 2,
                      "unverified_s7": 62, "worker_loads": plan["worker_loads"],
                      "tampered_plan_rejected": 4, "bad_receipts_rejected": 2,
                      "outcomes": UNKNOWN}))


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
        self_test()
        return
    need(bool(args.plan_out) != bool(args.audit_plan),
         "choose exactly one of --plan-out and --audit-plan")
    if args.plan_out:
        need(not (args.existing or args.worker or args.merged_out or
                  args.worklist is not None),
             "plan generation cannot consume reports")
        doc = freeze(args.focus_s6)
        old.receipts.atomic_new(
            args.plan_out, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"focus_s6": doc["focus_s6"],
                          "certified_loss7": len(doc["certified_loss7"]),
                          "unverified_s7": len(doc["unverified_s7"]),
                          "worker_loads": doc["worker_loads"],
                          "outcomes": UNKNOWN}))
        return
    doc = json.loads(args.audit_plan.read_text(encoding="utf-8"))
    audit_plan(doc)
    need(args.focus_s6 is None or args.focus_s6 == doc["focus_s6"],
         "focus differs from frozen plan")
    workers = []
    for wid, filename in args.worker:
        need(wid in ("0", "1", "2", "3"), "invalid worker")
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
        old.receipts.atomic_new(args.merged_out,
                                "\n".join(lines) + ("\n" if lines else ""))
    print(json.dumps({"focus_s6": doc["focus_s6"],
                      "terminal_certified_loss7": len(doc["certified_loss7"]),
                      "unverified_reported_loss7": len(merged),
                      "unreported_s7": len(doc["unverified_s7"]) - len(merged),
                      "report_stats": stats, "outcomes": UNKNOWN}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("N11_2094_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
