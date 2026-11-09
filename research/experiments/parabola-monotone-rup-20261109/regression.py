"""Compare addition-only checker with fresh Python UP and exhaustive SAT."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def rup(database, clause):
    values = {}
    for lit in clause:
        v, truth = abs(lit), lit < 0
        if v in values and values[v] != truth:
            return True
        values[v] = truth
    changed = True
    while changed:
        changed = False
        for c in database:
            if any(abs(l) in values and values[abs(l)] == (l > 0) for l in c):
                continue
            free = set(l for l in c if abs(l) not in values)
            if not free:
                return True
            if len(free) == 1:
                lit = next(iter(free))
                values[abs(lit)] = lit > 0
                changed = True
    return False


def reference(clauses, steps):
    db = list(clauses)
    for deletion, c in steps:
        if deletion:
            continue
        if not rup(db, c):
            return False
        if not c:
            return True
        db.append(c)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    cases = []
    # All four K0707 false-UNSAT deletion controls must be rejected.
    for sign, chain in itertools.product((1, -1), (False, True)):
        unit, implied = sign, 2*sign if chain else sign
        cs = [[unit]] + ([[-unit, implied]] if chain else [])
        steps = [(False, [3]), (True, [unit]), (False, [-unit]), (False, [])]
        cases.append((f'K0707-{sign}-{chain}', 3, cs, steps))
    # Contradictory full cubes; binary resolution tree is a RUP proof.
    for n in range(1, 6):
        cs = [list(c) for c in itertools.product(*[(i, -i) for i in range(1, n+1)])]
        steps = []
        for k in range(n-1, -1, -1):
            for c in itertools.product(*[(i, -i) for i in range(1, k+1)]):
                steps.extend([(True, cs[0]), (False, list(c))])
        cases.append((f'cube-{n}', n, cs, steps))
    # Random streams include non-RUP/RAT-only additions, duplicate literals,
    # tautologies, empty clauses and arbitrary deletion lines.
    rng = random.Random(20261109)
    for i in range(500):
        n = 4
        def draw():
            return [rng.choice((-1, 1))*rng.randint(1, n) for _ in range(rng.randrange(5))]
        cs = [draw() for _ in range(rng.randrange(1, 16))]
        steps = [(rng.random() < .3, draw()) for _ in range(20)] + [(False, [])]
        cases.append((f'random-{i}', n, cs, steps))
    records = []
    with tempfile.TemporaryDirectory(prefix='monotone-rup-regression-') as td:
        td = Path(td)
        exe = td/'checker.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(HERE/'rup_check.cpp'), '-o', str(exe)], check=True)
        def run(cnf, proof):
            (td/'input.cnf').write_text(cnf, encoding='ascii', newline='\n')
            (td/'proof.drat').write_text(proof, encoding='ascii', newline='\n')
            return subprocess.run([str(exe), str(td/'input.cnf'), str(td/'proof.drat')], capture_output=True, text=True, timeout=15)
        def line(c):
            return ' '.join(map(str, c)) + (' ' if c else '') + '0\n'
        for name, n, cs, steps in cases:
            expected = reference(cs, steps)
            satisfiable = any(all(any(vals[abs(l)-1] == (l > 0) for l in c) for c in cs)
                              for vals in itertools.product((False, True), repeat=n))
            assert not expected or not satisfiable
            cnf = f'p cnf {n} {len(cs)}\n'+''.join(map(line, cs))
            proof = ''.join(('d ' if d else '')+line(c) for d, c in steps)
            result = run(cnf, proof)
            assert (result.returncode == 0) == expected, (name, expected, result.stdout, result.stderr)
            records.append(dict(name=name, expected=expected, satisfiable=satisfiable,
                                cnf_sha256=hashlib.sha256(cnf.encode()).hexdigest(),
                                proof_sha256=hashlib.sha256(proof.encode()).hexdigest(),
                                returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        invalid = [
            ('missing-zero', 'p cnf 1 1\n1\n', '0\n'),
            ('out-of-range-input', 'p cnf 1 1\n2 0\n', '0\n'),
            ('wrong-count', 'p cnf 1 2\n1 0\n', '0\n'),
            ('out-of-range-proof', 'p cnf 1 1\n1 0\n', '2 0\n0\n'),
            ('overflow', 'p cnf 1 1\n1 0\n', '0 999999999999999999999999\n'),
            ('trailing-junk', 'p cnf 1 1\n1 0\n', '0 junk\n'),
            ('missing-empty', 'p cnf 1 2\n1 0\n-1 0\n', '1 0\n'),
        ]
        for name, cnf, proof in invalid:
            result = run(cnf, proof)
            assert result.returncode != 0, name
            records.append(dict(name=name, expected=False, returncode=result.returncode))
    result = dict(source_sha256=hashlib.sha256((HERE/'rup_check.cpp').read_bytes()).hexdigest(),
                  cases=records, passed=len(records), seed=20261109)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(f'PASS {len(records)} cases against fresh UP and exhaustive SAT, including four K0707 forgeries')


if __name__ == '__main__':
    main()
