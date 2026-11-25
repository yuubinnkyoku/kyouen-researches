#!/usr/bin/env python3
"""Independent standard-library checker for a shared S11 residual-game proof DAG.

Checks exact hypergraph transitions, explicit vertex permutations, AND/OR
outcomes, original S11 geometry, and the 672 S10 witness obligations.
Does not trust saved terminal verdicts or use networkx/ILP/optimizers.
"""
import json,sys
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'n11-s11-quotient-optimality-20261019'))
from verify_class_cover_189 import v
from itertools import combinations

def require(ok,msg):
    if not ok:raise ValueError(msg)

def check_signature(n,bad):
    require(isinstance(n,int) and 0<=n<=18,'invalid vertex count')
    require(isinstance(bad,list) and len(set(bad))==len(bad),'duplicate forbidden edge')
    require(bad==sorted(bad),'noncanonical edge list')
    for e in bad:
        require(isinstance(e,int) and 2<=e.bit_count()<=4 and e<(1<<n),'bad forbidden edge')
        require(not any(e!=f and e&f==f for f in bad),'nonminimal forbidden edge')

def check_map(src_n,src_bad,dst_n,dst_bad,perm):
    require(src_n==dst_n,'isomorphism vertex count mismatch')
    require(isinstance(perm,list) and sorted(perm)==list(range(src_n)),'invalid vertex permutation')
    translated=[]
    for e in src_bad:
        translated.append(sum(1<<perm[i] for i in range(src_n) if e>>i&1))
    require(set(translated)==set(dst_bad),'false hypergraph isomorphism')

def successor(n,bad,move):
    """Independently reduce an impartial placement game after one legal move.

    A remaining point becomes illegal exactly when a forbidden pair contains
    it and the just-played point. Larger constraints survive with the played
    vertex deleted. Constraints containing a newly illegal vertex disappear.
    """
    require(0<=move<n,'move out of range')
    pair_bans={e^(1<<move) for e in bad if e.bit_count()==2 and (e>>move&1)}
    available=[i for i in range(n) if i!=move and (1<<i) not in pair_bans]
    remaining=sum(1<<i for i in available)
    allowed=remaining|(1<<move)
    new=[]
    for e in bad:
        if e&~allowed:continue
        rem=e&remaining
        require(rem.bit_count()>=2,'illegal singleton constraint after move')
        renumbered=sum(1<<j for j,i in enumerate(available) if rem>>i&1)
        new.append(renumbered)
    new=sorted(set(new),key=lambda e:(e.bit_count(),e))
    minimal=[]
    for e in new:
        if not any(e&f==f for f in minimal):minimal.append(e)
    return len(available),sorted(minimal)

@lru_cache(maxsize=1024)
def board_signature(p):
    require(p.bit_count() in (10,11) and v.safe(p) and v.canonical(p)==p,'invalid board root')
    base=v.points(p)
    moves=v.legal(p)
    n=len(moves)
    bad=[]
    for i,j in combinations(range(n),2):
        if any(v.circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&b==b for b in bad):continue
        if any(v.circle(a,moves[i],moves[j],moves[k]) for a in base):bad.append(e)
    for ids in combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&b==b for b in bad):continue
        if v.circle(*(moves[i] for i in ids)):bad.append(e)
    return n,sorted(bad)

