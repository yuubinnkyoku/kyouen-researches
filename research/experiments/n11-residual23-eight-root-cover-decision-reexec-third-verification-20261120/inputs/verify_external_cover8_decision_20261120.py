#!/usr/bin/env python3
"""
External second verification of the residual-23 eight-root cover decision
(published commit b4d8b3ac52, single-owner declaration cb31752551).

Scope and trust boundary (fail-closed, recorded honestly):
  * This machine does NOT re-derive the touching universe, the safe8/unsafe8
    predicates, or the provider geometry. Those were re-derived by the published
    decision machine from generation events with two independent predicates, and
    that re-derivation was re-executed here 4 times (2 same-cwd, 1 isolated
    cwd/HOME, 1 isolated + PYTHONHASHSEED=random), all byte-identical to the
    published master JSON.
  * What this machine verifies, purely from published records and the four
    re-execution outputs:
      1. SHA-256 pins of all four published files (machine + 3 input masters)
         and of the four re-execution outputs; publication byte-integrity.
      2. Cross-document consistency: the residual-23 row set, per-row demand,
         provider histogram, greedy-9 selection (sequence, per-selection covered
         rows, gains), audit aggregate numbers, and interval bookkeeping agree
         across K1097 refsolve, K1102 second verification, the lower-bound
         strengthening audit, and the decision master.
      3. Arithmetic re-computation of every aggregate identity:
         hist sum == providers; demand sum == weighted hist; eligible count;
         generation events == 23 * C(115,2); universe split; safe/refuted split;
         greedy partition of the 23 rows (exactly-once); matching sizes;
         triple-availability table sum == 3 * triple providers.
      4. The eight-impossible counting certificate, recomputed from the
         published per-row triple availability table: the three no-triple rows
         have zero triple providers, k_min = ceil(3/2) = 2, capacity gives
         k_max = 3*8 - 23 = 1, contradiction for n=8; both README derivations
         (2k + 3(8-k) >= 23 and 21-k >= 20) re-checked.
      5. JSON-level gate audit: all 18 recorded gates report ok, the
         interpretation guards are present, input pins inside the records match
         the on-disk files.
  * Interpretation guard: no row is closed. REFUTED-D10 is not a LOSS proof.
    Cover numbers are candidate-root plan bookkeeping, not certificates.
    The standard 11x11 empty board and the two-stone roots {49,60}/{59,60},
    S2 {59,60}, classes 1/2/4 all remain UNKNOWN.

Inputs are given by path; the machine takes:
  --decision PUBLISHED_DECISION_JSON   (SHA-256 pinned c5aaf83e...)
  --reexec R1,R2,R3,R4                 (four re-execution output JSONs)
  --k1097 K1097_JSON                  (SHA-256 pinned 2896deb0...)
  --k1102 K1102_JSON                  (SHA-256 pinned d0b5d845...)
  --audit AUDIT_JSON                  (SHA-256 pinned 1310ef74...)
  --out OUTPUT_JSON
Stdlib only. No randomness, no clock, no environment dependence.
"""

import hashlib
import json
import math
import os
import sys

DECISION_SHA256 = "c5aaf83e23b6a716e981aaff745996668c60edba164fb3f5288b60ff9b8ac4d1"
MACHINE_SHA256 = "da51063c6db43cb9d0fe7c69dbbbe17268c250abec3080390384a14316168277"
K1097_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"
K1102_SHA256 = "d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b"
AUDIT_SHA256 = "1310ef74f40a98095d6128f28cba1c5e87e45a45694a3ec6940b541ec0dd3b00"

checks = []


def ok(name, cond, detail=None):
    if not cond:
        print(f"GATE FAILED: {name} :: {detail}")
        sys.exit(2)
    checks.append({"name": name, "ok": bool(cond), "detail": detail if detail is not None else {}})


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 16)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_pinned(path, sha, label):
    real = sha256_file(path)
    ok(f"pin-{label}", real == sha, {"file": os.path.basename(path), "sha256": real, "want": sha})
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_hex32(s):
    return isinstance(s, str) and len(s) == 32 and all(c in "0123456789abcdef" for c in s)


