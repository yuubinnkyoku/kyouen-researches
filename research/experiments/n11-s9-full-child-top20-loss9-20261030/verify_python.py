#!/usr/bin/env python3
"""Independent exact N11 LOSS9 witness replay (no Node imports or verdict cache)."""
import functools
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = json.loads((HERE / 'certificate.json').read_text())
AUDIT = json.loads((HERE / '../n11-s8-complete-child-audit-20261030/incidence.json').read_text())
XY = [(i % 11, i // 11) for i in range(121)]

def points(board):
    return [i for i in range(121) if (board >> i) & 1]

def canonical(board):
    transforms = (
        lambda x,y:(x,y), lambda x,y:(10-y,x),
        lambda x,y:(10-x,10-y), lambda x,y:(y,10-x),
        lambda x,y:(10-x,y), lambda x,y:(10-y,10-x),
        lambda x,y:(x,10-y), lambda x,y:(y,x))
    return min(sum(1 << (11*tr(*XY[i])[1]+tr(*XY[i])[0])
                   for i in points(board)) for tr in transforms)

def det(a,b,c,d):
    x,y = XY[d]
    r = [(XY[p][0]-x, XY[p][1]-y,
          XY[p][0]**2+XY[p][1]**2-x*x-y*y) for p in (a,b,c)]
    u,v,w = r
    return (u[0]*(v[1]*w[2]-v[2]*w[1])
            -u[1]*(v[0]*w[2]-v[2]*w[0])
            +u[2]*(v[0]*w[1]-v[1]*w[0]))

def legal(board):
    triples = list(itertools.combinations(points(board),3))
    return [i for i in range(121) if not (board >> i) & 1
            and all(det(*t,i) != 0 for t in triples)]

def children(board):
    return sorted({f'{canonical(board | (1 << i)):032x}' for i in legal(board)})

def solve10(h):
    board = int(h,16)
    base = points(board)
    moves = legal(board)
    n = len(moves)
    assert len(base)==10 and n<=30
    bad = []
    for i,j in itertools.combinations(range(n),2):
        if any(det(a,b,moves[i],moves[j])==0
               for a,b in itertools.combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in itertools.combinations(range(n),3):
        mask=(1<<i)|(1<<j)|(1<<k)
        if not any(mask&v==v for v in bad) and any(
                det(a,moves[i],moves[j],moves[k])==0 for a in base):
            bad.append(mask)
    for i,j,k,l in itertools.combinations(range(n),4):
        mask=(1<<i)|(1<<j)|(1<<k)|(1<<l)
        if not any(mask&v==v for v in bad) and det(
                moves[i],moves[j],moves[k],moves[l])==0:
            bad.append(mask)
    bans=[[] for _ in range(n)]
    for mask in bad:
        for i in range(n):
            if mask&(1<<i):
                bans[i].append(mask^(1<<i))
    @functools.lru_cache(None)
    def win(state):
        for i in range(n):
            bit=1<<i
            if state&bit or any(state&v==v for v in bans[i]):
                continue
            if not win(state|bit):
                return True
        return False
    result=win(0)
    return result,win.cache_info().currsize,n

def verify(negative=False):
    assert CERT['format']=='n11-fixed14-s8-full-child-top20-loss9-v1'
    assert CERT['board']==11 and CERT['emptyBoard']=='UNKNOWN'
    rows=CERT['s9LossWitnesses']
    selected=AUDIT['topUnknown9ByPotentialWIN8Coverage']
    assert len(rows)==len(selected)==CERT['s9LossCount']==20
    parents=set()
    states=0
    for row,src in zip(rows,selected):
        h=row['s9']
        assert h==src['h'] and src['missing8Parents']==2
        board=int(h,16)
        assert len(points(board))==9 and canonical(board)==board
        kids=children(board)
        assert len(kids)==src['legal10']
        assert 0<=row['index']<len(kids)
        assert kids[row['index']]==row['s10LossWitness']
        outcome,count,moves=solve10(row['s10LossWitness'])
        assert not outcome and count==row['s10TerminalStates']
        assert moves==row['s10LegalMoves']
        states+=count
        leaf=int(row['s10LossWitness'],16)
        for pt in points(leaf):
            parent=canonical(leaf^(1<<pt))
            assert row['s10LossWitness'] in children(parent)
            parents.add(f'{parent:032x}')
    digest=hashlib.sha256(('\n'.join(sorted(parents))+'\n').encode()).hexdigest()
    assert len(parents)==CERT['s9LossParentClosure']==192
    assert digest==CERT['s9LossParentSha256'] and states==2602
    if negative:
        fake=dict(rows[0],s10LossWitness=rows[1]['s10LossWitness'])
        assert fake['s10LossWitness']!=children(int(fake['s9'],16))[fake['index']]
        fake=dict(rows[0],index=255)
        assert fake['index']>=len(children(int(fake['s9'],16)))
    result={'verified':True,'independentLanguage':'Python','s9Loss':20,
            'terminalStates':states,'loss9ParentClosure':len(parents),
            'emptyBoard':'UNKNOWN'}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    import sys
    verify('--negative' in sys.argv)
