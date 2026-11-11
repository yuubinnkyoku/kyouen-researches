"""Bind eight verified negative gate cases to earlier necessary geometric conditions."""
import argparse
import gzip
import json
from pathlib import Path
from audit import HERE,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    prior=HERE.parent/'parabola-p2539-pair-obstructions-20261111';q=json.loads((prior/'qualification.json').read_bytes())
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert len(q['excluded_points'])==116 and len(q['must_add_one_of'])==26
    assert sha((prior/'README.md').read_bytes())==q['argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    inp=json.loads((HERE/'input-audit/summary.json').read_bytes());m=json.loads((HERE/'proof-audit/summary.json').read_bytes());rep=json.loads((HERE/'replay-output/receipt.json').read_bytes())
    assert inp['status_counts']=={'UNKNOWN':18,'SOLVER_UNSAT':8} and not inp['verified_safe_count']
    assert len(m['proved_points'])==8 and len(m['remaining_gate'])==18 and len(m['all_excluded_points'])==124
    assert set(m['proved_points'])|set(m['remaining_gate'])==set(q['must_add_one_of']) and not set(m['proved_points'])&set(m['remaining_gate'])
    assert set(m['all_excluded_points'])==set(q['excluded_points'])|set(m['proved_points'])
    base=gzip.decompress((HERE/'output/base.cnf.gz').read_bytes());assert sha(base)==m['base_input_sha256']==rep['base_input_sha256']==inp['base_input_sha256']
    assert rep['verified_base_only_derivation'] and not rep['parent_unsat_claimed'] and rep['remaining_gate']==m['remaining_gate']
    assert sha((HERE/'verify_cases.py').read_bytes())==m['source_sha256'] and sha((HERE/'replay.py').read_bytes())==rep['source_sha256']
    assert sha(gzip.decompress((HERE/'replay-output/coverage.rup.gz').read_bytes()))==rep['proof_sha256']
    save(a.output,dict(seed_sha256=q['seed_sha256'],max_removed=5,improvement_size_at_least=1259,necessary_origin=1,necessary_complete_pair=[6,2533],excluded_points=m['all_excluded_points'],
        newly_closed_gate_points=m['proved_points'],must_add_one_of=m['remaining_gate'],prior_qualification_sha256=sha((prior/'qualification.json').read_bytes()),
        independent_input_audit_sha256=sha((HERE/'input-audit/summary.json').read_bytes()),negative_case_summary_sha256=sha((HERE/'proof-audit/summary.json').read_bytes()),
        coverage_replay_sha256=sha((HERE/'replay-output/receipt.json').read_bytes()),argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Safe improvements of the fixed1258 seed with at most5 losses avoid124 points and add one of18 remaining empty-pair points. Eight extra exclusions use native RUP after116 geometric exclusions; original parent and full radius5 remain unresolved.'))
    print('PASS124 exclusions and remaining18-point gate;18 UNKNOWN cases not promoted')


if __name__=='__main__':main()
