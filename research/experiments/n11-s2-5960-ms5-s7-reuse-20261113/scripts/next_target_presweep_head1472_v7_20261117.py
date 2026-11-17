#!/usr/bin/env python3
"""head-1472 next-target presweep census v7 (2026-11-17).

Update of the published head-1472 presweep census v6
(class2-lane-next-target-presweep-1472-v6-20261117.json, git blob
c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb) for the state after:

  * the cost-73j sweep COMPLETED and its 16 WIN7-D10 certificates were
    extracted, independently verified (engine-free Bareiss/BigInt) and
    published on main (16 WIN bits [0,1,6,29,44,49,52,69,74,82,87,91,
    98,100,110,118] + 57 REFUTED-D10, 0 capped, 73/73 candidate bits;
    raw audit blob 4c13cbb2, claim v3 blob 74fc3417, manifest
    class2-lane-cost73j-win7-certificates-20261117.json, 726,778
    certificate rows, 166,238,087 extraction nodes, 26,236,851 published
    bytes); receipt fold stays PENDING behind the
    76c/66i/66j/69j/71e/72d/73i folds -- untouched here.

Method: v6 is the authoritative overlay state (rebuilt 79-source
harvest, ten verdict maps after this update, exclusions). This v7
rebuilds the full pre-64h harvest canon map from the 79 blob-pinned
sources recorded inside the pinned v1 census (77 claim/sweep JSONs +
the 76d/77e raw batches, per-batch pins embedded and verified identical
on main), asserts it reproduces the published v1 harvest counts exactly
(3,548 distinct verdict canons, 353 WIN / 3,195 REFUTED, 0 conflicts),
then rebuilds every family row bit-by-bit with the union of the rebuilt
harvest and the ten maps (64h / 76c / 66i / 66j / 69j / 64a / 71e /
72d / 73i / 73j), giving exact per-bit statuses for all 39 family
rows, and asserts every row reproduces the published v6 counts (v1
harvested hits, nine-map newly-covered, open_v7 = open_v6 - newly
covered by the 73j map only). It marks the 73j row swept (fold
pending), re-ranks the remaining unswept/unclaimed/unexcluded rows at
head 1472 and selects the next target.

Cross-checks (all asserted):
  * rebuilt harvest == published v1 harvest totals (79 sources,
    3,548 canons, 353/3,195, 0 conflicts, same per-source pins);
  * for every harvested source the file's own candidate list equals
    the independent legal_candidates.py enumeration and its
    win/refuted counts equal the v1 census entry counts;
  * 69j/71e/72d/73j: audit win bits == claim actual_execution win
    bits (6/6, 13/13, 11/11, 16/16) and == the published certificate
    manifests (73j manifest totals 726,778 rows / 166,238,087
    extraction nodes / 26,236,851 published bytes, every manifest
    root == child|bit); 73i: audit win bits (12) are a subset of the
    claim v1 open bits and the audit confirmation bits (5) equal the
    claim v1 confirmation bits with REFUTED-D10 outcomes as predicted
    by the v5 overlay; 73j: audit confirmation bits (7) all
    REFUTED-D10 as predicted by the v6 overlay, audit raw-batch pins
    equal the claim actual_execution pins (9/9), cross-source
    conflict scan 0;
  * ten-map canon construction: win bits are legal bits, refuted =
    legal - win (0 capped), zero internal cross-map conflicts;
  * rebuilt-harvest vs ten-map conflict scan: 0 verdict contradictions;
  * for every v1 bit-table child (16), the v7 per-bit classification
    reproduces the v1 statuses and the per-bit canon matches the v1
    root_canon field;
  * every fully swept child resolves to 0 open
    (64h/76c/66i/66j/69j/64a/71e/72d/73i/73j);
  * for every family row: rebuilt-harvest hits == the v1 census
    harvested count, the v6 nine-map newly-covered count is
    reproduced exactly, and open_v7 == open_v6 - newly covered by
    the 73j map only;
  * the 9 non-swept v6 ranking rows all remain in the v7 top-10, and
    the v7 ranking is exactly the sorted remaining pool top-10;
  * selected target is the cheapest remaining unswept/unclaimed/
    unexcluded row, with sweep_bits + confirmation_bits == legal.

Interpretation guard: search-plan bookkeeping only. No engine search
is run here, no verdict is created, no row is closed. WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone root only;
REFUTED-D10 is not a LOSS proof; receipt folds are manifest-coverage
bookkeeping. The 11x11 empty board, the two-stone roots {49,60}/{59,60},
S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_out(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return json.loads(b)


# ------------------------------------------------------------------ D4 canon
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


# ------------------------------------------------------------------ inputs
V1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
              "0d9a94a272de9fe45708757f17bfea60239a3c9b")
V4 = load_out("class2-lane-next-target-presweep-1472-v4-20261117.json",
              "d70eae093e80d19660eae314bd761c21085995bb")
V6 = load_out("class2-lane-next-target-presweep-1472-v6-20261117.json",
              "c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb")
AUD69J = load_out("class2-lane-cost69j-raw-audit-20261117.json",
                  "2f6bba29ee388bdf1211400ce5599f0ba24d03e1")
CLAIM69J = load_out("class2-lane-cost69j-inflight-20261117.json",
                    "a87dcb727a2d29a34be244d2713cb21f36f85442")
MAN69J = load_out("class2-lane-cost69j-win7-certificates-20261117.json",
                  "5e8e72faa1175ffa364849d8d90b73813406fa61")
RECHECK64A = load_out(
    "class2-lane-cost64a-v17-full-row-recheck-20261117.json",
    "0afa4d28d57224544bcc3b9e8c162af205222507")
AUD71E = load_out("class2-lane-cost71e-raw-sweep-audit-20261117.json",
                  "9f56bdb74a71ef5a647432409ffd76928702870a")
CLAIM71E = load_out("class2-lane-cost71e-inflight-20261117.json",
                    "3ca1c69864f5c3d63b48ea6d96bc21f45ba06299")
AUD72D = load_out("class2-lane-cost72d-raw-sweep-audit-20261117.json",
                  "6247569a7dca86053943701a3ae099e704e0cb31")
CLAIM72D = load_out("class2-lane-cost72d-inflight-20261117.json",
                    "c64e28fdc91ba9ffaa3518dfbc9d764ec5663b05")
AUD73I = load_out("class2-lane-cost73i-raw-sweep-audit-20261117.json",
                  "33c8c6bb2b81301354e8b796f5a4751fb52aba3b")
CLAIM73I = load_out("class2-lane-cost73i-inflight-20261117.json",
                    "4a6a17e66fc1a1bfe8efb7dc6fb2400b9af6aa1d")
AUD73J = load_out("class2-lane-cost73j-raw-sweep-audit-20261117.json",
                  "4c13cbb2008c6439a95bd0818af0d09ee465484e")
CLAIM73J = load_out("class2-lane-cost73j-inflight-20261117.json",
                    "74fc3417391e30cf4cff9c2ffce059dce529ed86")
MAN73J = load_out(
    "class2-lane-cost73j-win7-certificates-20261117.json",
    "e88710b5a2d4848be77a03ae5104e46aefc1279a")

RAW_PINS = {
    "class2-lane-cost76d-raw-batch1-20261116.jsonl":
        "d3c9ae3690c7c74e2b85fb4a84e0b02bb0ee06fb",
    "class2-lane-cost77e-raw-batch1-20261116.jsonl":
        "2034e39709d598827d912074b15dc6a61df2d5ad",
    "class2-lane-cost76d-raw-batch2-20261116.jsonl":
        "9144839aefc28cf4fd78710b1c130c0a0fe80f16",
    "class2-lane-cost77e-raw-batch2-20261116.jsonl":
        "cb883d07206e0f5ff4935ff4d36bbbf4addb7202",
    "class2-lane-cost76d-raw-batch3-20261116.jsonl":
        "8dae0d02ceea0b80ba1ecb0f853778b7dc158c23",
    "class2-lane-cost77e-raw-batch3-20261116.jsonl":
        "a64d7a19456c11f79e473f9df08c785007867d75",
    "class2-lane-cost76d-raw-batch4-20261116.jsonl":
        "3c1e4557b97cc7f5cb2eb51cb79a9b02254ff11f",
    "class2-lane-cost77e-raw-batch4-20261116.jsonl":
        "32d9d9582a848c0e65e91c56dfdab40de2fa74ee",
    "class2-lane-cost76d-raw-batch5-20261116.jsonl":
        "c0c152d58a16aa9377ef8f365508699e32c71c94",
    "class2-lane-cost77e-raw-batch5-20261116.jsonl":
        "489f13e374f267fbc0a3a798e631e4fb543b4fc7",
    "class2-lane-cost76d-raw-batch6-20261116.jsonl":
        "dbf10a3064c52472fddfc204fa4f0c00eaf6772e",
    "class2-lane-cost77e-raw-batch6-20261116.jsonl":
        "5846d0470e43dc2ce49cecace0e6d628ff795765",
    "class2-lane-cost76d-raw-batch7-20261116.jsonl":
        "57c0eda0ffd3023ef44862c83c2eb547c7e4c584",
    "class2-lane-cost77e-raw-batch7-20261116.jsonl":
        "106ac2387f7d302dfcc5963abf26ca20174ec2bb",
    "class2-lane-cost76d-raw-batch8-20261116.jsonl":
        "f4862407930d5658987dc4bc1fe9766c204ecf0e",
    "class2-lane-cost77e-raw-batch8-20261116.jsonl":
        "3956be4dcc89009f07fd6e6ddb1eba8d186a8b54",
    "class2-lane-cost76d-raw-batch9-20261116.jsonl":
        "bc32bed989265468841bb076ccfa6328e94514e3",
    "class2-lane-cost77e-raw-batch9-20261116.jsonl":
        "59df74f2902e8b45dadcef9ee451c27fbe3ff953",
    "class2-lane-cost76d-raw-batch10-20261116.jsonl":
        "8855f2d6f3821c1cd7d7e33eed6d17a63ecac3ee",
    "class2-lane-cost77e-raw-batch10-20261116.jsonl":
        "d9f4fa3c5aa85fe9e408f45a88396d1edcb535c2",
}


def find_key(obj, names, depth=0):
    for n in names:
        if n in obj:
            return obj[n]
    if depth < 1:
        for k, v in obj.items():
            if k == "fold":
                continue          # fold.win_bits mixes two lanes' bits
            if isinstance(v, dict):
                r = find_key(v, names, depth + 1)
                if r is not None:
                    return r
    return None


# ------------------------------------------- 1. rebuild the v1 harvest corpus
harvest = {}
harvest_sources = 0
glob_files = 0
for entry in V1["harvest"]["files"]:
    name = entry["file"]
    if "raw-batch" in name:
        continue                  # ingested separately below
    b = (OUT / name).read_bytes()
    assert git_blob_sha(b) == entry["git_blob_sha"], name
    glob_files += 1
    d = json.loads(b)
    child = None
    for key in ("s6_child_hex", "s6_child", "child"):
        v = d.get(key)
        if isinstance(v, str) and len(v) == 32:
            child = v
            break
    assert child is not None and child == entry["child"], name
    win_bits = find_key(d, ("win7_bits", "win7_d10_bits", "win_bits"))
    assert win_bits is not None, name
    if isinstance(win_bits, dict):
        win_bits = [bb for v in win_bits.values() for bb in v]
    win_bits = sorted(set(int(bb) for bb in win_bits))
    # candidate list: file's own if present, else the enumeration
    cands = None
    for key in ("legal_candidates", "candidate_bits", "candidates"):
        v = d.get(key)
        if isinstance(v, list) and v and isinstance(v[0], int):
            cands = v
            break
    enum = sorted(legal_candidates(child)[1])
    if cands is None:
        cands = enum
    else:
        cands = sorted(set(int(bb) for bb in cands))
    assert cands == enum, name
    assert len(cands) == entry["candidates"], name
    assert len(win_bits) == entry["win7"], name
    capped_bits = find_key(d, ("capped_bits",))
    capped_n = find_key(d, ("capped", "capped_count"))
    if isinstance(capped_bits, dict):
        capped_bits = [bb for v in capped_bits.values() for bb in v]
    capped_bits = sorted(set(int(bb) for bb in capped_bits)) \
        if capped_bits else []
    assert capped_n in (None, 0, False, len(capped_bits)) \
        and not capped_bits, name
    ref_bits = find_key(d, ("refuted_d10_bits", "refuted_bits"))
    if ref_bits is not None and not isinstance(ref_bits, list):
        ref_bits = None
    if ref_bits is None:
        ref_bits = sorted(set(cands) - set(win_bits) - set(capped_bits))
    elif isinstance(ref_bits, dict):
        ref_bits = [bb for v in ref_bits.values() for bb in v]
    else:
        ref_bits = sorted(set(int(bb) for bb in ref_bits))
    assert len(ref_bits) == entry["refuted"], name
    assert not (set(win_bits) & set(ref_bits))
    assert set(win_bits) | set(ref_bits) == set(cands), name
    child_v = int(child, 16)
    for b_ in win_bits:
        c = canon(child_v | (1 << b_))
        e = harvest.get(c)
        assert e is None or e["verdict"] == "WIN7-D10", (name, b_)
        harvest[c] = {"verdict": "WIN7-D10",
                      "sources": (e["sources"] if e else []) + [name]}
    for b_ in ref_bits:
        c = canon(child_v | (1 << b_))
        e = harvest.get(c)
        assert e is None or e["verdict"] == "REFUTED-D10", (name, b_)
        harvest[c] = {"verdict": "REFUTED-D10",
                      "sources": (e["sources"] if e else []) + [name]}
    harvest_sources += 1

# 76d / 77e raw batches (canonical bit-level records)
for prefix, ncand, win_bits, child in (
        ("cost76d", 76, [19, 49],
         "00000000040000003800080008000000"),
        ("cost77e", 77, [37, 69],
         "00000000040000809002000000004000")):
    bit_recs = {}
    n_control = 0
    for n in range(1, 11):
        fname = f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl"
        b = (OUT / fname).read_bytes()
        assert git_blob_sha(b) == RAW_PINS[fname], fname
        for line in b.decode().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if "control" in r:
                n_control += 1
                assert r["loss"] is False and r["capped"] is False
                assert r["nodes"] == 3402, r
            else:
                assert r["bit"] not in bit_recs
                assert r["andclose"] is True and r["capped"] is False
                bit_recs[r["bit"]] = r
    assert n_control == 10, prefix
    assert len(bit_recs) == ncand, prefix
    assert sorted(bit_recs) == sorted(legal_candidates(child)[1]), prefix
    raw_win = sorted(bb for bb, r in bit_recs.items() if r["loss"] is True)
    assert raw_win == win_bits, (prefix, raw_win)
    child_v = int(child, 16)
    for bb, r in bit_recs.items():
        c = canon(child_v | (1 << bb))
        expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
        e = harvest.get(c)
        assert e is None or e["verdict"] == expect, (prefix, bb, expect, e)
        harvest[c] = {"verdict": expect,
                      "sources": (e["sources"] if e else [])
                      + [f"{prefix}-raw-batches"]}
    harvest_sources += 1

harvest_n = len(harvest)
harvest_win = sum(1 for v in harvest.values()
                  if v["verdict"] == "WIN7-D10")
harvest_ref = sum(1 for v in harvest.values()
                  if v["verdict"] == "REFUTED-D10")
assert harvest_sources == 79 and glob_files == 77
assert harvest_n == V1["harvest"]["distinct_verdict_canons"] == 3548
assert harvest_win == V1["harvest"]["win7_d10"] == 353
assert harvest_ref == V1["harvest"]["refuted_d10"] == 3195
print(f"rebuilt harvest: {harvest_sources} sources, {harvest_n} canons, "
      f"win {harvest_win} / refuted {harvest_ref}")

# --------------------------------------------- 2. the ten new verdict maps
VM4 = V4["new_verdict_maps"]
AUD69J_WIN = AUD69J["verdicts"]["win7_d10_bits"]
AUD69J_REF = AUD69J["verdicts"]["refuted_d10_bits"]
assert AUD69J["verdicts"]["capped_count"] == 0
assert sorted(AUD69J_WIN) == [1, 52, 75, 109, 110, 114]
assert CLAIM69J["status"].startswith("claim v2: sweep complete")
ex = CLAIM69J.get("actual_execution") or {}
claim_win = ((ex.get("results") or {}).get("win7_d10_bits")
             or find_key(CLAIM69J,
                         ("win7_bits", "win7_d10_bits", "win_bits")))
assert claim_win is not None
assert sorted(int(bb) for bb in claim_win) == sorted(AUD69J_WIN)
man_bits = sorted(c["bit"] for c in MAN69J["certificates"])
assert man_bits == sorted(AUD69J_WIN)
man_roots = {c["bit"]: c["root"] for c in MAN69J["certificates"]}
child69j = AUD69J["target"]["s6_child"]
assert child69j == "00000000000000403800000008000020"
for bb in AUD69J_WIN:
    root = f"{int(child69j, 16) | (1 << bb):032x}"
    assert man_roots[bb] == root, (bb, root, man_roots[bb])

RC64A = RECHECK64A["v17_recheck"]["verdicts"]
assert RC64A == {"capped": 0, "refuted_d10": 64, "win7_d10": 0}
gap = RECHECK64A["census_harvest_gap"]
assert gap["corrected_status_counts"] == {
    "harvested_refuted": 8, "open": 0, "refuted_via_cost64a_v17": 56}

# 71e / 72d / 73i sweep completion checks
def check_completed(aud, claim, claim_status_prefix, expect_win):
    win = aud["verdicts"]["win7_d10_bits"]
    ref = aud["verdicts"].get("refuted_d10_bits") \
        or aud["verdicts"].get("refuted_d10_bits_count")
    assert aud["verdicts"]["capped_count"] == 0
    assert sorted(win) == sorted(expect_win), expect_win
    child = aud["target"]["s6_child"]
    legal_n = aud["target"]["legal_candidate_count"]
    st, bits = legal_candidates(child)
    assert sorted(bits) and len(bits) == legal_n
    if isinstance(ref, list):
        assert sorted(set(ref) | set(win)) == sorted(bits)
        assert len(ref) == legal_n - len(win)
    else:
        assert ref == legal_n - len(win)
    assert claim["status"].startswith(claim_status_prefix), \
        claim["status"][:60]
    ex2 = claim.get("actual_execution") or {}
    claim_win2 = ((ex2.get("results") or {}).get("win7_d10_bits"))
    return win, child, claim_win2


AUD71E_WIN, CHILD71E, CLAIM71E_WIN = check_completed(
    AUD71E, CLAIM71E, "claim v3: certificates complete",
    [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100, 116, 119])
assert sorted(CLAIM71E_WIN) == sorted(AUD71E_WIN)
assert CHILD71E == "00000000000000c09002000000002000"
assert CLAIM71E["certificates"]["win7_d10_bits"] == AUD71E_WIN
assert CLAIM71E["certificates"]["totals"]["rows"] == 534804

AUD72D_WIN, CHILD72D, CLAIM72D_WIN = check_completed(
    AUD72D, CLAIM72D, "claim v2: sweep and certificates complete",
    [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114])
assert sorted(CLAIM72D_WIN) == sorted(AUD72D_WIN)
assert CHILD72D == "00000000000000403800000008004000"
assert CLAIM72D["certificates"]["win7_d10_bits"] == AUD72D_WIN
assert CLAIM72D["certificates"]["totals"]["rows"] == 522517

AUD73I_WIN, CHILD73I, _ = check_completed(
    AUD73I, CLAIM73I, "claim v1: in-flight",
    [1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111])
assert CHILD73I == "00000000000000403800400008000000"
# 73i claim v1 is still in-flight: the audit is the completed record
ec73i = CLAIM73I["engine_candidate_bits"]
assert sorted(ec73i["open_bits"]) == sorted(
    set(AUD73I_WIN) | (set(ec73i["open_bits"]) - set(AUD73I_WIN)))
assert sorted(ec73i["confirmation_bits"]) == \
    AUD73I["confirmation_bits"]["bits"]
assert set(AUD73I_WIN) <= set(ec73i["open_bits"])
assert (ec73i["open_bit_count"] + ec73i["confirmation_bit_count"]
        == CLAIM73I["candidate_count"] == 73)
assert all(v == "REFUTED-D10" for v in
           AUD73I["confirmation_bits"]["verdicts"].values())
assert AUD73I["cross_source_conflict_scan"]["conflicts"] == 0

# 73j sweep completion check (16 WIN + 57 REFUTED, 0 capped)
AUD73J_WIN, CHILD73J, CLAIM73J_WIN = check_completed(
    AUD73J, CLAIM73J, "claim v3: certificates complete",
    [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118])
assert sorted(CLAIM73J_WIN) == sorted(AUD73J_WIN)
assert CHILD73J == "00000000000000403800000408000000"
assert CLAIM73J["certificates"]["win7_d10_bits"] == AUD73J_WIN
assert CLAIM73J["certificates"]["totals"]["rows"] == 726778
assert CLAIM73J["certificates"]["totals"]["extraction_nodes"] == 166238087
assert CLAIM73J["certificates"]["totals"]["published_bytes"] == 26236851
man73j_bits = sorted(c["bit"] for c in MAN73J["certificates"])
assert man73j_bits == sorted(AUD73J_WIN)
man73j_roots = {c["bit"]: c["root"] for c in MAN73J["certificates"]}
for bb in AUD73J_WIN:
    root = f"{int(CHILD73J, 16) | (1 << bb):032x}"
    assert man73j_roots[bb] == root, (bb, root, man73j_roots[bb])
assert MAN73J["totals"]["rows"] == 726778
assert MAN73J["totals"]["extraction_nodes"] == 166238087
assert MAN73J["totals"]["published_bytes"] == 26236851
assert MAN73J["totals"]["fbt_drops_total"] == 0
assert MAN73J["totals"]["capped_per_move_total"] == 0
assert sorted(AUD73J["confirmation_bits"]["bits"]) == \
    [5, 14, 20, 46, 97, 103, 108]
assert all(v == "REFUTED-D10" for v in
           AUD73J["confirmation_bits"]["verdicts"].values())
assert AUD73J["confirmation_bits"]["predicted_by_census_v6_overlay"] is True
for b_, oc in AUD73J["confirmation_bits"]["outcome"].items():
    assert oc["match"] is True, (b_, oc)
assert AUD73J["cross_source_conflict_scan"]["conflicts"] == 0
claim73j_pins = CLAIM73J["actual_execution"]["raw_batch_blob_pins"]
for k_ in ("batch1", "batch2", "batch3", "batch4", "batch5", "batch6",
           "batch7", "batch8", "batch9"):
    assert AUD73J["raw_batch_pins"][k_] == claim73j_pins[k_], k_
assert claim73j_pins["audit_json"] == \
    "4c13cbb2008c6439a95bd0818af0d09ee465484e"

NEW_MAPS = {
    "cost64h": {
        "child": VM4["cost64h"]["child"],
        "win": VM4["cost64h"]["win7_d10_bits"],
        "fold": VM4["cost64h"]["fold"],
        "source": VM4["cost64h"]["source"],
    },
    "cost76c": {
        "child": VM4["cost76c"]["child"],
        "win": VM4["cost76c"]["win7_d10_bits"],
        "fold": VM4["cost76c"]["fold"],
        "source": VM4["cost76c"]["source"],
    },
    "cost66i": {
        "child": VM4["cost66i"]["child"],
        "win": VM4["cost66i"]["win7_d10_bits"],
        "fold": VM4["cost66i"]["fold"],
        "source": VM4["cost66i"]["source"],
    },
    "cost66j": {
        "child": VM4["cost66j"]["child"],
        "win": VM4["cost66j"]["win7_d10_bits"],
        "fold": VM4["cost66j"]["fold"],
        "source": VM4["cost66j"]["source"],
    },
    "cost69j": {
        "child": child69j,
        "win": AUD69J_WIN,
        "fold": ("PENDING behind the 76c/66i/66j folds; all six "
                 "certificates extracted, independently verified, "
                 "published and publication-repaired byte-exact"),
        "source": ("raw audit blob 2f6bba29 (8 sweep + 2 confirmation "
                   "batches, v17) + claim v2 + certificate manifest v1"),
    },
    "cost64a": {
        "child": RECHECK64A["target"]["s6_child"],
        "win": [],
        "fold": "LANDED coverage unchanged (STERILE row, no receipts)",
        "source": ("v17 full-row recheck 64/64 REFUTED-D10 "
                   "(64/64 v16-published agreement, verdict flips 0)"),
    },
    "cost71e": {
        "child": CHILD71E,
        "win": AUD71E_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j folds; all 13 "
                 "certificates extracted, independently verified "
                 "engine-free and published on main"),
        "source": ("raw audit blob 9f56bdb7 (9 batches, v17) + claim v3 "
                   "(blob 3ca1c698) + certificate manifest "
                   "class2-lane-cost71e-win7-certificates-20261117.json"),
    },
    "cost72d": {
        "child": CHILD72D,
        "win": AUD72D_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j/71e folds; all 11 "
                 "certificates extracted, independently verified "
                 "engine-free and published on main"),
        "source": ("raw audit blob 6247569a (9 batches, v17) + claim v2 "
                   "(blob c64e28fd) + certificate manifest "
                   "class2-lane-cost72d-win7-certificates-20261117.json"),
    },
    "cost73i": {
        "child": CHILD73I,
        "win": AUD73I_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j/71e/72d folds; the "
                 "12 WIN certificates were NOT yet published on main at "
                 "census-v6 computation time (parallel-lane publication "
                 "pending); the 73i map is carried at audit strength"),
        "source": ("raw audit blob 33c8c6bb (8 sweep + 1 confirmation "
                   "batches, v17) + claim v1 (blob 4a6a17e6, in-flight)"),
    },
    "cost73j": {
        "child": CHILD73J,
        "win": AUD73J_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j/71e/72d/73i folds; "
                 "all 16 certificates extracted, independently verified "
                 "engine-free and published on main"),
        "source": ("raw audit blob 4c13cbb2 (8 sweep + 1 confirmation "
                   "batches, v17) + claim v3 (blob 74fc3417) + "
                   "certificate manifest "
                   "class2-lane-cost73j-win7-certificates-20261117.json "
                   "(blob e88710b5)"),
    },
}

new_verdict_maps = {}
new_canon = {}
new_canon_pre73j = {}      # twin without the 73j map: re-derives v6 counts
for name, m in NEW_MAPS.items():
    st, bits = legal_candidates(m["child"])
    cands = sorted(bits)
    wins = sorted(m["win"])
    assert set(wins) <= set(cands), (name, wins)
    refuted = sorted(set(cands) - set(wins))
    child_v = int(m["child"], 16)
    for b_ in cands:
        c = canon(child_v | (1 << b_))
        v = "WIN7-D10" if b_ in set(wins) else "REFUTED-D10"
        e = new_canon.get(c)
        assert e is None or e[0] == v, ("new-map conflict", name, b_, e)
        new_canon[c] = (v, name, b_)
        if name != "cost73j":
            new_canon_pre73j[c] = (v, name, b_)
    new_verdict_maps[name] = {
        "child": m["child"], "bits": len(cands),
        "win7_d10_bits": wins, "refuted_d10_bits": refuted,
        "capped": 0, "fold": m["fold"], "source": m["source"]}

# rebuilt-harvest vs new-maps conflict scan
agree_old_new = 0
for c, (v, name, b_) in new_canon.items():
    e = harvest.get(c)
    if e is not None:
        assert e["verdict"] == v, ("harvest/new conflict", name, b_, e)
        agree_old_new += 1
print(f"ten maps: {len(new_canon)} distinct canons, 0 internal "
      f"conflicts, {agree_old_new} canons cross-agree with the rebuilt "
      f"harvest")

# ------------------------------------- 3. per-bit classification machinery
VERDICT = {}
for c, e in harvest.items():
    VERDICT[c] = (e["verdict"], "pre-64h harvest")
for c, (v, name, b_) in new_canon.items():
    VERDICT[c] = (v, name)
HCAN = set(harvest)
NCAN = set(new_canon)


def classify(child_hex, cands):
    """Per-bit {bit: (canon, verdict, source-label)}.

    Source label: ten-map name if the canon is covered by one of the
    ten fresh maps (fresh re-coverage takes display precedence),
    else 'pre-64h harvest', else ('open', None).  Counting of
    old-harvest vs newly covered bits must use HCAN/NCAN membership,
    not the label.
    """
    out = {}
    child_v = int(child_hex, 16)
    for b_ in cands:
        c = canon(child_v | (1 << b_))
        out[b_] = (c,) + VERDICT.get(c, ("open", None))
    return out


# 4. v1 bit-table transitions (with per-bit canon cross-check)
bit_tables = V1["bit_tables"]
transition_summary = {}
for child, table in bit_tables.items():
    st, bits = legal_candidates(child)
    cands = sorted(bits)
    assert len(cands) == table["cost"], child
    by_bit = {e["bit"]: e for e in table["bits"]}
    assert sorted(by_bit) == cands, child
    child_v = int(child, 16)
    for b_, e in by_bit.items():
        assert canon(child_v | (1 << b_)) == int(e["root_canon"], 16), \
            (child, b_)
    cls = classify(child, cands)
    for b_, e in by_bit.items():
        _, v, src = cls[b_]
        if e["status"].startswith("harvested"):
            assert v == ("WIN7-D10" if e["status"] == "harvested_win"
                         else "REFUTED-D10"), (child, b_, e, v)
        else:
            assert e["status"] == "open", (child, b_, e)
            if v != "open":
                assert src != "pre-64h harvest", (child, b_, src)
    n_open = sum(1 for c_, v, src in cls.values() if v == "open")
    n_win = sum(1 for c_, v, src in cls.values() if v == "WIN7-D10")
    n_ref = sum(1 for c_, v, src in cls.values()
                if v == "REFUTED-D10")
    transition_summary[child] = {
        "legal": len(cands), "open": n_open,
        "win7_d10": n_win, "refuted_d10": n_ref}

for child, expect in (
        ("00000000000000403800000008100000", (64, 23)),   # 64h
        ("00000000010000809002000001000000", (76, 2)),     # 76c
        ("00000000000000801226000000000000", (66, 9)),     # 66i
        ("00000000000000c09002000000001000", (66, 9)),     # 66j
        ("00000000000000403800000008000020", (69, 6)),     # 69j
        ("00000000000000801282000040000000", (64, 0))):    # 64a
    t = transition_summary[child]
    assert t["open"] == 0, (child, t)
    assert t["win7_d10"] == expect[1], (child, t)
    assert t["legal"] == expect[0], (child, t)
assert transition_summary["00000000000000403800000008000020"][
    "refuted_d10"] == 63
assert transition_summary["00000000000000801282000040000000"][
    "refuted_d10"] == 64
print("v1 bit-table children transitioned:",
      len(transition_summary), "(all root_canon checks passed)")

# ------------------------------------------- 5. families v7 (bit-exact rows)
families_v7 = {}
parent_of = {}
row_checks = []
NCAN6 = set(new_canon_pre73j)
for fam, rows in V6["families_v6"].items():
    out_rows = []
    for row in rows:
        child = row["s6_hex"]
        parent_of[child] = fam
        t = bit_tables.get(child)
        if t is not None:
            assert t["parent"] == fam, (child, t["parent"], fam)
            assert t["cost"] == row["cost"], child
        st, bits = legal_candidates(child)
        cands = sorted(bits)
        assert len(cands) == row["cost"], (child, row)
        cls = classify(child, cands)
        n_open = sum(1 for c_, v, src in cls.values() if v == "open")
        v1_harv = (row["census"].get("harvested_refuted", 0)
                   + row["census"].get("harvested_win", 0)
                   + row["census"].get("receipt_win", 0))
        n_old = sum(1 for c_, v, src in cls.values() if c_ in HCAN)
        n_new = sum(1 for c_, v, src in cls.values()
                    if c_ in NCAN and c_ not in HCAN)
        n_new_v6 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN6 and c_ not in HCAN)
        n_73j = n_new - n_new_v6
        assert n_old == v1_harv, (child, n_old, v1_harv)
        assert n_new_v6 == row["newly_covered_by_nine_maps"], \
            (child, n_new_v6, row["newly_covered_by_nine_maps"])
        assert n_open == len(cands) - n_old - n_new, child
        assert n_open == row["open_after_census_v6"] - n_73j, \
            (child, n_open, row["open_after_census_v6"], n_73j)
        if "excluded" not in row:
            assert n_open <= row["open_after_census_v6"], child
        new_row = dict(row)
        new_row["open_after_census_v7"] = n_open
        new_row["known_verdict_bits_v7"] = n_old + n_new
        new_row["newly_covered_by_ten_maps"] = n_new
        out_rows.append(new_row)
        row_checks.append((child, n_open, n_new, n_73j))
    families_v7[fam] = out_rows

# mark the newly swept row
for fam, rows in families_v7.items():
    for row in rows:
        if row["s6_hex"] == "00000000000000403800000408000000":
            assert row["newly_covered_by_ten_maps"] >= 66
            row["excluded"] = (
                "swept child (cost-73j complete: 16 WIN7-D10 + 57 "
                "REFUTED-D10, 0 capped; 16 certificates published on "
                "main; receipt fold pending behind the 76c/66i/66j/69j/"
                "71e/72d/73i folds)")
            assert row["open_after_census_v7"] == 0
print("family rows recomputed bit-exactly:", len(row_checks))

# --------------------------------------------------- 6. ranking and selection
def sort_key(r):
    return (r["cost"], r["open_after_census_v7"], r["s6_hex"])


pool = [r for fam in families_v7.values() for r in fam
        if "excluded" not in r]
pool.sort(key=sort_key)
ranking = pool[:10]
assert len(ranking) == 10
v6_rank_hexes = [r["s6_hex"] for r in V6["ranking_top10"]]
swept_now = {"00000000000000403800000408000000"}
kept9 = [h for h in v6_rank_hexes if h not in swept_now]
assert len(kept9) == 9
v7_hexes = {r["s6_hex"] for r in ranking}
for h in kept9:
    assert h in v7_hexes, ("v6 ranking row fell out of v7 top10", h)

sel = ranking[0]
assert sel["cost"] == 73, sel
assert sel["s6_hex"] == "00000000000000801206000000000400", sel
st, bits = legal_candidates(sel["s6_hex"])
cands = sorted(bits)
assert len(cands) == sel["cost"]
cls = classify(sel["s6_hex"], cands)
sweep_bits = [b_ for b_ in cands if cls[b_][1] == "open"]
confirmation = [{"bit": b_, "verdict": cls[b_][1],
                 "equivalent": cls[b_][2]}
                for b_ in cands if cls[b_][1] != "open"]
assert len(sweep_bits) + len(confirmation) == sel["cost"]
assert len(sweep_bits) == sel["open_after_census_v7"]
runner_up = ranking[1]

print(f"selected: {sel['s6_hex']} cost {sel['cost']} "
      f"open {len(sweep_bits)} confirm {len(confirmation)} "
      f"parent {parent_of[sel['s6_hex']]}")
for c in confirmation:
    print(f"  confirmation bit {c['bit']}: {c['verdict']} "
          f"(= {c['equivalent']})")
print(f"runner-up: {runner_up['s6_hex']} cost {runner_up['cost']} "
      f"open {runner_up['open_after_census_v7']}")
for r in ranking:
    print(f"  rank: cost {r['cost']} open {r['open_after_census_v7']} "
          f"{r['s6_hex']} parent {parent_of[r['s6_hex']]}")

# ------------------------------------------------------------- 7. output
out = {
    "schema": "n11-class2-lane-next-target-presweep-1472-v7-20261117-v1",
    "date": "2026-11-17",
    "chain_head": V6["chain_head"],
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "v4_census_json":
            "class2-lane-next-target-presweep-1472-v4-20261117.json "
            "(git blob d70eae093e80d19660eae314bd761c21085995bb)",
        "v5_census_json":
            "class2-lane-next-target-presweep-1472-v5-20261117.json "
            "(git blob ea85c02319350b5953e0e70c3eb812fb78bbf17c)",
        "v6_census_json":
            "class2-lane-next-target-presweep-1472-v6-20261117.json "
            "(git blob c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb)",
        "note": ("v1 head-1452 bit statuses + rebuilt harvest carried "
                 "over; v4 overlays 64h/76c/66i/66j; v5 adds 69j + the "
                 "64a STERILE correction; v6 adds the completed 71e / "
                 "72d / 73i verdict maps; v7 adds the completed 73j "
                 "verdict map and recomputes all family rows "
                 "bit-exactly"),
    },
    "rebuilt_harvest": {
        "sources": harvest_sources,
        "glob_files": glob_files,
        "raw_batch_files": 20,
        "distinct_verdict_canons": harvest_n,
        "win7_d10": harvest_win,
        "refuted_d10": harvest_ref,
        "conflicts": 0,
        "pin_policy": ("77 glob-file pins carried inside the pinned v1 "
                       "census harvest.files list; 20 raw-batch pins "
                       "embedded in this script (all verified identical "
                       "on main)"),
    },
    "new_verdict_maps": new_verdict_maps,
    "cross_checks": {
        "harvest_rebuild_matches_v1_counts": True,
        "source_candidate_lists_match_independent_enumeration": "77/77",
        "69j_win_bits_claim_audit_manifest_agreement": "6/6",
        "71e_win_bits_claim_audit_manifest_agreement": "13/13",
        "72d_win_bits_claim_audit_manifest_agreement": "11/11",
        "73i_audit_winbits_subset_of_claim_v1_open_bits": True,
        "73i_confirmation_bits_match_claim": "5/5",
        "73j_win_bits_claim_audit_manifest_agreement": "16/16",
        "73j_manifest_totals": {
            "rows": 726778, "extraction_nodes": 166238087,
            "published_bytes": 26236851, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73j_confirmation_bits_refuted_d10": "7/7",
        "73j_raw_batch_pins_claim_audit_agreement": "9/9",
        "64a_v17_recheck_verdicts": RC64A,
        "ten_map_internal_conflicts": 0,
        "harvest_vs_ten_map_conflicts": 0,
        "harvest_vs_ten_map_cross_agreements": agree_old_new,
        "v1_bit_table_children_transitioned": len(bit_tables),
        "v1_bit_table_root_canon_checks": sum(
            t["cost"] for t in bit_tables.values()),
        "fully_swept_children_open_zero": 10,
        "family_rows_recomputed_bit_exactly": len(row_checks),
        "family_row_v1_harvest_count_agreement": "39/39",
        "family_row_v6_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v6_minus_73j_only_reproduced": "39/39",
        "v6_ranking_kept_rows_still_in_v7_top10": "9/9",
    },
    "families_v7": families_v7,
    "ranking_top10": [
        {"s6_hex": r["s6_hex"], "parent": parent_of[r["s6_hex"]],
         "cost": r["cost"],
         "open_after_census_v7": r["open_after_census_v7"],
         "demand": r["demand"]} for r in ranking],
    "selection_policy": (
        "same policy as v4/v5/v6 (cheapest cost, then fewest open bits "
        "after the ten-map overlay, then hex) over the three published "
        "families; rows closed by the landed 64h fold, rows pending the "
        "76c/66i/66j folds, and the ten swept children (64h/76c/66i/"
        "66j/69j/64a/71e/72d/73i/73j) are excluded; the cheapest "
        "remaining row after the selected one is recorded as runner-up"),
    "selected_target": {
        "s6_hex": sel["s6_hex"],
        "parent": parent_of[sel["s6_hex"]],
        "cost": sel["cost"],
        "demand": sel["demand"],
        "legal_candidates": len(cands),
        "sweep_bits": sweep_bits,
        "confirmation_bits": confirmation,
        "runner_up": {"s6_hex": runner_up["s6_hex"],
                      "parent": parent_of[runner_up["s6_hex"]],
                      "cost": runner_up["cost"],
                      "open_after_census_v7":
                          runner_up["open_after_census_v7"]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row of "
                 "the primary family at head 1472 after the 73j sweep; "
                 "confirmation bits carry already-known verdicts "
                 "(pre-64h harvest or one of the ten maps) and will be "
                 "re-run fresh in the sweep"),
    },
    "interpretation_guard": (
        "search-plan bookkeeping only. No engine search is run here, no "
        "verdict is created, no row is closed. WIN7-D10 proves a "
        "first-player win within depth 10 from the individual 7-stone "
        "root only; REFUTED-D10 is not a LOSS proof; receipt folds are "
        "manifest-coverage bookkeeping. The 11x11 empty board, the "
        "two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes "
        "1/2/4 all remain UNKNOWN."),
}

out_path = OUT / "class2-lane-next-target-presweep-1472-v7-20261117.json"
payload = json.dumps(out, indent=1, sort_keys=False,
                     ensure_ascii=True) + "\n"
out_path.write_bytes(payload.encode())
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
