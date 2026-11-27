#!/usr/bin/env python3
# Gate checks for PG(2,q) s=3 two-cone spectrum results.
# Usage: check_gates.py combined.json [--q 7] [--s 3]
import json,sys
from math import comb
d=json.load(open(sys.argv[1]))
q=7; s=3
for i,a in enumerate(sys.argv):
    if a=='--q': q=int(sys.argv[i+1])
    if a=='--s': s=int(sys.argv[i+1])
n=q*q+q+1
assert d['points']==n and d['lines']==n and d['s']==s
from math import comb as C
N3nc,N3c=d['N3nc'],d['N3c']
assert C(n,3)==N3nc+N3c, "triple split"
for m,tbl in d['grundy_tables'].items():
    mi=int(m)
    assert all(int(g)<64 for g in tbl)
    for g,N in tbl.items():
        Dn=d['raw_cone_noncoll'][m][int(g)]; Dc=d['raw_cone_coll'][m][int(g)]
        assert N*C(mi,3)==N3nc*Dn+N3c*Dc, f"identity fail m={m} g={g}"
    # raw cone counts sum to layer sizes
    assert sum(d['raw_cone_noncoll'][m])==d['layers_noncoll'][m], f"nc layer sum m={m}"
    assert sum(d['raw_cone_coll'][m])==d['layers_coll'][m], f"c layer sum m={m}"
# anchors (analytic m=3..5 totals for PG(2,7) s=3)
anchors={3:29260,4:391020,5:3988404}
for m,v in anchors.items():
    got=sum(d['grundy_tables'][str(m)].values())
    assert got==v, f"anchor m={m}: {got} != {v}"
# maximal identity per layer + maximal<=layer
for m in d['maximal_counts']:
    mi=int(m)
    assert d['maximal_counts'][m]*C(mi,3)==N3nc*d['raw_maximal_noncoll'][m]+N3c*d['raw_maximal_coll'][m], f"maximal identity m={m}"
    assert d['raw_maximal_noncoll'][m]<=d['layers_noncoll'][m] and d['raw_maximal_coll'][m]<=d['layers_coll'][m], f"maximal<=layer m={m}"
# weighted total
tot=1+n+C(n,2)+sum(sum(t.values()) for t in d['grundy_tables'].values())
assert tot==d['total_positions'], f"total {tot} vs {d['total_positions']}"
# every layer m>=3 represented up to max_size
for m in range(3,d['max_size']+1):
    assert str(m) in d['grundy_tables'] and str(m) in d['layers_noncoll'] and str(m) in d['layers_coll']
print("ALL GATES PASS")
