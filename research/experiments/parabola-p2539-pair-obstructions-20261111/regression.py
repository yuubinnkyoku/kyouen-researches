"""Check pair-to-singleton reduction exhaustively on small seeds and reject corrupt trees."""
import argparse
from itertools import combinations,permutations
import json
from pathlib import Path
from verify import HERE,OLD,families,checker,sha,save


def determinant(rows):
    result=0
    for perm in permutations(range(4)):
        term=1
        for i,j in enumerate(perm):term*=rows[i][j]
        inversions=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        result+=term*(-1 if inversions%2 else 1)
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    seeds=0;quads=0;deletions=0
    for p in [7,11]:
        fixed={0,1,p-1};free=sorted(set(range(p))-fixed)
        for mask in range(1<<len(free)):
            seed=fixed|{v for i,v in enumerate(free) if mask&(1<<i)};fs,added=families(seed,[],p,(1,p-1));seeds+=1
            for u,qs in fs.items():
                mirror=p-u;assert bool(qs)==(mirror in seed)
                if not qs:continue
                q=qs[0];assert len(qs)==1 and set(q)-fixed-{u}=={mirror}
                rows=[]
                for t in q:
                    y=t*t%p;rows.append([t*t+y*y,t,y,1])
                assert determinant(rows)==0;quads+=1
                removable=sorted(seed-fixed)
                for n in range(min(2,len(removable))+1):
                    for choice in combinations(removable,n):
                        d=set(choice);t=(seed-d)|{u}
                        assert (not set(q)<=t)==bool(d&{mirror});deletions+=1
    oldreg=json.loads((OLD/'regression.json').read_bytes());assert sha((OLD/'verify.py').read_bytes())==oldreg['verifier_source_sha256']
    # The new singleton must consume one unit of deletion budget.
    rows=[{9},{1,2},{3,4}];proof=dict(type='packing',edges=[0,1,2]);checker.check_tree(rows,2,proof)
    rejected=[]
    for name,bad in [('duplicate-constraint',dict(type='packing',edges=[0,0,2])),('under-budget-count',dict(type='packing',edges=[1,2])),('invalid-edge',dict(type='packing',edges=[0,1,3]))]:
        try:checker.check_tree(rows,2,bad)
        except (AssertionError,KeyError):rejected.append(name)
        else:raise AssertionError(name)
    for name,d in [('missed-singleton',[1,3]),('too-many-deletions',[9,1,3])]:
        try:checker.check_hitting(rows,2,d,{9,1,2,3,4})
        except AssertionError:rejected.append(name)
        else:raise AssertionError(name)
    save(a.output,dict(small_seed_cases=seeds,pair_quadruples=quads,deletion_cases=deletions,corruptions_rejected=rejected,
        source_sha256=sha(Path(__file__).read_bytes()),family_verifier_source_sha256=sha((HERE/'verify.py').read_bytes()),hitting_verifier_source_sha256=sha((OLD/'verify.py').read_bytes()),
        scope='Exhaustive p7/p11 seed families, independent integer determinant and deletion/singleton semantics; existing hitting-tree brute-force regression remains separately pinned.'))
    print('PASS',seeds,'small seeds,',quads,'pair determinants,',deletions,'deletion cases, 5 corruptions')


if __name__=='__main__':main()
