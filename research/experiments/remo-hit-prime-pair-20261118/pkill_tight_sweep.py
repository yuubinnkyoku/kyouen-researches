import time, json, sys
import hitpair_core as hp

def prime_factors(n):
    fs=set(); m=n; p=2
    while p*p<=m:
        while m%p==0: fs.add(p); m//=p
        p+=1
    if m>1: fs.add(m)
    return sorted(fs)

def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    i=3
    while i*i<=n:
        if n%i==0: return False
        i+=2
    return True

def spectrum(M, Kmax):
    hits = hp.census_hits(M, Kmax)
    main_hits=[K for K in hits if K!=M+1]
    live = sorted(set(K % (M+1) for K in main_hits))
    dead=set()
    for p in prime_factors(M+1):
        for kap in range(0,M-1):
            if kap % p == p-1: dead.add(kap)
    exp=[k for k in range(0,M-1) if k not in dead]
    first={}
    for K in main_hits:
        kap=K%(M+1)
        if kap not in first: first[kap]=K
    return {'M':M,'Kmax':Kmax,'hits_total':len(hits),'special_hit':(M+1 in hits),
            'main_hits':len(main_hits),'live':live,'expected':exp,
            'tight':live==exp,'missing':sorted(set(exp)-set(live)),
            'extra':sorted(set(live)-set(exp)),'first':first,
            'max_first_K':max(first.values()) if first else None}

if __name__=='__main__':
    mode=sys.argv[1]
    out={}
    if mode=='tier1':
        t0=time.time()
        Ms=[m for m in range(29,201) if isprime(m)]
        for M in Ms:
            r=spectrum(M,200000)
            out[M]=r
            if not r['tight']:
                print('TIGHTNESS FAIL M=%d missing=%s extra=%s' % (M,r['missing'],r['extra']), flush=True)
        nfail=sum(1 for r in out.values() if not r['tight'])
        print('tier1 done: %d primes M in [29,200], K<=2e5, tight fails=%d, %.1fs' % (len(out),nfail,time.time()-t0))
        json.dump(out,open('output/pkill_tight_tier1.json','w'),indent=1,sort_keys=True)
    elif mode=='tier2':
        t0=time.time()
        Ms=[int(x) for x in sys.argv[2].split(',')]
        Kmax=int(sys.argv[3])
        for M in Ms:
            t1=time.time()
            r=spectrum(M,Kmax)
            out[M]=r
            print('M=%d Kmax=%d tight=%s hits=%d live=%d/%d maxfirst=%s %.1fs' % (
                M,Kmax,r['tight'],r['hits_total'],len(r['live']),len(r['expected']),
                r['max_first_K'],time.time()-t1), flush=True)
            json.dump(out,open('output/pkill_tight_tier2.json','w'),indent=1,sort_keys=True)
        print('tier2 done %.1fs' % (time.time()-t0))
