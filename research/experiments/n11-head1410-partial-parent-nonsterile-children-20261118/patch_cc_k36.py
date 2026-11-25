#!/usr/bin/env python3
"""Machine transformation of the 231-check k=35 crosscheck (published as
commit a956245bfdca40a41b3145d291eedbd202d1259e, script git blob
a2df5648038ea9b3cecfce6d52ca5f1f9f01e764) into the k=36 edition: adds the
k=36 record layer, the rank-36 preread layer 9, the k=36 quint/sextet
structure censuses, the k=36 era closures, and the k=36 pins.  Every
replacement is anchored and count-asserted; the residual is audited so
no stale k=35-era reference leaks into the k=36 edition's values layer.
Usage: python3 patch_cc_k36.py <src.py> <dst.py>
"""
import sys

SRC, DST = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
orig_len = len(s)
reps = []


def rep(old, new, count=1):
    got = s.count(old)
    assert got == count, f"anchor count {got} != {count}: {old[:80]!r}"
    reps.append((old, new, count))


s_local = [s]


def apply(old, new):
    s_local[0] = s_local[0].replace(old, new)


# ---------- docstring: extend the k-series listing and add layer 9 ----------
rep("and k=35\n(script+log 141da801, log erratum bde016c4, result JSON 572b1365,\nper-record JSONL b1c73b50; pinned result JSON\n80a22ac77cdc0ba0a99643e3f1be13b71565a1b7, record JSONL\n89c15ec4fea859393dd673acde1654435f85bd01; rerun end-to-end by the\nverification lane with all values identical and 52-check finalize\npassing byte-identically twice before publication), verification\nlane.",
    "and k=35\n(script+log 141da801, log erratum bde016c4, result JSON 572b1365,\nper-record JSONL b1c73b50; pinned result JSON\n80a22ac77cdc0ba0a99643e3f1be13b71565a1b7, record JSONL\n89c15ec4fea859393dd673acde1654435f85bd01; rerun end-to-end by the\nverification lane with all values identical and 52-check finalize\npassing byte-identically twice before publication), and k=36\n(script+log 48dc73e6, transport erratum 21bf2cd2 restoring the\nexact blobs, result JSON 6fcea02c, per-record JSONL 0e96cde4;\npinned result JSON\nb7a78e79bdc82c8097222ef2fd057e6b1a4b9350, record JSONL\n7ba84693d302d2bc76851163fd3eb6a6fa7b0caa), verification\nlane.")

rep("     published k=35 result JSON's preread_match.* checks must\n     all be present and passing, and its rank35_root must equal\n     the aggregate exactly.\n\nFetches the published output JSONs",
    "     published k=35 result JSON's preread_match.* checks must\n     all be present and passing, and its rank35_root must equal\n     the aggregate exactly.\n\n  9. preread layer (k=36): the rank-36 structural preread JSON\n     (pure Python with exact integer serialization, commit\n     67985e92, reproduced byte-identically on the Proxmox runner at\n     commit fc46f01e) is fetched at its own pinned git blob sha1\n     and re-derived machine-side like layers 5/6/7/8: row 22 has\n     zero prior sharers among the top-35 (first-ever cover at\n     rank-36, so it can never double in any layer) while row 19 is\n     now a ten-sharer hub band row (indices 0,2,3,8,9,10,15,29,32,\n     33 -- the rank-36 root joins row 18/19 hub territory and ends\n     the two-rank fresh-row series of rows 21 and 22); all four\n     new-layer censuses (pair 10 shared / 25 disjoint, the largest\n     disjoint share of any rank so far), the three new-layer\n     double-row histograms, the b_only four-subset profiles, the\n     disjoint-quad fields (168 new, unions all 8, cumulative 1,363\n     against a fresh full C(35,4) disjoint count), the full triple\n     / quint / sextet censuses (all-zero 1,947,792 sextets), both\n     embedded regression blocks (rank-34 and rank-35) -- and,\n     closing the same 3-system pattern as layers 6/7/8, the\n     preread's rank-35 regression block is additionally compared\n     field-by-field against the now-published k=35 result JSON\n     structure fields; the published k=36 result JSON's\n     preread_match.* checks must all be present and passing, and\n     its rank36_root must equal the aggregate exactly.\n\nFetches the published output JSONs")

