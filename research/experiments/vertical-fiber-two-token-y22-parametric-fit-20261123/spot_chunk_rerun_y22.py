#!/usr/bin/env python3
"""Chunked re-execution driver for spot_y22.py determinism verification.

The sandbox caps a single foreground command at 300s while the full spot run
is expected above that, and background processes do not survive environment
resets between tool calls. Determinism re-runs therefore execute the EXACT
source slices of spot_y22.main() block by block: each slice is cut
byte-exactly from the published spot_y22.py between unique source markers
and exec'd in the spot_y22 module namespace with a small prelude
(t0/pts/bad/f*/firsts initialisation). The raw engine is a pure function of
(R, tokens, z): H_canonical values do not depend on cache state (the
published audits rely on this for the deterministic LRU eviction argument),
so blockwise execution is numerically equivalent. Each chunk run prints the
same aggregate lines as the reference full run (minus cross-block
accumulation); expected (pre-declared in the single-owner note):
  deep  46 rows pts 5980 bad 0
  bigz  pts 30240 bad 0
  edge  pts 4100 bad 0
  far   pts 2628 bad 0
  tail  78 bad 0 / merge 19449 bad 0
Usage: python3 spot_chunk_rerun_y22.py {deep|bigz|edge|far|tailmerge}
"""
import sys
import spot_y22 as S

SRC = open('spot_y22.py').read()

CHUNKS = {
    # (start marker, end marker, prelude needs)
    "deep": ("    deep = [", '"block deep done:"'),
    "bigz": ("    # bigz (d <= -10 is excluded", '"block bigz done: pts"'),
    "edge": ("    # x=y=22 edge", '"block edge done: pts"'),
    "far":  ("    # far d\n", 'firsts = (f + f2 + f3 + f4)[:20]'),
    "tailmerge": ("    # tail raw check on sweep/steady rows d>=24 (both x parities)",
                  '"merge regression points:"'),
}


def slice_source(name):
    start_m, end_m = CHUNKS[name]
    assert SRC.count(start_m) == 1, ("start marker not unique", start_m)
    i = SRC.index(start_m)
    j = SRC.index(end_m, i)
    j = SRC.index("\n", j) + 1
    # stop marker must appear after start; also require no stray earlier hit
    import textwrap
    return textwrap.dedent(SRC[i:j])


def main():
    name = sys.argv[1]
    chunk = slice_source(name)
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
    exec(compile(chunk, "spot_y22.py::main::" + name, "exec"), S.__dict__)
    print("CHUNK %s OK pts=%d bad=%d" % (name, S.pts, S.bad))


if __name__ == '__main__':
    main()
