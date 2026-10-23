#!/usr/bin/env python3
"""Lossless history splitting leaves ongoing searches and proofs identical."""
from pathlib import Path
import gzip
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from split_history import compact

engines = list(map(Path, sys.argv[1:3]))
verifier = Path(sys.argv[3])
root = Path(__file__).resolve().parent
reports = []
for engine in engines:
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        empty = work/'empty.memo';empty.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 3, 0, 0))
        many = work/'many.txt';many.write_text('0 1 3 4\n0 1\n')
        one = work/'one.txt';one.write_text('0 1\n')
        layer, active = work/'layer-1.hyb', work/'active-3.hyb'
        def run(bases, indices, checkpoint, roots, nodes, prefix, promote=False):
            command = list(map(str, [engine, 3, ','.join(map(str, bases)), ','.join(map(str, indices)),
                                    checkpoint, roots, nodes, 1, 4, 100000, 9, prefix, '--validate']))
            if promote:command.append('--promote')
            return subprocess.run(command, text=True, capture_output=True, check=True).stdout
        run([empty], [str(empty)+'.idx'], layer, many, 1, work/'seed')
        bases = [empty, layer];indices = [str(empty)+'.idx', str(layer)+'.idx']
        second = work/'layer-2.hyb'
        run(bases, indices, second, one, 0, work/'paused-first', True)
        bases.append(second);indices.append(str(second)+'.idx')
        run(bases, indices, active, one, 0, work/'paused', True)
        reference = work/'reference.hyb';reference.write_bytes(active.read_bytes())
        before = json.loads(run(bases, indices, reference, one, 1000000, work/'before'))
        expected = (work/'before-0-1.cert').read_bytes()
        state = {'status': 'paused', 'stage': 3, 'bases': list(map(str, bases)),
                 'indices': indices, 'checkpoint': str(active), 'pid': -1}
        (work/'run-state.json').write_text(json.dumps(state))
        records = compact(work, work/'history.json')
        assert len(records) == 1
        record = next(iter(records.values()))
        assert record['exact_rows_unchanged'] and record['unknown_rows_preserved']
        digest = hashlib.sha256(bytes.fromhex(record['original_header_hex']))
        with Path(record['table']).open('rb') as inp:
            inp.seek(80);left = 104*record['exact_rows_unchanged']
            while left:
                chunk = inp.read(min(left, 1024*1024));digest.update(chunk);left -= len(chunk)
        with gzip.open(record['tail'], 'rb') as inp:
            while chunk := inp.read(1024*1024):digest.update(chunk)
        assert digest.hexdigest() == record['original_sha256']
        state = json.loads((work/'run-state.json').read_text())
        after = json.loads(run(state['bases'], state['indices'], active, one, 1000000, work/'after'))
        assert after['outcome'] == before['outcome'] == 'P'
        assert after['cumulative_nodes'] == before['cumulative_nodes']
        assert expected == (work/'after-0-1.cert').read_bytes()
        checked = json.loads(subprocess.run([str(verifier), str(work/'after-0-1.cert')],
                                           text=True, capture_output=True, check=True).stdout)
        assert checked['verified']
        reports.append({'engine': engine.name, 'nonempty_exact_payload_preserved': True,
                        'all_unknown_history_reconstructs_original_hash': True,
                        'active_work_and_counter_preserved': True, 'same_full_proof': True,
                        'independent_verification': checked})
(root/'regression-history.json').write_text(json.dumps(reports, indent=2)+'\n')
