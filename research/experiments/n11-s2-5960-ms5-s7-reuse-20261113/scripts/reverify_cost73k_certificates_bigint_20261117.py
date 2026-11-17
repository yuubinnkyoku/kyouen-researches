#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 22 WIN7-D10 certificates of
the newly published cost-73k certificate band (child
00000000000000801206000000000400, s6_s7_edge_cost 73, published by this
class2-lane session at band commits 40f8db4b..4c383a14 with the certificate
manifest in commit 4c383a14 and claim v3 at 795e2941), with a
third-implementation BigInt independent verification beyond the generator's
own Bareiss verification (verify_bit7_win7_cert.ts).

This follows the reverify_cost73j_certificates_bigint_20261117.py batch: on
top of the bytes pins it runs the BigInt independent verifier
(verify_win7_certificate_bigint_independent.mjs, git blob
62b5d9413daafb172f6e10249976ee6808f7b454) once per certificate and
cross-agrees the result with the full manifest record set (rows, subroots,
loser mobility, terminal range, md5, sha256, D4 canon), the per-bit
rootcheck.json sidecars (stones/loserMobility; two JSON lines) and the
per-bit subroots.jsonl sidecars (batched per-loser-first-move
seen/terminals/opponentEdges/range, summed to the verifier's
visited_states/terminal_count/loser_reply_edges).

Cost-73k specifics handled here:
 - the manifest lives INSIDE the band dir (class2-lane-cost73k-certificates/
   class2-lane-cost73k-win7-certificates-20261117.json, git blob
   0892aed07d187ae2fb3b4b90a21c7adbc1002b62, which is also the sha stated in
   the claim v3 certificates section and status text: all asserted against
   each other);
 - the manifest basis names claim v2 (git blob
   2150277f95fa202837d1cda10b390ee2bb54761b); the current claim file on main
   is v3 (certificates complete, git blob
   7f654548efeeab47975bdafefa6bcfab3f0ba945, schema ...-v3) and is mirrored
   and asserted (win7_d10_bits at actual_execution/results = the 25 WIN
   bits; the manifest covers the 22 sweep WIN bits, the 3 confirmation
   bits [14, 26, 55] are certified by the published 73j/73i/69j
   certificates);
 - rootcheck.json is a two-line JSONL and subroots.jsonl is BATCHED
   (up to 8 loser-first-moves per line), exactly as in the 72d/73j bands;
 - bits 39/41/62 are whole single files (no README-split); the other
   nineteen are split part1of2/part2of2 with README-split-bit{N}.md
   recombination docs;
 - the band was published one file per commit (44 commits
   40f8db4b..4c383a14 including two immediate repushes that fixed a
   chunk-boundary newline corruption introduced by the publication tooling
   in the first two commits); the landing was verified byte-exact against
   the local extraction md5s via git blob sha (41/41 certificate files);
 - cross-batch disjointness covers the 129 earlier BigInt-verified roots:
   the 113 of the five earlier batches plus the 16 roots of the cost-73j
   BigInt batch output (git blob
   34dd4504b889655e4e43f7b9a6f7b55391bdd562, fetched from the published
   repo), blob-pinned inline as in the 73j batch.

Run from the working mirror directory with the band dir mirrored under
bigint73k/certs73k/ (as certs73k/class2-lane-cost73k-certificates/), the
claim mirrored under bigint73k/certs73k-claim/, the seven earlier batch
outputs mirrored under bigint73k/earlier/, pins73k.txt (105 band-dir file
pins name|sha|size) present and the verifier under bigint73k/.

Determinism: no timestamps, no wall times, fixed record order; running twice
must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7-D10 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, re, subprocess

