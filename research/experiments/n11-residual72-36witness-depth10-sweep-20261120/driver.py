#!/usr/bin/env python3
# K1075 residual-72 fresh-safe 36-root depth-10 sweep.
# runner v17 is pinned by git blob c132cc6425eee3feaeef1d697dd74f968cfedb59.
# Both AND orderings, cap 30M, pilot_d6 control, RAW child hex.
# Resume-safe: successful (root, ordering) records are skipped.
import json, os, subprocess, sys, time
from pathlib import Path

D = Path(__file__).resolve().parent
RUNNER = D / "runner_v17.ts"
CAP = 30_000_000
NW = 4
TIMEOUT = 280

W = int(sys.argv[1])
if W not in range(NW):
    raise SystemExit("worker id must be 0..3")
roots = json.loads((D / "roots.json").read_text())
mine = roots[W::NW]
outf = D / "output" / f"probe-records-w{W}.jsonl"
logf = D / "output" / f"worker{W}.log"

def log(s):
    with logf.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%S%z") + " " + s + "\n")
        f.flush()
        os.fsync(f.fileno())

done = set()
if outf.exists():
    for line in outf.read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
            if "result" in rec and rec.get("error") is None:
                done.add((rec["root"], rec["ordering"]))
        except Exception:
            pass
log(f"worker {W} starting, {len(mine)} roots, {len(done)} successful probes already recorded")
for idx, item in enumerate(mine):
    root, child, bit = item["root"], item["child"], item["bit"]
    for ordering in (1, 0):
        key = (root, f"andclose{ordering}")
        if key in done:
            continue
        rec_path = D / "output" / f".tmp-{W}-{root}-{ordering}.jsonl"
        if rec_path.exists():
            rec_path.unlink()
        t0 = time.time()
        cmd = ["node", "--experimental-strip-types", str(RUNNER),
               "--bits", str(bit), "--depth", "10", "--cap", str(CAP),
               "--andclose", str(ordering), "--child", child, "--out", str(rec_path)]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, cwd=D)
            rc, stdout, stderr = r.returncode, r.stdout.strip(), r.stderr.strip()
        except subprocess.TimeoutExpired as e:
            rc, stdout, stderr = "timeout", "", str(e.stderr or "")[-500:]
        wall = round(time.time() - t0, 1)
        control = result = None
        if rec_path.exists():
            for line in rec_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                obj = json.loads(line)
                if "control" in obj:
                    control = obj
                else:
                    result = obj
        rec = {"root": root, "ordering": f"andclose{ordering}", "cap": CAP,
               "worker": W, "seq": idx, "covered_rows": item["rows"],
               "bit": bit, "child": child, "wall_s": wall,
               "runner_blob": "c132cc6425eee3feaeef1d697dd74f968cfedb59"}
        if rc == "timeout":
            rec["error"] = f"timeout-{TIMEOUT}s"
            rec["control"] = control
            rec["stderr_tail"] = stderr[-500:]
        elif rc != 0:
            rec["error"] = f"exit-{rc}"
            rec["stdout_tail"] = stdout[-500:]
            rec["stderr_tail"] = stderr[-500:]
            rec["control"] = control
        elif result is None:
            rec["error"] = "missing-result"
            rec["stdout_tail"] = stdout[-500:]
            rec["stderr_tail"] = stderr[-500:]
            rec["control"] = control
        else:
            rec["control"] = control
            rec["result"] = result
        with outf.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())
        log(f"{root} ordering={ordering} rc={rc} wall={wall}s nodes={result['nodes'] if result else '?'} loss={result['loss'] if result else '?'} capped={result['capped'] if result else '?'}")
        if rec_path.exists():
            rec_path.unlink()
log(f"worker {W} done")
