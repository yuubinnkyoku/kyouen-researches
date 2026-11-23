#!/usr/bin/env python3
"""Chunked re-execution driver for spot_y23.py determinism verification.

The sandbox caps a single foreground command at 300s and background
processes do not survive environment resets; on this host the y=23 bigz
block (280 rows / 36,190 points at z=31..40, R<=x+z+48) exceeds that cap in
a single process (the first whole-block attempt was killed by the cap on
2026-11-23 and triggered a sandbox reset; the y=22 battery's largest block
was bigz at 168s). Therefore:
  deep / edge / far / tailmerge execute the EXACT source slices of
  spot_y23.main() block by block: each slice is cut byte-exactly from the
  published spot_y23.py between unique source markers and exec'd in the
  spot_y23 module namespace with a small prelude (t0/pts/bad/f* initialisation),
  exactly as in the published y=21/y=22 fit audits;
  bigz executes the same byte-exact bigz slice with the module-global
  BIGZ_ZS rebound to a z SUB-RANGE: 'bigz:a-b' runs z = a..b-1. The raw
  engine is a pure function of (R, tokens, z): H_canonical values do not
  depend on cache state (the published audits rely on this for the
  deterministic LRU eviction argument), so the UNION of the sub-range sweeps
  equals the full-range sweep point-for-point; the reference coverage uses
  the SIX sub-ranges 31-32, 32-33, 33-35, 35-37, 37-39, 39-41 (z=31..40,
  each z exactly once; honest record: the first pass used five sub-ranges
  whose range arithmetic silently skipped z=32 -- the sub-range point sum
  32,767 vs the pre-declared 36,190 caught the gap BEFORE any publication,
  the missing z=32 slice (3,423 points) was run, and the total reconciled
  to exactly 36,190; the z=39-41 pair is the wall-dominant chunk at 259s).
Each chunk run prints the same aggregate lines as the reference full run
(minus cross-block accumulation); expected (pre-declared in the
single-owner note):
  deep  46 rows pts 5980 bad 0
  bigz  pts 36190 bad 0 (over the six z sub-ranges)
  edge  pts 4125 bad 0
  far   pts 2700 bad 0
  tail  78 bad 0 / merge 117 rows / 19005 pts bad 0
Usage: python3 spot_chunk_rerun_y23.py {deep|edge|far|tailmerge|bigz|bigz:a-b}
"""
import sys
import spot_y23 as S

SRC = open('spot_y23.py').read()

CHUNKS = {
    # (start marker, end marker)
    "deep": ("    deep = [", '"block deep done:"'),
    "bigz": ("    # bigz (d <= -9 is excluded", '"block bigz done: pts"'),
    "edge": ("    # x=y=23 edge", '"block edge done: pts"'),
    "far":  ("    # far d\n", 'firsts = (f + f2 + f3 + f4)[:20]'),
    "tailmerge": ("    # tail raw check on sweep/steady rows d>=24 (both x parities)",
                  '"merge regression rows:"'),
}


def slice_source(name):
    start_m, end_m = CHUNKS[name]
    assert SRC.count(start_m) == 1, ("start marker not unique", start_m)
    i = SRC.index(start_m)
    j = SRC.index(end_m, i)
    j = SRC.index("\n", j) + 1
    import textwrap
    return textwrap.dedent(SRC[i:j])


def main():
    name = sys.argv[1]
    if name.startswith('bigz'):
        chunk = slice_source("bigz")
        try:
            a, b = name.split(':')[1].split('-')
            lo, hi = int(a), int(b)
        except IndexError:
            lo, hi = 31, 41   # plain 'bigz' = the full range
        assert 31 <= lo < hi <= 41, (lo, hi)
        S.BIGZ_ZS = range(lo, hi)
        label = name
    else:
        chunk = slice_source(name)
        label = name
    # prelude: main() locals that later slices reference
    import time as _t
    S.t0 = _t.time()
    S.pts = 0
    S.bad = 0
    S.f = []
    S.f2 = []
    S.f3 = []
    S.f4 = []
    S.firsts = []
    exec(compile(chunk, "spot_y23.py::main::" + label, "exec"), S.__dict__)
    print("CHUNK %s OK pts=%d bad=%d" % (label, S.pts, S.bad))


if __name__ == '__main__':
    main()
