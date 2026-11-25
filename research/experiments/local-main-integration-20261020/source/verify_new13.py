import itertools

n=13
ids=[25,28,35,55,84,85,90,99,107,108,119,130,140]
def idx_to_xy(p): return (p % n, p // n)
S=[idx_to_xy(p) for p in ids]
V=set(S)

def det4(pts):
    a=[]
    for x,y in pts:
        a.append([x*x+y*y, x, y, 1])
    def det(m):
        if len(m)==1: return m[0][0]
        if len(m)==2: return m[0][0]*m[1][1]-m[0][1]*m[1][0]
        total=0
        for j in range(len(m)):
            minor=[row[:j]+row[j+1:] for row in m[1:]]
            sign = -1 if j%2 else 1
            total += sign * m[0][j] * det(minor)
        return total
    return det(a)

# safety
bad=[]
for q in itertools.combinations(S,4):
    if det4(q)==0:
        bad.append(q)
print("safety forbidden quads:", len(bad))
if bad:
    print("example", bad[:3])

# maximality
empty=[(x,y) for x in range(n) for y in range(n) if (x,y) not in V]
not_blocked=[]
block_counts=[]
for p in empty:
    cnt=0
    found=False
    for tri in itertools.combinations(S,3):
        if det4(list(tri)+[p])==0:
            found=True
            cnt+=1
    block_counts.append((p,cnt))
    if not found:
        not_blocked.append(p)
print("empty points:", len(empty))
print("unblocked empty points:", len(not_blocked))
if not_blocked:
    print("UNBLOCKED:", not_blocked)
from collections import Counter
c=Counter(cnt for _,cnt in block_counts)
print("block count distribution:", dict(sorted(c.items())))
print("min block count:", min(cnt for _,cnt in block_counts), "max:", max(cnt for _,cnt in block_counts))
print("stones:", len(S), "density:", len(S)/(n*n))