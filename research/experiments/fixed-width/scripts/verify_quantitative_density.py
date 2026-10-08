#!/usr/bin/env python3
"""Independent finite audit of the QR/CRT lemma, not the unbounded theorem."""
from itertools import product
from math import prod

def primes(n):
    return [p for p in range(3, n) if all(p % k for k in range(2, int(p**0.5)+1))]

def square_filter(p, c, n):
    qr = {x*x % p for x in range(p)}
    return {i for i in range(p) if (n - (2*i+c)**2) % p in qr}

def equation_filter(p, c, n):
    return {i for i in range(p) if any((d*d+(2*i+c)**2-n) % p == 0 for d in range(p))}

def main():
    count = 0
    for p in primes(73):
        if p % 4 != 3: continue
        for c, n in product(range(p), repeat=2):
            a, b = square_filter(p, c, n), equation_filter(p, c, n)
            assert a == b and len(a) <= (p+3)//2, (p, c, n)
            count += 1
        print(f"p={p}: PASS all {p*p} coefficient choices")
    ps = [7,11,19]
    Q = prod(ps)
    bound = prod((p+3)//2 for p in ps)
    for c, n in [(0,1),(4,9),(19,97),(25,0)]:
        masks = [square_filter(p,c%p,n%p) for p in ps]
        enumerated = sum(all(i%p in mask for p,mask in zip(ps,masks)) for i in range(Q))
        assert enumerated == prod(map(len,masks)) <= bound
        print(f"CRT({c},{n}): {enumerated}/{Q} <= {bound}: PASS")
    print(f"PASS {count} local conditions, 4 CRT checks")

if __name__ == "__main__":
    main()
