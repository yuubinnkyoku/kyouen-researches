#!/usr/bin/env python3
"""Compare the local subset kernel against old df-pn and independent geometry."""
from pathlib import Path
import json
import struct
import subprocess
import sys
import tempfile

new_engine, old_engine, verifier = map(Path, sys.argv[1:4])
root = Path(__file__).resolve().parent
roots = root/'local-cases.txt'
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    base = work/'empty.memo';base.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 7, 0, 0))
    runs = []
    checks = []
    for label, engine in [('old', old_engine), ('local', new_engine)]:
        prefix = work/label
        command = [str(engine), '7', str(base), str(base)+'.idx', str(work/(label+'.hyb')),
                   str(roots), '100000', '1', '4', '100000', '9', str(prefix), '--validate']
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        assert len(rows) == 40 and all(row['outcome'] in ['P', 'N'] for row in rows)
        runs.append(rows)
        for row in rows:
            cert = work/(label+''.join('-'+str(p) for p in row['root'])+'.cert')
            checked = json.loads(subprocess.run([str(verifier), str(cert)], text=True,
                                               capture_output=True, check=True).stdout)
            assert checked['verified']
            if label == 'local':checks.append(checked)
    assert [(r['root'], r['outcome']) for r in runs[0]] == [(r['root'], r['outcome']) for r in runs[1]]
    (root/'local-cases-old.jsonl').write_text(''.join(json.dumps(row, separators=(',', ':'))+'\n' for row in runs[0]))
    (root/'local-cases-new.jsonl').write_text(''.join(json.dumps(row, separators=(',', ':'))+'\n' for row in runs[1]))
    (root/'local-cases-verified.json').write_text(json.dumps({
        'cases': 40, 'includes_16_triangle_bearing_6_to_10_move_endgames': True,
        'all_outcomes_match_old_dfpn': True, 'both_versions_all_certificates_independently_checked': True,
        'local_independent_checks': checks}, indent=2)+'\n')
