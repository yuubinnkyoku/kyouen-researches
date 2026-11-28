#!/usr/bin/env python3
"""n11 fourteenth ladder-top class 5804 k01 owner-union precheck (read-only).

Derives the graph owner-class union of the fourteenth ladder-top k01 WIN
row (s5 index 198576) from the frozen dependency graph, with the
published u04 zero-deviation flip as a method control, and pre-registers
the census-flip prediction for a future fourteenth k01 adoption Part.
Fail-closed: writes nothing unless every gate passes.
"""
import gzip, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "input"
OUT = ROOT / "output" / "owner-union-precheck.json"

PINS = {
    "graph": ("dependency-graph.json.gz",
              "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"),
    "ladder": ("closure-classes.csv",
               "be8bcff16a7a557d30703921d9a024a232b0fade5fab16afb015a07666fcdc62"),
    "batch_summary": ("fourteenth-batch-summary.json",
               "b6ee7a935d973fc28cb31f9e862df817bc584fa0ef7a41536b0d936171451f3a"),
    "k01_input": ("k01.input.csv",
               "fce9ae7a9c6d81c54a45bce79ff4c030940fabb829b7b9696fd3af3767a0136b"),
    "head": ("head.cache",
               "d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec"),
}
TARGETS = {"k01": 198576}
CONTROL = {"u04": (745184, [23092, 23101, 23115, 23938])}
SERVING_CLASS = 5804

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ok = True
    def g(name, cond, detail=""):
        nonlocal ok
        if not cond:
            ok = False
            print(f"GATE-FAIL {name} {detail}")
    # G0: input pins
    for label, (fname, want) in PINS.items():
        p = IN / fname
        g(f"G0:{label}", p.exists() and sha256(p) == want, f"want {want[:8]}")
    if not ok:
        return 1
    gph = json.load(gzip.open(IN / "dependency-graph.json.gz"))
    s4_cost = gph["s4_cost"]
    g("G1:graph-shape", len(s4_cost) == 34949 and len(gph["s4_masks"]) == 34949,
      f"len={len(s4_cost)}")
    bs = json.load(open(IN / "fourteenth-batch-summary.json"))
    # G2: targets match the published batch summary
    for key in ("k01",):
        row = bs["stage1_2m"][key]
        g(f"G2:{key}-index", row["s5_index"] == TARGETS[key],
          f"{row['s5_index']} vs {TARGETS[key]}")
        g(f"G2:{key}-class", row["class_index"] == SERVING_CLASS)
        g(f"G2:{key}-legal", row["legal"] == 86)
    g("G2:k01-win", bs["escalation_15m"]["k01"]["result"] == 1
      and bs["escalation_15m"]["k01"]["nodes"] == 4360661)
    # G3: owner derivation + u04 zero-deviation control
    owners = {k: [ci for ci in range(len(s4_cost)) if idx in s4_cost[ci]]
              for k, idx in TARGETS.items()}
    for k, (cidx, expect) in CONTROL.items():
        got = [ci for ci in range(len(s4_cost)) if cidx in s4_cost[ci]]
        g(f"G3:control-{k}", got == expect, f"{got} vs {expect}")
    g("G3:k01-owners", owners["k01"] == [5308, 5804, 8811], str(owners["k01"]))
    union = sorted(set().union(*owners.values()))
    g("G3:union", union == [5308, 5804, 8811], str(union))
    # G4: ladder status (serving class rank-1 unknown_now=4; owner 5308 absent,
    #     owner 8811 present at rank 17 with unknown_now 52)
    lad = {}
    with open(IN / "closure-classes.csv") as f:
        hdr = f.readline().strip().split(",")
        for line in f:
            r = dict(zip(hdr, line.strip().split(",")))
            lad[int(r["class_index"])] = (int(r["class_rank"]), int(r["unknown_now"]))
    g("G4:serving-rank1", lad.get(SERVING_CLASS, (None,))[0] == 1,
      str(lad.get(SERVING_CLASS)))
    g("G4:serving-unknown4", lad.get(SERVING_CLASS, (0, 0))[1] == 4)
    g("G4:owner-5308-not-in-ladder", 5308 not in lad)
    g("G4:owner-8811-in-ladder", lad.get(8811) == (17, 52), str(lad.get(8811)))
    # G5: freshness of the row vs the head of record
    head_txt = (IN / "head.cache").read_text()
    g("G5:k01-fresh", "6053401124017274880" not in head_txt)
    g("G5:head-shape",
      head_txt.count("\n") == 6897 and head_txt.endswith("\n")
      and head_txt.startswith("# S5 solver-trusted exact"))
    if not ok:
        return 1
    out = {
        "schema": "n11-fourteenth-owner-union-precheck-v1",
        "part": "read-only pre-registration of the class-5804 k01 adoption flip inputs",
        "inputs": {label: sha for label, (_, sha) in PINS.items()},
        "targets": {
            "k01": {"key": "6053401124017274880:0", "s5_index": 198576,
                    "escalation": "WIN(1) nodes 4360661 @15000000 (kit 5c670bc6)",
                    "pillars": "COMPLETE (cppgate GATE-PASS 86,15000000,1,4360661 kit 35b5fef1 + thirdimpl CORROBORATION-PASS result 1, log 68852ff2)",
                    "owner_classes": owners["k01"]}
        },
        "control": {"u04": {"s5_index": 745184,
                            "derived": CONTROL["u04"][1],
                            "published_flip": [23092, 23101, 23115, 23938],
                            "verdict": "exact match (zero-deviation flip published in 2092e7a8)"}},
        "combined_owner_union": union,
        "serving_class": {"class_index": 5804,
                          "key": "6053400849139367936:0",
                          "ladder_rank": 1, "unknown_now": 4,
                          "in_799_row_ladder": True},
        "predicted_k01_adoption_flip": {
            "note": "prediction only; replaced by measurement at the adoption reaudit",
            "owner_union": union,
            "expected_class_flips_if_all3_unknown": {str(ci): "unknown->excluded_now" for ci in union},
            "ladder_prediction": "serving class 5804 stays in the closure ladder (unknown_now 4->3); NOT a ladder exit unlike the thirteenth adoption",
            "caveats": [
                "u03 precedent: an owner class may already be excluded_now on the BASE side (serving-class pre-exclusion); census status must be measured, not assumed",
                "u04 precedent: unknown_now churn can be zero when flips land exactly as predicted",
                "owner class 8811 is itself a ladder row (rank 17, unknown_now 52): its census status must be measured; the k01 WIN row does not resolve class 8811",
                "class 5804 does NOT leave the 799-row ladder on a k01-only adoption (unknown_now 4->3); k02/k03/k04 stay 2M UNKNOWN",
                "Board-verified free_now required at adoption time for any class-completion claim",
                "class 5804 completion additionally requires k02/k03/k04 (all still stage-1 2M UNKNOWN, re-escalation only under a future declaration)"
            ]
        },
        "status_guard": "pre-registration bookkeeping only; NO verdict consumed; 11x11 UNKNOWN"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("PRECHECK-PASS owners k01=%s union=%s" % (owners["k01"], union))
    return 0

if __name__ == "__main__":
    sys.exit(main())
