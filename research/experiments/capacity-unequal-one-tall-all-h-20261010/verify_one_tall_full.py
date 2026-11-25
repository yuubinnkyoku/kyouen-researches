#!/usr/bin/env python3
"""Independent labelled-state mex audit of the one-tall, unit-short capacity family, all parameters.

No imported project modules. Two unrelated legality calculations are used:
  (1) raw top-h sort on all labelled column occupancies;
  (2) a two-coordinate (ell,a) quotient with explicit inequalities.
The proposed theorem's formula is evaluated separately from both recursions.
"""
import argparse
import hashlib
import json
from functools import lru_cache


def closed(h, r, k, ell, a):
    b = h - 1
    if k < b or r < h:
        return (r - ell - a) % 2
    t = k - b
    if t % 2 == 0:
        return (r - ell - a) % 2
    if a >= b:
        return (r + t - ell - a) % 2
    e = r - 2*b + 1 + a
    if ell == e:
        return 2
    if ell < e:
        return (e - ell) % 2
    return (r - ell - a) % 2


def run_case(h, r, k):
    b = h - 1
    full = (1 << k) - 1

    # Raw labelled game: no use of the simplified capacity inequalities.
    def raw_safe(ell, mask):
        occupancy = [ell] + [(mask >> j) & 1 for j in range(k)]
        return sum(sorted(occupancy, reverse=True)[:h]) <= r

    @lru_cache(None)
    def raw_grundy(ell, mask):
        assert raw_safe(ell, mask)
        children = []
        if ell < r and raw_safe(ell + 1, mask):
            children.append(raw_grundy(ell + 1, mask))
        for j in range(k):
            bit = 1 << j
            if not mask & bit and raw_safe(ell, mask | bit):
                children.append(raw_grundy(ell, mask | bit))
        mex = 0
        while mex in children:
            mex += 1
        return mex

    # Independently written quotient: direct inequalities, no sort or bitmasks.
    def quotient_safe(ell, a):
        if a < b:
            return ell + a <= r
        if ell == 0:
            return min(a, h) <= r
        return ell + b <= r

    @lru_cache(None)
    def quotient_grundy(ell, a):
        assert quotient_safe(ell, a)
        children = []
        if ell < r and quotient_safe(ell + 1, a):
            children.append(quotient_grundy(ell + 1, a))
        if a < k and quotient_safe(ell, a + 1):
            children.append(quotient_grundy(ell, a + 1))
        mex = 0
        while mex in children:
            mex += 1
        return mex

    states = 0
    raw_terminal_vectors = set()
    raw_g_values = set()
    for mask in range(full + 1):
        a = mask.bit_count()
        for ell in range(r + 1):
            if not raw_safe(ell, mask):
                assert not quotient_safe(ell, a), (h, r, k, ell, mask)
                continue
            assert quotient_safe(ell, a), (h, r, k, ell, mask)
            g = raw_grundy(ell, mask)
            q = quotient_grundy(ell, a)
            expected = closed(h, r, k, ell, a)
            assert g == q == expected, (h, r, k, ell, mask, g, q, expected)
            states += 1
            raw_g_values.add(g)
            has_tall = ell < r and raw_safe(ell + 1, mask)
            has_short = any(not mask & (1 << j) and raw_safe(ell, mask | (1 << j)) for j in range(k))
            if not (has_tall or has_short):
                raw_terminal_vectors.add((ell, mask))
    terminal_sizes = sorted({ell + mask.bit_count() for ell, mask in raw_terminal_vectors})
    if k < b or r < h:
        expected_sizes = [r]
        expected_terminal_count = sum(__import__('math').comb(k, a) for a in range(min(k, r) + 1))
        expected_max_g = 1 if r > 0 else 0
    else:
        expected_sizes = sorted(set([r, r + k - b]))
        expected_terminal_count = sum(__import__('math').comb(k, a) for a in range(b)) + 1
        expected_max_g = 2 if (k-b) % 2 else 1
    assert terminal_sizes == expected_sizes, (h, r, k, terminal_sizes, expected_sizes)
    assert len(raw_terminal_vectors) == expected_terminal_count, (h, r, k, len(raw_terminal_vectors), expected_terminal_count)
    assert max(raw_g_values) == expected_max_g, (h, r, k, raw_g_values)
    return states, len(raw_terminal_vectors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-h', type=int, default=7)
    parser.add_argument('--extra-r', type=int, default=5)
    parser.add_argument('--extra-k', type=int, default=5)
    parser.add_argument('--max-k', type=int, default=11)
    args = parser.parse_args()
    cases = 0
    states = 0
    terminals = 0
    records = []
    for h in range(2, args.max_h + 1):
        for r in range(0, h + args.extra_r + 1):
            for k in range(0, min(h - 1 + args.extra_k, args.max_k) + 1):
                s, t = run_case(h, r, k)
                cases += 1
                states += s
                terminals += t
                records.append([h, r, k, s, t])
    payload = json.dumps(records, separators=(',', ':')).encode()
    print(json.dumps({'result': 'PASS', 'cases': cases, 'labelled_safe_states': states,
                      'labelled_terminal_states': terminals,
                      'case_digest_sha256': hashlib.sha256(payload).hexdigest()},
                     ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