rep("k=26..k=34 per-record JSONLs; for layer 4 the k=31 preread JSON",
    "k=26..k=35 per-record JSONLs; for layer 4 the k=31 preread JSON")

rep("preread JSON and for layer 7 the k=34 preread JSON and for layer 8\nthe k=35 preread JSON) at their",
    "preread JSON and for layer 7 the k=34 preread JSON and for layer 8\nthe k=35 preread JSON and for layer 9 the k=36 preread JSON) at\ntheir")

# ---------- PINS: add k36 result and k36 preread ----------
rep("    \"k35pre\": (\"cost16-survival-k35-preread-20261118.json\",\n               \"490fa3a00b8e0b19229c94aa6b1aba4a5604ec13\"),\n    \"agg\":",
    "    \"k35pre\": (\"cost16-survival-k35-preread-20261118.json\",\n               \"490fa3a00b8e0b19229c94aa6b1aba4a5604ec13\"),\n    # k=36 (published 2026-11-19, commits 48dc73e6 script+log and\n    # 21bf2cd2 transport erratum restoring the exact blobs, result\n    # JSON commit 6fcea02c, record JSONL commit 0e96cde4): the\n    # published result JSON of the k=36 main computation, whose\n    # 10,028-record layer and preread layer (commit 67985e92,\n    # Proxmox reproduction fc46f01e) are cross-checked below\n    # (record layer + preread layer 9).\n    \"k36\": (\"cost16-survival-k36-20261118.json\",\n            \"b7a78e79bdc82c8097222ef2fd057e6b1a4b9350\"),\n    # k=36 rank-36 structural preread (published 2026-11-19,\n    # commit 67985e92): pure Python with exact integer\n    # serialization; cross-checked machine-side below (layer 9).\n    \"k36pre\": (\"cost16-survival-k36-preread-20261118.json\",\n               \"760aa396361cc7d2ea8bc371f4dd673d962f07fe\"),\n    \"agg\":")

# ---------- JSONL_K36 entry + structure comment ----------
rep("JSONL_K35 = (\"cost16-survival-k35-20261118.jsonl\", \"89c15ec4fea859393dd673acde1654435f85bd01\")",
    "JSONL_K35 = (\"cost16-survival-k35-20261118.jsonl\", \"89c15ec4fea859393dd673acde1654435f85bd01\")\n# k=36 per-record JSONL (published 2026-11-19, commit 0e96cde4):\n# 10,028 records = pair 35 + triple 595 + quad 6,545 + quint 2,835\n# (b_only only; the 49,525 new zero quints are structural, joint\n# 0) + anchors 10 (anchor4 = the two published disjoint quads\n# (2,14,28,34)/(2,16,28,34) of the k=35 record layer x both\n# lineages) + cross 8.  The rank-36 root (19,22) covers row 22\n# for the first time ever (zero prior sharers, so it never doubles\n# in any layer) while row 19 is now a ten-sharer hub whose rank-36\n# membership is itself a sharer: the new pair census is 10 shared /\n# 25 disjoint (the largest disjoint share yet), the 168 new\n# disjoint quads all have unions of exactly 8 rows, and row 19\n# overtakes row 18 as the dominant new double row in the triple\n# (232 vs 136) and quad (1,150 vs 992) layers while the new quint\n# layer keeps row 18 narrowly ahead (1,200 vs 1,195).\nJSONL_K36 = (\"cost16-survival-k36-20261118.jsonl\", \"7ba84693d302d2bc76851163fd3eb6a6fa7b0caa\")")

