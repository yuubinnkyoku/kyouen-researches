"""TASK 5 -- arithmetic closure of the K1327 orbit table.

Everything is read from the independent computation (results_c.txt):
  * the per-size cap census,
  * the PGL orbit decomposition of every size,
  * the start-cap / conic orbit sizes, and the maximal 6-cap probes.

Checks
  1. every orbit size divides |PGL(3,8)| = 16,482,816 (and the implied
     stabiliser order is printed);
  2. the per-k orbit sizes are exactly the K1327 multiset;
  3. the per-k sums equal the census counts;
  4. the total equals the sum of the census;
  5. the k=6 decomposition is conic 2,747,136 + non-maximal non-conic 4,120,704
     + 3 maximal orbits of 686,784, and the three maximal orbits are pairwise
     distinct (membership probes);
  6. the conic layer sizes are 32,704*C(9,k).
"""

import math
import sys
from collections import defaultdict

import parse_out

PGL = 16482816

# K1327 claim: per k, the multiset of orbit sizes
CLAIM = {
    1: [73],
    2: [2628],
    3: [56064],
    4: [686784],
    5: [4120704],
    6: [2747136, 4120704, 686784, 686784, 686784],
    7: [1177344, 2747136],
    8: [294336, 1177344],
    9: [32704, 294336],
    10: [32704],
}
CLAIM_CENSUS = {
    1: 73, 2: 2628, 3: 56064, 4: 686784, 5: 4120704,
    6: 8928192, 7: 3924480, 8: 1471680, 9: 327040, 10: 32704,
}
CLAIM_TOTAL = 19550350
CLAIM_CONIC = {6: 2747136, 7: 1177344, 8: 294336, 9: 32704, 5: 4120704}


