#!/usr/bin/env python3
"""Ultra-cheap class-completion candidate census under the canonical head
of record 1e2eeda2 (eleventh-cost k01 adoption, 6,890 rows WIN 208 /
LOSS 6,682) plus the update8 receipt verdicts.

Purpose (scheduling bookkeeping only, no verdict claimed or consumed):
the published eleventh-cost reaudit closure ladder
(reaudit/output/closure-classes.csv, sha256 d7ae77dd..., 804 rows)
shows four classes at exactly one remaining unknown S5 child under the
current head. A single resolved verdict on such a key would complete
its class (a candidate free_now flip for the adaptive coordinator,
Board-verified at adoption time). This instrument independently
recomputes the per-class unknown_now counts for ALL 804 ladder rows
from the frozen dependency graph (54f9c364...), the head of record and
the update8 receipts (the same trust boundary the published refresh
uses, re-implemented fresh here - the refresh machinery itself is NOT
read or executed), identifies the four single-unknown keys, and checks
each key against every published concurrent claim set to see whether
an ultra-cheap candidate is actually available for a future selection
Part or is already owned by another lane.

Fail-closed: rc=1 on any gate failure.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
CAND_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
HEAD_SHA = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"
CLOSURE_SHA = "d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6890, 208, 6682
EXPECTED_ONE_UNKNOWN = {16371, 23101, 1849, 2251}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ind = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("in")
    sel = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("selkit")
    closure = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("closure-classes.csv")
    out_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return bool(ok)

    ok = True

    # ---------- pins ----------
    ok &= g("P0:dependency-graph-sha", sha256(ind / "dependency-graph.json.gz") == GRAPH_SHA, "")
    ok &= g("P0:update8-sha", sha256(ind / "update8.json") == UPDATE8_SHA, "")
    ok &= g("P0:supply-sha", sha256(ind / "shared-s5-tasks.csv") == SUPPLY_SHA, "")
    ok &= g("P0:candidates-sha", sha256(ind / "candidate-classes.csv") == CAND_SHA, "")
    ok &= g("P0:quarantine-sha", sha256(ind / "quarantine.json") == QUAR_SHA, "")
    ok &= g("P0:closure-sha", sha256(closure) == CLOSURE_SHA, "")
    head_path = ind / "head-1e2eeda2.cache"
    ok &= g("P0:head-sha", sha256(head_path) == HEAD_SHA, "")

    # ---------- head ----------
    cache = {}
    for line in head_path.read_text().splitlines():
        if not line.startswith("s5verdict,"):
            continue
        p = line.strip().split(",")
        cache[(p[1], p[2])] = p[4]
    ok &= g("P1:head-shape", len(cache) == HEAD_ROWS
            and Counter(cache.values()) == {"2": HEAD_LOSS, "1": HEAD_WIN}, str(len(cache)))

    # ---------- frozen dependency graph ----------
    gph = json.load(gzip.open(ind / "dependency-graph.json.gz"))
    s4_masks, s4_status, s4_cost = gph["s4_masks"], gph["s4_status"], gph["s4_cost"]
    s5_masks = gph["s5_masks"]
    ok &= g("P1:graph-shape", len(s4_masks) == 34949 and len(s4_cost) == 34949
            and len(s5_masks) == 962525, "")

    # ---------- update8 receipts ----------
    u8 = json.loads((ind / "update8.json").read_text())
    ok &= g("P1:update8-shape", u8.get("schema") == "n11-night-repaired-joint-plan-update8-v1"
            and u8.get("union_size") == 31859
            and len(u8.get("required_new_s5", [])) == 31859
            and u8.get("verification", {}).get("passed") is True, "")
    receipts = {int(k): int(v) for k, v in u8["resolved_s5_verdicts"].items()}
    ok &= g("P1:update8-receipts", len(receipts) == 23, str(len(receipts)))
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    def known(j: int):
        v = cache.get((str(s5_masks[j][0]), str(s5_masks[j][1])))
        if v is not None:
            return int(v)
        return receipts.get(j)

    # receipt/cache conflict check (same trust boundary as the refresh)
    conflicts = 0
    for (lo, hi), v in cache.items():
        i = mask_to_index.get((int(lo), int(hi)))
        if i is not None and i in receipts and receipts[i] != int(v):
            conflicts += 1
    ok &= g("P1:receipt-cache-conflicts", conflicts == 0, conflicts)

    # ---------- closure ladder full recomputation ----------
    rows = list(csv.DictReader(open(closure)))
    ok &= g("P1:closure-rows", len(rows) == 804, len(rows))
    mismatch, one_unknown = [], {}
    for r in rows:
        i = int(r["class_index"])
        cost = s4_cost[i]
        unk = [j for j in cost if known(j) is None]
        if len(unk) != int(r["unknown_now"]):
            mismatch.append(f"{i}:{len(unk)}!={r['unknown_now']}")
        if len(unk) == 1:
            one_unknown[i] = unk[0]
    ok &= g("P2:closure-unknown-recomputed-804", not mismatch, ";".join(mismatch[:5]))
    ok &= g("P2:one-unknown-classes", set(one_unknown) == EXPECTED_ONE_UNKNOWN,
            str(sorted(one_unknown)))

    # ---------- supply ----------
    supply = {r["key"]: r for r in csv.DictReader(open(ind / "shared-s5-tasks.csv"))}
    ok &= g("P1:supply-shape", len(supply) == 4562, len(supply))

    # ---------- claim sets ----------
    ccp = json.load(open(ind / "ccp.json"))
    tf = json.load(open(ind / "claims/third_fourth.json"))
    claims = {
        "focus_35": [e["key"] if isinstance(e, dict) else e
                     for e in ccp["focus_class_exclusive_reference"]],
        "cert_38": [e["key"] if isinstance(e, dict) else e
                   for e in ccp["certificate_class_exclusive_probe_order"]],
        "third_39": tf["third_39"],
        "fourth_41": tf["fourth_41"],
    }
    for n in ["fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh"]:
        d = json.load(open(ind / f"claims/{n}.json"))
        claims[f"{n}"] = [e["key"] for e in d["exclusive_probe_order"]]
    tw = json.load(open(sel / "output" / "twelfth-cost-exclusive-keys.json"))
    claims["twelfth_51"] = [e["key"] for e in tw["exclusive_probe_order"]]
    km = json.load(open(ind / "keymap.json"))
    claims["sbd_101"] = [f"{v[0]}:{v[1]}" for v in km["targets"].values()]
    parked = []
    for p in list(ind.glob("parked2-*.csv")) + list(ind.glob("parked4/*.csv")):
        f = p.read_text().strip().split(",")
        parked.append(f"{f[3]}:{f[4]}")
    claims["parked_6"] = parked
    sizes = {k: len(v) for k, v in claims.items()}
    ok &= g("P3:claim-sizes", sizes == {"focus_35": 35, "cert_38": 38, "third_39": 39,
            "fourth_41": 41, "fifth": 44, "sixth": 43, "seventh": 42, "eighth": 43,
            "ninth": 45, "tenth": 44, "eleventh": 46, "twelfth_51": 51,
            "sbd_101": 101, "parked_6": 6}, json.dumps(sizes))
    quar = json.load(open(ind / "quarantine.json"))
    qkeys = []
    for e in (quar if isinstance(quar, list) else quar.get("entries", [])):
        qkeys.append(e.get("key") if isinstance(e, dict) else str(e))
    ok &= g("P3:quarantine-entries", len(qkeys) == 2, str(len(qkeys)))

    # ---------- per-candidate report ----------
    candidates = []
    for cidx in sorted(one_unknown):
        j = one_unknown[cidx]
        ukey = f"{s5_masks[j][0]}:{s5_masks[j][1]}"
        s = supply.get(ukey)
        claimed_in = [name for name, lst in claims.items() if ukey in lst]
        candidates.append({
            "class_index": cidx,
            "class_key": f"{s4_masks[cidx][0]}:{s4_masks[cidx][1]}",
            "unknown_key": ukey, "s5_index": j,
            "legal": int(s["legal"]) if s else None,
            "proxy": int(s["proxy"]) if s and s.get("proxy") else None,
            "in_probe13_supply": s is not None,
            "fresh_vs_head": (ukey.split(":")[0], ukey.split(":")[1]) not in cache,
            "claimed_in": claimed_in,
            "quarantined": ukey in qkeys,
        })

    out = {
        "schema": "n11-ultra-cheap-class-census-v1",
        "head_basis": {"sha256": HEAD_SHA, "rows": HEAD_ROWS, "win": HEAD_WIN, "loss": HEAD_LOSS},
        "closure_ladder": {"sha256": CLOSURE_SHA, "rows": 804,
                           "unknown_recomputed": "all 804 rows match the published unknown_now"},
        "one_unknown_classes": candidates,
        "claim_sets_checked": sorted(claims) + ["quarantine_2"],
        "gates": gates,
        "overall": "PASS" if ok else "FAIL",
        "meaning": ("scheduling bookkeeping only; no verdict is claimed or consumed; "
                    "resolving a listed key would still require the standing cold-pair + "
                    "C++-gate + third-implementation pillars before any adoption; the "
                    "standard 11x11 empty board, all 19 central-reply roots, the "
                    "two-stone root {60,27} and third moves 100/108 remain UNKNOWN"),
    }
    js = json.dumps(out, indent=1, sort_keys=True) + "\n"
    if out_path is not None:
        out_path.write_text(js)
    sys.stdout.write(js)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
