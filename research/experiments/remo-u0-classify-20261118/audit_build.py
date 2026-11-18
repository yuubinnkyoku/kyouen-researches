#!/usr/bin/env python3
"""K0948 audit: U0-CLASSIFY and corollaries (uniform E(P;n,0) zero locus).

Checks (all deterministic; run cold twice, byte-identical output required):
  PIN    pinned core sha256
  U0     direct engine vs U0-CLASSIFY formula  (P<=60, n<=400)
  SIEVE  engine zero vs divisor-sieve of T=P(n+1) (independent arithmetic path)
  U0N    U0-NEVER: sigma_E(M+1; Mt-1, 0) != 0  (M,t in [2,60])
  FIRST  FIRST-NEVER: P>=2, n>=P  => sigma_E(P;n,0) != 0
  P1     P=1 census (n<=60): zeros exactly at n+1 prime
  ZSET   zero-set equality {n: sigma=0} == {p-1: p prime <= min(spf(P), NMAX+1)}
"""
import sys, os, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from composite_core import sigma_E
from sievegen_core import isprime, spf

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

res = {"experiment": "remo-u0-classify-20261118", "checks": {}, "all_ok": None}

def chk(name, ok, **kw):
    res["checks"][name] = dict(ok=bool(ok), **kw)
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {kw}")

# PIN
p1 = sha256(os.path.join(HERE, "composite_core.py"))
p2 = sha256(os.path.join(HERE, "sievegen_core.py"))
chk("PIN", p1 == "3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40"
    and p2 == "a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499",
    composite_sha=p1[:16], sievegen_sha=p2[:16])

PMAX, NMAX = 60, 400
zeros = 0; bad_u0 = 0; bad_sieve = 0
for P in range(1, PMAX + 1):
    for n in range(1, NMAX + 1):   # n=0 is the degenerate empty circle (sigma=0 vacuously)
        s = sigma_E(P, n, 0)
        z = (s == 0)
        f = isprime(n + 1) and (P == 1 or spf(P) >= n + 1)
        if z != f: bad_u0 += 1
        if z: zeros += 1
        # independent divisor-sieve path: dies <=> exists k in [2,n] dividing P(n+1)
        T = P * (n + 1)
        dies = any(k <= n and T % k == 0 for k in range(2, n + 1))
        if dies != (not z): bad_sieve += 1
chk("U0", bad_u0 == 0, mismatches=bad_u0, zeros=zeros, states=PMAX * (NMAX + 1))
chk("SIEVE", bad_sieve == 0, mismatches=bad_sieve)

bad_u0n = 0; cnt = 0
for M in range(2, 61):
    for t in range(2, 61):
        cnt += 1
        if sigma_E(M + 1, M * t - 1, 0) == 0: bad_u0n += 1
chk("U0N", bad_u0n == 0, violations=bad_u0n, states=cnt)

bad_first = 0; cnt = 0
for P in range(2, PMAX + 1):
    for n in range(P, NMAX + 1):
        cnt += 1
        if sigma_E(P, n, 0) == 0: bad_first += 1
chk("FIRST", bad_first == 0, violations=bad_first, states=cnt)

p1z = [n for n in range(1, 61) if sigma_E(1, n, 0) == 0]
p1f = [n for n in range(1, 61) if isprime(n + 1)]
chk("P1", p1z == p1f, zeros=p1z)

bad_zs = 0
for P in range(2, PMAX + 1):
    actual = sorted(n for n in range(1, NMAX + 1) if sigma_E(P, n, 0) == 0)
    lim = min(spf(P), NMAX + 1)
    expect = sorted(p - 1 for p in range(2, lim + 1) if isprime(p))
    if actual != expect: bad_zs += 1
chk("ZSET", bad_zs == 0, mismatches=bad_zs, primes_P=PMAX - 1)

res["all_ok"] = all(c["ok"] for c in res["checks"].values())
out = os.path.join(HERE, "output", "u0_audit.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
print("all_ok =", res["all_ok"])
print("audit sha256:", sha256(out))
