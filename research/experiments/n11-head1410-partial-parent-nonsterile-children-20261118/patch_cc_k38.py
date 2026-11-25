#!/usr/bin/env python3
"""Anchored-rep machine transformation of the published k=37 crosscheck
(base blob sha1 3e1e9cbcd3c6b0e8f66dce9ab4ebebe2272da2e7, published at main
commit cb5714d3 with result fe8abfad, patch c430f75e, log 3cc3a8da) into
the k=38 edition: k=38 record and preread layers, k=38 era closures, k=38
pins, and the docstring updates.  Every replacement asserts its exact
occurrence count before running; the output is py_compiled and probed for
the expected k=38 literals.
"""
import hashlib
import py_compile
import sys

BASE_SHA256 = "eda88d670ac3947e52de873f905619385940990a5ef2436f66b3cece16c1048f"

with open("base/cc37.py", "rb") as f:
    data = f.read()
if hashlib.sha256(data).hexdigest() != BASE_SHA256:
    print("ERROR: base cc37.py sha256 mismatch:", hashlib.sha256(data).hexdigest())
    sys.exit(1)
src = data.decode("utf-8")
orig_len = len(src)

REPS = []


def rep(old, new, count=1):
    REPS.append((old, new, count))


# 1. docstring header: append the k=38 publication record
rep(
    """03084d81674e829015561351be799c8a757e7c7e, record JSONL
b5bf20215ef5578be1ebd605716473e21445296f), verification
lane.
""",
    """03084d81674e829015561351be799c8a757e7c7e, record JSONL
b5bf20215ef5578be1ebd605716473e21445296f), verification
lane, and k=38 (publication script 9d1b0a6a4c83, patch
aa3f78a28840, result JSON 78b6f1bd, per-record JSONL
b4ed53b2e, log cbade9c5e, second-execution agreement record
ec62057f4f; pinned result JSON
c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e, record JSONL
e8f9a8c9065bad3906a121f9bc816be6d299fb23), cross-check
lane.
""",
)

# 2. docstring record-layer range
rep(
    """  3. record layer (k=26 through k=37): each per-record JSONL is""",
    """  3. record layer (k=26 through k=38): each per-record JSONL is""",
)

# 3. docstring: layer 11 + fetch note
rep(
    """     published k=37 result JSON's preread_match.* checks must
     all be present and passing, and its rank37_root must
     equal the aggregate exactly.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=37 per-record JSONLs; for layer 4 the k=31 preread JSON""",
    """     published k=37 result JSON's preread_match.* checks must
     all be present and passing, and its rank37_root must
     equal the aggregate exactly.

  11. preread layer (k=38): the rank-38 structural preread JSON
     (pure Python with exact integer serialization, published
     2026-11-19: script commit 7d35406c, result commit 75fabfd0,
     anchored-rep patch 2cfb8705; independently verified by the
     bit-mask second lineage at commits 126614cc / f37ddd047 /
     e9a8a233 with a 48-check audit JSON and the verification
     log 5e0ef795) is fetched at its own pinned git blob sha1
     and re-derived machine-side like layers 5..10: row 29 has
     exactly one prior sharer among the top-37 (index 19, the
     rank-20 root (18,29)) while row 19 is now a 12-sharer hub
     band row (indices 0,2,3,8,9,10,15,29,32,33,35,36), so
     the (19,29) root makes row 29 the fourth single-share row
     to double (after rows 7/9/8 at ranks 33/34/37): triple
     layer 8 records, quad layer 11, never the quint layer --
     the first rank whose both root rows are already double
     rows; all four new-layer censuses (pair 13 shared /
     24 disjoint, the largest shared share of any rank so
     far), the three new-layer double-row histograms, the
     b_only four-subset profiles (all {3/2/0}), the
     disjoint-quad fields (157 new, unions all 8, cumulative
     1,677 against a fresh full C(37,4) disjoint count), the
     full triple / quint / sextet censuses (all-zero
     2,760,681 sextets), both embedded regression blocks
     (rank-36 and rank-37) -- and, closing the same 3-system
     pattern as layers 6/7/8/9/10, the preread's rank-37
     regression block is additionally compared field-by-field
     against the now-published k=37 result JSON structure
     fields; the published k=38 result JSON's preread_match.*
     checks must all be present and passing, and its rank38_root
     must equal the aggregate exactly.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=38 per-record JSONLs; for layer 4 the k=31 preread JSON""",
)

