#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn a set of s5 canonical keys into a `--exact-replay` input file, and
compare a replay run's verdicts against a cache file.

Recovering a verdict from a log is only progress if the verdict is still
right. This script is the second half of the check: it emits the canonical
keys in the replay driver's input shape so each one is re-solved from a COLD
solver (fresh transposition table, no oracle cache), and then compares the
fresh verdicts with the ones being persisted.

The comparison is on the VERDICT only. Node counts are not expected to
match: in the coordinator run each position was solved with a warm table,
while the replay starts empty. What must match is WIN/LOSS.

Usage:
    dfpn_s5_replay_check.py keys --cache <csv> --out <replay_in.csv>
    dfpn_s5_replay_check.py compare --cache <csv> --replay <replay_out.csv>
"""
import argparse
import io
import sys


def load_cache(path):
    cache = {}
    if not path:
        return cache
    for line in io.open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        f = line.split(',')
        if len(f) < 6 or f[0] != 's5verdict' or int(f[3]) != 5:
            continue
        r = int(f[4])
        if r in (1, 2):
            cache[(int(f[1]), int(f[2]))] = r
    return cache


def popcount2(lo, hi):
    return bin(lo).count('1') + bin(hi).count('1')


def cmd_keys(args):
    cache = load_cache(args.cache)
    keys = sorted(cache)
    n = 0
    with io.open(args.out, 'w', encoding='utf-8') as f:
        # tag,seq,stones,lo,hi,legal,depth,is_or,retries,nodes,result
        # `legal` is informational here: run_exact_replay reads the
        # occupancy from lo/hi and recomputes legality itself.
        for i, (lo, hi) in enumerate(keys):
            f.write('s5verify,%d,5,%d,%d,0,0,1,1,0,0\n' % (i, lo, hi))
            n += 1
    print('cache entries    : %d' % len(cache))
    print('replay rows      : %d' % n)
    for (lo, hi), r in sorted(cache.items()):
        if popcount2(lo, hi) != 5:
            print('MALFORMED: key %s,%s has %d bits set, expected 5'
                  % (lo, hi, popcount2(lo, hi)))
            return 1
    print('all keys carry exactly 5 bits set')
    print('KEYS_OK')
    return 0


def cmd_compare(args):
    cache = load_cache(args.cache)
    replay = {}
    for line in io.open(args.replay, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line.startswith('replay,'):
            continue
        f = line.split(',')
        if len(f) < 11:
            continue
        # replay,id,stones,legal,is_or,budget,result,nodes,wall_s,lo,hi
        replay[(int(f[9]), int(f[10]))] = int(f[6])

    agree = disagree = missing = undecided = 0
    bad = []
    for key, want in sorted(cache.items()):
        got = replay.get(key)
        if got is None:
            missing += 1
            continue
        if got not in (1, 2):
            undecided += 1
            continue
        if got != want:
            disagree += 1
            bad.append((key, want, got))
        else:
            agree += 1
    print('cache entries    : %d' % len(cache))
    print('replayed         : %d' % len(replay))
    print('agree            : %d' % agree)
    print('DISAGREE         : %d' % disagree)
    print('undecided replay : %d  (budget ran out; proves nothing either way)'
          % undecided)
    print('not replayed     : %d' % missing)
    if bad:
        print()
        print('mismatches (cache said, cold replay said):')
        for k, want, got in bad[:20]:
            print('  key=%s cache=%d replay=%d' % (k[0], want, got))
    ok = disagree == 0 and undecided == 0 and missing == 0
    print('VERIFY_OK' if ok else 'VERIFY_FAILED')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    k = sub.add_parser('keys')
    k.add_argument('--cache', required=True)
    k.add_argument('--out', required=True)
    k.set_defaults(fn=cmd_keys)

    c = sub.add_parser('compare')
    c.add_argument('--cache', required=True)
    c.add_argument('--replay', required=True)
    c.set_defaults(fn=cmd_compare)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())