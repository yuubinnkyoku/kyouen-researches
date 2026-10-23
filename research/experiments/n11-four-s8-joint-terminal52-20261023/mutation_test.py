from pathlib import Path
from verify_global import read_keys,read_s10,read_prior,read_dual,structural_check
from terminal_geometry import children
H=Path(__file__).resolve().parent
r=read_keys(H/'roots4.keys',8);v=read_s10(H/'s10-all1017.tsv');s=read_keys(H/'selected52.keys',10)
p=read_prior(H/'prior925.tsv');old=read_keys(H/'prior53.keys',10);u=set().union(*(children(x) for x in r));w=read_dual(H/'dual-weights.tsv',u)

def rejected(desc,rv,sv,wv,pv):
    try:structural_check(r,rv,sv,wv,pv,old)
    except ValueError:return
    raise AssertionError('mutation NOT rejected: '+desc)

k=next(iter(s));bad=dict(v);bad[k]=('WIN',v[k][1],v[k][2]);rejected('LOSS changed to WIN',bad,s,w,p)
bad=dict(v);bad.pop(k);rejected('missing candidate',bad,s,w,p)
rejected('missing proof leaf',v,s-{k},w,p)
bad=dict(w);j=next(iter(bad));bad[j]+=1;rejected('modified dual',v,s,bad,p)
bad=dict(p);j=next(iter(set(p)&set(v)));bad[j]='WIN' if v[j][0]=='LOSS' else 'LOSS';rejected('cache conflict',v,s,w,bad)
print('PASS 5 mutation rejection tests')
