"""Task 5: spot-check random caps of each interesting class.

For every sampled cap the script re-derives everything from the board file with
its own code (independent of the C enumerator):

* is it a cap (every line meets it in <= 2 points)?
* maximality by two independent formulations:
    (i)  'secant lines'  : q addable iff q is on no secant line of S;
    (ii) 'injective pencil': q addable iff s -> line(q,s) is injective on S.
  The two addable sets must be identical.
* class-specific expectations:
    9-caps         : exactly 1 addable point q, and S + q is a 10-cap present in
                     the census dump of 10-caps (i.e. a conic's missing point);
    maximal 6/7/8  : 0 addable points;
    non-maximal 8  : exactly 2 addable points.
"""

from __future__ import annotations

import json
import struct
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgcore as pc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
BOARD = HERE.parent / "output" / "board_pg2q9.txt"


def load_board(path):
    n, lines = pc.load_board(path)
    lmask = []
    lid = [[-1] * n for _ in range(n)]
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
        lmask.append(m)
        for a in range(len(L)):
            for b in range(a + 1, len(L)):
                lid[L[a]][L[b]] = li
                lid[L[b]][L[a]] = li
    return n, lines, lmask, lid


def is_cap(S, lmask):
    m = 0
    for p in S:
        m |= 1 << p
    return all(bin(lm & m).count("1") <= 2 for lm in lmask)


def addable_secants(S, n, lmask):
    blocked = 0
    for a, b in combinations(S, 2):
        li = next(li for li, m in enumerate(lmask)
                  if (m >> a) & 1 and (m >> b) & 1)
        blocked |= lmask[li]
    return [q for q in range(n) if not (blocked >> q) & 1]


def addable_injective(S, n, lid):
    out = []
    for q in range(n):
        if q in S:
            continue
        seen = set()
        add = True
        for s in S:
            li = lid[q][s]
            if li in seen:
                add = False
                break
            seen.add(li)
        if add:
            out.append(q)
    return out


def read_masks(path):
    data = path.read_bytes()
    (n,) = struct.unpack("<Q", data[:8])
    out = []
    for i in range(n):
        out.append(int.from_bytes(data[8 + 16 * i: 8 + 16 * (i + 1)], "little"))
    return out


def read_samples(path):
    caps = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        caps.append([int(x) for x in line.split()])
    return caps


EXPECT = {
    "caps9": {"size": 9, "addable": 1},
    "max6": {"size": 6, "addable": 0},
    "max7": {"size": 7, "addable": 0},
    "max8": {"size": 8, "addable": 0},
    "nonmax8": {"size": 8, "addable": 2},
}


def main() -> None:
    n, lines, lmask, lid = load_board(BOARD)
    caps10 = set(read_masks(OUT / "caps10.bin"))
    print(f"board: {n} points, {len(lines)} lines; census 10-caps loaded: {len(caps10)}")

    report = {}
    all_ok = True
    for cls, exp in EXPECT.items():
        path = OUT / f"samp_{cls}.txt"
        caps = read_samples(path)
        ok = 0
        problems = []
        for S in caps:
            tag = f"{cls}:{S}"
            if len(set(S)) != len(S) or len(S) != exp["size"] or not all(0 <= p < n for p in S):
                problems.append(f"{tag} bad shape")
                continue
            if not is_cap(S, lmask):
                problems.append(f"{tag} not a cap")
                continue
            a1 = addable_secants(S, n, lmask)
            a2 = addable_injective(S, n, lid)
            if sorted(a1) != sorted(a2):
                problems.append(f"{tag} addable sets differ {a1} vs {a2}")
                continue
            if len(a1) != exp["addable"]:
                problems.append(f"{tag} addable={len(a1)} expected {exp['addable']}")
                continue
            if cls == "caps9":
                q = a1[0]
                m = 0
                for p in S + [q]:
                    m |= 1 << p
                if not is_cap(S + [q], lmask):
                    problems.append(f"{tag} S+q not a cap")
                    continue
                if m not in caps10:
                    problems.append(f"{tag} S+q not a census 10-cap")
                    continue
                # S+q must be maximal (a 10-cap has no addable point)
                if addable_secants(S + [q], n, lmask):
                    problems.append(f"{tag} S+q not maximal")
                    continue
            ok += 1
        all_ok &= (not problems) and ok == len(caps) and len(caps) == 50
        report[cls] = {"sampled": len(caps), "ok": ok, "problems": problems}
        print(f"{cls}: {ok}/{len(caps)} verified, problems {len(problems)}")
        for p in problems[:5]:
            print("   ", p)

    (OUT / "task5_samples.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
