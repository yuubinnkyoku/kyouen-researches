#!/usr/bin/env python3
"""Independent, cache-free 11x11 S9 WIN / S8 WIN terminal certificate check."""
import json
import sys
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'n11-s8-to-s7-lift238-20261020'))
from terminal_geometry import canonical, children, legal, next_player_wins_at_s10, points, safe

def need(ok, msg):
    if not ok: raise ValueError(msg)

def mask(s):
    need(isinstance(s,str) and len(s)==32 and all(c in '0123456789abcdef' for c in s),'invalid mask')
    x=int(s,16)
    need(x < (1<<121),'out of board')
    return x

def verify(path=P/'certificate.json', cpp=P/'s10-cpp.tsv'):
    d=json.loads(Path(path).read_text())
    need(d.get('format')=='n11-s9-win-terminal13-v1' and d.get('board')==11 and
         d.get('perspective')=='fixed-original-first' and d.get('empty_winner')=='UNKNOWN','format/polarity')
    s9=mask(d['s9_win'])
    need(s9.bit_count()==9 and canonical(s9)==s9 and safe(s9),'invalid S9')
    ls=d['s10_win_children']; ps=d['s8_win_parents']
    need(len(ls)==len(set(ls))==13 and {mask(s) for s in ls}==children(s9),'incomplete S10 children')
    need(len(ps)==len(set(ps))==9 and {mask(s) for s in ps}==
         {canonical(s9^(1<<i)) for i in points(s9)},'incomplete S8 parents')
    for p in map(mask,ps):
        need(p.bit_count()==8 and safe(p) and s9 in children(p),'illegal S8->S9 edge')
    stats={}
    for s in ls:
        m=mask(s)
        need(m.bit_count()==10 and canonical(m)==m and safe(m),'invalid S10')
        win,n=next_player_wins_at_s10(m)
        need(win,f'LOSS S10 contradicts WIN: {s}')
        stats[s]=(n,len(legal(m)))
    rows={}
    for line in Path(cpp).read_text().splitlines():
        h,v,n,k=line.split()
        need(h not in rows and v=='WIN','duplicate or LOSS C++ row')
        rows[h]=(int(n),int(k))
    need(rows==stats,'C++/Python independent terminal mismatch')
    print('PASS: 13 S10 WIN leaves, S9 WIN, 9 S8 WIN parents; 557 terminal states; empty 11x11 UNKNOWN')
    need(sum(n for n,k in stats.values())==557,'unexpected state count')

if __name__=='__main__':
    verify(Path(sys.argv[1]) if len(sys.argv)>1 else P/'certificate.json')
