"""Bind the prior positive gate, new pair audits, and the finite covering argument."""
import argparse
import gzip
import json
from pathlib import Path
from verify import HERE,save,sha


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    previous=HERE.parent/'parabola-p2539-empty-gate-probes-20261111';qr=(previous/'qualification.json').read_bytes();q=json.loads(qr)
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert sha((previous/'README.md').read_bytes())==q['argument_sha256'] and sha((previous/'qualify.py').read_bytes())==q['source_sha256']
    raw=gzip.decompress((HERE/'output/certificate.json.gz').read_bytes());c=json.loads(raw);m=json.loads((HERE/'output/manifest.json').read_bytes());audit=json.loads((HERE/'audit-output/summary.json').read_bytes());reg=json.loads((HERE/'regression.json').read_bytes())
    assert sha(raw)==m['certificate_sha256']==audit['certificate_sha256'] and sha((HERE/'output/certificate.json.gz').read_bytes())==m['compressed_sha256']
    assert c['prior_qualification_sha256']==audit['prior_qualification_sha256']==sha(qr)
    assert c['source_sha256']==sha((HERE/'produce.py').read_bytes()) and audit['source_sha256']==reg['verifier_source_sha256']==sha((HERE/'verify.py').read_bytes()) and reg['source_sha256']==sha((HERE/'regression.py').read_bytes())
    assert c['newly_excluded']==m['newly_excluded']==audit['newly_excluded'] and len(c['newly_excluded'])==97
    assert audit['remaining_gate']==q['must_add_one_of'] and len(audit['remaining_gate'])==18
    assert audit['all_excluded']==sorted(set(q['excluded_points'])|set(c['newly_excluded'])) and len(audit['all_excluded'])==221
    assert audit['covered_pairs']==20502 and audit['negative_pairs']==5010 and audit['hitting_witness_pairs']==15492
    assert len(reg['corruptions_rejected'])==8
    save(a.output,dict(seed_sha256=q['seed_sha256'],max_removed=5,improvement_size_at_least=1259,necessary_origin=1,necessary_complete_pair=[6,2533],
        excluded_points=audit['all_excluded'],newly_excluded=c['newly_excluded'],must_add_one_of=audit['remaining_gate'],prior_qualification_sha256=sha(qr),
        independent_audit_sha256=sha((HERE/'audit-output/summary.json').read_bytes()),regression_sha256=sha((HERE/'regression.json').read_bytes()),argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Safe improvements of the fixed1258 seed with at most5 losses avoid221 points and add at least one of18 gate points. New97 exclusions use geometric hitting proofs covering all18 positive gate cases, not new native RUP or global UNSAT.'))
    print('PASS221 exclusions, unchanged18-point necessary gate; no global UNSAT')


if __name__=='__main__':main()
