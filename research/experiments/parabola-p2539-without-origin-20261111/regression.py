"""Check real origin-free schemas, origin deletion accounting, and subset selection."""
import argparse
import gzip
from itertools import product
from pathlib import Path
from schema import audit, prefix
from audit import HERE, sha, save


def encode(nv,clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();assert not args.output.exists()
    seed=list(map(int,(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes().split()))[2:]
    rows=[]
    for pairs in (0,1):
        raw=gzip.decompress((HERE/'output'/f'B{pairs}-target1259-remove4/input.cnf.gz').read_bytes())
        nv,clauses=prefix.parse(raw);_,report=audit(raw,seed,pairs);base=report['point_base']
        ids=[1,2,3,4,base+1,base+2538];local=[c for c in clauses if all(abs(v) in ids for v in c)]
        assert len(local)==(14 if pairs==0 else 13)
        for bits in product((False,True),repeat=6):
            values=dict(zip(ids,bits));b,n,l,h,a,z=bits
            expected=sum(bits[:4])==1 and a==(b or l) and z==(b or h) and (pairs==1 or not b)
            assert all(any((v>0)==values[abs(v)] for v in c) for c in local)==expected
        clone=lambda:[c[:] for c in clauses];mutations={}
        bad=clone();bad[0][-1]=bad[0][-2];mutations['broken-onehot']=bad
        bad=clone();bad[8883]=[-bad[8883][0]] if pairs==0 else bad[8883][:-1];mutations['wrong-BOTH-count']=bad
        start=next(i for i,c in enumerate(clauses) if c==[-base-1,3,1])
        bad=clone();bad[start][1]=7;mutations['wrong-point-definition']=bad
        bad=clone();bad[start][0]=-3;mutations['point-selector-alias']=bad
        geo=start+report['point_definition_clauses']
        bad=clone();bad[geo]=bad[geo][:-1];mutations['origin-dependent-triple']=bad
        loss=len(clauses)-report['deletion_clauses']
        bad=clone();bad[loss][0]=-bad[loss][0];mutations['wrong-loss-polarity']=bad
        overflow=next(i for i in range(loss,len(clauses)) if len(clauses[i])==2 and clauses[i][0]>0 and clauses[i][1]<0)
        bad=clone();bad[overflow][1]+=1;mutations['wrong-nonzero-bound']=bad
        rejected=[]
        for name,altered in mutations.items():
            try:audit(encode(nv,altered),seed,pairs)
            except (AssertionError,KeyError,StopIteration):rejected.append(name)
            else:raise AssertionError((pairs,name))
        assert report['origin_deletion_cost']+report['nonzero_deletion_bound']==report['total_deletion_bound']==4
        rows.append(dict(complete_pairs=pairs,rejected=rejected,point_truth_assignments=64))
    original={0,1,2,10};target=5;checked=0
    for mask in range(1<<11):
        chosen={t for t in range(11) if mask&(1<<t)}
        ps=[i for i in range(1,6) if i in chosen and 11-i in chosen]
        if 0 in chosen or len(chosen)<target or len(ps)>1 or len(original-chosen)>2:continue
        required=original&chosen
        if ps:required|={ps[0],11-ps[0]}
        assert len(required)<=target
        subset=required|set(sorted(chosen-required)[:target-len(required)])
        assert len(subset)==target and 0 not in subset and subset<=chosen and original-subset==original-chosen
        assert len(original-subset)==1+len((original-{0})-subset)
        assert [i for i in range(1,6) if i in subset and 11-i in subset]==ps
        checked+=1
    assert checked>0
    save(args.output,dict(cases=rows,point_truth_assignments=128,subset_cases=checked,
         schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha((HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py').read_bytes()),
         regression_source_sha256=sha(Path(__file__).read_bytes()),scope='Fourteen corrupt schemas rejected, origin-cost accounting, actual point truth tables, finite origin-free subset analogue. Not a general soundness proof.'))
    print('PASS 14 corruptions, 128 point truth assignments,',checked,'origin-free subset cases',flush=True)


if __name__=='__main__':main()