rep(
    """the k=35 preread JSON and for layer 9 the k=36 preread JSON
and for layer 10 the k=37 preread JSON) at
their""",
    """the k=35 preread JSON and for layer 9 the k=36 preread JSON
and for layer 10 the k=37 preread JSON and for layer 11 the
k=38 preread JSON) at
their""",
)

# 4. PINS: k=38 + k=38pre
rep(
    """    \"k37pre\": (\"cost16-survival-k37-preread-20261119.json\",
               \"b98ed685e772eacbd28dc3100e9813e81c27040a\"),
    \"agg\": (\"cost16-b-phase-groups-20261118.json\", \"31bdefdb2e2cc90b706cbb8090e98eb5eece4d87\"),""",
    """    \"k37pre\": (\"cost16-survival-k37-preread-20261119.json\",
               \"b98ed685e772eacbd28dc3100e9813e81c27040a\"),
    # k=38 (published 2026-11-19, single-owner main-lane
    # publication per the concurrency note 112a3247: result JSON
    # commit 78b6f1bd, per-record JSONL commit b4ed53b2, log
    # cbade9c5e, second-execution agreement record ec62057f4f):
    # the published result JSON of the k=38 main computation,
    # whose 11,359-record layer and preread layer (script
    # 7d35406c, result 75fabfd0, patch 2cfb8705, independently
    # verified by the bit-mask second lineage at
    # 126614cc/f37ddd047/e9a8a233 with the verification log
    # 5e0ef795) are cross-checked below (record layer + preread
    # layer 11).
    \"k38\": (\"cost16-survival-k38-20261119.json\",
            \"c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e\"),
    # k=38 rank-38 structural preread (published 2026-11-19,
    # commits 7d35406c script and 75fabfd0 result): pure Python
    # with exact integer serialization; cross-checked
    # machine-side below (layer 11).
    \"k38pre\": (\"cost16-survival-k38-preread-20261119.json\",
               \"3fa8297990d8e9880f386a0cfa075e3a95f226fd\"),
    \"agg\": (\"cost16-b-phase-groups-20261118.json\", \"31bdefdb2e2cc90b706cbb8090e98eb5eece4d87\"),""",
)

# 5. JSONL_K38 definition after JSONL_K37
rep(
    """JSONL_K37 = (\"cost16-survival-k37-20261119.jsonl\", \"b5bf20215ef5578be1ebd605716473e21445296f\")""",
    """JSONL_K37 = (\"cost16-survival-k37-20261119.jsonl\", \"b5bf20215ef5578be1ebd605716473e21445296f\")
# k=38 per-record JSONL (published 2026-11-19, commit b4ed53b2):
# 11,359 records = pair 37 + triple 666 + quad 7,770 + quint
# 2,868 (b_only only; the 63,177 new zero quints are structural,
# joint 0) + anchors 10 (anchor4 = the two published disjoint
# quads (4,13,25,36)/(4,16,25,36) of the k=37 record layer
# x both lineages) + cross 8.  The rank-38 root (19,29) makes
# row 29 the fourth single-share row to double (triple layer
# 8 records, quad layer 11, never the quint layer -- the
# row-7/rank-33, row-9/rank-34 and row-8/rank-37 pattern)
# while row 19 is now a 12-sharer hub whose rank-38 membership
# includes the new root itself: the new pair census is 13
# shared / 24 disjoint (the largest shared share of any rank
# so far), the 13 shared pairs all have joint_A == 0, the 157
# new disjoint quads all have unions of exactly 8 rows
# (cumulative 1,677), and the new quint double-row histogram
# keeps row 19 ahead ({15: 339, 16: 71, 18: 1,043, 19: 1,415}).
JSONL_K38 = (\"cost16-survival-k38-20261119.jsonl\", \"e8f9a8c9065bad3906a121f9bc816be6d299fb23\")""",
)

# 6. values source and K
rep(
    """    V = js[\"k37\"][\"values\"]  # contains the full k=1..37 series""",
    """    V = js[\"k38\"][\"values\"]  # contains the full k=1..38 series""",
)
rep(
    """    K = 37""",
    """    K = 38""",
)

# 7. quint census loop includes k=38
rep(
    """    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37):""",
    """    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38):""",
)

