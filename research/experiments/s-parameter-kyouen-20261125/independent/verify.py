#!/usr/bin/env python3
"""Independent exact verifier for the s-parameter kyouen game on AG(2,q).

Written from scratch for the independent-verification task.  Standard library
only.  It does *not* import the experiment's ``scripts/`` and it does *not*
read ``output/grundy_general.json``.

Game definition used here (from the task statement):
  * Board: AG(2,q), points 0..q^2-1, lines given by the board file.
  * A position is a set S of points with |S cap L| <= s for every line L.
  * A move adds one point (keeping the set safe).
  * Normal play: a player with no move LOSES.  Grundy(S) = mex of the
    Grundy values of the safe one-point extensions of S.
  * Misere play: a player with no move WINS.  misere_win(S) is True iff S is
    terminal or some move leads to a position that is a misere loss for the
    player to move.

Two canonical enumeration orders (increasing / decreasing point order) are
run and cross-compared; every enumerated set is re-checked directly against
the line definitions before the Grundy DP.

Outputs (in this directory):
  board_validation.json
  grundy_results.json
  parity_lemma_ag24_s2.json
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUTPUT = EXP / "output"

BOARD_FILES = {q: OUTPUT / f"board_ag2q{q}.txt" for q in (2, 3, 4, 5)}

CASES = [
    # (short key, q, s)
    ("AG(2,4)-s2", 4, 2),
    ("AG(2,5)-s2", 5, 2),
    ("AG(2,4)-s3", 4, 3),
]


def parse_board(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    """Parse '<n> <b>' followed by b lines '<k> p1 ... pk' (0-based points)."""
    rows = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not rows:
        raise ValueError(f"empty board file: {path}")
    head = rows[0].split()
    if len(head) != 2:
        raise ValueError(f"bad header in {path}: {rows[0]!r}")
    n, b = int(head[0]), int(head[1])
    lines: list[tuple[int, ...]] = []
    for ln in rows[1:]:
        vals = [int(x) for x in ln.split()]
        k, pts = vals[0], tuple(vals[1:])
        if len(pts) != k:
            raise ValueError(f"line length mismatch in {path}: {ln!r}")
        lines.append(pts)
    if len(lines) != b:
        raise ValueError(f"expected {b} lines in {path}, found {len(lines)}")
    return n, lines


# ---------------------------------------------------------------------------
# 1. Board validation
# ---------------------------------------------------------------------------

def validate_board(q: int, path: Path) -> dict:
    n, lines = parse_board(path)
    b = len(lines)
    lsets = [frozenset(L) for L in lines]

    checks: dict[str, dict] = {}
    problems: list[str] = []

    def check(name: str, ok: bool, detail) -> None:
        checks[name] = {"pass": bool(ok), "detail": detail}
        if not ok:
            problems.append(name)

    check("n_equals_q_squared", n == q * q, {"expected": q * q, "actual": n})
    check(
        "b_equals_q_times_q_plus_1",
        b == q * (q + 1),
        {"expected": q * (q + 1), "actual": b},
    )

    line_size_ok = all(len(L) == q and len(set(L)) == q for L in lines)
    check(
        "every_line_has_q_distinct_points",
        line_size_ok,
        {
            "line_sizes": sorted({len(L) for L in lines}),
            "all_distinct": all(len(set(L)) == len(L) for L in lines),
        },
    )

    points_ok = all(0 <= p < n for L in lines for p in L)
    check("points_in_range", points_ok, {"n": n})

    duplicate_lines = b - len(set(lsets))
    check("no_duplicate_lines", duplicate_lines == 0, {"duplicate_line_count": duplicate_lines})

    # Every pair of points on exactly one line.
    pair_counts: Counter = Counter()
    for L in lines:
        for a, c in itertools.combinations(sorted(set(L)), 2):
            pair_counts[(a, c)] += 1
    pairs_expected = n * (n - 1) // 2
    pair_ok = len(pair_counts) == pairs_expected and all(v == 1 for v in pair_counts.values())
    check(
        "every_pair_of_points_on_exactly_one_line",
        pair_ok,
        {
            "num_pairs_expected": pairs_expected,
            "num_pairs_seen": len(pair_counts),
            "max_pair_multiplicity": max(pair_counts.values()) if pair_counts else 0,
            "missing_pairs": pairs_expected - len(pair_counts),
        },
    )

    # Every point on q+1 lines.
    point_lines: list[list[int]] = [[] for _ in range(n)]
    for i, L in enumerate(lines):
        for p in set(L):
            point_lines[p].append(i)
    incidence = [len(v) for v in point_lines]
    check(
        "every_point_on_q_plus_1_lines",
        all(c == q + 1 for c in incidence),
        {
            "expected": q + 1,
            "min": min(incidence) if incidence else None,
            "max": max(incidence) if incidence else None,
            "histogram": dict(sorted(Counter(incidence).items())),
        },
    )

    # --- Additional affine-plane structure (not part of the four required
    #     checks, but a useful sanity/quality check). ---
    lsets_unique = list(dict.fromkeys(lsets))  # preserve order, drop duplicates
    m = len(lsets_unique)
    disjoint = [[False] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            d = lsets_unique[i].isdisjoint(lsets_unique[j])
            disjoint[i][j] = disjoint[j][i] = d

    parallel_classes: set[frozenset[int]] = set()
    for i in range(m):
        cls = frozenset([i] + [j for j in range(m) if disjoint[i][j]])
        parallel_classes.add(cls)
    class_sizes = sorted(len(c) for c in parallel_classes)
    parallel_classes_ok = (
        len(parallel_classes) == q + 1
        and all(size == q for size in class_sizes)
        and sum(class_sizes) == m
    )
    check(
        "additional_parallel_classes_partition",
        parallel_classes_ok,
        {
            "num_classes": len(parallel_classes),
            "class_sizes": class_sizes,
            "expected_classes": q + 1,
            "expected_class_size": q,
        },
    )

    # For a point p and a line L not through p: exactly one line through p
    # parallel to L (affine-plane parallel axiom).
    parallel_axiom_ok = True
    parallel_axiom_witness = None
    for p in range(n):
        for i, L in enumerate(lsets_unique):
            if p in L:
                continue
            cnt = sum(1 for j in point_lines[p] if lsets_unique[j].isdisjoint(L))
            if cnt != 1:
                parallel_axiom_ok = False
                parallel_axiom_witness = {"point": p, "line_index": i, "count": cnt}
                break
        if not parallel_axiom_ok:
            break
    check(
        "additional_affine_parallel_axiom",
        parallel_axiom_ok,
        {
            "rule": "for p not in L: exactly one line through p disjoint from L",
            "witness": parallel_axiom_witness,
        },
    )

    required = [
        "n_equals_q_squared",
        "b_equals_q_times_q_plus_1",
        "every_line_has_q_distinct_points",
        "points_in_range",
        "every_pair_of_points_on_exactly_one_line",
        "every_point_on_q_plus_1_lines",
    ]
    passed = all(checks[k]["pass"] for k in required)
    return {
        "q": q,
        "file": str(path.relative_to(EXP.parent.parent.parent)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "n": n,
        "b": b,
        "checks": checks,
        "required_checks": required,
        "passed": passed,
        "problems": problems,
    }


# ---------------------------------------------------------------------------
# 2. Exact enumeration / Grundy / misere analysis
# ---------------------------------------------------------------------------

def build_structure(n: int, lines: list[tuple[int, ...]], s: int):
    linemasks = []
    for L in lines:
        mask = 0
        for p in L:
            mask |= 1 << p
        linemasks.append(mask)
    point_lines: list[list[int]] = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
    return linemasks, point_lines


def enumerate_safe(n: int, lines: list[tuple[int, ...]], s: int, order: str) -> list[int]:
    """Enumerate every safe set exactly once (canonical increasing/decreasing order)."""
    _, point_lines = build_structure(n, lines, s)
    b = len(lines)
    counts = [0] * b
    out: list[int] = []

    if order == "increasing":
        def rec(start: int, mask: int) -> None:
            out.append(mask)
            for p in range(start, n):
                if (mask >> p) & 1:
                    continue
                pls = point_lines[p]
                if all(counts[li] < s for li in pls):
                    for li in pls:
                        counts[li] += 1
                    rec(p + 1, mask | (1 << p))
                    for li in pls:
                        counts[li] -= 1
        rec(0, 0)
    elif order == "decreasing":
        def rec(end: int, mask: int) -> None:
            out.append(mask)
            for p in range(end - 1, -1, -1):
                if (mask >> p) & 1:
                    continue
                pls = point_lines[p]
                if all(counts[li] < s for li in pls):
                    for li in pls:
                        counts[li] += 1
                    rec(p, mask | (1 << p))
                    for li in pls:
                        counts[li] -= 1
        rec(n, 0)
    else:
        raise ValueError(order)
    return out


def analyse(n: int, lines: list[tuple[int, ...]], s: int, masks: list[int]) -> dict:
    """Grundy + misere + maximal sets, given the complete list of safe sets."""
    b = len(lines)
    linemasks, point_lines = build_structure(n, lines, s)
    safe_set = set(masks)
    if len(safe_set) != len(masks):
        raise AssertionError("duplicate masks in enumeration")

    # Direct re-verification of safety for every enumerated set.
    unsafe = [m for m in masks if any((m & lm).bit_count() > s for lm in linemasks)]
    if unsafe:
        raise AssertionError(f"{len(unsafe)} enumerated sets are not safe")

    size = {m: m.bit_count() for m in masks}
    # Options have size+1, so process by decreasing size.
    order = sorted(masks, key=lambda m: (-size[m], m))

    grundy: dict[int, int] = {}
    misere: dict[int, bool] = {}
    maximal_by_size: Counter = Counter()
    num_options_total = 0

    for mask in order:
        # Recompute line counts of mask from scratch (no incremental state).
        cnt = [0] * b
        mm = mask
        while mm:
            low = mm & -mm
            p = low.bit_length() - 1
            for li in point_lines[p]:
                cnt[li] += 1
            mm ^= low

        opts: list[int] = []
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if all(cnt[li] < s for li in point_lines[p]):
                opts.append(mask | (1 << p))

        if not opts:
            maximal_by_size[size[mask]] += 1

        for o in opts:
            if o not in safe_set:
                raise AssertionError(f"option {o} missing from safe enumeration")
            if o not in grundy:
                raise AssertionError("option processed after superset")
        num_options_total += len(opts)

        vals = {grundy[o] for o in opts}
        g = 0
        while g in vals:
            g += 1
        grundy[mask] = g
        misere[mask] = True if not opts else any(not misere[o] for o in opts)

    # Stable hash over the full Grundy table (for independent cross-check).
    h = hashlib.sha256()
    for mask in sorted(grundy):
        h.update(f"{mask}:{grundy[mask]};".encode())
    hm = hashlib.sha256()
    for mask in sorted(misere):
        hm.update(f"{mask}:{int(misere[mask])};".encode())

    by_size = Counter(size.values())
    gdist = Counter(grundy.values())
    mdist = Counter(int(v) for v in misere.values())
    maximal_sizes = sorted(maximal_by_size)

    return {
        "safe_count": len(masks),
        "safe_by_size": {int(k): int(v) for k, v in sorted(by_size.items())},
        "maximal_by_size": {int(k): int(v) for k, v in sorted(maximal_by_size.items())},
        "num_maximal": int(sum(maximal_by_size.values())),
        "maximal_sizes": maximal_sizes,
        "maximal_parities": sorted({sz % 2 for sz in maximal_sizes}),
        "grundy_empty": int(grundy[0]),
        "misere_empty": int(bool(misere[0])),
        "misere_distribution": {int(k): int(v) for k, v in sorted(mdist.items())},
        "grundy_distribution": {int(k): int(v) for k, v in sorted(gdist.items())},
        "max_grundy": int(max(gdist)),
        "num_options_total": num_options_total,
        "grundy_sha256": h.hexdigest(),
        "misere_sha256": hm.hexdigest(),
    }


# ---------------------------------------------------------------------------
# 3. Parity-graded lemma check (see main)
# ---------------------------------------------------------------------------

def main() -> int:
    started = time.perf_counter()

    board_validation = {
        "generated_by": "independent/verify.py",
        "description": "Validation of output/board_ag2q{2,3,4,5}.txt as AG(2,q) boards.",
        "boards": {},
    }
    for q in (2, 3, 4, 5):
        path = BOARD_FILES[q]
        t0 = time.perf_counter()
        res = validate_board(q, path)
        res["validation_seconds"] = round(time.perf_counter() - t0, 6)
        board_validation["boards"][f"AG(2,{q})"] = res
        status = "PASS" if res["passed"] else "FAIL"
        print(f"board AG(2,{q}): {status}  n={res['n']} b={res['b']}  problems={res['problems']}")

    board_validation["all_passed"] = all(b["passed"] for b in board_validation["boards"].values())

    results: dict[str, dict] = {
        "generated_by": "independent/verify.py",
        "conventions": {
            "normal_play": "player with no move loses; Grundy = mex of option Grundy values",
            "misere_play": "player with no move wins; misere_win = terminal OR exists option "
                           "that is a misere loss for the opponent",
            "maximal_safe_set": "no single point can be added while remaining safe",
            "grundy_distribution": "number of safe sets per Grundy value over all safe sets",
        },
        "cases": {},
    }

    grundy_tables: dict[str, tuple[int, int, dict[int, int], dict[int, bool]]] = {}

    for key, q, s in CASES:
        n, lines = parse_board(BOARD_FILES[q])
        print(f"\n{key}: enumerating safe sets (n={n}, b={len(lines)}, s={s}) ...")
        t0 = time.perf_counter()
        inc = enumerate_safe(n, lines, s, "increasing")
        t_inc = time.perf_counter() - t0
        t0 = time.perf_counter()
        dec = enumerate_safe(n, lines, s, "decreasing")
        t_dec = time.perf_counter() - t0
        inc_sorted = sorted(inc)
        dec_sorted = sorted(dec)
        orders_agree = inc_sorted == dec_sorted
        print(f"  increasing order: {len(inc):,} sets ({t_inc:.2f}s); "
              f"decreasing order: {len(dec):,} sets ({t_dec:.2f}s); agree={orders_agree}")

        t0 = time.perf_counter()
        res = analyse(n, lines, s, inc)
        t_dp = time.perf_counter() - t0
        res.update(
            {
                "q": q,
                "s": s,
                "n": n,
                "b": len(lines),
                "board_file": str(BOARD_FILES[q].relative_to(EXP.parent.parent.parent)),
                "enumeration_orders_agree": orders_agree,
                "enumeration_seconds_increasing": round(t_inc, 3),
                "enumeration_seconds_decreasing": round(t_dec, 3),
                "grundy_dp_seconds": round(t_dp, 3),
            }
        )
        results["cases"][key] = res
        print(f"  safe={res['safe_count']:,}  maximal={res['maximal_by_size']}  "
              f"G(empty)={res['grundy_empty']}  misere(empty)={res['misere_empty']}  "
              f"Gdist={res['grundy_distribution']}  ({t_dp:.2f}s DP)")

        # Rebuild the tables for the parity lemma check.  (analyse returns only
        # aggregates to keep grundy_results.json small.)
        tables = grundy_and_misere_tables(n, lines, s, inc)
        grundy_tables[key] = (n, s, tables["grundy"], tables["misere"])

    # Parity lemma on AG(2,4), s=2.
    key = "AG(2,4)-s2"
    n, s, grundy, misere = grundy_tables[key]
    res = results["cases"][key]
    maximal_sizes = res["maximal_sizes"]
    parities = res["maximal_parities"]
    lemma: dict = {
        "generated_by": "independent/verify.py",
        "case": key,
        "statement": "all maximal safe sets have the same parity p => Grundy(S) = (p - |S|) mod 2 for every safe S",
        "maximal_sizes": maximal_sizes,
        "maximal_size_counts": {str(k): v for k, v in res["maximal_by_size"].items()},
        "parity_uniform": len(parities) == 1,
        "p": parities[0] if len(parities) == 1 else None,
        "num_safe_sets_checked": len(grundy),
        "violations": 0,
        "violation_examples": [],
        "grundy_values": [],
        "size_parity_counts": {},
        "grundy_distribution_equals_size_parity": False,
    }
    lemma["grundy_values"] = sorted(set(grundy.values()))
    if len(parities) == 1:
        p = parities[0]
        for mask, g in grundy.items():
            expected = (p - mask.bit_count()) % 2
            if g != expected:
                lemma["violations"] += 1
                if len(lemma["violation_examples"]) < 10:
                    lemma["violation_examples"].append(
                        {"mask": mask, "size": mask.bit_count(), "grundy": g, "formula": expected}
                    )
        spc: Counter = Counter(mask.bit_count() % 2 for mask in grundy)
        lemma["size_parity_counts"] = {int(k): int(v) for k, v in sorted(spc.items())}
        lemma["formula_holds_for_every_safe_set"] = lemma["violations"] == 0
        lemma["grundy_distribution_equals_size_parity"] = (
            {0: lemma["size_parity_counts"].get(0, 0), 1: lemma["size_parity_counts"].get(1, 0)}
            == res["grundy_distribution"]
        )
        lemma["p"] = p
        print(f"\nparity lemma {key}: p={p}, checked {len(grundy):,} safe sets, "
              f"violations={lemma['violations']}, "
              f"G-dist==size-parity-counts: {lemma['grundy_distribution_equals_size_parity']}")
    else:
        lemma["formula_holds_for_every_safe_set"] = None
        lemma["note"] = "precondition false: maximal sizes have mixed parity"

    # Also record parity status for the other two cases (lemma not applicable).
    lemma["other_cases"] = {}
    for other in ("AG(2,5)-s2", "AG(2,4)-s3"):
        r = results["cases"][other]
        lemma["other_cases"][other] = {
            "maximal_sizes": r["maximal_sizes"],
            "parity_uniform": len(r["maximal_parities"]) == 1,
            "grundy_distribution": r["grundy_distribution"],
            "grundy_two_present": r["grundy_distribution"].get(2, 0) > 0,
        }

    # --- write JSONs ---
    with open(HERE / "board_validation.json", "w", encoding="utf-8") as f:
        json.dump(board_validation, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(HERE / "grundy_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(HERE / "parity_lemma_ag24_s2.json", "w", encoding="utf-8") as f:
        json.dump(lemma, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"\ntotal elapsed: {time.perf_counter() - started:.2f}s")
    print("wrote board_validation.json, grundy_results.json, parity_lemma_ag24_s2.json")
    return 0


def grundy_and_misere_tables(
    n: int, lines: list[tuple[int, ...]], s: int, masks: list[int]
) -> dict[str, dict]:
    """Rebuild full Grundy/misere tables (same algorithm as analyse)."""
    b = len(lines)
    _, point_lines = build_structure(n, lines, s)
    safe_set = set(masks)
    order = sorted(masks, key=lambda m: (-m.bit_count(), m))
    grundy: dict[int, int] = {}
    misere: dict[int, bool] = {}
    for mask in order:
        cnt = [0] * b
        mm = mask
        while mm:
            low = mm & -mm
            p = low.bit_length() - 1
            for li in point_lines[p]:
                cnt[li] += 1
            mm ^= low
        opts = []
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if all(cnt[li] < s for li in point_lines[p]):
                o = mask | (1 << p)
                if o not in safe_set:
                    raise AssertionError("option not safe")
                opts.append(o)
        vals = {grundy[o] for o in opts}
        g = 0
        while g in vals:
            g += 1
        grundy[mask] = g
        misere[mask] = True if not opts else any(not misere[o] for o in opts)
    return {"grundy": grundy, "misere": misere}


if __name__ == "__main__":
    sys.exit(main())
