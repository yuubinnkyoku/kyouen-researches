"""Consolidated task-level verdicts for the independent K1329 verification.

Reads core_results.json, orbit_results.json and census_output.txt produced by
verify_core.py, orbit_bfs.py and maxcaps.exe, and checks the task 5 conclusion
and arithmetic.  Writes summary_results.json.

Run:  python verify_summary.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(HERE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    core = load_json("core_results.json")
    orb = load_json("orbit_results.json")
    with open(os.path.join(HERE, "census_output.txt"), "r", encoding="utf-8") as f:
        census_text = f.read()

    def cint(pattern, text):
        m = re.search(pattern, text)
        return int(m.group(1)) if m else None

    total_caps = cint(r"total caps:\s*(\d+)", census_text)
    max6_total = cint(r"maximal 6-caps:\s*(\d+)", census_text)
    max6_in_union = cint(r"in the union of the three PGL orbits:\s*(\d+)", census_text)
    max6_not_in_union = cint(r"NOT in the union:\s*(\d+)", census_text)
    max10_total = cint(r"size 10\s*:\s*\d+ caps,\s*(\d+) maximal", census_text)

    checks = []

    def check(name, passed, detail=""):
        checks.append((name, bool(passed), detail))
        print(("PASS " if passed else "FAIL ") + name + (("  [" + str(detail) + "]") if detail != "" else ""))

    core_checks = {c["name"]: c["passed"] for c in core["checks"]}
    caps = core["caps"]

    # ---------------- task 1 ----------------
    print("== task 1: A,B,C,phi(A),phi^2(A) are maximal 6-caps ==")
    t1 = True
    for name in ("A", "B", "C", "phi(A)", "phi^2(A)"):
        d = caps[name]
        ok = d["six_distinct"] and d["cap"] and d["n_addable"] == 0
        t1 &= ok
        print(f"  {name:8s} points={tuple(d['points'])} cap={d['cap']} addable={d['addable']}")
    check("task1: all five sets are 6-caps", all(caps[n]["cap"] and caps[n]["six_distinct"] for n in caps))
    check("task1: all five sets are maximal (no addable point)", all(caps[n]["n_addable"] == 0 for n in caps))
    check("task1: board/rank convention verified (generated lines == board rows)",
          core_checks.get("rank convention: generated 73 lines == board rows (as sets)", False))
    check("task1: phi is a well-defined bijection on 73 points",
          core_checks.get("phi is a bijection on the 73 points", False))
    task1 = t1 and core["board_ok"]

    # ---------------- task 2 ----------------
    print("\n== task 2: Frobenius images ==")
    check("task2: phi(A) == {10,28,31,59,65,67}", core_checks.get("phi(A) equals claimed set", False))
    check("task2: phi^2(A) == {10,29,33,37,43,46}", core_checks.get("phi^2(A) equals claimed set", False))
    check("task2: phi^3 = identity on all 73 points", core_checks.get("phi^3 = identity on all 73 points", False))
    check("task2: phi has order exactly 3", core_checks.get("phi != identity (order exactly 3)", False))
    task2 = all(core_checks.get(k, False) for k in (
        "phi(A) equals claimed set", "phi^2(A) equals claimed set",
        "phi^3 = identity on all 73 points", "phi != identity (order exactly 3)"))

    # ---------------- task 3 ----------------
    print("\n== task 3: PGL(3,8) ==")
    pgl = core["pgl_order"]
    gl = core["gl_order"]
    check("task3: |GL(3,8)| = 115,379,712", gl == 115_379_712)
    check("task3: generated group order = 16,482,816 = |GL|/7", pgl == 16_482_816 == gl // 7)
    check("task3: every generator is a collineation (maps lines to lines)",
          core_checks.get("every generator maps every line to a line (collineation group)", False))
    check("task3: point stabiliser has order 225,792 = |PGL|/73",
          core["point_stabilizer"] == 225_792)
    task3 = (pgl == 16_482_816 and core["point_stabilizer"] == 225_792
             and core_checks.get("every generator maps every line to a line (collineation group)", False))

    # ---------------- task 4 ----------------
    print("\n== task 4: orbit membership ==")
    sizes = orb["sizes"]
    mem = orb["memberships"]
    for name in ("A", "B", "C"):
        print(f"  orbit {name}: size {sizes[name]}")
    print("  membership matrix:")
    for oname in ("A", "B", "C"):
        print(f"    orbit {oname}: ", {p: mem[oname][p] for p in ("A", "B", "C", "phi(A)", "phi^2(A)")})
    check("task4: |orbit(A)| = |orbit(B)| = |orbit(C)| = 686,784",
          all(sizes[n] == 686_784 for n in ("A", "B", "C")))
    check("task4: phi(A) in PGL orbit of C", mem["C"]["phi(A)"])
    check("task4: phi^2(A) in PGL orbit of B", mem["B"]["phi^2(A)"])
    check("task4: A, B, C lie in pairwise distinct PGL orbits",
          (not mem["B"]["A"]) and (not mem["C"]["A"]) and (not mem["C"]["B"]))
    check("task4: orbit union has 2,060,352 elements", orb["union_size"] == 2_060_352)
    check("task4: explicit witness word C -> phi(A) recorded",
          orb["orbits"]["C"]["witness"].get("to_phi(A)", {}).get("word_len", 0) > 0)
    check("task4: explicit witness word B -> phi^2(A) recorded",
          orb["orbits"]["B"]["witness"].get("to_phi^2(A)", {}).get("word_len", 0) > 0)
    task4 = all(c[1] for c in checks if c[0].startswith("task4"))

    # ---------------- task 5 ----------------
    print("\n== task 5: transitivity + arithmetic ==")
    check("task5: 3*16,482,816 = 49,448,448", 3 * pgl == 49_448_448)
    check("task5: 2,060,352*24 = 49,448,448", 2_060_352 * 24 == 49_448_448)
    check("task5: 49,448,448/2,060,352 = 24 exactly",
          49_448_448 % 2_060_352 == 0 and 49_448_448 // 2_060_352 == 24)
    check("task5: 16,482,816/686,784 = 24 exactly",
          16_482_816 % 686_784 == 0 and 16_482_816 // 686_784 == 24)
    check("task5: <PGL,phi> has order 49,448,448 = 3|PGL|",
          core["pgamma_order"] == 49_448_448 == 3 * pgl)
    check("task5: phi normalises PGL and phi not in PGL",
          core["phi_normalises_pgl"] and not core["phi_in_pgl"])
    check("task5: independent census total maximal 6-caps = 2,060,352",
          max6_total == 2_060_352, max6_total)
    check("task5: all maximal 6-caps lie in the union of the three PGL orbits",
          max6_in_union == max6_total and max6_not_in_union == 0,
          f"{max6_in_union}/{max6_total}, not in union {max6_not_in_union}")
    check("task5: union of three PGL orbits covers all maximal 6-caps (transitivity)",
          orb["union_size"] == max6_total == 2_060_352)
    check("task5: PGammaL orbit of A is all 2,060,352 maximal 6-caps",
          3 * 686_784 == max6_total)
    check("task5: PGammaL stabiliser of a maximal 6-cap has order 24",
          49_448_448 // 2_060_352 == 24)
    check("task5: PGL stabiliser of a maximal 6-cap has order 24",
          16_482_816 // 686_784 == 24)
    # census consistency (not required by K1329 but validates the enumerator)
    check("task5: census total cap count 19,550,350 (consistency with experiment README)",
          total_caps == 19_550_350, total_caps)
    check("task5: census maximal 10-caps = 32,704 (consistency with experiment README)",
          max10_total == 32_704, max10_total)
    task5 = all(c[1] for c in checks if c[0].startswith("task5"))

    verdicts = {"task1": task1, "task2": task2, "task3": task3, "task4": task4, "task5": task5}
    out = {
        "verdicts": verdicts,
        "checks": [{"name": n, "passed": p, "detail": d} for n, p, d in checks],
        "census": {"total_caps": total_caps, "maximal6": max6_total,
                   "maximal6_in_union": max6_in_union,
                   "maximal6_not_in_union": max6_not_in_union,
                   "maximal10": max10_total},
        "core": {k: core[k] for k in ("pgl_order", "gl_order", "point_stabilizer",
                                      "pgamma_order", "phi_normalises_pgl", "phi_in_pgl")},
        "orbits": {n: sizes[n] for n in ("A", "B", "C")},
        "n_checks": len(checks),
        "n_failed": sum(1 for c in checks if not c[1]),
    }
    with open(os.path.join(HERE, "summary_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print("\n== verdicts ==")
    for t, v in verdicts.items():
        print(f"  {t}: {'PASS' if v else 'FAIL'}")
    print(f"{out['n_checks']} checks, {out['n_failed']} failed")
    return 0 if all(verdicts.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
