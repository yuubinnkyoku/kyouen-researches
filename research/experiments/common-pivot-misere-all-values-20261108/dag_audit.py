#!/usr/bin/env python3
"""Independent literal game-DAG audit of the cograph recursion without large graphs."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def mex(values):
    result=0
    while result in values:result+=1
    return result


def main():
    directory=Path(__file__).resolve().parent
    nodes=[];index={};normal=[];auxiliary=[];restricted=[]

    def intern(children):
        key=tuple(sorted(set(children)))
        if key in index:return index[key]
        identity=len(nodes);index[key]=identity;nodes.append(key)
        normal.append(mex({normal[c] for c in key}))
        h=mex({auxiliary[c] for c in key}) if key else 1
        auxiliary.append(h)
        restricted.append(mex({restricted[c] for c in key if auxiliary[c]<2}) if h<2 else None)
        return identity

    terminal=intern(());free=intern((terminal,));p3=intern((terminal,free))

    @lru_cache(None)
    def disjoint(left,right):
        if left>right:return disjoint(right,left)
        return intern([disjoint(child,right) for child in nodes[left]]+
                      [disjoint(left,child) for child in nodes[right]])

    roots=[[disjoint(p3,p3),terminal]];records=[]
    for m in range(65):
        if m:
            pair=[]
            for a in (0,1):
                blocks=[disjoint(roots[j][1-a],free) for j in range(m)]
                # A graph join exposes exactly the union of its blocks' options.
                pair.append(intern(child for block in blocks for child in nodes[block]))
            roots.append(pair)
        for a,node in enumerate(roots[m]):
            assert auxiliary[node]==a and restricted[node]==m
            options=sorted({restricted[c] for c in nodes[node] if auxiliary[c]<2})
            assert options==list(range(m))
            one=disjoint(node,free)
            assert auxiliary[one]==1-a and restricted[one]==m^1
            if m>=2:assert normal[node]==m+2
            record=dict(m=m,a=a,normal=normal[node],auxiliary=auxiliary[node],restricted=restricted[node],
                        one_free_auxiliary=auxiliary[one],one_free_restricted=restricted[one])
            if a==0 and m>=2:
                child_values=[];child_free_values=[]
                for child in nodes[node]:
                    h=auxiliary[child];t=restricted[child]
                    child_values.append(2+t if h==1 else 1)
                    other=disjoint(child,free);h=auxiliary[other];t=restricted[other]
                    child_free_values.append(2+t if h==0 else 0)
                pure=mex({auxiliary[node],*child_values})
                pure_free=mex({auxiliary[one],pure,*child_free_values})
                assert pure==m+2 and pure_free==(m+2)^1
                record.update(pure_pivot_auxiliary=pure,pure_one_free_auxiliary=pure_free)
            records.append(record)
    # The DAG's descendants are literal option sets, not assumed h/t profiles.
    original_count=len(nodes)
    for node in range(original_count):
        one=disjoint(node,free)
        if auxiliary[node]<2:
            assert auxiliary[one]==1-auxiliary[node]
        else:assert auxiliary[one]>=2
    payload=json.dumps(nodes,separators=(',',':')).encode()
    output=dict(audit='PASS',maximum_m=64,root_graphs=130,literal_game_positions=len(nodes),
                game_dag_sha256=hashlib.sha256(payload).hexdigest(),records=records,
                independence='Literal option DAG with ordinary disjunctive-sum recursion; no incidence cells or closed-neighborhood graph recursion.',
                limitation='Finite independent audit; the all-m conclusion is the mutual-induction proof.')
    target=directory/'output/dag_audit.json';target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()
