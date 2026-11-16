#!/usr/bin/env python3
"""Independent fold-projection tool for the class-2 lane at the canonical
head 1450 (the post-cost-66c-fold head).

Usage:
  python3 fold_projection_head1450_tool_20261116.py ROOT_HEX [ROOT_HEX ...]

Given one or more 7-stone WIN7-D10 receipt root hexes, this tool:
  1. independently reconstructs the solved set of the basis head 1450:
     the 764 published receipt roots (blob-pinned file list identical to
     the cost-66c fold script's BASIS_JSON_BLOBS / BASE_WIN7_ONLY /
     NAMED_FRONTIER inputs, 26 WIN7-only base certificate files included)
     plus the seven cost-66c WIN7-D10 receipt roots contributed by the
     published cost-66c fold JSON, plus the 498 sweep winners, with the
     frontier semantics verbatim-ported from the published
     recompute_frontier_full.py;
  2. asserts the basis head equals the published six-number summary of the
     cost-66c fold (1450/174/6398/506297/4671/370211, git blob
     8783993e5c73cc9697c3ca48aef981725f422be8) and its demand histogram;
  3. for each given root: checks it is a 7-stone position, computes its D4
     canon, asserts orbit disjointness from all 771 folded roots, and
     measures covers / marginal / marginal-in-manifest against the basis
     solved set;
  4. folds all given roots in the given order and projects the new head:
     the six-number summary, demand-histogram deltas, per-affected-parent
     row/edge-cost deltas, and the closed manifest rows.

The tool performs bookkeeping projections only; it runs no engine search
and creates no verdicts.  Interpretation guard: solved counts measure
manifest coverage, not the game-theoretic value of any position; WIN7
certificates prove a first-player win within depth 10 from individual
7-stone roots only; REFUTED-D10 is not a LOSS proof; 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import csv, gzip, hashlib, json, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
SCRIPTS = HERE / "scripts"

EXPECT_HEAD = [1450, 174, 6398, 506297, 4671, 370211]
FOLD66C_JSON = "class-frontier-cost66c-receipts-recompute-20261116.json"
FOLD66C_BLOB = "8783993e5c73cc9697c3ca48aef981725f422be8"
HIST_1450 = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12,
             "c2=1,c4=0": 208, "c2=1,c4=1": 54, "c2=1,c4=2": 8,
             "c2=2,c4=0": 797, "c2=2,c4=1": 5, "c2=2,c4=2": 50}


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


def covers(root):
    return {canon(root ^ (1 << i)) for i in range(121) if root >> i & 1}


def popcount(x):
    return bin(x).count("1")


def extract_roots(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("root_hex", "root") and isinstance(v, str):
                x = int(v, 16)
                if popcount(x) == 7:
                    acc.add(x)
            elif k == "roots" and isinstance(v, list):
                for e in v:
                    if isinstance(e, str):
                        x = int(e, 16)
                        if popcount(x) == 7:
                            acc.add(x)
            elif isinstance(v, (dict, list)):
                extract_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_roots(e, acc)


def extract_win7_roots(obj, acc):
    if isinstance(obj, dict):
        certs = None
        if "certificates" in obj and isinstance(obj["certificates"], list):
            certs = obj["certificates"]
        elif "verdict" in obj:
            certs = [obj]
        if certs is not None:
            for c in certs:
                if isinstance(c, dict):
                    v = c.get("verdict")
                    if v is not None and not str(v).startswith("WIN7"):
                        continue
                    for k in ("root", "root_hex"):
                        if k in c and isinstance(c[k], str):
                            x = int(c[k], 16)
                            if popcount(x) == 7:
                                acc.add(x)
            return
        for v in obj.values():
            if isinstance(v, (dict, list)):
                extract_win7_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_win7_roots(e, acc)


BASE_WIN7_ONLY = {
    "priority-certificates-verified.json",
    "class2-certificates-verified.json",
    "class2-next-certificates-verified.json",
    "class2-next2-certificates-verified.json",
    "class2-next3-certificates-verified.json",
    "class2-next4-certificates-verified.json",
    "class2-batch5-certificates-verified.json",
    "class2-batch3-certificates-verified.json",
    "class2-batch2-certificates-verified.json",
    "class2-batch2b-certificates-verified.json",
    "class2-batch1-certificates-verified.json",
    "class2-batch1b-certificates-verified.json",
    "class4-batch1-certificates-verified.json",
    "class4-batch2-certificates-verified.json",
    "class4-batch3-bit37-certificate.json",
    "class4-batch3-win7-certificates-20261114.json",
    "class4-batch3-win7-certificates-child5-20261114.json",
    "class4-batch3-win7-certificates-child7-20261114.json",
    "class2-lane-cost58-win7-certificates-20261114.json",
    "class2-lane-cost60-win7-certificates-20261114.json",
    "class2-lane-cost61-win7-certificates-20261114.json",
    "class2-lane-cost61b-win7-certificates-20261114.json",
    "class2-lane-cost64-win7-certificates-20261114.json",
    "class2-lane-cost65-win7-certificates-20261114.json",
    "class2-lane-cost68-win7-certificates-20261114.json",
    "class2-lane-cost75-win7-certificates-20261114.json",
}

NAMED_FRONTIER = [
    "class2-lane-cost63cd-frontier-recompute-20261114.json",
    "class2-lane-cost65c-frontier-recompute-20261114.json",
    "class2-lane-cost65d-frontier-recompute-20261114.json",
    "class2-lane-cost75-frontier-recompute-20261114.json",
    "class4-lane-cost78b-frontier-recompute-20261114.json",
    "class4-lane-cost80b-frontier-recompute-20261114.json",
]

# the 133 blob-pinned basis files of the cost-66c fold script (unchanged on
# main since its publication); imported from that published script to avoid
# transcription, with the blob of the script itself pinned here
C66C_SCRIPT = "recompute_frontier_cost66c_receipts_20261116.py"
C66C_SCRIPT_BLOB = "898cfa614e63049e52f19f080cdc398a22e0f6c9"


def load_basis_file_list():
    data = (SCRIPTS / C66C_SCRIPT).read_bytes()
    assert git_blob_sha(data) == C66C_SCRIPT_BLOB, "cost-66c fold script blob"
    ns = {"__file__": str(SCRIPTS / C66C_SCRIPT),
          "__name__": "c66c_dicts_only"}
    exec(compile(data.decode(), str(SCRIPTS / C66C_SCRIPT), "exec"), ns)
    return ns["BASIS_JSON_BLOBS"], ns["GZ_BLOBS"], ns["MS5_BLOBS"]


def reconstruct():
    basis_json_blobs, gz_blobs, ms5_blobs = load_basis_file_list()
    roots = set()
    for name in sorted(BASE_WIN7_ONLY):
        extract_win7_roots(json.loads((OUT / name).read_text()), roots)
    for name, blob in basis_json_blobs.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
        if name.startswith("class-frontier-") and name.endswith(".json"):
            extract_roots(json.loads((OUT / name).read_text()), roots)
    for name in NAMED_FRONTIER:
        extract_roots(json.loads((OUT / name).read_text()), roots)
    assert len(roots) == 764, len(roots)
    # the seven cost-66c WIN7-D10 receipt roots from the published fold JSON
    data = (OUT / FOLD66C_JSON).read_bytes()
    assert git_blob_sha(data) == FOLD66C_BLOB, FOLD66C_JSON
    fold = json.loads(data.decode())
    before = set(roots)
    extract_roots(fold, roots)
    seven = roots - before
    expected = {
        int("00000000000002003800000008002008", 16),
        int("00000000000008003800000008002008", 16),
        int("00000000000080003800000008002008", 16),
        int("00000000008000003800000008002008", 16),
        int("00000001000000003800000008002008", 16),
        int("00000002000000003800000008002008", 16),
        int("00010000000000003800000008002008", 16),
    }
    assert seven == expected, sorted(f"{r:032x}" for r in seven ^ expected)
    return roots


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: fold_projection_head1450_tool_20261116.py "
                 "ROOT_HEX [ROOT_HEX ...]")
    new_roots = [int(h, 16) for h in args]
    for r in new_roots:
        assert popcount(r) == 7, f"{r:032x} is not a 7-stone position"
    assert len(set(new_roots)) == len(new_roots)

    manifest = set()
    for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                manifest.add(int(row["hex"], 16))
    assert len(manifest) == 7867, len(manifest)

    classes = {}
    with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            classes[row["s5_hex"]] = int(row["classes"])
    with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="") as f:
        incidences = list(csv.DictReader(f))
    assert len(incidences) == 14558, len(incidences)
    winners = set()
    with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            winners.add(int(row["s6_hex"], 16))
    assert len(winners) == 498, len(winners)

    LOSS6 = ("00000000000000809202000400000000",
             "00000000000000003800004008000008",
             "00000000000000805202000000002000")
    loss = {int(x, 16) for x in LOSS6}
    rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16) in loss}

    def frontier(solved):
        remaining = defaultdict(list)
        for row in incidences:
            if row["s5_hex"] not in rejected and int(row["s6_hex"], 16) not in solved:
                remaining[row["s5_hex"]].append(row)
        unique = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
                  for rows in remaining.values() for r in rows}
        demand = defaultdict(lambda: {"c1": 0, "c2": 0, "c4": 0})
        for s5, rows in remaining.items():
            bits = classes.get(s5, 0)
            for row in rows:
                d = demand[row["s6_hex"]]
                if bits & 1:
                    d["c1"] += 1
                if bits & 2:
                    d["c2"] += 1
                if bits & 4:
                    d["c4"] += 1
        open_only = {k: v for k, v in demand.items() if v["c1"] == 0}
        return remaining, unique, demand, open_only

    def summary(solved):
        remaining, unique, demand, open_only = frontier(solved)
        hist = defaultdict(int)
        for v in open_only.values():
            hist[f"c2={v['c2']},c4={v['c4']}"] += 1
        return {
            "solved_s6_in_manifest": len(solved & manifest),
            "remaining_s5_orbits": len(remaining),
            "unique_remaining_s6": len(unique),
            "sum_remaining_cost": sum(unique.values()),
            "s6_needed_by_open_classes": len(open_only),
            "cost_needed_by_open_classes": sum(int(unique[k]) for k in open_only),
            "hist": dict(sorted(hist.items())),
        }

    basis_roots = reconstruct()
    solved = set(winners)
    for r in basis_roots:
        solved |= covers(r)
    got = [summary(solved)[k] for k in
           ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
            "sum_remaining_cost", "s6_needed_by_open_classes",
            "cost_needed_by_open_classes")]
    assert got == EXPECT_HEAD, f"basis head mismatch: {got}"
    base_summary = summary(solved)
    assert base_summary["hist"] == HIST_1450, base_summary["hist"]
    # cross-check against the published cost-66c fold record
    fold = json.loads((OUT / FOLD66C_JSON).read_text())
    fa = fold["frontier_after_cost66c"]
    assert [fa[k] for k in
            ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
             "sum_remaining_cost", "s6_needed_by_open_classes",
             "cost_needed_by_open_classes")] == got
    folded_canons = {canon(r) for r in basis_roots}
    assert len(basis_roots) == 771, len(basis_roots)
    assert len(folded_canons) == 756, len(folded_canons)

    rem_b, uniq_b, dem_b, _ = frontier(solved)
    receipts = []
    for r in new_roots:
        c = canon(r)
        assert c not in folded_canons, f"{r:032x} D4-collides with a folded root"
        folded_canons.add(c)
        cov = covers(r)
        marg = cov - solved
        marg_m = marg & manifest
        receipts.append({
            "root_hex": f"{r:032x}",
            "d4_canonical_hex": f"{c:032x}",
            "d4_orbit_distinct_from_all_folded_roots": True,
            "covers": len(cov),
            "covers_hexes": sorted(f"{x:032x}" for x in cov),
            "marginal": len(marg),
            "marginal_hexes": sorted(f"{x:032x}" for x in marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{x:032x}" for x in marg_m),
        })
        solved |= cov

    new_summary = summary(solved)
    hist_before = base_summary["hist"]
    hist_after = new_summary["hist"]
    hist_deltas = {k: hist_after.get(k, 0) - hist_before.get(k, 0)
                   for k in set(hist_before) | set(hist_after)}

    new_hexes = {int(h, 16) for rec in receipts
                 for h in rec["marginal_manifest_hexes"]}
    parents = {}
    rem_a, uniq_a, dem_a, _ = frontier(solved)
    for s5 in set(rem_b) | set(rem_a):
        rows_b = list(rem_b.get(s5, []))
        rows_a = list(rem_a.get(s5, []))
        if len(rows_b) == len(rows_a):
            continue
        lost = ({int(r["s6_hex"], 16) for r in rows_b}
                - {int(r["s6_hex"], 16) for r in rows_a})
        lost &= new_hexes
        if not lost:
            continue
        parents[s5] = {
            "s5_hex": s5,
            "classes": classes.get(s5, 0),
            "rows_before": len(rows_b),
            "rows_after": len(rows_a),
            "edge_cost_before": sum(int(r["s6_s7_edge_cost"]) for r in rows_b),
            "edge_cost_after": sum(int(r["s6_s7_edge_cost"]) for r in rows_a),
            "lost_rows_hexes": sorted(f"{x:032x}" for x in lost),
            "lost_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows_b
                                  if int(r["s6_hex"], 16) in lost),
        }

    incidences_after = sum(len(v["lost_rows_hexes"]) for v in parents.values())
    cost_delta = sum(v["lost_edge_cost"] for v in parents.values())

    result = {
        "schema": "n11-class2-lane-fold-projection-tool-head1450-20261116-v1",
        "date": "2026-11-16",
        "basis_head": 1450,
        "basis_head_numbers": EXPECT_HEAD,
        "basis_roots": len(basis_roots),
        "basis_distinct_d4_canons": 756,
        "basis_summary": {k: base_summary[k] for k in
                          ("solved_s6_in_manifest", "remaining_s5_orbits",
                           "unique_remaining_s6", "sum_remaining_cost",
                           "s6_needed_by_open_classes",
                           "cost_needed_by_open_classes", "hist")},
        "receipts": receipts,
        "projected_head": {k: new_summary[k] for k in
                           ("solved_s6_in_manifest", "remaining_s5_orbits",
                            "unique_remaining_s6", "sum_remaining_cost",
                            "s6_needed_by_open_classes",
                            "cost_needed_by_open_classes")},
        "demand_histogram_deltas": dict(sorted(hist_deltas.items())),
        "affected_parents": {k: v for k, v in sorted(parents.items())},
        "parent_row_incidences": incidences_after,
        "parent_edge_cost_delta": cost_delta,
        "interpretation_guard": (
            "bookkeeping fold projection only; no engine search, no verdicts; "
            "solved counts measure manifest coverage, not the game-theoretic "
            "value of any position; WIN7 certificates prove a first-player win "
            "within depth 10 from individual 7-stone roots only; REFUTED-D10 "
            "is not a LOSS proof; 11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    out_path = OUT / ("class2-lane-fold-projection-basis1450-"
                      f"{len(new_roots)}roots-20261116.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("basis 1450 head", got)
    for rec in receipts:
        print("root", rec["root_hex"], "marg", rec["marginal"],
              "mim", rec["marginal_in_manifest"],
              rec["marginal_manifest_hexes"])
    p = result["projected_head"]
    print("projected:", " ".join(str(p[k]) for k in
          ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
           "sum_remaining_cost", "s6_needed_by_open_classes",
           "cost_needed_by_open_classes")))
    print("hist deltas:", result["demand_histogram_deltas"])
    print("affected parents:", len(parents),
          "incidences", incidences_after, "cost delta", cost_delta)
    print("output:", out_path.name)


if __name__ == "__main__":
    main()
