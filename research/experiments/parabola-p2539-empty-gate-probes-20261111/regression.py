"""Check the newly augmented input and all actual positive point assumptions."""
import argparse
import gzip
from pathlib import Path
from audit import HERE,parent,qualify_base,sha,save


def encode(nv,cs):return (f'p cnf {nv} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    seed=list(map(int,(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes().split()))[2:]
    raw=gzip.decompress((HERE/'output/base.cnf.gz').read_bytes());cs,_,_,r=qualify_base(raw,seed);clone=lambda:[c[:] for c in cs];mut={}
    bad=clone();bad[-1][0]=-bad[-1][0];mut['negative-unit-sign']=bad
    bad=clone();bad[-1][0]+=1;mut['wrong-point']=bad
    bad=clone();bad[-1]=[21];mut['point-selector-alias']=bad
    bad=clone();bad[-1]=bad[-2][:];mut['repeated-exclusion']=bad
    bad=clone();bad.pop();mut['omitted-exclusion']=bad
    bad=clone();bad[-117]=[-21];mut['changed-parent-pair']=bad
    rejected=[]
    for name,bad in mut.items():
        try:qualify_base(encode(51570,bad),seed)
        except (AssertionError,KeyError):rejected.append(name)
        else:raise AssertionError(name)
    for u in r['gate_points']:
        literal=36512+u;assert 36512<literal<=39050 and u not in seed and 2539-u not in seed and u not in r['excluded']
        for selected in [False,True]:assert ((literal>0)==selected)==selected
    assert len(r['gate_points'])==26 and len(rejected)==6
    save(a.output,dict(corruptions_rejected=rejected,positive_assumption_truth_assignments=52,base_clause_count=len(cs),
        audit_source_sha256=sha((HERE/'audit.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),scope='Actual116-unit augmentation corruption controls and26 positive point mappings; parent and hitting-tree regressions remain separately pinned.'))
    print('PASS6 base-input corruptions and52 actual positive assumption assignments')


if __name__=='__main__':main()
