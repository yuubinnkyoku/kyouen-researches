"""Independent integer determinant audit for graph -> circle-board safe extensions.

No repository imports; exhaustive graph family and subset checks.
"""
from itertools import combinations, permutations
from math import lcm
import json
from pathlib import Path


def det4(rows):
    # Generic Leibniz expansion, intentionally independent of specialized geometry.
    total = 0
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i+1,4))
        term = 1
        for i in range(4):
            term *= rows[i][p[i]]
        total += (-1 if inversions % 2 else 1) * term
    return total


def circle_board(n, edges):
    params = [10**i for i in range(n)] + [-10**u-10**v for u,v in edges]
    scale = lcm(*(abs(t)*(1+4*t**4) for t in params)) if params else 1
    points = [(0,0)] + [(scale//(t*(1+4*t**4)), 2*scale*t//(1+4*t**4)) for t in params]
    return points


def forbidden(points):
    result = set()
    for quad in combinations(range(len(points)), 4):
        rows = [[x*x+y*y,x,y,1] for x,y in (points[i] for i in quad)]
        if det4(rows) == 0:
            result.add(quad)
    return result


def check(n, edges):
    points = circle_board(n, edges)
    bad = forbidden(points)
    expected = {(0, u+1, v+1, n+1+i) for i,(u,v) in enumerate(edges)}
    assert bad == expected, (n, edges, bad ^ expected)
    fixed = {0} | set(range(n+1,len(points)))
    safe_counts = {}
    maximal_sizes = []
    for mask in range(1<<n):
        selected = {i+1 for i in range(n) if mask >> i & 1}
        full = selected | fixed
        geometric_safe = all(not set(quad) <= full for quad in bad)
        graph_safe = all(not (mask >> u & 1 and mask >> v & 1) for u,v in edges)
        assert geometric_safe == graph_safe, (n,edges,mask)
        if geometric_safe:
            k = mask.bit_count()
            safe_counts[k] = safe_counts.get(k,0)+1
            if all((mask >> j & 1) or any((j==u and mask >> v & 1) or (j==v and mask >> u & 1)
                                              for u,v in edges) for j in range(n)):
                maximal_sizes.append(k)
    # Geometric terminal condition and graph independent domination, compared per subset.
    for mask in range(1<<n):
        full = fixed | {j+1 for j in range(n) if mask >> j & 1}
        if any(set(quad) <= full for quad in bad):
            continue
        terminal = all(any(set(quad) <= (full|{j+1}) for quad in bad)
                       for j in range(n) if not (mask >> j & 1))
        dominating = all((mask >> j & 1) or any(
            (j==u and mask >> v & 1) or (j==v and mask >> u & 1)
            for u,v in edges) for j in range(n))
        assert terminal == dominating, (n, edges, mask)
    return {'n':n,'m':len(edges),'safe_count':sum(safe_counts.values()),
            'independence_polynomial':[safe_counts.get(k,0) for k in range(n+1)],
            'alpha':max(safe_counts) if safe_counts else 0,
            'minimum_maximal':min(maximal_sizes) if maximal_sizes else 0,
            'maximum_maximal':max(maximal_sizes) if maximal_sizes else 0,
            'maximal_count':len(maximal_sizes), 'four_sets_checked':len(points)*(len(points)-1)*(len(points)-2)*(len(points)-3)//24}


def main():
    results=[]
    for n in range(5):
        edges_all=list(combinations(range(n),2))
        for m in range(1<<len(edges_all)):
            edges=[e for i,e in enumerate(edges_all) if m>>i&1]
            results.append(check(n,edges))
    # An unbounded-gap family's finite instances, including a 6-vertex star.
    stars=[check(t+1,[(0,i) for i in range(1,t+1)]) for t in range(1,6)]
    for t,r in enumerate(stars,1):
        assert r['safe_count']==2**t+1
        assert r['alpha']==t
        assert r['minimum_maximal']==1
        assert r['maximal_count']==2
    # Corona graph H: one pendant leaf per original vertex. Its maximal independent
    # sets are in bijection with ALL independent sets of the original graph.
    coronas=[]
    for n in range(4):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[e for i,e in enumerate(pairs) if mask>>i&1]
            h_edges=edges+[(i,n+i) for i in range(n)]
            r=check(2*n,h_edges)
            expected=sum(all(not (s>>u&1 and s>>v&1) for u,v in edges)
                         for s in range(1<<n))
            assert r['maximal_count']==expected, (n,edges,r)
            assert r['minimum_maximal']==r['maximum_maximal']==n
            coronas.append(r)
    for n,edges in [(4,[(0,1),(1,2),(2,3)]),
                    (4,list(combinations(range(4),2)))]:
        r=check(2*n,edges+[(i,n+i) for i in range(n)])
        expected=sum(all(not (s>>u&1 and s>>v&1) for u,v in edges)
                     for s in range(1<<n))
        assert r['maximal_count']==expected
        assert r['minimum_maximal']==r['maximum_maximal']==n
        coronas.append(r)
    all_results=results+stars+coronas
    out={'scope':'all labelled graphs n<=4; stars t<=5; corona graphs n<=3 plus 2 n4 cases',
         'graphs_checked':len(all_results),
         'quadruples_checked':sum(r['four_sets_checked'] for r in all_results),
         'safe_subsets_checked':sum(1<<r['n'] for r in all_results),
         'stars':stars, 'coronas_checked':len(coronas),
         'corona_maximal_counts':[r['maximal_count'] for r in coronas]}
    dest=Path(__file__).resolve().parents[1]/'output'/'safe_extensions_20261019.json'
    dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':
    main()
