#!/usr/bin/env python3
"""Independent audits for the t=3, q=3w-3 pure-fiber Grundy theorem.

The proof is in report.md. This program checks (i) both residual mex recurrences
against their closed forms, and (ii) labelled and sorted-multiset board engines
against the closed form on every safe state in the stated finite grid.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "audit.json"


def mex(values):
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n


def make_residual(z):
    @lru_cache(maxsize=None)
    def grundy(e0, e1, e2):
        L = 3 * e0 + 2 * e1 + e2
        if L == 4:
            return 0
        children = []
        if e0:
            children.append(grundy(e0 - 1, e1 + 1, e2))
        if e1:
            children.append(grundy(e0, e1 - 1, e2 + 1))
        if e2:
            children.append(z ^ grundy(e0, e1, e2 - 1))
        return mex(children)
    return grundy


def residual_formula(z, e0, e1, e2):
    L = 3 * e0 + 2 * e1 + e2
    if z == 0:
        return (L - 4) & 1
    if L == 4:
        return 0
    if L == 5:
        if (e0, e1, e2) in {(0, 1, 3), (0, 2, 1), (1, 0, 2)}:
            return 2
        if (e0, e1, e2) == (1, 1, 0):
            return 1
        return 0
    if L == 6:
        return int((e0, e1, e2) in {(0, 1, 4), (1, 1, 1)})
    if L == 7:
        if (e0, e1, e2) in {(0, 3, 1), (1, 2, 0)}:
            return 2
        if (e0, e1, e2) in {(0, 1, 5), (1, 1, 2)}:
            return 1
        return 0
    return e1 & 1


def board_formula(w, m, c):
    if m == 1:
        return (w - sum(c)) & 1
    if m == 2 and w >= 4:
        value = 0
        for x in c:
            value ^= x & 1
        return value
    if m == 2:  # w=2,3: every terminal has exactly 3w-4 stones
        return (3 * w - sum(c) - 4) & 1

    X = 0
    e0 = e1 = e2 = 0
    for x in c:
        if x >= 3:
            X ^= (m - x) & 1
        elif x == 0:
            e0 += 1
        elif x == 1:
            e1 += 1
        else:
            e2 += 1
    return X ^ residual_formula((m - 3) & 1, e0, e1, e2)


def make_board_engine(w, m, canonical):
    cap = 3 * w - 4

    @lru_cache(maxsize=None)
    def grundy(c):
        children = []
        for i, x in enumerate(c):
            if x == m:
                continue
            nxt = list(c)
            nxt[i] += 1
            if sum(min(v, 3) for v in nxt) > cap:
                continue
            nxt = tuple(sorted(nxt)) if canonical else tuple(nxt)
            children.append(grundy(nxt))
        return mex(children)

    return grundy


def audit_residual(max_L=100):
    counts = {}
    for z in (0, 1):
        engine = make_residual(z)
        checked = 0
        for L in range(4, max_L + 1):
            for e0 in range(L // 3 + 1):
                for e1 in range((L - 3 * e0) // 2 + 1):
                    e2 = L - 3 * e0 - 2 * e1
                    got = engine(e0, e1, e2)
                    expected = residual_formula(z, e0, e1, e2)
                    if got != expected:
                        raise AssertionError((z, e0, e1, e2, got, expected))
                    checked += 1
        counts[str(z)] = {"states": checked, "cache_states": engine.cache_info().currsize}
    return counts


def audit_boards():
    total = 0
    labelled_unique = 0
    canonical_unique = 0
    rows = []
    for w in range(2, 6):
        for m in range(1, 9):
            labelled = make_board_engine(w, m, False)
            canonical = make_board_engine(w, m, True)
            safe = 0
            distribution = Counter()
            cap = 3 * w - 4
            for c in product(range(m + 1), repeat=w):
                if sum(min(x, 3) for x in c) > cap:
                    continue
                expected = board_formula(w, m, c)
                gl = labelled(c)
                gc = canonical(tuple(sorted(c)))
                if gl != expected or gc != expected:
                    raise AssertionError({"w": w, "m": m, "c": c,
                                          "labelled": gl, "canonical": gc,
                                          "formula": expected})
                safe += 1
                distribution[str(gl)] += 1
            total += safe
            labelled_unique += labelled.cache_info().currsize
            canonical_unique += canonical.cache_info().currsize
            rows.append({"w": w, "m": m, "safe_states": safe,
                         "labelled_cache_states": labelled.cache_info().currsize,
                         "canonical_cache_states": canonical.cache_info().currsize,
                         "grundy_counts": dict(sorted(distribution.items(), key=lambda x: int(x[0])))})
    return {"safe_state_queries_per_engine": total,
            "labelled_unique_states": labelled_unique,
            "canonical_unique_states": canonical_unique,
            "rows": rows}


def audit_maxima(board_result):
    checks = 0
    for row in board_result["rows"]:
        w, m = row["w"], row["m"]
        observed = max(int(k) for k in row["grundy_counts"])
        if w == 2:
            expected = 1
        elif m >= 4 and m % 2 == 0:
            expected = 2 if w == 3 else 3
        else:
            expected = 1
        if observed != expected:
            raise AssertionError((w, m, observed, expected))
        checks += 1
    return checks


def main():
    residual = audit_residual()
    boards = audit_boards()
    max_checks = audit_maxima(boards)
    verifier_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    audit = {
        "theorem": "t=3, q=3w-3, pure-fiber all-safe-state Grundy classification",
        "residual": residual,
        "boards": boards,
        "maximum_checks": max_checks,
        "mismatches": 0,
        "verifier_sha256": verifier_hash,
        "scope": "finite audit only; universal validity is supplied by the induction proof in report.md",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("residual states:", sum(v["states"] for v in residual.values()))
    print("board safe-state queries per engine:", boards["safe_state_queries_per_engine"])
    print("labelled unique states:", boards["labelled_unique_states"])
    print("canonical unique states:", boards["canonical_unique_states"])
    print("maximum checks:", max_checks)
    print("mismatches: 0")
    print("verifier sha256:", verifier_hash)
    print("audit sha256:", hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
