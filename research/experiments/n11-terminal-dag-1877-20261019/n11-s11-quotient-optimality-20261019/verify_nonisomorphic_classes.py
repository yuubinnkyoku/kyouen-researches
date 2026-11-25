"""Exact color refinement plus finite exhaustive permutations to separate classes."""
from collections import defaultdict,Counter
from itertools import permutations

def distinct_classes(signatures):
    # Each signature is (n, set_of_minimal_forbidden_masks).
    graphs=[]
    for n,bad in signatures:
        bad=sorted(bad)
        adj=[set() for _ in range(n+len(bad))]
        labels=['m']*n+['e'+str(mask.bit_count()) for mask in bad]
        for j,mask in enumerate(bad):
            for i in range(n):
                if mask>>i&1:
                    adj[i].add(n+j);adj[n+j].add(i)
        graphs.append((adj,labels))
    # Global exact color identifiers, not hashes, across all graphs.
    keys=sorted({label for adj,labels in graphs for label in labels})
    cmap={key:i for i,key in enumerate(keys)}
    colors=[[cmap[x] for x in labels] for adj,labels in graphs]
    for round in range(12):
        sigs=[[(col[i],tuple(sorted(col[j] for j in adj[i]))) for i in range(len(col))] for (adj,_),col in zip(graphs,colors)]
        keys=sorted({key for row in sigs for key in row})
        cmap={key:i for i,key in enumerate(keys)}
        colors=[[cmap[key] for key in row] for row in sigs]
    buckets=defaultdict(list)
    for idx,col in enumerate(colors):buckets[tuple(sorted(Counter(col).items()))].append(idx)
    collisions=[group for group in buckets.values() if len(group)>1]
    print('color-refinement collision groups',collisions,flush=True)
    # Remaining candidate pairs must be exhaustively proved non-isomorphic.
    for group in collisions:
        for aidx in range(len(group)):
            for bidx in range(aidx+1,len(group)):
                a,b=group[aidx],group[bidx]
                n,aa=signatures[a];nn,bb=signatures[b]
                assert n==nn
                bb=set(bb);aa=set(aa)
                for perm in permutations(range(n)):
                    mapped={sum(1<<perm[i] for i in range(n) if mask>>i&1) for mask in aa}
                    if mapped==bb:raise ValueError(f'classes {a} and {b} are isomorphic')
    print('PASS all',len(signatures),'representative forbidden hypergraphs pairwise non-isomorphic',flush=True)