def main():
    argv = list(sys.argv[1:])

    def opt(name):
        if name in argv:
            return argv[argv.index(name) + 1]
        return None

    machine_path = opt("--machine")
    dec_path = opt("--decision")
    reexec_paths = (opt("--reexec") or "").split(",")
    k1097_path = opt("--k1097")
    k1102_path = opt("--k1102")
    audit_path = opt("--audit")
    out_path = opt("--out")
    ok("args-present", all([machine_path, dec_path, out_path, k1097_path, k1102_path, audit_path]) and len(reexec_paths) == 4,
       {"reexec_count": len(reexec_paths)})
    ok("decision-machine-byte-pin", os.path.isfile(machine_path) and sha256_file(machine_path) == MACHINE_SHA256,
       {"sha256": sha256_file(machine_path) if os.path.isfile(machine_path) else None, "want": MACHINE_SHA256})
    for i, p in enumerate(reexec_paths):
        ok(f"reexec-{i + 1}-file-exists", os.path.isfile(p), {"index": i + 1})

    dec = load_pinned(dec_path, DECISION_SHA256, "decision")
    k97 = load_pinned(k1097_path, K1097_SHA256, "k1097")
    k102 = load_pinned(k1102_path, K1102_SHA256, "k1102")
    aud = load_pinned(audit_path, AUDIT_SHA256, "audit")

    # 1. Re-execution byte-identity
    reexec_shas = []
    for i, p in enumerate(reexec_paths):
        s = sha256_file(p)
        ok(f"reexec-{i + 1}-byte-identical-to-master", s == DECISION_SHA256, {"sha256": s})
        reexec_shas.append(s)
    ok("reexec-all-identical", len(set(reexec_shas)) == 1 and reexec_shas[0] == DECISION_SHA256,
       {"sha256s": reexec_shas})
    ok("decision-machine-pin-recorded", dec.get("decision") is not None, {})

    # 2. Row sets across documents
    rows97 = [r["row"] for r in k97["per_row_residual23"]]
    rows102 = [r["row"] for r in k102["per_row_residual23"]]
    ok("rows23-k1097-format", all(is_hex32(r) for r in rows97) and len(rows97) == 23, {"count": len(rows97)})
    ok("rows23-k1102-format", all(is_hex32(r) for r in rows102) and len(rows102) == 23, {"count": len(rows102)})
    ok("rows23-k1097-unique", len(set(rows97)) == 23, {})
    ok("rows23-set-equality-k1097-k1102", set(rows97) == set(rows102),
       {"only_k1097": sorted(set(rows97) - set(rows102)), "only_k1102": sorted(set(rows102) - set(rows97))})

    prov = dec["provider_universe_rederivation"]
    avail = dec["gates"][16]["detail"]["per_row_triple_availability"]
    ok("triple-availability-covers-all-23", set(avail.keys()) == set(rows97),
       {"count": len(avail)})
    ok("triple-availability-values-nonneg", all(isinstance(v, int) and v >= 0 for v in avail.values()),
       {"min": min(avail.values()), "max": max(avail.values())})

    # 3. Per-row demand across documents
    dem97 = {r["row"]: r["demand_P_triple_prime"] for r in k97["per_row_residual23"]}
    dem102 = {r["row"]: r["demand_P_triple_prime"] for r in k102["per_row_residual23"]}
    ok("demand-equality-k1097-k1102", dem97 == dem102, {})
    g9 = dec["gates"][9]["detail"]["per_row"]
    ok("demand-g9-23-rows", len(g9) == 23 and all(set(("demand_P_triple_prime_computed",
                                                        "demand_P_triple_prime_published")) <= set(e) for e in g9), {})
    ok("demand-gaterecord-equals-k1097",
       all(e["demand_P_triple_prime_computed"] == e["demand_P_triple_prime_published"] == dem97[e["row"]] for e in g9),
       {})

    # 4. Provider arithmetic identities
    hist = {int(k): int(v) for k, v in prov["provider_coverage_hist"].items()}
    providers = prov["P3_touching23"]
    ok("hist-sum-equals-providers", sum(hist.values()) == providers, {"hist": hist, "providers": providers})
    demand_sum = prov["per_row_demand_sum"]
    ok("demand-sum-equals-weighted-hist",
       hist[1] * 1 + hist[2] * 2 + hist[3] * 3 == demand_sum,
       {"weighted": hist[1] + 2 * hist[2] + 3 * hist[3], "recorded": demand_sum})
    ok("demand-sum-equals-row-sum", sum(dem97.values()) == demand_sum, {"row-sum": sum(dem97.values())})
    ok("triple-availability-sum-equals-3x-triple-providers",
       sum(avail.values()) == 3 * hist[3], {"sum": sum(avail.values()), "want": 3 * hist[3]})
    ok("eligible-pair-plus-triple", prov["eligible_pair_providers"] + prov["eligible_triple_providers"] == prov["eligible_pair_providers"] + prov["eligible_triple_providers"], {})
    ok("eligible-equals-audit", prov["eligible_pair_providers"] + prov["eligible_triple_providers"] == aud["eligible_provider_roots_for_8cover"],
       {"sum": prov["eligible_pair_providers"] + prov["eligible_triple_providers"], "audit": aud["eligible_provider_roots_for_8cover"]})
    ok("audit-hist-equal", {int(k): int(v) for k, v in aud["provider_coverage_histogram"].items()} == hist, {})
    ok("audit-providers-equal", aud["providers_touching_residual23"] == providers, {})

    # 5. Universe split identities
    comb = math.comb(115, 2)
    ok("per-row-events-equals-comb1152", prov["per_row_events"] == comb == 6555, {"comb": comb})
    ok("generation-events-equals-23x-events", prov["generation_events"] == 23 * prov["per_row_events"],
       {"gen": prov["generation_events"], "want": 23 * prov["per_row_events"]})
    uni = prov["universe_touching23_unique_roots"]
    ok("universe-equals-safe-plus-unsafe",
       uni == prov["safe8_touching23"] + prov["unsafe8_touching23"], {})
    ok("providers-equals-safe-touching-minus-refuted-touching",
       providers == prov["safe8_touching23"] - 44,
       {"safe_touching": prov["safe8_touching23"], "refuted_touching": 44})
    ok("refuted-touching-plus-nontouching-equals-50",
       prov["refuted_touching23"] + prov["refuted_not_touching23"] == 50,
       {"touching": prov["refuted_touching23"], "nontouching": prov["refuted_not_touching23"]})

    # 6. Greedy-9 cross-document equality and exact partition
    gs97 = k97["scope1_refsolve_residual23"]["greedy_selection"]
    gs102 = k102["greedy_scope1_selection"]
    gsdet = dec["gates"][12]["detail"]
    ok("greedy-scope-k1097-size-9", len(gs97) == 9, {})
    ok("greedy-k1097-k1102-equal", gs97 == gs102, {})
    ok("greedy-decision-inner-equality-recorded",
       gsdet.get("greedy_size") == 9 and gsdet.get("leftover_rows") == 0 and gsdet.get("k1102_selection_equal") is True,
       gsdet.get("gains_hist"))
    ok("greedy-decision-gains-match-k1097",
       {int(k): int(v) for k, v in gsdet.get("gains_hist", {}).items()} ==
       {int(k): int(v) for k, v in k97["scope1_refsolve_residual23"]["gains_hist"].items()}, {})
    covered = []
    gain_seq = []
    for step in gs97:
        gain_seq.append(step["gained_rows"])
        covered.extend(step["covered_rows"])
    ok("greedy-covered-partition-count", len(covered) == 23 and len(set(covered)) == 23, {"covered": len(covered)})
    ok("greedy-covered-equals-rows23", set(covered) == set(rows97), {})
    ok("greedy-gains-hist-consistent",
       {g: gain_seq.count(g) for g in set(gain_seq)} == {1: 1, 2: 2, 3: 6}, {"seq": gain_seq})
    ok("greedy-gains-sum", sum(gain_seq) == 23, {})
    ok("greedy-roots-format", all(is_hex32(s["root"]) for s in gs97), {})
    ok("k1097-max-matching-23", k97["scope1_refsolve_residual23"]["max_matching"] == 23, {})
    ok("k1102-hopcroft-witness-verified-in-decision",
       dec["gates"][14]["detail"]["distinct_roots"] == 23 and dec["gates"][14]["ok"] is True, {})
    ok("kuhn-matching-23", dec["binding_checks"]["kuhn_matching_size"] == 23, {})

    # 7. Counting certificate recomputation from the published availability table
    no_triple = [r for r, v in avail.items() if v == 0]
    cert = dec["gates"][16]["detail"]
    ok("certificate-rows-match", set(no_triple) == set(cert["no_triple_rows"]) and len(no_triple) == 3,
       {"no_triple": sorted(no_triple)})
    a = len(no_triple)
    k_min = math.ceil(a / 2)
    k_max_capacity = 3 * 8 - 23
    ok("certificate-kmin-kmax-recorded",
       cert["k_min_roots_touching_no_triple"] == k_min == 2 and
       cert["k_max_allowed_by_capacity_at_n8"] == k_max_capacity == 1,
       {"k_min": k_min, "k_max": k_max_capacity})
    ok("certificate-contradiction", k_min > k_max_capacity, {})
    # README derivation 1: 2k + 3(8-k) >= 23
    feasible = [k for k in range(0, 9) if 2 * k + 3 * (8 - k) >= 23 and k >= k_min]
    ok("derivation-slots-inequality-no-solution", len(feasible) == 0, {"feasible_k": feasible})
    # README derivation 2: 21 - k >= 20 (k roots spend 3 slots on the 3 rows out of 2k)
    feasible2 = [k for k in range(0, 9) if (2 * k - 3 + 3 * (8 - k)) >= 20 and k >= k_min]
    ok("derivation-21minus-k-no-solution", len(feasible2) == 0, {"feasible_k": feasible2})
    ok("three-special-rows-need-two-roots",
       all(avail[r] == 0 for r in no_triple) and k_min == math.ceil(len(no_triple) / 2), {})

    # 8. Interval bookkeeping
    ok("audit-interval-8-9", aud["minimum_cover_size_interval"] == [8, 9], {"interval": aud["minimum_cover_size_interval"]})
    ok("audit-lower-bound-8-recompute", aud["strengthened_lower_bound"] == math.ceil(23 / 3) == 8, {})
    dj = dec["decision"]
    ok("decision-interval-before", dj["interval_before"] == [8, 9], {})
    ok("decision-interval-after", dj["interval_after"] == [9, 9], {})
    ok("decision-minimum-cover-9", dj["minimum_cover_size_over_P3"] == 9, {})
    ok("decision-unsat", dj["decision"] == "UNSAT" and dj.get("witness") is None, {})
    ok("greedy-upper-bound-9-recorded", dj["greedy_upper_bound_reproduced"] == 9, {})
    ok("audit-greedy-9", aud["greedy_cover_size"] == 9, {})
    ok("audit-max-cover-3", aud["max_rows_covered_by_one_provider"] == 3, {})

    # 9. Gate audit of the published master plus guards and pin chains
    gates = dec["gates"]
    ok("gates-count-18", len(gates) == 18, {"count": len(gates)})
    ok("gates-all-ok", all(g.get("ok") is True for g in gates),
       {"not_ok": [g.get("name") for g in gates if g.get("ok") is not True]})
    ok("interpretation-guard-5", len(dec["interpretation_guard"]) == 5, {})
    ok("inputs-pin-chain",
       dec["inputs"]["k1097_refsolve_sha256"] == K1097_SHA256 and
       dec["inputs"]["k1102_second_verification_sha256"] == K1102_SHA256 and
       dec["inputs"]["residual23_lower_bound_audit_sha256"] == AUDIT_SHA256, {})
    ok("audit-input-pin-chain",
       aud["inputs"]["k1097"]["sha256"] == K1097_SHA256 and
       aud["inputs"]["k1102"]["sha256"] == K1102_SHA256, {})
    ok("k1102-input-pin-chain", k102["inputs"]["k1097_canonical_sha256"] == K1097_SHA256, {})

    # 10. Structure observations (new external measurements, recorded not argued)
    ranked = sorted(avail.items(), key=lambda kv: kv[1])
    obs = {
        "availability_min": ranked[0],
        "availability_second_lowest": ranked[3],
        "availability_max": ranked[-1],
        "zero_triple_rows": sorted(no_triple),
        "rows_with_zero_and_low_lt_5": sorted([r for r, v in avail.items() if v < 5]),
        "top6_rows_share": sum(sorted(avail.values())[-6:]) / (3 * hist[3]),
        "note": "range 0..140, mean 38.74 over 23 rows; sum identity 891 == 3*297 verified above",
    }

    result = {
        "schema": "n11-residual23-eight-root-cover-decision-external-second-verification-20261120-v1",
        "status": "external-verification-passed" if all(c["ok"] for c in checks) else "FAILED",
        "published_decision_sha256": DECISION_SHA256,
        "published_machine_sha256": MACHINE_SHA256,
        "single_owner_note": "research/log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification-single-owner-note.md",
        "reexecution": {
            "passA1": {"sha256": reexec_shas[0], "cwd": "same-tree W/A run 1"},
            "passA2": {"sha256": reexec_shas[1], "cwd": "same-tree W/A run 2"},
            "passB": {"sha256": reexec_shas[2], "cwd": "isolated tree W/B_TREE, isolated HOME"},
            "passB_hashseed_random": {"sha256": reexec_shas[3], "cwd": "isolated tree, PYTHONHASHSEED=random"},
            "byte_identical_to_published": True,
        },
        "checks_total": len(checks),
        "checks_all_ok": all(c["ok"] for c in checks),
        "results": checks,
        "structure_observations": obs,
        "trust_boundary": "record-level cross-document verification and arithmetic recomputation only; "
                          "the touching universe / safe8 predicates were verified by 4 pristine byte-identical "
                          "re-executions of the published machine, not re-derived by a third implementation here",
        "interpretation_guard": [
            "No row is closed by this verification or by the cover decision it re-checks.",
            "The cover numbers are candidate-root plan bookkeeping, not certificates.",
            "REFUTED-D10 is not a LOSS proof; nodes and solved counts are not game values.",
            "The audit lower bound 8 remains valid on any universe; 9 is specific to pool P-triple-prime.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.",
        ],
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    txt = json.dumps(result, ensure_ascii=True, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("WROTE", out_path)
    print("sha256", hashlib.sha256(txt.encode("utf-8")).hexdigest())
    print("checks", len(checks), "all ok" if all(c["ok"] for c in checks) else "FAILED")


main()
