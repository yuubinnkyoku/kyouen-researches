#!/usr/bin/env python3
"""Replay-audit the two published cost-78a WIN7 certificates (bits 20 and 36)
from the parallel lane, against the published sweep audit, v15 crosscheck and
in-flight claim, with the independent BigInt verifier (no engine import).

The parallel lane published bit36 (single file) and bit20 (two parts split at a
line boundary) while this lane completed the cost-76a receipts fold; bits
8/29/109 are still pending publication there. This audit independently
re-verifies the two published certificates byte-exact against main by git
blob sha, re-joins the bit20 parts at the line boundary, re-runs
verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 cofactor expansion;
no solver, verdict cache, or repository verifier import) on both, re-derives
the six-stone parent-lift orbits, and ties the result to the new canonical
chain head 1195/6652/524884/4922/388607 produced by the cost-76a receipts fold:
the cost-78a child orbit 00000000000000809102000000400000 is still remaining
at the 1195 head (third class-2 target S5 rows 69/74/78 = 221), so this audit
changes no frontier count; the eventual cost-78a receipt fold must rebase on
the 1195 head.

Receipts-only bookkeeping: WIN7 certificates prove a first-player win within
depth 10 from the individual 7-stone roots only. REFUTED-D10 sweeps prove only
the absence of WIN7-D10. The 11x11 empty board, the two-stone roots {49,60}
and {59,60}, S2 {59,60}, class 2 and class 4 remain UNKNOWN.
"""
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
CERTS = OUT / "class2-lane-cost78a-certificates"
VERIFY = EXP / "scripts" / "verify_win7_certificate_bigint_independent.mjs"

CHILD = 0x00000000000000809102000000400000
PARENT_S5 = "00000000000000809102000000000000"
WIN_BITS_ALL = [8, 20, 29, 36, 109]
PUBLISHED_BITS = [20, 36]

# git blob shas verified against main in this session (files byte-exact)
MAIN_BLOBS = {
    "class2-lane-cost78a-sweep-audit-20261115.json":
        "227098581af12c2a1911f8edb02dc914a476a0d7",
    "class2-lane-cost78a-v15-crosscheck-20261115.jsonl":
        "eb22e9f8be6f2b5668d2d04567c37c6933731146",
    "class2-lane-cost78a-inflight-20261115.json":
        "5298e966634976651251479397b476c6a88b8923",
    "class2-lane-cost78a-certificates/bit20-root-00000000000000809102000000500000.cert.part1of2":
        "feedb02de70206f8630bfdeae9d7a5eadc068173",
    "class2-lane-cost78a-certificates/bit20-root-00000000000000809102000000500000.cert.part2of2":
        "84d59223f7fb4752dd115407f552563989e1a504",
    "class2-lane-cost78a-certificates/bit36-root-00000000000000809102001000400000.cert":
        "ea30ad286dd1c3de674ff834da5778b5e0a26ae0",
}

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def points(mask: int):
    return [p for p in range(121) if (mask >> p) & 1]

