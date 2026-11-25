#!/usr/bin/env python3
"""Independent finite checks for the local prime lemma; theorem is algebraic."""
for p in (7,11,19,23,31,43,47,59,71,83,103,107,127,131,139,151,163):
    assert all(p % d for d in range(2,int(p**0.5)+1))
    assert p % 4 == 3
    sq={x*x%p for x in range(p)}
    for v in range(p):
        good=sum(1 for z in range(p) if (v-z*z)%p in sq)
        assert good<=(p+3)//2,(p,v,good)
        if v:
            count=sum(1 for z in range(p) for d in range(p) if (d*d+z*z-v)%p==0)
            assert count==p+1,(p,v,count)
    print("PASS",p)
print("PASS local congruence lemma; unbounded theorem has separate proof")
