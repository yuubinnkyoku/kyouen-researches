#!/usr/bin/env python3
"""Complete loose (Berge-acyclic) three-uniform hyperforests by edge budget."""
from collections import Counter
from functools import reduce
import json
from operator import xor
from pathlib import Path
import shutil
import subprocess
import tempfile

MEMO={};TRANSITIONS=0


def mex(options):
    g=0
    while g in options:g+=1
    return g


def tree_code(n,edges):
    adjacency=[[] for _ in range(n+len(edges))]
    for j,edge in enumerate(edges,n):
        for v in range(n):
            if edge>>v&1:adjacency[v].append(j);adjacency[j].append(v)
    def rooted(v,parent):
        return (0 if v<n else 1,tuple(sorted(rooted(w,v) for w in adjacency[v] if w!=parent)))
    assert sum(map(len,adjacency))==2*(len(adjacency)-1)
    return min(rooted(v,-1) for v in range(n))


def normalize(vertices,edges):
    order=[v for v in range(vertices.bit_length()) if vertices>>v&1]
    mapping={v:i for i,v in enumerate(order)}
    return len(order),tuple(sorted({sum(1<<mapping[v] for v in order if edge>>v&1)
                                   for edge in edges if not edge&~vertices}))


def components(n,edges):
    parent=list(range(n))
    def find(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    active=0
    for edge in edges:
        active|=edge
        vs=[v for v in range(n) if edge>>v&1]
        for v in vs[1:]:parent[find(v)]=find(vs[0])
    groups={}
    for v in range(n):
        if active>>v&1:groups[find(v)]=groups.get(find(v),0)|(1<<v)
    return (n-active.bit_count())%2,[normalize(vertices,[e for e in edges if e&vertices]) for vertices in groups.values()]


def grundy(n,edges):
    global TRANSITIONS
    free,parts=components(n,edges)
    if not parts:return free
    if len(parts)>1 or free or parts[0][0]<n:
        return free^reduce(xor,(grundy(*part) for part in parts),0)
    code=tree_code(n,edges)
    if code in MEMO:return MEMO[code]
    options=set()
    for v in range(n):
        reduced=[edge&~(1<<v) for edge in edges]
        blocked=0
        for edge in reduced:
            if edge.bit_count()==1:blocked|=edge
        active=((1<<n)-1)&~(1<<v)&~blocked
        child=normalize(active,[e for e in reduced if e.bit_count()>=2 and not e&~active])
        options.add(grundy(*child));TRANSITIONS+=1
    result=mex(options);MEMO[code]=result
    return result


def main():
    directory=Path(__file__).resolve().parent
    previous={tree_code(1,()):(1,())};generated_codes={}
    records=[];summaries=[];connected_values={}
    for h in range(1,9):
        current={}
        for n,edges in previous.values():
            for v in range(n):
                new=tuple(sorted(edges+((1<<v)|(1<<n)|(1<<(n+1)),)))
                current.setdefault(tree_code(n+2,new),(n+2,new))
        hist=Counter()
        for code,(n,edges) in sorted(current.items()):
            g=grundy(n,edges);hist[g]+=1
            records.append(dict(h=h,n=n,edges=edges,grundy=g))
        connected_values[h]=set(hist)
        generated_codes[h]=set(current)
        summaries.append(dict(edges=h,connected_types=len(current),histogram=dict(sorted(hist.items())),maximum=max(hist)))
        print(summaries[-1],flush=True)
        previous=current
    # Separate all-subsets C++ implementation, reusing an already audited verifier.
    root=directory.parents[2]
    # A complete, independently generated Venn-type census exists through h=5.
    small=json.loads((root/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())
    for h in range(1,6):
        independent=set()
        for row in small['records']:
            if row['h']!=h or row['n']!=2*h+1:continue
            free,parts=components(row['n'],row['edges'])
            if free or len(parts)!=1:continue
            independent.add(tree_code(row['n'],row['edges']))
        assert independent==generated_codes[h]
    cpp=root/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-pure3-forest-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';executable=temp/'native.exe';values=temp/'values.bin'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],r['h'],*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(executable)],check=True)
        native=json.loads(subprocess.check_output([str(executable),str(data),str(values)],text=True))
        assert values.read_bytes()==bytes(r['grundy'] for r in records)
    possibilities={0:{0,1}};decomposition={(0,0):[],(0,1):['one_free_point']}
    for h in range(1,9):
        possibilities[h]=set()
        for k in range(1,h+1):
            for a in connected_values[k]:
                for b in possibilities[h-k]:
                    possibilities[h].add(a^b)
                    decomposition.setdefault((h,a^b),[(k,a)]+decomposition[(h-k,b)])
    output=dict(audit='PASS',connected_summaries=summaries,types_compared=len(records),
                independent_generation_verified_through_edges=5,
                cpp_safe_states=native['safe_states'],mixed_residual_tree_cache=len(MEMO),
                recursive_transitions=TRANSITIONS,
                forest_spectra={h:sorted(v) for h,v in possibilities.items()},
                largest_forest_witnesses={h:decomposition[(h,max(v))] for h,v in possibilities.items()},records=records)
    head={key:value for key,value in output.items() if key!='records'}
    text=json.dumps(head,indent=2);text=text[:-2]+',\n  "records": [\n'+',\n'.join('    '+json.dumps(r,separators=(',',':')) for r in records)+'\n  ]\n}\n'
    json.loads(text);target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True);target.write_text(text,encoding='utf-8')
    print(json.dumps(head,indent=2),flush=True)


if __name__=='__main__':main()
