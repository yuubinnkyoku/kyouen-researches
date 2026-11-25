#!/usr/bin/env python3
"""Prepare and audit a cold exact-replay gate benchmark.

Input is any --exact-record CSV.  We select unique s5 canonical roots and write
one replay input plus a manifest.  After native solver runs are produced, the
same script can compare verdicts row-by-row and reject any gate with a mismatch.

This closes a reproducibility hole in the historical 23-root benchmark: the
report survived, but its original root CSV is not present in the current repo.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def prepare(src: Path, out: Path, manifest: Path, stones: int):
    raw = rows(src)
    # exact-record has historically had comment/header variants.  Keep rows
    # containing a parseable stone count and a canonical key payload verbatim;
    # dedup by the final two 64-bit key fields when available, otherwise row.
    selected, seen = [], set()
    for row in raw:
        if not row or row[0].startswith("#"):
            continue
        try:
            ints = [int(x, 0) for x in row if x.strip()]
        except ValueError:
            continue
        if stones not in ints[:6]:
            continue
        key = tuple(row[-2:]) if len(row) >= 2 else tuple(row)
        if key in seen:
            continue
        seen.add(key); selected.append(row)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(selected)
    manifest.write_text(json.dumps({
        "source": str(src), "stones": stones, "unique_rows": len(selected),
        "dedup_rule": "last two fields (canonical key payload when present)"
    }, indent=2) + "\n", encoding="utf-8")
    print(f"prepared {len(selected)} unique s{stones} rows -> {out}")


def replay_map(path: Path):
    ans = {}
    for row in rows(path):
        if not row or row[0] != "replay":
            continue
        # Stable comparison key: replay id/key columns before volatile counters.
        # Verdict is searched explicitly to survive appended instrumentation.
        verdict = next((x for x in row if x in {"WIN","LOSS","UNKNOWN","UNK"}), None)
        if verdict is None:
            continue
        key = tuple(row[1:4])
        ans[key] = verdict.replace("UNK","UNKNOWN")
    return ans


def compare(control: Path, candidates: list[Path], out: Path):
    base = replay_map(control)
    report = {"control": str(control), "control_rows": len(base), "candidates": []}
    failed = False
    for p in candidates:
        cur = replay_map(p)
        mismatches = []
        for k, v in base.items():
            if cur.get(k) != v:
                mismatches.append({"key": list(k), "control": v, "candidate": cur.get(k)})
        item = {"path": str(p), "rows": len(cur), "mismatches": mismatches,
                "accepted_soundness": not mismatches and len(cur) == len(base)}
        report["candidates"].append(item)
        failed |= not item["accepted_soundness"]
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if failed else 0)


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("prepare")
    p.add_argument("record", type=Path); p.add_argument("out", type=Path)
    p.add_argument("--manifest", type=Path, required=True); p.add_argument("--stones",type=int,default=5)
    c=sub.add_parser("compare")
    c.add_argument("control",type=Path); c.add_argument("candidates",type=Path,nargs="+")
    c.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    if a.cmd=="prepare": prepare(a.record,a.out,a.manifest,a.stones)
    else: compare(a.control,a.candidates,a.out)


if __name__=="__main__": main()
