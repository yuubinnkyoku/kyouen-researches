"""Task A: cold trace regeneration of the three solver-trusted next10m LOSS rows.

Regenerates disposable native proof traces under build/n11-night-batch1-traces/
with the same solver source, memo power, order and node budget as the frozen
n11-conflict-closure-20261013 next10m run (indices 137694, 143240, 220231,
all verdict=2). This is NOT a re-derivation of the verdict: the raw completed
labels stay solver-trusted; the propositions are carried only by the
subsequent terminal-only check_trace receipt (trusted_leaves=0).

The regenerated trace is byte-compared against the frozen next10m-manifest
trace_sha256. Existing next10m/focus/adaptive artifacts are never overwritten.
Run under WSL Linux Python (os.wait4), like n11-adaptive-verify.
"""
import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json'
FROZEN = ROOT / 'research/experiments/n11-conflict-closure-20261013/output/next10m-manifest.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solver', type=Path, default=ROOT / 'build/kyouen-dfpn-root-adaptive')
    p.add_argument('--budget', type=int, default=10000000)
    p.add_argument('--memo', type=int, default=20)
    p.add_argument('--order', default='count')
    p.add_argument('--indices', type=int, nargs='*', default=[137694, 143240, 220231])
    args = p.parse_args()
    assert 0 < args.budget and 16 <= args.memo <= 24
    data = json.loads(SOURCE.read_text())
    frozen = json.loads(FROZEN.read_text())
    by_source = {r['s5_index']: r for r in data['rows'] if 'polarity_conflicts' in r['labels']}
    by_frozen = {r['s5_index']: r for r in frozen['rows']}
    manifest = EXP / 'output/night-a-manifest.json'
    assert not manifest.exists(), 'refusing to overwrite existing run'
    binary = args.solver.resolve()
    result = dict(schema='n11-night-batch1-task-a-v1', budget=args.budget, memo_power=args.memo,
                  order=args.order, source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
                  frozen_manifest=str(FROZEN.relative_to(ROOT)), frozen_manifest_sha256=sha(FROZEN),
                  solver_binary_sha256=sha(binary),
                  solver_source_sha256=sha(ROOT / 'cpp/solvers/kyouen_dfpn_root.cpp'),
                  rows=[],
                  trust=('regenerated raw solver completed labels stay solver-trusted; '
                         'independent evidence requires the terminal-only check_trace receipt '
                         'with trusted_leaves=0 and a byte-identical frozen trace SHA; UNKNOWN is not evidence'))
    trace_dir = ROOT / 'build/n11-night-batch1-traces'
    trace_dir.mkdir(exist_ok=True)
    for index in args.indices:
        row = by_source[index]
        frow = by_frozen[index]
        assert row['mask'] == frow['mask'], 'pilots/frozen mask mismatch'
        assert frow['status'] == 'SOLVED' and frow['verdict'] in (1, 2), index
        src = EXP / f'input/s5-{index}.csv'
        assert src.exists(), index
        out = EXP / f'output/night-a-{index}.csv'
        log = EXP / f'output/night-a-{index}.log'
        trace = trace_dir / f'night-a-{index}.csv'
        assert not out.exists() and not log.exists() and not trace.exists()
        command = [str(binary), '--n=11', f'--memo={args.memo}', '--only=5', f'--exact-order={args.order}',
                   f'--exact-replay={src}', f'--exact-replay-budget={args.budget}',
                   f'--proof-dag={trace}', f'--csv={out}']
        started = time.monotonic()
        with log.open('w') as stream:
            child = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, text=True)
            _, status, usage = os.wait4(child.pid, 0)
            child.returncode = os.waitstatus_to_exitcode(status)
        wall = time.monotonic() - started
        assert child.returncode == 0, index
        raw = out.read_text()
        assert 'replay_error,' not in raw and '# replay_done rows=1' in raw
        rows = [s.split(',') for s in raw.splitlines() if s.startswith('replay,')]
        assert len(rows) == 1
        r = rows[0]
        v = int(r[6])
        nodes = int(r[7])
        assert v in (1, 2) and 0 < nodes <= args.budget, 'regenerated run must re-solve'
        assert int(r[2]) == 5 and int(r[3]) == row['legal'] and [int(r[9]), int(r[10])] == row['mask']
        assert trace.exists()
        trace_sha = sha(trace)
        result['rows'].append(dict(s5_index=index, mask=row['mask'], legal=row['legal'],
                                   canonical_children=row['canonical_children'],
                                   status='SOLVED', verdict=v, nodes=nodes,
                                   wall_seconds=round(wall, 3), peak_rss_kib=usage.ru_maxrss,
                                   input_sha256=sha(src), output_sha256=sha(out),
                                   trace_bytes=trace.stat().st_size, trace_sha256=trace_sha,
                                   trace_path=str(trace.relative_to(ROOT)),
                                   frozen_nodes=frow['nodes'], frozen_verdict=frow['verdict'],
                                   frozen_trace_sha256=frow['trace_sha256'],
                                   nodes_match_frozen=nodes == frow['nodes'],
                                   verdict_match_frozen=v == frow['verdict'],
                                   trace_sha256_matches_frozen=trace_sha == frow['trace_sha256']))
        manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps(result['rows'][-1]), flush=True)
    assert all(r['trace_sha256_matches_frozen'] and r['verdict_match_frozen'] and r['nodes_match_frozen']
               for r in result['rows']), 'frozen byte-identity check failed'
    result['counts'] = dict(rows=len(result['rows']),
                            trace_sha256_matches_frozen=sum(r['trace_sha256_matches_frozen'] for r in result['rows']))
    manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result['counts']), flush=True)


if __name__ == '__main__':
    main()
