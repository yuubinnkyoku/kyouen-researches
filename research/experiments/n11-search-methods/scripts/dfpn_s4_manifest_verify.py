#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independently verify an s4 certificate manifest.

A coordinator manifest row
    s4verdict,first,r2,key_lo,key_hi,result,n_child,cov_size,child_lo,child_hi,...
claims that the canonical s4 class named by (key_lo,key_hi) has verdict
`result`. This script re-derives the claim from the board and the s5 cache,
without asking the solver for anything.

For a LOSS class the claim is strong and must hold in full:
  1. the class key is the D4 canonical form of {first,r2,a,b}
  2. n_child equals the number of DISTINCT canonical keys of every legal
     fifth move of every raw edge in the class -- completeness, not just a
     subset, because a truncated list would let a real WIN child hide
  3. every listed child is a 5-stone key carrying exactly 5 bits
  4. every listed child is present in the s5 cache as LOSS
For a WIN class one LOSS-free WIN witness is required:
  3'. the listed child is present in the s5 cache as WIN
  (and, as a sanity check, the class is NOT all-LOSS, i.e. a WIN witness
   does not contradict the cache)

A class that fails any check is reported and the exit code is non-zero, so
a manifest cannot be trusted on the strength of the file alone.

Usage:
    dfpn_s4_manifest_verify.py <manifest.csv> --cache <s5_verdicts.csv>
