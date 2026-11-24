"""Parse the C census output and compare it with the claimed numbers.

Produces out/checks.json and prints a PASS/FAIL table.  Also verifies that the
two maximality tests used by the C enumerator agree, that the size distribution
sums to the claimed total, and reports structural counts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

CLAIM_SIZES = {0: 1, 1: 91, 2: 4095, 3: 110565, 4: 1769040, 5: 14859936,
               6: 52009776, 7: 51554880, 8: 7960680, 9: 589680, 10: 58968}
CLAIM_MAX = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
             6: 707616, 7: 2021760, 8: 5307120, 9: 0, 10: 58968}
CLAIM_TOTAL = 128917712
CLAIM_MAXTOTAL = 8095464


def parse(path):
    cnt, mx1, mx2, ext = {}, {}, {}, {}
    meta = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "cnt":
            cnt[int(f[1])] = int(f[2])
        elif f[0] == "max1":
            mx1[int(f[1])] = int(f[2])
        elif f[0] == "max2":
            mx2[int(f[1])] = int(f[2])
        elif f[0] == "ext":
            ext[int(f[1])] = int(f[2])
        elif len(f) == 2:
            meta[f[0]] = f[1]
    return cnt, mx1, mx2, ext, meta


def main(census="out/census_pg2q9.txt"):
    cnt, mx1, mx2, ext, meta = parse(HERE / census)
    checks = {"meta": meta, "size": {}, "max": {}, "max_tests_agree": mx1 == mx2}
    ok = True
    for k in range(0, 11):
        c, m = cnt.get(k, 0), mx1.get(k, 0)
        cs, ms = CLAIM_SIZES[k], CLAIM_MAX.get(k, 0)
        checks["size"][k] = {"got": c, "claim": cs, "ok": c == cs}
        checks["max"][k] = {"got": m, "claim": ms, "ok": m == ms}
        ok &= (c == cs) and (m == ms)
    # edge count / node count identity:
    #   ext[k] = sum over k-caps of #addable points = (k+1) * cnt[k+1]
    # For k = 1 the blocked mask is empty, so 'avail' also contains the cap point
    # itself; the DFS never revisits it (candidates are restricted to indices
    # > last).  Subtract those self-counts.
    checks["ext_identity"] = {}
    for k in range(0, 11):
        lhs, rhs = ext.get(k, 0), (k + 1) * cnt.get(k + 1, 0)
        if k == 1:
            lhs -= cnt.get(1, 0)
        checks["ext_identity"][k] = {"ext": lhs, "k1_cnt": rhs, "ok": lhs == rhs}
        ok &= lhs == rhs
    total = sum(cnt.get(k, 0) for k in range(13))
    maxtot = sum(mx1.get(k, 0) for k in range(13))
    checks["total"] = {"got": total, "claim": CLAIM_TOTAL, "ok": total == CLAIM_TOTAL}
    checks["max_total"] = {"got": maxtot, "claim": CLAIM_MAXTOTAL, "ok": maxtot == CLAIM_MAXTOTAL}
    ok &= checks["total"]["ok"] and checks["max_total"]["ok"] and checks["max_tests_agree"]
    nonmax8 = cnt.get(8, 0) - mx1.get(8, 0)
    checks["nonmax8"] = {"got": nonmax8, "claim": 58968 * 45, "ok": nonmax8 == 58968 * 45}
    ok &= checks["nonmax8"]["ok"]
    checks["all_ok"] = ok

    print(f"{'k':>2} {'caps':>12} {'claim':>12} {'':>2} {'maximal':>10} {'claim':>10} {'':>2}")
    for k in range(0, 11):
        s, m = checks["size"][k], checks["max"][k]
        print(f"{k:>2} {s['got']:>12,} {s['claim']:>12,} {'ok' if s['ok'] else 'MISMATCH':>2} "
              f"{m['got']:>10,} {m['claim']:>10,} {'ok' if m['ok'] else 'MISMATCH':>2}")
    print(f"total: {total:,} (claim {CLAIM_TOTAL:,}) -> {'ok' if checks['total']['ok'] else 'MISMATCH'}")
    print(f"maximal total: {maxtot:,} (claim {CLAIM_MAXTOTAL:,}) -> "
          f"{'ok' if checks['max_total']['ok'] else 'MISMATCH'}")
    print(f"test1 == test2 on every cap: {checks['max_tests_agree']}")
    print(f"non-maximal 8-caps: {nonmax8:,} (claim 58,968*45 = {58968*45:,})")
    print("extension identity  ext[k] == (k+1)*cnt[k+1]:")
    for k in range(0, 11):
        e = checks["ext_identity"][k]
        print(f"  k={k:>2}: ext={e['ext']:>14,}  (k+1)*cnt[k+1]={e['k1_cnt']:>14,}  "
              f"{'ok' if e['ok'] else 'MISMATCH'}")
    (OUT / "checks.json").write_text(json.dumps(checks, indent=1), encoding="utf-8")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "out/census_pg2q9.txt"))
