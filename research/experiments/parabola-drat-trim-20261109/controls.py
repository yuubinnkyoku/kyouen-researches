"""Rebuild pinned upstream checker and reject all four K0707 forgeries."""
import argparse
import hashlib
import itertools
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
    provenance = json.loads((HERE/'vendor/provenance.json').read_text())
    records = []
    with tempfile.TemporaryDirectory(prefix='upstream-controls-') as td:
        td = Path(td)
        exe = td/'drat-trim.exe'
        subprocess.run(['gcc', str(HERE/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(exe)], check=True)
        cases = []
        for sign, chain in itertools.product((1, -1), (False, True)):
            unit, implied = sign, 2*sign if chain else sign
            clauses = [[unit]]+([[-unit, implied]] if chain else [])
            cnf = f'p cnf 3 {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
            proof = f'3 0\nd {unit} 0\n{-unit} 0\n0\n'
            cases.append((f'K0707-{sign}-{chain}', cnf, proof, False))
        cases.append(('resolution-unsat', 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n', '1 0\n0\n', True))
        cases.append(('sat-direct-false-empty', 'p cnf 1 1\n1 0\n', '0\n', False))
        for name, cnf, proof, expected in cases:
            (td/'input.cnf').write_bytes(cnf.encode())
            (td/'proof.drat').write_bytes(proof.encode())
            run = subprocess.run([str(exe), str(td/'input.cnf'), str(td/'proof.drat'), '-U'], capture_output=True, text=True, timeout=15)
            accepted = run.returncode == 0 and 's VERIFIED' in run.stdout.splitlines()
            assert accepted == expected, name
            records.append(dict(name=name, accepted=accepted, returncode=run.returncode,
                                stdout=run.stdout, stderr=run.stderr,
                                input_sha256=hashlib.sha256(cnf.encode()).hexdigest(),
                                proof_sha256=hashlib.sha256(proof.encode()).hexdigest()))
        result = dict(cases=records, source_sha256=hashlib.sha256((HERE/'vendor/drat-trim.c').read_bytes()).hexdigest(),
                      binary_sha256=hashlib.sha256(exe.read_bytes()).hexdigest())
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('PASS upstream -U checker: four K0707 rejections, resolution control, and SAT false empty rejection')


if __name__ == '__main__':
    main()
