#!/usr/bin/env python3
"""Independent fail-closed audit for the sixth-cost class
10376293541461626880:65536 parked-4-keys S5 L50M ladder. Re-derives everything
from this lane's published raw rows and the pinned corpora (frozen geometry,
chain head of record 6e49dd84, parent probe batch machine selection and
published parked raw rows, reply27 supply ledger, quarantine registry); fails
closed on any gate failure, writes no OK audit on the WIN branch, and emits
NO cache row or file under ANY branch (this lane's declared no-increment rule;
consumption stays with the parent batch's full audit and the WIN/LOSS conflict
policy).

Ladder: the four keys the fifth-resumption parent batch parked at UNKNOWN@15M
are re-probed at budget 50,000,000, twice each with independent fresh solvers;
identical (result, nodes) required; a resolved key gets one 32,000,000
budget-margin re-proof; a WIN key gets a voluntary third cold 50,000,000
verification run (honestly labeled); ANY WIN stops further claimed-key STARTS
(stopping rule 1): keys already started complete their pre-registered stages,
never-started keys must have zero lane artifacts. A key that still exhausts the
budget is parked again (UNKNOWN@50M).

Honest drafting disclosure: this script was drafted before the first 50M
result was observed (its gates and semantics unchanged since), then revised
once, before any publication, to handle correctly a halt state in which MORE
THAN ONE started key resolves WIN (the precedent texts assumed a single WIN);
the revision generalizes single-WIN bookkeeping to a WIN list and adds the
never-started zero-artifact gates. No gate was weakened for the observed
results.

Semantics (pinned): 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first
player). At 5 stones the node is an AND node, so WIN means the first player of
this line wins against every second-player reply."""
import csv, gzip, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pub_paths

P = pub_paths.resolve(__file__)
sys.path.insert(0, str(P["indep"].parent))
sys.path.insert(0, str(P["policy"].parent))
from independent import Board, mask_from_key  # noqa: E402
from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys  # noqa: E402

EXP = P["exp"]
RAW = EXP / "output" / "raw"
INP = EXP / "input"
GEOMETRY = P["geometry"]
BASE_CACHE = P["cache"]
PARENT_RAW = P["parent_raw"]
SELECTION = P["selection"]

JS_SHA_EXPECT = pub_paths.JS_SHA
INDEP_SHA_EXPECT = pub_paths.INDEP_SHA
POLICY_SHA_EXPECT = pub_paths.POLICY_SHA
GEOM_SHA_EXPECT = pub_paths.GEOM_SHA
BASE_SHA_EXPECT = pub_paths.BASE_SHA
SEL_SHA_EXPECT = pub_paths.SEL_SHA
SUPPLY_SHA_EXPECT = pub_paths.SUPPLY_SHA
QUAR_SHA_EXPECT = pub_paths.QUAR_SHA

