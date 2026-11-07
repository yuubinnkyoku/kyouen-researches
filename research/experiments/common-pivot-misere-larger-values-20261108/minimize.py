#!/usr/bin/env python3
"""All induced subgraphs of the n16 link witness, with poison parity costs."""
import json
from pathlib import Path


def mex(options):
    result=0
    while result in options:result+=1
    return result


def main():
    directory=Path(__file__).resolve().parent
    prior=json.loads((directory/'output/n16.json').read_text());n=prior['vertices']
    adjacency=[1<<v for v in range(n)]
    for edge in prior['edges']:
        u,v=[v for v in range(n) if edge>>v&1];adjacency[u]|=1<<v;adjacency[v]|=1<<u
    values=[];best={}
    for remaining in range(1<<n):
        children=[values[remaining&~adjacency[v]] for v in range(n) if remaining>>v&1]
        g=mex({g for g,h,t in children});h=mex({h for g,h,t in children}) if children else 1
        t=mex({t for g,h,t in children if h<2}) if h<2 else None
        values.append((g,h,t))
        if h>=2 or t<6:continue
        m=remaining.bit_count();parity=0 if h==1 else 1
        poison=1 if (m+1)%2==parity else 2;size=m+poison+1;target=2+t
        if target not in best or size<best[target]['total_legal_points']:
            order=[v for v in range(n) if remaining>>v&1];index={v:i for i,v in enumerate(order)}
            edges=[sum(1<<index[v] for v in order if edge>>v&1) for edge in prior['edges'] if edge&remaining==edge]
            best[target]=dict(total_legal_points=size,link_vertices=m,poison_points=poison,
                              original_vertices=order,link_edges=edges,link_normal=g,link_misere=h,restricted=t)
    output=dict(scope='all induced subgraphs of the discovered sixteen-vertex graph; no global minimum claim',
                induced_subgraphs=1<<n,best_by_misere_value=best)
    (directory/'output/induced.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
