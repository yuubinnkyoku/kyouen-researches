"""Cold exact re-probes of the two solver-trusted next10m S5 verdicts.

Regenerates disposable native proof traces under build/n11-adaptive-native-traces/
with the same solver source, memo power, order and budget as the
n11-conflict-closure-20261013 next10m run (indices 126899 LOSS, 144095 WIN).
Existing next10m/focus artifacts are never overwritten. The raw completed
labels recorded here stay solver-trusted; they become independent evidence
only through the subsequent terminal-only check_trace receipt.
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
PRIOR = ROOT / 'research/experiments/n11-conflict-closure-20261013/output/next10m-manifest.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solver', type=Path, default=ROOT / 'build/kyouen-dfpn-root-adaptive')
    p.add_argument('--budget', type=int, default=10000000)
    p.add_argument('--memo', type=int, default=20)
    p.add_argument('--order', default='count')
    p.add_argument('--prefix', default='adaptive10m')
    p.add_argument('--indices', type=int, nargs='*', default=[126899, 144095])
    p.add_argument('--timeout', type=int, default=600)
    args = p.parse_args()
    assert 0 < args.budget and 16 <= args.memo <= 24
    data = json.loads(SOURCE.read_text())
    prior = json.loads(PRIOR.read_text())
    by_source = {r['s5_index']: r for r in data['rows'] if 'polarity_conflicts' in r['labels']}
    by_prior = {r['s5_index']: r for r in prior['rows']}
    manifest = EXP / f'output/{args.prefix}-manifest.json'
    assert not manifest.exists(), 'refusing to overwrite existing run'
    binary = args.solver.resolve()
    result = dict(schema='n11-adaptive-terminal-verify-probes-v1', budget=args.budget, memo_power=args.memo,
                  order=args.order, source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
                  prior_manifest=str(PRIOR.relative_to(ROOT)), prior_manifest_sha256=sha(PRIOR),
                  solver_binary_sha256=sha(binary),
                  solver_source_sha256=sha(ROOT / 'cpp/solvers/kyouen_dfpn_root.cpp'),
                  rows=[],
                  trust='raw solver completed labels are solver-trusted only; independent evidence requires a terminal-only check_trace receipt with trusted_leaves=0; UNKNOWN is not evidence')
    trace_dir = ROOT / 'build/n11-adaptive-native-traces'
    trace_dir.mkdir(exist_ok=True)
    for index in args.indices:
        row = by_source[index]
        prow = by_prior[index]
        assert row['mask'] == prow['mask'], 'pilots/prior mask mismatch'
        src = EXP / f'input/s5-{index}.csv'
        text = f'conflict,{index},5,{row["mask"][0]},{row["mask"][1]},{row["legal"]},5,0,0,0,0\n'
        if src.exists():
            assert src.read_text() == text
        else:
            src.write_text(text)
        out = EXP / f'output/{args.prefix}-{index}.csv'
        log = EXP / f'output/{args.prefix}-{index}.log'
        trace = trace_dir / f'{args.prefix}-{index}.csv'
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
        assert v in (1, 2) and 0 < nodes <= args.budget, 'target row must re-solve; UNKNOWN is not evidence'
        assert int(r[2]) == 5 and int(r[3]) == row['legal'] and [int(r[9]), int(r[10])] == row['mask']
        assert trace.exists()
        trace_sha = sha(trace)
        result['rows'].append(dict(s5_index=index, mask=row['mask'], legal=row['legal'],
                                   canonical_children=row['canonical_children'], status='SOLVED', verdict=v,
                                   nodes=nodes, wall_seconds=round(wall, 3), peak_rss_kib=usage.ru_maxrss,
                                   input_sha256=sha(src), output_sha256=sha(out),
                                   trace_sha256=trace_sha, trace_path=str(trace.relative_to(ROOT)),
                                   prior_nodes=prow['nodes'], prior_wall_seconds=prow['wall_seconds'],
                                   prior_verdict=prow['verdict'], prior_trace_sha256=prow['trace_sha256'],
                                   trace_sha256_matches_prior=trace_sha == prow['trace_sha256'],
                                   verdict_matches_prior=v == prow['verdict']))
        manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps(result['rows'][-1]), flush=True)


if __name__ == '__main__':
    main()