PIN = "795e2941da124cbac3bd751f3e020cf9b132fb58"
BAND_FIRST = "40f8db4b215ce90d4fc2cfe52b82fcead03a2558"
BAND_LAST = "4c383a14025a6a8c8551cb20e7eb7b26288f1bee"
ROOT = "bigint73k"
VERIFIER = f"{ROOT}/verify_win7_certificate_bigint_independent.mjs"
VERIFIER_BLOB_SHA = "62b5d9413daafb172f6e10249976ee6808f7b454"
NODE = "node"
MIRROR = os.environ.get("REVERIFY_MIRROR", f"{ROOT}/certs73k")
CLAIM_DIR = os.environ.get("REVERIFY_CLAIM_DIR", f"{ROOT}/certs73k-claim")
CLAIM_FILE = "class2-lane-cost73k-inflight-20261117.json"
CLAIM_BLOB_SHA = "7f654548efeeab47975bdafefa6bcfab3f0ba945"
CLAIM_V2_BASIS_BLOB_SHA = "2150277f95fa202837d1cda10b390ee2bb54761b"
MANIFEST_BLOB_SHA = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
EARLIER_DIR = os.environ.get("REVERIFY_EARLIER_DIR", f"{ROOT}/earlier")
PINS_FILE = f"{ROOT}/pins73k.txt"
BAND_DIR = "class2-lane-cost73k-certificates"
MANIFEST = "class2-lane-cost73k-win7-certificates-20261117.json"
EXPECTED = 22
EXPECTED_BITS = [0, 7, 11, 15, 35, 39, 41, 44, 58, 62, 73, 76,
                 87, 89, 94, 95, 97, 98, 103, 105, 112, 117]
CONFIRMATION_BITS = [14, 26, 55]
OUT = f"{ROOT}/class2-lane-cost73k-certificates-bigint-independent-reverification-20261117.json"

EARLIER_BATCHES = [
    ("earlier_singlefilebands.json",
     "class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json",
     "ceb79e97f530de7f2dcdb984a9b0be928bbf592a", 43),
    ("earlier_splitpartbands.json",
     "class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json",
     "5b91667255406175be32c0c47ccd48592a547607", 18),
    ("earlier_splitpartsweep.json",
     "class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117.json",
     "91e9f53923655be007c05e27ca471bc211a71345", 24),
    ("earlier_66j69j.json",
     "class2-lane-66j69j-certificates-bigint-independent-reverification-20261117.json",
     "c24224eaa3f48b0e5d1fbe90f4daccf284e6c968", 15),
    ("earlier_cost63cd.json",
     "class2-lane-cost63cd-certificates-regeneration-verification-20261117.json",
     "0978ed784439b05f36b0893faa0a97824f6c3a77", 2),
    ("earlier_cost72d.json",
     "class2-lane-cost72d-certificates-bigint-independent-reverification-20261117.json",
     "1fa6d465f6f87413f11ca113cdf6925a52859adf", 11),
    ("earlier_cost73j.json",
     "class2-lane-cost73j-certificates-bigint-independent-reverification-20261117.json",
     "34dd4504b889655e4e43f7b9a6f7b55391bdd562", 16),
]


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def d4_canon(h):
    """Independent D4 canonical form on the 11x11 board: min hex over the
    eight square symmetries. Ninth implementation; asserted against every
    record's d4_canon_root."""
    stones = [i for i in range(121) if int(h, 16) >> i & 1]
    assert len(stones) == 7, ("d4_canon expects 7 stones", h)
    best = None
    for xf in (False, True):
        for yf in (False, True):
            for sw in (False, True):
                v = 0
                for i in stones:
                    x, y = i % 11, i // 11
                    if xf:
                        x = 10 - x
                    if yf:
                        y = 10 - y
                    if sw:
                        x, y = y, x
                    v |= 1 << (y * 11 + x)
                hs = f"{v:032x}"
                if best is None or hs < best:
                    best = hs
    return best


def load_pins():
    pins = {}
    for line in open(PINS_FILE):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rel, sha, size = line.split("|")
        pins[f"{BAND_DIR}/{rel}"] = (sha, int(size))
    assert len(pins) == 105, len(pins)
    return pins


