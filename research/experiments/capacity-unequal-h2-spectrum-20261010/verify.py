from itertools import combinations_with_replacement, product
from collections import Counter
from math import comb, prod

configs = states = terminals = 0
for w in range(2, 7):
    for asc in combinations_with_replacement(range(5), w):
        c = tuple(reversed(asc))
        for r in range(2*c[0]+3):
            maximal = []
            for x in product(*(range(z+1) for z in c)):
                if sum(sorted(x, reverse=True)[:2]) > r:
                    continue
                states += 1
                if all(x[i] == c[i] or
                       sum(sorted(x[:i]+(x[i]+1,)+x[i+1:], reverse=True)[:2]) > r
                       for i in range(w)):
                    maximal.append(x)
            predicted = set()
            if c[0]+c[1] <= r:
                predicted.add(c)
            else:
                L, U = max(0,r-c[0]), min(r//2,c[1])
                for b in range(L,U+1):
                    A = r-b
                    if A == b:
                        predicted.add(tuple(min(ci,b) for ci in c))
                    else:
                        for j in range(w):
                            if c[j] >= A:
                                predicted.add(tuple(A if i==j else min(ci,b)
                                                    for i,ci in enumerate(c)))
            assert set(maximal) == predicted, (c,r)
            configs += 1
            terminals += len(maximal)
print('PASS', configs, states, terminals)
