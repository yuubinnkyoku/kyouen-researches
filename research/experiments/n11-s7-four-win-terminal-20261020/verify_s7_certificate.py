#!/usr/bin/env python3
"""Independent geometry and terminal recursion verifier of fixed-player S7 WIN proofs.
No C++ solver output is used to derive edges or outcomes; it is compared only.
"""
import argparse, json,sys,copy
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from terminal_geometry import canonical, children, next_player_wins_at_s10, safe, legal

def require(v,msg):
    if not v: raise AssertionError(msg)

def verify_structure(cert):
    require(cert['rule']=='11x11 standard q4, complete call, normal play, fixed original-first-player WIN/LOSS','rule')
    roots=cert['roots'];witness=cert['s8_witness'];s9=cert['s9_children'];leaves=cert['s10_verdict']
    require(len(roots) in (1,4),'root count')
    require(set(roots).issubset(set(['00000000041000001000401080100000','00000000041000001000501000100000','00000000041000021000401000100000','00000000041002001000401000100000'])),'unexpected roots')
    s8all=set();s9all=set();leafall=set()
    for r,cs in roots.items():
        b=int(r,16)
        require(b.bit_count()==7 and canonical(b)==b and safe(b),'bad S7 root')
        expect={f'{x:032x}' for x in children(b)}
        require(len(cs)==len(set(cs)) and set(cs)==expect,'S7 children incomplete: '+r)
        s8all.update(cs)
    require(set(witness)==s8all,'S8 missing/extraneous')
    for a,b in witness.items():
        root=int(a,16);child=int(b,16)
        require(root.bit_count()==8 and canonical(root)==root and safe(root),'invalid S8')
        require(b in {f'{x:032x}' for x in children(root)},'S8->S9 invalid: '+a)
        s9all.add(b)
    require(set(s9)==s9all,'S9 missing/extraneous')
    for a,cs in s9.items():
        root=int(a,16)
        require(root.bit_count()==9 and canonical(root)==root and safe(root),'invalid S9')
        expect={f'{x:032x}' for x in children(root)}
        require(len(cs)==len(set(cs)) and set(cs)==expect,'S9 children incomplete: '+a)
        leafall.update(cs)
    require(set(leaves)==leafall,'S10 missing/extraneous')
    for a,r in leaves.items():
        b=int(a,16)
        require(b.bit_count()==10 and canonical(b)==b and safe(b),'invalid S10')
        require(isinstance(r,list) and len(r)==2 and all(isinstance(x,int) for x in r),'bad S10 result')
    s6=int(cert['s6_target'],16)
    require(s6.bit_count()==6 and canonical(s6)==s6 and safe(s6),'invalid S6')
    require(set(roots).issubset({f'{x:032x}' for x in children(s6)}),'S6->S7 invalid')
    return len(s8all),len(s9all),len(leafall)

def calc_one(item):
    h,record=item
    b=int(h,16)
    result,states=next_player_wins_at_s10(b)
    return h,result,states,len(legal(b)),record

def verify_terminal(cert,workers):
    items=sorted(cert['s10_verdict'].items())
    total=0
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i,(h,w,states,moves,record) in enumerate(pool.map(calc_one,items,chunksize=8)):
            require(w,'terminal LOSS at '+h)
            require(states==record[0] and moves==record[1],f'C++/Python mismatch {h}: {states,moves} != {record}')
            total+=states
            if (i+1)%500==0:print('verified',i+1,'/',len(items),flush=True)
    return total

def negative_tests(cert):
    bad=copy.deepcopy(cert)
    r=next(iter(bad['roots']));bad['roots'][r].pop()
    try:verify_structure(bad);raise AssertionError('missing S8 was accepted')
    except AssertionError as e:require(str(e)!='missing S8 was accepted','negative test1')
    bad=copy.deepcopy(cert)
    r=next(iter(bad['s9_children']));bad['s9_children'][r].pop()
    try:verify_structure(bad);raise AssertionError('missing S10 was accepted')
    except AssertionError as e:require(str(e)!='missing S10 was accepted','negative test2')
    bad=copy.deepcopy(cert)
    r=next(iter(bad['s8_witness']));bad['s8_witness'][r]=r
    try:verify_structure(bad);raise AssertionError('illegal edge accepted')
    except AssertionError as e:require(str(e)!='illegal edge accepted','negative test3')
    bad=copy.deepcopy(cert)
    r=next(iter(bad['s10_verdict']));bad['s10_verdict'][r]=[0,0]
    actual_win,actual_states=next_player_wins_at_s10(int(r,16))
    require(actual_win and actual_states!=bad['s10_verdict'][r][0],'negative test4 terminal alteration not detected')
    return 4

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default='s7_win_four_certificate.json');ap.add_argument('--workers',type=int,default=4);ap.add_argument('--structure-only',action='store_true');args=ap.parse_args()
    cert=json.loads(Path(args.certificate).read_text());counts=verify_structure(cert);print('STRUCTURE PASS S8,S9,S10:',counts,flush=True)
    print('NEGATIVE STRUCTURE TESTS:',negative_tests(cert),flush=True)
    if not args.structure_only:
        total=verify_terminal(cert,args.workers)
        print('TERMINAL PASS:',counts[-1],'WIN leaves, states=',total,flush=True)
        print(f'CONCLUSION: {len(cert["roots"])} S7 WIN; S6 WIN; empty board UNKNOWN',flush=True)
