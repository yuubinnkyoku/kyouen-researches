#!/usr/bin/env python3
"""Second independent verification of the cost-82c receipts fold
(2026-11-15, long-lane second-verification session).

The cost-82c fold (head 1305 -> 1306) was landed by the parallel lane
(research/log/2026-11-15-n11-class2-lane-cost82c-sweep-certificates-and-fold.md).
This script re-verifies it from published main bytes only, in a fresh
codeload-tarball mirror, without any state from the landing session:

1. the published fold script recompute_frontier_cost82c_receipts_20261115.py
   is executed twice in isolated short-lived subprocesses; both runs must
   produce the three outputs byte-identically and match the completed
   claim's recorded git blob shas;
2. the fold script is then re-executed once in-process via runpy to expose
   the chain namespace (s_base / manifest / prev / remF2) for the
   independent arithmetic below;
3. the sweep is re-aggregated from the eleven raw batch JSONLs with fresh
   code (82 candidates exactly once, 5 WIN7-D10 / 77 REFUTED-D10 / 0
   capped, node sum, pilots, determinism rerun, v15 anchors);
4. all 5 published certificates are re-assembled from their parts with
   fresh code (bytes / md5 / sha256 / git blob vs the extraction
   receipts, rows sorted-unique) and re-verified geometrically by the
   published third-system rational verifier (exact Fraction
   circumcentre / cross-product collinearity, iterative replay), with the
   consumed winner-row sets compared to the published TS consumed files;
5. an independently coded D4 group (explicit affine matrices, minimum
   over the 8 images) re-derives each root's D4-canonical hex, the
   deletion-orbit covers, the per-bit marginals (both in- and
   non-manifest hex sets, compared field-by-field with the published
   head JSON addition records), the exactly-once child closure, and the
   set-equality s_1306 == s_1305 UNION covers(5 roots);
6. the 592-root folded inventory (587 previous + 5 new) is re-analysed
   with the independent D4: 581 distinct orbits, 11 twin pairs (the
   5 new roots form 5 new orbits and no new twins), and the 5 new roots
   are disjoint from the previous inventory raw-hex and
   D4-canonically;
7. the completed claim fold record is matched against the recomputation.

Pure Python stdlib only. Deterministic output.
"""
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost82c-certificates"
TMP = OUT / "tmp-cost82c"
SCRIPTS = HERE / "scripts"
CHILD = "00000000200040003800000000000200"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
PARENT2 = "00000000000000003800000408000000"
WIN_BITS = [16, 37, 47, 71, 82]
ROOTS = {
    16: "00000000200040003800000000010200",
    37: "00000000200040003800002000000200",
    47: "00000000200040003800800000000200",
    71: "00000000200040803800000000000200",
    82: "00000000200440003800000000000200",
}
HEAD_JSON = "class-frontier-cost82c-receipts-recompute-20261115.json"
RANKING = "class-frontier-s5-ranking-after-cost82c-receipts-20261115.csv"
TOPCAND = "class-frontier-top-candidates-s6-after-cost82c-receipts-20261115.csv"
FOLD_SCRIPT = "recompute_frontier_cost82c_receipts_20261115.py"
RATIONAL_VERIFIER = "verify_cost75d_win7_rational_independent.py"
VERIF_JSON = OUT / "class2-lane-cost82c-fold-second-verification-20261115.json"

# blob pins of the published 82c fold script and the completed claim
PIN_FOLD_SCRIPT = ("d43fa6e5267eedca7c4bb81eedadba8a23a14424", 22562)
PIN_CLAIM = ("ac23ec77189aea9efaaf04c0197a356d864a7b76", 6396)
PIN_HEAD_JSON = ("4ee6aaab50b61e8d48e1d37afed373cd01094620", 8587)
PIN_RANKING = ("cc89c52b701076ce598c1e7b4fc71897df35eb64", 7537)
PIN_TOPCAND = ("6a1a2185d215ab587205e3da9ac5bec8833ee975", 7157)

