"""Warm-start data for the r=8 verifier: r=2..7 verdicts of the 278
profiles on the 10 new failing keys (ECHO dormancy check).

Resumable: appends one JSON line per computed verdict to warm_echo.jsonl.
"""
import importlib.util
import json
import os
import sys

spec = importlib.util.spec_from_file_location(
    "vrf", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "verify_remo_k_branch_r8_sweep.py"))
vrf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vrf)

KEYS = set()
for fam in ((6, 6, 8), (6, 8, 8)):
    for g in range(5):
        KEYS.add((fam, g))

done = {}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "warm_echo.jsonl")
if os.path.exists(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            j = json.loads(line)
            done[(tuple(j["a"]), j["r"])] = j

prof10 = vrf.constrained_profiles(10)
profs = [a for a in prof10 if vrf.key_of(a) in KEYS]
sys.stderr.write("target profiles: %d\n" % len(profs))
todo = [(a, r) for r in range(2, 8) for a in profs
        if (a, r) not in done]
sys.stderr.write("todo: %d (done %d)\n" % (len(todo), len(done)))
with open(path, "a") as f:
    for a, r in todo:
        v, _ = vrf.region_verdict_cached(a, 3, r)
        assert v is not None, (a, r)
        f.write(json.dumps({"a": list(a), "r": r,
                            "d": v["determined"], "od": v["order_determined"],
                            "s": v["survivors"], "fl": v["first_losers"],
                            "orders": v["orders"]}) + "\n")
        f.flush()
sys.stderr.write("warm_echo complete: %d records\n"
                 % (len(done) + len(todo)))
