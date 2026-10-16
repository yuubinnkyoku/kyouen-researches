#!/usr/bin/env python3
"""Chunked, resumable driver for nine_stone_exact_search.

Usage: nine_run.py <n> <k> <tag> <node_limit> [tl_per_chunk]

Runs the search once per D4 first-stone orbit representative. Each chunk runs
with a node limit; when a chunk times out, the binary reports a resume prefix
and the driver continues from it. When every representative completes with no
witness, the result is an exhaustive exclusion for (n, k) under the D4
reduction. Every chunk's JSON is saved for audit.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

BIN = "/root/kyouen-n10/nine_stone/nine_stone_exact_search"


def main():
    n, k, tag, node_limit = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    tl = sys.argv[5] if len(sys.argv) > 5 else "0"
    roots_filter = sys.argv[6].split(",") if len(sys.argv) > 6 else None
    outdir = Path("/root/kyouen-n10/nine_stone")
    outdir.mkdir(parents=True, exist_ok=True)
    reps = subprocess.run([BIN, n, "0", "0", "-list"],
                          capture_output=True, text=True, check=True).stdout.split()
    if roots_filter is not None:
        reps = [r for r in reps if r in roots_filter]
        if not reps:
            print("empty root filter", flush=True)
            return 2
    print(f"tag={tag} n={n} k={k} reps={reps}", flush=True)
    total_chunks = 0
    for root in reps:
        resume = "-"
        while True:
            cmd = [BIN, n, k, tl, root, resume, "0", str(node_limit)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(proc.stdout)
            total_chunks += 1
            log = outdir / f"{tag}_root{root}_chunk{total_chunks}.json"
            log.write_text(proc.stdout, encoding="utf-8")
            if data["found"]:
                print(f"FOUND tag={tag} root={root} witness={data['witness']} "
                      f"log={log}", flush=True)
                # remove accumulated chunks except this one's? keep all for audit
                return 0
            if data["complete"]:
                print(f"tag={tag} root={root} complete none found "
                      f"(nodes={data['nodes']}, secs={data['seconds']:.0f})",
                      flush=True)
                break
            prefix = data["timeout_prefix"]
            if not prefix:
                print(f"tag={tag} root={root} NO RESUME PREFIX, stopping", flush=True)
                return 4
            resume = ",".join(map(str, prefix))
    print(f"tag={tag} EXHAUSTIVE: no maximal {k}-stone set on {n}x{n} over all "
          f"{len(reps)} first-stone orbit reps "
          f"(chunks={total_chunks})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
