#!/usr/bin/env python3
"""Assemble one cost-78a WIN7 certificate from a blind-extraction rows file.

The extraction driver (scripts/cert_driver78a.ts) writes rows only, in
traversal order, as "<32-hex board> <move>" lines.  This assembler sorts the
rows lexicographically, rejects duplicate board keys, prepends the
n11-terminal-strategy-v1 header and root line, and writes the certificate.
It also emits a small JSON receipt with row count, bytes, md5, sha256 and the
git blob sha, so the manifest can be built without re-reading the file.

Usage:
  python assemble_cost78a_certificate_20261115.py \
      --bit 29 --root 00000000000000809102000020400000 \
      --rows <rows file> --out <cert file> [--receipt <json file>]
"""
import argparse
import hashlib
import json
from pathlib import Path

HEADER = "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bit", type=int, required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--receipt", default=None)
    args = ap.parse_args()

    root = args.root.strip().lower()
    assert len(root) == 32 and all(c in "0123456789abcdef" for c in root), root

    raw = Path(args.rows).read_text().splitlines()
    rows = []
    seen = set()
    for line in raw:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        assert len(parts) == 2, line
        board, move = parts
        assert len(board) == 32 and all(c in "0123456789abcdef" for c in board), line
        assert board not in seen, "duplicate board row: " + board
        seen.add(board)
        rows.append((board, int(move)))
    assert rows, "no rows"
    rows.sort(key=lambda r: r[0])

    text = HEADER + "\n" + "root " + root + "\n" + "".join(
        f"{board} {move}\n" for board, move in rows)
    data = text.encode()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)

    receipt = {
        "bit": args.bit,
        "root_hex": root,
        "rows": len(rows),
        "bytes": len(data),
        "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha": git_blob_sha(data),
        "path": str(out),
        "rows_sorted_unique": True,
    }
    if args.receipt:
        Path(args.receipt).write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
