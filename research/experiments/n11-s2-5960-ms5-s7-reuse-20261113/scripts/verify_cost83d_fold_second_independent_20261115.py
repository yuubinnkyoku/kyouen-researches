#!/usr/bin/env python3
"""Second independent verification of the cost-83d receipts fold
(2026-11-15, long-lane second-verification session).

The cost-83d fold (head 1313 -> 1314) was landed by the parallel lane
(commit 1c89d19e). Like the cost-83c lane, it published NO tmp-cost83d/
checkpoint at all: only the fold script, the three WIN7 certificates
(each split into two .cert.part*of2 pushes), the eleven raw batches,
the v15/v16 crosschecks, the completed claim and the three fold outputs
are on main. This session first fetches those 83d artifacts from the
main raw CDN into the mirror (git-blob-sha verified), then repairs the
gap with research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83d_20261115.py (regenerating
the 13 files the fold script reads - legal-moves.json from scratch via
exact-integer Bareiss, receipts / BigInt / TS-Bareiss / consumed from
the published verifiers), then re-verifies the whole fold from published
main bytes only, without any state from the landing session:

0. the published fold script, completed claim, head JSON, both CSVs, the
   first tmp reconstruction script and all six certificate parts are
   pinned to their main git blob shas;
1. BOTH tmp reconstruction scripts are executed as subprocesses: the
   published first implementation (legal_candidates module, published
   verifiers) and the second independent implementation written for this
   session (fresh exact-integer Bareiss, head-JSON-record
   cross-assertions, pinned parts); their outputs must agree (byte-level
   for legal-moves / consumed / joined certificates, field-level for the
   JSON receipts);
2. the published fold script recompute_frontier_cost83d_receipts_20261115.py
   is executed twice in isolated short-lived subprocesses; both runs must
   produce the three outputs byte-identically and match the completed
   claim's recorded git blob shas;
3. the fold script is then re-executed once in-process via runpy to expose
   the chain namespace (s_base / manifest / prev / remF2 / parents) for the
   independent arithmetic below;
4. the sweep is re-aggregated from the eleven raw batch JSONLs with fresh
   code (83 candidates exactly once, 3 WIN7-D10 / 80 REFUTED-D10 / 0
   capped, node sum, pilots, determinism rerun, v15 anchors);
5. all three published certificates are re-read with fresh code (fresh
   part-join, bytes / md5 / sha256 / git blob vs the reconstruction
   receipts and the head JSON records, rows sorted-unique) and
   re-verified geometrically by the published third-system rational
   verifier (exact Fraction circumcentre / cross-product collinearity,
   iterative replay), with the consumed winner-row sets compared to the
   reconstructed TS consumed files;
6. an independently coded D4 group (explicit affine matrices, minimum
   over the 8 images) re-derives each root's D4-canonical hex, the
   deletion-orbit covers, the per-bit marginals (both in- and
   non-manifest hex sets, compared field-by-field with the published
   head JSON addition records), the exactly-once child closure, and the
   set-equality s_1314 == s_1313 UNION covers(3 roots);
7. the 606-root folded inventory (603 previous + 3 new) is re-analysed
   with the independent D4: 595 distinct orbits, 11 twin pairs (the 3
   new roots form 3 new orbits and no new twins), and the 3 new roots
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
CERTS = OUT / "class2-lane-cost83d-certificates"
TMP = OUT / "tmp-cost83d"
SCRIPTS = HERE / "scripts"
CHILD = "00000000200000003800100000000200"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
PARENT2 = "00000000000000043800000008000000"
WIN_BITS = [16, 51, 82]
ROOTS = {
    16: "00000000200000003800100000010200",
    51: "00000000200000003808100000000200",
    82: "00000000200400003800100000000200",
}
HEAD_JSON = "class-frontier-cost83d-receipts-recompute-20261115.json"
RANKING = "class-frontier-s5-ranking-after-cost83d-receipts-20261115.csv"
TOPCAND = "class-frontier-top-candidates-s6-after-cost83d-receipts-20261115.csv"
FOLD_SCRIPT = "recompute_frontier_cost83d_receipts_20261115.py"
RECONSTRUCT_FIRST = "reconstruct_tmp_cost83d_20261115.py"
RECONSTRUCT_SECOND = "reconstruct_tmp_cost83d_second_independent_20261115.py"
RATIONAL_VERIFIER = "verify_cost75d_win7_rational_independent.py"
VERIF_JSON = OUT / "class2-lane-cost83d-fold-second-verification-20261115.json"

# blob pins of the published 83d fold script, the completed claim, and the
# first (simpler) tmp reconstruction script landed with the cost-84a claim
PIN_FOLD_SCRIPT = ("a07540cf8e8dd47dfd6d82e7ae8855017b24aeff", 22448)
PIN_CLAIM = ("e88ea50d7a27920df505e073266df15f07b7b0ce", 6413)
PIN_RECONSTRUCT_FIRST = ("591716b8f2c40295ddb529c4c4571f95e5dcbb55", 2520)
PIN_HEAD_JSON = ("49cb8022bc715fa22d7c2d483160083478676caa", 7407)
PIN_RANKING = ("d8adfb7e509af45bd1bd656dddc57b9087921486", 7537)
PIN_TOPCAND = ("454568f20685ac8f4da0d641b0a5f65fa2938234", 6813)
PIN_PARTS = {
    16: [("44176845d520a7feb3d1d18d3b1912a388c13623", 1226499),
         ("adb6daf529884d729731d45afa6c72b3dc7d2016", 1226472)],
    51: [("6a00807a4b47372df118b4dc4d6f80cf10d4be3b", 1049949),
         ("08378253032b6cb56d7ba914c9c6036aeaf2a96b", 1049928)],
    82: [("14559e5787772a4bd65f982181e8b05770d2d24b", 1638728),
         ("126b0a5f56c3ae7ed6ff94f6049225c9f30355cc", 1638684)],
}

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
           "schema": "n11-class2-lane-cost83d-fold-second-verification-20261115-v1"}

# ---------- 0. blob pins of the published artifacts under test ----------
for label, path, pin in (
        ("fold script", SCRIPTS / FOLD_SCRIPT, PIN_FOLD_SCRIPT),
        ("claim", OUT / "class2-lane-cost83d-inflight-20261115.json", PIN_CLAIM),
        ("head JSON", OUT / HEAD_JSON, PIN_HEAD_JSON),
        ("ranking CSV", OUT / RANKING, PIN_RANKING),
        ("top-candidates CSV", OUT / TOPCAND, PIN_TOPCAND)):
    sha, blen = blob_of(path)
    assert (sha, blen) == pin, (label, sha, blen)
for bit in WIN_BITS:
    for p, pin in zip(sorted(CERTS.glob(f"bit{bit}-root-{ROOTS[bit]}.cert.part*of2")),
                      PIN_PARTS[bit]):
        assert blob_of(p) == pin, (bit, p.name, blob_of(p))
print("CONTROL published artifact blob pins: fold script a07540cf (22,448 B), "
      "completed claim e88ea50d (6,413 B), head JSON 49cb8022 (7,407 B), "
      "ranking d8adfb7e (7,537 B), top-candidates 454568f2 (6,813 B), "
      "6 certificate parts (3 certificates x 2)")

claim = json.loads((OUT / "class2-lane-cost83d-inflight-20261115.json").read_text())
assert claim["status"].startswith("completed") and claim["s6_child"] == CHILD
assert claim["s6_s7_edge_cost"] == 83 and claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}
assert claim["candidate_count"] == 83 and len(claim["legal_candidates"]) == 83

# ---------- 1. dual tmp reconstruction (first + second implementation) ----------
sha, blen = blob_of(SCRIPTS / RECONSTRUCT_FIRST)
assert (sha, blen) == PIN_RECONSTRUCT_FIRST, (sha, blen)
# 1a. the first (published) reconstruction: legal_candidates module +
#     published verifiers, no published-value assertions of its own.
#     NOTE: the published TS verifier appends (--consumed-out uses
#     fs.appendFileSync) and the first implementation does not unlink the
#     target first, so its consumed.txt outputs are only deterministic
#     from a clean tmp-cost83d state; run it from a guaranteed-clean one.
import shutil
if TMP.exists():
    shutil.rmtree(TMP)
cp = subprocess.run([sys.executable, str(SCRIPTS / RECONSTRUCT_FIRST)],
                    capture_output=True, text=True, cwd=str(HERE))
assert cp.returncode == 0, ("first reconstruction failed", cp.stdout[-2000:], cp.stderr[-2000:])
assert "reconstructed" in cp.stdout
first_files = {}
first_files["legal-moves.json"] = (TMP / "legal-moves.json").read_bytes()
for bit in WIN_BITS:
    for suffix in ("cert-receipt.json", "bigint.json", "tsverify.json", "consumed.txt"):
        assert (TMP / f"bit{bit}.{suffix}").exists(), (bit, suffix)
    first_files[f"bit{bit}.consumed.txt"] = (TMP / f"bit{bit}.consumed.txt").read_bytes()
    first_files[f"bit{bit}.cert"] = (TMP / f"bit{bit}.cert").read_bytes()
    first_files[f"bit{bit}.cert-receipt.json"] = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    first_files[f"bit{bit}.bigint.json"] = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
    first_files[f"bit{bit}.tsverify.json"] = json.loads((TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1])
# 1b. the second independent reconstruction: fresh exact-integer Bareiss
#     geometry, head-JSON-record cross-assertions, pinned certificate parts
cp = subprocess.run([sys.executable, str(SCRIPTS / RECONSTRUCT_SECOND)],
                    capture_output=True, text=True, cwd=str(HERE))
assert cp.returncode == 0, ("second reconstruction failed", cp.stdout[-2000:], cp.stderr[-2000:])
assert "reconstruction complete" in cp.stdout
for bit in WIN_BITS:
    for suffix in ("cert-receipt.json", "bigint.json", "tsverify.json", "consumed.txt"):
        assert (TMP / f"bit{bit}.{suffix}").exists(), (bit, suffix)
# 1c. cross-implementation agreement of the two reconstructions
assert first_files["legal-moves.json"] == (TMP / "legal-moves.json").read_bytes()
for bit in WIN_BITS:
    assert first_files[f"bit{bit}.consumed.txt"] == (TMP / f"bit{bit}.consumed.txt").read_bytes(), bit
    joined_second = (TMP / f"c83d-bit{bit}.cert").read_bytes()
    assert first_files[f"bit{bit}.cert"] == joined_second, bit
    r1 = first_files[f"bit{bit}.cert-receipt.json"]
    r2 = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    assert (r1["bit"], r1["root_hex"], r1["rows"], r1["bytes"], r1["md5"], r1["sha256"]) == \
           (r2["bit"], r2["root_hex"], r2["rows"], r2["bytes"], r2["md5"], r2["sha256"]), bit
    assert first_files[f"bit{bit}.bigint.json"] == json.loads((TMP / f"bit{bit}.bigint.json").read_text()), bit
    assert first_files[f"bit{bit}.tsverify.json"] == json.loads(
        (TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1]), bit
print("CONTROL dual tmp reconstruction: the published first "
      "implementation (legal_candidates module + published verifiers, run "
      "from a guaranteed-clean tmp-cost83d because the TS verifier "
      "APPENDS to --consumed-out and the first implementation does not "
      "unlink it first) and the second independent implementation (fresh "
      "exact-integer Bareiss geometry, head-JSON-record cross-assertions, "
      "pinned parts, robust unlink-before-write) both regenerate "
      "tmp-cost83d/ and AGREE: legal-moves.json, the 3 consumed files and "
      "the 3 joined certificate byte streams byte-identical; receipts / "
      "BigInt / TS-verify JSONs field-identical when parsed")

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
      "reproduction of the 83c chain head 1313 with its blob-identical "
      "outputs), regenerate the three outputs byte-identically to each other "
      "and to the published main blobs "
      "(49cb8022 / d8adfb7e / 454568f2)")

# ---------- 3. in-process runpy for the chain namespace ----------
ns = runpy.run_path(str(SCRIPTS / FOLD_SCRIPT))
s_base = set(ns["s_base"])
s_cur = set(ns["s_cur"])
manifest = ns["manifest"]
prev = set(ns["prev"])
remF2 = ns["remF2"]
stF2 = ns["stF2"]
parents = ns["parents"]
assert len(prev) == 603
assert len(s_base & manifest) == 1313 and len(s_cur & manifest) == 1314
assert stF2["solved_s6_in_manifest"] == 1314 and stF2["unique_remaining_s6"] == 6533
assert stF2["sum_remaining_cost"] == 516061
assert stF2["s6_needed_by_open_classes"] == 4803 and stF2["cost_needed_by_open_classes"] == 379784
assert (len(parents["parent1"]), sum(parents["parent1"].values())) == (5, 376)
assert (len(parents["parent2"]), sum(parents["parent2"].values())) == (72, 6019)
assert CHILD in parents["parent1"] and CHILD in parents["parent2"]

# ---------- 4. independent sweep re-aggregation ----------
records = []
pilots = []
for i in range(1, 12):
    lines = jsonl(OUT / f"class2-lane-cost83d-raw-batch{i}-20261115.jsonl")
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False
    assert lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 83 and len(set(r["bit"] for r in records)) == 83
assert [r["bit"] for r in records] == claim["legal_candidates"]
win_bits = sorted(r["bit"] for r in records if r["loss"])
ref_bits = sorted(r["bit"] for r in records if not r["loss"])
assert win_bits == WIN_BITS and ref_bits == sorted(set(claim["legal_candidates"]) - set(WIN_BITS))
assert sum(1 for r in records if r["loss"]) == 3 and sum(1 for r in records if not r["loss"]) == 80
assert not any(r.get("capped") for r in records)
assert sum(r["nodes"] for r in records) == 153125301
win_node_sum = sum(r["nodes"] for r in records if r["loss"])
assert win_node_sum == 17873557
assert all(r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17 for r in records)
assert all(r["andclose"] is True for r in records)
assert pilots == [3402] * 11
det = jsonl(OUT / "class2-lane-cost83d-v16-determinism-rerun-20261115.jsonl")
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
raw_by_bit = {r["bit"]: r for r in records}
det_bits = sorted(r["bit"] for r in det[1:])
assert det_bits == [42, 43, 45, 46, 47, 48, 49, 50]
for r in det[1:]:
    raw = raw_by_bit[r["bit"]]
    assert r["nodes"] == raw["nodes"] and r["loss"] == raw["loss"]
v15 = jsonl(OUT / "class2-lane-cost83d-v15-crosscheck-20261115.jsonl")
v15_pilot = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilot) == 1 and v15_pilot[0]["nodes"] == 5949
v15_by_bit = {r["bit"]: r for r in v15 if "bit" in r}
assert set(v15_by_bit) == set(WIN_BITS) | {0, 1, 2}
assert all(v15_by_bit[b]["loss"] is True for b in WIN_BITS)
assert all(v15_by_bit[b]["loss"] is False for b in (0, 1, 2))
v15_win_nodes = {b: v15_by_bit[b]["nodes"] for b in WIN_BITS}
assert sum(v15_win_nodes.values()) == 29933192
print("CONTROL sweep re-aggregated with fresh code from 11 raw batches: 83 "
      "candidates exactly once (== claim enumeration), 3 WIN7-D10 "
      f"{WIN_BITS} / 80 REFUTED-D10 / 0 capped, 153,125,301 nodes (win sum "
      f"{win_node_sum}), terminal ranges within [13,17], pilots "
      "3402 x11, determinism rerun node-exact (8 bits 42..50), v15 "
      "cross-engine 3/3 WIN (sum 29,933,192) + 3/3 refuted anchors "
      "(bits 0/1/2), pilot 5949")

# ---------- 5. certificates: fresh part-join + third-system geometry ----------
moves_all = json.loads((TMP / "legal-moves.json").read_text())
cert_reports = []
for bit in WIN_BITS:
    root = ROOTS[bit]
    moves = legal_moves_of(root)
    assert moves == moves_all[str(bit)]["moves"], bit
    receipt = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
    assert len(parts) == 2, bit
    for p, pin in zip(parts, PIN_PARTS[bit]):
        assert blob_of(p) == pin, (bit, p.name)
    whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
    joined = Path(f"/tmp/second-verify-83d-bit{bit}.joined.cert")
    joined.write_bytes(whole)
    cert_arg = joined
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
        (OUT / HEAD_JSON).read_text())["cost83d_addition"]}[bit]
    assert len(rows) == pub_rec["rows"] and md5_of(whole) == pub_rec["md5"], bit
    mobility = len(moves)
    assert mobility == pub_rec["sub_roots_pass"]
    outc = Path(f"/tmp/second-verify-83d-bit{bit}.consumed.txt")
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
        "parts": [{"name": p.name, "bytes": p.stat().st_size,
                   "git_blob_sha": blob_of(p)[0]} for p in parts],
        "third_system": {"verdict": rat["verdict"], "union_missing": 0,
                         "union_extra": 0,
                         "terminal_stone_range": rat["terminal_stone_range"],
                         "winner_state_visits": rat["winner_state_visits"],
                         "loser_states": rat["loser_states"],
                         "loser_reply_edges": rat["loser_reply_edges"],
                         "consumed_set_equals_reconstructed_ts": True},
    })
assert sum(r["rows"] for r in cert_reports) == 216638
assert sum(r["bytes"] for r in cert_reports) == 7830260
assert sum(r["sub_roots"] for r in cert_reports) == 188
print("CONTROL 3 certificates re-joined from the pinned published parts "
      "and re-verified by the third-system rational verifier (Fraction "
      "circumcentre geometry, iterative replay): 216,638 rows / "
      "7,830,260 bytes / 188 sub-roots, roots safe, unions 0/0, terminal "
      "ranges within [13,17], consumed winner-row sets == the "
      "reconstructed TS consumed sets (3/3)")

# ---------- 6. independent D4 + marginal arithmetic ----------
pub_head = json.loads((OUT / HEAD_JSON).read_text())
pub_add = {rec["bit"]: rec for rec in pub_head["cost83d_addition"]}
assert [rec["bit"] for rec in pub_head["cost83d_addition"]] == WIN_BITS
my_marginals = {}
cov3 = set()
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
    cov3 |= cov
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
assert s_cur == s_base | cov3, "set-equality: s_1314 == s_1313 UNION covers(3 roots)"
total_marg = sum(len(m) for m, _ in my_marginals.values())
total_mim = sum(len(mm) for _, mm in my_marginals.values())
zero_mim = [b for b in WIN_BITS if not my_marginals[b][1]]
assert (total_marg, total_mim) == (13, 1)
assert zero_mim == [51, 82]
assert len(s_cur & manifest) == 1314

# parent bookkeeping with the independent covers
rows_after = {name: {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(h, [])}
              for name, h in (("parent1", PARENT1), ("parent2", PARENT2))}
for name in ("parent1", "parent2"):
    assert CHILD not in rows_after[name]
assert (len(rows_after["parent1"]), sum(rows_after["parent1"].values())) == (4, 293)
assert (len(rows_after["parent2"]), sum(rows_after["parent2"].values())) == (71, 5936)
lost = {name: set(parents[name]) - set(rows_after[name]) for name in ("parent1", "parent2")}
assert lost["parent1"] == {CHILD}
assert lost["parent2"] == {CHILD}
assert all(lost[name] <= {"%032x" % k for k in cov3} for name in ("parent1", "parent2"))
print("CONTROL independent D4 (explicit affine matrices) + deletion-orbit "
      "covers reproduce the published addition records field-by-field: 3 "
      "roots == child|1<<bit, popcount 7, 7 covers each, per-bit marginals "
      "5/4/4 = 13 / in-manifest 1 / zero-mim [51,82], child closed exactly "
      "once by bit16, set-equality holds, second target S5 5/376 -> 4 rows / "
      "293 and second open parent 72/6019 -> 71 rows / 5936")

# ---------- 7. 606-root inventory orbit analysis with the independent D4 ----------
inventory = set(prev) | {int(ROOTS[b], 16) for b in WIN_BITS}
assert len(inventory) == 606
orbits = {}
for r in inventory:
    orbits.setdefault(mycanon(r), []).append(r)
twin_pairs = sorted(
    sorted("%032x" % v for v in members) for members in orbits.values() if len(members) > 1)
assert len(orbits) == 595, len(orbits)
assert len(twin_pairs) == 11, len(twin_pairs)
new_orbits = {mycanon(int(ROOTS[b], 16)) for b in WIN_BITS}
assert len(new_orbits) == 3
assert not (new_orbits & {mycanon(r) for r in prev})
assert not ({int(ROOTS[b], 16) for b in WIN_BITS} & prev)
print("CONTROL 606-root folded inventory re-analysed with the independent "
      "D4: 606 roots / 595 distinct orbits / 11 twin pairs (592 + 3 new "
      "orbits, no new twins); the 3 new roots are disjoint from the "
      "603-root inventory raw-hex and D4-canonically")

# ---------- 8. completed claim closure ----------
f = claim["fold"]
head_str = "1314/6533/516061/4803/379784"
assert f["chain_head_before"] == "1313/6534/516144/4804/379867"
assert f["chain_head_after"] == head_str
assert f["receipts_folded"] == 3 and f["publication_order"] == WIN_BITS
assert f["total_marginal"] == total_marg and f["total_marginal_in_manifest"] == total_mim
assert f["zero_marginal_in_manifest"] == zero_mim
assert f["child_orbit_closed_by_bit"] == 16
assert f["parents_after"]["parent1"] == "4 rows / 293"
assert f["parents_after"]["parent2"] == "71 rows / 5936"
assert f["parents_lost_rows"]["parent1"] == [CHILD]
assert f["parents_lost_rows"]["parent2"] == [CHILD]
obs = f["output_blob_shas"]
assert (obs["head_json"], f["head_json_bytes"]) == PIN_HEAD_JSON
assert (obs["ranking_csv"], f["ranking_csv_bytes"]) == PIN_RANKING
assert (obs["top_candidates_csv"], f["top_candidates_csv_bytes"]) == PIN_TOPCAND
print("CONTROL completed claim fold record matches this recomputation: head "
      + head_str + ", three output blobs re-asserted byte-identical")

# ---------- 9. verification JSON ----------
results["controls_passed"] = {
    "dual_tmp_reconstruction_agreement":
        "the published first reconstruction (reconstruct_tmp_cost83d_20261115.py, "
        "git blob 591716b8, legal_candidates module + published verifiers) "
        "and the second independent reconstruction "
        "(reconstruct_tmp_cost83d_second_independent_20261115.py, fresh "
        "exact-integer Bareiss 4x4 geometry, published head-JSON-record "
        "cross-assertions, pinned certificate parts) are both executed here "
        "as subprocesses and AGREE: legal-moves.json, the 3 consumed files "
        "and the 3 joined certificate byte streams byte-identical; "
        "receipts / BigInt / TS-verify JSONs field-identical when parsed; "
        "BigInt verifier 3/3 PASS (union 0/0, terminal 13..17), TS-Bareiss "
        "verifier 3/3 PASS, md5/rows/mobility cross-asserted against the "
        "published head JSON records (the 83d lane published no tmp "
        "checkpoint at all). Implementation note: the published TS "
        "verifier APPENDS to --consumed-out (fs.appendFileSync) and the "
        "first implementation does not unlink the target first, so its "
        "consumed.txt outputs are deterministic only from a clean "
        "tmp-cost83d state (stale re-runs append duplicate keys; the "
        "fold script's set-based assertions still pass, but the files "
        "grow); the first implementation is therefore run here from a "
        "guaranteed-clean directory, and the second implementation "
        "unlinks before writing and is re-run safe",
    "fold_script_two_isolated_runs_byte_identical":
        "two short-lived subprocess re-runs of the published fold script "
        "complete with all in-script controls and regenerate the three "
        "outputs byte-identically to each other and to main (49cb8022 + "
        "7,407 B; d8adfb7e + 7,537 B; 454568f2 + 6,813 B)",
    "chain_head_1313_reproduced":
        "the fold script's runpy chain reproduces the cost-83c baseline "
        "1313/6534/516144/4804/379867 with the 83c head JSON and both CSVs "
        "blob-identical to main (in-script control, re-observed twice here)",
    "sweep_reaggregated":
        "fresh-code aggregation of the 11 raw batch JSONLs: 83 candidates "
        "exactly once (== claim enumeration), 3 WIN7-D10 [16,51,82] / "
        "80 REFUTED-D10 / 0 capped, 153,125,301 nodes (win sum 17,873,557), "
        "terminal ranges within [13,17], pilots 3402 x11, determinism rerun "
        "node-exact (8 bits 42..50), v15 cross-engine 3/3 WIN (sum "
        "29,933,192) + 3/3 refuted anchors (bits 0/1/2), pilot 5949",
    "certificates_third_system_verified":
        "3 certificates re-joined from the pinned published parts with "
        "fresh code (bytes / md5 / sha256 / git blob == the reconstruction "
        "receipts and the published head JSON records, rows sorted-unique) "
        "and geometrically re-verified by the published third-system "
        "rational verifier (exact Fraction circumcentre / cross-product "
        "collinearity, iterative replay): 216,638 rows / 7,830,260 bytes / "
        "188 sub-roots, roots safe, unions 0/0, terminal ranges within "
        "[13,17], consumed winner-row sets == the reconstructed TS "
        "consumed sets (3/3)",
    "independent_d4_and_marginal_arithmetic":
        "an independently coded D4 group (8 explicit affine matrices, min "
        "image) reproduces each root's d4_canonical_hex, the deletion-orbit "
        "covers, and the per-bit marginals field-by-field against the "
        "published head JSON addition records; roots == child|1<<bit with "
        "popcount 7; total marginal 13 / in-manifest 1 / zero-mim "
        "[51,82]; child closed exactly once by bit16; set-equality "
        "s_1314 == s_1313 UNION covers(3 roots); second target S5 5/376 -> "
        "4 rows / 293 and second open parent 72/6019 -> 71 rows / 5936",
    "inventory_orbit_analysis":
        "606-root folded inventory (603 previous + 3 new) re-analysed with "
        "the independent D4: 595 distinct orbits / 11 twin pairs (592 + 3 "
        "new orbits, no new twins); the 3 new roots are disjoint from the "
        "previous inventory raw-hex and D4-canonically",
    "completed_claim_closure":
        "the completed claim fold record matches this recomputation: head "
        "1313->1314, publication order [16,51,82], totals 13/1, "
        "zero-mim [51,82], child closed by bit16, parents_after "
        "4 rows / 293 and 71 rows / 5936, lost rows == the child only "
        "(both parents), three output blob shas re-asserted",
}
results["fold_script_blob_sha"] = {
    "git_blob_sha": PIN_FOLD_SCRIPT[0], "bytes": PIN_FOLD_SCRIPT[1],
    "md5": md5_of((SCRIPTS / FOLD_SCRIPT).read_bytes()),
}
results["inputs"] = (
    "published main bytes only: the codeload main tarball mirror "
    "(kyouen-researches@main, HEAD fcde0958) plus the cost-83d artifacts "
    "fetched from the main raw CDN and git-blob-sha verified (fold "
    "script, completed claim, 11 raw batches, determinism rerun, v15 "
    "crosscheck, 6 published certificate parts, head JSON and both CSVs); "
    "the 13 missing tmp files are regenerated in-step by the two "
    "reconstruction scripts (the published first implementation and the "
    "second independent implementation, both from main artifacts via "
    "the published verifiers; outputs agree byte- and field-level); no "
    "state from the landing session was reused")
results["interpretation_guard"] = (
    "bookkeeping verification of a receipts fold only; solved 1314 measures "
    "manifest coverage, not the game-theoretic value of any position; "
    "REFUTED-D10 sweeps prove only the absence of a WIN7-D10 certificate; "
    "WIN7 certificates prove a first-player win within depth 10 from the "
    "individual 7-stone roots only; the standard 11x11 empty board, the "
    "two-stone roots {49,60}/{59,60}, S2 {59,60}, class1, class2 and "
    "class4 all remain UNKNOWN")
results["second_target_s5_after"] = {
    "s5_hex": PARENT1, "rows": 4, "remaining_s7_edge_cost": 293,
    "note": "best coverable class-2 target, still unresolved",
}
VERIF_JSON.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
print("written " + VERIF_JSON.name)
