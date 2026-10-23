#!/usr/bin/env python3
"""Every known 3-cube root keeps its full proof after raw/gzip restriction."""
from pathlib import Path
import gzip
import json
import struct
import subprocess
import sys
import tempfile

filter_bin, engine, legacy, verifier = map(Path, sys.argv[1:5])
root = Path(__file__).resolve().parent
known = root.parent/'cube-q5-seven-frontier-20261022/known-roots3.txt'


def run(command):
    return subprocess.run(list(map(str, command)), text=True, capture_output=True, check=True).stdout


with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    old = work/'old.memo'
    run([legacy, '--batch', 3, 1000000, 10000, work/'legacy', known, old])
    reports = [json.loads(line) for line in run([filter_bin, 3, known, work/'focused', old, old]).splitlines()]
    assert len(reports) == 20
    zipped = work/'old.memo.gz';zipped.write_bytes(gzip.compress(old.read_bytes(), mtime=0))
    run([sys.executable, root/'filter_archives.py', 3, known, work/'archived', old, zipped,
         '--filter', filter_bin])
    bad = bytearray(old.read_bytes());bad[32+48] ^= 1;bad[32+56:32+104] = bytes(48)
    conflict = work/'conflict.memo';conflict.write_bytes(bad)
    rejected = subprocess.run(list(map(str, [filter_bin, 3, known, work/'bad', old, conflict])),
                              text=True, capture_output=True)
    assert rejected.returncode and 'conflicting exact labels' in rejected.stderr
    for i, line in enumerate(known.read_text().splitlines()):
        one = work/'one.txt';one.write_text(line+'\n');certificates = []
        for label, base in [('all', old), ('focused', work/f'focused-{i}.memo'),
                            ('archived', work/f'archived-{i}.memo')]:
            prefix = work/label
            result = json.loads(run([engine, 3, base, str(base)+'.idx', work/f'{label}-{i}.hyb',
                                     one, 0, 1, 4, 100000, 0, prefix]))
            assert result['outcome'] == 'P' and result['nodes'] == 0
            cert = work/(label+''.join('-'+p for p in line.split())+'.cert')
            certificates.append(cert.read_bytes())
            if label == 'focused':
                assert json.loads(run([verifier, cert]))['verified']
        assert certificates[0] == certificates[1] == certificates[2]
    (root/'regression.json').write_text(json.dumps({
        'roots': 20, 'all_filtered_root_proofs_identical': True,
        'all_filtered_proofs_independently_verified': True,
        'duplicate_sources_checked': True, 'conflicting_labels_rejected': True,
        'raw_and_archive_results_same_certificate': True,
        'unfiltered_rows': struct.unpack_from('<Q', old.read_bytes(), 24)[0],
        'filtered_rows': [row['rows'] for row in reports]}, indent=2)+'\n')