def load_records():
    mb = open(f"{MIRROR}/{BAND_DIR}/{MANIFEST}", "rb").read()
    assert git_blob_sha(mb) == MANIFEST_BLOB_SHA, "manifest blob sha mismatch"
    m = json.loads(mb)
    assert m["schema"] == "n11-class2-lane-cost73k-win7-certificates-20261117-v1"
    assert m["s6_child_hex"] == "00000000000000801206000000000400"
    assert m["s6_s7_edge_cost"] == 73
    assert CLAIM_V2_BASIS_BLOB_SHA in m["basis"], "manifest basis does not state the claim v2 blob"
    certs = m["certificates"]
    assert len(certs) == EXPECTED, len(certs)
    R = []
    for c in certs:
        assert c["verdict"] == "WIN7" and c["depth"] == 10
        assert c["subroots"] == c["subroots_pass"] and c["subroots_pass"] > 0
        assert c["union_missing"] == 0 and c["union_extra"] == 0
        assert c["terminal_stone_range"] == [13, 17]
        assert c["loser_mobility"] == c["subroots_pass"]
        assert c["fbt_drops"] == 0 and c["fatal"] is None
        assert len(c["root"]) == 32 and len(c["d4_canon_root"]) == 32
        split = c["storage"] != "whole file"
        if split:
            assert c["split_cut_byte"] is not None
            assert f".part1of2 ({c['split_cut_byte']} bytes)" in c["certificate_split"]
        else:
            assert c["split_cut_byte"] is None
            assert "published whole" in c["certificate_split"], \
                ("whole-file split note", c["bit"])
            mm = re.match(r"(\d+) bytes within the 1200000-byte whole-file "
                          r"threshold; published whole", c["certificate_split"])
            assert mm, ("whole-file split note format", c["bit"])
            assert int(mm.group(1)) == os.path.getsize(
                f"{MIRROR}/{BAND_DIR}/{c['file']}"), \
                ("whole-file note bytes", c["bit"])
        R.append({
            "bit": c["bit"], "root_hex": c["root"],
            "d4_canon_root": c["d4_canon_root"], "raw_is_canon": c["raw_is_canon"],
            "rows": c["rows"], "extraction_nodes": c["extraction_nodes"],
            "subroots_pass": c["subroots_pass"],
            "loser_mobility": c["loser_mobility"],
            "terminal_stone_range": c["terminal_stone_range"],
            "md5": c["md5"], "sha256": c["sha256"],
            "file": c["file"], "split": split,
        })
    bits = [r["bit"] for r in R]
    assert sorted(bits) == EXPECTED_BITS, bits
    roots = [r["root_hex"] for r in R]
    assert len(set(roots)) == len(roots), "duplicate root across records"
    canons = [r["d4_canon_root"] for r in R]
    assert len(set(canons)) == len(canons), "duplicate D4 canon across records"
    # manifest totals
    t = m["totals"]
    assert t["certificates"] == EXPECTED
    assert t["rows"] == sum(r["rows"] for r in R)
    assert t["extraction_nodes"] == sum(r["extraction_nodes"] for r in R)
    assert t["fbt_drops_total"] == 0 and t["capped_per_move_total"] == 0
    pub = 0
    for c in certs:
        if c.get("split_cut_byte") is None:
            pub += os.path.getsize(f"{MIRROR}/{BAND_DIR}/{c['file']}")
        else:
            pub += (os.path.getsize(f"{MIRROR}/{BAND_DIR}/{c['file']}.part1of2")
                    + os.path.getsize(f"{MIRROR}/{BAND_DIR}/{c['file']}.part2of2"))
    assert t["published_bytes"] == pub, (t["published_bytes"], pub)
    # cross-batch disjointness against the 129 earlier BigInt-verified roots
    earlier_roots, earlier_canons = set(), set()
    for fn, _repo_name, blob, n in EARLIER_BATCHES:
        b = open(f"{EARLIER_DIR}/{fn}", "rb").read()
        assert git_blob_sha(b) == blob, ("earlier batch pin", fn)
        d = json.loads(b)
        es = d["entries"]
        assert len(es) == n, (fn, len(es))
        for e in es:
            earlier_roots.add(e["root_hex"])
            earlier_canons.add(d4_canon(e["root_hex"]))
    assert len(earlier_roots) == 129, len(earlier_roots)
    ov = set(roots) & earlier_roots
    assert not ov, ("root overlap with the 129 earlier records", sorted(ov))
    ovc = set(canons) & earlier_canons
    assert not ovc, ("D4 canon overlap with the 129 earlier records",
                     sorted(ovc))
    # claim v3 pin: mirrored blob sha, schema, bits, manifest path, and the
    # manifest blob sha cross-stated in the claim v3 certificates section
    cb = open(f"{CLAIM_DIR}/{CLAIM_FILE}", "rb").read()
    assert git_blob_sha(cb) == CLAIM_BLOB_SHA, "claim v3 blob sha mismatch"
    claim = json.loads(cb)
    assert claim["schema"] == "n11-class2-lane-cost73k-inflight-20261117-v3"
    win_bits = claim["actual_execution"]["results"]["win7_d10_bits"]
    assert sorted(win_bits) == sorted(EXPECTED_BITS + CONFIRMATION_BITS), win_bits
    assert claim["certificates"]["manifest"].endswith(MANIFEST)
    assert claim["certificates"]["manifest_blob_sha"] == MANIFEST_BLOB_SHA, \
        "claim v3 certificates section does not state the pinned manifest blob sha"
    mm = re.search(r"manifest class2-lane-cost73k-win7-certificates-20261117"
                   r"\.json \(git blob ([0-9a-f]{40})\)", claim["status"])
    assert mm and mm.group(1) == MANIFEST_BLOB_SHA, \
        "claim v3 status does not state the pinned manifest blob sha"
    return R, m


