#!/usr/bin/env python3
\"\"\"Coverage audit for the (4,24,5) class-split sweep (m=24 lane, declaration d92c8f51).

Parses output/records24.jsonl and audits the complete-cover decomposition of the
row-deficient maximal safe configuration space on 4x24 (q=5):

- 9 canonical deficiency classes mod row mirror V (0<->3, 1<->2):
  singletons {0},{1} (exact count k in 0..3; k>=1 split by minpos p in 0..11,
  sound H-split min(x1, 22-x_k) <= 11) and 7 multi classes.
- Multi classes c01/c02/c03/c12 run direct; if direct is INDET they are decided
  by the krow-pinned decomposition (multigen24.sh): 16 exact-count pieces
  (k0,k1) in {0..3}^2 on the two deficient rows; a k0>=1 piece may itself be
  decided by its 12 minpos sub-pieces p=0..11 (sound H-split on the first
  deficient row). k0=0 pieces: direct only.
- Any k2/k3 bucket that is INDET direct may be decided by the complete x2
  second-stone split (sat4.js; k=3: B in p+1..22, k=2: B in p+1..23).
  c0k3p0/p1/p2 are decided by design via x2 (direct attempts are honest
  negatives recorded for calibration).

All decided instance keys must be UNSAT. Any SAT is a witness (claim switches to
the witness form). Any INDET/genfail without a completing sub-split leaves the
bucket undecided.
Output JSON: per-bucket states, undecided set, and the claim string.
\"\"\"
import json, sys
from collections import defaultdict

M, PMAX = 24, 11
MULTI = ['01', '02', '03', '12', '012', '013', '0123']
MULTI_KROW = ['01', '02', '03', '12']  # krow decomposition available

def expected_x2(bucket):
    k, p = int(bucket[3]), int(bucket[5:])
    bmax = (M - 2) if k >= 3 else (M - 1)
    return [f'{bucket}b{B}' for B in range(p + 1, bmax + 1)]

def expected_krow(mm):
    subs = []
    for k0 in range(0, 4):
        for k1 in range(0, 4):
            subs.append((f'c{mm}r{k0}s{k1}', k0))
    return subs

def main(path):
    recs = defaultdict(list)
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        res = r.get('kissat', {}).get('result') or ('GENFAIL' if r.get('genfail') else '?')
        recs[r['key']].append({'result': res, 'cap': r.get('cap'),
                               'conflicts': r.get('kissat', {}).get('conflicts')})
    def final(key):
        if key not in recs:
            return None
        for e in recs[key]:
            if e['result'] == 'SAT':
                return 'SAT'
        if any(e['result'] == 'UNSAT' for e in recs[key]):
            return 'UNSAT'
        if any(e['result'] == 'INDET' for e in recs[key]):
            return 'INDET'
        return 'GENFAIL' if any(e['result'] == 'GENFAIL' for e in recs[key]) else None
    coverage, undecided, sat_keys = {}, [], []
    def mark(key, st):
        coverage[key] = st
        if st != 'UNSAT':
            undecided.append(key)
            if st == 'SAT':
                sat_keys.append(key)
    for y in (0, 1):
        for k in range(0, 4):
            keys = [f'c{y}k0'] if k == 0 else [f'c{y}k{k}p{p}' for p in range(PMAX + 1)]
            for key in keys:
                st = final(key)
                if st == 'UNSAT':
                    mark(key, st)
                    continue
                # INDET (or unseen) k>=2 bucket: allow complete x2 split
                if k >= 2 and st != 'SAT':
                    subs = expected_x2(key)
                    sub_states = [final(s) for s in subs]
                    if sub_states and all(s == 'UNSAT' for s in sub_states):
                        mark(key, f'UNSAT_BY_X2 ({len(subs)} sub-buckets all UNSAT)')
                        continue
                    miss = [s for s, sst in zip(subs, sub_states) if sst != 'UNSAT']
                    if miss:
                        mark(key, f'x2 partial: {len(miss)}/{len(subs)} undecided')
                    else:
                        mark(key, st or 'UNSEEN')
                    continue
                mark(key, st or 'UNSEEN')
    for mm in MULTI:
        key = 'c' + mm
        st = final(key)
        if st in ('UNSAT', 'SAT'):
            mark(key, st or 'UNSEEN')
            continue
        if mm in MULTI_KROW:
            ok, bad, npieces, witness = True, [], 0, False
            for pk, k0 in expected_krow(mm):
                npieces += 1
                pst = final(pk)
                if pst == 'SAT':
                    witness = True
                    break
                if pst == 'UNSAT':
                    continue
                if k0 >= 1 and all(final(f'{pk}p{P}') == 'UNSAT' for P in range(0, PMAX + 1)):
                    continue
                bad.append(pk)
            if witness:
                mark(key, 'SAT')
            elif not bad:
                mark(key, f'UNSAT_BY_KROW ({npieces} exact-count pieces all UNSAT)')
            else:
                coverage[key] = f'krow partial: {len(bad)}/{npieces} undecided'
                undecided.append(key)
        else:
            mark(key, st or 'UNSEEN')
    out = {'m': M, 'records': sum(len(v) for v in recs.values()), 'keys_seen': len(recs),
           'coverage': coverage, 'undecided': undecided, 'sat_keys': sat_keys,
           'claim_complete': not undecided and not sat_keys}
    if out['claim_complete']:
        out['claim'] = ('witness-free width set {21,22,23,24}; '
                        'M_{4,5} = 21 or >= 26 (M=22,23,24 impossible; upper bound 140 unchanged)')
    elif sat_keys:
        out['claim'] = 'witness found at (4,24,5): M_{4,5} in [24,140] (pending witness verification)'
    else:
        out['claim'] = 'incomplete: %d buckets undecided' % len(undecided)
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'output/records24.jsonl')
