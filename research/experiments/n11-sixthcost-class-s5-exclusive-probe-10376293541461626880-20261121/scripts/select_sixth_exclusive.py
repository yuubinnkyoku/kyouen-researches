#!/usr/bin/env python3
"""Sixth-cost class exclusive single-live-parent S5 probe: fail-closed batch selector.

Selects the 43 exclusive (single-live-parent) S5 keys of the sixth-cost
candidate class `10376293541461626880:65536` (coverage {80, 84, 100, 108};
proxy_total rank 6 in the published class-closure-priority measurement; all of
the top-5 classes' exclusive keys are claimed by other lanes: focus-class
35, certificate-class 38, third-cost 39, fourth-cost 41, fifth-cost 44), under
the frozen 3,384-class geometry and the reply27 probe-13 merged exact chain
cache, cross-checked against the latest published increment base (the
third-cost lane merged cache, sha256 bb4495e0...).

Every gate is fail-closed. The machine list written to
`output/sixth-cost-exclusive-keys.json` (field `exclusive_probe_order`) is
authoritative; the prose enumeration in the single-owner declaration is
secondary and any discrepancy aborts the probe part.

This is a scheduling/selection artifact only: no verdict is claimed or
implied. Nodes and proxy values are never evidence of WIN or LOSS.
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
sys.path.insert(0, str(ROOT / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys  # noqa: E402

GEOMETRY = ROOT / 'research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz'
PROBE13 = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121'
CACHE = PROBE13 / 'output/merged-exact-s5-after-js-probe-13.cache'
SUPPLY = PROBE13 / 'output/post-probe/shared-s5-tasks.csv'
LEDGER = PROBE13 / 'output/post-probe/candidate-classes.csv'
PROFILE = ROOT / 'research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json'
CCP = ROOT / 'research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv'
QUARANTINE = ROOT / 'results/n11-s5-evidence-quarantine.json'
# latest published chain increment (base + third-cost 37 LOSS rows)
TCCACHE = ROOT / 'research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/merged-exact-s5-after-class-excl-1.cache'
KEYMAP = ROOT / 'research/experiments/n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json'
FIFTHKEYS = ROOT / 'research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/output/fifth-cost-exclusive-keys.json'

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
PROFILE_SHA = "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc"
CCP_SHA = "139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87"
KEYMAP_SHA = "0aa054c829b912afa10c56ccf62fa6ae5f3bec6bcf932a46b157565baa9d552a"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
TCCACHE_SHA = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
FIFTHKEYS_SHA = "2d7d3a9db62f10acd144dd096ebd2e624698c2057f0f963d177e516296965380"

SIXTH_CLASS = (10376293541461626880, 65536)
FOCUS_CLASS, CERT_CLASS = "1188950301626859520:536870912", "1297036692683752448:0"
THIRD_CLASS, FOURTH_CLASS = "1297036830122704896:0", "1297107061427929088:0"
FIFTH_CLASS = "1152921504612089856:536870912"

# ---- concurrent-lane fixed claims (machine-read from published pinned sources;
# ---- NO manual transcription, per the lane publication protocol) ----
# The focus-35 / cert-38 / third-39 / fourth-41 claim lists are the very lists
# published (and gate-checked) inside the fifth-cost lane's selector; they are
# extracted here by ast from that pinned source. The parked-2 keys of the S5 L50M
# ladder lane are read from that lane's pinned batch input CSVs. The fifth-44
# list is read from the published fifth-cost machine list JSON; the sbd 101
# targets from the published keymap JSON. Every source is sha256-pinned above.
import ast as _ast

FIFTHSEL = ROOT / 'research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/scripts/select_fifth_exclusive.py'  # noqa: E402
FIFTHSEL_SHA = "af68af3c9c9567487727161905e2622b35fd3e3724c5986d5186098a53324cc3"
LADDER_B1 = ROOT / 'research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-1297036830122704896-67108864.input.csv'
LADDER_B1_SHA = "8e530240731fea53d3655ca218ed3aa055d02928273035b56a825e1fb3161ca1"
LADDER_B2 = ROOT / 'research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-10376294091217440768-33554432.input.csv'
LADDER_B2_SHA = "d22df157dbb9ccde348e280b26fabb5aa68deeea0ceaa7ae845758cde4b7c63b"


def _extract_declared_list(source_text, name):
    """Return the list literal assigned to `name` in the module.

    Handles both plain list literals and `sorted([...])` declarations, as
    published in the fifth-cost selector source.
    """
    def literal(node):
        if isinstance(node, _ast.List):
            return _ast.literal_eval(node)
        if (isinstance(node, _ast.Call) and isinstance(node.func, _ast.Name)
                and node.func.id == "sorted" and len(node.args) == 1):
            return _ast.literal_eval(node.args[0])
        fail(f"unsupported literal form for {name}: {type(node).__name__}")
        return None

    tree = _ast.parse(source_text)
    for node in tree.body:
        if isinstance(node, _ast.Assign):
            for t in node.targets:
                if isinstance(t, _ast.Name) and t.id == name:
                    return literal(node.value)
    fail(f"list {name} not found in pinned fifth-cost selector")
    return None


FOCUS_35 = THIRD_39 = CERT_38 = FOURTH_41 = PARKED_2 = None  # loaded in main()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(msg):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


gates = []


def gate(name, ok, detail=""):
    if not ok:
        fail(f"{name} {detail}")
    gates.append(name)


def read_cache(p):
    cache = {}
    for row in csv.reader(Path(p).open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            fail(f"unexpected cache row {row}")
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            fail(f"verdict conflict in cache {k}")
        cache[k] = v
    return cache


def main():
    for path, want in [(GEOMETRY, GEOMETRY_SHA), (CACHE, CACHE_SHA), (SUPPLY, SUPPLY_SHA),
                       (LEDGER, LEDGER_SHA), (PROFILE, PROFILE_SHA), (CCP, CCP_SHA),
                       (QUARANTINE, QUARANTINE_SHA), (TCCACHE, TCCACHE_SHA),
                       (KEYMAP, KEYMAP_SHA), (FIFTHKEYS, FIFTHKEYS_SHA),
                       (FIFTHSEL, FIFTHSEL_SHA), (LADDER_B1, LADDER_B1_SHA),
                       (LADDER_B2, LADDER_B2_SHA)]:
        gate(f"pin_{Path(path).name}", sha(Path(path)) == want, f"{path}")

    global FOCUS_35, CERT_38, THIRD_39, FOURTH_41, PARKED_2
    src = FIFTHSEL.read_text(encoding="utf-8")
    FOCUS_35 = sorted(_extract_declared_list(src, "FOCUS_35"))
    CERT_38 = sorted(_extract_declared_list(src, "CERT_38"))
    THIRD_39 = sorted(_extract_declared_list(src, "THIRD_39"))
    FOURTH_41 = sorted(_extract_declared_list(src, "FOURTH_41"))
    # PARKED_2 from the L50M ladder lane's pinned batch inputs (key_lo/key_hi fields 4/5).
    def ladder_key(p):
        row = next(r for r in csv.reader(p.open(encoding="utf-8", newline=""))
                   if r and not r[0].startswith("#"))
        if row[0] != "target" or int(row[2]) != 5:
            fail(f"unexpected ladder input row {row}")
        return f"{row[3]}:{row[4]}"
    PARKED_2 = sorted([ladder_key(LADDER_B1), ladder_key(LADDER_B2)])

    # embedded lists: sizes and mutual sanity
    gate("claim_list_sizes",
         [len(FOCUS_35), len(CERT_38), len(THIRD_39), len(FOURTH_41), len(PARKED_2)] == [35, 38, 39, 41, 2])
    for nm, s in [("focus", FOCUS_35), ("cert", CERT_38), ("third", THIRD_39),
                  ("fourth", FOURTH_41), ("parked", PARKED_2)]:
        if len(set(s)) != len(s):
            fail(f"{nm} machine-read list has duplicates")
    keymap = json.loads(KEYMAP.read_text(encoding="utf-8"))
    sbd = sorted({f"{v[0]}:{v[1]}" for v in keymap["targets"].values()})
    gate("sbd_101", len(sbd) == 101)
    f5 = json.loads(FIFTHKEYS.read_text(encoding="utf-8"))
    fifth44 = sorted(r["key"] for r in f5["exclusive_probe_order"])
    gate("fifth44_size", len(fifth44) == 44 and len(set(fifth44)) == 44)
    gate("fifth44_schema", f5["class"] == FIFTH_CLASS)

    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("geometry_size", len(geo) == 3384)
    cache = read_cache(CACHE)
    gate("p13_rows", len(cache) == 5756)
    tc = read_cache(TCCACHE)
    gate("tc_rows", len(tc) == 5793)
    gate("tc_minus_p13", len(set(tc) - set(cache)) == 37)
    gate("tc_conflicts", all(tc[k] == cache[k] for k in set(tc) & set(cache)))

    def stage(vals):
        if 1 in vals:
            return "WIN"
        if all(v == 2 for v in vals):
            return "LOSS"
        return "UNKNOWN"

    active = []
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        vals = [cache.get(z, 0) for z in ch]
        if {100, 108}.intersection(g["coverage"]):
            active.append((tuple(g["key"]), g["coverage"], ch, stage(vals)))
    gate("candidates_115", len(active) == 115)
    live_classes = [c for c in active if c[3] == "UNKNOWN"]
    gate("live_62", len(live_classes) == 62)

    live_par = defaultdict(set)
    for k, cov, ch, st in live_classes:
        for child in ch:
            if child not in cache:
                live_par[child].add(k)
    supply = {}
    for row in csv.DictReader(SUPPLY.open(newline="")):
        supply[(int(row["key"].split(":")[0]), int(row["key"].split(":")[1]))] = row
    gate("supply_matches_live", set(supply) == set(live_par) and len(supply) == 4562)
    deg = defaultdict(int)
    for child in live_par:
        deg[len(live_par[child])] += 1
    gate("supply_degree_dist", dict(deg) == {1: 2688, 2: 1874})

    # ---- sixth-cost class membership and exclusivity -------------------------
    sk = next(c for c in live_classes if tuple(c[0]) == SIXTH_CLASS)
    unk = sorted(c for c in sk[2] if c not in cache)
    excl = [c for c in unk if live_par[c] == {SIXTH_CLASS}]
    gate("sixth_children_108", len(sk[2]) == 108)
    gate("sixth_unknown_101", len(unk) == 101)
    gate("sixth_exclusive_43", len(excl) == 43)
    gate("sixth_shared_58", len(unk) - len(excl) == 58)
    # cross-check against the latest chain increment (third-cost merged cache)
    unk_tc = sorted(c for c in sk[2] if c not in tc)
    gate("tc_no_sixth_overlap", len(unk_tc) == 101 and set(unk) == set(unk_tc))

    # published measurement cross-check (sixth row of the published 62-row table)
    pub = list(csv.DictReader(CCP.open(newline="")))
    gate("published_rows_62", len(pub) == 62)
    pub_row = next(r for r in pub if r["key"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")
    gate("pub_row_children", int(pub_row["s5_children"]) == 108)
    gate("pub_row_unknown", int(pub_row["s5_unknown"]) == 101)
    gate("pub_row_exclusive", int(pub_row["unknown_exclusive"]) == 43)
    gate("pub_row_shared", int(pub_row["unknown_shared"]) == 58)
    gate("pub_row_proxy_total", int(pub_row["proxy_total"]) == 559872854)
    def proxy(c):
        return int(supply[c]["truncated_cost_proxy_nodes"])
    gate("proxy_exclusive_sum", sum(proxy(c) for c in excl) == int(pub_row["proxy_exclusive_sum"]) == 229056664)
    gate("proxy_total_recomputed", sum(proxy(c) for c in unk) == int(pub_row["proxy_total"]))
    # class rank 6 by proxy_total; top-6 = the five other claimed classes + this one
    ranked = sorted(pub, key=lambda r: (int(r["proxy_total"]), r["key"]))
    gate("sixth_rank_6", ranked[5]["key"] == f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}")
    gate("top5_claimed", {r["key"] for r in ranked[:5]} ==
         {FOCUS_CLASS, CERT_CLASS, THIRD_CLASS, FOURTH_CLASS, FIFTH_CLASS})

    # ---- ordering, disjointness, absence -------------------------------------
    order_keys = sorted(excl, key=lambda c: (proxy(c), c))
    gate("order_43", len(order_keys) == 43)
    bands = defaultdict(list)
    for c in order_keys:
        bands[proxy(c)].append(c)
    gate("bands", {k: len(v) for k, v in bands.items()} == {5041585: 12, 5234938: 22, 5932112: 9})

    mine = [f"{c[0]}:{c[1]}" for c in order_keys]
    mset = set(mine)
    for name, s in [("focus", FOCUS_35), ("cert", CERT_38), ("third", THIRD_39),
                    ("fourth", FOURTH_41), ("parked2", PARKED_2),
                    ("fifth44", fifth44), ("sbd", sbd)]:
        gate(f"disjoint_{name}", not (mset & set(s)),
             str(sorted(mset & set(s))[:5]))
    gate("disjoint_union_all",
         not (mset & (set(FOCUS_35) | set(CERT_38) | set(THIRD_39) | set(FOURTH_41)
                      | set(PARKED_2) | set(fifth44) | set(sbd))))

    qkeys = quarantined_cache_keys()  # fails closed if registry missing/corrupt
    gate("quarantine_absent", not (mset & {f"{k[0]}:{k[1]}" for k in qkeys}))
    gate("base_cache_absent", not (mset & {f"{k[0]}:{k[1]}" for k in cache}))
    gate("tc_cache_absent", not (mset & {f"{k[0]}:{k[1]}" for k in tc}))

    # ---- independent geometry pre-check over the whole batch ------------------
    board = Board(11)
    rows = []
    for c in order_keys:
        mask = mask_from_key(*c)
        pts = board.points(mask)
        gate(f"stones_{c}", len(pts) == 5)
        gate(f"d4_{c}", board.canonical(mask) == mask)
        legal_mask = board.legal(mask)  # raises if unsafe
        derived = len(board.points(legal_mask))
        supply_legal = int(supply[c]["legal"])
        gate(f"legal_{c}", derived == supply_legal, f"derived {derived} supply {supply_legal}")
        gate(f"safe_{c}", is_canonical_safe_s5_key(c))
        rows.append({"key": f"{c[0]}:{c[1]}", "legal": supply_legal, "proxy": proxy(c)})

    ledger = {r["key"]: r for r in csv.DictReader(LEDGER.open(newline=""))}
    lr = ledger[f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}"]
    gate("ledger_unknown", int(lr["s5_unknown"]) == 101)
    gate("ledger_shared", int(lr["s5_unknown_shared_with_other_live_classes"]) == 58)
    gate("ledger_loss", int(lr["s5_loss"]) == 7 and int(lr["s5_win"]) == 0)

    out = {
        "schema": "n11-sixthcost-exclusive-selection-v1",
        "class": f"{SIXTH_CLASS[0]}:{SIXTH_CLASS[1]}",
        "coverage": sorted(sk[1]),
        "class_children_total": 108,
        "s5_unknown_before": 101,
        "unknown_exclusive": 43,
        "unknown_shared": 58,
        "proxy_total": int(pub_row["proxy_total"]),
        "proxy_exclusive_sum": 229056664,
        "proxy_shared_sum": int(pub_row["proxy_shared_sum"]),
        "bin_prior_all_loss_index": float(pub_row["bin_prior_all_loss_index"]),
        "exclusive_probe_order": rows,
        "bands_proxy_to_count": {str(k): len(v) for k, v in sorted(bands.items())},
        "concurrent_claims_respected": {
            "focus_35": len(FOCUS_35), "cert_38": len(CERT_38),
            "third_39": len(THIRD_39), "fourth_41": len(FOURTH_41),
            "fifth_44": len(fifth44), "sbd_101": len(sbd), "parked_2": len(PARKED_2),
        },
        "gates_passed": gates,
        "status_guard": ("Selection and scheduling only; no verdict is claimed. The standard 11x11 "
                         "empty board, the two-stone root {60,27}, and its remaining third moves "
                         "100/108 remain UNKNOWN."),
    }
    tmp = EXP / "output" / "sixth-cost-exclusive-keys.json.tmp"
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.rename(EXP / "output" / "sixth-cost-exclusive-keys.json")

    # per-key batch inputs, k01..k43 ascending (proxy, key)
    for i, c in enumerate(order_keys, start=1):
        (EXP / "input" / f"k{i:02d}.input.csv").write_text(
            f"target,0,5,{c[0]},{c[1]},{int(supply[c]['legal'])},0,0,0,0,0\n", encoding="utf-8")

    print(json.dumps({"all_gates_pass": True, "gates": len(gates),
                      "exclusive_keys": 43,
                      "proxy_exclusive_sum": 229056664}))


if __name__ == "__main__":
    main()
