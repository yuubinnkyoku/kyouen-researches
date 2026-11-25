#!/usr/bin/env python3
"""Audit the exhaustive k=9 chunk chain for (n,k,tag).

For every first-stone root, all chunks must form a continuous chain:
  chunk[0] starts fresh; chunk[i]'s resume_prefix equals chunk[i-1]'s
  timeout_prefix; the final chunk has complete=true; no chunk has found=true.
"""
import json
import sys
from pathlib import Path

OUTDIR = Path("/root/kyouen-n10/nine_stone")


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "nine_k9"
    ok = True
    grand_nodes = 0
    grand_secs = 0.0
    roots = {}
    for p in OUTDIR.glob(f"{tag}_root*_chunk*.json"):
        root = int(p.stem.split("_root")[1].split("_")[0])
        idx = int(p.stem.split("_chunk")[1])
        roots.setdefault(root, {})[idx] = p
    print(f"== {tag}: roots={sorted(roots)}")
    for root in sorted(roots):
        chunks = roots[root]
        idxs = sorted(chunks)
        if idxs != list(range(1, len(idxs) + 1)):
            print(f"  root={root} GAP NUMBERING: {idxs[0]}..{idxs[-1]} "
                  f"count={len(idxs)}")
            ok = False
        prev_prefix = []
        total_nodes = 0
        total_secs = 0.0
        for i in idxs:
            d = json.loads(chunks[i].read_text(encoding="utf-8"))
            if d["found"]:
                print(f"  root={root} chunk{i}: FOUND witness={d['witness']}")
                ok = False
            rp = d["resume_prefix"]
            if i == 1:
                if rp:
                    print(f"  root={root} chunk1: unexpected resume_prefix {rp}")
                    ok = False
            else:
                if rp != prev_prefix:
                    print(f"  root={root} chunk{i}: resume_prefix {rp} != "
                          f"prev timeout_prefix {prev_prefix}")
                    ok = False
            prev_prefix = d["timeout_prefix"]
            total_nodes += d["nodes"]
            total_secs += d["seconds"]
        last = json.loads(chunks[idxs[-1]].read_text(encoding="utf-8"))
        if not last["complete"]:
            print(f"  root={root}: LAST CHUNK NOT COMPLETE "
                  f"timeout_prefix={last['timeout_prefix']}")
            ok = False
        grand_nodes += total_nodes
        grand_secs += total_secs
        print(f"  root={root:>3}: chunks={len(idxs)} "
              f"nodes={total_nodes:>13,} secs={total_secs:>7.0f} "
              f"complete={last['complete']} found={last['found']}")
    print(f"  TOTAL: nodes={grand_nodes:,} proc-secs={grand_secs:.0f}")
    print(f"AUDIT {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
