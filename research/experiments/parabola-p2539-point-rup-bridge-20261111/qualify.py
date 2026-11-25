"""Bind native parent-only unit derivations, earlier shape constraints and the pruned input."""
import argparse
import gzip
import json
from pathlib import Path
from verify import HERE,PARENT,PARENT_SHA,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    prior=HERE.parent/'parabola-p2539-five-pair-split-20261111';q=json.loads((prior/'qualification.json').read_bytes())
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert sha((prior/'README.md').read_bytes())==q['subset_argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    d=HERE/'combined-output';m=json.loads((d/'summary.json').read_bytes());rep=json.loads((HERE/'replay.json').read_bytes())
    assert m['all_verified'] and len(m['points'])==60 and rep['verified_parent_only_derivation'] and not rep['parent_unsat_claimed']
    assert sha((HERE/'replay.py').read_bytes())==rep['source_sha256'] and sha((HERE/'combine.py').read_bytes())==m['source_sha256']
    assert sha((HERE/'verify.py').read_bytes())==m['individual_driver_source_sha256']
    parent=gzip.decompress(PARENT.read_bytes());assert sha(parent)==PARENT_SHA==m['parent_input_sha256']==rep['parent_input_sha256']
    proof=gzip.decompress((d/'all-units.rup.gz').read_bytes());assert sha(proof)==m['combined_raw_sha256']==rep['proof_sha256']
    assert rep['derived_points']==m['points'] and m['derived_units']==[-(36512+u) for u in m['points']]
    for u in m['points']:
        source=HERE/'output'/str(u);r=json.loads((source/'result.json').read_bytes());launch=json.loads((source/'launch.json').read_bytes())
        assert launch['returncode']==0 and not launch['timed_out'] and r['status']=='SOLVER_UNSAT' and r['proof_complete']
        expected=('p cnf 51570 144547\n'+'\n'.join(parent.decode('ascii').splitlines()[1:])+f'\n{36512+u} 0\n').encode('ascii')
        assert sha(expected)==r['child_input_sha256'] and sha((HERE/'produce.py').read_bytes())==r['source_sha256']
        individual=HERE/'audit-output'/str(u)
        one=json.loads((individual/'receipt.json').read_bytes());assert one['verified_parent_only_derivation'] and one['derived_unit']==-(36512+u)
        assert sha(gzip.decompress((individual/'lifted.rup.gz').read_bytes()))==one['lifted_raw_sha256']
    pruned=HERE.parent/'parabola-p2539-five-pruned-20261111/output/input.cnf.gz';praw=gzip.decompress(pruned.read_bytes())
    expected=('p cnf 51570 144606\n'+'\n'.join(parent.decode('ascii').splitlines()[1:])+'\n'+''.join(f'{v} 0\n' for v in m['derived_units'])).encode('ascii');assert praw==expected
    save(a.output,dict(seed_sha256=q['seed_sha256'],parent_input_sha256=PARENT_SHA,derived_points=m['points'],pruned_input_sha256=sha(praw),parent_and_pruned_equivalent=True,
        combined_proof_sha256=sha(proof),combined_lines=m['combined_lines'],prior_shape_qualification_sha256=sha((prior/'qualification.json').read_bytes()),
        replay_sha256=sha((HERE/'replay.json').read_bytes()),argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='All60 excluded point units are now RUP consequences of the retained parent CNF alone. Adding exactly these units preserves every parent model; neither CNF is claimed UNSAT.'))
    print('PASS60 parent-only RUP units and exact equivalence of retained/pruned CNFs; no UNSAT claim')


if __name__=='__main__':main()
