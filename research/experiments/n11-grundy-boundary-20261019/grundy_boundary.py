#!/usr/bin/env python3
"""Exact Grundy census of the S10 boundary of 18 proved S8 LOSS roots.

No saved S10 verdicts, certificates, DAG, solver, or optimizer are consulted.
Python 3.10+ standard library. A shard is selected by the sorted canonical
S10 board index modulo 4. Each S10 is solved to terminal positions by mex.
S9 and S8 values are then obtained by exhaustive legal-child propagation.
"""
import argparse, collections, hashlib, itertools, json, pathlib, time
from functools import lru_cache
N=11
ROOTS_HEX='''
10841000800010090000
10841000800210010000
10841008200004010000
10841208000004010000
2141001001000000080100
2141001001008000000100
40a8401000100000100000
20010841000800010010000
108010841000000010010000
810001001001010000140000
8000010841000800010010000
8000010841200000004010000
40000010849000000004010000
80000010841000800010010000
100100000001042100000000090
100100000001042100000004400
100100000001242100000000040
100100002001042100000000008
'''.split()
ROOTS=tuple(int(s,16) for s in ROOTS_HEX)

def pts(mask):
    while mask:
        bit=mask&-mask
        yield bit.bit_length()-1
        mask-=bit

def concyclic(a,b,c,d):
    ax,ay=a%11-d%11,a//11-d//11
    bx,by=b%11-d%11,b//11-d//11
    cx,cy=c%11-d%11,c//11-d//11
    aa=ax*ax+ay*ay;bb=bx*bx+by*by;cc=cx*cx+cy*cy
    return ax*(by*cc-bb*cy)-ay*(bx*cc-bb*cx)+aa*(bx*cy-by*cx)==0

@lru_cache(None)
def legal(board):
    occupied=list(pts(board))
    triples=list(itertools.combinations(occupied,3))
    return tuple(i for i in range(121) if not (board>>i&1)
                 and not any(concyclic(*triple,i) for triple in triples))

D4=[]
for typ in range(8):
    row=[]
    for v in range(121):
        x,y=v%11,v//11
        x,y=((x,y),(10-y,x),(10-x,10-y),(y,10-x),
             (10-x,y),(10-y,10-x),(x,10-y),(y,x))[typ]
        row.append(1<<(11*y+x))
    D4.append(tuple(row))

@lru_cache(None)
def canonical(board):
    pp=tuple(pts(board))
    return min(sum(row[i] for i in pp) for row in D4)

def children(board):
    return {canonical(board | (1<<i)) for i in legal(board)}

def boundary():
    assert len(ROOTS)==len(set(ROOTS))==18
    assert all(r.bit_count()==8 and canonical(r)==r for r in ROOTS)
    s9=set().union(*(children(r) for r in ROOTS))
    s10=set().union(*(children(p) for p in s9))
    assert len(s9)==387 and len(s10)==3044,(len(s9),len(s10))
    return tuple(sorted(s9)),tuple(sorted(s10))

def grundy(board):
    base=list(pts(board));moves=legal(board);n=len(moves)
    bad=[]
    for i,j in itertools.combinations(range(n),2):
        if any(concyclic(a,b,moves[i],moves[j]) for a,b in itertools.combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in itertools.combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&f==f for f in bad):continue
        if any(concyclic(a,moves[i],moves[j],moves[k]) for a in base):bad.append(e)
    for ids in itertools.combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&f==f for f in bad):continue
        if concyclic(*(moves[i] for i in ids)):bad.append(e)
    full=(1<<n)-1
    @lru_cache(None)
    def value(used):
        seen=set();free=full^used
        while free:
            bit=free&-free;free-=bit
            after=used|bit
            if any(after&edge==edge for edge in bad):continue
            seen.add(value(after))
        ans=0
        while ans in seen:ans+=1
        return ans
    g=value(0)
    return g,value.cache_info().currsize

def run_shard(i):
    start=time.perf_counter()
    s9,s10=boundary()
    selected=[p for k,p in enumerate(s10) if k%4==i]
    result={};total=0
    for p in selected:
        g,states=grundy(p)
        result[f'{p:032x}']=[g,states]
        total+=states
    output={'format':'n11-18s8-s10-exact-grundy-shard-v1',
            'shard':i,'shards':4,'count':len(result),'memo_states':total,
            's10':result}
    path=pathlib.Path(__file__).parent/f'shard-{i}.json'
    path.write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    print(f'shard {i}: {len(result)} S10 positions, {total} memo states, '
          f'Grundy {dict(sorted(collections.Counter(v[0] for v in result.values()).items()))}, '
          f'{time.perf_counter()-start:.2f}s, sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}')

def merge():
    start=time.perf_counter();s9,s10=boundary();all_values={};states=0
    for i in range(4):
        data=json.loads((pathlib.Path(__file__).parent/f'shard-{i}.json').read_text())
        assert data['format']=='n11-18s8-s10-exact-grundy-shard-v1' and data['shard']==i and data['shards']==4
        expected={f'{p:032x}' for k,p in enumerate(s10) if k%4==i}
        assert set(data['s10'])==expected and data['count']==len(expected)
        assert data['memo_states']==sum(item[1] for item in data['s10'].values())
        assert all(isinstance(g,int) and 0<=g<=121 and isinstance(st,int) and st>0 for g,st in data['s10'].values())
        assert not (set(data['s10'])&set(all_values))
        all_values.update(data['s10']);states+=data['memo_states']
    assert len(all_values)==3044
    g10={int(k,16):v[0] for k,v in all_values.items()}
    assert collections.Counter(g10.values())[0]==896
    g9={}
    for p in s9:
        childvals={g10[q] for q in children(p)}
        g=0
        while g in childvals:g+=1
        g9[p]=g
    g8={}
    for p in ROOTS:
        childvals={g9[q] for q in children(p)}
        g=0
        while g in childvals:g+=1
        g8[p]=g
    assert len(g9)==387 and len(g8)==18 and set(g8.values())=={0}
    output={'format':'n11-18s8-exact-grundy-census-v1',
            's10_count':len(g10),'s9_count':len(g9),'s8_count':len(g8),
            's10_histogram':dict(sorted(collections.Counter(g10.values()).items())),
            's9_histogram':dict(sorted(collections.Counter(g9.values()).items())),
            's8_histogram':dict(sorted(collections.Counter(g8.values()).items())),
            's10_memo_states_additive':states,
            's9_values':{f'{p:032x}':g for p,g in sorted(g9.items())},
            's8_values':{f'{p:032x}':g for p,g in sorted(g8.items())},
            's10_shard_sha256':{str(i):hashlib.sha256((pathlib.Path(__file__).parent/f'shard-{i}.json').read_bytes()).hexdigest() for i in range(4)},
            'empty_board':'UNKNOWN'}
    path=pathlib.Path(__file__).parent/'summary.json'
    path.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    print('S10',len(g10),output['s10_histogram'],'states',states)
    print('S9',len(g9),output['s9_histogram'])
    print('S8',len(g8),output['s8_histogram'])
    print('elapsed',time.perf_counter()-start,'summary_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
    print('11x11 empty-board outcome UNKNOWN')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--shard',type=int,choices=range(4))
    parser.add_argument('--merge',action='store_true')
    args=parser.parse_args()
    if args.merge:merge()
    elif args.shard is not None:run_shard(args.shard)
    else:parser.error('specify --shard 0..3 or --merge')
