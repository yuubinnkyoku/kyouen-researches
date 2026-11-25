"""Derive GF(9) coordinate labeling from board incidence and test candidates."""
import itertools
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOARD = ROOT.parent / "output" / "board_pg2q9.txt"

ELEMS = [(a, b) for a in range(3) for b in range(3)]
ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)


def fadd(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def fneg(x):
    return ((-x[0]) % 3, (-x[1]) % 3)


def fmul(x, y):
    a, b = x
    c, d = y
    return ((a * c + 2 * b * d) % 3, (a * d + b * c) % 3)


def parse():
    lines = BOARD.read_text().splitlines()
    n, m = map(int, lines[0].split())
    rows = []
    for ln in lines[1:]:
        v = list(map(int, ln.split()))
        assert v[0] == len(v) - 1
        rows.append(v[1:])
    return n, m, rows


def main():
    n, m, rows = parse()
    board_sets = set(frozenset(r) for r in rows)
    # field values
    z = (0, 0)
    one = (1, 0)
    two = (2, 0)
    ii = (0, 1)
    twoi = (0, 2)
    candidates = []
    for e1 in (ii, twoi):
        for x in [(1, 1), (2, 1), (1, 2), (2, 2)]:
            e = [None] * 9
            e[0] = z
            e[1] = e1
            e[3] = one
            e[6] = two
            # e1^2 = -1 => label 2? from pi: e1*e1 = e_pi(1)=e_6? Wait pi(1)=6 and
            # e1*e_a=e_pi(a), so e1*e1=e6 = 2 = -1.  consistent.
            # from pi(6)=2: e1*2 = e2
            e[2] = fmul(e1, two)
            e[4] = x
            e[5] = fneg(fmul(e1, x))  # pi(8)=5 => e1*e8 = e5, e8=-x => -e1 x
            e[7] = fmul(e1, x)
            e[8] = fneg(x)
            candidates.append((f"e1={e1} x={x}", e))

    cv = [((0, 0), (0, 0), one)]
    for zz in ELEMS:
        cv.append(((0, 0), one, zz))
    for y in ELEMS:
        for zz in ELEMS:
            cv.append((one, y, zz))

    for name, e in candidates:
        # rank of canonical vectors by labels
        # label value of field element
        inv = {}
        okmap = True
        for lab, val in enumerate(e):
            if val in inv:
                okmap = False
            inv[val] = lab
        if not okmap or len(inv) != 9:
            print(name, "not a bijection")
            continue
        keyed = sorted((inv[v[0]], inv[v[1]], inv[v[2]], k) for k, v in enumerate(cv))
        rank = {k: r for r, (_a, _b, _c, k) in enumerate(keyed)}
        # generated lines
        gen = set()
        for nv in cv:
            mem = []
            for k, v in enumerate(cv):
                s = fadd(fadd(fmul(nv[0], v[0]), fmul(nv[1], v[1])), fmul(nv[2], v[2]))
                if s == ZERO:
                    mem.append(rank[k])
            gen.add(frozenset(mem))
        same = gen == board_sets
        print(name, "MATCH" if same else "no", "symdiff", len(gen ^ board_sets))
        if same:
            print("  encoding labels 0..8 -> field values", e)
            return
        # show sample of board lines not in gen
        cnt = 0
        for r in rows:
            fs = frozenset(r)
            if fs not in gen:
                print("  board line not generated:", r)
                cnt += 1
                if cnt >= 3:
                    break

if __name__ == "__main__":
    main()
