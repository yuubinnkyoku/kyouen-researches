"""Independent coefficient-DP and partition-Moebius count for five labelled 4-edges."""
from collections import defaultdict
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent

def counts_for_k(k):
    # [x_1^4 ... x_k^4 z^n] product_{nonempty T subset [k]} (1-z product_{i in T} x_i)^(-1)
    dp={(0,)*k+(0,):1}
    for mask in range(1,1<<k):
        nxt=defaultdict(int)
        for state,ways in dp.items():
            bound=min((4-state[i] for i in range(k) if mask>>i&1),default=0)
            for multiplicity in range(bound+1):
                t=tuple(state[i]+(multiplicity if mask>>i&1 else 0) for i in range(k))+(state[-1]+multiplicity,)
                nxt[t]+=ways
        dp=nxt
    return {n:dp.get((4,)*k+(n,),0) for n in range(21)}

A={k:counts_for_k(k) for k in range(1,6)}
# Signed Stirling numbers of the first kind, n=5.
weights={1:24,2:-50,3:35,4:-10,5:1}
rows=[]
for n in range(4,21):
    patterns=A[5][n]
    distinct=sum(weights[k]*A[k][n] for k in range(1,6))
    assert distinct>=0
    rows.append((n,patterns,distinct))
assert sum(r[1] for r in rows)==507549
assert sum(r[2] for r in rows)==469368
for line in (HERE/'all_patterns_results.txt').read_text().splitlines():
    m=re.match(r'n=(\d+) patterns=(\d+) distinct=(\d+)',line)
    assert m and tuple(map(int,m.groups())) in rows
for line in (HERE/'independent_results.txt').read_text().splitlines():
    m=re.match(r'n=(\d+) patterns=(\d+) distinct=(\d+)',line)
    assert m and tuple(map(int,m.groups())) in rows
print('PASS: coefficient DP + partition Moebius agrees with both complete C++ enumerators')
print('patterns:',sum(r[1] for r in rows),'distinct:',sum(r[2] for r in rows))
