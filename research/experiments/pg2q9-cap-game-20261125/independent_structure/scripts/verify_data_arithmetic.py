"""Task 2 + Task 4: arithmetic decomposition and repo data-file cross-checks.

Reads (read-only):
  ../output/census_pg2q9.txt
  ../output/conic_layer.json
Writes nothing outside independent_structure.
"""
import json
import itertools
import math
import time
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"
DATA = ROOT.parent / "output"


def load_conics():
    return [int(ln) for ln in (OUT / "conics.txt").read_text().splitlines()]


def parse_census(path):
    rows = {}
    header = None
    for ln in path.read_text().splitlines():
        tok = ln.split()
        if tok[0] == "N":
            header = tok
        elif tok[0] == "SIZE":
            rows[int(tok[1])] = (int(tok[2]), int(tok[3]))
    return header, rows


def main():
    t0 = time.time()
    conics = load_conics()
    nconic = len(conics)
    print(f"independently enumerated conics: {nconic}")
    print(f"q^5-q^2 for q=9: {9**5 - 9**2}")

    C = {k: math.comb(10, k) for k in range(11)}
    print("\n[Task 2] conic k-subsets 58968*C(10,k):")
    for k in range(11):
        print(f"  k={k:2d}: C(10,k)={C[k]:4d}  n_conic={nconic * C[k]}")

    print("\n[Task 2] claimed decomposition arithmetic:")
    checks = []
    # k=5
    checks.append(("k5 conic", 58968 * C[5], 14859936))
    checks.append(("k5 nonconic", 0, 0))
    checks.append(("k5 maximal", 0, 0))
    # k=6
    checks.append(("k6 conic", 58968 * C[6], 12383280))
    checks.append(("k6 nonconic", 52009776 - 12383280, 39626496))
    checks.append(("k6 total sum", 12383280 + 39626496, 52009776))
    checks.append(("k6 maximal <= nonconic", 707616 <= 39626496, True))
    # k=7
    checks.append(("k7 conic", 58968 * C[7], 7076160))
    checks.append(("k7 total sum", 7076160 + 2021760 + 42456960, 51554880))
    checks.append(("k7 nonconic nonmax", 51554880 - 7076160 - 2021760, 42456960))
    # k=8
    checks.append(("k8 conic", 58968 * C[8], 2653560))
    checks.append(("k8 total sum", 2653560 + 5307120, 7960680))
    checks.append(("k8 nonconic (=maximal)", 7960680 - 2653560, 5307120))
    # k=9
    checks.append(("k9 total", 58968 * C[9], 589680))
    checks.append(("k9 maximal", 0, 0))
    # k=10
    checks.append(("k10 total", 58968 * C[10], 58968))
    checks.append(("k10 maximal", 58968, 58968))
    for name, got, want in checks:
        print(f"  {name:28s} {got} == {want}: {got == want}")
    all_arith = all(got == want for _n, got, want in checks)
    print(f"ARITHMETIC: {'PASS' if all_arith else 'FAIL'}")

    # ---- census ----
    header, census = parse_census(DATA / "census_pg2q9.txt")
    print("\n[Task 4] census_pg2q9.txt:", header)
    tot = {k: v[0] for k, v in census.items()}
    mx = {k: v[1] for k, v in census.items()}
    for k in sorted(census):
        print(f"  SIZE {k:2d}: total={tot[k]:10d} maximal={mx[k]:9d}")

    total_caps = sum(tot.values())
    print(f"  sum of all SIZE totals: {total_caps}")
    safe = int(header[header.index("SAFE") + 1])
    print(f"  header SAFE value: {safe}; equality: {total_caps == safe}")
    # independently known totals for k<=5
    known = {0: 1, 1: 91, 2: 4095, 3: 110565, 4: 1769040, 5: 14859936}
    # independently count 3-arcs
    n3 = 0
    for a, b, c in itertools.combinations(range(91), 3):
        if pg.PAIR_LINE[(a, b)] != pg.PAIR_LINE[(a, c)]:
            n3 += 1
    print(f"  independently counted 3-arcs: {n3}")
    known[3] = n3
    for k, v in known.items():
        print(f"  census SIZE {k} total {tot.get(k)} vs independent {v}: "
              f"{tot.get(k) == v}")

    # maximal-table cross checks
    print("\n[Task 4] maximal counts:")
    print(f"  maximal 6-caps 707616 (census): {mx[6]}")
    print(f"  maximal 7-caps 2021760 (census): {mx[7]}")
    print(f"  maximal 8-caps 5307120 (census): {mx[8]}")
    print(f"  maximal 9-caps 0 (census): {mx[9]}")
    print(f"  maximal 10-caps 58968 (census): {mx[10]}")
    print(f"  conic count 58968 (independent): {nconic}")

    # consistency: 9-caps all conic via 8-cap extensions conditional on
    # census maximal-8 / non-conic reasoning:
    conic8 = nconic * C[8]
    max8 = mx[8]
    tot8 = tot[8]
    print(f"\n  8-caps: conic {conic8} + max8 {max8} = {conic8 + max8} "
          f"(census total {tot8})")
    print(f"  every 8-cap either conic or maximal: "
          f"{conic8 + max8 == tot8 and tot[8] - max8 == conic8}")
    print(f"  9-cap total from conic 8-caps: conic8*2/9 = {conic8 * 2 // 9} "
          f"(census {tot[9]}); integer: {conic8 * 2 % 9 == 0}")
    print(f"  conic 9-subsets: {nconic * C[9]} = census 9-cap total: "
          f"{nconic * C[9] == tot[9]}")

    # conic_layer.json
    cl = json.loads((DATA / "conic_layer.json").read_text())
    print("\n[Task 4] conic_layer.json:")
    print(f"  conics field: {cl['conics']} == independent {nconic}: "
          f"{cl['conics'] == nconic}")
    print(f"  pgl2_9_order: {cl['pgl2_9_order']} == 9*(9^2-1)=720: "
          f"{cl['pgl2_9_order'] == 9 * (9**2 - 1)}")
    rep = cl["conic"]
    repm = 0
    for p in rep:
        repm |= 1 << p
    print(f"  representative {rep}: conic in independent list: {repm in set(conics)}")
    print(f"  representative is a 10-cap: {pg.is_cap(rep)} "
          f"size={len(rep)}")
    ok = True
    for k in map(str, range(3, 10)):
        entry = cl["k"][k]
        want = nconic * C[int(k)]
        rowsum = sum(o["orbit_size"] for o in entry["orbits"])
        good = entry["caps"] == want and rowsum == want
        ok &= good
        print(f"  k={k}: caps={entry['caps']} 58968*C(10,{k})={want} "
              f"orbit_sum={rowsum} match={good}")
    print(f"  conic_layer counts match 58968*C(10,k) for k=3..9: {ok}")

    # ---- PGL(3,9) and ordered 4-arcs ----
    pgl3 = 9**3 * (9**3 - 1) * (9**2 - 1)
    ordered4 = 91 * 90 * 81 * 64
    print("\n[Task 5] |PGL(3,9)|:")
    print(f"  9^3*(9^3-1)*(9^2-1) = {pgl3}")
    print(f"  ordered 4-arcs 91*90*81*64 = {ordered4}")
    print(f"  equality: {pgl3 == ordered4}")
    print(f"  unordered 4-arcs = {ordered4 // 24} (brute force: 1769040)")
    print(f"  non-conic non-maximal 7-caps (census totals minus conic minus max): "
          f"{tot[7] - nconic * C[7] - mx[7]}")
    print(f"  8-caps maximal count * 8 = {mx[8] * 8}")
    print(f"  equality with |PGL|: {mx[8] * 8 == pgl3}")

    print(f"\ntotal time {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
