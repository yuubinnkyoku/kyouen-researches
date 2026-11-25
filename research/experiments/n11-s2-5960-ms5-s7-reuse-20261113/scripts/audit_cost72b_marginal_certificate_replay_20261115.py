#!/usr/bin/env python3
"""Independently replay the nine positive-marginal cost72b WIN7 certificates."""
from __future__ import annotations
import hashlib, json, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUT = EXP / "output"
VERIFY = EXP / "scripts/verify_win7_certificate_bigint_independent.mjs"
BITS = (2, 30, 31, 36, 47, 95, 97, 100, 106)

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def points(mask: int):
    return [p for p in range(121) if (mask >> p) & 1]

def transform_point(point: int, index: int) -> int:
    x, y = point % 11, point // 11
    maps = ((x,y),(y,10-x),(10-x,10-y),(10-y,x),
            (10-x,y),(x,10-y),(y,x),(10-y,10-x))
    tx, ty = maps[index]
    return 11 * ty + tx

def transform(mask: int, index: int) -> int:
    return sum(1 << transform_point(p, index) for p in points(mask))

def canonical(mask: int) -> int:
    return min(transform(mask, index) for index in range(8))

def parent_orbits(root_hex: str):
    root = int(root_hex, 16)
    return sorted({f"{canonical(root ^ (1 << p)):032x}" for p in points(root)})

