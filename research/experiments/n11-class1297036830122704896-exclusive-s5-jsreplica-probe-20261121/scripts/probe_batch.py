#!/usr/bin/env python3
"""Slice driver for the declared probe order. Runs keys until slice time
budget used; per key: 2M stage, then 15M twice on UNKNOWN; determinism
required on any resolved stage; WIN halts (stopping rule 1). Progress and
per-key raws under kit lane/. Deterministic: re-runs reproduce byte-exact
rows except wall_s."""
import json, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pub_paths

P = pub_paths.resolve(__file__)
LANE = Path(__file__).resolve().parent
EXP = P["exp"]
RAW = EXP / "output" / "raw"
INP = EXP / "input"
JS = P["jsrelay"]
SELECTION = json.loads((EXP / "output" / "exclusive-selection.json").read_text())
KEYS = [r["key"] for r in SELECTION["exclusive_probe_order"]]
LEGAL = {r["key"]: r["legal"] for r in SELECTION["exclusive_probe_order"]}
TIME_BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 115.0

RAW.mkdir(parents=True, exist_ok=True)
INP.mkdir(parents=True, exist_ok=True)
pp = LANE / "progress.json"  # kit-local bookkeeping, not part of published audit
prog = json.loads(pp.read_text()) if pp.exists() else {"done": [], "parked": [], "win": None}

def run(budget, k, tag):
    lo, hi = k.split(":")
    ip = INP / f"batch-s5-{lo}-{hi}.input.csv"
    if not ip.exists():
        ip.write_text(f"target,0,5,{lo},{hi},{LEGAL[k]},0,0,0,0,0\n")
    out = RAW / f"{tag}-s5-{lo}-{hi}.out.csv"
    t0 = time.time()
    r = subprocess.run(["node", str(JS), f"--exact-replay={ip}", f"--exact-replay-budget={budget}"],
                       capture_output=True, text=True, check=True)
    out.write_text(r.stdout)
    row = [l for l in r.stdout.split("\n") if l.startswith("replay,")]
    assert len(row) == 1
    f = row[0].split(",")
    return int(f[6]), int(f[7]), time.time() - t0

t0 = time.time()
log = []
for k in KEYS:
    if time.time() - t0 > TIME_BUDGET:
        break
    if k in prog["done"] or k in prog["parked"] or prog["win"]:
        continue
    e = {"key": k}
    res2, nodes2, w2 = run(2_000_000, k, "at2m")
    e["at2m"] = {"result": res2, "nodes": nodes2, "wall_s": round(w2, 3)}
    if res2 == 0:
        r1, n1, w1 = run(15_000_000, k, "at15m")
        r2, n2, w2b = run(15_000_000, k, "at15m-run2")
        if (r1, n1) != (r2, n2):
            prog["halt"] = {"reason": "determinism", "key": k, "run1": [r1, n1], "run2": [r2, n2]}
            pp.write_text(json.dumps(prog, indent=1)); print("HALT determinism", k); sys.exit(1)
        e["at15m"] = {"result": r1, "nodes": n1, "wall_s": round(w1, 3)}
        e["at15m_run2"] = {"result": r2, "nodes": n2, "wall_s": round(w2b, 3)}
        if r1 == 1:
            prog["win"] = k; e["verdict"] = "WIN"
            pp.write_text(json.dumps(prog, indent=1)); print("HALT WIN", k); sys.exit(0)
        if r1 == 2:
            prog["done"].append(k); e["verdict"] = "LOSS"
        else:
            prog["parked"].append(k); e["verdict"] = "UNKNOWN@15M"
    else:
        r2b, n2b, w2b = run(2_000_000, k, "at2m-run2")
        if (res2, nodes2) != (r2b, n2b):
            prog["halt"] = {"reason": "determinism@2m", "key": k}
            pp.write_text(json.dumps(prog, indent=1)); print("HALT det2m", k); sys.exit(1)
        e["at2m_run2"] = {"result": r2b, "nodes": n2b, "wall_s": round(w2b, 3)}
        if res2 == 1:
            prog["win"] = k; e["verdict"] = "WIN@2m"
            pp.write_text(json.dumps(prog, indent=1)); print("HALT WIN@2m", k); sys.exit(0)
        prog["done"].append(k); e["verdict"] = "LOSS@2m"
    log.append(e)
    pp.write_text(json.dumps(prog, indent=1))
print(json.dumps({"done": len(prog["done"]), "parked": len(prog["parked"]), "win": prog["win"], "slice": log}, indent=1))
