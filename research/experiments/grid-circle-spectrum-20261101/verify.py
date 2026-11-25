#!/usr/bin/env python3
"""Independent audits of the grid-circle family: safe layers and terminal gaps."""
from collections import Counter
from math import comb


def edges(m, n):
    return [sum(1 << k for k in (0, 1+i, 1+m+j, 1+m+n+i*n+j))
            for i in range(m) for j in range(n)]


def safe_polynomial(m, n):
    """Formula via conditioning on the center and row/column choices."""
    N = (m+1)*(n+1)
    out = Counter({k: comb(N-1, k) for k in range(N)})
    for a in range(m+1):
        for b in range(n+1):
            ways = comb(m, a)*comb(n, b)
            for t in range(m*n-a*b+1):
                out[1+a+b+t] += ways*comb(m*n-a*b, t)
    return +out


def expected_terminal_polynomial(m, n):
    """Coefficient formula from the earlier K0599 theorem."""
    N = (m+1)*(n+1)
    out = Counter({N-1: 1})
    out[N-m] += 1
    out[N-n] += 1
    for a in range(m):
        for b in range(n):
            out[N-a-b-(m-a)*(n-b)] += comb(m, a)*comb(n, b)
    return out


def brute_all_subsets(m, n):
    """Directly test all labeled point subsets; no transversal formula used."""
    N = (m+1)*(n+1)
    E = edges(m, n)
    layers = Counter()
    terminals = Counter()
    for mask in range(1 << N):
        if any(mask & e == e for e in E):
            continue
        layers[mask.bit_count()] += 1
        if all(any((mask | (1 << i)) & e == e for e in E)
               for i in range(N) if not (mask >> i & 1)):
            terminals[mask.bit_count()] += 1
    return layers, terminals


def transversal_enumeration(m, n):
    """Enumerate row/column subsets and test minimality by deleting each point."""
    N = (m+1)*(n+1)
    E = edges(m, n)
    ans = Counter({N-1: 1})  # the singleton transversal {O}
    for rows in range(1 << m):
        for cols in range(1 << n):
            T = 0
            for i in range(m):
                if rows >> i & 1:
                    T |= 1 << (1+i)
            for j in range(n):
                if cols >> j & 1:
                    T |= 1 << (1+m+j)
            for i in range(m):
                for j in range(n):
                    if not (rows >> i & 1) and not (cols >> j & 1):
                        T |= 1 << (1+m+n+i*n+j)
            if not all(T & e for e in E):
                raise AssertionError('transversal construction failed')
            if all(any((T ^ (1 << k)) & e == 0 for e in E)
                   for k in range(N) if T >> k & 1):
                ans[N-T.bit_count()] += 1
    return ans


def two_row_polynomial(n):
    N = 3*(n+1)
    ans = Counter({N-1: 1})
    ans[N-2] += 1
    ans[N-n] += 1
    for b in range(n):
        ans[n+3+b] += comb(n, b)
    ans[2*n+2] += 2*(2**n-1)
    return ans


def main():
    full = ((2, 2), (2, 3), (2, 4), (3, 3))
    for m, n in full:
        safe, terminal = brute_all_subsets(m, n)
        assert safe == safe_polynomial(m, n), (m, n, 'safe polynomial')
        independent_total = (1 << ((m+1)*(n+1)-1)) + sum(
            comb(m, a)*(2**m+2**(m-a))**n for a in range(m+1))
        assert sum(safe.values()) == independent_total
        t = min(m, n)
        assert (sum(safe.values())-(1 << ((m+1)*(n+1)-1)))*8**t <= \
            (1 << ((m+1)*(n+1)-1))*7**t
        assert terminal == expected_terminal_polynomial(m, n), (m, n, 'terminal polynomial')
        assert terminal == transversal_enumeration(m, n), (m, n, 'minimal transversals')
        print(f'full {m}x{n}: {sum(safe.values())} safe subsets, '
              f'{sum(terminal.values())} maximal subsets, s={min(terminal)}, K={max(terminal)}')

    checked = 0
    for m, n in [(2, n) for n in range(2, 11)] + [(k, k) for k in range(2, 8)]:
        terminal = transversal_enumeration(m, n)
        assert terminal == expected_terminal_polynomial(m, n)
        assert min(terminal) == m+n+1 and terminal[min(terminal)] == 1
        assert max(terminal) == (m+1)*(n+1)-1 and terminal[max(terminal)] == 1
        if m == 2:
            assert terminal == two_row_polynomial(n)
            spectrum = set(range(n+3, 2*n+4)) | {3*n+1, 3*n+2}
            assert set(terminal) == spectrum
            gaps = set(range(min(terminal), max(terminal)+1)) - spectrum
            assert gaps == set(range(2*n+4, 3*n+1))
        checked += 1
    print(f'{checked} further transversal-enumerated families: all formulas and gaps verified')
    print('all independent checks passed')


if __name__ == '__main__':
    main()
