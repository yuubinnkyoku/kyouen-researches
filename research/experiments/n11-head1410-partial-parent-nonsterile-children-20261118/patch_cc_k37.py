#!/usr/bin/env python3
"""Anchored-rep machine transformation of the published k=36 crosscheck
(base blob 4d3036eff58ef30c9be9739e2e8a3e18cabbed5c14235e69b2c6900d7d4c6734,
main commit dfe8e6cc) into the k=37 edition: k=37 record and preread
layers, k=37 era closures, k=37 pins, and the docstring updates.
Every replacement asserts its exact occurrence count before running;
the output is py_compiled and probed for the expected k=37 literals.
"""
import hashlib
import py_compile
import sys

BASE_SHA256 = "4d3036eff58ef30c9be9739e2e8a3e18cabbed5c14235e69b2c6900d7d4c6734"

with open("base/cc36.py", "rb") as f:
    data = f.read()
if hashlib.sha256(data).hexdigest() != BASE_SHA256:
    print("ERROR: base cc36.py sha256 mismatch")
    sys.exit(1)
src = data.decode("utf-8")
orig_len = len(src)

REPS = []


def rep(old, new, count=1):
    REPS.append((old, new, count))


# 1. docstring header: append the k=37 publication record
rep(
    """pinned result JSON
b7a78e79bdc82c8097222ef2fd057e6b1a4b9350, record JSONL
7ba84693d302d2bc76851163fd3eb6a6fa7b0caa), verification
lane.
""",
    """pinned result JSON
b7a78e79bdc82c8097222ef2fd057e6b1a4b9350, record JSONL
7ba84693d302d2bc76851163fd3eb6a6fa7b0caa), verification
lane, and k=37 (script+log 8423c971, result JSON a4a7ce31,
per-record JSONL 9ff089ce; pinned result JSON
03084d81674e829015561351be799c8a757e7c7e, record JSONL
b5bf20215ef5578be1ebd605716473e21445296f), verification
lane.
""",
)

# 2. docstring record-layer range
rep(
    """  3. record layer (k=26 through k=35): each per-record JSONL is""",
    """  3. record layer (k=26 through k=37): each per-record JSONL is""",
)

# 3. docstring: layer 10 + fetch note
rep(
    """     preread_match.* checks must all be present and passing, and
     its rank36_root must equal the aggregate exactly.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=35 per-record JSONLs; for layer 4 the k=31 preread JSON""",
    """     preread_match.* checks must all be present and passing, and
     its rank36_root must equal the aggregate exactly.

  10. preread layer (k=37): the rank-37 structural preread JSON
     (pure Python with exact integer serialization, commit
     98321003, independently verified by a second bit-mask
     derivation lineage at commit 958057fb, with the exact-byte
     restoration erratum 059db03e) is fetched at its own pinned
     git blob sha1 and re-derived machine-side like layers
     5/6/7/8/9: row 8 has exactly one prior sharer among the
     top-36 (index 23, the rank-24 root (8,18)) while row 19 is
     now an 11-sharer hub band row (indices 0,2,3,8,9,10,15,29,
     32,33,35), so the (8,19) root makes row 8 the third
     single-share row to double (after row 7 at rank-33 and
     row 9 at rank-34): triple layer 8 records, quad layer 11,
     never the quint layer; all four new-layer censuses (pair
     12 shared / 24 disjoint), the three new-layer double-row
     histograms, the b_only four-subset profiles, the
     disjoint-quad fields (157 new, unions all 8, cumulative
     1,520 against a fresh full C(36,4) disjoint count), the
     full triple / quint / sextet censuses (all-zero 2,324,784
     sextets), both embedded regression blocks (rank-35 and
     rank-36) -- and, closing the same 3-system pattern as
     layers 6/7/8/9, the preread's rank-36 regression block is
     additionally compared field-by-field against the
     now-published k=36 result JSON structure fields; the
     published k=37 result JSON's preread_match.* checks must
     all be present and passing, and its rank37_root must
     equal the aggregate exactly.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=37 per-record JSONLs; for layer 4 the k=31 preread JSON""",
)

