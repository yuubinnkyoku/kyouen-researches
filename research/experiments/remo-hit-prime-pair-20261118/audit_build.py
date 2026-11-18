#!/usr/bin/env python3
"""K0950 audit: engine anchoring of the HIT-ARITH / pair-prime reduction.

All checks deterministic; output/hitpair_audit.json must be byte-identical
across cold runs.  Checks:
  PIN          pinned core + published input sha256 (K0945/K0949 outputs)
  ARITH-GRID   engine sigma_Z vs arith_hit, M in [2,30], K in (M,1500]
               (the K0949 VOCE grid: 43,036 states, 656 engine hits)
  SP-REG       engine vs special-case formula, M in [2,200]
  PAIR-ENGINE  engine vs PAIR-2 / PAIR-3 predicates, u <= 2000
  K0-FAM       engine vs K0-FAMILY formula, M in {5,7,11,13,17}, u<=400
  MSQ          engine vs M-SQ formula (incl. PRIME-M), M in [3,200]
  CENSUS-REPRO HIT-ARITH census at K<=2e5 vs the K0949 CENSPRIME/PARITY
               tables (main-regime counts, M=2 odd-hit locus)
  DEEP3        PAIR-3 deep sweep: exact set == K0945 U_all (u<=1e5),
               bucket equality, extension to u<=1e6
  DEEP2        PAIR-2 deep sweep: u<=66,666 count == 2,024 (K0949 PARITY
               main-regime anchor), extension to u<=333,333
  PKILL        dead kappa residues (prime p | M+1) carry no hits
  SPECTRUM     kappa-residue spectrum of all census hits (K<=2e5)
  UM-DENSITY   kappa=0 family U_M census for M in {2,3,5,7,11,13} with
               doubling density buckets, cross-checked against the deep
               AP-sieve lists for M=2,3 (K0946 next-task-4 data)
  HL-OBS       singular series, HL integrals, observed/predicted ratios,
               effective local exponents (conjecture-level, NOT a proof)
"""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

from composite_core import sigma_Z                     # pinned engine
from sievegen_core import isprime
from hitpair_core import (arith_hit, hit_special, census_hits,
                          k0_family_hit, msq_hit, pair2_hit, pair3_hit,
                          pair_deep, singular_series, hl_integral,
                          set_prime_flags)

