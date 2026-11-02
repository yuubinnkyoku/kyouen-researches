#!/usr/bin/env python3
"""Current K0646 2154-class cover: independently secured, focused S7 worklists.

The five SHA256-pinned K0637 terminal strategies are replayed before any
K0644 lifted LOSS7 is omitted from worklists. Unverified worker receipts
are NEVER promoted to game verdicts. Any reported WIN triggers replanning.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile

import verify_central49_2154_two_swap_descent as current
import verify_five_terminal_loss7 as terminal
import focus_s7_worker_1984 as receipts

HERE = Path(__file__).resolve().parent
SCHEMA = "n11-central49-2154-certified-focus-v1"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def key(mask):
    return f"{mask:032x}"


def selection():
    doc = json.loads(current.CERT.read_text(encoding="utf-8"))
    # Audits the entire 2301 source, ten swaps, 4x4 geometry and complete
    # two-witness neighborhood, rejecting any promoted game outcome.
    result = current.audit(doc)
    need(result["final_s7_classes"] == 2154 and
         result["secured_loss7_from_k0644"] == 6 and
         result["two_swap_local_minimum"] == 2154,
         "K0646 independent audit changed")
    selected = current.source_selection()
    for step in doc["steps"]:
        rm = {int(k, 16) for k in step["removed"]}
        ad = {int(k, 16) for k in step["added"]}
        need(len(rm) == len(ad) == 2 and rm <= selected and
             not (ad & selected), "invalid witness exchange")
        selected = (selected - rm) | ad
    need(len(selected) == 46, "selected S6 count changed")
    return selected


@lru_cache(maxsize=1)
def geometry():
    selected = selection()
    # Unlike the geometry-only K0644 parent lift, replay all five original
    # complete terminal strategies and check their pinned SHA256 first.
    terminal_result = terminal.audit(HERE)
    need(len(terminal_result["certificates"]) == 5 and
         terminal_result["total_terminal_states"] == 1901,
         "five complete LOSS7 strategies changed")
    loss7 = current.terminal_loss7()
    need(len(loss7) == 23, "terminal-backed LOSS7 lift changed")
    _, _, win6, win7, _ = current.current.comparison_inventories()
    need(not {key(s) for s in selected} & set(win6),
         "selected S6 is certified WIN6")
    frontiers = {}
    for s in sorted(selected):
        raw = current.current.geometry.children(s)
        children = {current.current.geometry.canonical(c) for c in raw}
        need(len(raw) == len(children), "duplicate S7 inside witness")
        need(not {key(c) for c in children} & set(win7),
             "known WIN7 in conditional LOSS7 frontier")
        frontiers[s] = children
    multiplicity = Counter(c for ch in frontiers.values() for c in ch)
    secured = set(multiplicity) & loss7
    need(sum(map(len, frontiers.values())) == 2990 and
         len(multiplicity) == 2154 and len(secured) == 6,
         "2154 frontier or secured coverage changed")
    return frontiers, multiplicity, secured


def freeze(focus=None):
    frontiers, multiplicity, secured = geometry()
    # Prefer a witness that can reuse complete proofs; then minimize
    # unshared obligations, total unknown children and canonical key.
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
        need(len(focus) == 32 and
             all(c in "0123456789abcdef" for c in focus),
             "invalid canonical focus key")
        focus = int(focus, 16)
        need(focus in frontiers, "focus not in current 2154 plan")
        policy = ("most_certified_then_fewest_unshared_unknown_then_key"
                  if focus == preferred else "explicit_selected_s6")
    children = frontiers[focus]
    certified = sorted(children & secured)
    pending = sorted(children - secured)
    worklists = [[key(c) for c in pending[i::4]] for i in range(4)]
    need(len(set().union(*map(set, worklists))) == len(pending) and
         sum(map(len, worklists)) == len(pending),
         "missing or duplicate S7 worklist owner")
    selected = sorted(frontiers)
    return {
        "schema": SCHEMA,
        "source_certificate": current.CERT.name,
        "source_sha256": receipts.file_digest(current.CERT),
        "selected_s6_sha256": hashlib.sha256(
            ("\n".join(key(s) for s in selected) + "\n").encode()).hexdigest(),
        "selected_s6_count": len(selected),
        "total_distinct_s7": len(multiplicity),
        "terminal_certified_s7_in_cover": len(secured),
        "focus_s6": key(focus),
        "focus_policy": policy,
        "focus_s7_children": [key(c) for c in sorted(children)],
        "certified_loss7": [key(c) for c in certified],
        "unverified_s7": [key(c) for c in pending],
        "unshared_unverified_s7": sum(multiplicity[c] == 1 for c in pending),
        "worker_loads": list(map(len, worklists)),
        "worker_sha256": [receipts.digest(
            ("\n".join(keys) + ("\n" if keys else "")).encode())
            for keys in worklists],
        "worklists": worklists,
        "terminal_provenance": "K0637_SHA256_5_STRATEGIES_REPLAYED_K0644_23_PARENT_LIFT",
        "evidence_level": "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
        "outcomes": UNKNOWN,
    }


def audit_plan(doc):
    need(isinstance(doc, dict) and doc.get("schema") == SCHEMA and
         doc.get("outcomes") == UNKNOWN and
         doc.get("evidence_level") ==
         "TERMINAL_CERTIFIED_S7_AND_UNVERIFIED_WORKER_REPORTS",
         "wrong plan identity or verdict promotion")
    need(doc == freeze(doc.get("focus_s6")),
         "frozen plan differs from independently checked current evidence")
    need(max(doc["worker_loads"]) ==
         (len(doc["unverified_s7"]) + 3) // 4,
         "unbalanced focused ownership")


def merge(doc, existing, worker_files):
    allowed = set(doc["unverified_s7"])
    owners = {k: wid for wid, keys in enumerate(doc["worklists"]) for k in keys}
    need(set(owners) == allowed, "incomplete worklist ownership")
    files = ([existing] if existing else []) + [p for _, p in worker_files]
    before = [receipts.file_digest(p) for p in files]
    merged = {}
    stats = {"rows": 0, "unknown_ignored": 0, "repeated_consistent": 0}
    if existing:
        with existing.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, existing, allowed, owners,
                                  None, merged, stats)
    for wid, path in worker_files:
        with path.open(encoding="utf-8", newline="") as stream:
            receipts.parse_report(stream, path, allowed, owners,
                                  wid, merged, stats)
    need(before == [receipts.file_digest(p) for p in files],
         "receipt changed during merge")
    need(not any(verdict == "WIN" for _, verdict in merged.values()),
         "REPLAN_REQUIRED: reported WIN7 requires independent replay")
    return merged, stats


def self_test():
    receipts.self_test()
    plan = freeze()
    audit_plan(plan)
    need(len(plan["certified_loss7"]) >= 1,
         "default focus does not reuse terminal evidence")
    need(not (set(plan["certified_loss7"]) & set(plan["unverified_s7"])),
         "certified S7 incorrectly dispatched")
    need(sum(plan["worker_loads"]) + len(plan["certified_loss7"]) ==
         len(plan["focus_s7_children"]), "focused coverage incomplete")
    # Altered proof, worklist and verdict are rejected by the real auditor.
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
            raise AssertionError("tampered focus accepted: " + mode)
    owners = {k: wid for wid, keys in enumerate(plan["worklists"]) for k in keys}
    first = plan["worklists"][0][0]
    good = f"s7workerreport,0,{first},original_first,LOSS,unverified\n"
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "worker.csv"
        p.write_text(good, encoding="utf-8")
        merged, _ = merge(plan, None, [(0, p)])
        need(len(merged) == 1, "valid unverified receipt not merged")
        p.write_text(good.replace(",LOSS,", ",WIN,"), encoding="utf-8")
        try:
            merge(plan, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("reported WIN did not stop dispatch")
        p.write_text(good.replace(first, plan["certified_loss7"][0]),
                     encoding="utf-8")
        try:
            merge(plan, None, [(0, p)])
        except ValueError:
            pass
        else:
            raise AssertionError("certified child was redispatched")
    print(json.dumps({
        "self_test": "PASS", "focus_s6": plan["focus_s6"],
        "total_children": len(plan["focus_s7_children"]),
        "certified_loss7": len(plan["certified_loss7"]),
        "unverified_s7": len(plan["unverified_s7"]),
        "worker_loads": plan["worker_loads"],
        "tampered_plan_rejected": 4,
        "bad_receipts_rejected": 2,
        "outcomes": UNKNOWN
    }, ensure_ascii=False))


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
        receipts.atomic_new(args.plan_out,
                            json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
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
        receipts.atomic_new(args.merged_out,
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
        print("N11_2154_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
