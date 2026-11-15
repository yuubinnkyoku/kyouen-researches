#!/usr/bin/env python3
"""Second independent verification of the cost-83c receipts fold
(2026-11-15, long-lane second-verification session).

The cost-83c fold (head 1312 -> 1313) was landed by the parallel lane
(commit e255a9cc). Unlike the cost-83b lane, it published NO tmp-cost83c/
checkpoint at all: only the fold script, the two WIN7 certificates, the
eleven raw batches, the v15/v16 crosschecks, the completed claim and the
three fold outputs are on main. This session first fetches those 83c
artifacts from the main raw CDN into the mirror (git-blob-sha verified),
then repairs the gap with research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83c_20261115.py (regenerating
the 9 files the fold script reads - legal-moves.json from scratch via
exact-integer Bareiss, receipts / BigInt / TS-Bareiss / consumed from the
published verifiers), then re-verifies the whole fold from published main
bytes only, without any state from the landing session:

0. the published fold script, completed claim, head JSON and both CSVs are
   pinned to their main git blob shas;
1. the reconstruction script is executed as a subprocess (it re-derives
   every missing tmp file and re-asserts md5/rows/mobility/union against
   the published head JSON records);
2. the published fold script recompute_frontier_cost83c_receipts_20261115.py
   is executed twice in isolated short-lived subprocesses; both runs must
   produce the three outputs byte-identically and match the completed
   claim's recorded git blob shas;
3. the fold script is then re-executed once in-process via runpy to expose
   the chain namespace (s_base / manifest / prev / remF2 / parents) for the
   independent arithmetic below;
4. the sweep is re-aggregated from the eleven raw batch JSONLs with fresh
   code (83 candidates exactly once, 2 WIN7-D10 / 81 REFUTED-D10 / 0
   capped, node sum, pilots, determinism rerun, v15 anchors);
5. both published certificates are re-read with fresh code (bytes / md5 /
   sha256 / git blob vs the head JSON records, rows sorted-unique) and
   re-verified geometrically by the published third-system rational
   verifier (exact Fraction circumcentre / cross-product collinearity,
   iterative replay), with the consumed winner-row sets compared to the
   reconstructed TS consumed files;
6. an independently coded D4 group (explicit affine matrices, minimum
   over the 8 images) re-derives each root's D4-canonical hex, the
   deletion-orbit covers, the per-bit marginals (both in- and
   non-manifest hex sets, compared field-by-field with the published
   head JSON addition records), the exactly-once child closure, and the
   set-equality s_1313 == s_1312 UNION covers(2 roots);
7. the 603-root folded inventory (601 previous + 2 new) is re-analysed
   with the independent D4: 592 distinct orbits, 11 twin pairs (the 2
   new roots form 2 new orbits and no new twins), and the 2 new roots
   are disjoint from the previous inventory raw-hex and D4-canonically;
8. the completed claim fold record is matched against the recomputation.

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
CERTS = OUT / "class2-lane-cost83c-certificates"
TMP = OUT / "tmp-cost83c"
SCRIPTS = HERE / "scripts"
CHILD = "00000000200000003800000000400200"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
PARENT2 = "00000000000000801202000000000100"
WIN_BITS = [16, 82]
ROOTS = {
    16: "00000000200000003800000000410200",
    82: "00000000200400003800000000400200",
}
HEAD_JSON = "class-frontier-cost83c-receipts-recompute-20261115.json"
RANKING = "class-frontier-s5-ranking-after-cost83c-receipts-20261115.csv"
TOPCAND = "class-frontier-top-candidates-s6-after-cost83c-receipts-20261115.csv"
FOLD_SCRIPT = "recompute_frontier_cost83c_receipts_20261115.py"
RECONSTRUCT_SCRIPT = "reconstruct_tmp_cost83c_20261115.py"
RATIONAL_VERIFIER = "verify_cost75d_win7_rational_independent.py"
VERIF_JSON = OUT / "class2-lane-cost83c-fold-second-verification-20261115.json"

# blob pins of the published 83c fold script and the completed claim
PIN_FOLD_SCRIPT = ("9d25d201d86d92eddecc5de71128c9060e6a1bb4", 22389)
PIN_CLAIM = ("6fdd0e63614d1632a792eef98b0ede40b4c8b66e", 6385)
PIN_HEAD_JSON = ("fc7832edce1f736ea5f15b2632d79d709fa004f4", 6811)
PIN_RANKING = ("08f0d715d5675b3ec11b0482030bad3faee0e876", 7537)
PIN_TOPCAND = ("6a40509db4bba256d509e3aa3677f5aa285f4397", 6899)

# independent D4 group: explicit affine matrices on (x, y), 11x11 board.
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

XR = [i % N for i in range(N * N)]
YR = [i // N for i in range(N * N)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(N * N)]


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


def det4rows(a, b, c, d):
    """Exact-integer Bareiss 4x4 determinant of [x^2+y^2, x, y, 1]."""
    mm = [[QR[a], XR[a], YR[a], 1], [QR[b], XR[b], YR[b], 1],
          [QR[c], XR[c], YR[c], 1], [QR[d], XR[d], YR[d], 1]]
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


def mask_over(cells):
    F = 0
    n = len(cells)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = cells[i], cells[j], cells[k]
                for d in range(N * N):
                    if det4rows(a, b, c, d) == 0:
                        F |= 1 << d
    return F


def legal_moves_of(root_hex):
    v = int(root_hex, 16)
    stones = [i for i in range(N * N) if (v >> i) & 1]
    assert len(stones) == 7
    F = mask_over(stones)
    return [p for p in range(N * N) if not (v >> p) & 1 and not (F >> p) & 1]


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
           "schema": "n11-class2-lane-cost83c-fold-second-verification-20261115-v1"}

# ---------- 0. blob pins of the published artifacts under test ----------
for label, path, pin in (
        ("fold script", SCRIPTS / FOLD_SCRIPT, PIN_FOLD_SCRIPT),
        ("claim", OUT / "class2-lane-cost83c-inflight-20261115.json", PIN_CLAIM),
        ("head JSON", OUT / HEAD_JSON, PIN_HEAD_JSON),
        ("ranking CSV", OUT / RANKING, PIN_RANKING),
        ("top-candidates CSV", OUT / TOPCAND, PIN_TOPCAND)):
    sha, blen = blob_of(path)
    assert (sha, blen) == pin, (label, sha, blen)
print("CONTROL published artifact blob pins: fold script 9d25d201 (22,389 B), "
      "completed claim 6fdd0e63 (6,385 B), head JSON fc7832ed (6,811 B), "
      "ranking 08f0d715 (7,537 B), top-candidates 6a40509d (6,899 B)")

claim = json.loads((OUT / "class2-lane-cost83c-inflight-20261115.json").read_text())
assert claim["status"].startswith("completed") and claim["s6_child"] == CHILD
assert claim["s6_s7_edge_cost"] == 83 and claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}
assert claim["candidate_count"] == 83 and len(claim["legal_candidates"]) == 83

# ---------- 1. reconstruction step (subprocess, published verifiers) ----------
cp = subprocess.run([sys.executable, str(SCRIPTS / RECONSTRUCT_SCRIPT)],
                    capture_output=True, text=True, cwd=str(HERE))
assert cp.returncode == 0, ("reconstruction failed", cp.stdout[-2000:], cp.stderr[-2000:])
assert "reconstruction complete" in cp.stdout
for bit in WIN_BITS:
    for suffix in ("cert-receipt.json", "bigint.json", "tsverify.json", "consumed.txt"):
        assert (TMP / f"bit{bit}.{suffix}").exists(), (bit, suffix)
print("CONTROL tmp reconstruction executed as a subprocess: the 9 missing "
      "tmp-cost83c files regenerated from main artifacts (legal-moves.json "
      "from scratch by exact-integer Bareiss 4x4, receipts / BigInt / "
      "TS-Bareiss / consumed by the published verifiers), every step "
      "cross-asserted against the published head JSON records")

# ---------- 2. two isolated subprocess runs of the published fold script ----------
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
      "both complete with all in-script controls (including the runpy "
      "reproduction of the 83b chain head 1312 with its blob-identical "
      "outputs), regenerate the three outputs byte-identically to each other "
      "and to the published main blobs "
      "(fc7832ed / 08f0d715 / 6a40509d)")

# ---------- 3. in-process runpy for the chain namespace ----------
ns = runpy.run_path(str(SCRIPTS / FOLD_SCRIPT))
s_base = set(ns["s_base"])
s_cur = set(ns["s_cur"])
manifest = ns["manifest"]
prev = set(ns["prev"])
remF2 = ns["remF2"]
stF2 = ns["stF2"]
parents = ns["parents"]
assert len(prev) == 601
assert len(s_base & manifest) == 1312 and len(s_cur & manifest) == 1313
assert stF2["solved_s6_in_manifest"] == 1313 and stF2["unique_remaining_s6"] == 6534
assert stF2["sum_remaining_cost"] == 516144
assert stF2["s6_needed_by_open_classes"] == 4804 and stF2["cost_needed_by_open_classes"] == 379867
assert (len(parents["parent1"]), sum(parents["parent1"].values())) == (6, 459)
assert (len(parents["parent2"]), sum(parents["parent2"].values())) == (65, 5330)
assert CHILD in parents["parent1"] and CHILD in parents["parent2"]

# ---------- 4. independent sweep re-aggregation ----------
records = []
pilots = []
for i in range(1, 12):
    lines = jsonl(OUT / f"class2-lane-cost83c-raw-batch{i}-20261115.jsonl")
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False
    assert lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 83 and len(set(r["bit"] for r in records)) == 83
assert [r["bit"] for r in records] == claim["legal_candidates"]
win_bits = sorted(r["bit"] for r in records if r["loss"])
ref_bits = sorted(r["bit"] for r in records if not r["loss"])
assert win_bits == WIN_BITS and ref_bits == sorted(set(claim["legal_candidates"]) - set(WIN_BITS))
assert sum(1 for r in records if r["loss"]) == 2 and sum(1 for r in records if not r["loss"]) == 81
assert not any(r.get("capped") for r in records)
assert sum(r["nodes"] for r in records) == 132219127
win_node_sum = sum(r["nodes"] for r in records if r["loss"])
assert win_node_sum == 2357798
assert all(r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17 for r in records)
assert all(r["andclose"] is True for r in records)
assert pilots == [3402] * 11
det = jsonl(OUT / "class2-lane-cost83c-v16-determinism-rerun-20261115.jsonl")
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
raw_by_bit = {r["bit"]: r for r in records}
for r in det[1:]:
    raw = raw_by_bit[r["bit"]]
    assert r["nodes"] == raw["nodes"] and r["loss"] == raw["loss"]
v15 = jsonl(OUT / "class2-lane-cost83c-v15-crosscheck-20261115.jsonl")
v15_pilot = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilot) == 1 and v15_pilot[0]["nodes"] == 5949
v15_by_bit = {r["bit"]: r for r in v15 if "bit" in r}
assert set(v15_by_bit) == set(WIN_BITS) | {0, 1, 2}
assert all(v15_by_bit[b]["loss"] is True for b in WIN_BITS)
assert all(v15_by_bit[b]["loss"] is False for b in (0, 1, 2))
print("CONTROL sweep re-aggregated with fresh code from 11 raw batches: 83 "
      "candidates exactly once (== claim enumeration), 2 WIN7-D10 "
      f"{WIN_BITS} / 81 REFUTED-D10 / 0 capped, 132,219,127 nodes (win sum "
      f"{win_node_sum}), terminal ranges within [13,17], pilots "
      "3402 x11, determinism rerun node-exact (8 bits), v15 cross-engine "
      "2/2 WIN + 3/3 refuted anchors (bits 0/1/2), pilot 5949")

# ---------- 5. certificates: fresh part-join + third-system geometry ----------
moves_all = json.loads((TMP / "legal-moves.json").read_text())
cert_reports = []
for bit in WIN_BITS:
    root = ROOTS[bit]
    moves = legal_moves_of(root)
    assert moves == moves_all[str(bit)]["moves"], bit
    receipt = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
    if parts:
        whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
        joined = Path(f"/tmp/second-verify-83c-bit{bit}.joined.cert")
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
    pub_rec = {r["bit"]: r for r in json.loads(
        (OUT / HEAD_JSON).read_text())["cost83c_addition"]}[bit]
    assert len(rows) == pub_rec["rows"] and md5_of(whole) == pub_rec["md5"], bit
    mobility = len(moves)
    assert mobility == pub_rec["sub_roots_pass"]
    outc = Path(f"/tmp/second-verify-83c-bit{bit}.consumed.txt")
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
                         "consumed_set_equals_reconstructed_ts": True},
    })
assert sum(r["rows"] for r in cert_reports) == 90144
assert sum(r["bytes"] for r in cert_reports) == 3257864
assert sum(r["sub_roots"] for r in cert_reports) == 121
print("CONTROL 2 certificates re-read from published whole files and "
      "re-verified by the third-system rational verifier (Fraction "
      "circumcentre geometry, iterative replay): 90,144 rows / "
      "3,257,864 bytes / 121 sub-roots, roots safe, unions 0/0, terminal "
      "ranges within [13,17], consumed winner-row sets == the "
      "reconstructed TS consumed sets (2/2)")

# ---------- 6. independent D4 + marginal arithmetic ----------
pub_head = json.loads((OUT / HEAD_JSON).read_text())
pub_add = {rec["bit"]: rec for rec in pub_head["cost83c_addition"]}
assert [rec["bit"] for rec in pub_head["cost83c_addition"]] == WIN_BITS
my_marginals = {}
cov2 = set()
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
    cov2 |= cov
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
assert s_cur == s_base | cov2, "set-equality: s_1313 == s_1312 UNION covers(2 roots)"
total_marg = sum(len(m) for m, _ in my_marginals.values())
total_mim = sum(len(mm) for _, mm in my_marginals.values())
zero_mim = [b for b in WIN_BITS if not my_marginals[b][1]]
assert (total_marg, total_mim) == (9, 1)
assert zero_mim == [82]
assert len(s_cur & manifest) == 1313

# parent bookkeeping with the independent covers
rows_after = {name: {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(h, [])}
              for name, h in (("parent1", PARENT1), ("parent2", PARENT2))}
for name in ("parent1", "parent2"):
    assert CHILD not in rows_after[name]
assert (len(rows_after["parent1"]), sum(rows_after["parent1"].values())) == (5, 376)
assert (len(rows_after["parent2"]), sum(rows_after["parent2"].values())) == (64, 5247)
lost = {name: set(parents[name]) - set(rows_after[name]) for name in ("parent1", "parent2")}
assert lost["parent1"] == {CHILD}
assert lost["parent2"] == {CHILD}
assert lost["parent2"] <= {"%032x" % k for k in cov2}
print("CONTROL independent D4 (explicit affine matrices) + deletion-orbit "
      "covers reproduce the published addition records field-by-field: 2 "
      "roots == child|1<<bit, popcount 7, 7 covers each, per-bit marginals "
      "9 / in-manifest 1 / zero-mim [82], child closed exactly "
      "once by bit16, set-equality holds, second target S5 6/459 -> 5 rows / "
      "376 and second open parent 65/5330 -> 64 rows / 5247")

# ---------- 7. 603-root inventory orbit analysis with the independent D4 ----------
inventory = set(prev) | {int(ROOTS[b], 16) for b in WIN_BITS}
assert len(inventory) == 603
orbits = {}
for r in inventory:
    orbits.setdefault(mycanon(r), []).append(r)
twin_pairs = sorted(
    sorted("%032x" % v for v in members) for members in orbits.values() if len(members) > 1)
assert len(orbits) == 592, len(orbits)
assert len(twin_pairs) == 11, len(twin_pairs)
new_orbits = {mycanon(int(ROOTS[b], 16)) for b in WIN_BITS}
assert len(new_orbits) == 2
assert not (new_orbits & {mycanon(r) for r in prev})
assert not ({int(ROOTS[b], 16) for b in WIN_BITS} & prev)
print("CONTROL 603-root folded inventory re-analysed with the independent "
      "D4: 603 roots / 592 distinct orbits / 11 twin pairs (590 + 2 new "
      "orbits, no new twins); the 2 new roots are disjoint from the "
      "601-root inventory raw-hex and D4-canonically")

# ---------- 8. completed claim closure ----------
f = claim["fold"]
head_str = "1313/6534/516144/4804/379867"
assert f["chain_head_before"] == "1312/6535/516227/4805/379950"
assert f["chain_head_after"] == head_str
assert f["receipts_folded"] == 2 and f["publication_order"] == WIN_BITS
assert f["total_marginal"] == total_marg and f["total_marginal_in_manifest"] == total_mim
assert f["zero_marginal_in_manifest"] == zero_mim
assert f["child_orbit_closed_by_bit"] == 16
assert f["parents_after"]["parent1"] == "5 rows / 376"
assert f["parents_after"]["parent2"] == "64 rows / 5247"
assert f["parents_lost_rows"]["parent1"] == [CHILD]
assert f["parents_lost_rows"]["parent2"] == sorted(lost["parent2"])
obs = f["output_blob_shas"]
assert (obs["head_json"], f["head_json_bytes"]) == PIN_HEAD_JSON
assert (obs["ranking_csv"], f["ranking_csv_bytes"]) == PIN_RANKING
assert (obs["top_candidates_csv"], f["top_candidates_csv_bytes"]) == PIN_TOPCAND
print("CONTROL completed claim fold record matches this recomputation: head "
      + head_str + ", three output blobs re-asserted byte-identical")

# ---------- 9. verification JSON ----------
results["controls_passed"] = {
    "tmp_reconstruction_executed":
        "the 9 missing tmp-cost83c files (legal-moves.json regenerated from "
        "scratch by exact-integer Bareiss 4x4, plus cert-receipts / bigint "
        "/ tsverify / consumed for bits 16,82) are regenerated from main "
        "artifacts by research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83c_20261115.py, executed "
        "here as a subprocess: published BigInt verifier 2/2 PASS (union "
        "0/0, terminal 13..17), published TS-Bareiss verifier 2/2 PASS, "
        "md5/rows/mobility cross-asserted against the published head JSON "
        "records (the 83c lane published no tmp checkpoint at all)",
    "fold_script_two_isolated_runs_byte_identical":
        "two short-lived subprocess re-runs of the published fold script "
        "complete with all in-script controls and regenerate the three "
        "outputs byte-identically to each other and to main (fc7832ed + "
        "6,811 B; 08f0d715 + 7,537 B; 6a40509d + 6,899 B)",
    "chain_head_1312_reproduced":
        "the fold script's runpy chain reproduces the cost-83b baseline "
        "1312/6535/516227/4805/379950 with the 83b head JSON and both CSVs "
        "blob-identical to main (in-script control, re-observed twice here)",
    "sweep_reaggregated":
        "fresh-code aggregation of the 11 raw batch JSONLs: 83 candidates "
        "exactly once (== claim enumeration), 2 WIN7-D10 [16,82] / "
        "81 REFUTED-D10 / 0 capped, 132,219,127 nodes (win sum 2,357,798), "
        "terminal ranges within [13,17], pilots 3402 x11, determinism rerun "
        "node-exact (8 bits), v15 cross-engine 2/2 WIN + 3/3 refuted "
        "anchors (bits 0/1/2), pilot 5949",
    "certificates_third_system_verified":
        "2 certificates re-read from published whole files with fresh code (bytes / "
        "md5 / sha256 / git blob == extraction receipts and the published "
        "head JSON records, rows sorted-unique) and geometrically "
        "re-verified by the published third-system rational verifier "
        "(exact Fraction circumcentre / cross-product collinearity, "
        "iterative replay): 90,144 rows / 3,257,864 bytes / 121 sub-roots, "
        "roots safe, unions 0/0, terminal ranges within [13,17], consumed "
        "winner-row sets == the reconstructed TS consumed sets (2/2)",
    "independent_d4_and_marginal_arithmetic":
        "an independently coded D4 group (8 explicit affine matrices, min "
        "image) reproduces each root's d4_canonical_hex, the deletion-orbit "
        "covers, and the per-bit marginals field-by-field against the "
        "published head JSON addition records; roots == child|1<<bit with "
        "popcount 7; total marginal 9 / in-manifest 1 / zero-mim "
        "[82]; child closed exactly once by bit16; set-equality "
        "s_1313 == s_1312 UNION covers(2 roots); second target S5 6/459 -> "
        "5 rows / 376 and second open parent 65/5330 -> 64 rows / 5247",
    "inventory_orbit_analysis":
        "603-root folded inventory (601 previous + 2 new) re-analysed with "
        "the independent D4: 592 distinct orbits / 11 twin pairs (590 + 2 "
        "new orbits, no new twins); the 2 new roots are disjoint from the "
        "previous inventory raw-hex and D4-canonically",
    "completed_claim_closure":
        "the completed claim fold record matches this recomputation: head "
        "1312->1313, publication order [16,82], totals 9/1, "
        "zero-mim [82], child closed by bit16, parents_after "
        "5 rows / 376 and 64 rows / 5247, lost rows == the child only "
        "(both parents), three output blob shas re-asserted",
}
results["fold_script_blob_sha"] = {
    "git_blob_sha": PIN_FOLD_SCRIPT[0], "bytes": PIN_FOLD_SCRIPT[1],
    "md5": md5_of((SCRIPTS / FOLD_SCRIPT).read_bytes()),
}
results["inputs"] = (
    "published main bytes only: the codeload main tarball mirror "
    "(kyouen-researches@main, HEAD e5673851) plus the cost-83c artifacts "
    "fetched from the main raw CDN and git-blob-sha verified (fold "
    "script, completed claim, 11 raw batches, determinism rerun, v15 "
    "crosscheck, 2 published certificates, head JSON and both CSVs); "
    "the 9 missing tmp files are regenerated in-step by the "
    "reconstruction script (itself from main artifacts via the published "
    "verifiers and exact-integer Bareiss); no state from the landing "
    "session was reused")
results["interpretation_guard"] = (
    "bookkeeping verification of a receipts fold only; solved 1313 measures "
    "manifest coverage, not the game-theoretic value of any position; "
    "REFUTED-D10 sweeps prove only the absence of a WIN7-D10 certificate; "
    "WIN7 certificates prove a first-player win within depth 10 from the "
    "individual 7-stone roots only; the standard 11x11 empty board, the "
    "two-stone roots {49,60}/{59,60}, S2 {59,60}, class1, class2 and "
    "class4 all remain UNKNOWN")
results["second_target_s5_after"] = {
    "s5_hex": PARENT1, "rows": 5, "remaining_s7_edge_cost": 376,
    "note": "best coverable class-2 target, still unresolved",
}
VERIF_JSON.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
print("written " + VERIF_JSON.name)