# independent D4 group: explicit affine matrices on (x, y), 11x11 board.
# transform i: (x, y) -> (a_i*x + b_i*y + e_i, c_i*x + d_i*y + f_i)
N = 11
AFFINES = [
    (1, 0, 0, 1, 0, 0),    # identity
    (0, 1, -1, 0, 0, 10),  # rot90: (x,y)->(y,10-x)
    (-1, 0, 0, -1, 10, 10),  # rot180
    (0, -1, 1, 0, 10, 0),  # rot270: (x,y)->(10-y,x)
    (-1, 0, 0, 1, 10, 0),  # mirror x: (10-x, y)
    (1, 0, 0, -1, 0, 10),  # mirror y: (x, 10-y)
    (0, 1, 1, 0, 0, 0),    # transpose: (y, x)
    (0, -1, -1, 0, 10, 10),  # anti-transpose: (10-y, 10-x)
]


def mycanon(mask):
    """Independent D4 canonical form: min over the 8 affine images."""
    pts = [(p % N, p // N) for p in range(N * N) if (mask >> p) & 1]
    best = None
    for a, b, c, d, e, f in AFFINES:
        v = 0
        for x, y in pts:
            tx = a * x + b * y + e
            ty = c * x + d * y + f
            v |= 1 << (N * ty + tx)
        if best is None or v < best:
            best = v
    return best


def mycovers(root):
    """Deletion-orbit covers: D4-canonical forms of the 7 one-stone deletions."""
    return {mycanon(root & ~(1 << s))
            for s in range(N * N) if (root >> s) & 1}


def popcount(x):
    return bin(x).count("1")


def blob_of(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def sha256_of(data):
    return hashlib.sha256(data).hexdigest()


def md5_of(data):
    return hashlib.md5(data).hexdigest()


def jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x]


results = {"controls_passed": {}, "date": "2026-11-15",
           "schema": "n11-class2-lane-cost82c-fold-second-verification-20261115-v1"}

# ---------- 0. blob pins of the published artifacts under test ----------
for label, path, pin in (
        ("fold script", SCRIPTS / FOLD_SCRIPT, PIN_FOLD_SCRIPT),
        ("claim", OUT / "class2-lane-cost82c-inflight-20261115.json", PIN_CLAIM),
        ("head JSON", OUT / HEAD_JSON, PIN_HEAD_JSON),
        ("ranking CSV", OUT / RANKING, PIN_RANKING),
        ("top-candidates CSV", OUT / TOPCAND, PIN_TOPCAND)):
    sha, blen = blob_of(path)
    assert (sha, blen) == pin, (label, sha, blen)
print("CONTROL published artifact blob pins: fold script d43fa6e5 (22,562 B), "
      "completed claim ac23ec77 (6,396 B), head JSON 4ee6aaab (8,587 B), "
      "ranking cc89c52b (7,537 B), top-candidates 6a1a2185 (7,157 B)")

claim = json.loads((OUT / "class2-lane-cost82c-inflight-20261115.json").read_text())
assert claim["status"].startswith("completed") and claim["s6_child"] == CHILD
assert claim["s6_s7_edge_cost"] == 82 and claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}
assert claim["candidate_count"] == 82 and len(claim["legal_candidates"]) == 82

# ---------- 1. two isolated subprocess runs of the published fold script ----------
out_paths = [OUT / HEAD_JSON, OUT / RANKING, OUT / TOPCAND]
run_digests = []
for rep in range(2):
    cp = subprocess.run([sys.executable, str(SCRIPTS / FOLD_SCRIPT)],
                        capture_output=True, text=True, cwd=str(HERE))
    assert cp.returncode == 0, (rep, cp.stdout[-2000:], cp.stderr[-2000:])
    digests = [sha256_of(p.read_bytes()) for p in out_paths]
    run_digests.append(digests)
    for p, pin in zip(out_paths, [PIN_HEAD_JSON, PIN_RANKING, PIN_TOPCAND]):
        sha, blen = blob_of(p)
        assert (sha, blen) == pin, (p.name, sha, blen)
assert run_digests[0] == run_digests[1], "two fold-script runs must agree byte-identically"
print("CONTROL two isolated subprocess re-runs of the published fold script: "
      "both complete with all in-script controls, regenerate the three outputs "
      "byte-identically to each other and to the published main blobs "
      "(4ee6aaab / cc89c52b / 6a1a2185)")

# ---------- 2. in-process runpy for the chain namespace ----------
ns = runpy.run_path(str(SCRIPTS / FOLD_SCRIPT))
s_base = set(ns["s_base"])
s_cur = set(ns["s_cur"])
manifest = ns["manifest"]
prev = set(ns["prev"])
remF2 = ns["remF2"]
stF2 = ns["stF2"]
assert len(prev) == 587
assert stF2["solved_s6_in_manifest"] == 1306 and stF2["unique_remaining_s6"] == 6541
assert stF2["sum_remaining_cost"] == 516711
assert stF2["s6_needed_by_open_classes"] == 4811 and stF2["cost_needed_by_open_classes"] == 380434

# ---------- 3. independent sweep re-aggregation ----------
records = []
pilots = []
for i in range(1, 12):
    lines = jsonl(OUT / f"class2-lane-cost82c-raw-batch{i}-20261115.jsonl")
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False
    assert lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 82 and len(set(r["bit"] for r in records)) == 82
assert [r["bit"] for r in records] == claim["legal_candidates"]
win_bits = sorted(r["bit"] for r in records if r["loss"])
ref_bits = sorted(r["bit"] for r in records if not r["loss"])
assert win_bits == WIN_BITS and ref_bits == sorted(set(claim["legal_candidates"]) - set(WIN_BITS))
assert sum(1 for r in records if r["loss"]) == 5 and sum(1 for r in records if not r["loss"]) == 77
assert not any(r.get("capped") for r in records)
assert sum(r["nodes"] for r in records) == 151736232
assert all(r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17 for r in records)
assert all(r["andclose"] is True for r in records)
assert pilots == [3402] * 11
det = jsonl(OUT / "class2-lane-cost82c-v16-determinism-rerun-20261115.jsonl")
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
raw_by_bit = {r["bit"]: r for r in records}
for r in det[1:]:
    raw = raw_by_bit[r["bit"]]
    assert r["nodes"] == raw["nodes"] and r["loss"] == raw["loss"]
v15 = jsonl(OUT / "class2-lane-cost82c-v15-crosscheck-20261115.jsonl")
v15_pilot = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilot) == 1 and v15_pilot[0]["nodes"] == 5949
v15_by_bit = {r["bit"]: r for r in v15 if "bit" in r}
assert set(v15_by_bit) == set(WIN_BITS) | {0, 1, 2}
assert all(v15_by_bit[b]["loss"] is True for b in WIN_BITS)
assert all(v15_by_bit[b]["loss"] is False for b in (0, 1, 2))
win_nodes = {r["bit"]: r["nodes"] for r in records if r["loss"]}
print("CONTROL sweep re-aggregated with fresh code from 11 raw batches: 82 "
      "candidates exactly once (== claim enumeration), 5 WIN7-D10 "
      f"{WIN_BITS} / 77 REFUTED-D10 / 0 capped, 151,736,232 nodes (win sum "
      f"{sum(win_nodes.values())}), terminal ranges within [13,17], pilots "
      "3402 x11, determinism rerun node-exact, v15 cross-engine 5/5 WIN + "
      "3/3 refuted anchors (bits 0/1/2), pilot 5949")