rep(
    """the k=35 preread JSON and for layer 9 the k=36 preread JSON) at
their""",
    """the k=35 preread JSON and for layer 9 the k=36 preread JSON
and for layer 10 the k=37 preread JSON) at
their""",
)

# 4. PINS: k=37 + k=37pre
rep(
    """    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "agg":""",
    """    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    # k=37 (published 2026-11-19, commits 8423c971 script+log,
    # a4a7ce31 result JSON and 9ff089ce record JSONL): the
    # published result JSON of the k=37 main computation, whose
    # 10,546-record layer and preread layer (script 900f68c3,
    # result 98321003, independently verified by the second
    # bit-mask lineage at 958057fb with the exact-byte restoration
    # erratum 059db03e) are cross-checked below (record layer +
    # preread layer 10); rerun by the long lane end-to-end with
    # the 52-check finalize passing byte-identically before
    # publication.
    "k37": ("cost16-survival-k37-20261119.json",
            "03084d81674e829015561351be799c8a757e7c7e"),
    # k=37 rank-37 structural preread (published 2026-11-19,
    # commit 98321003): pure Python with exact integer
    # serialization; cross-checked machine-side below (layer 10).
    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
    "agg":""",
)

# 5. JSONL_K37 constant
rep(
    """JSONL_K36 = ("cost16-survival-k36-20261118.jsonl", "7ba84693d302d2bc76851163fd3eb6a6fa7b0caa")
""",
    """JSONL_K36 = ("cost16-survival-k36-20261118.jsonl", "7ba84693d302d2bc76851163fd3eb6a6fa7b0caa")
# k=37 per-record JSONL (published 2026-11-19, commit 9ff089ce):
# 10,546 records = pair 36 + triple 630 + quad 7,140 + quint 2,722
# (b_only only; the 56,183 new zero quints are structural, joint
# 0) + anchors 10 (anchor4 = the two published disjoint quads
# (4,13,25,35)/(4,16,25,35) of the k=36 record layer x both
# lineages) + cross 8.  The rank-37 root (8,19) makes row 8 the
# third single-share row to double (triple layer 8 records, quad
# layer 11, quint layer 0 -- the row-7/rank-33 and row-9/rank-34
# pattern) while row 19 is now an 11-sharer hub whose rank-37
# membership includes the new root itself: the new pair census is
# 12 shared / 24 disjoint, the 157 new disjoint quads all have
# unions of exactly 8 rows, and row 19 overtakes row 18 again in
# the triple (246 vs 120), quad (1,214 vs 870) and, for the first
# time, quint (1,269 vs 1,043) new layers.
JSONL_K37 = ("cost16-survival-k37-20261119.jsonl", "b5bf20215ef5578be1ebd605716473e21445296f")
""",
)

# 6. --out default
rep(
    """    ap.add_argument("--out", default="output/cost16-k36-crosscheck-20261119.json",""",
    """    ap.add_argument("--out", default="output/cost16-k37-crosscheck-20261119.json",""",
)

# 7. value layer source + K
rep(
    """    V = js["k36"]["values"]  # contains the full k=1..36 series""",
    """    V = js["k37"]["values"]  # contains the full k=1..37 series""",
)
rep(
    """    K = 36
    checks = []""",
    """    K = 37
    checks = []""",
)

# 8. quint census loop + prev-layer identities
rep(
    """    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36):
        qn = {"b_only": 0, "zero": 0, "disjoint": 0}""",
    """    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37):
        qn = {"b_only": 0, "zero": 0, "disjoint": 0}""",
)
rep(
    """    # the whole quint era k=27..35.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),
                 (34, 33), (35, 34), (36, 35)):""",
    """    # the whole quint era k=27..36.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),
                 (34, 33), (35, 34), (36, 35), (37, 36)):""",
)

