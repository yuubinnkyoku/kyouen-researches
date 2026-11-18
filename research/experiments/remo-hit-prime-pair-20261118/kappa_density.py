import json, sys, time
import hitpair_core as hp
from pkill_tight_sweep import isprime, prime_factors

lo, hi, kmax, outfile = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
out = {}
try:
    out = json.load(open(outfile))
except Exception:
    pass
Ms = [m for m in range(lo, hi+1) if isprime(m) and str(m) not in out]
t0 = time.time()
for M in Ms:
    hits = hp.census_hits(M, kmax)
    main = [K for K in hits if K != M+1]
    cnt = {}
    for K in main:
        cnt[K % (M+1)] = cnt.get(K % (M+1), 0) + 1
    dead = set()
    for p in prime_factors(M+1):
        for kap in range(0, M-1):
            if kap % p == p-1: dead.add(kap)
    exp = [k for k in range(0, M-1) if k not in dead]
    missing = [k for k in exp if k not in cnt]
    minlive = min(cnt.values()) if cnt else None
    out[M] = {'M': M, 'Kmax': kmax, 'main_hits': len(main), 'kappa_counts': {str(k): v for k, v in sorted(cnt.items())},
              'expected_live': exp, 'missing_live_with_zero_hits': missing,
              'min_kappa_count': minlive, 'argmin_kappa': [k for k in sorted(cnt) if cnt[k] == minlive][:8]}
    if missing:
        print('ZERO-HIT LIVE KAPPA M=%d: %s' % (M, missing), flush=True)
    json.dump(out, open(outfile, 'w'), indent=1, sort_keys=True)
print('done %d M in %.1fs' % (len(out), time.time()-t0), flush=True)
