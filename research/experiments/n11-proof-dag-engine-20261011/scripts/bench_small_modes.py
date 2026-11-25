"""Small solved-position comparison of proof search ordering and state sharing."""
import argparse
import gzip
import hashlib
import json
import time
from pathlib import Path

from dag_builder import build_certificate
from dag_verifier import verify_certificate


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out.resolve()
    if out.exists():
        ap.error(f"refusing to overwrite {out}")
    rows = []
    for sharing in ("d4", "none"):
        for order in ("count-asc", "count-desc", "key"):
            start = time.monotonic()
            certificate, stats = build_certificate(4, 0, order=order,
                                                   state_sharing=sharing,
                                                   node_limit=100000)
            verified = verify_certificate(certificate)
            payload = (json.dumps(certificate, sort_keys=True,
                                  separators=(",", ":")) + "\n").encode()
            rows.append(dict(state_sharing=sharing, order=order,
                             wall_seconds=time.monotonic() - start,
                             proof_stats=stats, verification=verified,
                             json_bytes=len(payload),
                             gzip_bytes=len(gzip.compress(payload, mtime=0))))
    out.parent.mkdir(parents=True, exist_ok=True)
    data = dict(schema="n11-proof-dag-small-mode-benchmark-v1",
                board_size=4, root_mask="0", solver_outcome=2, rows=rows)
    payload = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
    out.write_bytes(payload)
    manifest = dict(schema="n11-proof-dag-small-mode-manifest-v1",
                    path=out.name, bytes=len(payload),
                    sha256=hashlib.sha256(payload).hexdigest())
    (out.parent / "small-mode-manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8")
    print(json.dumps(rows, sort_keys=True))


if __name__ == "__main__":
    main()