# 9. sextet loop + comment
rep(
    """    # row 19 becomes a ten-sharer hub that includes rank-36 itself)
    # with all 1,947,792 sextets still zero.
    sx_census = {}
    for n in (29, 30, 31, 32, 33, 34, 35, 36):""",
    """    # row 19 becomes a ten-sharer hub that includes rank-36 itself)
    # with all 1,947,792 sextets still zero, and row 8 doubles for
    # the first time at k=37 (the single-share rank-37 root (8,19),
    # triple and quad layers only, like rows 7/9 at ranks 33/34)
    # with all 2,324,784 sextets still zero.
    sx_census = {}
    for n in (29, 30, 31, 32, 33, 34, 35, 36, 37):""",
)

# 10. record layer comment + loop
rep(
    """    # ---- record layer (k=26 through k=35): each per-record JSONL is fetched""",
    """    # ---- record layer (k=26 through k=37): each per-record JSONL is fetched""",
)
rep(
    """    # layer disjoint quads; at k=36: (2,14,28,34)/(2,16,28,34),
    # the k=35 record layer disjoint quads).
    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),
                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),
                         (30, JSONL_K30, 2), (31, JSONL_K31, 2),
                         (32, JSONL_K32, 2), (33, JSONL_K33, 2),
                         (34, JSONL_K34, 2), (35, JSONL_K35, 2),
                         (36, JSONL_K36, 2)):""",
    """    # layer disjoint quads; at k=36: (2,14,28,34)/(2,16,28,34),
    # the k=35 record layer disjoint quads; at k=37:
    # (4,13,25,35)/(4,16,25,35), the k=36 record layer disjoint
    # quads).
    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),
                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),
                         (30, JSONL_K30, 2), (31, JSONL_K31, 2),
                         (32, JSONL_K32, 2), (33, JSONL_K33, 2),
                         (34, JSONL_K34, 2), (35, JSONL_K35, 2),
                         (36, JSONL_K36, 2), (37, JSONL_K37, 2)):""",
)

