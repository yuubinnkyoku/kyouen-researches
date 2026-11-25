#!/usr/bin/env python3
"""Independent whole-record second verification of K1075 (residual-72 full cache-join
candidate supply): probe-corpus, value-identity and chain-numerics routes.

Single-owner experiment declared in
research/log/2026-11-20-n11-candidate-supply-whole-record-second-verification-single-owner-note.md.

A complementary geometry lane has already published (research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/candidate-supply-second-verification-20261120.json, 44 gates: independent D4/Bareiss re-derivation of the witness/retired geometry). This machine is deliberately non-overlapping in method: it re-derives the same record through published-record identity routes that geometry cannot cover (raw probe corpus rebuild, resolve6 value identities, dead-sweep rebuild, fold-chain numerics, cross-lane consistency with the 76-gate resolve7 second verification).

Verification target:
  K1075 record  research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json
  SHA-256 49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa (25 checks, all PASS)

This machine consumes the published records the K1075 run consumed, plus raw worker
probe records, and re-derives the determinations by independent routes:

  route A  K1069 live-sweep classification rebuilt from the raw 4-worker probe records
           (probe-records-w{0..3}.jsonl) with a fresh dedup/agreement implementation,
           instead of trusting sweep39.classification; node statistics rebuilt from the
           deduplicated corpus. Additionally the K1059 dead-sweep REFUTED verdicts are
           rebuilt from the per-record probe_runs of sweep39dead itself.
  route B  the fold-chain bookkeeping: rows78 -> fold9 -4 rows -> fold10 -2 rows -> 72,
           via set arithmetic per link against resolve5/resolve6/fold9/fold10 records
           and the published frontier numerics of fold10.
  route C  the join statistics: stage-1 reproduction identity against the published
           resolve6 verdict_join (stats and universe hits field-by-field) and the
           exact +38 refuted / +1 win / judged 7532 delta arithmetic of the 39-root
           live sweep, plus universe size identities for both universes.
  route D  the phase-2 candidate-supply anatomy: row_demand re-aggregation for all 72
           rows, exact one-cover of the residual by the fresh-safe pool and by the
           36-root witness, the maximum-matching-36 proof from the record alone
           (36 disjoint 2-row pairs cover all 72 rows, and no matching on 72 rows can
           exceed 36 pairs), witness-root disjointness from every judged/retired/dead
           set, and cross-agreement with the resolve7 record and the independent
           resolve7 second verification.

Honest trust boundary (stated in the output record): the root-level universe lists
(the 7969/7448 universes and the 4109-root fresh pool) are not published in any
pinned record; per-root pool membership, pair_edges=536, greedy_set_cover_size=40,
singleton eligibility and universe-intersection counts (dead39_in_universe72=37,
live38_in_universe72=38) are therefore not recomputable from records alone and are
recorded as K1075-internal claims, not as second-verification gates.

The machine performs no search, judges no root, closes no row, and does not rebuild
the candidate universe. REFUTED-D10 is not a LOSS proof. The standard 11x11 empty
board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.

Usage: python3 k1075_second_verification.py <input_dir> <out_path>
"""
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

RETIRED_ROOT = "00004000000000821082000000000100"
CAP = 30000000
PILOT = {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}

PINS = {
    # the K1075 consumed upstream records (same corpus as the published run)
    "resolve5.json": "5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e",
    "resolve6.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    "fold9.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    "fold10.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    "sv17.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
    "sweep39.json": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "sweep39dead.json": "f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246",
    "resolve7.json": "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
    # raw worker probe records and the 39-root manifest
    "probes-w0.jsonl": "6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984",
    "probes-w1.jsonl": "4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967",
    "probes-w2.jsonl": "2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032",
    "probes-w3.jsonl": "e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c",
    "roots.json": "9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc",
    # the independent resolve7 second verification record (cross-lane consistency)
    "r7second.json": "4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6",
    # the verification target itself
    "k1075.json": "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa",
}

