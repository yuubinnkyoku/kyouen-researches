"""Replay the fixed witness without reading SAT, local models, or search edges."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def determinant(q, p):
    # Fraction-free Bareiss elimination, independent of the C++ Leibniz sum.
    a = [[1, t, t*t % p, t*t + (t*t % p)**2] for t in q]
    sign, previous = 1, 1
    for k in range(3):
        if not a[k][k]:
            r = next((r for r in range(k+1, 4) if a[r][k]), None)
            if r is None:
                return 0
            a[k], a[r] = a[r], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign*a[3][3]


def parse(candidate, blockers):
    values = list(map(int, candidate.split()))
    p, n = values[:2]
    points = values[2:]
    assert p == 2539 and len(points) == n
    assert points == sorted(set(points)) and 0 <= points[0] < points[-1] < p
    lines = blockers.decode('ascii').splitlines()
    assert list(map(int, lines[0].split())) == [p, n, p-n]
    rows = [list(map(int, line.split())) for line in lines[1:]]
    assert all(len(row) == 5 for row in rows)
    assert len(rows) == p-n
    assert sorted(row[0] for row in rows) == sorted(set(range(p))-set(points))
    selected = set(points)
    for t, *q in rows:
        assert q == sorted(set(q)) and 0 <= q[0] < q[-1] < p
        assert t in q and set(q)-{t} <= selected
        assert determinant(q, p) == 0
    return p, n, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    candidate = (args.saved/'candidate.txt').read_bytes()
    blockers = (args.saved/'blockers.txt').read_bytes()
    receipt = json.loads((args.saved/'verification.json').read_text())
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert sha(candidate) == receipt['candidate_sha256']
    assert sha(blockers) == receipt['blockers_sha256']
    assert sha(generic.read_bytes()) == receipt['generic_source_sha256']
    assert sha((HERE/'augment.py').read_bytes()) == receipt['source_sha256']
    p, n, rows = parse(candidate, blockers)
    with tempfile.TemporaryDirectory(prefix='p2539-saved-replay-') as folder:
        exe = Path(folder)/'subset.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(exe)], check=True, timeout=60)
        result = subprocess.run([str(exe), '--modular-filter'], input=candidate, capture_output=True, timeout=120)
        assert result.returncode == 0, result.stdout+result.stderr
        assert list(map(int, result.stdout.split()))[:3] == [p, n, math.comb(n, 4)]
        controls = []
        for name, raw, expected in [
            ('safe-three', b'5 3\n0 1 2\n', 0),
            ('forbidden-two-pairs', b'5 4\n1 2 3 4\n', 4),
            ('duplicate', b'5 3\n0 1 1\n', 3),
            ('truncated', b'5 3\n0 1\n', 2),
            ('composite', b'9 3\n0 1 2\n', 2),
        ]:
            r = subprocess.run([str(exe), '--modular-filter'], input=raw, capture_output=True, timeout=10)
            assert r.returncode == expected, name
            controls.append(dict(name=name, returncode=r.returncode, expected=expected))
    report = dict(p=p, size=n, verified_safe=True, verified_inclusion_maximal=True,
                  stdout=result.stdout.decode(), returncode=result.returncode,
                  blocker_bareiss_zero_count=len(rows), candidate_sha256=sha(candidate),
                  blockers_sha256=sha(blockers), generic_source_sha256=sha(generic.read_bytes()),
                  replay_source_sha256=sha(Path(__file__).read_bytes()), controls=controls,
                  scope='Fixed subset safety and all missing-point blockers; maximal, not maximum. No search edge cache or solver model is read.')
    with args.output.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(report, indent=2)+'\n')
    print(f'PASS saved replay: {n} safe points; {len(rows)} independent Bareiss blockers; five controls')


if __name__ == '__main__':
    main()
