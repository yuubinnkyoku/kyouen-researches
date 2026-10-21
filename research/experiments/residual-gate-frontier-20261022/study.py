#!/usr/bin/env python3
"""Bounded, manually run gate study; freeze and select before confirmation."""
import argparse, hashlib, itertools, json, pathlib, random, statistics, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / 'residual-dfpn-integration-20261021'
sys.path.insert(0, str(OLD))
from integration import parse, roots_csv
sys.path.insert(0, str(HERE.parent / 'n11-search-methods/scripts'))
from dfpn_edge_classes import forbidden, d4_canonical_key

GATES = (0, 6, 12, 18, 24, 32, 48, 64)
CORE = ('cpp/solvers/kyouen_dfpn_root.cpp', 'cpp/solvers/kyouen_residual_micro.hpp')


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, data):
    path = HERE / name
    assert not path.exists(), f'cannot overwrite {path}'
    path.write_text(json.dumps(data, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def committed(name):
    path = HERE / name
    assert subprocess.check_output(['git', 'show', f'HEAD:{path.relative_to(ROOT)}'], cwd=ROOT) == path.read_bytes()


def freeze(solver):
    for name in CORE:
        assert subprocess.check_output(['git', 'show', f'HEAD:{name}'], cwd=ROOT) == (ROOT / name).read_bytes()
    old = json.loads((OLD / 'fixtures.json').read_text())
    train = [dict(f, id=f'train-{i}') for i, f in enumerate(old) if f['group'] == 'deep']
    seen = {d4_canonical_key(f['occupied']) for f in train}
    rng = random.Random(20261022)
    confirm = []
    attempts = 0
    while len(confirm) < 6:
        attempts += 1
        occ = sorted(rng.sample(range(121), 5))
        if any(forbidden(*q) for q in itertools.combinations(occ, 4)):
            continue
        key = d4_canonical_key(occ)
        if key in seen:
            continue
        seen.add(key)
        legal = [v for v in range(121) if v not in occ and not any(forbidden(*t, v) for t in itertools.combinations(occ, 3))]
        confirm.append(dict(id=f'confirm-{len(confirm)}', occupied=occ, legal=len(legal), expected=0, group='deep'))
    late = [dict(f, id=f'late-{i}') for i, f in enumerate(old) if f['group'] == 'late']
    data = dict(train=train, confirm=confirm, late=late)
    write('fixtures.json', data)
    (HERE / 'roots').mkdir(exist_ok=True)
    for f in train + confirm + late:
        roots_csv(HERE / 'roots' / f'{f["id"]}.csv', [f['occupied']])
    write('protocol.json', dict(gates=GATES, quota=128, repeats=3, train_limit=20000,
        confirmation_limits=[20000, 100000], seed=20261022, generation_attempts=attempts,
        source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        source_hashes={p: sha(ROOT / p) for p in CORE}, solver_sha256=sha(pathlib.Path(solver)),
        fixtures_sha256=sha(HERE / 'fixtures.json'), roots_sha256={p.name: sha(p) for p in (HERE / 'roots').glob('*.csv')},
        compiler=subprocess.check_output(['g++', '--version'], text=True).splitlines()[0],
        selection='among gates >=12: minimize unknown roots, sum of per-root median solve_us, then gate; use training only',
        diagnostic='OFF, profile ON, 100000 nodes on three training roots; distinct from unprofiled timing',
        confirmation='six seeded unseen safe S5 roots; OFF, gate6, selected broader gate; three repeats at both limits',
        correctness='26 reused known late roots, each selected setting once at 20000; no timing generalization',
        abort='stop on newly decided deep verdict; independently validate before adoption',
        node_definition='df-pn iterations plus native exact nodes; residual quota separate',
        default='OFF unchanged; no automatic or push-triggered long searches'))


def histogram(raw):
    result = {}
    for line in raw.splitlines():
        if line.startswith('# residual_gate_profile '):
            row = {k: int(v) for k, v in (x.split('=') for x in line.split()[2:])}
            assert row['seq'] == 1 and 0 <= row['legal'] <= 121 and row['frames'] > 0
            assert row['legal'] not in result
            result[row['legal']] = row['frames']
    return result


def validate(raw, f, gate, limit, profile=False):
    rows = parse(raw)
    assert len(rows) == 1
    r = rows[0]
    assert r['stones'] == len(f['occupied'])
    assert r['occupied_lo'] == sum(1 << v for v in f['occupied'] if v < 64)
    assert r['occupied_hi'] == sum(1 << (v - 64) for v in f['occupied'] if v >= 64)
    assert r['node_limited'] == 1 and r['node_budget'] == limit and r['exact_nodes'] == 0
    assert r['residual_gate'] == gate and r['pn_enabled'] == int(gate > 0) and r['pn_budget'] == 128
    assert r['result'] == f['expected'], 'new deep verdict requires independent verification'
    assert r['pn_aborts'] <= 1
    if not gate:
        assert r['pn_nodes'] == r['residual_calls'] == 0
    if not profile:
        assert r['build_ns'] == r['structure_ns'] == r['grundy_ns'] == 0
        assert not histogram(raw)
    else:
        h = histogram(raw)
        assert sum(h.values()) <= r['visited']
        if r['visited']:
            assert h
        r['histogram'] = h
    return r


def run(solver, phase, fixtures, gates, limits, repeats, profile=False):
    records = []
    rawdir = HERE / 'raw'
    rawdir.mkdir(exist_ok=True)
    for repeat in range(repeats):
        order = gates[repeat % len(gates):] + gates[:repeat % len(gates)]
        for limit in limits:
            for gate in order:
                for f in fixtures:
                    stem = f'{phase}-{f["id"]}-g{gate}-n{limit}-r{repeat}'
                    output = rawdir / f'{stem}.csv'
                    assert not output.exists()
                    cmd = [solver, '--n=11', '--memo=18', '--budget=30', '--exact-legal=0',
                        f'--node-budget={limit}', f'--roots-csv={HERE / "roots" / (f["id"] + ".csv")}',
                        f'--csv={output}', f'--log={rawdir / (stem + ".log")}', '--residual-outcome-budget=128']
                    if gate:
                        cmd += [f'--residual-exact-legal={gate}', '--residual-evaluator=outcome']
                    if profile:
                        cmd += ['--residual-profile']
                    subprocess.run(cmd, check=True, timeout=45, stdout=subprocess.DEVNULL)
                    r = validate(output.read_text(), f, gate, limit, profile)
                    records.append(dict(id=f['id'], gate=gate, limit=limit, repeat=repeat, raw=str(output.relative_to(HERE)), **r))
                    print(stem, r['result'], r['nodes'], r['residual_calls'], r['solve_us'], flush=True)
    return records


def aggregate(records, gates):
    totals = {}
    for limit in sorted({r['limit'] for r in records}):
        for gate in gates:
            rows = [r for r in records if r['limit'] == limit and r['gate'] == gate]
            groups = [[r for r in rows if r['id'] == i] for i in sorted({r['id'] for r in rows})]
            for group in groups:
                if not any(r['reason'] == 'TIME_BUDGET' for r in group):
                    assert len({(r['result'], r['nodes'], r['pn_nodes'], r['residual_calls']) for r in group}) == 1
            totals[f'n{limit}-g{gate}'] = dict(unknown=sum(any(r['result'] == 0 for r in g) for g in groups),
                watchdogs=sum(r['reason'] == 'TIME_BUDGET' for r in rows),
                **{k: sum(statistics.median(r[k] for r in g) for g in groups)
                   for k in ('solve_us', 'nodes', 'expansions', 'pn_nodes', 'pn_aborts', 'residual_calls')})
    return totals


def main():
    p = argparse.ArgumentParser()
    p.add_argument('phase', choices=['freeze', 'train', 'confirm', 'verify'])
    p.add_argument('--solver', default='/tmp/dfpn-gate-profile')
    args = p.parse_args()
    if args.phase == 'freeze':
        freeze(args.solver)
        return
    protocol, data = read('protocol.json'), read('fixtures.json')
    assert sha(HERE / 'fixtures.json') == protocol['fixtures_sha256']
    for name, value in protocol['roots_sha256'].items():
        assert sha(HERE / 'roots' / name) == value
    if args.phase in ('train', 'confirm'):
        committed('protocol.json'); committed('fixtures.json')
        assert sha(pathlib.Path(args.solver)) == protocol['solver_sha256']
    if args.phase == 'train':
        assert not (HERE / 'training.json').exists()
        write('diagnostic.json', run(args.solver, 'diagnostic', data['train'], [0], [100000], 1, True))
        rows = run(args.solver, 'train', data['train'], list(GATES), [20000], 3)
        totals = aggregate(rows, GATES)
        gate = min(GATES[2:], key=lambda g: (totals[f'n20000-g{g}']['unknown'], totals[f'n20000-g{g}']['solve_us'], g))
        write('training.json', dict(records=rows, totals=totals))
        write('selection.json', dict(gate=gate, training_sha256=sha(HERE / 'training.json'), rule=protocol['selection']))
    elif args.phase == 'confirm':
        committed('selection.json'); committed('training.json')
        selected = read('selection.json')['gate']
        gates = [0, 6, selected]
        rows = run(args.solver, 'confirm', data['confirm'], gates, protocol['confirmation_limits'], 3)
        write('confirmation.json', dict(records=rows, totals=aggregate(rows, gates)))
        write('late.json', run(args.solver, 'late', data['late'], gates, [20000], 1))
    else:
        count = 0
        for name, fixtures, profile in [('diagnostic.json', data['train'], True), ('training.json', data['train'], False),
                ('confirmation.json', data['confirm'], False), ('late.json', data['late'], False)]:
            saved = read(name)
            rows = saved['records'] if isinstance(saved, dict) else saved
            lookup = {f['id']: f for f in fixtures}
            keys = set()
            for r in rows:
                key = (r['id'], r['gate'], r['limit'], r['repeat'])
                assert key not in keys
                keys.add(key)
                actual = validate((HERE / r['raw']).read_text(), lookup[r['id']], r['gate'], r['limit'], profile)
                assert json.loads(json.dumps(actual)) == {k: v for k, v in r.items() if k in actual}
                count += 1
            if isinstance(saved, dict):
                assert aggregate(rows, sorted({r['gate'] for r in rows})) == saved['totals']
        assert len(read('diagnostic.json')) == 3 and len(read('training.json')['records']) == 72
        assert len(read('confirmation.json')['records']) == 108 and len(read('late.json')) == 78
        train = read('training.json')['totals']
        selected = min(GATES[2:], key=lambda g: (train[f'n20000-g{g}']['unknown'], train[f'n20000-g{g}']['solve_us'], g))
        assert read('selection.json')['gate'] == selected
        assert read('selection.json')['training_sha256'] == sha(HERE / 'training.json')
        for f in data['confirm']:
            occ = f['occupied']
            assert not any(forbidden(*q) for q in itertools.combinations(occ, 4))
            legal = [v for v in range(121) if v not in occ and not any(forbidden(*t, v) for t in itertools.combinations(occ, 3))]
            assert len(legal) == f['legal']
        print(f'VERIFIED {count} root evaluations, histograms, training selection, prospective inputs, quotas and aggregates')


if __name__ == '__main__':
    main()
