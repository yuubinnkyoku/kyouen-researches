#!/usr/bin/env python3
"""Win-finding if-adopted analysis for the k03 resumption checkpoint (fail-closed).

Reads this lane's own checkpoint raw rows (k01, k02 from the parent batch, k03
from the resumption batch), enforces the ladder and determinism gates, and
computes machine-checked IF-ADOPTED scenarios against the pinned published
chain cache base (probe-13 base + third-cost increment, sha256 bb4495e0...):

  scenario A: only the fresh k03 WIN row is adopted;
  scenario B: all three unconsumed batch rows (k01 LOSS, k02 WIN, k03 WIN).

Neither scenario is adopted by this script; verdicts are NOT consumed. Every
WIN row follows the exclusive-probe program's WIN-row precedent: adoption
requires a second-implementation (C++) verification of the published replica
raw, which this sandbox cannot run (no C++ toolchain; re-verified).

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
CACHE = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache'
TCCACHE = ROOT / 'research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/merged-exact-s5-after-class-excl-1.cache'
CCP = ROOT / 'research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv'
SELECTOR_OUT = EXP / 'output/sixth-cost-exclusive-keys.json'
RAW = EXP / 'output/raw'

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
TCCACHE_SHA = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
CCP_SHA = "139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87"
SIXTH_CLASS = (10376293541461626880, 65536)
LOSS_KEY_1 = (1297036692683751424, 1114112)   # k01 (parent batch)
WIN_KEY_1 = (1297036692683751424, 68157440)   # k02 (parent batch)
WIN_KEY_2 = (10376293541461626880, 65792)     # k03 (resumption batch)
FLIP_CLASS_A2 = (1297319267171041280, 0)      # {48, 50, 80, 84}
FLIP_CLASS_B2 = (1297037792211107840, 0)      # {24, 30, 80, 84}
MEMBER_CLASS_WIN_ALREADY = (1297036692683751424, 64)  # base stage WIN (84 unknown children)


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


def stage_changes(geo, base, sc):
    out = []
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        s0 = stage([base.get(z, 0) for z in ch])
        s1 = stage([sc.get(z, 0) for z in ch])
        if s0 != s1:
            out.append((tuple(g["key"]), sorted(g["coverage"]), s0, s1))
    return out


def main():
    for path, want in [(GEOMETRY, GEOMETRY_SHA), (CACHE, CACHE_SHA), (TCCACHE, TCCACHE_SHA), (CCP, CCP_SHA)]:
        gate(f"pin_{Path(path).name}", sha(Path(path)) == want, f"{path}")
    sel = json.loads(SELECTOR_OUT.read_text(encoding="utf-8"))
    gate("selector_class", sel["class"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")
    keys_in_order = [tuple(int(x) for x in r["key"].split(":")) for r in sel["exclusive_probe_order"]]
    gate("order_k01", keys_in_order[0] == LOSS_KEY_1)
    gate("order_k02", keys_in_order[1] == WIN_KEY_1)
    gate("order_k03", keys_in_order[2] == WIN_KEY_2)
    gate("order_43", len(keys_in_order) == 43)
    legal = {tuple(int(x) for x in r["key"].split(":")): r["legal"] for r in sel["exclusive_probe_order"]}
    proxy = {tuple(int(x) for x in r["key"].split(":")): r["proxy"] for r in sel["exclusive_probe_order"]}
    for k in (LOSS_KEY_1, WIN_KEY_1, WIN_KEY_2):
        gate(f"proxy_band1_{k[0]%97}_{k[1]%89}", proxy[k] == 5041585, str(proxy[k]))

    # ---- this lane's own raw rows: ladder + determinism gates ----------------
    r1_2m = replay_row(RAW / "at2m-k01.out.csv")
    r1_a = replay_row(RAW / "at15m-run1-k01.out.csv")
    r1_b = replay_row(RAW / "at15m-run2-k01.out.csv")
    r2_2m = replay_row(RAW / "at2m-k02.out.csv")
    r2_a = replay_row(RAW / "at15m-run1-k02.out.csv")
    r2_b = replay_row(RAW / "at15m-run2-k02.out.csv")
    r2_c = replay_row(RAW / "at15m-run3-verify-k02.out.csv")
    r3_2m = replay_row(RAW / "at2m-k03.out.csv")
    r3_a = replay_row(RAW / "at15m-run1-k03.out.csv")
    r3_b = replay_row(RAW / "at15m-run2-k03.out.csv")
    r3_c = replay_row(RAW / "at15m-run3-verify-k03.out.csv")
    for nm, rr, k in [("k01_2m", r1_2m, LOSS_KEY_1), ("k01_a", r1_a, LOSS_KEY_1), ("k01_b", r1_b, LOSS_KEY_1),
                      ("k02_2m", r2_2m, WIN_KEY_1), ("k02_a", r2_a, WIN_KEY_1), ("k02_b", r2_b, WIN_KEY_1),
                      ("k02_c", r2_c, WIN_KEY_1), ("k03_2m", r3_2m, WIN_KEY_2), ("k03_a", r3_a, WIN_KEY_2),
                      ("k03_b", r3_b, WIN_KEY_2), ("k03_c", r3_c, WIN_KEY_2)]:
        gate(f"stones5_{nm}", rr["stones"] == 5)
        gate(f"legal_{nm}", rr["legal"] == legal[k], f"{rr['legal']}")
        gate(f"isor0_{nm}", rr["is_or"] == 0 and rr["id"] == 0)
        gate(f"key_{nm}", (rr["key_lo"], rr["key_hi"]) == k)
    gate("k01_2m_unknown", r1_2m["result"] == 0 and r1_2m["budget"] == 2000000 and r1_2m["nodes"] == 2000000)
    gate("k02_2m_unknown", r2_2m["result"] == 0 and r2_2m["budget"] == 2000000 and r2_2m["nodes"] == 2000000)
    gate("k03_2m_unknown", r3_2m["result"] == 0 and r3_2m["budget"] == 2000000 and r3_2m["nodes"] == 2000000)
    gate("k01_15m_pair", r1_a["budget"] == 15000000 and (r1_a["result"], r1_a["nodes"]) == (2, 10369650)
         and (r1_b["result"], r1_b["nodes"]) == (2, 10369650))
    gate("k02_15m_pair", r2_a["budget"] == 15000000 and (r2_a["result"], r2_a["nodes"]) == (1, 7717432)
         and (r2_b["result"], r2_b["nodes"]) == (1, 7717432))
    gate("k02_extra_recheck", (r2_c["result"], r2_c["nodes"]) == (1, 7717432) and r2_c["budget"] == 15000000)
    gate("k03_15m_pair", r3_a["budget"] == 15000000 and (r3_a["result"], r3_a["nodes"]) == (1, 9255414)
         and (r3_b["result"], r3_b["nodes"]) == (1, 9255414))
    gate("k03_extra_recheck", (r3_c["result"], r3_c["nodes"]) == (1, 9255414) and r3_c["budget"] == 15000000)
    for nm, rr in [("k01", r1_a), ("k02", r2_a), ("k03", r3_a)]:
        gate(f"{nm}_nodes_within_budget", 0 < rr["nodes"] <= 15000000)

    # independent geometry re-verification of the three fresh keys
    board = Board(11)
    for nm, k in [("k01", LOSS_KEY_1), ("k02", WIN_KEY_1), ("k03", WIN_KEY_2)]:
        mask = mask_from_key(*k)
        gate(f"{nm}_stones", len(board.points(mask)) == 5)
        gate(f"{nm}_d4", board.canonical(mask) == mask)
        gate(f"{nm}_legal", len(board.points(board.legal(mask))) == legal[k])

    # ---- base census ----------------------------------------------------------
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("geometry_size", len(geo) == 3384)
    base = read_cache(TCCACHE)
    gate("base_rows", len(base) == 5793)
    for row in read_cache(CACHE).items():
        gate_row = base.get(row[0]) == row[1]
        if not gate_row:
            die(f"probe13 base not embedded in chain tip at {row[0]}")
    secured0, cand0, counts0 = census(geo, base)
    gate("base_live_62", sum(1 for c in cand0 if c[3] == "UNKNOWN") == 62)
    gate("base_secured_117", len(secured0) == 117 and {100, 108} - secured0 == {100, 108})
    gate("base_none_loss_candidate", sum(1 for c in cand0 if c[3] == "LOSS") == 0)
    gate("base_census_counts", dict(counts0) == {"UNKNOWN": 3081, "WIN": 272, "LOSS": 31}, str(dict(counts0)))
    for k in (LOSS_KEY_1, WIN_KEY_1, WIN_KEY_2):
        gate(f"no_base_conflict_{k[1]%97}", k not in base)
    gate("member_class_win_already", stage([base.get(z, 0) for z in
        {tuple(z) for z in next(g for g in geo if tuple(g["key"]) == MEMBER_CLASS_WIN_ALREADY)["children"]}]) == "WIN"
        and sum(1 for c in {tuple(z) for z in next(g for g in geo if tuple(g["key"]) == MEMBER_CLASS_WIN_ALREADY)["children"]} if c not in base) == 84)

    sixth = next(g for g in geo if tuple(g["key"]) == SIXTH_CLASS)
    sixth_ch = {tuple(z) for z in sixth["children"]}
    gate("sixth_base_unknown", stage([base.get(z, 0) for z in sixth_ch]) == "UNKNOWN")
    gate("sixth_unknown_101", sum(1 for c in sixth_ch if c not in base) == 101)
    for k in (WIN_KEY_1, WIN_KEY_2, LOSS_KEY_1):
        gate(f"sixth_member_{k[1]%83}", k in sixth_ch)

    # exclusivity re-check under the base cache: only the sixth class is a live parent
    for nm, k in [("win2", WIN_KEY_2), ("win1", WIN_KEY_1)]:
        live_par = {tuple(c[0]) for c in cand0 if c[3] == "UNKNOWN" and k in {tuple(z) for z in c[2]}}
        gate(f"{nm}_exclusive_live_parent", live_par == {SIXTH_CLASS}, str(live_par))

    # ---- scenario A: adopt only the fresh k03 WIN row --------------------------
    scA = dict(base)
    scA[WIN_KEY_2] = 1
    securedA, candA, countsA = census(geo, scA)
    changesA = stage_changes(geo, base, scA)
    gate("A_changes_two", len(changesA) == 2, str(changesA))
    gate("A_all_to_win", all(c[3] == "WIN" and c[2] == "UNKNOWN" for c in changesA))
    gate("A_flip_set", {c[0] for c in changesA} == {FLIP_CLASS_A2, SIXTH_CLASS})
    gate("A_sixth_win", stage([scA.get(z, 0) for z in sixth_ch]) == "WIN")
    gate("A_sixth_unknown_100", sum(1 for c in sixth_ch if c not in scA) == 100)
    gate("A_secured_unchanged", securedA == secured0)
    gate("A_remaining_unchanged", {100, 108} - securedA == {100, 108})
    gate("A_live_61", sum(1 for c in candA if c[3] == "UNKNOWN") == 61)
    gate("A_counts", dict(countsA) == {"UNKNOWN": 3079, "WIN": 274, "LOSS": 31}, str(dict(countsA)))
    sixth_A = next(c for c in candA if tuple(c[0]) == SIXTH_CLASS)

    # ---- scenario B: adopt all three unconsumed batch rows ---------------------
    scB = dict(base)
    scB[LOSS_KEY_1] = 2
    scB[WIN_KEY_1] = 1
    scB[WIN_KEY_2] = 1
    securedB, candB, countsB = census(geo, scB)
    changesB = stage_changes(geo, base, scB)
    gate("B_changes_three", len(changesB) == 3, str(changesB))
    gate("B_all_to_win", all(c[3] == "WIN" and c[2] == "UNKNOWN" for c in changesB))
    gate("B_flip_set", {c[0] for c in changesB} == {FLIP_CLASS_A2, FLIP_CLASS_B2, SIXTH_CLASS})
    gate("B_sixth_win", stage([scB.get(z, 0) for z in sixth_ch]) == "WIN")
    gate("B_sixth_unknown_98", sum(1 for c in sixth_ch if c not in scB) == 98)
    gate("B_secured_unchanged", securedB == secured0)
    gate("B_remaining_unchanged", {100, 108} - securedB == {100, 108})
    gate("B_live_61", sum(1 for c in candB if c[3] == "UNKNOWN") == 61)
    gate("B_counts", dict(countsB) == {"UNKNOWN": 3078, "WIN": 275, "LOSS": 31}, str(dict(countsB)))

    # full-class membership of the fresh keys
    mem3 = sorted(tuple(g["key"]) for g in geo if WIN_KEY_2 in {tuple(z) for z in g["children"]})
    gate("k03_membership_three", mem3 == sorted([MEMBER_CLASS_WIN_ALREADY, FLIP_CLASS_A2, SIXTH_CLASS]), str(mem3))
    mem1 = sorted(tuple(g["key"]) for g in geo if LOSS_KEY_1 in {tuple(z) for z in g["children"]})
    gate("k01_membership_three", len(mem1) == 3 and SIXTH_CLASS in mem1)
    mem2 = sorted(tuple(g["key"]) for g in geo if WIN_KEY_1 in {tuple(z) for z in g["children"]})
    gate("k02_membership_three", len(mem2) >= 2 and SIXTH_CLASS in mem2 and FLIP_CLASS_B2 in mem2)

    pub = list(csv.DictReader(CCP.open(newline="")))
    gate("published_rows_62", len(pub) == 62)
    pub_row = next(r for r in pub if r["key"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")
    gate("pub_row_children_108", int(pub_row["s5_children"]) == 108)
    gate("pub_row_unknown_101", int(pub_row["s5_unknown"]) == 101)

    def mech(key, verdict, nodes):
        return (f"fresh replica verdict {verdict} on child {key[0]}:{key[1]} (result {verdict}, "
                f"nodes {nodes}, identical cold replays at budget 15,000,000)")

    out = {
        "schema": "n11-sixthcost-win-finding-ifadopted-k03-v1",
        "finding": {
            "kind": "fresh replica WIN on an exclusive child of the sixth-cost candidate class (resumption batch k03)",
            "win_child_key": f"{WIN_KEY_2[0]}:{WIN_KEY_2[1]}",
            "win_child_class": f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}",
            "win_runs": [{"budget": r["budget"], "result": r["result"], "nodes": r["nodes"]}
                         for r in (r3_2m, r3_a, r3_b, r3_c)],
            "extra_recheck_run": "at15m-run3-verify-k03.out.csv (voluntary third cold replay, identical result and nodes)",
            "ladder": "2M unknown -> 15M WIN on all runs; determinism pair + voluntary third cold run identical (result 1, nodes 9,255,414)",
            "batch_state": ("halted after k03 per the pre-registered WIN stopping rule (resumption session); "
                            "k04..k43 not started this session; parent batch rows k01/k02 still unconsumed"),
            "verdict_consumed": False,
            "adoption_requirement": ("second-implementation (C++) verification of the published replica raw rows, "
                                     "per the exclusive-probe WIN-row precedent; no C++ toolchain in this sandbox "
                                     "(re-verified); any later C++ disagreement fails closed in favor of discarding the row. "
                                     "C++ targets: target,0,5,10376293541461626880,65792,81,0,0,0,0,0 @15,000,000 "
                                     "(expected result 1, nodes 9,255,414); plus the k01/k02 rows as published "
                                     "(k01 expected 2 / 10,369,650; k02 expected 1 / 7,717,432). The concurrent "
                                     "third-implementation re-verification (declared 20:45Z) is additional evidence only; "
                                     "its declared targets did not include k03 and extend only with a new declaration."),
        },
        "unconsumed_batch_rows": [
            {"key": f"{LOSS_KEY_1[0]}:{LOSS_KEY_1[1]}", "verdict": 2, "nodes": r1_a["nodes"], "source": "parent batch k01"},
            {"key": f"{WIN_KEY_1[0]}:{WIN_KEY_1[1]}", "verdict": 1, "nodes": r2_a["nodes"], "source": "parent batch k02"},
            {"key": f"{WIN_KEY_2[0]}:{WIN_KEY_2[1]}", "verdict": 1, "nodes": r3_a["nodes"], "source": "resumption batch k03"},
        ],
        "base_pins": {"geometry_sha256": GEOMETRY_SHA,
                      "probe13_base_sha256": CACHE_SHA,
                      "chain_increment_base_sha256": TCCACHE_SHA,
                      "class_closure_priority_sha256": CCP_SHA,
                      "base_rows": len(base)},
        "base_snapshot": {
            "class_census": dict(counts0),
            "candidate_classes": len(cand0), "live_unknown": 62,
            "secured_third_moves": len(secured0), "remaining_third_moves": sorted({100, 108} - secured0),
            "sixth_class_unknown_children": 101,
        },
        "if_adopted_k03_only": {
            "status_changes": [
                {"class": f"{c[0][0]}:{c[0][1]}", "coverage": c[1], "before": c[2], "after": c[3],
                 "mechanism": mech(WIN_KEY_2, 1, r3_a["nodes"]), "verdict_consumed": False}
                for c in changesA],
            "sixth_class_children_unknown_after": 100,
            "live_unknown_after": 61,
            "secured_third_moves_after": len(securedA),
            "candidate_pool_delta": "-1 (the sixth-cost class is WIN-eliminated as a route; the flipped non-candidate class 1297319267171041280:0 covers {48, 50, 80, 84}; not a coverage event)",
        },
        "if_adopted_all_three_unconsumed_batch_rows": {
            "status_changes": [
                {"class": f"{c[0][0]}:{c[0][1]}", "coverage": c[1], "before": c[2], "after": c[3],
                 "mechanism": (mech(WIN_KEY_1, 1, r2_a["nodes"]) if c[0] == FLIP_CLASS_B2
                               else mech(WIN_KEY_2, 1, r3_a["nodes"]) if c[0] == FLIP_CLASS_A2
                               else mech(WIN_KEY_2, 1, r3_a["nodes"]) + " (with the sibling fresh WIN k02 also in the scenario)"),
                 "verdict_consumed": False}
                for c in changesB],
            "sixth_class_children_unknown_after": 98,
            "live_unknown_after": 61,
            "secured_third_moves_after": len(securedB),
            "remaining_third_moves_after": sorted({100, 108} - securedB),
            "note": ("the sixth-cost class would be WIN with TWO fresh WIN children (k02, k03); both scenarios leave "
                      "secured third-move coverage unchanged at 117/119 with {100, 108} remaining; neither is a "
                      "coverage event or a route to the root certificate"),
        },
        "k03_full_class_membership": [
            {"class": f"{MEMBER_CLASS_WIN_ALREADY[0]}:{MEMBER_CLASS_WIN_ALREADY[1]}", "note": "base stage WIN already (84 unknown children) - no flip"},
            {"class": f"{FLIP_CLASS_A2[0]}:{FLIP_CLASS_A2[1]}", "note": "NON-candidate class, coverage {48, 50, 80, 84}, flips UNKNOWN->WIN"},
            {"class": f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}", "note": "the exclusive live-parent candidate class, flips UNKNOWN->WIN"},
        ],
        "class_bin_prior_all_loss_index_published": float(pub_row["bin_prior_all_loss_index"]),
        "gates_passed": gates,
        "status_guard": ("If-adopted machine scenarios only; NOT adopted; no verdict consumed. The standard "
                         "11x11 empty board, the two-stone root {60,27}, and its remaining third moves "
                         "100/108 remain UNKNOWN. Nodes and budgets are never verdicts."),
    }
    tmp = EXP / "output" / "win-finding-ifadopted-k03.json.tmp"
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.rename(EXP / "output" / "win-finding-ifadopted-k03.json")
    print(json.dumps({"all_gates_pass": True, "gates": len(gates),
                      "live_after_A": 61, "secured_after": len(securedA)}))


if __name__ == "__main__":
    main()
