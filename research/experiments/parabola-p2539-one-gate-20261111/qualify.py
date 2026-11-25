"""Combine the restricted refutation, subset argument, and saved conditional pair proofs."""
import argparse
from collections import Counter
import gzip
import importlib.util
import json
from pathlib import Path
from verify import HERE,save,sha


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    prior=HERE.parent/'parabola-p2539-gate-cover-20261111';qr=(prior/'qualification.json').read_bytes();q=json.loads(qr)
    assert sha((prior/'README.md').read_bytes())==q['argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_complete_pair']==[6,2533] and q['necessary_origin']==1
    audit=json.loads((HERE/'audit-final/summary.json').read_bytes());replay=json.loads((HERE/'replay.json').read_bytes());reg=json.loads((HERE/'regression.json').read_bytes())
    raw=gzip.decompress((HERE/'output/input.cnf.gz').read_bytes());proof=gzip.decompress((HERE/'output/proof.drat.gz').read_bytes())
    assert audit['verified_refutation'] and replay['verified_refutation'] and audit['restricted_gate_cardinality']==1
    assert audit['input_sha256']==replay['input_sha256']==sha(raw) and audit['proof_sha256']==replay['proof_sha256']==sha(proof) and audit['prior_qualification_sha256']==sha(qr)
    assert sha((HERE/'verify.py').read_bytes())==audit['source_sha256']==reg['verifier_source_sha256'] and sha((HERE/'replay.py').read_bytes())==replay['source_sha256'] and sha((HERE/'regression.py').read_bytes())==reg['source_sha256']
    assert reg['exact_one_truth_assignments']==262144 and reg['accepted_exact_one_assignments']==18 and len(reg['corruptions_rejected'])==6
    cross_raw=gzip.decompress((prior/'output/certificate.json.gz').read_bytes());cross=json.loads(cross_raw);cross_audit=json.loads((prior/'audit-output/summary.json').read_bytes())
    assert sha(cross_raw)==cross_audit['certificate_sha256'] and sha((prior/'audit-output/summary.json').read_bytes())==q['independent_audit_sha256'] and sha((prior/'verify.py').read_bytes())==cross_audit['source_sha256']
    spec=importlib.util.spec_from_file_location('one_gate_saved_cover',prior/'verify.py');cover=importlib.util.module_from_spec(spec);spec.loader.exec_module(cover)
    seed,fs,two,_=cover.inputs(cross);gate=q['must_add_one_of'];assert cross['gate']==gate and len(gate)==18
    newly=[];details=[];counts=Counter();negative_cases=0
    for entry in cross['entries']:
        u=entry['point'];assert [case['gate_point'] for case in entry['cases']]==gate
        if u in q['excluded_points']:continue
        allowed=[case['gate_point'] for case in entry['cases'] if case['status']=='HITTING_WITNESS']
        assert all(case['status'] in ['HITTING_WITNESS','EXCLUDED'] for case in entry['cases'])
        if len(allowed)>1:continue
        for case in entry['cases']:
            if case['status']!='EXCLUDED':continue
            v=case['gate_point'];quads=cover.case_quads(u,v,fs,two);assert len(quads)==case['obstructions']
            counts.update(cover.checker.check_tree([set(quad)-{0,6,2533,u,v} for quad in quads],5,case['refutation']));negative_cases+=1
        newly.append(u);details.append(dict(point=u,remaining_gate_points=allowed))
    assert len(newly)==27 and negative_cases==459 and all(len(d['remaining_gate_points'])==1 for d in details)
    excluded=sorted(set(q['excluded_points'])|set(newly));assert len(excluded)==248 and set(excluded).isdisjoint(gate)
    save(a.output,dict(seed_sha256=q['seed_sha256'],max_removed=5,improvement_size_at_least=1259,necessary_origin=1,necessary_complete_pair=[6,2533],excluded_points=excluded,
        newly_excluded=newly,necessary_gate_points=gate,minimum_gate_additions=2,conditional_cover_details=details,replayed_negative_pair_cases=negative_cases,refutation_nodes=dict(counts),
        prior_qualification_sha256=sha(qr),restricted_audit_sha256=sha((HERE/'audit-final/summary.json').read_bytes()),replay_sha256=sha((HERE/'replay.json').read_bytes()),
        conditional_pair_certificate_sha256=sha(cross_raw),argument_sha256=sha((HERE/'README.md').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Safe improvements of the fixed1258 seed with at most5 losses avoid248 points and add at least two of18 residual empty-pair points. New27 exclusions combine at-least-two necessity with459 rechecked saved negative pair proofs; unrestricted improvement remains unresolved.'))
    print('PASS minimum2 gate additions;27 further exclusions;248 total;459 saved negative cases rechecked')


if __name__=='__main__':main()
