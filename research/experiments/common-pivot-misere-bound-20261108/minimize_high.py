#!/usr/bin/env python3
"""Exhaust all induced subgraphs of the discovered graph; no global minimality."""
import json
from pathlib import Path


def mex(options):
    value=0
    while value in options:value+=1
    return value


def main():
    directory=Path(__file__).resolve().parent
    prior=json.loads((directory/'output/restricted_mutations.json').read_text())
    n=14;adjacency=[1<<v for v in range(n)]
    for edge in prior['edges']:
        u,v=[v for v in range(n) if edge>>v&1]
        adjacency[u]|=1<<v;adjacency[v]|=1<<u
    values=[];best={}
    for remaining in range(1<<n):
        children=[values[remaining&~adjacency[v]] for v in range(n) if remaining>>v&1]
        g=mex({g for g,h,t in children});h=mex({h for g,h,t in children}) if children else 1
        t=mex({t for g,h,t in children if h<2}) if h<2 else None
        values.append((g,h,t))
        if h>=2 or t<4:continue
        m=remaining.bit_count();parity=0 if h==1 else 1
        poison=1 if (m+1)%2==parity else 2
        size=m+poison+1;target=2+t
        if target not in best or size<best[target]['total_legal_points']:
            order=[v for v in range(n) if remaining>>v&1];index={v:i for i,v in enumerate(order)}
            edges=[sum(1<<index[v] for v in order if edge>>v&1) for edge in prior['edges'] if edge&remaining==edge]
            best[target]=dict(total_legal_points=size,link_vertices=m,poison_points=poison,
                              original_vertices=order,link_edges=edges,link_normal=g,link_misere=h,restricted=t)
    output=dict(scope='all induced subgraphs of one discovered fourteen-point graph; no global minimum claim',
                induced_subgraphs=1<<n,best_by_misere_value=best)
    (directory/'output/induced_high.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
