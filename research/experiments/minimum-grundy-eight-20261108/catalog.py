#!/usr/bin/env python3
"""Exact normal point/edge Pareto fronts from <=7-edge census and point-optimal witnesses."""
import json
from pathlib import Path
from verify import ROOT


def main():
    directory=Path(__file__).resolve().parent
    old=json.loads((ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())['records']
    six=json.loads((ROOT/'research/experiments/pure-triple-six-edge-complete-20261108/output/audit.json').read_text())['records']
    seven=json.loads((ROOT/'research/experiments/pure-triple-seven-edge-complete-20261108/output/audit.json').read_text())['records']
    rows=[dict(n=r['n'],edges=r['edges'],grundy=r['grundy']) for r in old+six+seven]
    candidates={g:{} for g in range(2,10)}
    for row in rows:
        for free in (0,1):
            g=row['grundy']^free
            if g not in candidates:continue
            h=len(row['edges']);n=row['n']+free
            if h not in candidates[g] or n<candidates[g][h]['n']:
                candidates[g][h]=dict(n=n,edges=row['edges'],grundy=g,free_parity=free)
    extra=json.loads((directory/'output/audit_pruned.json').read_text())['records']
    for row in extra:
        g=row['normal'];h=len(row['edges'])
        if h not in candidates[g] or row['n']<candidates[g][h]['n']:
            candidates[g][h]=dict(n=row['n'],edges=row['edges'],grundy=g,free_parity=g%2)
    minima={2:6,3:7,4:6,5:7,6:8,7:9,8:10,9:11};fronts={}
    for g,by_edges in candidates.items():
        assert min(row['n'] for row in by_edges.values())==minima[g]
        points=[(row['n'],h,row) for h,row in by_edges.items()]
        fronts[g]=[]
        for n,h,row in sorted(points):
            if not any((p<=n and e<=h and (p,e)!=(n,h)) for p,e,other in points):
                fronts[g].append(dict(legal_points=n,edge_count=h,witness=row))
        assert any(r['legal_points']==minima[g] and r['edge_count']<=8 for r in fronts[g])
    output=dict(audit='PASS',complete_kernel_types_through_seven_edges=len(rows),free_parity_classes=2*len(rows),
                fronts=fronts,completeness='all higher edge counts are dominated by a point-minimal witness with at most eight edges',
                global_point_lower_bounds=minima,limitation='normal Grundy fronts only; not a minimum occupied-anchor count')
    (directory/'output/pareto.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({g:[(r['legal_points'],r['edge_count']) for r in front] for g,front in fronts.items()},indent=2))


if __name__=='__main__':main()
