#!/usr/bin/env python3
"""Fifth-cost class exclusive single-live-parent S5 probe: fail-closed batch selector.

Selects the 44 exclusive (single-live-parent) S5 keys of the fifth-cost
candidate class `1152921504612089856:536870912` (coverage {88, 98, 100, 108};
proxy_total rank 5 in the published class-closure-priority measurement; all of
the top-4 classes' exclusive keys are claimed by other lanes), under the
frozen 3,384-class geometry and the reply27 probe-13 merged exact chain cache.

Every gate is fail-closed. The machine list written to
`output/fifth-cost-exclusive-keys.json` (field `exclusive_probe_order`) is
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

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
PROFILE_SHA = "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc"
CCP_SHA = "139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87"
KEYMAP_SHA = "0aa054c829b912afa10c56ccf62fa6ae5f3bec6bcf932a46b157565baa9d552a"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

FIFTH_CLASS = (1152921504612089856, 536870912)
FOCUS_CLASS, CERT_CLASS = "1188950301626859520:536870912", "1297036692683752448:0"
THIRD_CLASS, FOURTH_CLASS = "1297036830122704896:0", "1297107061427929088:0"

# ---- concurrent-lane fixed claims (embedded; provenance in the declaration) ----
# focus-class exclusive lane (commit aa33434c), 35 keys:
FOCUS_35 = sorted([
    "10376293541461622816:68719476737",
    "10376293545756590112:68719476736",
    "10412322338481635328:536870912",
    "1152921504606851072:536870922",
    "1152921504606851072:536870978",
    "1152921504606851072:536936450",
    "1152921504606851072:537001986",
    "1152921504606851072:553648130",
    "1152921504606851072:570425346",
    "1152921504606851072:603979778",
    "1152921504741064705:68719476738",
    "1152921504741068800:68719476738",
    "1188950301626859520:536870913",
    "1188950301626859520:536870976",
    "1188950301626859520:537001984",
    "1188950301626859520:537133056",
    "1188950301626859520:603979776",
    "1188950301626859520:805306368",
    "1188950301626863616:536870912",
    "1188950301626867712:536870912",
    "1188950301626892288:536870912",
    "1188950301643636736:536870912",
    "1188950302700601344:536870912",
    "1188950305921826816:536870912",
    "1188950310216794112:536870912",
    "1188950576504766464:536870912",
    "1188951401138487296:536870912",
    "1188959097719881728:536870912",
    "1189020670371037184:536870912",
    "1189091039115214848:536870912",
    "1193453901254230016:536870912",
    "1197957500881600512:536870912",
    "1261007895664787456:536870912",
    "1765411053930283008:536870912",
    "5800636320054247424:536870912",
])
# certificate-class exclusive probe lane (ccp Part B, commit 9e4e6f4c), 38 keys:
CERT_38 = sorted([
    "10376293541461626881:131072",
    "10376293541461626881:268435456",
    "10376293541461626881:33554432",
    "10376293541461626881:67108864",
    "10376293541461626881:8",
    "10412322338480590849:0",
    "1152921504607896576:553648128",
    "1152921513197831168:536870912",
    "1152956688979985408:536870912",
    "1224979098645824512:536870912",
    "1297036692683752448:128",
    "1297036692683752448:16",
    "1297036692683752448:16777216",
    "1297036692683752448:32",
    "1297036692683752448:536870912",
    "1297036692683752448:8",
    "1297036692683752449:0",
    "1297036692683752452:0",
    "1297036692683752480:0",
    "1297036692683752576:0",
    "1297036692683752704:0",
    "1297036692683756544:0",
    "1297036692683760640:0",
    "1297036692683785216:0",
    "1297036692683817984:0",
    "1297036692683883520:0",
    "1297036692700529664:0",
    "1297036692817970176:0",
    "1297036761403229184:0",
    "1297036967561659392:0",
    "1297177430172107776:0",
    "1297318167660463104:0",
    "1297599642637173760:0",
    "1369094286721680384:0",
    "1585267068835464192:0",
    "1873497444987175936:0",
    "3602879701897446400:0",
    "5908722711111140352:0",
])
# third-cost class exclusive probe lane (commit 5ec015a0), 39 keys:
THIRD_39 = sorted([
    "10376294091217440768:131072",
    "10376294091217440768:268435456",
    "10376294091217440768:33554432",
    "10376294091217440768:67108864",
    "10376294091217440768:8",
    "10412322888236404736:0",
    "1152921504606851072:536870945",
    "1152921504607895552:553648640",
    "1152930300699873280:536870944",
    "1153062242230468608:68719476736",
    "1161928703861592064:536870944",
    "1297036830122704896:128",
    "1297036830122704896:16",
    "1297036830122704896:16384",
    "1297036830122704896:16777216",
    "1297036830122704896:65536",
    "1297036830122704896:67108864",
    "1297036830122704896:8",
    "1297036830122704897:0",
    "1297036830122704900:0",
    "1297036830122704928:0",
    "1297036830122705152:0",
    "1297036830122708992:0",
    "1297036830122713088:0",
    "1297036830122737664:0",
    "1297036830122770432:0",
    "1297036830122835968:0",
    "1297036830139482112:0",
    "1297036830256922624:0",
    "1297036830391140352:0",
    "1297036831196446720:0",
    "1297037105000611840:0",
    "1297037929634332672:0",
    "1297177567611060224:0",
    "1369094424160632832:0",
    "1585267206274416640:0",
    "1873497582426128384:0",
    "3602879839336398848:0",
    "5908722848550092800:0",
])
# fourth-cost class exclusive probe lane (wave-2 refresh Part C, commit 1f94f501), 41 keys:
FOURTH_41 = sorted([
    "10380797141088997376:131072",
    "10380797141088997376:67108864",
    "10380797141088997376:8",
    "10416825938107961344:0",
    "1152921504606851072:805306369",
    "1152921504607895552:1627389952",
    "1152921504607899648:805306368",
    "1152921504809222144:68719476736",
    "1152930300699873280:805306368",
    "1161928703861592064:805306368",
    "1297107061427929088:128",
    "1297107061427929088:16",
    "1297107061427929088:16384",
    "1297107061427929088:16777216",
    "1297107061427929088:536870912",
    "1297107061427929088:65536",
    "1297107061427929088:67108864",
    "1297107061427929088:8",
    "1297107061427929089:0",
    "1297107061427929092:0",
    "1297107061427929120:0",
    "1297107061427929216:0",
    "1297107061427929344:0",
    "1297107061427933184:0",
    "1297107061427937280:0",
    "1297107061427961856:0",
    "1297107061427994624:0",
    "1297107061428060160:0",
    "1297107061444706304:0",
    "1297107061562146816:0",
    "1297107061696364544:0",
    "1297107062501670912:0",
    "1297107336305836032:0",
    "1297108160939556864:0",
    "1297247798916284416:0",
    "1297388536404639744:0",
    "1369164655465857024:0",
    "1585337437579640832:0",
    "1873567813731352576:0",
    "3602950070641623040:0",
    "5908793079855316992:0",
])
# sbd fresh-corpus regeneration lane (commit 0dd5773e), 101 targets (99 corpus + 2 extra):
SBD_101 = None  # loaded from the published keymap (machine-read, sha-pinned below)


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


def main():
    for path, want in [(GEOMETRY, GEOMETRY_SHA), (CACHE, CACHE_SHA), (SUPPLY, SUPPLY_SHA),
                       (LEDGER, LEDGER_SHA), (PROFILE, PROFILE_SHA), (CCP, CCP_SHA),
                       (QUARANTINE, QUARANTINE_SHA)]:
        gate(f"pin_{Path(path).name}", sha(Path(path)) == want, f"{path}")

    # focus/cert/third/fourth embedded lists: sizes and mutual sanity
    gate("claim_list_sizes", [len(FOCUS_35), len(CERT_38), len(THIRD_39), len(FOURTH_41)] == [35, 38, 39, 41])
    third27 = {k for k in THIRD_39}
    if len(third27) != 39:
        fail("third-cost embedded list has duplicates")

    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("geometry_size", len(geo) == 3384)
    cache = {}
    for row in csv.reader(Path(CACHE).open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            fail(f"unexpected cache row {row}")
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            fail(f"verdict conflict in cache {k}")
        cache[k] = v

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
            candidates = (tuple(g["key"]), g["coverage"], ch, stage(vals))
            active.append(candidates)
    gate("candidates_115", len(active) == 115)
    live_classes = [c for c in active if c[3] == "UNKNOWN"]
    gate("live_62", len(live_classes) == 62)

    live_par = defaultdict(set)
    for k, cov, ch, st in live_classes:
        for child in ch:
            if child not in cache:
                live_par[child].add(k)
    supply = {}
    for row in csv.DictReader(Path(SUPPLY).open(newline="")):
        supply[(int(row["key"].split(":")[0]), int(row["key"].split(":")[1]))] = row
    gate("supply_matches_live", set(supply) == set(live_par) and len(supply) == 4562)
    deg = defaultdict(int)
    for child in live_par:
        deg[len(live_par[child])] += 1
    gate("supply_degree_dist", dict(deg) == {1: 2688, 2: 1874})

    # ---- fifth-cost class membership and exclusivity -------------------------
    fk = next(c for c in live_classes if tuple(c[0]) == FIFTH_CLASS)
    unk = sorted(c for c in fk[2] if c not in cache)
    excl = [c for c in unk if live_par[c] == {FIFTH_CLASS}]
    gate("fifth_unknown_99", len(unk) == 99)
    gate("fifth_exclusive_44", len(excl) == 44)
    gate("fifth_shared_55", len(unk) - len(excl) == 55)

    # published measurement cross-check (fifth row of the published 62-row table)
    pub = list(csv.DictReader(Path(CCP).open(newline="")))
    gate("published_rows_62", len(pub) == 62)
    pub_row = next(r for r in pub if r["key"] == f"{FIFTH_CLASS[0]}:{FIFTH_CLASS[1]}")
    gate("pub_row_children", int(pub_row["s5_children"]) == 114)
    gate("pub_row_unknown", int(pub_row["s5_unknown"]) == 99)
    gate("pub_row_exclusive", int(pub_row["unknown_exclusive"]) == 44)
    gate("pub_row_shared", int(pub_row["unknown_shared"]) == 55)
    gate("pub_row_proxy_total", int(pub_row["proxy_total"]) == 559112936)
    # proxy sums over recomputed sets
    def proxy(c):
        return int(supply[c]["truncated_cost_proxy_nodes"])
    gate("proxy_exclusive_sum", sum(proxy(c) for c in excl) == int(pub_row["proxy_exclusive_sum"]) == 255270268)
    gate("proxy_total_recomputed", sum(proxy(c) for c in unk) == int(pub_row["proxy_total"]))
    # class rank 5 by proxy_total; top-4 = the four other claimed classes
    ranked = sorted(pub, key=lambda r: (int(r["proxy_total"]), r["key"]))
    gate("fifth_rank_5", ranked[4]["key"] == f"{FIFTH_CLASS[0]}:{FIFTH_CLASS[1]}")
    gate("top4_claimed", {r["key"] for r in ranked[:4]} == {FOCUS_CLASS, CERT_CLASS, THIRD_CLASS, FOURTH_CLASS})

    # ---- ordering, disjointness, absence -------------------------------------
    order_keys = sorted(excl, key=lambda c: (proxy(c), c))
    gate("order_44", len(order_keys) == 44)
    bands = defaultdict(list)
    for c in order_keys:
        bands[proxy(c)].append(c)
    gate("bands", {k: len(v) for k, v in bands.items()} == {5069670: 1, 5234938: 7, 5932112: 36})

    mine = [f"{c[0]}:{c[1]}" for c in order_keys]
    mset = set(mine)
    # sbd keymap (machine list of the sbd lane claim)
    KEYMAP = ROOT / "research/experiments/n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json"
    gate("pin_keymap.json", sha(KEYMAP) == KEYMAP_SHA)
    keymap = json.loads(KEYMAP.read_text(encoding="utf-8"))
    sbd = sorted({f"{v[0]}:{v[1]}" for v in keymap["targets"].values()})
    gate("sbd_101", len(sbd) == 101)
    for name, s in [("focus", FOCUS_35), ("cert", CERT_38), ("third", THIRD_39),
                    ("fourth", FOURTH_41), ("sbd", sbd)]:
        gate(f"disjoint_{name}", not (mset & set(s)),
             str(sorted(mset & set(s))[:5]))
    gate("disjoint_union_all", not (mset & (set(FOCUS_35) | set(CERT_38) | set(THIRD_39) | set(FOURTH_41) | set(sbd))))

    qkeys = quarantined_cache_keys()  # fails closed if registry missing/corrupt
    gate("quarantine_absent", not (mset & {f"{k[0]}:{k[1]}" for k in qkeys}))
    gate("base_cache_absent", not (mset & {f"{k[0]}:{k[1]}" for k in cache}))

    # ---- independent geometry pre-check over the whole batch -----------------------------
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

    ledger = {r["key"]: r for r in csv.DictReader(Path(LEDGER).open(newline=""))}
    lr = ledger[f"{FIFTH_CLASS[0]}:{FIFTH_CLASS[1]}"]
    gate("ledger_unknown", int(lr["s5_unknown"]) == 99)
    gate("ledger_shared", int(lr["s5_unknown_shared_with_other_live_classes"]) == 55)

    out = {
        "schema": "n11-fifthcost-exclusive-selection-v1",
        "class": f"{FIFTH_CLASS[0]}:{FIFTH_CLASS[1]}",
        "coverage": sorted(fk[1]),
        "class_children_total": 114,
        "s5_unknown_before": 99,
        "unknown_exclusive": 44,
        "unknown_shared": 55,
        "proxy_total": int(pub_row["proxy_total"]),
        "proxy_exclusive_sum": 255270268,
        "proxy_shared_sum": int(pub_row["proxy_shared_sum"]),
        "bin_prior_all_loss_index": float(pub_row["bin_prior_all_loss_index"]),
        "exclusive_probe_order": rows,
        "bands_proxy_to_count": {str(k): len(v) for k, v in sorted(bands.items())},
        "concurrent_claims_respected": {
            "focus_35": len(FOCUS_35), "cert_38": len(CERT_38),
            "third_39": len(THIRD_39), "fourth_41": len(FOURTH_41), "sbd_101": len(sbd),
        },
        "gates_passed": gates,
        "status_guard": ("Selection and scheduling only; no verdict is claimed. The standard 11x11 "
                         "empty board, the two-stone root {60,27}, and its remaining third moves "
                         "100/108 remain UNKNOWN."),
    }
    tmp = EXP / "output" / "fifth-cost-exclusive-keys.json.tmp"
    tmp.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    tmp.rename(EXP / "output" / "fifth-cost-exclusive-keys.json")
    print(json.dumps({"all_gates_pass": True, "gates": len(gates),
                      "exclusive_keys": 44,
                      "proxy_exclusive_sum": 255270268}))


if __name__ == "__main__":
    main()
