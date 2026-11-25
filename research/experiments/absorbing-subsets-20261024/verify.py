"""Finite exact audits of the absorbing-subset theorem and both sharpness families."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def games():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('finite_games',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def absorbing(n,q,target,edges):
    for ids in combinations(range(n),q):
        mask=sum(1<<i for i in ids)
        if mask & target==target and mask not in edges:return False
    return True


def main():
    engine=games();rows=[]
    for q in range(2,13):
        n=q+1;r=q//2;full=(1<<n)-1
        for sharp in (False,True):
            # On n=q+1 vertices every q-edge is the complement of one point.
            a_size=r+1 if sharp else r
            a=(1<<a_size)-1
            forbidden={full ^ (1<<f) for f in range(a_size,n)}
            if q%2==0:
                assert absorbing(n,q,a,forbidden)
                if not sharp:assert a.bit_count()<=r
            else:
                for v in range(n):
                    target=a | (1<<v)
                    assert absorbing(n,q,target,forbidden)
                    if not sharp:assert target.bit_count()<=r+1
            g,report=engine.occupied_game(n,sorted(forbidden))
            root,other=engine.residual_game(n,sorted(forbidden))
            assert root==g[0] and all(g[s]==value for s,value in other.items())
            assert len(other)==report['safe_count']
            expected_first=(q%2==0) != sharp
            assert (g[0]!=0)==expected_first,(q,sharp,g[0])
            if q%2==0 and not sharp:
                assert all(g[1<<i]==0 for i in range(a_size))
            if q%2==1 and not sharp:
                assert all(g[1<<i]!=0 for i in range(n))
            row={'q':q,'points':n,'sharpness_counterexample':sharp,'A_mask':a,
                 'forbidden_edges':sorted(forbidden),'individually_compared_states':len(other),**report}
            rows.append(row)
            print('q',q,'sharpness',sharp,'g',g[0],'states',len(other),flush=True)
    (HERE/'results.json').write_text(json.dumps({'cases':rows},separators=(',',':'))+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
