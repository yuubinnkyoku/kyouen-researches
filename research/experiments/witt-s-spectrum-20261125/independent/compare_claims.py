"""Compare the claimed engine outputs with the independent recomputation.

Claimed raw files: design-kyouen-witt-20261125/output/grundy_w24_s{2..7}.txt
(no s=1 or s=8 raw file exists; those claims live only in the README/report
tables and in witt-s-spectrum-20261125/output/spectrum.json).

Independent data used:
  out/c_full_s{1..7}.txt            C engine (DFS + full mex DP)
  out/task2_python_1_2_3_4.json     Python DFS + DP, s=1..4
  out/task2_python_5.json           Python DFS + DP, s=5
  out/task2_python_6.json           Python DFS + DP, s=6
  out/task5_crosscheck.json         s=7 per-size Grundy-0 counts from the C DP table
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
CLAIM_DIR = HERE.parents[1] / "design-kyouen-witt-20261125" / "output"
SPECTRUM = HERE.parents[0] / "output" / "spectrum.json"


def parse_claim(s: int):
    path = CLAIM_DIR / f"grundy_w24_s{s}.txt"
    d = {"path": str(path), "SIZE": {}, "GRUNDY": {}}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "POINTS":
            d["POINTS"] = int(parts[1])
        elif parts[0] == "CIRCLES":
            d["CIRCLES"] = int(parts[1])
        elif parts[0] == "SAFE":
            d["SAFE"] = int(parts[1])
        elif parts[0] == "ROOT":
            d["ROOT"] = (int(parts[1]), int(parts[2]))
        elif parts[0] == "SIZE":
            d["SIZE"][int(parts[1])] = (int(parts[2]), int(parts[3]), int(parts[4]))
        elif parts[0] == "GRUNDY":
            d["GRUNDY"][int(parts[1])] = int(parts[2])
    return d


def parse_c(s: int):
    path = OUT / f"c_full_s{s}.txt"
    d = {"SIZE": {}, "GRUNDY": {}, "MISERE": {}}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "SIZE":
            d["SIZE"][int(parts[1])] = (int(parts[2]), int(parts[3]))
        elif parts[0] == "SAFE":
            d["SAFE"] = int(parts[1])
        elif parts[0] == "MAXIMAL":
            d["MAXIMAL"] = int(parts[1])
        elif parts[0] == "GRUNDY":
            d["GRUNDY"][int(parts[1])] = int(parts[2])
        elif parts[0] == "ROOT_GRUNDY":
            d["ROOT_GRUNDY"] = int(parts[1])
        elif parts[0] == "ROOT_MISERE":
            d["ROOT_MISERE"] = int(parts[1])
        elif parts[0] == "MISERE":
            d["MISERE"][int(parts[1])] = int(parts[2])
    return d


def load_json(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def our_g0_by_size(s: int):
    def g0(d):
        return sum(c for g, c in d.items() if int(g) == 0)

    if s <= 4:
        data = load_json("task2_python_1_2_3_4.json")[f"s{s}"]
        return {int(k): g0(v) for k, v in data["grundy_by_size"].items()}
    if s == 5:
        data = load_json("task2_python_5.json")["s5"]
        return {int(k): g0(v) for k, v in data["grundy_by_size"].items()}
    if s == 6:
        data = load_json("task2_python_6.json")["s6"]
        return {int(k): g0(v) for k, v in data["grundy_by_size"].items()}
    data = load_json("task5_crosscheck.json")["grundy0_by_size"]
    return {int(k): v for k, v in data.items()}


def main() -> int:
    spectrum = json.loads(SPECTRUM.read_text(encoding="utf-8"))
    discrepancies = []
    per_s = {}
    for s in range(1, 8):
        c = parse_c(s)
        entry = {"our_safe": c["SAFE"], "our_maximal": c["MAXIMAL"],
                 "our_grundy": c["GRUNDY"],
                 "our_root": [c["ROOT_GRUNDY"], c["ROOT_MISERE"]]}
        if s >= 2:
            cl = parse_claim(s)
            entry["claim_file"] = cl["path"]
            entry["claim_safe"] = cl["SAFE"]
            entry["claim_root"] = list(cl["ROOT"])
            entry["claim_grundy"] = cl["GRUNDY"]
            entry["claim_maximal_total"] = sum(v[1] for v in cl["SIZE"].values())
            if cl["SAFE"] != c["SAFE"]:
                discrepancies.append(f"s={s}: SAFE claim {cl['SAFE']} != ours {c['SAFE']}")
            if cl["GRUNDY"] != c["GRUNDY"]:
                discrepancies.append(f"s={s}: GRUNDY claim {cl['GRUNDY']} != ours {c['GRUNDY']}")
            if (cl["ROOT"][0], cl["ROOT"][1]) != (c["ROOT_GRUNDY"], c["ROOT_MISERE"]):
                discrepancies.append(f"s={s}: ROOT claim {cl['ROOT']} != ours {(c['ROOT_GRUNDY'], c['ROOT_MISERE'])}")
            g0 = our_g0_by_size(s)
            claim_sizes = set(cl["SIZE"])
            ours_sizes = set(c["SIZE"])
            if claim_sizes != ours_sizes:
                discrepancies.append(f"s={s}: size support {sorted(claim_sizes)} != {sorted(ours_sizes)}")
            for k in sorted(claim_sizes & ours_sizes):
                ccnt, cmax, cg0 = cl["SIZE"][k]
                ocnt, omax = c["SIZE"][k]
                if ccnt != ocnt:
                    discrepancies.append(f"s={s} size {k}: count {ccnt} != {ocnt}")
                if cmax != omax:
                    discrepancies.append(f"s={s} size {k}: maximal {cmax} != {omax}")
                if cg0 != g0.get(k, 0):
                    discrepancies.append(f"s={s} size {k}: grundy0 {cg0} != {g0.get(k, 0)}")
            entry["claim_size"] = {str(k): list(v) for k, v in cl["SIZE"].items()}
        # spectrum.json (aggregated claims) for s=2..7
        if str(s) in spectrum.get("s", {}):
            sp = spectrum["s"][str(s)]
            if sp["safe"] != c["SAFE"]:
                discrepancies.append(f"s={s}: spectrum.safe {sp['safe']} != {c['SAFE']}")
            if sp["size_total"] != c["SAFE"]:
                discrepancies.append(f"s={s}: spectrum.size_total {sp['size_total']} != {c['SAFE']}")
            if sp["root_grundy"] != c["ROOT_GRUNDY"]:
                discrepancies.append(f"s={s}: spectrum.root_grundy {sp['root_grundy']} != {c['ROOT_GRUNDY']}")
            if sp["root_misere"] != c["ROOT_MISERE"]:
                discrepancies.append(f"s={s}: spectrum.root_misere {sp['root_misere']} != {c['ROOT_MISERE']}")
            sp_max = {int(k): v for k, v in sp["maximal_sizes"].items()}
            our_max = {k: v[1] for k, v in c["SIZE"].items() if v[1]}
            if sp_max != our_max:
                discrepancies.append(f"s={s}: spectrum.maximal_sizes {sp_max} != {our_max}")
            sp_g = {int(k): v for k, v in sp["grundy"].items()}
            if sp_g != c["GRUNDY"]:
                discrepancies.append(f"s={s}: spectrum.grundy {sp_g} != {c['GRUNDY']}")
        per_s[f"s{s}"] = entry

    result = {
        "claimed_raw_files_present": [2, 3, 4, 5, 6, 7],
        "claimed_s1_raw_file_present": (CLAIM_DIR / "grundy_w24_s1.txt").exists(),
        "per_s": per_s,
        "discrepancies": discrepancies,
        "PASS": not discrepancies,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "compare_claims.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0 if not discrepancies else 1


if __name__ == "__main__":
    sys.exit(main())
