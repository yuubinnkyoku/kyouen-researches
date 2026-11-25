"""Audit the saved p2207 witness using generic integer geometry, without SAT."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE.parent / 'parabola-p2207-no-equality-witness-20261107/output/shape_c_2207.json'
VERIFIER = HERE.parent / 'parabola-local-repair-20261109/verify_subset.cpp'
VERIFIER_SHA = 'c817e7808e5d853a6ca0b897e5a0f454944f38069c8c32b5a10ef7f97b32261c'
CANDIDATE_SHA = 'ce97d4a9447fd32cd67e3cfad59151774fa45cf90c8985287abb1a45480e2347'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def run(binary, raw, timeout):
    started = time.monotonic()
    try:
        result = subprocess.run([str(binary), '--modular-filter'], input=raw,
                                capture_output=True, timeout=timeout)
        return dict(returncode=result.returncode, stdout=result.stdout.decode(),
                    stderr=result.stderr.decode(), elapsed_seconds=time.monotonic()-started,
                    timed_out=False)
    except subprocess.TimeoutExpired as exc:
        return dict(returncode=None, stdout=(exc.stdout or b'').decode(errors='replace'),
                    stderr=(exc.stderr or b'').decode(errors='replace'),
                    elapsed_seconds=time.monotonic()-started, timed_out=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    original = SOURCE.read_bytes()
    data = json.loads(original)
    assert data['p'] == 2207 and data['h'] == 1103 and data['shape'] == 'c'
    assert data['sat'] is True and data['unknown'] is False
    assert data['target_size'] == data['size'] == 1104
    points = data['points']
    assert len(points) == 1104 and all(type(t) is int and 0 <= t < 2207 for t in points)
    assert points == sorted(set(points)) and 0 in points
    chosen = set(points)
    complete = [d for d in range(1, 1104) if d in chosen and 2207-d in chosen]
    empty = [d for d in range(1, 1104) if d not in chosen and 2207-d not in chosen]
    assert complete == data['complete'] == [307] and empty == data['empty'] == [1078]
    candidate = ('2207 1104\n' + ' '.join(map(str, points)) + '\n').encode('ascii')
    assert sha(candidate) == CANDIDATE_SHA
    assert sha(VERIFIER.read_bytes()) == VERIFIER_SHA
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'candidate.txt').write_bytes(candidate)
    binding = dict(source_path=SOURCE.relative_to(ROOT).as_posix(),
                   source_commit='eece6d3cf909f97cc2edfaa5cd85fd0701b50bc1',
                   source_receipt_sha256=sha(original), candidate_input_sha256=sha(candidate),
                   driver_source_sha256=sha(Path(__file__).read_bytes()),
                   verifier_source_sha256=VERIFIER_SHA, p=2207, size=1104,
                   complete=complete, empty=empty, contains_origin=True,
                   scope='The supplied point list only; no trust in safe_against_edges or solver claims.')
    save(args.output / 'extraction.json', binding)
    with tempfile.TemporaryDirectory(prefix='p2207-1104-geometry-') as temporary:
        binary = Path(temporary) / 'geometry.exe'
        command = ['g++', '-O2', '-std=c++17', str(VERIFIER), '-o', str(binary)]
        subprocess.run(command, check=True, timeout=60)
        controls = [('safe-three', b'5 3\n0 1 2\n', 0),
                    ('unsafe-two-pairs', b'5 4\n1 2 3 4\n', 4),
                    ('duplicate', b'5 3\n0 1 1\n', 3),
                    ('truncated', b'5 3\n0 1\n', 2),
                    ('composite', b'9 2\n0 1\n', 2)]
        rows = []
        for name, raw, expected in controls:
            result = run(binary, raw, 10)
            assert result['returncode'] == expected, (name, result)
            rows.append(dict(name=name, input=raw.decode(), expected_returncode=expected, **result))
        save(args.output / 'controls.json', dict(verifier_source_sha256=VERIFIER_SHA,
             binary_sha256=sha(binary.read_bytes()), cases=rows,
             scope='Finite parser and geometry controls, not general verifier soundness.'))
        result = run(binary, candidate, 120)
        passed = result['returncode'] == 0
        if passed:
            values = list(map(int, result['stdout'].split()))
            assert len(values) == 4 and values[:3] == [2207, 1104, math.comb(1104, 4)]
            assert 0 < values[3] <= values[2]
            result.update(covered_quadruples=values[2], exact_determinants=values[3])
        result.update(binding, verified=passed, binary_sha256=sha(binary.read_bytes()),
                      build_flags=['-O2', '-std=c++17'],
                      scope='Generic integer 4x4 geometry with complete modular filter (K0334); no CNF or cached edge list. Proves the finite witness safety, not A(2207)=1104.')
        save(args.output / 'geometry.json', result)
        print(json.dumps(result, indent=2))
        if not passed:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
