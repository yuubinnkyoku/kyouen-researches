"""n11 class2-lane pre-sweep census v12 (head 1473, 2026-11-18).

What changed since census v11 (published as
class2-lane-next-target-presweep-1473-v11-20261117.json, git blob
1e2b6a2b688db1a93098edea62b5793b54efaaba):

  * the cost-78c sweep COMPLETED with 11 WIN7-D10 bits [1, 4, 9, 30,
    49, 69, 75, 79, 100, 114, 116] / 67 REFUTED-D10 / 0 capped over
    the 78 legal bits of the census v11 rank-1 child
    00000000000000403800000008000008 (238,626,461 candidate nodes;
    raw audit git blob 8e3ee7aa; claim v5 git blob 18508321, where
    the v5 is a pin-provenance correction over v4 with no new
    computation); this is the first WIN-bearing swept row of the
    presweep-1473 band;
  * all 11 WIN7-D10 certificates are published on main (band commits
    b359756f..97650e27; 614,003 rows / 77,967,826 extraction nodes /
    22,223,603 published bytes; manifest class2-lane-cost78c-win7-
    certificates-20261117.json git blob b7fe519e), independently
    verified engine-free (root-check stones=7 + loser mobility
    match, all sub-roots PASS, consumed-union 0 missing / 0 extra),
    with fresh-process re-extraction byte-identical on bits 69 and
    116;
  * the parallel-lane batches-1-6 audit (git blob 7460b42b after the
    provenance-only 321ccf06 republication of the d8e5f9b7 version)
    agrees bit-exactly with the 9 WIN7-D10 bits it covered;
  * this v12 adds the completed 78c verdict map to the fourteen v11
    maps (fifteen maps total: 64h / 76c / 66i / 66j / 69j / 64a /
    71e / 72d / 73i / 73j / 73k / 73l / 74i / 75f / 78c), marks the
    78c row swept (receipt fold still pending behind the 66i/66j/
    69j/71e/72d/73i/73j/73k/73l folds) and re-ranks the remaining
    unswept/unclaimed/unexcluded rows at the unchanged head
    1473/174/6375/504596/4648/368510.

Method: v11 is the authoritative overlay state (rebuilt 79-source
harvest, fourteen verdict maps, exclusions). This v12 rebuilds the
full pre-64h harvest canon map from the 79 blob-pinned sources
recorded in the v1 census harvest.files list, re-derives all fifteen
verdict maps (64h / 76c / 66i / 66j / 69j / 64a / 71e / 72d / 73i /
73j / 73k / 73l / 74i / 75f / 78c), giving exact per-bit
classification. It then recomputes all 39 family rows bit-exactly,
reproducing the published v11 counts (v1 harvested hits,
fourteen-map newly-covered, open_v12 = open_v11 - newly covered by
the 78c map only). It marks the 78c row swept (11 published and
engine-free-verified WIN7-D10 certificates, receipt fold pending),
re-ranks the remaining unswept/unclaimed/unexcluded rows at the
unchanged head 1473, and selects the census v11 runner-up
00000000000000c09002000200000000 (cost 79) as the next sweep target.

Checks (all asserted in this script):

  * harvest rebuild: 79 sources, 3,548 distinct verdict canons
    (353 WIN7-D10 / 3,195 REFUTED-D10), 0 conflicts, matching the
    v1 census counts bit-exactly;
  * 69j/71e/72d/73j/73k/73l/74i/75f/78c: audit win bits == claim
    bits == manifest bits (6/6, 13/13, 11/11, 16/16, 22/25 minus
    {14,26,55}, 32/34 minus {106,110}, 0/0, 0/0, 11/11); 78c
    certificate roots all equal child|1<<bit;
  * fifteen-map canon construction: win bits are legal bits,
    refuted = legal - win (0 capped), zero internal cross-map
    conflicts;
  * rebuilt-harvest vs fifteen-map conflict scan: 0 verdict
    conflicts;
  * every fully swept child resolves to 0 open
    (64h/76c/66i/66j/69j/64a/71e/72d/73i/73j/73k/73l/74i/75f/78c);
  * the 9 non-swept v11 ranking rows all remain in the v12 top-10,
    and the v12 ranking is exactly the sorted remaining pool top-10;
  * selected target is the cheapest remaining unswept/unclaimed/
    unexcluded row (cost 79), recorded together with its runner-up.

Search-plan bookkeeping only. No engine search is run here, no
verdict is created, no row is closed by this census itself (the 78c
row is closed at audit strength by its published sweep +
certificates, with the receipt fold still pending). WIN7-D10 proves
a first-player win within depth 10 from the individual 7-stone
root only; REFUTED-D10 is not a LOSS proof; receipt folds are
manifest-coverage bookkeeping. The 11x11 empty board, the two-stone
roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain
UNKNOWN.
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
    "class2-lane-cost73j-certificates/"
    "class2-lane-cost73j-win7-certificates-20261117.json",
    "e88710b5a2d4848be77a03ae5104e46aefc1279a")
V7 = load_out("class2-lane-next-target-presweep-1472-v7-20261117.json",
              "68246f3263fe6cbb49ffafa866f73b49cf3c2ebb")
FOLD76C = load_out(
    "class-frontier-cost76c-receipts-recompute-20261117.json",
    "953beaea054989e8b1de33f48b1f2ebc13ae7e11")
AUD73K = load_out("class2-lane-cost73k-raw-sweep-audit-20261117.json",
                  "85f4f73fa061c02612f5d24320d668e12468ca4e")
CLAIM73K = load_out("class2-lane-cost73k-inflight-20261117.json",
                    "7f654548efeeab47975bdafefa6bcfab3f0ba945")
MAN73K = load_out(
    "class2-lane-cost73k-certificates/"
    "class2-lane-cost73k-win7-certificates-20261117.json",
    "0892aed07d187ae2fb3b4b90a21c7adbc1002b62")
V8 = load_out("class2-lane-next-target-presweep-1473-v8-20261117.json",
              "2542914e02db14a8426a1a16ef1c2cfcd9817375")
AUD73L = load_out("class2-lane-cost73l-raw-sweep-audit-20261117.json",
                  "f2ea204413b31405b9e0f54a6a3d76205ca749b9")
CLAIM73L = load_out("class2-lane-cost73l-inflight-20261117.json",
                    "39cf0f9b31a28ad6358f157e2433477ab0659243")
MAN73L = load_out(
    "class2-lane-cost73l-certificates/"
    "class2-lane-cost73l-win7-certificates-20261117.json",
    "6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4")
V9 = load_out("class2-lane-next-target-presweep-1473-v9-20261117.json",
              "af1d609490472b916eb6991e7864be98af60e9b9")
AUD74I = load_out("class2-lane-cost74i-raw-sweep-audit-20261117.json",
                  "e5c803ed6dbbfcf2398b75d2406089805dff5770")
CLAIM74I = load_out("class2-lane-cost74i-inflight-20261117.json",
                    "d915e1205f658d8297a444ef5fef6b7944397bf8")
V10 = load_out("class2-lane-next-target-presweep-1473-v10-20261117.json",
               "fc2509f0bfa49359a3053289a9af1244cafcd950")
AUD75F = load_out("class2-lane-cost75f-raw-sweep-audit-20261117.json",
                  "0951327a4b346af20ffc3c7065b96af82c531ce9")
CLAIM75F = load_out("class2-lane-cost75f-inflight-20261117.json",
                    "6df1e54d1fc7253a048ee4a7d8d0073d8bcf5e05")
BIGINT73L = load_out(
    "class2-lane-cost73l-certificates-bigint-independent-"
    "reverification-20261117.json",
    "547fe617abc179ff47f3607079d3ca8c1de4359b")
V11 = load_out("class2-lane-next-target-presweep-1473-v11-20261117.json",
               "1e2b6a2b688db1a93098edea62b5793b54efaaba")
AUD78C = load_out("class2-lane-cost78c-raw-sweep-audit-20261117.json",
                  "8e3ee7aa1827ae70b099d6a7c34d122f944b2fa3")
CLAIM78C = load_out("class2-lane-cost78c-inflight-20261117.json",
                    "1850832186ba9c8715624094f05d67aa4eb10f0b")
AUD78C16 = load_out(
    "class2-lane-cost78c-raw-batches-1-6-audit-20261118.json",
    "7460b42bb8846ad6e5e3249b3a78d39aa3e94ffa")
MAN78C = load_out(
    "class2-lane-cost78c-certificates/"
    "class2-lane-cost78c-win7-certificates-20261117.json",
    "b7fe519e923c6170e836f71e3f084f73219319d5")

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

# ------------------------------------------- 2. the fifteen verdict maps
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

# 73k sweep completion check (25 WIN + 48 REFUTED, 0 capped)
AUD73K_WIN = AUD73K["verdicts"]["win7_d10_bits"]
assert AUD73K["verdicts"]["capped_count"] == 0
assert sorted(AUD73K_WIN) == [0, 7, 11, 14, 15, 26, 35, 39, 41, 44, 55,
                              58, 62, 73, 76, 87, 89, 94, 95, 97, 98,
                              103, 105, 112, 117]
assert CLAIM73K["status"].startswith("claim v3: certificates complete")
ex73k = CLAIM73K.get("actual_execution") or {}
claim73k_win = ((ex73k.get("results") or {}).get("win7_d10_bits"))
assert claim73k_win is not None
assert sorted(int(bb) for bb in claim73k_win) == sorted(AUD73K_WIN)
CHILD73K = AUD73K["target"]["s6_child"]
assert CHILD73K == "00000000000000801206000000000400"
assert AUD73K["target"]["candidate_bits"] == 73
assert AUD73K["target"]["confirmation_bits"] == [14, 23, 26, 34, 53, 55,
                                                 107]
ec73k = CLAIM73K["engine_candidate_bits"]
assert sorted(ec73k["confirmation_bits"]) == \
    AUD73K["target"]["confirmation_bits"]
assert set(AUD73K_WIN) <= set(ec73k["open_bits"]) | set(ec73k["confirmation_bits"])
assert (ec73k["open_bit_count"] + ec73k["confirmation_bit_count"]
        == CLAIM73K["candidate_count"] == 73)
man73k_bits = sorted(c["bit"] for c in MAN73K["certificates"])
assert man73k_bits == sorted(set(AUD73K_WIN) - {14, 26, 55})
man73k_roots = {c["bit"]: c["root"] for c in MAN73K["certificates"]}
for bb in man73k_bits:
    root = f"{int(CHILD73K, 16) | (1 << bb):032x}"
    assert man73k_roots[bb] == root, (bb, root, man73k_roots[bb])
assert MAN73K["totals"]["rows"] == 966535
assert MAN73K["totals"]["extraction_nodes"] == 155946109
assert MAN73K["totals"]["published_bytes"] == 34933538
assert MAN73K["totals"]["fbt_drops_total"] == 0
assert MAN73K["totals"]["capped_per_move_total"] == 0
assert MAN73K["totals"]["certificates"] == 22
claim73k_pins = CLAIM73K["actual_execution"]["raw_batch_blob_pins"]
assert claim73k_pins["audit_json"] == \
    "85f4f73fa061c02612f5d24320d668e12468ca4e"
assert (AUD73K["verdicts"]["per_bit_identical_to_concurrent_record"]
        == "73/73 (loss, nodes, capped)")

# 73l sweep completion check (34 WIN + 39 REFUTED, 0 capped)
AUD73L_WIN = AUD73L["verdicts"]["win7_d10_bits"]
AUD73L_REF = AUD73L["verdicts"]["refuted_d10_bits"]
assert AUD73L["verdicts"]["capped_count"] == 0
assert sorted(AUD73L_WIN) == [1, 2, 3, 4, 6, 8, 9, 18, 21, 23, 25,
                              28, 29, 32, 34, 41, 42, 44, 47, 53,
                              54, 61, 62, 64, 66, 80, 95, 105, 106,
                              110, 112, 113, 116, 119]
assert len(AUD73L_WIN) == 34 and len(AUD73L_REF) == 39
assert not (set(AUD73L_WIN) & set(AUD73L_REF))
CHILD73L = AUD73L["target"]["s6_child"]
assert CHILD73L == "00000000000000c09002000000400000"
st73l, bits73l = legal_candidates(CHILD73L)
cands73l = sorted(bits73l)
assert len(cands73l) == AUD73L["target"]["candidate_bits"] == 73
assert set(AUD73L_WIN) | set(AUD73L_REF) == set(cands73l)
assert CLAIM73L["status"].startswith("claim v3: certificates complete")
ex73l = CLAIM73L["actual_execution"]["results"]
assert sorted(ex73l["win7_d10_bits"]) == sorted(AUD73L_WIN)
assert sorted(ex73l["refuted_d10_bits"]) == sorted(AUD73L_REF)
assert ex73l["refuted_d10_bits_count"] == 39
ec73l = CLAIM73L["engine_candidate_bits"]
assert sorted(ec73l["confirmation_bits"]) == \
    AUD73L["confirmation_bits"]["bits"] == [65, 86, 90, 94, 97, 106,
                                            110]
assert ec73l["open_bit_count"] == 66
assert ec73l["confirmation_bit_count"] == 7
assert (ec73l["open_bit_count"] + ec73l["confirmation_bit_count"]
        == CLAIM73L["candidate_count"] == 73)
pred73l = ec73l["confirmation_verdicts_predicted"]
assert [pred73l[str(b_)] for b_ in (65, 86, 90, 94, 97)] == \
    ["REFUTED-D10"] * 5
assert pred73l["106"] == "WIN7-D10" and pred73l["110"] == "WIN7-D10"
for b_, rec in AUD73L["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True and rec["raw_identical"] is False
man73l_bits = sorted(c["bit"] for c in MAN73L["certificates"])
assert man73l_bits == sorted(set(AUD73L_WIN) - {106, 110})
man73l_roots = {c["bit"]: c["root"] for c in MAN73L["certificates"]}
for bb in man73l_bits:
    root = f"{int(CHILD73L, 16) | (1 << bb):032x}"
    assert man73l_roots[bb] == root, (bb, root, man73l_roots[bb])
assert MAN73L["totals"] == {"certificates": 32, "rows": 1693203,
                            "extraction_nodes": 424657112,
                            "published_bytes": 61171191,
                            "fbt_drops_total": 0,
                            "capped_per_move_total": 0}
bs73l = BIGINT73L["summary"]
assert bs73l["records"] == 32 and bs73l["verifier_pass"] == 32
assert bs73l["verifier_fail"] == 0
assert bs73l["total_rows_independently_verified"] == 1693203
assert bs73l["total_certificate_bytes_rehashed"] == 61171191
assert bs73l["total_extraction_nodes_in_manifest"] == 424657112
assert AUD73L["v15_cross_engine_check"]["win_agreement"] == \
    "34/34 loss=true"
assert AUD73L["v15_cross_engine_check"]["capped"] == 0
assert AUD73L["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"

# 74i sweep completion check (0 WIN + 74 REFUTED, 0 capped)
AUD74I_WIN = AUD74I["verdicts"]["win7_d10_bits"]
AUD74I_REF = AUD74I["verdicts"]["refuted_d10_bits"]
assert AUD74I["verdicts"]["capped_count"] == 0
assert AUD74I_WIN == [] and len(AUD74I_REF) == 74
CHILD74I = AUD74I["target"]["s6_child"]
assert CHILD74I == "00000000020000003800000088000000"
st74i, bits74i = legal_candidates(CHILD74I)
cands74i = sorted(bits74i)
assert len(cands74i) == AUD74I["target"]["candidate_bits"] == 74
assert set(AUD74I_REF) == set(cands74i)
assert CLAIM74I["status"].startswith("claim v2: sweep COMPLETE")
ex74i = CLAIM74I["actual_execution"]["results"]
assert ex74i["win7_d10_bits"] == []
assert ex74i["refuted_d10_bits_count"] == 74
assert ex74i["capped_count"] == 0
assert ex74i["candidate_nodes_total"] == 56125895
ec74i = CLAIM74I["engine_candidate_bits"]
assert sorted(ec74i["confirmation_bits"]) == \
    AUD74I["confirmation_bits"]["bits"] == [30, 71, 72, 90, 115]
assert ec74i["open_bit_count"] == 69
assert ec74i["confirmation_bit_count"] == 5
assert (ec74i["open_bit_count"] + ec74i["confirmation_bit_count"]
        == CLAIM74I["candidate_count"] == 74)
pred74i = ec74i["confirmation_verdicts_predicted"]
assert [pred74i[str(b_)] for b_ in (30, 71, 72, 90, 115)] == \
    ["REFUTED-D10"] * 5
for b_, rec in AUD74I["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True
    assert rec["raw_identical"] == (b_ == "30"), (b_, rec)
assert AUD74I["v15_cross_engine_check"]["verdict_agreement"] == \
    "10/10 loss=false"
assert AUD74I["v15_cross_engine_check"]["capped"] == 0
assert AUD74I["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
assert CLAIM74I["receipt_fold"]["status"].startswith("not needed")
assert CLAIM74I["certificates"]["status"].startswith("not applicable")
assert CLAIM74I["s5"] == "00000000020000003800000080000000"

# 75f sweep completion check (0 WIN + 75 REFUTED, 0 capped)
AUD75F_WIN = AUD75F["verdicts"]["win7_d10_bits"]
AUD75F_REF = AUD75F["verdicts"]["refuted_d10_bits"]
assert AUD75F["verdicts"]["capped_count"] == 0
assert AUD75F_WIN == [] and len(AUD75F_REF) == 75
CHILD75F = AUD75F["target"]["s6_child"]
assert CHILD75F == "00000000020000003800020080000000"
st75f, bits75f = legal_candidates(CHILD75F)
cands75f = sorted(bits75f)
assert len(cands75f) == AUD75F["target"]["candidate_bits"] == 75
assert set(AUD75F_REF) == set(cands75f)
assert CLAIM75F["status"].startswith("claim v2: sweep COMPLETE")
ex75f = CLAIM75F["actual_execution"]["results"]
assert ex75f["win7_d10_bits"] == []
assert ex75f["refuted_d10_bits_count"] == 75
assert ex75f["capped_count"] == 0
assert ex75f["candidate_nodes_total"] == 76432898
ec75f = CLAIM75F["engine_candidate_bits"]
assert sorted(ec75f["confirmation_bits"]) == \
    AUD75F["confirmation_bits"]["bits"] == [27, 90, 93, 115]
assert ec75f["open_bit_count"] == 71
assert ec75f["confirmation_bit_count"] == 4
assert (ec75f["open_bit_count"] + ec75f["confirmation_bit_count"]
        == CLAIM75F["candidate_count"] == 75)
pred75f = ec75f["confirmation_verdicts_predicted"]
assert [pred75f[str(b_)] for b_ in (27, 90, 93, 115)] == \
    ["REFUTED-D10"] * 4
for b_, rec in AUD75F["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True
    assert rec["raw_identical"] == (b_ == "27"), (b_, rec)
assert AUD75F["v15_cross_engine_check"]["verdict_agreement"] == \
    "9/9 loss=false"
assert AUD75F["v15_cross_engine_check"]["capped"] == 0
assert AUD75F["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
assert CLAIM75F["receipt_fold"]["status"].startswith("not needed")
assert CLAIM75F["certificates"]["status"].startswith("not applicable")
assert CLAIM75F["s5"] == "00000000020000003800000080000000"

# 78c sweep completion check (11 WIN + 67 REFUTED, 0 capped)
AUD78C_WIN = AUD78C["verdicts"]["win7_d10_bits"]
AUD78C_REF = AUD78C["verdicts"]["refuted_d10_bits"]
assert AUD78C["verdicts"]["capped_count"] == 0
assert sorted(AUD78C_WIN) == [1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116]
assert len(AUD78C_REF) == 67
assert not (set(AUD78C_WIN) & set(AUD78C_REF))
CHILD78C = AUD78C["target"]["s6_child"]
assert CHILD78C == "00000000000000403800000008000008"
st78c, bits78c = legal_candidates(CHILD78C)
cands78c = sorted(bits78c)
assert len(cands78c) == AUD78C["target"]["candidate_bits"] == 78
assert AUD78C["target"]["open_bits"] == 66
assert set(AUD78C_WIN) | set(AUD78C_REF) == set(cands78c)
assert sorted(AUD78C["target"]["confirmation_bits"]) == \
    [5, 13, 14, 20, 34, 46, 97, 103, 108, 110, 115, 118]
assert CLAIM78C["status"].startswith(
    "claim v5: COMPLETED + CERTIFICATES PUBLISHED")
ex78c = CLAIM78C["actual_execution"]
assert sorted(ex78c["win7_d10_bits"]) == sorted(AUD78C_WIN)
assert len(ex78c["refuted_d10_bits"]) == 67
assert ex78c["capped_bits"] == []
assert ex78c["candidate_nodes"] == 238626461
ec78c = CLAIM78C["engine_candidate_bits"]
assert sorted(ec78c["confirmation_bits"]) == \
    AUD78C["target"]["confirmation_bits"]
assert ec78c["open_bit_count"] == 66
assert ec78c["confirmation_bit_count"] == 12
assert (ec78c["open_bit_count"] + ec78c["confirmation_bit_count"]
        == CLAIM78C["candidate_count"] == 78)
pred78c = ec78c["confirmation_verdicts_predicted"]
assert [pred78c[str(b_)] for b_ in AUD78C["target"]["confirmation_bits"]] \
    == ["REFUTED-D10"] * 12
for b_, rec in AUD78C["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True, (b_, rec)
    assert rec["raw_identical"] == (b_ in ("5", "13", "14", "20",
                                           "34", "46")), (b_, rec)
assert AUD78C["v15_cross_engine_check"]["verdict_agreement"] == \
    "17/17 (16 loss=false, 1 loss=true)"
assert AUD78C["v15_cross_engine_check"]["capped"] == 0
assert AUD78C["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
man78c_bits = sorted(c["bit"] for c in MAN78C["certificates"])
assert man78c_bits == sorted(AUD78C_WIN)
man78c_roots = {c["bit"]: c["root"] for c in MAN78C["certificates"]}
for bb in AUD78C_WIN:
    root = f"{int(CHILD78C, 16) | (1 << bb):032x}"
    assert man78c_roots[bb] == root, (bb, root, man78c_roots[bb])
assert MAN78C["totals"] == {"certificates": 11, "rows": 614003,
                            "extraction_nodes": 77967826,
                            "published_bytes": 22223603,
                            "fbt_drops_total": 0,
                            "capped_per_move_total": 0}
cert78c = CLAIM78C["certificates"]
assert cert78c["manifest"] == \
    "class2-lane-cost78c-win7-certificates-20261117.json"
assert cert78c["manifest_blob_sha"] == \
    "b7fe519e923c6170e836f71e3f084f73219319d5"
assert cert78c["totals"] == MAN78C["totals"]
assert cert78c["determinism_sample_bits"] == [69, 116]
assert CLAIM78C["receipt_fold"]["status"].startswith("pending behind")
assert AUD78C16["schema"] == \
    "n11-cost78c-raw-batches-1-6-audit-20261118-v1"
assert AUD78C16["all_pass"] is True and AUD78C16["failures"] == []
t78c16 = AUD78C16["totals"]
assert t78c16["candidate_bits"] == 54
assert t78c16["win7_d10_bits"] == [1, 4, 9, 30, 49, 69, 75, 79, 100]
assert len(t78c16["refuted_d10_bits"]) == 45
pb78c = {e["bit"]: e for e in AUD78C16["per_bit"]}
assert sorted(pb78c) == sorted(ec78c["open_bits"])[:54]
for bb, e in pb78c.items():
    exp = "WIN7-D10" if bb in set(AUD78C_WIN) else "REFUTED-D10"
    assert e["verdict"] == exp, (bb, e["verdict"], exp)
assert FOLD76C["status"] == "fold-complete"
fa = FOLD76C["frontier_after_cost76c"]
assert (fa["solved_s6_in_manifest"], fa["remaining_s5_orbits"],
        fa["unique_remaining_s6"], fa["sum_remaining_cost"],
        fa["s6_needed_by_open_classes"],
        fa["cost_needed_by_open_classes"]) == \
    (1473, 174, 6375, 504596, 4648, 368510)

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
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i folds after "
                 "the landed 76c bit61 fold; all 16 certificates "
                 "extracted, independently verified engine-free and "
                 "published on main"),
        "source": ("raw audit blob 4c13cbb2 (8 sweep + 1 confirmation "
                   "batches, v17) + claim v3 (blob 74fc3417) + "
                   "certificate manifest "
                   "class2-lane-cost73j-win7-certificates-20261117.json "
                   "(blob e88710b5)"),
    },
    "cost73k": {
        "child": CHILD73K,
        "win": AUD73K_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j folds; "
                 "all 22 new certificates extracted, independently "
                 "verified engine-free and published on main; the 3 "
                 "confirmation WIN roots (bits 14/26/55) are covered by "
                 "the published cost73j bit 110 / cost73i bit 110 / "
                 "cost69j bit 110 certificates"),
        "source": ("raw audit blob 85f4f73f (third independent "
                   "regeneration, 8 sweep + 1 confirmation batches, "
                   "v17, 73/73 per-bit identical to the concurrent "
                   "record) + claim v3 (blob 7f654548) + certificate "
                   "manifest class2-lane-cost73k-win7-certificates-"
                   "20261117.json (blob 0892aed0)"),
    },
    "cost73l": {
        "child": CHILD73L,
        "win": AUD73L_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j/73k "
                 "folds; all 32 new certificates extracted, "
                 "independently verified engine-free, BigInt "
                 "third-implementation re-verified (32/32 PASS, "
                 "reverification blob 547fe617) and published on "
                 "main; the 2 confirmation WIN roots (bits 106/110) "
                 "are covered by the published cost73j bit 118 / "
                 "cost73k bit 98 certificates"),
        "source": ("raw audit blob f2ea2044 (9 sweep batches incl. 1 "
                   "confirmation batch, v17) + claim v3 (blob "
                   "39cf0f9b) + certificate manifest class2-lane-"
                   "cost73l-win7-certificates-20261117.json (blob "
                   "6e0a94ab)"),
    },
    "cost74i": {
        "child": CHILD74I,
        "win": AUD74I_WIN,
        "fold": ("NOT NEEDED: the sweep found 0 WIN7-D10 roots (74/74 "
                 "REFUTED-D10, 0 capped), so this row produces no "
                 "receipts; fully determined at audit strength"),
        "source": ("raw audit blob e5c803ed (8 sweep + 1 confirmation "
                   "batches + 2 det reruns + 2 v15 crosscheck chunks, "
                   "v17) + claim v2 (blob d915e120)"),
    },
    "cost75f": {
        "child": CHILD75F,
        "win": AUD75F_WIN,
        "fold": ("NOT NEEDED: the sweep found 0 WIN7-D10 roots (75/75 "
                 "REFUTED-D10, 0 capped), so this row produces no "
                 "receipts; fully determined at audit strength"),
        "source": ("raw audit blob 0951327a (8 sweep + 1 confirmation "
                   "batches + 2 det reruns + 2 v15 crosscheck chunks, "
                   "v17) + claim v2 (blob 6df1e54d)"),
    },
    "cost78c": {
        "child": CHILD78C,
        "win": AUD78C_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
                 "folds; all 11 certificates extracted, independently "
                 "verified engine-free (root-check stones=7 + loser "
                 "mobility match, all sub-roots PASS, consumed-union 0 "
                 "missing / 0 extra), determinism re-extraction "
                 "byte-identical on bits 69 and 116, and published on "
                 "main"),
        "source": ("raw audit blob 8e3ee7aa (7x9 + 1x3 open + 1x12 "
                   "confirmation batches, v17, 238,626,461 candidate "
                   "nodes, plus 2 det reruns and 2 v15 crosscheck "
                   "chunks) + claim v5 (blob 18508321, a pin-provenance "
                   "correction over v4) + certificate manifest "
                   "class2-lane-cost78c-win7-certificates-20261117.json "
                   "(blob b7fe519e); the parallel batches-1-6 audit "
                   "(blob 7460b42b, provenance-only republication of "
                   "d8e5f9b7) agrees bit-exactly on its 54 bits"),
    },
}

new_verdict_maps = {}
new_canon = {}
new_canon_pre73k = {}      # twin without 73k/73l/74i/75f: re-derives v7 counts
new_canon_pre73l = {}      # twin without 73l/74i/75f: re-derives v8 counts
new_canon_pre74i = {}      # twin without 74i/75f: re-derives v9 counts
new_canon_pre75f = {}      # twin without the 75f map: re-derives v10 counts
new_canon_pre78c = {}      # twin without the 78c map: re-derives v11 counts
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
        if name not in ("cost73k", "cost73l", "cost74i", "cost75f",
                        "cost78c"):
            new_canon_pre73k[c] = (v, name, b_)
        if name not in ("cost73l", "cost74i", "cost75f", "cost78c"):
            new_canon_pre73l[c] = (v, name, b_)
        if name not in ("cost74i", "cost75f", "cost78c"):
            new_canon_pre74i[c] = (v, name, b_)
        if name not in ("cost75f", "cost78c"):
            new_canon_pre75f[c] = (v, name, b_)
        if name != "cost78c":
            new_canon_pre78c[c] = (v, name, b_)
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
print(f"fifteen maps: {len(new_canon)} distinct canons, 0 internal "
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

    Source label: map name if the canon is covered by one of the
    fifteen fresh maps (fresh re-coverage takes display precedence),
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

# ------------------------------------------ 5. families v12 (bit-exact rows)
families_v12 = {}
parent_of = {}
row_checks = []
NCAN7 = set(new_canon_pre73k)
NCAN11 = set(new_canon_pre73l)
NCAN12 = set(new_canon_pre74i)
NCAN13 = set(new_canon_pre75f)
NCAN14 = set(new_canon_pre78c)
for fam, rows in V11["families_v11"].items():
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
        n_new_v7 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN7 and c_ not in HCAN)
        n_new_v8 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN11 and c_ not in HCAN)
        n_new_v9 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN12 and c_ not in HCAN)
        n_new_v10 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN13 and c_ not in HCAN)
        n_new_v11 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN14 and c_ not in HCAN)
        n_78c = n_new - n_new_v11
        assert n_old == v1_harv, (child, n_old, v1_harv)
        assert n_new_v7 == row["newly_covered_by_ten_maps"], \
            (child, n_new_v7, row["newly_covered_by_ten_maps"])
        assert n_new_v8 == row["newly_covered_by_eleven_maps"], \
            (child, n_new_v8, row["newly_covered_by_eleven_maps"])
        assert n_new_v9 == row["newly_covered_by_twelve_maps"], \
            (child, n_new_v9, row["newly_covered_by_twelve_maps"])
        assert n_new_v10 == row["newly_covered_by_thirteen_maps"], \
            (child, n_new_v10, row["newly_covered_by_thirteen_maps"])
        assert n_new_v11 == row["newly_covered_by_fourteen_maps"], \
            (child, n_new_v11, row["newly_covered_by_fourteen_maps"])
        assert n_open == len(cands) - n_old - n_new, child
        assert n_open == row["open_after_census_v11"] - n_78c, \
            (child, n_open, row["open_after_census_v11"], n_78c)
        if "excluded" not in row:
            assert n_open <= row["open_after_census_v11"], child
        new_row = dict(row)
        new_row["open_after_census_v12"] = n_open
        new_row["known_verdict_bits_v12"] = n_old + n_new
        new_row["newly_covered_by_fifteen_maps"] = n_new
        out_rows.append(new_row)
        row_checks.append((child, n_open, n_new, n_78c))
    families_v12[fam] = out_rows

# the 73k / 73j / 76c / 64a / 73l / 74i / 75f exclusions are carried
# verbatim from the v11 census rows; mark the newly swept 78c row
for fam, rows in families_v12.items():
    for row in rows:
        if row["s6_hex"] == "00000000000000801206000000000400":
            assert "excluded" in row and "cost-73k complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v10"] == 0
        if row["s6_hex"] == "00000000000000403800000408000000":
            assert "excluded" in row and "cost-73j complete" \
                in row["excluded"], row["excluded"][:60]
        if row["s6_hex"] == "00000000010000809002000001000000":
            assert "excluded" in row and "fold LANDED" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v10"] == 0
        if row["s6_hex"] == "00000000000000c09002000000400000":
            assert "excluded" in row and "cost-73l complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000020000003800000088000000":
            assert "excluded" in row and "cost-74i complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000020000003800020080000000":
            assert "excluded" in row and "cost-75f complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000000000403800000008000008":
            assert "excluded" not in row
            assert row["newly_covered_by_fifteen_maps"] >= 66
            row["excluded"] = (
                "swept child (cost-78c complete: 11 WIN7-D10 + 67 "
                "REFUTED-D10, 0 capped; the first WIN-bearing swept row "
                "of the presweep-1473 band; all 11 certificates "
                "published on main (manifest git blob b7fe519e, band "
                "commits b359756f..97650e27) and independently verified "
                "engine-free (root-check stones=7 + loser mobility "
                "match, all sub-roots PASS, consumed-union 0 missing / "
                "0 extra); fresh-process re-extraction byte-identical "
                "on bits 69 and 116; the parallel batches-1-6 audit "
                "(blob 7460b42b) agrees bit-exactly on its 54 bits; "
                "receipt fold pending behind the 66i/66j/69j/71e/72d/"
                "73i/73j/73k/73l folds)")
            assert row["open_after_census_v12"] == 0
print("family rows recomputed bit-exactly:", len(row_checks))

# --------------------------------------------------- 6. ranking and selection
def sort_key(r):
    return (r["cost"], r["open_after_census_v12"], r["s6_hex"])


pool = [r for fam in families_v12.values() for r in fam
        if "excluded" not in r]
pool.sort(key=sort_key)
ranking = pool[:10]
assert len(ranking) == 10
v11_rank_hexes = [r["s6_hex"] for r in V11["ranking_top10"]]
swept_now = {"00000000000000403800000008000008"}
kept9 = [h for h in v11_rank_hexes if h not in swept_now]
assert len(kept9) == 9
v12_hexes = {r["s6_hex"] for r in ranking}
for h in kept9:
    assert h in v12_hexes, ("v11 ranking row fell out of v12 top10", h)

sel = ranking[0]
assert sel["cost"] == 79, sel
assert sel["s6_hex"] == "00000000000000c09002000200000000", sel
assert sel["open_after_census_v12"] <= 69, sel
st, bits = legal_candidates(sel["s6_hex"])
cands = sorted(bits)
assert len(cands) == sel["cost"]
cls = classify(sel["s6_hex"], cands)
sweep_bits = [b_ for b_ in cands if cls[b_][1] == "open"]
confirmation = [{"bit": b_, "verdict": cls[b_][1],
                 "equivalent": cls[b_][2]}
                for b_ in cands if cls[b_][1] != "open"]
assert len(sweep_bits) + len(confirmation) == sel["cost"]
assert len(sweep_bits) == sel["open_after_census_v12"]
runner_up = ranking[1]

print(f"selected: {sel['s6_hex']} cost {sel['cost']} "
      f"open {len(sweep_bits)} confirm {len(confirmation)} "
      f"parent {parent_of[sel['s6_hex']]}")
for c in confirmation:
    print(f"  confirmation bit {c['bit']}: {c['verdict']} "
          f"(= {c['equivalent']})")
print(f"runner-up: {runner_up['s6_hex']} cost {runner_up['cost']} "
      f"open {runner_up['open_after_census_v12']}")
for r in ranking:
    print(f"  rank: cost {r['cost']} open {r['open_after_census_v12']} "
          f"{r['s6_hex']} parent {parent_of[r['s6_hex']]}")

# ------------------------------------------------------------- 7. output
out = {
    "schema": "n11-class2-lane-next-target-presweep-1473-v12-20261118-v1",
    "date": "2026-11-18",
    "chain_head": "1473/174/6375/504596/4648/368510",
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
        "v7_census_json":
            "class2-lane-next-target-presweep-1472-v7-20261117.json "
            "(git blob 68246f3263fe6cbb49ffafa866f73b49cf3c2ebb)",
        "v8_census_json":
            "class2-lane-next-target-presweep-1473-v8-20261117.json "
            "(git blob 2542914e02db14a8426a1a16ef1c2cfcd9817375)",
        "v9_census_json":
            "class2-lane-next-target-presweep-1473-v9-20261117.json "
            "(git blob af1d609490472b916eb6991e7864be98af60e9b9)",
        "v10_census_json":
            "class2-lane-next-target-presweep-1473-v10-20261117.json "
            "(git blob fc2509f0bfa49359a3053289a9af1244cafcd950)",
        "v11_census_json":
            "class2-lane-next-target-presweep-1473-v11-20261117.json "
            "(git blob 1e2b6a2b688db1a93098edea62b5793b54efaaba)",
        "cost76c_fold_receipt":
            "class-frontier-cost76c-receipts-recompute-20261117.json "
            "(git blob 953beaea054989e8b1de33f48b1f2ebc13ae7e11; "
            "frontier_after [1473, 174, 6375, 504596, 4648, 368510])",
        "note": ("v1 head-1452 bit statuses + rebuilt harvest carried "
                 "over; v4 overlays 64h/76c/66i/66j; v5 adds 69j + the "
                 "64a STERILE correction; v6 adds the completed 71e / "
                 "72d / 73i verdict maps; v7 adds the completed 73j "
                 "verdict map; v8 adds the completed 73k verdict map, "
                 "the LANDED 76c bit61 fold (canonical head 1473) and "
                 "recomputes all family rows bit-exactly; v9 adds the "
                 "completed 73l verdict map (with its 32 published and "
                 "BigInt-re-verified certificates) and recomputes all "
                 "family rows bit-exactly at the unchanged head 1473; "
             "v10 adds the completed 74i verdict map (the first fully "
             "refuted sweep row: 0 WIN7-D10 / 74 REFUTED-D10 / 0 capped, "
             "audit strength only, no certificates and no receipt fold "
             "needed) and recomputes all family rows bit-exactly at the "
             "unchanged head 1473; v11 adds the completed 75f verdict "
             "map (the SECOND fully refuted sweep row: 0 WIN7-D10 / 75 "
             "REFUTED-D10 / 0 capped, audit strength only, no "
             "certificates and no receipt fold needed) and recomputes "
             "all family rows bit-exactly at the unchanged head 1473; "
             "v12 adds the completed 78c verdict map (the first "
             "WIN-bearing swept row of the presweep-1473 band: 11 "
             "WIN7-D10 with all 11 certificates published on main "
             "(manifest git blob b7fe519e) and independently verified "
             "engine-free, 67 REFUTED-D10, 0 capped; receipt fold "
             "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
             "folds) and recomputes all family rows bit-exactly at "
             "the unchanged head 1473"),
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
        "73k_win_bits_claim_audit_agreement": "25/25",
        "73k_manifest_bits_are_win_minus_transfers": "22 = 25 - {14,26,55}",
        "73k_manifest_totals": {
            "rows": 966535, "extraction_nodes": 155946109,
            "published_bytes": 34933538, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73k_confirmation_bits_match_claim": "7/7",
        "73k_audit_per_bit_identical_to_concurrent_record":
            "73/73 (loss, nodes, capped)",
        "73l_win_bits_claim_audit_agreement": "34/34",
        "73l_manifest_bits_are_win_minus_transfers":
            "32 = 34 - {106,110}",
        "73l_manifest_totals": {
            "rows": 1693203, "extraction_nodes": 424657112,
            "published_bytes": 61171191, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73l_confirmation_bits_match_claim": "7/7",
        "73l_bigint_third_implementation_reverification":
            "32/32 PASS (reverification JSON git blob 547fe617; "
            "BigInt-verified certificate population now 381)",
        "73l_v15_cross_engine_win_agreement": "34/34 loss=true",
        "74i_refuted_bits_claim_audit_agreement": "74/74",
        "74i_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "74i_confirmation_bits_match_claim": "5/5",
        "74i_confirmation_bits_refuted_d10": "5/5",
        "74i_v15_cross_engine_refuted_agreement": "10/10 loss=false",
        "74i_determinism_rerun":
            "field-identical on every non-ms field",
        "74i_receipt_fold": "not needed (0 win bits)",
        "74i_certificates": "not applicable (0 win bits)",
        "75f_refuted_bits_claim_audit_agreement": "75/75",
        "75f_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "75f_confirmation_bits_match_claim": "4/4",
        "75f_confirmation_bits_refuted_d10": "4/4",
        "75f_v15_cross_engine_refuted_agreement": "9/9 loss=false",
        "75f_determinism_rerun":
            "field-identical on every non-ms field",
        "75f_receipt_fold": "not needed (0 win bits)",
        "75f_certificates": "not applicable (0 win bits)",
        "78c_win_bits_claim_audit_manifest_agreement": "11/11",
        "78c_manifest_roots_are_child_or_bit": True,
        "78c_manifest_totals": {
            "rows": 614003, "extraction_nodes": 77967826,
            "published_bytes": 22223603, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "78c_confirmation_bits_match_claim": "12/12",
        "78c_confirmation_bits_refuted_d10": "12/12",
        "78c_confirmation_transfer_sources_reverified":
            "6 raw-identical + 6 canon-equal (fresh sweep verdicts "
            "match all twelve source verdicts)",
        "78c_v15_cross_engine_win_agreement":
            "17/17 (16 loss=false + 1 loss=true at WIN bit 116)",
        "78c_determinism":
            "fresh-process re-extraction byte-identical on bits "
            "[69, 116]; raw-batch det reruns field-identical",
        "78c_parallel_batches_1_6_audit_agreement":
            "54/54 per-bit verdicts agree (9 WIN / 45 REFUTED; git "
            "blob 7460b42b, the provenance-only 321ccf06 republication "
            "of the d8e5f9b7 version)",
        "78c_receipt_fold":
            "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
            "folds",
        "78c_certificates":
            "11/11 published (manifest git blob b7fe519e, band "
            "commits b359756f..97650e27) and engine-free verified",
        "73i_win_certificates_published_on_main_at_v9_time": False,
        "cost76c_fold_receipt_frontier_after":
            [1473, 174, 6375, 504596, 4648, 368510],
        "64a_v17_recheck_verdicts": RC64A,
        "fifteen_map_internal_conflicts": 0,
        "harvest_vs_fifteen_map_conflicts": 0,
        "harvest_vs_fifteen_map_cross_agreements": agree_old_new,
        "v1_bit_table_children_transitioned": len(bit_tables),
        "v1_bit_table_root_canon_checks": sum(
            t["cost"] for t in bit_tables.values()),
        "fully_swept_children_open_zero": 15,
        "family_rows_recomputed_bit_exactly": len(row_checks),
        "family_row_v1_harvest_count_agreement": "39/39",
        "family_row_v10_newly_covered_counts_reproduced": "39/39",
        "family_row_v11_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v10_minus_75f_only_reproduced": "39/39",
        "family_row_open_v11_minus_78c_only_reproduced": "39/39",
        "v11_ranking_kept_rows_still_in_v12_top10": "9/9",
    },
    "families_v12": families_v12,
    "ranking_top10": [
        {"s6_hex": r["s6_hex"], "parent": parent_of[r["s6_hex"]],
         "cost": r["cost"],
         "open_after_census_v12": r["open_after_census_v12"],
         "demand": r["demand"]} for r in ranking],
    "selection_policy": (
        "same policy as v4/v5/v6/v7/v8/v9/v10/v11 (cheapest cost, "
        "then fewest open bits after the fifteen-map overlay, then "
        "hex) over the three published families; rows closed by the "
        "landed 64h and 76c folds, rows pending the 66i/66j folds, "
        "and the fifteen swept children "
        "(64h/76c/66i/66j/69j/64a/71e/72d/73i/73j/73k/73l/74i/75f/"
        "78c) are excluded; the cheapest remaining row after the "
        "selected one is recorded as runner-up"),
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
                      "open_after_census_v12":
                          runner_up["open_after_census_v12"]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row "
                 "at head 1473 after the 78c sweep (the census v11 "
                 "runner-up); confirmation bits carry already-known "
                 "verdicts (pre-64h harvest or one of the fifteen "
                 "maps) and will be re-run fresh in the sweep"),
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

out_path = OUT / "class2-lane-next-target-presweep-1473-v12-20261118.json"
payload = json.dumps(out, indent=1, sort_keys=False,
                     ensure_ascii=True) + "\n"
out_path.write_bytes(payload.encode())
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