def verify():
    cert=json.loads((HERE/'joint_dag_optimized_final.json').read_text())
    require(cert['format']=='n11-s11-shared-residual-hypergraph-dag-v1','invalid format')
    nodes=cert['nodes']
    require(len(nodes)==1877,'unexpected DAG node count')
    sig=[]
    for j,node in enumerate(nodes):
        n,bad=node['n'],node['bad']
        check_signature(n,bad)
        require(isinstance(node['win'],bool),'missing exact verdict')
        sig.append((n,bad))
    edges=0
    for j,node in enumerate(nodes):
        n,bad=sig[j]
        outgoing=node['edges']
        require(isinstance(outgoing,list),'invalid edge list')
        require(len(outgoing)==(1 if node['win'] else n),'wrong AND/OR edge count')
        seen=set()
        for entry in outgoing:
            require(isinstance(entry,list) and len(entry)==3,'bad edge entry')
            move,target,perm=entry
            require(isinstance(move,int) and move not in seen and 0<=move<n,'duplicate or illegal move')
            seen.add(move)
            require(isinstance(target,int) and 0<=target<len(nodes),'invalid child reference')
            require(sig[target][0]<n,'cycle/non-decreasing game size')
            child_n,child_bad=successor(n,bad,move)
            check_map(child_n,child_bad,*sig[target],perm)
            require(nodes[target]['win']!=node['win'],'invalid AND/OR child verdict')
            edges+=1
        if not node['win']:
            require(seen==set(range(n)),'LOSS omitted a legal child')
    require(edges==5097,'unexpected proof edge count')
    root_entries=cert['roots']
    roots={int(key,16):(target,perm) for key,target,perm in root_entries}
    require(len(root_entries)==len(roots)==377,'invalid root list')
    cover=json.loads((HERE/'joint_cover_optimized_final.json').read_text())
    expected={int(r,16) for r in cover['representatives']}
    leaves=set(v.decode_positions(v.LEAVES_B85))
    require(len(leaves)==184,'S10 leaf count mismatch')
    require(set(roots)==expected|leaves and len(expected|leaves)==377,'joint S10/S11 root mismatch')
    reachable=set()
    for p,(target,perm) in roots.items():
        require(not nodes[target]['win'],'S11 root is WIN')
        require(isinstance(target,int) and 0<=target<len(nodes),'invalid root reference')
        check_map(*board_signature(p),*sig[target],perm)
        reachable.add(target)
    todo=list(reachable)
    while todo:
        j=todo.pop()
        for move,target,perm in nodes[j]['edges']:
            if target not in reachable:
                reachable.add(target);todo.append(target)
    require(len(reachable)==len(nodes),'orphan proof nodes')
    selected=set()
    for phex,rhex,perm in cover['witnesses']:
        p,r=int(phex,16),int(rhex,16)
        require(p not in selected and r in roots,'duplicate or unproved witness')
        selected.add(p)
        check_map(*board_signature(p),*board_signature(r),perm)
    require(len(selected)==352,'wrong S11 witness count')
    s8=set(v.decode_positions(v.ROOTS_B85))
    require(len(s8)==18,'wrong S8 root count')
    obligations=set().union(*(v.children(p) for p in s8))
    require(len(obligations)==387,'wrong S9 obligation count')
    boundary=set().union(*(v.children(p) for p in obligations))
    require(len(boundary)==3044,'wrong S10 boundary count')
    cover_map={p:{v.canonical(p^(1<<i)) for i in v.points(p)}&obligations for p in boundary}
    require(set().union(*(cover_map[p] for p in leaves))==obligations,'S8 LOSS root proof incomplete')
    packed=v.decode(v.WEIGHTS_B85)
    sorted_obligations=sorted(obligations)
    weights={p:(packed[i//4]>>(2*(i%4)))&3 for i,p in enumerate(sorted_obligations)}
    require(len(packed)==(len(sorted_obligations)+3)//4 and set(weights.values())<={0,1,2},'bad dual weights')
    require(tuple(sum(w==k for w in weights.values()) for k in (2,1,0))==(81,203,103),'dual weight counts changed')
    high={p for p in boundary if sum(weights[q] for q in cover_map[p])>2}
    require(len(high)==672,'wrong S10 obligation count')
    halves={p for p in obligations if weights[p]==1}
    graph={p:set() for p in halves}
    for p in boundary-high:
        pair=list(cover_map[p]&halves)
        if len(pair)==2:
            a,b=pair;graph[a].add(b);graph[b].add(a)
    seen=set();sizes=[]
    for p in halves:
        if p in seen:continue
        todo=[p];seen.add(p);count=0
        while todo:
            q=todo.pop();count+=1
            for r in graph[q]-seen:
                seen.add(r);todo.append(r)
        sizes.append(count)
    require(sorted(sizes)==[13,19,46,125] and 81+sum((x+1)//2 for x in sizes)==184,'184-leaf lower bound failed')
    allowed=set()
    for p in high:
        children=v.children(p)
        allowed.update(children)
        require(bool(children&selected),f'uncovered S10 WIN obligation {p:032x}')
    require(selected<=allowed,'unreachable witness board')
    print(f'PASS: {len(nodes)} shared residual games, {edges} independently checked proof edges')
    print(f'PASS: {len(roots)} terminal S10/S11 roots all LOSS; {len(selected)} geometrically mapped witnesses')
    print(f'PASS: all {len(high)} S10 WIN obligations have a certified LOSS child')
    print(f'PASS: 18 S8 LOSS roots, 387 S9 obligations, 184 S10 LOSS leaves, minimality lower bound 184')
    print('Standard 11x11 empty-board outcome: UNKNOWN')

if __name__=='__main__':verify()
