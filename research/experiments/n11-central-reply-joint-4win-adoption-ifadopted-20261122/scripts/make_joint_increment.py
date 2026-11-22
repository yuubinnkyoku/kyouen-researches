# make_joint_increment.py -- machine-derive the JOINT unconsumed-packet increment cache
# (4 WINs b018/d002/e002/f017 + 21 LOSS rows) from the published closure-batch raws.
# Fail-closed: every source row must be a 2-pass node-exact pinned-replica raw.
# The increment exists ONLY for the if-adopted what-if analysis; verdicts are NOT consumed.
import os, sys

KIT = "/home/user/knowledge/kyouen-research/_19root-refresh-kit"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output",
                   "increment-unconsumed-packet-25rows-IFADOPTED-20261122.cache")

ROWS = [
    # (key, batch_dir, expectation)
    ("b018", "batch16757", 1),
    ("d001", "batch20421", 2), ("d002", "batch20421", 1), ("d003", "batch20421", 2), ("d004", "batch20421", 2),
    ("e001", "batch16371", 2), ("e002", "batch16371", 1),
] + [("f%03d" % i, "batch12264", 2) for i in range(1, 17)] + [
    ("f017", "batch12264", 1), ("f018", "batch12264", 2),
]


def parse(batch, key):
    got = []
    for p in (f"{KIT}/{batch}/output/raw/{key}.p1.out", f"{KIT}/{batch}/output/raw/{key}.p2.out"):
        if not os.path.isfile(p):
            sys.exit(f"ABORT missing raw {p}")
        line = [l for l in open(p) if l.startswith("replay,")]
        if len(line) != 1:
            sys.exit(f"ABORT raw parse {p}: {len(line)} rows")
        # replay,<id>,<stones>,<legal>,<is_or>,<budget>,<result>,<nodes>,<wall>,<lo>,<hi>
        got.append(line[0].strip().split(","))
    f1, f2 = got
    for i in (2, 3, 6, 7):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: passes differ at field {i}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {key}: schema {f1[:6]}")
    return int(f1[9]), int(f1[10]), int(f1[6]), int(f1[7])


def main():
    rows = []
    for key, batch, expect in ROWS:
        lo, hi, result, nodes = parse(batch, key)
        if result != expect:
            sys.exit(f"ABORT {key}: result {result} != expected {expect}")
        rows.append((lo, hi, result, nodes, key))
    seen = set()
    for lo, hi, *_ in rows:
        if (lo, hi) in seen:
            sys.exit(f"ABORT duplicate key {(lo, hi)}")
        seen.add((lo, hi))
    wins = [r for r in rows if r[2] == 1]
    losses = [r for r in rows if r[2] == 2]
    hdr = [
        "# n11 central-reply closure grind: JOINT unconsumed-packet IF-ADOPTED increment (2026-11-22)",
        "# 25 rows: 4 WINs (b018/d002/e002/f017) + 21 LOSS rows (d001/d003/d004, e001, f001-f016/f018)",
        "# All rows are 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# The WINs are NOT consumed by the lane (scrutiny owner pending); all 25 rows are independently",
        "# corroborated verdict-level by the third implementation (Part G, audit 281/281 gates PASS).",
        "# This increment exists ONLY for the joint if-adopted what-if analysis.",
        "# experiment: research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/ (Part G/H)",
    ]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for h in hdr:
            fh.write(h + "\n")
        for lo, hi, v, nodes, key in sorted(rows, key=lambda r: (r[0], r[1])):
            fh.write(f"s5verdict,{lo},{hi},5,{v},{nodes}\n")
    print(f"wrote {OUT}: {len(wins)} WIN + {len(losses)} LOSS = {len(rows)} rows")


if __name__ == "__main__":
    main()
