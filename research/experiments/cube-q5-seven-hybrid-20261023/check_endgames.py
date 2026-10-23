#!/usr/bin/env python3
"""Recheck the fixed seven-cube endgames and independently check all proofs."""
from pathlib import Path
import json
import struct
import subprocess
import sys
import tempfile

engine, verifier = map(Path, sys.argv[1:3])
root = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    base = work/'empty.memo'
    base.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 7, 0, 0))
    command = [str(engine), '7', str(base), str(base)+'.idx', str(work/'work.hyb'),
               str(root/'endgames.txt'), '100000', '1', '4', '100000', '9',
               str(work/'proof'), '--validate']
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    legacy = [json.loads(line) for line in (root/'endgames-legacy.jsonl').read_text().splitlines()]
    assert len(rows) == len(legacy) == 24
    assert [(r['root'], r['outcome']) for r in rows] == [(r['root'], r['outcome']) for r in legacy]
    verified = []
    for row in rows:
        cert = work/('proof'+''.join('-'+str(p) for p in row['root'])+'.cert')
        checked = json.loads(subprocess.run([str(verifier), str(cert)], text=True,
                                           capture_output=True, check=True).stdout)
        assert checked['verified']
        verified.append(checked)
    (root/'endgames-current.jsonl').write_text(result.stdout)
    (root/'endgames-current-verified.json').write_text(json.dumps({
        'samples': 24, 'all_outcomes_match_legacy': True,
        'independently_verified': verified}, indent=2)+'\n')
