"""Adopt the sixty completed individual derivations independently of combined-proof status."""
import argparse
import gzip
import json
from pathlib import Path
from verify import HERE,PARENT,PARENT_SHA,sha,save,derivation


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    parent=gzip.decompress(PARENT.read_bytes());assert sha(parent)==PARENT_SHA
    points=json.loads((HERE.parent/'parabola-p2539-five-obstructions-20261111/output/certificate.json').read_bytes())['excluded'];assert len(points)==60
    controls=json.loads((HERE/'audit-output/controls.json').read_bytes());assert len(controls['cases'])==5
    for c in controls['cases']:assert derivation(c)==c['expected_derivation']
    rows=[]
    for u in points:
        d=HERE/'audit-output'/str(u);receipt=(d/'receipt.json').read_bytes();r=json.loads(receipt);packed=(d/'lifted.rup.gz').read_bytes();raw=gzip.decompress(packed)
        assert r['point']==u and r['derived_unit']==-(36512+u) and r['parent_input_sha256']==PARENT_SHA
        assert r['verified_parent_only_derivation'] and derivation(r) and sha(raw)==r['lifted_raw_sha256']
        assert sha((HERE/'verify.py').read_bytes())==r['driver_source_sha256']
        assert raw.decode('ascii').splitlines()[-1]==f'{-(36512+u)} 0'
        rows.append(dict(point=u,derived_unit=r['derived_unit'],proof_path=f'audit-output/{u}/lifted.rup.gz',receipt_path=f'audit-output/{u}/receipt.json',
            proof_raw_sha256=sha(raw),proof_gzip_sha256=sha(packed),receipt_sha256=sha(receipt),lifted_lines=r['lifted_lines']))
    save(a.output,dict(points=points,parent_input_sha256=PARENT_SHA,all_parent_only_derivations_verified=True,parent_unsat_claimed=False,derivations=rows,
        source_sha256=sha(Path(__file__).read_bytes()),individual_driver_source_sha256=sha((HERE/'verify.py').read_bytes()),controls_sha256=sha((HERE/'audit-output/controls.json').read_bytes()),
        scope='Sixty individually completed native RUP derivations from the retained parent. This inventory does not assert acceptance of any combined proof or parent UNSAT.'))
    print('ADOPTED60 individually accepted parent-only RUP unit derivations; combined status separate')


if __name__=='__main__':main()
