#!/usr/bin/env python3
"""head-1472 next-target presweep census v5 (2026-11-17).

Update of the published head-1472 presweep census v4
(class2-lane-next-target-presweep-1472-v4-20261117.json, git blob
d70eae093e80d19660eae314bd761c21085995bb) for the state after:

  * the cost-69j sweep COMPLETED (69 legal bits fresh v17 depth-10,
    8 sweep + 2 confirmation batches, 0 capped): 6 WIN7-D10 bits
    [1, 52, 75, 109, 110, 114] + 63 REFUTED-D10, raw audit blob
    2f6bba29...; all six WIN7 certificates were extracted, independently
    verified and published, and the publication repair (11/11 files,
    commits 4bfa43ed..7e13045f) restored byte-exact certificate bytes on
    main; the 69j receipt fold stays PENDING behind the 76c/66i/66j
    folds -- untouched here;
  * the cost-64a STERILE correction (class2-lane-cost64a-v17-full-row-
    recheck-20261117.json, blob 0afa4d28...): the v4 ranking runner-up
    (cost-64 row 00000000000000801282000040000000, reported open 55)
    was a census harvest gap -- the row is fully swept STERILE
    (64/64 REFUTED-D10, v17-confirmed, verdict flips 0). v5 marks the
    row swept/STERILE and removes it from the ranking;
  * the 64h/76c/66i/66j maps, the landed-64h closure and the pending
    76c/66i/66j exclusions are carried over from v4 unchanged.

Method: v4 is the authoritative overlay state (families_v4, verdict
maps, exclusions). This v5 additionally rebuilds the full pre-64h
harvest canon map from the 79 blob-pinned sources recorded inside the
pinned v1 census (77 claim/sweep JSONs + the 76d/77e raw batches,
per-batch pins embedded below and verified identical on main), asserts
it reproduces the published v1 harvest counts exactly (3,548 distinct
verdict canons, 353 WIN / 3,195 REFUTED, 0 conflicts), then rebuilds
every family row bit-by-bit with the union of the rebuilt harvest and
the six new maps (64h / 76c / 66i / 66j / 69j / 64a), giving exact
per-bit statuses for all 39 family rows (v4 could only aggregate rows
without a v1 bit table). It marks the 69j row swept (fold pending) and
the 64a row swept STERILE, re-ranks the remaining unswept/unclaimed/
unexcluded rows at head 1472 and selects the next target.

Cross-checks (all asserted):
  * rebuilt harvest == published v1 harvest totals (79 sources,
    3,548 canons, 353/3,195, 0 conflicts, same per-source pins);
  * for every harvested source the file's own candidate list equals
    the independent legal_candidates.py enumeration and its
    win/refuted counts equal the v1 census entry counts;
  * 69j WIN bits == claim v2 == raw audit == certificate manifest (6/6,
    root == child|1<<bit);
  * 64a: 64 legal bits, 64/64 REFUTED-D10, 0 WIN, 0 capped (v17
    recheck), v1 bit-table transition open->refuted for the 56 v1-open
    bits;
  * six-map canon construction: win bits are legal bits, refuted =
    legal - win (0 capped), zero internal cross-map conflicts;
  * rebuilt-harvest vs six-map conflict scan: 0 verdict contradictions;
  * for every v1 bit-table child (16), the v5 per-bit classification
    reproduces the v1 statuses (harvested bits keep their verdict via
    the rebuilt harvest, v1-open bits are only resolved by the new
    maps) and the per-bit canon matches the v1 root_canon field;
  * every fully swept child resolves to 0 open (64h/76c/66i/66j/69j/64a);
  * for every family row: rebuilt-harvest hits == the v1 census
    harvested count, and open_v5 == legal - v1 harvested - newly
    covered by the six maps;
  * the 8 v4 ranking rows that are not the two newly swept rows all
    remain in the v5 top-10, and the v5 ranking is exactly the sorted
    remaining pool top-10;
  * selected target is the cheapest remaining unswept/unclaimed/
    unexcluded row, with sweep_bits + confirmation_bits == legal.

Interpretation guard: search-plan bookkeeping only. No engine search is
run here, no verdict is created, no row is closed. WIN7-D10 proves a
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
AUD69J = load_out("class2-lane-cost69j-raw-audit-20261117.json",
                  "2f6bba29ee388bdf1211400ce5599f0ba24d03e1")
CLAIM69J = load_out("class2-lane-cost69j-inflight-20261117.json",
                    "a87dcb727a2d29a34be244d2713cb21f36f85442")
MAN69J = load_out("class2-lane-cost69j-win7-certificates-20261117.json",
                  "5e8e72faa1175ffa364849d8d90b73813406fa61")
RECHECK64A = load_out(
    "class2-lane-cost64a-v17-full-row-recheck-20261117.json",
    "0afa4d28d57224544bcc3b9e8c162af205222507")

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

# ------------------------------------------------- 2. the six new verdict maps
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
}

new_verdict_maps = {}
new_canon = {}
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
print(f"six maps: {len(new_canon)} distinct canons, 0 internal conflicts, "
      f"{agree_old_new} canons cross-agree with the rebuilt harvest")

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

    Source label: six-map name if the canon is covered by one of the
    six fresh maps (fresh re-coverage takes display precedence),
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
self_map_of = {m["child"]: name for name, m in NEW_MAPS.items()}
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
            # verdict must agree; the source may be the pre-64h harvest
            # or any six-map canon-equivalent re-coverage (cross-row
            # equivalence is legitimate and conflict-scan-checked)
            assert v == ("WIN7-D10" if e["status"] == "harvested_win"
                         else "REFUTED-D10"), (child, b_, e, v)
        else:
            assert e["status"] == "open", (child, b_, e)
            if v != "open":
                # a v1-open bit must not be resolved by the pre-64h
                # harvest (that would contradict the v1 census)
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

# ------------------------------------------- 5. families v5 (bit-exact rows)
families_v5 = {}
parent_of = {}
row_checks = []
for fam, rows in V4["families_v4"].items():
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
        assert n_old == v1_harv, (child, n_old, v1_harv)
        assert n_open == len(cands) - n_old - n_new, child
        expected_open = row["census"]["open"] - n_new
        assert n_open == expected_open, (child, n_open, expected_open)
        new_row = dict(row)
        new_row["open_after_census_v5"] = n_open
        new_row["known_verdict_bits_v5"] = n_old + n_new
        new_row["newly_covered_by_six_maps"] = n_new
        out_rows.append(new_row)
        row_checks.append((child, n_open, n_new))
    families_v5[fam] = out_rows

# mark the two newly swept rows
for fam, rows in families_v5.items():
    for row in rows:
        if row["s6_hex"] == "00000000000000403800000008000020":
            assert row["newly_covered_by_six_maps"] == 62
            row["excluded"] = ("swept child (cost-69j complete: 6 WIN7-D10 "
                               "+ 63 REFUTED-D10, 0 capped; receipt fold "
                               "pending behind the 76c/66i/66j folds)")
            row["open_after_census_v5"] = 0
        if row["s6_hex"] == "00000000000000801282000040000000":
            assert row["newly_covered_by_six_maps"] == 56
            row["excluded"] = ("swept child (cost-64a STERILE: v17 full-row "
                               "recheck 64/64 REFUTED-D10, verdict flips 0; "
                               "v4 ranking false-open corrected)")
            row["open_after_census_v5"] = 0
print("family rows recomputed bit-exactly:", len(row_checks))

# --------------------------------------------------- 6. ranking and selection
def sort_key(r):
    return (r["cost"], r["open_after_census_v5"], r["s6_hex"])


pool = [r for fam in families_v5.values() for r in fam
        if "excluded" not in r]
pool.sort(key=sort_key)
ranking = pool[:10]
assert len(ranking) == 10
v4_rank_hexes = [r["s6_hex"] for r in V4["ranking_top10"]]
removed = {"00000000000000801282000040000000",
           "00000000000000403800000008000020"}
kept8 = [h for h in v4_rank_hexes if h not in removed]
assert len(kept8) == 8
v5_hexes = {r["s6_hex"] for r in ranking}
for h in kept8:
    assert h in v5_hexes, ("v4 ranking row fell out of v5 top10", h)

sel = ranking[0]
assert sel["s6_hex"] == "00000000000000c09002000000002000", sel["s6_hex"]
st, bits = legal_candidates(sel["s6_hex"])
cands = sorted(bits)
assert len(cands) == sel["cost"] == 71
cls = classify(sel["s6_hex"], cands)
sweep_bits = [b_ for b_ in cands if cls[b_][1] == "open"]
confirmation = [{"bit": b_, "verdict": cls[b_][1],
                 "equivalent": cls[b_][2]}
                for b_ in cands if cls[b_][1] != "open"]
assert len(sweep_bits) + len(confirmation) == 71
assert len(sweep_bits) == sel["open_after_census_v5"]
runner_up = ranking[1]

print(f"selected: {sel['s6_hex']} cost {sel['cost']} "
      f"open {len(sweep_bits)} confirm {len(confirmation)} "
      f"parent {parent_of[sel['s6_hex']]}")
for c in confirmation:
    print(f"  confirmation bit {c['bit']}: {c['verdict']} "
          f"(= {c['equivalent']})")
print(f"runner-up: {runner_up['s6_hex']} cost {runner_up['cost']} "
      f"open {runner_up['open_after_census_v5']}")
for r in ranking:
    print(f"  rank: cost {r['cost']} open {r['open_after_census_v5']} "
          f"{r['s6_hex']} parent {parent_of[r['s6_hex']]}")

# ------------------------------------------------------------- 7. output
out = {
    "schema": "n11-class2-lane-next-target-presweep-1472-v5-20261117-v1",
    "date": "2026-11-17",
    "chain_head": V4["chain_head"],
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "v3_census_json": V4["baseline"]["v3_census_json"],
        "v4_census_json":
            "class2-lane-next-target-presweep-1472-v4-20261117.json "
            "(git blob d70eae093e80d19660eae314bd761c21085995bb)",
        "note": ("v1 head-1452 bit statuses + rebuilt harvest carried "
                 "over; v4 overlays 64h/76c/66i/66j; v5 adds the 69j "
                 "verdict map and the 64a STERILE correction and "
                 "recomputes all family rows bit-exactly"),
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
        "69j_manifest_root_is_child_or_bit": "6/6",
        "64a_v17_recheck_verdicts": RC64A,
        "six_map_internal_conflicts": 0,
        "harvest_vs_six_map_conflicts": 0,
        "harvest_vs_six_map_cross_agreements": agree_old_new,
        "v1_bit_table_children_transitioned": len(bit_tables),
        "v1_bit_table_root_canon_checks": sum(
            t["cost"] for t in bit_tables.values()),
        "fully_swept_children_open_zero": 6,
        "family_rows_recomputed_bit_exactly": len(row_checks),
        "family_row_v1_harvest_count_agreement": "39/39",
        "v4_ranking_kept_rows_still_in_v5_top10": "8/8",
    },
    "families_v5": families_v5,
    "ranking_top10": [
        {"s6_hex": r["s6_hex"], "parent": parent_of[r["s6_hex"]],
         "cost": r["cost"],
         "open_after_census_v5": r["open_after_census_v5"],
         "demand": r["demand"]} for r in ranking],
    "selection_policy": (
        "same policy as v4 (cheapest cost, then fewest open bits after "
        "the six-map overlay, then hex) over the three published "
        "families; rows closed by the landed 64h fold, rows pending the "
        "76c/66i/66j folds, and the six swept children (64h/76c/66i/66j/"
        "69j/64a) are excluded; the cheapest remaining row after the "
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
                      "open_after_census_v5":
                          runner_up["open_after_census_v5"]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row of "
                 "the primary family at head 1472 after the 69j sweep "
                 "and the 64a correction; confirmation bits carry "
                 "already-known verdicts (pre-64h harvest or one of the "
                 "six maps) and will be re-run fresh in the sweep"),
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

out_path = OUT / "class2-lane-next-target-presweep-1472-v5-20261117.json"
payload = json.dumps(out, indent=1, sort_keys=False,
                     ensure_ascii=True) + "\n"
out_path.write_bytes(payload.encode())
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
