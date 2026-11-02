#!/usr/bin/env python3
"""Rebind the proven 64-child focus to the current 2090 conditional cover.

The selected focus S6 is unchanged by the independently checked 2091->2090
two-swap. All terminal-backed children and unverified worklists are
revalidated, and the global source/digest is rebound to 2090. Reports
remain unverified and can never be promoted to game outcomes here.
"""
import argparse
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import sys
import tempfile

import focus_s7_worker_2091 as previous
import verify_central49_2090_two_swap as proof

HERE = Path(__file__).resolve().parent
SCHEMA = "n11-central49-2090-terminal-gated-focus-v1"
FOCUS = "00000000000000203808000000000040"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, message):
    if not ok:
        raise ValueError(message)


@lru_cache(maxsize=1)
def geometry():
    doc = json.loads(proof.CERT.read_text(encoding="utf-8"))
    predecessor, _, _ = previous.geometry()
    predecessor_keys = set(predecessor)
    result = proof.audit(doc)  # Five complete terminal replays and 4x4 geometry.
    need(set(previous.geometry()[0]) == predecessor_keys,
         "2090 audit mutated the cached 2091 source")
    need(result["final_distinct_s7"] == 2090 and
         result["terminal_certified_loss7"] == 6,
         "2090 independent proof changed")
    frontiers, _, _ = previous.geometry()
    frontiers = dict(frontiers)
    for key in doc["removed"]:
        need(int(key, 16) in frontiers, "removed S6 missing")
        del frontiers[int(key, 16)]
    for key in doc["added"]:
        s = int(key, 16)
        need(s not in frontiers, "added S6 already selected")
        frontiers[s] = proof.geometry.four_frontier(s)
    multiplicity = Counter(c for children in frontiers.values() for c in children)
    loss7 = proof.geometry.context()[6]
    secured = set(multiplicity) & loss7
    need(len(frontiers) == 46 and len(multiplicity) == 2090
         and sum(multiplicity.values()) == 2983 and len(secured) == 6,
         "current 2090 frontier mismatch")
    need(int(FOCUS, 16) in frontiers, "pinned focus was removed")
    return frontiers, multiplicity, secured


def freeze():
    # The focus is unchanged; preserve its already terminal-gated child
    # ownership, but never reuse the obsolete 2091 global plan identity.
    old = previous.freeze()
    frontiers, multiplicity, secured = geometry()
    children = frontiers[int(FOCUS, 16)]
    need({f"{c:032x}" for c in children} == set(old["focus_s7_children"]),
         "focused children changed under the 2090 replan")
    need({f"{c:032x}" for c in children & secured} ==
         set(old["certified_loss7"]), "terminal-secured focus changed")
    old.update({
        "schema": SCHEMA,
        "source_certificate": proof.CERT.name,
        "source_sha256": previous.previous.previous.old.receipts.file_digest(proof.CERT),
        "selected_s6_sha256": proof.geometry.digest(frontiers),
        "total_distinct_s7": len(multiplicity),
        "terminal_certified_s7_in_cover": len(secured),
        "focus_policy": "pinned_terminal_backed_focus_reused_from_2091",
        "terminal_provenance": "K0637_SHA256_5_REPLAYED_K0644_23_PARENT_LIFT_2090",
        "outcomes": UNKNOWN,
    })
    return old


def audit_plan(doc):
    need(type(doc) is dict and doc.get("schema") == SCHEMA
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
         "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
         "wrong 2090 plan identity or promoted verdict")
    need(doc == freeze(), "frozen plan differs from current 2090 proof")
    need(max(doc["worker_loads"]) ==
         (len(doc["unverified_s7"]) + 3) // 4,
         "worker ownership not balanced")


def merge(doc, existing, workers):
    # Also enforce the frozen 2090 identity for direct library callers.
    # The CLI already audits the plan, but a direct merge() previously
    # accepted a forged worklist and could admit off-plan receipts.
    audit_plan(doc)
    return previous.merge(doc, existing, workers)


def self_test():
    doc = freeze()
    audit_plan(doc)
    need((doc["total_distinct_s7"], len(doc["focus_s7_children"]),
          len(doc["certified_loss7"]), len(doc["unverified_s7"])) ==
         (2090, 64, 2, 62) and doc["worker_loads"] == [16, 16, 15, 15],
         "2090 focused obligations changed")
    for mode in ("verdict", "source", "secured", "owner"):
        bad = json.loads(json.dumps(doc))
        if mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "source":
            bad["source_sha256"] = "0" * 64
        elif mode == "secured":
            bad["certified_loss7"].pop()
        else:
            bad["worklists"][0].append(bad["worklists"][1][0])
        try:
            audit_plan(bad)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("tampered 2090 focus accepted: " + mode)
        # A direct merge() must reject the same tampered plan even without
        # the command-line audit step; no worker report is needed to test it.
        try:
            merge(bad, None, [])
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("direct merge accepted tampered plan: " + mode)
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
            raise AssertionError("reported WIN failed to require replanning")
        p.write_text(good.replace(first, doc["certified_loss7"][0]),
                     encoding="utf-8")
        try:
            merge(doc, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("certified child was redispatched")
    print(json.dumps({
        "self_test": "PASS", "focus_s6": FOCUS,
        "total_distinct_s7": 2090, "total_children": 64,
        "certified_loss7": 2, "unverified_s7": 62,
        "worker_loads": [16, 16, 15, 15],
        "tampered_plan_rejected": 4, "bad_receipts_rejected": 2,
        "outcomes": UNKNOWN,
    }))


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
        need(not (args.existing or args.worker or args.merged_out or
                  args.worklist is not None),
             "plan generation cannot consume reports")
        doc = freeze()
        previous.previous.previous.old.receipts.atomic_new(
            args.plan_out, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"focus_s6": FOCUS,
                          "certified_loss7": len(doc["certified_loss7"]),
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
        previous.previous.previous.old.receipts.atomic_new(
            args.merged_out, "\n".join(lines) + ("\n" if lines else ""))
    print(json.dumps({
        "focus_s6": FOCUS,
        "terminal_certified_loss7": len(doc["certified_loss7"]),
        "unverified_reported_loss7": len(merged),
        "unreported_s7": len(doc["unverified_s7"]) - len(merged),
        "report_stats": stats, "outcomes": UNKNOWN,
    }))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("N11_2090_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
