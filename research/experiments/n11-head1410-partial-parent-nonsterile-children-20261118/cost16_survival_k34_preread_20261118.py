#!/usr/bin/env python3
"""Rank-34 structural preread for the 31-row cost-16 parent survival lane.

Deterministic pure-Python preread (exact integer arithmetic, no pm
recomputation): re-derives the full structural census of the top-34
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-32 preread
layer (pinned k32 preread JSON, commit 490a3e44bc; the k=32 main result
JSON is not yet published, so the rank-32 regression compares against
the preread artifact that the k=32 main computation's load/assert chain
will consume) and the published rank-33 preread layer (pinned k33 preread
JSON, commit 67068e077, second-derivation verified by commit 2ae6b6b8),
and records the rank-34 facts (root rows [9,19], prior hits, membership
split, new pair/triple/quad/quint censuses, full C(34,3)/C(34,5)
censuses, sextet C(34,6) census) needed by the k=34 main computation's
load/assert chain.

Pure Python (following the k=32/k=33 preread scripts): all large
integers are exact and the final check asserts the exact aggregate
integers round trip through JSON on every run.

Two classifiers (dict-accumulate vs Counter-variant) must agree on
every enumerated combination. Fully deterministic: fixed insertion
order, no timestamps, so two runs produce byte-identical output.

Fetches all inputs at pinned git blob sha1s via the jsdelivr mirror
with a raw.githubusercontent.com fallback (a mirror serving
stale-but-wrong bytes fails the sha1 check and the next mirror is
tried), or from a local directory with --local DIR (sha1 checked).

Usage: python3 cost16_survival_k34_preread_20261118.py [--local DIR] [--out PATH]
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
import urllib.request
from collections import Counter

REPO = "yuubinnkyoku/kyouen-researches"
PATH = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
PINS = {
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
    "k31": ("cost16-survival-k31-20261118.json", "0d9f67ee69ad4fb8aa37904ddbf6666745786807"),
    "k32pre": ("cost16-survival-k32-preread-20261118.json",
               "6d49ab5bea27c967e15b482b33e376510c62b857"),
    "k33pre": ("cost16-survival-k33-preread-20261118.json",
               "e4346ddd7e08799b4406dcdba930de714e4f462c"),
}
PARENT_ROOT = "00000000000000003800000008001000"  # 31-row cost-16 parent
R = 31          # parent rows (fixed: new ranks ban one more pair root)
RANK = 34      # 1-based top50 rank of the new root
IDX = RANK - 1  # 0-based index of the new root


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def fetch_bytes(name: str, want_sha: str, local_dir: str | None) -> bytes:
    if local_dir:
        data = open(f"{local_dir}/{name}", "rb").read()
    else:
        urls = [
            f"https://cdn.jsdelivr.net/gh/{REPO}@main/{PATH}/{name}",
            f"https://raw.githubusercontent.com/{REPO}/main/{PATH}/{name}",
        ]
        data = None
        shas = []
        for u in urls:
            try:
                data = urllib.request.urlopen(u, timeout=60).read()
            except Exception:
                continue
            got = git_blob_sha1(data)
            if got == want_sha:
                break
            shas.append((u.split("/")[2], got))
            data = None
        if data is None:
            raise RuntimeError(f"could not fetch {name} at pinned sha "
                               f"{want_sha} (mirror results: {shas})")
        return data
    got = git_blob_sha1(data)
    if got != want_sha:
        raise RuntimeError(f"{name}: blob sha1 {got} != pinned {want_sha}")
    return data


def fetch(name: str, want_sha: str, local_dir: str | None) -> dict:
    return json.loads(fetch_bytes(name, want_sha, local_dir))


# ---- classifier A: dict accumulate (same definition as the k14 publication)
def classify_a(rows, combo):
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    if max(c.values()) >= 3:
        return "zero", None
    twos = [r for r, v in c.items() if v == 2]
    if len(twos) >= 2:
        return "zero", None
    if len(twos) == 1:
        return "b_only", twos[0]
    return "disjoint", None


# ---- classifier B: independent Counter variant (different code path)
def classify_b(rows, combo):
    cnt = Counter()
    for i in combo:
        cnt.update(rows[i])
    if any(v >= 3 for v in cnt.values()):
        return "zero", None
    pair_rows = sorted(r for r, v in cnt.items() if v == 2)
    if len(pair_rows) == 1:
        return "b_only", pair_rows[0]
    if not pair_rows:
        return "disjoint", None
    return "zero", None


def census(rows, combos, both=True):
    """Count classes over combos with both classifiers; returns
    (counts, twos_histogram, comparisons, mismatches)."""
    cen = {"b_only": 0, "zero": 0, "disjoint": 0}
    twos = {}
    mism = 0
    n = 0
    for c in combos:
        ca, ta = classify_a(rows, c)
        n += 1
        if both:
            cb, tb = classify_b(rows, c)
            if (ca, ta) != (cb, tb):
                mism += 1
        cen[ca] += 1
        if ca == "b_only":
            twos[ta] = twos.get(ta, 0) + 1
    return cen, dict(sorted(twos.items())), n, mism


def new_census(rows, idx, size, both=True):
    """Census over combinations of `size` roots that all include idx."""
    others = range(idx)
    return census(rows, ((idx,) + c for c in itertools.combinations(others, size - 1)), both)


def profile_of(rows, five):
    """4-subset profile key 'b/d/z' of a b_only quint (b_only /
    disjoint / zero counts over its five 4-subsets)."""
    cls = []
    for drop in range(5):
        sub = tuple(x for k, x in enumerate(five) if k != drop)
        cl, _ = classify_a(rows, sub)
        cls.append(cl)
    return "%d/%d/%d" % (cls.count("b_only"), cls.count("disjoint"), cls.count("zero"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=None,
                    help="directory with the pinned input JSONs (offline mode; sha1 still checked)")
    ap.add_argument("--out", default="output/cost16-survival-k34-preread-20261118.json",
                    help="output JSON path")
    args = ap.parse_args()

    agg = fetch(*PINS["agg"], args.local)
    k31 = fetch(*PINS["k31"], args.local)
    k32pre = fetch(*PINS["k32pre"], args.local)
    k33pre = fetch(*PINS["k33pre"], args.local)
    if not k31.get("all_pass"):
        print("FAIL k31 all_pass is false")
        return 1
    if not (k32pre.get("all_pass") and k32pre.get("check_count") == 31):
        print("FAIL k32 preread all_pass/check_count unexpected")
        return 1
    if not (k33pre.get("all_pass") and k33pre.get("check_count") == 31):
        print("FAIL k33 preread all_pass/check_count unexpected")
        return 1

    top = agg["derived"]["top50_by_membership"]
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]

    checks = []

    def check(name, ok, detail=None):
        checks.append({"name": name, "pass": bool(ok), "detail": detail or {}})

    # 1. aggregate sanity
    check("top50_has_50_unique_pair_roots",
          len(top) == 50 and len({e["root"] for e in top}) == 50
          and all(len(e["rows_covered"]) == 2 for e in top),
          {"len": len(top)})
    # 2. publication chain: the pinned k33 preread declares the pinned
    #    aggregate, k31 result and k32 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k33pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k33_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k31_result") == PINS["k31"][1]
          and in_pins.get("k32_preread") == PINS["k32pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k31": PINS["k31"][1], "pinned_k32pre": PINS["k32pre"][1]})

    # ---- rank-32 regression (vs the pinned published k32 preread JSON)
    reg = {}
    n = 32
    idx = n - 1
    pub32 = k32pre["rank32"]
    prior = {}
    for r in rows[idx]:
        prior[r] = [i for i in range(idx) if r in rows[i]]
    pc, _, pcmp, pmis = new_census(rows, idx, 2)
    shared = idx - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, idx, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, idx, 4)
    uc, utwos, ucmp, umis = new_census(rows, idx, 5)
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(n), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(n), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(n), 6))
    dusizes = {}
    for c in itertools.combinations(range(idx), 3):
        combo = (idx,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    check(f"rank{n}_root_matches_published_preread",
          pub32["root"] == "00000000000000801222000000081000" == top[idx]["root"]
          and sorted(pub32["rows"]) == sorted(rows[idx]) == [15, 23]
          and int(pub32["membership"]) == int(mem[idx]) == 120146272057315812
          and int(pub32["a_part"]) == 92121445452103947
          and int(pub32["b_part"]) == 28024826605211865,
          {"root": pub32["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {15: [0, 13, 14, 16, 17, 22], 23: [11]}
          and {k: sorted(v) for k, v in pub32["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub32["new_census"]["pair"]["shared"] == shared
          and pub32["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub32["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub32["new_census"]["triple"]["zero"] == tc["zero"]
          and pub32["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub32["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub32["new_census"]["quad"]["zero"] == qc["zero"]
          and pub32["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub32["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub32["new_census"]["quint"]["zero"] == uc["zero"]
          and pub32["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 275, "zero": 50, "disjoint": 140}
          and qc == {"b_only": 1878, "zero": 2459, "disjoint": 158}
          and uc == {"b_only": 2010, "zero": 29455, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub32["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub32["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub32["new_quint_double_row_histogram"].items()} == utwos
          and pub32["disjoint_quad_count"] == qc["disjoint"] == 158
          and {int(k): v for k, v in pub32["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub32["cumulative_disjoint_quads"] == 662 + qc["disjoint"] == 820,
          {"disjoint_union_sizes": dusizes, "cumulative": 662 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub32["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 2992, "zero": 980, "disjoint": 988}
          and {int(k): v for k, v in pub32["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub32["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 8797, "zero": 192579, "disjoint": 0}
          and {int(k): v for k, v in pub32["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub32["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(32, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_published_k31",
          ful5["b_only"] - uc["b_only"] == 6787
          and k31["structure"]["quint_census_k31"]["b_only"] == 6787
          and ful5["zero"] - uc["zero"] == 163124
          and k31["structure"]["quint_census_k31"]["zero"] == 163124
          and ful5["disjoint"] == 0,
          {"prev_b_only": 6787, "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})
    check(f"rank{n}_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})
    reg[n] = {
        "root": top[idx]["root"],
        "rows": sorted(rows[idx]),
        "membership": int(mem[idx]),
        "a_part": int(memA[top[idx]["root"]]),
        "b_part": int(memB[top[idx]["root"]]),
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "new_census": {
            "pair": {"b_only": shared, "zero": 0, "disjoint": pc["disjoint"],
                     "total": idx, "expected_total": idx},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(idx, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(idx, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(idx, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

    # ---- rank-33 regression (vs the pinned published k33 preread JSON)
    n = 33
    idx = n - 1
    pub33 = k33pre["rank33"]
    prior = {}
    for r in rows[idx]:
        prior[r] = [i for i in range(idx) if r in rows[i]]
    pc, _, pcmp, pmis = new_census(rows, idx, 2)
    shared = idx - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, idx, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, idx, 4)
    uc, utwos, ucmp, umis = new_census(rows, idx, 5)
    new_quint_b_only = []
    for c in itertools.combinations(range(idx), 4):
        cl, two = classify_a(rows, (idx,) + c)
        if cl == "b_only":
            new_quint_b_only.append((idx,) + c)
    profiles = {}
    for five in new_quint_b_only:
        k = profile_of(rows, five)
        profiles[k] = profiles.get(k, 0) + 1
    dusizes = {}
    for c in itertools.combinations(range(idx), 3):
        combo = (idx,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(n), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(n), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(n), 6))
    check(f"rank{n}_root_matches_published_preread",
          pub33["root"] == "00000000000000801302020000001000" == top[idx]["root"]
          and sorted(pub33["rows"]) == sorted(rows[idx]) == [7, 19]
          and int(pub33["membership"]) == int(mem[idx]) == 120083817332086665
          and int(pub33["a_part"]) == 92100657745931553
          and int(pub33["b_part"]) == 27983159586155112,
          {"root": pub33["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {7: [20], 19: [0, 2, 3, 8, 9, 10, 15, 29]}
          and {k: sorted(v) for k, v in pub33["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub33["new_census"]["pair"]["shared"] == shared
          and pub33["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub33["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub33["new_census"]["triple"]["zero"] == tc["zero"]
          and pub33["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub33["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub33["new_census"]["quad"]["zero"] == qc["zero"]
          and pub33["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub33["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub33["new_census"]["quint"]["zero"] == uc["zero"]
          and pub33["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 304, "zero": 67, "disjoint": 125}
          and qc == {"b_only": 1827, "zero": 2987, "disjoint": 146}
          and uc == {"b_only": 2036, "zero": 33924, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub33["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub33["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub33["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub33["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub33["disjoint_quad_count"] == qc["disjoint"] == 146
          and {int(k): v for k, v in pub33["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub33["cumulative_disjoint_quads"] == 820 + qc["disjoint"] == 966,
          {"disjoint_union_sizes": dusizes, "cumulative": 820 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub33["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 3296, "zero": 1047, "disjoint": 1113}
          and {int(k): v for k, v in pub33["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub33["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 10833, "zero": 226503, "disjoint": 0}
          and {int(k): v for k, v in pub33["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub33["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(33, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_vs_rank32_regression",
          ful5["b_only"] - uc["b_only"] == reg[32]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[32]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[32]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})
    check(f"rank{n}_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})
    reg[n] = {
        "root": top[idx]["root"],
        "rows": sorted(rows[idx]),
        "membership": int(mem[idx]),
        "a_part": int(memA[top[idx]["root"]]),
        "b_part": int(memB[top[idx]["root"]]),
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "new_census": {
            "pair": {"b_only": shared, "zero": 0, "disjoint": pc["disjoint"],
                     "total": idx, "expected_total": idx},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(idx, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(idx, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(idx, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

    # ---- rank-34 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m34 = int(mem[IDX])
    a34 = int(memA[root])
    b34 = int(memB[root])
    prior = {}
    for r in rows[IDX]:
        prior[r] = [i for i in range(IDX) if r in rows[i]]

    pc, _, pcmp, pmis = new_census(rows, IDX, 2)
    shared = IDX - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, IDX, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, IDX, 4)
    uc, utwos, ucmp, umis = new_census(rows, IDX, 5)
    new_quint_b_only = []
    for c in itertools.combinations(range(IDX), 4):
        cl, two = classify_a(rows, (IDX,) + c)
        if cl == "b_only":
            new_quint_b_only.append((IDX,) + c)
    profiles = {}
    for five in new_quint_b_only:
        k = profile_of(rows, five)
        profiles[k] = profiles.get(k, 0) + 1
    dusizes = {}
    for c in itertools.combinations(range(IDX), 3):
        combo = (IDX,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(RANK), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(RANK), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(RANK), 6))

    check("rank34_root_matches_top50",
          root == "00000000080000003800000088001000"
          and sorted(rows[IDX]) == [9, 19],
          {"root": root, "rows": sorted(rows[IDX])})
    check("rank34_prior_hits_recorded",
          prior == {9: [21], 19: [0, 2, 3, 8, 9, 10, 15, 29, 32]},
          {str(k): v for k, v in sorted(prior.items())})
    check("rank34_membership_split_identity",
          a34 + b34 == m34
          and m34 == 120079520746539458
          and m34 < int(reg[33]["membership"]),
          {"membership": m34, "a_part": a34, "b_part": b34})
    check("rank34_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 10 and pc["disjoint"] == 23,
          {"shared": shared, "disjoint": pc["disjoint"], "total": IDX})
    check("rank34_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 326, "zero": 77, "disjoint": 125}, tc)
    check("rank34_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 1944, "zero": 3366, "disjoint": 146}, qc)
    check("rank34_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"]
          and uc == {"b_only": 2171, "zero": 38749, "disjoint": 0},
          {**uc, "records": len(new_quint_b_only)})
    check("rank34_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 9 not in utwos and 19 in utwos
          and utwos == {15: 314, 16: 66, 18: 897, 19: 894}, utwos)
    check("rank34_b_only_quint_profiles",
          profiles == {"3/2/0": uc["b_only"]}, profiles)
    check("rank34_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 146,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 966 + qc["disjoint"]})
    dj34 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")
    check("rank34_cumulative_disjoint_quads_global_recount",
          dj34 == 1112 and dj34 == 966 + qc["disjoint"]
          and dj34 == pub33["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C34_4": dj34, "prev_cumulative": pub33["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})
    check("rank34_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 3622, "zero": 1124, "disjoint": 1238}
          and ful5 == {"b_only": 13004, "zero": 265252, "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "quint_double_rows": f5twos})
    check("rank34_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[33]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[33]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[33]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[33]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})
    check("rank34_sextet_census_all_zero",
          six == {"b_only": 0, "zero": math.comb(RANK, 6), "disjoint": 0},
          {"total": math.comb(RANK, 6), **six})
    check("rank34_expected_totals",
          math.comb(RANK, 3) == 5984 and math.comb(IDX, 2) == 528
          and math.comb(IDX, 3) == 5456 and math.comb(IDX, 4) == 40920
          and math.comb(RANK, 5) == 278256 and math.comb(RANK, 6) == 1344904,
          {"C33_2": math.comb(IDX, 2), "C33_3": math.comb(IDX, 3), "C33_4": math.comb(IDX, 4),
           "C34_3": math.comb(RANK, 3), "C34_5": math.comb(RANK, 5), "C34_6": math.comb(RANK, 6)})
    check("rank34_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})

    rank34 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m34,
        "a_part": a34,
        "b_part": b34,
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "note": ("rank-34 (9,19) continues the single-share structure: row 9 has "
                 "exactly one prior sharer (index 21) and is covered for the "
                 "first time, while row 19 is now a nine-sharer hub band row "
                 "(indices 0,2,3,8,9,10,15,29,32). The new pair census is 10 "
                 "shared / 23 disjoint; row 9 appears in the triple (8 records) "
                 "and quad (11 records) double-row families but never in the "
                 "quint layer, whose double-row histogram stays within the four "
                 "hub rows 15/16/18/19. The 146 new disjoint quads all have "
                 "8-row unions (cumulative 1,112 = 966 + 146), the new b_only "
                 "quints are 2,171 (all 3/2/0 four-subset profiles, cumulative "
                 "13,004), and the C(34,6)=1,344,904 sextet census stays all "
                 "zero, so the quint inclusion-exclusion truncation carries "
                 "over to k=34."),
        "new_census": {
            "pair": {"shared": shared, "disjoint": pc["disjoint"],
                     "total": IDX, "expected_total": IDX},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(IDX, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(IDX, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(IDX, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "disjoint_quad_count": qc["disjoint"],
        "disjoint_quad_union_sizes": {str(k): v for k, v in sorted(dusizes.items())},
        "cumulative_disjoint_quads": 966 + qc["disjoint"],
        "full_triples": {"counts": ful3, "total": math.comb(RANK, 3),
                         "double_row_histogram": f3twos,
                         "compared": math.comb(RANK, 3), "mismatches": f3mis},
        "full_quints": {"counts": ful5, "total": math.comb(RANK, 5),
                        "double_row_histogram": f5twos,
                        "compared": math.comb(RANK, 5), "mismatches": f5mis},
        "sextet_census": {"total": math.comb(RANK, 6), "counts": six,
                          "compared": math.comb(RANK, 6), "mismatches": s6mis},
    }

    out = {
        "schema": "n11-cost16-k34-preread-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-34 structural preread",
        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33 preread scripts); the rank-32 regression layer "
                          "compares against the pinned published k=32 preread JSON and "
                          "the rank-33 regression layer against the pinned published "
                          "k=33 preread JSON because neither main result JSON is yet "
                          "published; the k=32 and k=33 main computations must still "
                          "pin their own results before k=33/k=34 main regresses "
                          "against them."),
        "inputs": {
            "aggregate": {"path": f"{PATH}/cost16-b-phase-groups-20261118.json",
                          "git_blob_sha1": PINS["agg"][1]},
            "k31_result": {"path": f"{PATH}/cost16-survival-k31-20261118.json",
                           "git_blob_sha1": PINS["k31"][1],
                           "commit": "5da4cc6c"},
            "k32_preread": {"path": f"{PATH}/cost16-survival-k32-preread-20261118.json",
                            "git_blob_sha1": PINS["k32pre"][1],
                            "commit": "490a3e44bc"},
            "k33_preread": {"path": f"{PATH}/cost16-survival-k33-preread-20261118.json",
                            "git_blob_sha1": PINS["k33pre"][1],
                            "commit": "67068e077"},
            "k33_preread_independent_verification": (
                "verify_cost16_k33_preread_independent_20261118.py, "
                "commit 2ae6b6b8, 29 checks 0 failures (second derivation lineage)"),
        },
        "scope": {
            "parent": PARENT_ROOT,
            "rows": R,
            "minimum_cover_size": 16,
            "top50_rank": RANK,
            "rank_convention": "top50_by_membership; 1-based rank 34",
        },
        "rank32_regression": reg[32],
        "rank33_regression": reg[33],
        "rank34": rank34,
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN; cover-plan "
                           "combinatorics only, no verdict is produced."),
    }

    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    # final check: exact integers survive the JSON round trip
    back = json.loads(text)
    ok = (back["rank34"]["membership"] == m34
          and back["rank34"]["a_part"] == a34 and back["rank34"]["b_part"] == b34
          and back["rank32_regression"]["membership"] == int(mem[31])
          and back["rank33_regression"]["membership"] == int(mem[32])
          and back["rank33_regression"]["a_part"] == int(memA[top[32]["root"]])
          and back["rank33_regression"]["b_part"] == int(memB[top[32]["root"]]))
    checks.append({"name": "rank34_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m34, "a_part": a34, "b_part": b34}})
    out["checks"] = checks
    out["check_count"] = len(checks)
    out["all_pass"] = all(c["pass"] for c in checks)
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"

    open(args.out, "w", encoding="utf-8").write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    for c in checks:
        print("PASS" if c["pass"] else "FAIL", c["name"])
    print(f"--- {len(checks)} checks, {sum(0 if c['pass'] else 1 for c in checks)} failures")
    print(f"rank-34 root {root} rows {sorted(rows[IDX])} m34 {m34} (A {a34} / B {b34})")
    print("new census: pair %d/%d  triple %d/%d/%d  quad %d/%d/%d  quint b%d/z%d/d%d"
          % (shared, pc["disjoint"], tc["b_only"], tc["zero"], tc["disjoint"],
             qc["b_only"], qc["zero"], qc["disjoint"], uc["b_only"], uc["zero"], uc["disjoint"]))
    print(f"full C(34,5): {ful5}  sextet C(34,6): {six}")
    print("output sha256:", sha)
    print("size:", len(text.encode('utf-8')), "bytes")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
