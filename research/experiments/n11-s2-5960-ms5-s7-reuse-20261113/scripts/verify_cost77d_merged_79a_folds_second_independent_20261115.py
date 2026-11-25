#!/usr/bin/env python3
"""Second independent verification of the four landed class2-lane folds:
cost-77d receipts fold (head 1290 -> 1299), merged cost-75d+77d warm-hygiene
fold (head 1296 -> 1302), cost-79a receipts fold (head 1302 -> 1304) and
cost-80d receipts fold (head 1304 -> 1305).

Method: the four published fold scripts are re-executed end-to-end from this
fresh codeload-main mirror (no state from the landing sessions), each in its own
short-lived subprocess and twice over; every built-in control must pass, every
regenerated output must be byte-identical to the published git blobs, and the
two reruns must agree. On top of that, this script adds controls the fold scripts
do not contain:

  * the cost-77d bit-78 duplicate-root identity is asserted directly: the
    published 77d bit-78 root must equal the 75d bit-92 receipt root raw-hex,
    and every independently re-derived covers(root) orbit of the bit-78 root
    must already be solved at the 1296 baseline (zero marginal, which is what
    justifies the merged fold excluding it from the receipt list);
  * the 12 (77d) + 3 (79a) new roots are re-canonicalized with an independent
    8-element D4 board-group implementation and re-checked disjoint (raw and
    D4) against the pre-fold inventories (565 @1290, 569 @1296, 580 @1302);
  * the legal candidate enumerations of the 77d and 79a children are
    re-derived from scratch with exact-integer Bareiss determinants and must
    equal the published claim candidate lists;
  * the published pre-fold prediction brief
    (class2-lane-cost77d-fold-prediction-20261115.json) is compared field by
    field against the landed merged fold (head numbers, per-bit marginals,
    parent row losses, zero-mim convention).

Interpretation guard: solved counts measure manifest coverage, not the
game-theoretic value of any position; REFUTED-D10 is not a LOSS proof; WIN7
certificates prove a win within depth 10 from the individual 7-stone roots
only; the 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60},
class 1, class 2 and class 4 all remain UNKNOWN.
"""
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCR = HERE / "scripts"