rep("stays all zero (the twelfth consecutive rank).\n\n\ndef git_blob_sha1",
    "stays all zero (the twelfth consecutive rank).  k=36 (C(36,5) =\n# 376,992: 17,434 b_only / 359,558 zero / 0 disjoint, the rank-36-new\n# layer being 2,835 b_only / 49,525 zero, cumulative double rows\n# 15:2785 / 16:545 / 18:9217 / 19:4887) is the hub root (19,22):\n# row 22 receives its first-ever cover (zero prior sharers, never\n# a double row) and row 19 is now a ten-sharer hub that the rank-36\n# root itself belongs to, the new pair census is 10 shared / 25\n# disjoint (the largest disjoint share of any rank so far), there\n# are 168 new disjoint quads (unions all 8, cumulative 1,363), row\n# 19 overtakes row 18 as the dominant new double row in the triple\n# and quad layers while the quint layer stays with row 18 (1,200 vs\n# 1,195), and the sextet census C(36,6) = 1,947,792 stays all zero\n# (the thirteenth consecutive rank).\n\n\ndef git_blob_sha1")

# ---------- value layer: source JSON and K ----------
rep("    V = js[\"k35\"][\"values\"]  # contains the full k=1..35 series",
    "    V = js[\"k36\"][\"values\"]  # contains the full k=1..36 series")
rep("    K = 35\n", "    K = 36\n")

# ---------- structure layer: quint / prev-layer / sextet loops ----------
rep("    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35):\n        qn = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}",
    "    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36):\n        qn = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}")
rep("    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),\n                 (34, 33), (35, 34)):",
    "    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),\n                 (34, 33), (35, 34), (36, 35)):")
rep("    for n in (29, 30, 31, 32, 33, 34, 35):\n        sx = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}",
    "    for n in (29, 30, 31, 32, 33, 34, 35, 36):\n        sx = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}")
rep("    # time at k=35 (the hub-band rank-35 root (18,21): a\n    # first-ever covered row can never double in any layer)\n    # with all 1,623,160 sextets still zero.",
    "    # time at k=35 (the hub-band rank-35 root (18,21): a\n    # first-ever covered row can never double in any layer)\n    # with all 1,623,160 sextets still zero, and row 22 is covered\n    # for the first time at k=36 (the hub rank-36 root (19,22):\n    # again a first-ever covered row that can never double, while\n    # row 19 becomes a ten-sharer hub that includes rank-36 itself)\n    # with all 1,947,792 sextets still zero.")

# ---------- record layer: loop tuple, comment ----------
rep("    # quads; at k=35: (4,13,25,33)/(4,16,25,33), the k=34 record\n    # layer disjoint quads).\n    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),\n                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),\n                         (30, JSONL_K30, 2), (31, JSONL_K31, 2),\n                         (32, JSONL_K32, 2), (33, JSONL_K33, 2),\n                         (34, JSONL_K34, 2), (35, JSONL_K35, 2)):",
    "    # quads; at k=35: (4,13,25,33)/(4,16,25,33), the k=34 record\n    # layer disjoint quads; at k=36: (2,14,28,34)/(2,16,28,34),\n    # the k=35 record layer disjoint quads).\n    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),\n                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),\n                         (30, JSONL_K30, 2), (31, JSONL_K31, 2),\n                         (32, JSONL_K32, 2), (33, JSONL_K33, 2),\n                         (34, JSONL_K34, 2), (35, JSONL_K35, 2),\n                         (36, JSONL_K36, 2)):")

