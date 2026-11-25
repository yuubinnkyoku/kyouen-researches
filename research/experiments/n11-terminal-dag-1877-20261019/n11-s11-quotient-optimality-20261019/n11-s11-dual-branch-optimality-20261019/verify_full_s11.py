#!/usr/bin/env python3
"""Independently re-enumerate all relevant S11 positions and check C++ results."""
from collections import defaultdict
from pathlib import Path
from time import perf_counter
import argparse
from compact_proof184 import (ROOTS_B85,WEIGHTS_B85,decode,decode_positions,children,canonical,legal,points,next_player_wins_at_s10,check)

def candidates():
    roots=decode_positions(ROOTS_B85)
    obligations=set().union(*(children(r) for r in roots))
    packed=decode(WEIGHTS_B85)
    weights={p:(packed[i//4]>>(2*(i%4)))&3 for i,p in enumerate(sorted(obligations))}
    boundary=set().union(*(children(o) for o in obligations))
    high=sorted(p for p in boundary if sum(weights[q] for q in ({canonical(p^(1<<i)) for i in points(p)}&obligations))>2)
    parents=defaultdict(set)
    for idx,p in enumerate(high):
        for q in legal(p):parents[canonical(p|(1<<q))].add(idx)
    check(len(high)==672 and len(parents)==4522)
    return high,parents

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",type=int,default=0)
    ap.add_argument("--end",type=int,default=4522)
    args=ap.parse_args()
    check(0<=args.start<args.end<=4522)
    start=perf_counter()
    high,parents=candidates()
    source=Path(__file__).resolve().parent/'all_s11_cpp.tsv'
    data={}
    for line in source.read_text().splitlines():
        key,outcome,states,moves,witness=line.split()
        p=int(key,16)
        check(p not in data,'duplicate C++ row')
        data[p]=(outcome,int(states),int(moves))
    check(set(data)==set(parents),'C++ table has missing or extra states')
    check(len(data)==4522)
    total=0
    for j,p in enumerate(sorted(parents)):
        if not args.start<=j<args.end:continue
        win,states=next_player_wins_at_s10(p)
        verdict='WIN' if win else 'LOSS'
        check(data[p][:2]==(verdict,states),f'Python/C++ disagreement: {p:032x}')
        total+=states
        if (j+1)%100==0:print(f'checked {j+1}/4522',flush=True)
    if args.start==0 and args.end==4522:check(total==86411)
    check(sum(v[0]=='LOSS' for v in data.values())==982)
    selected={int(x,16) for x in (source.parent/'selected_s11_witnesses.txt').read_text().split()}
    check(len(selected)==345 and selected<=data.keys())
    check(all(data[p][0]=='LOSS' for p in selected))
    check(sum(data[p][1] for p in selected)==7779)
    check(set().union(*(parents[p] for p in selected))==set(range(672)))
    print(f'PASS Python/C++ independent check S11 indices [{args.start},{args.end}), {total} states')
    print(f'PASS selected 345 S11 LOSS cover all 672 high-weight S10 positions, cost 7779')
    print(f'elapsed {perf_counter()-start:.2f}s')
if __name__=='__main__':main()
