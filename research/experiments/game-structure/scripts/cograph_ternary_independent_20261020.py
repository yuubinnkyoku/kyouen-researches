#!/usr/bin/env python3
"""Independent priority-queue enumeration of all cograph option signatures by minimum order.
No fixed-n dynamic programming is used. Option sets are frozensets of nimbers.
"""
import argparse, heapq, json

def mex(a):
    k=0
    while k in a:k+=1
    return k

def combined(a,b):
    ga,gb=mex(a),mex(b)
    return (a|b, frozenset({x^gb for x in a}|{ga^y for y in b}))

def enumerate_minimum(nmax):
    initial=frozenset({0})
    queue=[(1, tuple(sorted(initial)), 'v')]
    seen={}
    while queue:
        n, signature, witness=heapq.heappop(queue)
        if n>nmax:break
        sig=frozenset(signature)
        if sig in seen:continue
        seen[sig]=(n,witness)
        # every earlier discovered signature has cost <= n;
        # combine once for each unordered pair, including itself
        for other,(cost,ow) in list(seen.items()):
            if cost+n>nmax:continue
            for op,options in zip('*+',combined(sig,other)):
                if options not in seen:
                    heapq.heappush(queue,(cost+n,tuple(sorted(options)),f'({witness}{op}{ow})'))
    return seen

def explicit_power(k):
    """(n,grundy,option-set), independent algebraic construction."""
    n,g,o=1,1,frozenset({0})
    for _ in range(k):
        oo=frozenset({x^g for x in o})
        assert mex(oo)==0
        o=oo|o
        n*=3
        g*=2
        assert o==frozenset(range(g)) and mex(o)==g
    return n,g,sorted(o)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=400)
    parser.add_argument('--cpp-dump',type=str)
    args=parser.parse_args()
    results=enumerate_minimum(args.max_n)
    by_n={n:0 for n in range(1,args.max_n+1)}
    first={}
    for opts,(n,_) in results.items():
        by_n[n]+=1
        g=mex(opts)
        first[g]=min(first.get(g,n),n)
    if args.cpp_dump:
        from collections import defaultdict
        actual=defaultdict(set)
        with open(args.cpp_dump) as f:
            for line in f:
                n, mask=map(int,line.split())
                actual[n].add(frozenset(i for i in range(64) if mask>>i&1))
        for n in range(1,args.max_n+1):
            expected={s for s,(minimum,_) in results.items() if minimum<=n}
            assert actual[n]==expected, (n,len(actual[n]),len(expected))
        print('PASS: exact signature sets match C++ for every n <=',args.max_n)
    # n=1 yields 1 signature; n>=2 yields exactly one new signature.
    assert all(by_n[n]==1 for n in by_n),(len(results),[(n,k) for n,k in by_n.items() if k!=1])
    # Binary digits of g read as ternary digits.
    for g,n in first.items():
        f=sum(3**i for i in range(g.bit_length()) if g>>i&1)
        assert n==(2 if g==0 else f),(g,n,f)
    assert explicit_power(5)==(243,32,list(range(32)))
    print('PASS independent priority-queue closure',len(results),'signatures, up to n=',args.max_n)
    print('g minima:',dict(sorted(first.items())))
    print('power witness:',explicit_power(5))
    print('new per n:',min(by_n.values()),max(by_n.values()))
    with open('results.json','w') as out:
        json.dump({'nmax':args.max_n,'signature_count':len(results),'min_vertices_by_grundy':dict(sorted(first.items())), 'new_signature_count_by_n':by_n, 'power_witness':explicit_power(5)},out,indent=2)
if __name__=='__main__':main()