# 11. preread layer 10 code block, inserted between the layer-9 tail
# and the closure-comment block
rep(
    """                   (str(em36), str(ea36), str(eb36))))


    # Two closure checks added after the 201-check k=34 publication
    # (plus two more closing the k=35 era and two more closing the
    # k=36 era, appended below):""",
    """                   (str(em36), str(ea36), str(eb36))))

    # ---- preread layer 10 (k=37): the rank-37 structural preread
    # JSON (commit 98321003, pure Python with exact integer
    # serialization, independently verified by the second bit-mask
    # lineage at 958057fb with the exact-byte restoration erratum
    # 059db03e) is re-derived machine-side from the pinned
    # aggregate: root rows / hex and the row-8 / row-19 prior hit
    # indices (row 8 has a single prior sharer among the top-36,
    # index 23, the rank-24 root (8,18), so the (8,19) root makes
    # row 8 the third single-share row to double -- triple layer
    # 8 records, quad layer 11, never the quint layer, the
    # row-7/rank-33 and row-9/rank-34 pattern -- while row 19 is
    # now an 11-sharer hub band row that the rank-37 root itself
    # belongs to), all four new-layer censuses (pair shared/
    # disjoint schema 12/24), the three new-layer b_only
    # double-row histograms, the b_only quint four-subset
    # profiles, the disjoint-quad fields (157 new disjoint quads,
    # every union exactly 8 rows; cumulative 1,520 asserted
    # against a fresh full C(36,4) disjoint count, no hardcoded
    # constants), the full triple census with its double-row
    # histogram, the full quint census and the all-zero sextet
    # census (2,324,784), both embedded regression blocks
    # (rank-35 and rank-36) re-derived with the same combined
    # logic, and a closed 3-system comparison, same pattern as
    # layers 6/7/8/9: the preread's rank-36 regression block
    # against the now-published k=36 result JSON structure fields
    # (an independent third system: the preread's own load-time
    # asserts and the main lane's preread_match checks are the
    # other two).  The three large integers must be the exact
    # aggregate values satisfying A+B==M.
    pre37 = js["k37pre"]["rank37"]
    hits8b = sorted(i for i in range(36) if 8 in rows[i])
    hits19b = sorted(i for i in range(36) if 19 in rows[i])
    em37 = int(mem[36])
    ea37 = int(memA[top[36]["root"]])
    eb37 = int(memB[top[36]["root"]])
    checks.append(("k37preread_rank37_root_prior_hits_exact_ints",
                   pre37["root"] == top[36]["root"]
                   and sorted(pre37["rows"]) == sorted(rows[36])
                   and pre37["prior_hits"] == {"8": len(hits8b), "19": len(hits19b)}
                   and {k: sorted(v) for k, v in pre37["prior_hit_indices"].items()}
                   == {"8": hits8b, "19": hits19b}
                   and int(pre37["membership"]) == em37
                   and int(pre37["a_part"]) == ea37
                   and int(pre37["b_part"]) == eb37
                   and ea37 + eb37 == em37,
                   (len(hits8b), len(hits19b), (ea37, eb37, em37))))
    nc37 = pre37["new_census"]
    shared37 = sum(1 for i in range(36) if set(rows[i]) & set(rows[36]))
    m37_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(36), 2):
        m37_tri[classify(rows, (36,) + c)] += 1
    m37_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(36), 3):
        m37_quad[classify(rows, (36,) + c)] += 1
    nb5_37 = len(q_new_b_only[37])
    checks.append(("k37preread_new_layer_censuses_machine_rederived",
                   nc37["pair"] == {"shared": shared37, "disjoint": 36 - shared37,
                                    "total": 36, "expected_total": 36}
                   and nc37["triple"]["b_only"] == m37_tri["b_only"]
                   and nc37["triple"]["zero"] == m37_tri["zero"]
                   and nc37["triple"]["disjoint"] == m37_tri["disjoint"]
                   and nc37["triple"]["total"] == nc37["triple"]["expected_total"]
                   == math.comb(36, 2)
                   and nc37["quad"]["b_only"] == m37_quad["b_only"]
                   and nc37["quad"]["zero"] == m37_quad["zero"]
                   and nc37["quad"]["disjoint"] == m37_quad["disjoint"]
                   and nc37["quad"]["total"] == nc37["quad"]["expected_total"]
                   == math.comb(36, 3)
                   and nc37["quint"]["b_only"] == nb5_37
                   and nc37["quint"]["zero"] == math.comb(36, 4) - nb5_37
                   and nc37["quint"]["disjoint"] == 0
                   and nc37["quint"]["total"] == nc37["quint"]["expected_total"]
                   == math.comb(36, 4),
                   (nc37["pair"], m37_tri, m37_quad, nb5_37)))
    h_tri37 = {}
    h_quad37 = {}
    h_qt37 = {}
    for c in itertools.combinations(range(36), 2):
        cl, two = classify2(rows, (36,) + c)
        if cl == "b_only":
            h_tri37[two] = h_tri37.get(two, 0) + 1
    for c in itertools.combinations(range(36), 3):
        cl, two = classify2(rows, (36,) + c)
        if cl == "b_only":
            h_quad37[two] = h_quad37.get(two, 0) + 1
    for c in q_new_b_only[37]:
        cl, two = classify2(rows, c)
        h_qt37[two] = h_qt37.get(two, 0) + 1
    checks.append(("k37preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri37 == {int(k): v for k, v in pre37["new_triple_double_row_histogram"].items()}
                   and h_quad37 == {int(k): v for k, v in pre37["new_quad_double_row_histogram"].items()}
                   and h_qt37 == {int(k): v for k, v in pre37["new_quint_double_row_histogram"].items()},
                   (h_tri37, h_quad37, h_qt37)))
    prof37 = {}
    for c in q_new_b_only[37]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof37[key] = prof37.get(key, 0) + 1
    dq37_sizes = {}
    dq37_cnt = 0
    for c in itertools.combinations(range(36), 3):
        if classify(rows, (36,) + c) == "disjoint":
            dq37_cnt += 1
            u = set()
            for i in (36,) + c:
                u |= set(rows[i])
            dq37_sizes[len(u)] = dq37_sizes.get(len(u), 0) + 1
    dj36 = 0
    for c in itertools.combinations(range(36), 4):
        if classify(rows, c) == "disjoint":
            dj36 += 1
    checks.append(("k37preread_quint_profiles_and_disjoint_quad_fields",
                   prof37 == {str(k): v for k, v in pre37["b_only_quint_four_subset_profiles"].items()}
                   and pre37["disjoint_quad_count"] == dq37_cnt
                   and dq37_cnt == m37_quad["disjoint"]
                   and {int(k): v for k, v in pre37["disjoint_quad_union_sizes"].items()} == dq37_sizes
                   and pre37["cumulative_disjoint_quads"] == dj36 + dq37_cnt,
                   (prof37, dq37_cnt, dq37_sizes, dj36)))
    ft37 = pre37["full_triples"]
    ft37m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft37_twos = {}
    for c in itertools.combinations(range(37), 3):
        cl, two = classify2(rows, c)
        ft37m[cl] += 1
        if cl == "b_only":
            ft37_twos[two] = ft37_twos.get(two, 0) + 1
    fq37 = pre37["full_quints"]
    checks.append(("k37preread_full_triples_and_quints_machine_rederived",
                   ft37["counts"] == ft37m and ft37["total"] == math.comb(37, 3)
                   and ft37.get("compared") in (None, math.comb(37, 3))
                   and ft37.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft37["double_row_histogram"].items()} == ft37_twos
                   and fq37["counts"] == q_full[37] and fq37["total"] == math.comb(37, 5)
                   and fq37.get("compared") in (None, math.comb(37, 5))
                   and fq37.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq37["double_row_histogram"].items()} == q_twos[37],
                   (ft37m, ft37_twos)))
    sx37 = pre37["sextet_census"]
    checks.append(("k37preread_sextet_census_machine_rederived",
                   sx37["counts"] == sx_census[37] and sx37["total"] == math.comb(37, 6)
                   and sx37.get("compared") in (None, math.comb(37, 6))
                   and sx37.get("mismatches", 0) == 0,
                   sx_census[37]))
    r35b37_ok, r35b37_bad = regression_block_ok(js["k37pre"]["rank35_regression"], 34)
    checks.append(("k37preread_rank35_regression_block_machine_rederived",
                   r35b37_ok, r35b37_bad[:6]))
    r36b37_ok, r36b37_bad = regression_block_ok(js["k37pre"]["rank36_regression"], 35)
    checks.append(("k37preread_rank36_regression_block_machine_rederived",
                   r36b37_ok, r36b37_bad[:6]))
    # closed 3-system comparison, same pattern as layers 6/7/8/9: the
    # preread's rank-36 regression block against the now-published
    # k=36 result JSON structure fields.
    r36reg = js["k37pre"]["rank36_regression"]
    j36st = js["k36"]["structure"]
    qreg37 = r36reg["new_census"]["quad"]
    checks.append(("k37preread_rank36_regression_matches_published_k36_result",
                   r36reg["root"] == j36st["rank36_root"]["root"]
                   and sorted(r36reg["rows"]) == sorted(j36st["rank36_root"]["rows"])
                   and r36reg["full_triples"]["counts"] == j36st["triple_census_k36"]
                   and int(qreg37["b_only"]) == int(j36st["new_quad_census"]["b_only"])
                   and int(qreg37["zero"]) == int(j36st["new_quad_census"]["zero"])
                   and int(qreg37["disjoint"]) == int(j36st["new_quad_census"]["disjoint"])
                   and {k: int(v) for k, v in r36reg["full_quints"]["counts"].items()}
                   == {k: int(v) for k, v in j36st["quint_census_k36"].items()}
                   and {int(k): int(v) for k, v in r36reg["full_quints"]["double_row_histogram"].items()}
                   == {int(k): int(v) for k, v in j36st["quint_b_only_double_rows"].items()}
                   and {k: int(v) for k, v in r36reg["sextet_census"]["counts"].items()}
                   == {k: int(v) for k, v in j36st["sextet_census_k36"].items()}
                   and int(r36reg["membership"]) == int(j36st["rank36_root"]["membership"]),
                   None))
    j37 = js["k37"]
    pmatch37 = {c["name"]: c["pass"] for c in j37["checks"]}
    need37 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k37json_preread_match_checks_all_present_and_pass",
                   all(pmatch37.get(nm) is True for nm in need37), need37))
    checks.append(("k37json_rank37_root_exactly_matches_aggregate",
                   int(j37["structure"]["rank37_root"]["membership"]) == em37
                   and int(j37["structure"]["rank37_root"]["a_part"]) == ea37
                   and int(j37["structure"]["rank37_root"]["b_part"]) == eb37
                   and j37["structure"]["rank37_root"]["root"] == top[36]["root"],
                   (str(em37), str(ea37), str(eb37))))


    # Two closure checks added after the 201-check k=34 publication
    # (plus two more closing the k=35 era, two more closing the k=36
    # era and two more closing the k=37 era, appended below):""",
)

