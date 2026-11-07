#!/usr/bin/env python3
"""Complete small forbidden families whose every edge contains a fixed pivot."""
from collections import Counter
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('all_clutters',ROOT/
    'research/experiments/incidence-weighted-grundy-bound-20261107/verify.py')
GEN=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(GEN)


def value(n,edges):
    @lru_cache(None)
    def g(s):
        options={g(s|1<<v) for v in range(n) if not s>>v&1
                 and all((s|1<<v)&edge!=edge for edge in edges)}
        result=0
        while result in options:result+=1
        return result
    return g(0)


def main():
    summaries=[]
    for m in range(6):
        histogram=Counter();witnesses={}
        # The link after playing pivot may block any set of outside vertices.
        for blocked in range(1<<m):
            remaining=[v for v in range(m) if not blocked>>v&1]
            for core in GEN.clutters(len(remaining)):
                edges=[1|(1<<(v+1)) for v in range(m) if blocked>>v&1]
                edges.extend(1|sum(1<<(remaining[v]+1) for v in range(len(remaining)) if edge>>v&1)
                             for edge in core)
                g=value(m+1,tuple(edges));histogram[g]+=1
                witnesses.setdefault(g,edges)
        summaries.append(dict(outside_points=m,total_legal_points=m+1,
                              histogram=dict(sorted(histogram.items())),witnesses=witnesses))
    output=dict(scope='every edge contains vertex 0; arbitrary rank; all labeled cases up to six legal points',
                summaries=summaries)
    target=Path(__file__).with_name('output')/'probe.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
