"""Bind strengthened point obstructions and the empty-pair gate to the same local improvement scope."""
import argparse
import gzip
import json
from pathlib import Path
from verify import HERE,OLD,checker,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    prior=HERE.parent/'parabola-p2539-five-pair-split-20261111';q=json.loads((prior/'qualification.json').read_bytes())
    assert q['seed_sha256']==checker.SEED_SHA and q['max_removed']==5 and q['improvement_size_at_least']==1259
    assert q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert sha((prior/'README.md').read_bytes())==q['subset_argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    cert_raw=(HERE/'output/certificate.json').read_bytes();cert=json.loads(cert_raw);r=json.loads((HERE/'audit-output/summary.json').read_bytes())
    assert sha(cert_raw)==r['certificate_sha256'] and cert['excluded']==r['excluded'] and cert['newly_excluded']==r['newly_excluded']
    assert len(r['excluded'])==116 and len(r['newly_excluded'])==56 and r['hitting_witness_count']==1165
    assert sha((HERE/'produce.py').read_bytes())==cert['source_sha256'] and sha((OLD/'produce.py').read_bytes())==cert['hitting_search_source_sha256']
    assert sha((HERE/'verify.py').read_bytes())==r['source_sha256'] and sha((OLD/'verify.py').read_bytes())==r['hitting_verifier_source_sha256']
    g=json.loads((HERE/'gate-output/receipt.json').read_bytes());assert g['verified_parent_only_derivation'] and not g['parent_unsat_claimed']
    assert sha((HERE/'empty_gate.py').read_bytes())==g['source_sha256'] and sha(gzip.decompress((HERE/'gate-output/empty-pair-clause.rup.gz').read_bytes()))==g['proof_sha256']
    assert g['derived_positive_clause']==[36512+u for u in g['empty_pair_points']] and len(g['empty_pair_points'])==26
    assert not set(g['empty_pair_points'])&set(r['excluded'])
    save(a.output,dict(seed_sha256=checker.SEED_SHA,max_removed=5,improvement_size_at_least=1259,necessary_origin=1,necessary_complete_pair=[6,2533],excluded_points=r['excluded'],
        newly_excluded=r['newly_excluded'],must_add_one_of=g['empty_pair_points'],prior_shape_qualification_sha256=sha((prior/'qualification.json').read_bytes()),
        certificate_sha256=sha(cert_raw),independent_audit_sha256=sha((HERE/'audit-output/summary.json').read_bytes()),gate_receipt_sha256=sha((HERE/'gate-output/receipt.json').read_bytes()),
        argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Any safe improvement losing at most5 seed points must retain origin/original pair, avoid116 listed points and add at least one of26 originally empty-pair points. No full exclusion or new global bound.'))
    print('PASS116 exclusions and positive26-point gate bound to the same seed/scope')


if __name__=='__main__':main()
