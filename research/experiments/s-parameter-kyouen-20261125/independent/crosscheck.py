#!/usr/bin/env python3
"""Independent cross-check of independent/verify.py by two different methods.

Method A (n = 16 boards): brute force the ENTIRE powerset 0..2^n-1, test
safety directly from the line definitions (mask & line).bit_count() <= s, and
compute Grundy / misere by DP over the resulting safe-flag table using safe-set
membership only (no incremental line counts, no DFS).

Method B (AG(2,5), n = 25, s = 2): enumerate subsets by increasing size with
itertools.combinations until the first size level containing no safe set.
Because every subset of a safe set is safe, an empty level proves completeness.
Then DP as in Method A.

Both methods write a SHA-256 over the full Grundy table and over the full
misere table; these hashes are compared with the ones in grundy_results.json
(produced by verify.py, a different algorithm: canonical DFS + incremental
line counts + DP in decreasing size order).

Output: crosscheck.json
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


def parse_board(path: Path):
    rows = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    head = rows[0].split()
    n, b = int(head[0]), int(head[1])
    lines = []
    for ln in rows[1:]:
        vals = [int(x) for x in ln.split()]
        k = vals[0]
        pts = tuple(vals[1:])
        assert len(pts) == k
        lines.append(pts)
    assert len(lines) == b
    return n, lines


def linemasks_of(n: int, lines) -> tuple[int, ...]:
    out = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        out.append(m)
    return tuple(out)


def is_safe(mask: int, linemasks: tuple[int, ...], s: int) -> bool:
    for lm in linemasks:
        if (mask & lm).bit_count() > s:
            return False
    return True


def mex(values) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def analyse_from_membership(n: int, safe_set: set[int]) -> dict:
    """Grundy / misere from a complete safe-set membership oracle."""
    order = sorted(safe_set, key=lambda m: (-m.bit_count(), m))
    grundy: dict[int, int] = {}
    misere: dict[int, bool] = {}
    maximal: Counter = Counter()
    for mask in order:
        opts = []
        for p in range(n):
            if (mask >> p) & 1:
                continue
            o = mask | (1 << p)
            if o in safe_set:
                opts.append(o)
        if not opts:
            maximal[mask.bit_count()] += 1
        vals = {grundy[o] for o in opts}
        grundy[mask] = mex(vals)
        misere[mask] = True if not opts else any(not misere[o] for o in opts)

    hg = hashlib.sha256()
    for mask in sorted(grundy):
        hg.update(f"{mask}:{grundy[mask]};".encode())
    hm = hashlib.sha256()
    for mask in sorted(misere):
        hm.update(f"{mask}:{int(misere[mask])};".encode())

    by_size = Counter(m.bit_count() for m in safe_set)
    gdist = Counter(grundy.values())
    mdist = Counter(int(v) for v in misere.values())
    return {
        "safe_count": len(safe_set),
        "safe_by_size": {int(k): int(v) for k, v in sorted(by_size.items())},
        "maximal_by_size": {int(k): int(v) for k, v in sorted(maximal.items())},
        "grundy_empty": int(grundy[0]),
        "misere_empty": int(bool(misere[0])),
        "misere_distribution": {int(k): int(v) for k, v in sorted(mdist.items())},
        "grundy_distribution": {int(k): int(v) for k, v in sorted(gdist.items())},
        "grundy_sha256": hg.hexdigest(),
        "misere_sha256": hm.hexdigest(),
        # full table kept for the parity lemma check (not serialised)
        "_grundy": grundy,
    }


def powerset_method(n: int, lines, s: int) -> dict:
    """Method A: direct test of all 2^n subsets."""
    linemasks = linemasks_of(n, lines)
    t0 = time.perf_counter()
    safe: set[int] = set()
    for mask in range(1 << n):
        if is_safe(mask, linemasks, s):
            safe.add(mask)
    t_scan = time.perf_counter() - t0
    t0 = time.perf_counter()
    out = analyse_from_membership(n, safe)
    out["method"] = "powerset-brute-force"
    out["subsets_scanned"] = 1 << n
    out["scan_seconds"] = round(t_scan, 3)
    out["dp_seconds"] = round(time.perf_counter() - t0, 3)
    out["completeness"] = "all 2^n subsets tested directly"
    out["_safe"] = safe
    return out


def combinations_method(n: int, lines, s: int) -> dict:
    """Method B: direct test of all subsets by increasing size until empty level."""
    linemasks = linemasks_of(n, lines)
    t0 = time.perf_counter()
    safe: set[int] = set()
    level_counts: dict[int, int] = {}
    k = 0
    scanned = 0
    while True:
        found = 0
        for comb in itertools.combinations(range(n), k):
            mask = 0
            for p in comb:
                mask |= 1 << p
            scanned += 1
            if is_safe(mask, linemasks, s):
                safe.add(mask)
                found += 1
        level_counts[k] = found
        if found == 0:
            break
        k += 1
    empty_level = k
    t_scan = time.perf_counter() - t0
    t0 = time.perf_counter()
    out = analyse_from_membership(n, safe)
    out["method"] = "combinations-by-size"
    out["subsets_scanned"] = scanned
    out["scan_seconds"] = round(t_scan, 3)
    out["dp_seconds"] = round(time.perf_counter() - t0, 3)
    out["level_counts"] = {int(kk): int(vv) for kk, vv in sorted(level_counts.items())}
    out["first_empty_level"] = empty_level
    out["completeness"] = (
        f"level {empty_level} contained no safe set; every subset of a safe set is safe, "
        "so no safe set of size >= that level exists"
    )
    out["_safe"] = safe
    return out


def compare_with_verify(case_key: str, cross: dict) -> dict:
    with open(HERE / "grundy_results.json", encoding="utf-8") as f:
        ver = json.load(f)["cases"][case_key]
    fields = [
        "safe_count",
        "safe_by_size",
        "maximal_by_size",
        "grundy_empty",
        "misere_empty",
        "misere_distribution",
        "grundy_distribution",
        "grundy_sha256",
        "misere_sha256",
    ]
    diffs = {}
    for field in fields:
        ver_val = ver.get(field)
        cross_val = cross.get(field)
        if isinstance(ver_val, dict):
            ver_val = {int(k): v for k, v in ver_val.items()}
        if cross_val != ver_val:
            diffs[field] = {"crosscheck": cross_val, "verify": ver_val}
    return {
        "case": case_key,
        "fields_compared": fields,
        "matches_verify": not diffs,
        "diffs": diffs,
        "crosscheck_misere_sha256": cross.get("misere_sha256"),
        "note": "full Grundy and misere tables compared via SHA-256 hashes",
    }


def parity_check(n: int, safe_set: set[int], grundy: dict[int, int], maximal: dict) -> dict:
    max_sizes = sorted(maximal)
    parities = sorted({sz % 2 for sz in max_sizes})
    out = {
        "maximal_sizes": max_sizes,
        "parity_uniform": len(parities) == 1,
        "p": parities[0] if len(parities) == 1 else None,
        "checked": 0,
        "violations": 0,
        "examples": [],
    }
    if len(parities) == 1:
        p = parities[0]
        for mask, g in grundy.items():
            out["checked"] += 1
            if g != (p - mask.bit_count()) % 2:
                out["violations"] += 1
                if len(out["examples"]) < 10:
                    out["examples"].append(
                        {"mask": mask, "size": mask.bit_count(), "grundy": g}
                    )
    return out


def main() -> int:
    started = time.perf_counter()
    cases = [
        ("AG(2,4)-s2", 4, 2, "powerset"),
        ("AG(2,4)-s3", 4, 3, "powerset"),
        ("AG(2,5)-s2", 5, 2, "combinations"),
    ]
    out: dict = {
        "generated_by": "independent/crosscheck.py",
        "description": "Second, algorithmically different computation compared with verify.py",
        "cases": {},
    }
    for key, q, s, method in cases:
        n, lines = parse_board(BOARD_FILES[q])
        print(f"{key}: method={method} ...")
        if method == "powerset":
            cross = powerset_method(n, lines, s)
        else:
            cross = combinations_method(n, lines, s)
        grundy_table = cross.pop("_grundy")
        safe_set = cross.pop("_safe")
        safe_count = cross["safe_count"]
        assert len(safe_set) == safe_count
        cmp = compare_with_verify(key, cross)
        par = parity_check(n, safe_set, grundy_table, cross["maximal_by_size"])
        cross["comparison_with_verify"] = cmp
        cross["parity_lemma_check"] = par
        cross["safe_by_size_total"] = sum(cross["safe_by_size"].values())
        out["cases"][key] = cross
        print(
            f"  safe={cross['safe_count']:,} maximal={cross['maximal_by_size']} "
            f"Gdist={cross['grundy_distribution']} G(empty)={cross['grundy_empty']} "
            f"misere={cross['misere_empty']} | matches verify: {cmp['matches_verify']}"
        )
        if not cmp["matches_verify"]:
            print(f"  DIFFS: {json.dumps(cmp['diffs'], sort_keys=True)}")
        if par["parity_uniform"]:
            print(f"  parity p={par['p']} checked={par['checked']:,} violations={par['violations']}")

    out["all_match_verify"] = all(
        c["comparison_with_verify"]["matches_verify"] for c in out["cases"].values()
    )
    out["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    with open(HERE / "crosscheck.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"\nall match verify: {out['all_match_verify']}  ({out['elapsed_seconds']}s)")
    print("wrote crosscheck.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
