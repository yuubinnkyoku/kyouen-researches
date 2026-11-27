"""Extra direct checks:
  (1) verify the explicit witness words from orbit_bfs.py (C -> phi(A),
      B -> phi^2(A)) really compose to group elements with the claimed action;
  (2) verify phi maps the WHOLE saved PGL orbit A -> C, C -> B, B -> A
      (686,784 caps each), giving the cyclic permutation of the three classes
      without relying on the normaliser argument.

Run:  python verify_extra.py
"""

import json
import os
import sys

import pg2q8 as G

HERE = os.path.dirname(os.path.abspath(__file__))

A = (10, 47, 49, 55, 61, 64)
B = (17, 27, 30, 44, 52, 70)
C = (8, 48, 50, 51, 58, 61)

ph = G.phi_perm()
ph2 = G.perm_mul(ph, ph)
PHI_A = tuple(sorted(ph[p] for p in A))
PHI2_A = tuple(sorted(ph2[p] for p in A))

CAPS = {"A": A, "B": B, "C": C, "phi(A)": PHI_A, "phi^2(A)": PHI2_A}

def load_orbit(name):
    path = os.path.join(HERE, f"orbit_{name}.bin")
    out = set()
    with open(path, "rb") as f:
        while True:
            buf = f.read(6)
            if len(buf) < 6:
                break
            out.add(int.from_bytes(buf, "little"))
    return out

def pack(points):
    return int.from_bytes(bytes(points), "little")

def unpack(key):
    return key.to_bytes(6, "little")

def phi_cap_key(key):
    pts = list(unpack(key))
    return pack(sorted(ph[p] for p in pts))

def main():
    checks = []

    def check(name, passed, detail=""):
        checks.append((name, bool(passed), detail))
        print(("PASS " if passed else "FAIL ") + name + (("  [" + str(detail) + "]") if detail != "" else ""))

    print("== replay of explicit witness words ==")
    mats = G.pgl_generators()
    gens = [G.mat_perm(M) for M in mats]
    names = ["E01", "E02", "E10", "E12", "E20", "E21", "D1", "D2"]
    with open(os.path.join(HERE, "orbit_results.json"), "r", encoding="utf-8") as f:
        orb = json.load(f)

    def replay(orbit_name, target_cap, target_name):
        w = orb["orbits"][orbit_name]["witness"][target_name]
        seq = w["word_generators"]
        perm = G.IDENT
        for gi in seq:
            perm = G.perm_mul(perm, gens[gi])
        start = CAPS[orbit_name]
        image = tuple(sorted(perm[p] for p in start))
        ok = image == tuple(sorted(target_cap))
        # the composed map must be a collineation (word in PGL generators)
        line_set = {frozenset(L) for L in G.generated_lines()}
        coll = all(frozenset(perm[p] for p in L) in line_set for L in G.generated_lines())
        print(f"  {orbit_name} -> {target_name}: word {seq} = {[names[i] for i in seq]}")
        print(f"    image {image}  target {tuple(sorted(target_cap))}  collineation={coll}")
        return ok and coll, seq

    ok1, seq1 = replay("C", PHI_A, "to_phi(A)")
    ok2, seq2 = replay("B", PHI2_A, "to_phi^2(A)")
    check("witness word C -> phi(A) verified", ok1, f"{len(seq1)} letters")
    check("witness word B -> phi^2(A) verified", ok2, f"{len(seq2)} letters")

    print("\n== phi maps whole PGL orbits cyclically ==")
    O = {name: load_orbit(name) for name in ("A", "B", "C")}
    for name in ("A", "B", "C"):
        check(f"orbit_{name}.bin has 686,784 caps", len(O[name]) == 686_784, len(O[name]))
    # expected: phi(orbit A) = orbit C, phi(orbit C) = orbit B, phi(orbit B) = orbit A
    mapping = [("A", "C"), ("C", "B"), ("B", "A")]
    for src, dst in mapping:
        bad = 0
        for key in O[src]:
            if phi_cap_key(key) not in O[dst]:
                bad += 1
        # phi is injective and both sets have the same size => equality
        check(f"phi(orbit {src}) = orbit {dst} (all 686,784 caps)", bad == 0,
              f"{bad} images outside")
    # phi(A) and phi^2(A) are literally in the expected orbits
    check("phi(A) is a cap of orbit_C.bin", pack(PHI_A) in O["C"])
    check("phi^2(A) is a cap of orbit_B.bin", pack(PHI2_A) in O["B"])
    check("A is not in orbit_B.bin or orbit_C.bin",
          pack(A) not in O["B"] and pack(A) not in O["C"])
    check("B is not in orbit_C.bin", pack(B) not in O["C"])

    out = {"checks": [{"name": n, "passed": p, "detail": d} for n, p, d in checks],
           "witness_C_to_phiA": seq1, "witness_B_to_phi2A": seq2,
           "n_checks": len(checks), "n_failed": sum(1 for c in checks if not c[1])}
    with open(os.path.join(HERE, "extra_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(f"\n{len(checks)} checks, {out['n_failed']} failed")
    return 0 if out["n_failed"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
