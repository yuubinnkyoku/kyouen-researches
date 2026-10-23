#!/usr/bin/env python3
"""Rank S7 certificate gaps from frozen S8 cache and independently certified S9 roots.

All WIN/LOSS labels use the *original first player's* viewpoint.  This is a
coverage audit, NOT a new S7 certificate: the frozen S8 cache has a separate
trust boundary.  UNKNOWN means 'not covered by the selected inputs'.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

EXP = Path(__file__).resolve().parents[1]
BASE = EXP / "n11-targeted-terminal-lift-20261015" / "data"
S9_FILES = [
    EXP / "n11-s9-win29-lift-20261023" / "s9-win29.keys",
    EXP / "n11-s9-win27-expansion-20261024" / "s9-win27.keys",
    EXP / "n11-s9-win2-followup-20261024" / "s9-win2.keys",
    EXP / "n11-s9-win10-20261024" / "s9-win10.keys",
]
ALL = (1 << 121) - 1
BIT = [1 << i for i in range(121)]
XY = [(p % 11, p // 11) for p in range(121)]
D4 = []
for transform in range(8):
    positions = []
    for x, y in XY:
        xx, yy = (
            (x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
            (10-x, y), (10-y, 10-x), (x, 10-y), (y, x)
        )[transform]
        positions.append(1 << (11 * yy + xx))
    D4.append(positions)


def points(board: int) -> list[int]:
    result = []
    while board:
        bit = board & -board
        result.append(bit.bit_length() - 1)
        board ^= bit
    return result


@lru_cache(maxsize=None)
def canonical(board: int) -> int:
    ps = points(board)
    return min(sum(t[p] for p in ps) for t in D4)


@lru_cache(maxsize=None)
def forbidden_by_triple(a: int, b: int, c: int) -> int:
    # Exact integer equation A*x + B*y + C*(x*x+y*y) + D = 0.
    # Also handles collinear triples: C=0, leaving their forbidden line.
    x0, y0 = XY[a]
    x1, y1 = XY[b]
    x2, y2 = XY[c]
    z0 = x0*x0 + y0*y0
    u = (x1-x0, y1-y0, x1*x1+y1*y1-z0)
    v = (x2-x0, y2-y0, x2*x2+y2*y2-z0)
    A = u[1]*v[2] - u[2]*v[1]
    B = u[2]*v[0] - u[0]*v[2]
    C = u[0]*v[1] - u[1]*v[0]
    D = -A*x0 - B*y0 - C*z0
    return sum(BIT[p] for p, (x, y) in enumerate(XY)
               if A*x + B*y + C*(x*x+y*y) + D == 0)


def legal_points(board: int) -> list[int]:
    blocked = board
    for triple in combinations(points(board), 3):
        blocked |= forbidden_by_triple(*triple)
    return points(ALL ^ blocked)


def read_keys(path: Path, count: int) -> set[int]:
    raw = path.read_text(encoding="utf-8").splitlines()
    if len(raw) != count or raw != sorted(set(raw)):
        raise ValueError(f"count/order/duplicate mismatch: {path}")
    if any(len(k) != 32 or set(k) - set("0123456789abcdef") for k in raw):
        raise ValueError(f"bad canonical key: {path}")
    values = {int(k, 16) for k in raw}
    if any(canonical(m) != m for m in values):
        raise ValueError(f"noncanonical key: {path}")
    return values


def hexdigest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict:
    s9 = set().union(*(read_keys(p, n) for p, n in zip(S9_FILES, (29, 27, 2, 10))))
    if len(s9) != 68 or any(m.bit_count() != 9 for m in s9):
        raise ValueError("68 S9 roots changed")
    old8 = read_keys(BASE / "lifted_s8_win_51571.txt", 13501)
    loss8 = read_keys(BASE / "all_s8_loss_294.txt", 294)
    win7 = read_keys(BASE / "all_s7_win_17.txt", 17)
    loss7 = read_keys(BASE / "all_s7_loss_2232.txt", 2232)
    if old8 & loss8 or win7 & loss7:
        raise ValueError("frozen WIN/LOSS conflict")
    lifted8 = {canonical(m ^ BIT[p]) for m in s9 for p in points(m)}
    if lifted8 & loss8:
        raise ValueError("new S8 WIN / known S8 LOSS conflict")
    secured8 = old8 | lifted8
    candidates7 = {canonical(m ^ BIT[p]) for m in lifted8 for p in points(m)}
    rows = []
    total_gain = 0
    improved = 0
    closed = []
    for m in sorted(candidates7):
        child8 = {canonical(m | BIT[p]) for p in legal_points(m)}
        old_covered = len(child8 & old8)
        covered = len(child8 & secured8)
        missing = sorted(child8 - secured8)
        gain = covered - old_covered
        total_gain += gain
        improved += (gain > 0)
        label = ("frozen-WIN" if m in win7 else
                 "frozen-LOSS" if m in loss7 else "not-in-frozen-S7")
        if not missing:
            closed.append((m, label))
            if label != "frozen-WIN":
                raise ValueError("new S7 closure or conflicting S7 LOSS: audit separately")
        rows.append({
            "s7": f"{m:032x}", "label": label, "children": len(child8),
            "old_secured": old_covered, "secured": covered,
            "gain": gain, "uncovered": len(missing),
            "missing_s8": [f"{v:032x}" for v in missing],
        })
    rows.sort(key=lambda r: (r["uncovered"], -r["secured"], r["s7"]))
    target = [r for r in rows if r["label"] == "not-in-frozen-S7"]
    summary = {
        "schema": "n11-s7-certificate-gap-audit-v1",
        "outcome": "UNKNOWN",
        "trust": "frozen S8 WIN is cache-derived; lifted S8 WIN depends on the four S9 terminal certificates; S7 gaps are coverage only",
        "inputs_sha256": {str(p.relative_to(EXP)): hexdigest(p)
                          for p in S9_FILES + [
                              BASE / "lifted_s8_win_51571.txt",
                              BASE / "all_s8_loss_294.txt",
                              BASE / "all_s7_win_17.txt",
                              BASE / "all_s7_loss_2232.txt"]},
        "s9_roots": len(s9), "lifted_s8": len(lifted8),
        "new_s8_vs_frozen": len(lifted8 - old8),
        "secured_s8_union": len(secured8),
        "s7_candidates": len(candidates7),
        "s7_unclassified_in_frozen": len(target),
        "s7_closed_already_known": len(closed),
        "improved_s7_candidates": improved,
        "additional_secured_s7_edges": total_gain,
        "top_unclassified": target[:10],
    }
    expected = (538, 505, 14006, 1850, 1833, 2, 1773, 4040)
    actual = (summary[k] for k in (
        "lifted_s8", "new_s8_vs_frozen", "secured_s8_union",
        "s7_candidates", "s7_unclassified_in_frozen",
        "s7_closed_already_known", "improved_s7_candidates",
        "additional_secured_s7_edges"))
    if tuple(actual) != expected:
        raise ValueError("frozen coverage metrics changed")
    if target[0]["s7"] != "00000000100000021081000020000020" or target[0]["uncovered"] != 26:
        raise ValueError("top target changed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="write deterministic JSON manifest")
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
