#!/usr/bin/env python3
"""Complete byte-for-byte crosscheck, orbit classification, and seven-point witnesses."""
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def mex(options):
    g=0
    while g in options:g+=1
    return g


def direct(n,edges):
    @lru_cache(None)
    def game(s):
        return mex({game(s|(1<<v)) for v in range(n) if not s>>v&1
                    and all((s|(1<<v))&edge!=edge for edge in edges)})
    return game(0),[game(1<<v) for v in range(n)],game.cache_info().currsize


def main():
    directory=Path(__file__).resolve().parent
    compiler=shutil.which('g++')
    if compiler is None:
        raise SystemExit('g++ is needed for the independent full census')
    with tempfile.TemporaryDirectory(prefix='kyouen-pure3-census-') as scratch:
        temp=Path(scratch).resolve()
        assert temp.parent==Path(tempfile.gettempdir()).resolve()
        py_values=temp/'python.bin';cpp_values=temp/'cpp.bin';executable=temp/'audit.exe'
        subprocess.run([sys.executable,str(directory/'scan.py'),'--values-out',str(py_values)],check=True)
        subprocess.run([compiler,'-std=c++17','-O2',str(directory/'independent.cpp'),'-o',str(executable)],check=True)
        report=json.loads(subprocess.check_output([str(executable),str(cpp_values)],text=True))
        python=py_values.read_bytes();native=cpp_values.read_bytes()
        assert len(python)==len(native)==1<<20
        assert python==native
        digest=hashlib.sha256(python).hexdigest()
        assert Counter(python)==Counter({g:count for g,count in enumerate(report['histogram']) if count})
        triples=list(combinations(range(6),3))
        permutation_maps=[]
        triple_index={triple:j for j,triple in enumerate(triples)}
        for permutation in permutations(range(6)):
            permutation_maps.append([1<<triple_index[tuple(sorted(permutation[v] for v in triple))] for triple in triples])
        pending={family for family,g in enumerate(python) if g==4}
        orbit_records=[]
        while pending:
            representative=min(pending)
            indices=[j for j in range(20) if representative>>j&1]
            orbit={sum(mapping[j] for j in indices) for mapping in permutation_maps}
            assert orbit<=pending and all(python[family]==4 for family in orbit)
            pending-=orbit
            edges=[sum(1<<v for v in triples[j]) for j in indices]
            value,children,states=direct(6,edges)
            assert value==4
            orbit_records.append(dict(family_mask=representative,triples=[triples[j] for j in indices],
                labeled_orbit_size=len(orbit),automorphism_order=720//len(orbit),
                child_grundy=children,safe_states=states))
        # A compact exact characterization of every maximum-four family:
        # up to relabeling, choose any subset of {012,013,014} above base 4040.
        interval_images=set()
        for extra in range(8):
            family=4040|extra
            assert python[family]==4
            selected=[j for j in range(20) if family>>j&1]
            interval_images.update(sum(mapping[j] for j in selected) for mapping in permutation_maps)
        assert interval_images=={family for family,g in enumerate(python) if g==4}
    census=json.loads((directory/'output/six_census.json').read_text(encoding='utf-8'))
    second=census['first_witnesses']['2']
    four=census['first_witnesses']['4']
    edges2=[sum(1<<v for v in triple) for triple in second['triples']]
    edges4=[sum(1<<v for v in triple) for triple in four['triples']]
    # Add one free vertex: xor 1, independently checked as a seven-point raw game.
    g3,child3,states3=direct(7,edges2)
    g5,child5,states5=direct(7,edges4)
    assert (g3,g5)==(3,5)
    # A no-isolated-vertex, linear pure-three-point witness for 3.
    linear_edges=[88,38,97,13]
    assert all((a&b).bit_count()<=1 for a,b in combinations(linear_edges,2))
    linear_g,linear_children,linear_states=direct(7,linear_edges)
    assert linear_g==3
    smaller=[]
    for n in range(6):
        triples=list(combinations(range(n),3))
        counts=Counter()
        for family in range(1<<len(triples)):
            edges=[sum(1<<v for v in triple) for j,triple in enumerate(triples) if family>>j&1]
            value,_,_=direct(n,edges)
            assert value<=1
            counts[value]+=1
        smaller.append(dict(n=n,families=1<<len(triples),histogram=dict(counts)))
    # Save concrete geometric realizations of maximum-four orbit representatives.
    import importlib.util
    root=directory.parents[2]
    spec=importlib.util.spec_from_file_location('rank_three_universal',root/
        'research/experiments/rank-three-residual-universality-20261107/verify.py')
    geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
    geometric=[]
    for row in orbit_records:
        edges=tuple(sum(1<<v for v in triple) for triple in row['triples'])
        record=geometry.audit(6,edges)
        assert record['grundy']==4
        geometric.append(record)
    output=dict(audit='PASS',families_compared=1<<20,all_values_sha256=digest,
        cpp_raw_safe_states=report['safe_states'],histogram=census['histogram'],
        maximum_four_isomorphism_types=len(orbit_records),maximum_four_orbits=orbit_records,
        maximum_four_interval=dict(mandatory_mask=4040,optional_mask=7,labeled_images=len(interval_images)),
        smaller_pure_triple_censuses=smaller,
        minimum_vertices_values_zero_through_five=[0,1,6,7,6,7],
        maximum_four_geometric_witnesses=geometric,
        seven_point_value_three=dict(edges=edges2,child_grundy=child3,safe_states=states3),
        seven_point_value_five=dict(edges=edges4,child_grundy=child5,safe_states=states5),
        seven_point_linear_three=dict(edges=linear_edges,child_grundy=linear_children,safe_states=linear_states))
    (directory/'output/independent_audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:output[key] for key in ('audit','families_compared','all_values_sha256',
        'cpp_raw_safe_states','histogram','maximum_four_isomorphism_types',
        'minimum_vertices_values_zero_through_five')},indent=2))


if __name__=='__main__':main()
