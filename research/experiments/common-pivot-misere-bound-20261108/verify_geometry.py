#!/usr/bin/env python3
"""Integer q4 realizations of the pure-triple h4/h5 witnesses."""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('rank_three_geometry',ROOT/
    'research/experiments/rank-three-residual-universality-20261107/verify.py')
GEOMETRY=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(GEOMETRY)


def misere_values(n,edges):
    values={}
    for s in range((1<<n)-1,-1,-1):
        if any(s&e==e for e in edges):continue
        options={values[s|1<<v] for v in range(n) if not s>>v&1 and s|1<<v in values}
        result=0
        while result in options:result+=1
        values[s]=result if options else 1
    return values


def main():
    directory=Path(__file__).resolve().parent
    prior=json.loads((directory/'output/audit.json').read_text())
    records=[]
    for row in prior['special_witnesses']:
        if not row['name'].startswith('pure'):continue
        geometric=GEOMETRY.audit(row['n'],tuple(row['edges']))
        stones=sum(1<<v for v in geometric['occupied'])
        quad_masks=[sum(1<<v for v in quad) for quad in geometric['actual_quads']]
        assert all(quad&1 for quad in quad_masks)
        # Read all forbidden occupancies from determinant-checked geometric quads.
        residual=[quad&~stones for quad in quad_masks]
        actual=misere_values(row['n'],residual)
        assert actual==misere_values(row['n'],row['edges'])
        assert actual[0]==row['misere_aux']
        geometric.update(misere_aux=actual[0],all_bad_quads_share_legal_pivot=True,
                         misere_safe_states=len(actual))
        records.append(geometric)
    output=dict(audit='PASS',cases=len(records),integer_quadruples_checked=sum(r['quadruples'] for r in records),
                all_safe_misere_states=sum(r['misere_safe_states'] for r in records),records=records)
    (directory/'output/geometry.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()