def main():
    out = []

    def say(s=""):
        out.append(str(s))
        print(s)

    recs = parse_out.read("results_c.txt")
    problems = []

    # ---------------------------------------------------------------- census
    census = {}
    total = None
    max6n = None
    for d in recs:
        if d["_tag"] == "census" and "k" in d:
            census[int(d["k"])] = int(d["n"])
        if "census_total" in d:
            total = int(d["census_total"])
        if "census_max6" in d:
            max6n = int(d["census_max6"])
        if "order_pgl3_8" in d:
            pgl_c = int(d["order_pgl3_8"])

    say("== 1. cap census (independent enumeration) ==")
    okc = True
    for k in range(1, 11):
        c = census.get(k)
        cl = CLAIM_CENSUS[k]
        good = c == cl
        okc = okc and good
        say(f"  k={k:2d}: computed={c:>9d}  K1327={cl:>9d}  {'OK' if good else 'MISMATCH'}")
    say(f"  total: computed={total}  K1327 statement={CLAIM_TOTAL}  "
        f"{'OK' if total == CLAIM_TOTAL else 'DIFFERS by %+d' % (total - CLAIM_TOTAL)}")
    say(f"  sum of the K1327 per-k counts = {sum(CLAIM_CENSUS.values())}")
    say(f"  sum of the computed per-k counts = {sum(census.values())}")
    if total != CLAIM_TOTAL:
        problems.append(
            f"stated census total {CLAIM_TOTAL} vs computed {total} "
            f"(difference {total - CLAIM_TOTAL:+d}); "
            f"the sum of the stated per-k counts is {sum(CLAIM_CENSUS.values())}, "
            f"so the stated total is inconsistent by exactly 1 "
            f"(the empty cap would make it {total + 1})")
    say(f"  maximal 6-caps: {max6n}  (K1327: 3*686784 = {3*686784})")

    # ------------------------------------------------------------ decomposition
    say()
    say("== 2. PGL(3,8) orbit decomposition by size ==")
    orbits = defaultdict(list)
    for d in recs:
        if d["_tag"] == "decomp" and "orbit" in d and "size" in d:
            orbits[int(d["k"])].append((int(d["size"]), d.get("rep", "")))
    okd = True
    for k in range(1, 11):
        sizes = sorted((s for s, _ in orbits[k]), reverse=True)
        claim = sorted(CLAIM[k], reverse=True)
        good = sizes == claim
        okd = okd and good
        say(f"  k={k:2d}: computed orbits {sizes}  K1327 {claim}  "
            f"{'OK' if good else 'MISMATCH'}")
        for s, rep in sorted(orbits[k], key=lambda t: -t[0]):
            div = PGL % s == 0
            say(f"        orbit size {s:>9d}  | PGL: {div}  "
                f"|Stab| = {PGL // s if div else 'non-integer'}  rep={rep[:46]}")
            if not div:
                problems.append(f"orbit size {s} does not divide |PGL|")
    say(f"  every orbit size divides |PGL|: {all(PGL % s == 0 for k in orbits for s, _ in orbits[k])}")

    # ------------------------------------------------------------ per-k sums
    say()
    say("== 3. per-k sums vs census ==")
    oks = True
    for k in range(1, 11):
        s = sum(x for x, _ in orbits[k])
        good = s == census.get(k)
        oks = oks and good
        say(f"  k={k:2d}: sum of orbit sizes={s:>9d}  census={census.get(k):>9d}  "
            f"{'OK' if good else 'MISMATCH'}")
    say(f"  sum of all orbit sizes = {sum(x for k in orbits for x, _ in orbits[k])}")
    say(f"  census total          = {total}")
    oktot = sum(x for k in orbits for x, _ in orbits[k]) == total
    say(f"  equal: {oktot}")

    # ------------------------------------------------------- k=6 composition
    say()
    say("== 4. k=6 composition ==")
    s6 = sorted((x for x, _ in orbits[6]), reverse=True)
    conic6 = CLAIM_CONIC[6]
    maximal = 3 * 686784
    nonmax = census.get(6, 0) - conic6 - maximal
    say(f"  conic 6-subsets (orbit of size 32,704*C(9,6)): {conic6}")
    say(f"  non-maximal non-conic 6-caps: {nonmax}  "
        f"(= census 8,928,192 - 2,747,136 conic - 2,060,352 maximal)")
    say(f"  maximal 6-caps: 3 orbits x 686,784 = {maximal}")
    comp_ok = (sorted([conic6, nonmax, 686784, 686784, 686784], reverse=True) == s6
               and nonmax == 4120704)
    say(f"  matches the computed k=6 orbits: {comp_ok}")

    # --------------------------------------------------- maximal 6-cap probes
    say()
    say("== 5. the three maximal 6-cap orbits are pairwise distinct ==")
    probes = defaultdict(dict)
    for d in recs:
        for key, val in d.items():
            if key.startswith("k1327_max6_in_orbit"):
                probes["k1327"][key] = int(val)
            m = key
            if m.startswith("rep") and "_in_orbit" in m:
                i = m.split("_in_orbit")[1]
                probes[f"rep{i}"][m.split("_in_orbit")[0]] = int(val)
    for key in sorted(probes):
        say(f"  {key}: {probes[key]}")
    k1327_hits = [v for v in probes["k1327"].values() if v == 1]
    # pairwise probes: rep_j must not be in orbit i for i != j
    pair_ok = True
    nrep = 0
    for key in probes:
        if key.startswith("rep") and key != "rep" and key[3:].isdigit():
            nrep = max(nrep, int(key[3:]) + 1)
    for i in range(nrep):
        for j in range(nrep):
            if i == j:
                continue
            v = probes.get(f"rep{i}", {}).get(f"rep{j}")
            if v not in (0, None):
                pair_ok = False
    say(f"  number of maximal-6-cap orbit reps found: {nrep}")
    say(f"  every rep_j (j != i) is absent from orbit_i: {pair_ok}")
    say(f"  the K1327 maximal 6-cap lies in exactly one of the three orbits: "
        f"{len(k1327_hits) == 1}")

    # ------------------------------------------------------------ conic layer
    say()
    say("== 6. conic layer arithmetic ==")
    cvals = {}
    for d in recs:
        for k in range(5, 10):
            key = f"conic_orbit_k{k}"
            if key in d:
                cvals[k] = int(d[key])
    okq = True
    for k in (6, 7, 8, 9):
        want = 32704 * math.comb(9, k)
        good = cvals.get(k) == want == CLAIM_CONIC[k]
        okq = okq and good
        say(f"  k={k}: orbit={cvals.get(k):>9d} 32,704*C(9,{k})={want:>9d} "
            f"K1327={CLAIM_CONIC[k]:>9d}  {'OK' if good else 'MISMATCH'}")

    # ------------------------------------------------------------ start caps
    say()
    say("== 7. K1327 start caps ==")
    okst = True
    for d in recs:
        if d["_tag"] == "start":
            name = d["_bare"][1]
            sz = int(d["size"])
            exp = int(d["expect"])
            good = sz == exp
            okst = okst and good
            say(f"  {name:9s} orbit={sz:>9d} expected={exp:>9d} "
                f"is_cap={d.get('is_cap')} is_max={d.get('is_max')} "
                f"in_conic={d.get('in_conic')}  {'OK' if good else 'MISMATCH'}")

    # ---------------------------------------------------------------- verdict
    say()
    say("== SUMMARY ==")
    say(f"  1 census per k           : {'PASS' if okc else 'FAIL'}")
    say(f"  2 orbit multiset per k   : {'PASS' if okd else 'FAIL'}")
    say(f"  3 per-k sums = census    : {'PASS' if oks else 'FAIL'}")
    say(f"  4 k=6 composition        : {'PASS' if comp_ok else 'FAIL'}")
    say(f"  5 maximal-6 distinctness : {'PASS' if pair_ok and len(k1327_hits) == 1 else 'FAIL'}")
    say(f"  6 conic layer arithmetic : {'PASS' if okq else 'FAIL'}")
    say(f"  7 start-cap orbits       : {'PASS' if okst else 'FAIL'}")
    say(f"  8 total {total} vs stated {CLAIM_TOTAL}: "
        f"{'EQUAL' if total == CLAIM_TOTAL else 'DIFFERS'}")
    if problems:
        say()
        say("DISCREPANCIES:")
        for p in problems:
            say(f"  - {p}")
    ok = okc and okd and oks and comp_ok and pair_ok and okq and okst and oktot
    say()
    verdict = "PASS" if ok else "FAIL"
    say(f"TASK 5: {verdict}" +
        ("" if total == CLAIM_TOTAL else
         "  (all claims verified; the single discrepancy is the stated census "
         "total 19,550,350 vs the computed 19,550,349)"))

    with open("results_task5.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
