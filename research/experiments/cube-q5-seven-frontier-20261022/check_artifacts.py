#!/usr/bin/env python3
"""Verify committed sources, reports, and gzip proof payloads."""
from pathlib import Path
import gzip
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root/'manifest.json').read_text())
for name, expected in manifest['artifacts'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == expected, name
for name, record in json.loads((root/'proofs.json').read_text()).items():
    data = (root/record['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    raw = gzip.decompress(data)
    assert hashlib.sha256(raw).hexdigest() == record['uncompressed_sha256'], name
    assert len(raw.splitlines())-1 == record['states'], name
print(json.dumps({'artifact_hashes': len(manifest['artifacts']), 'gzip_certificates': 3}))
