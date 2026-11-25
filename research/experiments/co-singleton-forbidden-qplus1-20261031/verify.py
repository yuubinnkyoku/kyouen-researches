#!/usr/bin/env python3
"""All nonempty co-singleton forbidden families, independent subset-mex audit."""
from functools import lru_cache
from math import comb

def mex(xs):
    n = 0
    while n in xs:
        n += 1
    return n

def formula(a, b):
    r = a + b
    assert r >= 1 and not (r == 1 and a == 1)
    if r == 1:
        g = 0
    elif r % 2 == 0:
        g = int(a <= r // 2)
    elif a <= (r - 1) // 2:
        g = 0
    elif a == (r + 1) // 2:
        g = 2
    else:
        g = 1
    return g, (1 if g == 0 else 0 if g == 1 else g)

def audit(n):
    full = (1 << n) - 1
    families = states = openings = 0
    for fmask in range(1, full + 1):
        forbidden = [full ^ (1 << v) for v in range(n) if fmask >> v & 1]
        @lru_cache(None)
        def direct(s):
            children = []
            for v in range(n):
                bit = 1 << v
                if s & bit:
                    continue
                nxt = s | bit
                if any((nxt & edge) == edge for edge in forbidden):
                    continue
                children.append(direct(nxt))
            if not children:
                return (0, 1)
            return mex({g for g, h in children}), mex({h for g, h in children})
        terminal_by_size = {}
        for s in range(1 << n):
            if any((s & edge) == edge for edge in forbidden):
                continue
            a = (fmask & ~s & full).bit_count()
            b = ((full ^ fmask) & ~s).bit_count()
            actual = direct(s)
            expected = formula(a, b)
            assert actual == expected, (n, fmask, s, actual, expected)
            states += 1
            if s == 0:
                families += 1
                for v in range(n):
                    child = direct(1 << v)
                    ca = a - bool(fmask >> v & 1)
                    cb = b - bool((full ^ fmask) >> v & 1)
                    fg, fh = formula(ca, cb)
                    assert (child[0] == 0, child[1] == 0) == (fg == 0, fh == 0)
                    openings += 1
            terminal = True
            for v in range(n):
                if s >> v & 1:
                    continue
                nxt = s | (1 << v)
                if not any((nxt & edge) == edge for edge in forbidden):
                    terminal = False
                    break
            if terminal:
                size = s.bit_count()
                terminal_by_size[size] = terminal_by_size.get(size, 0) + 1
        f = fmask.bit_count()
        assert terminal_by_size.get(n-2, 0) == comb(f, 2)
        assert terminal_by_size.get(n-1, 0) == n-f
        assert sum(terminal_by_size.values()) == comb(f, 2) + n-f
        direct.cache_clear()
    return families, states, openings

if __name__ == "__main__":
    totals = [0, 0, 0]
    for n in range(3, 11):
        row = audit(n)
        totals = [x+y for x,y in zip(totals, row)]
        print(f"N={n}: families={row[0]}, safe_states={row[1]}, first_moves={row[2]}")
    assert totals == [2032, 1384796, 18372], totals
    print("TOTAL", dict(zip(("families", "safe_states", "first_moves"), totals)))
