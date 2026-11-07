#!/usr/bin/env python3
"""Bounded SMT witness synthesis; UNSAT/UNKNOWN is not promoted to a theorem."""
import argparse
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import time


def direct(n,edges):
    def mex(options):
        value=0
        while value in options:value+=1
        return value
    @lru_cache(None)
    def game(s):
        return mex({game(s|1<<v) for v in range(n) if not s>>v&1
                    and all((s|1<<v)&edge!=edge for edge in edges)})
    return game(0),[game(1<<v) for v in range(n)]


def main():
    import z3
    parser=argparse.ArgumentParser();parser.add_argument('--vertices',type=int,default=8)
    parser.add_argument('--grundy',type=int,default=6);parser.add_argument('--timeout-ms',type=int,default=60000)
    parser.add_argument('--edge-count',type=int)
    args=parser.parse_args();n=args.vertices
    triples=[sum(1<<v for v in edge) for edge in combinations(range(n),3)]
    selected=[z3.Bool('edge_'+str(i)) for i in range(len(triples))]
    safe=[z3.And([z3.Not(selected[i]) for i,t in enumerate(triples) if s&t==t]) for s in range(1<<n)]
    values=[z3.Int('g_'+str(s)) for s in range(1<<n)]
    solver=z3.Solver();solver.set(timeout=args.timeout_ms)
    for s in range(1<<n):
        children=[s|1<<v for v in range(n) if not s>>v&1]
        mobility=z3.Sum([z3.If(safe[child],1,0) for child in children]) if children else z3.IntVal(0)
        # The universal gap-two bound is independently audited in a separate experiment.
        upper=z3.If(mobility>=5,mobility-2,z3.If(mobility>=2,mobility-1,mobility))
        solver.add(z3.Implies(safe[s],z3.And(values[s]>=0,values[s]<=upper)))
        solver.add(z3.Implies(z3.Not(safe[s]),values[s]==-1))
        for child in children:
            solver.add(z3.Implies(z3.And(safe[s],safe[child]),values[s]!=values[child]))
        for k in range(n-s.bit_count()):
            solver.add(z3.Implies(z3.And(safe[s],values[s]>k),
                                 z3.Or([z3.And(safe[child],values[child]==k) for child in children])))
    solver.add(values[0]==args.grundy)
    # Distinct options of these values exist by mex; relabel them as vertices 0,1.
    if args.grundy>=2:
        solver.add(values[1]==args.grundy-1,values[2]==args.grundy-2)
    if args.edge_count is not None:
        solver.add(z3.Sum([z3.If(edge,1,0) for edge in selected])==args.edge_count)
    start=time.monotonic();result=solver.check()
    output=dict(vertices=n,target_grundy=args.grundy,edge_count_constraint=args.edge_count,
                solver='z3 '+z3.get_version_string(),timeout_ms=args.timeout_ms,
                result=str(result),seconds=time.monotonic()-start)
    if result==z3.sat:
        model=solver.model();edges=[t for i,t in enumerate(triples) if z3.is_true(model.eval(selected[i]))]
        actual,children=direct(n,edges)
        assert actual==args.grundy
        output.update(edges=edges,independent_python_grundy=actual,child_grundy=children)
    elif result==z3.unknown:
        output['reason']=solver.reason_unknown()
    target=Path(__file__).with_name('output')/('n'+str(n)+'_g'+str(args.grundy)+'_e'+str(args.edge_count)+'.json')
    target.parent.mkdir(exist_ok=True);target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
