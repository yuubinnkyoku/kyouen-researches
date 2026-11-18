#!/usr/bin/env python3
"""Independent shared-memo cross-check of the 31-row cost-16 parent.

This script rebuilds the target rows from pinned source files, regenerates
all legal D4-canonical 7-stone roots with integer det4, and computes the
odd-r A/B minimum-cover totals.  Its B calculation shares one PmLazy memo
across all 31 doubled-row slices; the checkpoint used 31 fresh-memo slices.
Two fresh shared-memo runs are compared before the deterministic JSON is
written.  No game-tree search or verdict is performed.
"""
from __future__ import annotations

import csv
import gc
import hashlib
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(
    HERE, "output", "cost16-shared-memo-crosscheck-20261118.json"
)

TARGET = "00000000000000003800000008001000"
STATE_CAP = 12_000_000
EXPECTED_A16 = 2_305_787_291_293_934_388
EXPECTED_B16 = 660_663_050_386_546_968
EXPECTED_TOTAL = 2_966_450_341_680_481_356

PINS = {
    "worklist": (
        "research/experiments/n11-class2-lane-closability-ranking-20261116/"
        "output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
        "2fee1d0718547a62e346d35f5858d7913e37c097",
    ),
    "census": (
        "research/experiments/n11-head1410-receipt-unclosability-census-20261116/"
        "output/n11-head1410-receipt-unclosability-census-20261116.json",
        "9c251da3138c5cb0516e097be5e5d35ab4f26a5d",
    ),
    "ledger": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/"
        "output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
        "e8785d509e8a11a37c0d03cc450455a14708c34d",
    ),
    "cover": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/"
        "output/parent-minimum-cover-cost-table-20261118.json",
        "4e4a911d0e05779437d4a8e97685a8feb66c0d25",
    ),
    "phase_a": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/"
        "output/cost16-a-phase-20261118.json",
        "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b",
    ),
}

EXPECTED_ROWS = [
    ("00000000000000003800000008001001", 74),
    ("00000000000000003800000008001020", 65),
    ("00000000000000003800000008001080", 79),
    ("00000000000000003800000008001100", 82),
    ("00000000000000003800000008001200", 76),
    ("00000000000000003800000008001800", 73),
    ("00000000000000003800000008005000", 71),
    ("00000000000000003800000008011000", 74),
    ("00000000000000003800000008500000", 75),
    ("00000000000000003800000008900000", 76),
    ("00000000000000003800000808001000", 73),
    ("00000000000000003800200008001000", 72),
    ("00000000000000003800200008100000", 79),
    ("00000000000000043800000008100000", 84),
    ("00000000000000083800000008100000", 74),
    ("00000000000000801202000000081000", 66),
    ("00000000000000801202000000101000", 71),
    ("00000000000000801202000020001000", 74),
    ("00000000000000801202010000001000", 64),
    ("00000000000000801202020000001000", 66),
    ("00000000000000801202040000001000", 82),
    ("00000000000000801202080000001000", 79),
    ("00000000000000801212000000001000", 78),
    ("00000000000000801222000000001000", 76),
    ("00000000000000889002000000100000", 74),
    ("00000000000000909002000000100000", 79),
    ("00000000000040809002000000100000", 82),
    ("00000000010000003800000008100000", 80),
    ("00000000010000809002000000100000", 81),
    ("00000008000000003800000008100000", 81),
    ("00000010000000801202000000000400", 73),
]

