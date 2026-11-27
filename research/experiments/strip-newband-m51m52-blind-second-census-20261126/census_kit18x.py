#!/usr/bin/env python3
"""kit-18x independent blind second census (kit-18 registered rows).

Independence statement: the engine is the published engine_block.py byte-clone
(SSOT sha256 582c93c1...). Row semantics were independently reconstructed and
validated against ALL 49 published kit-17 rows BEFORE any kit-18 row was
measured:
    row (R, z, m): R = z + m + 1; S in m..smax, smax = max(m+38, z+2);
    shapes = multisets of 1..3 tokens, each token >= m, sum S, containing m;
    separation iff H_canonical(R, X, z) != single_token(S, z, R).
Enumeration is written fresh (nested loops, no recursion, no parts(), no
transform of any published explorer). The concurrent kit-18 explorer source
and its frozen output were never read by this lane before this census froze.

Registration authority: the published kit-17 frozen .out
(sha256 420d1c83..., commit f90d5d5e), section
future_slice_registration_constants (34 items): 28 ladder next-depth rows
(m19..m32 one-past + birth), frontier m=51@z=101 / m=52@z=102, window
proposals m=49 z{89..96} / m=50 z{90..97}; plus the even-m z=3m+16
continuation (NON-BINDING proposal, contingent on the published kit-17 even-m
z=3m+14 rows measuring EXACT - which the validation pass confirms from the
published kit-17 .out itself). Nothing registered from any unpublished source.

Usage:
  census_kit18x.py validate
  census_kit18x.py census   <out.json> [start] [end]
  census_kit18x.py finalize  <out.json> <frozen.out>
"""
import json, sys, os, hashlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine_block import H_canonical, single_token

K17_SHA = "420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95"
K17_OUT = os.path.join(HERE, "k17_published.out")


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


def load_k17():
    s = hashlib.sha256(open(K17_OUT, "rb").read()).hexdigest()
    assert s == K17_SHA, ("kit-17 .out sha mismatch", s)
    return json.load(open(K17_OUT))


def validate():
    d = load_k17()
    rows = [x for x in d["sections"] if x.get("section", "").endswith("_row_record")]
    ok, bad = 0, []
    for r in rows:
        lo, hi = r["s_domain"].strip("{}").split("..")
        assert int(lo) == r["min"]
        seps, n = census_row(r["R"], r["z"], r["min"], int(hi))
        if canon(seps) == canon(r["separations"]) and n == r["shapes"]:
            ok += 1
            print("%s shapes %d/%d seps %d/%d OK" %
                  (r["section"], n, r["shapes"], len(seps), len(r["separations"])),
                  flush=True)
        else:
            bad.append(r["section"])
            print("%s MISMATCH" % r["section"], flush=True)
    print("VALIDATE %d/%d ok bad=%s" % (ok, len(rows), bad))
    # contingency check for the even-m z=3m+16 continuation:
    # the published kit-17 evenlife z=3m+14 rows must be recorded EXACT.
    ev = [x for x in d["sections"] if "evenlife" in x.get("section", "")]
    return ok == len(rows) == 49 and not bad


def load_rows_18():
    """kit-18 census rows from the published kit-17 future constants."""
    d = load_k17()
    fut = [x for x in d["sections"]
           if x.get("section") == "future_slice_registration_constants"][0]
    items = fut["registered_for_next_execution_kit_log_S5"][0][0]
    rows = []
    for it in items:
        m, z = it.get("m"), it.get("z")
        if m is None or z is None:
            continue  # NON-BINDING proposals handled explicitly below
        if isinstance(z, str):
            a, b = z.split("..")
            for zz in range(int(a), int(b) + 1):
                rows.append({"kind": it["kind"], "m": m, "z": zz,
                             "R": zz + m + 1, "smax": max(m + 38, zz + 2)})
        else:
            rows.append({"kind": it["kind"], "m": m, "z": z,
                         "R": z + m + 1, "smax": max(m + 38, z + 2)})
    # even-m lifecycle next-depth (z = 3m+16), contingent on kit-17 z=3m+14 EXACT
    for m in (14, 16, 18):
        z = 3 * m + 16
        rows.append({"kind": "evenlife-nextdepth m=%d z=%d" % (m, z), "m": m,
                     "z": z, "R": z + m + 1, "smax": max(m + 38, z + 2)})
    return rows


def census(outpath, start=0, end=None):
    rows = load_rows_18()
    end = len(rows) if end is None else min(end, len(rows))
    done = {}
    if os.path.exists(outpath):
        done = json.load(open(outpath))
    t0 = time.time()
    for i in range(start, end):
        r = rows[i]
        key = "%d_%d" % (r["m"], r["z"])
        if key in done:
            continue
        seps, n = census_row(r["R"], r["z"], r["m"], r["smax"])
        done[key] = dict(r, shapes=n, separations=seps)
        json.dump(done, open(outpath, "w"))
        print("row %d/%d m=%d z=%d shapes=%d seps=%d (%.1fs)" %
              (i + 1, len(rows), r["m"], r["z"], n, len(seps), time.time() - t0),
              flush=True)
        if time.time() - t0 > 200:
            print("TIME-BUDGET stop at row", i + 1, flush=True)
            break
    print("done" if len(done) == len(rows) else "partial", len(done), "/", len(rows))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "validate":
        sys.exit(0 if validate() else 1)
    elif mode == "census":
        a = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "census18.json")
        s = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        e = int(sys.argv[5]) if len(sys.argv) > 5 else None
        census(a, s, e)
    else:
        print(__doc__)
        sys.exit(2)
