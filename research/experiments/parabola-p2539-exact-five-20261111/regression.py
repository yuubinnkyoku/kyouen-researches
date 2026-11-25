"""Compare exact deletion counts with direct small-prime geometry and actual SAT models."""
import argparse
from itertools import combinations,product
from pathlib import Path
import sys
from pysat.solvers import Cadical195
from search import HERE, build, save, sha
sys.path.insert(0,str(HERE.parent/'parabola-p2539-pair-pilot-20261110'))
from verify_saved import determinant


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();assert not args.output.exists()
    rows=[]
    for p in (5,7,17):
        h=(p-1)//2;edges=[q for q in combinations(range(p),4) if determinant(q,p)==0];free=list(range(2,h+1))
        seed=next(sorted([0,1,p-1]+[p-i if b else i for i,b in zip(free,bits)]) for bits in product((False,True),repeat=h-1)
                  if all(not set(q)<=set([0,1,p-1]+[p-i if b else i for i,b in zip(free,bits)]) for q in edges))
        for origin in (0,1):
            for both_count in (0,1):
                choices=sorted({1,h}) if both_count else [None];states=[]
                for both in choices:
                    variable_pairs=[i for i in range(1,h+1) if i!=both]
                    for sides in product((1,2,3),repeat=len(variable_pairs)):
                        values=dict(zip(variable_pairs,sides))
                        if both is not None:values[both]=0
                        positive={4*i-3+values[i] for i in range(1,h+1)}
                        points=([0] if origin else [])+[t for i in range(1,h+1) for t in ([i,p-i] if values[i]==0 else [i] if values[i]==2 else [p-i] if values[i]==3 else [])]
                        safe=all(not set(q)<=set(points) for q in edges);states.append((positive,points,safe))
                for target in sorted({h+origin+both_count,max(1,h+origin+both_count-1)}):
                    for loss in (0,1,min(3,len(seed)-1)):
                        removed=loss+(1-origin)
                        clauses,nv,base,prior,_,actual_loss=build(p,seed,target,origin,both_count,removed,edges)
                        assert base>=4*h and nv>=prior>=base+p-1 and actual_loss==loss
                        yes,no=0,0
                        with Cadical195(bootstrap_with=clauses) as solver:
                            for positive,points,safe in states:
                                expected=safe and len(points)==target and len(set(seed)-set(points))==removed
                                assumptions=[v if v in positive else -v for v in range(1,4*h+1)]
                                actual=solver.solve(assumptions=assumptions);assert actual==expected,(p,origin,both_count,target,removed,points)
                                yes+=actual;no+=not actual
                        rows.append(dict(p=p,origin=origin,complete_pairs=both_count,target=target,removed_exactly=removed,
                                         assignments=len(states),sat=yes,unsat=no))
    assert any(r['sat'] for r in rows) and any(r['unsat'] for r in rows)
    save(args.output,dict(rows=rows,total_assignments=sum(r['assignments'] for r in rows),source_sha256=sha(Path(__file__).read_bytes()),
         search_source_sha256=sha((HERE/'search.py').read_bytes()),scope='Small-prime exact-size/exact-loss semantics with signed loss literals and origin accounting; complete-pair identity sampled at p17. Not a general soundness proof.'))
    print('PASS',sum(r['assignments'] for r in rows),'exact-loss assignments',flush=True)


if __name__=='__main__':main()
