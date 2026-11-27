"""Twelfth-cost class exclusive single-live-parent S5 probe: fail-closed batch selector.

Adaptive-coordinator next selection after the eleventh-cost k01
canonical adoption closed the eleventh-cost batch stage-1 sweep
(1 row adopted: 1 WIN k01, canonical head of record 1e2eeda2...,
6,890 rows WIN 208 / LOSS 6,682, flip-census + reaudit refresh
published in kit n11-eleventhcost-k01-adoption-reaudit-20261127).

Selects, from the published class-closure-priority measurement (62 live
candidate classes ranked by proxy_total under the frozen 3,384-class geometry
and the probe-13 cache), the next candidate class whose exclusive
(single-live-parent) S5 keys are not claimed by any concurrent lane: the top-11
ranks are the focus-35 / cert-38 / third-39 / fourth-41 / fifth-44 /
sixth-43 / seventh-42 / eighth-43 / ninth-45 / tenth-44 / eleventh-46 claimed
classes, so the coordinator's next selection starts at rank 12. The class is
then re-validated against the CURRENT canonical head of record (the
eleventh-cost k01 merged cache 1e2eeda2...), which supersedes the probe-13 +
seventh-cost + eighth-cost + ninth-cost + tenth-cost + eleventh-cost basis of
the published priority table: live classes, unknown children and exclusivity
are recomputed under the head, fail-closed.  The eleventh-cost serving class
1297036696978718720:0 is now excluded_now under the head (a measured win-hit
flip of the eleventh-cost adoption reaudit), so it cannot be re-selected; its
46 exclusive keys and the shared keys of its batch stay claimed by the
eleventh lane and excluded here.

Every gate is fail-closed. The machine list written to
output/twelfth-cost-exclusive-keys.json (field exclusive_probe_order) is
authoritative; any prose enumeration is secondary and any discrepancy aborts.

This is a scheduling/selection artifact only: no verdict is claimed or implied.
Nodes and proxy values are never evidence of WIN or LOSS. The standard 11x11
empty board, the two-stone root {60,27} and its remaining third moves 100/108
stay UNKNOWN.
"""
from __future__ import annotations

