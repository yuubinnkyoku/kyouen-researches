#!/usr/bin/env python3
"""Rank-38 structural preread for the 31-row cost-16 parent survival lane.

Deterministic pure-Python preread (exact integer arithmetic, no pm
recomputation): re-derives the full structural census of the top-38
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-36 preread
layer (pinned k36 preread JSON, commit 67985e92, reproduced
byte-identically on the Proxmox runner at commit fc46f01e) and the
published rank-37 preread layer (pinned k37 preread JSON, commit
98321003, independent bit-mask-vector second-derivation lineage commit
958057fb with erratum 059db03e), and records the rank-38 facts (root
rows [19,29], prior hits, membership split, new pair/triple/quad/quint
censuses, full C(38,3)/C(38,5) censuses, sextet C(38,6) census) needed
by the k=38 main computation's load/assert chain.  The k=36 and k=37
main result JSONs are already published (commits 6fcea02c / a4a7ce31)
and the k=36/k=37 crosscheck extensions are published (latest 287
checks, all pass, 2026-11-19), so the k=38 main computation pins the
published k=37 result and regresses against it in addition to this
preread.

Pure Python (following the k=32/k=33/k=34/k=35 preread scripts): all
large integers are exact and the final check asserts the exact
aggregate integers round trip through JSON on every run.

Two classifiers (dict-accumulate vs Counter-variant) must agree on
every enumerated combination. Fully deterministic: fixed insertion
order, no timestamps, so two runs produce byte-identical output.

Fetches all inputs at pinned git blob sha1s via the jsdelivr mirror
with a raw.githubusercontent.com fallback (a mirror serving
stale-but-wrong bytes fails the sha1 check and the next mirror is
tried), or from a local directory with --local DIR (sha1 checked).

Usage: python3 cost16_survival_k38_preread_20261119.py [--local DIR] [--out PATH]
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
    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
}
# sha1 the pinned k37 preread must declare for the k35 preread it
# consumed (publication chain: the k37 preread consumed the aggregate
# and the k35/k36 preread artifacts; k36 is pinned above)
K35PRE_SHA = "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"
PARENT_ROOT = "00000000000000003800000008001000"  # 31-row cost-16 parent
R = 31          # parent rows (fixed: new ranks ban one more pair root)
RANK = 38      # 1-based top50 rank of the new root
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
    ap.add_argument("--out", default="output/cost16-survival-k38-preread-20261119.json",
                    help="output JSON path")
    args = ap.parse_args()

    agg = fetch(*PINS["agg"], args.local)
    k36pre = fetch(*PINS["k36pre"], args.local)
    k37pre = fetch(*PINS["k37pre"], args.local)
    if not (k36pre.get("all_pass") and k36pre.get("check_count") == 33):
        print("FAIL k36 preread all_pass/check_count unexpected")
        return 1
    if not (k37pre.get("all_pass") and k37pre.get("check_count") == 34):
        print("FAIL k37 preread all_pass/check_count unexpected")
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
    # 2. publication chain: the pinned k37 preread declares the pinned
    #    aggregate, k35 preread and k36 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k37pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k37_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k35_preread") == K35PRE_SHA
          and in_pins.get("k36_preread") == PINS["k36pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k35pre": K35PRE_SHA, "pinned_k36pre": PINS["k36pre"][1]})

    # ---- rank-36 regression (vs the pinned published k36 preread JSON)
    reg = {}
    n = 36
    idx = n - 1
    pub36 = k36pre["rank36"]
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
          pub36["root"] == "00000000000000801212020000001000" == top[idx]["root"]
          and sorted(pub36["rows"]) == sorted(rows[idx]) == [19, 22]
          and int(pub36["membership"]) == int(mem[idx]) == 120046727515486665
          and int(pub36["a_part"]) == 92003630985566871
          and int(pub36["b_part"]) == 28043096529919794,
          {"root": pub36["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33], 22: []}
          and {k: sorted(v) for k, v in pub36["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub36["new_census"]["pair"]["shared"] == shared
          and pub36["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub36["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub36["new_census"]["triple"]["zero"] == tc["zero"]
          and pub36["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub36["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub36["new_census"]["quad"]["zero"] == qc["zero"]
          and pub36["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub36["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub36["new_census"]["quint"]["zero"] == uc["zero"]
          and pub36["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 391, "zero": 63, "disjoint": 141}
          and qc == {"b_only": 2458, "zero": 3919, "disjoint": 168}
          and uc == {"b_only": 2835, "zero": 49525, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub36["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub36["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub36["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub36["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub36["disjoint_quad_count"] == qc["disjoint"] == 168
          and {int(k): v for k, v in pub36["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub36["cumulative_disjoint_quads"] == 1195 + qc["disjoint"] == 1363,
          {"disjoint_union_sizes": dusizes, "cumulative": 1195 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub36["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 4361, "zero": 1320, "disjoint": 1459}
          and {int(k): v for k, v in pub36["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub36["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 17434, "zero": 359558, "disjoint": 0}
          and {int(k): v for k, v in pub36["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub36["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(36, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_k36_preread_rank35_regression",
          ful5["b_only"] - uc["b_only"] == 14599
          and k36pre["rank35_regression"]["full_quints"]["counts"]["b_only"] == 14599
          and ful5["zero"] - uc["zero"] == 310033
          and k36pre["rank35_regression"]["full_quints"]["counts"]["zero"] == 310033
          and ful5["disjoint"] == 0,
          {"prev_b_only": 14599,
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
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

    # ---- rank-37 regression (vs the pinned published k37 preread JSON)
    n = 37
    idx = n - 1
    pub37 = k37pre["rank37"]
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
          pub37["root"] == "00000000080000003800000108001000" == top[idx]["root"]
          and sorted(pub37["rows"]) == sorted(rows[idx]) == [8, 19]
          and int(pub37["membership"]) == int(mem[idx]) == 119973409932394637
          and int(pub37["a_part"]) == 91996175553485330
          and int(pub37["b_part"]) == 27977234378909307,
          {"root": pub37["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {8: [23], 19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35]}
          and {k: sorted(v) for k, v in pub37["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub37["new_census"]["pair"]["shared"] == shared
          and pub37["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub37["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub37["new_census"]["triple"]["zero"] == tc["zero"]
          and pub37["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub37["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub37["new_census"]["quad"]["zero"] == qc["zero"]
          and pub37["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub37["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub37["new_census"]["quint"]["zero"] == uc["zero"]
          and pub37["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 397, "zero": 100, "disjoint": 133}
          and qc == {"b_only": 2394, "zero": 4589, "disjoint": 157}
          and uc == {"b_only": 2722, "zero": 56183, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub37["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub37["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub37["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub37["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub37["disjoint_quad_count"] == qc["disjoint"] == 157
          and {int(k): v for k, v in pub37["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub37["cumulative_disjoint_quads"] == 1363 + qc["disjoint"] == 1520,
          {"disjoint_union_sizes": dusizes, "cumulative": 1363 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub37["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 4758, "zero": 1420, "disjoint": 1592}
          and {int(k): v for k, v in pub37["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub37["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 20156, "zero": 415741, "disjoint": 0}
          and {int(k): v for k, v in pub37["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub37["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(37, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_k37_preread_rank36_regression",
          ful5["b_only"] - uc["b_only"] == 17434
          and k37pre["rank36_regression"]["full_quints"]["counts"]["b_only"] == 17434
          and ful5["zero"] - uc["zero"] == 359558
          and k37pre["rank36_regression"]["full_quints"]["counts"]["zero"] == 359558
          and ful5["disjoint"] == 0,
          {"prev_b_only": 17434,
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
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

    # ---- rank-38 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m38 = int(mem[IDX])
    a38 = int(memA[root])
    b38 = int(memB[root])
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

    check("rank38_root_matches_top50",
          root == "00000008800000003800000008100000"
          and sorted(rows[IDX]) == [19, 29],
          {"root": root, "rows": sorted(rows[IDX])})
    check("rank38_prior_hits_recorded",
          prior == {19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35, 36], 29: [19]},
          {str(k): v for k, v in sorted(prior.items())})
    check("rank38_membership_split_identity",
          a38 + b38 == m38
          and m38 == 119940649042609991
          and m38 < int(reg[37]["membership"]),
          {"membership": m38, "a_part": a38, "b_part": b38})
    check("rank38_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 13 and pc["disjoint"] == 24,
          {"shared": shared, "disjoint": pc["disjoint"], "total": IDX})
    check("rank38_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 420, "zero": 113, "disjoint": 133}, tc)
    check("rank38_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 2519, "zero": 5094, "disjoint": 157}, qc)
    check("rank38_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"]
          and uc == {"b_only": 2868, "zero": 63177, "disjoint": 0},
          {**uc, "records": len(new_quint_b_only)})
    check("rank38_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 29 not in utwos and 19 in utwos
          and utwos == {15: 339, 16: 71, 18: 1043, 19: 1415}, utwos)
    check("rank38_b_only_quint_profiles",
          profiles == {"3/2/0": uc["b_only"]}, profiles)
    check("rank38_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 157,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 1520 + qc["disjoint"]})
    dj38 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")
    check("rank38_cumulative_disjoint_quads_global_recount",
          dj38 == 1677 and dj38 == 1520 + qc["disjoint"]
          and dj38 == pub37["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C38_4": dj38, "prev_cumulative": pub37["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})
    check("rank38_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 5178, "zero": 1533, "disjoint": 1725}
          and ful5 == {"b_only": 23024, "zero": 478918, "disjoint": 0}
          and f5twos == {15: 3463, 16: 687, 18: 11303, 19: 7571},
          {"full_triples": ful3, "full_quints": ful5, "quint_double_rows": f5twos})
    check("rank38_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[37]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[37]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[37]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[37]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})
    check("rank38_single_share_row_29_doubles_triple_quad_only",
          # row 29 appears before rank-38 only via index 19 (the rank-20
          # root (18,29), single share): it joins the double-row family
          # for the first time here, with 8 records in the triple layer
          # and 11 in the quad layer, never in the quint layer (the same
          # single-sharer doubling pattern as row 7 at rank-33, row 9 at
          # rank-34 and row 8 at rank-37)
          prior[29] == [19]
          and ttwos == {0: 1, 4: 1, 15: 15, 16: 3, 18: 120, 19: 269, 23: 1, 24: 1, 29: 8, 30: 1}
          and qtwos == {0: 15, 4: 2, 15: 245, 16: 31, 18: 870, 19: 1339, 23: 2, 24: 2, 29: 11, 30: 2}
          and 29 not in utwos,
          {"triple": ttwos, "quad": qtwos, "quint": utwos,
           "row29_prior_sharers": prior[29]})
    check("rank38_sextet_census_all_zero",
          six == {"b_only": 0, "zero": math.comb(RANK, 6), "disjoint": 0},
          {"total": math.comb(RANK, 6), **six})
    check("rank38_expected_totals",
          math.comb(RANK, 3) == 8436 and math.comb(IDX, 2) == 666
          and math.comb(IDX, 3) == 7770 and math.comb(IDX, 4) == 66045
          and math.comb(RANK, 5) == 501942 and math.comb(RANK, 6) == 2760681,
          {"C37_2": math.comb(IDX, 2), "C37_3": math.comb(IDX, 3), "C37_4": math.comb(IDX, 4),
           "C38_3": math.comb(RANK, 3), "C38_5": math.comb(RANK, 5), "C38_6": math.comb(RANK, 6)})
    check("rank38_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})

    rank38 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m38,
        "a_part": a38,
        "b_part": b38,
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "note": ("rank-38 (19,29) has no fresh row: row 29 arrives with a "
                 "single prior sharer (index 19, the rank-20 root (18,29)) "
                 "and doubles for the first time in the triple layer (8 "
                 "records) and the quad layer (11 records), never in the "
                 "quint layer (the same single-sharer doubling pattern as "
                 "row 7 at rank-33, row 9 at rank-34 and row 8 at "
                 "rank-37), while row 19 becomes a twelve-sharer hub band "
                 "row (prior sharers 0,2,3,8,9,10,15,29,32,33,35,36 -- "
                 "rank-37 itself is a sharer). The new pair census is 13 "
                 "shared / 24 disjoint (the shared pairs are exactly the "
                 "twelve row-19 sharers plus the one row-29 sharer, index "
                 "19). Row 19 stays the dominant double row of the new "
                 "layers and the new quint double-row histogram stays "
                 "within the four hub rows 15/16/18/19 (339/71/1,043/1,415; "
                 "row 29 absent). The 157 new disjoint quads all have "
                 "8-row unions (cumulative 1,677 = 1,520 + 157), the new "
                 "b_only quints are 2,868 (all 3/2/0 four-subset "
                 "profiles, cumulative 23,024 = 20,156 + 2,868 b_only in "
                 "C(38,5)), the full C(38,3)=8,436 census is "
                 "5,178/1,533/1,725 and the C(38,6)=2,760,681 sextet "
                 "census stays all zero, so the quint inclusion-exclusion "
                 "truncation carries over to k=38. The rank-36 and "
                 "rank-37 regression layers above re-derive the published "
                 "rank-36/rank-37 preread facts from the pinned aggregate, "
                 "and row 29's pattern gives the k=38 main computation the "
                 "same single-share structural bound as "
                 "k=33/k=34/k=37."),
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
        "cumulative_disjoint_quads": 1520 + qc["disjoint"],
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
        "schema": "n11-cost16-k38-preread-20261119-v1",
        "date": "2026-11-19",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-38 structural preread",
        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33/k=34/k=35/k=36/k=37 preread scripts); the rank-36 "
                          "regression layer compares against the pinned published k=36 "
                          "preread JSON and the rank-37 regression layer against the "
                          "pinned published k=37 preread JSON; the k=36 and k=37 main "
                          "result JSONs are already published (commits 6fcea02c / "
                          "a4a7ce31) and the k=36/k=37 crosscheck extensions are "
                          "published (latest 287 checks, all pass, 2026-11-19), so the "
                          "k=38 main computation pins the published k=37 result and "
                          "regresses against it as well; this preread carries the "
                          "single-share structural check over to row 29, so "
                          "check_count stays 34."),
        "inputs": {
            "aggregate": {"path": f"{PATH}/cost16-b-phase-groups-20261118.json",
                          "git_blob_sha1": PINS["agg"][1]},
            "k36_preread": {"path": f"{PATH}/cost16-survival-k36-preread-20261118.json",
                            "git_blob_sha1": PINS["k36pre"][1],
                            "commit": "67985e92"},
            "k37_preread": {"path": f"{PATH}/cost16-survival-k37-preread-20261119.json",
                            "git_blob_sha1": PINS["k37pre"][1],
                            "commit": "98321003"},
            "k36_preread_independent_verification": (
                "Proxmox runner reproduction (commit fc46f01e): the same script "
                "re-run produced byte-identical output"),
            "k37_preread_independent_verification": (
                "bit-mask-vector second derivation lineage (commit 958057fb, "
                "erratum 059db03e): the independent re-derivation agreed on "
                "every machine-derived fact"),
        },
        "scope": {
            "parent": PARENT_ROOT,
            "rows": R,
            "minimum_cover_size": 16,
            "top50_rank": RANK,
            "rank_convention": "top50_by_membership; 1-based rank 38",
        },
        "rank36_regression": reg[36],
        "rank37_regression": reg[37],
        "rank38": rank38,
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
    ok = (back["rank38"]["membership"] == m38
          and back["rank38"]["a_part"] == a38 and back["rank38"]["b_part"] == b38
          and back["rank36_regression"]["membership"] == int(mem[35])
          and back["rank37_regression"]["membership"] == int(mem[36])
          and back["rank36_regression"]["a_part"] == int(memA[top[35]["root"]])
          and back["rank36_regression"]["b_part"] == int(memB[top[35]["root"]])
          and back["rank37_regression"]["a_part"] == int(memA[top[36]["root"]])
          and back["rank37_regression"]["b_part"] == int(memB[top[36]["root"]]))
    checks.append({"name": "rank38_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m38, "a_part": a38, "b_part": b38}})
    out["checks"] = checks
    out["check_count"] = len(checks)
    out["all_pass"] = all(c["pass"] for c in checks)
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"

    open(args.out, "w", encoding="utf-8").write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    for c in checks:
        print("PASS" if c["pass"] else "FAIL", c["name"])
    print(f"--- {len(checks)} checks, {sum(0 if c['pass'] else 1 for c in checks)} failures")
    print(f"rank-38 root {root} rows {sorted(rows[IDX])} m38 {m38} (A {a38} / B {b38})")
    print("new census: pair %d/%d  triple %d/%d/%d  quad %d/%d/%d  quint b%d/z%d/d%d"
          % (shared, pc["disjoint"], tc["b_only"], tc["zero"], tc["disjoint"],
             qc["b_only"], qc["zero"], qc["disjoint"], uc["b_only"], uc["zero"], uc["disjoint"]))
    print(f"full C(38,5): {ful5}  sextet C(38,6): {six}")
    print("output sha256:", sha)
    print("size:", len(text.encode('utf-8')), "bytes")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
