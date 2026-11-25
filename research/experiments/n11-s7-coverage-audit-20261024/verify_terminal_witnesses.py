#!/usr/bin/env python3
"""Independently check S9->S8->S7 witness geometry, not S9 terminal outcomes.

The four published S9 terminal certificates are premises. Frozen S8 cache
verdicts are not premises for the 4,304 terminal-witnessed S7->S8 edges.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "n11-four-s8-joint-terminal52-20261023"))
from terminal_geometry import canonical, legal, points, safe  # noqa: E402
from analyze import BASE, S9_FILES, audit, read_keys  # noqa: E402


def check_witnesses(witnesses, roots):
    edges = set()
    for s8_hex, s9_hex in witnesses.items():
        s8, s9 = int(s8_hex, 16), int(s9_hex, 16)
        if (s9 not in roots or s8.bit_count() != 8 or s9.bit_count() != 9
                or canonical(s8) != s8 or not safe(s8) or not safe(s9)
                or not any(canonical(s9 ^ (1 << p)) == s8 for p in points(s9))):
            raise ValueError(f"invalid terminal witness: {s8_hex} -> {s9_hex}")
        for p in points(s8):
            s7 = canonical(s8 ^ (1 << p))
            edges.add((s7, s8))
    return edges


def main():
    roots = set().union(*(read_keys(p, n) for p, n in
                          zip(S9_FILES, (29, 27, 2, 10))))
    report = audit()
    witnesses = report["terminal_s8_witnesses"]
    if len(witnesses) != 538:
        raise ValueError("S8 witness count changed")
    edges = check_witnesses(witnesses, roots)
    parents = {s7 for s7, _ in edges}
    if (len(edges), len(parents)) != (4304, 1850):
        raise ValueError("independent S7 edge coverage changed")
    if report["terminal_only_secured_s7_edges"] != len(edges):
        raise ValueError("report does not match independent edge count")

    top = report["top_unclassified"][0]
    s7 = int(top["s7"], 16)
    win7 = read_keys(BASE / "all_s7_win_17.txt", 17)
    loss7 = read_keys(BASE / "all_s7_loss_2232.txt", 2232)
    if s7 in win7 or s7 in loss7:
        raise ValueError("target already has a frozen S7 verdict")
    children = {canonical(s7 | (1 << p)) for p in legal(s7)}
    certified = {s8 for parent, s8 in edges if parent == s7}
    if certified != children & {int(k, 16) for k in witnesses}:
        raise ValueError("top target certified edges mismatch")
    if (len(children), len(certified), len(children - certified)) != (36, 10, 26):
        raise ValueError("top target terminal-only 10/36 coverage changed")
    if sorted(f"{m:032x}" for m in certified) != top["terminal_s8"]:
        raise ValueError("top target witness list changed")

    # A forged S9 witness must be rejected even if its S8 key is well formed.
    bad = dict(witnesses)
    first = next(iter(bad))
    bad[first] = "0" * 32
    try:
        check_witnesses(bad, roots)
    except ValueError:
        pass
    else:
        raise ValueError("tampered witness was accepted")

    print("PASS 538 S8 witnesses, 4304 S7->S8 edges, 1850 S7 parents; "
          "unclassified target 10/36 terminal-secured, 26 missing; tamper rejected")


if __name__ == "__main__":
    main()
