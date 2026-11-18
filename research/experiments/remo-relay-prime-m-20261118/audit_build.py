#!/usr/bin/env python3
"""K0949 audit: RELAY-REDUCE, VALUE-ONE-CHAR, P'-SIMPLIFY, HIT-KT-EQ-M (PRIME-M), PARITY.

Checks (deterministic; cold 2x byte-identical):
  PIN        pinned core sha256
  RELAY      sigma_E(P;alpha,beta)==alpha+1 vs 3-clause relay formula
             (grid P<=24,k<=69,beta>=2 + seeded random P<=200,k<=600)
  VOCE       engine sigma_Z vs full formula (M<=30, K<=1500 + random K<=20000)
  VOCFF      full formula vs simplified v2 formula (M<=40, K<=3000)
  PSIM       P'-simplify identities (kT>M prime: P'=M*Y/kT, beta_d!=0,
             spf(P')<=spf(M); kT==M: P'=Y)  M<=40, s<80
  ONECHAR    hits satisfy sigma_E(M;kappa,M(s+1))==kappa+1 (K0946 anchor)
  PRIMEM     composite M<=16, K<=1500: engine never hits value 1
  CENSCOMP   composite M in {4,6,8,9,10,25,49}, K<=2e5: no all-clause pass
             with kT>M; P'=M*Y/kT identity holds deep; per-M max spf(P')<=spf(M)
  CENSPRIME  prime M<=23, K<=2e5: formula hits all have kT==M, all even (M>=3)
  PARITYM2   M=2, K<=2e5: odd-K hits == {3} only
"""
import sys, os, json, hashlib, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from composite_core import sigma_E, sigma_Z
from sievegen_core import isprime, spf

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def largest_divisor_le(n, bound):
    best = 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            if d <= bound and d > best: best = d
            if n // d <= bound and n // d > best: best = n // d
        d += 1
    if 2 <= n <= bound and n > best: best = n
    return best

def formula_parts(M, K):
    """K0946/previous full characterization: (hit, clause, kT, kT1, Pp)."""
    kap = K % (M + 1)
    s = (K - M - 1) // (M + 1)
    if kap == M - 1 or kap == M: return (False, 'EXCL', 0, 0, 0)
    if s == 0 and kap == 0:
        return (isprime(M) and spf(M + 2) >= M, 'SPECIAL', 0, 0, 0)
    k0 = M * (s + 1) + kap - 1
    Y = (M + 1) * (s + 1) + kap + 1
    T = M * Y
    kT = largest_divisor_le(T, k0)
    if kT == 0: return (False, 'kT0', 0, 0, 0)
    if not isprime(kT): return (False, 'kTcomp', kT, 0, 0)
    kT1 = largest_divisor_le(T - 1, k0)
    if kT1 >= kT: return (False, 'kT1ge', kT, kT1, 0)
    Pd = T // (kT + 1)
    Pp = Pd + Pd // kT + 1
    if spf(Pp) < kT: return (False, 'spf', kT, kT1, Pp)
    return (True, 'HIT', kT, kT1, Pp)

def formula_v2(M, K):
    """Simplified form: hit <=> M prime, kT==M, kT1<M, spf(Y)>=M (main regime)."""
    kap = K % (M + 1)
    s = (K - M - 1) // (M + 1)
    if kap == M - 1 or kap == M: return False
    if s == 0 and kap == 0:
        return isprime(M) and spf(M + 2) >= M
    if not isprime(M): return False
    k0 = M * (s + 1) + kap - 1
    Y = (M + 1) * (s + 1) + kap + 1
    T = M * Y
    if largest_divisor_le(T, k0) != M: return False
    if largest_divisor_le(T - 1, k0) >= M: return False
    return spf(Y) >= M

res = {"experiment": "remo-relay-prime-m-20261118", "checks": {}, "all_ok": None}
def chk(name, ok, **kw):
    res["checks"][name] = dict(ok=bool(ok), **kw)
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {kw}")

chk("PIN", sha256(os.path.join(HERE, "composite_core.py")) ==
    "3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40" and
    sha256(os.path.join(HERE, "sievegen_core.py")) ==
    "a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499")

