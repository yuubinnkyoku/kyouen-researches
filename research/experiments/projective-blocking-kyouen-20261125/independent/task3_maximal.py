"""Task 3: independent DFS enumeration of all maximal safe sets, q = 3, 4.

Verifies
  * the total number of safe sets (4330 / 180058),
  * the maximal-safe-set size counts (q=3: {7:234, 9:13}; q=4: {7:360, 9:11480}),
  * for q=4 the complement line profiles of the two size classes
    (size 9 -> 12-point complement with profile {2:10,3:6,4:3,5:2};
     size 7 -> 14-point complement with profile {2:7,4:14}),
  * that every complement is an inclusion-minimal (q-2)-fold blocking set
    (q=3: ordinary blocking set; q=4: 2-fold blocking set),
  * that every maximal safe set really admits no extension.
"""

from __future__ import annotations

import json
import os
import time

from common import (
    Board,
    bits,
    complement_profiles,
    is_inclusion_minimal_d_fold,
    read_board,
    size_histogram,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)

CLAIMED_MAXIMAL = {
    3: {7: 234, 9: 13},
    4: {7: 360, 9: 11480},
}
CLAIMED_SAFE = {3: 4330, 4: 180058}
CLAIMED_PROFILES_Q4 = {
    9: {(2, 10), (3, 6), (4, 3), (5, 2)},
    7: {(2, 7), (4, 14)},
}


def analyse(q):
    path = os.path.join(BASE, "output", f"board_pg2q{q}.txt")
    n, blocks = read_board(path)
    board = Board(n, blocks, cap=3)
    t0 = time.time()
    sizes, _by_size, maximal = board.enumerate_safe(collect=False)
    elapsed = time.time() - t0
    safe_total = sum(sizes)
    maximal_hist = size_histogram(maximal)
    profiles = complement_profiles(board, maximal)

    # every maximal set really has no safe extension (recheck point by point)
    no_extension_ok = True
    for s in maximal:
        complement = ((1 << n) - 1) ^ s
        for p in bits(complement):
            if board.safe(s | (1 << p)):
                no_extension_ok = False
                break
        if not no_extension_ok:
            break

    # every complement is an inclusion-minimal (q-2)-fold blocking set
    d = q - 2
    minimal_ok = True
    minimal_note = ""
    for s in maximal:
        complement = ((1 << n) - 1) ^ s
        ok, note = is_inclusion_minimal_d_fold(board, complement, d)
        if not ok:
            minimal_ok = False
            minimal_note = note
            break

    # profile details per size class
    profile_detail = {}
    for k, prof_map in sorted(profiles.items()):
        profile_detail[k] = {
            "num_sets": sum(prof_map.values()),
            "distinct_profiles": [
                {"profile": {int(a): int(b) for a, b in prof},
                 "count": cnt}
                for prof, cnt in sorted(prof_map.items())
            ],
        }
        uniform = len(prof_map) == 1
        profile_detail[k]["uniform"] = uniform

    # arithmetic identity per profile: sum_s s * (#blocks with load s) = |X|*(q+1)
    identity_ok = True
    for k, prof_map in profiles.items():
        xsize = n - k
        for prof in prof_map:
            total = sum(sz * cnt for sz, cnt in prof)
            if total != xsize * (q + 1):
                identity_ok = False

    result = {
        "q": q,
        "n": n,
        "blocks": len(board.block_masks),
        "safe_by_size": {int(k): int(v) for k, v in enumerate(sizes) if v},
        "safe_total": safe_total,
        "maximal_by_size": maximal_hist,
        "maximal_total": len(maximal),
        "dfs_seconds": round(elapsed, 2),
        "profiles": profile_detail,
        "checks": {
            "safe_total": safe_total == CLAIMED_SAFE[q],
            "maximal_by_size": maximal_hist == CLAIMED_MAXIMAL[q],
            "maximal_sets_have_no_safe_extension": no_extension_ok,
            "complements_inclusion_minimal_d_fold": minimal_ok,
            "profile_arithmetic_identity": identity_ok,
        },
        "minimal_note": minimal_note,
    }
    if q == 4:
        q4_checks = {}
        for k, expected in CLAIMED_PROFILES_Q4.items():
            profiles_seen = profile_detail[k]["distinct_profiles"]
            if len(profiles_seen) == 1:
                got = {(int(a), int(b))
                       for a, b in profiles_seen[0]["profile"].items()}
                q4_checks[f"profile_size_{k}"] = got == expected
                result[f"profile_size_{k}"] = {
                    "expected": {int(a): int(b) for a, b in expected},
                    "got": profiles_seen[0]["profile"],
                    "count": profiles_seen[0]["count"],
                    "uniform": True,
                }
            else:
                q4_checks[f"profile_size_{k}"] = False
                result[f"profile_size_{k}"] = {
                    "expected": {int(a): int(b) for a, b in expected},
                    "got": [p["profile"] for p in profiles_seen],
                    "uniform": False,
                }
        result["checks"].update(q4_checks)
    result["ok"] = all(result["checks"].values())
    return result


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"tasks": []}
    for q in (3, 4):
        res = analyse(q)
        out["tasks"].append(res)
        print(f"--- q={q} (n={res['n']}, blocks={res['blocks']}) ---")
        print(f"  safe sets: {res['safe_total']}  by size: {res['safe_by_size']}")
        print(f"  maximal: {res['maximal_by_size']} (total {res['maximal_total']}) "
              f"[{res['dfs_seconds']} s]")
        for k, det in res["profiles"].items():
            print(f"  size {k}: {det['num_sets']} maximal sets, "
                  f"uniform profile={det['uniform']}")
            for prof in det["distinct_profiles"]:
                print(f"      profile {prof['profile']} x {prof['count']}")
        if q == 4:
            for k in (7, 9):
                det = res[f"profile_size_{k}"]
                print(f"  claimed profile for size {k}: "
                      f"{'MATCH' if res['checks'][f'profile_size_{k}'] else 'MISMATCH'}"
                      f"  got {det['got']} (expected {det['expected']})")
        for name, ok in res["checks"].items():
            print(f"  check {name}: {'OK' if ok else 'FAIL'}")
        print(f"  overall: {'PASS' if res['ok'] else 'FAIL'}")
    out["all_ok"] = all(t["ok"] for t in out["tasks"])
    with open(os.path.join(OUT, "task3_maximal.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("TASK 3:", "PASS" if out["all_ok"] else "FAIL")


if __name__ == "__main__":
    main()