RELAY_PUB = {
    "composite_core.py":
        "3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40",
    "sievegen_core.py":
        "a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499",
}
INPUT_PUB = {
    "relay_audit.json":
        "c92cb52f3a02d32a117441f8cbbbc3f5cc0a9a2ff1f5a63f6ca6056a90fc60b6",
    "deep_census.json":
        "3821c19b0828ebdcfc7bc0d830b317e23144106f506df4f1d72e6ee753c1bc1a",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_list(l):
    return hashlib.sha256(json.dumps(l).encode()).hexdigest()


def locate(names):
    for n in names:
        if os.path.exists(n):
            return n
    raise FileNotFoundError(names)


R = {"experiment": "remo-hit-prime-pair-20261118", "checks": {}}
OK_ALL = [True]


def check(name, payload, ok):
    payload = dict(payload)
    payload["ok"] = bool(ok)
    R["checks"][name] = payload
    OK_ALL[0] = OK_ALL[0] and bool(ok)


# ---------------- 1. PIN ----------------
pins = {}
pin_ok = True
for fn, want in RELAY_PUB.items():
    got = sha256_file(os.path.join(HERE, fn))
    pins[fn] = got
    pin_ok = pin_ok and got == want
relay_path = locate([os.path.join("..", "remo-relay-prime-m-20261118",
                                  "output", "relay_audit.json"),
                     os.path.join("..", "..", "relay_audit.json")])
census_path = locate([os.path.join("..", "remo-sigmaz3-fold-20261118",
                                   "output", "deep_census.json"),
                      os.path.join("..", "..", "deep_census.json")])
for p in (relay_path, census_path):
    got = sha256_file(p)
    pins[os.path.basename(p)] = got
    pin_ok = pin_ok and got == INPUT_PUB[os.path.basename(p)]
check("PIN", {"files": pins}, pin_ok)

RELAY = json.load(open(relay_path))
CENSP = RELAY["checks"]["CENSPRIME"]["hits_all_kTeqM"]
PARITY_TOTAL = RELAY["checks"]["PARITY"]["M2_hits_total"]
VOCE_HITS = RELAY["checks"]["VOCE"]["engine_hits"]
DEEPC = json.load(open(census_path))["A"]

# ---------------- 2. ARITH-GRID ----------------
bad = []
hits = 0
per_M = {}
states = 0
for M in range(2, 31):
    hM = 0
    for K in range(M + 1, 1501):
        states += 1
        e = sigma_Z(M, K) == 1
        a = arith_hit(M, K)
        if e != a:
            bad.append([M, K, int(e), int(a)])
        if e:
            hM += 1
    per_M[str(M)] = hM
    hits += hM
check("ARITH-GRID", {
    "domain": "M in [2,30], K in (M,1500]",
    "states": states,
    "mismatches": len(bad),
    "bad_sample": bad[:5],
    "engine_hits": hits,
    "voice_anchor": VOCE_HITS,
    "per_M": per_M,
}, not bad and states == 43036 and hits == VOCE_HITS)

# ---------------- 3. SP-REG ----------------
bad = []
hit_M = []
for M in range(2, 201):
    e = sigma_Z(M, M + 1) == 1
    a = hit_special(M)
    if e != a:
        bad.append(M)
    if a:
        hit_M.append(M)
check("SP-REG", {
    "domain": "M in [2,200]",
    "mismatches": len(bad),
    "bad_M": bad,
    "hit_M": hit_M,
}, not bad)

# ---------------- 4. PAIR-ENGINE ----------------
set_prime_flags(2000000)
bad2 = []
h2 = 0
for u in range(2, 2001):
    e = sigma_Z(2, 3 * u) == 1
    a = pair2_hit(u)
    if e != a:
        bad2.append(u)
    if a:
        h2 += 1
odd_u = [u for u in range(2, 2001) if pair2_hit(u) and u % 2]
bad3 = []
h3 = 0
for u in range(1, 2001):
    e = sigma_Z(3, 4 * u) == 1
    a = pair3_hit(u)
    if e != a:
        bad3.append(u)
    if a:
        h3 += 1
# K0-FAMILY vs pair-predicate consistency for M=2,3 (both engine-anchored
# above; this checks the two proved reductions against each other)
badk = []
for u in range(2, 2001):
    if k0_family_hit(2, u) != pair2_hit(u):
        badk.append(["M2", u])
    if k0_family_hit(3, u) != pair3_hit(u):
        badk.append(["M3", u])
check("PAIR-ENGINE", {
    "M2_u_range": [2, 2000], "M2_mismatches": len(bad2), "M2_bad": bad2[:5],
    "M2_pair_hits": h2, "M2_odd_u_hits": odd_u,
    "M3_u_range": [1, 2000], "M3_mismatches": len(bad3), "M3_bad": bad3[:5],
    "M3_pair_hits": h3,
    "k0_vs_pair_mismatches": len(badk),
}, not bad2 and not bad3 and not odd_u and not badk)

# ---------------- 5. K0-FAM ----------------
bad = []
hits = 0
bad_cross = []
for M in (5, 7, 11, 13, 17):
    for u in range(2, 401):
        K = (M + 1) * u
        e = sigma_Z(M, K) == 1
        a = k0_family_hit(M, u)
        if e != a:
            bad.append([M, u])
        if a:
            hits += 1
        if a != arith_hit(M, K):          # internal consistency
            bad_cross.append([M, u])
check("K0-FAM", {
    "domain": "M in {5,7,11,13,17}, u in [2,400]",
    "engine_mismatches": len(bad), "bad_sample": bad[:5],
    "cross_mismatches": len(bad_cross),
    "formula_hits": hits,
}, not bad and not bad_cross)

# ---------------- 6. MSQ ----------------
bad = []
hit_M = []
for M in range(3, 201):
    e = sigma_Z(M, M * M - 1) == 1
    a = isprime(M) and msq_hit(M)   # PRIME-M is part of the criterion
    if e != a:
        bad.append(M)
    if a:
        hit_M.append(M)
check("MSQ", {
    "domain": "M in [3,200] (composite M included: engine must be 0)",
    "mismatches": len(bad), "bad_M": bad,
    "hit_M": hit_M,
}, not bad)

# ---------------- 7. CENSUS-REPRO (cached for later checks) -------------
KMAX = 200000
HITS = {}
cens = {}
main_counts = {}
repro_ok = True
for M in (2, 3, 5, 7, 11, 13, 17, 19, 23):
    hs = census_hits(M, KMAX)
    HITS[M] = hs
    cens[str(M)] = {"total": len(hs),
                    "special_in": M + 1 in hs,
                    "msq_in": (M * M - 1) in hs,
                    "list_sha256": sha_list(hs),
                    "first10": hs[:10], "last10": hs[-10:]}
    main = len(hs) - (1 if (M + 1) in hs else 0)
    main_counts[str(M)] = main
    if M >= 3:
        repro_ok = repro_ok and main == CENSP[str(M)]
hs2 = HITS[2]
odd_hits_M2 = [K for K in hs2 if K % 2 == 1]
m2_total = len(hs2)
m2_main = m2_total - (1 if 3 in hs2 else 0)
main_sum = sum(main_counts[str(m)] for m in (3, 5, 7, 11, 13, 17, 19, 23))
check("CENSUS-REPRO", {
    "Kmax": KMAX,
    "per_M": cens,
    "main_counts": main_counts,
    "anchor_censprime": CENSP,
    "anchor_sum_23731": main_sum,
    "M2": {"total": m2_total, "main": m2_main,
           "parity_anchor_main": PARITY_TOTAL,
           "odd_hits": odd_hits_M2},
}, repro_ok and m2_main == PARITY_TOTAL and odd_hits_M2 == [3]
   and main_sum == 23731)

# ---------------- 8. DEEP3 ----------------
U_all = DEEPC["U_all"]
deep3 = pair_deep(4, 6, 100000, extra=(2,))
set_ok = deep3 == U_all
buck_pub = DEEPC["U_density_buckets"]
EDGES = [(1, 1000), (1000, 2000), (2000, 4000), (4000, 8000),
         (8000, 16000), (16000, 32000), (32000, 64000), (64000, 100000)]
buck_mine = {}
for lo, hi in EDGES:
    buck_mine["(%d,%d]" % (lo, hi)] = sum(1 for u in deep3 if lo < u <= hi)
buck_ok = all(buck_mine["(%d,%d]" % e] == buck_pub["(%d,%d]" % e]
              for e in EDGES)
deep3x = pair_deep(4, 6, 1000000, extra=(2,))
EDGESX = [(100000, 200000), (200000, 400000), (400000, 600000),
          (600000, 800000), (800000, 1000000)]
buckx = {}
for lo, hi in EDGESX:
    buckx["(%d,%d]" % (lo, hi)] = sum(1 for u in deep3x if lo < u <= hi)
check("DEEP3", {
    "set_equal_upto_1e5": set_ok,
    "count_1e5": len(deep3), "count_1e5_anchor": DEEPC["U_count"],
    "buckets_1e5": buck_mine, "buckets_1e5_anchor": buck_pub,
    "buckets_ok": buck_ok,
    "count_1e6": len(deep3x),
    "buckets_1e6_ext": buckx,
    "first10_1e6": deep3x[:10], "last10_1e6": deep3x[-10:],
    "list_sha256_1e6": sha_list(deep3x),
}, set_ok and buck_ok and len(deep3) == DEEPC["U_count"])

# ---------------- 9. DEEP2 ----------------
deep2 = pair_deep(3, 6, 333333)
n66666 = sum(1 for u in deep2 if u <= 66666)
odd_u2 = [u for u in deep2 if u % 2]
n2e5 = sum(1 for u in deep2 if u <= 200000)
check("DEEP2", {
    "u_max_domain": 333333,
    "count_u_le_66666": n66666,
    "anchor_parity_main": PARITY_TOTAL,
    "count_u_le_200000": n2e5,
    "count_u_le_333333": len(deep2),
    "odd_u_hits": len(odd_u2),
    "first10": deep2[:10], "last10": deep2[-10:],
    "list_sha256": sha_list(deep2),
}, n66666 == PARITY_TOTAL and not odd_u2)

# ---------------- 10. PKILL ----------------
dead = {}
for M in range(3, 62):
    if not isprime(M):
        continue
    ds = set()
    for p in range(2, M + 2):
        if (M + 1) % p == 0 and isprime(p):
            for kap in range(p - 1, M - 1, p):
                if kap <= M - 2:
                    ds.add(kap)
    dead[str(M)] = sorted(ds)
dead_hit = []
for M in (5, 7, 11, 13, 17, 19, 23):
    for K in HITS[M]:
        if (K % (M + 1)) in dead[str(M)]:
            dead_hit.append([M, K])
dead_engine = []
for M in (5, 7, 11, 13, 17, 19, 23, 29):
    for K in range(M + 2, 1201):
        kap = K % (M + 1)
        if kap in dead[str(M)] and sigma_Z(M, K) == 1:
            dead_engine.append([M, K])
check("PKILL", {
    "dead_kappa": dead,
    "census_dead_hits_K_le_2e5": dead_hit,
    "engine_dead_hits_K_le_1200": dead_engine,
}, not dead_hit and not dead_engine)

# ---------------- 11. SPECTRUM ----------------
spec = {}
for M in (2, 3, 5, 7, 11, 13, 17, 19, 23):
    d = {}
    for K in HITS[M]:
        kap = K % (M + 1)
        d[str(kap)] = d.get(str(kap), 0) + 1
    spec[str(M)] = d
check("SPECTRUM", {"Kmax": KMAX, "per_M_kappa_counts": spec}, True)

# ---------------- 12. UM-DENSITY ----------------
UMAX = {2: 33333, 3: 25000, 5: 15000, 7: 12000, 11: 8000, 13: 6000}
BEDGES = [(2, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 128),
          (128, 256), (256, 512), (512, 1024), (1024, 2048),
          (2048, 4096), (4096, 8192)]
um = {}
cross_deep = {}
for M in (2, 3, 5, 7, 11, 13):
    N = UMAX[M]
    fam = [u for u in range(2, N + 1) if k0_family_hit(M, u)]
    buck = {}
    for lo, hi in BEDGES:
        if lo > N:
            break
        cnt = sum(1 for u in fam if lo < u <= min(hi, N))
        buck["(%d,%d]" % (lo, min(hi, N))] = cnt
    um[str(M)] = {"u_max": N, "count": len(fam),
                  "first15": fam[:15], "last10": fam[-10:],
                  "buckets": buck,
                  "list_sha256": sha_list(fam)}
# independent cross-check: divisor-scan family vs AP-sieve deep lists
cross_deep["M2"] = {"k0_count": um["2"]["count"],
                   "deep_count": sum(1 for u in deep2 if 2 <= u <= 33333)}
cross_deep["M3"] = {"k0_count": um["3"]["count"],
                   "deep_count": sum(1 for u in deep3x if 2 <= u <= 25000)}
check("UM-DENSITY", {"families": um, "cross_vs_deep_AP_sieve": cross_deep},
      cross_deep["M2"]["k0_count"] == cross_deep["M2"]["deep_count"]
      and cross_deep["M3"]["k0_count"] == cross_deep["M3"]["deep_count"])

# ---------------- 13. HL-OBS (conjecture-level) ----------------
SS2 = singular_series(3, 6, 100000)
SS3 = singular_series(4, 6, 100000)
hl = {"SS2_3u_6u": SS2, "SS3_4u_6u": SS3,
      "pmax": 100000, "note": "conjecture-level (Hardy-Littlewood)"}
obs3 = {}
for N in (10000, 100000, 1000000):
    cnt = sum(1 for u in deep3x if u <= N) - 1      # drop the u=2 exception
    pred = SS3 * hl_integral(4, 6, N)
    obs3[str(N)] = {"observed": cnt, "predicted": round(pred, 1),
                    "ratio": round(cnt / pred, 4)}
hl["M3"] = obs3
obs2 = {}
for N in (20000, 66666, 200000, 333333):
    cnt = sum(1 for u in deep2 if u <= N)
    pred = SS2 * hl_integral(3, 6, N)
    obs2[str(N)] = {"observed": cnt, "predicted": round(pred, 1),
                    "ratio": round(cnt / pred, 4)}
hl["M2"] = obs2
expo = []
for lo, hi in EDGESX:
    cnt = sum(1 for u in deep3x if lo < u <= hi)
    ueff = (lo * hi) ** 0.5
    d = cnt / (hi - lo)
    expo.append({"bucket": "(%d,%d]" % (lo, hi), "density": round(d, 6),
                 "hl_local_exponent": round(2.0 / math.log(ueff), 4)})
pts = []
for lo, hi in [(1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000),
               (16000, 32000), (32000, 64000), (64000, 100000),
               (100000, 200000), (200000, 400000), (400000, 600000),
               (600000, 800000), (800000, 1000000)]:
    cnt = sum(1 for u in deep3x if lo < u <= hi)
    pts.append((math.log((lo * hi) ** 0.5),
                math.log(cnt / (hi - lo))))
n = len(pts)
sx = sum(p[0] for p in pts)
sy = sum(p[1] for p in pts)
sxx = sum(p[0] * p[0] for p in pts)
sxy = sum(p[0] * p[1] for p in pts)
slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
hl["M3_density_powerlaw_fit_slope_1e3_1e6"] = round(slope, 4)
hl["M3_bucket_local_exponents"] = expo
check("HL-OBS", hl, True)

R["all_ok"] = OK_ALL[0]
out = os.path.join(HERE, "output", "hitpair_audit.json")
with open(out, "w") as f:
    json.dump(R, f, indent=1, sort_keys=False)
    f.write("\n")
print("all_ok =", R["all_ok"])
for k, v in R["checks"].items():
    print("%-12s ok=%s" % (k, v["ok"]))
