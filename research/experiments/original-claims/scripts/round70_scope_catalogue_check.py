"""Content-audit checks on the existing n6 maximum and n8 minimal catalogues.
Recomputes requested features, never imports legacy classifications.
Catalogue completeness remains the cited historical enumeration's obligation.
"""
from collections import Counter, defaultdict
from itertools import combinations
import json, math, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/research'))
from kyouen_core import det4

def bits(s, n):
    return [p for p in range(n*n) if s >> p & 1]

def row(p):
    x,y=p
    return (x*x+y*y,x,y,1)

def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def curve(t):
    rr=[row(p) for p in t]
    return tuple((-1 if j%2 else 1)*det3(*[tuple(r[c] for c in range(4) if c!=j) for r in rr]) for j in range(4))

def on(c,p):
    return sum(a*b for a,b in zip(c,row(p)))==0

def perms(n):
    out=[]
    for sw in [0,1]:
        for fx in [0,1]:
            for fy in [0,1]:
                out.append([(n-1-y if fx else y)+n*(n-1-x if fy else x) if sw else
                            (n-1-x if fx else x)+n*(n-1-y if fy else y)
                            for y in range(n) for x in range(n)])
    return out

def image(s,pp,n):
    return sum(1<<pp[p] for p in bits(s,n))

