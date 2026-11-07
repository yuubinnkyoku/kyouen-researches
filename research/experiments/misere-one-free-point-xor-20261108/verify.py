#!/usr/bin/env python3
"""Complete small impartial-game DAG audit and all stored pure-triple free pairs."""
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]


def mex(values):
    answer=0
    while answer in values:answer+=1
    return answer


def main():
    directory=Path(__file__).resolve().parent
    nodes=[];lookup={};g=[];h=[];t=[]
    def intern(children):
        key=tuple(sorted(set(children)))
        if key in lookup:return lookup[key]
        identity=len(nodes);lookup[key]=identity;nodes.append(key)
        g.append(mex({g[c] for c in key}))
        value=mex({h[c] for c in key}) if key else 1;h.append(value)
        t.append(mex({t[c] for c in key if h[c]<2}) if value<2 else None)
        return identity
    terminal=intern(())
    previous=[terminal];birthday_counts=[1]
    for birthday in range(1,5):
        current=[intern(previous[j] for j in range(len(previous)) if mask>>j&1)
                 for mask in range(1<<len(previous))]
        assert len(current)==len(set(current))
        previous=current;birthday_counts.append(len(current))
    assert birthday_counts==[1,2,4,16,65536]
    @lru_cache(None)
    def one_free(node):
        return intern([node,*[one_free(child) for child in nodes[node]]])
    histogram=Counter()
    for node in previous:
        other=one_free(node)
        assert h[other]==h[node]^1 and g[other]==g[node]^1
        if h[node]<2:assert t[other]==t[node]^1
        else:assert t[other] is None
        two=one_free(other)
        assert h[two]==h[node] and g[two]==g[node]
        if h[node]<2:assert t[two]==t[node]
        histogram[g[node],h[node],t[node]]+=1
    sources=[]
    for name in ('pure-triple-six-edge-complete-20261108/output/misere_values.json',
                 'pure-triple-seven-edge-complete-20261108/output/misere.json'):
        path=ROOT/'research/experiments'/name;data=json.loads(path.read_text())
        a=data['misere_values_free_zero'];b=data['misere_values_free_one']
        assert len(a)==len(b) and all(y==x^1 for x,y in zip(a,b))
        sources.append(dict(path=path.relative_to(ROOT).as_posix(),kernel_pairs=len(a),
                            sha256_utf8_lf=hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()))
    output=dict(audit='PASS',birthday_counts=birthday_counts,complete_games_through_birthday_four=65536,
                game_dag_positions=len(nodes),pure_triple_kernel_pairs=sum(s['kernel_pairs'] for s in sources),
                source_audits=sources,
                histogram={f'{a},{b},{c}':count for (a,b,c),count in sorted(histogram.items(),key=lambda x:(x[0][0],x[0][1],-1 if x[0][2] is None else x[0][2]))},
                limitation='The universal identity follows by mex induction; finite DAG and stored-data audits are independent checks.')
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='histogram'},indent=2),flush=True)


if __name__=='__main__':main()
