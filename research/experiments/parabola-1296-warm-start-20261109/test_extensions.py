#!/usr/bin/env python3
"""Check that altered or incomplete single-point blocker certificates are rejected."""
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
EXAMPLE=HERE/'output/target1303-seed1302-budget300000'
source=(EXAMPLE/'extensions.txt').read_text().splitlines()
with tempfile.TemporaryDirectory() as tmp:
    bad=Path(tmp)/'bad.txt'
    for name,lines in [('missing',source[:-1]),('changed',source[:1]+['2 2 2 2']+source[2:])]:
        bad.write_text('\n'.join(lines)+'\n')
        proc=subprocess.run([sys.executable,str(HERE/'verify_extensions.py'),
                             str(EXAMPLE/'candidate.txt'),str(bad)],
                            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if proc.returncode==0:
            raise AssertionError(f'{name} certificate was accepted')
        print(f'PASS: {name} blocker certificate rejected')
