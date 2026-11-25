import math

def factor(n):
    f={}
    d=2
    while d*d<=n:
        while n%d==0:
            f[d]=f.get(d,0)+1
            n//=d
        d+=1 if d==2 else 2
    if n>1:
        f[n]=f.get(n,0)+1
    return f

def odd_repr_brute(m):
    target=2*m
    cnt=0
    r=int(math.isqrt(target))
    for x in range(-r,r+1):
        rem=target-x*x
        if rem<0: continue
        y2=rem
        y=int(math.isqrt(y2))
        if y*y==y2:
            if y==0:
                cnt+=1
            else:
                cnt+=2
    return cnt

def formula(m):
    f=factor(m)
    for q,exp in f.items():
        if q%4==3:
            if exp%2!=0:
                return 0
    prod=1
    for p,exp in f.items():
        if p%4==1:
            prod*=(exp+1)
    return 4*prod

bad=[]
N=500
for m in range(1,N+1,2):
    b=odd_repr_brute(m)
    fr=formula(m)
    if b!=fr:
        bad.append((m,b,fr))
print("N",N,"odd m count",(N+1)//2)
print("mismatches",len(bad))
print("first mismatches",bad[:20])
for m in [1,3,5,9,15,25,45,65,125]:
    print(m, "brute", odd_repr_brute(m), "formula", formula(m))