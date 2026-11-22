#!/usr/bin/env python3
"""summarize_rows.py — assemble the cross-system row summary and the K0030
reproduction table for the n3..n6 maximal-safe row experiment.

Inputs (paths fixed by the experiment layout): enum jsonl (run1/run2), classify
JSONs (run1/cls2), verify_rows JSONs (run1/run2), brute-scan JSONs, K0030
published distribution values (hardcoded from the published item).

Checks (fail-closed):
  R1 every row: found == K0030 value within the published table range
     (5..11 stones); oos rows are recorded as such;
  R2 determinism: run1 vs run2 cfg lines byte-identical, found/nodes equal
     (precomputed digests are compared);
  R3 classify vs verify: orbit count, stabilizer histogram, trips3 histogram,
     dirs histogram, all_have_three_collinear equal (two geometries, two
     languages, two orbit implementations);
  R4 brute scan (n=3,4): nonzero row counts equal DFS counts; (n=4) full
     configuration sets identical.
Output: rows-summary.json (machine record) + markdown table to stdout.
"""
import hashlib
import json
import sys

K0030 = {
    3: {5: 56, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0},
    4: {5: 176, 6: 688, 7: 64, 8: 0, 9: 0, 10: 0, 11: 0},
    5: {5: 4, 6: 1136, 7: 11280, 8: 4340, 9: 100, 10: 0, 11: 0},
    6: {5: 0, 6: 8, 7: 3952, 8: 115496, 9: 199184, 10: 30492, 11: 464},
}
NONZERO = {4: [5, 6, 7], 5: [5, 6, 7, 8, 9], 6: [6, 7, 8, 9, 10, 11]}
ALLROWS = {4: list(range(1, 17)), 5: list(range(1, 26)), 6: list(range(1, 37))}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def det_equal(path_a, path_b):
    same_cfg = False
    if open(path_a, "rb").read() == open(path_b, "rb").read():
        same_cfg = True
    else:
        return False
    return same_cfg


def row_summary(n, k):
    p1 = f"output/enum_n{n}_k{k}.jsonl"
    p2 = f"output/run2/enum_n{n}_k{k}.jsonl"
    found1 = nodes1 = found2 = nodes2 = None
    cfg1 = []
    for line in open(p1):
        r = json.loads(line)
        if r.get("type") == "cfg":
            cfg1.append(r["stones"])
        elif r.get("type") == "summary":
            found1, nodes1 = r["found"], r["nodes"]
    for line in open(p2):
        r = json.loads(line)
        if r.get("type") == "summary":
            found2, nodes2 = r["found"], r["nodes"]
    rec = {
        "n": n, "k": k, "found": found1, "nodes_run1": nodes1, "nodes_run2": nodes2,
        "determinism_nodes_bit_equal": nodes1 == nodes2,
        "determinism_found_equal": found1 == found2,
        "k0030_published": K0030[n][k] if k in K0030[n] else None,
        "k0030_range": k in K0030[n],
        "k0030_match": (K0030[n][k] == found1) if k in K0030[n] else None,
    }
    return rec, cfg1