# ---------- preread layer 9: insert after layer 8's last check ----------
LAYER9 = '''
    # ---- preread layer 9 (k=36): the rank-36 structural preread JSON
    # (commit 67985e92, pure Python with exact integer serialization,
    # reproduced byte-identically on the Proxmox runner at commit
    # fc46f01e) is re-derived machine-side from the pinned aggregate:
    # root rows / hex and the row-19 / row-22 prior hit indices (row
    # 22 has zero prior sharers among the top-35, a first-ever cover
    # at rank-36, so row 22 can never double in any layer; row 19 is
    # now a ten-sharer hub band row that the rank-36 root itself
    # belongs to, ending the fresh-row series of rows 21 and 22), all
    # four new-layer censuses (pair shared/disjoint schema 10/25, the
    # largest disjoint share of any rank so far), the three new-layer
    # b_only double-row histograms, the b_only quint four-subset
    # profiles, the disjoint-quad fields (168 new disjoint quads,
    # every union exactly 8 rows; cumulative 1,363 asserted against a
    # fresh full C(35,4) disjoint count, no hardcoded constants), the
    # full triple census with its double-row histogram, the full
    # quint census and the all-zero sextet census (1,947,792), both
    # embedded regression blocks (rank-34 and rank-35) re-derived with
    # the same combined logic, and a closed 3-system comparison, same
    # pattern as layers 6/7/8: the preread's rank-35 regression block
    # against the now-published k=35 result JSON structure fields (an
    # independent third system: the preread's own load-time asserts and
    # the main lane's preread_match checks are the other two).  The
    # three large integers must be the exact aggregate values
    # satisfying A+B==M.
    pre36 = js["k36pre"]["rank36"]
    hits19b = sorted(i for i in range(35) if 19 in rows[i])
    hits22 = sorted(i for i in range(35) if 22 in rows[i])
    em36 = int(mem[35])
    ea36 = int(memA[top[35]["root"]])
    eb36 = int(memB[top[35]["root"]])
    checks.append(("k36preread_rank36_root_prior_hits_exact_ints",
                   pre36["root"] == top[35]["root"]
                   and sorted(pre36["rows"]) == sorted(rows[35])
                   and pre36["prior_hits"] == {"19": len(hits19b), "22": len(hits22)}
                   and {k: sorted(v) for k, v in pre36["prior_hit_indices"].items()}
                   == {"19": hits19b, "22": hits22}
                   and int(pre36["membership"]) == em36
                   and int(pre36["a_part"]) == ea36
                   and int(pre36["b_part"]) == eb36
                   and ea36 + eb36 == em36,
                   (len(hits19b), len(hits22), (ea36, eb36, em36))))
    nc36 = pre36["new_census"]
    shared36 = sum(1 for i in range(35) if set(rows[i]) & set(rows[35]))
    m36_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(35), 2):
        m36_tri[classify(rows, (35,) + c)] += 1
    m36_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(35), 3):
        m36_quad[classify(rows, (35,) + c)] += 1
    nb5_36 = len(q_new_b_only[36])
    checks.append(("k36preread_new_layer_censuses_machine_rederived",
                   nc36["pair"] == {"shared": shared36, "disjoint": 35 - shared36,
                                    "total": 35, "expected_total": 35}
                   and nc36["triple"]["b_only"] == m36_tri["b_only"]
                   and nc36["triple"]["zero"] == m36_tri["zero"]
                   and nc36["triple"]["disjoint"] == m36_tri["disjoint"]
                   and nc36["triple"]["total"] == nc36["triple"]["expected_total"]
                   == math.comb(35, 2)
                   and nc36["quad"]["b_only"] == m36_quad["b_only"]
                   and nc36["quad"]["zero"] == m36_quad["zero"]
                   and nc36["quad"]["disjoint"] == m36_quad["disjoint"]
                   and nc36["quad"]["total"] == nc36["quad"]["expected_total"]
                   == math.comb(35, 3)
                   and nc36["quint"]["b_only"] == nb5_36
                   and nc36["quint"]["zero"] == math.comb(35, 4) - nb5_36
                   and nc36["quint"]["disjoint"] == 0
                   and nc36["quint"]["total"] == nc36["quint"]["expected_total"]
                   == math.comb(35, 4),
                   (nc36["pair"], m36_tri, m36_quad, nb5_36)))
    h_tri36 = {}
    h_quad36 = {}
    h_qt36 = {}
    for c in itertools.combinations(range(35), 2):
        cl, two = classify2(rows, (35,) + c)
        if cl == "b_only":
            h_tri36[two] = h_tri36.get(two, 0) + 1
    for c in itertools.combinations(range(35), 3):
        cl, two = classify2(rows, (35,) + c)
        if cl == "b_only":
            h_quad36[two] = h_quad36.get(two, 0) + 1
    for c in q_new_b_only[36]:
        cl, two = classify2(rows, c)
        h_qt36[two] = h_qt36.get(two, 0) + 1
    checks.append(("k36preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri36 == {int(k): v for k, v in pre36["new_triple_double_row_histogram"].items()}
                   and h_quad36 == {int(k): v for k, v in pre36["new_quad_double_row_histogram"].items()}
                   and h_qt36 == {int(k): v for k, v in pre36["new_quint_double_row_histogram"].items()},
                   (h_tri36, h_quad36, h_qt36)))
    prof36 = {}
    for c in q_new_b_only[36]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof36[key] = prof36.get(key, 0) + 1
    dq36_sizes = {}
    dq36_cnt = 0
    for c in itertools.combinations(range(35), 3):
        if classify(rows, (35,) + c) == "disjoint":
            dq36_cnt += 1
            u = set()
            for i in (35,) + c:
                u |= set(rows[i])
            dq36_sizes[len(u)] = dq36_sizes.get(len(u), 0) + 1
    dj35 = 0
    for c in itertools.combinations(range(35), 4):
        if classify(rows, c) == "disjoint":
            dj35 += 1
    checks.append(("k36preread_quint_profiles_and_disjoint_quad_fields",
                   prof36 == {str(k): v for k, v in pre36["b_only_quint_four_subset_profiles"].items()}
                   and pre36["disjoint_quad_count"] == dq36_cnt
                   and dq36_cnt == m36_quad["disjoint"]
                   and {int(k): v for k, v in pre36["disjoint_quad_union_sizes"].items()} == dq36_sizes
                   and pre36["cumulative_disjoint_quads"] == dj35 + dq36_cnt,
                   (prof36, dq36_cnt, dq36_sizes, dj35)))
    ft36 = pre36["full_triples"]
    ft36m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft36_twos = {}
    for c in itertools.combinations(range(36), 3):
        cl, two = classify2(rows, c)
        ft36m[cl] += 1
        if cl == "b_only":
            ft36_twos[two] = ft36_twos.get(two, 0) + 1
    fq36 = pre36["full_quints"]
    checks.append(("k36preread_full_triples_and_quints_machine_rederived",
                   ft36["counts"] == ft36m and ft36["total"] == math.comb(36, 3)
                   and ft36.get("compared") in (None, math.comb(36, 3))
                   and ft36.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft36["double_row_histogram"].items()} == ft36_twos
                   and fq36["counts"] == q_full[36] and fq36["total"] == math.comb(36, 5)
                   and fq36.get("compared") in (None, math.comb(36, 5))
                   and fq36.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq36["double_row_histogram"].items()} == q_twos[36],
                   (ft36m, ft36_twos)))
    sx36 = pre36["sextet_census"]
    checks.append(("k36preread_sextet_census_machine_rederived",
                   sx36["counts"] == sx_census[36] and sx36["total"] == math.comb(36, 6)
                   and sx36.get("compared") in (None, math.comb(36, 6))
                   and sx36.get("mismatches", 0) == 0,
                   sx_census[36]))
    r34b36_ok, r34b36_bad = regression_block_ok(js["k36pre"]["rank34_regression"], 33)
    checks.append(("k36preread_rank34_regression_block_machine_rederived",
                   r34b36_ok, r34b36_bad[:6]))
    r35b36_ok, r35b36_bad = regression_block_ok(js["k36pre"]["rank35_regression"], 34)
    checks.append(("k36preread_rank35_regression_block_machine_rederived",
                   r35b36_ok, r35b36_bad[:6]))
    # closed 3-system comparison, same pattern as layers 6/7/8: the
    # preread's rank-35 regression block against the now-published
    # k=35 result JSON structure fields.
    r35reg = js["k36pre"]["rank35_regression"]
    j35st = js["k35"]["structure"]
    qreg36 = r35reg["new_census"]["quad"]
    checks.append(("k36preread_rank35_regression_matches_published_k35_result",
                   r35reg["root"] == j35st["rank35_root"]["root"]
                   and sorted(r35reg["rows"]) == sorted(j35st["rank35_root"]["rows"])
                   and r35reg["full_triples"]["counts"] == j35st["triple_census_k35"]
                   and int(qreg36["b_only"]) == int(j35st["new_quad_census"]["b_only"])
                   and int(qreg36["zero"]) == int(j35st["new_quad_census"]["zero"])
                   and int(qreg36["disjoint"]) == int(j35st["new_quad_census"]["disjoint"])
                   and {k: int(v) for k, v in r35reg["full_quints"]["counts"].items()}
                   == {k: int(v) for k, v in j35st["quint_census_k35"].items()}
                   and {int(k): int(v) for k, v in r35reg["full_quints"]["double_row_histogram"].items()}
                   == {int(k): int(v) for k, v in j35st["quint_b_only_double_rows"].items()}
                   and {k: int(v) for k, v in r35reg["sextet_census"]["counts"].items()}
                   == {k: int(v) for k, v in j35st["sextet_census_k35"].items()}
                   and int(r35reg["membership"]) == int(j35st["rank35_root"]["membership"]),
                   None))
    j36 = js["k36"]
    pmatch36 = {c["name"]: c["pass"] for c in j36["checks"]}
    need36 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k36json_preread_match_checks_all_present_and_pass",
                   all(pmatch36.get(nm) is True for nm in need36), need36))
    checks.append(("k36json_rank36_root_exactly_matches_aggregate",
                   int(j36["structure"]["rank36_root"]["membership"]) == em36
                   and int(j36["structure"]["rank36_root"]["a_part"]) == ea36
                   and int(j36["structure"]["rank36_root"]["b_part"]) == eb36
                   and j36["structure"]["rank36_root"]["root"] == top[35]["root"],
                   (str(em36), str(ea36), str(eb36))))
'''
rep('''    checks.append(("k35json_rank35_root_exactly_matches_aggregate",
                   int(j35["structure"]["rank35_root"]["membership"]) == em35
                   and int(j35["structure"]["rank35_root"]["a_part"]) == ea35
                   and int(j35["structure"]["rank35_root"]["b_part"]) == eb35
                   and j35["structure"]["rank35_root"]["root"] == top[34]["root"],
                   (str(em35), str(ea35), str(eb35))))


    # Two closure checks added after the 201-check k=34 publication''',
    '''    checks.append(("k35json_rank35_root_exactly_matches_aggregate",
                   int(j35["structure"]["rank35_root"]["membership"]) == em35
                   and int(j35["structure"]["rank35_root"]["a_part"]) == ea35
                   and int(j35["structure"]["rank35_root"]["b_part"]) == eb35
                   and j35["structure"]["rank35_root"]["root"] == top[34]["root"],
                   (str(em35), str(ea35), str(eb35))))
''' + LAYER9 + '''

    # Two closure checks added after the 201-check k=34 publication''')

