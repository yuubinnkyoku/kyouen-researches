#!/usr/bin/env bash
# End-to-end fail-closed S5 cache merge regression using REAL canonical safe keys.
# The former test used invalid 5-stone masks and a machine-specific /mnt/d path:
# its "clean" merge could fail while the script still printed MERGE_GUARD_OK.
set -euo pipefail
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dfpn_s5_merge.sh"
python3 - "$SCRIPT" <<'PY'
import pathlib
import subprocess
import sys
import tempfile

script = pathlib.Path(sys.argv[1])
# Safe, canonical S5 keys from the frozen reply27-hard9 verdict cache.
A = (1152921504742115328, 536870912)
B = (3602879701897445376, 134217728)
C = (10520408729537478660, 67108864)
D = (10520408729538527232, 16384)


def line(key, verdict, nodes=10):
    return f's5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n'


def write(path, data):
    path.write_text(data, encoding='utf-8')
    return path


def run(out, *inputs):
    return subprocess.run(['bash', str(script), str(out),
                           *map(str, inputs)], capture_output=True, text=True)


def exact(path):
    result = {}
    for raw in path.read_text(encoding='utf-8').splitlines():
        if not raw or raw.startswith('#'):
            continue
        f = raw.split(',')
        assert len(f) == 6 and f[0] == 's5verdict', raw
        key = (int(f[1]), int(f[2]))
        assert key not in result, 'duplicate output key'
        result[key] = (int(f[4]), int(f[5]))
    return result


def success(p):
    assert p.returncode == 0 and 'MERGE_OK' in p.stdout, (
        p.returncode, p.stdout, p.stderr)


def refused(p, why):
    assert p.returncode != 0 and 'MERGE_REFUSED' in p.stderr, (
        p.returncode, p.stdout, p.stderr)
    assert why in p.stderr, p.stderr


with tempfile.TemporaryDirectory(prefix='n11-s5-merge-test-') as td:
    d = pathlib.Path(td)
    base = write(d/'base.csv', line(A, 2, 10))
    agreeing = write(d/'agree.csv', line(A, 2, 7) + line(B, 1, 20))
    conflicting = write(d/'conflict.csv', line(A, 1, 30))
    unknown = write(d/'unknown.csv', line(C, 0) + line(D, 2, 4))

    # 1. Clean overlap must SUCCEED, and duplicate exact verdicts take min(nodes).
    out = d/'clean.csv'
    success(run(out, base, agreeing))
    assert exact(out) == {A: (2, 7), B: (1, 20)}
    print('PASS clean canonical merge')

    # 2. Conflicting WIN/LOSS must fail BEFORE creating any output.
    out = d/'conflict-out.csv'
    refused(run(out, base, conflicting), 'CONFLICT')
    assert not out.exists()
    print('PASS conflict leaves no output')

    # 3. UNKNOWN is not a proof; it must not appear in the merged cache.
    out = d/'unknown-out.csv'
    success(run(out, base, unknown))
    assert exact(out) == {A: (2, 10), D: (2, 4)}
    print('PASS UNKNOWN discarded')

    # 4. An already committed output is an input and must not be clobbered.
    out = d/'existing.csv'
    success(run(out, base))
    before = out.read_bytes()
    refused(run(out, agreeing, conflicting), 'CONFLICT')
    assert out.read_bytes() == before
    print('PASS existing output preserved on conflict')

    # 5. Two cooperating writers must serialize on the stable .lock inode.
    out = d/'parallel.csv'
    wb = write(d/'worker-b.csv', line(B, 1, 21))
    wc = write(d/'worker-c.csv', line(C, 2, 22))
    procs = [subprocess.Popen(['bash', str(script), str(out), str(base),
                               str(worker)], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)
             for worker in (wb, wc)]
    for p in procs:
        stdout, stderr = p.communicate(timeout=45)
        assert p.returncode == 0 and 'MERGE_OK' in stdout, (
            p.returncode, stdout, stderr)
    assert exact(out) == {A: (2, 10), B: (1, 21), C: (2, 22)}
    print('PASS concurrent writer union')

    # 6. Invalid geometry cannot be mistaken for a conflicting exact result.
    out = d/'invalid-out.csv'
    invalid = write(d/'invalid.csv', line((31, 0), 2))
    refused(run(out, base, invalid), 'noncanonical or unsafe')
    assert not out.exists()
    print('PASS invalid geometry refused')

print('MERGE_GUARD_OK')
PY