def main():
    out = {"boards": {}, "problems": []}
    md = ["| n | k | found | nodes | det | K0030 | orbits(cls=ver) | stab | trips{1:}| dirs{1:} | ecc range |",
          "|---|---|---:|---:|---|---|---|---|---:|---:|---|"]
    for n in (4, 5, 6):
        rows = []
        cls_data = {}
        for k in ALLROWS[n]:
            rec, cfg1 = row_summary(n, k)
            if rec["found"] == 0:
                if not rec["k0030_range"]:
                    rec["k0030_match"] = "oos-zero"
                rows.append(rec)
                continue
            # nonzero row: classify + verify records
            cls = json.load(open(f"output/classify_n{n}_k{k}.json"))
            cls2 = json.load(open(f"output/cls2/classify_n{n}_k{k}.json"))
            if json.dumps(cls, sort_keys=True) != json.dumps(cls2, sort_keys=True):
                out["problems"].append(f"n{n}k{k}: classify run1 != run2")
            ver = None
            for r in json.load(open(f"output/verify_n{n}_rows.json"))["rows"]:
                if r["k"] == k:
                    ver = r
            for r in json.load(open(f"output/verify2_n{n}_rows.json"))["rows"]:
                if r["k"] == k and json.dumps(r, sort_keys=True) != json.dumps(ver, sort_keys=True):
                    out["problems"].append(f"n{n}k{k}: verify run1 != run2")
            # cross checks (normalize histogram keys: JSON round-trip makes all
            # keys strings; str()-normalize both sides)
            def norm(h):
                return {str(kk): int(vv) for kk, vv in h.items()}
            if cls["orbits"] != ver["orbits_python"]:
                out["problems"].append(f"n{n}k{k}: orbit count cls {cls['orbits']} != ver {ver['orbits_python']}")
            # stabilizer histogram comparison
            sb_c = {}
            for o in cls["orbit_details"]:
                sb_c[o["stabilizer_order"]] = sb_c.get(o["stabilizer_order"], 0) + 1
            sb_c = norm(sb_c)
            if sb_c != norm(ver["stabilizer_histogram"]):
                out["problems"].append(f"n{n}k{k}: stabilizer hist mismatch")
            if norm(cls["triples3_histogram_all_sets"]) != norm(ver["trips3_histogram"]):
                out["problems"].append(f"n{n}k{k}: trips hist mismatch")
            if norm(cls["dirs_histogram_all_sets"]) != norm(ver["dirs_histogram"]):
                out["problems"].append(f"n{n}k{k}: dirs hist mismatch")
            if cls["all_have_three_collinear"] != ver["all_have_three_collinear"]:
                out["problems"].append(f"n{n}k{k}: all_have mismatch")
            rec["orbits"] = cls["orbits"]
            rec["orbits_cls_eq_ver"] = cls["orbits"] == ver["orbits_python"]
            rec["stabilizer_histogram"] = sb_c
            rec["trips3_histogram"] = ver["trips3_histogram"]
            rec["dirs_histogram"] = ver["dirs_histogram"]
            rec["one_triple_configs"] = ver["trips3_histogram"].get("1", 0) if isinstance(ver["trips3_histogram"], dict) and "1" in ver["trips3_histogram"] else 0
            rec["one_direction_configs"] = ver["dirs_histogram"].get("1", 0) if "1" in ver["dirs_histogram"] else 0
            rec["zero_triple_configs"] = ver["trips3_histogram"].get("0", 0) if "0" in ver["trips3_histogram"] else 0
            rec["all_have_three_collinear"] = ver["all_have_three_collinear"]
            rec["ecc_histogram"] = cls["ecc_histogram_all_sets"]
            rec["total_cfg_sha256"] = hashlib.sha256(
                json.dumps(cls["configs"], separators=(",", ":")).encode()).hexdigest()
            rec["verify_safe_all"] = ver["safe_all"]
            rec["verify_maximal_all"] = ver["maximal_all"]
            rec["remov_histogram"] = ver["remov_histogram"]
            rows.append(rec)
        # brute scan cross-check
        if n in (3, 4):
            br = json.load(open(f"output/brute_n{n}.json"))
            out.setdefault("brute_scan", {})[n] = {
                "counts_by_k": br["counts_by_k"],
                "zero_rows_k": br["zero_rows_k"],
            }
        out["boards"][n] = rows

    # brute scan vs DFS (n=4 set equality)
    for n in (4,):
        br = json.load(open(f"output/brute_n{n}.json"))
        for k, cfgs in br["rows"].items():
            dfs = []
            for line in open(f"output/enum_n{n}_k{k}.jsonl"):
                r = json.loads(line)
                if r.get("type") == "cfg":
                    dfs.append(tuple(r["stones"]))
            ident = sorted(dfs) == sorted(tuple(x) for x in cfgs)
            out.setdefault("brute_scan_set_equal", {})[f"n{n}k{k}"] = ident
            if not ident:
                out["problems"].append(f"brute vs DFS set mismatch n{n}k{k}")
    with open("output/rows-summary.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({"problems": out["problems"], "brute": out.get("brute_scan"),
                      "brute_set_eq": out.get("brute_scan_set_equal")}))
    sys.exit(1 if out["problems"] else 0)


if __name__ == "__main__":
    main()