def main() -> None:
    manifest = read_json(OUT / "class2-lane-cost72b-win7-certificates-20261115.json")
    frontier = read_json(OUT / "class-frontier-cost72b-receipts-recompute-20261115.json")
    prior = read_json(OUT / "cost74d-published-certificate-replay-20261115.json")
    cost74e = read_json(OUT / "class2-lane-cost74e-inflight-20261115.json")
    marginal = {h for e in frontier["cost72b_addition"] for h in e.get("marginal_manifest_hexes", [])}
    check(len(marginal) == 9, "cost72b marginal S6 set is not nine orbits")

    verified = []
    for bit in BITS:
        cert = next(x for x in manifest["certificates"] if x["bit"] == bit)
        check(cert["verdict"] == "WIN7", f"bit{bit} is not WIN7")
        chunks, part_results = [], []
        for part in cert["storage"]["parts"]:
            data = (ROOT / part["path"]).read_bytes()
            check(len(data) == part["bytes"], f"part byte mismatch bit{bit}")
            sha = git_blob_sha(data)
            check(sha == part["git_blob_sha"], f"part Git blob SHA mismatch bit{bit}")
            chunks.append(data)
            part_results.append({"path":part["path"],"bytes":len(data),"git_blob_sha":sha})
        data = b"".join(chunks)
        check(len(data) == cert["bytes"], f"joined byte mismatch bit{bit}")
        whole_sha = git_blob_sha(data)
        check(whole_sha == cert["whole_git_blob_sha"], f"whole Git blob SHA mismatch bit{bit}")
        if cert.get("md5"):
            check(hashlib.md5(data).hexdigest() == cert["md5"], f"MD5 mismatch bit{bit}")
        if cert.get("sha256"):
            check(hashlib.sha256(data).hexdigest() == cert["sha256"], f"SHA256 mismatch bit{bit}")
        with tempfile.NamedTemporaryFile(prefix=f"n11-bit{bit}-", suffix=".cert", delete=False) as tmp:
            tmp.write(data)
            temp_path = Path(tmp.name)
        try:
            run = subprocess.run(["node", str(VERIFY), str(temp_path), str(cert["sub_roots_total"])],
                                 check=True, capture_output=True, text=True)
        finally:
            temp_path.unlink(missing_ok=True)
        result = json.loads(run.stdout)
        check(result["verdict"] == "WIN7 certificate independently verified", f"verdict bit{bit}")
        check(result["root_hex"] == cert["root_hex"], f"root mismatch bit{bit}")
        check(result["strategy_rows"] == cert["rows"], f"row mismatch bit{bit}")
        check(result["root_mobility"] == cert["sub_roots_total"], f"mobility mismatch bit{bit}")
        check(result["root_safe"] and result["rows_sorted_unique"], f"root/row invariant bit{bit}")
        check(result["union_missing"] == result["union_extra"] == 0, f"strategy union bit{bit}")
        check(result["terminal_range"] == [13,17], f"terminal range bit{bit}")
        backed = [p for p in parent_orbits(cert["root_hex"]) if p in marginal]
        check(len(backed) == 1, f"bit{bit} should back exactly one marginal S6 orbit")
        verified.append({
            "bit":bit,"root_hex":cert["root_hex"],"rows":result["strategy_rows"],
            "root_mobility":result["root_mobility"],"bytes":len(data),
            "whole_git_blob_sha":whole_sha,"parts":part_results,
            "visited_states_across_subroots":result["visited_states_across_subroots"],
            "winner_states":result["winner_states"],"loser_states":result["loser_states"],
            "loser_reply_edges":result["loser_reply_edges"],"terminal_count":result["terminal_count"],
            "terminal_range":result["terminal_range"],"rows_sorted_unique":result["rows_sorted_unique"],
            "union_missing":result["union_missing"],"union_extra":result["union_extra"],
            "root_safe":result["root_safe"],"marginal_manifest_parent":backed[0],
        })

    backed = sorted(x["marginal_manifest_parent"] for x in verified)
    check(backed == sorted(marginal), "not every cost72b marginal S6 orbit is certificate-backed")
    prior_lower = prior["frontier"]["certificate_backed_lower_bound"]
    receipt = frontier["frontier_after_cost72b"]
    check(prior_lower == 1169, "prior certificate-backed lower bound changed")
    check(receipt["solved_s6_in_manifest"] == 1188 and receipt["unique_remaining_s6"] == 6659,
          "cost72b receipt head changed")
    zero_bits = [x["bit"] for x in frontier["cost72b_addition"] if not x.get("marginal_manifest_hexes")]
    check(zero_bits == [11,21,66,85], "zero-marginal receipt set changed")
    check(cost74e["status"] == "in-flight" and cost74e["s6_child"] == "00000000000000809142000000000000",
          "cost74e in-flight claim changed")

    output = {
        "schema":"n11-cost72b-marginal-certificate-replay-20261115-v1",
        "date":"2026-11-15",
        "source_main_head":"00a2c4751351fe6e1eff9117ef5c0d3fc1d1730b",
        "verifier":"verify_win7_certificate_bigint_independent.mjs; exact BigInt geometry; no solver or verdict cache",
        "certificates_verified":len(verified),"certificate_bits":list(BITS),"certificates":verified,
        "totals":{
            "strategy_rows_sum":sum(x["rows"] for x in verified),
            "visited_states_sum_across_certificates_not_deduplicated":sum(x["visited_states_across_subroots"] for x in verified),
            "terminal_count_sum_across_certificates_not_deduplicated":sum(x["terminal_count"] for x in verified),
            "published_parts_verified":sum(len(x["parts"]) for x in verified)
        },
        "frontier":{
            "previous_certificate_backed_lower_bound":prior_lower,
            "cost72b_new_manifest_orbits":len(marginal),
            "cost72b_new_orbits_backed_by_independent_certificates":len(backed),
            "certificate_backed_lower_bound":prior_lower+len(backed),
            "receipt_frontier_s6":receipt["solved_s6_in_manifest"],
            "receipt_minus_audited_lower_bound":receipt["solved_s6_in_manifest"]-prior_lower-len(backed),
            "remaining_s6":receipt["unique_remaining_s6"],
            "remaining_s7_edge_cost":receipt["sum_remaining_cost"],
            "open_class_s6_demand":receipt["s6_needed_by_open_classes"],
            "open_class_s7_edge_cost":receipt["cost_needed_by_open_classes"],
            "best_class2_s5":receipt["best_class2"],
            "new_certificate_backed_s6_orbits":backed,
            "zero_marginal_receipt_bits":zero_bits,"all_nine_marginals_backed":True
        },
        "current_inflight_claim":{
            "status":cost74e["status"],"claimed_by":cost74e["claimed_by"],
            "s5_hex":cost74e["s5"],"s6_child_hex":cost74e["s6_child"],
            "edge_cost":cost74e["s6_s7_edge_cost"],"demand":cost74e["demand"],
            "open_parent_count":len(cost74e["open_parents_at_head_1188"])
        },
        "unknown_status":{
            "empty_11x11":"UNKNOWN","two_stone_roots_49_60_and_59_60":"UNKNOWN",
            "s2_59_60":"UNKNOWN","class2":"UNKNOWN","class4":"UNKNOWN"
        },
        "interpretation_guard":"The receipt frontier 1188 is not a count of independently certificate-backed S6 orbits. This audit raises the prior certificate-backed lower bound 1169 to 1178 by verifying all nine positive-marginal cost72b receipts. The remaining gap of ten is not asserted to be unproved; it is outside this audit's certificate set."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
