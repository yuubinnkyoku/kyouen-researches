#!/usr/bin/env python3
"""The compact in-memory child descriptors still read old explicit-child saves."""
from pathlib import Path
import json
import struct
import subprocess
import sys
import tempfile

old_engine, new_engine, verifier = map(Path, sys.argv[1:4])
root = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    base = work/'empty.memo';base.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 3, 0, 0))
    roots = work/'roots.txt';roots.write_text('0 1\n')
    checkpoint = work/'work.hyb'
    command = [str(old_engine), '3', str(base), str(base)+'.idx', str(checkpoint),
               str(roots), '10', '1', '4', '100000', '9', str(work/'old'), '--validate']
    first = json.loads(subprocess.run(command, text=True, capture_output=True, check=True).stdout)
    assert first['outcome'] == 'UNKNOWN' and checkpoint.read_bytes()[:8] == b'Q5HYB1\n\0'
    command[0] = str(new_engine);command[6] = '1000000';command[11] = str(work/'new')
    final = json.loads(subprocess.run(command, text=True, capture_output=True, check=True).stdout)
    assert final['outcome'] == 'P' and checkpoint.read_bytes()[:8] == b'Q5HYB2\n\0'
    checked = json.loads(subprocess.run([str(verifier), str(work/'new-0-1.cert')], text=True,
                                       capture_output=True, check=True).stdout)
    assert checked['verified']
    (root/'legacy-format-local-verified.json').write_text(json.dumps({
        'old_explicit_child_checkpoint_loaded': True,
        'new_compact_checkpoint_written': True,
        'independent_verification': checked}, indent=2)+'\n')
