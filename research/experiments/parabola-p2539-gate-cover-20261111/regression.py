"""Reject corruption at both pair-proof and18-case covering layers of the actual certificate."""
import argparse
import copy
import gzip
import json
from pathlib import Path
from verify import HERE,audit,save,sha


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();cert=json.loads(gzip.decompress((HERE/'output/certificate.json.gz').read_bytes()));audit(cert)
    rejected=[]
    def reject(name,mutation):
        c=copy.deepcopy(cert);mutation(c)
        try:audit(c)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(name);return
        raise AssertionError('accepted '+name)
    ci=next(i for i,e in enumerate(cert['entries']) if e['point'] in cert['newly_excluded'])
    pi,pj=next((i,j) for i,e in enumerate(cert['entries']) for j,r in enumerate(e['cases']) if r['status']=='HITTING_WITNESS')
    reject('missing-point',lambda c:c['entries'].pop())
    reject('missing-cover-case',lambda c:c['entries'][ci]['cases'].pop())
    reject('repeated-cover-case',lambda c:c['entries'][ci]['cases'].__setitem__(1,c['entries'][ci]['cases'][0]))
    reject('false-empty-refutation',lambda c:c['entries'][ci]['cases'][0].__setitem__('refutation',dict(type='empty',edge=0)))
    reject('empty-hitting-witness',lambda c:c['entries'][pi]['cases'][pj].__setitem__('deletions',[]))
    reject('omitted-new-point',lambda c:c['newly_excluded'].pop())
    reject('wrong-prior-gate',lambda c:c['gate'].__setitem__(0,61))
    reject('wrong-budget',lambda c:c.__setitem__('max_deletions',6))
    save(a.output,dict(corruptions_rejected=rejected,verifier_source_sha256=sha((HERE/'verify.py').read_bytes()),
        source_sha256=sha(Path(__file__).read_bytes()),scope='Actual covering/proof corruption controls. The frozen hitting solver/verifier already have495 brute-force comparisons in the gate-pair experiment; these controls test the new cover layer.'))
    print('PASS',len(rejected),'actual covering/proof corruptions rejected')


if __name__=='__main__':main()
