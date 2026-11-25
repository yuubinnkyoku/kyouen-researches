#!/usr/bin/env python3
"""Standalone terminal-only proof of one S8 LOSS on standard 11x11.

Standard 11x11, q=4, complete call, normal play, fixed original-first-player
WIN/LOSS.  All geometry uses exact integer determinants; no search cache is read.
"""
from functools import lru_cache
from itertools import combinations
N=11
def check(condition,message='invalid certificate'):
    if not condition: raise ValueError(message)
def points(m): return [i for i in range(121) if m>>i&1]
def circle(a,b,c,d):
    def vec(p):
        x,y=p%N,p//N
        return (x,y,x*x+y*y)
    z=vec(d)
    u=[x-y for x,y in zip(vec(a),z)]
    v=[x-y for x,y in zip(vec(b),z)]
    w=[x-y for x,y in zip(vec(c),z)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))==0
def safe(m): return all(not circle(*q) for q in combinations(points(m),4))
def legal(m):
    p=points(m); triples=list(combinations(p,3))
    return [x for x in range(121) if not (m>>x&1) and all(not circle(a,b,c,x) for a,b,c in triples)]
def canonical(m):
    best=None
    for t in range(8):
        v=0
        for p in points(m):
            x,y=p%11,p//11
            xx,yy=((x,y),(10-y,x),(10-x,10-y),(y,10-x),(10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]
            v|=1<<(11*yy+xx)
        best=v if best is None else min(best,v)
    return best
def children(m): return {canonical(m|(1<<p)) for p in legal(m)}
def next_player_wins_at_s10(m):
    check(m.bit_count() in (10,11) and safe(m))
    base=points(m); moves=legal(m); n=len(moves)
    check(n<=31,f'terminal bitmask width exceeded: {n}')
    bad=set()
    for i,j in combinations(range(n),2):
        if any(circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.add((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&b==b for b in bad):continue
        if any(circle(a,moves[i],moves[j],moves[k]) for a in base):bad.add(e)
    for ids in combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&b==b for b in bad):continue
        if circle(*(moves[i] for i in ids)):bad.add(e)
    ban_by=[[] for _ in range(n)]
    for e in bad:
        for i in range(n):
            if e>>i&1:ban_by[i].append(e^(1<<i))
    @lru_cache(None)
    def win(state):
        for i in range(n):
            bit=1<<i
            if state&bit or any(state&b==b for b in ban_by[i]):continue
            if not win(state|bit):return True
        return False
    return win(0),win.cache_info().currsize


from pathlib import Path
from hashlib import sha256

def read_positions(path, stone_count):
    raw=Path(path).read_text(encoding='ascii').split()
    check(len(raw)==len(set(raw)), f'duplicate in {path}')
    out=[int(x,16) for x in raw]
    for x in out:
        check(f'{x:032x}' in raw and x.bit_count()==stone_count and x>>121==0, f'invalid bit count in {path}')
        check(safe(x) and canonical(x)==x, f'unsafe/noncanonical position in {path}')
    return out

def verify(roots_path=None, leaves_path=None):
    base=Path(__file__).resolve().parent
    roots=read_positions(roots_path or base/'roots.txt',8)
    leaves=read_positions(leaves_path or base/'leaves.txt',10)
    check(len(roots)==10 and len(leaves)==111)
    leafset=set(leaves)
    obligations=set()
    edges=0
    for root in roots:
        cs=children(root)
        check(cs, f'root has no legal child: {root:032x}')
        obligations.update(cs)
        edges+=len(cs)
    check(len(obligations)==224 and edges==230)
    expected_obligations={int(x,16) for x in (base/'obligations.txt').read_text().split()}
    check(expected_obligations==obligations, 'stored S9 obligations mismatch')
    for child in obligations:
        check(children(child)&leafset, f'uncovered S9 child: {child:032x}')
    unused=set(leaves)
    for child in obligations:unused.difference_update(children(child))
    check(not unused, f'unused leaf(s): {len(unused)}')
    s7={canonical(root^(1<<p)) for root in roots for p in points(root)}
    s6={canonical(parent^(1<<p)) for parent in s7 for p in points(parent)}
    check(len(s7)==76 and len(s6)==249)
    total_states=0
    rows=[]
    for leaf in leaves:
        first_wins, states=next_player_wins_at_s10(leaf)
        check(not first_wins, f'non-LOSS S10 leaf: {leaf:032x}')
        total_states+=states
        rows.append(f'{leaf:032x}\tLOSS\t{states}\t{len(legal(leaf))}')
    out=base/'python-verified-leaves.tsv'
    out.write_text('\n'.join(rows)+'\n',encoding='ascii')
    print(f'PASS: {len(roots)} S8 LOSS, {len(obligations)} distinct S9 obligations ({edges} root-child edges)')
    print(f'PASS: {len(leaves)} S10 terminal LOSS leaves; {total_states} explored states')
    print(f'PASS: {len(s7)} distinct S7 LOSS; {len(s6)} distinct S6 parents')
    print('PASS: leaf table SHA256',sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--roots',type=Path)
    parser.add_argument('--leaves',type=Path)
    args=parser.parse_args()
    verify(args.roots,args.leaves)
