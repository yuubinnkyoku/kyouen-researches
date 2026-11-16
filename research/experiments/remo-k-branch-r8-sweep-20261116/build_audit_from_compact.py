"""Generate output/remo_k_branch_r8_sweep_audit.json WITHOUT the ~75 min
cold r=8 sweep: inject the committed compact per-profile record and the
warm_echo r=2..7 dormancy record into the verifier's _VERDICT_CACHE, then
call run() (which recomputes the full assembly twice and byte-checks).

The chain verdicts, Burnside counts, Theorem D recursion and the profile
enumeration are still recomputed from scratch here. CI re-derives the
injected verdicts cold (the committed audit is the byte-identity
authority), so this warm path is a convenience, not a second source of
truth. (C11 is circular in this warm path by construction; documented in
report.md.)
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "vrf", os.path.join(HERE, "verify_remo_k_branch_r8_sweep.py"))
vrf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vrf)

def verdict_from_compact(j):
    return {
        "determined": j["d"],
        "survivors": j["s"],
        "first_losers": j["fl"],
        "orders": [j["o0"]] if j["od"] else [],
        "order_determined": j["od"],
    }

n = 0
with open(os.path.join(HERE, vrf.COMPACT_NAME)) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        j = json.loads(line)
        vrf._VERDICT_CACHE[(tuple(j["a"]), 3, 8)] = (
            verdict_from_compact(j), 0)
        n += 1
print("injected compact r=8 verdicts: %d" % n)

m = 0
with open(os.path.join(HERE, "warm_echo.jsonl")) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        j = json.loads(line)
        v = {
            "determined": j["d"],
            "survivors": j["s"],
            "first_losers": j["fl"],
            "orders": j["orders"],
            "order_determined": j["od"],
        }
        vrf._VERDICT_CACHE[(tuple(j["a"]), 3, j["r"])] = (v, 0)
        m += 1
print("injected warm_echo r=2..7 verdicts: %d" % m)

vrf.run()