N = 11
XR = [i % N for i in range(N * N)]
YR = [i // N for i in range(N * N)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(N * N)]


def det4(a, b, c, d):
    """Exact-integer Bareiss determinant of [[q,x,y,1]] rows: zero iff the
    four cells lie on a common circle or line (kyoen-relevant degeneracy)."""
    mm = [[QR[a], XR[a], YR[a], 1],
          [QR[b], XR[b], YR[b], 1],
          [QR[c], XR[c], YR[c], 1],
          [QR[d], XR[d], YR[d], 1]]
    prev = 1
    for k in range(3):
        if mm[k][k] == 0:
            for r in range(k + 1, 4):
                if mm[r][k] != 0:
                    mm[k], mm[r] = mm[r], mm[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                mm[i][j] = (mm[i][j] * mm[k][k] - mm[i][k] * mm[k][j]) // prev
        prev = mm[k][k]
    return mm[3][3]


def d4_canonical(pattern):
    """Minimum 128-bit pattern over the 8 board symmetries (independent D4)."""
    stones = [i for i in range(N * N) if (pattern >> i) & 1]
    best = None
    for t in range(8):
        v = 0
        for i in stones:
            x, y = XR[i], YR[i]
            if t == 0:
                nx, ny = x, y
            elif t == 1:
                nx, ny = N - 1 - y, x
            elif t == 2:
                nx, ny = N - 1 - x, N - 1 - y
            elif t == 3:
                nx, ny = y, N - 1 - x
            elif t == 4:
                nx, ny = x, N - 1 - y
            elif t == 5:
                nx, ny = N - 1 - x, y
            elif t == 6:
                nx, ny = y, x
            else:
                nx, ny = N - 1 - y, N - 1 - x
            v |= 1 << (nx + N * ny)
        if best is None or v < best:
            best = v
    return best


def independent_covers(root_v):
    """D4-canonical one-stone-deletion orbits of a 7-stone root, recomputed
    with the independent D4 group (the chain's covers() equivalent)."""
    stones = [i for i in range(N * N) if (root_v >> i) & 1]
    assert len(stones) == 7
    return {d4_canonical(root_v & ~(1 << s)) for s in stones}


def legal_candidates(child_pattern):
    """Empty cells whose 7-stone completion keeps the position free of any
    4-on-a-circle/line degeneracy, re-derived from scratch."""
    stones = [i for i in range(N * N) if (child_pattern >> i) & 1]
    assert len(stones) == 6
    forbidden = 0
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for d in range(N * N):
                    if (child_pattern >> d) & 1:
                        continue
                    if det4(stones[i], stones[j], stones[k], d) == 0:
                        forbidden |= 1 << d
    return sorted(p for p in range(N * N)
                  if not (child_pattern >> p) & 1 and not (forbidden >> p) & 1)


def git_blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return git_blob_sha_bytes(data), len(data), hashlib.md5(data).hexdigest()


# published output artifacts (file -> git blob sha on main)
PUBLISHED = {
    "class-frontier-cost77d-receipts-recompute-20261115.json":
        "d19c96b7cb0a01f8fd50179b3ff77595408537d7",
    "class-frontier-s5-ranking-after-cost77d-receipts-20261115.csv":
        "a69f5e7a19ccb0ef4565de6c6b5be303eb80e60c",
    "class-frontier-top-candidates-s6-after-cost77d-receipts-20261115.csv":
        "49b7f37815f120829d86cd2370dbd0026dec1d63",
    "class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json":
        "97130384432e4a0e1e022292748f9fed1e957c0f",
    "class-frontier-s5-ranking-after-merged-cost75d-77d-20261115.csv":
        "aba88980c02505b37da936de0f3d19eb23d37798",
    "class-frontier-top-candidates-s6-after-merged-cost75d-77d-20261115.csv":
        "49b7f37815f120829d86cd2370dbd0026dec1d63",
    "class-frontier-cost79a-receipts-recompute-20261115.json":
        "7dea99ffe76d767223666241964824f005843893",
    "class-frontier-s5-ranking-after-cost79a-receipts-20261115.csv":
        "d31201b1f846733e2510a57e4cb15281db8e9660",
    "class-frontier-top-candidates-s6-after-cost79a-receipts-20261115.csv":
        "34efacb35fc6437740745e0ed631c982d06feb96",
    "class-frontier-cost80d-receipts-recompute-20261115.json":
        "289c93373692d6627347dc9bbb9ffdc3653f508b",
    "class-frontier-s5-ranking-after-cost80d-receipts-20261115.csv":
        "723e1e1ec05ede265595d0ff997ff3a019eca8a1",
    "class-frontier-top-candidates-s6-after-cost80d-receipts-20261115.csv":
        "a38f1563bb82de256922949d5b5ed8fe39f88cf5",
}

SCRIPTS = [
    "recompute_frontier_cost77d_receipts_20261115.py",
    "recompute_frontier_merged_cost75d_77d_20261115.py",
    "recompute_frontier_cost79a_receipts_20261115.py",
    "recompute_frontier_cost80d_receipts_20261115.py",
]

ROOTS_77D = {
    7: "00000000100000801202000000200080",
    12: "00000000100000801202000000201000",
    39: "00000000100000801202008000200000",
    58: "00000000100000801602000000200000",
    62: "00000000100000805202000000200000",
    64: "00000000100000811202000000200000",
    66: "00000000100000841202000000200000",
    78: "00000000100040801202000000200000",
    94: "00000000500000801202000000200000",
    96: "00000001100000801202000000200000",
    108: "00001000100000801202000000200000",
    111: "00008000100000801202000000200000",
}
CHILD_77D = "00000000100000801202000000200000"
ROOTS_79A = {
    9: "00000000000000801212000000200200",
    50: "00000000000000801216000000200000",
    64: "00000000000000811212000000200000",
}
CHILD_79A = "00000000000000801212000000200000"
ROOTS_80D = {
    48: "00000008000000809003000000000400",
    61: "0000000800000080b002000000000400",
    81: "00000008000200809002000000000400",
    96: "00000009000000809002000000000400",
}
CHILD_80D = "00000008000000809002000000000400"

# capture the published bytes before the fold scripts overwrite them
published_bytes = {f: (OUT / f).read_bytes() for f in PUBLISHED}
published_ok = all(
    git_blob_sha_bytes(published_bytes[f]) == PUBLISHED[f] for f in PUBLISHED)
assert published_ok, "the mirror must hold the published blobs before any rerun"
print("CONTROL published artifacts present in the fresh mirror and blob-pinned:",
      len(PUBLISHED), "files")

# ---------- 1. re-execute the four published fold scripts end-to-end ----------
script_blobs = {}
for s in SCRIPTS:
    sha, blen, md5 = git_blob_sha(SCR / s)
    script_blobs[s] = {"git_blob_sha": sha, "bytes": blen, "md5": md5}
    print(f"CONTROL fold script blob pinned: {s} {sha} ({blen} B)")

import subprocess
import sys

GROUPS = [
    # (script, output files it owns, state var: name -> namespace variable)
    (SCRIPTS[0], [f for f in PUBLISHED if "cost77d" in f],
     {"s_1290": "s_base", "s_1299": "s_cur", "prev_1290": "prev"}),
    (SCRIPTS[1], [f for f in PUBLISHED if "merged-cost75d-77d" in f],
     {"s_1296": "s_base", "s_1302": "s_cur", "prev_1296": "prev"}),
    (SCRIPTS[2], [f for f in PUBLISHED if "cost79a" in f],
     {"s_1304": "s_cur", "prev_1302": "prev"}),
    (SCRIPTS[3], [f for f in PUBLISHED if "cost80d" in f],
     {"s_1305": "s_cur", "prev_1304": "prev"}),
]

# The fold scripts nest their whole prior chain via runpy, and part of that
# state survives del+gc across executions inside one interpreter, so running
# all four scripts twice in a single process exhausts the ~1 GB cgroup limit
# (observed: run 1 fully passes, run 2 dies mid-chain with SIGKILL/OOM). Each
# script therefore re-executes in its own short-lived subprocess (peak RSS
# ~150-200 MB per script); process exit releases everything unconditionally.
STATE_DIR = Path("/home/user/krwork/verify-second-state")
STATE_DIR.mkdir(parents=True, exist_ok=True)

states = {}
for run_idx in (1, 2):
    for script, files, varmap in GROUPS:
        dump = STATE_DIR / ("state-run%d-%s" % (run_idx, script))
        code = (
            "import runpy, json\n"
            "ns = runpy.run_path(%r)\n" % str(SCR / script) +
            "json.dump({k: sorted(int(x) for x in ns[v]) for k, v in %r.items()},"
            " open(%r, 'w'))\n" % (varmap, str(dump))
        )
        subprocess.run([sys.executable, "-c", code], check=True)
        for f in files:
            data = (OUT / f).read_bytes()
            assert git_blob_sha_bytes(data) == PUBLISHED[f], (run_idx, script, f)
            assert data == published_bytes[f], (run_idx, f, "bytes drifted")
        got = json.loads(dump.read_text())
        states.setdefault(run_idx, {}).update(
            {k: set(int(x) for x in vals) for k, vals in got.items()})
        # restore the published bytes so the mirror stays byte-faithful to main
        for f in files:
            (OUT / f).write_bytes(published_bytes[f])
        print(f"CONTROL rerun {run_idx} {script}: re-executed end-to-end in a "
              "fresh subprocess, every built-in control passed, its regenerated "
              "artifacts byte-identical to the published blobs")
for k in states[1]:
    assert states[1][k] == states[2][k], ("rerun state mismatch", k)

s_1290 = states[2]["s_1290"]
s_1299 = states[2]["s_1299"]
prev_1290 = states[2]["prev_1290"]     # 565 roots through cost-77c @head 1290
s_1296 = states[2]["s_1296"]
s_1302 = states[2]["s_1302"]
prev_1296 = states[2]["prev_1296"]     # 569 roots through cost-75d @head 1296
s_1304 = states[2]["s_1304"]
prev_1302 = states[2]["prev_1302"]     # 580 roots through the merged fold @head 1302
s_1305 = states[2]["s_1305"]
prev_1304 = states[2]["prev_1304"]     # 583 roots through cost-79a @head 1304
assert len(prev_1290) == 565 and len(prev_1296) == 569 and len(prev_1302) == 580
assert len(prev_1304) == 583

# ---------- 2. bit-78 duplicate-root identity (the control the fold lacks) ----
d75 = json.loads((OUT / "class-frontier-cost75d-receipts-recompute-20261115.json").read_text())
root75_92 = {r["bit"]: r["root_hex"] for r in d75["cost75d_addition"]}[92]
root_78 = ROOTS_77D[78]
assert root_78 == root75_92, "77d bit-78 root must equal the 75d bit-92 receipt root"
assert int(root_78, 16) in prev_1296, "the duplicate root is in the 1296 inventory"
assert d4_canonical(int(root_78, 16)) == d4_canonical(int(root75_92, 16))
cov78 = independent_covers(int(root_78, 16))
assert len(cov78) == 7, "7 deletion orbits (all distinct under D4)"
assert cov78 <= s_1296, "bit-78 root covers must be fully pre-solved at 1296"
assert not (cov78 - set(s_1296)), "zero marginal at the 1296 baseline"
print("CONTROL bit-78 duplicate identity: 77d bit-78 root == 75d bit-92 receipt "
      "root raw-hex; all 7 independently re-derived deletion orbits are already "
      "solved at head 1296 (zero marginal), which justifies the merged fold "
      "excluding it from the receipt list")

# ---------- 3. independent D4 disjointness of the 15 new roots ---------------
new_77d = {int(h, 16) for h in ROOTS_77D.values()}
new_79a = {int(h, 16) for h in ROOTS_79A.values()}
assert len(new_77d) == 12 and len(new_79a) == 3
assert not (new_77d & prev_1290), "77d roots disjoint from the 1290 inventory (raw)"
inv_d4_1290 = {d4_canonical(r) for r in prev_1290}
d4_77d = {d4_canonical(r) for r in new_77d}
assert not (d4_77d & inv_d4_1290), "77d roots disjoint from the 1290 inventory (D4)"
assert len(d4_77d) == 12, "12 distinct D4 orbits among the 77d roots"
inv_d4_1296 = {d4_canonical(r) for r in prev_1296}
d4_merged = {d4_canonical(int(ROOTS_77D[b], 16)) for b in
             [7, 12, 39, 58, 62, 64, 66, 94, 96, 108, 111]}
assert len(d4_merged) == 11 and not (d4_merged & inv_d4_1296), \
    "the 11 folded 77d roots disjoint from the 1296 inventory (D4)"
assert d4_canonical(int(root_78, 16)) in inv_d4_1296, \
    "the excluded bit-78 root IS in the 1296 inventory (duplicate, as claimed)"
inv_d4_1302 = {d4_canonical(r) for r in prev_1302}
d4_79a = {d4_canonical(r) for r in new_79a}
assert len(d4_79a) == 3 and not (d4_79a & inv_d4_1302), \
    "79a roots disjoint from the 1302 inventory (D4)"
assert not (new_79a & prev_1302), "79a roots disjoint from the 1302 inventory (raw)"
new_80d = {int(h, 16) for h in ROOTS_80D.values()}
assert len(new_80d) == 4 and not (new_80d & prev_1304), \
    "80d roots disjoint from the 1304 inventory (raw)"
inv_d4_1304 = {d4_canonical(r) for r in prev_1304}
d4_80d = {d4_canonical(r) for r in new_80d}
assert len(d4_80d) == 4 and not (d4_80d & inv_d4_1304), \
    "80d roots disjoint from the 1304 inventory (D4)"
# root identity: root == child | 1<<bit for all 19 roots
for bit, h in ROOTS_77D.items():
    assert int(h, 16) == int(CHILD_77D, 16) | (1 << bit)
for bit, h in ROOTS_79A.items():
    assert int(h, 16) == int(CHILD_79A, 16) | (1 << bit)
for bit, h in ROOTS_80D.items():
    assert int(h, 16) == int(CHILD_80D, 16) | (1 << bit)
# popcount 7
for h in list(ROOTS_77D.values()) + list(ROOTS_79A.values()) + list(ROOTS_80D.values()):
    assert bin(int(h, 16)).count("1") == 7
print("CONTROL independent D4: 12 77d roots distinct-orbit and disjoint from the "
      "565-root 1290 inventory (raw+D4); the 11 folded roots disjoint from the "
      "569-root 1296 inventory while bit-78 is IN it (duplicate); 3 79a roots "
      "disjoint from the 580-root 1302 inventory (raw+D4); 4 80d roots disjoint "
      "from the 583-root 1304 inventory (raw+D4); all 19 roots equal "
      "child | 1<<bit with popcount 7")

# ---------- 4. legal candidate enumerations re-derived from scratch ----------
claim77 = json.loads((OUT / "class2-lane-cost77d-inflight-20261115.json").read_text())
claim79 = json.loads((OUT / "class2-lane-cost79a-inflight-20261115.json").read_text())
claim80 = json.loads((OUT / "class2-lane-cost80d-inflight-20261115.json").read_text())
cand77 = legal_candidates(int(CHILD_77D, 16))
cand79 = legal_candidates(int(CHILD_79A, 16))
cand80 = legal_candidates(int(CHILD_80D, 16))
assert cand77 == claim77["legal_candidates"] and len(cand77) == 77
assert cand79 == claim79["legal_candidates"] and len(cand79) == 79
assert cand80 == claim80["legal_candidates"] and len(cand80) == 80
print("CONTROL independent Bareiss candidate enumeration: 77, 79 and 80 legal "
      "candidates re-derived from scratch, bit-equal to the published claims")

# ---------- 5. covers/marginal arithmetic re-derived independently -----------
merged = json.loads((OUT / "class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json").read_text())
add = {r["bit"]: r for r in merged["cost77d_addition"]}
growing = set(s_1296)
per_bit_check = []
for bit in [7, 12, 39, 58, 62, 64, 66, 94, 96, 108, 111]:
    cov = independent_covers(int(ROOTS_77D[bit], 16))
    marg = cov - growing
    marg_m_hexes = sorted(f"{k:032x}" for k in marg)
    rec = add[bit]
    assert rec["marginal"] == len(marg), (bit, rec["marginal"], len(marg))
    assert sorted(rec["marginal_manifest_hexes"] + rec["marginal_non_manifest_hexes"]) == marg_m_hexes, bit
    assert rec["marginal_in_manifest"] == len(rec["marginal_manifest_hexes"])
    # the child must be covered by every root (added-stone lift)
    assert int(CHILD_77D, 16) in cov, bit
    per_bit_check.append({"bit": bit, "marginal": len(marg),
                          "marginal_in_manifest": rec["marginal_in_manifest"]})
    growing |= marg
union_11 = set(s_1296)
for bit in [7, 12, 39, 58, 62, 64, 66, 94, 96, 108, 111]:
    union_11 |= independent_covers(int(ROOTS_77D[bit], 16))
assert union_11 == s_1302, "independent union of the 11 roots' covers == the landed 1302 state"
assert growing == s_1302
d79 = json.loads((OUT / "class-frontier-cost79a-receipts-recompute-20261115.json").read_text())
add79 = {r["bit"]: r for r in d79["cost79a_addition"]}
g79 = set(s_1302)
for bit in [9, 50, 64]:
    cov = independent_covers(int(ROOTS_79A[bit], 16))
    marg = cov - g79
    rec = add79[bit]
    assert rec["marginal"] == len(marg), (bit, "79a marginal mismatch")
    assert sorted(rec["marginal_manifest_hexes"] + rec["marginal_non_manifest_hexes"]) == \
        sorted(f"{k:032x}" for k in marg), (bit, "79a hexset mismatch")
    assert int(CHILD_79A, 16) in cov
    g79 |= marg
assert g79 == s_1304, "independent union of the 3 79a roots' covers == the landed 1304 state"
d80 = json.loads((OUT / "class-frontier-cost80d-receipts-recompute-20261115.json").read_text())
add80 = {r["bit"]: r for r in d80["cost80d_addition"]}
g80 = set(s_1304)
for bit in [48, 61, 81, 96]:
    cov = independent_covers(int(ROOTS_80D[bit], 16))
    marg = cov - g80
    rec = add80[bit]
    assert rec["marginal"] == len(marg), (bit, "80d marginal mismatch")
    assert sorted(rec["marginal_manifest_hexes"] + rec["marginal_non_manifest_hexes"]) == \
        sorted(f"{k:032x}" for k in marg), (bit, "80d hexset mismatch")
    assert int(CHILD_80D, 16) in cov
    g80 |= marg
assert g80 == s_1305, "independent union of the 4 80d roots' covers == the landed 1305 state"
print("CONTROL independent marginal arithmetic: per-bit covers/marginals of the "
      "11 merged receipts, the 3 79a receipts and the 4 80d receipts re-derived "
      "with the independent D4 group and set-equal to the published records; "
      "unions reproduce the 1302, 1304 and 1305 states exactly")

# ---------- 6. prediction-vs-actual comparison -------------------------------
pred = json.loads((OUT / "class2-lane-cost77d-fold-prediction-20261115.json").read_text())
ph = pred["predicted_head_after_fold"]
actual_head = merged["frontier_after_merged_75d_77d"]
head_match = {
    "solved_s6_in_manifest": (ph["solved_s6_in_manifest"], actual_head["solved_s6_in_manifest"]),
    "unique_remaining_s6": (ph["unique_remaining_s6"], actual_head["unique_remaining_s6"]),
    "sum_remaining_cost": (ph["sum_remaining_cost"], actual_head["sum_remaining_cost"]),
    "s6_needed_by_open_classes": (ph["s6_needed_by_open_classes"], actual_head["s6_needed_by_open_classes"]),
    "cost_needed_by_open_classes": (ph["cost_needed_by_open_classes"], actual_head["cost_needed_by_open_classes"]),
}
for k, (pv, av) in head_match.items():
    assert pv == av, (k, pv, av)
assert pred["predicted_totals"]["union_marginal"] == merged["totals"]["total_marginal"] == 51
assert pred["predicted_totals"]["union_marginal_in_manifest"] == merged["totals"]["total_marginal_in_manifest"] == 6
pr = {r["bit"]: r for r in pred["predicted_receipts"]}
per_bit_prediction = []
for bit in sorted(pr):
    a = add.get(bit)
    if a is None:
        assert pr[bit]["already_folded_root_duplicate"] is True
        assert pr[bit]["predicted_marginal"] == 0
        per_bit_prediction.append({"bit": bit, "status": "predicted zero-marginal duplicate; "
                                   "landed fold excludes the root from the receipt list"})
        continue
    assert pr[bit]["predicted_marginal"] == a["marginal"], (bit, "marginal")
    assert pr[bit]["predicted_marginal_in_manifest"] == a["marginal_in_manifest"], (bit, "mim")
    assert sorted(pr[bit]["predicted_marginal_hexes"]) == \
        sorted(a["marginal_manifest_hexes"] + a["marginal_non_manifest_hexes"]), (bit, "hexes")
    per_bit_prediction.append({"bit": bit, "predicted_marginal": pr[bit]["predicted_marginal"],
                               "actual_marginal": a["marginal"],
                               "predicted_mim": pr[bit]["predicted_marginal_in_manifest"],
                               "actual_mim": a["marginal_in_manifest"], "match": True})
ppe = pred["predicted_parent_effects"]
assert ppe["00000000000000801202000000200000"]["lost_rows"] == [] and \
    ppe["00000000000000801202000000200000"]["rows_after"] == 11
assert ppe["00000000000000003800400008000000"]["rows_after"] == 58 and \
    len(ppe["00000000000000003800400008000000"]["lost_rows"]) == 6
zero_mim_pred = pred["predicted_totals"]["zero_mim_receipts"]
zero_mim_actual = [int(s[3:]) for s in merged["totals"]["zero_marginal_in_manifest"]]
assert zero_mim_actual == [b for b in zero_mim_pred if b != 78]
print("CONTROL prediction-vs-actual: the pre-fold prediction brief matches the "
      "landed merged fold on all 5 head numbers, all 11 per-bit marginals / "
      "mim / hex-sets, the 51/6 totals, both parents' row losses (11->11 lost "
      "none, 64->58 with the same 6 rows), and the zero-mim set modulo the "
      "bookkeeping convention on bit-78 (predicted as zero-marginal receipt, "
      "landed as excluded duplicate root)")

# ---------- 7. 79a fold parent effects ---------------------------------------
assert d79["frontier_after_cost79a"]["solved_s6_in_manifest"] == 1304
assert d79["frontier_after_cost79a"]["unique_remaining_s6"] == 6543
assert d79["frontier_after_cost79a"]["sum_remaining_cost"] == 516873
assert d79["frontier_after_cost79a"]["s6_needed_by_open_classes"] == 4813
assert d79["frontier_after_cost79a"]["cost_needed_by_open_classes"] == 380596
assert d79["totals"]["receipts"] == 3 and d79["totals"]["total_marginal"] == 14
assert d79["totals"]["total_marginal_in_manifest"] == 2
assert d79["totals"]["child_closed_by_bit"] == 9
best = d79["frontier_after_cost79a"]["best_coverable_class2"]
assert best["s5_hex"] == "00000000000000801202000000200000"
assert (best["remaining_s6_orbits"], best["remaining_s7_edge_cost"]) == (10, 787)
print("CONTROL 79a fold: head 1304/6543/516873/4813/380596, 3 receipts, marginal "
      "14 / in-manifest 2, child closed by bit9, second target S5 11/866 -> "
      "10/787")

# ---------- 7b. 80d fold effects ---------------------------------------------
assert d80["frontier_after_cost80d"]["solved_s6_in_manifest"] == 1305
assert d80["frontier_after_cost80d"]["unique_remaining_s6"] == 6542
assert d80["frontier_after_cost80d"]["sum_remaining_cost"] == 516793
assert d80["frontier_after_cost80d"]["s6_needed_by_open_classes"] == 4812
assert d80["frontier_after_cost80d"]["cost_needed_by_open_classes"] == 380516
assert d80["totals"]["receipts"] == 4 and d80["totals"]["total_marginal"] == 18
assert d80["totals"]["total_marginal_in_manifest"] == 1
assert d80["totals"]["child_closed_by_bit"] == 48
best80 = d80["frontier_after_cost80d"]["best_coverable_class2"]
assert best80["s5_hex"] == "00000000000000801202000000200000"
assert (best80["remaining_s6_orbits"], best80["remaining_s7_edge_cost"]) == (9, 707)
assert d80["totals"]["zero_marginal_in_manifest"] == ["bit61", "bit81", "bit96"]
print("CONTROL 80d fold: head 1305/6542/516793/4812/380516, 4 receipts, marginal "
      "18 / in-manifest 1, child closed by bit48, second target S5 10/787 -> "
      "9/707 (now the best coverable class-2)")

# ---------- 8. write the verification record ---------------------------------
result = {
    "schema": "n11-class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115-v1",
    "date": "2026-11-15",
    "lane": "class2-lane long-term lane (second independent verification session)",
    "verified_folds": [
        "cost-77d receipts fold: head 1290/6557/517923/4827/381646 -> 1299/6548/517249/4818/380972 (12 receipts, child closed by bit7)",
        "merged cost-75d+77d warm-hygiene fold: head 1296/6551/517468/4821/381191 -> 1302/6545/517025/4815/380748 (11 receipts, bit-78 excluded as duplicate, no child closure claimed)",
        "cost-79a receipts fold: head 1302 -> 1304/6543/516873/4813/380596 (3 receipts bits 9/50/64, child closed by bit9, second target S5 11/866 -> 10/787)",
        "cost-80d receipts fold: head 1304 -> 1305/6542/516793/4812/380516 (4 receipts bits 48/61/81/96, child closed by bit48, second target S5 10/787 -> 9/707, now the best coverable class-2)",
    ],
    "method": "fresh codeload-main mirror (plus the published cost-80d artifacts fetched from main and blob-pinned before the rerun); the four published fold scripts re-executed end-to-end twice; every built-in control passed on both runs and all 12 regenerated artifacts were byte-identical to the published git blobs on both runs; additional independent controls: an 8-element D4 board-group implementation and exact-integer Bareiss determinants written for this verification (no repository engine, solver, cache or df-pn import, no floating point)",
    "inputs": "published main bytes only (codeload tarball mirror); no state from the landing sessions was reused",
    "fold_script_blobs": script_blobs,
    "outputs_byte_identical_to_main": {
        f: {"git_blob_sha": PUBLISHED[f], "bytes": len(published_bytes[f]),
            "md5": hashlib.md5(published_bytes[f]).hexdigest()}
        for f in PUBLISHED
    },
    "controls_passed": {
        "fold_scripts_rerun_end_to_end_twice": "both reruns passed every built-in control of all four scripts and regenerated all 12 artifacts byte-identically (also byte-identical between the two reruns), each script re-executed in its own short-lived subprocess (del+gc across runpy chains leaks past the ~1 GB cgroup limit, measured: run 1 in-process passes, run 2 OOMs; process exit releases everything)",
        "bit78_duplicate_root_identity": {
            "root_hex": root_78,
            "equals_75d_bit92_receipt_root_raw": True,
            "in_1296_inventory_raw": True,
            "independent_covers_all_pre_solved_at_1296": True,
            "zero_marginal_at_1296": True,
            "exclusion_from_receipt_list_justified": True,
        },
        "independent_d4_disjointness": "12 77d roots: distinct D4 orbits, disjoint from the 565-root 1290 inventory raw+D4; the 11 folded roots disjoint from the 569-root 1296 inventory raw+D4 while bit-78 is in it as the 75d bit-92 duplicate; 3 79a roots: distinct D4 orbits, disjoint from the 580-root 1302 inventory raw+D4; 4 80d roots: distinct D4 orbits, disjoint from the 583-root 1304 inventory raw+D4; all 19 roots == child | 1<<bit, popcount 7",
        "independent_candidate_enumeration": "77, 79 and 80 legal candidates re-derived from scratch with exact Bareiss determinants, bit-equal to the published claims",
        "independent_marginal_arithmetic": "per-bit covers/marginals of the 11 merged receipts, 3 79a receipts and 4 80d receipts recomputed with the independent D4 group; all hex-sets set-equal to the published records; the unions reproduce the 1302, 1304 and 1305 solved states exactly",
        "prediction_vs_actual": {
            "head_five_numbers": "all 5 predicted head numbers match the landed merged head 1302/6545/517025/4815/380748",
            "totals": "predicted union marginal 51 / in-manifest 6 == landed 51/6",
            "per_bit": per_bit_prediction,
            "parent_effects": "second target 11->11 (lost none) and parent 00000000000000003800400008000000 64->58 (same 6 lost rows) as predicted",
            "zero_mim_convention": "predicted [7, 39, 58, 64, 78, 108] vs landed [7, 39, 58, 64, 108]: the only difference is bit-78, predicted as a zero-marginal receipt and landed as an excluded duplicate root - semantically identical (zero contribution either way)",
        },
        "top_candidates_csv_identity_note": "the after-cost77d and after-merged top-candidates CSVs are byte-identical on main (git blob 49b7f37815f120829d86cd2370dbd0026dec1d63); this is genuine: both fold paths leave the same spotlight-candidate remaining-row sets (second target 11/866, class-4 18/1460, audit-blocked 10/698, second coverable 40/2778), confirmed by the byte-identical regeneration from both scripts",
    },
    "errata_recorded": [
        "merged fold script prose (published head JSON method field and section-6 print) says 'the 12 roots asserted disjoint ... then the 12 receipts folded in publication order [7, 12, 39, 58, 62, 64, 66, 78, 94, 96, 108, 111]' and set_equality_after_12 'covers(12 cost-77d roots)', while the code folds 11 receipts (bit-78 excluded) and the disjointness assert covers 11 roots; the arithmetic is unaffected because the bit-78 root's covers are fully pre-solved at the 1296 baseline (zero marginal, independently confirmed here), so the 11-root set-equality and a hypothetical 12-root version coincide; prose-only, published blobs unchanged",
        "merged fold script section-4 print says 'CONTROL 12 published certificates asserted ... 11/11 PASS' while 11 certificates are asserted; prose-only",
    ],
    "interpretation_guard": "bookkeeping verification of receipts folds only; solved 1305 measures manifest coverage, not the game-theoretic value of any position; REFUTED-D10 is not a LOSS proof; WIN7 certificates prove a win within depth 10 from the individual 7-stone roots only; the cost-80d fold (head 1304 -> 1305) landed during this session and is covered by this verification; the parallel lane may already be sweeping further children beyond head 1305; 11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 all remain UNKNOWN",
}
(OUT / "class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115.json")
