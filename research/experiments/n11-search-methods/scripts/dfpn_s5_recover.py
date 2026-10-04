#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recover proved s5 verdicts from a coordinator/quant log and merge them
into a worker cache file.

Why this exists: the coordinator proved a whole s4 class LOSS on 2026-10-03
(158 exact searches, all decided) but the run had no cache-output flag, so
every one of those verdicts died with the process. The cache still holds
only the earlier 103-row seed. The log lines
    [q-done]   q=<n> key=<lo>,<hi> result=<r> nodes=<m> ms=<t> ...
carry the canonical key and the DECIDED verdict, so the proof material is
recoverable without re-running 419M nodes.

Rules that keep the merge honest:
  * only `result=1` (WIN) or `result=2` (LOSS) rows are kept. An UNKNOWN
    (`result=0`) means the node budget ran out and must never be persisted,
    or a later, better funded query inherits the earlier failure.
  * a `[q-start]` with no matching `[q-done]` was interrupted and is
    dropped, which is exactly the intended behaviour.
  * the same key must not appear with two different verdicts anywhere, in
    the log or against the existing cache. A conflict is reported and the
    merge is REFUSED; nothing is written.
  * the output is a worker file, never an in-place append: workers own
    their own CSV and the coordinator merges afterwards.

Usage:
    dfpn_s5_recover.py <log>... --out <worker.csv> [--cache <existing.csv>]
"""
import argparse
import io
import re
import sys

HEADER = ('# s5 verdict cache: n=11 schema=1 '
          '(canonical key -> WIN/LOSS, UNKNOWN never stored)\n')

# [q-done]   q=7 key=1152921504606848001,16777220 result=2 nodes=3580140 ms=...
Q_DONE = re.compile(r'\[q-done\].*?key=(\d+),(\d+)\s+result=(\d+)\s+nodes=(\d+)')
# The replay driver prints the same verdicts in a different shape.
REPLAY = re.compile(r'^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)')


def scan(path):
    """Return (verdicts, started) for one log.

    verdicts: {(lo,hi): (result, nodes)} from completed queries only
    started:  set of (lo,hi) that were begun, so a key can be reported as
             interrupted when it has no verdict.
    """
    verdicts = {}
    started = set()
    for line in io.open(path, encoding='utf-8', errors='replace'):
        m = Q_DONE.search(line)
        if m:
            key = (int(m.group(1)), int(m.group(2)))
            res = int(m.group(3))
            verdicts[key] = (res, int(m.group(4)))
            continue
        # replay,id,stones,legal,is_or,budget,result,nodes,wall_s,lo,hi
        m = REPLAY.match(line.strip())
        if m:
            key = (int(m.group(10)), int(m.group(11)))
            verdicts[key] = (int(m.group(7)), int(m.group(8)))
            continue
        # Track starts so an unfinished query is visible as such.
        for m2 in re.finditer(r'\[q-start\]\s+q=\d+\s+key=(\d+),(\d+)', line):
            started.add((int(m2.group(1)), int(m2.group(2))))
    return verdicts, started


def load_cache(path):
    cache = {}
    if not path:
        return cache
    for line in io.open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        f = line.split(',')
        if len(f) < 6 or f[0] != 's5verdict':
            continue
        if int(f[3]) != 5:
            continue
        r = int(f[4])
        if r not in (1, 2):
            continue
        cache[(int(f[1]), int(f[2]))] = r
    return cache


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('logs', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--cache', default=None)
    args = ap.parse_args()

    recovered = {}
    started = set()
    interrupted = set()
    for path in args.logs:
        v, s = scan(path)
        for k, val in v.items():
            if k in recovered and recovered[k][0] != val[0]:
                print('CONFLICT between logs: key=%s %s vs %s'
                      % (k, recovered[k][0], val[0]))
                print('REFUSED: verdicts disagree, refusing to merge')
                return 1
            recovered[k] = val
        started |= s
    interrupted = started - set(recovered)

    existing = load_cache(args.cache)

    win = sum(1 for r, _ in recovered.values() if r == 1)
    loss = sum(1 for r, _ in recovered.values() if r == 2)
    unknown = sum(1 for r, _ in recovered.values() if r not in (1, 2))
    print('log verdicts        : %d  (WIN=%d LOSS=%d UNKNOWN_dropped=%d)'
          % (len(recovered), win, loss, unknown))
    print('interrupted queries : %d  (no verdict line, dropped)'
          % len(interrupted))

    fresh = [k for k in recovered if k not in existing]
    overlap = [k for k in recovered if k in existing]
    conflicts = [k for k in overlap if existing[k] != recovered[k][0]]
    print('already in cache    : %d' % len(overlap))
    print('new to the cache    : %d' % len(fresh))
    if conflicts:
        print()
        print('CONFLICT: %d key(s) already cached with a different verdict'
              % len(conflicts))
        for k in conflicts[:10]:
            print('  key=%s cached=%s recovered=%s'
                  % (k, existing[k], recovered[k][0]))
        print('REFUSED: not writing; a conflict must be resolved by a human.')
        return 1
    if not fresh:
        print('nothing new to write')

    with io.open(args.out, 'w', encoding='utf-8') as f:
        f.write(HEADER)
        for k in sorted(fresh):
            r, nodes = recovered[k]
            f.write('s5verdict,%d,%d,5,%d,%d\n' % (k[0], k[1], r, nodes))
    print('written             : %s (%d rows)' % (args.out, len(fresh)))
    print('MERGE_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())