def profile(s,n):
    ps=bits(s,n)
    return tuple(sum(p//n==y for p in ps) for y in range(n)),tuple(sum(p%n==x for p in ps) for x in range(n))

def families(s,n):
    ids=bits(s,n); xy=[(p%n,p//n) for p in ids]
    assert all(det4(*[row(p) for p in t]) for t in combinations(xy,4))
    cc=[(sum(1<<ids[i] for i in ix),curve(tuple(xy[i] for i in ix))) for ix in combinations(range(len(ids)),3)]
    ff={p:[m for m,c in cc if on(c,(p%n,p//n))] for p in range(n*n) if not s>>p&1}
    assert all(ff.values()),'catalogue member not maximal'
    dirs=set(); nc=0
    for t in combinations(xy,3):
        (x,y),(xx,yy),(xxx,yyy)=t
        if (xx-x)*(yyy-y)==(xxx-x)*(yy-y):
            dx,dy=xx-x,yy-y;dd=math.gcd(abs(dx),abs(dy));dx//=dd;dy//=dd
            if dx<0 or dx==0 and dy<0:dx,dy=-dx,-dy
            dirs.add((dx,dy));nc+=1
    return ff,cc,dirs,nc

def rho(ff,s,n):
    ids=bits(s,n)
    for k in range(1,len(ids)+1):
        for dd in combinations(ids,k):
            dm=sum(1<<p for p in dd)
            if any(all(t&dm for t in ts) for ts in ff.values()):return k
    raise AssertionError

def ext_radius(cc,s,n):
    xy=[(p%n,p//n) for p in bits(s,n)]
    a,b=min(x for x,y in xy),max(x for x,y in xy);c,d=min(y for x,y in xy),max(y for x,y in xy)
    for r in range(1,5):
        shell=[(x,y) for y in range(c-r,d+r+1) for x in range(a-r,b+r+1)
               if max(a-x,x-b,c-y,y-d,0)==r]
        free=[p for p in shell if not any(on(cf,p) for m,cf in cc)]
        if free:return r,free
    raise AssertionError('radius beyond checked shells')

def load(path,header=False):
    raw=(ROOT/path).read_bytes();v=list(struct.unpack('<'+'Q'*(len(raw)//8),raw))
    if header:
        assert v[0]==len(v)-1
        v=v[1:]
    assert len(v)==len(set(v))
    return v

def main():
    out={}
    n=8;cat=load('research/experiments/original-claims/output/round4_b371.bin',True);assert len(cat)==408
    pp=perms(n);assert len(set(tuple(x) for x in pp))==8
    po=[min(p[p0] for p in pp) for p0 in range(n*n)];orb=sorted(set(po))
    hist={k:Counter() for k in ['triples','directions','sides','corners','delmin','stabilizer','rho']}
    signatures={};byb=defaultdict(list);witnesses={}
    canon=set()
    for s in cat:
        ff,cc,dirs,nc=families(s,n);ps=bits(s,n)
        sides=sum([any(p%n==0 for p in ps),any(p%n==7 for p in ps),any(p//n==0 for p in ps),any(p//n==7 for p in ps)])
        corners=sum(p in [0,7,56,63] for p in ps)
        dels=[sum(all(t&(1<<a) for t in ts) for ts in ff.values()) for a in ps]
        sig=tuple(sum(po[p]==o for p in ps) for o in orb);signatures[s]=sig
        imgs=[image(s,p,n) for p in pp];canon.add(min(imgs));st=imgs.count(s)
        rr=rho(ff,s,n)
        for k,v in [('triples',nc),('directions',len(dirs)),('sides',sides),('corners',corners),('delmin',min(dels)),('stabilizer',st),('rho',rr)]:hist[k][v]+=1
        for k,yes in [('B372',len(dirs)<2),('B373',sides<2),('B374',corners==0)]:
            if yes and k not in witnesses:witnesses[k]={'S':ps,'directions':sorted(dirs),'sides':sides,'corners':corners}
        se=sum(len(ts)==1 and (p%n in [0,7] or p//n in [0,7]) for p,ts in ff.items())
        si=sum(len(ts)==1 and not(p%n in [0,7] or p//n in [0,7]) for p,ts in ff.items())
        byb[sum(map(len,ff.values()))].append((se,si))
    w=sum(1<<p for p in [0,1,6,20,24,32,34,60]);assert w in signatures
    other=next(s for s in cat if signatures[s]!=signatures[w])
    out['n8']={'count':len(cat),'d4_orbits':len(canon),'hist':hist,'witnesses':witnesses,
        'B375':{'W':bits(w,n),'signature_W':signatures[w],'T':bits(other,n),'signature_T':signatures[other]},
        'B380':{'same_sum_groups_opposite_majorities':[k for k,v in byb.items() if any(a>b for a,b in v) and any(a<b for a,b in v)],
        'groups':{k:dict(Counter(str(x) for x in v)) for k,v in byb.items()}}}
    print('n8 catalogue features checked',flush=True)
    n=6;cat=load('research/experiments/structural-discovery/output/maxsafe_n6_K11.bin');assert len(cat)==464 and all(s.bit_count()==11 for s in cat)
    profiles={s:profile(s,n) for s in cat};swap={s:sum((s^t).bit_count()==2 for t in cat) for s in cat}
    cells=defaultdict(lambda:defaultdict(list));rdirs=defaultdict(list);rstates={};meta={}
    for s in cat:
        ff,cc,dirs,nc=families(s,n);r,free=ext_radius(cc,s,n);rr=rho(ff,s,n);bs=sum(map(len,ff.values()))
        cells[bs][rr].append(swap[s]);rdirs[r].append(len(dirs));meta[s]=(rr,bs)
        rstates.setdefault(r,{'S':bits(s,n),'r':r,'free':free})
    empty=[s for s in cat if 0 in profiles[s][0] or 0 in profiles[s][1]]
    group=defaultdict(list)
    for s in cat:group[profiles[s]].append(s)
    # Identification uses all 464 maxima, not only the profile group.
    point_sets={p:sum(1<<i for i,s in enumerate(cat) if s>>p&1) for p in range(36)}
    def minid(s):
        for k in range(1,12):
            for sub in combinations(bits(s,n),k):
                acc=(1<<len(cat))-1
                for p in sub:acc &= point_sets[p]
                if acc.bit_count()==1:return k
    split=None
    for prof,ss in group.items():
        if len(ss)<2:continue
        kk=[minid(s) for s in ss]
        if len(set(kk))>1:
            split={'profile':prof,'states':[{'S':bits(s,n),'min_id':k} for s,k in zip(ss,kk)]};break
    disjoint=next((ss for ss in group.values() if len(ss)>1 and not any((s^t).bit_count()==4 for s,t in combinations(ss,2))),None)
    out['n6']={'B383':rstates,'B389':{r:{'count':len(v),'sum_three_line_directions':sum(v),'mean':sum(v)/len(v),'hist':Counter(v)} for r,v in rdirs.items()},
       'B365':{bs:{rr:{'count':len(v),'sum_swap_degree':sum(v),'mean':sum(v)/len(v)} for rr,v in cv.items()} for bs,cv in cells.items() if len(cv)>1},
       'B391':sum(any(a==b==0 for a,b in zip(profiles[s][0],profiles[s][0][1:])) or any(a==b==0 for a,b in zip(profiles[s][1],profiles[s][1][1:])) for s in cat),
       'B392':sum(profiles[s][0].count(0)>=2 and profiles[s][1].count(0)>=2 for s in cat),
       'B393':Counter('with_col' if 0 in profiles[s][1] else 'without_col' for s in cat if 0 in profiles[s][0]),
       'B394':Counter(y for s in cat for y,c in enumerate(profiles[s][0]) if c==0),
       'B395':{'empty_n':len(empty),'empty_sum_degree':sum(swap[s] for s in empty),'full_n':len(cat)-len(empty),'full_sum_degree':sum(swap[s] for s in cat if s not in empty)},
       'B396':split,'B399':{'profile':profiles[disjoint[0]],'members':[bits(s,n) for s in disjoint]} if disjoint else None}
    # Legacy "wrong" in residual stats means unequal nimbers, not unequal P/N.
    raw=json.loads((ROOT/'research/experiments/original-claims/output/round3_chunk6_residual.json').read_text(encoding='utf-8'))
    out['residual_stat_boundary']={n:{'rows':len(v['B347']['rows']),'nimber_wrong':sum(r['wrong'] for r in v['B347']['rows']),
        'PN_wrong':sum((r['g_full']==0)!=(r['g2']==0) for r in v['B347']['rows'])} for n,v in raw.items()}
    controlled={}
    for n,v in raw.items():
        ca=defaultdict(lambda:defaultdict(lambda:[0,0]));cb=defaultdict(lambda:defaultdict(lambda:[0,0]))
        assert len(v['B347']['rows'])==len(v['B348']['rows'])
        for a,b in zip(v['B347']['rows'],v['B348']['rows']):
            assert (a['k'],a['nL'])==(b['k'],b['nL'])
            err=int((a['g_full']==0)!=(a['g2']==0))
            key=(a['k'],a['nL'],a['n3']+a['n4'])
            for cells,feat in [(ca,a['cov']),(cb,b['bridged'])]:
                tally=cells[key][feat];tally[0]+=err;tally[1]+=1
        def summarize(cells):
            pairs=[(key,x,y,cells[key][x],cells[key][y]) for key in cells for x in cells[key] for y in cells[key] if x<y]
            up=[p for p in pairs if p[3][0]*p[4][1]<p[4][0]*p[3][1]]
            down=[p for p in pairs if p[3][0]*p[4][1]>p[4][0]*p[3][1]]
            return {'pairs':len(pairs),'up':len(up),'down':len(down),'up_examples':up[:2],'down_examples':down[:2]}
        controlled[n]={'B347':summarize(ca),'B348':summarize(cb)}
    out['controlled_PN_stats']=controlled
    from kyouen_core import board_square
    board=board_square(4);g=board.solve_grundy();adj=[set() for _ in range(16)]
    edges=[(a,b) for a,b in combinations(range(16),2) if g[(1<<a)|(1<<b)]==0]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    td=[(a,b) for a,b in combinations(range(16),2) if len(adj[a]|adj[b])==16]
    assert set(td)<=set(edges)
    pp=perms(4)
    def orbit(pair):return min(image((1<<pair[0])|(1<<pair[1]),p,4) for p in pp)
    out['B312']={'P_pairs':len(edges),'TD_pairs':len(td),'P_orbits':len(set(map(orbit,edges))),
        'TD_orbits':len(set(map(orbit,td))),'TD_intersection_hist':Counter(len(adj[a]&adj[b]) for a,b in td)}
    path=ROOT/'research/experiments/original-claims/output/round70_scope_catalogue_check.json'
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: n6 maximum catalogue and n8 minimal catalogue; exact point/deletion/profile features')
if __name__=='__main__':main()