# 12. k=37 era closures, appended after the k=36 era closures
rep(
    """                   and {int(k): v for k, v in s36[\"quint_b_only_double_rows\"].items()} == q_twos[36],
                   None))

    n_fail = 0""",
    """                   and {int(k): v for k, v in s36[\"quint_b_only_double_rows\"].items()} == q_twos[36],
                   None))

    # Two more closure checks close the k=37 era the same way: the
    # k=37 preread's embedded regression blocks against their earlier
    # preread publications, and the rank-37 preread's full structural
    # fields against the published k=37 result JSON (which was
    # produced by the long lane from the same pinned inputs, with
    # the 52-check finalize passing and the record layer, result
    # JSON and JSONL all pinned at their own blob sha1s; the
    # preread was additionally verified by the second bit-mask
    # lineage at 958057fb, with the exact-byte restoration erratum
    # 059db03e).
    checks.append((\"k37preread_embedded_rank35_rank36_blocks_match_prior_prereads\",
                   regression_projection(js[\"k37pre\"][\"rank35_regression\"])
                   == regression_projection(js[\"k35pre\"][\"rank35\"])
                   and regression_projection(js[\"k37pre\"][\"rank36_regression\"])
                   == regression_projection(js[\"k36pre\"][\"rank36\"]),
                   None))
    s37 = j37[\"structure\"]
    checks.append((\"k37json_preread_structure_matches_published_result\",
                   s37[\"new_quad_census\"] == {k: nc37[\"quad\"][k] for k in (\"b_only\", \"zero\", \"disjoint\")}
                   and s37[\"new_quint_census\"] == {k: nc37[\"quint\"][k] for k in (\"b_only\", \"zero\", \"disjoint\")}
                   and s37[\"quints_zero_synth_count\"] == nc37[\"quint\"][\"zero\"]
                   and s37[\"triple_census_k37\"] == ft37[\"counts\"]
                   and s37[\"quint_census_k37\"] == fq37[\"counts\"]
                   and s37[\"sextet_census_k37\"] == sx37[\"counts\"]
                   and published_histogram(s37[\"new_triple_b_only_double_row_histogram\"]) == h_tri37
                   and published_histogram(s37[\"new_quad_b_only_double_row_histogram\"]) == h_quad37
                   and {int(k): v for k, v in s37[\"quint_b_only_double_rows\"].items()} == q_twos[37],
                   None))

    n_fail = 0""",
)

