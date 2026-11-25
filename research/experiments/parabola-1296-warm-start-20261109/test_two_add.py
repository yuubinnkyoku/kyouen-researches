#!/usr/bin/env python3
"""Ensure incomplete and altered exchange certificates are rejected."""
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
EXAMPLE=HERE/'output/target1303-seed1302-budget300000'
single=(EXAMPLE/'one-deletion-blockers.txt').read_text().splitlines()
pairs=(EXAMPLE/'two-add-blockers.txt').read_text().splitlines()
with tempfile.TemporaryDirectory() as tmp:
    s=Path(tmp)/'single.txt'; q=Path(tmp)/'pairs.txt'
    for name,ss,qq in [
        ('missing pair',single,pairs[:-1]),
        ('altered pair',single,['0 0 0 0 0']+pairs[1:]),
        ('missing point',single[:-1],pairs),
        ('altered point',single[:1]+['2 2 2 2']+single[2:],pairs),
    ]:
        s.write_text('\n'.join(ss)+'\n');q.write_text('\n'.join(qq)+'\n')
        proc=subprocess.run([sys.executable,str(HERE/'verify_two_add.py'),
                             str(EXAMPLE/'candidate.txt'),str(s),str(q)],
                            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if proc.returncode==0: raise AssertionError(f'{name} accepted')
        print(f'PASS: {name} rejected')
