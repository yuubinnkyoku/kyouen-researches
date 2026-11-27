"""Independent fail-closed cross-check audit of the published kit-17 frozen output
against the kit-17x independent blind second census (this kit).

Fresh single-file implementation; does not read or transform the published
audit_kit17.py. Engine = published engine_block.py byte-clone
(sha256 582c93c1...). Default paths are repo-relative so the audit re-runs from
a checkout of this kit directory.

Gates:
  G0 published kit-17 frozen .out sha256 = 420d1c83...
  G1 engine gate pin = bd5f22e4... and PASS
  G2 k0832 battery: recompute all 2,162 literals (closed, vC, vO) independently
  G3 anchors: recompute all 1,210 spots independently
  G4 census cross-check: every published row equals the blind second census row
     (shapes, R, and order-independent separation content)
  G5 windows: the 16 window rows have 0 separations
  G6 registration provenance: binding candidate texts byte-verbatim in the
     published kit-16 frozen .out future constants (sha256 85c04e43...)
  G7 binding hit-check: registered seats appear as separations
  G8 second-census totals: 49 rows / 211 separations / frontier+evenlife verdicts

Usage: python3 audit_kit17x.py [kit17.out] [census_kit17x.out] [kit16.out]
"""
import json, sys, hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine_block import H_canonical, H_ordered, single_token

ENGINE_PIN = "bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92"
KIT17_SHA = "420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95"
KIT16_SHA = "85c04e431b53d4f1d5538cd152c9b05bb475379be6243ef26a9022a4cb4c9589"
DEFAULTS = [
    os.path.join(HERE, "..", "strip-newband-m49m50-frontier-windows-evenlife-20261126",
                 "explore_m49m50_frontier_windows_evenlife.out"),
    os.path.join(HERE, "census_kit17x.out"),
    os.path.join(HERE, "..", "strip-newband-m47m48-frontier-windows-evenlife-20261126",
                 "explore_m47m48_frontier_windows_evenlife.out"),
]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    paths = sys.argv[1:4] if len(sys.argv) > 1 else DEFAULTS
    kit17, census, kit16 = (os.path.abspath(p) for p in paths)
    res = {}

    res["G0_kit17_sha"] = ("PASS" if sha(kit17) == KIT17_SHA else "FAIL", sha(kit17)[:16])
    d = json.load(open(kit17))

    eg = [x for x in d["sections"] if x.get("section") == "engine_gate"][0]
    res["G1_engine_gate"] = ("PASS" if eg["gate"] == "PASS" and eg["pin"] == ENGINE_PIN
                             and eg["engine_sha"] == ENGINE_PIN else "FAIL", "")

    bat = [x for x in d["sections"] if x.get("section") == "k0832_battery"][0]
    bad = 0
    for i, r in enumerate(bat["rows"]):
        if i % 200 == 0:
            H_canonical.cache_clear(); H_ordered.cache_clear()
        closed = single_token(r["x"], r["z"], r["R"])
        vc = H_canonical(r["R"], (r["x"],), r["z"])
        vo = H_ordered(r["R"], (r["x"],), r["z"])
        if not (closed == r["closed"] == vc == r["vC"] == vo == r["vO"] and r["match"]):
            bad += 1
    res["G2_battery"] = ("PASS" if bad == 0 and bat["literals"] == 2162 and bat["bad"] == 0
                         and bat["all_match"] else "FAIL", "bad %d" % bad)

    anc = [x for x in d["sections"] if x.get("section") == "published_anchor_rechecks"][0]
    bad = 0
    for i, r in enumerate(anc["rows"]):
        if i % 100 == 0:
            H_canonical.cache_clear()
        hv = H_canonical(r["R"], tuple(sorted(r["X"], reverse=True)), r["z"])
        if hv != r["value"] or r["value"] != r["published_value"] or not r["match"]:
            bad += 1
    res["G3_anchors"] = ("PASS" if bad == 0 and len(anc["rows"]) == 1210 else "FAIL",
                         "bad %d" % bad)

    cs = json.load(open(census))
    crows = {("%d_%d" % (r["m"], r["z"])): r for r in cs["sections"]}
    rows = [x for x in d["sections"] if x.get("section", "").endswith("_row_record")]
    def canon(lst):
        return sorted(([t["X"], t["S"], t["value"], t["collapse"], t["direction"]] for t in lst))
    mm, diffs = 0, []
    for r in rows:
        key = "%d_%d" % (r["min"], r["z"])
        m = crows.get(key)
        if m and canon(r["separations"]) == canon(m["separations"]) and \
           r["shapes"] == m["shapes"] and r["R"] == m["R"]:
            mm += 1
        else:
            diffs.append(key)
    res["G4_census_crosscheck"] = ("PASS" if mm == len(rows) == 49 and not diffs else "FAIL",
                                   "%d/%d diffs %s" % (mm, len(rows), diffs[:3]))

    win = [r for r in rows if r.get("section", "").startswith("inband_")]
    dirty = [r["section"] for r in win if r["separations"]]
    res["G5_windows_clean"] = ("PASS" if len(win) == 16 and not dirty else "FAIL",
                               "%d rows dirty %s" % (len(win), dirty))

    ok16 = sha(kit16) == KIT16_SHA
    k16 = json.load(open(kit16))
    fut = [x for x in k16["sections"] if x.get("section") == "future_slice_registration_constants"][0]
    fut_text = json.dumps(fut["registered_for_next_execution_kit_log_S5"][0][0], ensure_ascii=False)
    missing = [r["section"] for r in rows if r.get("binding") and r.get("candidate")
               and r["candidate"] not in fut_text]
    res["G6_registration_provenance"] = ("PASS" if ok16 and not missing else "FAIL",
                                         "missing %s" % missing[:3])

    hits, fails = 0, []
    for r in rows:
        if not r.get("binding"):
            continue
        seps = [(s["S"], sorted(s["X"])) for s in r["separations"]]
        for seat in (r.get("expect_seats") or []):
            X, S = sorted(seat[:2]), seat[2]
            if (S, X) in seps:
                hits += 1
            else:
                fails.append((r["section"], X, S))
    res["G7_binding_hits"] = ("PASS" if not fails else "FAIL",
                              "hits %d fails %s" % (hits, fails[:3]))

    tot = sum(len(r["separations"]) for r in cs["sections"])
    meta_ok = (cs["meta"]["total_separations"] == 211 and tot == 211 and
               cs["meta"]["rows"] == 49 and len(cs["sections"]) == 49)
    res["G8_census_totals"] = ("PASS" if meta_ok else "FAIL", "rows 49 seps %d" % tot)

    ok = all(v[0] == "PASS" for v in res.values())
    for k, v in sorted(res.items()):
        print(k, v[0], v[1])
    print("AUDIT-" + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
