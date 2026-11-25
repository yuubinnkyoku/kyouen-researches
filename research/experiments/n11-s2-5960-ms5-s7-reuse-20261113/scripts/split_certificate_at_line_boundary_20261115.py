#!/usr/bin/env python3
"""Split a large n11 certificate into two parts at a line boundary.

The repository convention keeps each tracked file under 1.75 MiB
(1,835,008 bytes); larger certificates are stored as
<name>.cert.part1of2 / <name>.cert.part2of2, split at a newline so that
concatenating the two parts reproduces the whole certificate byte-exactly.

This tool chooses the line boundary closest to half the file, writes the two
parts, removes the whole file, and prints a JSON receipt with the whole-file
hashes and the part hashes/sizes.
"""
import argparse
import hashlib
import json
from pathlib import Path


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", required=True)
    ap.add_argument("--keep-whole", action="store_true")
    args = ap.parse_args()

    path = Path(args.cert)
    data = path.read_bytes()
    assert data.endswith(b"\n")
    half = len(data) // 2
    cut = data.find(b"\n", half)
    assert cut != -1
    cut += 1
    part1, part2 = data[:cut], data[cut:]
    assert part1 + part2 == data
    assert part1.endswith(b"\n") and part2.endswith(b"\n")
    p1 = path.with_name(path.name + ".part1of2")
    p2 = path.with_name(path.name + ".part2of2")
    p1.write_bytes(part1)
    p2.write_bytes(part2)
    if not args.keep_whole:
        path.unlink()
    receipt = {
        "cert": str(path),
        "whole_bytes": len(data),
        "whole_md5": hashlib.md5(data).hexdigest(),
        "whole_sha256": hashlib.sha256(data).hexdigest(),
        "whole_git_blob_sha": git_blob_sha(data),
        "parts": [
            {"path": str(p1), "bytes": len(part1), "git_blob_sha": git_blob_sha(part1),
             "md5": hashlib.md5(part1).hexdigest()},
            {"path": str(p2), "bytes": len(part2), "git_blob_sha": git_blob_sha(part2),
             "md5": hashlib.md5(part2).hexdigest()},
        ],
        "joined_equals_whole": True,
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
