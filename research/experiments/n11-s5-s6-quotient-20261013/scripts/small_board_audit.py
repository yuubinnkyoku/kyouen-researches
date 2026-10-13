"""Exhaustive small-board check and sharp three-stone counterexample."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'research/experiments/n11-independent-exact-audit-20261010/scripts'))
from independent import Board


def record(board,mask):
    pts=board.points(mask)
    moves=board.points(board.legal(mask))
    stab=[t for t,m in enumerate(board.maps) if sum(m[p] for p in pts)==mask]
    orbits={min(board.maps[t][p] for t in stab) for p in moves}
    children={board.canonical(mask|1<<p) for p in moves}
    assert len(children)<=len(orbits)
    return dict(points=list(pts),legal=len(moves),stabilizer_order=len(stab),
                stabilizer_orbits=len(orbits),canonical_children=len(children),
                extra_merges=len(orbits)-len(children))


def main():
    result={'schema':'safe-child-orbit-audit-v1','boards':[]}
    for n in range(1,6):
        board=Board(n)
        masks=range(1<<(n*n)) if n<=4 else (sum(1<<p for p in ps) for k in range(4) for ps in combinations(range(n*n),k))
        hist=Counter();extra=Counter();edges=0;examples=[]
        for mask in masks:
            try: r=record(board,mask)
            except ValueError: continue
            k=mask.bit_count();hist[k]+=1;edges+=r['legal']
            if r['extra_merges']:
                extra[k]+=1
                assert k<4,(n,r)
                if len(examples)<3:examples.append(r)
        result['boards'].append(dict(n=n,coverage='all safe subsets' if n<=4 else 'all subsets of size 0..3',
                                     safe_parents=sum(hist.values()),legal_edges=edges,
                                     safe_by_size=dict(sorted(hist.items())),
                                     extra_merge_parents_by_size=dict(sorted(extra.items())),examples=examples))
        board.canonical.cache_clear(); board.legal.cache_clear();board.completion.cache_clear()
    board=Board(11)
    parent=sum(1<<p for p in (60,69,83))
    witness=record(board,parent)
    p,q=37,51
    assert board.legal(parent)>>p&1 and board.legal(parent)>>q&1
    assert board.canonical(parent|1<<p)==board.canonical(parent|1<<q)
    assert witness['stabilizer_order']==1 and witness['extra_merges']>0
    witness.update(p=p,q=q,canonical_child=str(board.canonical(parent|1<<p)),
                   meaning='safe three-stone parent; two legal moves in distinct stabilizer orbits have D4-equivalent children')
    result['sharp_counterexample']=witness
    out=Path(__file__).resolve().parents[1]/'output/small-board-audit.json'
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
