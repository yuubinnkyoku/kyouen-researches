"""Task A: 197665 budget-extension run (node budget 25M, memo 20, cold TT, capture).

This is a NEW run with an expanded node budget, not a re-run of the frozen 10M
condition: the 10M run (n11-night-batch1) ended NODE_LIMIT with 85/87 root
children WIN and 2 UNKNOWN. Verdicts (WIN=1/LOSS=2/UNKNOWN=0) are saved
verbatim; if 25M still ends NODE_LIMIT the row stays UNKNOWN and is never
imputed or re-run at this budget. SOLVED rows carry a captured terminal proof
DAG and go to terminal-only independent verification (verify_night2.py).
Runs are strictly sequential (workers=1); cold TT means a fresh process with
no --s5-cache. Peak RSS is taken from wait4 rusage.
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
RANKING = ROOT / 'research/experiments/n11-conflict-ranking-20261013/output/ranking.tsv'
FROZEN_10M = ROOT / 'research/experiments/n11-night-batch1-20261014/output/nightb10m-manifest.json'

DEFAULT_INDEX = 197665


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_profile(csv_path):
    census = {'WIN': 0, 'LOSS': 0, 'UNKNOWN': 0}
    table = {}
    for line in csv_path.read_text().splitlines():
        if line.startswith('# exact-profile-child '):
            fields = dict(kv.split('=', 1) for kv in line.split()[2:])
            census[fields['verdict']] = census.get(fields['verdict'], 0) + 1
        elif line.startswith('# exact-profile '):
            table = dict(kv.split('=', 1) for kv in line.split()[2:])
    return census, table


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solver', type=Path, default=ROOT / 'build/kyouen-dfpn-root-adaptive')
    p.add_argument('--budget', type=int, default=25000000)
    p.add_argument('--memo', type=int, default=20)
    p.add_argument('--order', default='count')
    p.add_argument('--prefix', default='nighta25m')
    p.add_argument('--indices', type=int, nargs='*', default=[DEFAULT_INDEX])
    p.add_argument('--profile', action='store_true', default=True)
    p.add_argument('--no-profile', dest='profile', action='store_false')
    args = p.parse_args()
    assert 0 < args.budget and 16 <= args.memo <= 24
    assert args.budget > 10000000, 'task A is the 25M extension, not a 10M re-run'
    data = json.loads(SOURCE.read_text())
    candidates = [r for r in data['rows'] if 'polarity_conflicts' in r['labels'] and r['s5_index'] in args.indices]
    candidates.sort(key=lambda r: (r['canonical_children'], r['legal'], r['s5_index']))
    assert {r['s5_index'] for r in candidates} == set(args.indices)
    ranking = {}
    with RANKING.open() as stream:
        header = stream.readline().rstrip('\n').split('\t')
        for line in stream:
            row = dict(zip(header, line.rstrip('\n').split('\t')))
            ranking[int(row['s5_index'])] = row
    frozen = json.loads(FROZEN_10M.read_text())
    manifest = EXP / f'output/{args.prefix}-manifest.json'
    assert not manifest.exists(), 'refusing to overwrite existing run'
    binary = args.solver.resolve()
    result = dict(schema='n11-night-batch2-task-a-v1', budget=args.budget, memo_power=args.memo,
                  order=args.order, workers=1, profile=args.profile, prefix=args.prefix,
                  kind='budget-extension-new-run (not a same-condition re-run of the 10M probe)',
                  source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
                  ranking=str(RANKING.relative_to(ROOT)), ranking_sha256=sha(RANKING),
                  frozen_10m_manifest=str(FROZEN_10M.relative_to(ROOT)),
                  frozen_10m_manifest_sha256=sha(FROZEN_10M),
                  solver_binary_sha256=sha(binary),
                  solver_source_sha256=sha(ROOT / 'cpp/solvers/kyouen_dfpn_root.cpp'),
                  rows=[],
                  trust=('completed labels solver-trusted until independent terminal-only verification; '
                         'UNKNOWN is not evidence; NODE_LIMIT rows stay UNKNOWN and are not re-run at this budget'))
    trace_dir = ROOT / 'build/n11-night-batch2-traces'
    trace_dir.mkdir(exist_ok=True)
    for row in candidates:
        index = row['s5_index']
        src = EXP / f'input/s5-{index}.csv'
        assert src.exists(), index
        out = EXP / f'output/{args.prefix}-{index}.csv'
        log = EXP / f'output/{args.prefix}-{index}.log'
        trace = trace_dir / f'{args.prefix}-{index}-proof.csv'
        assert not out.exists() and not log.exists() and not trace.exists()
        frow = next(r for r in frozen['rows'] if r['s5_index'] == index)
        command = [str(binary), '--n=11', f'--memo={args.memo}', '--only=5', f'--exact-order={args.order}',
                   f'--exact-replay={src}', f'--exact-replay-budget={args.budget}', f'--csv={out}']
        if args.profile:
            command.append('--exact-replay-profile')
        command.append(f'--proof-dag={trace}')
        started = time.monotonic()
        with log.open('w') as stream:
            child = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, text=True)
            _, status, usage = os.wait4(child.pid, 0)
            child.returncode = os.waitstatus_to_exitcode(status)
        wall = time.monotonic() - started
        item = dict(s5_index=index, mask=row['mask'], legal=row['legal'],
                    canonical_children=row['canonical_children'],
                    budget=args.budget, wall_seconds=round(wall, 3), peak_rss_kib=usage.ru_maxrss,
                    returncode=child.returncode,
                    frozen_10m_status=frow['status'], frozen_10m_verdict=frow['verdict'],
                    frozen_10m_nodes=frow['nodes'])
        if child.returncode != 0:
            item.update(status='RUN_FAILED', verdict=None, nodes=None,
                        trust_class='no-run; process died (e.g. OOM-killed) before verdict')
            result['rows'].append(item)
            manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
            print(json.dumps(item), flush=True)
            continue
        raw = out.read_text()
        assert 'replay_error,' not in raw and '# replay_done rows=1' in raw
        rows = [s.split(',') for s in raw.splitlines() if s.startswith('replay,')]
        assert len(rows) == 1
        r = rows[0]
        v = int(r[6])
        nodes = int(r[7])
        assert v in (0, 1, 2) and 0 < nodes <= args.budget
        assert int(r[2]) == 5 and int(r[3]) == row['legal'] and [int(r[9]), int(r[10])] == row['mask']
        if v == 0:
            assert nodes == args.budget and not trace.exists()
        else:
            assert trace.exists()
        census, table = parse_profile(out) if args.profile else ({}, {})
        rank_row = ranking[index]
        item.update(status='SOLVED' if v else 'NODE_LIMIT', verdict=v, nodes=nodes,
                    input_sha256=sha(src), output_sha256=sha(out),
                    trace_bytes=trace.stat().st_size if trace.exists() else None,
                    trace_sha256=sha(trace) if trace.exists() else None,
                    trace_path=str(trace.relative_to(ROOT)) if trace.exists() else None,
                    root_child_census=census or None,
                    exact_profile=table or None,
                    trust_class='solver-trusted pending terminal-only receipt' if v else 'UNKNOWN (not evidence)',
                    ranking={k: rank_row[k] for k in
                             ('geometry_rank', 'canonical_s6_children', 'stabilizer_order',
                              'if_win_loss_choices_invalidated', 'if_loss_fixed_win_branches_uncovered',
                              'if_win_new_free_win_branches', 'if_win_greedy_delta', 'impact_per_child_rank')})
        result['rows'].append(item)
        manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps(item), flush=True)
    result['counts'] = {name: sum(r.get('verdict') == v for r in result['rows']) for name, v in [('UNKNOWN', 0), ('WIN', 1), ('LOSS', 2)]}
    result['completed_candidates'] = len(candidates)
    manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result['counts']), flush=True)


if __name__ == '__main__':
    main()
