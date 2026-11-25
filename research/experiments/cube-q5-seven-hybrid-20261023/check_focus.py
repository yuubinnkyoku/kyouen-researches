#!/usr/bin/env python3
"""Check that removing irrelevant unknown work preserves the focused proof."""
from pathlib import Path
import json
import struct
import subprocess
import sys
import tempfile
from focus_checkpoint import focus

engine, verifier = map(Path, sys.argv[1:3])
root = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    base = work/'empty.memo';base.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 3, 0, 0))
    many = work/'many.txt';many.write_text('0 1\n0 4\n')
    one = work/'one.txt';one.write_text('0 1\n')
    original, focused = work/'original.hyb', work/'focused.hyb'
    def run(checkpoint, roots, budget, prefix):
        command = [str(engine), '3', str(base), str(base)+'.idx', str(checkpoint),
                   str(roots), str(budget), '1', '4', '100000', '9', str(prefix), '--validate']
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return [json.loads(line) for line in result.stdout.splitlines()]
    run(original, many, 10, work/'first')
    report = focus(original, focused, one)
    a = run(original, one, 1000000, work/'a')[0]
    b = run(focused, one, 1000000, work/'b')[0]
    assert a['outcome'] == b['outcome'] == 'P' and a['nodes'] == b['nodes']
    assert a['cumulative_nodes'] == b['cumulative_nodes']
    assert (work/'a-0-1.cert').read_bytes() == (work/'b-0-1.cert').read_bytes()
    checked = json.loads(subprocess.run([str(verifier), str(work/'b-0-1.cert')],
                                       text=True, capture_output=True, check=True).stdout)
    assert checked['verified']
    (root/'regression-focus.json').write_text(json.dumps({
        'unknown_before': report['unknown_before'], 'unknown_after': report['unknown_after'],
        'same_new_nodes': a['nodes'], 'same_cumulative_nodes': a['cumulative_nodes'],
        'same_certificate': True, 'independent_certificate_check': checked}, indent=2)+'\n')