N = 11
TRANSFORMS = (
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
)
TO = tuple(
    tuple(
        TRANSFORMS[k](i % N, i // N)[1] * N
        + TRANSFORMS[k](i % N, i // N)[0]
        for i in range(121)
    )
    for k in range(8)
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(name: str) -> bytes:
    rel, pin = PINS[name]
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    actual = git_blob_sha(data)
    if actual != pin:
        raise SystemExit(
            "pin mismatch for %s: expected %s got %s" % (name, pin, actual)
        )
    return data


def orbit_masks(mask: int) -> list[int]:
    out = []
    for to in TO:
        v = 0
        for i in range(121):
            if (mask >> i) & 1:
                v |= 1 << to[i]
        out.append(v)
    return out


def canon(mask: int) -> int:
    return min(orbit_masks(mask))


def det3(a: int, b: int, c: int) -> int:
    x1, y1 = a % N, a // N
    x2, y2 = b % N, b // N
    x3, y3 = c % N, c // N
    A, B, C = x1 * x1 + y1 * y1, x1, y1
    D, E, F = x2 * x2 + y2 * y2, x2, y2
    G, H, I = x3 * x3 + y3 * y3, x3, y3
    return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)


def det4(a: int, b: int, c: int, d: int) -> int:
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def derive_parent_rows(worklist: bytes, census: dict, ledger: dict):
    sterile = {x["hex"] for x in census["sterile_row_registry"]}
    closed = set(ledger["derived"]["closed_rows_66"])
    parent_orbit = set(orbit_masks(int(TARGET, 16)))
    rows = {}
    reader = csv.DictReader(worklist.decode("utf-8").splitlines())
    for rec in reader:
        h = rec["s6_canonical_hex"].strip()
        if not h or h in sterile or h in closed:
            continue
        mask = int(h, 16)
        if any(
            (mask >> b) & 1 and (mask ^ (1 << b)) in parent_orbit
            for b in range(121)
        ):
            rows[h] = int(rec["own_candidates_s6_s7_edge_cost"])
    return sorted(rows.items())


def build_graph(target_rows):
    proot_rows = defaultdict(set)
    candidate_counts = {}
    for ri, (h, expected_cost) in enumerate(target_rows):
        mask = int(h, 16)
        stones = [i for i in range(121) if (mask >> i) & 1]
        if len(stones) != 6:
            raise AssertionError((h, len(stones)))
        count = 0
        for d in range(121):
            if (mask >> d) & 1:
                continue
            legal = True
            for i in range(6):
                if not legal:
                    break
                for j in range(i + 1, 6):
                    if not legal:
                        break
                    for k in range(j + 1, 6):
                        if det4(stones[i], stones[j], stones[k], d) == 0:
                            legal = False
                            break
            if legal:
                proot_rows[canon(mask | (1 << d))].add(ri)
                count += 1
        candidate_counts[h] = count
        if count != expected_cost:
            raise AssertionError((h, count, expected_cost))

    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, covered in proot_rows.items():
        if len(covered) == 2:
            a, b = sorted(covered)
            pair_roots[(a, b)].append(root)
        elif len(covered) == 1:
            (s,) = tuple(covered)
            singleton_roots[s].append(root)
        else:
            raise AssertionError(("root covers >2 rows", root, covered))

    edge_w = {pair: len(roots) for pair, roots in pair_roots.items()}
    adj = [[] for _ in target_rows]
    for (a, b), weight in edge_w.items():
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    for row in adj:
        row.sort()
    w1 = {s: len(singleton_roots.get(s, [])) for s in range(len(target_rows))}
    return proot_rows, pair_roots, singleton_roots, edge_w, adj, w1, candidate_counts


class PmLazy:
    """Exact weighted perfect-matching count on induced row subsets."""

    def __init__(self, adj):
        self.adj = adj
        self.memo = {0: 1}

    def get(self, mask: int) -> int:
        memo = self.memo
        if mask in memo:
            return memo[mask]
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            if len(memo) + len(seen) > STATE_CAP:
                raise MemoryError(
                    "PmLazy state cap exceeded: %d + %d"
                    % (len(memo), len(seen))
                )
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            for j, _weight in self.adj[first]:
                bit = 1 << j
                if rest & bit:
                    sub = rest ^ bit
                    if sub not in memo and sub not in seen:
                        seen.add(sub)
                        stack.append(sub)
        order.sort(key=int.bit_count)
        seen.clear()
        for m in order:
            if m in memo:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            acc = 0
            for j, weight in self.adj[first]:
                bit = 1 << j
                if rest & bit:
                    acc += weight * memo[rest ^ bit]
            memo[m] = acc
        return memo[mask]


def run_shared_memo(adj, w1):
    r = len(adj)
    full = (1 << r) - 1
    pm = PmLazy(adj)
    b_rows = []
    for d in range(r):
        neighbors = adj[d]
        b_d = 0
        anchors = 0
        for i, (a, wa) in enumerate(neighbors):
            for b, wb in neighbors[i + 1:]:
                b_d += wa * wb * pm.get(
                    full ^ (1 << d) ^ (1 << a) ^ (1 << b)
                )
                anchors += 1
        degree = len(neighbors)
        if anchors != degree * (degree - 1) // 2:
            raise AssertionError(("anchor count", d, anchors, degree))
        b_rows.append({
            "double_row_index": d,
            "degree": degree,
            "anchors": anchors,
            "B_d": b_d,
            "shared_memo_states_after": len(pm.memo),
        })
    memo_after_b = len(pm.memo)
    B = sum(x["B_d"] for x in b_rows)
    a_per_row = {str(s): pm.get(full ^ (1 << s)) for s in range(r)}
    A = sum(w1[s] * a_per_row[str(s)] for s in range(r))
    memo_after_a = len(pm.memo)
    result = {
        "A": A,
        "A_per_row": a_per_row,
        "B": B,
        "B_by_d": b_rows,
        "memo_after_B": memo_after_b,
        "memo_after_A": memo_after_a,
    }
    del pm
    gc.collect()
    return result


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({
            "name": name,
            "pass": bool(ok),
            "detail": detail if isinstance(detail, str) else json.dumps(detail),
        })

    raw = {name: read_pinned(name) for name in PINS}
    worklist = raw["worklist"]
    census = json.loads(raw["census"])
    ledger = json.loads(raw["ledger"])
    cover = json.loads(raw["cover"])
    phase_a = json.loads(raw["phase_a"])

    target_rows = derive_parent_rows(worklist, census, ledger)
    check("target_rows_exact", target_rows == EXPECTED_ROWS, len(target_rows))
    check("target_rows_count", len(target_rows) == 31, len(target_rows))
    check("target_edge_cost", sum(c for _, c in target_rows) == 2333,
          sum(c for _, c in target_rows))
    tbl = {x["hex"]: x for x in cover["derived"]["table"]}[TARGET]
    check("cover_table_anchor",
          tbl["rows_r"] == 31 and tbl["candidates"] == 2333
          and tbl["distinct_roots"] == 1908 and tbl["witness_size"] == 16
          and tbl["exact"], tbl)

    graph = build_graph(target_rows)
    proot_rows, pair_roots, singleton_roots, edge_w, adj, w1, candidate_counts = graph
    hist = defaultdict(int)
    for covered in proot_rows.values():
        hist[len(covered)] += 1
    multiplicities = defaultdict(int)
    for roots in pair_roots.values():
        multiplicities[len(roots)] += 1
    check("candidate_counts_match_worklist",
          all(candidate_counts[h] == c for h, c in target_rows),
          len(candidate_counts))
    check("distinct_roots", len(proot_rows) == 1908, len(proot_rows))
    check("root_coverage_histogram",
          dict(hist) == {1: 1483, 2: 425}, dict(hist))
    check("pair_types", len(pair_roots) == 425, len(pair_roots))
    check("pair_multiplicity_one", dict(multiplicities) == {1: 425},
          dict(multiplicities))

    first = run_shared_memo(adj, w1)
    second = run_shared_memo(adj, w1)
    check("two_fresh_memo_runs_identical",
          first == second, "all A/B values, anchors and memo counts")
    check("A16_matches_published",
          first["A"] == phase_a["derived"]["type_A_total"] == EXPECTED_A16,
          str(first["A"]))
    published_per_row = phase_a["derived"]["singleton_membership_stats"]["per_row"]
    check("A16_per_row_matches_published",
          first["A_per_row"] == published_per_row,
          sum(first["A_per_row"][str(s)] == published_per_row[str(s)]
              for s in range(31)))
    check("B16_matches_checkpoint",
          first["B"] == EXPECTED_B16, str(first["B"]))
    total = first["A"] + first["B"]
    check("total_matches_checkpoint", total == EXPECTED_TOTAL, str(total))
    anchors = [x["anchors"] for x in first["B_by_d"]]
    check("B_slices_complete", len(first["B_by_d"]) == 31, len(anchors))
    check("B_anchor_range",
          min(anchors) == 276 and max(anchors) == 435,
          [min(anchors), max(anchors)])
    check("B_anchor_total", sum(anchors) == 11267, sum(anchors))
    check("memo_below_cap",
          first["memo_after_B"] < STATE_CAP
          and first["memo_after_A"] < STATE_CAP,
          [first["memo_after_B"], first["memo_after_A"]])

    row_payload = json.dumps(
        [{"row": h, "edge_cost": c} for h, c in target_rows],
        sort_keys=True, separators=(",", ":")
    ).encode()
    output = {
        "schema": "n11-cost16-parent-shared-memo-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "source_main_commit": "e5f2fab7b7004a79d6352e087c02230c5b5baf9e",
        "checkpoint_commit": "d2901d15a6bd23bb2d4096322c237c002f684bca",
        "target_parent": TARGET,
        "inputs": {
            name: {"path": PINS[name][0], "git_blob_sha1": PINS[name][1]}
            for name in sorted(PINS)
        },
        "method": (
            "The 31 target rows are selected from the pinned head-1410 worklist "
            "by D4 parent inclusion, after subtracting the pinned 66-row fold "
            "closure set and 35 STERILE rows. Candidate roots are regenerated "
            "with integer det4 and D4 canonicalization. For B, one memo is shared "
            "across all 31 doubled-row slices B_d=sum_{a<b in N(d)} "
            "w(d,a)w(d,b)pm(V\\\\{d,a,b}); this differs from the checkpoint's "
            "31 fresh-memo per-d slices while preserving the exact recurrence. "
            "A is recomputed and compared row-by-row with the pinned phase-A "
            "output. Two fresh shared-memo runs are compared."
        ),
        "derived": {
            "target_rows": [
                {"row": h, "edge_cost": c} for h, c in target_rows
            ],
            "target_row_count": len(target_rows),
            "candidate_occurrences": sum(c for _, c in target_rows),
            "distinct_D4_roots": len(proot_rows),
            "root_coverage_histogram": {
                str(k): v for k, v in sorted(hist.items())
            },
            "pair_types": len(pair_roots),
            "pair_type_multiplicity_histogram": {
                str(k): v for k, v in sorted(multiplicities.items())
            },
            "singleton_root_count": sum(w1.values()),
            "A16": first["A"],
            "A16_per_row_pm": first["A_per_row"],
            "B16": first["B"],
            "total_minimum_covers": total,
            "type_A_share": first["A"] / total,
            "type_B_share": first["B"] / total,
            "B_by_doubled_row": first["B_by_d"],
            "B_anchor_total": sum(anchors),
            "B_anchor_min": min(anchors),
            "B_anchor_max": max(anchors),
            "shared_memo_states_after_B": first["memo_after_B"],
            "shared_memo_states_after_A": first["memo_after_A"],
            "two_fresh_memo_runs_identical": first == second,
            "row_subset_sha256": hashlib.sha256(row_payload).hexdigest(),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(x["pass"] for x in checks),
        "interpretation_guard": (
            "Finite cover-plan combinatorics only. These totals count minimum "
            "certificate-cover plans for the candidate-root graph; they are "
            "not search costs, engine verdicts, WIN7-D10 certificates, or a "
            "game-theoretic value. No S5 parent was closed. REFUTED-D10 and "
            "STERILE are not LOSS proofs."
        ),
        "unknown_status": (
            "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "all_pass": output["all_pass"],
        "check_count": output["check_count"],
        "failed": [x["name"] for x in checks if not x["pass"]],
        "A16": str(first["A"]),
        "B16": str(first["B"]),
        "total": str(total),
        "memo_after_B": first["memo_after_B"],
        "memo_after_A": first["memo_after_A"],
        "output": OUT,
    }, indent=2))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
