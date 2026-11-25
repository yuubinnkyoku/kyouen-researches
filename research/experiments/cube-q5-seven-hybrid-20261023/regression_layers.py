#!/usr/bin/env python3
"""Disk base, exact delta and resumable unknown tree regression."""
from pathlib import Path
import json
import shutil
import struct
import subprocess
import sys
import tempfile

engine, legacy, verifier = map(Path, sys.argv[1:4])
known = Path(__file__).resolve().parent.parent/'cube-q5-seven-frontier-20261022/known-roots3.txt'


def run(*args, ok=True):
    result = subprocess.run(list(map(str, args)), text=True, capture_output=True)
    assert (result.returncode == 0) == ok, (args, result.stdout, result.stderr)
    return result.stdout


with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    empty = root/'empty.memo'; empty.write_bytes(b'Q5MEMO2\n'+struct.pack('<3Q', 3, 0, 0))
    one = root/'one.txt'; one.write_text('0 1\n')
    def command(base, checkpoint, roots, budget, epochs=1, prior=4, tree=100000):
        return [engine, 3, base, str(base)+'.idx', checkpoint, roots, budget,
                epochs, prior, tree, 9, root/'cert', '--validate']
    checkpoint = root/'resumed.hyb'
    first = json.loads(run(*command(empty, checkpoint, one, 10)))
    assert first['outcome'] == 'UNKNOWN' and first['unknown_rows'] == 10
    untouched = checkpoint.read_bytes()
    resumed = json.loads(run(*command(empty, checkpoint, one, 1000000)))
    resumed_cert = (root/'cert-0-1.cert').read_bytes()
    fresh = json.loads(run(*command(empty, root/'fresh.hyb', one, 1000000)))
    assert resumed['outcome'] == fresh['outcome'] == 'P'
    assert resumed['cumulative_nodes'] == fresh['cumulative_nodes']
    assert (root/'cert-0-1.cert').read_bytes() == resumed_cert
    assert json.loads(run(verifier, root/'cert-0-1.cert'))['verified']
    trimmed = [json.loads(line) for line in run(*command(
        empty, root/'trim.hyb', one, 10000, epochs=200, tree=40)).splitlines()]
    assert trimmed[-1]['outcome'] == 'P'
    assert any(r['reason'] == 'tree-limit' for r in trimmed)
    assert json.loads(run(verifier, root/'cert-0-1.cert'))['verified']
    full = root/'old.memo'
    run(legacy, '--batch', 3, 1000000, 10000, root/'old', known, full)
    records = [json.loads(line) for line in run(*command(full, root/'based.hyb', known, 0)).splitlines()]
    assert len(records) == 20 and all(r['outcome'] == 'P' and r['nodes'] == 0 for r in records)
    for record in records:
        suffix = ''.join('-'+str(p) for p in record['root'])
        assert json.loads(run(verifier, root/('cert'+suffix+'.cert')))['verified']
    # The entire file includes both exact delta and nonverdict work estimates.
    bad = root/'bad.hyb'; bad.write_bytes(untouched[:-1])
    run(*command(empty, bad, one, 1), ok=False)
    bad.write_bytes(untouched)
    run(*command(empty, bad, one, 1, prior=2), ok=False)
    run(*command(full, bad, one, 1), ok=False)
    # Wrong legal sets in a restored unknown node must fail validation.
    data = bytearray(untouched)
    assert struct.unpack_from('<Q', data, 8+7*8)[0] == 0  # delta rows
    key = struct.unpack_from('<6Q', data, 80)
    point = next(i for i in range(27) if key[i//64] >> (i%64) & 1)
    offset = 80+48+8*(point//64)
    struct.pack_into('<Q', data, offset, struct.unpack_from('<Q', data, offset)[0] | (1 << (point%64)))
    bad.write_bytes(data)
    run(*command(empty, bad, one, 1), ok=False)
    # Seal an exact delta as a second immutable layer and retain its unknown work.
    sealed = root/'fresh.hyb'
    promoted = root/'promoted.hyb'
    args = command(empty, promoted, one, 0)
    args[2] = str(empty)+','+str(sealed)
    args[3] = str(empty)+'.idx,'+str(root/'sealed.idx')
    args.append('--promote')
    lifted = json.loads(run(*args))
    assert lifted['outcome'] == 'P' and lifted['nodes'] == 0 and lifted['delta_rows'] == 0
    assert json.loads(run(verifier, root/'cert-0-1.cert'))['verified']
    run(*command(empty, promoted, one, 0), ok=False)
    unfinished = root/'unfinished.hyb'; unfinished.write_bytes(untouched)
    args = command(empty, root/'promoted-work.hyb', one, 1000000)
    args[2] = str(empty)+','+str(unfinished)
    args[3] = str(empty)+'.idx,'+str(root/'unfinished.idx')
    args.append('--promote')
    completed = json.loads(run(*args))
    assert completed['cumulative_nodes'] == fresh['cumulative_nodes']
    assert completed['outcome'] == 'P'
    assert json.loads(run(verifier, root/'cert-0-1.cert'))['verified']
print(json.dumps({'known_three_cube_roots_independently_verified': 20,
                  'layer_promotion_preserves_exact_and_unknown_work': True,
                  'base_reuse_zero_expansions': True,
                  'unknown_tree_resume_same_nodes_and_certificate': True,
                  'bounded_tree_replacement_independently_verified': True,
                  'negative_checkpoint_cases': 4}, indent=2))