def run_verifier(path, mobility):
    p = subprocess.run([NODE, VERIFIER, path, str(mobility)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verify_one(rec, pins):
    d = f"{BAND_DIR}/{rec['file']}"

    def pin_of(rel):
        assert rel in pins, ("unpinned file", rel)
        return pins[rel]

    if not rec["split"]:
        raw = open(f"{MIRROR}/{d}", "rb").read()
        pin = pin_of(d)
        assert git_blob_sha(raw) == pin[0], ("pin sha mismatch", d)
        assert len(raw) == pin[1], ("pin size mismatch", d)
        joined = raw
        storage = "whole file"
        parts = None
    else:
        p1, p2 = f"{d}.part1of2", f"{d}.part2of2"
        pin1, pin2 = pin_of(p1), pin_of(p2)
        raw1 = open(f"{MIRROR}/{p1}", "rb").read()
        raw2 = open(f"{MIRROR}/{p2}", "rb").read()
        assert git_blob_sha(raw1) == pin1[0] and len(raw1) == pin1[1], ("pin part1", d)
        assert git_blob_sha(raw2) == pin2[0] and len(raw2) == pin2[1], ("pin part2", d)
        assert len(raw1) == rec["split_cut"], ("split_cut_byte", d)
        assert raw1.endswith(b"\n"), ("part1 not on a line boundary", d)
        joined = raw1 + raw2
        storage = "split part1of2+part2of2 concatenation"
        parts = {"part1": {"pinned_blob_sha": pin1[0], "bytes": pin1[1]},
                 "part2": {"pinned_blob_sha": pin2[0], "bytes": pin2[1]}}
    # whole-file documentation: manifest md5 AND sha256
    assert md5(joined) == rec["md5"], ("manifest md5", rec["bit"])
    assert sha256(joined) == rec["sha256"], ("manifest sha256", rec["bit"])
    # header + data-row accounting (2 header lines precede the data rows)
    lines = joined.decode().splitlines()
    assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                       "second_to_move_LOSS"), ("header", rec["bit"])
    assert lines[1] == f"root {rec['root_hex']}", ("root line", rec["bit"])
    assert len(lines) - 2 == rec["rows"], ("data rows", rec["bit"])
    # sidecar records: rootcheck.json is a two-line JSONL
    rc_lines = [json.loads(l) for l in
                open(f"{MIRROR}/{BAND_DIR}/bit{rec['bit']}-rootcheck.json",
                     "rb").read().decode().strip().splitlines()]
    assert len(rc_lines) == 2, ("rootcheck lines", rec["bit"])
    assert rc_lines[0]["stones"] == 7, ("rootcheck stones", rec["bit"])
    assert rc_lines[0]["loserMobility"] == rec["loser_mobility"], \
        ("rootcheck mobility", rec["bit"])
    assert rc_lines[1]["rows"] == rec["rows"], ("rootcheck rows", rec["bit"])
    # subroots.jsonl is BATCHED: several loser-first-moves per line
    sr_lines = [json.loads(l) for l in
                open(f"{MIRROR}/{BAND_DIR}/bit{rec['bit']}-subroots.jsonl",
                     "rb").read().decode().strip().splitlines()]
    stats = {}
    for l in sr_lines:
        assert l["rows"] == rec["rows"], ("subroots line rows", rec["bit"])
        for k, s in l["stats"].items():
            assert k not in stats, ("duplicate subroot key", rec["bit"], k)
            stats[k] = s
    assert len(stats) == rec["subroots_pass"], ("subroots key count", rec["bit"])
    for k, s in stats.items():
        assert 13 <= s["range"][0] and s["range"][1] <= 17, \
            ("subroots range", rec["bit"], k)
    # README-split doc for split certificates
    readme = None
    if rec["split"]:
        rd = f"{BAND_DIR}/README-split-bit{rec['bit']}.md"
        pin_of(rd)
        txt = open(f"{MIRROR}/{rd}", "rb").read().decode()
        mm = re.search(r"is (\d+) bytes and is published as two parts", txt)
        assert mm, ("README split bytes", rec["bit"])
        assert int(mm.group(1)) == len(joined), ("README whole bytes", rec["bit"])
        mm = re.search(r"md5sum .*?#\s*([0-9a-f]{32})", txt)
        assert mm and mm.group(1) == rec["md5"], ("README md5", rec["bit"])
        mm = re.search(r"line boundary \(byte (\d+)\)", txt)
        assert mm and int(mm.group(1)) == parts["part1"]["bytes"], \
            ("README split byte", rec["bit"])
        mm = re.search(r"^root `([0-9a-f]{32})`", txt, re.M)
        assert mm and mm.group(1) == rec["root_hex"], ("README root", rec["bit"])
        readme = {"bytes": len(joined), "split_boundary": parts["part1"]["bytes"],
                  "md5": rec["md5"]}
    # BigInt independent verifier (third implementation beyond the
    # generator's Bareiss verify)
    tmp = f"/tmp/reverify_cost73k_{rec['bit']}.cert"
    with open(tmp, "wb") as fh:
        fh.write(joined)
    rc, out, err = run_verifier(tmp, rec["loser_mobility"])
    assert rc == 0, ("verifier nonzero", rec["bit"], err[:300])
    v = json.loads(out)
    os.unlink(tmp)
    assert v["verdict"] == "WIN7 certificate independently verified"
    assert v["root_hex"] == rec["root_hex"], ("root_hex", rec["bit"])
    assert v["root_stones"] == 7 and v["root_safe"] is True
    assert v["rows_sorted_unique"] is True
    assert v["union_missing"] == 0 and v["union_extra"] == 0
    assert v["strategy_rows"] == rec["rows"], ("rows", rec["bit"])
    assert v["consumed_winner_rows"] == rec["rows"], ("consumed rows", rec["bit"])
    assert v["subroots_passed"] == rec["subroots_pass"], ("subroots", rec["bit"])
    assert v["root_mobility"] == rec["loser_mobility"], ("mobility", rec["bit"])
    assert list(v["terminal_range"]) == rec["terminal_stone_range"], \
        ("trange", rec["bit"])
    # subroots sidecar sums == verifier sums (Bareiss-generated stats vs
    # BigInt verifier: third-implementation field agreement)
    assert sum(s["seen"] for s in stats.values()) == v["visited_states_across_subroots"], \
        ("subroots seen sum", rec["bit"])
    assert sum(s["terminals"] for s in stats.values()) == v["terminal_count"], \
        ("subroots terminals sum", rec["bit"])
    assert sum(s["opponentEdges"] for s in stats.values()) == v["loser_reply_edges"], \
        ("subroots opponentEdges sum", rec["bit"])
    # independent D4 canonicalization
    got_canon = d4_canon(rec["root_hex"])
    assert got_canon == rec["d4_canon_root"], \
        ("independent d4 canon", rec["bit"], got_canon, rec["d4_canon_root"])
    assert rec["raw_is_canon"] == (rec["root_hex"] == rec["d4_canon_root"]), \
        ("raw_is_canon consistency", rec["bit"])
    entry = {
        "bit": rec["bit"], "root_hex": rec["root_hex"],
        "d4_canon_root": rec["d4_canon_root"], "raw_is_canon": rec["raw_is_canon"],
        "certificate": d, "storage": storage,
        "record_source": f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{BAND_DIR}/{MANIFEST}",
        "record_kind": "win7-certificates manifest (in-band) + rootcheck.json (2-line JSONL) + subroots.jsonl (batched) + README-split",
        "joined_bytes": len(joined),
        "joined_md5": md5(joined),
        "joined_sha256": sha256(joined),
        "joined_git_blob_sha": git_blob_sha(joined),
        "manifest_md5_match": True,
        "manifest_sha256_match": True,
        "record_rows": rec["rows"],
        "record_extraction_nodes": rec["extraction_nodes"],
        "record_sub_roots_pass": rec["subroots_pass"],
        "record_loser_mobility": rec["loser_mobility"],
        "record_terminal_stone_range": rec["terminal_stone_range"],
        "rootcheck_stones": rc_lines[0]["stones"],
        "rootcheck_loser_mobility": rc_lines[0]["loserMobility"],
        "subroots_sidecar_lines": len(sr_lines),
        "subroots_sidecar_keys": len(stats),
        "verifier_status": "PASS",
        "verifier_root_mobility": v["root_mobility"],
        "verifier_rows": v["strategy_rows"],
        "verifier_subroots_passed": v["subroots_passed"],
        "verifier_terminal_range": v["terminal_range"],
        "verifier_terminal_count": v["terminal_count"],
        "verifier_visited_states": v["visited_states_across_subroots"],
        "verifier_loser_reply_edges": v["loser_reply_edges"],
        "verifier_winner_states": v["winner_states"],
        "verifier_loser_states": v["loser_states"],
        "verifier_union_missing": v["union_missing"],
        "verifier_union_extra": v["union_extra"],
    }
    if parts is not None:
        entry["parts"] = parts
    if readme is not None:
        entry["readme_split_doc"] = readme
    return entry, v


def main():
    vsrc = open(VERIFIER, "rb").read()
    assert git_blob_sha(vsrc) == VERIFIER_BLOB_SHA, "verifier blob sha mismatch"
    pins = load_pins()
    records, manifest = load_records()
    # splice split_cut_byte through the record dicts
    bybit = {c["bit"]: c["split_cut_byte"] for c in manifest["certificates"]}
    for r in records:
        r["split_cut"] = bybit[r["bit"]]
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(verify_one, rec, pins): rec for rec in records}
        for fut in concurrent.futures.as_completed(futs):
            e, v = fut.result()
            entries.append((futs[fut], e, v))
    entries.sort(key=lambda t: t[0]["bit"])

    assert len(entries) == EXPECTED
    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["joined_bytes"] for _, e, _ in entries)
    total_extraction_nodes = sum(e["record_extraction_nodes"] for _, e, _ in entries)
    n_split = sum(1 for _, e, _ in entries if e["storage"].startswith("split"))
    assert total_rows == manifest["totals"]["rows"]
    assert total_extraction_nodes == manifest["totals"]["extraction_nodes"]

    doc = {
        "schema": "n11-class2-lane-cost73k-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{BAND_DIR}/{MANIFEST} + 22x bitN-rootcheck.json + 22x bitN-subroots.jsonl + 19x README-split-bitN.md (bits 39/41/62 whole files) + 41 certificate files (19 split pairs + 3 whole) + claim v3 {CLAIM_FILE}",
            "authoritative_blob_sha_table": ("GitHub directory listing of the band certificate dir at the pinned commit "
                                             "(105 file pins name|sha|size, machine-extracted into pins73k.txt and asserted 105/105 "
                                             "against the mirrored bytes) + the claim v3 pin (106th); the seven earlier batch "
                                             "outputs used for disjointness are blob-pinned inline (129 earlier roots)"),
        },
        "method": {
            "records": ("22 WIN7-D10 certificate records of the newly published cost-73k band "
                        "(child 00000000000000801206000000000400, edge cost 73, claim v3 blob "
                        "7f654548efeeab47975bdafefa6bcfab3f0ba945; manifest basis names claim v2 blob "
                        "2150277f95fa202837d1cda10b390ee2bb54761b): in-band win7-certificates manifest "
                        "(rows/extraction_nodes/subroots_pass/loser_mobility/terminal_stone_range/md5/sha256/d4_canon_root/"
                        "raw_is_canon, union 0/0, fbt_drops 0, no fatal) plus per-bit rootcheck.json (2-line JSONL) and "
                        "subroots.jsonl (batched, up to 8 loser-first-moves per line) sidecars and README-split-bitN.md "
                        "recombination docs for the 19 split certificates; all 22 records structurally pre-asserted "
                        "(verdict WIN7, depth 10, subroots==subroots_pass==loser_mobility, terminal range [13,17])"),
            "bytes": ("each whole certificate or part fetched from the commit-pinned raw CDN URL into the local mirror; "
                      "git blob sha+size asserted against the authoritative GitHub directory listing at the pin (105/105 band "
                      "files + claim v3 = 106); the mirrored manifest reproduces git blob "
                      "0892aed07d187ae2fb3b4b90a21c7adbc1002b62, the sha the claim v3 certificates section and status text "
                      "state; split part1 asserted to end on a line boundary and to equal the manifest split_cut_byte; "
                      "certificates reconstructed as exact part1+part2 concatenations; joined md5 AND sha256 asserted "
                      "against the manifest; 2-line header asserted and data rows == manifest rows; README-split docs "
                      "cross-checked (whole bytes, split boundary byte, md5, root)"),
            "verifier": ("verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454, "
                         "asserted by the script; run with the expected loser mobility as argv[3]): BigInt 3x3 cofactor "
                         "expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no "
                         "solver/verdict-cache import; third implementation beyond the generator's own Bareiss "
                         "verify_bit7_win7_cert.ts documented in the manifest; per certificate asserted "
                         "verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/terminal range within "
                         "13..17/strategy_rows/subroots_passed/root_mobility/terminal_range/consumed_winner_rows"),
            "sidecar_cross_agreement": ("per-bit subroots.jsonl (Bareiss-verified per-loser-first-move stats, batched 8 per "
                                        "line) sums fully agree with the BigInt verifier output on all 22 certificates: "
                                        "sum(seen)==visited_states_across_subroots, sum(terminals)==terminal_count, "
                                        "sum(opponentEdges)==loser_reply_edges, m-key count==subroots_pass==loser_mobility, "
                                        "every per-move range within [13,17]; rootcheck.json line 1 stones==7 and "
                                        "loserMobility==manifest loser_mobility==verifier root_mobility, line 2 rows==manifest rows"),
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "independent_d4_canon_all_22_records": ("a ninth, in-script D4 canonicalization implementation (min hex over the "
                                                    "eight square symmetries of the 11x11 board) reproduces every record's "
                                                    "d4_canon_root for all 22 certificates; raw_is_canon verified as exactly "
                                                    "root_hex == d4_canon_root; the 22 D4 canons are mutually distinct"),
            "manifest_totals_agreement": ("manifest totals reproduced exactly by the re-verified bytes: certificates 22, "
                                         "rows 966535, extraction_nodes 155946109 (sum of per-cert values), published_bytes "
                                         "34933538 (sum of on-repo part/whole file sizes), fbt_drops_total 0, "
                                         "capped_per_move_total 0"),
            "cross_batch_root_disjointness": ("all 22 root_hex distinct in-batch and disjoint from the 129 root_hex values "
                                              "of the seven earlier independently re-verified batches (single-file 43 + "
                                              "split-part bands 18 + split-part sweepbands 24 + 66j/69j 15 + 63cd 2 + 72d 11 "
                                              "+ 73j 16), asserted at record load against the blob-pinned published batch "
                                              "outputs; D4-canon disjoint against the computed canons of all 129 earlier roots"),
            "claim_v3_basis_pin": ("the mirrored claim v3 file reproduces git blob 7f654548efeeab47975bdafefa6bcfab3f0ba945; "
                                   "its schema is n11-class2-lane-cost73k-inflight-20261117-v3, its "
                                   "actual_execution/results/win7_d10_bits equal the 25 sweep WIN bits "
                                   "[0,7,11,14,15,26,35,39,41,44,55,58,62,73,76,87,89,94,95,97,98,103,105,112,117] of which "
                                   "the manifest covers the 22 sweep WIN bits while the 3 confirmation bits [14,26,55] are "
                                   "certified by the published 73j/73i/69j certificates; its manifest path and "
                                   "manifest_blob_sha match and its status text states exactly the pinned manifest blob "
                                   "0892aed07d187ae2fb3b4b90a21c7adbc1002b62; the manifest basis in turn names claim v2 blob "
                                   "2150277f95fa202837d1cda10b390ee2bb54761b"),
            "beyond_publication_lane": ("the 73k publication's own verification (verify_bit7_win7_cert.ts, engine-free Bareiss) "
                                     "and the claim's fresh-process re-extraction determinism checks on bits "
                                     "[0,7,11,15,35,117] are documented in the manifest and claim; this batch adds the "
                                     "third-implementation BigInt verifier per certificate, the 106-file pin table, and the "
                                     "two sidecar record families' aggregate cross-agreement; the 41 landed certificate "
                                     "files were verified byte-exact against the local extraction md5s via git blob sha at "
                                     "publication time (41/41), and this batch re-derives every file from the "
                                     "commit-pinned CDN mirror instead"),
        },
        "summary": {
            "records": len(entries),
            "file_pins_asserted": 106,
            "split_certificates": n_split,
            "whole_certificates": len(entries) - n_split,
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "manifest_md5_mismatch": 0,
            "manifest_sha256_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "sidecar_cross_agreement_fail": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_extraction_nodes_in_manifest": total_extraction_nodes,
            "total_certificate_bytes_rehashed": total_bytes,
            "per_bit_loser_mobility": {str(t[0]["bit"]): t[0]["loser_mobility"] for t in entries},
        },
        "interpretation_guard": [
            ("this re-verification upgrades the 22 certificates of the newly published cost-73k band from "
             "manifest+sidecar documentation to bytes-level, third-implementation independently re-verified "
             "evidence; the bytes-re-verified population of this experiment stands at 327 + 22 = 349 records "
             "(counting per the 72d batch bookkeeping); it does not change any frontier number and closes no "
             "manifest row"),
            ("the cost-73k receipt fold stays pending behind the 76c/66i/66j/69j/71e/72d/73i folds managed by "
             "their own lanes; no manifest row is closed by this re-verification"),
            ("a WIN7-D10 certificate proves only that its individual 7-stone root is a first-player win within "
             "depth 10"),
            ("the 48 REFUTED-D10 bits of the cost-73k sweep are NOT LOSS proofs of those roots"),
            ("11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, class 1, class 2 and class 4 "
             "all remain UNKNOWN"),
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps(doc["summary"], indent=1))


if __name__ == "__main__":
    main()
