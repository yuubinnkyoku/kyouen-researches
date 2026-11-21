#!/usr/bin/env python3
"""Independent fail-closed audit for the third-cost class 1297036830122704896:0
parked-2-keys S5 L50M ladder. Re-derives everything from the published raw rows
and the pinned corpora (parent probe audit, chain cache increment, frozen
geometry); fails closed on any gate failure and writes no OK audit.

Ladder: the two keys the parent probe parked at UNKNOWN@15M are re-probed at
budget 50,000,000, twice each, independent fresh solvers; identical (result,
nodes) required; WIN halts (no OK audit, no cache row); a key that still
exhausts the budget is parked again (no cache row)."""
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
PARENT_AUDIT = P["parent_audit"]
QUARANTINE = P["quar"]
SUPPLY = P["supply"]

INDEP_SHA_EXPECT = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA_EXPECT = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
GEOM_SHA_EXPECT = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
BASE_SHA_EXPECT = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
PARENT_AUDIT_SHA_EXPECT = "950a716b68530e62cdf5fdd094be5b399c2f983d5b16b4cdec9352dca9b93fd2"
JS_SHA_EXPECT = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

MY_CLASS = (1297036830122704896, 0)
BASE_ROWS_EXPECT = 5793
BASE_CLASS_BEFORE = {"status": "UNKNOWN", "loss": 44, "unknown": 63}
MY_KEYS = ["1297036830122704896:67108864", "10376294091217440768:33554432"]


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
    out_path = EXP / "output" / "probe-audit.json"
    # ---- pins ----
    gate("independent_sha", sha(P["indep"]) == INDEP_SHA_EXPECT)
    gate("policy_sha", sha(P["policy"]) == POLICY_SHA_EXPECT)
    gate("jsreplay_sha", sha(P["jsrelay"]) == JS_SHA_EXPECT)
    gate("geometry_sha", sha(GEOMETRY) == GEOM_SHA_EXPECT)
    gate("base_chain_cache_sha", sha(BASE_CACHE) == BASE_SHA_EXPECT)
    gate("parent_audit_sha", sha(PARENT_AUDIT) == PARENT_AUDIT_SHA_EXPECT)

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

    # ---- targets = exactly the parent probe's parked keys ----
    parent = json.loads(Path(PARENT_AUDIT).read_text(encoding="utf-8"))
    gate("parent_audit_all_pass", parent.get("all_gates_pass") is True)
    gate("parent_parked_list", sorted(parent["probe"]["parked_unknown_15m"]) == sorted(MY_KEYS))
    parked_legal = {r["key"]: r["legal"] for r in parent_audit_order(parent)}
    supply = {}
    for row in csv.DictReader(SUPPLY.open(newline="")):
        lo, hi = row["key"].split(":")
        supply[(int(lo), int(hi))] = row
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

    per_key, done, parked50, win = {}, [], [], None
    for k in MY_KEYS:
        lo, hi = k.split(":")
        K = (int(lo), int(hi))
        # inputs
        ip = INP / f"batch-s5-{lo}-{hi}.input.csv"
        line = [l for l in ip.read_text().split("\n") if l][0]
        f = line.split(",")
        gate(f"{k}.input_target", f[0] == "target" and int(f[2]) == 5 and
             (int(f[3]), int(f[4])) == K and int(f[5]) == parked_legal[k])
        gate(f"{k}.legal_supply", int(supply[K]["legal"]) == parked_legal[k])
        # geometry and policy
        board = Board(11)
        mask = mask_from_key(*K)
        gate(f"{k}.stone_count", len(board.points(mask)) == 5)
        gate(f"{k}.d4_canonical", board.canonical(mask) == mask)
        legal = board.legal(mask)
        gate(f"{k}.legal_count", len(board.points(legal)) == parked_legal[k])
        gate(f"{k}.policy_canonical_safe", is_canonical_safe_s5_key(K))
        gate(f"{k}.quarantine_absent", K not in qkeys)
        gate(f"{k}.base_absent", K not in base_vals)
        gate(f"{k}.my_class_child", K in my_children)
        # baseline parked reproduction (fresh this session, 15M single run)
        rb = read_replay(RAW / f"base15m-{lo}-{hi}.out.csv")
        gate(f"{k}.base15m_row", len(rb) == 1 and rb[0]["budget"] == 15_000_000
             and (rb[0]["key_lo"], rb[0]["key_hi"]) == K)
        gate(f"{k}.base15m_parked_reproduced", rb[0]["result"] == 0 and rb[0]["nodes"] == 15_000_000)
        # ladder 50M twice
        r1 = read_replay(RAW / f"l50m-run1-{lo}-{hi}.out.csv")
        r2 = read_replay(RAW / f"l50m-run2-{lo}-{hi}.out.csv")
        for tag, rr in (("run1", r1), ("run2", r2)):
            gate(f"{k}.{tag}_row", len(rr) == 1 and rr[0]["budget"] == 50_000_000
                 and (rr[0]["key_lo"], rr[0]["key_hi"]) == K
                 and rr[0]["stones"] == 5 and rr[0]["is_or"] == 0)
            gate(f"{k}.{tag}_form", rr[0]["result"] in (0, 1, 2) and 0 < rr[0]["nodes"] <= 50_000_000
                 and (rr[0]["result"] != 0 or rr[0]["nodes"] == 50_000_000))
        gate(f"{k}.determinism", (r1[0]["result"], r1[0]["nodes"]) == (r2[0]["result"], r2[0]["nodes"]))
        # optional budget-margin re-proof (different budget, same deterministic search):
        # for a resolved key any budget >= proof-completion node count must return the
        # exact same (result, nodes); for a parked key the file must simply park.
        margin_info = None
        mpath = RAW / f"l50m-margin-{lo}-{hi}.out.csv"
        if mpath.exists():
            rm = read_replay(mpath)
            gate(f"{k}.margin_row", len(rm) == 1 and (rm[0]["key_lo"], rm[0]["key_hi"]) == K
                 and rm[0]["budget"] < 50_000_000
                 and (rm[0]["result"] != 0 or rm[0]["nodes"] == rm[0]["budget"]))
            if r1[0]["result"] != 0:
                gate(f"{k}.margin_determinism",
                     rm[0]["budget"] >= rm[0]["nodes"] and
                     (rm[0]["result"], rm[0]["nodes"]) == (r1[0]["result"], r1[0]["nodes"]))
            margin_info = {"budget": rm[0]["budget"], "result": rm[0]["result"], "nodes": rm[0]["nodes"]}
        if r1[0]["result"] == 1:
            win = k
        elif r1[0]["result"] == 2:
            done.append(k)
        else:
            parked50.append(k)
        per_key[k] = {"stages": {"base15m": {"result": rb[0]["result"], "nodes": rb[0]["nodes"]},
                                 "at50m": {"result": r1[0]["result"], "nodes": r1[0]["nodes"]},
                                 "at50m_run2": {"result": r2[0]["result"], "nodes": r2[0]["nodes"]}},
                      "verdict": {1: "WIN", 2: "LOSS", 0: "UNKNOWN@50M"}[r1[0]["result"]],
                      "legal": parked_legal[k]}
        if margin_info is not None:
            per_key[k]["stages"]["margin_reproof"] = margin_info
    gate("batch_complete", len(done) + len(parked50) + (1 if win else 0) == 2)

    if win is not None:
        # ---- stopping rule 1: WIN halts the batch before consumption ----
        # No OK audit, no cache row, no adoption. Record the halted state with
        # every non-verdict gate already passed, plus a NOT-ADOPTED if-adopted
        # scenario for scrutiny owners (reconciliation-lane precedent).
        hyp_vals = dict(base_vals)
        for k in done + [win]:
            lo, hi = k.split(":")
            hyp_vals[(int(lo), int(hi))] = 1 if k == win else 2
        ch = classes_with(hyp_vals)
        class_after_hyp = ch[MY_CLASS]
        status_changes_hyp = []
        cb_all = classes_with(base_vals)
        for kk in cb_all:
            if cb_all[kk]["status"] != ch[kk]["status"]:
                status_changes_hyp.append({"key": list(kk), "before": cb_all[kk]["status"],
                                           "after": ch[kk]["status"], "coverage": cb_all[kk]["coverage"]})
        halt = {
            "schema": "n11-class-parked2-l50m-ladder-halt-audit-v1",
            "all_gates_pass_before_halt": True,
            "halted_on_win": win,
            "gates_passed_count": len(gates),
            "title": ("third-cost class 1297036830122704896:0 parked-2-keys S5 L50M ladder HALTED on WIN "
                      f"at key {win} (stopping rule 1): 1 WIN + {len(done)} LOSS raw recorded, no verdict consumed, "
                      "no cache row, no class/root claim"),
            "pins": {"jsreplay_sha256": sha(P["jsrelay"]),
                     "independent_geometry_python_sha256": sha(P["indep"]),
                     "geometry_sha256": sha(GEOMETRY),
                     "base_chain_cache_sha256": sha(BASE_CACHE),
                     "parent_probe_audit_sha256": sha(PARENT_AUDIT),
                     "quarantine_sha256": sha(QUARANTINE),
                     "supply_sha256": sha(SUPPLY),
                     "policy_sha256": sha(P["policy"])},
            "probe": {
                "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
                "claimed_keys": MY_KEYS,
                "resolved_loss_raw": sorted(done),
                "win_raw_needing_scrutiny": win,
                "per_key": per_key,
                "determinism": ("all executed stages ran twice-or-more with identical (result, nodes); the WIN key "
                                "completed within budget (nodes < budget), so it is a full df-pn proof, not a truncation; "
                                "a second implementation (the pinned C++ kyouen_dfpn_root.cpp) re-verification is REQUIRED "
                                "before the WIN row may be consumed; this environment has no C++ compiler, so the task is "
                                "handed to the scrutiny owner"),
                "pinned_semantics": ("exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player "
                                     "'proposition: the player who moved FIRST on this line eventually wins'; 5 stones "
                                     "is an AND node, so WIN = first player wins against every second-player reply)"),
            },
            "if_adopted_would_not_adopted_recorded_only": {
                "my_class_after": class_after_hyp,
                "global_status_changes": status_changes_hyp,
                "note": ("NOT adopted by this lane. If scrutiny adopts the raw rows, the class "
                         f"{MY_CLASS[0]}:{MY_CLASS[1]} would become WIN (its coverage "
                         "{47,51,100,108} includes the two remaining third moves 100/108); the root "
                         "impact through the depth-2/depth-1 chain is NOT computed by this lane and "
                         "belongs to the K0414/K0416-lineage owners."),
            },
            "records": {"validation_raw_rows_reproduced": [
                {"tag": t, "row": {"stones": v["stones"], "legal": v["legal"], "is_or": v["is_or"],
                                   "budget": v["budget"], "result": v["result"], "nodes": v["nodes"]}}
                for t, v in val_rows.items()]},
            "status_guard": ("halted evidence only; NO verdict is consumed; the 11x11 empty board, the two-stone "
                             "root {60,27}, and third moves 100/108 remain UNKNOWN; nodes and proxy values are "
                             "never verdicts; no cache file is published from this lane while halted"),
        }
        (EXP / "output" / "halt-audit.json").write_text(
            json.dumps(halt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ALL {len(gates)} PRE-WIN GATES PASS -> HALTED ON WIN {win}")
        print(f"loss_raw={sorted(done)} parked50m={parked50}")
        print("halt-audit.json written; no OK audit, no cache file")
        sys.exit(2)

    # ---- merged cache increment on the chain base ----
    merged_path = None
    merged_sha = None
    if done:
        new_rows = []
        for k in done:
            lo, hi = k.split(":")
            nodes = per_key[k]["stages"]["at50m"]["nodes"]
            new_rows.append((int(lo), int(hi), 2, nodes))
        conflict = [(lo, hi) for lo, hi, v, _ in new_rows
                    if (lo, hi) in base_vals and base_vals[(lo, hi)] != v]
        gate("no_conflict_with_base", not conflict, f"{conflict}")
        gate("no_duplicate_new", len(set((lo, hi) for lo, hi, _, _ in new_rows)) == len(new_rows))
        lines = dict(base_rowmap)
        for lo, hi, v, nodes in new_rows:
            gate(f"merge_new_absent_{lo}_{hi}", (lo, hi) not in lines)
            lines[(lo, hi)] = f"s5verdict,{lo},{hi},5,{v},{nodes}"
        out_lines = [base_header] + [lines[k] for k in sorted(lines)]
        merged_path = EXP / "output" / "merged-exact-s5-after-parked2-l50m.cache"
        merged_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        gate("base_byte_preserved",
             all(lines[k] == base_rowmap[k] for k in base_keys),
             "base rows must appear verbatim (incl. original nodes fields)")
        hdr_n, new_rowmap = read_cache_rows(merged_path)
        new_keys = sorted(new_rowmap)
        gate("merge_exactly_done",
             set(new_keys) - set(base_keys) == set((int(k.split(":")[0]), int(k.split(":")[1])) for k in done)
             and len(new_keys) == len(base_keys) + len(done))
        gate("new_sorted", new_keys == sorted(new_keys))
        merged_sha = sha(merged_path)
    gate("parked50_no_rows", all((int(k.split(":")[0]), int(k.split(":")[1])) not in
                                 (read_cache_rows(merged_path)[1] if merged_path else {}) for k in parked50))

    # ---- class recomputation on the frozen geometry ----
    merged_vals = dict(base_vals)
    if merged_path:
        _, m_rowmap = read_cache_rows(merged_path)
        merged_vals = {k: int(m_rowmap[k].split(",")[4]) for k in m_rowmap}

    cb = classes_with(base_vals)
    cn = classes_with(merged_vals)
    gate("my_class_before", cb[MY_CLASS]["status"] == BASE_CLASS_BEFORE["status"]
         and cb[MY_CLASS]["unknown"] == BASE_CLASS_BEFORE["unknown"]
         and cb[MY_CLASS]["loss"] == BASE_CLASS_BEFORE["loss"])
    gate("my_class_after", cn[MY_CLASS]["status"] == "UNKNOWN"
         and cn[MY_CLASS]["unknown"] == 63 - len(done)
         and cn[MY_CLASS]["loss"] == 44 + len(done),
         f"{cn[MY_CLASS]}")
    status_changes = []
    for k in cb:
        if cb[k]["status"] != cn[k]["status"]:
            status_changes.append({"key": list(k), "before": cb[k]["status"],
                                   "after": cn[k]["status"], "coverage": cb[k]["coverage"]})
    gate("no_candidate_closes",
         not [k for k in cb if {100, 108} & set(cb[k]["coverage"])
          and cb[k]["status"] == "UNKNOWN" and cn[k]["status"] == "LOSS"])
    secured_b = {v for k in cb if cb[k]["status"] == "LOSS" for v in cb[k]["coverage"]}
    secured_n = {v for k in cn if cn[k]["status"] == "LOSS" for v in cn[k]["coverage"]}
    gate("secured_unchanged", secured_b == secured_n)
    third = {v for k in cb for v in cb[k]["coverage"]}
    gate("remaining_third_moves_unchanged", third - secured_n == {100, 108})
    counts_b, counts_n = {}, {}
    for k in cb:
        counts_b[cb[k]["status"]] = counts_b.get(cb[k]["status"], 0) + 1
        counts_n[cn[k]["status"]] = counts_n.get(cn[k]["status"], 0) + 1
    gate("status_changes_only_recorded",
         counts_b.get("WIN") == counts_n.get("WIN") and
         counts_n.get("LOSS", 0) - counts_b.get("LOSS", 0) == len(status_changes))

    audit = {
        "schema": "n11-class-parked2-l50m-ladder-audit-v1",
        "all_gates_pass": True,
        "title": ("third-cost class 1297036830122704896:0 parked-2-keys S5 L50M ladder: "
                  f"{len(done)} LOSS / {len(parked50)} UNKNOWN@50M / {1 if win else 0} WIN of 2 claimed keys"),
        "gates_passed_count": len(gates),
        "pins": {"jsreplay_sha256": sha(P["jsrelay"]),
                 "independent_geometry_python_sha256": sha(P["indep"]),
                 "geometry_sha256": sha(GEOMETRY),
                 "base_chain_cache_sha256": sha(BASE_CACHE),
                 "parent_probe_audit_sha256": sha(PARENT_AUDIT),
                 "quarantine_sha256": sha(QUARANTINE),
                 "supply_sha256": sha(SUPPLY),
                 "policy_sha256": sha(P["policy"])},
        "validation": {
            "published_raw_rows_reproduced": [
                {"tag": t, "row": {"stones": v["stones"], "legal": v["legal"], "is_or": v["is_or"],
                                   "budget": v["budget"], "result": v["result"], "nodes": v["nodes"]}}
                for t, v in val_rows.items()],
            "rule": "stones/legal/is_or/budget/result/nodes must match the published C++ raw rows; wall_s may differ",
        },
        "probe": {
            "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
            "claimed_keys": MY_KEYS,
            "resolved_loss": sorted(done),
            "parked_unknown_50m": sorted(parked50),
            "win": win,
            "pinned_semantics": "exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player)",
            "evidence_class": ("replica solver-trusted exact, node-exact against all four published C++ raw "
                               "rows and the parent probe's parked@15M baseline; NOT terminal-only minimax"),
            "per_key": per_key,
            "determinism": ("every 50M stage executed twice with identical (result, nodes); baseline 15M "
                            "parked state reproduced fresh (result 0, nodes 15,000,000)"),
        },
        "class_recomputation": {
            "before": cb[MY_CLASS], "after": cn[MY_CLASS],
            "parent_parked_keys": parent["probe"]["parked_unknown_15m"],
            "global_status_changes": status_changes,
            "status_counts_before": counts_b, "status_counts_after": counts_n,
            "merged_increment_sha256": merged_sha,
        },
        "status_guard": ("evidence increment only; the 11x11 empty board, the two-stone root {60,27}, "
                         "and third moves 100/108 remain UNKNOWN; nodes and proxy values are never "
                         "verdicts; the class keeps at least 61 unproven shared children and is NOT closed"),
    }
    out_path.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ALL {len(gates)} GATES PASS")
    print(f"loss={len(done)} parked50m={parked50} win={win}")
    print(f"class: {cb[MY_CLASS]['unknown']}->{cn[MY_CLASS]['unknown']} unknown")
    print(f"status_changes={[(c['key'], c['before'], c['after']) for c in status_changes]}")
    if merged_path:
        print("new merged cache sha256:", merged_sha)


def parent_audit_order(parent):
    # legal map from the parent probe audit's per_key section
    return [{"key": k, "legal": v["legal"]} for k, v in parent["probe"]["per_key"].items()]


if __name__ == "__main__":
    main()
