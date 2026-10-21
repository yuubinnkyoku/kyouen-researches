#!/usr/bin/env python3
"""Bounded n4 CLI regression for sliced P/N attempts; no unknown n11 search."""
import argparse, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'residual-dfpn-integration-20261021'))
from integration import parse, roots_csv

def main():
    p = argparse.ArgumentParser(); p.add_argument('--solver', required=True); args = p.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        tmp = pathlib.Path(directory)
        options = ['--residual-evaluator=outcome', '--residual-exact-legal=16', '--residual-outcome-budget=128']
        def run(name, extra):
            output = tmp / f'{name}.csv'
            subprocess.run([args.solver, '--n=4', '--memo=16', '--budget=5', f'--csv={output}',
                f'--log={tmp / (name + ".log")}', *extra], check=True, timeout=15)
            return parse(output.read_text())
        for cap in (1, 8, 32, 1000):
            r = run(f'empty-{cap}', ['--empty', '--node-budget=20000', *options, f'--residual-attempt-budget={cap}'])[0]
            assert r['result'] == 2 and r['pn_attempt_budget'] == cap
            assert r['pn_nodes'] <= r['pn_attempted'] * cap and r['pn_attempted'] == r['residual_calls']
            assert r['pn_aborts'] <= r['pn_attempted'] <= r['pn_nodes'] <= 128
        source = tmp / 'roots.csv'; roots_csv(source, [[0, 1, 2, 4, 9]] * 2)
        rows = run('repeat', [f'--roots-csv={source}', '--node-budget=1', *options, '--residual-attempt-budget=1'])
        assert len(rows) == 2 and rows[0]['result'] == rows[1]['result'] != 0
        assert rows[0]['pn_attempted'] == rows[0]['pn_nodes'] == 1
        assert rows[1]['pn_attempted'] == rows[1]['pn_nodes'] == rows[1]['pn_attempt_skips'] == 0
        zero = run('zero', ['--empty', '--node-budget=1', *options, '--residual-attempt-budget=8', '--residual-outcome-budget=0'])[0]
        assert zero['pn_nodes'] == zero['pn_attempted'] == zero['residual_calls'] == 0
        baseline = run('whole', ['--empty', '--node-budget=20000', *options])[0]
        assert baseline['result'] == 2 and baseline['pn_attempt_budget'] == baseline['pn_attempted'] == baseline['pn_attempt_skips'] == 0
        for extra in (['--residual-attempt-budget=0'], ['--residual-attempt-budget=-1'],
            ['--residual-attempt-budget=1'], [*options, '--exact-replay=unused', '--residual-attempt-budget=1'],
            ['--residual-evaluator=grundy', '--residual-exact-legal=16', '--residual-attempt-budget=1'],
            ['--residual-evaluator=outcome', '--residual-attempt-budget=1']):
            r = subprocess.run([args.solver, '--empty', *extra], capture_output=True, text=True, timeout=5)
            assert r.returncode != 0 and 'error:' in r.stderr
    print('VERIFIED capped CLI, budgets 1/8/32/1000, quota zero, root reset, default whole-quota mode and invalid modes')

if __name__ == '__main__': main()