# 8. consecutive-era identities extend to (38, 37)
rep(
    """    # zero) must equal the full census of the previous rank, for
    # the whole quint era k=27..36.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),
                 (34, 33), (35, 34), (36, 35), (37, 36)):""",
    """    # zero) must equal the full census of the previous rank, for
    # the whole quint era k=27..37.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),
                 (34, 33), (35, 34), (36, 35), (37, 36), (38, 37)):""",
)

# 9. sextet comment tail + census loop includes k=38
rep(
    """    # the first time at k=37 (the single-share rank-37 root (8,19),
    # triple and quad layers only, like rows 7/9 at ranks 33/34)
    # with all 2,324,784 sextets still zero.
    sx_census = {}
    for n in (29, 30, 31, 32, 33, 34, 35, 36, 37):""",
    """    # the first time at k=37 (the single-share rank-37 root (8,19),
    # triple and quad layers only, like rows 7/9 at ranks 33/34)
    # with all 2,324,784 sextets still zero, and row 29 doubles
    # for the first time at k=38 (the single-share rank-38 root
    # (19,29), again triple and quad layers only) with all
    # 2,760,681 sextets still zero.
    sx_census = {}
    for n in (29, 30, 31, 32, 33, 34, 35, 36, 37, 38):""",
)

# 10. record layer: k=38 entry + anchor comment
rep(
    """                         (36, JSONL_K36, 2), (37, JSONL_K37, 2)):""",
    """                         (36, JSONL_K36, 2), (37, JSONL_K37, 2),
                         (38, JSONL_K38, 2)):""",
)
rep(
    """    # the k=35 record layer disjoint quads; at k=37:
    # (4,13,25,35)/(4,16,25,35), the k=36 record layer disjoint
    # quads).""",
    """    # the k=35 record layer disjoint quads; at k=37:
    # (4,13,25,35)/(4,16,25,35), the k=36 record layer disjoint
    # quads; at k=38: (4,13,25,36)/(4,16,25,36), the k=37
    # record layer disjoint quads).""",
)

