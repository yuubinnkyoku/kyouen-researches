#!/usr/bin/env python3
"""Reproduce the public cost-74d certificate replay and S6 parent-lift audit."""
from __future__ import annotations
import hashlib, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUT = EXP / "output"
VERIFY = EXP / "scripts/verify_win7_certificate_bigint_independent.mjs"

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
    inventory = read_json(OUT / "class2-lane-cost74d-certificate-hash-inventory-20261115.json")
    manifest72 = read_json(OUT / "class2-lane-cost72b-win7-certificates-20261115.json")
    frontier = read_json(OUT / "class-frontier-cost74d-receipts-recompute-20261115.json")
    inflight74 = read_json(OUT / "class2-lane-cost74d-inflight-20261115.json")

    bit85 = next(item for item in manifest72["certificates"] if item["bit"] == 85)
    check(bit85["verdict"] == "WIN7", "cost72b bit85 manifest record missing")
    file85 = bit85["storage"]["parts"][0]
    specs = [{
        "lane":"cost72b","bit":85,"root_hex":bit85["root_hex"],"rows":bit85["rows"],
        "mobility":bit85["sub_roots_total"],"bytes":bit85["bytes"],
        "git_blob_sha":bit85["whole_git_blob_sha"],"path":file85["path"]
    }]
    for bit in (12,66,68,118):
        item = next(x for x in inventory["certificates"] if x["bit"] == bit)
        check(item["verdict"] == "WIN7", f"cost74d bit{bit} is not WIN7")
        file_record = next((x for x in item.get("files", [])
                            if x["path"].endswith(".cert") and ".part" not in x["path"]),
                           item.get("whole_file_local"))
        check(file_record is not None and file_record.get("path"), f"bit{bit} certificate file missing")
        specs.append({
            "lane":"cost74d","bit":bit,"root_hex":item["root_hex"],"rows":item["rows"],
            "mobility":item["sub_roots_total"],"bytes":file_record["bytes"],
            "git_blob_sha":file_record["git_blob_sha"],"path":file_record["path"]
        })

    marginal = {h for e in frontier["cost74d_addition"] for h in e.get("marginal_manifest_hexes", [])}
    verified = []
    for spec in specs:
        path = ROOT / spec["path"]
        data = path.read_bytes()
        check(len(data) == spec["bytes"], f"byte count mismatch: bit{spec['bit']}")
        blob = git_blob_sha(data)
        check(blob == spec["git_blob_sha"], f"Git blob SHA mismatch: bit{spec['bit']}")
        run = subprocess.run(["node", str(VERIFY), str(path), str(spec["mobility"])],
                             check=True, capture_output=True, text=True)
        result = json.loads(run.stdout)
        check(result["verdict"] == "WIN7 certificate independently verified", f"verdict: bit{spec['bit']}")
        check(result["root_hex"] == spec["root_hex"], f"root mismatch: bit{spec['bit']}")
        check(result["strategy_rows"] == spec["rows"], f"row count mismatch: bit{spec['bit']}")
        check(result["root_mobility"] == spec["mobility"], f"mobility mismatch: bit{spec['bit']}")
        check(result["root_safe"] and result["rows_sorted_unique"], f"root/row invariant: bit{spec['bit']}")
        check(result["union_missing"] == result["union_extra"] == 0, f"strategy union: bit{spec['bit']}")
        check(result["terminal_range"] == [13,17], f"terminal range: bit{spec['bit']}")
        parents = parent_orbits(spec["root_hex"])
        verified.append({
            "lane":spec["lane"],"bit":spec["bit"],"root_hex":spec["root_hex"],"path":spec["path"],
            "bytes":len(data),"git_blob_sha":blob,"rows":result["strategy_rows"],
            "root_mobility":result["root_mobility"],
            "visited_states_across_subroots":result["visited_states_across_subroots"],
            "winner_states":result["winner_states"],"loser_states":result["loser_states"],
            "loser_reply_edges":result["loser_reply_edges"],"terminal_count":result["terminal_count"],
            "terminal_range":result["terminal_range"],"rows_sorted_unique":result["rows_sorted_unique"],
            "union_missing":result["union_missing"],"union_extra":result["union_extra"],
            "root_safe":result["root_safe"],
            "marginal_manifest_parents":[p for p in parents if p in marginal]
        })

    backed = sorted({p for item in verified for p in item["marginal_manifest_parents"]})
    match = re.search(r"\((\d+)\s*/", frontier["baseline_main"])
    check(match is not None, "could not parse baseline frontier")
    baseline = int(match.group(1))
    receipt_head = frontier["frontier_after_cost74d"]["solved_s6_in_manifest"]
    check(baseline == 1163 and receipt_head == 1179, "frontier chain head mismatch")
    check(len(frontier["cost74d_addition"]) == 15 and len(marginal) == 16, "cost74d receipt union mismatch")
    check(len(backed) == 6, "unexpected certificate-backed parent union")

    root85 = int(bit85["root_hex"],16)
    root91 = int(inflight74["s6_child"],16) | (1 << 91)
    check(transform(root85,5) == root91, "bit85/bit91 D4 transform mismatch")
    check(canonical(root85) == canonical(root91), "bit85/bit91 canonical roots differ")
    check(parent_orbits(bit85["root_hex"]) == parent_orbits(f"{root91:032x}"),
          "bit85/bit91 parent orbit sets differ")
    backed85 = set(verified[0]["marginal_manifest_parents"])
    backed74 = {p for item in verified if item["lane"] == "cost74d"
                for p in item["marginal_manifest_parents"]}
    additional = sorted(backed74 - backed85)
    check(len(additional) == 3, "cost74d public certificates did not add exactly three orbits")

    output = {
        "schema":"n11-cost74d-published-certificate-replay-20261115-v1",
        "date":"2026-11-15",
        "source_main_head":"5a8977f13090f2beddd05353072db652153371bf",
        "verifier":"verify_win7_certificate_bigint_independent.mjs; BigInt 3x3 cofactor expansion; no solver, verdict cache, or repository verifier import",
        "certificates_verified":len(verified),
        "certificates":verified,
        "totals":{
            "strategy_rows_sum":sum(x["rows"] for x in verified),
            "visited_states_sum_across_certificates_not_deduplicated":sum(x["visited_states_across_subroots"] for x in verified),
            "terminal_count_sum_across_certificates_not_deduplicated":sum(x["terminal_count"] for x in verified)
        },
        "d4_cross_cover":{
            "cost72b_bit85_root":bit85["root_hex"],
            "cost74d_bit91_root":f"{root91:032x}",
            "transform_index":5,"coordinate_map":"(x,y)->(x,10-y)",
            "canonical_root_hex":f"{canonical(root85):032x}",
            "same_parent_orbits":True,"bit91_body_published":False
        },
        "frontier":{
            "baseline_s6_manifest_orbits":baseline,"cost74d_receipt_frontier_s6":receipt_head,
            "cost74d_new_manifest_orbits":len(marginal),"certificate_backed_new_s6_orbits":len(backed),
            "cost74d_public_certificates_additional_orbits_beyond_bit85":len(additional),
            "certificate_backed_lower_bound":baseline+len(backed),
            "certificate_backed_new_orbit_hexes":backed,"cost74d_additional_orbit_hexes":additional
        },
        "unknown_status":{
            "empty_11x11":"UNKNOWN","two_stone_roots_49_60_and_59_60":"UNKNOWN",
            "s2_59_60":"UNKNOWN","class2":"UNKNOWN","class4":"UNKNOWN"
        },
        "interpretation_guard":"The receipt frontier 1179 is not a count of independently certificate-backed S6 orbits. This audit establishes a certificate-backed lower bound of 1169 from the prior 1163 baseline. It does not solve the empty 11x11 board or any two-stone root."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
