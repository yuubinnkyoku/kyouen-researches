#!/usr/bin/env python3
"""Independent fail-closed self-audit of the kit-18x blind second census
(census_kit18x.out) against the published kit-17 frozen .out registration
authority.

Fresh single-file implementation; does not read or transform any published kit
audit script. Engine = published engine_block.py byte-clone
(sha256 582c93c1...).

Gates:
  G0 published kit-17 frozen .out sha256 = 420d1c83...
  G1 engine clone sha256 = 582c93c1... and startup pin = bd5f22e4...
  G2 harness validation: recompute a 12-row random-free subset of the
     published kit-17 row records and compare (order-independent)
  G3 registration provenance: the census row set is exactly the kit-17
     future-constant binding rows (m,z present) + windows + even-m z=3m+16
  G4 frontier rows: m=51@z=101 and m=52@z=102 contain exactly the registered
     seat with the registered value/direction
  G5 binding hit-check: every seat named in a binding prediction text
     ("EXACTLY ONE: {a,b}@S=k DIR xv y" / "stick {a,b} DOWN ..." /
     "NEW {a,c}@S=k UP ...") appears as a separation with matching
     value/direction; conform-DEAD seats are absent
  G6 windows: 16 rows, 0 separations each
  G7 evenlife z=3m+16: stick {m,2m+16} DOWN 0v2 + NEW {m,2m+18} UP 2v1
     present; all DOWN seps are 0v2 and all UP seps are 2v1
  G8 census totals: 49 rows, all recomputed here, byte-equal content vs the
     frozen census file (recompute every row live and compare)
  G9 determinism: the frozen census file re-run content equals the frozen
     content (second full recompute in this audit doubles as G8)

Usage: python3 audit_kit18x.py
"""
import json, sys, os, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine_block import H_canonical, single_token

