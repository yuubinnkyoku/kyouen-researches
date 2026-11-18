import time, json, sys
sys.path.insert(0, '.')
import hitpair_core as hp
from pkill_tight_sweep import spectrum, isprime

def main():
    m_lo, m_hi, kmax, outfile = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    Ms = [m for m in range(m_lo, m_hi + 1) if isprime(m)]
    out = {}
    # resume support
    try:
        out = json.load(open(outfile))
        Ms = [m for m in Ms if str(m) not in out]
        print('resume: %d remaining' % len(Ms), flush=True)
    except Exception:
        pass
    t0 = time.time()
    for M in Ms:
        t1 = time.time()
        r = spectrum(M, kmax)
        out[M] = r
        if not r['tight']:
            print('TIGHTNESS FAIL M=%d missing=%s extra=%s' % (M, r['missing'], r['extra']), flush=True)
        print('M=%d tight=%s hits=%d live=%d/%d maxfirst=%s %.1fs (elapsed %.0fs)' % (
            M, r['tight'], r['hits_total'], len(r['live']), len(r['expected']),
            r['max_first_K'], time.time() - t1, time.time() - t0), flush=True)
        json.dump(out, open(outfile, 'w'), indent=1, sort_keys=True)
    print('done %d primes in %.1fs' % (len(out), time.time() - t0), flush=True)

main()