"""
import argparse
import collections
import io
import sys

from dfpn_edge_classes import (d4_canonical_key, legal_after,  # noqa: E402
                               forbidden, V)


def popcount2(lo, hi):
    return bin(lo).count('1') + bin(hi).count('1')


def load_s5_cache(path):
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


def load_manifest(path):
    rows = []
    for line in io.open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        f = line.split(',')
        if f[0] != 's4verdict':
            continue
        if len(f) < 7:
            raise ValueError('s4verdict row has only %d fields: %r'
                             % (len(f), line))
        rows.append(f)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    ap.add_argument('--cache', required=True)
    args = ap.parse_args()

    cache = load_s5_cache(args.cache)
    rows = load_manifest(args.manifest)

    print('manifest entries : %d' % len(rows))
    print('s5 cache entries : %d' % len(cache))

    seen_keys = {}
    problems = []
    checked_children = 0
    verdicts = collections.Counter()

    for f in rows:
        first, r2 = int(f[1]), int(f[2])
        klo, khi = int(f[3]), int(f[4])
        result = int(f[5])
        n_child = int(f[6])
        cov_size = int(f[7])
        kids = [(int(f[8 + 2 * i]), int(f[9 + 2 * i]))
                for i in range(n_child)]
        tail = len(f) - (8 + 2 * n_child)
        label = 's4 key=%d,%d root={%d,%d}' % (klo, khi, first, r2)

        if tail != 0:
            problems.append('%s: %d trailing field(s) after %d children'
                            % (label, tail, n_child))
        if result not in (1, 2):
            problems.append('%s: result=%d is not WIN(1) or LOSS(2)'
                            % (label, result))
            continue

        # The same key must not appear twice with different verdicts.
        if (klo, khi) in seen_keys:
            if seen_keys[(klo, khi)][0] != result:
                problems.append('%s: key already recorded as result=%d'
                                % (label, seen_keys[(klo, khi)][0]))
        seen_keys[(klo, khi)] = (result, khi)

        # (1) every listed child must be a real 5-stone position.
        for c in kids:
            checked_children += 1
            if popcount2(c[0], c[1]) != 5:
                problems.append('%s: child %d,%d has %d bits, expected 5'
                                % (label, c[0], c[1], popcount2(c[0], c[1])))

        # (2) recompute the class: the raw edges are the pairs {a,b} of
        # legal third moves with b a legal reply to a. The manifest does not
        # list the raw edges, so they are re-derived here and the coverage
        # and child set are compared against the claim.
        base = {first, r2}
        verts = legal_after(base)
        edge_set = set()
        for a in verts:
            for b in legal_after(base | {a}):
                if b == a:
                    continue
                edge_set.add((min(a, b), max(a, b)))

        # Edges of THIS class only, and the children each edge contributes.
        #
        # The verdict is a CLASS verdict but the children are per EDGE:
        #   LOSS  every legal fifth move of every edge in the class
        #   WIN   at least one legal fifth move of at least one edge
        # So a WIN class legitimately lists many LOSS children: those are
        # the children of the other edges in the class. Checking every
        # listed child against the class verdict would wrongly reject every
        # WIN class.
        want_cov = set()
        want_children = set()
        per_edge = []
        for (a, b) in sorted(edge_set):
            # Compare BOTH halves of the key. Matching on `lo` alone lumps
            # together unrelated classes that happen to agree in the low
            # word, which made a correct 4-edge class look like it had 77
            # endpoints and 2002 children.
            lo, hi = d4_canonical_key([first, r2, a, b])
            if (lo, hi) != (klo, khi):
                continue
            want_cov.update((a, b))
            occ4 = base | {a, b}
            kids_here = set()
            for z in legal_after(occ4):
                ck = d4_canonical_key([first, r2, a, b, z])
                kids_here.add(ck)
                want_children.add(ck)
            per_edge.append(((a, b), kids_here))

        if not want_cov:
            problems.append('%s: no raw edge maps to this canonical key, so '
                            'the certificate names a non-existent class'
                            % label)
            continue

        if len(want_cov) != cov_size:
            problems.append('%s: claims cov_size=%d, recomputed %d'
                            % (label, cov_size, len(want_cov)))

        if len(want_children) != n_child:
            problems.append(
                '%s: claims %d children, recomputed %d from the class edges '
                '(a truncated manifest would hide an unproved child)'
                % (label, n_child, len(want_children)))

        listed = set(kids)
        missing = want_children - listed
        extra = listed - want_children
        if missing:
            problems.append('%s: %d child key(s) absent from the manifest'
                            % (label, len(missing)))
        if extra:
            problems.append('%s: %d manifest child key(s) are not legal '
                            'children of the class' % (label, len(extra)))

        # (3)/(4) every child must be in the cache, and the per-edge
        # verdicts implied by the cache must imply the claimed class
        # verdict.
        #
        # A class is LOSS only if EVERY edge is LOSS, and a class is WIN
        # as soon as ONE edge is WIN. So recompute each edge's verdict from
        # the cache and combine:
        #     edge LOSS  <=> all its cached children are LOSS
        #     edge WIN   <=> some cached child is WIN
        #     class LOSS <=> every edge is LOSS
        #     class WIN  <=> some edge is WIN
        # An edge with an undecided child makes the class undecided, which
        # contradicts a claimed decided verdict.
        n_ok = 0
        undecided_edges = 0
        win_edges = []
        loss_edges = 0
        for (a, b), kids_here in per_edge:
            verts_e = []
            for c in kids_here:
                got = cache.get(c)
                if got is None:
                    problems.append('%s: child %d,%d (edge %d-%d) not in the '
                                    's5 cache' % (label, c[0], c[1], a, b))
                elif got == 1:
                    verts_e.append('WIN')
                else:
                    verts_e.append('LOSS')
                if got is not None:
                    n_ok += 1
            if not verts_e:
                undecided_edges += 1
            elif 'WIN' in verts_e:
                win_edges.append((a, b))
            else:
                loss_edges += 1

        implied = None
        if undecided_edges:
            implied = 'UNDECIDED'
        elif win_edges:
            implied = 'WIN'
        elif loss_edges:
            implied = 'LOSS'
        claimed = 'LOSS' if result == 2 else 'WIN'
        if implied != claimed:
            problems.append('%s: class is claimed %s but the cached children '
                            'imply %s (win_edges=%d loss_edges=%d '
                            'undecided_edges=%d)'
                            % (label, claimed, implied, len(win_edges),
                               loss_edges, undecided_edges))

        verdicts[claimed] += 1
        print('  %s result=%s cov=%d children=%d (%d in cache) '
              'edges=%d win_edges=%d loss_edges=%d'
              % (label, claimed, len(want_cov), n_child, n_ok,
                 len(per_edge), len(win_edges), loss_edges))

    print()
    print('classes verified  : LOSS=%d WIN=%d'
          % (verdicts['LOSS'], verdicts['WIN']))
    print('children checked  : %d' % checked_children)
    print('distinct s4 keys  : %d' % len(seen_keys))
    if problems:
        print('PROBLEMS          : %d' % len(problems))
        for p in problems[:25]:
            print('  %s' % p)
        print('MANIFEST_INVALID')
        return 1
    print('MANIFEST_VERIFIED')
    return 0


if __name__ == '__main__':
    sys.exit(main())