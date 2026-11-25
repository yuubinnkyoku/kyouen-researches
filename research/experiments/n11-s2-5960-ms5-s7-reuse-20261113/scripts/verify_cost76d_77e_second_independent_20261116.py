#!/usr/bin/env python3
"""Second independent verification of the published cost-76d and cost-77e
sweep artifacts and WIN7-D10 certificates (2026-11-16).

Pure-stdlib, published-files-only verification, run from the experiment
directory (research/experiments/n11-s2-5960-ms5-s7-reuse-20261113). It
re-fetches nothing from the network. It re-reads, for both parallel-lane
sweeps of the second coverable class-2 candidate S5
(00000000000000801202000040000000) at the reconciled canonical head
1405/6443/509457/4713/373180:

cost-76d (child 00000000040000003800080008000000, 76 candidates):
  1. the claim JSON's chain_head_at_claim pins the canonical head 1405
     (blob b3ad19d7..., commit ca0e8c42) and its status/completion record;
  2. the certificate manifest's own pins: sweep-audit git blob sha, both
     published_cert {bytes, md5, sha256, git blob sha} and both
     bareiss-verify {git blob sha} records byte-exact;
  3. the two WIN7 certificates (bits 19/49) re-verified with the published
     BigInt independent verifier (verify_win7_certificate_bigint_independent
     .mjs, no repository engine import): verdict, root hex/stones/safety,
     root mobility vs the manifest root_check loserMobility (55/54),
     strategy rows (44810/33648), sorted-unique, sub-roots (55/54),
     strategy/consumed union 0 missing / 0 extra, terminal range [13,17]
     and terminal counts (15404/11853) vs the manifest; the manifest
     totals (rows 78458 / sub_roots 109 / winner_states 109726 /
     loser_states 32979 / terminal_count 27257) re-summed;
  4. the sweep audit re-derived from the ten raw batch JSONLs (Python
     standard library): 76 distinct candidate bits == the claim's legal
     candidate list == the swept set, WIN bits [19,49], REFUTED-D10 74,
     capped 0, node_sum 96246915, global terminal range [13,17], andclose
     all true, ten pilot_d6 controls loss=false nodes=3402 uncapped;
  5. the v15 cross-engine JSONL (pilot 5949, both WIN bits loss=true) and
     the claim's determinism notes read back;
  6. the legal candidate list independently re-enumerated with the
     published legal_candidates.py (exact Bareiss 4x4 determinants) and
     compared bit-exact to the claim list.

cost-77e (child 00000000040000809002000000004000, 77 candidates):
  1. the claim JSON's chain_head_at_claim pins the canonical head 1405;
  2. both certificates re-assembled from their two published parts and
     checked against the cert receipts: part git blob shas, part bytes,
     whole bytes/md5/sha256;
  3. both consumed winner-state lists re-assembled and checked against
     the receipts (lines/distinct) and the sweep JSON certificate records;
  4. both WIN7 certificates (bits 37/69) re-verified with the published
     BigInt independent verifier and compared record-for-record with the
     published tmp-cost77e bigint.json outputs (byte-equal JSON records);
  5. the sweep aggregate re-derived from the ten raw batch JSONLs: 77
     distinct candidate bits == claim legal list == swept set, WIN bits
     [37,69] with nodes 1819936/2623346, REFUTED-D10 75, capped 0,
     total_nodes 116019458, win_node_sum 4443282, refuted_node_sum
     111576176, heaviest bits [33/110/68/44/31], global terminal range
     [13,17], andclose all, ten pilot_d6 controls;
  6. the v16 determinism rerun JSONL checked node-exact against the
     original batches 4 and 6 (the WIN-containing batches);
  7. the v15 cross-engine JSONL (pilot 5949; bit 0 refuted anchor
     11578726 nodes; WIN bits 37/69 loss=true) read back;
  8. the legal candidate list independently re-enumerated with
     legal_candidates.py and compared bit-exact to the claim list.

The output JSON records every check, the git blob sha of every input
file it read, the full BigInt verifier rerun records, and the verdict.
REFUTED-D10 is NOT a LOSS proof; solved counts are manifest bookkeeping;
the 11x11 empty board, the two-stone roots {49,60}/{59,60}, S2 {59,60},
class 1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
OUT = EXP / "output"

CANON_HEAD = "1405/6443/509457/4713/373180"
CANON_BLOB = "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb"

FAILURES = []


def blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check(label, value):
    if value is not True:
        FAILURES.append(label)
    return value is True


def load_json(path):
    return json.loads(Path(path).read_text())


def load_jsonl(path):
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def rederive_batches(lane, n_batches=10):
    recs, pilots = [], []
    for n in range(1, n_batches + 1):
        for r in load_jsonl(OUT / f"class2-lane-cost{lane}-raw-batch{n}-20261116.jsonl"):
            (pilots if "control" in r else recs).append(r)
    terms = set()
    for r in recs:
        terms.update(r["terminalStoneRange"])
    return {
        "records": recs,
        "pilots": pilots,
        "bits": sorted(r["bit"] for r in recs),
        "win_bits": sorted(r["bit"] for r in recs if r["loss"] is True and not r["capped"]),
        "refuted": sum(1 for r in recs if r["loss"] is False and not r["capped"]),
        "capped": sum(1 for r in recs if r["capped"]),
        "node_sum": sum(r["nodes"] for r in recs),
        "terminal_global_range": [min(terms), max(terms)],
        "andclose_all": all(r["andclose"] is True for r in recs),
        "pilot_all_loss_false_uncapped": all(p["loss"] is False and not p["capped"] for p in pilots),
        "pilot_node_counts": sorted(set(p["nodes"] for p in pilots)),
    }


def run_bigint(cert_path, expected_mobility):
    proc = subprocess.run(
        ["node", str(EXP / "scripts" / "verify_win7_certificate_bigint_independent.mjs"),
         str(cert_path), str(expected_mobility)],
        capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def run_legal_candidates(hexstr):
    proc = subprocess.run(
        ["python3", str(EXP / "scripts" / "legal_candidates.py"), hexstr],
        capture_output=True, text=True, check=True)
    lines = proc.stdout.splitlines()
    return int(lines[0].split()[4]), [int(x) for x in lines[1].split(",")]


def main():
    report = {}

    # ---------- inputs (git blob shas of every file read) ----------
    input_files = [
        "output/class2-lane-cost76d-inflight-20261116.json",
        "output/class2-lane-cost76d-sweep-audit-20261116.json",
        "output/class2-lane-cost76d-win7-certificates-20261116.json",
        "output/class2-lane-cost76d-v15-crosscheck-20261116.jsonl",
        "output/class2-lane-cost77e-inflight-20261116.json",
        "output/class2-lane-cost77e-sweep-20261116.json",
        "output/class2-lane-cost77e-v15-crosscheck-20261116.jsonl",
        "output/class2-lane-cost77e-v16-determinism-rerun-20261116.jsonl",
        "output/tmp-cost77e/bit37.cert-receipt.json",
        "output/tmp-cost77e/bit37.bigint.json",
        "output/tmp-cost77e/bit37.tsverify.json",
        "output/tmp-cost77e/bit69.cert-receipt.json",
        "output/tmp-cost77e/bit69.bigint.json",
        "output/tmp-cost77e/bit69.tsverify.json",
        "output/tmp-cost77e/legal-moves.json",
    ]
    for n in range(1, 11):
        input_files.append(f"output/class2-lane-cost76d-raw-batch{n}-20261116.jsonl")
        input_files.append(f"output/class2-lane-cost77e-raw-batch{n}-20261116.jsonl")
    inputs = {p: blob_sha(EXP / p) for p in input_files}

    # ---------- cost-76d ----------
    claim76 = load_json(EXP / "output/class2-lane-cost76d-inflight-20261116.json")
    audit76 = load_json(EXP / "output/class2-lane-cost76d-sweep-audit-20261116.json")
    man76 = load_json(EXP / "output/class2-lane-cost76d-win7-certificates-20261116.json")

    c76 = {}
    c76["claim_pins_canonical_head_1405"] = check(
        "76d claim baseline", CANON_HEAD in claim76["chain_head_at_claim"]
        and CANON_BLOB in claim76["chain_head_at_claim"])
    c76["claim_status_completed"] = check("76d claim status", claim76["status"] == "completed")
    c76["claim_completion_win_bits"] = check(
        "76d claim completion bits",
        claim76["completion"]["sweep"]["win7_d10_bits"] == [19, 49]
        and claim76["completion"]["sweep"]["node_sum"] == 96246915)
    c76["manifest_pins_sweep_audit_blob"] = check(
        "76d manifest sweep_source pin",
        inputs["output/class2-lane-cost76d-sweep-audit-20261116.json"]
        == man76["sweep_source"]["git_blob_sha"]
        and audit76["sweep_totals"]["candidates"]
        == man76["sweep_source"]["s6_s7_edge_cost"] == 76)

    # certificate manifest pins + BigInt rerun
    bigint76 = {}
    sum_rows = sum_subs = sum_win = sum_lose = sum_term = 0
    for cert in man76["certificates"]:
        bit = cert["bit"]
        pc = cert["published_cert"]
        cert_path = EXP / "output/class2-lane-cost76d-certificates" / pc["path"].split("/")[-1]
        data = cert_path.read_bytes()
        check(f"76d bit{bit} cert blob", blob_sha(cert_path) == pc["git_blob_sha"])
        check(f"76d bit{bit} cert bytes", len(data) == pc["bytes"])
        check(f"76d bit{bit} cert md5", hashlib.md5(data).hexdigest() == pc["md5"])
        check(f"76d bit{bit} cert sha256", hashlib.sha256(data).hexdigest() == pc["sha256"])
        bv = cert["bareiss_verify"]
        bvp = EXP / "output/class2-lane-cost76d-certificates" / bv["path"].split("/")[-1]
        check(f"76d bit{bit} bareiss blob", blob_sha(bvp) == bv["git_blob_sha"])
        check(f"76d bit{bit} bareiss root_check",
              bv["root_check"] == {"stones": 7, "loserMobility": 55 if bit == 19 else 54})
        rec = run_bigint(cert_path, bv["root_check"]["loserMobility"])
        bigint76[str(bit)] = rec
        check(f"76d bit{bit} bigint verdict", rec["verdict"] == "WIN7 certificate independently verified")
        check(f"76d bit{bit} bigint root", rec["root_hex"] == cert["root_hex"]
              and rec["root_stones"] == 7 and rec["root_safe"] is True
              and rec["root_mobility"] == bv["root_check"]["loserMobility"])
        check(f"76d bit{bit} bigint rows", rec["strategy_rows"] == cert["rows"]
              and rec["rows_sorted_unique"] is True)
        check(f"76d bit{bit} bigint subroots", rec["subroots_passed"] == cert["sub_roots"])
        check(f"76d bit{bit} bigint union", rec["union_missing"] == 0 and rec["union_extra"] == 0)
        check(f"76d bit{bit} bigint terminal",
              rec["terminal_range"] == cert["terminal_range"] == [13, 17]
              and rec["terminal_count"] == cert["terminal_count"])
        sum_rows += rec["strategy_rows"]; sum_subs += rec["subroots_passed"]
        sum_win += rec["winner_states"]; sum_lose += rec["loser_states"]; sum_term += rec["terminal_count"]
    tot = man76["totals"]
    c76["bigint_rerun_reproduces_manifest_totals"] = check(
        "76d totals", (sum_rows, sum_subs, sum_win, sum_lose, sum_term)
        == (tot["rows"], tot["sub_roots"], tot["winner_states"], tot["loser_states"], tot["terminal_count"]))

    # sweep re-derivation from raw batches
    d76 = rederive_batches("76d")
    st = audit76["sweep_totals"]
    c76["sweep_rederivation"] = {
        "candidates": check("76d candidates", d76["bits"] and len(d76["bits"]) == len(set(d76["bits"])) == 76),
        "bits_equal_claim_legal_list": check("76d bits == claim legal", d76["bits"] == claim76["legal_candidates"]),
        "win_bits": check("76d win bits", d76["win_bits"] == st["win7_d10_bits"] == [19, 49]),
        "refuted": check("76d refuted", d76["refuted"] == st["refuted_d10_count"] == 74),
        "capped": check("76d capped", d76["capped"] == st["capped_count"] == 0),
        "node_sum": check("76d node sum", d76["node_sum"] == st["node_sum"] == 96246915),
        "terminal_range": check("76d terminal", d76["terminal_global_range"] == st["terminal_stone_range_all"] == [13, 17]),
        "andclose": check("76d andclose", d76["andclose_all"] is True and st["andclose_all"] is True),
        "pilots": check("76d pilots", len(d76["pilots"]) == 10
                        and d76["pilot_node_counts"] == [3402]
                        and d76["pilot_all_loss_false_uncapped"] is True),
    }

    # v15 crosscheck + determinism notes
    v15_76 = load_jsonl(EXP / "output/class2-lane-cost76d-v15-crosscheck-20261116.jsonl")
    v15_bits = {r["bit"]: r for r in v15_76 if "control" not in r}
    v15_pilot = [r for r in v15_76 if "control" in r]
    c76["v15_crosscheck"] = check(
        "76d v15", len(v15_pilot) == 1 and v15_pilot[0]["nodes"] == 5949
        and all(v15_bits[b]["loss"] is True and not v15_bits[b]["capped"] for b in (19, 49))
        and audit76["v15_crosscheck"]["win_bits_loss_true"] == [19, 49])
    c76["determinism_notes_published"] = [
        o["batch"] for o in audit76["determinism_observations"] if o["node_exact_rerun"]
    ] == [3, 5]

    # legal candidate re-enumeration
    n_legal76, legal76 = run_legal_candidates(claim76["s6_child"])
    c76["legal_candidates_reenumerated"] = check(
        "76d legal renum", n_legal76 == 76 and legal76 == claim76["legal_candidates"])
    report["cost76d"] = c76
    report["cost76d_bigint_rerun"] = bigint76

    # ---------- cost-77e ----------
    claim77 = load_json(EXP / "output/class2-lane-cost77e-inflight-20261116.json")
    sweep77 = load_json(EXP / "output/class2-lane-cost77e-sweep-20261116.json")

    c77 = {}
    c77["claim_pins_canonical_head_1405"] = check(
        "77e claim baseline", CANON_HEAD in claim77["chain_head_at_claim"]
        and CANON_BLOB in claim77["chain_head_at_claim"])
    c77["sweep_record_pins_head_1405"] = check(
        "77e sweep head", sweep77["chain_head_at_claim"] == CANON_HEAD)

    certs77 = {}
    for bit, root, mobility in ((37, "00000000040000809002002000004000", 57),
                                (69, "00000000040000a09002000000004000", 57)):
        rec = load_json(EXP / f"output/tmp-cost77e/bit{bit}.cert-receipt.json")
        p1 = (OUT / "class2-lane-cost77e-certificates" / f"bit{bit}-root-{root}.cert.part1of2").read_bytes()
        p2 = (OUT / "class2-lane-cost77e-certificates" / f"bit{bit}-root-{root}.cert.part2of2").read_bytes()
        whole = p1 + p2
        cert_dir = Path("/tmp") / "cost77e-second-independent-verification"
        cert_dir.mkdir(parents=True, exist_ok=True)
        whole_path = cert_dir / f"bit{bit}-whole.cert"
        whole_path.write_bytes(whole)
        c1 = (OUT / f"tmp-cost77e/bit{bit}.consumed.txt.part1of2").read_bytes()
        c2 = (OUT / f"tmp-cost77e/bit{bit}.consumed.txt.part2of2").read_bytes()
        consumed = (c1 + c2).decode().splitlines()
        checks = {
            "root_hex": rec["root_hex"] == root,
            "part1_blob": blob_sha_bytes(p1) == rec["parts"][0]["git_blob_sha"] and len(p1) == rec["parts"][0]["bytes"],
            "part2_blob": blob_sha_bytes(p2) == rec["parts"][1]["git_blob_sha"] and len(p2) == rec["parts"][1]["bytes"],
            "whole_bytes": len(whole) == rec["whole_bytes"],
            "whole_md5": hashlib.md5(whole).hexdigest() == rec["whole_md5"],
            "whole_sha256": hashlib.sha256(whole).hexdigest() == rec["whole_sha256"],
            "consumed_lines": len(consumed) == rec["consumed_lines"],
            "consumed_distinct": len(set(consumed)) == rec["consumed_distinct"],
        }
        rerun = run_bigint(whole_path, mobility)
        pub = load_json(EXP / f"output/tmp-cost77e/bit{bit}.bigint.json")
        checks["bigint_rerun_record_equals_published"] = rerun == pub
        sweepcert = sweep77["certificates"][f"bit{bit}"]
        checks["sweep_record_crosscheck"] = (
            rec["whole_md5"] == sweepcert["md5"] and rec["whole_bytes"] == sweepcert["bytes"]
            and rec["consumed_distinct"] == sweepcert["rows"]
            and rerun["strategy_rows"] == sweepcert["rows"])
        for k, v in checks.items():
            check(f"77e bit{bit} {k}", v)
        certs77[str(bit)] = {"checks": checks, "bigint_rerun": rerun}
    c77["certificates"] = certs77

    # sweep aggregate re-derivation
    d77 = rederive_batches("77e")
    agg = sweep77["aggregate"]
    recs77 = {}
    for r in d77["records"]:
        recs77[r["bit"]] = r
    heaviest = sorted(((r["bit"], r["nodes"]) for r in d77["records"]), key=lambda t: -t[1])[:5]
    c77["sweep_rederivation"] = {
        "candidates": check("77e candidates", len(d77["bits"]) == len(set(d77["bits"])) == 77),
        "bits_equal_claim_legal_list": check("77e bits == claim legal", d77["bits"] == claim77["legal_candidates"]),
        "win_bits": check("77e win bits", d77["win_bits"] == agg["win7_d10_bits"] == [37, 69]),
        "win_bit_nodes": check("77e win nodes",
                               {str(b): recs77[b]["nodes"] for b in (37, 69)} == agg["win7_d10_nodes"]),
        "refuted": check("77e refuted", d77["refuted"] == agg["refuted_d10"] == 75),
        "capped": check("77e capped", d77["capped"] == agg["capped"] == 0),
        "total_nodes": check("77e nodes", d77["node_sum"] == agg["total_nodes"] == 116019458),
        "win_node_sum": check("77e win sum", sum(recs77[b]["nodes"] for b in (37, 69)) == agg["win_node_sum"]),
        "refuted_node_sum": check("77e refuted sum",
                                  sum(r["nodes"] for r in d77["records"] if r["loss"] is False) == agg["refuted_node_sum"]),
        "heaviest_bits": check("77e heaviest", heaviest == [tuple(x) for x in agg["heaviest_bits"]]),
        "terminal_range": check("77e terminal", d77["terminal_global_range"] == agg["terminal_range_all"] == [13, 17]),
        "andclose": check("77e andclose", d77["andclose_all"] is True and agg["andclose_all"] is True),
        "pilots": check("77e pilots", len(d77["pilots"]) == 10 and d77["pilot_node_counts"] == [3402]
                        and d77["pilot_all_loss_false_uncapped"] is True and agg["pilots_3402"] == 10),
    }

    # determinism rerun: batches 4 and 6 node-exact (WIN-containing batches)
    rerun_recs = [r for r in load_jsonl(EXP / "output/class2-lane-cost77e-v16-determinism-rerun-20261116.jsonl")
                  if "control" not in r]
    det_ok = True
    for bn in (4, 6):
        orig = {r["bit"]: r for r in load_jsonl(OUT / f"class2-lane-cost77e-raw-batch{bn}-20261116.jsonl")
                if "control" not in r}
        rr = [r for r in rerun_recs if r["bit"] in orig]
        if not (len(rr) == len(orig) and all(
                orig[r["bit"]]["nodes"] == r["nodes"] and orig[r["bit"]]["loss"] == r["loss"]
                and orig[r["bit"]]["capped"] == r["capped"]
                and orig[r["bit"]]["terminalStoneRange"] == r["terminalStoneRange"] for r in rr)):
            det_ok = False
    c77["determinism_rerun_batches_4_6_node_exact"] = check("77e determinism", det_ok)
    win_batches = sorted({n for n in range(1, 11)
                          if any(r.get("bit") in (37, 69) for r in load_jsonl(
                              OUT / f"class2-lane-cost77e-raw-batch{n}-20261116.jsonl"))})
    c77["determinism_rerun_covers_win_batches"] = check("77e det win batches", win_batches == [4, 6])

    # v15 crosscheck
    v15_77 = load_jsonl(EXP / "output/class2-lane-cost77e-v15-crosscheck-20261116.jsonl")
    v15_bits77 = {r["bit"]: r for r in v15_77 if "control" not in r}
    v15_pilot77 = [r for r in v15_77 if "control" in r]
    c77["v15_crosscheck"] = check(
        "77e v15", len(v15_pilot77) == 1 and v15_pilot77[0]["nodes"] == 5949
        and v15_bits77[0]["loss"] is False and v15_bits77[0]["nodes"] == 11578726
        and all(v15_bits77[b]["loss"] is True and not v15_bits77[b]["capped"] for b in (37, 69)))

    # legal candidate re-enumeration
    n_legal77, legal77 = run_legal_candidates(claim77["s6_child"])
    c77["legal_candidates_reenumerated"] = check(
        "77e legal renum", n_legal77 == 77 and legal77 == claim77["legal_candidates"])
    report["cost77e"] = c77

    # ---------- cross-lane facts ----------
    report["cross_lane_facts"] = {
        "both_claims_base_on_canonical_head_1405": (
            c76["claim_pins_canonical_head_1405"] and c77["claim_pins_canonical_head_1405"]),
        "stale_baseline_quote": "none observed: both 76d and 77e quote the reconciled canonical head 1405 (blob b3ad19d7..., commit ca0e8c42) directly",
        "fold_status_at_record_time": "both receipt folds onto 1405 PENDING on main at this record's publication; this verification covers the published sweep and certificate artifacts only",
        "claim77_status_note": "the 77e claim JSON on main is still status=in-flight at this record's publication (the sweep record class2-lane-cost77e-sweep-20261116.json and its certificates are the publication of the completed sweep)",
    }

    report["schema"] = "n11-class2-lane-cost76d-77e-second-independent-verification-20261116-v1"
    report["date"] = "2026-11-16"
    report["verified_by"] = "n11 long-term class2 lane (published chain-roots audit v12 round)"
    report["inputs_git_blob_shas"] = inputs
    report["method"] = ("pure-stdlib re-derivation from the published raw batch JSONLs, claims, sweep records, "
                        "certificate manifests/receipts, consumed winner-state lists and re-assembled whole "
                        "certificates; the published BigInt independent verifier "
                        "(verify_win7_certificate_bigint_independent.mjs, node) re-run on all four WIN7-D10 "
                        "certificates; the published legal_candidates.py (exact Bareiss 4x4 determinants) "
                        "re-enumerated for both children")
    report["verdict"] = "VERIFICATION PASSED" if not FAILURES else "VERIFICATION FAILED"
    report["failures"] = FAILURES
    report["verdict_semantics"] = ("loss=true => WIN7-within-depth-10 for that 7-stone root (certified); "
                                   "loss=false && !capped => REFUTED-D10, no first-player win within depth 10 "
                                   "(NOT a LOSS proof); capped proves nothing either way")
    report["unknown_status"] = ("11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, "
                                "class 2 and class 4: UNKNOWN; solved 1405 is manifest-coverage bookkeeping")

    dest = OUT / "class2-lane-cost76d-77e-second-independent-verification-20261116.json"
    dest.write_text(json.dumps(report, indent=1, sort_keys=False) + "\n")
    print("verdict:", report["verdict"])
    print("failures:", FAILURES if FAILURES else "none")
    print("wrote:", dest.relative_to(EXP))


def blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


if __name__ == "__main__":
    main()
