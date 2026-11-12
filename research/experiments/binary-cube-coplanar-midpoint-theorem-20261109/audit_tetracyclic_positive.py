#!/usr/bin/env python3
"""Positive control: compare n=8 tetracyclic cores with all edge masks."""
from itertools import combinations, permutations
from math import factorial
from pathlib import Path
import json
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
N = 8


def expand(line):
    fields = line.split()
    b = int(fields[0])
    edges, nxt = set(), b
    for field in fields[1:]:
        u,v,length = map(int,field.split(','))
        for _ in range(length-1):
            edges.add(tuple(sorted((u,nxt))))
            u,nxt = nxt,nxt+1
        edges.add(tuple(sorted((u,v))))
    assert nxt == N and len(edges) == 11
    return edges


def c4_free(edges):
    for a,b,c,d in combinations(range(N),4):
        for q in ((a,b,c,d),(a,b,d,c),(a,c,b,d)):
            if all(tuple(sorted((q[i],q[(i+1)%4]))) in edges for i in range(4)):
                return False
    return True


def equivalent(a,b):
    da = [sum(v in e for e in a) for v in range(N)]
    db = [sum(v in e for e in b) for v in range(N)]
    if sorted(da) != sorted(db):
        return False
    for p in permutations(range(N)):
        if any(da[v] != db[p[v]] for v in range(N)):
            continue
        if {tuple(sorted((p[u],p[v]))) for u,v in a} == b:
            return True
    return False


def automorphisms(edges):
    degree = [sum(v in e for e in edges) for v in range(N)]
    return sum({tuple(sorted((p[u],p[v]))) for u,v in edges} == edges
               for p in permutations(range(N))
               if all(degree[v] == degree[p[v]] for v in range(N)))


def main():
    with tempfile.TemporaryDirectory(prefix='tetracyclic-positive-') as tmp:
        directory = Path(tmp)
        core_binary, mask_binary, candidates = directory/'core', directory/'mask', directory/'candidates'
        for source,binary in (('enumerate_tetracyclic_cores.cpp',core_binary),
                              ('enumerate_sparse_masks_n10.cpp',mask_binary)):
            subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-Werror',
                            str(HERE/source),'-o',str(binary)],check=True)
        subprocess.run([str(core_binary),'8',str(candidates)],check=True,capture_output=True,text=True)
        output = subprocess.run([str(mask_binary),'8','11'],check=True,capture_output=True,text=True).stdout
        mask_counts = dict(field.split('=',1) for field in output.split())
        assert int(mask_counts['checked']) == 8436285
        assert int(mask_counts['c4_free']) == int(mask_counts['saturated']) == 35640
        safe = [edges for line in candidates.read_text().splitlines()
                if c4_free(edges := expand(line))]
    assert len(safe) == 7
    classes = []
    for graph in safe:
        if not any(equivalent(graph,representative) for representative in classes):
            classes.append(graph)
    counts = [factorial(N)//automorphisms(graph) for graph in classes]
    assert len(classes) == 5 and sum(counts) == 90720
    assert sum(counts)*11 == int(mask_counts['c4_free'])*28
    print(json.dumps({'vertices':8,'edges':11,'fixed_edge_candidates':8436285,
                      'fixed_edge_c4_free':35640,'core_candidates_c4_free':len(safe),
                      'isomorphism_classes':len(classes),'labelled_c4_free':sum(counts),
                      'orbit_sizes':sorted(counts)},indent=2))


if __name__ == '__main__':
    main()
