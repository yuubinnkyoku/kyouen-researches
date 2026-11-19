#!/usr/bin/env python3
"""Independent arithmetic and structural cross-check of the published
cost-16 survival-curve extensions k=13 (commit 3a1b9481), k=14 (dc8cb4a4),
k=15 (commit be21591ef), k=16 (b39202a4), k=17 (5b4b4f99), k=18 (2c307c6a),
k=19 (00c4a352), k=20 (52501cad), k=21 (e3efa46a), k=22
(d9d48bd6), k=23 (c0179112), k=24 (b89cd0f5), k=25
(9c41b23a), k=26 (674cdf06 result JSON 3b68d6b4,
per-record JSONL d974042f), k=27 (script+log 16ca07d0,
result JSON 9b804a9c, per-record JSONL d43eb059), k=28 (script+log
a6010eef, result JSON efc500fa, per-record JSONL 42182831), k=29
(script+log f6966f18, result JSON 29fb9f92, per-record JSONL
40f74ef1), k=30 (script+log 69b4e029, result JSON f6a08dc5,
per-record JSONL b3b5ee32), k=31 (script+log cf8d7dcc,
result JSON 5da4cc6c, per-record JSONL a4bef2aa), k=32
(script+log 62c29d080, result JSON 595f0a2795,
per-record JSONL f8bd71fed1, log corrected 71d6f07c3e; pinned
result JSON 6bf47e8745300ae6235180591978daf9d7fe09e5, record JSONL
c4f06b23ad64ae97cb642b244f2d675cd0bf6903), and k=33
(script+log 7ef6dcfd, result JSON b7ec3ebd, per-record JSONL
410008a3; pinned result JSON 3446e9a0aec2d4cc01cbb8f062db0a36d660a65a,
record JSONL 594ff7882931dc8535b892db4006920e66519b1e), and k=34
(script+log f097e6a3, result JSON b64d8fe1, per-record JSONL
76fe66e9; pinned result JSON d485914cf7f6198a2fbb05b09d778ecec510343f,
record JSONL 8cdb7b20c1bccf932e6acc7b6324c4e81a10b47d), and k=35
(script+log 141da801, log erratum bde016c4, result JSON 572b1365,
per-record JSONL b1c73b50; pinned result JSON
80a22ac77cdc0ba0a99643e3f1be13b71565a1b7, record JSONL
89c15ec4fea859393dd673acde1654435f85bd01; rerun end-to-end by the
verification lane with all values identical and 52-check finalize
passing byte-identically twice before publication), and k=36
(script+log 48dc73e6, transport erratum 21bf2cd2 restoring the
exact blobs, result JSON 6fcea02c, per-record JSONL 0e96cde4;
pinned result JSON
b7a78e79bdc82c8097222ef2fd057e6b1a4b9350, record JSONL
7ba84693d302d2bc76851163fd3eb6a6fa7b0caa), verification
lane.

This k=35 edition also repairs the crosscheck script itself: the
203-check k=34 version (published as commit d7001467, 87,336
bytes) was damaged in transport to main at commit 2331d99e, which
truncated the tail mid-statement (the file on main ends at
`if __name__ == "__main` with no sys.exit(main()), blob
49606fc61005f9c8652fbda4985e542f5e7ffe95, py_compile fails).  The
tail is restored byte-exactly (the only missing bytes are the tail
of the final if-statement) and this edition extends the same
script to k=35 with the record and preread layers.
Four independent layers, no experiment-script imports:

  1. value layer: exact BigInt arithmetic over the published numbers
     (grand-total identity, monotonicity, marginal chain, A/B split,
     share percentages, reproduce anchors, cross-publication series
     consistency, and the independent per-d-slice survive anchors
     at k=4/8/10 plus the k=11/12 A/B split anchors);
  2. structure layer: a fresh re-derivation of the structural census
     (shared/disjoint new pairs, b_only/zero/disjoint new triples and
     quads, full triple census, all-C(N,5) 5-subsets zero up to k=25,
     and the k=26..k=35 5-subset censuses, the first ranks that are
     not all-zero, with the new-sensitive prev/new split)
     from the pinned phase-B aggregate with an inline row-multiplicity
     classifier, compared against the published structure fields;
     the k=29..k=35 sextet (6-subset) censuses are re-derived the
     same way and asserted all-zero (the inclusion-exclusion
     truncation justification at those ranks);
  3. record layer (k=26 through k=35): each per-record JSONL is
     fetched at its own pinned git blob sha1, every joint record is
     re-classified with the same independent classifier, the new
     pairs / triples / quads and the recorded new b_only quint set
     are checked for combinatorial completeness,
     and the marginal inclusion-exclusion identities (total, A-type,
     B-type) are re-summed from the record joints alone;
  4. preread layer (k=31 only): the rank-31 structural preread JSON
     is fetched at its own pinned git blob sha1 and its structural
     fields (root rows, prior hit indices, all four new-layer
     censuses, the embedded rank-30 regression censuses, the new
     quint double-row histogram, the b_only four-subset profiles,
     the full triple and quint censuses, and the all-zero sextet
     census) are re-derived machine-side from the pinned aggregate,
     while its three large integers are verified to be Node-double-
     rounded approximations of the exact aggregate values that fail
     the A+B==M identity by a tiny gap, matching the erratum recorded
     in the published k=31 result JSON (which states the exact
     integers, and whose preread_match.* checks must all be present
     and passing);

  5. preread layer (k=32): the rank-32 structural preread JSON
     (pure Python with exact integer serialization, commit 490a3e44)
     is fetched at its own pinned git blob sha1 and its structural
     fields are re-derived machine-side from the pinned aggregate:
     root rows / hex and the row-15 / row-23 prior hit indices, all
     four new-layer censuses (the pair census now carrying the
     shared/disjoint schema), the three new-layer double-row
     histograms, the b_only four-subset profiles, the disjoint-quad
     fields (158 new; union sizes all 8; cumulative 820 asserted
     against a fresh full C(32,4) disjoint count), the full triple
     census with its double-row histogram, the full quint census
     and sextet census (all zero), plus both embedded regression
     blocks (rank-30 and rank-31) whose full quint / sextet numbers
     must match the cached k=30 / k=31 machine censuses; and its
     three large integers are verified to be the exact aggregate
     values satisfying A+B==M (no Node erratum at this rank, in
     contrast with the k=31 preread);

  6. preread layer (k=33): the rank-33 structural preread JSON
     (pure Python with exact integer serialization, commit 67068e07)
     is fetched at its own pinned git blob sha1 and re-derived
     machine-side like layer 5: row 7 has exactly one prior sharer
     (index 20) and row 19 is an 8-sharer hub row, so the (7,19)
     root makes row 7 the first single-share row to double
     (triple layer 8 records, quad layer 11, never the quint
     layer); all four new-layer censuses (pair 9 shared /
     23 disjoint), the three new-layer double-row histograms,
     the b_only four-subset profiles, the disjoint-quad fields
     (146 new, unions all 8, cumulative 966 against a fresh full
     C(32,4) disjoint count), the full triple / quint / sextet
     censuses, both embedded regression blocks (rank-31 and
     rank-32) -- and, new at this rank, the preread's rank-32
     regression block is additionally compared field-by-field
     against the now-published k=32 result JSON structure fields,
     closing a 3-system comparison (independent re-derivation /
     preread regression / published k=32 main) that the k=33
     preread's own verification could only run against the k=32
     preread JSON because the k=32 main result JSON was not yet
     published then.

  7. preread layer (k=34): the rank-34 structural preread JSON
     (pure Python with exact integer serialization, commit 2a14f351)
     is fetched at its own pinned git blob sha1 and re-derived
     machine-side like layers 5/6: row 9 has exactly one prior
     sharer (index 21) and row 19 is now a 9-sharer hub row, so
     the rank-34 root (9,19) is the second consecutive row-19
     root and makes row 9 the first single-share row since
     rank-22 to double (triple layer 8 records, quad layer 11,
     never the quint layer); all four new-layer censuses (pair
     10 shared / 23 disjoint), the three new-layer double-row
     histograms, the b_only four-subset profiles, the
     disjoint-quad fields (146 new, unions all 8, cumulative
     1,112 against a fresh full C(33,4) disjoint count), the full
     triple / quint / sextet censuses, both embedded regression
     blocks (rank-32 and rank-33) -- and, closing the same
     3-system pattern as layer 6, the preread's rank-33 regression
     block is additionally compared field-by-field against the
     now-published k=33 result JSON structure fields; the
     published k=34 result JSON's preread_match.* checks must all
     be present and passing, and its rank34_root must equal the
     aggregate exactly.

  8. preread layer (k=35): the rank-35 structural preread JSON
     (pure Python with exact integer serialization, commit
     90fc51c9, independently verified by a second derivation
     lineage at commit 41c4cf12) is fetched at its own pinned git
     blob sha1 and re-derived machine-side like layers 5/6/7:
     row 18 is now a 16-sharer hub band row and row 21 has zero
     prior sharers (first-ever cover at rank-35), so the (18,21)
     root can never double row 21 in any layer; all four
     new-layer censuses (pair 16 shared / 18 disjoint), the three
     new-layer double-row histograms, the b_only four-subset
     profiles, the disjoint-quad fields (83 new, unions all 8,
     cumulative 1,195 against a fresh full C(34,4) disjoint
     count), the full triple / quint / sextet censuses (all-zero
     1,623,160 sextets), both embedded regression blocks (rank-33
     and rank-34) -- and, closing the same 3-system pattern as
     layers 6/7, the preread's rank-34 regression block is
     additionally compared field-by-field against the
     now-published k=34 result JSON structure fields; the
     published k=35 result JSON's preread_match.* checks must
     all be present and passing, and its rank35_root must equal
     the aggregate exactly.

  9. preread layer (k=36): the rank-36 structural preread JSON
     (pure Python with exact integer serialization, commit
     67985e92, reproduced byte-identically on the Proxmox runner at
     commit fc46f01e) is fetched at its own pinned git blob sha1
     and re-derived machine-side like layers 5/6/7/8: row 22 has
     zero prior sharers among the top-35 (first-ever cover at
     rank-36, so it can never double in any layer) while row 19 is
     now a ten-sharer hub band row (indices 0,2,3,8,9,10,15,29,32,
     33 -- the rank-36 root joins row 18/19 hub territory and ends
     the two-rank fresh-row series of rows 21 and 22); all four
     new-layer censuses (pair 10 shared / 25 disjoint, the largest
     disjoint share of any rank so far), the three new-layer
     double-row histograms, the b_only four-subset profiles, the
     disjoint-quad fields (168 new, unions all 8, cumulative 1,363
     against a fresh full C(35,4) disjoint count), the full triple
     / quint / sextet censuses (all-zero 1,947,792 sextets), both
     embedded regression blocks (rank-34 and rank-35) -- and,
     closing the same 3-system pattern as layers 6/7/8, the
     preread's rank-35 regression block is additionally compared
     field-by-field against the now-published k=35 result JSON
     structure fields; the published k=36 result JSON's
     preread_match.* checks must all be present and passing, and
     its rank36_root must equal the aggregate exactly.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=35 per-record JSONLs; for layer 4 the k=31 preread JSON
and for layer 5 the k=32 preread JSON and for layer 6 the k=33
preread JSON and for layer 7 the k=34 preread JSON and for layer 8
the k=35 preread JSON and for layer 9 the k=36 preread JSON) at
their
pinned git blob sha1s
(via the jsdelivr mirror with a raw.githubusercontent.com fallback;
a mirror serving stale-but-wrong bytes fails the sha1 check and the
next mirror is tried).
No recomputation of pm values: every value check is exact BigInt
arithmetic over the published numbers.

Usage: python3 cost16_survival_k13_k14_crosscheck_20261118.py [--local DIR]
"""
import argparse
import hashlib
import itertools
import json
import math
import os
import sys
import urllib.request

