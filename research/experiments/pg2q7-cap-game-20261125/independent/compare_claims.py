#!/usr/bin/env python3
"""Compare all independently computed results with the claimed values.

Inputs (all produced by the scripts in this directory):
  board_checks.json
  pg2q7_result.txt, ag2q7_result.txt          (C engine)
  pg2q7_py_enum.json, ag2q7_py_enum.json      (Python enumeration)
  pg2q7_py_grundy.json, ag2q7_py_grundy.json  (Python DP)

Writes comparison.json and prints a PASS/FAIL summary.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CLAIMS = {
    "pg2q7": {
        "n": 57,
        "safe": 2446460,
        "counts": {0: 1, 1: 57, 2: 1596, 3: 26068, 4: 234612,
                   5: 938448, 6: 1094856, 7: 134064, 8: 16758},
        "maximal": {6: 625632, 8: 16758},
        "grundy": {0: 1347823, 1: 1098637},
        "root_g": 0,
        "misere": 1,
    },
    "ag2q7": {
        "n": 49,
        "safe": 1108724,
        "counts": {0: 1, 1: 49, 2: 1176, 3: 16464, 4: 127596,
                   5: 444528, 6: 460992, 7: 51744, 8: 6174},
        "maximal": {6: 271656, 7: 2352, 8: 6174},
        "grundy": {0: 581827, 1: 477505, 2: 49392},
        "root_g": 0,
        "misere": 1,
    },
}


def parse_c(path):
    d = {"chk": {}, "mchk_a": {}, "mchk_b": {}, "sizes": {}, "grundy": {}}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            key = t[0]
            if key == "BOARD":
                d["tag"] = t[1]
            elif key == "N":
                d["n"] = int(t[1])
            elif key == "B":
                d["b"] = int(t[1])
            elif key == "SAFE":
                d["safe"] = int(t[1])
            elif key == "MAXSIZE":
                d["max_size"] = int(t[1])
            elif key == "CHK":
                d["chk"][int(t[1])] = int(t[2])
            elif key == "MCHK_A":
                d["mchk_a"][int(t[1])] = int(t[2])
            elif key == "MCHK_B":
                d["mchk_b"][int(t[1])] = int(t[2])
            elif key == "SIZE":
                sz = int(t[1])
                rec = {"count": int(t[2]), "maxA": int(t[3]),
                       "maxB": int(t[4]), "grundy": {}, "win": 0, "loss": 0}
                i = 5
                while i < len(t):
                    if t[i] == "WIN":
                        rec["win"] = int(t[i + 1])
                        i += 2
                    elif t[i] == "LOSS":
                        rec["loss"] = int(t[i + 1])
                        i += 2
                    else:
                        assert t[i][0] == "G", t[i]
                        rec["grundy"][int(t[i][1:])] = int(t[i + 1])
                        i += 2
                d["sizes"][sz] = rec
            elif key == "GRUNDY":
                d["grundy"][int(t[1])] = int(t[2])
            elif key == "ROOT_G":
                d["root_g"] = int(t[1])
            elif key == "ROOT_WIN":
                d["root_win"] = int(t[1])
            elif key == "PARITY_MISMATCH":
                d["parity_mismatch"] = int(t[1])
            elif key == "MAXA_EQ_MAXB":
                d["maxa_eq_maxb"] = int(t[1])
            elif key == "HAS_ODD_MAXIMAL":
                d["has_odd_maximal"] = int(t[1])
            elif key == "HAS_EVEN_MAXIMAL":
                d["has_even_maximal"] = int(t[1])
            elif key == "SECONDS_ENUM":
                d["seconds_enum"] = float(t[1])
            elif key == "SECONDS_DP":
                d["seconds_dp"] = float(t[1])
    return d


def load_json(name):
    with open(os.path.join(HERE, name), "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    boards = load_json("board_checks.json")
    checks = []

    def add(task, name, expected, got_c, got_py, extra=""):
        ok = (got_c == expected) and (got_py == expected)
        checks.append({
            "task": task, "name": name,
            "expected": expected, "c_engine": got_c,
            "python": got_py, "pass": ok, "note": extra,
        })
        return ok

    def add_cross(task, name, got_c, got_py, extra=""):
        ok = (got_c == got_py)
        checks.append({
            "task": task, "name": name,
            "expected": "C == Python", "c_engine": got_c,
            "python": got_py, "pass": ok, "note": extra,
        })
        return ok

    for tag in ("pg2q7", "ag2q7"):
        claim = CLAIMS[tag]
        c = parse_c(os.path.join(HERE, tag + "_result.txt"))
        pe = load_json(tag + "_py_enum.json")
        pd = load_json(tag + "_py_grundy.json")

        # --- Task 2: safe-set totals and size distribution ---
        add(2, tag + " SAFE total", claim["safe"], c["safe"], pe["safe"])
        for sz in range(9):
            add(2, tag + " count(size=%d)" % sz, claim["counts"][sz],
                c["sizes"][sz]["count"], pe["counts"][sz])

        # Closed-form counts for the small sizes (independent of enumeration).
        # PG: any 2 points; a 3rd point off the joining line; a 4th off the
        # union of the 3 secants (3*8-3=21 points); a 5th off the union of the
        # 6 secants (48-15+4=37 points).  AG analogous with lines of size 7
        # and 3*7-3=18 points on the three secants.
        if tag == "pg2q7":
            formulas = {
                2: math.comb(57, 2),
                3: 57 * 56 * 49 // 6,
                4: 57 * 56 * 49 * 36 // 24,
                5: 57 * 56 * 49 * 36 * 20 // 120,
            }
        else:
            formulas = {
                2: math.comb(49, 2),
                3: 49 * 48 * 42 // 6,
                4: 49 * 48 * 42 * 31 // 24,
            }
        for sz, val in formulas.items():
            add(2, tag + " analytic count(size=%d)" % sz, val,
                c["sizes"][sz]["count"], pe["counts"][sz],
                "closed-form count, no enumeration used")

        # --- Task 3: maximal sets ---
        for sz in range(9):
            exp = claim["maximal"].get(sz, 0)
            add(3, tag + " maximal(size=%d)" % sz, exp,
                c["sizes"][sz]["maxA"], pe["maximal"][sz])
        add(3, tag + " testA vs testB counts",
            {s: c["sizes"][s]["maxA"] for s in c["sizes"]},
            {s: c["sizes"][s]["maxB"] for s in c["sizes"]},
            {s: c["sizes"][s]["maxB"] for s in c["sizes"]},
            "C test A and test B must agree")
        add(3, tag + " maximal checksum A==B", True,
            c["mchk_a"] == c["mchk_b"], True,
            "identical maximal set under both C tests")
        py_mchk = {s: pe["maximal_checksums"][s]
                   for s in range(len(pe["maximal_checksums"]))
                   if pe["maximal_checksums"][s]}
        add(3, tag + " maximal checksum C==Python", True,
            c["mchk_a"] == py_mchk, True,
            "C test A vs Python maximal sets")

        # --- Task 4: complete Grundy / misere ---
        for g, cnt in claim["grundy"].items():
            add(4, tag + " grundy(%d)" % g, cnt, c["grundy"].get(g, 0),
                pd["grundy"].get(str(g), 0))
        add(4, tag + " root Grundy", claim["root_g"], c["root_g"], pd["root_g"])
        add(4, tag + " root misere win", claim["misere"], c["root_win"],
            pd["root_win"], "1 = player to move wins under misere")
        add_cross(4, tag + " per-size Grundy C==Python",
                  {s: c["sizes"][s]["grundy"] for s in c["sizes"]},
                  {r["size"]: {int(k): v for k, v in r["grundy"].items()}
                   for r in pd["per_size"]},
                  "full per-size distribution")
        add_cross(4, tag + " per-size misere C==Python",
                  {s: (c["sizes"][s]["win"], c["sizes"][s]["loss"])
                   for s in c["sizes"]},
                  {r["size"]: (r["win"], r["loss"]) for r in pd["per_size"]},
                  "misere win/loss counts by size")

        # --- enumeration cross-check: actual mask sets ---
        py_chk = {s: pe["checksums"][s]
                  for s in range(len(pe["checksums"])) if pe["counts"][s]}
        add(2, tag + " mask checksums C==Python", True,
            c["chk"] == py_chk, True,
            "sum splitmix64(mask) per size; equality => identical enumerated sets")

        # --- Task 5: parity theorem consistency ---
        if tag == "pg2q7":
            add(5, tag + " all maximal sizes even", True,
                c["has_odd_maximal"] == 0, True,
                "maximal sizes present: 6,8")
            add(5, tag + " Grundy subset of {0,1}", True,
                set(c["grundy"]) <= {0, 1},
                set(pd["grundy"]) <= {"0", "1"})
            add(5, tag + " Grundy = |S| mod 2 on all safe sets", 0,
                c["parity_mismatch"], pd["parity_mismatch"],
                "mismatch count, so 0 = formula holds everywhere")
            add(5, tag + " size-8 count = q^5-q^2 (conics)", 7 ** 5 - 7 ** 2,
                c["sizes"][8]["count"], pe["counts"][8],
                "independent combinatorial count of conics in PG(2,7)")
        else:
            add(5, tag + " has maximal size 7 (odd)", True,
                c["has_odd_maximal"] == 1, True)
            add(5, tag + " has maximal size 6 and 8 (even)", True,
                c["has_even_maximal"] == 1, True)
            add(5, tag + " Grundy 2 exists", True,
                c["grundy"].get(2, 0) > 0, pd["grundy"].get("2", 0) > 0)
            add(5, tag + " parity formula fails somewhere", True,
                c["parity_mismatch"] > 0, pd["parity_mismatch"] > 0,
                "mixed maximal parity => no graded formula")

        # --- board verification ---
        key = "is_projective_plane_order_7" if tag == "pg2q7" else \
            "is_affine_plane_order_7"
        checks.append({"task": 1, "name": tag + " board axioms",
                       "expected": True, "c_engine": None,
                       "python": boards[tag][key],
                       "pass": bool(boards[tag][key]), "note": ""})

    # summary
    by_task = {}
    for ck in checks:
        by_task.setdefault(ck["task"], []).append(ck)
    summary = {}
    for task in sorted(by_task):
        ok = all(x["pass"] for x in by_task[task])
        summary["task%d" % task] = "PASS" if ok else "FAIL"
    failed = [x for x in checks if not x["pass"]]
    out = {"summary": summary, "failed": failed, "checks": checks,
           "c_timings": {
               tag: {"enum_seconds": parse_c(
                   os.path.join(HERE, tag + "_result.txt")).get(
                       "seconds_enum"),
                   "dp_seconds": parse_c(
                       os.path.join(HERE, tag + "_result.txt")).get(
                       "seconds_dp")}
               for tag in ("pg2q7", "ag2q7")},
           "python_timings": {
               tag: {"enum_seconds": load_json(
                   tag + "_py_enum.json")["seconds"],
                   "dp_seconds": load_json(tag + "_py_grundy.json")["seconds"]}
               for tag in ("pg2q7", "ag2q7")}}
    with open(os.path.join(HERE, "comparison.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(summary, indent=2))
    if failed:
        print("FAILED CHECKS:")
        for x in failed:
            print(" ", x)
    else:
        print("all %d checks passed" % len(checks))
    print("c timings:", out["c_timings"])
    print("python timings:", out["python_timings"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
