"""Finite mex-algebra certificate for the universal h<=3 capacity-game bound.

The mathematical proof is by induction on the sum of the top h occupancies.
Only the 15 subsets of at most three of four possible child pairs are checked.
"""
from itertools import combinations

T = {(0, 1), (1, 0), (2, 3), (3, 2)}

def mex(values):
    n = 0
    while n in values:
        n += 1
    return n

def phi(children):
    even = mex({u for u, v in children})
    odd = mex({v for u, v in children} | {even})
    return even, odd

def main():
    count = 0
    for k in range(4):
        for children in combinations(sorted(T), k):
            assert phi(children) in T, (children, phi(children))
            count += 1
    assert count == 15
    assert phi(T) == (4, 5)
    print("PASS 15 subsets, first four-type obstruction (4,5)")

if __name__ == "__main__":
    main()
