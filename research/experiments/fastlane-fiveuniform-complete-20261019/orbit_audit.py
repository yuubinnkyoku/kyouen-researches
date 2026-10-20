import collections,itertools,json
from pathlib import Path
here=Path(__file__).resolve().parent
rows=[s.strip() for s in (here/'g6patterns_raw.txt').read_text().splitlines() if len(s.strip())==31 and s.strip().isdigit()]
perms=list(itertools.permutations(range(5)))
def permute(t,p):return sum(1<<p[i] for i in range(5) if t>>i&1)
def canon(s):return min(''.join(s[permute(t,p)-1] for t in range(1,32)) for p in perms)
def edges_from_counts(s):
    E=[0]*5;k=0
    for t in range(1,32):
        for _ in range(int(s[t-1])):
            for i in range(5):
                if t>>i&1:E[i]|=1<<k
            k+=1
    return E,k
def grundy(E,n):
    f=(1<<n)-1
    G=[-1]*(f+1)
    for s in range(f,-1,-1):
        if any((s&e)==e for e in E):continue
        values={G[s|1<<i] for i in range(n) if not s>>i&1 and G[s|1<<i]>=0}
        g=0
        while g in values:g+=1
        G[s]=g
    return G[0], [G[1<<i] for i in range(n)],sum(v>=0 for v in G)
cl=collections.Counter(map(canon,rows))
assert len(rows)==240 and sorted(cl.values())==[120,120]
result=[]
for s,multiplicity in sorted(cl.items()):
    E,n=edges_from_counts(s)
    g,ch,safe=grundy(E,n)
    assert g==6 and n==12 and set(range(6)).issubset(ch)
    overlaps=[(E[i]&E[j]).bit_count() for i in range(5) for j in range(i)]
    result.append({'multiplicity_labelled_edges':multiplicity,'n':n,'edge_masks':E,'edge_vertex_lists':[[i for i in range(n) if e>>i&1] for e in E],'overlap_multiset':sorted(overlaps),'grundy':g,'children':ch,'safe_states':safe})
# Add one isolated vertex to the first 12-point example.
E=result[0]['edge_masks'];g,ch,safe=grundy(E,13)
assert g==7 and safe==2*result[0]['safe_states']
print(json.dumps({'g6_labelled_patterns':len(rows),'g6_isomorphism_classes':len(cl),'representatives':result,'free_vertex_13_point':{'edge_masks':E,'grundy':g,'children':ch,'safe_states':safe}},indent=2,ensure_ascii=False))
(here/'orbit_results.json').write_text(json.dumps({'g6_labelled_patterns':len(rows),'g6_isomorphism_classes':len(cl),'representatives':result,'free_vertex_13_point':{'edge_masks':E,'grundy':g,'children':ch,'safe_states':safe}},indent=2,ensure_ascii=False)+'\n')
