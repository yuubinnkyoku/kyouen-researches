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
                               forbidden, has_forbidden_quad, V)


def popcount2(lo, hi):
    return bin(lo).count('1') + bin(hi).count('1')


def load_s5_cache(path):
    """Accept only exact, safe canonical S5 verdicts from unquarantined keys.

    An opposite-verdict duplicate is a proof conflict, never last-writer-wins.
    Historical UNKNOWN rows are ignored and cannot certify a child.
    """
    if not path:
        raise ValueError('S5 cache path is required')
    from pathlib import Path
    policy_dir = (Path(__file__).resolve().parents[2]
                  / 'n11-frontier-selection-20261005/scripts')
    if str(policy_dir) not in sys.path:
        sys.path.insert(0, str(policy_dir))
    from s5_evidence_policy import quarantined_cache_keys
    quarantine = quarantined_cache_keys()

    cache = {}
    for lineno, line in enumerate(io.open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        f = line.split(',')
        if len(f) != 6 or f[0] != 's5verdict':
            raise ValueError('malformed S5 cache row at %s:%d' % (path, lineno))
        try:
            lo, hi, stones, result, nodes = map(int, f[1:])
        except ValueError as exc:
            raise ValueError('noninteger S5 cache row at %s:%d'
                             % (path, lineno)) from exc
        if (stones != 5 or result not in (0, 1, 2) or nodes < 0
                or not (0 <= lo < 2**64 and 0 <= hi < 2**57)
                or lo.bit_count() + hi.bit_count() != 5):
            raise ValueError('invalid S5 cache evidence at %s:%d'
                             % (path, lineno))
        pts = [p for p in range(V)
               if ((lo if p < 64 else hi) >> (p % 64)) & 1]
        if d4_canonical_key(pts) != (lo, hi) or has_forbidden_quad(pts):
            raise ValueError('unsafe or noncanonical S5 key at %s:%d'
                             % (path, lineno))
        if result == 0:
            continue
        key = (lo, hi)
        previous = cache.get(key)
        if previous is not None and previous != result:
            raise ValueError('CONFLICT S5 key=%s at %s:%d'
                             % (key, path, lineno))
        cache[key] = result

    # Remove withdrawn cache ancestry even if a legacy input still contains it.
    # A certificate depending on such a child must fail as unproved.
    for key in quarantine:
        cache.pop(key, None)
    return cache

def load_manifest(path):
    """Fail closed on missing, truncated, or contaminated S4 manifests.

    A zero-row file is not evidence of a verified certificate. Validate the
    row shape before using n_child as an index or performing board searches.
    The full legal-child and verdict checks remain in main().
    """
    rows = []
    seen_claims = set()
    for lineno, line in enumerate(io.open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        f = line.split(',')
        location = '%s:%d' % (path, lineno)
        if f[0] != 's4verdict':
            raise ValueError('unexpected S4 manifest row at %s' % location)
        if len(f) < 8:
            raise ValueError('truncated S4 manifest row at %s' % location)
        try:
            first, r2, klo, khi, result, n_child, cov_size = map(int, f[1:8])
        except ValueError as exc:
            raise ValueError('noninteger S4 manifest header at %s'
                             % location) from exc
        if not (0 <= first < V and 0 <= r2 < V and first != r2):
            raise ValueError('invalid S4 root at %s' % location)
        if not (0 <= klo < 2**64 and 0 <= khi < 2**57
                and popcount2(klo, khi) == 4):
            raise ValueError('invalid S4 canonical-key shape at %s'
                             % location)
        if result not in (1, 2) or n_child < 0 or cov_size < 1:
            raise ValueError('invalid S4 verdict or counts at %s'
                             % location)
        # A certificate row is one claim for one two-stone root and class.
        # Repeating it (even with the same verdict) can inflate reported
        # certificate counts and silently hide contradictory child lists.
        # Different roots may legitimately refer to the same D4 board key.
        claim = (first, r2, klo, khi)
        if claim in seen_claims:
            raise ValueError('duplicate S4 root/class claim at %s' % location)
        seen_claims.add(claim)
        if len(f) != 8 + 2 * n_child:
            raise ValueError('S4 child count/field count mismatch at %s'
                             % location)
        try:
            child_words = list(map(int, f[8:]))
        except ValueError as exc:
            raise ValueError('noninteger S4 child at %s' % location) from exc
        for lo, hi in zip(child_words[::2], child_words[1::2]):
            if (not (0 <= lo < 2**64 and 0 <= hi < 2**57)
                    or popcount2(lo, hi) != 5):
                raise ValueError('invalid S4 child key shape at %s'
                                 % location)
        rows.append(f)
    if not rows:
        raise ValueError('empty S4 manifest: no certificate was supplied')
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

        listed = set(kids)
        if len(listed) != n_child:
            problems.append('%s: manifest repeats child key(s): n_child=%d '
                            'distinct=%d' % (label, n_child, len(listed)))

        extra = listed - want_children
        if extra:
            problems.append('%s: %d manifest child key(s) are not legal '
                            'children of the class' % (label, len(extra)))

        claimed = 'LOSS' if result == 2 else 'WIN'
        n_ok = 0
        win_edges = []
        loss_edges = 0
        undecided_edges = 0

        if result == 1:
            # WIN is existential: one legal cached WIN s5 child is a complete
            # certificate.  Older manifests may list the full child set; that
            # remains valid, but completeness is deliberately NOT required.
            # This asymmetry is the reason the coordinator can stop as soon as
            # it finds a single WIN witness.
            if n_child < 1:
                problems.append('%s: WIN certificate has no child witness'
                                % label)
            listed_win = 0
            for c in listed:
                got = cache.get(c)
                if got is None:
                    problems.append('%s: listed WIN-certificate child %d,%d '
                                    'not in the s5 cache'
                                    % (label, c[0], c[1]))
                else:
                    n_ok += 1
                    if got == 1:
                        listed_win += 1
            if listed_win == 0:
                problems.append('%s: WIN certificate contains no cached WIN '
                                'child witness' % label)
            implied = 'WIN' if listed_win else 'UNDECIDED'
        else:
            # LOSS is universal: the manifest must contain EVERY legal s5
            # child, and every one must be cached LOSS.  A truncated LOSS
            # manifest is unsound because an omitted WIN child could exist.
            if len(want_children) != n_child:
                problems.append(
                    '%s: LOSS claims %d children, recomputed %d from the '
                    'class edges (a truncated manifest would hide an '
                    'unproved child)'
                    % (label, n_child, len(want_children)))
            missing = want_children - listed
            if missing:
                problems.append('%s: %d child key(s) absent from LOSS '
                                'manifest' % (label, len(missing)))

            for (a, b), kids_here in per_edge:
                edge_unknown = False
                edge_win = False
                for c in kids_here:
                    got = cache.get(c)
                    if got is None:
                        edge_unknown = True
                        problems.append('%s: child %d,%d (edge %d-%d) not in '
                                        'the s5 cache'
                                        % (label, c[0], c[1], a, b))
                    elif got == 1:
                        edge_win = True
                    n_ok += int(got is not None)
                if edge_win:
                    win_edges.append((a, b))
                elif edge_unknown:
                    undecided_edges += 1
                else:
                    loss_edges += 1

            if win_edges:
                implied = 'WIN'
            elif undecided_edges:
                implied = 'UNDECIDED'
            else:
                implied = 'LOSS'
            if implied != 'LOSS':
                problems.append('%s: class is claimed LOSS but cached '
                                'children imply %s (win_edges=%d '
                                'loss_edges=%d undecided_edges=%d)'
                                % (label, implied, len(win_edges),
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