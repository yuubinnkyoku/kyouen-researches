import sys, time, json
import hitpair_core as hp

def _divisors(g):
    """Factor via hp prime list (fast) and return sorted divisors."""
    hp._ensure_primes(int(g ** 0.5) + 2)
    fs = {}
    m = g
    for p in hp._P:
        if p * p > m:
            break
        while m % p == 0:
            fs[p] = fs.get(p, 0) + 1
            m //= p
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    divs = [1]
    for p, e in fs.items():
        divs = [d * p ** i for d in divs for i in range(e + 1)]
    return sorted(divs)

def probe(M, kap, Kmax):
    """All main-regime hits with K <= Kmax in the single residue class
    K = kap (mod M+1), via HIT-ARITH (Y prime + divisor condition)."""
    M1 = M + 1
    hp.set_prime_flags(Kmax + 2)
    hits = []
    killing = {}
    nY = 0
    Y = kap + 1
    while Y <= M + 1:                      # ensure K = Y-1 > M
        Y += M1
    while Y <= Kmax + 1:
        if hp._isp(Y):
            nY += 1
            K = Y - 1
            s = (K - M - 1) // M1
            k0 = M * (s + 1) + kap - 1
            g = M * Y - 1
            kill = [d for d in _divisors(g) if M <= d <= k0]
            if kill:
                killing[kill[0]] = killing.get(kill[0], 0) + 1
            else:
                hits.append(K)
        Y += M1
    return {'M': M, 'kappa': kap, 'Kmax': Kmax, 'prime_Y_candidates': nY,
            'n_hits': len(hits), 'first_hits': hits[:10], 'last_hits': hits[-5:],
            'kill_histogram_top': sorted(killing.items(), key=lambda x: -x[1])[:12],
            'n_distinct_killers': len(killing)}

if __name__ == '__main__':
    targets = [(1367, 682), (1741, 648), (991, 494), (1231, 614), (1723, 860), (1783, 772)]
    out = []
    for (M, kap) in targets:
        t0 = time.time()
        r = probe(M, kap, 10000000)
        r['time_s'] = round(time.time() - t0, 1)
        print('M=%d kap=%d Kmax=1e7 hits=%d first=%s last=%s (%.1fs)' % (
            M, kap, r['n_hits'], r['first_hits'][:3], r['last_hits'][-2:], r['time_s']), flush=True)
        out.append(r)
    json.dump(out, open('output/pkill_probe_deep.json', 'w'), indent=1)
    print('written output/pkill_probe_deep.json')