# RELAY grid
bad = 0; pos = 0; n = 0
for P in range(1, 25):
    for k0 in range(2, 70):
        for beta in range(2, k0 + 1):
            alpha = k0 - beta
            n += 1
            T = P * (k0 + 1) + beta
            kT = largest_divisor_le(T, k0)
            hit = False
            if kT and isprime(kT):
                kT1 = largest_divisor_le(T - 1, k0)
                if kT1 < kT:
                    Pd = T // (kT + 1)
                    if spf(Pd + Pd // kT + 1) >= kT: hit = True
            eng = (sigma_E(P, alpha, beta) == alpha + 1)
            if hit != eng: bad += 1
            if hit: pos += 1
random.seed(777)
badr = 0; nr = 0
for _ in range(4000):
    P = random.randint(1, 200); k0 = random.randint(2, 600); beta = random.randint(2, k0)
    alpha = k0 - beta
    nr += 1
    T = P * (k0 + 1) + beta
    kT = largest_divisor_le(T, k0)
    hit = False
    if kT and isprime(kT):
        kT1 = largest_divisor_le(T - 1, k0)
        if kT1 < kT:
            Pd = T // (kT + 1)
            if spf(Pd + Pd // kT + 1) >= kT: hit = True
    if hit != (sigma_E(P, alpha, beta) == alpha + 1): badr += 1
chk("RELAY", bad == 0 and badr == 0, grid_mismatch=bad, grid_states=n, grid_hits=pos,
    rnd_mismatch=badr, rnd_states=nr)

# VOCE: engine vs full formula
bad = 0; cnt = 0; hits = 0
for M in range(2, 31):
    for K in range(M + 1, 1501):
        cnt += 1
        a = (sigma_Z(M, K) == 1)
        ok = formula_parts(M, K)[0]
        if a != ok: bad += 1
        if a: hits += 1
random.seed(778)
badr = 0; cntr = 0
for _ in range(1500):
    M = random.randint(2, 40); K = random.randint(M + 1, 20000)
    cntr += 1
    if (sigma_Z(M, K) == 1) != formula_parts(M, K)[0]: badr += 1
chk("VOCE", bad == 0 and badr == 0, mismatches=bad, states=cnt, engine_hits=hits,
    rnd_mismatches=badr, rnd_states=cntr)

# VOCFF: full formula vs v2
bad = 0; cnt = 0
for M in range(2, 41):
    for K in range(M + 1, 3001):
        cnt += 1
        if formula_parts(M, K)[0] != formula_v2(M, K): bad += 1
chk("VOCFF", bad == 0, mismatches=bad, states=cnt)

# PSIM: P'-simplify identities
nA = 0; badA = 0; nD = 0; badD = 0
for M in range(2, 41):
    for s in range(0, 80):
        for kap in range(0, M - 1):
            if s == 0 and kap == 0: continue
            if kap > M - 2: continue
            k0 = M * (s + 1) + kap - 1
            Y = (M + 1) * (s + 1) + kap + 1
            T = M * Y
            kT = largest_divisor_le(T, k0)
            Pd = T // (kT + 1)
            Plit = Pd + Pd // kT + 1
            if kT > M and isprime(kT):
                nA += 1
                if Plit != M * (Y // kT): badA += 1
                if T % (kT + 1) == 0: badA += 1
                if spf(Plit) > spf(M): badA += 1
            elif kT == M:
                nD += 1
                if Plit != Y: badD += 1
                if (M + 1) % 1 == 0 and Y % (M + 1) == 0: badD += 1  # (M+1)!|Y must hold in main regime
chk("PSIM", badA == 0 and badD == 0, kTgtM_states=nA, kTgtM_violations=badA,
    kTeqM_states=nD, kTeqM_violations=badD)

# ONECHAR anchor on hits (K<=1500 grid recomputed cheaply via formula; engine on tails)
bad = 0; hits = 0
for M in range(2, 31):
    for K in range(M + 1, 1501):
        if formula_parts(M, K)[0]:
            hits += 1
            kap = K % (M + 1); s = (K - M - 1) // (M + 1)
            if sigma_E(M, kap, M * (s + 1)) != kap + 1: bad += 1
chk("ONECHAR", bad == 0, hits_checked=hits, violations=bad)

# PRIMEM: composite M never hits (engine)
bad = 0; cnt = 0
for M in range(4, 17):
    if isprime(M): continue
    for K in range(M + 1, 1501):
        cnt += 1
        if sigma_Z(M, K) == 1: bad += 1
chk("PRIMEM", bad == 0, violations=bad, composite_states=cnt)

# ---- deep census (fast sieve machinery) ----
LIM = 260000
spfs = [0] * (LIM + 1)
for i in range(2, LIM + 1):
    if spfs[i] == 0:
        for j in range(i, LIM + 1, i):
            if spfs[j] == 0: spfs[j] = i
def factor(n):
    f = {}
    while n > 1:
        p = spfs[n] if n <= LIM else spf(n)
        f[p] = f.get(p, 0) + 1
        n //= p
    return f
def divs_of(f):
    d = [1]
    for p, e in f.items():
        d = [x * p ** i for x in d for i in range(e + 1)]
    return d
def ldiv(divs, bound):
    b = 0
    for x in divs:
        if 2 <= x <= bound and x > b: b = x
    return b

def census(M, Kmax):
    Mf = factor(M)
    smax = (Kmax - M - 1) // (M + 1)
    st = dict(states=0, kTprime_gtM=0, pass_kTgtM=0, hits_kTeqM=0,
              psim_bad=0, max_spf=0, spf_dist={})
    for s in range(0, smax + 1):
        for kap in range(0, M - 1):
            K = (M + 1) * s + M + 1 + kap
            if K > Kmax: break
            if s == 0 and kap == 0: continue
            k0 = M * (s + 1) + kap - 1
            Y = (M + 1) * (s + 1) + kap + 1
            T = M * Y
            f = dict(Mf)
            for p, e in factor(Y).items(): f[p] = f.get(p, 0) + e
            kT = ldiv(divs_of(f), k0)
            st['states'] += 1
            if kT == M and isprime(M):
                kT1 = ldiv(divs_of(factor(T - 1)), k0)
                if kT1 < M and spf(Y) >= M: st['hits_kTeqM'] += 1
                continue
            if kT <= M or not isprime(kT): continue
            st['kTprime_gtM'] += 1
            kT1 = ldiv(divs_of(factor(T - 1)), k0)
            if kT1 >= kT: continue
            Pd = T // (kT + 1); Pp = Pd + Pd // kT + 1
            sf = spf(Pp)
            st['spf_dist'][sf] = st['spf_dist'].get(sf, 0) + 1
            if sf > st['max_spf']: st['max_spf'] = sf
            if Pp != M * (Y // kT): st['psim_bad'] += 1
            if T % (kT + 1) == 0: st['psim_bad'] += 1
            if sf > spf(M): st['psim_bad'] += 1
            if sf >= kT: st['pass_kTgtM'] += 1
    return st

comp_ms = [4, 6, 8, 9, 10, 25, 49]
tot_pass = 0; tot_psimbad = 0; per_m = {}
for M in comp_ms:
    st = census(M, 200000)
    per_m[M] = dict(kTprime_gtM=st['kTprime_gtM'], max_spf=st['max_spf'],
                    spfM=spf(M), hits=st['hits_kTeqM'])
    tot_pass += st['pass_kTgtM']; tot_psimbad += st['psim_bad']
chk("CENSCOMP", tot_pass == 0 and tot_psimbad == 0, composite_M=comp_ms, Kmax=200000,
    all_clause_pass_kTgtM=tot_pass, psim_violations=tot_psimbad, per_M=per_m)

prime_ms = [3, 5, 7, 11, 13, 17, 19, 23]
bad_kT = 0; odd_hits = 0; tot_hits = 0; tot_pass = 0; hit_counts = {}
for M in prime_ms:
    st = census(M, 200000)
    tot_hits += st['hits_kTeqM']; tot_pass += st['pass_kTgtM']
    hit_counts[M] = st['hits_kTeqM']
chk("CENSPRIME", tot_pass == 0, prime_M=prime_ms, Kmax=200000,
    pass_kTgtM=tot_pass, hits_all_kTeqM=hit_counts, total_hits=tot_hits)

# PARITY: prime M>=3 hits all even; M=2 odd hits == {3}
odd3 = []
for M in prime_ms:
    st = census(M, 200000)
    # recompute hit K values' parity
    smax = (200000 - M - 1) // (M + 1)
    for s in range(0, smax + 1):
        for kap in range(0, M - 1):
            K = (M + 1) * s + M + 1 + kap
            if K > 200000: break
            if s == 0 and kap == 0: continue
            if not formula_v2(M, K): continue
            if K % 2 == 1: odd3.append((M, K))
st2 = census(2, 200000)
odd2 = []
smax = (200000 - 3) // 3
for s in range(0, smax + 1):
    K = 3 * s + 3
    if K > 200000: break
    if s == 0:
        if formula_v2(2, K) and K % 2 == 1: odd2.append(K)
        continue
    if formula_v2(2, K) and K % 2 == 1: odd2.append(K)
chk("PARITY", len(odd3) == 0 and odd2 == [3], odd_hits_primeM3=odd3,
    odd_hits_M2=odd2, M2_hits_total=st2['hits_kTeqM'])

res["all_ok"] = all(c["ok"] for c in res["checks"].values())
out = os.path.join(HERE, "output", "relay_audit.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
print("all_ok =", res["all_ok"])
print("audit sha256:", sha256(out))
