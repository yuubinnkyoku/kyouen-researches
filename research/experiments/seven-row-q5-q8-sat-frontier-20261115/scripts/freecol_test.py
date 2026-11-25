#!/usr/bin/env python3
"""Free-column extension test: given a verified deficient-maximal witness at
(w, m, q), check the same stone set at larger widths m' > m (appended columns
are empty; the config stays safe, and stays maximal iff every appended cell
lies on a line/circle with >= q-1 stones). Prints the largest width that
still verifies, per source witness."""
import json, subprocess, sys

VW = "/home/user/kr/scripts/verify_witness.py"

def verify(w, m, q, stones):
    p = subprocess.run([sys.executable, VW, str(w), str(m), str(q)],
                       input=json.dumps(stones), capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"ok": False, "err": p.stdout + p.stderr}

def probe(name, w, m0, q, stones, limit):
    res = {"name": name, "w": w, "q": q, "source_m": m0, "extends_to": None, "chain": []}
    m = m0
    # first confirm at source width
    r = verify(w, m, q, stones)
    res["chain"].append({"m": m, "ok": r.get("ok")})
    while m < limit:
        m += 1
        r = verify(w, m, q, stones)
        res["chain"].append({"m": m, "ok": r.get("ok"), "uncovered": r.get("uncovered_cells")})
        if not r.get("ok"):
            break
    res["extends_to"] = m - 1 if res["chain"][-1].get("ok") is False else m
    # fix extends_to: last ok width
    last_ok = None
    for c in res["chain"]:
        if c.get("ok"):
            last_ok = c["m"]
    res["extends_to"] = last_ok
    return res

def main():
    out = []
    # (7,5) m=32 rowY=0 SAT witness (calibration C2, published-identical CNF)
    st = json.load(open("/home/user/kr/out/cal/s7x32q5_rowY0.witness.json"))["stones"]
    out.append(probe("7x32q5-rowY0-SAT", 7, 32, 5, st, 40))
    # (7,6) m=27 rowY=3 SAT witness
    st = json.load(open("/home/user/kr/wit/q6m27.json"))["stones"]
    out.append(probe("7x27q6-rowY3-SAT", 7, 27, 6, st, 35))
    # (7,7) m=26 rowY=3 SAT witness (bare stone list)
    st = json.load(open("/home/user/kr/wit/q7m26.json"))
    out.append(probe("7x26q7-rowY3-SAT", 7, 26, 7, st, 33))
    # (7,8) m=24 rowY=3 SAT witness
    st = json.load(open("/home/user/kr/wit/q8m24.json"))["stones"]
    out.append(probe("7x24q8-rowY3-SAT", 7, 24, 8, st, 31))
    # (7,4) m=53 SA base (extends to 56 per SA lane)
    st = json.load(open("/home/user/kr/wit/q4band56.json"))["53"]
    if isinstance(st, dict):
        st = st["stones"]
    out.append(probe("7x53q4-SA-base", 7, 53, 4, st, 62))
    print(json.dumps(out, indent=1))

main()
