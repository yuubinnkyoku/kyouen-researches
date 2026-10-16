"""Resumable parallel driver for the n=9, k=9 exhaustive enumeration.

For each D4 first-stone orbit representative it repeatedly runs
nine_stone_exact_search with enumerate_all=1 and a node limit, resuming from the
saved timeout prefix, accumulating every maximal size-9 safe set.  Progress is
persisted after every chunk, so the run can be stopped and relaunched.

Usage: python3 enumerate_n9.py <root> <node_limit> <wall_seconds>
The binary is expected at ./enum (build nine_stone_exact_search.cpp with -O3).
"""
import json
import os
import subprocess
import sys
import time

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(D, "..", "output"))
os.makedirs(OUT, exist_ok=True)
root = int(sys.argv[1])
NODE = int(sys.argv[2])
WALL = float(sys.argv[3]) if len(sys.argv) > 3 else 9000.0
state_path = os.path.join(OUT, "state_root%d.json" % root)

sets = []
seen = set()
total = 0
chunks = 0
rp = None
if os.path.exists(state_path):
    st = json.load(open(state_path))
    if st.get("complete"):
        print("root", root, "already complete")
        sys.exit(0)
    sets = st["sets"]
    seen = {tuple(s) for s in sets}
    total = st["nodes"]
    chunks = st["chunks"]
    rp = st["rp"]

t0 = time.time()
status = "running"
while True:
    args = [os.path.join(D, "enum"), "9", "9", "0", str(root),
            (rp if rp else "-"), "1", str(NODE)]
    p = subprocess.run(args, capture_output=True, text=True)
    if not p.stdout.strip():
        status = "no-output"
        break
    d = json.loads(p.stdout)
    total += d["nodes"]
    chunks += 1
    for s in d["maximal_sets"]:
        key = tuple(s)
        if key not in seen:
            seen.add(key)
            sets.append(s)
    if d["complete"]:
        status = "complete"
        rp = None
    else:
        tp = d["timeout_prefix"]
        if not tp or tp[0] != root:
            status = "stuck"
        else:
            rp = ",".join(str(x) for x in tp)
            status = "running"
            if time.time() - t0 > WALL:
                status = "wall"
    json.dump({"n": 9, "k": 9, "root": root, "complete": status == "complete",
               "status": status, "nodes": total, "chunks": chunks, "rp": rp,
               "sets": sets}, open(state_path, "w"))
    print("root", root, "chunk", chunks, "nodes", total, "sets", len(sets),
          "status", status, flush=True)
    if status in ("complete", "stuck", "no-output"):
        break
    if status == "wall":
        break
