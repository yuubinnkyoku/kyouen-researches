#!/usr/bin/env python3
"""Independently replay the eight-point g6 / nine-point g7 witnesses."""
import importlib.util
import json
from pathlib import Path
from search import direct


def main():
    directory=Path(__file__).resolve().parent
    root=directory.parents[2]
    report=json.loads((directory/'output/random_n8.json').read_text())
    assert report['maximum_found']==6 and report['vertices']==8
    edges=tuple(report['witness_edges'])
    assert len(edges)==len(set(edges))==6
    assert all(edge.bit_count()==3 and edge<256 for edge in edges)
    records=[]
    for n,expected in ((8,6),(9,7)):
        value,children=direct(n,edges)
        assert value==expected
        records.append(dict(n=n,edges=edges,grundy=value,child_grundy=children))
    spec=importlib.util.spec_from_file_location('geometry',root/
        'research/experiments/rank-three-residual-universality-20261107/verify.py')
    geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
    geometries=[geometry.audit(row['n'],edges) for row in records]
    assert [row['grundy'] for row in geometries]==[6,7]
    ten=json.loads((directory/'output/random_n10.json').read_text())
    ten_value,ten_children=direct(ten['vertices'],tuple(ten['witness_edges']))
    assert ten_value==ten['maximum_found']==7
    assert sum(ten['histogram'])==ten['evaluated']==500000
    output=dict(audit='PASS',discovery=dict(seed=report['seed'],evaluated=report['evaluated']),
                witness_checks=records,integer_realizations=geometries,
                minimum_legal_points=dict(grundy_six=8,grundy_seven=9),
                lower_bound='K0690: g>=4 implies legal_points>=g+2',
                minimum_triple_edges=dict(grundy_six=6,grundy_seven=6),
                edge_lower_bound='K0687: at most five pure-triple edges imply g<=5',
                ten_point_probe=dict(evaluated=ten['evaluated'],maximum_found=ten_value,
                                     witness_edges=ten['witness_edges'],child_grundy=ten_children,
                                     limitation='no absence or upper-bound claim from this sample'))
    target=directory/'output/witness_audit.json'
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='integer_realizations'},indent=2))


if __name__=='__main__':main()
