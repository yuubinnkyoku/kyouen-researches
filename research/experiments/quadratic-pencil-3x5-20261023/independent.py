#!/usr/bin/env python3
"""Independent 4x4 determinant and top-down recursive mex check."""
from itertools import combinations,permutations
from fractions import Fraction
from functools import lru_cache
import json,sys

def det4(a):
    ans=0
    for p in permutations(range(4)):
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        prod=1
        for i in range(4):prod*=a[i][p[i]]
        ans+=(-1 if inversions%2 else 1)*prod
    return ans

def main():
    data=json.load(open(sys.argv[1],encoding="utf-8"))
    pts=[tuple(v) for v in data["points"]]
    roots=set(data["exceptional_values"])
    n=len(pts)
    checked=0
    for case in data["cases"]:
        label=case["lambda_value"]
        lam=(next(Fraction(k) for k in range(100)
                  if str(Fraction(k)) not in roots)
             if label=="generic" else Fraction(label))
        by_point=[[] for _ in pts]
        forbidden=0
        for ids in combinations(range(n),4):
            mat=[[x*x*lam.denominator+y*y*lam.numerator,
                  x*lam.denominator,y*lam.denominator,lam.denominator]
                 for x,y in (pts[i] for i in ids)]
            if det4(mat):continue
            forbidden+=1
            for i in ids:
                by_point[i].append(sum(1<<j for j in ids if j!=i))
        @lru_cache(None)
        def grundy(mask):
            values=set()
            for i in range(n):
                if mask>>i&1:continue
                if any(mask&tri==tri for tri in by_point[i]):continue
                values.add(grundy(mask|(1<<i)))
            v=0
            while v in values:v+=1
            return v
        assert grundy(0)==case["root_grundy"],label
        assert grundy.cache_info().currsize==case["safe_positions"],label
        assert forbidden==case["forbidden_quadruples"],label
        assert [list(pts[i]) for i in range(n) if grundy(1<<i)==0]==case["winning_first_moves"],label
        checked+=grundy.cache_info().currsize
    print("PASS",len(data["cases"]),"parameter types;",checked,"safe positions")
if __name__=="__main__":main()
