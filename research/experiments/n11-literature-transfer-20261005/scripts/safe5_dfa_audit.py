#!/usr/bin/env python3
"""Exact finite-language compression audit for Kyouen safe 5-stone layers.

This is a deliberately small transfer experiment inspired by Jeffrey
Considine's "Compressed Game Solving" (arXiv:2411.07273).

For n=5,6,7:
  * enumerate every forbidden four-set exactly by the integer circle/line
    determinant;
  * enumerate every 5-subset and keep it iff none of its five 4-subsets is
    forbidden;
  * encode each safe 5-set as its strictly increasing point-id string;
  * build the exact prefix trie;
  * bottom-up merge equivalent suffix states.  The resulting acyclic DFA
    recognizes exactly the same finite language (a dead sink is omitted).

This is NOT yet Considine's full compressed solver: no forward/reverse set
move generation is implemented here.  It only measures whether an exact,
operation-friendly finite-state representation has enough redundancy to be
worth pursuing on Kyouen.
"""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import log
from pathlib import Path


def det3(a00, a01, a02, a10, a11, a12, a20, a21, a22):
    return (
        a00 * (a11 * a22 - a12 * a21)
        - a01 * (a10 * a22 - a12 * a20)
        + a02 * (a10 * a21 - a11 * a20)
    )


def forbidden4(ids, n):
    rows = []
    for v in ids:
        x, y = v % n, v // n
        rows.append((x * x + y * y, x, y, 1))
    answer = 0
    for col in range(4):
        z = []
        for r in range(1, 4):
            z.append([rows[r][c] for c in range(4) if c != col])
        md = det3(
            z[0][0], z[0][1], z[0][2],
            z[1][0], z[1][1], z[1][2],
            z[2][0], z[2][1], z[2][2],
        )
        answer += (1 if col % 2 == 0 else -1) * rows[0][col] * md
    return answer == 0


def audit(n):
    v = n * n
    forbidden = {
        quad for quad in combinations(range(v), 4) if forbidden4(quad, n)
    }

    # Trie nodes are dictionaries label -> child index.
    trie = [{}]
    safe_count = 0
    for s in combinations(range(v), 5):
        # A five-set is safe iff all five of its four-subsets are safe.
        if any(s[:i] + s[i + 1 :] in forbidden for i in range(5)):
            continue
        safe_count += 1
        node = 0
        for label in s:
            child = trie[node].get(label)
            if child is None:
                child = len(trie)
                trie[node][label] = child
                trie.append({})
            node = child

    # Minimize the acyclic trie by merging states with identical labelled
    # continuation languages.  All accepted strings have length five, so a
    # leaf accepting marker plus labelled child classes is sufficient.
    cls = [None] * len(trie)
    signatures = {}
    for node in range(len(trie) - 1, -1, -1):
        sig = (
            not trie[node],  # accepting leaf
            tuple(sorted((label, cls[child]) for label, child in trie[node].items())),
        )
        cid = signatures.get(sig)
        if cid is None:
            cid = len(signatures)
            signatures[sig] = cid
        cls[node] = cid

    dfa_states = len(signatures)
    return {
        "n": n,
        "forbidden_four_sets": len(forbidden),
        "safe_five_sets": safe_count,
        "trie_states": len(trie),
        "minimal_acyclic_dfa_states_without_dead_sink": dfa_states,
        "dfa_over_safe_sets": dfa_states / safe_count,
        "trie_reduction_ratio": 1.0 - dfa_states / len(trie),
        "safe_sets_per_dfa_state": safe_count / dfa_states,
        "empirical_power_log_dfa_over_log_safe": log(dfa_states) / log(safe_count),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    rows = [audit(n) for n in (5, 6, 7)]
    out = {
        "scope": "exact safe 5-stone layers on 5x5, 6x6, 7x7",
        "n11_empty_root_outcome": "UNKNOWN",
        "representation": "minimal acyclic DFA of increasing point-id strings; dead sink omitted",
        "rows": rows,
        "limitations": [
            "This measures representation redundancy only; it does not implement compressed forward/reverse move generation.",
            "Point-id ordering was not optimized. A geometry-aware variable/order choice may improve or worsen compression.",
            "The observed exponent across only n=5..7 is empirical and must not be extrapolated as a theorem.",
        ],
    }
    text = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
