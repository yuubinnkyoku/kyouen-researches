#!/usr/bin/env python3
"""Fail-closed focused S7 dispatch and unverified receipt merge for the 1984 plan.

This does not prove any S7/S6 verdict. Never import its s7workerreport rows
as solver-trusted s7verdict cache entries without independent proof replay.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

import verify_s7_balanced_ownership_1984 as routing

HERE = Path(__file__).resolve().parent
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
SCHEMA = "n11-central49-1984-s7-frozen-single-s6-focus-v1"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    return digest(path.read_bytes()) if path is not None else None


def atomic_new(path, content):
    """Never overwrite an existing receipt, even across concurrent writers."""
    path = Path(path)
    need(not path.exists(), "output already exists: " + str(path))
    fd, tmp = tempfile.mkstemp(prefix=".s7-focus-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(tmp, path)  # EEXIST fails closed; never rename over an input.
    finally:
        os.unlink(tmp)


def final_keys():
    # This is the same source chain audited by routing.source_frontier().
    _, selected = routing.source.source()
    cert = json.loads(routing.source.CERT.read_text(encoding="utf-8"))
    for step in cert["steps"]:
        selected.difference_update(routing.source.base.decode(k)
                                   for k in step["removed_s6_classes"])
        selected.update(routing.source.base.decode(k)
                        for k in step["added_s6_classes"])
    keys = sorted(routing.source.base.key(k) for k in selected)
    need(len(keys) == 46 and len(set(keys)) == 46,
         "final S6 witness identity changed")
    return keys


def frozen(focus=None, existing=None):
    sets = routing.source_frontier()
    owner_doc = json.loads(routing.PLAN.read_text(encoding="utf-8"))
    _, owners = routing.verify(owner_doc, sets)
    keys = final_keys()
    need(len(keys) == len(sets) == 46, "source frontier mismatch")
    if focus is None:
        focus = min(keys, key=lambda k: (len(sets[keys.index(k)]), k))
    need(focus in keys, "focus must be one of the 46 selected S6 witnesses")
    children = sorted(sets[keys.index(focus)])
    worklists = [[k for k in children if owners[k] == worker]
                 for worker in range(4)]
    need(len(children) == len(set(children))
         and set().union(*map(set, worklists)) == set(children)
         and sum(map(len, worklists)) == len(children),
         "focused S7 ownership is not unique and complete")
    return {
        "schema": SCHEMA,
        "source_certificate": routing.source.CERT.name,
        "source_sha256": file_digest(routing.source.CERT),
        "ownership_certificate": routing.PLAN.name,
        "ownership_sha256": file_digest(routing.PLAN),
        "focus_policy": "minimum_raw_s7_children_then_canonical_key"
                        if focus == min(keys, key=lambda k: (len(sets[keys.index(k)]), k))
                        else "explicit_selected_s6",
        "focused_s6": focus,
        "s7_children": children,
        "worker_loads": list(map(len, worklists)),
        "worker_sha256": [digest(("\\n".join(w) + ("\\n" if w else "")).encode())
                          for w in worklists],
        "worklists": worklists,
        "existing_report_sha256": file_digest(existing),
        "evidence_level": "SCHEDULING_AND_UNVERIFIED_REPORTS_ONLY",
        "outcomes": UNKNOWN,
        "caveat": "No S7 or S6 verdict is proved; independent replay is mandatory."
    }


def parse_report(stream, origin, allowed, owners, requested_worker, merged, stats):
    local = set()
    for line_no, row in enumerate(csv.reader(stream), 1):
        if not row or (len(row) == 1 and not row[0].strip()):
            continue
        where = f"{origin}:{line_no}"
        need(len(row) == 6 and row[0] == "s7workerreport"
             and row[3] == "original_first" and row[5] == "unverified",
             "wrong receipt format/perspective at " + where)
        worker, key, verdict = row[1], row[2], row[4]
        need(worker in ("0", "1", "2", "3")
             and len(key) == 32
             and all(c in "0123456789abcdef" for c in key)
             and verdict in ("WIN", "LOSS", "UNKNOWN"),
             "invalid worker/key/verdict at " + where)
        w = int(worker)
        need(key in allowed and owners[key] == w
             and (requested_worker is None or requested_worker == w),
             "off-focus or wrong-owner report at " + where)
        need(key not in local, "duplicate key within report at " + where)
        local.add(key)
        stats["rows"] += 1
        if verdict == "UNKNOWN":
            stats["unknown_ignored"] += 1
            continue
        if key in merged:
            need(merged[key] == (w, verdict),
                 "WIN/LOSS conflict or owner mismatch at " + where)
            stats["repeated_consistent"] += 1
        else:
            merged[key] = (w, verdict)


def reports(plan, existing, worker_files):
    allowed = set(plan["s7_children"])
    owners = {key: w for w, worklist in enumerate(plan["worklists"])
              for key in worklist}
    need(len(owners) == len(allowed), "invalid focused owner map")
    merged, stats = {}, {"rows": 0, "unknown_ignored": 0,
                         "repeated_consistent": 0}
    if existing is not None:
        with existing.open(encoding="utf-8", newline="") as stream:
            parse_report(stream, existing, allowed, owners, None, merged, stats)
    for worker, path in worker_files:
        with path.open(encoding="utf-8", newline="") as stream:
            parse_report(stream, path, allowed, owners, worker, merged, stats)
    return merged, stats


def verify_frozen(plan, existing):
    need(isinstance(plan, dict) and plan.get("schema") == SCHEMA
         and plan.get("evidence_level") ==
             "SCHEDULING_AND_UNVERIFIED_REPORTS_ONLY"
         and plan.get("outcomes") == UNKNOWN,
         "plan identity or UNKNOWN evidence boundary changed")
    need(plan.get("existing_report_sha256") == file_digest(existing),
         "existing receipt changed since focus was frozen")
    expected = frozen(plan.get("focused_s6"), existing)
    need(plan == expected, "frozen focus, ownership or digest changed")


def self_test():
    keys = [f"{n:032x}" for n in range(2)]
    owners = {keys[0]: 0, keys[1]: 1}
    def check(rows, worker=None):
        merged, stats = {}, {"rows": 0, "unknown_ignored": 0,
                             "repeated_consistent": 0}
        parse_report(io.StringIO(rows), "synthetic", set(keys),
                     owners, worker, merged, stats)
        return merged, stats
    good = f"s7workerreport,0,{keys[0]},original_first,LOSS,unverified\\n"
    unknown = f"s7workerreport,1,{keys[1]},original_first,UNKNOWN,unverified\\n"
    need(check(good + unknown)[0] == {keys[0]: (0, "LOSS")}
         and check(good + unknown)[1]["unknown_ignored"] == 1,
         "UNKNOWN must not become a verdict")
    bad = [
        good + good,
        good.replace(",LOSS,", ",WIN,") + good,
        good.replace(",0,", ",1,"),
        good.replace(keys[0], "f" * 32),
        good.replace("original_first", "side_to_move"),
        good.replace("s7workerreport", "s7verdict"),
        good.replace("unverified", "verified"),
        good.replace(",LOSS,", ",DRAW,"),
    ]
    for i, rows in enumerate(bad):
        try:
            check(rows)
        except ValueError:
            continue
        raise AssertionError("bad synthetic receipt accepted: " + str(i))
    try:
        check(good, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("wrong worker accepted")
    print(json.dumps({"self_test": "PASS", "negative_tests": 9}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--focus-s6", help="selected canonical S6 key; default: fewest S7 children")
    parser.add_argument("--plan-out", type=Path)
    parser.add_argument("--audit-plan", type=Path)
    parser.add_argument("--existing", type=Path)
    parser.add_argument("--worker", nargs=2, action="append", default=[], metavar=("ID", "CSV"))
    parser.add_argument("--worklist", type=int, choices=range(4))
    parser.add_argument("--merged-out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    need(bool(args.plan_out) != bool(args.audit_plan),
         "choose exactly one of --plan-out and --audit-plan")
    need(not (args.plan_out and (args.worker or args.merged_out or args.worklist is not None)),
         "dispatch generation cannot accept worker results")
    if args.plan_out:
        plan = frozen(args.focus_s6, args.existing)
        atomic_new(args.plan_out, json.dumps(plan, indent=2, ensure_ascii=False) + "\\n")
        print(json.dumps({"focused_s6": plan["focused_s6"],
                          "s7_children": len(plan["s7_children"]),
                          "worker_loads": plan["worker_loads"],
                          "outcomes": UNKNOWN}))
        return
    plan = json.loads(args.audit_plan.read_text(encoding="utf-8"))
    need(args.focus_s6 is None or args.focus_s6 == plan.get("focused_s6"),
         "requested focus differs from frozen plan")
    verify_frozen(plan, args.existing)
    worker_files = []
    for ident, filename in args.worker:
        need(ident in ("0", "1", "2", "3"), "worker must be 0..3")
        worker_files.append((int(ident), Path(filename)))
    merged, stats = reports(plan, args.existing, worker_files)
    need(not any(verdict == "WIN" for _, verdict in merged.values()),
         "REPLAN_REQUIRED: reported original-first WIN7 may refute S6 LOSS; verify first")
    if args.worklist is not None:
        need(not args.merged_out and not args.worker,
             "worklist export cannot consume new worker reports")
        pending = [k for k in plan["worklists"][args.worklist] if k not in merged]
        if pending:
            sys.stdout.write("\\n".join(pending) + "\\n")
        return
    if args.merged_out is not None:
        lines = [f"s7workerreport,{w},{key},original_first,{verdict},unverified"
                 for key, (w, verdict) in sorted(merged.items())]
        atomic_new(args.merged_out, "\\n".join(lines) + ("\\n" if lines else ""))
    print(json.dumps({
        "schema": "n11-central49-s7-focused-unverified-merge-audit-v1",
        "focused_s6": plan["focused_s6"],
        "total_s7_children": len(plan["s7_children"]),
        "reported_loss7": len(merged),
        "unreported_s7": len(plan["s7_children"]) - len(merged),
        "report_stats": stats,
        "evidence_level": "WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED",
        "s6_outcome": "UNKNOWN", "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN"
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("S7_FOCUS_REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
