"""Bind the geometric point exclusions and prior fixed-point necessity to the same seed."""
import argparse
import json
from pathlib import Path
from verify import HERE,sha,save,SEED_SHA


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    prior=HERE.parent/'parabola-p2539-five-pair-split-20261111';q=json.loads((prior/'qualification.json').read_bytes())
    assert q['seed_sha256']==SEED_SHA and q['max_removed']==5 and q['improvement_size_at_least']==1259
    assert q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert sha((prior/'README.md').read_bytes())==q['subset_argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    r=json.loads((HERE/'audit-output/summary.json').read_bytes());cert=HERE/'output/certificate.json'
    assert r['seed_sha256']==SEED_SHA and r['fixed']==[0,6,2533] and r['max_deletions']==5
    assert r['all_outside_points']==1281 and r['excluded_count']==len(r['excluded'])==60 and r['hitting_witness_count']==1221
    assert sha(cert.read_bytes())==r['certificate_sha256'] and sha((HERE/'verify.py').read_bytes())==r['verifier_source_sha256']
    regression=json.loads((HERE/'regression.json').read_bytes())
    assert regression['verifier_source_sha256']==r['verifier_source_sha256'] and regression['bruteforce_cases']==2224
    assert sha((HERE/'regression.py').read_bytes())==regression['source_sha256']
    save(a.output,dict(seed_sha256=SEED_SHA,max_removed=5,improvement_size_at_least=1259,necessary_origin=1,necessary_complete_pair=[6,2533],excluded_points=r['excluded'],
        prior_shape_qualification_sha256=sha((prior/'qualification.json').read_bytes()),obstruction_certificate_sha256=sha(cert.read_bytes()),
        independent_audit_sha256=sha((HERE/'audit-output/summary.json').read_bytes()),regression_sha256=sha((HERE/'regression.json').read_bytes()),
        argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Any safe improvement of this fixed seed losing at most5 points retains origin/original pair and avoids the listed60 points. Other points are not certified feasible.'))
    print('PASS 60 forbidden additions bound to prior five-deletion improvement conditions')


if __name__=='__main__':main()
