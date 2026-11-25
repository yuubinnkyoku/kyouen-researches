#!/usr/bin/env python3
"""Independent residual recursion for the sampled high-value cover-two witnesses."""
from functools import lru_cache
import json
from pathlib import Path


@lru_cache(None)
def grundy(n,edges):
    if not n:return 0
    options=set()
    for v in range(n):
        reduced=[e&~(1<<v) for e in edges];blocked=0
        for edge in reduced:
            if edge.bit_count()==1:blocked|=edge
        remaining=[u for u in range(n) if u!=v and not blocked>>u&1]
        active=sum(1<<u for u in remaining)
        candidates={sum(1<<j for j,u in enumerate(remaining) if e>>u&1)
                    for e in reduced if not e&~active}
        minimal=tuple(sorted(e for e in candidates if not any(f!=e and f&e==f for f in candidates)))
        assert all(e.bit_count()>=2 for e in minimal)
        options.add(grundy(len(remaining),minimal))
    result=0
    while result in options:result+=1
    return result


def main():
    directory=Path(__file__).resolve().parent;records=[]
    for n in (10,12,14):
        row=json.loads((directory/'output'/('n'+str(n)+'.json')).read_text())
        edges=tuple(sorted(row['witness_edges']))
        assert all(e.bit_count()==3 and e&3 for e in edges)
        value=grundy(n,edges);assert value==row['maximum_found']
        records.append(dict(n=n,edges=edges,grundy=value,cpp_discovery_samples=row['evaluated']))
    output=dict(audit='PASS',independent_implementation='labeled residual shrink and blocked-point deletion recursion',
                records=records,limitation='no exhaustive census or universal cover-two upper bound')
    (directory/'output/audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
