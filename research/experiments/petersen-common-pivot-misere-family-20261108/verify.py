#!/usr/bin/env python3
"""Petersen joins: exact local proof and raw full-game verification at k=1,2."""
from functools import lru_cache
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('misere_geometry',ROOT/
    'research/experiments/common-pivot-misere-bound-20261108/verify_geometry.py')
GEOMETRY=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(GEOMETRY)


def nk_values(n,edges):
    adjacency=[1<<v for v in range(n)]
    for u,v in edges:adjacency[u]|=1<<v;adjacency[v]|=1<<u
    def mex(options):
        result=0
        while result in options:result+=1
        return result
    @lru_cache(None)
    def game(remaining):
        options=[game(remaining&~adjacency[v]) for v in range(n) if remaining>>v&1]
        return mex({g for g,h in options}),mex({h for g,h in options}) if options else 1
    full=(1<<n)-1
    return game(full),[game(full&~adjacency[v]) for v in range(n)]


def family(k):
    pairs=list(combinations(range(5),2))
    local=[(u,v) for u,v in combinations(range(10),2) if set(pairs[u]).isdisjoint(pairs[v])]
    edges=[(10*j+u,10*j+v) for j in range(k) for u,v in local]
    edges.extend((10*i+u,10*j+v) for i,j in combinations(range(k),2) for u in range(10) for v in range(10))
    return 10*k,edges


def main():
    directory=Path(__file__).resolve().parent;records=[];local_checks=[]
    for k in range(1,6):
        n,pairs=family(k)
        assert len(pairs)==50*k*k-35*k
        neighbors=[set() for _ in range(n)]
        for u,v in pairs:neighbors[u].add(v);neighbors[v].add(u)
        for v in range(n):
            remaining=set(range(n))-{v}-neighbors[v]
            assert len(remaining)==6
            assert all(len(neighbors[u]&remaining)==2 for u in remaining)
            reached={next(iter(remaining))}
            while True:
                enlarged=reached|set().union(*(neighbors[u]&remaining for u in reached))
                if enlarged==reached:break
                reached=enlarged
            assert reached==remaining
        root,children=nk_values(n,pairs)
        assert root==(1,1) and set(children)=={(0,0)}
        local_checks.append(dict(k=k,link_vertices=n,link_edges=len(pairs),link_value=root,
                                 all_closed_neighborhood_children_are_C6=len(children)))
        if k<=2:
            triples=tuple(1|(1<<(u+1))|(1<<(v+1)) for u,v in pairs)
            records.append((n+1,triples))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-petersen-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'verify.exe';result=temp/'values.bin';meta=temp/'meta.json'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(result),str(meta)],check=True)
        assert result.read_bytes()==bytes([0,0]*len(records))
        native=json.loads(meta.read_text())
    n,edges=records[0]
    geometric=GEOMETRY.GEOMETRY.audit(n,edges)
    h=GEOMETRY.misere_values(n,edges)
    occupied=sum(1<<v for v in geometric['occupied'])
    geometric_residual=[sum(1<<v for v in quad)&~occupied for quad in geometric['actual_quads']]
    assert GEOMETRY.misere_values(n,geometric_residual)==h
    assert geometric['grundy']==h[0]==0
    assert all(0 in quad for quad in geometric['actual_quads'])
    geometric.update(misere_aux=h[0],all_bad_quads_share_legal_pivot=True)
    output=dict(audit='PASS',local_checks=local_checks,cpp_full_games=len(records),
                cpp_safe_states=native['safe_states'],full_game_normal_misere=[[0,0]]*len(records),
                k1_integer_geometry=geometric,
                all_k_formulas=dict(legal_points='10*k+1',occupied_anchors='50*k*k-35*k',
                                    board_points='50*k*k-25*k+1',normal_grundy=0,misere_aux=0))
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='k1_integer_geometry'},indent=2),flush=True)


if __name__=='__main__':main()
