#!/usr/bin/env python3
"""Independent generating-function coefficients and partition-lattice Mobius inversion."""


def unrestricted(h,rank=3):
    base=rank+1;total=base**h;dp=[0]*total;dp[0]=1
    powers=[base**i for i in range(h)]
    digits=[[state//power%base for power in powers] for state in range(total)]
    for mask in range(1,1<<h):
        rows=[e for e in range(h) if mask>>e&1];step=sum(powers[e] for e in rows)
        # Unbounded coin update in increasing base-(rank+1) state order.
        for state in range(total):
            if dp[state] and all(digits[state][e]<rank for e in rows):
                dp[state+step]+=dp[state]
    return dp[-1]


def distinct_counts(max_edges,rank=3):
    f=[unrestricted(h,rank) for h in range(max_edges+1)]
    signed=[[1]]
    for h in range(1,max_edges+1):
        row=[0]*(h+1)
        for k in range(1,h+1):
            row[k]=(signed[-1][k-1] if k-1<len(signed[-1]) else 0)-(h-1)*(signed[-1][k] if k<len(signed[-1]) else 0)
        signed.append(row)
    distinct=[sum(signed[h][k]*f[k] for k in range(h+1)) for h in range(max_edges+1)]
    return f,distinct


if __name__=='__main__':
    import json
    f,d=distinct_counts(6)
    assert d[1:6]==[1,3,29,666,28344]
    print(json.dumps(dict(unrestricted=f,distinct=d),indent=2))
