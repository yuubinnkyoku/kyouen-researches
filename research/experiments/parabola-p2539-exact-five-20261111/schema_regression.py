"""Exercise actual exact-five schemas, both loss bounds and subset preservation."""
import argparse
import gzip
from itertools import product
from pathlib import Path
from schema import audit, prefix, CASES
from verify import HERE, sha, save


def encode(nv,clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();assert not args.output.exists()
    seed=list(map(int,(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes().split()))[2:]
    rows=[]
    for case,(x,pairs) in CASES.items():
        raw=gzip.decompress((HERE/'output'/f'{case}-target1259-remove5/input.cnf.gz').read_bytes())
        nv,clauses=prefix.parse(raw);_,report=audit(raw,seed,case);base=report['point_base']
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
        bad=clone();bad[geo]=bad[geo][:-1] if not x else [-base-1,-base-2,-base-3];mutations['wrong-geometric-arity-or-sum']=bad
        loss=len(clauses)-report['deletion_clauses'];upper=loss+report['counters'][-2]['clauses']
        for label,pos in [('loss-lower',loss),('loss-upper',upper)]:
            bad=clone();bad[pos][0]=-bad[pos][0];mutations[label+'-polarity']=bad
            bad=clone();del bad[pos];mutations[label+'-missing-clause']=bad
        rejected=[]
        for name,altered in mutations.items():
            try:audit(encode(nv,altered),seed,case)
            except (AssertionError,KeyError,StopIteration):rejected.append(name)
            else:raise AssertionError((case,name))
        assert report['origin_deletion_cost']+report['nonzero_removed_exactly']==report['removed_exactly']==5
        rows.append(dict(case=case,rejected=rejected,point_truth_assignments=64))
    original={0,1,2,10};target=5;checked=0;origins=set()
    for mask in range(1<<11):
        chosen={t for t in range(11) if mask&(1<<t)}
        ps=[i for i in range(1,6) if i in chosen and 11-i in chosen]
        if len(chosen)<target or len(ps)>1 or len(original-chosen)!=2:continue
        required=original&chosen
        if ps:required|={ps[0],11-ps[0]}
        assert len(required)<=target
        subset=required|set(sorted(chosen-required)[:target-len(required)])
        assert len(subset)==target and subset<=chosen and original-subset==original-chosen
        assert (0 in subset)==(0 in chosen)
        assert [i for i in range(1,6) if i in subset and 11-i in subset]==ps
        checked+=1;origins.add(0 in chosen)
    assert checked>0 and origins=={False,True}
    save(args.output,dict(cases=rows,corruptions_rejected=sum(len(r['rejected']) for r in rows),point_truth_assignments=192,subset_cases=checked,
         schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha((HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py').read_bytes()),
         regression_source_sha256=sha(Path(__file__).read_bytes()),scope='Actual CNF mutations, both exact-loss inequalities, point truth tables and finite subset analogues. General subset/model-extension arguments are separate.'))
    print('PASS',sum(len(r['rejected']) for r in rows),'corruptions, 192 point assignments,',checked,'subset cases',flush=True)


if __name__=='__main__':main()