# ---------- closure: k36 era ----------
rep("    # Two closure checks added after the 201-check k=34 publication\n    # (plus two more closing the k=35 era, appended below):",
    "    # Two closure checks added after the 201-check k=34 publication\n    # (plus two more closing the k=35 era and two more closing the\n    # k=36 era, appended below):")
rep("                   and {int(k): v for k, v in s35[\"quint_b_only_double_rows\"].items()} == q_twos[35],\n                   None))",
    '''                   and {int(k): v for k, v in s35["quint_b_only_double_rows"].items()} == q_twos[35],
                   None))

    # Two more closure checks close the k=36 era the same way: the
    # k=36 preread's embedded regression blocks against their earlier
    # preread publications, and the rank-36 preread's full structural
    # fields against the published k=36 result JSON (which was
    # produced by the long verification lane from the same pinned
    # inputs, with the 52-check finalize passing and the record
    # layer, result JSON and JSONL all pinned at their own blob
    # sha1s, plus a Proxmox reproduction of the preread script).
    checks.append(("k36preread_embedded_rank34_rank35_blocks_match_prior_prereads",
                   regression_projection(js["k36pre"]["rank34_regression"])
                   == regression_projection(js["k34pre"]["rank34"])
                   and regression_projection(js["k36pre"]["rank35_regression"])
                   == regression_projection(js["k35pre"]["rank35"]),
                   None))
    s36 = j36["structure"]
    checks.append(("k36json_preread_structure_matches_published_result",
                   s36["new_quad_census"] == {k: nc36["quad"][k] for k in ("b_only", "zero", "disjoint")}
                   and s36["new_quint_census"] == {k: nc36["quint"][k] for k in ("b_only", "zero", "disjoint")}
                   and s36["quints_zero_synth_count"] == nc36["quint"]["zero"]
                   and s36["triple_census_k36"] == ft36["counts"]
                   and s36["quint_census_k36"] == fq36["counts"]
                   and s36["sextet_census_k36"] == sx36["counts"]
                   and published_histogram(s36["new_triple_b_only_double_row_histogram"]) == h_tri36
                   and published_histogram(s36["new_quad_b_only_double_row_histogram"]) == h_quad36
                   and {int(k): v for k, v in s36["quint_b_only_double_rows"].items()} == q_twos[36],
                   None))''')

