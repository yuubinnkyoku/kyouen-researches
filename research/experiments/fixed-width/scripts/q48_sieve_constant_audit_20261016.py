#!/usr/bin/env python3
"""Independent finite audit for explicit constant of q48 slope sieve denominator."""
from array import array
from math import log, pi
import json

def run(N):
    prime=bytearray(b'\x01')*(N+1)
    prime[:2]=b'\x00\x00'
    for d in range(2,int(N**.5)+1):
        if prime[d]:
            prime[d*d::d]=b'\x00'*((N-d*d)//d+1)
    a=array('d',[0.0])*(N+1)
    a[1]=1.0
    constant=1/(2*pi*pi)
    count=0
    for p in range(7,N+1,4):
        if not prime[p]: continue
        count+=1
        w=4.0/(p-4)
        for n in range(N//p,0,-1):
            if a[n]:a[n*p]+=a[n]*w
        constant*=p*(p-1)**2/((p-4)*(p+1)**2)
    samples=[]
    running=0.0
    stops=set([1000,10000,100000,N])
    for i in range(1,N+1):
        running+=a[i]
        if i in stops:
            samples.append({'z':i,'G':running,'G/log(z)^2':running/log(i)**2})
    return {'N':N,'primes_3mod4_at_least7':count,'constant_truncated_at_N':constant,'samples':samples}

if __name__=='__main__':
    print(json.dumps(run(1000000),indent=2))
