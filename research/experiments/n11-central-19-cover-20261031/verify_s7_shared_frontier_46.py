#!/usr/bin/env python3
"""Independent 4x4-integer geometry audit of S7 sharing in the conditional 46-S6 plan.

This only counts proof obligations. Historical solver-trusted LOSS7 labels are
compared as cache evidence, never promoted to independently checked verdicts.
"""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
BASE = EXP / "n11-targeted-terminal-lift-20261015" / "data"
CERT = HERE / "conditional_s6_cover_46.json"
LIFT = EXP / "n11-s8-fixed37-terminal-closure-20261030" / "lift_result.json"
BLOBS = {
    CERT: "bbeb4fb13b6b881b8b1d6528170d678edb58fadd",
    BASE / "all_s7_loss_2232.txt": "e2b8fc243422751ce048302a3ed65df1ef7e5211",
    BASE / "all_s7_win_17.txt": "677e962f3f70be73abcd77037df8822880927b22",
    LIFT: "f8e335cd8fafec9d98745e89cb207d4e31c220be",
}
N, V = 11, 121
XY = [(p % N, p // N) for p in range(V)]
D4 = []
for mode in range(8):
    row = []
    for x, y in XY:
        u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[mode]
        row.append(11*v + u)
    D4.append(row)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def frozen(path):
    data = path.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    need(sha == BLOBS[path], f"frozen input changed: {path}")
    return data.decode("utf-8")


def decode(k, count):
    need(isinstance(k, str) and len(k) == 32 and
         all(c in "0123456789abcdef" for c in k), "bad hex key")
    m = int(k, 16)
    need(m.bit_count() == count and m >> V == 0, "bad stone count or board")
    return m


def points(m):
    return [p for p in range(V) if (m >> p) & 1]


def canonical(m):
    ps = points(m)
    return min(sum(1 << t[p] for p in ps) for t in D4)


def determinant4(rows):
    # Fraction-free Bareiss on the full 4x4 matrix, independent of the
    # existing 3x3-difference determinant used by the cover verifier.
    a = [row[:] for row in rows]
    sign, prev = 1, 1
    for k in range(3):
        if not a[k][k]:
            j = next((j for j in range(k+1, 4) if a[j][k]), None)
            if j is None:
                return 0
            a[k], a[j] = a[j], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = a[i][j]*pivot - a[i][k]*a[k][j]
                need(numerator % prev == 0, "nonintegral Bareiss step")
                a[i][j] = numerator // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[3][3]


def forbidden(a, b, c, d):
    rows = []
    for p in (a, b, c, d):
        x, y = XY[p]
        rows.append([x*x+y*y, x, y, 1])
    return determinant4(rows) == 0


def children(m):
    triples = tuple(combinations(points(m), 3))
    return [m | (1 << p) for p in range(V)
            if not (m >> p) & 1 and
            all(not forbidden(a, b, c, p) for a, b, c in triples)]


def inventory(path, expected):
    keys = frozen(path).splitlines()
    need(len(keys) == expected and keys == sorted(set(keys)), "bad S7 inventory")
    for k in keys:
        m = decode(k, 7)
        need(canonical(m) == m, "noncanonical S7 inventory")
    return set(keys)


def audit():
    cert = json.loads(frozen(CERT))
    need(cert["schema"] == "n11-central49-priority-s4-conditional-s6-cover-v1"
         and cert["evidence_level"] == "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and cert["s4_outcome"] == cert["root_outcome"]
         == cert["empty_board_outcome"] == "UNKNOWN",
         "conditional certificate identity or outcome changed")
    selected = cert["selected_s6_classes"]
    need(len(selected) == 46 and selected == sorted(set(selected)),
         "invalid selected S6 classes")
    incidence = defaultdict(set)
    raw = within = 0
    local_children = []
    for i, k in enumerate(selected):
        m = decode(k, 6)
        need(canonical(m) == m, "noncanonical S6")
        cs = children(m)
        raw += len(cs)
        keys = {f"{canonical(s):032x}" for s in cs}
        within += len(keys)
        local_children.append(keys)
        for key in keys:
            incidence[key].add(i)
    histogram = Counter(map(len, incidence.values()))
    need(raw == within == cert["selected_s6_total_raw_s7_edges"] == 2897
         and len(incidence) == 2737 and histogram == {1: 2577, 2: 160},
         "S7-sharing geometry changed")

    old_loss = inventory(BASE / "all_s7_loss_2232.txt", 2232)
    old_win = inventory(BASE / "all_s7_win_17.txt", 17)
    need(not (old_loss & old_win), "frozen WIN7/LOSS7 conflict")
    lift = json.loads(frozen(LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "fixed14 lift identity changed")
    # lift_result labels side-to-move; at odd S7, WIN means original-first LOSS.
    new_loss = {r["s7"] for r in lift["rows"] if r["verdict"] == "WIN"}
    new_win = {r["s7"] for r in lift["rows"] if r["verdict"] == "LOSS"}
    need(len(lift["rows"]) == 14 and len(new_loss) == 13
         and len(new_win) == 1 and not ((old_loss | new_loss) & (old_win | new_win)),
         "fixed14 polarity, duplicate or outcome conflict")
    all_keys = set(incidence)
    cache_hits = all_keys & old_loss
    terminal_hits = all_keys & new_loss
    known_win = all_keys & (old_win | new_win)
    need((len(cache_hits), len(terminal_hits), len(known_win)) == (8, 0, 0),
         "S7 evidence intersection changed")
    need(Counter(len(keys & cache_hits) for keys in local_children)
         == {0: 42, 2: 4}, "cached LOSS7 distribution changed")
    return {
        "schema": "n11-central49-conditional46-s7-sharing-audit-v1",
        "empty_board_outcome": "UNKNOWN",
        "selected_s6_outcomes": "UNKNOWN",
        "selected_s6": 46,
        "raw_s6_to_s7_edges": raw,
        "canonical_s7_edges_within_each_s6": within,
        "distinct_s7_classes": len(all_keys),
        "s7_parent_multiplicity": {str(k): v for k, v in sorted(histogram.items())},
        "shared_s7_obligations_avoided": raw - len(all_keys),
        "frozen_solver_trusted_loss7_hits": len(cache_hits),
        "fixed14_terminal_backed_loss7_hits": len(terminal_hits),
        "known_win7_hits": len(known_win),
        "s7_not_in_these_inventories": len(all_keys - old_loss - old_win - new_loss - new_win),
        "minimum_s7_children_per_s6": min(map(len, local_children)),
        "maximum_s7_children_per_s6": max(map(len, local_children)),
        "cached_loss7_keys": sorted(cache_hits),
        "evidence_limit": "No S6 outcome is established. The 2232 LOSS7 labels are not independently terminal-reproved."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