REPO = "yuubinnkyoku/kyouen-researches"
PATH = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
PINS = {
    "k13": ("cost16-survival-k13-20261118.json", "bcf680f7529a119223f362099ed89685b9e37db6"),
    "k14": ("cost16-survival-k14-20261118.json", "1f0b64b1d0587333be30b412e87178dd28afec6a"),
    "k15": ("cost16-survival-k15-20261118.json", "fdf99a93571c8c76d5e97325dd2e92ef4b57ce31"),
    "k16": ("cost16-survival-k16-20261118.json", "c6902c85424680b98e00d959f497562b6c3ef729"),
    "k17": ("cost16-survival-k17-20261118.json", "37e9e848c8b7b9c0faa0ba536eb56cb9464ef576"),
    "k18": ("cost16-survival-k18-20261118.json", "f35df4f230d46c158cbc4655e325dde60878017f"),
    "k19": ("cost16-survival-k19-20261118.json", "7c87ba5b0b69109b8caddf18b323b7819d4a6c26"),
    "k20": ("cost16-survival-k20-20261118.json", "69c7d84edeae57d79291a9603e3a2e130b7d97bf"),
    "k21": ("cost16-survival-k21-20261118.json", "5631e3f307119cdc067e7c6de24a305cd09a1109"),
    "k22": ("cost16-survival-k22-20261118.json", "c1e9598ba79b7dc424a8d975b9b93179e4a13abf"),
    "k23": ("cost16-survival-k23-20261118.json", "fc60c3660c42e71a92ddf2964d11656b9aa263c9"),
    "k24": ("cost16-survival-k24-20261118.json", "a0955297355beef8b2cf2560afebb0001fcf880b"),
    "k25": ("cost16-survival-k25-20261118.json", "c69b63354314537880006bea4590d99fe1921b62"),
    "k26": ("cost16-survival-k26-20261118.json", "1841a281ff604e7f677b8c7772a7312f6f9da5e1"),
    "k27": ("cost16-survival-k27-20261118.json", "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"),
    "k28": ("cost16-survival-k28-20261118.json", "99db3a9a48d044727b3a4d83fb7fc97daa7513d2"),
    "k29": ("cost16-survival-k29-20261118.json", "795665316c300a186979bafd2817b6961de2de60"),
    "k30": ("cost16-survival-k30-20261118.json", "9c24e7a30ad213d3b7675e620ec606b00f73a330"),
    "k31": ("cost16-survival-k31-20261118.json", "0d9f67ee69ad4fb8aa37904ddbf6666745786807"),
    # k=32 (published 2026-11-18, commit 595f0a2795): the published
    # result JSON of the parallel lane, independently rerun by the
    # verification lane and cross-verified all-values-identical
    # (rerun log commit 713cc6dde):
    "k32": ("cost16-survival-k32-20261118.json", "6bf47e8745300ae6235180591978daf9d7fe09e5"),
    # k=33 (published 2026-11-18, commit b7ec3ebd): the published
    # result JSON of the k=33 main computation (record JSONL commit
    # 410008a3), whose 7,542-record layer and preread layer are
    # cross-checked below.
    "k33": ("cost16-survival-k33-20261118.json", "3446e9a0aec2d4cc01cbb8f062db0a36d660a65a"),
    # k=34 (published 2026-11-19, commit b64d8fe1): the published
    # result JSON of the k=34 main computation (record JSONL commit
    # 76fe66e9), whose 8,206-record layer and preread layer are
    # cross-checked below (layer 7).
    "k34": ("cost16-survival-k34-20261118.json", "d485914cf7f6198a2fbb05b09d778ecec510343f"),
    # k=31 rank-31 structural preread (published 2026-11-18, commit
    # 188106bb): its structural fields (rows, hex, prior hit indices,
    # all four new-layer censuses, new quint double-row histogram,
    # b_only four-subset profiles, full triple/quint censuses, all-zero
    # sextet census) are exact small integers, but its three large
    # integers (membership/a_part/b_part) went through Node's
    # double-rounded Number display and are corrected by the k=31
    # result JSON's preread_erratum; the preread artifact itself is
    # pinned and cross-checked machine-side below (preread layer).
    "k31pre": ("cost16-survival-k31-preread-20261118.json",
               "51d08148e0d449dbd4e93df77bbab0b00326491f"),
    # k=32 rank-32 structural preread (published 2026-11-18, commit
    # 490a3e44): pure Python with exact integer serialization (the
    # lesson of the k=31 Node double-rounding erratum), so its three
    # large integers are exact and satisfy A+B==M; its structural
    # fields are cross-checked machine-side below (preread layer 5).
    "k32pre": ("cost16-survival-k32-preread-20261118.json",
               "6d49ab5bea27c967e15b482b33e376510c62b857"),
    # k=33 rank-33 structural preread (published 2026-11-18, commit
    # 67068e07): pure Python with exact integer serialization.  Its
    # rank-32 regression block was published against the k=32 preread
    # JSON (the k=32 main result JSON did not exist yet), so the
    # cross-check below re-derives it machine-side and additionally
    # compares it field-by-field against the now-published k=32
    # result JSON structure fields.
    "k33pre": ("cost16-survival-k33-preread-20261118.json",
               "e4346ddd7e08799b4406dcdba930de714e4f462c"),
    # k=34 rank-34 structural preread (published 2026-11-18,
    # commit 2a14f351): pure Python with exact integer
    # serialization; cross-checked machine-side below (layer 7).
    "k34pre": ("cost16-survival-k34-preread-20261118.json",
               "8dbb1bcbdaed9bee475f3b95932d35a9500e62cb"),
    # k=35 (published 2026-11-19, commit 572b1365): the published
    # result JSON of the k=35 main computation (script+log commit
    # 141da801, log erratum bde016c4, record JSONL commit b1c73b50),
    # whose 8,192-record layer and preread layer (commit 90fc51c9)
    # are cross-checked below (record layer + preread layer 8);
    # rerun end-to-end by the verification lane before publication
    # with all values identical (52-check finalize all pass,
    # byte-identical across two runs).
    "k35": ("cost16-survival-k35-20261118.json",
            "80a22ac77cdc0ba0a99643e3f1be13b71565a1b7"),
    # k=35 rank-35 structural preread (published 2026-11-19,
    # commit 90fc51c9): pure Python with exact integer
    # serialization; cross-checked machine-side below (layer 8),
    # and independently verified by a second derivation lineage
    # (commit 41c4cf12).
    "k35pre": ("cost16-survival-k35-preread-20261118.json",
               "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"),
    # k=36 (published 2026-11-19, commits 48dc73e6 script+log and
    # 21bf2cd2 transport erratum restoring the exact blobs, result
    # JSON commit 6fcea02c, record JSONL commit 0e96cde4): the
    # published result JSON of the k=36 main computation, whose
    # 10,028-record layer and preread layer (commit 67985e92,
    # Proxmox reproduction fc46f01e) are cross-checked below
    # (record layer + preread layer 9).
    "k36": ("cost16-survival-k36-20261118.json",
            "b7a78e79bdc82c8097222ef2fd057e6b1a4b9350"),
    # k=36 rank-36 structural preread (published 2026-11-19,
    # commit 67985e92): pure Python with exact integer
    # serialization; cross-checked machine-side below (layer 9).
    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
}
# k=26 per-record JSONL (published 2026-11-18, commit d974042f): 4,513
# records = pair 25 + triple 300 + quad 2,300 + quint 1,872 (b_only only;
# the 10,778 new zero quints are structural, joint 0) + anchors 8 + cross 8.
JSONL_K26 = ("cost16-survival-k26-20261118.jsonl", "e39f9c2d0cde767bad9b0dbdc74df7439177d6ca")
# k=27 per-record JSONL (published 2026-11-18, commit d43eb059): 3,278
# records = pair 26 + triple 325 + quad 2,600 + quint 309 (new b_only
# only; the 14,641 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=26 disjoint quads x both lineages)
# + cross 8.
JSONL_K27 = ("cost16-survival-k27-20261118.jsonl", "9674ab19e14a41836e065ee4b1d5042ab94eb18b")
# Independent anchors: survive totals recomputed per-d-slice from scratch
# with the ban-survival runner (script cost16_ban_survival_20261118.py,
# point/assemble modes; k=4/8/10 from commit 33abfdb8, k=11/12 extended on
# 2026-11-18, assemble 11-check JSON all_pass).
DIRECT_SURVIVE = {4: 2453842390618094434, 8: 2001925712552127087,
                   10: 1789978398755093008, 11: 1684364881947656288,
                   12: 1592021370388208692}
# Same direct recomputation, A-type / B-type split (exact integers from the
# per-d-slice B sums; independently confirms the published kill_A/kill_B
# split at every direct anchor, including the first two points k=11/12
# beyond the k=10 inclusion-exclusion curve range).
DIRECT_SPLIT = {
    4: (1912189176067079977, 541653214551014457),
    8: (1564239038548375836, 437686674003751251),
    10: (1400734279274103379, 389244119480989629),
    11: (1319225112917587991, 365139769030068297),
    12: (1247882269674605395, 344139100713603297),
}
# k=28 per-record JSONL (published 2026-11-18, commit 42182831): 3,652
# records = pair 27 + triple 351 + quad 2,925 + quint 331 (new b_only
# only; the 17,219 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=27 disjoint quads x both lineages)
# + cross 8.
JSONL_K28 = ("cost16-survival-k28-20261118.jsonl", "6316793b94fe7e95c3d91e283a4229cc7c7f5730")
# k=29 per-record JSONL (published 2026-11-18, commit 40f74ef1): 5,828
# records = pair 28 + triple 378 + quad 3,276 + quint 2,128 (new b_only
# only; the 18,347 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=28 disjoint quads x both lineages)
# + cross 8.
JSONL_K29 = ("cost16-survival-k29-20261118.jsonl", "7b2afe8559de6d94a82a4b0d3f62208572b51910")
# k=30 per-record JSONL (published 2026-11-18, commit b3b5ee32): 5,435
# records = pair 29 + triple 406 + quad 3,654 + quint 1,328 (new b_only
# only; the 22,423 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=29 disjoint quads x both lineages)
# + cross 8.
JSONL_K30 = ("cost16-survival-k30-20261118.jsonl", "98062c66b522e8df6604cd508427f37b2fbe8220")
# k=31 per-record JSONL (published 2026-11-18, commit a4bef2aa): 5,362
# records = pair 30 + triple 435 + quad 4,060 + quint 819 (new b_only
# only; the 26,586 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published (4,13,25,29)/(4,16,25,29) disjoint quads
# of the k=30 record layer x both lineages) + cross 8.
JSONL_K31 = ("cost16-survival-k31-20261118.jsonl", "d308b6d537e8606dadef33c52cdade6cda109320")
# k=32 per-record JSONL (published 2026-11-18, commit f8bd71fed1): 7,019
# records = pair 31 + triple 465 + quad 4,495 + quint 2,010 (new b_only
# only; the 29,455 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published disjoint quads of the k=31 record layer
# x both lineages) + cross 8.  Independently rerun by the verification
# lane with sec-only / record-complete agreement (rerun log commit
# 713cc6dde).
JSONL_K32 = ("cost16-survival-k32-20261118.jsonl", "c4f06b23ad64ae97cb642b244f2d675cd0bf6903")
# k=33 per-record JSONL (published 2026-11-18, commit 410008a3): 7,542
# records = pair 32 + triple 496 + quad 4,960 + quint 2,036 (new b_only
# only; the 33,924 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published disjoint quads (2,4,28,31)/(2,5,28,31)
# of the k=32 record layer x both lineages) + cross 8.  Row 7 is the
# first single-share row of a top-33 root to join the double-row
# families (triple layer 8 records, quad layer 11, never the quint
# layer); the new pair census is 9 shared / 23 disjoint.
JSONL_K33 = ("cost16-survival-k33-20261118.jsonl", "594ff7882931dc8535b892db4006920e66519b1e")
# k=34 per-record JSONL (published 2026-11-19, commit 76fe66e9):
# 8,206 records = pair 33 + triple 528 + quad 5,456 + quint 2,171
# (new b_only only; the 38,749 new zero quints are structural,
# joint 0) + anchors 10 (anchor4 = the two published disjoint
# quads (4,13,25,32)/(4,16,25,32) of the k=33 record layer
# x both lineages) + cross 8.  Row 9 doubles for the first time
# (the rank-34 root (9,19) is only the second member of row 9,
# whose single prior sharer is the rank-22 root at index 21):
# triple layer 8 records, quad layer 11, never the quint layer;
# the new pair census is 10 shared / 23 disjoint.
JSONL_K34 = ("cost16-survival-k34-20261118.jsonl", "8cdb7b20c1bccf932e6acc7b6324c4e81a10b47d")
# k=35 per-record JSONL (published 2026-11-19, commit b1c73b50):
# 8,192 records = pair 34 + triple 561 + quad 5,984 + quint 1,595
# (b_only only; the 44,781 new zero quints are structural, joint
# 0) + anchors 8 (anchor4 = the two published disjoint quads
# (4,13,25,33)/(4,16,25,33) of the k=34 record layer x both
# lineages) + cross 8.  The rank-35 root (18,21) covers row 21
# for the first time ever (zero prior sharers, so it never doubles
# in any layer) while row 18 is a 16-sharer hub band row: the new
# pair census is 16 shared / 18 disjoint, and the 83 new disjoint
# quads all have unions of exactly 8 rows.
# The k=35 record JSONL was also independently rerun by the
# verification lane: same 8,192 record kinds, same joint sums,
# all values identical (record order differs between the two
# runs; the joint totals are order-independent).
JSONL_K35 = ("cost16-survival-k35-20261118.jsonl", "89c15ec4fea859393dd673acde1654435f85bd01")
# k=36 per-record JSONL (published 2026-11-19, commit 0e96cde4):
# 10,028 records = pair 35 + triple 595 + quad 6,545 + quint 2,835
# (b_only only; the 49,525 new zero quints are structural, joint
# 0) + anchors 10 (anchor4 = the two published disjoint quads
# (2,14,28,34)/(2,16,28,34) of the k=35 record layer x both
# lineages) + cross 8.  The rank-36 root (19,22) covers row 22
# for the first time ever (zero prior sharers, so it never doubles
# in any layer) while row 19 is now a ten-sharer hub whose rank-36
# membership is itself a sharer: the new pair census is 10 shared /
# 25 disjoint (the largest disjoint share yet), the 168 new
# disjoint quads all have unions of exactly 8 rows, and row 19
# overtakes row 18 as the dominant new double row in the triple
# (232 vs 136) and quad (1,150 vs 992) layers while the new quint
# layer keeps row 18 narrowly ahead (1,200 vs 1,195).
JSONL_K36 = ("cost16-survival-k36-20261118.jsonl", "7ba84693d302d2bc76851163fd3eb6a6fa7b0caa")
# 5-subset counts are machine-derived with math.comb (no hand-written
# table): C(15..25,5) = 3003..53130, all verified zero-valued; k=26 and
# k=27 are the first censuses that are not all-zero (C(26,5) = 65,780
# with 1,872 b_only / 63,908 zero / 0 disjoint; C(27,5) = 80,730 with
# 2,181 b_only / 78,549 zero / 0 disjoint, of which the rank-27-new
# 5-subsets are 309 b_only / 14,641 zero / 0 disjoint), so their
# quints checks are census-based instead of the quints.all_zero
# anchors used at k<=25; k=28 (C(28,5) = 98,280: 2,512 b_only /
# 95,768 zero / 0 disjoint), k=29 (C(29,5) = 118,755: 4,640
# b_only / 114,115 zero / 0 disjoint, the rank-29-new layer being
# 2,128 b_only / 18,347 zero, with row 16 joining the double-row
# family {15,16,18,19}) and k=30 (C(30,5) = 142,506: 5,968 b_only /
# 136,538 zero / 0 disjoint, the rank-30-new layer being 1,328
# b_only / 22,423 zero) continue the census-based treatment.  At
# k=30 the quint double-row family stays {15,16,18,19}: row 14
# enters the quad double-row family for the first time (9 b_only
# quads) but never the quint one.  k=31 (C(31,5) = 169,911:
# 6,787 b_only / 163,124 zero / 0 disjoint, the rank-31-new layer
# being 819 b_only / 26,586 zero, cumulative double rows
# 15:1003 / 16:239 / 18:4149 / 19:1396) is the hub-band (18,26)
# rank: row 26 receives its first-ever cover there, so it never
# enters any double-row family, and the k=31 record layer is the
# first whose new pair census is evenly split 15 shared / 15
# disjoint (the rank-31 root is the only new-pair member with no
# doubled row).  k=32 (C(32,5) = 201,376: 8,797 b_only / 192,579
# zero / 0 disjoint, the rank-32-new layer being 2,010 b_only /
# 29,455 zero, cumulative double rows 15:1616 / 16:304 / 18:5111 /
# 19:1766) is the mid-hub root (15,23): row 23 has exactly one
# prior sharer (index 11), so row 23 doubles for the first time in
# the triple layer (9 records) and the quad layer (12 records) and
# never in the quint layer; the new pair census drops back to
# 7 shared / 24 disjoint (row 15 has 6 prior sharers), and the
# sextet census C(32,6) = 906,192 stays all zero (the quint I-E
# stays closed, the ninth consecutive rank).  k=33 (C(33,5) =
# 237,336: 10,833 b_only / 226,503 zero / 0 disjoint, the
# rank-33-new layer being 2,036 b_only / 33,924 zero, cumulative
# double rows 15:1930 / 16:370 / 18:6008 / 19:2525) is the
# single-share root (7,19): row 7 sees its first double in the
# triple (8 records) and quad (11 records) layers and never the
# quint layer, the new pair census is 9 shared / 23 disjoint, and
# the sextet census C(33,6) = 1,107,568 stays all zero (the tenth
# consecutive rank).  k=34 (C(34,5) = 278,256: 13,004 b_only /
# 265,252 zero / 0 disjoint, the rank-34-new layer being 2,171
# b_only / 38,749 zero, cumulative double rows 15:2244 / 16:436 /
# 18:6905 / 19:3419) is the second consecutive row-19 root
# (9,19): row 9 sees its first double in the triple (8 records)
# and quad (11 records) layers and never the quint layer, the
# new pair census is 10 shared / 23 disjoint, and the sextet
# census C(34,6) = 1,344,904 stays all zero (the eleventh
# consecutive rank).  k=35 (C(35,5) = 324,632: 14,599 b_only /
# 310,033 zero / 0 disjoint, the rank-35-new layer being 1,595
# b_only / 44,781 zero, cumulative double rows 15:2421 / 16:469 /
# 18:8017 / 19:3692) is the hub-band root (18,21): row 21
# receives its first-ever cover (zero prior sharers, never a
# double row), row 18 adds 275 / 1,155 / 1,112 new b_only
# triples / quads / quints, the new pair census is 16 shared /
# 18 disjoint, there are 83 new disjoint quads (unions all 8,
# cumulative 1,195), and the sextet census C(35,6) = 1,623,160
# stays all zero (the twelfth consecutive rank).  k=36 (C(36,5) =
# 376,992: 17,434 b_only / 359,558 zero / 0 disjoint, the rank-36-new
# layer being 2,835 b_only / 49,525 zero, cumulative double rows
# 15:2785 / 16:545 / 18:9217 / 19:4887) is the hub root (19,22):
# row 22 receives its first-ever cover (zero prior sharers, never
# a double row) and row 19 is now a ten-sharer hub that the rank-36
# root itself belongs to, the new pair census is 10 shared / 25
# disjoint (the largest disjoint share of any rank so far), there
# are 168 new disjoint quads (unions all 8, cumulative 1,363), row
# 19 overtakes row 18 as the dominant new double row in the triple
# and quad layers while the quint layer stays with row 18 (1,200 vs
# 1,195), and the sextet census C(36,6) = 1,947,792 stays all zero
# (the thirteenth consecutive rank).


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