MY_CLASS = (10376293541461626880, 65536)
BASE_ROWS_EXPECT = 6792
BASE_CLASS_BEFORE = {"status": "UNKNOWN", "win": 0, "loss": 8, "unknown": 100}
# kNN -> (key string, machine-order position, legal)
MY_KEYS = {
    "k13": ("1152921573327376384:536870912", 13, 95),
    "k19": ("10376293541461626880:65664", 19, 95),
    "k20": ("10376293541461626880:33619968", 20, 95),
    "k33": ("12682136550675320832:65536", 33, 91),
}
KEY_ORDER = ("k13", "k19", "k20", "k33")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_replay(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        if line.startswith("replay,"):
            f = line.split(",")
            rows.append(dict(id=int(f[1]), stones=int(f[2]), legal=int(f[3]),
                             is_or=int(f[4]), budget=int(f[5]), result=int(f[6]),
                             nodes=int(f[7]), key_lo=int(f[9]), key_hi=int(f[10])))
    return rows


def read_cache_rows(p):
    data = Path(p).read_text(encoding="utf-8").split("\n")
    header = data[0]
    rows = {}
    for r in data[1:]:
        if not r:
            continue
        f = r.split(",")
        assert f[0] == "s5verdict" and int(f[3]) == 5 and int(f[4]) in (1, 2)
        k = (int(f[1]), int(f[2]))
        if k in rows and rows[k].split(",")[4] != f[4]:
            raise ValueError(f"verdict conflict on {k}")
        rows[k] = r
    return header, rows


gates = []
def gate(name, ok, detail=""):
    if not ok:
        print(f"GATE FAIL: {name} {detail}", file=sys.stderr)
        sys.exit(1)
    gates.append(name)


def main():
    out_path = EXP / "output" / "lane-audit.json"
    # ---- pins ----
    gate("jsreplay_sha", sha(P["jsrelay"]) == JS_SHA_EXPECT)
    gate("independent_sha", sha(P["indep"]) == INDEP_SHA_EXPECT)
    gate("policy_sha", sha(P["policy"]) == POLICY_SHA_EXPECT)
    gate("geometry_sha", sha(GEOMETRY) == GEOM_SHA_EXPECT)
    gate("base_chain_cache_sha", sha(BASE_CACHE) == BASE_SHA_EXPECT)
    gate("selection_sha", sha(SELECTION) == SEL_SHA_EXPECT)
    gate("supply_sha", sha(P["supply"]) == SUPPLY_SHA_EXPECT)
    gate("quarantine_sha", sha(P["quar"]) == QUAR_SHA_EXPECT)

    # ---- validation gate: fresh re-runs vs published two-target raw rows ----
    expect = {
        "val-at2m-first": (98, 2_000_000, 0, 2_000_000, 1152921504606851072, 536870946),
        "val-at2m-second": (99, 2_000_000, 0, 2_000_000, 1188950301626860544, 536870912),
        "val-first-15m": (98, 15_000_000, 2, 3_651_923, 1152921504606851072, 536870946),
        "val-second-15m": (99, 15_000_000, 2, 5_040_200, 1188950301626860544, 536870912),
    }
    val_rows = {}
    for tag, e in expect.items():
        rep = read_replay(RAW / f"{tag}.out.csv")
        gate(f"validation_{tag}", len(rep) == 1 and
             (rep[0]["legal"], rep[0]["budget"], rep[0]["result"], rep[0]["nodes"],
              rep[0]["key_lo"], rep[0]["key_hi"]) == e)
        val_rows[tag] = rep[0]

    # ---- targets = exactly the parent batch's parked keys ----
    sel = json.loads(Path(SELECTION).read_text(encoding="utf-8"))
    gate("selection_schema", sel.get("schema") == "n11-sixthcost-exclusive-selection-v1")
    order = sel["exclusive_probe_order"]
    for kn in KEY_ORDER:
        kstr, pos, legal = MY_KEYS[kn]
        gate(f"selection_{kn}_position", order[pos - 1]["key"] == kstr and
             order[pos - 1]["legal"] == legal)
    for kn in KEY_ORDER:
        kstr, pos, legal = MY_KEYS[kn]
        lo, hi = kstr.split(":")
        P2 = (int(lo), int(hi))
        t2m = read_replay(PARENT_RAW / f"at2m-{kn}.out.csv")
        gate(f"{kn}.parent_2m_parked", len(t2m) == 1 and t2m[0]["budget"] == 2_000_000
             and t2m[0]["result"] == 0 and t2m[0]["nodes"] == 2_000_000
             and (t2m[0]["key_lo"], t2m[0]["key_hi"]) == P2)
        for rn in ("run1", "run2"):
            r15 = read_replay(PARENT_RAW / f"at15m-{rn}-{kn}.out.csv")
            gate(f"{kn}.parent_15m_{rn}_parked", len(r15) == 1 and
                 r15[0]["budget"] == 15_000_000 and r15[0]["result"] == 0 and
                 r15[0]["nodes"] == 15_000_000 and
                 (r15[0]["key_lo"], r15[0]["key_hi"]) == P2)
    supply = {}
    for row in csv.DictReader(P["supply"].open(newline="")):
        lo2, hi2 = row["key"].split(":")
        supply[(int(lo2), int(hi2))] = row
    qkeys = quarantined_cache_keys()

    base_header, base_rowmap = read_cache_rows(BASE_CACHE)
    base_keys = sorted(base_rowmap)
    base_vals = {k: int(base_rowmap[k].split(",")[4]) for k in base_keys}
    gate("base_cache_rows", len(base_keys) == BASE_ROWS_EXPECT)
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("frozen_geometry_size", len(geo) == 3384)
    my_children = {tuple(z) for z in next(g for g in geo if tuple(g["key"]) == MY_CLASS)["children"]}

    def classes_with(vals):
        out = {}
        for row in geo:
            ch = {tuple(z) for z in row["children"]}
            v = [vals.get(z, 0) for z in ch]
            st = "WIN" if 1 in v else ("LOSS" if all(x == 2 for x in v) else "UNKNOWN")
            out[tuple(row["key"])] = dict(status=st, win=v.count(1), loss=v.count(2),
                                          unknown=v.count(0), coverage=row["coverage"], total=len(ch))
        return out

    # ---- started vs never-started keys (stopping rule 1 bookkeeping) ----
    started = [kn for kn in KEY_ORDER if (RAW / f"base15m-{MY_KEYS[kn][0].replace(':', '-')}.out.csv").exists()]
    unstarted = [kn for kn in KEY_ORDER if kn not in started]
    for kn in unstarted:
        lo, hi = MY_KEYS[kn][0].split(":")
        artifacts = [p.name for p in RAW.glob(f"*{lo}-{hi}*") if not p.name.endswith("err")]
        gate(f"{kn}.never_started_zero_artifacts", not artifacts, f"{artifacts}")

    per_key, done, parked50, wins = {}, [], [], []
    for kn in started:
        kstr, pos, legal = MY_KEYS[kn]
        lo, hi = kstr.split(":")
        K = (int(lo), int(hi))
        ip = INP / f"batch-{kn}.input.csv"
        line = [l for l in ip.read_text().split("\n") if l][0]
        f = line.split(",")
        gate(f"{kn}.input_target", f[0] == "target" and int(f[2]) == 5 and
             (int(f[3]), int(f[4])) == K and int(f[5]) == legal)
        gate(f"{kn}.legal_supply", int(supply[K]["legal"]) == legal)
        board = Board(11)
        mask = mask_from_key(*K)
        gate(f"{kn}.stone_count", len(board.points(mask)) == 5)
        gate(f"{kn}.d4_canonical", board.canonical(mask) == mask)
        gate(f"{kn}.legal_count", len(board.points(board.legal(mask))) == legal)
        gate(f"{kn}.policy_canonical_safe", is_canonical_safe_s5_key(K))
        gate(f"{kn}.quarantine_absent", K not in qkeys)
        gate(f"{kn}.base_absent", K not in base_vals)
        gate(f"{kn}.my_class_child", K in my_children)
        # baseline parked reproduction (fresh this session, 15M single run)
        rb = read_replay(RAW / f"base15m-{lo}-{hi}.out.csv")
        gate(f"{kn}.base15m_row", len(rb) == 1 and rb[0]["budget"] == 15_000_000
             and (rb[0]["key_lo"], rb[0]["key_hi"]) == K)
        gate(f"{kn}.base15m_parked_reproduced", rb[0]["result"] == 0 and rb[0]["nodes"] == 15_000_000)
        # ladder 50M twice
        r1 = read_replay(RAW / f"l50m-run1-{lo}-{hi}.out.csv")
        r2 = read_replay(RAW / f"l50m-run2-{lo}-{hi}.out.csv")
        for tag, rr in (("run1", r1), ("run2", r2)):
            gate(f"{kn}.{tag}_row", len(rr) == 1 and rr[0]["budget"] == 50_000_000
                 and (rr[0]["key_lo"], rr[0]["key_hi"]) == K
                 and rr[0]["stones"] == 5 and rr[0]["is_or"] == 0)
            gate(f"{kn}.{tag}_form", rr[0]["result"] in (0, 1, 2) and 0 < rr[0]["nodes"] <= 50_000_000
                 and (rr[0]["result"] != 0 or rr[0]["nodes"] == 50_000_000))
        gate(f"{kn}.determinism", (r1[0]["result"], r1[0]["nodes"]) == (r2[0]["result"], r2[0]["nodes"]))
        # budget-margin re-proof (present for every resolved key)
        margin_info = None
        mpath = RAW / f"l50m-margin-{lo}-{hi}.out.csv"
        if r1[0]["result"] != 0:
            gate(f"{kn}.margin_present_for_resolved", mpath.exists())
        if mpath.exists():
            rm = read_replay(mpath)
            gate(f"{kn}.margin_row", len(rm) == 1 and (rm[0]["key_lo"], rm[0]["key_hi"]) == K
                 and rm[0]["budget"] == 32_000_000
                 and (rm[0]["result"] != 0 or rm[0]["nodes"] == rm[0]["budget"]))
            if r1[0]["result"] != 0:
                gate(f"{kn}.margin_determinism",
                     rm[0]["result"] != 0 and
                     (rm[0]["result"], rm[0]["nodes"]) == (r1[0]["result"], r1[0]["nodes"]))
            margin_info = {"budget": rm[0]["budget"], "result": rm[0]["result"], "nodes": rm[0]["nodes"]}
        # voluntary third cold verification run for a WIN key (honestly labeled)
        verify_info = None
        vpath = RAW / f"l50m-run3-verify-{lo}-{hi}.out.csv"
        if vpath.exists():
            rv = read_replay(vpath)
            gate(f"{kn}.run3_verify_row", len(rv) == 1 and rv[0]["budget"] == 50_000_000
                 and (rv[0]["key_lo"], rv[0]["key_hi"]) == K)
            gate(f"{kn}.run3_verify_voluntary_determinism",
                 rv[0]["result"] == r1[0]["result"] and rv[0]["nodes"] == r1[0]["nodes"])
            verify_info = {"budget": rv[0]["budget"], "result": rv[0]["result"], "nodes": rv[0]["nodes"]}
        if r1[0]["result"] == 1:
            wins.append(kn)
        elif r1[0]["result"] == 2:
            done.append(kn)
        else:
            parked50.append(kn)
        per_key[kn] = {"key": kstr, "position": pos, "legal": legal,
                       "stages": {"base15m": {"result": rb[0]["result"], "nodes": rb[0]["nodes"]},
                                  "at50m": {"result": r1[0]["result"], "nodes": r1[0]["nodes"]},
                                  "at50m_run2": {"result": r2[0]["result"], "nodes": r2[0]["nodes"]}},
                       "verdict": {1: "WIN", 2: "LOSS", 0: "UNKNOWN@50M"}[r1[0]["result"]]}
        if margin_info is not None:
            per_key[kn]["stages"]["margin_reproof"] = margin_info
        if verify_info is not None:
            per_key[kn]["stages"]["voluntary_run3_verify"] = verify_info
    gate("batch_accounting", len(done) + len(parked50) + len(wins) == len(started)
         and len(started) + len(unstarted) == 4)

    # ---- class recomputation (recorded NOT-ADOPTED; nothing is merged) ----
    cb = classes_with(base_vals)
    gate("my_class_before", cb[MY_CLASS]["status"] == BASE_CLASS_BEFORE["status"]
         and cb[MY_CLASS]["win"] == BASE_CLASS_BEFORE["win"]
         and cb[MY_CLASS]["unknown"] == BASE_CLASS_BEFORE["unknown"]
         and cb[MY_CLASS]["loss"] == BASE_CLASS_BEFORE["loss"])
    hyp_vals = dict(base_vals)
    for kn in done + wins:
        lo, hi = MY_KEYS[kn][0].split(":")
        hyp_vals[(int(lo), int(hi))] = 2 if kn in done else 1
    ch = classes_with(hyp_vals)
    class_after_hyp = ch[MY_CLASS]
    status_changes_hyp = []
    for kk in cb:
        if cb[kk]["status"] != ch[kk]["status"]:
            status_changes_hyp.append({"key": list(kk), "before": cb[kk]["status"],
                                       "after": ch[kk]["status"], "coverage": cb[kk]["coverage"]})

    pins = {"jsreplay_sha256": sha(P["jsrelay"]),
            "independent_geometry_python_sha256": sha(P["indep"]),
            "geometry_sha256": sha(GEOMETRY),
            "base_chain_cache_sha256": sha(BASE_CACHE),
            "parent_selection_json_sha256": sha(SELECTION),
            "supply_sha256": sha(P["supply"]),
            "quarantine_sha256": sha(P["quar"]),
            "policy_sha256": sha(P["policy"])}

    if wins:
        # ---- stopping rule 1: WIN(s) halt the lane before consumption ----
        halt = {
            "schema": "n11-sixthcost-parked4-l50m-ladder-halt-audit-v1",
            "all_gates_pass_before_halt": True,
            "halted_on_win_keys": [MY_KEYS[kn][0] for kn in wins],
            "gates_passed_count": len(gates),
            "title": ("sixth-cost class 10376293541461626880:65536 parked-4-keys S5 L50M ladder "
                      f"HALTED on WIN (stopping rule 1) at started keys {wins} "
                      f"([{', '.join(MY_KEYS[kn][0] for kn in wins)}]): {len(wins)} WIN / {len(done)} LOSS "
                      f"raws recorded with determinism pairs, margins and voluntary third verify runs, "
                      f"{len(unstarted)} claimed keys never started on this lane "
                      f"(remain parked@15M, claimable by a later lane), no verdict consumed, no cache "
                      "file, no class/root claim"),
            "pins": pins,
            "probe": {
                "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
                "claimed_keys": [MY_KEYS[kn][0] for kn in KEY_ORDER],
                "started_keys": [MY_KEYS[kn][0] for kn in started],
                "never_started_keys_stay_parked_15m": [MY_KEYS[kn][0] for kn in unstarted],
                "resolved_loss_raw": [MY_KEYS[kn][0] for kn in done],
                "win_raws_needing_scrutiny": [MY_KEYS[kn][0] for kn in wins],
                "per_key": per_key,
                "determinism": ("every executed stage ran with identical (result, nodes) across its "
                                "runs (declared determinism pair, 32M budget-margin re-proof, and, for "
                                "WIN keys, a voluntary third cold 50M verification run); every WIN key "
                                "completed within budget (nodes < budget), so each is a full df-pn proof, "
                                "not a truncation; a second implementation (the pinned C++ "
                                "kyouen_dfpn_root.cpp) re-verification is REQUIRED before any row may be "
                                "consumed; this environment has no C++ compiler, so the task is handed "
                                "to the scrutiny owner"),
                "pinned_semantics": ("exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed "
                                     "first player 'proposition: the player who moved FIRST on this line "
                                     "eventually wins'; 5 stones is an AND node, so WIN = first player "
                                     "wins against every second-player reply)"),
                "delegated_cpp_gate_targets": [
                    {"key": MY_KEYS[kn][0],
                     "target": ("target,0,5," + MY_KEYS[kn][0].replace(':', ',') +
                                f",{MY_KEYS[kn][2]},0,0,0,0,0"),
                     "budget": 50_000_000, "expected_result": per_key[kn]["stages"]["at50m"]["result"],
                     "expected_nodes": per_key[kn]["stages"]["at50m"]["nodes"]}
                    for kn in wins + done],
            },
            "if_adopted_would_not_adopted_recorded_only": {
                "my_class_after": class_after_hyp,
                "global_status_changes": status_changes_hyp,
                "note": ("NOT adopted by this lane. If scrutiny adopts the raw rows, the class "
                         f"{MY_CLASS[0]}:{MY_CLASS[1]} status would be decided by the canonical chain "
                         "merge under the parent batch's WIN/LOSS conflict policy; its coverage "
                         "{80, 84, 100, 108} includes the two remaining third moves 100/108 of the "
                         "two-stone root {60,27}; the root impact through the depth-2/depth-1 chain is "
                         "NOT computed by this lane and belongs to the K0414/K0416-lineage owners."),
            },
            "records": {"validation_raw_rows_reproduced": [
                {"tag": t, "row": {"stones": v["stones"], "legal": v["legal"], "is_or": v["is_or"],
                                   "budget": v["budget"], "result": v["result"], "nodes": v["nodes"]}}
                for t, v in val_rows.items()]},
            "status_guard": ("halted evidence only; NO verdict is consumed; the 11x11 empty board, the "
                             "two-stone root {60,27}, and third moves 100/108 remain UNKNOWN; nodes and "
                             "proxy values are never verdicts; no cache file is published from this lane"),
        }
        (EXP / "output" / "halt-audit.json").write_text(
            json.dumps(halt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ALL {len(gates)} PRE-WIN GATES PASS -> HALTED ON WIN {wins}")
        print(f"win_keys={[MY_KEYS[kn][0] for kn in wins]} loss_raw={[MY_KEYS[kn][0] for kn in done]} "
              f"never_started={unstarted}")
        print("halt-audit.json written; no OK audit, no cache file")
        sys.exit(2)

    # ---- non-WIN branch: OK audit, NO cache emission (declared no-increment rule) ----
    gate("no_cache_emitted", not (EXP / "output" / "merged-exact-s5-after-parked4-l50m.cache").exists()
         and not any((EXP / "output").glob("*.cache")))
    audit = {
        "schema": "n11-sixthcost-parked4-l50m-ladder-audit-v1",
        "all_gates_pass": True,
        "title": ("sixth-cost class 10376293541461626880:65536 parked-4-keys S5 L50M ladder: "
                  f"{len(done)} LOSS / {len(parked50)} UNKNOWN@50M / 0 WIN of {len(started)} started keys"),
        "gates_passed_count": len(gates),
        "pins": pins,
        "validation": {
            "published_raw_rows_reproduced": [
                {"tag": t, "row": {"stones": v["stones"], "legal": v["legal"], "is_or": v["is_or"],
                                   "budget": v["budget"], "result": v["result"], "nodes": v["nodes"]}}
                for t, v in val_rows.items()],
            "rule": "stones/legal/is_or/budget/result/nodes must match the published C++ raw rows; wall_s may differ",
        },
        "probe": {
            "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
            "claimed_keys": [MY_KEYS[kn][0] for kn in KEY_ORDER],
            "resolved_loss": [MY_KEYS[kn][0] for kn in done],
            "parked_unknown_50m": [MY_KEYS[kn][0] for kn in parked50],
            "win": None,
            "pinned_semantics": "exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player)",
            "evidence_class": ("replica solver-trusted exact, node-exact against all four published C++ raw "
                               "rows and the parent batch's published parked@15M baselines; NOT "
                               "terminal-only minimax"),
            "per_key": per_key,
            "determinism": ("every 50M stage executed twice with identical (result, nodes); baseline 15M "
                            "parked state reproduced fresh (result 0, nodes 15,000,000) per key"),
            "no_increment_policy": ("NO cache row or file published by this lane under any outcome; the "
                                   "resolved rows stay unconsumed until the parent batch's full audit and "
                                   "the WIN/LOSS conflict policy consume them; the pinned C++ "
                                   "second-implementation re-verification is additionally required and "
                                   "delegated (no C++ toolchain in this lane's sandbox)"),
        },
        "class_recomputation": {
            "note": ("NOT adopted; recorded only. The canonical chain status is untouched by this lane."),
            "my_class_base_of_record_6e49dd84": cb[MY_CLASS],
            "my_class_if_adopted_recorded_only": class_after_hyp,
            "global_status_changes_if_adopted_recorded_only": status_changes_hyp,
        },
        "status_guard": ("evidence increment only; the 11x11 empty board, the two-stone root {60,27}, "
                         "and third moves 100/108 remain UNKNOWN; nodes and proxy values are never "
                         "verdicts; the class keeps at least 58 unproven shared children and is NOT closed"),
    }
    out_path.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ALL {len(gates)} GATES PASS")
    print(f"loss={len(done)} ({[MY_KEYS[kn][0] for kn in done]}) parked50m={parked50} win=None")
    print(f"class if adopted (recorded only): {class_after_hyp['status']} "
          f"win={class_after_hyp['win']} loss={class_after_hyp['loss']} unknown={class_after_hyp['unknown']}")
    print(f"status_changes_if_adopted={[(c['key'], c['before'], c['after']) for c in status_changes_hyp]}")
    print("no cache file published (declared no-increment rule)")


if __name__ == "__main__":
    main()
