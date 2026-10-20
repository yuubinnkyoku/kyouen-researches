#!/usr/bin/env python3
"""Complete independent finite-field audits for five-row ten-point circles."""
from itertools import product

def square_patterns_by_recurrence(p):
    Q = {x*x % p for x in range(p)}
    out = set()
    for a,b in product(Q, repeat=2):
        z = [a,b]
        for _ in range(3):
            z.append((2*z[-1]-z[-2]-2) % p)
        if all(v in Q for v in z):
            out.add(tuple(z))
    return out

def square_patterns_by_coefficients(p,d):
    Q = {x*x % p for x in range(p)}
    inv = pow(4*d*d % p, -1, p)
    out = set()
    for B,C,D in product(range(p), repeat=3):
        delta = tuple((B*B-4*(j*j*d*d+C*j*d+D)) % p for j in range(5))
        if all(v in Q for v in delta):
            out.add(tuple(v*inv % p for v in delta))
    return out

def main():
    expected = {
        5: {(0,4,1,1,4), (1,1,4,0,4), (1,4,0,4,1),
            (4,0,4,1,1), (4,1,1,4,0)},
        7: {(4,0,1,0,4)}
    }
    for p, want in expected.items():
        by_recurrence = square_patterns_by_recurrence(p)
        assert by_recurrence == want
        for d in range(1,p):
            by_coefficients = square_patterns_by_coefficients(p,d)
            assert by_coefficients == by_recurrence, (p,d)
        for z in sorted(by_recurrence):
            zero_rows = tuple(i for i in range(5) if z[i] == 0)
            assert (len(zero_rows)==1 if p==5 else zero_rows==(1,3))
            print(f"p={p}: normalized squared chords={z}, zero rows={zero_rows}")
        print(f"PASS p={p}: {len(by_recurrence)} patterns, all {p-1} nonzero row spacings, {(p-1)*p**3} coefficient triples")
    print("PASS all assertions")

if __name__ == "__main__":
    main()
