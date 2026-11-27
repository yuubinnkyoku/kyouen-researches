from itertools import product
q=7; s=3; n=q*q+q+1
pts=[(x,y,1) for y in range(q) for x in range(q)]+[(1,m,0) for m in range(q)]+[(0,1,0)]
lines=[]; seen=set()
for a,b,c in product(range(q),repeat=3):
    if (a,b,c)==(0,0,0): continue
    pl=frozenset(i for i,(x,y,z) in enumerate(pts) if (a*x+b*y+c*z)%q==0)
    if len(pl)!=q+1 or pl in seen: continue
    seen.add(pl); lines.append(pl)
assert len(lines)==n
linemask=[sum(1<<i for i in L) for L in lines]
ptlines=[]
for i in range(n):
    ls=[j for j,L in enumerate(lines) if i in L]; assert len(ls)==q+1; ptlines.append(ls)
def safe_add(S,p):
    for li in ptlines[p]:
        if bin(S & linemask[li]).count('1')>=s: return False
    return True
F_nc=(1<<0)|(1<<1)|(1<<q)
assert not any(F_nc & linemask[j]==F_nc for j in range(n))
F_c_mask=None
for j in range(n):
    lm=linemask[j]; on=[i for i in range(n) if lm>>i&1][:3]
    F_c_mask=sum(1<<i for i in on); break
import json
d=json.load(open('/tmp/q7/combined.json'))
for name,F,exp in [('nc',F_nc,d['layers_noncoll']),('c',F_c_mask,d['layers_coll'])]:
    sizes={3:0}; maxnomove=0
    def rec(S,last,depth):
        sizes[depth]=sizes.get(depth,0)+1
        ext=False
        if depth<7:
            for p in range(last+1,n):
                if S>>p&1: continue
                if not safe_add(S,p): continue
                ext=True
                rec(S|1<<p,p,depth+1)
        else:
            for p in range(last+1,n):
                if S>>p&1: continue
                if safe_add(S,p): ext=True; break
        if not ext: globals()['maxnomove']=globals().get('maxnomove',0)+1
    rec(F,-1,3)
    ok=all(sizes.get(m,0)==exp[str(m)] for m in range(3,8))
    print(f"cone {name}: independent py layer sizes m=3..7:",{m:sizes.get(m,0) for m in range(3,8)},"match:",ok)
    print("   sets with no safe extension found at depth<8:",globals().get('maxnomove',0))
