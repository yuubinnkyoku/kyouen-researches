#!/usr/bin/env python3
"""Independent 12-base period and p^2 check for p<1,000,000."""
from collections import Counter
from math import isqrt
A=(2,4,6,8,10,12,14,16,18,20,24,32)
C={32:1,24:-30,20:140,18:135,16:-1215,14:2205,12:-1977,10:780,8:250,6:-495,4:255,2:-49}
def factors(n):
 out=[];d=2
 while d*d<=n:
  if n%d==0:
   out.append(d)
   while n%d==0:n//=d
  d+=1 if d==2 else 2
 if n>1:out.append(n)
 return out
def order(p):
 v=p-1
 for q in factors(v):
  while v%q==0 and all(pow(a,v//q,p)==1 for a in A):v//=q
 return v
def value(d,m):return sum(c*pow(a,d,m) for a,c in C.items())*pow(120,-1,m)%m
def main():
 N=1000000; sieve=bytearray(N)
 for p in range(2,isqrt(N-1)+1):
  if not sieve[p]:sieve[p*p:N:p]=b'\1'*len(range(p*p,N,p))
 hist=Counter()
 for p in range(37,N):
  if sieve[p]:continue
  L=order(p);hist[(p-1)//L]+=1
  assert any(pow(a,L,p*p)!=1 for a in (2,3,5,7)),p
 assert hist==Counter({1:73196,2:4717,3:433,4:106,5:25,7:1,8:6,9:1,10:2}),hist
 for p in (37,127,311,659,1021,18311,128831,515231,8218681):
  L=order(p)
  for t in (1,2):
   m=p**t;T=L*p**(t-1)
   assert all(value(d+T,m)==value(d,m) for d in range(5,17))
   for q in factors(T):assert any(value(d+T//q,m)!=value(d,m) for d in range(5,17))
  print('direct periods OK',p,L)
 print('PASS: 78487 primes and selected direct tests')
if __name__=='__main__':main()
