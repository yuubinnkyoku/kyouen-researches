"""Bind prior necessary shape and changed-pair exclusion to preservation of the original pair."""
import argparse
import gzip
import json
from pathlib import Path
from check_inputs import HERE, SEED_SHA, sha, save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    old=HERE.parent/'parabola-p2539-exact-five-20261111';prior=json.loads((old/'qualification.json').read_bytes())
    assert prior['seed_sha256']==SEED_SHA and prior['max_removed']==5 and prior['improvement_size_at_least']==1259
    assert (prior['necessary_removed_exactly'],prior['necessary_origin'],prior['necessary_complete_pairs'])==(5,1,1)
    assert sha((old/'README.md').read_bytes())==prior['subset_argument_sha256']
    assert sha((old/'qualify.py').read_bytes())==prior['source_sha256'] and sha((old/'replay.json').read_bytes())==prior['replay_sha256']
    rep=json.loads((HERE/'replay.json').read_bytes());assert rep['changed_verified'] and rep['seed_sha256']==SEED_SHA and len(rep['cases'])==1
    assert sha((HERE/'replay.py').read_bytes())==rep['replay_source_sha256'];r=rep['cases'][0];assert r['case']=='changed'
    d=HERE/'audit-output/changed';m=json.loads((d/'manifest.json').read_bytes());s=json.loads((d/'schema.json').read_bytes())
    assert m['schema_geometry_rup_lrat_verified'] and m['seed_sha256']==SEED_SHA
    assert (m['origin'],m['complete_pairs'],m['target_size'],m['removed_exactly'],m['excluded_complete_pair'],m['split_unit'])==(1,1,1259,5,6,-21)
    assert s['split_unit']==-21 and r['schema_verified'] and r['geometry']['returncode']==0
    assert r['rup']['returncode']==0 and 's VERIFIED' in r['rup']['stdout'].splitlines()
    assert sha(gzip.decompress((d/'input.cnf.gz').read_bytes()))==m['input_sha256']==r['input_sha256']
    packed=(d/'verified-proof.drat.gz').read_bytes();assert sha(packed)==m['drat_gzip_sha256'] and sha(gzip.decompress(packed))==m['drat_raw_sha256']==r['drat_raw_sha256']
    inputs=json.loads((HERE/'input-audit/summary.json').read_bytes());assert inputs['exhaustive_partition'] and inputs['seed_sha256']==SEED_SHA
    u=json.loads((HERE/'output/retained/result.json').read_bytes());assert u['status']=='UNKNOWN' and (u['split_unit'],u['removed_exactly'],u['target'])==(21,5,1259)
    save(a.output,dict(seed_sha256=SEED_SHA,max_removed=5,improvement_size_at_least=1259,necessary_removed_exactly=5,necessary_origin=1,necessary_complete_pair=[6,2533],
        prior_shape_qualification_sha256=sha((old/'qualification.json').read_bytes()),changed_pair_manifest_sha256=sha((d/'manifest.json').read_bytes()),
        input_partition_audit_sha256=sha((HERE/'input-audit/summary.json').read_bytes()),replay_sha256=sha((HERE/'replay.json').read_bytes()),
        subset_argument_sha256=sha((HERE/'README.md').read_bytes()),unresolved_status='UNKNOWN',unresolved_result_sha256=sha((HERE/'output/retained/result.json').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Any safe improvement of this fixed1258 seed losing at most5 points must retain origin and its original complete pair, losing exactly5. Existence of such an improvement remains UNKNOWN.'))
    print('PASS five-deletion improvements must retain origin and original pair; feasibility UNKNOWN')


if __name__=='__main__':main()