# ---------- report / output ----------
rep('    ap.add_argument("--out", default="output/cost16-k35-crosscheck-20261119.json",',
    '    ap.add_argument("--out", default="output/cost16-k36-crosscheck-20261119.json",')
rep('        "schema": "n11-cost16-k35-crosscheck-20261119-v1",',
    '        "schema": "n11-cost16-k36-crosscheck-20261119-v1",')
rep('        "source_main_commit": "a2814ea0f1f802df1cff0fed86950d5ee0358dba",',
    '        "source_main_commit": "b1484dddb9e410c23f024d6759305b13b98afe1a",')
rep('''        "source_note": ("k=35 edition: extends the k=34 crosscheck "
                        "(script published as commit d7001467) with the k=35 "
                        "record and preread layers, and repairs the "
                        "transport-truncated tail that commit 2331d99e left "
                        "on main"),''',
    '''        "source_note": ("k=36 edition: extends the k=35 crosscheck "
                        "(script published as commit a956245b) with the "
                        "k=36 record and preread layers and the k=36 era "
                        "closures (the k=36 main artifacts were verified "
                        "against their published blob sha1s before the "
                        "pins were recorded; preread reproduced on the "
                        "Proxmox runner)"),''')
rep('            "k35_jsonl": {"file": JSONL_K35[0], "git_blob_sha1": JSONL_K35[1]},\n        },',
    '            "k35_jsonl": {"file": JSONL_K35[0], "git_blob_sha1": JSONL_K35[1]},\n            "k36_jsonl": {"file": JSONL_K36[0], "git_blob_sha1": JSONL_K36[1]},\n        },')

