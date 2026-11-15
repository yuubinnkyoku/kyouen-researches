#!/usr/bin/env python3
"""Generate the |S n T| = j (j = 0..9) exhaustive case split of n10_ge20_cuts.cnf.

The identity D4 image of T is one of the 16 at-most-9 cut blocks in the CNF.
Its sequential counter s(i,j) over T's 19 cells uses block offset boff with
s(i,j) = boff + (i-1)*10 + j (k = 10, one-based j), i.e. s(19,j) = boff+180+j.
Pinning |S n T| = j exactly = units [+s(19,j), -s(19,j+1)] (j>=1) resp.
[-s(19,1)] (j=0). j = 0..9 is exhaustive over the cut-admissible values
(|S n T| <= 9), so all-UNSAT over the 10 sub-CNFs proves the base CNF UNSAT.
Each sub-CNF differs from the base only by 1-2 unit clauses (sound: case
analysis on a counter value).
"""
import hashlib
import sys
from build_n10_cuts import T, d4_images, U

BASE = "n10_ge20_cuts.cnf"
NT = len(T)  # 19


def cut_specs():
    return sorted(d4_images(T) | d4_images(U), key=lambda f: sorted(f)[:1])


def t_block_offset(nvars_base=2100):
    specs = cut_specs()
    off = nvars_base
    target = frozenset(T)
    for f in specs:
        if f == target:
            return off
        off += len(f) * 10
    raise RuntimeError("identity T image not found among cut blocks")


def main():
    with open(BASE) as fh:
        lines = fh.read().splitlines()
    header = lines[0].split()
    assert header[:4] == ["p", "cnf", "5220", "74020"], header
    body = lines[1:]
    assert len(body) == 74020, len(body)

    boff = t_block_offset()
    # sanity: the at-most-9 negative unit [-s(19,10)] of the T block must be a clause
    s19_10 = boff + (NT - 1) * 10 + 10
    assert f"-{s19_10} 0" in body, "T-block final unit clause not found"
    # sanity: total vars check
    total = 2100 + sum(len(f) * 10 for f in cut_specs())
    assert total == 5220, total

    out = {}
    for j in range(0, 10):
        if j == 0:
            units = [-(boff + (NT - 1) * 10 + 1)]
        else:
            units = [boff + (NT - 1) * 10 + j, -(boff + (NT - 1) * 10 + j + 1)]
        unit_lines = ["%d 0" % u for u in units]
        text = "p cnf 5220 %d\n" % (len(body) + len(units)) + "\n".join(body + unit_lines) + "\n"
        name = "n10_ge20_cuts_tj%d.cnf" % j
        with open(name, "w") as fh:
            fh.write(text)
        out[j] = {"file": name, "units": units, "md5": hashlib.md5(text.encode()).hexdigest()}
        print(j, out[j]["units"], out[j]["md5"])
    return out


if __name__ == "__main__":
    main()
