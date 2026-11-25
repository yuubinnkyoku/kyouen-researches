#!/usr/bin/env python3
"""Rebuild and independently compare both exact modular-mask constructions."""
import csv
import hashlib
import subprocess
import tempfile
from pathlib import Path
from check_nonprimitive_rows_2_32 import FAMILIES, main as check_witness

HERE = Path(__file__).resolve().parent
SRC = HERE / 'verify_nonprimitive_rows_2_32.cpp'
OUT = HERE.parent / 'output' / 'nonprimitive_rows_2_32_audit.csv'

def run():
    check_witness()
    cases = sorted((k, width) for _, mapping in FAMILIES for k, width in mapping.items())
    cases += [(9, 40)]  # no 9 nonprimitive rows in 40 lines: F(9) >= 41.
    with tempfile.TemporaryDirectory() as temp:
        binaries = []
        for flags, name in (([], 'transposed'), (['-DDIRECT_RESIDUES'], 'direct')):
            binary = Path(temp) / name
            subprocess.run(['g++', '-O3', '-std=c++20', *flags, str(SRC), '-o', str(binary)], check=True)
            binaries.append(binary)
        records = []
        for k, width in cases:
            # For the exact cases, the upper exclusion concerns F(k)-1.
            W = width if k == 9 else width-1
            outputs = [subprocess.run([str(b), str(W), str(k)], capture_output=True,
                                      text=True, timeout=240, check=True).stdout
                       for b in binaries]
            assert outputs[0] == outputs[1], (k, W)
            assert outputs[0].endswith(f'PASS W={W} K={k} gcd>=2 cases=' +
                                        outputs[0].split('cases=')[-1])
            steps = outputs[0].count('CASE ')
            peak = max([int(line.split()[3]) for line in outputs[0].splitlines()
                        if line.startswith('CASE ')] or [0])
            records.append(dict(k=k, witness_width='' if k == 9 else width,
                                excluded_width=W, modular_steps=steps,
                                max_states=peak,
                                sha256=hashlib.sha256(outputs[0].encode()).hexdigest()))
            print(f'PASS k={k} W={W} steps={steps} peak={peak}')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f'PASS {len(records)} dual-method exclusions; audit: {OUT}')

if __name__ == '__main__':
    run()