def fetch_lines(name: str, want_sha: str, local_dir: str | None) -> list:
    data = fetch_bytes(name, want_sha, local_dir)
    return [json.loads(l) for l in data.decode("utf-8").splitlines() if l]


def classify(rows, combo):
    """Row-multiplicity classifier, written independently for this
    cross-check (same definition as the k14 publication): 'zero' for a
    3x row or two 2x rows, 'b_only' for exactly one 2x row, 'disjoint'
    otherwise."""
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    if max(c.values()) >= 3:
        return "zero"
    twos = [r for r, v in c.items() if v == 2]
    if len(twos) >= 2:
        return "zero"
    if len(twos) == 1:
        return "b_only"
    return "disjoint"


def classify2(rows, combo):
    """classify plus provenance: returns (class, doubled_row_or_None);
    the doubled row is the b_only signature used for the k=26 quint
    double-row census."""
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=None, help="directory with the published JSONs (offline mode; sha1 still checked)")
    ap.add_argument("--out", default="output/cost16-k36-crosscheck-20261119.json",
                    help="write deterministic machine-readable check results")
    args = ap.parse_args()

    js = {tag: fetch(*PINS[tag], args.local) for tag in PINS}
    for tag in [t for t in js if t != "agg"]:
        if not js[tag].get("all_pass"):
            print(f"FAIL {tag} all_pass is false")
            return 1
    agg = js["agg"]
    top = agg["derived"]["top50_by_membership"]
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]

    V = js["k36"]["values"]  # contains the full k=1..36 series
    kill = {int(k[1:]): int(v) for k, v in V["kill"].items()}
    A = {int(k[1:]): int(v) for k, v in V["A_survive"].items()}
    B = {int(k[1:]): int(v) for k, v in V["B_survive_full_singleton_ban"].items()}
    sh = {int(k[1:]): v for k, v in V["B_survive_share_percent"].items()}
    ksh = {int(k[1:]): v for k, v in V["kill_share_percent"].items()}
    kA = {int(k[1:]): int(v) for k, v in V["kill_A"].items()}
    kB = {int(k[1:]): int(v) for k, v in V["kill_B"].items()}
    K = 36
    checks = []

    # 1. grand-total identity, constant across all k
    T = A[1] + B[1] + kill[1]
    checks.append((f"grand_total_constant_k1_{K}",
                   all(A[k] + B[k] + kill[k] == T for k in kill), T))
    # 2. B(0) anchor == B16
    checks.append(("B0_equals_B16", B[0] == 660663050386546968, None))
    checks.append(("B0_share_k0_consistent", abs(B[0] / T * 100 - sh[0]) < 5e-6, None))
    # 3. monotonicity over the full series
    checks.append((f"kill_monotone_k1_{K}", all(kill[k] < kill[k + 1] for k in range(1, K)), None))
    checks.append(("A_survive_monotone_decreasing", all(A[k] > A[k + 1] for k in range(1, K)), None))
    checks.append(("B_survive_monotone_decreasing", all(B[k] > B[k + 1] for k in range(0, K)), None))
    # 4. marginal chain vs published marginals
    marg = {k: kill[k + 1] - kill[k] for k in range(1, K)}
    km = None
    for c in js["k13"]["checks"]:
        if c["name"] == "survival.marginals" and isinstance(c["detail"], dict):
            km = {int(k.split("_minus_")[0][1:]): int(v) for k, v in c["detail"].items()}
    checks.append((f"marginal_chain_k2_k{K}_matches_published",
                   km is not None and all(marg[k - 1] == km[k] for k in km),
                   f"k2..k{max(km) if km else 0} from k13"))
    chain_ok = True
    m_ok = True
    for n in range(14, K + 1):
        det = None
        for c in js["k%d" % n]["checks"]:
            if c["name"] == "survival.marginal":
                det = c["detail"]
        if det is None:
            chain_ok = False
            continue
        chain_ok = chain_ok and marg[n - 1] == int(det["k%d_minus_k%d" % (n, n - 1)])
        m_ok = m_ok and int(det["m%d" % n]) == mem[n - 1] and marg[n - 1] <= mem[n - 1]
    checks.append((f"marginal_chain_k14_k{K}_matches_published", chain_ok, None))
    checks.append((f"marginal_le_membership_k14_k{K}", m_ok,
                   "mN from pinned aggregate, independent of published detail"))
    # 5. independent direct-recomputation anchors (survive totals + A/B split)
    checks.append(("survive_totals_match_direct_recompute_k4k8k10k11k12",
                   all(A[k] + B[k] == DIRECT_SURVIVE[k] for k in DIRECT_SURVIVE),
                   sorted(DIRECT_SURVIVE)))
    checks.append(("A_B_split_matches_direct_recompute_k4k8k10k11k12",
                   all(A[k] == DIRECT_SPLIT[k][0] and B[k] == DIRECT_SPLIT[k][1]
                       for k in DIRECT_SPLIT),
                   {k: (str(DIRECT_SPLIT[k][0]), str(DIRECT_SPLIT[k][1]))
                    for k in DIRECT_SPLIT}))
    # 6. A/B kill split identity
    checks.append(("kill_A_plus_kill_B_identity",
                   all(kA[k] + kB[k] == kill[k] for k in kA), f"k=1..{max(kA)}"))
    checks.append((f"kill_A_monotone_k1_{K}", all(kA[k] <= kA[k + 1] for k in range(1, K)), None))
    checks.append((f"kill_B_monotone_k1_{K}", all(kB[k] <= kB[k + 1] for k in range(1, K)), None))
    # 7. share percentages consistent
    checks.append((f"B_share_percent_consistent_k0_{K}",
                   all(abs(B[k] / T * 100 - sh[k]) < 5e-6 for k in sh), None))
    checks.append((f"kill_share_percent_consistent_k1_{K}",
                   all(abs(kill[k] / T * 100 - ksh[k]) < 5e-6 for k in ksh), None))
    # 8. mixed full-singleton-ban endpoint == B_survive(14)
    mixed = None
    for c in js["k14"]["checks"]:
        if c["name"] == "mixed.k14_value":
            mixed = int(c["detail"]["full_singleton_ban_survive_k14"])
    checks.append(("mixed_k14_endpoint_equals_B_survive_14", mixed == B[14], (mixed, B[14])))
    # 9. published reproduce anchors
    rep = None
    for c in js["k13"]["checks"]:
        if c["name"] == "survival.reproduce_k1_k10":
            rep = c["detail"]
    checks.append(("k13_json_reproduces_direct_k10",
                   rep is not None and rep["k10_mine"] == rep["k10_pub"] == str(kill[10]), None))
    rep14 = None
    for c in js["k14"]["checks"]:
        if c["name"] == "reproduce_k1_13":
            rep14 = c["detail"]
    checks.append(("k14_json_reproduces_k13",
                   rep14 is not None and rep14["k13_mine"] == rep14["k13_pub"] == str(kill[13]), None))
    checks.append(("k15_json_reproduces_k1_14",
                   any(c["name"] == "reproduce_k1_14" and c["pass"] for c in js["k15"]["checks"]), None))
    rep_ok = True
    for n in range(16, K + 1):
        rep_ok = rep_ok and any(
            c["name"] == "reproduce_k1_%d" % (n - 1) and c["pass"]
            for c in js["k%d" % n]["checks"])
    checks.append((f"k16_k{K}_reproduce_anchors_all_pass", rep_ok, None))
    # 10. quints all-zero anchors as published (k=15..k=25 only: at
    # k>=26 non-zero quint censuses appear and are handled below)
    q_ok = True
    for n in range(15, 26):
        q_ok = q_ok and any(
            c["name"] == "quints.all_zero_%d" % math.comb(n, 5) and c["pass"]
            for c in js["k%d" % n]["checks"])
    checks.append(("quints_all_zero_published_k15_k25", q_ok,
                   "checks quints.all_zero_3003..53130 at k=15..25 (machine.comb counts)"))

    # ---- structure layer: independent re-derivation from the aggregate
    s_ok = True
    s_bad = []
    for n in range(16, K + 1):
        tag = "k%d" % n
        st = js[tag]["structure"]
        rk = st["rank%d_root" % n]
        idx = n - 1
        if sorted(rk["rows"]) != sorted(rows[idx]) or rk["root"] != top[idx]["root"]:
            s_ok = False
            s_bad.append((tag, "rank rows"))
        if int(rk["membership"]) != mem[idx] or int(rk["a_part"]) != memA[top[idx]["root"]] \
                or int(rk["b_part"]) != memB[top[idx]["root"]]:
            s_ok = False
            s_bad.append((tag, "membership split"))
    checks.append((f"rank_root_fields_match_aggregate_k16_k{K}", s_ok, s_bad[:4]))
    pc_ok = True
    pc_bad = []
    for n in range(16, K + 1):
        det = None
        for c in js["k%d" % n]["checks"]:
            if c["name"] == "pairs.new_census":
                det = c["detail"]
        shared = sum(1 for i in range(n - 1) if set(rows[i]) & set(rows[n - 1]))
        if det is None or det["shared"] != shared or det["disjoint"] != (n - 1) - shared:
            pc_ok = False
            pc_bad.append((n, shared, det))
    checks.append((f"new_pair_census_rederived_k16_k{K}", pc_ok, pc_bad[:4]))
    tc_ok = True
    tc_bad = []
    for n in range(16, K + 1):
        cen = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n), 3):
            cen[classify(rows, c)] += 1
        pub = js["k%d" % n]["structure"]["triple_census_k%d" % n]
        if cen != pub:
            tc_ok = False
            tc_bad.append((n, cen, pub))
    checks.append((f"full_triple_census_rederived_k16_k{K}", tc_ok, tc_bad[:4]))
    qc_ok = True
    qc_bad = []
    for n in range(16, K + 1):
        cen = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n - 1), 3):
            cen[classify(rows, (n - 1,) + c)] += 1
        pub = js["k%d" % n]["structure"]["new_quad_census"]
        if "disjoint" in pub:
            # k=26 and later: full census comparison (k=26 is the first
            # rank with a nonzero disjoint new-quad count: 233 records)
            ok = cen == pub
        else:
            # k<=25 publications list b_only/zero only; disjoint must be 0
            ok = cen["disjoint"] == 0 and pub["b_only"] == cen["b_only"] and pub["zero"] == cen["zero"]
        if not ok:
            qc_ok = False
            qc_bad.append((n, cen, pub))
    checks.append((f"new_quad_census_rederived_k16_k{K}", qc_ok, qc_bad[:4]))
    n5_ok = True
    n5_bad = []
    for n in range(15, 26):
        cnt = 0
        for c in itertools.combinations(range(n), 5):
            cnt += 1
            if classify(rows, c) != "zero":
                n5_ok = False
                n5_bad.append((n, c))
        if cnt != math.comb(n, 5):
            n5_ok = False
            n5_bad.append((n, "count", cnt))
    checks.append(("quints_rederived_all_zero_k15_k25", n5_ok,
                   "machine.comb counts 3003..53130 at k=15..25, bad %s" % (n5_bad[:4],)))
    # k=26 and k=27 quint censuses: the first non-all-zero 5-subset
    # censuses. Machine re-derivation over all C(n,5) 5-subsets with
    # the independent classifier, including the b_only double-row
    # histogram and the new-sensitive split (b_only 5-subsets that
    # contain the new rank n-1 are the recorded new-b_only layer).
    q_new_b_only = {}
    q_full = {}
    q_twos = {}
    for n in (26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36):
        qn = {"b_only": 0, "zero": 0, "disjoint": 0}
        qn_twos = {}
        for c in itertools.combinations(range(n), 5):
            cl, two = classify2(rows, c)
            qn[cl] += 1
            if cl == "b_only":
                qn_twos[two] = qn_twos.get(two, 0) + 1
                if (n - 1) in c:
                    q_new_b_only.setdefault(n, set()).add(c)
        q_full[n] = qn
        q_twos[n] = qn_twos
        q_new_b_only.setdefault(n, set())
        strn = js["k%d" % n]["structure"]
        checks.append((f"quint_census_k{n}_machine_rederived_C{n}5_{math.comb(n, 5)}",
                       qn["b_only"] + qn["zero"] + qn["disjoint"] == math.comb(n, 5)
                       and qn == strn["quint_census_k%d" % n]
                       and int(strn["quints_zero_synth_count"]) == math.comb(n - 1, 4) - len(q_new_b_only[n]),
                       (qn, qn_twos)))
        checks.append((f"quint_b_only_double_rows_k{n}_machine_rederived",
                       qn_twos == {int(k): v for k, v in strn["quint_b_only_double_rows"].items()},
                       qn_twos))
    # consecutive-era prev-layer identities: full(k) minus the
    # rank-k-new 5-subsets (C(k-1,4) counted as new b_only + new
    # zero) must equal the full census of the previous rank, for
    # the whole quint era k=27..35.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29), (31, 30), (32, 31), (33, 32),
                 (34, 33), (35, 34), (36, 35)):
        checks.append((f"quint_census_k{n}_prev_layer_equals_published_k{m}_census",
                       q_full[n]["b_only"] - len(q_new_b_only[n]) == q_full[m]["b_only"]
                       and q_full[n]["zero"] - (math.comb(n - 1, 4) - len(q_new_b_only[n])) == q_full[m]["zero"]
                       and q_full[n]["disjoint"] == q_full[m]["disjoint"] == 0,
                       (len(q_new_b_only[n]), q_full[n], q_full[m])))
    # k=26 is all-new: every b_only 5-subset of the C(26,5) census
    # contains the rank-26 root (published as such), so the full
    # census b_only set equals the new layer (len 1,872).
    checks.append(("k26_all_census_b_only_contain_rank26",
                   len(q_new_b_only[26]) == q_full[26]["b_only"], len(q_new_b_only[26])))
    # ---- sextet (6-subset) censuses at k=29, k=30, k=31, k=32,
    # k=33, k=34 and k=35:
    # machine re-derivation over all C(n,6) 6-subsets with the same
    # independent classifier.  These are the published I-E truncation
    # justifications (the seventh order is never needed), previously
    # only self-verified inside each experiment finalize; here they
    # are re-derived independently and asserted all-zero.  Row 26
    # joins the covered rows at k=31 (first-ever cover by the
    # rank-31 root (18,26)) yet all 736,281 sextets stay zero, and
    # row 23 doubles for the first time at k=32 (the rank-32 root
    # (15,23) is only its second member) with all 906,192 sextets
    # still zero, and row 7 doubles for the first time at k=33 (the
    # single-share rank-33 root (7,19); triple and quad layers only)
    # with all 1,107,568 sextets still zero, and row 9 doubles for
    # the first time at k=34 (the single-share rank-34 root (9,19),
    # again triple and quad layers only) with all 1,344,904
    # sextets still zero, and row 21 is covered for the first
    # time at k=35 (the hub-band rank-35 root (18,21): a
    # first-ever covered row can never double in any layer)
    # with all 1,623,160 sextets still zero, and row 22 is covered
    # for the first time at k=36 (the hub rank-36 root (19,22):
    # again a first-ever covered row that can never double, while
    # row 19 becomes a ten-sharer hub that includes rank-36 itself)
    # with all 1,947,792 sextets still zero.
    sx_census = {}
    for n in (29, 30, 31, 32, 33, 34, 35, 36):
        sx = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n), 6):
            sx[classify(rows, c)] += 1
        sx_census[n] = sx
        pub = js["k%d" % n]["structure"]["sextet_census_k%d" % n]
        checks.append((f"sextet_census_k{n}_machine_rederived_C{n}6_{math.comb(n, 6)}",
                       sum(sx.values()) == math.comb(n, 6) and sx == pub
                       and pub["b_only"] == 0 and pub["disjoint"] == 0
                       and pub["zero"] == math.comb(n, 6), sx))
    # ---- cross-publication series consistency (no history rewrite)
    xs_ok = True
    xs_bad = []
    for n in range(13, K + 1):
        v = js["k%d" % n]["values"]
        for key, ref in (("kill", kill), ("kill_A", kA), ("kill_B", kB)):
            for kk, vv in v[key].items():
                k = int(kk[1:])
                if k <= K and int(vv) != ref[k]:
                    xs_ok = False
                    xs_bad.append((n, key, kk))
    checks.append((f"kill_series_consistent_across_publications_k13_k{K}", xs_ok, xs_bad[:4]))

    # ---- record layer (k=26 through k=35): each per-record JSONL is fetched
    # at its own pinned blob sha1; every joint record is re-classified
    # with the same independent classifier, the new pairs / triples /
    # quads and the recorded new b_only quint set are checked for
    # combinatorial completeness, and the marginal inclusion-exclusion
    # identities are re-summed from the record joints alone (no
    # experiment-script imports, no pm calls). anchor4 agreement is
    # re-derived from the two lineage records per combo; at k=26 the
    # single anchor4 combo is the published (25,3,4,16), at k=27 the
    # two combos are the published (25,3,4,16)/(25,3,4,17) disjoint
    # quads of the k=26 record layer, and k=28/k=29/k=30/k=31 likewise
    # anchor on the two published disjoint quads of the previous
    # rank's record layer (at k=31: (4,13,25,29)/(4,16,25,29); at k=33: (2,4,28,31)/(2,5,28,31), the k=32 record layer disjoint quads; at k=34: (4,13,25,32)/(4,16,25,32), the k=33 record layer disjoint
    # quads; at k=35: (4,13,25,33)/(4,16,25,33), the k=34 record
    # layer disjoint quads; at k=36: (2,14,28,34)/(2,16,28,34),
    # the k=35 record layer disjoint quads).
    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),
                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),
                         (30, JSONL_K30, 2), (31, JSONL_K31, 2),
                         (32, JSONL_K32, 2), (33, JSONL_K33, 2),
                         (34, JSONL_K34, 2), (35, JSONL_K35, 2),
                         (36, JSONL_K36, 2)):
        jl = fetch_lines(*pin, args.local)
        new = n - 1
        kinds = {}
        rec = {"pair": [], "triple": [], "quad": [], "quint": []}
        rl_ok = True
        for r in jl:
            k = r["kind"]
            kinds[k] = kinds.get(k, 0) + 1
            if k in rec:
                rec[k].append(r)
            elif k.startswith("anchor") or k.startswith("cross"):
                # anchor4 records carry no match field (the two lineages
                # are the two records; agreement re-derived separately)
                rl_ok = rl_ok and r.get("match", True) is True
            else:
                rl_ok = False
        kinds_exp = {"pair": new, "triple": math.comb(new, 2), "quad": math.comb(new, 3),
                     "quint": len(q_new_b_only[n]), "anchor2": 4, "anchor3": 2,
                     "anchor4": 2 * a4c, "cross3": 2, "cross4": 2,
                     "cross5": 2, "crossq4": 2}
        checks.append((f"jsonl_record_kind_counts_k{n}_{len(jl)}",
                       kinds == kinds_exp and len(jl) == sum(kinds_exp.values()), kinds))
        checks.append((f"jsonl_anchor_cross_records_all_match_k{n}", rl_ok, None))
        # anchor4 records carry no "match" field: the two lineages are
        # the two records themselves, so the agreement is re-derived
        # here (both lineages present per combo, identical A/B joints,
        # union rows re-derived from the aggregate where present).
        a4 = {}
        a4_ok = True
        for r in jl:
            if r["kind"] == "anchor4":
                key = tuple(sorted(r["combo"]))
                a4.setdefault(key, {})[r["lineage"]] = (int(r["joint_A"]), int(r["joint_B"]))
            elif r["kind"].startswith("anchor") or r["kind"].startswith("cross"):
                if r.get("union") is not None:
                    u = set()
                    for i in r["combo"]:
                        u |= set(rows[i])
                    if sorted(r["union"]) != sorted(u):
                        a4_ok = False
        a4_ok = a4_ok and len(a4) == a4c and all(
            sorted(v) == ["lazypm", "mypm"] for v in a4.values()) and all(
            len({v["lazypm"], v["mypm"]}) == 1 for v in a4.values())
        checks.append((f"jsonl_anchor4_two_lineage_agreement_{a4c}x8_union_rederived_k{n}",
                       a4_ok, None))
        p_ok = True
        for r in rec["pair"]:
            i, j = r["idx_i"], r["idx_j"]
            if j != new or not (0 <= i <= new - 1):
                p_ok = False
            elif r["shared_row"] != bool(set(rows[i]) & set(rows[j])):
                p_ok = False
            elif int(r["joint"]) != int(r["joint_A"]) + int(r["joint_B"]):
                p_ok = False
        checks.append((f"jsonl_pairs_are_exactly_the_{new}_new_pairs",
                       p_ok and sorted(r["idx_i"] for r in rec["pair"]) == list(range(new)),
                       None))
        # records store combos as (new, sorted others); classify is
        # order-independent so we normalize with sorted() everywhere
        cl_ok = True
        for kind in ("triple", "quad", "quint"):
            for r in rec[kind]:
                combo = tuple(sorted(r["combo"]))
                if new not in combo or r["class"] != classify(rows, combo) \
                        or (r["class"] == "zero" and int(r.get("joint", 0)) != 0):
                    cl_ok = False
        checks.append((f"jsonl_joint_records_reclassified_independently_k{n}", cl_ok, None))
        t_ex = {tuple(sorted((new,) + c)) for c in itertools.combinations(range(new), 2)}
        q_ex = {tuple(sorted((new,) + c)) for c in itertools.combinations(range(new), 3)}
        checks.append((f"jsonl_new_triples_quads_combinatorially_complete_k{n}",
                       {tuple(sorted(r["combo"])) for r in rec["triple"]} == t_ex
                       and {tuple(sorted(r["combo"])) for r in rec["quad"]} == q_ex,
                       (len(t_ex), len(q_ex))))
        checks.append((f"jsonl_quints_are_exactly_the_new_b_only_set_k{n}",
                       {tuple(sorted(r["combo"])) for r in rec["quint"]} == q_new_b_only[n],
                       len(q_new_b_only[n])))
        qc2 = {"b_only": 0, "zero": 0, "disjoint": 0}
        for r in rec["quad"]:
            qc2[r["class"]] += 1
        checks.append((f"jsonl_quad_record_census_matches_structure_k{n}",
                       qc2 == js["k%d" % n]["structure"]["new_quad_census"], qc2))
        # marginal inclusion-exclusion identities from the record joints
        s2 = sum(int(r["joint"]) for r in rec["pair"])
        s3 = sum(int(r["joint"]) for r in rec["triple"])
        s4 = sum(int(r["joint"]) for r in rec["quad"])
        s5 = sum(int(r["joint"]) for r in rec["quint"])
        rootn = top[new]["root"]
        mn, mna, mnb = int(mem[new]), int(memA[rootn]), int(memB[rootn])
        checks.append((f"jsonl_ie_marginal_identity_k{n}_total",
                       mn - s2 + s3 - s4 + s5 == kill[n] - kill[n - 1],
                       (mn - s2 + s3 - s4 + s5, kill[n] - kill[n - 1])))
        s2a = sum(int(r["joint_A"]) for r in rec["pair"])
        s2b = sum(int(r["joint_B"]) for r in rec["pair"])
        s3a = sum(int(r["joint_A"]) for r in rec["triple"])
        s3b = sum(int(r["joint_B"]) for r in rec["triple"])
        s4a = s4b = 0
        for r in rec["quad"]:
            if r["class"] == "disjoint":
                s4a += int(r["joint_A"])
                s4b += int(r["joint_B"])
            elif r["class"] == "b_only":
                s4b += int(r["joint"])
        s5b = sum(int(r["joint_B"]) for r in rec["quint"])
        checks.append((f"jsonl_ie_marginal_identity_k{n}_A_type",
                       mna - s2a + s3a - s4a == kA[n] - kA[n - 1],
                       (mna - s2a + s3a - s4a, kA[n] - kA[n - 1])))
        checks.append((f"jsonl_ie_marginal_identity_k{n}_B_type",
                       mnb - s2b + s3b - s4b + s5b == kB[n] - kB[n - 1],
                       (mnb - s2b + s3b - s4b + s5b, kB[n] - kB[n - 1])))

    # ---- preread layer (k=31): the rank-31 structural preread JSON
    # (commit 188106bb) is re-derived machine-side from the pinned
    # aggregate: root rows and hex, prior hit indices (row 18 hub
    # band: 15 priors; row 26: first-ever cover, 0 priors), all four
    # new-layer censuses, the new quint double-row histogram, the
    # b_only four-subset profiles (drop-one classify over each new
    # b_only quint), the full triple / quint / sextet censuses, and
    # the embedded rank-30 regression censuses.  The three large
    # integers are verified to be Node double-rounded approximations
    # of the exact aggregate values: within 8 of the exact integers
    # (half-ULP scale at 2^56..2^57), never equal to them, and
    # failing the A+B==M identity that the exact integers satisfy --
    # the preread_erratum of the published k=31 result JSON states
    # the exact integers, and its preread_match.* checks must all be
    # present and passing.
    def census_ok(pub, mach, total):
        return (pub["b_only"] == mach["b_only"] and pub["zero"] == mach["zero"]
                and pub["disjoint"] == mach["disjoint"]
                and pub["total"] == total and pub["expected_total"] == total
                and sum(mach.values()) == total)

    pre31 = js["k31pre"]["rank31"]
    hits18 = sorted(i for i in range(30) if 18 in rows[i])
    hits26 = sorted(i for i in range(30) if 26 in rows[i])
    checks.append(("k31preread_rank31_root_and_prior_hits_machine_rederived",
                   pre31["root"] == top[30]["root"]
                   and sorted(pre31["rows"]) == sorted(rows[30])
                   and pre31["prior_hits"] == {"18": len(hits18), "26": len(hits26)}
                   and {k: sorted(v) for k, v in pre31["prior_hit_indices"].items()}
                   == {"18": hits18, "26": hits26}, (len(hits18), len(hits26))))
    nc = pre31["new_census"]
    m_pair = {"b_only": 0, "zero": 0, "disjoint": 0}
    for i in range(30):
        m_pair[classify(rows, (30, i))] += 1
    m_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(30), 2):
        m_tri[classify(rows, (30,) + c)] += 1
    m_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(30), 3):
        m_quad[classify(rows, (30,) + c)] += 1
    m_quint = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(30), 4):
        m_quint[classify(rows, (30,) + c)] += 1
    checks.append(("k31preread_new_layer_censuses_machine_rederived",
                   census_ok(nc["pair"], m_pair, 30)
                   and census_ok(nc["triple"], m_tri, math.comb(30, 2))
                   and census_ok(nc["quad"], m_quad, math.comb(30, 3))
                   and census_ok(nc["quint"], m_quint, math.comb(30, 4))
                   and m_quint["b_only"] == len(q_new_b_only[31]),
                   (m_pair, m_tri, m_quad, m_quint)))
    rg30 = js["k31pre"]["rank30_regression"]["new_census"]
    r_pair = {"b_only": 0, "zero": 0, "disjoint": 0}
    for i in range(29):
        r_pair[classify(rows, (29, i))] += 1
    r_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(29), 2):
        r_tri[classify(rows, (29,) + c)] += 1
    r_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(29), 3):
        r_quad[classify(rows, (29,) + c)] += 1
    r_quint = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(29), 4):
        r_quint[classify(rows, (29,) + c)] += 1
    checks.append(("k31preread_rank30_regression_censuses_machine_rederived",
                   census_ok(rg30["pair"], r_pair, 29)
                   and census_ok(rg30["triple"], r_tri, math.comb(29, 2))
                   and census_ok(rg30["quad"], r_quad, math.comb(29, 3))
                   and census_ok(rg30["quint"], r_quint, math.comb(29, 4)),
                   (r_pair, r_tri, r_quad, r_quint)))
    ft = pre31["full_triples"]
    ftm = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft_twos = {}
    for c in itertools.combinations(range(31), 3):
        cl, two = classify2(rows, c)
        ftm[cl] += 1
        if cl == "b_only":
            ft_twos[two] = ft_twos.get(two, 0) + 1
    fq = pre31["full_quints"]
    checks.append(("k31preread_full_triples_and_quints_machine_rederived",
                   ft["counts"] == ftm and ft["total"] == math.comb(31, 3)
                   and ft["compared"] == math.comb(31, 3) and ft["mismatches"] == 0
                   and {int(k): v for k, v in ft["double_row_histogram"].items()} == ft_twos
                   and fq["counts"] == q_full[31] and fq["total"] == math.comb(31, 5)
                   and fq["compared"] == math.comb(31, 5) and fq["mismatches"] == 0
                   and {int(k): v for k, v in fq["double_row_histogram"].items()} == q_twos[31],
                   (ftm, ft_twos)))
    nq_twos = {}
    prof = {}
    for c in q_new_b_only[31]:
        cl, two = classify2(rows, c)
        nq_twos[two] = nq_twos.get(two, 0) + 1
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof[key] = prof.get(key, 0) + 1
    checks.append(("k31preread_new_quint_double_rows_and_profiles_machine_rederived",
                   nq_twos == {int(k): v for k, v in pre31["new_quint_double_row_histogram"].items()}
                   and prof == {str(k): v for k, v in pre31["b_only_quint_four_subset_profiles"].items()},
                   (nq_twos, prof)))
    sx31 = pre31["sextet_census"]
    checks.append(("k31preread_sextet_census_machine_rederived",
                   sx31["counts"] == sx_census[31] and sx31["total"] == math.comb(31, 6)
                   and sx31["mismatches"] == 0, sx_census[31]))
    # the preread's three large integers: Node double-rounded
    pm_, pa_, pb_ = int(pre31["membership"]), int(pre31["a_part"]), int(pre31["b_part"])
    em, ea, eb = int(mem[30]), int(memA[top[30]["root"]]), int(memB[top[30]["root"]])
    deltas = (pm_ - em, pa_ - ea, pb_ - eb)
    checks.append(("k31preread_large_ints_are_double_rounded_approximations",
                   all(0 < abs(d) <= 8 for d in deltas) and pa_ + pb_ != pm_
                   and ea + eb == em and abs((pa_ + pb_) - pm_) <= 16,
                   (deltas, (pa_ + pb_) - pm_)))
    j31 = js["k31"]
    note = j31["structure"]["preread_erratum"]["note"]
    checks.append(("k31json_rank31_root_and_erratum_state_exact_aggregate_ints",
                   j31["structure"]["rank31_root"]["membership"] == str(em)
                   and j31["structure"]["rank31_root"]["a_part"] == str(ea)
                   and j31["structure"]["rank31_root"]["b_part"] == str(eb)
                   and str(em) in note and str(ea) in note and str(eb) in note,
                   (str(em), str(ea), str(eb))))
    pmatch = {c["name"]: c["pass"] for c in j31["checks"]}
    need = ("preread_match.triple_census", "preread_match.new_quad_census",
            "preread_match.quint_census", "preread_match.quint_double_rows",
            "preread_match.sextet_census")
    checks.append(("k31json_preread_match_checks_all_present_and_pass",
                   all(pmatch.get(nm) is True for nm in need), need))

    # ---- preread layer 5 (k=32): the rank-32 structural preread JSON
    # (commit 490a3e44, pure Python with exact integer serialization)
    # is re-derived machine-side from the pinned aggregate: root rows /
    # hex and the row-15 / row-23 prior hit indices (row 15 has 6 prior
    # sharers, row 23 exactly one: index 11), all four new-layer
    # censuses (the pair census carries the shared/disjoint schema here
    # -- shared pairs classify as b_only in the row-multiplicity
    # classifier, so the machine counts map shared->b_only-count), the
    # three new-layer b_only double-row histograms, the b_only quint
    # four-subset profiles, the disjoint-quad fields (158 new disjoint
    # quads, every union exactly 8 rows; cumulative 820 asserted
    # against a fresh full C(31,4)+new split, no hardcoded constants),
    # the full triple census with double-row histogram, the full quint
    # and sextet censuses (all-zero sextets, 906,192), both embedded
    # regression blocks (rank-30 and rank-31) re-derived with the same
    # combined logic, and the three large integers verified to be the
    # exact aggregate values satisfying A+B==M (the k=31 Node
    # double-rounding erratum deliberately does not recur: the preread
    # is pinned pure-Python-serialized and the integers must be exact
    # now).
    pre32 = js["k32pre"]["rank32"]
    hits15 = sorted(i for i in range(31) if 15 in rows[i])
    hits23 = sorted(i for i in range(31) if 23 in rows[i])
    em32 = int(mem[31])
    ea32 = int(memA[top[31]["root"]])
    eb32 = int(memB[top[31]["root"]])
    checks.append(("k32preread_rank32_root_prior_hits_exact_ints",
                   pre32["root"] == top[31]["root"]
                   and sorted(pre32["rows"]) == sorted(rows[31])
                   and pre32["prior_hits"] == {"15": len(hits15), "23": len(hits23)}
                   and {k: sorted(v) for k, v in pre32["prior_hit_indices"].items()}
                   == {"15": hits15, "23": hits23}
                   and int(pre32["membership"]) == em32
                   and int(pre32["a_part"]) == ea32
                   and int(pre32["b_part"]) == eb32
                   and ea32 + eb32 == em32,
                   (len(hits15), len(hits23), (ea32, eb32, em32))))
    nc32 = pre32["new_census"]
    shared32 = sum(1 for i in range(31) if set(rows[i]) & set(rows[31]))
    m32_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(31), 2):
        m32_tri[classify(rows, (31,) + c)] += 1
    m32_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(31), 3):
        m32_quad[classify(rows, (31,) + c)] += 1
    nb5_32 = len(q_new_b_only[32])
    checks.append(("k32preread_new_layer_censuses_machine_rederived",
                   nc32["pair"] == {"shared": shared32, "disjoint": 31 - shared32,
                                    "total": 31, "expected_total": 31}
                   and nc32["triple"]["b_only"] == m32_tri["b_only"]
                   and nc32["triple"]["zero"] == m32_tri["zero"]
                   and nc32["triple"]["disjoint"] == m32_tri["disjoint"]
                   and nc32["triple"]["total"] == nc32["triple"]["expected_total"]
                   == math.comb(31, 2)
                   and nc32["quad"]["b_only"] == m32_quad["b_only"]
                   and nc32["quad"]["zero"] == m32_quad["zero"]
                   and nc32["quad"]["disjoint"] == m32_quad["disjoint"]
                   and nc32["quad"]["total"] == nc32["quad"]["expected_total"]
                   == math.comb(31, 3)
                   and nc32["quint"]["b_only"] == nb5_32
                   and nc32["quint"]["zero"] == math.comb(31, 4) - nb5_32
                   and nc32["quint"]["disjoint"] == 0
                   and nc32["quint"]["total"] == nc32["quint"]["expected_total"]
                   == math.comb(31, 4),
                   (nc32["pair"], m32_tri, m32_quad, nb5_32)))
    h_tri32 = {}
    h_quad32 = {}
    h_qt32 = {}
    for c in itertools.combinations(range(31), 2):
        cl, two = classify2(rows, (31,) + c)
        if cl == "b_only":
            h_tri32[two] = h_tri32.get(two, 0) + 1
    for c in itertools.combinations(range(31), 3):
        cl, two = classify2(rows, (31,) + c)
        if cl == "b_only":
            h_quad32[two] = h_quad32.get(two, 0) + 1
    for c in q_new_b_only[32]:
        cl, two = classify2(rows, c)
        h_qt32[two] = h_qt32.get(two, 0) + 1
    checks.append(("k32preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri32 == {int(k): v for k, v in pre32["new_triple_double_row_histogram"].items()}
                   and h_quad32 == {int(k): v for k, v in pre32["new_quad_double_row_histogram"].items()}
                   and h_qt32 == {int(k): v for k, v in pre32["new_quint_double_row_histogram"].items()},
                   (h_tri32, h_quad32, h_qt32)))
    prof32 = {}
    for c in q_new_b_only[32]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof32[key] = prof32.get(key, 0) + 1
    dq_sizes = {}
    dq_cnt = 0
    for c in itertools.combinations(range(31), 3):
        if classify(rows, (31,) + c) == "disjoint":
            dq_cnt += 1
            u = set()
            for i in (31,) + c:
                u |= set(rows[i])
            dq_sizes[len(u)] = dq_sizes.get(len(u), 0) + 1
    dj31 = 0
    for c in itertools.combinations(range(31), 4):
        if classify(rows, c) == "disjoint":
            dj31 += 1
    checks.append(("k32preread_quint_profiles_and_disjoint_quad_fields",
                   prof32 == {str(k): v for k, v in pre32["b_only_quint_four_subset_profiles"].items()}
                   and pre32["disjoint_quad_count"] == dq_cnt
                   and dq_cnt == m32_quad["disjoint"]
                   and {int(k): v for k, v in pre32["disjoint_quad_union_sizes"].items()} == dq_sizes
                   and pre32["cumulative_disjoint_quads"] == dj31 + dq_cnt,
                   (prof32, dq_cnt, dq_sizes, dj31)))
    ft32 = pre32["full_triples"]
    ft32m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft32_twos = {}
    for c in itertools.combinations(range(32), 3):
        cl, two = classify2(rows, c)
        ft32m[cl] += 1
        if cl == "b_only":
            ft32_twos[two] = ft32_twos.get(two, 0) + 1
    fq32 = pre32["full_quints"]
    checks.append(("k32preread_full_triples_and_quints_machine_rederived",
                   ft32["counts"] == ft32m and ft32["total"] == math.comb(32, 3)
                   and ft32.get("compared") in (None, math.comb(32, 3))
                   and ft32.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft32["double_row_histogram"].items()} == ft32_twos
                   and fq32["counts"] == q_full[32] and fq32["total"] == math.comb(32, 5)
                   and fq32.get("compared") in (None, math.comb(32, 5))
                   and fq32.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq32["double_row_histogram"].items()} == q_twos[32],
                   (ft32m, ft32_twos)))
    sx32 = pre32["sextet_census"]
    checks.append(("k32preread_sextet_census_machine_rederived",
                   sx32["counts"] == sx_census[32] and sx32["total"] == math.comb(32, 6)
                   and sx32.get("compared") in (None, math.comb(32, 6))
                   and sx32.get("mismatches", 0) == 0,
                   sx_census[32]))

    def regression_block_ok(block, idx):
        # machine re-derivation of a preread regression block for the
        # 1-based rank idx+1 (idx = 0-based root index); pairwise census
        # keys {b_only, zero, disjoint, total, expected_total} map
        # shared pairs to the b_only class as everywhere else.
        n = idx + 1
        problems = []
        if block["root"] != top[idx]["root"] or sorted(block["rows"]) != sorted(rows[idx]):
            problems.append("root/rows")
        nc = block["new_census"]
        pair = {"b_only": 0, "zero": 0, "disjoint": 0}
        for i in range(idx):
            pair[classify(rows, (idx, i))] += 1
        tri = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(idx), 2):
            tri[classify(rows, (idx,) + c)] += 1
        quad = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(idx), 3):
            quad[classify(rows, (idx,) + c)] += 1
        nb5 = len(q_new_b_only[n])
        for key in ("b_only", "zero", "disjoint"):
            if nc["pair"][key] != pair[key] or nc["pair"]["total"] != idx:
                problems.append(("pair", key))
            if nc["triple"][key] != tri[key] or nc["triple"]["total"] != math.comb(idx, 2):
                problems.append(("triple", key))
            if nc["quad"][key] != quad[key] or nc["quad"]["total"] != math.comb(idx, 3):
                problems.append(("quad", key))
        if (nc["quint"]["b_only"] != nb5
                or nc["quint"]["zero"] != math.comb(idx, 4) - nb5
                or nc["quint"]["disjoint"] != 0
                or nc["quint"]["total"] != math.comb(idx, 4)):
            problems.append("quint")
        htri, hquad, hq = {}, {}, {}
        for c in itertools.combinations(range(idx), 2):
            cl, two = classify2(rows, (idx,) + c)
            if cl == "b_only":
                htri[two] = htri.get(two, 0) + 1
        for c in itertools.combinations(range(idx), 3):
            cl, two = classify2(rows, (idx,) + c)
            if cl == "b_only":
                hquad[two] = hquad.get(two, 0) + 1
        for c in q_new_b_only[n]:
            cl, two = classify2(rows, c)
            hq[two] = hq.get(two, 0) + 1
        if not ({int(k): v for k, v in block["new_triple_double_row_histogram"].items()} == htri
                and {int(k): v for k, v in block["new_quad_double_row_histogram"].items()} == hquad
                and {int(k): v for k, v in block["new_quint_double_row_histogram"].items()} == hq):
            problems.append("drh")
        ftm = {"b_only": 0, "zero": 0, "disjoint": 0}
        ftw = {}
        for c in itertools.combinations(range(n), 3):
            cl, two = classify2(rows, c)
            ftm[cl] += 1
            if cl == "b_only":
                ftw[two] = ftw.get(two, 0) + 1
        if not (block["full_triples"]["counts"] == ftm
                and block["full_triples"]["total"] == math.comb(n, 3)
                and {int(k): v for k, v in block["full_triples"]["double_row_histogram"].items()} == ftw):
            problems.append("full_triples")
        if not (block["full_quints"]["counts"] == q_full[n]
                and block["full_quints"]["total"] == math.comb(n, 5)
                and {int(k): v for k, v in block["full_quints"]["double_row_histogram"].items()} == q_twos[n]):
            problems.append("full_quints")
        if not (block["sextet_census"]["counts"] == sx_census[n]
                and block["sextet_census"]["total"] == math.comb(n, 6)):
            problems.append("sextet")
        return (not problems), problems

    r30_ok, r30_bad = regression_block_ok(js["k32pre"]["rank30_regression"], 29)
    checks.append(("k32preread_rank30_regression_block_machine_rederived",
                   r30_ok, r30_bad[:6]))
    r31_ok, r31_bad = regression_block_ok(js["k32pre"]["rank31_regression"], 30)
    checks.append(("k32preread_rank31_regression_block_machine_rederived",
                   r31_ok, r31_bad[:6]))
    j32 = js["k32"]
    pmatch32 = {c["name"]: c["pass"] for c in j32["checks"]}
    need32 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k32json_preread_match_checks_all_present_and_pass",
                   all(pmatch32.get(nm) is True for nm in need32), need32))
    checks.append(("k32json_rank32_root_exactly_matches_aggregate",
                   int(j32["structure"]["rank32_root"]["membership"]) == em32
                   and int(j32["structure"]["rank32_root"]["a_part"]) == ea32
                   and int(j32["structure"]["rank32_root"]["b_part"]) == eb32
                   and j32["structure"]["rank32_root"]["root"] == top[31]["root"],
                   (str(em32), str(ea32), str(eb32))))

    # ---- preread layer 6 (k=33): the rank-33 structural preread JSON
    # (commit 67068e07, pure Python with exact integer serialization)
    # is re-derived machine-side from the pinned aggregate: root rows /
    # hex and the row-7 / row-19 prior hit indices (row 7 has exactly
    # one prior sharer: index 20 -- rank-33 is the first doubling of
    # row 7, triple layer 8 records and quad layer 11 records, never
    # the quint layer; row 19 is a hub row with 8 prior sharers), all
    # four new-layer censuses (pair shared/disjoint schema 9/23), the
    # three new-layer b_only double-row histograms, the b_only quint
    # four-subset profiles, the disjoint-quad fields (146 new disjoint
    # quads, every union exactly 8 rows; cumulative 966 asserted
    # against a fresh full C(32,4) disjoint count, no hardcoded
    # constants), the full triple census with its double-row
    # histogram, the full quint census and the all-zero sextet census
    # (1,107,568), both embedded regression blocks (rank-31 and
    # rank-32) re-derived with the same combined logic, and a closed
    # 3-system comparison that is new at this rank: the preread's
    # rank-32 regression block against the now-published k=32 result
    # JSON structure fields (the k=32 main publication postdates the
    # preread, whose own verification could only compare against the
    # k=32 preread JSON).  The three large integers must be the exact
    # aggregate values satisfying A+B==M.
    pre33 = js["k33pre"]["rank33"]
    hits7 = sorted(i for i in range(32) if 7 in rows[i])
    hits19 = sorted(i for i in range(32) if 19 in rows[i])
    em33 = int(mem[32])
    ea33 = int(memA[top[32]["root"]])
    eb33 = int(memB[top[32]["root"]])
    checks.append(("k33preread_rank33_root_prior_hits_exact_ints",
                   pre33["root"] == top[32]["root"]
                   and sorted(pre33["rows"]) == sorted(rows[32])
                   and pre33["prior_hits"] == {"7": len(hits7), "19": len(hits19)}
                   and {k: sorted(v) for k, v in pre33["prior_hit_indices"].items()}
                   == {"7": hits7, "19": hits19}
                   and int(pre33["membership"]) == em33
                   and int(pre33["a_part"]) == ea33
                   and int(pre33["b_part"]) == eb33
                   and ea33 + eb33 == em33,
                   (len(hits7), len(hits19), (ea33, eb33, em33))))
    nc33 = pre33["new_census"]
    shared33 = sum(1 for i in range(32) if set(rows[i]) & set(rows[32]))
    m33_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(32), 2):
        m33_tri[classify(rows, (32,) + c)] += 1
    m33_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(32), 3):
        m33_quad[classify(rows, (32,) + c)] += 1
    nb5_33 = len(q_new_b_only[33])
    checks.append(("k33preread_new_layer_censuses_machine_rederived",
                   nc33["pair"] == {"shared": shared33, "disjoint": 32 - shared33,
                                    "total": 32, "expected_total": 32}
                   and nc33["triple"]["b_only"] == m33_tri["b_only"]
                   and nc33["triple"]["zero"] == m33_tri["zero"]
                   and nc33["triple"]["disjoint"] == m33_tri["disjoint"]
                   and nc33["triple"]["total"] == nc33["triple"]["expected_total"]
                   == math.comb(32, 2)
                   and nc33["quad"]["b_only"] == m33_quad["b_only"]
                   and nc33["quad"]["zero"] == m33_quad["zero"]
                   and nc33["quad"]["disjoint"] == m33_quad["disjoint"]
                   and nc33["quad"]["total"] == nc33["quad"]["expected_total"]
                   == math.comb(32, 3)
                   and nc33["quint"]["b_only"] == nb5_33
                   and nc33["quint"]["zero"] == math.comb(32, 4) - nb5_33
                   and nc33["quint"]["disjoint"] == 0
                   and nc33["quint"]["total"] == nc33["quint"]["expected_total"]
                   == math.comb(32, 4),
                   (nc33["pair"], m33_tri, m33_quad, nb5_33)))
    h_tri33 = {}
    h_quad33 = {}
    h_qt33 = {}
    for c in itertools.combinations(range(32), 2):
        cl, two = classify2(rows, (32,) + c)
        if cl == "b_only":
            h_tri33[two] = h_tri33.get(two, 0) + 1
    for c in itertools.combinations(range(32), 3):
        cl, two = classify2(rows, (32,) + c)
        if cl == "b_only":
            h_quad33[two] = h_quad33.get(two, 0) + 1
    for c in q_new_b_only[33]:
        cl, two = classify2(rows, c)
        h_qt33[two] = h_qt33.get(two, 0) + 1
    checks.append(("k33preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri33 == {int(k): v for k, v in pre33["new_triple_double_row_histogram"].items()}
                   and h_quad33 == {int(k): v for k, v in pre33["new_quad_double_row_histogram"].items()}
                   and h_qt33 == {int(k): v for k, v in pre33["new_quint_double_row_histogram"].items()},
                   (h_tri33, h_quad33, h_qt33)))
    prof33 = {}
    for c in q_new_b_only[33]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof33[key] = prof33.get(key, 0) + 1
    dq33_sizes = {}
    dq33_cnt = 0
    for c in itertools.combinations(range(32), 3):
        if classify(rows, (32,) + c) == "disjoint":
            dq33_cnt += 1
            u = set()
            for i in (32,) + c:
                u |= set(rows[i])
            dq33_sizes[len(u)] = dq33_sizes.get(len(u), 0) + 1
    dj32 = 0
    for c in itertools.combinations(range(32), 4):
        if classify(rows, c) == "disjoint":
            dj32 += 1
    checks.append(("k33preread_quint_profiles_and_disjoint_quad_fields",
                   prof33 == {str(k): v for k, v in pre33["b_only_quint_four_subset_profiles"].items()}
                   and pre33["disjoint_quad_count"] == dq33_cnt
                   and dq33_cnt == m33_quad["disjoint"]
                   and {int(k): v for k, v in pre33["disjoint_quad_union_sizes"].items()} == dq33_sizes
                   and pre33["cumulative_disjoint_quads"] == dj32 + dq33_cnt,
                   (prof33, dq33_cnt, dq33_sizes, dj32)))
    ft33 = pre33["full_triples"]
    ft33m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft33_twos = {}
    for c in itertools.combinations(range(33), 3):
        cl, two = classify2(rows, c)
        ft33m[cl] += 1
        if cl == "b_only":
            ft33_twos[two] = ft33_twos.get(two, 0) + 1
    fq33 = pre33["full_quints"]
    checks.append(("k33preread_full_triples_and_quints_machine_rederived",
                   ft33["counts"] == ft33m and ft33["total"] == math.comb(33, 3)
                   and ft33.get("compared") in (None, math.comb(33, 3))
                   and ft33.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft33["double_row_histogram"].items()} == ft33_twos
                   and fq33["counts"] == q_full[33] and fq33["total"] == math.comb(33, 5)
                   and fq33.get("compared") in (None, math.comb(33, 5))
                   and fq33.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq33["double_row_histogram"].items()} == q_twos[33],
                   (ft33m, ft33_twos)))
    sx33 = pre33["sextet_census"]
    checks.append(("k33preread_sextet_census_machine_rederived",
                   sx33["counts"] == sx_census[33] and sx33["total"] == math.comb(33, 6)
                   and sx33.get("compared") in (None, math.comb(33, 6))
                   and sx33.get("mismatches", 0) == 0,
                   sx_census[33]))
    r31bs_ok, r31bs_bad = regression_block_ok(js["k33pre"]["rank31_regression"], 30)
    checks.append(("k33preread_rank31_regression_block_machine_rederived",
                   r31bs_ok, r31bs_bad[:6]))
    r32bs_ok, r32bs_bad = regression_block_ok(js["k33pre"]["rank32_regression"], 31)
    checks.append(("k33preread_rank32_regression_block_machine_rederived",
                   r32bs_ok, r32bs_bad[:6]))
    # closed 3-system comparison, new at this rank: the preread's
    # rank-32 regression block against the now-published k=32 result
    # JSON structure fields (its own pinned-input verification could
    # only compare against the k=32 preread JSON).
    r32reg = js["k33pre"]["rank32_regression"]
    j32st = js["k32"]["structure"]
    qreg = r32reg["new_census"]["quad"]
    checks.append(("k33preread_rank32_regression_matches_published_k32_result",
                   r32reg["root"] == j32st["rank32_root"]["root"]
                   and sorted(r32reg["rows"]) == sorted(j32st["rank32_root"]["rows"])
                   and r32reg["full_triples"]["counts"] == j32st["triple_census_k32"]
                   and int(qreg["b_only"]) == int(j32st["new_quad_census"]["b_only"])
                   and int(qreg["zero"]) == int(j32st["new_quad_census"]["zero"])
                   and int(qreg["disjoint"]) == int(j32st["new_quad_census"]["disjoint"])
                   and {k: int(v) for k, v in r32reg["full_quints"]["counts"].items()}
                   == {k: int(v) for k, v in j32st["quint_census_k32"].items()}
                   and {int(k): int(v) for k, v in r32reg["full_quints"]["double_row_histogram"].items()}
                   == {int(k): int(v) for k, v in j32st["quint_b_only_double_rows"].items()}
                   and {k: int(v) for k, v in r32reg["sextet_census"]["counts"].items()}
                   == {k: int(v) for k, v in j32st["sextet_census_k32"].items()}
                   and int(r32reg["membership"]) == int(j32st["rank32_root"]["membership"]),
                   None))
    j33 = js["k33"]
    pmatch33 = {c["name"]: c["pass"] for c in j33["checks"]}
    need33 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k33json_preread_match_checks_all_present_and_pass",
                   all(pmatch33.get(nm) is True for nm in need33), need33))
    checks.append(("k33json_rank33_root_exactly_matches_aggregate",
                   int(j33["structure"]["rank33_root"]["membership"]) == em33
                   and int(j33["structure"]["rank33_root"]["a_part"]) == ea33
                   and int(j33["structure"]["rank33_root"]["b_part"]) == eb33
                   and j33["structure"]["rank33_root"]["root"] == top[32]["root"],
                   (str(em33), str(ea33), str(eb33))))


    # ---- preread layer 7 (k=34): the rank-34 structural preread JSON
    # (commit 2a14f351, pure Python with exact integer serialization)
    # is re-derived machine-side from the pinned aggregate: root rows /
    # hex and the row-9 / row-19 prior hit indices (row 9 has exactly
    # one prior sharer: index 21 -- rank-34 is the first doubling of
    # row 9, triple layer 8 records and quad layer 11 records, never
    # the quint layer; row 19 is now a 9-sharer hub row, so the
    # rank-34 root (9,19) is the second consecutive row-19 root -- and
    # the preread's rank-33 regression block is additionally compared
    # field-by-field against the now-published k=33 result JSON
    # structure fields), all four new-layer censuses (pair
    # shared/disjoint schema 10/23), the three new-layer b_only
    # double-row histograms, the b_only quint four-subset profiles,
    # the disjoint-quad fields (146 new disjoint quads, every union
    # exactly 8 rows; cumulative 1,112 asserted against a fresh full
    # C(33,4) disjoint count, no hardcoded constants), the full
    # triple census with its double-row histogram, the full quint
    # census and the all-zero sextet census (1,344,904), and both
    # embedded regression blocks (rank-32 and rank-33) re-derived
    # with the same combined logic.  The three large integers must
    # be the exact aggregate values satisfying A+B==M.
    pre34 = js["k34pre"]["rank34"]
    hits9 = sorted(i for i in range(33) if 9 in rows[i])
    hits19b = sorted(i for i in range(33) if 19 in rows[i])
    em34 = int(mem[33])
    ea34 = int(memA[top[33]["root"]])
    eb34 = int(memB[top[33]["root"]])
    checks.append(("k34preread_rank34_root_prior_hits_exact_ints",
                   pre34["root"] == top[33]["root"]
                   and sorted(pre34["rows"]) == sorted(rows[33])
                   and pre34["prior_hits"] == {"9": len(hits9), "19": len(hits19b)}
                   and {k: sorted(v) for k, v in pre34["prior_hit_indices"].items()}
                   == {"9": hits9, "19": hits19b}
                   and int(pre34["membership"]) == em34
                   and int(pre34["a_part"]) == ea34
                   and int(pre34["b_part"]) == eb34
                   and ea34 + eb34 == em34,
                   (len(hits9), len(hits19b), (ea34, eb34, em34))))
    nc34 = pre34["new_census"]
    shared34 = sum(1 for i in range(33) if set(rows[i]) & set(rows[33]))
    m34_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(33), 2):
        m34_tri[classify(rows, (33,) + c)] += 1
    m34_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(33), 3):
        m34_quad[classify(rows, (33,) + c)] += 1
    nb5_34 = len(q_new_b_only[34])
    checks.append(("k34preread_new_layer_censuses_machine_rederived",
                   nc34["pair"] == {"shared": shared34, "disjoint": 33 - shared34,
                                    "total": 33, "expected_total": 33}
                   and nc34["triple"]["b_only"] == m34_tri["b_only"]
                   and nc34["triple"]["zero"] == m34_tri["zero"]
                   and nc34["triple"]["disjoint"] == m34_tri["disjoint"]
                   and nc34["triple"]["total"] == nc34["triple"]["expected_total"]
                   == math.comb(33, 2)
                   and nc34["quad"]["b_only"] == m34_quad["b_only"]
                   and nc34["quad"]["zero"] == m34_quad["zero"]
                   and nc34["quad"]["disjoint"] == m34_quad["disjoint"]
                   and nc34["quad"]["total"] == nc34["quad"]["expected_total"]
                   == math.comb(33, 3)
                   and nc34["quint"]["b_only"] == nb5_34
                   and nc34["quint"]["zero"] == math.comb(33, 4) - nb5_34
                   and nc34["quint"]["disjoint"] == 0
                   and nc34["quint"]["total"] == nc34["quint"]["expected_total"]
                   == math.comb(33, 4),
                   (nc34["pair"], m34_tri, m34_quad, nb5_34)))
    h_tri34 = {}
    h_quad34 = {}
    h_qt34 = {}
    for c in itertools.combinations(range(33), 2):
        cl, two = classify2(rows, (33,) + c)
        if cl == "b_only":
            h_tri34[two] = h_tri34.get(two, 0) + 1
    for c in itertools.combinations(range(33), 3):
        cl, two = classify2(rows, (33,) + c)
        if cl == "b_only":
            h_quad34[two] = h_quad34.get(two, 0) + 1
    for c in q_new_b_only[34]:
        cl, two = classify2(rows, c)
        h_qt34[two] = h_qt34.get(two, 0) + 1
    checks.append(("k34preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri34 == {int(k): v for k, v in pre34["new_triple_double_row_histogram"].items()}
                   and h_quad34 == {int(k): v for k, v in pre34["new_quad_double_row_histogram"].items()}
                   and h_qt34 == {int(k): v for k, v in pre34["new_quint_double_row_histogram"].items()},
                   (h_tri34, h_quad34, h_qt34)))
    prof34 = {}
    for c in q_new_b_only[34]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof34[key] = prof34.get(key, 0) + 1
    dq34_sizes = {}
    dq34_cnt = 0
    for c in itertools.combinations(range(33), 3):
        if classify(rows, (33,) + c) == "disjoint":
            dq34_cnt += 1
            u = set()
            for i in (33,) + c:
                u |= set(rows[i])
            dq34_sizes[len(u)] = dq34_sizes.get(len(u), 0) + 1
    dj33 = 0
    for c in itertools.combinations(range(33), 4):
        if classify(rows, c) == "disjoint":
            dj33 += 1
    checks.append(("k34preread_quint_profiles_and_disjoint_quad_fields",
                   prof34 == {str(k): v for k, v in pre34["b_only_quint_four_subset_profiles"].items()}
                   and pre34["disjoint_quad_count"] == dq34_cnt
                   and dq34_cnt == m34_quad["disjoint"]
                   and {int(k): v for k, v in pre34["disjoint_quad_union_sizes"].items()} == dq34_sizes
                   and pre34["cumulative_disjoint_quads"] == dj33 + dq34_cnt,
                   (prof34, dq34_cnt, dq34_sizes, dj33)))
    ft34 = pre34["full_triples"]
    ft34m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft34_twos = {}
    for c in itertools.combinations(range(34), 3):
        cl, two = classify2(rows, c)
        ft34m[cl] += 1
        if cl == "b_only":
            ft34_twos[two] = ft34_twos.get(two, 0) + 1
    fq34 = pre34["full_quints"]
    checks.append(("k34preread_full_triples_and_quints_machine_rederived",
                   ft34["counts"] == ft34m and ft34["total"] == math.comb(34, 3)
                   and ft34.get("compared") in (None, math.comb(34, 3))
                   and ft34.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft34["double_row_histogram"].items()} == ft34_twos
                   and fq34["counts"] == q_full[34] and fq34["total"] == math.comb(34, 5)
                   and fq34.get("compared") in (None, math.comb(34, 5))
                   and fq34.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq34["double_row_histogram"].items()} == q_twos[34],
                   (ft34m, ft34_twos)))
    sx34 = pre34["sextet_census"]
    checks.append(("k34preread_sextet_census_machine_rederived",
                   sx34["counts"] == sx_census[34] and sx34["total"] == math.comb(34, 6)
                   and sx34.get("compared") in (None, math.comb(34, 6))
                   and sx34.get("mismatches", 0) == 0,
                   sx_census[34]))
    r32bs_ok, r32bs_bad = regression_block_ok(js["k34pre"]["rank32_regression"], 31)
    checks.append(("k34preread_rank32_regression_block_machine_rederived",
                   r32bs_ok, r32bs_bad[:6]))
    r33bs_ok, r33bs_bad = regression_block_ok(js["k34pre"]["rank33_regression"], 32)
    checks.append(("k34preread_rank33_regression_block_machine_rederived",
                   r33bs_ok, r33bs_bad[:6]))
    # closed 3-system comparison, same pattern as the k=33 rank: the
    # preread's rank-33 regression block against the now-published
    # k=33 result JSON structure fields (its own pinned-input
    # verification predates the k=33 main publication and could only
    # compare against the k=33 preread JSON).
    r33reg = js["k34pre"]["rank33_regression"]
    j33st = js["k33"]["structure"]
    qreg34 = r33reg["new_census"]["quad"]
    checks.append(("k34preread_rank33_regression_matches_published_k33_result",
                   r33reg["root"] == j33st["rank33_root"]["root"]
                   and sorted(r33reg["rows"]) == sorted(j33st["rank33_root"]["rows"])
                   and r33reg["full_triples"]["counts"] == j33st["triple_census_k33"]
                   and int(qreg34["b_only"]) == int(j33st["new_quad_census"]["b_only"])
                   and int(qreg34["zero"]) == int(j33st["new_quad_census"]["zero"])
                   and int(qreg34["disjoint"]) == int(j33st["new_quad_census"]["disjoint"])
                   and {k: int(v) for k, v in r33reg["full_quints"]["counts"].items()}
                   == {k: int(v) for k, v in j33st["quint_census_k33"].items()}
                   and {int(k): int(v) for k, v in r33reg["full_quints"]["double_row_histogram"].items()}
                   == {int(k): int(v) for k, v in j33st["quint_b_only_double_rows"].items()}
                   and {k: int(v) for k, v in r33reg["sextet_census"]["counts"].items()}
                   == {k: int(v) for k, v in j33st["sextet_census_k33"].items()}
                   and int(r33reg["membership"]) == int(j33st["rank33_root"]["membership"]),
                   None))
    j34 = js["k34"]
    pmatch34 = {c["name"]: c["pass"] for c in j34["checks"]}
    need34 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k34json_preread_match_checks_all_present_and_pass",
                   all(pmatch34.get(nm) is True for nm in need34), need34))
    checks.append(("k34json_rank34_root_exactly_matches_aggregate",
                   int(j34["structure"]["rank34_root"]["membership"]) == em34
                   and int(j34["structure"]["rank34_root"]["a_part"]) == ea34
                   and int(j34["structure"]["rank34_root"]["b_part"]) == eb34
                   and j34["structure"]["rank34_root"]["root"] == top[33]["root"],
                   (str(em34), str(ea34), str(eb34))))

    # ---- preread layer 8 (k=35): the rank-35 structural preread JSON
    # (commit 90fc51c9, pure Python with exact integer serialization,
    # independently verified by a second derivation lineage at commit
    # 41c4cf12) is re-derived machine-side from the pinned aggregate:
    # root rows / hex and the row-18 / row-21 prior hit indices (row 18
    # is now a 16-sharer hub band row; row 21 has zero prior sharers
    # among the top-34, a first-ever cover at rank-35, so row 21 can
    # never double in any layer), all four new-layer censuses (pair
    # shared/disjoint schema 16/18), the three new-layer b_only
    # double-row histograms, the b_only quint four-subset profiles,
    # the disjoint-quad fields (83 new disjoint quads, every union
    # exactly 8 rows; cumulative 1,195 asserted against a fresh full
    # C(34,4) disjoint count, no hardcoded constants), the full triple
    # census with its double-row histogram, the full quint census and
    # the all-zero sextet census (1,623,160), both embedded regression
    # blocks (rank-33 and rank-34) re-derived with the same combined
    # logic, and a closed 3-system comparison, same pattern as layers
    # 6/7: the preread's rank-34 regression block against the
    # now-published k=34 result JSON structure fields (an independent
    # third system: the preread's own load-time asserts and the main
    # lane's preread_match checks are the other two).  The three
    # large integers must be the exact aggregate values satisfying
    # A+B==M.
    pre35 = js["k35pre"]["rank35"]
    hits18b = sorted(i for i in range(34) if 18 in rows[i])
    hits21 = sorted(i for i in range(34) if 21 in rows[i])
    em35 = int(mem[34])
    ea35 = int(memA[top[34]["root"]])
    eb35 = int(memB[top[34]["root"]])
    checks.append(("k35preread_rank35_root_prior_hits_exact_ints",
                   pre35["root"] == top[34]["root"]
                   and sorted(pre35["rows"]) == sorted(rows[34])
                   and pre35["prior_hits"] == {"18": len(hits18b), "21": len(hits21)}
                   and {k: sorted(v) for k, v in pre35["prior_hit_indices"].items()}
                   == {"18": hits18b, "21": hits21}
                   and int(pre35["membership"]) == em35
                   and int(pre35["a_part"]) == ea35
                   and int(pre35["b_part"]) == eb35
                   and ea35 + eb35 == em35,
                   (len(hits18b), len(hits21), (ea35, eb35, em35))))
    nc35 = pre35["new_census"]
    shared35 = sum(1 for i in range(34) if set(rows[i]) & set(rows[34]))
    m35_tri = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(34), 2):
        m35_tri[classify(rows, (34,) + c)] += 1
    m35_quad = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(34), 3):
        m35_quad[classify(rows, (34,) + c)] += 1
    nb5_35 = len(q_new_b_only[35])
    checks.append(("k35preread_new_layer_censuses_machine_rederived",
                   nc35["pair"] == {"shared": shared35, "disjoint": 34 - shared35,
                                    "total": 34, "expected_total": 34}
                   and nc35["triple"]["b_only"] == m35_tri["b_only"]
                   and nc35["triple"]["zero"] == m35_tri["zero"]
                   and nc35["triple"]["disjoint"] == m35_tri["disjoint"]
                   and nc35["triple"]["total"] == nc35["triple"]["expected_total"]
                   == math.comb(34, 2)
                   and nc35["quad"]["b_only"] == m35_quad["b_only"]
                   and nc35["quad"]["zero"] == m35_quad["zero"]
                   and nc35["quad"]["disjoint"] == m35_quad["disjoint"]
                   and nc35["quad"]["total"] == nc35["quad"]["expected_total"]
                   == math.comb(34, 3)
                   and nc35["quint"]["b_only"] == nb5_35
                   and nc35["quint"]["zero"] == math.comb(34, 4) - nb5_35
                   and nc35["quint"]["disjoint"] == 0
                   and nc35["quint"]["total"] == nc35["quint"]["expected_total"]
                   == math.comb(34, 4),
                   (nc35["pair"], m35_tri, m35_quad, nb5_35)))
    h_tri35 = {}
    h_quad35 = {}
    h_qt35 = {}
    for c in itertools.combinations(range(34), 2):
        cl, two = classify2(rows, (34,) + c)
        if cl == "b_only":
            h_tri35[two] = h_tri35.get(two, 0) + 1
    for c in itertools.combinations(range(34), 3):
        cl, two = classify2(rows, (34,) + c)
        if cl == "b_only":
            h_quad35[two] = h_quad35.get(two, 0) + 1
    for c in q_new_b_only[35]:
        cl, two = classify2(rows, c)
        h_qt35[two] = h_qt35.get(two, 0) + 1
    checks.append(("k35preread_new_layer_double_row_histograms_machine_rederived",
                   h_tri35 == {int(k): v for k, v in pre35["new_triple_double_row_histogram"].items()}
                   and h_quad35 == {int(k): v for k, v in pre35["new_quad_double_row_histogram"].items()}
                   and h_qt35 == {int(k): v for k, v in pre35["new_quint_double_row_histogram"].items()},
                   (h_tri35, h_quad35, h_qt35)))
    prof35 = {}
    for c in q_new_b_only[35]:
        p = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            p[classify(rows, tuple(x for j, x in enumerate(c) if j != drop))] += 1
        key = "%d/%d/%d" % (p["b_only"], p["disjoint"], p["zero"])
        prof35[key] = prof35.get(key, 0) + 1
    dq35_sizes = {}
    dq35_cnt = 0
    for c in itertools.combinations(range(34), 3):
        if classify(rows, (34,) + c) == "disjoint":
            dq35_cnt += 1
            u = set()
            for i in (34,) + c:
                u |= set(rows[i])
            dq35_sizes[len(u)] = dq35_sizes.get(len(u), 0) + 1
    dj34 = 0
    for c in itertools.combinations(range(34), 4):
        if classify(rows, c) == "disjoint":
            dj34 += 1
    checks.append(("k35preread_quint_profiles_and_disjoint_quad_fields",
                   prof35 == {str(k): v for k, v in pre35["b_only_quint_four_subset_profiles"].items()}
                   and pre35["disjoint_quad_count"] == dq35_cnt
                   and dq35_cnt == m35_quad["disjoint"]
                   and {int(k): v for k, v in pre35["disjoint_quad_union_sizes"].items()} == dq35_sizes
                   and pre35["cumulative_disjoint_quads"] == dj34 + dq35_cnt,
                   (prof35, dq35_cnt, dq35_sizes, dj34)))
    ft35 = pre35["full_triples"]
    ft35m = {"b_only": 0, "zero": 0, "disjoint": 0}
    ft35_twos = {}
    for c in itertools.combinations(range(35), 3):
        cl, two = classify2(rows, c)
        ft35m[cl] += 1
        if cl == "b_only":
            ft35_twos[two] = ft35_twos.get(two, 0) + 1
    fq35 = pre35["full_quints"]
    checks.append(("k35preread_full_triples_and_quints_machine_rederived",
                   ft35["counts"] == ft35m and ft35["total"] == math.comb(35, 3)
                   and ft35.get("compared") in (None, math.comb(35, 3))
                   and ft35.get("mismatches", 0) == 0
                   and {int(k): v for k, v in ft35["double_row_histogram"].items()} == ft35_twos
                   and fq35["counts"] == q_full[35] and fq35["total"] == math.comb(35, 5)
                   and fq35.get("compared") in (None, math.comb(35, 5))
                   and fq35.get("mismatches", 0) == 0
                   and {int(k): v for k, v in fq35["double_row_histogram"].items()} == q_twos[35],
                   (ft35m, ft35_twos)))
    sx35 = pre35["sextet_census"]
    checks.append(("k35preread_sextet_census_machine_rederived",
                   sx35["counts"] == sx_census[35] and sx35["total"] == math.comb(35, 6)
                   and sx35.get("compared") in (None, math.comb(35, 6))
                   and sx35.get("mismatches", 0) == 0,
                   sx_census[35]))
    r33b35_ok, r33b35_bad = regression_block_ok(js["k35pre"]["rank33_regression"], 32)
    checks.append(("k35preread_rank33_regression_block_machine_rederived",
                   r33b35_ok, r33b35_bad[:6]))
    r34b35_ok, r34b35_bad = regression_block_ok(js["k35pre"]["rank34_regression"], 33)
    checks.append(("k35preread_rank34_regression_block_machine_rederived",
                   r34b35_ok, r34b35_bad[:6]))
    # closed 3-system comparison, same pattern as layers 6/7: the
    # preread's rank-34 regression block against the now-published
    # k=34 result JSON structure fields.
    r34reg = js["k35pre"]["rank34_regression"]
    j34st = js["k34"]["structure"]
    qreg35 = r34reg["new_census"]["quad"]
    checks.append(("k35preread_rank34_regression_matches_published_k34_result",
                   r34reg["root"] == j34st["rank34_root"]["root"]
                   and sorted(r34reg["rows"]) == sorted(j34st["rank34_root"]["rows"])
                   and r34reg["full_triples"]["counts"] == j34st["triple_census_k34"]
                   and int(qreg35["b_only"]) == int(j34st["new_quad_census"]["b_only"])
                   and int(qreg35["zero"]) == int(j34st["new_quad_census"]["zero"])
                   and int(qreg35["disjoint"]) == int(j34st["new_quad_census"]["disjoint"])
                   and {k: int(v) for k, v in r34reg["full_quints"]["counts"].items()}
                   == {k: int(v) for k, v in j34st["quint_census_k34"].items()}
                   and {int(k): int(v) for k, v in r34reg["full_quints"]["double_row_histogram"].items()}
                   == {int(k): int(v) for k, v in j34st["quint_b_only_double_rows"].items()}
                   and {k: int(v) for k, v in r34reg["sextet_census"]["counts"].items()}
                   == {k: int(v) for k, v in j34st["sextet_census_k34"].items()}
                   and int(r34reg["membership"]) == int(j34st["rank34_root"]["membership"]),
                   None))
    j35 = js["k35"]
    pmatch35 = {c["name"]: c["pass"] for c in j35["checks"]}
    need35 = ("preread_match.triple_census", "preread_match.new_quad_census",
              "preread_match.quint_census", "preread_match.quint_double_rows",
              "preread_match.sextet_census")
    checks.append(("k35json_preread_match_checks_all_present_and_pass",
                   all(pmatch35.get(nm) is True for nm in need35), need35))
    checks.append(("k35json_rank35_root_exactly_matches_aggregate",
                   int(j35["structure"]["rank35_root"]["membership"]) == em35
                   and int(j35["structure"]["rank35_root"]["a_part"]) == ea35
                   and int(j35["structure"]["rank35_root"]["b_part"]) == eb35
                   and j35["structure"]["rank35_root"]["root"] == top[34]["root"],
                   (str(em35), str(ea35), str(eb35))))

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


    # Two closure checks added after the 201-check k=34 publication
    # (plus two more closing the k=35 era and two more closing the
    # k=36 era, appended below):
    # compare the embedded regression blocks directly with their earlier
    # preread publications, and compare the rank-34 preread's full
    # structure fields directly with the published k=34 result JSON.
    s34 = j34["structure"]
    def regression_projection(block):
        nc = block["new_census"]
        pair = nc["pair"]
        pair_norm = {
            "b_only": pair.get("b_only", pair.get("shared", 0)),
            "zero": pair.get("zero", 0),
            "disjoint": pair["disjoint"],
            "total": pair["total"],
            "expected_total": pair["expected_total"],
        }
        def census_projection(x):
            return {"counts": x["counts"], "total": x["total"],
                    "double_row_histogram": x.get("double_row_histogram", {})}
        def sextet_projection(x):
            return {"counts": x["counts"], "total": x["total"]}
        return {
            "root": block["root"], "rows": block["rows"],
            "membership": block["membership"], "a_part": block["a_part"],
            "b_part": block["b_part"], "prior_hits": block["prior_hits"],
            "prior_hit_indices": block["prior_hit_indices"],
            "new_census": {
                "pair": pair_norm,
                "triple": nc["triple"], "quad": nc["quad"], "quint": nc["quint"],
            },
            "new_quint_double_row_histogram": block["new_quint_double_row_histogram"],
            "new_triple_double_row_histogram": block["new_triple_double_row_histogram"],
            "new_quad_double_row_histogram": block["new_quad_double_row_histogram"],
            "full_triples": census_projection(block["full_triples"]),
            "full_quints": census_projection(block["full_quints"]),
            "sextet_census": sextet_projection(block["sextet_census"]),
        }
    checks.append(("k34preread_embedded_rank32_rank33_blocks_match_prior_prereads",
                   regression_projection(js["k34pre"]["rank32_regression"])
                   == regression_projection(js["k32pre"]["rank32"])
                   and regression_projection(js["k34pre"]["rank33_regression"])
                   == regression_projection(js["k33pre"]["rank33"]),
                   None))
    def published_histogram(obj):
        return {int(k): v for k, v in obj.get("histogram", obj).items()}
    checks.append(("k34json_preread_structure_matches_published_result",
                   s34["new_quad_census"] == {k: nc34["quad"][k] for k in ("b_only", "zero", "disjoint")}
                   and s34["new_quint_census"] == {k: nc34["quint"][k] for k in ("b_only", "zero", "disjoint")}
                   and s34["quints_zero_synth_count"] == nc34["quint"]["zero"]
                   and s34["triple_census_k34"] == ft34["counts"]
                   and s34["quint_census_k34"] == fq34["counts"]
                   and s34["sextet_census_k34"] == sx34["counts"]
                   and published_histogram(s34["new_triple_b_only_double_row_histogram"]) == h_tri34
                   and published_histogram(s34["new_quad_b_only_double_row_histogram"]) == h_quad34
                   and {int(k): v for k, v in s34["quint_b_only_double_rows"].items()} == q_twos[34],
                   None))

    # Two more closure checks close the k=35 era the same way: the
    # k=35 preread's embedded regression blocks against their earlier
    # preread publications, and the rank-35 preread's full structural
    # fields against the published k=35 result JSON (which was
    # produced by the parallel main lane from the same pinned inputs
    # and was rerun end-to-end by the verification lane before any of
    # these artifacts were pinned).
    checks.append(("k35preread_embedded_rank33_rank34_blocks_match_prior_prereads",
                   regression_projection(js["k35pre"]["rank33_regression"])
                   == regression_projection(js["k33pre"]["rank33"])
                   and regression_projection(js["k35pre"]["rank34_regression"])
                   == regression_projection(js["k34pre"]["rank34"]),
                   None))
    s35 = j35["structure"]
    checks.append(("k35json_preread_structure_matches_published_result",
                   s35["new_quad_census"] == {k: nc35["quad"][k] for k in ("b_only", "zero", "disjoint")}
                   and s35["new_quint_census"] == {k: nc35["quint"][k] for k in ("b_only", "zero", "disjoint")}
                   and s35["quints_zero_synth_count"] == nc35["quint"]["zero"]
                   and s35["triple_census_k35"] == ft35["counts"]
                   and s35["quint_census_k35"] == fq35["counts"]
                   and s35["sextet_census_k35"] == sx35["counts"]
                   and published_histogram(s35["new_triple_b_only_double_row_histogram"]) == h_tri35
                   and published_histogram(s35["new_quad_b_only_double_row_histogram"]) == h_quad35
                   and {int(k): v for k, v in s35["quint_b_only_double_rows"].items()} == q_twos[35],
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
                   None))

    n_fail = 0
    for name, ok, extra in checks:
        print(("PASS" if ok else "FAIL"), name, extra if extra is not None else "")
        n_fail += 0 if ok else 1
    print(f"--- {len(checks)} checks, {n_fail} failures")
    print(f"grand total = {T}")
    print("kill(k)% =", {k: round(kill[k] / T * 100, 4) for k in sorted(kill)})
    report = {
        "schema": "n11-cost16-k36-crosscheck-20261119-v1",
        "date": "2026-11-19",
        "source_main_commit": "b1484dddb9e410c23f024d6759305b13b98afe1a",
        "source_note": ("k=36 edition: extends the k=35 crosscheck "
                        "(script published as commit a956245b) with the "
                        "k=36 record and preread layers and the k=36 era "
                        "closures (the k=36 main artifacts were verified "
                        "against their published blob sha1s before the "
                        "pins were recorded; preread reproduced on the "
                        "Proxmox runner)"),
        "inputs": {
            **{tag: {"file": name, "git_blob_sha1": sha}
               for tag, (name, sha) in PINS.items()},
            "k34_jsonl": {"file": JSONL_K34[0], "git_blob_sha1": JSONL_K34[1]},
            "k35_jsonl": {"file": JSONL_K35[0], "git_blob_sha1": JSONL_K35[1]},
            "k36_jsonl": {"file": JSONL_K36[0], "git_blob_sha1": JSONL_K36[1]},
        },
        "check_count": len(checks),
        "all_pass": n_fail == 0,
        "checks": [{"name": name, "pass": bool(ok), "detail": extra}
                   for name, ok, extra in checks],
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True, default=str)
        f.write("\n")
    print("wrote", args.out)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