PUBLISHED_CHECKS = [
    "pin-resolve5", "pin-sweep39", "pin-resolve6out", "pin-windfall4",
    "pin-seventeenth_fold", "pin-seventeenth_verify", "pin-sweep39_live",
    "pin-resolve7out", "corpus-manifest", "k0863-harvest",
    "k0863-target-children-exact", "k0863-transfers", "sweep6", "receipt-roots",
    "join-conflict-free", "universe-size", "dead39-excluded",
    "win-coverage-of-residual", "stage1-reproduction-vs-published-resolve6",
    "residual72-derivation-exact", "phase2-join-conflict-free",
    "universe72-subset-of-universe78", "live39-supply-status", "win-supply-72",
    "resolve7-postretire-geometry-recheck",
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def popcount_hex(s):
    return bin(int(s, 16)).count("1")


def gates_of(ln):
    global GATES
    GATES.append({"name": ln[0], "pass": bool(ln[1]), "detail": str(ln[2])})
    return bool(ln[1])


GATES = []


def in_(v, seq):
    return v in seq


def onecover_ok(entries, rows):
    """Entries (with 'covered') must one-cover exactly `rows`, disjointly."""
    flat = []
    for e in entries:
        cov = e["covered"]
        if not isinstance(cov, list) or len(cov) != 2:
            return False
        flat.extend(cov)
    if sorted(flat) != sorted(rows):
        return False
    return len(flat) == len(set(flat))


def main():
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output/candidate-supply-whole-record-second-verification-20261120.json"

    rec = {}
    for name in sorted(PINS):
        p = os.path.join(input_dir, name)
        got = sha256_file(p)
        gates_of(("pin-" + name, got == PINS[name], got))
        if got != PINS[name]:
            raise SystemExit("pin mismatch for " + name)
        if name.endswith(".jsonl"):
            rows = []
            with open(p) as f:
                for ln in f:
                    ln = ln.strip()
                    if ln:
                        rows.append(json.loads(ln))
            rec[name] = rows
        else:
            with open(p) as f:
                rec[name] = json.load(f)

    k = rec["k1075.json"]
    r5 = rec["resolve5.json"]
    r6 = rec["resolve6.json"]
    f9 = rec["fold9.json"]
    f10 = rec["fold10.json"]
    sv = rec["sv17.json"]
    sw = rec["sweep39.json"]
    sd = rec["sweep39dead.json"]
    r7 = rec["resolve7.json"]
    r7s = rec["r7second.json"]
    roots_manifest = rec["roots.json"]
    probes = (rec["probes-w0.jsonl"] + rec["probes-w1.jsonl"]
              + rec["probes-w2.jsonl"] + rec["probes-w3.jsonl"])

    # record self-identification gates
    gates_of(("k1075-schema", k["schema"] == "n11-residual72-full-cache-join-candidate-supply-20261120-v1", k["schema"]))
    gates_of(("k1075-date-2026-11-20", k["date"] == "2026-11-20", k["date"]))
    gates_of(("k1075-status", isinstance(k["status"], str) and k["status"] == "fresh-pool-exact-live-candidate-cover", k["status"]))
    ig = json.dumps(k.get("interpretation_guard", []))
    gates_of(("k1075-interpretation-guard-loss-clause", "not a LOSS proof" in ig, "guard[0]=" + str(k["interpretation_guard"][0])[:80]))
    gates_of(("k1075-interpretation-guard-not-certificates", "not certificates" in ig, ""))

    # ------------------------------------------------------------------ route A
    # K1069 live classification rebuilt from raw worker probe records.
    per_key = defaultdict(list)
    for p in probes:
        per_key[(p["root"], p["ordering"])].append(p)
    unique_pairs = sorted(per_key.keys())
    dup_records = len(probes) - len(unique_pairs)
    agree_fail = []
    for key, ps in per_key.items():
        sig = [(p["result"]["loss"], p["result"]["nodes"], p["result"]["capped"],
                p["result"]["bit"], p["child"], p["result"]["terminalStoneRange"]) for p in ps]
        if len(set(map(str, sig))) != 1 or len(set(json.dumps(sorted(p["covered_rows"])) for p in ps)) != 1:
            agree_fail.append(key)
    gates_of(("probes-corpus-parsed", len(probes) == 98 and len(unique_pairs) == 78,
              "records=%d unique(root,ordering)=%d" % (len(probes), len(unique_pairs))))
    gates_of(("probes-duplicate-records-node-exact-agree", not agree_fail and dup_records == 20,
              "dups=%d disagree=%s" % (dup_records, agree_fail)))
    dup_ok = True
    for ps in per_key.values():
        if len(ps) < 2:
            continue
        first = ps[0]
        for other in ps[1:]:
            for fld in ("root", "ordering", "cap", "worker", "seq",
                        "covered_rows", "bit", "child", "control"):
                if first.get(fld) != other.get(fld):
                    dup_ok = False
            for fld in ("loss", "nodes", "capped", "bit", "terminalStoneRange", "andclose"):
                if first["result"].get(fld) != other["result"].get(fld):
                    dup_ok = False
    gates_of(("probes-duplicates-differ-only-in-timing-fields", dup_ok,
              "checked dup keys=%d; wall_s/result.ms may differ, all evidence fields identical"
              % len([1 for ps in per_key.values() if len(ps) > 1])))
    gates_of(("probes-cap-uniform-30000000", all(p["cap"] == CAP for p in probes), ""))
    gates_of(("probes-control-pilot-d6-uniform", all(p["control"] == PILOT for p in probes), ""))

    root_probes = defaultdict(list)
    for key in unique_pairs:
        root_probes[key[0]].append(per_key[key][0])
    both_missing = [r for r, ps in root_probes.items()
                    if sorted(pp["ordering"] for pp in ps) != ["andclose0", "andclose1"]]
    gates_of(("probes-both-orders-per-root", len(root_probes) == 39 and not both_missing,
              "roots=%d missing=%s" % (len(root_probes), both_missing)))
    gates_of(("probes-andclose-field-consistent",
              all((p["ordering"] == "andclose1") == p["result"]["andclose"] for p in probes), ""))

    rebuilt_cls = {}
    order_conflicts = []
    for r, ps in root_probes.items():
        losses = set(p["result"]["loss"] for p in ps)
        capped = any(p["result"]["capped"] for p in ps)
        if capped:
            verdict = "CAPPED"
        elif len(losses) == 1:
            verdict = "WIN7-D10" if losses.pop() else "REFUTED-D10"
        else:
            verdict = "CONFLICT"
            order_conflicts.append(r)
        rebuilt_cls[r] = verdict
    gates_of(("k1069-classification-rebuilt-from-raw-probes",
              rebuilt_cls == sw["classification"],
              "mismatch=%s" % sorted(r for r in set(rebuilt_cls) | set(sw["classification"])
                                     if rebuilt_cls.get(r) != sw["classification"].get(r))))
    rebuilt_counts = Counter(rebuilt_cls.values())
    gates_of(("k1069-rebuilt-won1-refuted38-capped0",
              rebuilt_counts["WIN7-D10"] == 1 and rebuilt_counts["REFUTED-D10"] == 38
              and rebuilt_counts["CAPPED"] == 0 and not order_conflicts,
              json.dumps(rebuilt_counts)))

    total_nodes = sum(per_key[key][0]["result"]["nodes"] for key in unique_pairs)
    max_probe = max((per_key[key][0] for key in unique_pairs), key=lambda p: p["result"]["nodes"])
    gates_of(("k1069-total-nodes-rebuilt", total_nodes == sw["summary"]["total_nodes"] == 169615508,
              "%d vs %d" % (total_nodes, sw["summary"]["total_nodes"])))
    gates_of(("k1069-max-probe-fields-rebuilt",
              max_probe["result"]["nodes"] == sw["summary"]["max_probe"]["nodes"]
              and max_probe["root"] == sw["summary"]["max_probe"]["root"]
              and max_probe["result"]["loss"] == sw["summary"]["max_probe"]["loss"],
              "root=%s nodes=%d" % (max_probe["root"], max_probe["result"]["nodes"])))
    gates_of(("k1069-avg-nodes-rebuilt",
              total_nodes // len(unique_pairs) == sw["summary"]["avg_nodes_per_probe"],
              "%d vs %d" % (total_nodes // len(unique_pairs), sw["summary"]["avg_nodes_per_probe"])))
    gates_of(("k1069-no-capped", sw["summary"]["capped"] == 0
              and not any(p["result"]["capped"] for p in probes), ""))
    gates_of(("k1069-win-root-is-retired-root",
              [r for r, v in rebuilt_cls.items() if v == "WIN7-D10"] == [RETIRED_ROOT],
              ""))

    # K1059 dead-sweep REFUTED rebuild from the sweep39dead witness_records themselves.
    dead39_cls = sd["classification"]["refuted_d10"]["roots"]
    deadrec_roots = [x["root"] for x in sd["witness_records"]]
    gates_of(("k1059-dead39-set-agreement",
              sorted(dead39_cls) == sorted(deadrec_roots) == sorted(r6["base_state"]["dead_roots_39"])
              and sd["classification"]["win7_d10"] == {"count": 0, "roots": []}
              and sd["classification"]["counted_roots"] == 39,
              "cls=%d records=%d r6dead=%d" % (len(dead39_cls), len(deadrec_roots),
                                                len(r6["base_state"]["dead_roots_39"]))))
    dead_ok = True
    for wr in sd["witness_records"]:
        runs = wr["probe_runs"]
        if sorted(set(r["ordering"] for r in runs)) != ["andclose0", "andclose1"]:
            dead_ok = False
        if any(r["loss"] is not False or r["capped"] for r in runs):
            dead_ok = False
        if sum(r["nodes"] for r in runs) != wr["nodes_total"]:
            dead_ok = False
    gates_of(("k1059-refuted-d10-rebuilt-from-probe-runs", dead_ok and len(deadrec_roots) == 39,
              "both-order uncapped loss=false runs for 39/39 records"))

    # three-source agreement for the retired live 39: probes / roots.json / resolve6 witness.
    roots39 = {e["root"]: e for e in roots_manifest}
    gates_of(("roots39-manifest-is-classification-keys", set(roots39) == set(sw["classification"]), ""))
    gates_of(("roots39-manifest-anatomy",
              all(e["pcount"] == 7 and e["safe"] is True for e in roots39.values())
              and len(roots_manifest) == 39,
              ""))
    r6w_cov = {x["root"]: x["covered"] for x in r6["witness_full"]}
    pcov = defaultdict(set)
    for p in probes:
        pcov[p["root"]].update(p["covered_rows"])
    three_ok = (set(roots39) == set(r6w_cov) == set(pcov)
                and all(sorted(roots39[r]["rows"]) == sorted(r6w_cov[r])
                        and pcov[r] == set(roots39[r]["rows"]) for r in roots39))
    gates_of(("retired39-three-source-row-agreement", three_ok,
              "roots.json vs resolve6.witness_full vs probe covered_rows"))

    # ------------------------------------------------------------------ route B
    rows78 = r5["base_state"]["residual_row_hex"]
    gates_of(("resolve5-rows-78", len(rows78) == 78 and len(set(rows78)) == 78, ""))
    gates_of(("resolve5-rows-identical-to-resolve6",
              rows78 == r6["base_state"]["residual_row_hex"], ""))
    gates_of(("resolve5-witness-39-onecover-78",
              len(r5["witness_full"]) == 39 and onecover_ok(r5["witness_full"], rows78)
              and all(popcount_hex(e["root"]) == 7 for e in r5["witness_full"]),
              "39 roots x 2 rows, popcount 7"))
    gates_of(("resolve6-witness-39-onecover-78",
              len(r6["witness_full"]) == 39 and onecover_ok(r6["witness_full"], rows78)
              and all(popcount_hex(e["root"]) == 7 for e in r6["witness_full"]),
              "39 roots x 2 rows, popcount 7"))

    f9_target = set()
    for r in f9["receipts"]:
        f9_target.update(r["covered_five_parent_target_rows"])
    f10_target = set(f10["receipts"][0]["covered_five_parent_target_rows"])
    gates_of(("fold9-4receipts-4rows",
              len(f9["receipts"]) == 4 and len(f9_target) == 4 and f9_target <= set(rows78),
              sorted(f9_target)))
    gates_of(("fold10-1receipt-2rows",
              len(f10["receipts"]) == 1 and len(f10_target) == 2
              and f10_target <= (set(rows78) - f9_target),
              sorted(f10_target)))
    residual72 = set(rows78) - f9_target - f10_target
    fa10 = f10["five_parent_target_after"]
    krows = k["base_state"]["residual_row_hex"]
    r72_after = r7["recheck"]["residual_72_after"]["rows"]
    gates_of(("residual72-set-derivation",
              len(residual72) == 72 and residual72 == set(krows)
              and residual72 == set(fa10["residual_row_hex_after"])
              and residual72 == set(r72_after),
              "78 - 4 (fold9) - 2 (fold10) == 72; agrees with k1075, fold10, resolve7"))
    # r5 witness differs from r6 witness by design (each re-derived); the invariant is
    # each is a one-cover of the same 78 rows, gated above.
    gates_of(("fold9-frontier-chain-link", f9["frontier_after"] == f10["frontier_before"],
              json.dumps(f9["frontier_after"])[:120]))
    pb = k["base_state"]["published_base"]
    gates_of(("published-base-equals-fold10-frontier-after",
              pb["frontier_cost"] == f10["frontier_after"]["sum_remaining_cost"] == 491497
              and pb["frontier_s6"] == f10["frontier_after"]["unique_remaining_s6"] == 6206
              and pb["solved_s6"] == f10["frontier_after"]["solved_s6_in_manifest"] == 1642,
              "cost/s6/solved fields"))
    gates_of(("five-parent-target-40-of-112",
              pb["five_parent_target"] == "40/112"
              and fa10["closed_target_rows_total"] == 40 and fa10["residual_target_rows"] == 72
              and 40 + 72 == 112,
              ""))
    gates_of(("sv17-retired-root-consensus",
              sv["root_hex"] == RETIRED_ROOT
              and f10["receipts"][0]["root"] == RETIRED_ROOT
              and rebuilt_cls.get(RETIRED_ROOT) == "WIN7-D10"
              and k["verdict_join"]["newly_judged_since_resolve6"]["win"] == [RETIRED_ROOT]
              and sv["gates_all_pass"] is True and sv["gates_total"] == 38,
              "seventeenth receipt root == live-sweep WIN == record win root; sv17 38 gates"))
    wc = None
    for c in k["checks"]:
        if c["name"] == "win-coverage-of-residual":
            wc = c["detail"]
    wc_rows = set()
    for e in wc["evidence"]:
        wc_rows.update(e["covered_residual_rows"])
    gates_of(("resolve6-win-cover-rows-equal-fold9-target-rows",
              len(wc["evidence"]) == 4 and wc_rows == f9_target,
              "the 4 judge-WIN-covered rows of residual-78 are exactly the fold9 receipts"))

    # ------------------------------------------------------------------ route C
    st_detail = None
    for c in k["checks"]:
        if c["name"] == "stage1-reproduction-vs-published-resolve6":
            st_detail = c["detail"]
    r6_stats = r6["verdict_join"]["stats"]
    r6_hits = r6["verdict_join"]["universe_hits"]
    gates_of(("stage1-join-stats-equal-published-resolve6",
              all(st_detail["join_stats"][f] == r6_stats[f] for f in r6_stats),
              json.dumps(st_detail["join_stats"])))
    gates_of(("stage1-universe-hits-equal-published-resolve6",
              all(st_detail["universe_hits"][f] == r6_hits[f]
                  for f in ("fresh_safe", "fresh_unsafe", "judged_refuted", "judged_win", "unjudged_fresh")),
              json.dumps(st_detail["universe_hits"])))
    gates_of(("stage1-win-cover-hits-4", st_detail["win_cover_hits"] == 4, ""))
    gates_of(("stage1-witness-39-live-roots", st_detail["witness_39_live_roots"] == 39, ""))

    ks = k["verdict_join"]["stats"]
    gates_of(("join-stats-plus-39-arithmetic",
              ks["cache_engine_roots"] == r6_stats["cache_engine_roots"] == 7145
              and ks["canonical_roots_judged"] == r6_stats["canonical_roots_judged"] + 39 == 7532
              and ks["refuted_roots"] == r6_stats["refuted_roots"] + 38 == 6745
              and ks["win_roots"] == r6_stats["win_roots"] + 1 == 787
              and ks["win_refuted_conflicts"] == 0 and r6_stats["win_refuted_conflicts"] == 0
              and ks["published_transfer_only_roots"] == 0 and r6_stats["published_transfer_only_roots"] == 0,
              "7532=7493+39, 6745=6707+38, 787=786+1, conflicts 0"))
    nj = k["verdict_join"]["newly_judged_since_resolve6"]
    ref38 = set(sw["classification"]) - {RETIRED_ROOT}
    gates_of(("newly-judged-since-resolve6-anatomy",
              nj["roots"] == 39 and nj["refuted_38"] == 38 and nj["win"] == [RETIRED_ROOT]
              and len(ref38) == 38,
              "39 = 38 REFUTED-D10 + 1 WIN7-D10 (the seventeenth receipt root)"))

    uh72 = k["verdict_join"]["universe_hits_over_72"]
    cs = k["candidate_supply"]
    gates_of(("universe72-hits-identity",
              uh72["fresh_safe"] + uh72["fresh_unsafe"] == uh72["unjudged_fresh"]
              and uh72["unjudged_fresh"] + uh72["judged_refuted"] + uh72["judged_win"]
              == cs["universe72_roots"] == 7448,
              "4109+2871=6980; 6980+468+0=7448=universe72_roots"))
    gates_of(("universe72-hits-equal-published-numbers",
              (uh72["fresh_safe"], uh72["fresh_unsafe"], uh72["judged_refuted"],
               uh72["judged_win"], uh72["unjudged_fresh"]) == (4109, 2871, 468, 0, 6980),
              json.dumps(uh72)))
    gates_of(("fresh-safe-pool-equals-hits", cs["fresh_safe_pool"] == uh72["fresh_safe"] == 4109, ""))
    gates_of(("universe78-hits-identity",
              r6_hits["fresh_safe"] + r6_hits["fresh_unsafe"] == r6_hits["unjudged_fresh"]
              and r6_hits["unjudged_fresh"] + r6_hits["judged_refuted"] + r6_hits["judged_win"] == 7969,
              "4417+3102=7519; 7519+446+4=7969"))
    usz = None
    for c in k["checks"]:
        if c["name"] == "universe-size":
            usz = c["detail"]
    gates_of(("universe-size-check-78-7969", usz == {"published": 7969, "rebuilt": 7969}, json.dumps(usz)))
    u72sub = None
    for c in k["checks"]:
        if c["name"] == "universe72-subset-of-universe78":
            u72sub = c["detail"]
    gates_of(("universe72-subset-check-7448-of-7969",
              u72sub == {"rebuilt72": 7448, "universe78": 7969} and cs["universe72_roots"] == u72sub["rebuilt72"],
              json.dumps(u72sub)))

    # ------------------------------------------------------------------ route D
    rd = cs["row_demand"]
    fs = sorted(rd[r]["fresh_safe_candidates"] for r in rd)
    jr = sorted(rd[r]["judged_refuted_candidates"] for r in rd)
    jw = sorted(rd[r]["judged_win_candidates_covering"] for r in rd)
    gates_of(("row-demand-covers-all-72-rows", len(rd) == 72 and set(rd) == set(krows), ""))
    gates_of(("fresh-safe-per-row-52-76",
              fs[0] == 52 and fs[-1] == 76 and sum(fs) == 4678,
              "min=%d max=%d sum=%d" % (fs[0], fs[-1], sum(fs))))
    gates_of(("judged-refuted-per-row-4-13",
              jr[0] == 4 and jr[-1] == 13 and sum(jr) == 638,
              "min=%d max=%d sum=%d" % (jr[0], jr[-1], sum(jr))))
    gates_of(("judged-win-supply-zero", jw[-1] == 0 and sum(jw) == 0, "no judged-WIN root covers any open row"))
    gates_of(("no-fresh-safe-deficit",
              all(rd[r]["fresh_safe_candidate_deficit"] is False for r in rd), ""))
    gates_of(("fresh-safe-pool-one-covers-residual72",
              sorted(cs["fresh_safe_72row_coverage"]) == sorted(krows)
              and cs["rows_uncovered_by_fresh_safe_pool"] == [],
              ""))
    wit = k["witness_full"]
    wit_roots = set(x["root"] for x in wit)
    gates_of(("witness-36-entries-distinct-roots",
              len(wit) == 36 and len(wit_roots) == 36 and cs["witness_size"] == 36, ""))
    gates_of(("witness-anatomy-2row-safe-popcount7",
              all(len(e["covered"]) == 2 and e["covered"] == e["rows"] and e["safe"] is True
                  and popcount_hex(e["root"]) == 7 for e in wit),
              "36 roots, popcount 7, each covering exactly its 2 assigned open rows "
              "(cover relation is the join's row-graph data, see trust boundary)"))
    flat = [r for e in wit for r in e["covered"]]
    gates_of(("witness-onecover-of-residual72",
              sorted(flat) == sorted(krows) and len(flat) == len(set(flat)) == 72,
              "36 x 2 rows, disjoint, exact cover"))
    gates_of(("maximum-matching-36-proof-from-record",
              cs["matched_rows"] == 72 == 2 * cs["maximum_matching"]
              and cs["maximum_matching"] == 36 and cs["multi_cover_roots"] == {},
              "36 disjoint 2-row pairs cover all 72 rows (>=36); no matching on 72 rows "
              "can pair more than floor(72/2)=36; witness proves 36 attained -> maximum = 36"))
    judged_all = set(sw["classification"]) | set(dead39_cls) | {RETIRED_ROOT}
    gates_of(("witness-roots-disjoint-from-all-judged-sets",
              not (wit_roots & judged_all), "witness roots are unjudged fresh candidates"))
    live38 = set(cs["live38_killed_open_72row_supply"]["roots"])
    gates_of(("live38-record-anatomy",
              live38 == ref38
              and live38 == set(r7["recheck"]["post_retire_assignment"]["rows_per_root"]),
              "live38 == live-sweep-39-minus-WIN == resolve7 rows_per_root keys"))
    gates_of(("dead39-live39-disjoint", not (set(dead39_cls) & set(sw["classification"])), ""))
    gates_of(("witness-roots-disjoint-from-dead-3rd", not (wit_roots & set(dead39_cls)), ""))
    r7geom = None
    for c in k["checks"]:
        if c["name"] == "resolve7-postretire-geometry-recheck":
            r7geom = c["detail"]
    gates_of(("resolve7-geometry-recheck-detail",
              r7geom == {"assigned_rows_covered_geometrically": 72, "one_row_roots": 4, "two_row_roots": 34},
              json.dumps(r7geom)))
    gates_of(("receipted-and-windfall-open-row-supply-empty",
              cs["receipted_win_covering_open_rows"] == []
              and cs["windfall_18th_certificate_candidates"] == [],
              ""))
    gates_of(("unmatched-and-greedy-leftovers-zero",
              in_(cs["unmatched_rows"], (0, [])) and in_(cs["unmatched_with_singleton"], (0, []))
              and in_(cs["greedy_leftover_rows"], (0, []))
              and in_(cs["stranded_rows"], (0, [])),
              "unmatched=%s unmatched+singleton=%s greedy_leftover=%s stranded=%s"
              % (cs["unmatched_rows"], cs["unmatched_with_singleton"],
                 cs["greedy_leftover_rows"], cs["stranded_rows"])))
    gates_of(("trust-boundary-stated-in-record",
              "fails closed on any conflict" in k.get("trust_boundary", "")
              and "stage-1 must reproduce the published resolve6 stats exactly or the run aborts"
              in k.get("trust_boundary", ""),
              "conflict-fails-closed + stage-1 abort semantics present"))

    # published 25-check self-audit
    kchecks = {c["name"]: c for c in k["checks"]}
    gates_of(("published-25-checks-all-pass",
              len(k["checks"]) == 25 and all(c["pass"] is True for c in k["checks"]),
              "count=%d all_pass=%s" % (len(k["checks"]), all(c["pass"] for c in k["checks"]))))
    gates_of(("published-25-check-names-exact",
              sorted(kchecks) == sorted(PUBLISHED_CHECKS), ""))

    # resolve7 cross-record consistency
    gates_of(("resolve7-record-pin-match",
              k["resolve7_cross_check"]["record_sha256"] == PINS["resolve7.json"],
              k["resolve7_cross_check"]["record_sha256"]))
    gates_of(("resolve7-gates-all-pass-27",
              r7["gates_all_pass"] is True and r7["gates_total"] == 27, ""))
    gates_of(("resolve7-cross-check-fields",
              k["resolve7_cross_check"]["assignment_34x2_plus_4x1"] is True
              and k["resolve7_cross_check"]["post_retire_assignment_geometry_recheck"] is True,
              "34x2+4x1 == 72 == r7geom 34+4 (2-row roots + 1-row roots)"))
    # cross-lane consistency with the independent resolve7 second verification
    gates_of(("r7second-record-consistency",
              r7s["schema"] == "resolve7-second-verification/1"
              and r7s["gates_total"] == 76 and r7s["gates_all_pass"] is True
              and r7s["input_pins"]["resolve7.json"] == PINS["resolve7.json"],
              "76-gate resolve7 second verification agrees on the resolve7 pin"))

    gates_tot = len(GATES)
    all_pass = all(g["pass"] for g in GATES)
    result = {
        "schema": "n11-residual72-candidate-supply-whole-record-second-verification/1",
        "date": "2026-11-20",
        "status": "independent second verification; published records only; no search, no new judging",
        "verification_target": {
            "path": "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json",
            "sha256": PINS["k1075.json"],
            "published_checks": 25,
        },
        "single_owner_note": "research/log/2026-11-20-n11-candidate-supply-whole-record-second-verification-single-owner-note.md",
        "input_pins": {name: PINS[name] for name in sorted(PINS)},
        "gates": [{"name": g["name"], "pass": g["pass"], "detail": g["detail"]} for g in GATES],
        "gates_total": gates_tot,
        "gates_all_pass": all_pass,
        "independent_routes": [
            "route A: K1069 classification + node statistics rebuilt from raw 4-worker probe "
            "records (98 lines, 78 unique (root,ordering), 20 duplicates node-exact), and "
            "K1059 dead-39 REFUTED-D10 rebuilt from sweep39dead probe_runs",
            "route B: fold-chain set arithmetic rows78 -> fold9 -4 -> fold10 -2 -> 72 with "
            "frontier/published-base numerics, checked against four independent row lists "
            "(k1075, fold10, resolve7, set derivation)",
            "route C: stage-1 reproduction identity against resolve6 verdict_join plus the "
            "+38/+1/7532 delta arithmetic and universe-size identities 7448/7969",
            "route D: phase-2 row_demand re-aggregation for all 72 rows, witness one-cover "
            "anatomy, maximum-matching-36 proof from the record alone, and disjointness "
            "from every judged set, cross-checked with resolve7 and its 76-gate second verification",
        ],
        "rederived": {
            "residual72": 72,
            "residual72_rows_equal_in_k1075_fold10_resolve7_and_set_derivation": True,
            "judged_roots_after_live_sweep": 7532,
            "refuted_roots": 6745,
            "win_roots": 787,
            "win_refuted_conflicts": 0,
            "universe78": 7969,
            "universe72": 7448,
            "fresh_safe_pool": 4109,
            "fresh_safe_per_row_min_max_sum": [52, 76, 4678],
            "judged_refuted_per_row_min_max_sum": [4, 13, 638],
            "judged_win_open_row_supply": 0,
            "witness_size": 36,
            "maximum_matching": 36,
            "probe_records": 98,
            "probe_unique_pairs": 78,
            "probe_duplicate_records_node_exact": 20,
            "probe_total_nodes": 169615508,
            "retired_live_witness_supply_for_residual72": 0,
            "dead_sweep_refuted_rebuilt_from_probe_runs": 39,
        },
        "trust_boundary": [
            "The root-level universe lists (7969 and 7448 roots) and the 4109-root fresh pool "
            "are not published in any pinned record; per-root pool membership is not "
            "recomputable from records alone.",
            "pair_edges=536, greedy_set_cover_size=40, singleton_eligible_rows=72 and the "
            "universe-intersection counts (dead39_in_universe72=37, live38_in_universe72=38) "
            "are K1075-internal claims outside the independent gate set of this second "
            "verification.",
            "The maximum-matching-36 claim is re-proved here only through the pairing bound: "
            "the published witness is 36 disjoint 2-row pairs covering all 72 rows, and no "
            "matching on 72 rows exceeds 36 pairs; the row-graph itself is not published.",
            "The root-to-row cover relation for the 36 witness roots (and the whole "
            "candidate supply) is the join's row-graph list as published in the record; "
            "it is not bitset-set-inclusion and is not re-derivable from the hexes alone.",
            "Engine depth-10 verdict soundness and D4 invariance are upstream premises, "
            "identical to the published resolve6 join; this record judges no position.",
        ],
        "target_record_faithful": all(g["pass"] for g in GATES
                                      if g["name"].startswith(("universe", "join", "stage1",
                                                               "newly", "row-demand", "fresh-safe",
                                                               "witness", "maximum", "published-25",
                                                               "resolve7-", "k1075-"))),
        "interpretation_guard": [
            "REFUTED-D10 is NOT a LOSS proof; it certifies no first-player win within depth-10 from that root only.",
            "A fold is row-coverage bookkeeping and says nothing about game-theoretic values.",
            "Witness roots and candidate supply are conditional depth-10 sweep plans, not certificates.",
            "This second verification judges no root, closes no row, and rebuilds no candidate universe.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("gates", result["gates_total"], "all_pass", result["gates_all_pass"],
          "faithful", result["target_record_faithful"])


if __name__ == "__main__":
    main()
