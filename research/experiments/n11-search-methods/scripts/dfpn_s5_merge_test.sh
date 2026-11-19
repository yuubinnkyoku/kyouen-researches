#!/usr/bin/env bash
# End-to-end fail-closed S5 cache merge regression using real canonical safe keys.
set -euo pipefail
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dfpn_s5_merge.sh"
python3 - "$SCRIPT" <<'PY'
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile

script = pathlib.Path(sys.argv[1]).resolve()
root = script.parents[4]
A = (1152921504742115328, 536870912)
B = (3602879701897445376, 134217728)
C = (10520408729537478660, 67108864)
D = (10520408729538527232, 16384)
REGISTRY_REL = pathlib.Path('results/n11-s5-evidence-quarantine.json')
POLICY_REL = pathlib.Path('research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py')


def line(key, verdict, nodes=10):
    return f's5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n'


def write(path, data):
    path.write_text(data, encoding='utf-8')
    return path


def run(out, *inputs, using=script):
    return subprocess.run(['bash', str(using), str(out), *map(str, inputs)],
                          capture_output=True, text=True)


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


def success(proc):
    assert proc.returncode == 0 and 'MERGE_OK' in proc.stdout, (
        proc.returncode, proc.stdout, proc.stderr)


def refused(proc, why):
    assert proc.returncode != 0 and 'MERGE_REFUSED' in proc.stderr and why in proc.stderr, (
        proc.returncode, proc.stdout, proc.stderr)


def transform(key, reflection=False, rotation=1):
    lo, hi = key
    points = [i for i in range(121)
              if ((lo if i < 64 else hi) >> (i % 64)) & 1]
    transformed = []
    for p in points:
        x, y = p % 11, p // 11
        if reflection:
            x = 10 - x
        for _ in range(rotation):
            x, y = y, 10 - x
        transformed.append(11 * y + x)
    mask = sum(1 << p for p in transformed)
    return mask & ((1 << 64) - 1), mask >> 64


