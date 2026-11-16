#!/usr/bin/env python3
"""Pre-registration of the cost-76d / cost-77e receipt fold on the canonical
head 1450 (the post-cost-66c-fold head), published BEFORE the fold receipt.

The four WIN7-D10 receipt roots (publication order):
  cost-76d bit 19  root 00000000040000003800080008080000  (commit 2384d263)
  cost-76d bit 49  root 00000000040000003802080008000000  (commit 4e7f932f)
  cost-77e bit 37  root 00000000040000809002002000004000  (commit 9c10999f)
  cost-77e bit 69  root 00000000040000a09002000000004000  (commit 51ace05a)

This script:
  1. blob-verifies every input artifact (claims, sweep records, raw batches,
     v15 crosschecks, determinism rerun, certificates, verify records, the
     head-1450 fold-projection tool and its output);
  2. re-derives both sweeps' aggregates from the 20 blob-pinned raw batches
     (candidate sets, WIN/REFUTED verdicts, node sums, terminal ranges,
     pilots) and re-asserts the cross-engine v15 crosschecks and the 77e
     determinism rerun;
  3. re-hashes all four certificates byte-for-byte (whole or joined parts)
     against the published manifests / certificate receipts, including the
     sorted-unique row property;
  4. runs the conflict census: 76 + 77 candidate D4 orbits vs the 771
     folded roots at head 1450, the pairwise 76d/77e candidate census, and
     the four WIN roots;
  5. asserts both children genuinely remain open at head 1450 on their two
     open class-2 parents each;
  6. independently projects the four-receipt fold (frontier semantics
     verbatim-ported from the published fold-projection tool) and asserts
     field-by-field equality with the pre-computed projection constants
     below, then emits the pre-registration JSON.

Bookkeeping over published receipts only.  Interpretation guard: solved
counts measure manifest coverage, not the game-theoretic value of any
position; WIN7 certificates prove a first-player win within depth 10 from
the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; the
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
SCRIPTS = HERE / "scripts"
sys.path.insert(0, str(SCRIPTS))
from fold_projection_head1450_tool_20261116 import (  # noqa: E402
    canon, covers, popcount, reconstruct, EXPECT_HEAD, HIST_1450,
    FOLD66C_JSON, FOLD66C_BLOB, git_blob_sha)

TOOL_SCRIPT = "fold_projection_head1450_tool_20261116.py"
TOOL_SCRIPT_BLOB = "49fcd8ae6706c075b39eea5b115b2a045c2950cf"
PROJ_JSON = "class2-lane-fold-projection-basis1450-4roots-20261116.json"
PROJ_JSON_BLOB = "005423113c601301e2b5c208d1138e17283cb774"

INPUT_BLOBS = {
    "class2-lane-cost76d-inflight-20261116.json":
        "d2e40a3e4c3ff5002395c7dcf46d50977c3a4964",
    "class2-lane-cost77e-inflight-20261116.json":
        "1cfa89e5b95b43dc497b439f9e1bfb4481c64669",
    "class2-lane-cost77e-sweep-20261116.json":
        "57afde38509ae3c10df0c6c38883c9b5d4fc67a5",
    "class2-lane-cost76d-sweep-audit-20261116.json":
        "a57af0161942a6f597cfabe9aef892df2fa7be3f",
    "class2-lane-cost76d-win7-certificates-20261116.json":
        "e8a6116aec45c19642877db85340e120d23331b3",
    "class2-lane-cost76d-77e-second-independent-verification-20261116.json":
        "d267fa8d93017110ff74df4520b3a8e8a47bee5b",
    "class2-lane-cost76d-v15-crosscheck-20261116.jsonl":
        "2268d5efc30b2f7966ac58742c08af017b0df956",
    "class2-lane-cost77e-v15-crosscheck-20261116.jsonl":
        "da60946a8a062403f43deead72f85ee5c1810195",
    "class2-lane-cost77e-v16-determinism-rerun-20261116.jsonl":
        "ca2007e1926b80ec6029f118f25a5380eebebe39",
    "class2-lane-cost76d-certificates/bit19-root-00000000040000003800080008080000.cert":
        "f36ac20a9d4c9ed27e76f3968f4619042e343beb",
    "class2-lane-cost76d-certificates/bit19-bareiss-verify.json":
        "abbd82383319babd136e143cd710d2e29526bbbf",
    "class2-lane-cost76d-certificates/bit19-root-00000000040000003800080008080000.cert.part1of1.summary.json":
        "0947b6255675541e376bc8d71ccd6754442c412a",
    "class2-lane-cost76d-certificates/bit49-root-00000000040000003802080008000000.cert":
        "5e2b8d56de5d8ecca8d309a930b1b5133f09a61f",
    "class2-lane-cost76d-certificates/bit49-bareiss-verify.json":
        "f884fcc072aa12d5c60abf6a571854cf5b8722ea",
    "class2-lane-cost76d-certificates/bit49-root-00000000040000003802080008000000.cert.part1of1.summary.json":
        "45add910f6a9b95d0d1ab456c26cb8a6b3094ae1",
    "class2-lane-cost77e-certificates/bit37-root-00000000040000809002002000004000.cert.part1of2":
        "e03ad8ec4285a66735ea5442f068fdf48ab051f3",
    "class2-lane-cost77e-certificates/bit37-root-00000000040000809002002000004000.cert.part2of2":
        "c249ed15b022ec3fe65f8dd62a4240fb3ec0770e",
    "class2-lane-cost77e-certificates/bit69-root-00000000040000a09002000000004000.cert.part1of2":
        "f696513ad9f8eea19466b9a1068210362bf0b2d4",
    "class2-lane-cost77e-certificates/bit69-root-00000000040000a09002000000004000.cert.part2of2":
        "f566c7014b11ff7a4bf22d32ef0e1244e406b3a5",
    "tmp-cost77e/bit37.bigint.json":
        "9eef2a342a733d38e270c8142912a6b79e3142b8",
    "tmp-cost77e/bit37.cert-receipt.json":
        "b4a352c2f0938e4c73ff7ee05209f790f653ad31",
    "tmp-cost77e/bit37.tsverify.json":
        "e885858319816b9276f3f50d05e25c939c673379",
    "tmp-cost77e/bit69.bigint.json":
        "90428fc23f65020e148e00e21dd6b0629867b9a1",
    "tmp-cost77e/bit69.cert-receipt.json":
        "6fefefa9afbd875d4dea8ccd5a2c387eb202f95e",
    "tmp-cost77e/bit69.tsverify.json":
        "d23e1b82551821641c197e9544aae1a1235f42b0",
    "tmp-cost77e/legal-moves.json":
        "04b2cac5f0a0d2287c3b4ae606f5a32d91eb862f",
}
for _n in range(1, 11):
    INPUT_BLOBS[f"class2-lane-cost76d-raw-batch{_n}-20261116.jsonl"] = {
        1: "d3c9ae3690c7c74e2b85fb4a84e0b02bb0ee06fb",
        2: "9144839aefc28cf4fd78710b1c130c0a0fe80f16",
        3: "8dae0d02ceea0b80ba1ecb0f853778b7dc158c23",
        4: "3c1e4557b97cc7f5cb2eb51cb79a9b02254ff11f",
        5: "c0c152d58a16aa9377ef8f365508699e32c71c94",
        6: "dbf10a3064c52472fddfc204fa4f0c00eaf6772e",
        7: "57c0eda0ffd3023ef44862c83c2eb547c7e4c584",
        8: "f4862407930d5658987dc4bc1fe9766c204ecf0e",
        9: "bc32bed989265468841bb076ccfa6328e94514e3",
        10: "8855f2d6f3821c1cd7d7e33eed6d17a63ecac3ee",
    }[_n]
    INPUT_BLOBS[f"class2-lane-cost77e-raw-batch{_n}-20261116.jsonl"] = {
        1: "2034e39709d598827d912074b15dc6a61df2d5ad",
        2: "cb883d07206e0f5ff4935ff4d36bbbf4addb7202",
        3: "a64d7a19456c11f79e473f9df08c785007867d75",
        4: "32d9d9582a848c0e65e91c56dfdab40de2fa74ee",
        5: "489f13e374f267fbc0a3a798e631e4fb543b4fc7",
        6: "5846d0470e43dc2ce49cecace0e6d628ff795765",
        7: "106ac2387f7d302dfcc5963abf26ca20174ec2bb",
        8: "3956be4dcc89009f07fd6e6ddb1eba8d186a8b54",
        9: "59df74f2902e8b45dadcef9ee451c27fbe3ff953",
        10: "d9f4fa3c5aa85fe9e408f45a88396d1edcb535c2",
    }[_n]

CHILD76 = "00000000040000003800080008000000"
CHILD77 = "00000000040000809002000000004000"
CHILD76_V = int(CHILD76, 16)
CHILD77_V = int(CHILD77, 16)
WIN76 = [19, 49]
WIN77 = [37, 69]
ROOTS = {
    ("76d", 19): "00000000040000003800080008080000",
    ("76d", 49): "00000000040000003802080008000000",
    ("77e", 37): "00000000040000809002002000004000",
    ("77e", 69): "00000000040000a09002000000004000",
}
NODES76 = 96246915
NODES77 = 116019458
WIN_NODES76 = {19: 1738943, 49: 1263398}     # v16 sweep nodes
EXTRACT_NODES76 = {19: 7205539, 49: 4333257}  # certificate extraction nodes
WIN_NODES77 = {37: 1819936, 69: 2623346}
PARENT_A = "00000000000000801202000040000000"   # second coverable class-2 S5
PARENT_B76 = "00000000000000003800000208000000"
PARENT_B77 = "00000000000000801202000000040000"

# ---- expected projection constants (independently pre-computed with the
# ---- head-1450 fold-projection tool, blob 00542311..., this session) -----
EXPECT_PROJ_HEAD = [1452, 174, 6396, 506144, 4669, 370058]
EXPECT_HIST_DELTA = {"c2=0,c4=1": 0, "c2=0,c4=2": 0, "c2=0,c4=3": 0,
                     "c2=1,c4=0": 0, "c2=1,c4=1": 0, "c2=1,c4=2": 0,
                     "c2=2,c4=0": -2, "c2=2,c4=1": 0, "c2=2,c4=2": 0}
EXPECT_MARG = {("76d", 19): (5, 1), ("76d", 49): (4, 0),
               ("77e", 37): (6, 1), ("77e", 69): (4, 0)}
EXPECT_CROSS = ("00000000040000809002000000004080", 86, 7, 242529, 251746)
EXPECT_AFFECTED = {
    PARENT_A: {"rows_before": 5, "rows_after": 3, "edge_cost_before": 364,
               "edge_cost_after": 211, "lost_edge_cost": 153,
               "lost_rows_hexes": [CHILD76, CHILD77]},
    PARENT_B76: {"rows_before": 65, "rows_after": 64,
                  "edge_cost_before": 5358, "edge_cost_after": 5282,
                  "lost_edge_cost": 76, "lost_rows_hexes": [CHILD76]},
    PARENT_B77: {"rows_before": 72, "rows_after": 71,
                  "edge_cost_before": 5960, "edge_cost_after": 5883,
                  "lost_edge_cost": 77, "lost_rows_hexes": [CHILD77]},
}
EXPECT_INCIDENCES = 4
EXPECT_COST_DELTA = 306
WATCH_65O = "00000000000000a09002080080000000"   # cost-65o bit-43 watch canon


def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def load_basis():
    import csv
    import gzip
    manifest = set()
    for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                manifest.add(int(row["hex"], 16))
    assert len(manifest) == 7867, len(manifest)
    classes = {}
    with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            classes[row["s5_hex"]] = int(row["classes"])
    with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="") as f:
        incidences = list(csv.DictReader(f))
    assert len(incidences) == 14558, len(incidences)
    winners = set()
    with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            winners.add(int(row["s6_hex"], 16))
    assert len(winners) == 498, len(winners)
    LOSS6 = ("00000000000000809202000400000000",
             "00000000000000003800004008000008",
             "00000000000000805202000000002000")
    rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16)
                in {int(x, 16) for x in LOSS6}}
    return manifest, classes, incidences, winners, rejected


def make_frontier(classes, incidences, rejected):
    def frontier(solved):
        remaining = defaultdict(list)
        for row in incidences:
            if row["s5_hex"] not in rejected and int(row["s6_hex"], 16) not in solved:
                remaining[row["s5_hex"]].append(row)
        unique = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
                  for rows in remaining.values() for r in rows}
        demand = defaultdict(lambda: {"c1": 0, "c2": 0, "c4": 0})
        for s5, rows in remaining.items():
            bits = classes.get(s5, 0)
            for row in rows:
                d = demand[row["s6_hex"]]
                if bits & 1:
                    d["c1"] += 1
                if bits & 2:
                    d["c2"] += 1
                if bits & 4:
                    d["c4"] += 1
        open_only = {k: v for k, v in demand.items() if v["c1"] == 0}
        return remaining, unique, demand, open_only

    def summary(solved):
        remaining, unique, demand, open_only = frontier(solved)
        hist = defaultdict(int)
        for v in open_only.values():
            hist[f"c2={v['c2']},c4={v['c4']}"] += 1
        return {
            "solved_s6_in_manifest": len(solved & manifest_holder[0]),
            "remaining_s5_orbits": len(remaining),
            "unique_remaining_s6": len(unique),
            "sum_remaining_cost": sum(unique.values()),
            "s6_needed_by_open_classes": len(open_only),
            "cost_needed_by_open_classes": sum(int(unique[k]) for k in open_only),
            "hist": dict(sorted(hist.items())),
        }
    return frontier, summary


manifest_holder = [None]


def check_cert_whole(path, rows, root_hex, md5, sha256, blob_sha, nbytes):
    data = Path(path).read_bytes()
    assert git_blob_sha(data) == blob_sha, path
    assert len(data) == nbytes, path
    assert hashlib.md5(data).hexdigest() == md5, path
    assert hashlib.sha256(data).hexdigest() == sha256, path
    lines = data.decode().splitlines()
    assert len(lines) == rows + 2, path
    assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                        "second_to_move_LOSS"), path
    assert lines[1] == f"root {root_hex}", path
    hexes = [ln.split(" ")[0] for ln in lines[2:]]
    assert len(hexes) == rows and hexes == sorted(set(hexes)), path


def main():
    # ---------- 0. blob verification of every input ------------------------
    for name, blob in INPUT_BLOBS.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
    assert git_blob_sha((SCRIPTS / TOOL_SCRIPT).read_bytes()) == TOOL_SCRIPT_BLOB
    assert git_blob_sha((OUT / PROJ_JSON).read_bytes()) == PROJ_JSON_BLOB
    assert git_blob_sha((OUT / FOLD66C_JSON).read_bytes()) == FOLD66C_BLOB
    print(f"CONTROL all {len(INPUT_BLOBS) + 3} input artifacts blob-verified "
          f"(claims, sweeps, 20 raw batches, crosschecks, determinism, "
          f"certificates, verify records, 66c fold JSON, projection tool "
          f"+ output)")

    claim76 = json.loads((OUT / "class2-lane-cost76d-inflight-20261116.json").read_text())
    claim77 = json.loads((OUT / "class2-lane-cost77e-inflight-20261116.json").read_text())
    assert claim76["status"] == "completed" and claim76["schema"] == \
        "n11-class2-lane-cost76d-inflight-20261116-v1"
    assert claim77["status"] == "in-flight" and claim77["schema"] == \
        "n11-class2-lane-cost77e-inflight-20261116-v1"
    assert claim76["s6_child"] == CHILD76 and claim77["s6_child"] == CHILD77
    assert claim76["candidate_count"] == 76 and claim77["candidate_count"] == 77
    assert claim76["demand"] == {"c1": 0, "c2": 2, "c4": 0}
    assert claim77["demand"] == {"c1": 0, "c2": 2, "c4": 0}

    # ---------- 1. sweep re-derivation from the raw batches ----------------
    def rederive(prefix, ncand, win_bits, node_total, win_nodes):
        recs = {}
        for n in range(1, 11):
            rows = load_jsonl(OUT / f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl")
            ctrl = [r for r in rows if "control" in r]
            cand = [r for r in rows if "bit" in r]
            assert len(ctrl) == 1 and ctrl[0]["control"] == "pilot_d6"
            assert ctrl[0]["nodes"] == 3402 and ctrl[0]["loss"] is False \
                and ctrl[0]["capped"] is False
            for r in cand:
                assert r["bit"] not in recs
                assert r["andclose"] is True
                assert r["terminalStoneRange"] == [13, 17]
                assert r["capped"] is False
                recs[r["bit"]] = r
        assert len(recs) == ncand
        assert sorted(recs) == sorted(claim76["legal_candidates"] if prefix == "cost76d"
                                      else claim77["legal_candidates"])
        win = sorted(b for b, r in recs.items() if r["loss"])
        refuted = sorted(b for b, r in recs.items() if not r["loss"])
        assert win == win_bits, win
        assert len(refuted) == ncand - len(win_bits)
        assert all(not r["capped"] for r in recs.values())
        assert sum(r["nodes"] for r in recs.values()) == node_total
        for b in win_bits:
            assert recs[b]["nodes"] == win_nodes[b], b
        # root identity: root = child | 1<<bit, each exactly 7 stones
        child_v = CHILD76_V if prefix == "cost76d" else CHILD77_V
        for b, r in recs.items():
            root_v = child_v | (1 << b)
            assert popcount(root_v) == 7
        return recs, win, refuted

    recs76, win76, refuted76 = rederive("cost76d", 76, WIN76, NODES76, WIN_NODES76)
    recs77, win77, refuted77 = rederive("cost77e", 77, WIN77, NODES77, WIN_NODES77)
    assert claim76["completion"]["sweep"]["win7_d10_bits"] == WIN76
    assert claim76["completion"]["sweep"]["node_sum"] == NODES76
    assert claim76["completion"]["sweep"]["win_roots"] == [ROOTS[("76d", 19)],
                                                           ROOTS[("76d", 49)]]
    sw77 = json.loads((OUT / "class2-lane-cost77e-sweep-20261116.json").read_text())
    ag = sw77["aggregate"]
    assert (ag["candidates"], ag["win7_d10_bits"], ag["refuted_d10"], ag["capped"]) == \
        (77, WIN77, 75, 0)
    assert ag["total_nodes"] == NODES77 and ag["win_node_sum"] == 4443282
    assert ag["win7_d10_nodes"] == {str(b): WIN_NODES77[b] for b in WIN77}
    assert ag["refuted_node_sum"] == NODES77 - 4443282
    assert ag["terminal_range_all"] == [13, 17] and ag["andclose_all"] is True
    assert ag["pilots_3402"] == 10
    print(f"CONTROL sweeps re-derived from the 20 raw batches: 76d 76/76 "
          f"(WIN {WIN76}, {NODES76} nodes) + 77e 77/77 (WIN {WIN77}, "
          f"{NODES77} nodes), 0 capped, all pilots 3402, terminal [13,17], "
          f"root=child|1<<bit identities OK, published aggregates agree")

    # v15 cross-engine anchors (verdict agreement only; nodes differ by engine)
    v15_76 = load_jsonl(OUT / "class2-lane-cost76d-v15-crosscheck-20261116.jsonl")
    v15_77 = load_jsonl(OUT / "class2-lane-cost77e-v15-crosscheck-20261116.jsonl")
    for lane, recs, win_bits, lines in (("76d", recs76, WIN76, v15_76),
                                        ("77e", recs77, WIN77, v15_77)):
        pit = [r for r in lines if "control" in r]
        assert len(pit) == 1 and pit[0]["nodes"] == 5949 and pit[0]["loss"] is False
        bits = {r["bit"]: r for r in lines if "bit" in r}
        for b, r in bits.items():
            assert r["capped"] is False
            assert r["loss"] == recs[b]["loss"], (lane, b, "v15/v16 disagree")
        for b in win_bits:
            assert b in bits and bits[b]["loss"] is True, (lane, b)
    det = [r for r in load_jsonl(OUT / "class2-lane-cost77e-v16-determinism-rerun-20261116.jsonl")
           if "bit" in r]
    assert len(det) == 16
    for r in det:
        raw = recs77[r["bit"]]
        assert (r["loss"], r["nodes"], r["capped"]) == \
            (raw["loss"], raw["nodes"], raw["capped"]), r["bit"]
    print("CONTROL v15 crosschecks agree with v16 on every anchor (incl. all "
          "four WIN bits); 77e v16 determinism rerun (batches 4+6, 16 bits) "
          "node-exact")

    # ---------- 2. certificates byte-for-byte -------------------------------
    wman = json.loads((OUT / "class2-lane-cost76d-win7-certificates-20261116.json").read_text())
    certs76 = {c["bit"]: c for c in wman["certificates"]}
    assert sorted(certs76) == WIN76
    for bit in WIN76:
        c = certs76[bit]
        pc = c["published_cert"]
        assert c["root_hex"] == ROOTS[("76d", bit)] and c["child_hex"] == CHILD76
        assert c["d4_canonical_hex"] == f"{canon(int(c['root_hex'], 16)):032x}"
        assert c["verdict"] == "WIN7" and c["fbt_drops"] == 0 and c["fatal"] is None
        assert c["terminal_range"] == [13, 17]
        assert c["extraction_nodes"] == EXTRACT_NODES76[bit], bit
        check_cert_whole(
            OUT / f"class2-lane-cost76d-certificates/bit{bit}-root-{c['root_hex']}.cert",
            c["rows"], c["root_hex"], pc["md5"], pc["sha256"],
            pc["git_blob_sha"], pc["bytes"])
        bv_lines = [json.loads(x) for x in
                    (OUT / f"class2-lane-cost76d-certificates/bit{bit}-bareiss-verify.json")
                    .read_text().splitlines() if x.strip()]
        assert bv_lines[0] == {"stones": 7, "loserMobility": c["sub_roots"]}, bit
        summ = json.loads((OUT / (f"class2-lane-cost76d-certificates/bit{bit}-root-"
                                  f"{c['root_hex']}.cert.part1of1.summary.json")).read_text())
        assert summ["bit"] == bit and summ["child"] == CHILD76
        assert summ["nRows"] == c["rows"] and summ["sum"] == EXTRACT_NODES76[bit]
        assert summ["fbt_drops"] == 0
        assert len(summ["moves"]) == c["sub_roots"]
        assert all(v["ok"] is True and v["capped"] is False
                   for v in summ["perMove"].values()), bit
        assert sorted(int(k) for k in summ["perMove"]) == sorted(summ["moves"])
    assert wman["totals"] == {"certificates": 2, "published_certificates": 2,
                              "rows": 78458, "extraction_nodes": 11538796,
                              "sub_roots": 109, "winner_states": 109726,
                              "loser_states": 32979, "terminal_count": 27257}
    assert wman["sweep_source"]["git_blob_sha"] == \
        INPUT_BLOBS["class2-lane-cost76d-sweep-audit-20261116.json"]
    print("CONTROL 76d certificates re-hashed byte-for-byte (bit19 44,810 "
          "rows / 1,618,698 B, bit49 33,648 rows / 1,215,488 B), sorted-"
          "unique rows, Bareiss 55/54 sub-roots PASS, manifest totals agree")

    for bit in WIN77:
        root_hex = ROOTS[("77e", bit)]
        rec = json.loads((OUT / f"tmp-cost77e/bit{bit}.cert-receipt.json").read_text())
        assert rec["root_hex"] == root_hex and rec["bit"] == bit
        whole = b""
        for part in rec["parts"]:
            pd = (OUT / f"class2-lane-cost77e-certificates/{part['name']}").read_bytes()
            assert git_blob_sha(pd) == part["git_blob_sha"], part["name"]
            assert len(pd) == part["bytes"], part["name"]
            whole += pd
        assert len(whole) == rec["whole_bytes"]
        assert hashlib.md5(whole).hexdigest() == rec["whole_md5"]
        assert hashlib.sha256(whole).hexdigest() == rec["whole_sha256"]
        lines = whole.decode().splitlines()
        assert len(lines) == rec["strategy_rows"] + 2, bit
        assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                            "second_to_move_LOSS"), bit
        assert lines[1] == f"root {root_hex}", bit
        hexes = [ln.split(" ")[0] for ln in lines[2:]]
        assert len(hexes) == rec["strategy_rows"] and \
            hexes == sorted(set(hexes)), bit
        bi = json.loads((OUT / f"tmp-cost77e/bit{bit}.bigint.json").read_text())
        assert bi["verdict"] == "WIN7 certificate independently verified"
        assert bi["root_hex"] == root_hex and bi["root_stones"] == 7 and \
            bi["root_safe"] is True and bi["rows_sorted_unique"] is True
        assert bi["union_missing"] == 0 and bi["union_extra"] == 0
        assert bi["strategy_rows"] == rec["strategy_rows"]
        assert bi["subroots_passed"] == 57 and bi["terminal_range"] == [13, 17]
        tv = json.loads((OUT / f"tmp-cost77e/bit{bit}.tsverify.json").read_text())
        assert tv["rows"] == rec["strategy_rows"]
        s = sw77["certificates"][f"bit{bit}"]
        assert s["root_hex"] == root_hex and s["md5"] == rec["whole_md5"]
        assert s["bytes"] == rec["whole_bytes"] and s["sub_roots"] == 57
    print("CONTROL 77e certificates re-hashed byte-for-byte (parts joined == "
          "whole; bit37 47,018 rows / 1,695,679 B, bit69 54,491 rows / "
          "1,964,949 B), sorted-unique rows, BigInt union 0/0 with 57/57 "
          "sub-roots each, tsverify rows agree, sweep record pins agree")

    ver = json.loads((OUT / "class2-lane-cost76d-77e-second-independent-verification-20261116.json").read_text())
    assert ver["verdict"] == "VERIFICATION PASSED" and ver["failures"] == []
    assert ver["cost76d"]["claim_status_completed"] is True
    assert ver["cost76d"]["claim_completion_win_bits"] is True
    assert ver["cost76d"]["sweep_rederivation"]["win_bits"] is True
    assert ver["cost76d"]["sweep_rederivation"]["node_sum"] is True
    assert ver["cost76d"]["bigint_rerun_reproduces_manifest_totals"] is True
    assert ver["cost76d"]["determinism_notes_published"] is True
    assert ver["cost76d"]["legal_candidates_reenumerated"] is True
    assert ver["cost77e"]["determinism_rerun_batches_4_6_node_exact"] is True
    assert ver["cost77e"]["determinism_rerun_covers_win_batches"] is True
    assert ver["cost77e"]["legal_candidates_reenumerated"] is True
    for b in ("37", "69"):
        assert all(v is True for v in ver["cost77e"]["certificates"][b]["checks"].values())
    assert ver["cost76d_bigint_rerun"]["19"]["strategy_rows"] == 44810
    assert ver["cost76d_bigint_rerun"]["49"]["strategy_rows"] == 33648
    print("CONTROL published second independent verification re-asserted "
          "(sweep re-derivations, determinism, all four certificates, "
          "BigInt reruns; commit ce88e071)")

    # ---------- 3. conflict census ----------------------------------------
    basis_roots = reconstruct()
    folded_d4 = {canon(r) for r in basis_roots}
    assert len(basis_roots) == 771 and len(folded_d4) == 756
    canons76 = {canon(CHILD76_V | (1 << b)) for b in claim76["legal_candidates"]}
    canons77 = {canon(CHILD77_V | (1 << b)) for b in claim77["legal_candidates"]}
    assert len(canons76) == 76 and len(canons77) == 77
    overlap_folded = sorted(canons76 & folded_d4) + sorted(canons77 & folded_d4)
    assert overlap_folded == [], overlap_folded
    cross = sorted(canons76 & canons77)
    assert len(cross) == 1, cross
    cross_canon = cross[0]
    b76 = [b for b in claim76["legal_candidates"]
           if canon(CHILD76_V | (1 << b)) == cross_canon][0]
    b77 = [b for b in claim77["legal_candidates"]
           if canon(CHILD77_V | (1 << b)) == cross_canon][0]
    assert recs76[b76]["loss"] is False and recs77[b77]["loss"] is False
    assert (recs76[b76]["capped"], recs77[b77]["capped"]) == (False, False)
    assert (b76, b77) == (EXPECT_CROSS[1], EXPECT_CROSS[2])
    assert f"{cross_canon:032x}" == EXPECT_CROSS[0]
    assert recs76[b76]["nodes"] == EXPECT_CROSS[3]
    assert recs77[b77]["nodes"] == EXPECT_CROSS[4]
    win_vs = [int(h, 16) for h in ROOTS.values()]
    assert len({canon(v) for v in win_vs}) == 4
    for v in win_vs:
        assert v not in basis_roots and canon(v) not in folded_d4
    for k, v in ROOTS.items():
        child_v = CHILD76_V if k[0] == "76d" else CHILD77_V
        assert v == f"{child_v | (1 << k[1]):032x}" and popcount(int(v, 16)) == 7
    assert WATCH_65O not in canons76 and WATCH_65O not in canons77
    print(f"CONTROL conflict census: 76+77 candidate D4 orbits all distinct "
          f"({len(canons76)} + {len(canons77)}), zero overlaps with the 771 "
          f"folded roots (756 canons); one cross-lane orbit "
          f"{cross_canon:032x} = 76d bit {b76} == 77e bit {b77}, both "
          f"REFUTED-D10 ({recs76[b76]['nodes']} vs {recs77[b77]['nodes']} "
          f"nodes, agreement, no conflict); the four WIN roots are pairwise "
          f"distinct and absent from the folded set; cost-65o bit-43 watch "
          f"canon absent from both candidate sets")

    # ---------- 4. frontier / basis head -----------------------------------
    manifest, classes, incidences, winners, rejected = load_basis()
    manifest_holder[0] = manifest
    frontier, summary = make_frontier(classes, incidences, rejected)
    solved = set(winners)
    for r in basis_roots:
        solved |= covers(r)
    base_summary = summary(solved)
    got = [base_summary[k] for k in
           ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
            "sum_remaining_cost", "s6_needed_by_open_classes",
            "cost_needed_by_open_classes")]
    assert got == EXPECT_HEAD, f"basis head mismatch: {got}"
    assert base_summary["hist"] == HIST_1450, base_summary["hist"]
    fold66 = json.loads((OUT / FOLD66C_JSON).read_text())
    fa = fold66["frontier_after_cost66c"]
    assert [fa[k] for k in
            ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
             "sum_remaining_cost", "s6_needed_by_open_classes",
             "cost_needed_by_open_classes")] == got

    # ---------- 5. the children genuinely remain open at head 1450 ---------
    rem_b, uniq_b, dem_b, open_b = frontier(solved)
    for child, parents in ((CHILD76, (PARENT_A, PARENT_B76)),
                           (CHILD77, (PARENT_A, PARENT_B77))):
        for h in parents:
            rows = rem_b.get(h, [])
            ch = [r for r in rows if r["s6_hex"] == child]
            assert len(ch) == 1, (child, h, len(ch))
            assert classes[h] == 2, h
        assert child in dem_b
        d = dem_b[child]
        assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), (child, d)
    for h, (rows, cost) in ((PARENT_A, (5, 364)), (PARENT_B76, (65, 5358)),
                            (PARENT_B77, (72, 5960))):
        rr = rem_b[h]
        assert len(rr) == rows, (h, len(rr))
        assert sum(int(r["s6_s7_edge_cost"]) for r in rr) == cost, h
    print("CONTROL both children genuinely remain open at head 1450 on "
          "their two open class-2 parents each (demand c1=0,c2=2,c4=0; "
          "parents 00000000000000801202000040000000 5 rows/364, "
          "00000000000000003800000208000000 65/5358, "
          "00000000000000801202000000040000 72/5960)")

    # ---------- 6. projection of the four-receipt fold ---------------------
    order = [("76d", 19), ("76d", 49), ("77e", 37), ("77e", 69)]
    s_cur = set(solved)
    receipts = []
    child_closed_by = {}
    marg_union = set()
    for lane, bit in order:
        root_v = int(ROOTS[(lane, bit)], 16)
        child_v = CHILD76_V if lane == "76d" else CHILD77_V
        cov = covers(root_v)
        assert child_v in cov, "the receipt must cover the child"
        marg = cov - s_cur
        marg_m = marg & manifest
        assert not (marg & marg_union), "receipt marginals must be disjoint"
        marg_union |= marg
        em, emim = EXPECT_MARG[(lane, bit)]
        assert (len(marg), len(marg_m)) == (em, emim), (lane, bit)
        if child_v in marg_m:
            child_closed_by[f"cost-{lane}"] = bit
        receipts.append({
            "lane": f"cost-{lane}",
            "bit": bit,
            "root_hex": ROOTS[(lane, bit)],
            "d4_canonical_hex": f"{canon(root_v):032x}",
            "d4_orbit_distinct_from_all_folded_roots": True,
            "covers": len(cov),
            "covers_hexes": sorted(f"{k:032x}" for k in cov),
            "marginal": len(marg),
            "marginal_hexes": sorted(f"{k:032x}" for k in marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
            "marginal_non_manifest_hexes":
                sorted(f"{k:032x}" for k in marg - marg_m),
            "certified": True,
            "sweep_nodes": (WIN_NODES76 if lane == "76d" else WIN_NODES77)[bit],
            "source": (f"cost-{lane} raw batches 1-10 (v16, blob-pinned) + "
                       f"published certificate"),
        })
        s_cur |= marg
    assert child_closed_by == {"cost-76d": 19, "cost-77e": 37}, child_closed_by
    assert len(marg_union) == 19 and sum(r["marginal_in_manifest"] for r in receipts) == 2
    cov_all = set()
    for lane, bit in order:
        cov_all |= covers(int(ROOTS[(lane, bit)], 16))
    assert s_cur == solved | cov_all, "set-equality control"

    st_after = summary(s_cur)
    got_after = [st_after[k] for k in
                 ("solved_s6_in_manifest", "remaining_s5_orbits",
                  "unique_remaining_s6", "sum_remaining_cost",
                  "s6_needed_by_open_classes", "cost_needed_by_open_classes")]
    assert got_after == EXPECT_PROJ_HEAD, got_after
    hist_deltas = {k: st_after["hist"].get(k, 0) - base_summary["hist"].get(k, 0)
                   for k in set(base_summary["hist"]) | set(st_after["hist"])}
    assert dict(sorted(hist_deltas.items())) == EXPECT_HIST_DELTA, hist_deltas

    # affected parents
    rem_a, uniq_a, dem_a, open_a = frontier(s_cur)
    new_hexes = {int(h, 16) for r in receipts for h in r["marginal_manifest_hexes"]}
    parents = {}
    for s5 in set(rem_b) | set(rem_a):
        rows_b = list(rem_b.get(s5, []))
        rows_a = list(rem_a.get(s5, []))
        if len(rows_b) == len(rows_a):
            continue
        lost = ({int(r["s6_hex"], 16) for r in rows_b}
                - {int(r["s6_hex"], 16) for r in rows_a}) & new_hexes
        if not lost:
            continue
        parents[s5] = {
            "s5_hex": s5,
            "classes": classes.get(s5, 0),
            "rows_before": len(rows_b), "rows_after": len(rows_a),
            "edge_cost_before": sum(int(r["s6_s7_edge_cost"]) for r in rows_b),
            "edge_cost_after": sum(int(r["s6_s7_edge_cost"]) for r in rows_a),
            "lost_rows_hexes": sorted(f"{x:032x}" for x in lost),
            "lost_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows_b
                                  if int(r["s6_hex"], 16) in lost),
        }
    assert sorted(parents) == sorted(EXPECT_AFFECTED), sorted(parents)
    for h, exp in EXPECT_AFFECTED.items():
        p = parents[h]
        for k, v in exp.items():
            assert p[k] == v, (h, k, p[k], v)
        assert p["classes"] == 2
    incidences_lost = sum(len(v["lost_rows_hexes"]) for v in parents.values())
    cost_delta = sum(v["lost_edge_cost"] for v in parents.values())
    assert (incidences_lost, cost_delta) == (EXPECT_INCIDENCES, EXPECT_COST_DELTA)
    # open-set deltas: exactly the two children leave the open-needed set
    assert set(open_b) - set(open_a) == {CHILD76, CHILD77}
    assert set(open_a) - set(open_b) == set()
    print(f"CONTROL four-receipt fold projection re-derived independently: "
          f"head {got[0]} -> {got_after}, hist delta c2=2,c4=0: -2, "
          f"marginal 19 / in-manifest 2, affected parents 3 "
          f"(incidences {incidences_lost}, edge-cost delta {cost_delta}); "
          f"open-needed set loses exactly the two children")

    result = {
        "schema": "n11-class2-lane-cost76d-77e-fold-preregistration-20261116-v1",
        "date": "2026-11-16",
        "method": (
            "pre-registration computed with scripts/fold_projection_"
            "head1450_tool_20261116.py (blob 49fcd8ae..., published in the "
            "same commit) and independently re-derived by this script on the "
            "independently reconstructed basis head 1450 (764 published "
            "receipt roots + the seven cost-66c WIN7-D10 receipt roots from "
            "the published fold JSON 8783993e + the 498 sweep winners; head "
            "numbers and demand histogram asserted equal to the published "
            "cost-66c fold record), folding in publication order the four "
            "WIN7-D10 receipt roots cost-76d bit 19 (commit 2384d263), "
            "cost-76d bit 49 (4e7f932f), cost-77e bit 37 (9c10999f) and "
            "cost-77e bit 69 (51ace05a), all four certified, dual-verified "
            "and re-hashed byte-for-byte here from the blob-pinned published "
            "files; both sweeps re-derived from the 20 blob-pinned raw "
            "batches with the v15 crosschecks and the 77e determinism rerun "
            "re-asserted. Every input is a blob-pinned pre-fold artifact. "
            "Published BEFORE the fold receipt lands."),
        "basis_head": 1450,
        "basis_head_numbers": EXPECT_HEAD,
        "basis_roots": 771,
        "basis_distinct_d4_canons": 756,
        "basis_summary": {k: base_summary[k] for k in
                          ("solved_s6_in_manifest", "remaining_s5_orbits",
                           "unique_remaining_s6", "sum_remaining_cost",
                           "s6_needed_by_open_classes",
                           "cost_needed_by_open_classes", "hist")},
        "receipt_bits": {"cost-76d": WIN76, "cost-77e": WIN77},
        "receipts": receipts,
        "projected_head": {k: st_after[k] for k in
                           ("solved_s6_in_manifest", "remaining_s5_orbits",
                            "unique_remaining_s6", "sum_remaining_cost",
                            "s6_needed_by_open_classes",
                            "cost_needed_by_open_classes")},
        "projected_head_numbers": EXPECT_PROJ_HEAD,
        "projected_hist": st_after["hist"],
        "demand_histogram_deltas": dict(sorted(hist_deltas.items())),
        "affected_parents": {k: v for k, v in sorted(parents.items())},
        "parent_row_incidences": incidences_lost,
        "parent_edge_cost_delta": cost_delta,
        "total_marginal": 19,
        "total_marginal_in_manifest": 2,
        "children_open_before_fold": {
            CHILD76: {"demand": {"c1": 0, "c2": 2, "c4": 0},
                      "open_parents": [PARENT_A, PARENT_B76]},
            CHILD77: {"demand": {"c1": 0, "c2": 2, "c4": 0},
                      "open_parents": [PARENT_A, PARENT_B77]},
        },
        "child_closed_by": {"cost-76d": 19, "cost-77e": 37},
        "conflict_census": {
            "candidate_d4_orbits": {"cost-76d": 76, "cost-77e": 77},
            "overlaps_with_folded_roots": 0,
            "cross_lane_overlap": {
                "d4_canonical_hex": f"{cross_canon:032x}",
                "cost-76d_bit": b76,
                "cost-77e_bit": b77,
                "verdicts": ["REFUTED-D10", "REFUTED-D10"],
                "nodes": {"cost-76d": recs76[b76]["nodes"],
                          "cost-77e": recs77[b77]["nodes"]},
                "agreement": True,
            },
            "win_roots_pairwise_distinct": True,
            "win_roots_absent_from_folded": True,
            "win_loss_conflicts": 0,
        },
        "cross_row_watch": {
            "cost-65o-bit43": ("the in-flight cost-65o bit-43 candidate "
                               f"canon {WATCH_65O} is absent from both "
                               "candidate sets"),
        },
        "planned_fold_publication": {
            "fold_json": "class-frontier-cost76d77e-receipts-recompute-20261116.json",
            "fold_script": "recompute_frontier_cost76d_77e_receipts_20261116.py",
            "log": "research/log/2026-11-16-n11-class2-lane-cost76d77e-fold.md",
            "claims_update": ("cost-76d claim gains a fold record; cost-77e "
                              "claim updated from in-flight to completed "
                              "with its sweep/certificate/fold records"),
            "check": ("the fold script must assert field-by-field agreement "
                       "with this pre-registration (head numbers, histogram, "
                       "receipts, affected parents, incidences, cost delta) "
                       "before writing the fold JSON"),
        },
        "interpretation_guard": (
            "bookkeeping fold projection only; no engine search beyond the "
            "already-published blob-pinned sweeps, no new verdicts; solved "
            "counts measure manifest coverage, not the game-theoretic value "
            "of any position; WIN7 certificates prove a first-player win "
            "within depth 10 from the individual 7-stone roots only; "
            "REFUTED-D10 is not a LOSS proof; 11x11 empty board, two-stone "
            "roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain "
            "UNKNOWN"),
    }
    out = OUT / "class2-lane-cost76d-77e-fold-preregistration-20261116.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print("written", out.name)


if __name__ == "__main__":
    main()
