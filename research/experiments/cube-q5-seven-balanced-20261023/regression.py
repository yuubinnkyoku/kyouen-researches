#!/usr/bin/env python3
"""Independently verify small roots and new N parents from P children."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

engine, verifier = map(Path, sys.argv[1:3])
here = Path(__file__).resolve().parent
known = here.parent/'cube-q5-seven-frontier-20261022/known-roots3.txt'


def run(*args):
    return subprocess.run(list(map(str, args)), capture_output=True, text=True, check=True).stdout


with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    checkpoint = root/'small.memo'
    records = [json.loads(line) for line in run(engine, '--batch', 3, 1000000,
               10000, root/'small', known, checkpoint, '--direct', '--reverse', 9,
               '--base', 4, '--validate').splitlines()]
    assert len(records) == 20 and all(r['outcome'] == 'P' for r in records)
    for record in records:
        path = root/('small'+''.join('-'+str(i) for i in record['root'])+'.cert')
        assert json.loads(run(verifier, path))['verified']
    parents = root/'parents.txt'; parents.write_text('0\n1\n4\n13\n')
    lifted = [json.loads(line) for line in run(engine, '--batch', 3, 0, 10000,
              root/'lifted', parents, checkpoint, '--direct', '--reverse', 9,
              '--validate').splitlines()]
    assert all(r['outcome'] == 'N' and r['nodes'] == 0 for r in lifted)
    for record in lifted:
        assert json.loads(run(verifier, root/('lifted-'+str(record['root'][0])+'.cert')))['verified']
print(json.dumps({'three_cube_known_roots': 20, 'all_independently_verified': True,
                  'one_stone_parents_reused_without_expansions': 4,
                  'every_incremental_move_compared_to_full_legal': True}, indent=2))
