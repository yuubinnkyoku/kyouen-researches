"""Check actual split clauses, parent decomposition and new independent schema failure modes."""
import argparse
import gzip
from itertools import product
from pathlib import Path
from schema import audit, prefix, CASES, SEED_SHA
from check_inputs import HERE, SEED, sha, save


def encode(nv,clauses):return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA;seed=list(map(int,seed_raw.split()))[2:];rows=[];parents=[]
    for case in CASES:
        raw=gzip.decompress((HERE/'output'/case/'input.cnf.gz').read_bytes());nv,clauses=prefix.parse(raw);_,report=audit(raw,seed,case);parents.append(encode(nv,clauses[:-1]))
        base=report['point_base'];ids=[21,22,23,24,base+6,base+2533];local=[c for c in clauses if all(abs(v) in ids for v in c)];assert len(local)==14
        for bits in product((False,True),repeat=6):
            values=dict(zip(ids,bits));b,n,l,h,lo,hi=bits
            expected=sum(bits[:4])==1 and lo==(b or l) and hi==(b or h) and b==(case=='retained')
            assert all(any((v>0)==values[abs(v)] for v in c) for c in local)==expected
        clone=lambda:[c[:] for c in clauses];mut={}
        bad=clone();bad[-1]=[-bad[-1][0]];mut['opposite-split']=bad
        bad=clone();bad[-1]=[23 if case=='retained' else -23];mut['wrong-selector']=bad
        bad=clone();bad.pop();mut['missing-split']=bad
        bad=clone();bad.append([1]);mut['extra-unit']=bad
        bad=clone();bad[0][-1]=bad[0][-2];mut['broken-onehot']=bad
        point=next(i for i,c in enumerate(clauses) if c==[-base-1,3,1])
        bad=clone();bad[point][1]=7;mut['wrong-point-definition']=bad
        loss=len(clauses)-1-report['deletion_clauses'];upper=loss+report['counters'][-2]['clauses']
        for name,pos in [('lower-loss',loss),('upper-loss',upper)]:
            bad=clone();bad[pos][0]=-bad[pos][0];mut[name+'-sign']=bad
        for name,bad in mut.items():
            try:audit(encode(nv,bad),seed,case)
            except (AssertionError,KeyError,StopIteration):pass
            else:raise AssertionError((case,name))
        rows.append(dict(case=case,point_and_split_truth_assignments=64,rejected=list(mut)))
    assert parents[0]==parents[1] and sha(parents[0])=='d23890f881d73064f41719de379346d80193fea8ec507a9f7fe0050edf73f40a'
    save(a.output,dict(cases=rows,truth_assignments=128,corruptions_rejected=16,parent_reconstruction_verified=True,
        schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha((HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),scope='Actual B6 units, exact shared parent, local truth tables and rejection controls. Existing parent exact-loss regressions retained; no universal proof inferred from finite samples.'))
    print('PASS 16 corruptions, 128 actual point/split assignments and shared parent')


if __name__=='__main__':main()