# 11. preread layer 11 (k=38): full block after the k=37 layer
rep(
    """                   and j37[\"structure\"][\"rank37_root\"][\"root\"] == top[36][\"root\"],
                   (str(em37), str(ea37), str(eb37))))


    # Two closure checks added after the 201-check k=34 publication""",
    """                   and j37[\"structure\"][\"rank37_root\"][\"root\"] == top[36][\"root\"],
                   (str(em37), str(ea37), str(eb37))))

    # ---- preread layer 11 (k=38): the rank-38 structural preread
    # JSON (published 2026-11-19: script commit 7d35406c, result
    # commit 75fabfd0, anchored-rep patch 2cfb8705; pure Python
    # with exact integer serialization, independently verified by
    # the bit-mask second lineage at commits 126614cc /
    # f37ddd047 / e9a8a233 with the 48-check audit JSON and the
    # verification log 5e0ef795) is re-derived machine-side from
    # the pinned aggregate: root rows / hex and the row-19 /
    # row-29 prior hit indices (row 29 has a single prior sharer
    # among the top-37, index 19, the rank-20 root (18,29), so
    # the (19,29) root makes row 29 the fourth single-share row
    # to double -- triple layer 8 records, quad layer 11, never
    # the quint layer, the row-7/rank-33, row-9/rank-34 and
    # row-8/rank-37 pattern -- while row 19 is now a 12-sharer
    # hub band row that the rank-38 root itself belongs to),
    # all four new-layer censuses (pair shared/disjoint schema
    # 13/24, the largest shared share of any rank so far), the
    # three new-layer b_only double-row histograms, the b_only
    # quint four-subset profiles (all {3/2/0}), the
    # disjoint-quad fields (157 new disjoint quads, every union
    # exactly 8 rows; cumulative 1,677 asserted against a fresh
    # full C(37,4) disjoint count, no hardcoded constants), the
    # full triple census with its double-row histogram, the full
    # quint census and the all-zero sextet census (2,760,681),
    # both embedded regression blocks (rank-36 and rank-37)
    # re-derived with the same combined logic, and a closed
    # 3-system comparison, same pattern as layers 6/7/8/9/10:
    # the preread's rank-37 regression block against the
    # now-published k=37 result JSON structure fields.  The
    # three large integers must be the exact aggregate values
    # satisfying A+B==M.
    pre38 = js[\"k38pre\"][\"rank38\"]
    hits19c = sorted(i for i in range(37) if 19 in rows[i])
    hits29c = sorted(i for i in range(37) if 29 in rows[i])
    em38 = int(mem[37])
    ea38 = int(memA[top[37][\"root\"]])
    eb38 = int(memB[top[37][\"root\"]])
    checks.append((\"k38preread_rank38_root_prior_hits_exact_ints\",
                   pre38[\"root\"] == top[37][\"root\"]
                   and sorted(pre38[\"rows\"]) == sorted(rows[37])
                   and pre38[\"prior_hits\"] == {\"19\": len(hits19c), \"29\": len(hits29c)}
                   and {k: sorted(v) for k, v in pre38[\"prior_hit_indices\"].items()}
                   == {\"19\": hits19c, \"29\": hits29c}
                   and int(pre38[\"membership\"]) == em38
                   and int(pre38[\"a_part\"]) == ea38
                   and int(pre38[\"b_part\"]) == eb38
                   and ea38 + eb38 == em38,
                   (len(hits19c), len(hits29c), (ea38, eb38, em38))))
    nc38 = pre38[\"new_census\"]
    shared38 = sum(1 for i in range(37) if set(rows[i]) & set(rows[37]))
    m38_tri = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}
    for c in itertools.combinations(range(37), 2):
        m38_tri[classify(rows, (37,) + c)] += 1
    m38_quad = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}
    for c in itertools.combinations(range(37), 3):
        m38_quad[classify(rows, (37,) + c)] += 1
    nb5_38 = len(q_new_b_only[38])
    checks.append((\"k38preread_new_layer_censuses_machine_rederived\",
                   nc38[\"pair\"] == {\"shared\": shared38, \"disjoint\": 37 - shared38,
                                    \"total\": 37, \"expected_total\": 37}
                   and nc38[\"triple\"][\"b_only\"] == m38_tri[\"b_only\"]
                   and nc38[\"triple\"][\"zero\"] == m38_tri[\"zero\"]
                   and nc38[\"triple\"][\"disjoint\"] == m38_tri[\"disjoint\"]
                   and nc38[\"triple\"][\"total\"] == nc38[\"triple\"][\"expected_total\"]
                   == math.comb(37, 2)
                   and nc38[\"quad\"][\"b_only\"] == m38_quad[\"b_only\"]
                   and nc38[\"quad\"][\"zero\"] == m38_quad[\"zero\"]
                   and nc38[\"quad\"][\"disjoint\"] == m38_quad[\"disjoint\"]
                   and nc38[\"quad\"][\"total\"] == nc38[\"quad\"][\"expected_total\"]
                   == math.comb(37, 3)
                   and nc38[\"quint\"][\"b_only\"] == nb5_38
                   and nc38[\"quint\"][\"zero\"] == math.comb(37, 4) - nb5_38
                   and nc38[\"quint\"][\"disjoint\"] == 0
                   and nc38[\"quint\"][\"total\"] == nc38[\"quint\"][\"expected_total\"]
                   == math.comb(37, 4),
                   (nc38[\"pair\"], m38_tri, m38_quad, nb5_38)))
    h_tri38 = {}
    h_quad38 = {}
    h_qt38 = {}
    for c in itertools.combinations(range(37), 2):
        cl, two = classify2(rows, (37,) + c)
        if cl == \"b_only\":
            h_tri38[two] = h_tri38.get(two, 0) + 1
    for c in itertools.combinations(range(37), 3):
        cl, two = classify2(rows, (37,) + c)
        if cl == \"b_only\":
            h_quad38[two] = h_quad38.get(two, 0) + 1
    for c in q_new_b_only[38]:
        cl, two = classify2(rows, c)
        h_qt38[two] = h_qt38.get(two, 0) + 1
    checks.append((\"k38preread_new_layer_double_row_histograms_machine_rederived\",
                   h_tri38 == {int(k): v for k, v in pre38[\"new_triple_double_row_histogram\"].items()}
                   and h_quad38 == {int(k): v for k, v in pre38[\"new_quad_double_row_histogram\"].items()}
                   and h_qt38 == {int(k): v for k, v in pre38[\"new_quint_double_row_histogram\"].items()},
                   (h_tri38, h_quad38, h_qt38)))
    prof38 = {}
    for c in q_new_b_only[38]:
        p = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = \"%d/%d/%d\" % (p[\"b_only\"], p[\"disjoint\"], p[\"zero\"])
        prof38[key] = prof38.get(key, 0) + 1
    dq38_sizes = {}
    dq38_cnt = 0
    for c in itertools.combinations(range(37), 3):
        if classify(rows, (37,) + c) == \"disjoint\":
            dq38_cnt += 1
            u = set()
            for i in (37,) + c:
                u |= set(rows[i])
            dq38_sizes[len(u)] = dq38_sizes.get(len(u), 0) + 1
    dj37 = 0
    for c in itertools.combinations(range(37), 4):
        if classify(rows, c) == \"disjoint\":
            dj37 += 1
    checks.append((\"k38preread_quint_profiles_and_disjoint_quad_fields\",
                   prof38 == {str(k): v for k, v in pre38[\"b_only_quint_four_subset_profiles\"].items()}
                   and pre38[\"disjoint_quad_count\"] == dq38_cnt
                   and dq38_cnt == m38_quad[\"disjoint\"]
                   and {int(k): v for k, v in pre38[\"disjoint_quad_union_sizes\"].items()} == dq38_sizes
                   and pre38[\"cumulative_disjoint_quads\"] == dj37 + dq38_cnt,
                   (prof38, dq38_cnt, dq38_sizes, dj37)))
    ft38 = pre38[\"full_triples\"]
    ft38m = {\"b_only\": 0, \"zero\": 0, \"disjoint\": 0}
    ft38_twos = {}
    for c in itertools.combinations(range(38), 3):
        cl, two = classify2(rows, c)
        ft38m[cl] += 1
        if cl == \"b_only\":
            ft38_twos[two] = ft38_twos.get(two, 0) + 1
    fq38 = pre38[\"full_quints\"]
    checks.append((\"k38preread_full_triples_and_quints_machine_rederived\",
                   ft38[\"counts\"] == ft38m and ft38[\"total\"] == math.comb(38, 3)
                   and ft38.get(\"compared\") in (None, math.comb(38, 3))
                   and ft38.get(\"mismatches\", 0) == 0
                   and {int(k): v for k, v in ft38[\"double_row_histogram\"].items()} == ft38_twos
                   and fq38[\"counts\"] == q_full[38] and fq38[\"total\"] == math.comb(38, 5)
                   and fq38.get(\"compared\") in (None, math.comb(38, 5))
                   and fq38.get(\"mismatches\", 0) == 0
                   and {int(k): v for k, v in fq38[\"double_row_histogram\"].items()} == q_twos[38],
                   (ft38m, ft38_twos)))
    sx38 = pre38[\"sextet_census\"]
    checks.append((\"k38preread_sextet_census_machine_rederived\",
                   sx38[\"counts\"] == sx_census[38] and sx38[\"total\"] == math.comb(38, 6)
                   and sx38.get(\"compared\") in (None, math.comb(38, 6))
                   and sx38.get(\"mismatches\", 0) == 0,
                   sx_census[38]))
    r36b38_ok, r36b38_bad = regression_block_ok(js[\"k38pre\"][\"rank36_regression\"], 35)
    checks.append((\"k38preread_rank36_regression_block_machine_rederived\",
                   r36b38_ok, r36b38_bad[:6]))
    r37b38_ok, r37b38_bad = regression_block_ok(js[\"k38pre\"][\"rank37_regression\"], 36)
    checks.append((\"k38preread_rank37_regression_block_machine_rederived\",
                   r37b38_ok, r37b38_bad[:6]))
    # closed 3-system comparison, same pattern as layers 6/7/8/9/10:
    # the preread's rank-37 regression block against the now-published
    # k=37 result JSON structure fields.
    r37reg = js[\"k38pre\"][\"rank37_regression\"]
    j37st = js[\"k37\"][\"structure\"]
    qreg38 = r37reg[\"new_census\"][\"quad\"]
    checks.append((\"k38preread_rank37_regression_matches_published_k37_result\",
                   r37reg[\"root\"] == j37st[\"rank37_root\"][\"root\"]
                   and sorted(r37reg[\"rows\"]) == sorted(j37st[\"rank37_root\"][\"rows\"])
                   and r37reg[\"full_triples\"][\"counts\"] == j37st[\"triple_census_k37\"]
                   and int(qreg38[\"b_only\"]) == int(j37st[\"new_quad_census\"][\"b_only\"])
                   and int(qreg38[\"zero\"]) == int(j37st[\"new_quad_census\"][\"zero\"])
                   and int(qreg38[\"disjoint\"]) == int(j37st[\"new_quad_census\"][\"disjoint\"])
                   and {k: int(v) for k, v in r37reg[\"full_quints\"][\"counts\"].items()}
                   == {k: int(v) for k, v in j37st[\"quint_census_k37\"].items()}
                   and {int(k): int(v) for k, v in r37reg[\"full_quints\"][\"double_row_histogram\"].items()}
                   == {int(k): int(v) for k, v in j37st[\"quint_b_only_double_rows\"].items()}
                   and {k: int(v) for k, v in r37reg[\"sextet_census\"][\"counts\"].items()}
                   == {k: int(v) for k, v in j37st[\"sextet_census_k37\"].items()}
                   and int(r37reg[\"membership\"]) == int(j37st[\"rank37_root\"][\"membership\"]),
                   None))
    j38 = js[\"k38\"]
    pmatch38 = {c[\"name\"]: c[\"pass\"] for c in j38[\"checks\"]}
    need38 = (\"preread_match.triple_census\", \"preread_match.new_quad_census\",
              \"preread_match.quint_census\", \"preread_match.quint_double_rows\",
              \"preread_match.sextet_census\")
    checks.append((\"k38json_preread_match_checks_all_present_and_pass\",
                   all(pmatch38.get(nm) is True for nm in need38), need38))
    checks.append((\"k38json_rank38_root_exactly_matches_aggregate\",
                   int(j38[\"structure\"][\"rank38_root\"][\"membership\"]) == em38
                   and int(j38[\"structure\"][\"rank38_root\"][\"a_part\"]) == ea38
                   and int(j38[\"structure\"][\"rank38_root\"][\"b_part\"]) == eb38
                   and j38[\"structure\"][\"rank38_root\"][\"root\"] == top[37][\"root\"],
                   (str(em38), str(ea38), str(eb38))))


    # Two closure checks added after the 201-check k=34 publication""",
)