for old, new, _cnt in reps:
    apply(old, new)

s = s_local[0]
# residual audit: the values layer must no longer reference k35 as source
assert s.count('V = js["k36"]["values"]') == 1
assert 'V = js["k35"]' not in s
assert s.count("    K = 36\n") == 1
# every replaced anchor gave exactly one new occurrence
for old, new, cnt in reps:
    assert s.count(new) >= cnt
# record layer tuple covers 26..36
assert "(36, JSONL_K36, 2)):" in s
assert "(35, JSONL_K35, 2)," in s
# structure loops cover 36
assert "for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36):" in s
assert "for n in (29, 30, 31, 32, 33, 34, 35, 36):" in s
# preread layer 9 present exactly once
assert s.count('k36preread_rank36_root_prior_hits_exact_ints') == 1
assert s.count('k36preread_embedded_rank34_rank35_blocks_match_prior_prereads') == 1
assert s.count('k36json_preread_structure_matches_published_result') == 1
# pins present
assert '"k36": ("cost16-survival-k36-20261118.json"' in s
assert '"k36pre": ("cost16-survival-k36-preread-20261118.json"' in s
assert 'JSONL_K36 = ("cost16-survival-k36-20261118.jsonl", "7ba84693d302d2bc76851163fd3eb6a6fa7b0caa")' in s

open(DST, "w", encoding="utf-8").write(s)
print(f"transformed {orig_len} -> {len(s)} bytes, {len(reps)} anchored reps")