# ---------- 4. certificates: fresh part-join + third-system geometry ----------
moves_all = json.loads((TMP / "legal-moves.json").read_text())
cert_reports = []
for bit in WIN_BITS:
    root = ROOTS[bit]
    receipt = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
    if parts:
        whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
        cert_arg = parts[0].parent / (CERTS / f"bit{bit}-root-{root}.cert").name
        # the rational verifier reads a single file: materialise the joined
        # whole once for the third-system run
        joined = Path(f"/tmp/second-verify-bit{bit}.joined.cert")
        joined.write_bytes(whole)
        cert_arg = joined
    else:
        whole = (CERTS / f"bit{bit}-root-{root}.cert").read_bytes()
        cert_arg = CERTS / f"bit{bit}-root-{root}.cert"
    assert len(whole) == receipt["bytes"] and md5_of(whole) == receipt["md5"]
    assert sha256_of(whole) == receipt["sha256"]
    blob_sha = hashlib.sha1(b"blob %d\0" % len(whole) + whole).hexdigest()
    assert blob_sha == receipt["git_blob_sha"]
    lines = whole.splitlines()
    assert lines[0] == b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
    assert lines[1] == b"root " + root.encode()
    rows = lines[2:]
    assert rows == sorted(set(rows))
    assert len(rows) == receipt["rows"]
    mobility = len(moves_all[str(bit)]["moves"])
    outc = Path(f"/tmp/second-verify-bit{bit}.consumed.txt")
    cp = subprocess.run(
        [sys.executable, str(SCRIPTS / RATIONAL_VERIFIER),
         str(cert_arg), str(mobility), str(len(rows)), str(outc)],
        capture_output=True, text=True, cwd=str(HERE))
    assert cp.returncode == 0, (bit, cp.stderr[-2000:])
    rat = json.loads(cp.stdout.strip().splitlines()[-1])
    assert rat["root_hex"] == root and rat["root_safe"] is True
    assert rat["root_loser_mobility"] == mobility and rat["subroots_passed"] == mobility
    assert rat["strategy_rows"] == len(rows) == rat["consumed_rows"]
    assert rat["union_missing"] == 0 and rat["union_extra"] == 0
    assert 13 <= min(rat["terminal_stone_range"]) and max(rat["terminal_stone_range"]) <= 17
    mine = set(outc.read_text().split())
    pub = set((TMP / f"bit{bit}.consumed.txt").read_text().split())
    assert mine == pub and len(mine) == len(rows)
    bj = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
    assert bj["root_hex"] == root and bj["strategy_rows"] == len(rows)
    assert bj["union_missing"] == 0 and bj["union_extra"] == 0
    assert bj["subroots_passed"] == mobility and bj["terminal_range"] == [13, 17]
    cert_reports.append({
        "bit": bit, "root_hex": root, "rows": len(rows), "bytes": len(whole),
        "md5": receipt["md5"], "git_blob_sha": blob_sha,
        "sub_roots": mobility,
        "third_system": {"verdict": rat["verdict"], "union_missing": 0,
                         "union_extra": 0,
                         "terminal_stone_range": rat["terminal_stone_range"],
                         "winner_state_visits": rat["winner_state_visits"],
                         "loser_states": rat["loser_states"],
                         "loser_reply_edges": rat["loser_reply_edges"],
                         "consumed_set_equals_published": True},
    })
