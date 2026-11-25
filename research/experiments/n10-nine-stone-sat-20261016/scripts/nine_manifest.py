#!/usr/bin/env python3
"""Build a manifest of the exhaustive-search chunk files.

Hashes every chunk JSON of a tag and records per-root totals, so the
computation committed with this experiment is auditable end to end.
"""
import hashlib
import json
import sys
from pathlib import Path

OUTDIR = Path("/root/kyouen-n10/nine_stone")


def main():
    tag = sys.argv[1]
    roots = {}
    for p in sorted(OUTDIR.glob(f"{tag}_root*_chunk*.json")):
        root = int(p.stem.split("_root")[1].split("_chunk")[0])
        idx = int(p.stem.split("_chunk")[1])
        data = p.read_bytes()
        d = json.loads(data)
        roots.setdefault(root, {})[idx] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "complete": d["complete"],
            "found": d["found"],
            "nodes": d["nodes"],
            "seconds": d["seconds"],
            "resume_prefix": d["resume_prefix"],
            "timeout_prefix": d["timeout_prefix"],
        }
    manifest = {"tag": tag, "roots": roots}
    Path(f"/root/kyouen-n10/nine_stone/manifest_{tag}.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    total_nodes = sum(c["nodes"] for r in roots.values() for c in r.values())
    print(f"{tag}: roots={len(roots)} chunks="
          f"{sum(len(r) for r in roots.values())} nodes={total_nodes:,}")


if __name__ == "__main__":
    main()
