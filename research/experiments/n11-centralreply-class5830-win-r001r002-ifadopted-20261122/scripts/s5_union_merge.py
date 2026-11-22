#!/usr/bin/env python3
"""n11 S5 verdict-cache union merger (fail-closed).

Merges one or more `s5verdict` exact-S5 cache files into a single
deterministic, independently checkable sorted cache:

  row format : `s5verdict,<lo>,<hi>,5,<verdict>,<nodes>`  (verdict in {1,2})
  comments   : lines starting with `#` are comments of the FIRST input only;
               they are emitted verbatim ahead of the sorted rows.
  conflicts   : same (lo,hi) with different WIN/LOSS value, whether within
               one file or across files, aborts the merge: rc=1, NO output
               file is written (fail closed).
  duplicates : same-value duplicate rows are elided; the FIRST occurrence
               (file order, then line order) fixes the nodes field.  A later
               same-verdict row with a different nodes value is kept out of
               the output and recorded in the audit (nodes are bookkeeping,
               never verdicts).
  output     : comment block, then all unique rows sorted ascending by
               (lo, hi).  Single-input merge therefore re-renders a sorted,
               comment-topped, conflict-free file byte-identically.

Audit JSON  : inputs with sha256, per-file row counts, unique total,
duplicates elided, verdict counts, nodes-mismatch bookkeeping, and the
output sha256.  The audit is written next to the output.

Exit codes : 0 ok, 1 fail-closed (no output), 2 selftest failure.

No verdict is created or interpreted here.  11x11 remains UNKNOWN.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

VERDICTS = (1, 2)


def fail(msg: str, code: int = 1):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(code)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_row(line: str):
    """Strict row gate. Returns (lo, hi, verdict, nodes) or None for blank."""
    s = line.strip("\r\n")
    if not s.strip():
        return None
    parts = s.split(",")
    if len(parts) != 6 or parts[0] != "s5verdict":
        fail(f"malformed row (not s5verdict,6 fields): {line!r}")
    try:
        lo, hi, depth, verdict, nodes = (int(x) for x in parts[1:])
    except ValueError:
        fail(f"malformed row (non-integer field): {line!r}")
    if depth != 5 or verdict not in VERDICTS or nodes < 0 or lo < 0 or hi < 0:
        fail(f"malformed row (depth/verdict/nodes domain): {line!r}")
    return lo, hi, verdict, nodes


def read_cache(path: Path):
    """Returns (comments, rows); rows = list of (lo, hi, verdict, nodes, line_index)."""
    comments = []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.startswith("#"):
                comments.append(line.rstrip("\n"))
            elif line.strip() == "":
                continue
            else:
                r = parse_row(line)
                if r is None:
                    continue
                rows.append(r + (i,))
    return comments, rows


def merge(inputs):
    comments = None
    out_rows = {}          # (lo,hi) -> [verdict, nodes, first_file, first_line]
    stats = {"per_input": [], "nodes_mismatch": []}
    dup_total = 0
    conflict = None
    for fi, path in enumerate(inputs):
        c, rows = read_cache(Path(path))
        if comments is None:
            comments = c
        for lo, hi, v, nodes, li in rows:
            k = (lo, hi)
            if k in out_rows:
                pv, pnodes, pf, pl = out_rows[k]
                if pv != v:
                    conflict = (
                        f"WIN/LOSS conflict at {lo}:{hi}: verdict {pv} "
                        f"(input #{pf + 1} line {pl + 1}) vs verdict {v} "
                        f"(input #{fi + 1} line {li + 1})"
                    )
                else:
                    dup_total += 1
                    if pnodes != nodes:
                        stats["nodes_mismatch"].append(
                            {"key": f"{lo}:{hi}", "verdict": v,
                             "kept_nodes": pnodes, "later_nodes": nodes,
                             "later_input": fi + 1, "later_line": li + 1}
                        )
            else:
                out_rows[k] = [v, nodes, fi, li]
        stats["per_input"].append(
            {"file": str(path), "sha256": sha256_file(Path(path)),
             "rows": len(rows), "unique_new": len({(r[0], r[1]) for r in rows})}
        )
    if conflict is not None:
        fail(conflict)
    keys = sorted(out_rows)
    return comments, out_rows, keys, dup_total, stats


def render(comments, out_rows, keys):
    lines = list(comments or [])
    body = []
    for lo, hi in keys:
        v, nodes, _, _ = out_rows[(lo, hi)]
        body.append(f"s5verdict,{lo},{hi},5,{v},{nodes}")
    return ("\n".join(lines + body) + "\n").encode("utf-8")


def run_merge(args):
    inputs = [Path(p) for p in args.inputs]
    if not inputs:
        fail("no inputs")
    for p in inputs:
        if not p.is_file():
            fail(f"missing input {p}")
    comments, out_rows, keys, dup_total, stats = merge(inputs)
    blob = render(comments, out_rows, keys)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    # write temp then rename: a failure never leaves a partial output
    tmp = out.with_suffix(out.suffix + ".tmp")
    with tmp.open("wb") as f:
        f.write(blob)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, out)
    counts = {1: 0, 2: 0}
    for k in out_rows:
        counts[out_rows[k][0]] += 1
    audit = {
        "tool": "s5_union_merge.py",
        "fail_closed_gates": "strict 6-field row schema, depth==5, verdict in {1,2}, "
                             "WIN/LOSS conflict abort (no output), first-occurrence nodes",
        "inputs": stats["per_input"],
        "unique_rows": len(keys),
        "duplicate_rows_elided": dup_total,
        "verdict_counts": {"WIN(1)": counts[1], "LOSS(2)": counts[2]},
        "nodes_field_mismatches_recorded": stats["nodes_mismatch"],
        "comments_kept_from_first_input": comments or [],
        "output_sha256": hashlib.sha256(blob).hexdigest(),
        "output_bytes": len(blob),
        "row_format": "s5verdict,<lo>,<hi>,5,<verdict>,<nodes>",
        "interpretation_guard": "nodes are bookkeeping, never verdicts; merge of "
                                "solver-trusted cache rows; no new verdict is created; "
                                "11x11 root questions remain UNKNOWN",
    }
    if args.audit:
        ap = Path(args.audit)
        ap.parent.mkdir(parents=True, exist_ok=True)
        ap.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(f"MERGED unique={len(keys)} dup_elided={dup_total} "
          f"WIN={counts[1]} LOSS={counts[2]} -> {out}")


# ---------------- selftest ----------------

def selftest(root: Path):
    """Fail-closed validation battery. Returns 0 iff all cases pass."""
    import random
    tmp = root / "selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    ok = []

    def make(name, lines):
        p = tmp / name
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return p

    def attempt(files, outname):
        out = tmp / outname
        try:
            run_merge(argparse.Namespace(inputs=[str(f) for f in files],
                                         out=str(out),
                                         audit=str(out.with_suffix(".audit.json"))))
            return 0, out
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
            return rc, out

    # case 1: positive dedupe+sort over a shuffled pseudo-corpus
    rng = random.Random(20261121)
    base_rows = [(1000 + i * 7, 536870912 + i * 3, v) for i, v in
                 [(0, 1), (1, 2), (2, 2), (3, 1), (4, 2), (5, 1), (6, 2)]]
    shuffled = list(base_rows)
    rng.shuffle(shuffled)
    dup_rows = shuffled[:3]
    lines = ["# pseudo corpus"] + [
        f"s5verdict,{lo},{hi},5,{v},{(lo + hi) % 97}" for (lo, hi, v) in
        shuffled + dup_rows]
    a = make("a.cache", lines)
    rc, out = attempt([a], "out-pos.cache")
    if rc != 0:
        fail("selftest positive rc", 2)
    got = out.read_text().splitlines()
    want = ["# pseudo corpus"] + [
        f"s5verdict,{lo},{hi},5,{v},{(lo + hi) % 97}" for (lo, hi, v) in
        sorted(base_rows)]
    if got != want:
        fail("selftest positive dedupe/sort mismatch", 2)
    ok.append("positive dedupe+sort")

    # case 2: cross-file conflict reject (no output file)
    a2 = make("a2.cache", ["s5verdict,1000,536870912,5,2,1"])
    b = make("b.cache", ["s5verdict,1000,536870912,5,1,1"])
    rc, out2 = attempt([a2, b], "out-conf.cache")
    if rc == 0 or out2.exists():
        fail("selftest cross-file conflict not rejected (or output written)", 2)
    ok.append("cross-file conflict reject: no output")

    # case 3: within-file conflict reject
    c = make("c.cache", ["s5verdict,5,7,5,1,1", "s5verdict,5,7,5,2,1"])
    rc, out3 = attempt([c], "out-conf2.cache")
    if rc == 0 or out3.exists():
        fail("selftest within-file conflict not rejected", 2)
    ok.append("within-file conflict reject: no output")

    # case 4: malformed verdict reject
    d = make("d.cache", ["s5verdict,5,7,5,3,1"])
    rc, out4 = attempt([d], "out-mal.cache")
    if rc == 0 or out4.exists():
        fail("selftest malformed verdict not rejected", 2)
    ok.append("malformed row reject: no output")

    # case 5: merge determinism (same input twice -> identical bytes + audit)
    rc, out5 = attempt([a], "det1.cache")
    rc2, out6 = attempt([a], "det2.cache")
    if rc != 0 or rc2 != 0:
        fail("selftest determinism runs rc", 2)
    if out5.read_bytes() != out6.read_bytes():
        fail("selftest double-run non-determinism", 2)
    if (tmp / "det1.audit.json").read_bytes() != (tmp / "det2.audit.json").read_bytes():
        fail("selftest double-run audit non-determinism", 2)
    ok.append("double-run determinism")

    print("SELFTEST PASS: " + "; ".join(ok))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("merge")
    m.add_argument("--out", required=True)
    m.add_argument("--audit", default=None)
    m.add_argument("inputs", nargs="+")
    s = sub.add_parser("selftest")
    s.add_argument("--root", default="/tmp/s5-union-merge-selftest")
    args = ap.parse_args()
    if args.cmd == "selftest":
        selftest(Path(args.root))
        return
    if args.cmd == "merge":
        run_merge(args)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
