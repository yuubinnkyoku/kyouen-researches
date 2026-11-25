"""Validate the C enumerator against reference planes with known distributions.

Required by the task: PG(2,3) (560 caps) and PG(2,8) (19,550,350 caps with the
distribution {0:1,1:73,2:2628,3:56064,4:686784,5:4120704,6:8928192,7:3924480,
8:1471680,9:327040,10:32704}).  PG(2,5) and PG(2,7) are checked as extra data
points (41,572 caps / maximal all 6; 2,446,460 caps / maximal 6 and 8).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

EXPECT = {
    3: {0: 1, 1: 13, 2: 78, 3: 234, 4: 234},
    8: {0: 1, 1: 73, 2: 2628, 3: 56064, 4: 686784, 5: 4120704, 6: 8928192,
        7: 3924480, 8: 1471680, 9: 327040, 10: 32704},
}
EXPECT_TOTAL = {3: 560, 8: 19550350}
EXTRA = {
    5: ({0: 1, 1: 31, 2: 465, 3: 3875, 4: 15500, 5: 18600, 6: 3100}, 41572),
    7: ({0: 1, 1: 57, 2: 1596, 3: 26068, 4: 234612, 5: 938448, 6: 1094856,
         7: 134064, 8: 16758}, 2446460),
}


def parse(path):
    cnt, mx, tot = {}, {}, None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        f = line.split()
        if len(f) == 3 and f[0] == "cnt":
            cnt[int(f[1])] = int(f[2])
        if len(f) == 3 and f[0] == "max1":
            mx[int(f[1])] = int(f[2])
        if len(f) == 2 and f[0] == "total":
            tot = int(f[1])
    return cnt, mx, tot


def check(q, expected, total, extra=False):
    cnt, mx, tot = parse(OUT / f"census_pg2q{q}.txt")
    ok = True
    rows = []
    for k in range(0, 11):
        e = expected.get(k, 0)
        g = cnt.get(k, 0)
        ok &= (g == e)
        rows.append((k, g, e, g == e))
    ok &= (tot == total)
    print(f"PG(2,{q}){' [extra]' if extra else ''}: total {tot:,} (expect {total:,}) "
          f"-> {'ok' if tot == total else 'MISMATCH'}; maximal counts "
          f"{ {k: v for k, v in sorted(mx.items()) if v} }")
    for k, g, e, o in rows:
        if not o or g:
            print(f"   k={k:>2}: {g:>12,} (expect {e:>12,}) {'ok' if o else 'MISMATCH'}")
    return ok, rows, tot == total, mx


def main() -> None:
    res = {}
    ok_all = True
    for q in (3, 8):
        ok, rows, tot_ok, mx = check(q, EXPECT[q], EXPECT_TOTAL[q])
        res[str(q)] = {"ok": ok and tot_ok}
        ok_all &= ok and tot_ok
    for q in (5, 7):
        exp, total = EXTRA[q]
        ok, rows, tot_ok, mx = check(q, exp, total, extra=True)
        res[str(q)] = {"ok": ok and tot_ok}
        ok_all &= ok and tot_ok
    (OUT / "validate_reference.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