# 12. era-closure comment header now mentions the k=38 era
rep(
    """    # Two closure checks added after the 201-check k=34 publication
    # (plus two more closing the k=35 era, two more closing the k=36
    # era and two more closing the k=37 era, appended below):""",
    """    # Two closure checks added after the 201-check k=34 publication
    # (plus two more closing the k=35 era, two more closing the k=36
    # era, two more closing the k=37 era and two more closing the
    # k=38 era, appended below):""",
)

# 13. k=38 era closure checks after the k=37 closure
rep(
    """    s37 = j37[\"structure\"]
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
""",
    """    s37 = j37[\"structure\"]
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

    # Two more closure checks close the k=38 era the same way: the
    # k=38 preread's embedded regression blocks against their
    # earlier preread publications, and the rank-38 preread's full
    # structural fields against the published k=38 result JSON
    # (which was produced by the single-owner main lane per the
    # concurrency note 112a3247, with the 52-check finalize
    # passing and the record layer, result JSON and JSONL all
    # pinned at their own blob sha1s, plus the independent
    # second-execution agreement record ec62057f4f).
    checks.append((\"k38preread_embedded_rank36_rank37_blocks_match_prior_prereads\",
                   regression_projection(js[\"k38pre\"][\"rank36_regression\"])
                   == regression_projection(js[\"k36pre\"][\"rank36\"])
                   and regression_projection(js[\"k38pre\"][\"rank37_regression\"])
                   == regression_projection(js[\"k37pre\"][\"rank37\"]),
                   None))
    s38 = j38[\"structure\"]
    checks.append((\"k38json_preread_structure_matches_published_result\",
                   s38[\"new_quad_census\"] == {k: nc38[\"quad\"][k] for k in (\"b_only\", \"zero\", \"disjoint\")}
                   and s38[\"new_quint_census\"] == {k: nc38[\"quint\"][k] for k in (\"b_only\", \"zero\", \"disjoint\")}
                   and s38[\"quints_zero_synth_count\"] == nc38[\"quint\"][\"zero\"]
                   and s38[\"triple_census_k38\"] == ft38[\"counts\"]
                   and s38[\"quint_census_k38\"] == fq38[\"counts\"]
                   and s38[\"sextet_census_k38\"] == sx38[\"counts\"]
                   and published_histogram(s38[\"new_triple_b_only_double_row_histogram\"]) == h_tri38
                   and published_histogram(s38[\"new_quad_b_only_double_row_histogram\"]) == h_quad38
                   and {int(k): v for k, v in s38[\"quint_b_only_double_rows\"].items()} == q_twos[38],
                   None))
""",
)

