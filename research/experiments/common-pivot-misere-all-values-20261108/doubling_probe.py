#!/usr/bin/env python3
"""Bounded exploratory sums/joins of the two m=2 graphs; not an infinite proof."""
from functools import lru_cache
import json
from pathlib import Path


def mex(values):
    n=0
    while n in values:n+=1
    return n


def main():
    nodes=[];lookup={};values=[]
    def intern(children):
        key=tuple(sorted(set(children)))
        if key in lookup:return lookup[key]
        identity=len(nodes);lookup[key]=identity;nodes.append(key)
        g=mex({values[c][0] for c in key});h=mex({values[c][1] for c in key}) if key else 1
        t=mex({values[c][2] for c in key if values[c][1]<2}) if h<2 else None
        values.append((g,h,t));return identity
    @lru_cache(None)
    def plus(a,b):
        if a>b:return plus(b,a)
        return intern([plus(c,b) for c in nodes[a]]+[plus(a,c) for c in nodes[b]])
    def join(a,b):return intern([*nodes[a],*nodes[b]])
    empty=intern([]);free=intern([empty]);p3=intern([empty,free])
    roots=[[plus(p3,p3),empty]]
    for m in (1,2):
        roots.append([intern(c for j in range(m) for c in nodes[plus(roots[j][1-a],free)]) for a in (0,1)])
    result=[]
    for a in (0,1):
        for b in (0,1):
            x=plus(roots[2][a],roots[2][b])
            row=dict(sum_colors=[a,b],sum_values=values[x],sum_restricted_options=sorted({values[c][2] for c in nodes[x] if values[c][1]<2}))
            row['join_values']={str(color):values[join(x,roots[2][color])] for color in (0,1)}
            result.append(row)
    output=dict(status='BOUNDED_PROBE',records=result,game_positions=len(nodes),
                limitation='No sum law or infinite doubling family is inferred from these cases.')
    target=Path(__file__).resolve().parent/'output/doubling_probe.json'
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
