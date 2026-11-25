#!/usr/bin/env python3
"""Independently audit the n=13 tetracyclic core and four-cycle enumeration."""
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) == 2 else 13
if N not in (13,14):
    raise ValueError('dimension must be 13 or 14')
INPUT = HERE/f'tetracyclic-n{N}-candidates.txt.gz'
EDGES = list(combinations(range(N),2))
EDGE_INDEX = {e:i for i,e in enumerate(EDGES)}
CYCLES = []
for a,b,c,d in combinations(range(N),4):
    for q in ((a,b,c,d),(a,b,d,c),(a,c,b,d)):
        CYCLES.append(sum(1 << EDGE_INDEX[tuple(sorted((q[i],q[(i+1)%4])))] for i in range(4)))
assert len(CYCLES) == len(set(CYCLES)) == 3*len(list(combinations(range(N),4)))


def canonical(b, pairs):
    matrix = [[0]*b for _ in range(b)]
    for u,v in pairs:
        matrix[u][v] += 1
        if u != v:
            matrix[v][u] += 1
    return min(bytes(matrix[p[i]][p[j]] for i in range(b) for j in range(i,b))
               for p in permutations(range(b)))


def all_core_types(b):
    """Enumerate labelled core edge multisets independently, modulo relabelling."""
    types = list(combinations_with_replacement(range(b),2))
    result = set()
    admissible = set()
    labelled = 0
    for choice in combinations_with_replacement(range(len(types)),b+3):
        degrees = [0]*b
        pairs = []
        for i in choice:
            u,v = types[i]
            degrees[u] += 1
            degrees[v] += 1
            pairs.append((u,v))
        if min(degrees) < 3:
            continue
        seen, stack = {0}, [0]
        adjacency = [set() for _ in range(b)]
        for u,v in pairs:
            adjacency[u].add(v)
            adjacency[v].add(u)
        while stack:
            for v in adjacency[stack.pop()] - seen:
                seen.add(v)
                stack.append(v)
        if len(seen) != b:
            continue
        labelled += 1
        # Some relabelling always sorts degrees; only those are needed to see
        # every unlabelled core. Canonicalization itself uses all permutations.
        if degrees != sorted(degrees):
            continue
        key = canonical(b,pairs)
        result.add(key)
        loops = sum(u == v for u,v in pairs)
        distinct = len({(u,v) for u,v in pairs if u != v})
        minimum = 2*len(pairs)+loops-distinct
        if minimum <= N+3:
            admissible.add(key)
    return labelled, result, admissible


def expected_lengths(pairs):
    """Enumerate compositions directly; equivalent paths are ordered by length."""
    result = set()
    def visit(prefix, remaining):
        i = len(prefix)
        if i == len(pairs):
            if remaining == 0:
                result.add(tuple(prefix))
            return
        u,v = pairs[i]
        minimum = 3 if u == v else 1
        if i and pairs[i] == pairs[i-1]:
            minimum = max(minimum,prefix[-1])
            if u != v and minimum == 1:
                minimum = 2
        for length in range(minimum,remaining+1):
            visit(prefix+[length],remaining-length)
    visit([],N+3)
    return result


def expand(b,pairs,lengths):
    edge_set = set()
    nxt = b
    for (u,v),length in zip(pairs,lengths):
        previous = u
        for _ in range(length-1):
            edge_set.add(tuple(sorted((previous,nxt))))
            previous,nxt = nxt,nxt+1
        edge_set.add(tuple(sorted((previous,v))))
    assert nxt == N and len(edge_set) == N+3
    return sum(1 << EDGE_INDEX[e] for e in edge_set)


def mask_verdict(state):
    blocked = 0
    for circle in CYCLES:
        overlap = circle & state
        if overlap == circle:
            return False,False
        if overlap.bit_count() == 3:
            blocked |= circle & ~state
    missing = ((1 << len(EDGES))-1) & ~state
    return True, (missing & ~blocked) == 0


def main():
    raw = gzip.decompress(INPUT.read_bytes())
    groups = defaultdict(set)
    checked = Counter()
    free = Counter()
    saturated = Counter()
    for line in raw.decode('ascii').splitlines():
        fields = line.split()
        b = int(fields[0])
        triples = [tuple(map(int,x.split(','))) for x in fields[1:]]
        assert 1 <= b <= 6 and len(triples) == b+3
        pairs = tuple((u,v) for u,v,_ in triples)
        lengths = tuple(length for _,_,length in triples)
        assert pairs == tuple(sorted(pairs)) and sum(lengths) == N+3
        assert lengths not in groups[b,pairs]
        groups[b,pairs].add(lengths)
        ok, sat = mask_verdict(expand(b,pairs,lengths))
        checked[b] += 1
        free[b] += ok
        saturated[b] += sat
    records = []
    for b in range(1,7):
        labelled, expected_cores, admissible = all_core_types(b)
        actual_groups = [(pairs,ls) for (bb,pairs),ls in groups.items() if bb == b]
        actual_cores = {canonical(b,pairs) for pairs,_ in actual_groups}
        # Only cores which admit an (n+3)-edge simple expansion can appear.
        assert len(actual_cores) == len(actual_groups)
        assert actual_cores == admissible and admissible <= expected_cores
        for pairs,lengths in actual_groups:
            assert lengths == expected_lengths(pairs)
        records.append({'branch_vertices':b,'labelled_cores':labelled,'core_types':len(expected_cores),
                        'admissible_core_types':len(actual_cores),
                        'assignments':checked[b],'c4_free':free[b],'saturated':saturated[b]})
    expected = {13:(55822,19567),14:(109249,44296)}
    assert (sum(checked.values()),sum(free.values())) == expected[N]
    assert sum(saturated.values()) == 0
    print(json.dumps({'candidate_sha256':hashlib.sha256(raw).hexdigest(),
                      'records':records,'total_assignments':sum(checked.values()),
                      'total_c4_free':sum(free.values()),'total_saturated':sum(saturated.values())},indent=2))


if __name__ == '__main__':
    main()
