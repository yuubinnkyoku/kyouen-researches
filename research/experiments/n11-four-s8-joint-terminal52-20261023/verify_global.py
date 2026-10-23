#!/usr/bin/env python3
"""Self-contained 11x11 four-root S8 LOSS certificate verifier.

WIN/LOSS is from the original first player's fixed perspective:
S8 even OR is LOSS iff every S9 child is LOSS;
S9 odd AND is LOSS iff at least one S10 child is LOSS.
S10 even roots are directly solved to terminal positions, independently of cache.
"""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path
from fastgeom import canonical, children, legal
from terminal_geometry import next_player_wins_at_s10, safe

HERE=Path(__file__).resolve().parent

def require(cond,msg):
    if not cond:raise ValueError(msg)

def read_keys(path,stones):
    lines=path.read_text().splitlines()
    require(lines==sorted(set(lines)),f'nonunique or unsorted keys: {path.name}')
    result=set()
    for h in lines:
        require(len(h)==32 and all(c in '0123456789abcdef' for c in h),f'bad key: {h}')
        m=int(h,16)
        require(m.bit_count()==stones and canonical(m)==m and safe(m),f'invalid position: {h}')
        result.add(m)
    return result

def read_s10(path):
    out={}
    for line in path.read_text().splitlines():
        a=line.split()
        require(len(a)==4 and a[1] in ('WIN','LOSS'),f'bad S10 row: {line}')
        h,v,n,l=a
        require(len(h)==32 and all(c in '0123456789abcdef' for c in h),f'bad S10 key: {h}')
        require(n.isdecimal() and l.isdecimal(),f'bad numeric S10 field: {line}')
        m=int(h,16)
        require(m not in out,f'duplicate S10: {h}')
        require(m.bit_count()==10 and canonical(m)==m and safe(m),f'invalid S10 position: {h}')
        out[m]=(v,int(n),int(l))
    return out

def read_prior(path):
    out={}
    for line in path.read_text().splitlines():
        a=line.split()
        require(len(a)==2 and a[1] in ('WIN','LOSS'),f'bad prior row: {line}')
        h,v=a
        require(len(h)==32 and all(c in '0123456789abcdef' for c in h),'bad prior key')
        m=int(h,16)
        require(m not in out and m.bit_count()==10 and canonical(m)==m and safe(m),'bad prior S10')
        out[m]=v
    return out

def read_dual(path,obligations):
    weights={}
    for line in path.read_text().splitlines():
        a=line.split()
        require(len(a)==2 and len(a[0])==32 and a[1] in ('1','2'),'bad dual row')
        m=int(a[0],16)
        require(m not in weights and m in obligations,'bad dual key')
        weights[m]=int(a[1])
    return weights

def structural_check(roots,s10,selected,weights,prior,prior_leaves):
    require(len(roots)==4,'expected four roots')
    obligation_by_root={r:children(r) for r in roots}
    obligations=set().union(*obligation_by_root.values())
    require(len(obligations)==103,'unexpected S9 obligation count')
    candidates=set().union(*(children(x) for x in obligations))
    require(len(candidates)==1017,'unexpected candidate universe')
    require(candidates==set(s10),'incomplete S10 candidate universe')
    require(len(s10)==1017 and Counter(x[0] for x in s10.values())=={'WIN':780,'LOSS':237},'S10 count mismatch')
    require(len(selected)==52 and selected <= {m for m in s10 if s10[m][0]=='LOSS'},'bad 52 selected LOSS leaves')
    require(len(prior_leaves)==53 and prior_leaves <= {m for m in s10 if s10[m][0]=='LOSS'},'bad prior 53 leaves')
    for m,(v,n,l) in s10.items():
        require(n>=1 and l==len(legal(m)),f'S10 legal-count mismatch: {m:032x}')
    covered={canonical(m^(1<<p)) for m in selected for p in range(121) if (m>>p)&1}
    require(obligations<=covered,'missing S9 obligation')
    prior_covered={canonical(m^(1<<p)) for m in prior_leaves for p in range(121) if (m>>p)&1}
    require(obligations<=prior_covered,'prior 53 leaves do not cover obligations')
    require(len(weights)==79 and sum(weights.values())==104 and Counter(weights.values())=={1:54,2:25},'bad dual total')
    for m,(v,_,_) in s10.items():
        if v!='LOSS':continue
        score=sum(weights.get(canonical(m^(1<<p)),0) for p in range(121) if (m>>p)&1)
        require(score<=2,f'dual constraint violated at {m:032x}: {score}/2')
    overlap=set(prior)&set(s10)
    require(len(prior)==925 and len(overlap)==730,'prior overlap mismatch')
    for m in overlap:
        require(prior[m]==s10[m][0],f'WIN/LOSS conflict with prior: {m:032x}')
    require(sum(s10[m][1] for m in selected)==12280,'selected leaf-state cost mismatch')
    require(sum(s10[m][1] for m in prior_leaves)==12327,'prior leaf-state cost mismatch')
    return dict(roots=len(roots),s9_edges=sum(map(len,obligation_by_root.values())),
                distinct_s9_obligations=len(obligations),all_s10_candidates=len(candidates),
                terminal_s10_win=780,terminal_s10_loss=237,selected_s10_loss=len(selected),
                dual_half_units=sum(weights.values()),lower_bound_leaves=52,
                selected_leaf_individual_state_sum=12280,prior_leaf_count=53,prior_leaf_individual_state_sum=12327,prior925_overlap=len(overlap),
                newly_classified_relative_to_prior925=len(candidates)-len(overlap),
                newly_classified_win=sum(v[0]=='WIN' for m,v in s10.items() if m not in prior),
                newly_classified_loss=sum(v[0]=='LOSS' for m,v in s10.items() if m not in prior),
                empty_board='UNKNOWN')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--skip-terminal',action='store_true',help='STRUCTURAL TEST ONLY; not an independent terminal proof')
    args=ap.parse_args()
    roots=read_keys(HERE/'roots4.keys',8)
    s10=read_s10(HERE/'s10-all1017.tsv')
    selected=read_keys(HERE/'selected52.keys',10)
    prior_leaves=read_keys(HERE/'prior53.keys',10)
    prior=read_prior(HERE/'prior925.tsv')
    obligations=set().union(*(children(x) for x in roots))
    weights=read_dual(HERE/'dual-weights.tsv',obligations)
    result=structural_check(roots,s10,selected,weights,prior,prior_leaves)
    if not args.skip_terminal:
        for i,m in enumerate(sorted(s10)):
            first_win,n=next_player_wins_at_s10(m)
            v,states,legal_count=s10[m]
            require(('WIN' if first_win else 'LOSS',n,len(legal(m)))==(v,states,legal_count),
                    f'INDEPENDENT TERMINAL CONFLICT at {m:032x}')
            if (i+1)%250==0:print('independent Python terminal:',i+1,'/ 1017',flush=True)
        result['independent_python_terminal']='PASS: all 1017 exact verdict, states, legal counts'
    print('PASS',result)

if __name__=='__main__':main()