assert sum(r["rows"] for r in cert_reports) == 289911
assert sum(r["bytes"] for r in cert_reports) == 10488172
assert sum(r["sub_roots"] for r in cert_reports) == 311
print("CONTROL 5 certificates re-joined from parts and re-verified by the "
      "third-system rational verifier (Fraction circumcentre geometry, "
      "iterative replay): 289,911 rows / 10,488,172 bytes / 311 sub-roots, "
      "roots safe, unions 0/0, terminal ranges within [13,17], consumed "
      "winner-row sets == published TS consumed sets (5/5)")

# ---------- 5. independent D4 + marginal arithmetic ----------
pub_head = json.loads((OUT / HEAD_JSON).read_text())
pub_add = {rec["bit"]: rec for rec in pub_head["cost82c_addition"]}
assert [rec["bit"] for rec in pub_head["cost82c_addition"]] == WIN_BITS
my_marginals = {}
cov5 = set()
child_closure_events = []
running = set(s_base)
for bit in WIN_BITS:
    root_v = int(ROOTS[bit], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    assert popcount(root_v) == 7 and popcount(CHILD_V) == 6
    assert (root_v & CHILD_V) == CHILD_V
    cov = mycovers(root_v)
    assert len(cov) == 7
    assert CHILD_V in cov and mycanon(CHILD_V) == CHILD_V
    marg = cov - running
    marg_m = marg & manifest
    running |= marg
    if CHILD_V in marg_m:
        child_closure_events.append(bit)
    my_marginals[bit] = (marg, marg_m)
    cov5 |= cov
    rec = pub_add[bit]
    assert rec["root_hex"] == ROOTS[bit]
    assert rec["d4_canonical_hex"] == "%032x" % mycanon(root_v), bit
    assert rec["covers"] == 7 and rec["certified"] is True
    assert rec["marginal"] == len(marg), bit
    assert rec["marginal_in_manifest"] == len(marg_m), bit
    assert rec["marginal_manifest_hexes"] == sorted("%032x" % k for k in marg_m), bit
    assert rec["marginal_non_manifest_hexes"] == sorted("%032x" % k for k in marg - marg_m), bit
    assert rec["rows"] == next(r["rows"] for r in cert_reports if r["bit"] == bit)
    assert rec["md5"] == next(r["md5"] for r in cert_reports if r["bit"] == bit)
    assert rec["sub_roots_pass"] == next(r["sub_roots"] for r in cert_reports if r["bit"] == bit)
assert child_closure_events == [16], "the child must be closed exactly once, by bit16"
assert s_cur == s_base | cov5, "set-equality: s_1306 == s_1305 UNION covers(5 roots)"
total_marg = sum(len(m) for m, _ in my_marginals.values())
total_mim = sum(len(mm) for _, mm in my_marginals.values())
zero_mim = [b for b in WIN_BITS if not my_marginals[b][1]]
assert (total_marg, total_mim) == (21, 1)
assert zero_mim == [37, 47, 71, 82]
assert len(s_cur & manifest) == 1306

# parent bookkeeping with the independent covers
rows_after = {name: {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(h, [])}
              for name, h in (("parent1", PARENT1), ("parent2", PARENT2))}
for name in ("parent1", "parent2"):
    assert CHILD not in rows_after[name]
assert (len(rows_after["parent1"]), sum(rows_after["parent1"].values())) == (8, 625)
assert (len(rows_after["parent2"]), sum(rows_after["parent2"].values())) == (59, 4854)
print("CONTROL independent D4 (explicit affine matrices) + deletion-orbit "
      "covers reproduce the published addition records field-by-field: 5 "
      "roots == child|1<<bit, popcount 7, 7 covers each, per-bit marginals "
      "21 / in-manifest 1 / zero-mim [37,47,71,82], child closed exactly "
      "once by bit16, set-equality holds, second target S5 9/707 -> 8 rows / "
      "625 and second open parent 60/4936 -> 59 rows / 4854 (only the child "
      "row lost from each)")

# ---------- 6. 592-root inventory orbit analysis with the independent D4 ----------
inventory = set(prev) | {int(ROOTS[b], 16) for b in WIN_BITS}
assert len(inventory) == 592
orbits = {}
for r in inventory:
    orbits.setdefault(mycanon(r), []).append(r)
twin_pairs = sorted(
    sorted("%032x" % v for v in members) for members in orbits.values() if len(members) > 1)
assert len(orbits) == 581, len(orbits)
assert len(twin_pairs) == 11, len(twin_pairs)
new_orbits = {mycanon(int(ROOTS[b], 16)) for b in WIN_BITS}
assert len(new_orbits) == 5
assert not (new_orbits & {mycanon(r) for r in prev})
assert not ({int(ROOTS[b], 16) for b in WIN_BITS} & prev)
print("CONTROL 592-root folded inventory re-analysed with the independent "
      "D4: 592 roots / 581 distinct orbits / 11 twin pairs (576+5 orbits, "
      "no new twins); the 5 new roots are disjoint from the 587-root "
      "inventory raw-hex and D4-canonically")

# ---------- 7. completed claim closure ----------
f = claim["fold"]
head_str = "1306/6541/516711/4811/380434"
assert f["chain_head_before"] == "1305/6542/516793/4812/380516"
assert f["chain_head_after"] == head_str
assert f["receipts_folded"] == 5 and f["publication_order"] == WIN_BITS
assert f["total_marginal"] == total_marg and f["total_marginal_in_manifest"] == total_mim
assert f["zero_marginal_in_manifest"] == zero_mim
assert f["child_orbit_closed_by_bit"] == 16
assert f["parents_after"]["parent1"] == "8 rows / 625"
assert f["parents_after"]["parent2"] == "59 rows / 4854"
assert f["parents_lost_rows"]["parent1"] == [CHILD]
assert f["parents_lost_rows"]["parent2"] == [CHILD]
obs = f["output_blob_shas"]
assert (obs["head_json"], f["head_json_bytes"]) == PIN_HEAD_JSON
assert (obs["ranking_csv"], f["ranking_csv_bytes"]) == PIN_RANKING
assert (obs["top_candidates_csv"], f["top_candidates_csv_bytes"]) == PIN_TOPCAND
print("CONTROL completed claim fold record matches this recomputation: head "
      + head_str + ", three output blobs re-asserted byte-identical")

# ---------- 8. verification JSON ----------
results["controls_passed"] = {
    "fold_script_two_isolated_runs_byte_identical":
        "two short-lived subprocess re-runs of the published fold script "
        "complete with all in-script controls and regenerate the three "
        "outputs byte-identically to each other and to main (4ee6aaab + "
        "8,587 B; cc89c52b + 7,537 B; 6a1a2185 + 7,157 B)",
    "chain_head_1305_reproduced":
        "the fold script's runpy chain reproduces the cost-80d baseline "
        "1305/6542/516793/4812/380516 with the 80d head JSON and both CSVs "
        "blob-identical to main (in-script control, re-observed twice here)",
    "sweep_reaggregated":
        "fresh-code aggregation of the 11 raw batch JSONLs: 82 candidates "
        "exactly once (== claim enumeration), 5 WIN7-D10 [16,37,47,71,82] / "
        "77 REFUTED-D10 / 0 capped, 151,736,232 nodes, terminal ranges "
        "within [13,17], pilots 3402 x11, determinism rerun node-exact, v15 "
        "cross-engine 5/5 WIN + 3/3 refuted anchors (bits 0/1/2), pilot 5949",
    "certificates_third_system_verified":
        "5 certificates re-joined from their parts with fresh code (bytes / "
        "md5 / sha256 / git blob == extraction receipts, rows "
        "sorted-unique) and geometrically re-verified by the published "
        "third-system rational verifier (exact Fraction circumcentre / "
        "cross-product collinearity, iterative replay): 289,911 rows / "
        "10,488,172 bytes / 311 sub-roots, roots safe, unions 0/0, "
        "terminal ranges within [13,17], consumed winner-row sets == "
        "published TS consumed sets (5/5)",
    "independent_d4_and_marginal_arithmetic":
        "an independently coded D4 group (8 explicit affine matrices, min "
        "image) reproduces each root's d4_canonical_hex, the deletion-orbit "
        "covers, and the per-bit marginals field-by-field against the "
        "published head JSON addition records; roots == child|1<<bit with "
        "popcount 7; total marginal 21 / in-manifest 1 / zero-mim "
        "[37,47,71,82]; child closed exactly once by bit16; set-equality "
        "s_1306 == s_1305 UNION covers(5 roots); second target S5 9/707 -> "
        "8 rows / 625 and second open parent 60/4936 -> 59 rows / 4854 "
        "(only the child row lost from each)",
    "inventory_orbit_analysis":
        "592-root folded inventory (587 previous + 5 new) re-analysed with "
        "the independent D4: 581 distinct orbits / 11 twin pairs (576 + 5 "
        "new orbits, no new twins); the 5 new roots are disjoint from the "
        "previous inventory raw-hex and D4-canonically",
    "completed_claim_closure":
        "the completed claim fold record matches this recomputation: head "
        "1305->1306, publication order [16,37,47,71,82], totals 21/1, "
        "zero-mim [37,47,71,82], child closed by bit16, parents_after "
        "8 rows / 625 and 59 rows / 4854, lost rows == the child only, "
        "three output blob shas re-asserted",
}
results["fold_script_blob_sha"] = {
    "git_blob_sha": PIN_FOLD_SCRIPT[0], "bytes": PIN_FOLD_SCRIPT[1],
    "md5": md5_of((SCRIPTS / FOLD_SCRIPT).read_bytes()),
}
results["inputs"] = (
    "published main bytes only: the codeload main tarball mirror "
    "(kyouen-researches@main), including the fold script, the completed "
    "claim, the 11 raw batches, the determinism rerun, the v15 crosscheck, "
    "the 5 published certificates and the tmp-cost82c extraction records; "
    "no state from the landing session was reused")
results["interpretation_guard"] = (
    "bookkeeping verification of a receipts fold only; solved 1306 measures "
    "manifest coverage, not the game-theoretic value of any position; "
    "REFUTED-D10 sweeps prove only the absence of a WIN7-D10 certificate; "
    "WIN7 certificates prove a first-player win within depth 10 from the "
    "individual 7-stone roots only; the standard 11x11 empty board, the "
    "two-stone roots {49,60}/{59,60}, S2 {59,60}, class1, class2 and "
    "class4 all remain UNKNOWN")
results["second_target_s5_after"] = {
    "s5_hex": PARENT1, "rows": 8, "remaining_s7_edge_cost": 625,
    "note": "best coverable class-2 target, still unresolved",
}
VERIF_JSON.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
print("written " + VERIF_JSON.name)
