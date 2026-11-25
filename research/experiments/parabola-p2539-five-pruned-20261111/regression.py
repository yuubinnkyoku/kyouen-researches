"""Reject wrong unit mappings, parent mutations and malformed augmented inputs."""
import argparse
import gzip
from pathlib import Path
from schema import audit,parent,HERE,sha
from check_inputs import save


def encode(nv,clauses):return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    seed=list(map(int,(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes().split()))[2:]
    raw=gzip.decompress((HERE/'output/input.cnf.gz').read_bytes());nv,cs=parent.prefix.parse(raw);_,_,r=audit(raw,seed)
    clone=lambda:[c[:] for c in cs];mut={}
    bad=clone();bad[-1][0]=-bad[-1][0];mut['wrong-unit-sign']=bad
    bad=clone();bad[-1][0]+=1;mut['wrong-point-index']=bad
    bad=clone();bad[-1]=[21];mut['selector-instead-of-point']=bad
    bad=clone();bad[-1]=bad[-2][:];mut['duplicate-unit']=bad
    bad=clone();bad[-1],bad[-2]=bad[-2],bad[-1];mut['wrong-unit-order']=bad
    bad=clone();bad.pop();mut['missing-unit']=bad
    bad=clone();bad.append([-1]);mut['extra-unit']=bad
    bad=clone();bad[-61]=[-21];mut['changed-parent-pair']=bad
    bad=clone();bad[0][-1]=bad[0][-2];mut['changed-parent-onehot']=bad
    rejected=[]
    for name,cs2 in mut.items():
        try:audit(encode(nv,cs2),seed)
        except (AssertionError,KeyError):rejected.append(name)
        else:raise AssertionError(name)
    try:audit(encode(nv+1,cs),seed)
    except AssertionError:rejected.append('wrong-variable-count')
    else:raise AssertionError('wrong-variable-count')
    for clause in cs[-60:]:
        assert len(clause)==1 and clause[0]<0
        for selected in [False,True]:assert ((clause[0]>0)==selected)==(not selected)
    assert len(rejected)==10 and r['added_units']==60 and len(r['excluded'])==60
    save(a.output,dict(corruptions_rejected=rejected,point_unit_truth_assignments=120,schema_source_sha256=sha((HERE/'schema.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Actual pruned CNF parent preservation and60 negative point mappings checked; parent and hitting-tree regressions are separately preserved. Not a new soundness proof or search result.'))
    print('PASS 10 corruptions, 120 actual point-unit assignments')


if __name__=='__main__':main()
