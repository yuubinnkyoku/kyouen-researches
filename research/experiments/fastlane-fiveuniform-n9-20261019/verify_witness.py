"""Independent small witness verifier using recursive memoization over occupied sets."""
from functools import lru_cache
from pathlib import Path
import json

data=json.loads((Path(__file__).parent/'results.json').read_text())
for rec in data['records']:
    n=rec['n']
    for kind in ('witness_bitmasks','triple_free_witness_bitmasks'):
        E=rec[kind]
        if E is None: continue
        assert len(set(E))==5 and all(e.bit_count()==4 for e in E)
        assert set().union(*({i for i in range(n) if e>>i&1} for e in E))==set(range(n))
        if kind.startswith('triple'):
            assert all((E[i]&E[j]).bit_count()<=2 for i in range(5) for j in range(i))
        @lru_cache(None)
        def g(occ):
            opts={g(occ|(1<<i)) for i in range(n)
                  if not (occ>>i&1) and all(((occ|(1<<i))&e)!=e for e in E)}
            mex=0
            while mex in opts:mex+=1
            return mex
        children=[g(1<<i) for i in range(n)]
        target=rec['maximum_grundy_spanning'] if kind=='witness_bitmasks' else max(map(int,rec['distribution_triple_free_spanning']))
        assert g(0)==target,(n,kind,g(0),target)
        print(n,kind,'g=',g(0),'children=',children,'safe_states=',g.cache_info().currsize)
