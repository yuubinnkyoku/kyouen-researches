"""Bind radius-four exclusion and exact-five class certificates to a necessary shape."""
import argparse
import gzip
import json
from pathlib import Path
from schema import CASES, SEED_SHA
from verify import HERE, sha, save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();assert not args.output.exists()
    old=HERE.parent/'parabola-p2539-without-origin-20261111';prior=json.loads((old/'qualification.json').read_text())
    assert prior['seed_sha256']==SEED_SHA and prior['unrestricted_four_deletion_local_optimum']
    assert prior['excluded_size_at_least']==1259 and prior['max_removed']==4
    assert sha((old/'README.md').read_bytes())==prior['subset_argument_sha256']
    assert sha((old/'qualify.py').read_bytes())==prior['source_sha256']
    assert sha((old/'replay.json').read_bytes())==prior['replay_sha256']
    rep=json.loads((HERE/'replay.json').read_text());assert rep['all_three_verified'] and rep['seed_sha256']==SEED_SHA
    assert sha((HERE/'replay.py').read_bytes())==rep['replay_source_sha256']
    assert len(rep['cases'])==3 and {r['case'] for r in rep['cases']}==set(CASES)
    rows=[]
    for r in rep['cases']:
        case=r['case'];x,c=CASES[case];d=HERE/'audit-output'/case;m=json.loads((d/'manifest.json').read_text())
        assert m['seed_sha256']==SEED_SHA and m['schema_geometry_rup_lrat_verified']
        assert (m['origin'],m['complete_pairs'],m['target_size'],m['removed_exactly'])==(x,c,1259,5)
        assert r['schema_verified'] and r['geometry']['returncode']==0
        assert r['rup']['returncode']==0 and 's VERIFIED' in r['rup']['stdout'].splitlines()
        assert sha(gzip.decompress((d/'input.cnf.gz').read_bytes()))==m['input_sha256']==r['input_sha256']
        packed=(d/'verified-proof.drat.gz').read_bytes();assert sha(packed)==m['drat_gzip_sha256']
        assert sha(gzip.decompress(packed))==m['drat_raw_sha256']==r['drat_raw_sha256']
        rows.append(dict(case=case,manifest_sha256=sha((d/'manifest.json').read_bytes()),input_sha256=r['input_sha256'],proof_sha256=r['drat_raw_sha256']))
    unresolved=HERE/'output/x1-B1-target1259-remove5/result.json';u=json.loads(unresolved.read_text())
    assert u['status']=='UNKNOWN' and u['removed_exactly']==5 and u['origin']==1 and u['complete_pairs']==1
    assert u['seed_sha256']==SEED_SHA and u['conflict_budget']==100000
    save(args.output,dict(seed_sha256=SEED_SHA,improvement_size_at_least=1259,max_removed=5,necessary_removed_exactly=5,necessary_origin=1,necessary_complete_pairs=1,
        radius_four_qualification_sha256=sha((old/'qualification.json').read_bytes()),excluded_exact_five_cases=rows,unresolved_status='UNKNOWN',unresolved_result_sha256=sha(unresolved.read_bytes()),
        replay_sha256=sha((HERE/'replay.json').read_bytes()),subset_argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Necessary shape of a safe improvement losing at most5 points from this fixed1258 seed. The surviving shape is UNKNOWN, not known feasible or infeasible.'))
    print('PASS exact-five necessary-shape binding; surviving x1-B1 remains UNKNOWN')


if __name__=='__main__':main()
