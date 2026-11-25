#!/usr/bin/env python3
"""Rank-32 structural preread for the 31-row cost-16 parent survival lane.

Deterministic pure-Python preread (exact integer arithmetic, no pm
recomputation): re-derives the full structural census of the top-32
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-30 and
rank-31 structure layers (pinned k30/k31 result JSONs), and records
the rank-32 facts (root rows [15,23], prior hits, membership split,
new pair/triple/quad/quint censuses, full C(32,3)/C(32,5) censuses,
sextet C(32,6) census) needed by the k=32 main computation's
load/assert chain.

Python (not Node) deliberately: the k=31 preread JSON (commit
188106bb) printed its three big integers through Node's
double-rounded Number display and required an erratum block in the
k=31 result; this script asserts the exact aggregate integers round
trip through JSON on every run (check rank32_exact_integer_json_
serialization).

Two classifiers (dict-accumulate vs Counter-variant) must agree on
every enumerated combination. Fully deterministic: fixed insertion
order, no timestamps, so two runs produce byte-identical output.

Fetches all inputs at pinned git blob sha1s via the jsdelivr mirror
with a raw.githubusercontent.com fallback (a mirror serving
stale-but-wrong bytes fails the sha1 check and the next mirror is
tried), or from a local directory with --local DIR (sha1 checked).

Usage: python3 cost16_survival_k32_preread_20261118.py [--local DIR] [--out PATH]
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
import urllib.request

REPO = "yuubinnkyoku/kyouen-researches"
PATH = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
PINS = {
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
    "k30": ("cost16-survival-k30-20261118.json", "9c24e7a30ad213d3b7675e620ec606b00f73a330"),
    "k31": ("cost16-survival-k31-20261118.json", "0d9f67ee69ad4fb8aa37904ddbf6666745786807"),
}
PARENT_ROOT = "00000000000000003800000008001000"  # 31-row cost-16 parent
R = 31          # parent rows (fixed: rank-32 bans 31 pair roots)
RANK = 32       # 1-based top50 rank of the new root
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
    multi = []
    for i in combo:
        multi.extend(rows[i])
    total = len(multi)
    uniq = len(set(multi))
    pair_rows = sorted({r for r in multi if multi.count(r) == 2})
    trip_rows = sorted({r for r in set(multi) if multi.count(r) >= 3})
    if trip_rows:
        return "zero", None
    if len(pair_rows) == 1:
        return "b_only", pair_rows[0]
    if len(pair_rows) == 0 and total == uniq:
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
    ap.add_argument("--out", default="output/cost16-survival-k32-preread-20261118.json",
                    help="output JSON path")
    args = ap.parse_args()

    agg = fetch(*PINS["agg"], args.local)
    k30 = fetch(*PINS["k30"], args.local)
    k31 = fetch(*PINS["k31"], args.local)
    for tag, j in (("k30", k30), ("k31", k31)):
        if not j.get("all_pass"):
            print(f"FAIL {tag} all_pass is false")
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
    # 2. publication chain: k31 result pins the k30 JSON it consumed
    k30_pin_in_k31 = k31.get("inputs", {}).get("survival_k30_json", {}).get("git_blob_sha1")
    check("k31_declares_pinned_k30_input",
          k30_pin_in_k31 == PINS["k30"][1],
          {"declared": k30_pin_in_k31, "pinned": PINS["k30"][1]})

    # ---- rank-30 / rank-31 regression (published layers re-derived)
    reg = {}
    for n, js, (root_hex, m, a, b) in ((30, k30, ("00000000080008003800000008001000", "120210131097430568", None, None)),
                                         (31, k31, ("00000000000040809002001000100000", "120181378067473629", "92082202719887124", "28099175347586505"))):
        idx = n - 1
        rk = js["structure"][f"rank{n}_root"]
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
        new_quint_b_only = set()
        for c in itertools.combinations(range(idx), 4):
            cl, two = classify_a(rows, (idx,) + c)
            if cl == "b_only":
                new_quint_b_only.add((idx,) + c)
        # published comparison targets
        pub_pair = None
        pub_quad = js["structure"]["new_quad_census"]
        pub_newquint = js["structure"]["new_quint_census"]
        pub_tri = js["structure"][f"triple_census_k{n}"]
        pub_qui = js["structure"][f"quint_census_k{n}"]
        pub_hist = {int(k): v for k, v in js["structure"]["quint_b_only_double_rows"].items()}
        pub_zsc = int(js["structure"]["quints_zero_synth_count"])
        pub_six = js["structure"][f"sextet_census_k{n}"]
        for c in js["checks"]:
            if c["name"] == "pairs.new_census":
                pub_pair = c["detail"]
        ok_root = (rk["root"] == root_hex == top[idx]["root"]
                   and sorted(rk["rows"]) == sorted(rows[idx])
                   and int(rk["membership"]) == int(mem[idx]))
        if a is not None:
            ok_root = ok_root and int(rk["a_part"]) == int(a) and int(rk["b_part"]) == int(b)
        check(f"rank{n}_root_matches_published", ok_root,
              {"root": root_hex, "rows": sorted(rows[idx]), "membership": int(mem[idx])})
        check(f"rank{n}_new_census_matches_published",
              pub_pair is not None
              and pub_pair["shared"] == shared and pub_pair["disjoint"] == pc["disjoint"]
              and pub_quad == qc and pub_newquint == {"b_only": uc["b_only"], "zero": uc["zero"], "disjoint": uc["disjoint"]}
              and uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(idx, 4),
              {"pair": {"shared": shared, "disjoint": pc["disjoint"]},
               "triple": tc, "quad": qc, "quint": uc})
        check(f"rank{n}_full_census_matches_published",
              ful3 == pub_tri and ful5 == pub_qui and f5twos == pub_hist
              and pub_zsc == math.comb(n - 1, 4) - len(new_quint_b_only)
              and ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(n, 3)
              and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(n, 5),
              {"full_triples": ful3, "full_quints": ful5, "double_rows": f5twos,
               "quints_zero_synth": pub_zsc})
        check(f"rank{n}_sextet_census_all_zero_published",
              six == pub_six and six["b_only"] + six["zero"] + six["disjoint"] == math.comb(n, 6),
              six)
        check(f"rank{n}_two_classifiers_agree",
              pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
              {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
               "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})
        reg[n] = {
            "root": root_hex,
            "rows": sorted(rows[idx]),
            "membership": int(mem[idx]),
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
        if n == 31:
            # quint-era continuation inside the regression: the machine-derived
            # full(31) census minus the rank-31 new layer must equal the published
            # k=30 full quint census (independently of the crosscheck lane).
            check("quint_census_k31_prev_layer_equals_k30_published",
                  ful5["b_only"] - len(new_quint_b_only) == k30["structure"]["quint_census_k30"]["b_only"]
                  and ful5["zero"] - (math.comb(n - 1, 4) - len(new_quint_b_only))
                  == k30["structure"]["quint_census_k30"]["zero"]
                  and ful5["disjoint"] == 0,
                  {"new_b_only": len(new_quint_b_only), "full_k31": ful5,
                   "published_k30": k30["structure"]["quint_census_k30"]})

    # k=31 regression against its published marginal (m31 exact)
    check("rank31_membership_split_identity",
          int(mem[30]) == int(k31["structure"]["rank31_root"]["membership"])
          and int(memA[top[30]["root"]]) + int(memB[top[30]["root"]]) == int(mem[30]),
          {"membership": int(mem[30]), "a_part": int(memA[top[30]["root"]]),
           "b_part": int(memB[top[30]["root"]])})
    for c in k31["checks"]:
        if c["name"] == "survival.marginal":
            check("rank31_published_marginal_uses_exact_m31",
                  int(c["detail"]["m31"]) == int(mem[30])
                  and c["detail"]["k31_minus_k30"] == "52914484706624166",
                  c["detail"])

    # ---- rank-32 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m32 = int(mem[IDX])
    a32 = int(memA[root])
    b32 = int(memB[root])
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

    check("rank32_root_matches_top50",
          root == "00000000000000801222000000081000"
          and sorted(rows[IDX]) == [15, 23],
          {"root": root, "rows": sorted(rows[IDX])})
    check("rank32_prior_hits_recorded",
          prior == {15: [0, 13, 14, 16, 17, 22], 23: [11]},
          {str(k): v for k, v in sorted(prior.items())})
    check("rank32_membership_split_identity",
          a32 + b32 == m32 and m32 == 120146272057315812,
          {"membership": m32, "a_part": a32, "b_part": b32})
    check("rank32_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 7 and pc["disjoint"] == 24,
          {"shared": shared, "disjoint": pc["disjoint"], "total": IDX})
    check("rank32_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2), tc)
    check("rank32_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3), qc)
    check("rank32_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"], {**uc, "records": len(new_quint_b_only)})
    check("rank32_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 23 not in utwos, utwos)
    check("rank32_b_only_quint_profiles",
          profiles == {"3/2/0": uc["b_only"]}, profiles)
    check("rank32_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8},
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 662 + qc["disjoint"]})
    check("rank32_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"],
          {"full_triples": ful3, "full_quints": ful5, "quint_double_rows": f5twos})
    check("rank32_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[31]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[31]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0
          and (uc["b_only"] + reg[31]["full_quints"]["counts"]["b_only"] == ful5["b_only"]),
          {"prev_b_only": reg[31]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[31]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})
    check("rank32_sextet_census_all_zero",
          six == {"b_only": 0, "zero": math.comb(RANK, 6), "disjoint": 0},
          {"total": math.comb(RANK, 6), **six})
    check("rank32_expected_totals",
          math.comb(RANK, 3) == 4960 and math.comb(IDX, 2) == 465
          and math.comb(IDX, 3) == 4495 and math.comb(IDX, 4) == 31465
          and math.comb(RANK, 5) == 201376 and math.comb(RANK, 6) == 906192,
          {"C31_2": math.comb(IDX, 2), "C31_3": math.comb(IDX, 3), "C31_4": math.comb(IDX, 4),
           "C32_3": math.comb(RANK, 3), "C32_5": math.comb(RANK, 5), "C32_6": math.comb(RANK, 6)})
    check("rank32_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})

    rank32 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m32,
        "a_part": a32,
        "b_part": b32,
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "note": ("rank-32 (15,23) is a mid-hub root: row 15 is covered by 6 prior top "
                 "roots (indices 0,13,14,16,17,22), while row 23 has exactly one prior "
                 "sharer (index 11), so rank-32 is the first rank where row 23 doubles: "
                 "b_only records with doubled row 23 appear in the triple layer (9 "
                 "records) and the quad layer (12 records), but never in the quint "
                 "layer (a row-23 quint would need three further roots avoiding every "
                 "doubled-row family, which does not exist in the top-32). The new pair "
                 "census is 7 shared / 24 disjoint."),
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
        "cumulative_disjoint_quads": 662 + qc["disjoint"],
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
        "schema": "n11-cost16-k32-preread-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-32 structural preread",
        "language_note": ("pure Python with exact integer serialization; the k=31 preread "
                          "JSON (commit 188106bb) printed membership/a_part/b_part through "
                          "Node's double-rounded Number display and required an erratum "
                          "block in the k=31 result JSON; this preread asserts the exact "
                          "aggregate integers round-trip through JSON (final check)."),
        "inputs": {
            "aggregate": {"path": f"{PATH}/cost16-b-phase-groups-20261118.json",
                          "git_blob_sha1": PINS["agg"][1]},
            "k30_result": {"path": f"{PATH}/cost16-survival-k30-20261118.json",
                           "git_blob_sha1": PINS["k30"][1],
                           "commit": "f6a08dc5"},
            "k31_result": {"path": f"{PATH}/cost16-survival-k31-20261118.json",
                           "git_blob_sha1": PINS["k31"][1],
                           "commit": "5da4cc6c"},
            "k31_publication": ("script+log cf8d7dcc, result JSON 5da4cc6c, "
                                "record JSONL a4bef2aa, log bb0d6e3b"),
        },
        "scope": {
            "parent": PARENT_ROOT,
            "rows": R,
            "minimum_cover_size": 16,
            "top50_rank": RANK,
            "rank_convention": "top50_by_membership; 1-based rank 32",
        },
        "rank30_regression": reg[30],
        "rank31_regression": reg[31],
        "rank32": rank32,
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
    ok = (back["rank32"]["membership"] == m32
          and back["rank32"]["a_part"] == a32 and back["rank32"]["b_part"] == b32
          and back["rank30_regression"]["membership"] == int(mem[29])
          and back["rank31_regression"]["membership"] == int(mem[30]))
    checks.append({"name": "rank32_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m32, "a_part": a32, "b_part": b32}})
    out["checks"] = checks
    out["check_count"] = len(checks)
    out["all_pass"] = all(c["pass"] for c in checks)
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"

    open(args.out, "w", encoding="utf-8").write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    for c in checks:
        print("PASS" if c["pass"] else "FAIL", c["name"])
    print(f"--- {len(checks)} checks, {sum(0 if c['pass'] else 1 for c in checks)} failures")
    print(f"rank-32 root {root} rows {sorted(rows[IDX])} m32 {m32} (A {a32} / B {b32})")
    print("new census: pair %d/%d  triple %d/%d/%d  quad %d/%d/%d  quint b%d/z%d/d%d"
          % (shared, pc["disjoint"], tc["b_only"], tc["zero"], tc["disjoint"],
             qc["b_only"], qc["zero"], qc["disjoint"], uc["b_only"], uc["zero"], uc["disjoint"]))
    print(f"full C(32,5): {ful5}  sextet C(32,6): {six}")
    print("output sha256:", sha)
    print("size:", len(text.encode('utf-8')), "bytes")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
