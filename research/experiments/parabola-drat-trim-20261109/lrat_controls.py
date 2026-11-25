"""Positive LRAT and missing/wrong-hint/false-empty controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    cnf = 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n'
    valid = '5 1 0 1 2 0\n6 0 5 3 4 0\n'
    cases = [('valid-resolution', cnf, valid, True),
             ('missing-needed-hint', cnf, valid.replace('1 2 0', '1 0', 1), False),
             ('wrong-clause', cnf, valid.replace('5 1 0', '5 2 0'), False),
             ('sat-forged-empty', 'p cnf 1 1\n1 0\n', '2 0 1 0\n', False),
             ('no-empty-clause', cnf, '5 1 0 1 2 0\n', False)]
    records = []
    with tempfile.TemporaryDirectory(prefix='lrat-controls-') as td:
        td = Path(td)
        bins = {}
        for kind, source in [('upstream', HERE/'vendor/lrat-check.c'), ('empty-fixed', HERE/'lrat-check-empty-fixed.c')]:
            exe = td/(kind+'.exe')
            subprocess.run(['gcc', str(source), '-std=c99', '-O2', '-DLONGTYPE', '-Dgetc_unlocked=getc', '-o', str(exe)], check=True)
            bins[kind] = exe
        for name, formula, proof, expected in cases:
            (td/'input.cnf').write_bytes(formula.encode())
            (td/'proof.lrat').write_bytes(proof.encode())
            results = {}
            for kind, exe in bins.items():
                run = subprocess.run([str(exe), str(td/'input.cnf'), str(td/'proof.lrat')], capture_output=True, text=True, timeout=15)
                accepted = run.returncode == 0 and 'c VERIFIED' in run.stdout.splitlines()
                results[kind] = dict(accepted=accepted, returncode=run.returncode, stdout=run.stdout, stderr=run.stderr)
            assert results['empty-fixed']['accepted'] == expected, name
            assert results['upstream']['accepted'] == (expected or name == 'sat-forged-empty'), name
            records.append(dict(name=name, expected=expected, formula=formula, proof=proof, results=results))
        result = dict(source_sha256={name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in
                          [('upstream', HERE/'vendor/lrat-check.c'), ('empty-fixed', HERE/'lrat-check-empty-fixed.c')]},
                      binary_sha256={name:hashlib.sha256(exe.read_bytes()).hexdigest() for name, exe in bins.items()}, cases=records)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('PASS five fixed LRAT controls; upstream falsely accepts SAT false empty')


if __name__ == '__main__':
    main()
