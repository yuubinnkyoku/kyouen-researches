#!/usr/bin/env python3
"""kit-17x independent blind second census (kit-17 registered rows).

Independence: engine = published engine_block.py byte-clone (sha256
582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0). Row
semantics independently reconstructed and validated against ALL 49 published
kit-16 rows before any kit-17 row was measured:
    row (R, z, m): R = z + m + 1; S in m..smax, smax = max(m+38, z+2);
    shapes = multisets of 1..3 tokens, each token >= m, sum S, containing m;
    separation iff H_canonical(R, X, z) != single_token(S, z, R).

Modes:
  validate : recompute all 49 kit-16 rows and compare with the published
             kit-16 frozen .out (order-independent content equality).
  census   : census the kit-17 registered rows from the published kit-16
             frozen .out future constants (+ window proposals + even-m
             z=3m+14 continuation) and write census output JSON.

Usage:
  census_kit17x.py validate <kit16.out>
  census_kit17x.py census   <kit16.out> <out.json>
"""
import json, sys, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine_block import H_canonical, single_token

K16_SHA = "85c04e431b53d4f1d5538cd152c9b05bb475379be6243ef26a9022a4cb4c9589"

def shapes_for(S, m):
    """multisets of 1..3 tokens, each token >= m, sum S, containing m."""
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

def load_k16(path):
    s = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert s == K16_SHA, ("kit-16 .out sha mismatch", s)
    return json.load(open(path))

def validate(k16path):
    d = load_k16(k16path)
    rows = [x for x in d["sections"] if x.get("section", "").endswith("_row_record")]
    ok, bad = 0, []
    for r in rows:
        lo, hi = r["s_domain"].strip("{}").split("..")
        assert int(lo) == r["min"]
        seps, n = census_row(r["R"], r["z"], r["min"], int(hi))
        if canon(seps) == canon(r["separations"]) and n == r["shapes"]:
            ok += 1
        else:
            bad.append(r["section"])
        print("%s shapes %d/%d seps %d/%d %s" %
              (r["section"], n, r["shapes"], len(seps), len(r["separations"]),
               "OK" if not bad or bad[-1] != r["section"] else "MISMATCH"), flush=True)
    print("VALIDATE %d/%d ok bad=%s" % (ok, len(rows), bad))
    return ok == len(rows)

def census(k16path, outpath):
    d = load_k16(k16path)
    fut = [x for x in d["sections"] if x.get("section") == "future_slice_registration_constants"][0]
    items = fut["registered_for_next_execution_kit_log_S5"][0][0]
    rows = []
    for it in items:
        m, z = it.get("m"), it.get("z")
        if m is None or z is None:
            continue
        if isinstance(z, str):
            a, b = z.split("..")
            for zz in range(int(a), int(b) + 1):
                rows.append({"kind": it["kind"], "m": m, "z": zz, "R": zz + m + 1,
                             "smax": max(m + 38, zz + 2)})
        else:
            rows.append({"kind": it["kind"], "m": m, "z": z, "R": z + m + 1,
                         "smax": max(m + 38, z + 2)})
    for m in (14, 16, 18):  # even-m lifecycle next-depth z=3m+14 continuation
        z = 3 * m + 14
        rows.append({"kind": "evenlife-nextdepth", "m": m, "z": z,
                     "R": z + m + 1, "smax": max(m + 38, z + 2)})
    out = {}
    for i, r in enumerate(rows):
        seps, n = census_row(r["R"], r["z"], r["m"], r["smax"])
        out["%d_%d" % (r["m"], r["z"])] = dict(r, shapes=n, separations=seps)
        print("row %d/%d m=%d z=%d shapes=%d seps=%d" %
              (i + 1, len(rows), r["m"], r["z"], n, len(seps)), flush=True)
    json.dump(out, open(outpath, "w"))
    print("CENSUS-DONE rows=%d seps=%d" %
          (len(out), sum(len(v["separations"]) for v in out.values())))

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "validate":
        sys.exit(0 if validate(sys.argv[2]) else 1)
    elif mode == "census":
        census(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(2)
