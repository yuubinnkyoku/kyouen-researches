#!/usr/bin/env python3
"""Retune interrupted P and N searches and independently check final proofs."""
from pathlib import Path
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from retune import retune

engine, verifier = map(Path, sys.argv[1:3])
root = Path(__file__).resolve().parent
records = []
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    base = work/'empty.memo';base.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 3, 0, 0))
    for i, (points, expected) in enumerate([([0, 1], 'P'), ([0], 'N')]):
        roots = work/'roots.txt';roots.write_text(' '.join(map(str, points))+'\n')
        before, after = work/f'before-{i}.hyb', work/f'after-{i}.hyb'
        prefix = work/f'proof-{i}'
        def command(checkpoint, budget, prior):
            return list(map(str, [engine, 3, base, str(base)+'.idx', checkpoint,
                                  roots, budget, 1, prior, 100000, 9, prefix, '--validate']))
        first = subprocess.run(command(before, 1, 4), text=True, capture_output=True, check=True)
        assert json.loads(first.stdout)['outcome'] == 'UNKNOWN'
        original = hashlib.sha256(before.read_bytes()).hexdigest()
        change = retune(before, after, 2)
        assert original == hashlib.sha256(before.read_bytes()).hexdigest()
        wrong = subprocess.run(command(after, 1, 4), text=True, capture_output=True)
        assert wrong.returncode
        final = json.loads(subprocess.run(command(after, 1000000, 2), text=True,
                                         capture_output=True, check=True).stdout)
        assert final['outcome'] == expected
        cert = work/(prefix.name+''.join('-'+str(p) for p in points)+'.cert')
        checked = json.loads(subprocess.run([str(verifier), str(cert)], text=True,
                                           capture_output=True, check=True).stdout)
        assert checked['verified']
        records.append({'root': points, 'outcome': expected,
                        'exact_rows_unchanged': change['exact_rows_unchanged'],
                        'unknown_rows_reseeded': change['unknown_rows_reseeded'],
                        'source_snapshot_unchanged': True, 'wrong_prior_rejected': True,
                        'independent_verification': checked})
(root/'regression-retune.json').write_text(json.dumps(records, indent=2)+'\n')