# 14. output default (single-quoted literals: the anchored text
# ends in a double-quote-comma, so triple-quoted blocks would be
# ambiguous)
rep(
    '    ap.add_argument("--out", default="output/cost16-k37-crosscheck-20261119.json",',
    '    ap.add_argument("--out", default="output/cost16-k38-crosscheck-20261119.json",',
)

# 15. report schema / source pins / inputs
rep(
    """        \"schema\": \"n11-cost16-k37-crosscheck-20261119-v1\",
        \"date\": \"2026-11-19\",
        \"source_main_commit\": \"dfe8e6cc877b132c52f766af790cf31735fba409\",
        \"source_note\": (\"k=37 edition: extends the k=36 crosscheck \"
                        \"(script published as commit f688d657) with the \"
                        \"k=37 record and preread layers and the k=37 era \"
                        \"closures (the k=37 main artifacts were verified \"
                        \"against their published blob sha1s before the \"
                        \"pins were recorded; preread independently \"
                        \"verified by the second bit-mask lineage at \"
                        \"958057fb, with the exact-byte restoration \"
                        \"erratum 059db03e)\"),""",
    """        \"schema\": \"n11-cost16-k38-crosscheck-20261119-v1\",
        \"date\": \"2026-11-19\",
        \"source_main_commit\": \"2878e9e02b33059ab0d192f893b9598587ec92cd\",
        \"source_note\": (\"k=38 edition: extends the k=37 crosscheck \"
                        \"(script at commit cb5714d3, result fe8abfad, \"
                        \"patch c430f75e, log 3cc3a8da) with the k=38 \"
                        \"record and preread layers and the k=38 era \"
                        \"closures (the k=38 main artifacts were verified \"
                        \"against their published blob sha1s before the \"
                        \"pins were recorded; the k=38 main publication \"
                        \"is the single-owner main-lane result per the \"
                        \"concurrency note 112a3247, cross-verified by \"
                        \"the independent second-execution agreement \"
                        \"record ec62057f4f)\"),""",
)
rep(
    """            \"k37_jsonl\": {\"file\": JSONL_K37[0], \"git_blob_sha1\": JSONL_K37[1]},
        },""",
    """            \"k37_jsonl\": {\"file\": JSONL_K37[0], \"git_blob_sha1\": JSONL_K37[1]},
            \"k38_jsonl\": {\"file\": JSONL_K38[0], \"git_blob_sha1\": JSONL_K38[1]},
        },""",
)

