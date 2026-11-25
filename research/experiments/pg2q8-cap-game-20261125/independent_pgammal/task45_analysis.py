"""Tasks 4 and 5: PGammaL(3,8) orbit arithmetic and total counts.

Reads orbits_output.json (produced by task3_orbits.py) and census_output.txt
(produced by the independent C census).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
PGL = 16482816
PGAMMA = 3 * PGL  # 49,448,448

EXPECTED_CENSUS = {0: 1, 1: 73, 2: 2628, 3: 56064, 4: 686784,
                   5: 4120704, 6: 8928192, 7: 3924480, 8: 1471680,
                   9: 327040, 10: 32704}


def load_census():
    counts = {}
    total = None
    nonempty = None
    for line in open(os.path.join(HERE, "census_output.txt"), encoding="utf-8"):
        line = line.strip()
        if line.startswith("caps k="):
            # caps k= 6 : 8928192   maximal: 2060352
            left, right = line.split(":", 1)
            k = int(left.split("=")[1])
            counts[k] = int(right.strip().split()[0])
        elif line.startswith("TOTAL (including empty)"):
            total = int(line.split("=")[1])
        elif line.startswith("TOTAL non-empty"):
            nonempty = int(line.split("=")[1])
    return counts, total, nonempty


def main():
    data = json.load(open(os.path.join(HERE, "orbits_output.json"),
                          encoding="utf-8"))
    census, census_total, census_nonempty = load_census()
    print("PGL =", PGL, " PGammaL = 3*PGL =", PGAMMA)
    print("census:", census, "total", census_total, "non-empty", census_nonempty)
    assert census == EXPECTED_CENSUS
    assert census_total == 19550350 and census_nonempty == 19550349

    # ---- check PGL orbit sizes, disjointness, Frobenius stability ----------
    labels = list(data)
    problems = []
    for lab, rec in data.items():
        if rec["size"] != rec["expected"]:
            problems.append((lab, "size", rec["size"], rec["expected"]))
        # representatives membership: exactly self
        for other, inside in rec["memberships"].items():
            if inside != (other == lab):
                problems.append((lab, "membership", other, inside))
    print("PGL orbit size/disjointness problems:", problems)
    assert not problems

    # maximal 6 triple: exactly three distinct PGL orbits permuted 3-cyclically
    A, B, Cc = "k6-max-A", "k6-max-B", "k6-max-C"
    print("maximal triple sizes:", [data[x]["size"] for x in (A, B, Cc)])
    assert [data[x]["size"] for x in (A, B, Cc)] == [686784] * 3
    # phi(A) in orbit C, phi(C) in orbit B, phi(B) in orbit A
    assert data[Cc][f"phi({A})_in_orbit"] is True, "phi(A) not in orbit C"
    assert data[B][f"phi({Cc})_in_orbit"] is True, "phi(C) not in orbit B"
    assert data[A][f"phi({B})_in_orbit"] is True, "phi(B) not in orbit A"
    assert data[A][f"phi({A})_in_orbit"] is False
    assert data[B][f"phi({B})_in_orbit"] is False
    assert data[Cc][f"phi({Cc})_in_orbit"] is False
    print("maximal triple: A -> C -> B -> A under phi: True")

    # every other representative is phi-stable
    non_stable = [lab for lab, rec in data.items()
                  if lab not in (A, B, Cc) and not rec["phi_in_orbit"]]
    print("non-maximal reps with phi(rep) outside own orbit:", non_stable)
    assert not non_stable

    # ---- per-k sums against independent census ---------------------------
    per_k = {}
    for lab, rec in data.items():
        per_k.setdefault(rec["k"], 0)
        per_k[rec["k"]] += rec["size"]
    print("\nper-k orbit sums vs census:")
    all_ok = True
    for k in range(1, 11):
        ok = per_k.get(k, 0) == census[k]
        all_ok &= ok
        print(f"  k={k:2d}: sum={per_k.get(k, 0):9d}  census={census[k]:9d}  "
              f"{'OK' if ok else 'MISMATCH'}")
    assert all_ok
    total_pgl = sum(per_k.values())
    print("sum of 17 non-empty PGL orbits:", total_pgl,
          "(census non-empty", census_nonempty, ")")
    assert total_pgl == census_nonempty
    print("PGL non-empty orbits:", len(data), "+ empty = ", len(data) + 1)

    # ---- PGammaL orbit decomposition -------------------------------------
    pg_sizes = [1]  # empty cap, fixed by everything
    for lab, rec in data.items():
        if lab == A:
            triple = data[A]["size"] + data[B]["size"] + data[Cc]["size"]
            pg_sizes.append(triple)
        elif lab in (B, Cc):
            continue
        else:
            pg_sizes.append(rec["size"])
    pg_sizes_nonempty = [s for s in pg_sizes if s != 1]
    print("\nPGammaL orbit sizes (including empty):")
    print(pg_sizes)
    print("non-empty PGammaL orbits:", len(pg_sizes_nonempty))
    print("sum non-empty:", sum(pg_sizes_nonempty))
    print("sum including empty:", sum(pg_sizes))
    assert len(pg_sizes_nonempty) == 15
    assert sum(pg_sizes_nonempty) == 19550349
    assert sum(pg_sizes) == 19550350

    print("\n|PGammaL| / size for each PGammaL orbit size:")
    for s in pg_sizes:
        q, r = divmod(PGAMMA, s)
        print(f"  size={s:9d}  quotient={q:8d}  remainder={r}")
        assert r == 0, (s, r)

    # ---- the four pairwise sums quoted in the claim ----------------------
    sums = {
        "k6 conic + nonmax nonconic": 2747136 + 4120704,
        "k7 conic + nonconic": 1177344 + 2747136,
        "k8 conic + nonconic": 294336 + 1177344,
        "k9 conic + nonconic": 32704 + 294336,
    }
    print("\npairwise-sum divisibility checks:")
    for name, s in sums.items():
        q, r = divmod(PGAMMA, s)
        print(f"  {name:32s} sum={s:9d}  |PGammaL| = {q}*{s} + {r}"
              f" -> {'DIVIDES' if r == 0 else 'does not divide'}")
        assert r != 0
        assert s % 5 == 0 and PGAMMA % 5 != 0  # why this is immediate

    # ---- all phi-closed unions inside k=6 --------------------------------
    print("\nk=6 phi-closed unions (sanity):")
    singles = {"conic": 2747136, "nonmax": 4120704}
    triple = 2060352
    candidates = {
        "conic": singles["conic"],
        "nonmax": singles["nonmax"],
        "max triple": triple,
        "conic + max triple": singles["conic"] + triple,
        "nonmax + max triple": singles["nonmax"] + triple,
        "all k=6": singles["conic"] + singles["nonmax"] + triple,
    }
    for name, s in candidates.items():
        q, r = divmod(PGAMMA, s)
        print(f"  {name:22s} size={s:9d}  remainder={r:9d}"
              f"  {'divides' if r == 0 else 'no'}")
    # nonmax+triple happens to divide, but nonmax is phi-stable, so it cannot
    # be merged with the maximal triple; verified above.
    print("  note: nonmax+triple divides |PGammaL| but nonmax is phi-stable")
    print("\nTASKS 4/5 ARITHMETIC CHECKS PASSED")


if __name__ == "__main__":
    main()