# 13. report section
rep(
    """        \"schema\": \"n11-cost16-k36-crosscheck-20261119-v1\",""",
    """        \"schema\": \"n11-cost16-k37-crosscheck-20261119-v1\",""",
)
rep(
    """        \"source_main_commit\": \"b1484dddb9e410c23f024d6759305b13b98afe1a\",""",
    """        \"source_main_commit\": \"dfe8e6cc877b132c52f766af790cf31735fba409\",""",
)
rep(
    """        \"source_note\": (\"k=36 edition: extends the k=35 crosscheck \"
                        \"(script published as commit a956245b) with the \"
                        \"k=36 record and preread layers and the k=36 era \"
                        \"closures (the k=36 main artifacts were verified \"
                        \"against their published blob sha1s before the \"
                        \"pins were recorded; preread reproduced on the \"
                        \"Proxmox runner)\"),""",
    """        \"source_note\": (\"k=37 edition: extends the k=36 crosscheck \"
                        \"(script published as commit f688d657) with the \"
                        \"k=37 record and preread layers and the k=37 era \"
                        \"closures (the k=37 main artifacts were verified \"
                        \"against their published blob sha1s before the \"
                        \"pins were recorded; preread independently \"
                        \"verified by the second bit-mask lineage at \"
                        \"958057fb, with the exact-byte restoration \"
                        \"erratum 059db03e)\"),""",
)
rep(
    """            \"k36_jsonl\": {\"file\": JSONL_K36[0], \"git_blob_sha1\": JSONL_K36[1]},
        },""",
    """            \"k36_jsonl\": {\"file\": JSONL_K36[0], \"git_blob_sha1\": JSONL_K36[1]},
            \"k37_jsonl\": {\"file\": JSONL_K37[0], \"git_blob_sha1\": JSONL_K37[1]},
        },""",
)