# ---- run all replacements with exact-count assertions
for i, (old, new, count) in enumerate(REPS, 1):
    got = src.count(old)
    if got != count:
        print(f"ERROR: rep #{i} anchor count {got} != {count}")
        print("anchor head:", repr(old[:80]))
        sys.exit(1)
    src = src.replace(old, new)

out = "base/cc38.py"
with open(out, "w", encoding="utf-8") as f:
    f.write(src)
py_compile.compile(out, doraise=True)
print("wrote", out, len(src), "bytes (base was", orig_len, ")")
# probe: expected k=38 literals present, k=37-only literals gone
probes = [
    '"k38pre": ("cost16-survival-k38-preread-20261119.json",',
    '"k38": ("cost16-survival-k38-20261119.json",',
    'JSONL_K38 = ("cost16-survival-k38-20261119.jsonl", "e8f9a8c9065bad3906a121f9bc816be6d299fb23")',
    'K = 38',
    'V = js["k38"]["values"]',
    'k38preread_rank38_root_prior_hits_exact_ints',
    'k38json_rank38_root_exactly_matches_aggregate',
    'k38preread_rank37_regression_matches_published_k37_result',
    'k38preread_embedded_rank36_rank37_blocks_match_prior_prereads',
    '(38, JSONL_K38, 2))',
    'cost16-k38-crosscheck-20261119.json',
    'n11-cost16-k38-crosscheck-20261119-v1',
]
for p in probes:
    if src.count(p) != 1:
        print("ERROR: probe not found exactly once:", p, src.count(p))
        sys.exit(1)
assert 'K = 37' not in src
assert 'default="output/cost16-k37-crosscheck' not in src
print("all", len(REPS), "replacements applied; probes OK")