def transform_point(point: int, index: int) -> int:
    x, y = point % 11, point // 11
    maps = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
            (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
    tx, ty = maps[index]
    return 11 * ty + tx

def transform(mask: int, index: int) -> int:
    return sum(1 << transform_point(p, index) for p in points(mask))

def canonical(mask: int) -> int:
    return min(transform(mask, index) for index in range(8))

def main() -> None:
    # ---------- 1. input files byte-exact against main ----------
    for name, want in MAIN_BLOBS.items():
        data = (OUT / name).read_bytes()
        sha = git_blob_sha(data)
        check(sha == want, f"git blob sha mismatch vs main: {name} ({sha} != {want})")
    print(f"CONTROL {len(MAIN_BLOBS)} cost-78a input files byte-exact against main "
          "(git blob shas: sweep audit, v15 crosscheck, claim, bit20 part1/part2, bit36 cert)")

    sweep = json.loads((OUT / "class2-lane-cost78a-sweep-audit-20261115.json").read_text())
    check(sweep["schema"] == "n11-class2-lane-cost78a-raw-sweep-audit-20261115-v1", "sweep schema")
    check(sweep["target"]["s6_child_hex"] == f"{CHILD:032x}", "sweep child")
    check(sweep["target"]["edge_cost"] == 78 and sweep["target"]["legal_candidate_count"] == 78, "sweep target")
    agg = sweep["aggregate"]
    check(agg["candidates"] == 78 and agg["win7_d10"] == 5 and agg["refuted_d10"] == 73
          and agg["capped"] == 0, "sweep aggregate")
    check(agg["win7_d10_bits"] == WIN_BITS_ALL, "sweep win bits")
    wr = {w["bit"]: w for w in sweep["win_roots"]}
    check(sorted(wr) == WIN_BITS_ALL, "sweep win_roots")

    v15_lines = (OUT / "class2-lane-cost78a-v15-crosscheck-20261115.jsonl").read_text().splitlines()
    v15 = [json.loads(l) for l in v15_lines if l.strip()]
    v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
    pilots = [r for r in v15 if r.get("control") == "pilot_d6"]
    check(len(pilots) == 2 and all(p["loss"] is False and p["nodes"] == 5949 for p in pilots),
          "v15 pilots 5949 x2")

    claim = json.loads((OUT / "class2-lane-cost78a-inflight-20261115.json").read_text())
    check(claim["schema"] == "n11-class2-lane-cost78a-inflight-20261115-v1", "claim schema")
    check(claim["s6_child"] == f"{CHILD:032x}" and claim["s6_s7_edge_cost"] == 78, "claim child")
    check(claim["status"] == "in-flight", "claim status at audit time")
    pub = {e["bit"]: e for e in claim["certificates"]["published"]}
    check(sorted(pub) == PUBLISHED_BITS, "claim published bits at audit time")
    check(claim["certificates"]["win7_bits_pending"] == [8, 29, 109], "claim pending bits")
    print(f"CONTROL claim: {len(pub)}/5 published (bits {sorted(pub)}), pending [8, 29, 109]; "
          "sweep 78 candidates / 5 WIN7-D10 / 73 REFUTED / 0 capped")

    # ---------- 2. bit20 parts: join at line boundary ----------
    p1 = CERTS / "bit20-root-00000000000000809102000000500000.cert.part1of2"
    p2 = CERTS / "bit20-root-00000000000000809102000000500000.cert.part2of2"
    d1, d2 = p1.read_bytes(), p2.read_bytes()
    check(d1.endswith(b"\n"), "bit20 part1 must end at a line boundary")
    joined = d1 + d2
    joined_md5 = hashlib.md5(joined).hexdigest()
    c20 = pub[20]
    check(len(d1) == c20["parts"][0]["bytes"] == 1020151, "part1 bytes")
    check(len(d2) == c20["parts"][1]["bytes"] == 1018923, "part2 bytes")
    check(len(joined) == c20["bytes"] == 2039074, "joined bytes")
    check(joined_md5 == c20["joined_md5_equals_whole_md5"] == "348871fd605dedeb34b5a4c4ad6f518c",
          f"joined md5 mismatch: {joined_md5}")
    jpath = CERTS / "replay-joined-bit20.cert"
    jpath.write_bytes(joined)
    whole_sha20 = git_blob_sha(joined)
    print("CONTROL bit20 parts re-joined at the line boundary: 1,020,151 + 1,019,023 = "
          f"2,039,074 bytes, md5 {joined_md5} == claim joined_md5")

    # ---------- 3. independent BigInt verification of both published certs ----------
    verified = []
    for bit, path, mobility, rows_expect, nodes16, nodes15, d4 in (
            (20, jpath, 64, 56452, 2523199, 9116968, "00000000000000809102000000500000"),
            (36, CERTS / "bit36-root-00000000000000809102001000400000.cert",
             59, 50711, 1435988, 6829497, "00000000000000809102001000400000")):
        w = wr[bit]
        c = pub[bit]
        root = int(w["root_hex"], 16)
        check(root == CHILD | (1 << bit), f"root must equal child | 1<<bit{bit}")
        check(w["root_hex"] == c["root_hex"], "root vs claim")
        check(w["nodes"] == nodes16 == c["v16_sweep_nodes"] == c["v16_sweep_nodes"], "v16 nodes")
        check(w["opponent_legal_replies"] == mobility, "sweep opponent replies")
        check(c["rows"] == rows_expect, "claim rows")
        v = v15_bits[bit]
        check(v["loss"] is True and v["capped"] is False and v["nodes"] == nodes15
              == c["v15_anchor_nodes"], f"v15 anchor bit {bit}")
        data = Path(path).read_bytes()
        check(git_blob_sha(data) == (whole_sha20 if bit == 20 else
                                    MAIN_BLOBS["class2-lane-cost78a-certificates/"
                                               "bit36-root-00000000000000809102001000400000.cert"]),
              f"whole-file blob sha bit {bit}")
        run = subprocess.run(["node", str(VERIFY), str(path), str(mobility)],
                              capture_output=True, text=True, timeout=1200)
        check(run.returncode == 0, f"verifier failed for bit {bit}: {run.stderr[-500:]}")
        result = json.loads(run.stdout)
        check(result["verdict"] == "WIN7 certificate independently verified", "verifier verdict")
        check(result["root_hex"] == f"{root:032x}" and result["root_stones"] == 7
              and result["root_safe"] is True, "root check")
        check(result["root_mobility"] == mobility == result["subroots_passed"], "sub-roots")
        check(result["strategy_rows"] == rows_expect and result["rows_sorted_unique"] is True,
              "rows")
        check(result["consumed_winner_rows"] == rows_expect, "consumed == rows")
        check(result["union_missing"] == 0 and result["union_extra"] == 0, "union")
        check(result["terminal_range"] == [13, 17], "terminal range")
        # d4 canonical agreement
        check(w["d4_canonical_hex"] == d4 == f"{canonical(root):032x}", "d4 canonical")
        # parent-lift: the child orbit must be among the 6-stone one-stone deletions
        parents = sorted({canonical(root ^ (1 << p)) for p in points(root)})
        check(canonical(CHILD) in parents, "the child orbit must be a parent-lift of the root")
        verified.append({
            "bit": bit,
            "root_hex": f"{root:032x}",
            "d4_canonical_hex": f"{canonical(root):032x}",
            "root_mobility": mobility,
            "subroots_passed": result["subroots_passed"],
            "rows": result["strategy_rows"],
            "joined_or_single": "2 parts joined at line boundary" if bit == 20 else "single file",
            "bytes": len(data),
            "md5": hashlib.md5(data).hexdigest(),
            "whole_git_blob_sha": git_blob_sha(data),
            "visited_states_across_subroots": result["visited_states_across_subroots"],
            "winner_states": result["winner_states"],
            "loser_states": result["loser_states"],
            "loser_reply_edges": result["loser_reply_edges"],
            "terminal_count": result["terminal_count"],
            "terminal_range": result["terminal_range"],
            "union_missing": result["union_missing"],
            "union_extra": result["union_extra"],
            "v16_sweep_nodes": nodes16,
            "v15_anchor_nodes": nodes15,
            "claim_extraction_nodes": c["extraction_nodes"],
            "parent_lift_orbits": [f"{p:032x}" for p in parents],
            "child_orbit_covered": True,
        })
        print(f"CONTROL bit {bit}: BigInt independent verifier PASS - {mobility} sub-roots "
              f"== mobility == sweep opponent replies, {result['strategy_rows']} rows "
              "sorted-unique, consumed union 0/0, terminal [13,17], child orbit present "
              "in the parent-lift")
    jpath.unlink()

    # ---------- 4. tie-in to the 1195 head ----------
    # the child must still be remaining at the new canonical head (no fold yet)
    top = (OUT / "class-frontier-top-candidates-s6-after-cost76a-receipts-20261115.csv").read_text()
    rows = {}
    for line in top.splitlines():
        if line.startswith(PARENT_S5 + ","):
            parts = line.split(",")
            rows[parts[1]] = int(parts[2])
    check(rows == {
        "00000000000000809102000000002000": 69,
        "00000000000000809142000000000000": 74,
        "00000000000000809102000000400000": 78,
    }, f"third class-2 target rows at the 1195 head: {rows}")
    check(f"{CHILD:032x}" in rows, "the cost-78a child must still be remaining at the 1195 head")

    output = {
        "schema": "n11-class2-cost78a-published-certificate-replay-20261115-v1",
        "date": "2026-11-15",
        "status": "PASS",
        "audit_scope": "the two cost-78a WIN7 certificates published on main at audit time "
                       "(bit36 single file, bit20 two parts); bits 8/29/109 pending publication "
                       "by the parallel lane and not audited here",
        "method": "all six input files asserted byte-exact against main by git blob sha; the "
                  "bit20 parts re-joined at the verified line boundary (joined md5 == claim "
                  "joined_md5); both certificates re-verified by "
                  "verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 cofactor expansion "
                  "of the exact lifted determinant [x^2+y^2,x,y,1]; no solver, verdict cache, or "
                  "repository verifier import); root == child | 1<<bit; sub-roots == loser "
                  "mobility == sweep opponent_legal_replies; consumed union missing/extra 0/0; "
                  "terminal stone range [13,17]; rows sorted-unique; the six-stone parent-lift "
                  "orbits re-derived and the child orbit asserted present; v15 anchor and v16 "
                  "sweep node counts matched to the published crosscheck and sweep audit",
        "sources": {name: {"git_blob_sha": sha} for name, sha in MAIN_BLOBS.items()},
        "certificates": verified,
        "totals": {
            "certificates_audited": len(verified),
            "strategy_rows_sum": sum(v["rows"] for v in verified),
            "visited_states_sum_across_certificates_not_deduplicated":
                sum(v["visited_states_across_subroots"] for v in verified),
            "terminal_count_sum_across_certificates_not_deduplicated":
                sum(v["terminal_count"] for v in verified),
        },
        "frontier_tie_in": {
            "canonical_chain_head": "1195/6652/524884/4922/388607 "
                                    "(class-frontier-cost76a-receipts-recompute-20261115.json, "
                                    "the cost-76a receipts fold completed by this lane)",
            "child_still_remaining_at_head_1195": True,
            "third_class2_target_rows_at_head_1195": {k: v for k, v in rows.items()},
            "third_class2_target_remaining_edge_cost": sum(rows.values()),
            "s6_frontier_contribution": 0,
            "rebase_requirement": "the eventual cost-78a receipt fold must rebase on the 1195 "
                                  "head (not 1188) and assert it before extending; this audit "
                                  "changes no frontier count",
        },
        "unknown_status": {
            "empty_11x11": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
            "class2": "UNKNOWN",
            "class4": "UNKNOWN",
        },
        "interpretation_guard": "WIN7 certificates prove a first-player win within depth 10 from "
                                "the individual seven-stone roots only; they do not close the "
                                "78-legal-move six-stone parent. REFUTED-D10 is not a LOSS proof. "
                                "This audit is independent verification bookkeeping over "
                                "published material and does not determine the game-theoretic "
                                "value of any position.",
    }
    out_path = OUT / "cost78a-published-certificate-replay-20261115.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"written {out_path.name}")
    print(json.dumps(output["totals"], indent=2))

if __name__ == "__main__":
    main()
