#!/usr/bin/env python3
"""Check committed source, result, and compressed certificate SHA-256s."""
from pathlib import Path
import gzip
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest-5.json").read_text())
for name, expected in manifest["artifacts"].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
certificate = manifest["certificate"]
path = root / certificate["path"]
assert path.stat().st_size == certificate["bytes"]
assert hashlib.sha256(path.read_bytes()).hexdigest() == certificate["sha256"]
digest = hashlib.sha256()
length = 0
with gzip.open(path, "rb") as stream:
    while chunk := stream.read(1024*1024):
        digest.update(chunk)
        length += len(chunk)
assert length == certificate["uncompressed_bytes"]
assert digest.hexdigest() == certificate["uncompressed_sha256"]
print(json.dumps({"artifact_hashes": len(manifest["artifacts"]),
                  "compressed_and_uncompressed_certificate": True}))
