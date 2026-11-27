#!/usr/bin/env python3
# run_lane.py — batch driver for the four declared 6x26 q=6 lanes (2026-11-28).
# Generates CNFs with the byte-cloned sat3.js (sha256 e04581eb..., inside the lane
# scripts/ dir), runs one kissat 4.0.4 official linux-amd64 invocation per probe
# (sha256 21da5d98...) under `timeout -s TERM <cap>`, and publishes raw logs,
# encoder meta json and records.jsonl into the lane output dir.
#
# Usage (inside WSL):
#   python3 run_lane.py <lane_scripts_dir> <lane_out_dir_mnt> <work_cnf_dir> <parallel> <spec.json>
#
# spec.json: {"probes": [{"id": "...", "w":6, "m":26, "q":6,
#                         "class":"2", "krow":"2:4", "minpos": 11 or null,
#                         "cap_s": 272, "note": "..."}],
#             "positive_control": {...same shape, cap_s 275...} or null}
import json
import os
import re
import subprocess
import sys
import concurrent.futures as cf

KISSAT = os.path.expanduser("~/lane-work/kissat/kissat-4.0.4-linux-amd64")


def gen_cnf(scripts, work, p):
    """Generate one CNF with the byte-cloned sat3.js; return (meta, cnf_path)."""
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, "cnf_%s.cnf" % p["id"])
    argv = ["node", os.path.join(scripts, "sat3.js"),
            str(p["w"]), str(p["m"]), str(p["q"]),
            "--class=%s" % p["class"], "--krow=%s" % p["krow"]]
    if p.get("minpos") is not None:
        argv.append("--minpos=%d" % p["minpos"])
    argv.append(cnf)
    r = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError("gen failed %s: %s %s" % (p["id"], r.stdout, r.stderr))
    meta = json.loads(r.stdout.strip().splitlines()[-1])
    return meta, cnf


def parse_log(path):
    """Return (result, conflicts, process_time_s) from a raw kissat log."""
    result = None
    conflicts = None
    ptime = None
    with open(path, "r", errors="replace") as f:
        for line in f:
            if line.startswith("s SATISFIABLE"):
                result = "SAT"
            elif line.startswith("s UNSATISFIABLE"):
                result = "UNSAT"
            else:
                m = re.match(r"^c conflicts:\s+(\d+)", line)
                if m:
                    conflicts = int(m.group(1))
                m = re.match(r"^c process-time:\s+\S+\s+(\d+\.\d+) seconds", line)
                if m:
                    ptime = float(m.group(1))
    if result is None:
        result = "INDET"  # cap reached (SIGTERM), no solution line
    return result, conflicts, ptime


def run_probe(scripts, work, outdir, p):
    meta, cnf = gen_cnf(scripts, work, p)
    raw = os.path.join(outdir, "r%s.txt" % p["id"])
    cap = p["cap_s"]
    subprocess.run(["timeout", "-s", "TERM", str(cap), KISSAT, cnf],
                   stdout=open(raw, "w"), stderr=subprocess.DEVNULL, timeout=cap + 120)
    result, conflicts, ptime = parse_log(raw)
    metaj = os.path.join(outdir, "meta_%s.json" % p["id"])
    with open(metaj, "w") as f:
        json.dump(meta, f, indent=0)
        f.write("\n")
    rec = {"id": p["id"], "board": [p["w"], p["m"], p["q"]],
           "class": [int(c) for c in str(p["class"]).split(",")],
           "krow": [p["krow"]],
           "minpos": p.get("minpos"), "result": result,
           "conflicts": conflicts, "cap_s": cap,
           "process_time_s": ptime, "note": p.get("note", "")}
    return rec


def main():
    scripts, outdir, work, par, specpath = sys.argv[1:6]
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    with open(specpath) as f:
        spec = json.load(f)
    probes = spec["probes"]
    records = []
    pc = spec.get("positive_control")
    if pc:
        rec = run_probe(scripts, work, outdir, pc)
        records.append(rec)
        print("CONTROL", json.dumps(rec), flush=True)
        if rec["result"] != "SAT":
            print("CONTROL-NOT-SAT — aborting lane", flush=True)
            write_records(outdir, records)
            return 2
    with cf.ThreadPoolExecutor(max_workers=int(par)) as ex:
        futs = {ex.submit(run_probe, scripts, work, outdir, p): p for p in probes}
        for fut in cf.as_completed(futs):
            rec = fut.result()
            records.append(rec)
            print("PROBE", json.dumps(rec), flush=True)
    write_records(outdir, records)
    return 0


def write_records(outdir, records):
    recs = sorted(records, key=lambda r: r["id"])
    with open(os.path.join(outdir, "records.jsonl"), "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    n_indet = sum(1 for r in recs if r["result"] == "INDET" and r["cap_s"] == 272)
    n_sat = [r for r in recs if r["result"] == "SAT"]
    summary = {
        "probes": len(recs),
        "INDET_at_272s": n_indet,
        "SAT": [{"id": r["id"], "conflicts": r["conflicts"]} for r in n_sat],
        "UNSAT": [r["id"] for r in recs if r["result"] == "UNSAT"],
    }
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("DONE", json.dumps(summary), flush=True)


if __name__ == "__main__":
    sys.exit(main())