import ast as _ast
import csv
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("/home/user/repo")
EXP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
from independent import Board, mask_from_key  # noqa: E402
sys.path.insert(0, str(ROOT / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys  # noqa: E402

GEOMETRY = ROOT / 'research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz'
SUPPLY = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/shared-s5-tasks.csv'
LEDGER = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/candidate-classes.csv'
CCP = ROOT / 'research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv'
QUARANTINE = ROOT / 'results/n11-s5-evidence-quarantine.json'
P13CACHE = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache'
HEAD = ROOT / 'research/experiments/n11-eleventhcost-k01-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache'
NINTHKEYS = ROOT / 'research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127/output/ninth-cost-exclusive-keys.json'
TENTHKEYS = ROOT / 'research/experiments/n11-tenthcost-class-s5-exclusive-probe-20261127/output/tenth-cost-exclusive-keys.json'
ELEVENTHKEYS = ROOT / 'research/experiments/n11-eleventhcost-class-s5-exclusive-probe-20261127/output/eleventh-cost-exclusive-keys.json'
KEYMAP = ROOT / 'research/experiments/n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json'
FIFTHKEYS = ROOT / 'research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/output/fifth-cost-exclusive-keys.json'
SIXTHKEYS = ROOT / 'research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/sixth-cost-exclusive-keys.json'
SEVENTHKEYS = ROOT / 'research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/seventh-cost-exclusive-keys.json'
EIGHTHKEYS = ROOT / 'research/experiments/n11-eighthcost-class-s5-exclusive-probe-1297036692750860288-20261127/output/eighth-cost-exclusive-keys.json'

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
CCP_SHA = "139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
P13_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
HEAD_SHA = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"
NINTHKEYS_SHA = "772c9235fe226e9b52a36a6860ef2096a099a3be374daf0b80de21ee81bd4568"
TENTHKEYS_SHA = "3d0f791effe78d73697f8f627ab0111e1c58e7fefbc154d99935e5a6d9a3ba6e"
ELEVENTHKEYS_SHA = "5a29b5be27430eb0f19221234b7d001a92a7f02be577a30d169c5e011da14bd5"
KEYMAP_SHA = "0aa054c829b912afa10c56ccf62fa6ae5f3bec6bcf932a46b157565baa9d552a"
FIFTHKEYS_SHA = "2d7d3a9db62f10acd144dd096ebd2e624698c2057f0f963d177e516296965380"
SIXTHKEYS_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"
SEVENTHKEYS_SHA = "c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627"
EIGHTHKEYS_SHA = "691dcd807d52b9b9dbe0118f2347db9a613565377350246fda53a6c518aeef33"

FOCUS_CLASS, CERT_CLASS = "1188950301626859520:536870912", "1297036692683752448:0"
THIRD_CLASS, FOURTH_CLASS = "1297036830122704896:0", "1297107061427929088:0"
FIFTH_CLASS = "1152921504612089856:536870912"
SIXTH_CLASS = "10376293541461626880:65536"
SEVENTH_CLASS = "1306043891938492416:0"
EIGHTH_CLASS = "1297036692750860288:0"
NINTH_CLASS = "1297036692683751424:134217728"
TENTH_CLASS = "1297036692683751424:131072"
ELEVENTH_CLASS = "1297036696978718720:0"

# concurrent-lane claim sources (machine-read from published pinned sources)
FIFTHSEL = ROOT / 'research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/scripts/select_fifth_exclusive.py'
FIFTHSEL_SHA = "af68af3c9c9567487727161905e2622b35fd3e3724c5986d5186098a53324cc3"
LADDER_B1 = ROOT / 'research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-1297036830122704896-67108864.input.csv'
LADDER_B1_SHA = "8e530240731fea53d3655ca218ed3aa055d02928273035b56a825e1fb3161ca1"
LADDER_B2 = ROOT / 'research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-10376294091217440768-33554432.input.csv'
LADDER_B2_SHA = "d22df157dbb9ccde348e280b26fabb5aa68deeea0ceaa7ae845758cde4b7c63b"
PARKED4_DIR = ROOT / 'research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/input'
JSREPLAY = EXP / 'scripts/jsreplay.js'
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"


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


def _extract_declared_list(source_text, name):
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


def read_cache(p, name):
    cache = {}
    win = loss = 0
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
        if v == 1:
            win += 1
        else:
            loss += 1
    return cache, win, loss


def stage(vals):
    if 1 in vals:
        return "WIN"
    if all(v == 2 for v in vals):
        return "LOSS"
    return "UNKNOWN"


def ladder_key(p):
    row = next(r for r in csv.reader(Path(p).open(encoding="utf-8", newline=""))
               if r and not r[0].startswith("#"))
    if row[0] != "target" or int(row[2]) != 5:
        fail(f"unexpected ladder input row {row}")
    return f"{row[3]}:{row[4]}"


def main():
    for path, want in [(GEOMETRY, GEOMETRY_SHA), (SUPPLY, SUPPLY_SHA), (LEDGER, LEDGER_SHA),
                       (CCP, CCP_SHA), (QUARANTINE, QUARANTINE_SHA), (P13CACHE, P13_SHA),
                       (HEAD, HEAD_SHA), (KEYMAP, KEYMAP_SHA), (FIFTHKEYS, FIFTHKEYS_SHA),
                       (SIXTHKEYS, SIXTHKEYS_SHA), (SEVENTHKEYS, SEVENTHKEYS_SHA),
                       (EIGHTHKEYS, EIGHTHKEYS_SHA), (NINTHKEYS, NINTHKEYS_SHA), (TENTHKEYS, TENTHKEYS_SHA),
                       (ELEVENTHKEYS, ELEVENTHKEYS_SHA), (FIFTHSEL, FIFTHSEL_SHA),
                       (LADDER_B1, LADDER_B1_SHA), (LADDER_B2, LADDER_B2_SHA),
                       (JSREPLAY, JSREPLAY_SHA)]:
        gate(f"pin_{Path(path).name}", sha(path) == want, f"{path}")

    # ---- machine-read concurrent-lane claim sets -----------------------------
    src = FIFTHSEL.read_text(encoding="utf-8")
    FOCUS_35 = sorted(_extract_declared_list(src, "FOCUS_35"))
    CERT_38 = sorted(_extract_declared_list(src, "CERT_38"))
    THIRD_39 = sorted(_extract_declared_list(src, "THIRD_39"))
    FOURTH_41 = sorted(_extract_declared_list(src, "FOURTH_41"))
    PARKED_2 = sorted([ladder_key(LADDER_B1), ladder_key(LADDER_B2)])
    parked4_files = sorted(PARKED4_DIR.glob("batch-k*.input.csv"))
    gate("parked4_files", len(parked4_files) == 4, str(parked4_files))
    PARKED_4 = sorted(ladder_key(p) for p in parked4_files)
    keymap = json.loads(KEYMAP.read_text(encoding="utf-8"))
    sbd = sorted({f"{v[0]}:{v[1]}" for v in keymap["targets"].values()})
    gate("sbd_101", len(sbd) == 101)
    f5 = json.loads(FIFTHKEYS.read_text(encoding="utf-8"))
    fifth44 = sorted(r["key"] for r in f5["exclusive_probe_order"])
    gate("fifth44_size", len(fifth44) == 44 and len(set(fifth44)) == 44)
    gate("fifth44_schema", f5["class"] == FIFTH_CLASS)
    f6 = json.loads(SIXTHKEYS.read_text(encoding="utf-8"))
    sixth43 = sorted(r["key"] for r in f6["exclusive_probe_order"])
    gate("sixth43_size", len(sixth43) == 43 and len(set(sixth43)) == 43)
    gate("sixth43_schema", f6["schema"] == "n11-sixthcost-exclusive-selection-v1"
         and f6["class"] == SIXTH_CLASS)
    f7 = json.loads(SEVENTHKEYS.read_text(encoding="utf-8"))
    seventh42 = sorted(r["key"] for r in f7["exclusive_probe_order"])
    gate("seventh42_size", len(seventh42) == 42 and len(set(seventh42)) == 42)
    gate("seventh42_schema", f7["schema"] == "n11-seventhcost-exclusive-selection-v1"
         and f7["class"] == SEVENTH_CLASS)
    f8 = json.loads(EIGHTHKEYS.read_text(encoding="utf-8"))
    eighth43 = sorted(r["key"] for r in f8["exclusive_probe_order"])
    gate("eighth43_size", len(eighth43) == 43 and len(set(eighth43)) == 43)
    gate("eighth43_schema", f8["schema"] == "n11-eighthcost-exclusive-selection-v1"
         and f8["class"] == EIGHTH_CLASS)
    f9 = json.loads(NINTHKEYS.read_text(encoding="utf-8"))
    ninth45 = sorted(r["key"] for r in f9["exclusive_probe_order"])
    gate("ninth45_size", len(ninth45) == 45 and len(set(ninth45)) == 45)
    gate("ninth45_schema", f9["schema"] == "n11-ninthcost-exclusive-selection-v1"
         and f9["class"] == NINTH_CLASS)
    f10 = json.loads(TENTHKEYS.read_text(encoding="utf-8"))
    tenth44 = sorted(r["key"] for r in f10["exclusive_probe_order"])
    gate("tenth44_size", len(tenth44) == 44 and len(set(tenth44)) == 44)
    gate("tenth44_schema", f10["schema"] == "n11-tenthcost-exclusive-selection-v1"
         and f10["class"] == TENTH_CLASS)
    f11 = json.loads(ELEVENTHKEYS.read_text(encoding="utf-8"))
    eleventh46 = sorted(r["key"] for r in f11["exclusive_probe_order"])
    gate("eleventh46_size", len(eleventh46) == 46 and len(set(eleventh46)) == 46)
    gate("eleventh46_schema", f11["schema"] == "n11-eleventhcost-exclusive-selection-v1"
         and f11["class"] == ELEVENTH_CLASS)
    gate("parked4_subset_sixth43", set(PARKED_4) <= set(sixth43))
    gate("parked2_claim_sizes", [len(FOCUS_35), len(CERT_38), len(THIRD_39),
                                 len(FOURTH_41), len(PARKED_2)] == [35, 38, 39, 41, 2])
    for nm, s in [("focus", FOCUS_35), ("cert", CERT_38), ("third", THIRD_39),
                  ("fourth", FOURTH_41), ("parked", PARKED_2), ("sixth", sixth43)]:
        if len(set(s)) != len(s):
            fail(f"{nm} machine-read list has duplicates")
    CLAIMED_CLASSES = {FOCUS_CLASS, CERT_CLASS, THIRD_CLASS, FOURTH_CLASS,
                       FIFTH_CLASS, SIXTH_CLASS, SEVENTH_CLASS, EIGHTH_CLASS,
                       NINTH_CLASS, TENTH_CLASS, ELEVENTH_CLASS}
    claim_union = set(FOCUS_35) | set(CERT_38) | set(THIRD_39) | set(FOURTH_41) \
        | set(PARKED_2) | set(fifth44) | set(sbd) | set(sixth43) | set(seventh42) \
        | set(eighth43) | set(ninth45) | set(tenth44) | set(eleventh46)

    # ---- caches --------------------------------------------------------------
    p13, p13w, p13l = read_cache(P13CACHE, "p13")
    gate("p13_rows", len(p13) == 5756)
    head, hw, hl = read_cache(HEAD, "head")
    gate("head_rows", len(head) == 6890 and [hw, hl] == [208, 6682], f"{len(head)} {hw} {hl}")
    gate("p13_subset_head", set(p13) <= set(head)
         and all(head[k] == p13[k] for k in set(p13) & set(head)))

    # ---- geometry, live classes under the CURRENT head ----------------------
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("geometry_size", len(geo) == 3384)
    active = []
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        vals = [head.get(z, 0) for z in ch]
        if {100, 108}.intersection(g["coverage"]):
            active.append((tuple(g["key"]), g["coverage"], ch, stage(vals)))
    gate("candidates_115", len(active) == 115)
    live_classes = [c for c in active if c[3] == "UNKNOWN"]
    gate("live_nonempty", len(live_classes) >= 1, str(len(live_classes)))

    live_par = defaultdict(set)
    for k, cov, ch, st in live_classes:
        for child in ch:
            if child not in head:
                live_par[child].add(k)
    supply = {}
    for row in csv.DictReader(SUPPLY.open(newline="")):
        supply[(int(row["key"].split(":")[0]), int(row["key"].split(":")[1]))] = row
    gate("supply_covers_live_par", set(live_par) <= set(supply),
         f"missing {sorted(set(live_par) - set(supply))[:3]}")

    # ---- coordinator next selection: first unclaimed live rank ---------------
    pub = list(csv.DictReader(CCP.open(newline="")))
    gate("published_rows_62", len(pub) == 62)
    ranked = sorted(pub, key=lambda r: (int(r["proxy_total"]), r["key"]))
    gate("top11_claimed", {r["key"] for r in ranked[:11]} == CLAIMED_CLASSES,
         str({r["key"] for r in ranked[:11]}))

    sel = None
    for r in ranked[11:]:
        if r["key"] in CLAIMED_CLASSES:
            continue
        cand = next((c for c in live_classes if f"{c[0][0]}:{c[0][1]}" == r["key"]), None)
        if cand is None:
            continue
        unk = sorted(c for c in cand[2] if c not in head)
        excl = [c for c in unk if live_par[c] == {cand[0]}]
        if excl:
            sel = (r, cand, unk, excl)
            break
    if sel is None:
        fail("no unclaimed live candidate class with exclusive unknown children")
    pub_row, sc, unk, excl = sel
    TWELFTH = sc[0]
    gate("selection_rank12", pub_row["key"] == f"{TWELFTH[0]}:{TWELFTH[1]}"
         and ranked[11]["key"] == pub_row["key"], pub_row["key"])

    def proxy(c):
        return int(supply[c]["truncated_cost_proxy_nodes"])

    order_keys = sorted(excl, key=lambda c: (proxy(c), c))
    bands = defaultdict(list)
    for c in order_keys:
        bands[proxy(c)].append(c)
    mine = [f"{c[0]}:{c[1]}" for c in order_keys]
    mset = set(mine)
    for name, s in [("focus", FOCUS_35), ("cert", CERT_38), ("third", THIRD_39),
                    ("fourth", FOURTH_41), ("parked2", PARKED_2), ("parked4", PARKED_4),
                    ("fifth44", fifth44), ("sbd", sbd), ("sixth43", sixth43),
                    ("seventh42", seventh42), ("eighth43", eighth43),
                    ("ninth45", ninth45), ("tenth44", tenth44), ("eleventh46", eleventh46)]:
        gate(f"disjoint_{name}", not (mset & set(s)), str(sorted(mset & set(s))[:5]))
    qkeys = quarantined_cache_keys()
    gate("quarantine_absent", not (mset & {f"{k[0]}:{k[1]}" for k in qkeys}))
    gate("head_absent", not (mset & {f"{k[0]}:{k[1]}" for k in head}))
    gate("mine_unique", len(mset) == len(mine))

    # ---- independent geometry pre-check over the whole batch -----------------
    board = Board(11)
    rows = []
    for c in order_keys:
        mask = mask_from_key(*c)
        pts = board.points(mask)
        gate(f"stones_{c}", len(pts) == 5)
        gate(f"d4_{c}", board.canonical(mask) == mask)
        legal_mask = board.legal(mask)
        derived = len(board.points(legal_mask))
        supply_legal = int(supply[c]["legal"])
        gate(f"legal_{c}", derived == supply_legal, f"derived {derived} supply {supply_legal}")
        gate(f"safe_{c}", is_canonical_safe_s5_key(c))
        rows.append({"key": f"{c[0]}:{c[1]}", "legal": supply_legal, "proxy": proxy(c)})

    # ledger is frozen at probe-13 time: cross-check only its historical fields
    ledger = {r["key"]: r for r in csv.DictReader(LEDGER.open(newline=""))}
    lr = ledger[f"{TWELFTH[0]}:{TWELFTH[1]}"]
    gate("ledger_children", int(lr["s5_children"]) == int(pub_row["s5_children"]))
    gate("pub_row_children", int(pub_row["s5_children"]) == len(sc[2]))

    unk_head = len(unk)
    shared = unk_head - len(excl)
    out = {
        "schema": "n11-twelfthcost-exclusive-selection-v1",
        "class": f"{TWELFTH[0]}:{TWELFTH[1]}",
        "coverage": sorted(sc[1]),
        "class_children_total": len(sc[2]),
        "s5_unknown_before_head": unk_head,
        "unknown_exclusive_head": len(excl),
        "unknown_shared_head": shared,
        "head_basis": {
            "path": "research/experiments/n11-eleventhcost-k01-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache",
            "sha256": HEAD_SHA,
            "rows": 6890, "win": 208, "loss": 6682,
        },
        "published_priority_row_probe13_basis": {
            "s5_children": int(pub_row["s5_children"]),
            "s5_unknown": int(pub_row["s5_unknown"]),
            "unknown_exclusive": int(pub_row["unknown_exclusive"]),
            "unknown_shared": int(pub_row["unknown_shared"]),
            "proxy_total": int(pub_row["proxy_total"]),
            "proxy_exclusive_sum": int(pub_row["proxy_exclusive_sum"]),
            "proxy_shared_sum": int(pub_row["proxy_shared_sum"]),
            "bin_prior_all_loss_index": float(pub_row["bin_prior_all_loss_index"]),
        },
        "proxy_exclusive_sum_head": sum(proxy(c) for c in excl),
        "exclusive_probe_order": rows,
        "bands_proxy_to_count": {str(k): len(v) for k, v in sorted(bands.items())},
        "concurrent_claims_respected": {
            "focus_35": len(FOCUS_35), "cert_38": len(CERT_38),
            "third_39": len(THIRD_39), "fourth_41": len(FOURTH_41),
            "fifth_44": len(fifth44), "sbd_101": len(sbd),
            "parked_2": len(PARKED_2), "parked_4": len(PARKED_4),
            "sixth_43": len(sixth43),
            "seventh_42": len(seventh42),
            "eighth_43": len(eighth43),
            "ninth_45": len(ninth45),
            "tenth_44": len(tenth44),
            "eleventh_46": len(eleventh46),
        },
        "gates_passed": gates,
        "status_guard": ("Selection and scheduling only; no verdict is claimed. The standard "
                         "11x11 empty board, the two-stone root {60,27}, and its remaining "
                         "third moves 100/108 remain UNKNOWN."),
    }
    tmp = EXP / "output" / "twelfth-cost-exclusive-keys.json.tmp"
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.rename(EXP / "output" / "twelfth-cost-exclusive-keys.json")

    for i, c in enumerate(order_keys, start=1):
        (EXP / "input" / f"k{i:02d}.input.csv").write_text(
            f"target,0,5,{c[0]},{c[1]},{int(supply[c]['legal'])},0,0,0,0,0\n", encoding="utf-8")

    print(json.dumps({"all_gates_pass": True, "gates": len(gates),
                      "class": out["class"], "coverage": out["coverage"],
                      "exclusive_keys": len(excl),
                      "unknown_before_head": unk_head,
                      "shared_head": shared,
                      "proxy_exclusive_sum_head": out["proxy_exclusive_sum_head"],
                      "bands": out["bands_proxy_to_count"]}, indent=1))


if __name__ == "__main__":
    main()