for i, (old, new, count) in enumerate(REPS, 1):
    found = src.count(old)
    if found != count:
        print(f"ERROR: rep {i} found {found} occurrences (expected {count}):")
        print(old[:200])
        sys.exit(1)
    src = src.replace(old, new, count)

with open("cc37.py", "w", encoding="utf-8") as f:
    f.write(src)
py_compile.compile("cc37.py", doraise=True)

# post-checks on the transformed output
probes = [
    '"k37": ("cost16-survival-k37-20261119.json",',
    '"k37pre": ("cost16-survival-k37-preread-20261119.json",',
    'JSONL_K37 = ("cost16-survival-k37-20261119.jsonl", "b5bf20215ef5578be1ebd605716473e21445296f")',
    "    K = 37\n",
    'V = js["k37"]["values"]',
    "(37, JSONL_K37, 2)",
    "k37preread_rank37_root_prior_hits_exact_ints",
    "k37json_preread_structure_matches_published_result",
    "n11-cost16-k37-crosscheck-20261119-v1",
    '"k37_jsonl"',
    "pre37 = js[\"k37pre\"][\"rank37\"]",
]
for p in probes:
    if p not in src:
        print("ERROR: probe missing:", p)
        sys.exit(1)
# stale-literal guards: the old edition's K must not survive anywhere
for stale in ("    K = 36\n", 'js["k36"]["values"]  # contains the full k=1..36 series'):
    if stale in src:
        print("ERROR: stale literal survived:", stale)
        sys.exit(1)
print(f"OK: {len(REPS)} anchored reps applied, {orig_len} -> {len(src)} bytes")
print("matches:", len([1 for m in __import__('re').finditer(r'checks\.append', src)]))
