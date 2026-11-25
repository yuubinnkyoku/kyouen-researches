#!/usr/bin/env python3
"""Resume driver: continues a nine_stone_exact_search run from saved chunks.

Usage: nine_run_resume.py <n> <k> <tag> <node_limit> <roots_csv>

For each root, the last saved chunk is inspected. If it completed, the root is
done. Otherwise the search resumes from that chunk's timeout_prefix (the same
conservative lexicographic frontier rule as round56), saving new chunks with
continuing numbering.
"""
import json
import subprocess
import sys
from pathlib import Path

BIN = "/root/kyouen-n10/nine_stone/nine_stone_exact_search"
OUTDIR = Path("/root/kyouen-n10/nine_stone")


def main():
    n, k, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    node_limit = int(sys.argv[4])
    roots = sys.argv[5].split(",")
    for root in roots:
        chunks = sorted(
            OUTDIR.glob(f"{tag}_root{root}_chunk*.json"),
            key=lambda p: int(p.stem.split("chunk")[1]),
        )
        resume = "-"
        if chunks:
            last = json.loads(chunks[-1].read_text(encoding="utf-8"))
            if last["complete"]:
                print(f"tag={tag} root={root} already complete "
                      f"(found={last['found']})", flush=True)
                if last["found"]:
                    print(f"FOUND tag={tag} root={root} "
                          f"witness={last['witness']}", flush=True)
                    return 0
                continue
            resume = ",".join(map(str, last["timeout_prefix"]))
            print(f"tag={tag} root={root} resuming from "
                  f"{last['timeout_prefix']} (chunk {chunks[-1].name})",
                  flush=True)
        else:
            print(f"tag={tag} root={root} no chunks, starting fresh", flush=True)
        idx = len(chunks)
        while True:
            cmd = [BIN, n, k, "0", root, resume, "0", str(node_limit)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(proc.stdout)
            idx += 1
            log = OUTDIR / f"{tag}_root{root}_chunk{idx}.json"
            log.write_text(proc.stdout, encoding="utf-8")
            if data["found"]:
                print(f"FOUND tag={tag} root={root} witness={data['witness']} "
                      f"log={log}", flush=True)
                return 0
            if data["complete"]:
                print(f"tag={tag} root={root} complete none found "
                      f"(nodes={data['nodes']}, secs={data['seconds']:.0f})",
                      flush=True)
                break
            prefix = data["timeout_prefix"]
            if not prefix:
                print(f"tag={tag} root={root} NO RESUME PREFIX, stopping",
                      flush=True)
                return 4
            resume = ",".join(map(str, prefix))
    return 0


if __name__ == "__main__":
    sys.exit(main())
