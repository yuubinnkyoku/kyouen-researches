#!/usr/bin/env python3
"""n11 thirteenth ladder-top class 16757 owner-union precheck (read-only).

Derives the graph owner-class unions of the thirteenth k01/k02 WIN rows
(s5 indices 556117 / 558553) from the frozen dependency graph, with the
published u04 zero-deviation flip as a method control, and pre-registers
the census-flip prediction for a future class-16757 adoption Part.
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
               "ef3447481abb14af3c56a64251d86e63b178c7fb57b0ce8898e67303c24dc3e2"),
    "batch_summary": ("thirteenth-batch-summary.json",
               "bf390835a3c2af0484adfc032d0da6705e70145685fd18db5200aeb3d5b144c9"),
    "k01_input": ("k01.input.csv",
               "eda6e3d6d5d639039b7b57c34aaaaa960ffe5d1172b187aadfe63a9393b8e00f"),
    "k02_input": ("k02.input.csv",
               "6ff8d84eacaa5a3c8091ec91935caf743b74641116f91f9de9d2413e30682aa5"),
    "head": ("head.cache",
               "beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544"),
}
TARGETS = {"k01": 556117, "k02": 558553}
CONTROL = {"u04": (745184, [23092, 23101, 23115, 23938])}
SERVING_CLASS = 16757

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
    bs = json.load(open(IN / "thirteenth-batch-summary.json"))
    # G2: targets match the published batch summary
    for key in ("k01", "k02"):
        row = bs["stage1_2m"][key]
        g(f"G2:{key}-index", row["s5_index"] == TARGETS[key],
          f"{row['s5_index']} vs {TARGETS[key]}")
        g(f"G2:{key}-class", row["class_index"] == SERVING_CLASS)
    g("G2:k01-win", bs["escalation_15m"]["k01"]["result"] == 1
      and bs["escalation_15m"]["k01"]["nodes"] == 2678305)
    # G3: owner derivation + u04 zero-deviation control
    owners = {k: [ci for ci in range(len(s4_cost)) if idx in s4_cost[ci]]
              for k, idx in TARGETS.items()}
    for k, (cidx, expect) in CONTROL.items():
        got = [ci for ci in range(len(s4_cost)) if cidx in s4_cost[ci]]
        g(f"G3:control-{k}", got == expect, f"{got} vs {expect}")
    g("G3:k01-owners", owners["k01"] == [16612, 16757, 30542], str(owners["k01"]))
    g("G3:k02-owners", owners["k02"] == [16740, 16757, 30542], str(owners["k02"]))
    union = sorted(set(owners["k01"]) | set(owners["k02"]))
    g("G3:union", union == [16612, 16740, 16757, 30542], str(union))
    # G4: ladder status (serving class rank-1 unknown_now=2; other owners absent)
    lad = {}
    with open(IN / "closure-classes.csv") as f:
        hdr = f.readline().strip().split(",")
        for line in f:
            r = dict(zip(hdr, line.strip().split(",")))
            lad[int(r["class_index"])] = (int(r["class_rank"]), int(r["unknown_now"]))
    g("G4:serving-rank1", lad.get(SERVING_CLASS, (None,))[0] == 1,
      str(lad.get(SERVING_CLASS)))
    g("G4:serving-unknown2", lad.get(SERVING_CLASS, (0, 0))[1] == 2)
    for ci in (16612, 16740, 30542):
        g(f"G4:owner-{ci}-not-in-ladder", ci not in lad)
    # G5: freshness of both rows vs the head of record
    head_txt = (IN / "head.cache").read_text()
    g("G5:k01-fresh", "1153204147814662144" not in head_txt)
    g("G5:k02-fresh", "1152922672837951488" not in head_txt)
    g("G5:head-shape", head_txt.count("\n") + (0 if head_txt.endswith("\n") else 1) == 6895)
    if not ok:
        return 1
    out = {
        "schema": "n11-thirteenth-owner-union-precheck-v1",
        "part": "read-only pre-registration of the class-16757 adoption flip inputs",
        "inputs": {label: sha for label, (_, sha) in PINS.items()},
        "targets": {
            "k01": {"key": "1153204147814662144:65536", "s5_index": 556117,
                    "escalation": "WIN(1) nodes 2678305 @15000000 (kit 12d8359c)",
                    "pillars": "COMPLETE (f1f5c49d) + XHOST-PASS (this lane, eb542121)",
                    "owner_classes": owners["k01"]},
            "k02": {"key": "1152922672837951488:65792", "s5_index": 558553,
                    "escalation": "WIN(1) nodes 3485963 @15000000 (kit 3087c38b, other lane; pillars declared 177b1086)",
                    "owner_classes": owners["k02"]}
        },
        "control": {"u04": {"s5_index": 745184,
                            "derived": CONTROL["u04"][1],
                            "published_flip": [23092, 23101, 23115, 23938],
                            "verdict": "exact match (zero-deviation flip published in 2092e7a8)"}},
        "combined_owner_union": union,
        "serving_class": {"class_index": 16757,
                          "key": "1153204079095185408:65536",
                          "ladder_rank": 1, "unknown_now": 2,
                          "in_800_row_ladder": True},
        "predicted_combined_adoption_flip": {
            "note": "prediction only; replaced by measurement at the adoption reaudit",
            "owner_union": union,
            "expected_class_flips": {str(ci): "unknown->excluded_now" for ci in union},
            "census_prediction_if_all4_unknown": {
                "unknown": [34376, 34372], "excluded_now": [144, 148],
                "free_now": [39, 39]},
            "caveats": [
                "u03 precedent: an owner class may already be excluded_now on the BASE side (serving-class pre-exclusion); census status must be measured, not assumed",
                "u04 precedent: unknown_now churn can be zero when flips land exactly as predicted",
                "class 16757 leaves the 800-row closure ladder (unknown_now 2->0); ladder churn must be machine-measured",
                "Board-verified free_now required at adoption time for any class-completion claim",
                "k02 WIN row pillars are still OPEN at the time of this precheck (declared 177b1086, owned by another lane); no k02 row may be adopted before they close"
            ]
        },
        "status_guard": "pre-registration bookkeeping only; NO verdict consumed; 11x11 UNKNOWN"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("PRECHECK-PASS owners k01=%s k02=%s union=%s" %
          (owners["k01"], owners["k02"], union))
    return 0

if __name__ == "__main__":
    sys.exit(main())