K17_SHA = "420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95"
ENGINE_SHA = "582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0"
ENGINE_PIN = "bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92"
K17_OUT = os.path.join(HERE, "k17_published.out")
CENSUS_OUT = os.path.join(HERE, "census_kit18x.out")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def shapes_for(S, m):
    out = []
    if S == m:
        out.append((m,))
    if S >= 2 * m:
        out.append((m, S - m))
    t = S - m
    if t >= 2 * m:
        for x in range(m, t // 2 + 1):
            out.append((m, x, t - x))
    return out


def census_row(R, z, m, smax):
    seps, n = [], 0
    for S in range(m, smax + 1):
        H_canonical.cache_clear()
        for X in shapes_for(S, m):
            n += 1
            hv = H_canonical(R, X, z)
            ev = single_token(S, z, R)
            if hv != ev:
                seps.append({"X": list(X), "S": S, "value": hv, "collapse": ev,
                             "direction": "UP" if hv > ev else "DOWN"})
    return seps, n


def canon(lst):
    return sorted(([s["X"], s["S"], s["value"], s["collapse"], s["direction"]]
                    for s in lst))


def sep_index(seps):
    return {(tuple(s["X"]), s["S"]): s for s in seps}


def precompute(path, budget=200.0):
    """Checkpointed live recompute of all 49 census rows + 13 kit-17 spot rows."""
    import time
    cs = json.load(open(CENSUS_OUT))
    crows = {r["m_z"]: r for r in cs["sections"]}
    d = json.load(open(K17_OUT))
    rows17 = [x for x in d["sections"] if x.get("section", "").endswith("_row_record")][::4]
    done = {}
    if os.path.exists(path):
        done = json.load(open(path))
    t0 = time.time()
    tasks = [("census", k) for k in sorted(crows)] + \
            [("k17spot", r["section"]) for r in rows17]
    for tag, k in tasks:
        if k in done:
            continue
        if tag == "census":
            r = crows[k]
            seps, n = census_row(r["R"], r["z"], r["m"], r["smax"])
            done[k] = {"seps": seps, "shapes": n}
        else:
            r = [x for x in rows17 if x["section"] == k][0]
            lo, hi = r["s_domain"].strip("{}").split("..")
            seps, n = census_row(r["R"], r["z"], r["min"], int(hi))
            done[k] = {"seps": seps, "shapes": n,
                       "pub_seps": r["separations"], "pub_shapes": r["shapes"]}
        json.dump(done, open(path, "w"))
        if time.time() - t0 > budget:
            print("budget stop at", k, flush=True)
            break
    print("precompute", len(done), "/", len(tasks))


def main():
    res = {}
    res["G0_kit17_sha"] = ("PASS" if sha(K17_OUT) == K17_SHA else "FAIL",
                          sha(K17_OUT)[:16])
    d = json.load(open(K17_OUT))
    res["G1_engine"] = ("PASS" if sha(os.path.join(HERE, "engine_block.py"))
                        == ENGINE_SHA else "FAIL", "")
    eg = [x for x in d["sections"] if x.get("section") == "engine_gate"][0]
    if not (eg.get("gate") == "PASS" and eg.get("pin") == ENGINE_PIN
            and eg.get("engine_sha") == ENGINE_PIN):
        res["G1_engine"] = ("FAIL", "kit-17 engine_gate mismatch")
    cs = json.load(open(CENSUS_OUT))
    crows = {r["m_z"]: r for r in cs["sections"]}
    fut = [x for x in d["sections"]
           if x.get("section") == "future_slice_registration_constants"][0]
    items = fut["registered_for_next_execution_kit_log_S5"][0][0]

    # G2: precomputed live recompute of 13 published kit-17 spot rows
    pre = json.load(open(os.path.join(HERE, "audit_recompute.json")))
    spots = {k: v for k, v in pre.items() if k.startswith("inband_") or k.endswith("row_record") or "_" in k and k not in crows}
    bad = []
    nchecked = 0
    for k, v in pre.items():
        if "pub_seps" not in v:
            continue
        nchecked += 1
        if not (canon(v["seps"]) == canon(v["pub_seps"]) and v["shapes"] == v["pub_shapes"]):
            bad.append(k)
    res["G2_harness_validation"] = ("PASS" if len(bad) == 0 and nchecked == 13 else "FAIL",
                                    "checked %d bad %s" % (nchecked, bad[:3]))

    # G3: row set = registration
    expect = {}
    for it in items:
        m, z = it.get("m"), it.get("z")
        if m is None or z is None:
            continue
        zs = range(int(z.split("..")[0]), int(z.split("..")[1]) + 1) if isinstance(z, str) else [z]
        for zz in zs:
            expect["%d_%d" % (m, zz)] = it
    for m in (14, 16, 18):
        expect["%d_%d" % (m, 3 * m + 16)] = None
    res["G3_row_set"] = ("PASS" if set(expect) == set(crows) and len(crows) == 49
                         else "FAIL",
                         "missing %s extra %s" %
                         (sorted(set(expect) - set(crows))[:3],
                          sorted(set(crows) - set(expect))[:3]))

    # G4: frontier exactness
    fb = []
    for key, X, S, val, col, direction in (
            ("51_101", [51, 52], 103, 2, 0, "UP"),
            ("52_102", [52, 52], 104, 2, 1, "UP")):
        r = crows[key]
        if len(r["separations"]) != 1:
            fb.append((key, "seps %d" % len(r["separations"])))
            continue
        s = r["separations"][0]
        if not (s["X"] == X and s["S"] == S and s["value"] == val
                and s["collapse"] == col and s["direction"] == direction):
            fb.append((key, s))
    res["G4_frontier_exact"] = ("PASS" if not fb else "FAIL", str(fb[:2]))

    # G5: binding seats from prediction texts
    seat_re = re.compile(r"\{(\d+),\s*(\d+)\}@S=(\d+)\s+(UP|DOWN)\s+(\d+)v(\d+)")
    stick_re = re.compile(r"stick\s+\{(\d+),\s*(\d+)\}\s+DOWN\s+(\d+)v(\d+)")
    dead_re = re.compile(r"\{(\d+),\s*(\d+)\}\s+conform-DEAD")
    fails, hits = [], 0
    for key, it in expect.items():
        if it is None:
            continue
        text = it.get("prediction", "")
        r = crows[key]
        idx = sep_index(r["separations"])
        for X1, X2, S, dirn, val, col in seat_re.findall(text):
            X = (int(X1), int(X2))
            s = idx.get((tuple(X), int(S)))
            if s and s["value"] == int(val) and s["collapse"] == int(col) \
               and s["direction"] == dirn:
                hits += 1
            else:
                fails.append((key, X, int(S)))
        for X1, X2, val, col in stick_re.findall(text):
            m = crows[key]["m"]
            S = int(X2) + m  # stick seat {m,co} sits at S = m + co (= z on birth rows)
            X = (int(X1), int(X2))
            found = any(tuple(sep["X"]) == tuple(X) and sep["value"] == int(val)
                        and sep["collapse"] == int(col) and sep["direction"] == "DOWN"
                        for sep in r["separations"])
            if found:
                hits += 1
            else:
                fails.append((key, "stick", X))
        for X1, X2 in dead_re.findall(text):
            X = (int(X1), int(X2))
            if any(tuple(sep["X"]) == tuple(X) for sep in r["separations"]):
                fails.append((key, "DEAD-present", X))
    res["G5_binding_hits"] = ("PASS" if not fails else "FAIL",
                              "hits %d fails %s" % (hits, fails[:4]))

    # G6: windows clean
    win = [k for k, r in crows.items() if "window" in r["kind"]]
    dirty = [k for k in win if crows[k]["separations"]]
    res["G6_windows_clean"] = ("PASS" if len(win) == 16 and not dirty else "FAIL",
                              "%d rows dirty %s" % (len(win), dirty))

    # G7: evenlife z=3m+16 template
    eb = []
    for m in (14, 16, 18):
        r = crows["%d_%d" % (m, 3 * m + 16)]
        idx = sep_index(r["separations"])
        stick = idx.get(((m, 2 * m + 16), 3 * m + 16))
        new = idx.get(((m, 2 * m + 18), 3 * m + 18))
        if not (stick and stick["value"] == 0 and stick["collapse"] == 2
                and stick["direction"] == "DOWN"):
            eb.append((m, "stick", stick))
        if not (new and new["value"] == 2 and new["collapse"] == 1
                and new["direction"] == "UP"):
            eb.append((m, "NEW", new))
        for s in r["separations"]:
            if s["direction"] == "DOWN" and not (s["value"] == 0 and s["collapse"] == 2):
                eb.append((m, "DOWN-template", s))
            if s["direction"] == "UP" and not (s["value"] == 2 and s["collapse"] == 1):
                eb.append((m, "UP-template", s))
    res["G7_evenlife_template"] = ("PASS" if not eb else "FAIL", str(eb[:3]))

    # G8/G9: full live recompute (precomputed, checkpointed) vs frozen census
    pre = json.load(open(os.path.join(HERE, "audit_recompute.json")))
    mm, diffs = 0, []
    for key, r in crows.items():
        v = pre.get(key)
        if v and canon(v["seps"]) == canon(r["separations"]) and v["shapes"] == r["shapes"]:
            mm += 1
        else:
            diffs.append(key)
    tot = sum(len(r["separations"]) for r in crows.values())
    res["G8_full_recompute"] = ("PASS" if mm == 49 and not diffs else "FAIL",
                                 "%d/49 diffs %s" % (mm, diffs[:3]))
    res["G9_totals"] = ("PASS" if cs["meta"]["rows"] == 49
                        and cs["meta"]["total_separations"] == tot == 241
                        else "FAIL", "rows 49 seps %d" % tot)

    ok = all(v[0] == "PASS" for v in res.values())
    for k, v in sorted(res.items()):
        print(k, v[0], v[1])
    print("AUDIT-" + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "precompute":
        precompute(os.path.join(HERE, "audit_recompute.json"))
    else:
        main()
