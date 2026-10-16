#!/usr/bin/env python3
"""Stand-alone checker for the 3x3x3 five-point 3D game P certificate.

Verifies all claimed P/N implications after symmetry reduction; does not
calculate Grundy values or trust the certificate generator's search table.
"""
import base64
import hashlib
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import struct
import sys

points = list(product(range(3), repeat=3))
index = {p:i for i,p in enumerate(points)}
perms = []
for perm in permutations(range(4)):
    inversions = sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
    perms.append((perm, -1 if inversions%2 else 1))

def det4(mat):
    return sum(sign*mat[0][p[0]]*mat[1][p[1]]*mat[2][p[2]]*mat[3][p[3]]
               for p,sign in perms)

lifts = [(sum(v*v for v in p),*p) for p in points]
completion = {}
forbidden = 0
for five in combinations(range(27),5):
    base = lifts[five[0]]
    mat = [[lifts[i][j]-base[j] for j in range(4)] for i in five[1:]]
    if det4(mat):
        continue
    forbidden += 1
    edge = sum(1<<i for i in five)
    for i in five:
        rest = edge^(1<<i)
        completion[rest] = completion.get(rest,0)|(1<<i)
assert forbidden == 16026

@lru_cache(None)
def legal(mask):
    blocked = 0
    ids = [i for i in range(27) if (mask>>i)&1]
    for four in combinations(ids,4):
        blocked |= completion.get(sum(1<<i for i in four),0)
    return ((1<<27)-1)&~(mask|blocked)

symmetries = []
for axes in permutations(range(3)):
    for flips in product((0,1),repeat=3):
        symmetries.append([index[tuple(2-p[axes[j]] if flips[j] else p[axes[j]]
                                        for j in range(3))] for p in points])
assert len({tuple(a) for a in symmetries}) == 48

@lru_cache(None)
def canonical(mask):
    ids = [i for i in range(27) if (mask>>i)&1]
    return min(sum(1<<sym[i] for i in ids) for sym in symmetries)

filename = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("certificate.b64")
raw = base64.b64decode(filename.read_text())
assert len(raw)%4 == 0
assert hashlib.sha256(raw).hexdigest() == "1ae0a113582046e73c2849afda9b6e7e4b500a8b13b7d1df31ad80e0ff0e80f4"
labels = {}
for (packed,) in struct.iter_unpack("<I",raw):
    mask,kind = packed>>1,packed&1 # 0 = next player loses; 1 = next player wins
    assert mask not in labels
    assert mask.bit_count()<=8 and (mask>>27)==0 and canonical(mask)==mask
    labels[mask]=kind
assert len(labels)==839

edges_verified = 0
level_counts = {}
for mask,kind in labels.items():
    ids=[i for i in range(27) if (mask>>i)&1]
    # Independently confirm claimed position itself is safe.
    for five in combinations(ids,5):
        base=lifts[five[0]]
        mat=[[lifts[i][j]-base[j] for j in range(4)] for i in five[1:]]
        assert det4(mat)!=0, ("unsafe certificate position",mask)
    children=set()
    moves=legal(mask)
    while moves:
        bit=moves&-moves
        moves ^= bit
        children.add(canonical(mask|bit))
    if kind==0:
        # For P: EVERY legal child is proved N (empty set permitted at terminal).
        assert all(labels.get(child)==1 for child in children),("invalid P",mask)
        edges_verified+=len(children)
    else:
        # For N: at least ONE legal child is proved P.
        assert any(labels.get(child)==0 for child in children),("invalid N",mask)
        edges_verified+=1
    level_counts[mask.bit_count()]=level_counts.get(mask.bit_count(),0)+1

reps={canonical((1<<a)|(1<<b)) for a,b in combinations(range(27),2)}
assert len(reps)==20
assert all(labels.get(rep)==0 for rep in reps)
assert edges_verified==1130
# After any first move, the second player can move to one of these P positions.
print("PASS: 3x3x3 five-point game has losing empty root")
print("forbidden_five_sets=",forbidden,
      "certificate_nodes=",len(labels),"edges=",edges_verified,
      "losing_two_stone_orbits=",len(reps),
      "levels=",dict(sorted(level_counts.items())))
