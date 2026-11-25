#!/usr/bin/env python3
"""Win-finding if-adopted analysis for the sixth-cost class probe batch (fail-closed).

Reads this lane's own checkpoint raw rows (k01, k02), enforces the ladder and
determinism gates, and computes the machine-checked IF-ADOPTED scenario: what
would change, against the pinned published chain cache base (probe-13 base +
third-cost increment, sha256 bb4495e0...), IF this lane's two fresh rows were
adopted into the S5 verdict cache. The scenario is NOT adopted by this script;
verdicts are NOT consumed. The WIN row follows the exclusive-probe program's
WIN-row precedent: adoption requires a second-implementation (C++) verification
of the published replica raw, which this sandbox cannot run (no C++ toolchain).

No verdict is created here. 11x11, {60,27}, third moves 100/108 remain UNKNOWN.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
ROOT = EXP.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
from independent import Board, mask_from_key  # noqa: E402

GEOMETRY = ROOT / 'research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz'
PROBE13 = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121'
CACHE = PROBE13 / 'output/merged-exact-s5-after-js-probe-13.cache'
TCCACHE = ROOT / 'research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/merged-exact-s5-after-class-excl-1.cache'
CCP = ROOT / 'research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv'
SELECTOR_OUT = EXP / 'output/sixth-cost-exclusive-keys.json'
RAW = EXP / 'output/raw'
inputs = EXP / 'input'

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
TCCACHE_SHA = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
SIXTH_CLASS = (10376293541461626880, 65536)
LOSS_KEY_1 = (1297036692683751424, 1114112)   # k01
WIN_KEY_1 = (1297036692683751424, 68157440)   # k02


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def die(msg):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


gates = []


def gate(name, ok, detail=""):
    if not ok:
        die(f"{name} {detail}")
    gates.append(name)


def read_cache(p):
    cache = {}
    for row in csv.reader(Path(p).open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            die(f"unexpected cache row {row}")
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            die(f"verdict conflict in cache {k}")
        cache[k] = v
    return cache


def replay_row(p):
    for r in csv.reader(Path(p).open(encoding="utf-8-sig", newline="")):
        if r and r[0] == "replay":
            return {"id": int(r[1]), "stones": int(r[2]), "legal": int(r[3]),
                    "is_or": int(r[4]), "budget": int(r[5]), "result": int(r[6]),
                    "nodes": int(r[7]), "key_lo": int(r[9]), "key_hi": int(r[10])}
    die(f"no replay row in {p}")
    return None


def stage(vals):
    if 1 in vals:
        return "WIN"
    if all(v == 2 for v in vals):
        return "LOSS"
    return "UNKNOWN"


def census(geo, cache):
    required = {100, 108}
    secured, candidates, counts = set(), [], defaultdict(int)
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        st = stage([cache.get(z, 0) for z in ch])
        counts[st] += 1
        if st == "LOSS":
            secured.update(g["coverage"])
        if required.intersection(g["coverage"]):
            candidates.append((tuple(g["key"]), g["coverage"], ch, st))
    return secured, candidates, counts


def main():
    for path, want in [(GEOMETRY, GEOMETRY_SHA), (CACHE, CACHE_SHA), (TCCACHE, TCCACHE_SHA)]:
        gate(f"pin_{Path(path).name}", sha(Path(path)) == want)
    sel = json.loads(SELECTOR_OUT.read_text(encoding="utf-8"))
    gate("selector_class", sel["class"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")
    keys_in_order = [tuple(int(x) for x in r["key"].split(":")) for r in sel["exclusive_probe_order"]]
    gate("order_k01", keys_in_order[0] == LOSS_KEY_1)
    gate("order_k02", keys_in_order[1] == WIN_KEY_1)
    legal1 = {tuple(int(x) for x in r["key"].split(":")): r["legal"] for r in sel["exclusive_probe_order"]}

    # ---- this lane's own raw rows: ladder + determinism gates ----------------
    r1_2m = replay_row(RAW / "at2m-k01.out.csv")
    r1_a = replay_row(RAW / "at15m-run1-k01.out.csv")
    r1_b = replay_row(RAW / "at15m-run2-k01.out.csv")
    r2_2m = replay_row(RAW / "at2m-k02.out.csv")
    r2_a = replay_row(RAW / "at15m-run1-k02.out.csv")
    r2_b = replay_row(RAW / "at15m-run2-k02.out.csv")
    r2_c = replay_row(RAW / "at15m-run3-verify-k02.out.csv")
    for nm, rr, k in [("k01", r1_2m, LOSS_KEY_1), ("k01a", r1_a, LOSS_KEY_1),
                      ("k01b", r1_b, LOSS_KEY_1), ("k02", r2_2m, WIN_KEY_1),
                      ("k02a", r2_a, WIN_KEY_1), ("k02b", r2_b, WIN_KEY_1),
                      ("k02c", r2_c, WIN_KEY_1)]:
        gate(f"stones5_{nm}", rr["stones"] == 5)
        gate(f"legal_{nm}", rr["legal"] == legal1[k], f"{rr['legal']}")
        gate(f"isor0_{nm}", rr["is_or"] == 0 and rr["id"] == 0)
        gate(f"key_{nm}", (rr["key_lo"], rr["key_hi"]) == k)
    gate("k01_2m_unknown", r1_2m["result"] == 0 and r1_2m["budget"] == 2000000)
    gate("k02_2m_unknown", r2_2m["result"] == 0 and r2_2m["budget"] == 2000000)
    gate("k01_15m_budget", r1_a["budget"] == 15000000 and r1_b["budget"] == 15000000)
    gate("k02_15m_budget", r2_a["budget"] == 15000000 and r2_b["budget"] == 15000000
         and r2_c["budget"] == 15000000)
    gate("k01_determinism_pair", (r1_a["result"], r1_a["nodes"]) == (r1_b["result"], r1_b["nodes"])
         and r1_a["result"] == 2 and r1_a["nodes"] == 10369650)
    gate("k02_determinism_pair", (r2_a["result"], r2_a["nodes"]) == (r2_b["result"], r2_b["nodes"])
         and r2_a["result"] == 1 and r2_a["nodes"] == 7717432)
    gate("k02_extra_recheck_identical", (r2_c["result"], r2_c["nodes"]) == (r2_a["result"], r2_a["nodes"]))
    gate("k01_nodes_within_budget", 0 < r1_a["nodes"] <= 15000000)
    gate("k02_nodes_within_budget", 0 < r2_a["nodes"] <= 15000000)

    # independent geometry re-verification of both fresh keys
    board = Board(11)
    for nm, k in [("k01", LOSS_KEY_1), ("k02", WIN_KEY_1)]:
        mask = mask_from_key(*k)
        gate(f"{nm}_stones", len(board.points(mask)) == 5)
        gate(f"{nm}_d4", board.canonical(mask) == mask)
        gate(f"{nm}_legal", len(board.points(board.legal(mask))) == legal1[k])

    # ---- base and scenario censuses ------------------------------------------
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("geometry_size", len(geo) == 3384)
    base = read_cache(TCCACHE)
    gate("base_rows", len(base) == 5793)
    secured0, cand0, counts0 = census(geo, base)
    gate("base_live_62", sum(1 for c in cand0 if c[3] == "UNKNOWN") == 62)
    gate("base_secured_117", len(secured0) == 117 and {100, 108} - secured0 == {100, 108})
    gate("base_none_loss_candidate", sum(1 for c in cand0 if c[3] == "LOSS") == 0)

    sc = dict(base)
    sc[LOSS_KEY_1] = 2
    sc[WIN_KEY_1] = 1
    gate("scenario_no_base_conflict", LOSS_KEY_1 not in base and WIN_KEY_1 not in base)
    secured1, cand1, counts1 = census(geo, sc)
    live1 = [c for c in cand1 if c[3] == "UNKNOWN"]

    # sixth-cost class statement under both readings
    six_base = next(c for c in cand0 if tuple(c[0]) == SIXTH_CLASS)
    six_scen = next(c for c in cand1 if tuple(c[0]) == SIXTH_CLASS)
    gate("sixth_base_unknown", six_base[3] == "UNKNOWN")
    gate("sixth_scen_win", six_scen[3] == "WIN")
    unk_base = sum(1 for ch in six_base[2] if ch not in base)
    unk_scen = sum(1 for ch in six_scen[2] if ch not in sc)
    gate("sixth_unknown_delta", unk_base - unk_scen == 2 and unk_base == 101 and unk_scen == 99)
    gate("win_child_sixth_member", WIN_KEY_1 in {tuple(z) for z in six_scen[2]})
    gate("loss_child_sixth_member", LOSS_KEY_1 in {tuple(z) for z in six_scen[2]})
    # exclusivity re-check under the base cache: only the sixth class is a live parent
    live_par_w = {tuple(c[0]) for c in cand0 if c[3] == "UNKNOWN" and WIN_KEY_1 in {tuple(z) for z in c[2]}}
    gate("win_exclusive_live_parent", live_par_w == {SIXTH_CLASS}, str(live_par_w))
    live_par_l = {tuple(c[0]) for c in cand0 if c[3] == "UNKNOWN" and LOSS_KEY_1 in {tuple(z) for z in c[2]}}
    gate("loss_exclusive_live_parent", live_par_l == {SIXTH_CLASS}, str(live_par_l))
    # WIN only removes classes from the candidate pool; coverage unchanged
    gate("sec_coverage_unchanged", secured1 == secured0)
    gate("remaining_moves_unchanged", {100, 108} - secured1 == {100, 108})
    gate("live_61", len(live1) == 61)
    # full-class census: the WIN child may also belong to non-candidate classes
    all_changes = []
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        s0 = stage([base.get(z, 0) for z in ch])
        s1 = stage([sc.get(z, 0) for z in ch])
        if s0 != s1:
            all_changes.append((tuple(g["key"]), sorted(g["coverage"]), s0, s1))
    gate("scenario_counts_win_plus_two", counts1["WIN"] == counts0["WIN"] + 2, f"{counts0['WIN']}->{counts1['WIN']}")
    gate("scenario_counts_no_loss", counts1["LOSS"] == counts0["LOSS"])
    gate("scenario_changes_two", len(all_changes) == 2)
    gate("scenario_changes_all_to_win", all(c[3] == "WIN" for c in all_changes))
    win_child_all_classes = sorted(
        tuple(g["key"]) for g in geo
        if WIN_KEY_1 in {tuple(z) for z in g["children"]})
    loss_child_all_classes = sorted(
        tuple(g["key"]) for g in geo
        if LOSS_KEY_1 in {tuple(z) for z in g["children"]})
    status_changes = [
        {"class": f"{c[0][0]}:{c[0][1]}", "coverage": c[1], "before": c[2], "after": c[3],
         "mechanism": f"fresh WIN(1) verdict on child {WIN_KEY_1[0]}:{WIN_KEY_1[1]} (result 1 nodes {r2_a['nodes']}, 2+1 identical cold replays at budget 15,000,000)",
         "verdict_consumed": False}
        for c in all_changes
    ]
    pub = list(csv.DictReader(CCP.open(newline="")))
    pub_row = next(r for r in pub if r["key"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")

    out = {
        "schema": "n11-sixthcost-win-finding-ifadopted-v1",
        "finding": {
            "kind": "fresh replica WIN on an exclusive child of the sixth-cost candidate class",
            "win_child_key": f"{WIN_KEY_1[0]}:{WIN_KEY_1[1]}",
            "win_child_class": f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}",
            "win_runs": [{"budget": r["budget"], "result": r["result"], "nodes": r["nodes"]}
                         for r in (r2_2m, r2_a, r2_b, r2_c)],
            "extra_recheck_run": "at15m-run3-verify-k02.out.csv (voluntary third cold replay, identical result and nodes)",
            "loss_child_key_k01": f"{LOSS_KEY_1[0]}:{LOSS_KEY_1[1]}",
            "loss_runs": [{"budget": r["budget"], "result": r["result"], "nodes": r["nodes"]}
                          for r in (r1_2m, r1_a, r1_b)],
            "batch_state": "halted after k02 per the pre-registered WIN stopping rule; k03..k43 not started this session",
            "verdict_consumed": False,
            "adoption_requirement": ("second-implementation (C++) verification of the published replica raw, "
                                     "per the exclusive-probe WIN-row precedent; no C++ toolchain in this sandbox; "
                                     "any later C++ disagreement fails closed in favor of discarding the row"),
        },
        "base_pins": {"geometry_sha256": GEOMETRY_SHA,
                      "probe13_base_sha256": CACHE_SHA,
                      "chain_increment_base_sha256": TCCACHE_SHA,
                      "base_rows": len(base)},
        "base_snapshot": {
            "candidate_classes": len(cand0), "live_unknown": 62,
            "secured_third_moves": len(secured0), "secured_third_moves_detail": sorted(secured0),
            "remaining_third_moves": sorted({100, 108} - secured0),
            "sixth_class_unknown_children": unk_base,
        },
        "if_adopted_scenario": {
            "adopted_rows": [
                {"key": f"{LOSS_KEY_1[0]}:{LOSS_KEY_1[1]}", "verdict": 2, "nodes": r1_a["nodes"]},
                {"key": f"{WIN_KEY_1[0]}:{WIN_KEY_1[1]}", "verdict": 1, "nodes": r2_a["nodes"]},
            ],
            "status_changes": status_changes,
            "win_child_full_class_membership": [f"{c[0]}:{c[1]}" for c in win_child_all_classes],
            "loss_child_full_class_membership": [f"{c[0]}:{c[1]}" for c in loss_child_all_classes],
            "live_unknown_after": len(live1),
            "candidate_pool_delta": "-1 (the sixth-cost class is WIN-eliminated as a route to a LOSS-complete 100/108-covering class; the second flipped class is a NON-candidate class covering {24, 30, 80, 84}; neither is a coverage event)",
            "secured_third_moves_after": len(secured1),
            "remaining_third_moves_after": sorted({100, 108} - secured1),
            "class_bin_prior_all_loss_index_published": float(pub_row["bin_prior_all_loss_index"]),
        },
        "gates_passed": gates,
        "status_guard": ("If-adopted machine scenario only; NOT adopted; no verdict consumed. The standard "
                         "11x11 empty board, the two-stone root {60,27}, and its remaining third moves "
                         "100/108 remain UNKNOWN. Nodes and budgets are never verdicts."),
    }
    tmp = EXP / "output" / "win-finding-ifadopted.json.tmp"
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.rename(EXP / "output" / "win-finding-ifadopted.json")
    print(json.dumps({"all_gates_pass": True, "gates": len(gates),
                      "live_after": len(live1), "secured_after": len(secured1)}))


if __name__ == "__main__":
    main()