with tempfile.TemporaryDirectory(prefix='n11-s5-merge-test-') as td:
    d = pathlib.Path(td)
    base = write(d / 'base.csv', line(A, 2, 10))
    agreeing = write(d / 'agree.csv', line(A, 2, 7) + line(B, 1, 20))
    conflicting = write(d / 'conflict.csv', line(A, 1, 30))
    unknown = write(d / 'unknown.csv', line(C, 0) + line(D, 2, 4))

    # 1. Clean overlap succeeds; duplicate exact verdicts take min(nodes).
    out = d / 'clean.csv'
    success(run(out, base, agreeing))
    assert exact(out) == {A: (2, 7), B: (1, 20)}
    print('PASS clean canonical merge')

    # 2. Conflicting WIN/LOSS fails before creating any output.
    out = d / 'conflict-out.csv'
    refused(run(out, base, conflicting), 'CONFLICT')
    assert not out.exists()
    assert not list(d.glob(f'.{out.name}.*.tmp'))
    print('PASS conflict leaves no output')

    # 3. UNKNOWN is not a proof and never appears in the merged cache.
    out = d / 'unknown-out.csv'
    success(run(out, base, unknown))
    assert exact(out) == {A: (2, 10), D: (2, 4)}
    print('PASS UNKNOWN discarded')

    # 4. Existing committed output is an input and is not clobbered on conflict.
    out = d / 'existing.csv'
    success(run(out, base))
    before = out.read_bytes()
    refused(run(out, agreeing, conflicting), 'CONFLICT')
    assert out.read_bytes() == before
    print('PASS existing output preserved on conflict')

    # 5. Two nonconflicting writers serialize and their union is preserved.
    out = d / 'parallel.csv'
    wb = write(d / 'worker-b.csv', line(B, 1, 21))
    wc = write(d / 'worker-c.csv', line(C, 2, 22))
    procs = [subprocess.Popen(['bash', str(script), str(out), str(base), str(worker)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for worker in (wb, wc)]
    for proc in procs:
        stdout, stderr = proc.communicate(timeout=45)
        assert proc.returncode == 0 and 'MERGE_OK' in stdout, (
            proc.returncode, stdout, stderr)
    assert exact(out) == {A: (2, 10), B: (1, 21), C: (2, 22)}
    print('PASS concurrent writer union')

    # 6. Invalid geometry is refused.
    out = d / 'invalid-out.csv'
    invalid = write(d / 'invalid.csv', line((31, 0), 2))
    refused(run(out, base, invalid), 'noncanonical or unsafe')
    assert not out.exists()
    print('PASS invalid geometry refused')

    # 7. A safe D4 alias is rejected before it can bypass canonical-key conflicts.
    alias = transform(A)
    assert alias != A
    alias_input = write(d / 'd4-alias.csv', line(alias, 2, 11))
    out = d / 'd4-alias-out.csv'
    refused(run(out, base, alias_input), 'noncanonical or unsafe')
    assert not out.exists()
    print('PASS D4 alias rejected')

    # 8. Active quarantined cache keys are removed from the committed union.
    registry = json.loads((root / REGISTRY_REL).read_text(encoding='utf-8'))
    active = [row for row in registry['entries'] if row.get('active') is True]
    assert active, 'expected at least one active quarantine fixture'
    qrow = active[0]
    qkey = tuple(qrow['key'])
    qinput = write(d / 'quarantine.csv', line(qkey, qrow['unsupported_verdict'], 99))
    out = d / 'quarantine-out.csv'
    qresult = run(out, qinput)
    success(qresult)
    assert exact(out) == {}
    assert 'quarantined keys: 1' in qresult.stdout
    print('PASS active quarantine removed')

    # 9. Conflicting concurrent writers cannot both commit; the loser sees the winner.
    for i in range(5):
        out = d / f'conflict-race-{i}.csv'
        w1 = write(d / f'conflict-w1-{i}.csv', line(B, 1, 100 + i))
        w2 = write(d / f'conflict-w2-{i}.csv', line(B, 2, 200 + i))
        procs = [subprocess.Popen(['bash', str(script), str(out), str(base), str(worker)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for worker in (w1, w2)]
        results = []
        for proc in procs:
            stdout, stderr = proc.communicate(timeout=45)
            results.append((proc.returncode, stdout, stderr))
        winners = [r for r in results if r[0] == 0 and 'MERGE_OK' in r[1]]
        losers = [r for r in results if r[0] != 0 and 'CONFLICT' in r[2]]
        assert len(winners) == 1 and len(losers) == 1, results
        merged = exact(out)
        assert merged[A] == (2, 10) and merged[B][0] in (1, 2), merged
    print('PASS 5 conflicting-writer races (one commit, one refusal each)')

    if os.name != 'nt':
        # 10. A symlinked lock sidecar is refused without touching its target.
        out = d / 'symlink-lock.csv'
        target = write(d / 'lock-target', 'do-not-touch')
        (d / 'symlink-lock.csv.lock').symlink_to(target)
        refused(run(out, base), 'symlinked S5 cache lock is unsafe')
        assert target.read_text(encoding='utf-8') == 'do-not-touch' and not out.exists()
        print('PASS symlink lock refused')

        # 11. A hard-linked output is refused without splitting or modifying aliases.
        out = write(d / 'hardlinked.csv', 'sentinel\n')
        alias_out = d / 'hardlinked-alias.csv'
        os.link(out, alias_out)
        refused(run(out, base), 'hard-linked S5 cache output is unsafe')
        assert out.read_text(encoding='utf-8') == 'sentinel\n'
        assert alias_out.read_text(encoding='utf-8') == 'sentinel\n'
        print('PASS hard-linked output refused')

        # 12. Atomic replacement preserves ordinary group-readable mode bits.
        out = write(d / 'mode.csv', '# old\n')
        out.chmod(0o640)
        success(run(out, base))
        assert stat.S_IMODE(out.stat().st_mode) == 0o640
        print('PASS output mode preserved')

    # 13. Missing/corrupt quarantine registries fail closed in an isolated copy.
    with tempfile.TemporaryDirectory(prefix='n11-s5-registry-fixture-') as td2:
        fixture = pathlib.Path(td2)
        alt_script = fixture / 'research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh'
        alt_script.parent.mkdir(parents=True)
        shutil.copy2(script, alt_script)
        alt_policy = fixture / POLICY_REL
        alt_policy.parent.mkdir(parents=True)
        shutil.copy2(root / POLICY_REL, alt_policy)
        alt_registry = fixture / REGISTRY_REL
        alt_registry.parent.mkdir(parents=True)
        shutil.copy2(root / REGISTRY_REL, alt_registry)
        out = d / 'missing-registry.csv'
        alt_registry.unlink()
        refused(run(out, base, using=alt_script), 'missing S5 evidence quarantine registry')
        assert not out.exists()
        alt_registry.write_text('{"schema":"wrong","entries":[]}', encoding='utf-8')
        out = d / 'corrupt-registry.csv'
        refused(run(out, base, using=alt_script), 'invalid S5 quarantine registry schema')
        assert not out.exists()
    print('PASS missing/corrupt registry fails closed')

print('MERGE_GUARD_OK')
PY
