"""Cold partial re-verification: fresh process, recompute a hierarchical
sample of r=8 verdicts from scratch and compare against the committed
compact record. Complements the warm audit build (whose C11 is circular)
and the future CI cold full run."""
import importlib.util
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "vrf", os.path.join(HERE, "verify_remo_k_branch_r8_sweep.py"))
vrf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vrf)

comp = {}
with open(os.path.join(HERE, "sweep_r8_verdicts_compact.jsonl")) as f:
    for line in f:
        j = json.loads(line)
        comp[j["i"]] = j
N = len(comp)

audit = json.load(open(os.path.join(HERE, "output",
                                    "remo_k_branch_r8_sweep_audit.json")))
wit = set()
for k, v in audit["failing_partition_and_witnesses"].items():
    wit.add(tuple(v["det_witness"]["atoms"]))
    wit.add(tuple(v["ndet_witness"]["atoms"]))

prof10 = vrf.constrained_profiles(10)
assert len(prof10) == N

sample = [i for i in range(N) if i % 13 == 0]
widx = {a: i for i, a in enumerate(prof10)}
for a in wit:
    sample.append(widx[a])
sample = sorted(set(sample))
print("sample size: %d (stride 13: %d, witnesses: %d)"
      % (len(sample), sum(1 for i in sample if i % 13 == 0), len(wit)))

mism = 0
skipped = 0
t0 = time.time()
for n, i in enumerate(sample):
    a = prof10[i]
    t1 = time.time()
    v, _ = vrf.region_verdict(a, 3, 8, 20_000_000)
    dt = time.time() - t1
    assert v is not None, (i, a)
    j = comp[i]
    o0 = v["orders"][0] if v["order_determined"] else None
    ok = (tuple(j["a"]) == a and j["d"] == v["determined"]
          and j["od"] == v["order_determined"] and j["s"] == v["survivors"]
          and j["fl"] == v["first_losers"] and j["o0"] == o0)
    if not ok:
        mism += 1
        print("MISMATCH i=%d a=%s compact=%s cold=%s" % (i, a, j, v))
    if dt > 20:
        print("  slow i=%d a=%s %.1fs d=%s" % (i, a, dt, v["determined"]))
    if n % 25 == 0:
        print("  %d/%d done (%.0fs)" % (n, len(sample), time.time() - t0))
print("cold sample: %d profiles, %d mismatches, %.0fs total"
      % (len(sample), mism, time.time() - t0))
assert mism == 0, "cold sample mismatch"
print("COLD SAMPLE OK")
