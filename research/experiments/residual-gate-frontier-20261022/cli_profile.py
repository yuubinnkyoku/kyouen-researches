#!/usr/bin/env python3
"""Tiny CLI check that frame profiles do not leak across root boundaries."""
import argparse
import pathlib
import subprocess
import tempfile
from study import roots_csv, parse

p = argparse.ArgumentParser()
p.add_argument('--solver', required=True)
args = p.parse_args()
with tempfile.TemporaryDirectory() as directory:
    directory = pathlib.Path(directory)
    source, output = directory / 'roots.csv', directory / 'output.csv'
    roots_csv(source, [[0, 1, 2, 4, 9]] * 2)
    subprocess.run([args.solver, '--n=4', '--memo=16', '--node-budget=1', '--budget=5',
        f'--roots-csv={source}', f'--csv={output}', f'--log={directory / "solver.log"}',
        '--residual-exact-legal=6', '--residual-evaluator=outcome', '--residual-outcome-budget=128',
        '--residual-profile'], check=True, timeout=15)
    raw = output.read_text()
    rows = parse(raw)
    assert len(rows) == 2 and rows[0]['result'] == rows[1]['result'] != 0
    assert rows[0]['pn_nodes'] == 1 and rows[1]['pn_nodes'] == 0
    profiles = [line for line in raw.splitlines() if line.startswith('# residual_gate_profile ')]
    assert profiles == ['# residual_gate_profile seq=1 legal=2 frames=1']
print('VERIFIED CLI frame histogram excludes solved TT reuse and reports per-root differences')
