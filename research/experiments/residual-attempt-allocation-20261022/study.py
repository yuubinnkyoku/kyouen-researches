#!/usr/bin/env python3
"""Manually run bounded comparison of whole-root and sliced residual quotas."""
import argparse, hashlib, itertools, json, pathlib, random, statistics, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREVIOUS = HERE.parent / 'residual-gate-frontier-20261022'
sys.path.insert(0, str(HERE.parent / 'residual-dfpn-integration-20261021'))
from integration import parse, roots_csv
sys.path.insert(0, str(HERE.parent / 'n11-search-methods/scripts'))
from dfpn_edge_classes import forbidden, d4_canonical_key
SETTINGS = ('off', 'whole', 'slice8', 'slice32')
CAP = dict(off=0, whole=0, slice8=8, slice32=32)
CORE = ('cpp/solvers/kyouen_dfpn_root.cpp', 'cpp/solvers/kyouen_residual_micro.hpp')

def read(name): return json.loads((HERE / name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, data):
    path = HERE / name
    assert not path.exists(), f'refusing to overwrite {path}'
    path.write_text(json.dumps(data, indent=2) + '\n')
def committed(name):
    path = HERE / name
    assert subprocess.check_output(['git', 'show', f'HEAD:{path.relative_to(ROOT)}'], cwd=ROOT) == path.read_bytes()

def fresh_roots(train):
    rng = random.Random(2026102202)
    seen = {d4_canonical_key(f['occupied']) for f in train}
    rows = []
    while len(rows) < 6:
        occ = sorted(rng.sample(range(121), 5))
        key = d4_canonical_key(occ)
        if key in seen or any(forbidden(*q) for q in itertools.combinations(occ, 4)): continue
        seen.add(key)
        legal = [v for v in range(121) if v not in occ and not any(forbidden(*t, v) for t in itertools.combinations(occ, 3))]
        rows.append(dict(id=f'confirm-{len(rows)}', occupied=occ, legal=len(legal), expected=0, group='deep'))
    return rows

def freeze(solver):
    for name in CORE:
        assert subprocess.check_output(['git', 'show', f'HEAD:{name}'], cwd=ROOT) == (ROOT / name).read_bytes()
    old = json.loads((PREVIOUS / 'fixtures.json').read_text())
    train = [dict(f, id=f'train-{i}') for i, f in enumerate(old['train'] + old['confirm'])]
    data = dict(train=train, confirm=fresh_roots(train), late=old['late'])
    write('fixtures.json', data)
    (HERE / 'roots').mkdir(exist_ok=True)
    for group in data.values():
        for f in group: roots_csv(HERE / 'roots' / f'{f["id"]}.csv', [f['occupied']])
    write('protocol.json', dict(settings=SETTINGS, gate=18, quota=128, caps=CAP, repeats=3,
        train_limit=20000, confirmation_limits=[20000, 100000], seed=2026102202,
        selection='among slice8/slice32: minimize unknown roots, sum of per-root median expansions, sum of median solve_us, then cap',
        train='nine reused S5 roots from K0499; three repeats, fresh process and TT each root',
        confirm='six fresh safe seeded S5 roots, D4-distinct from training; OFF/whole/selected; three repeats at both limits',
        correctness='26 reused known late roots; OFF/whole/selected, one repeat at 20000; not timing evidence',
        abort='stop on a new deep root verdict; independently verify before adoption',
        duplicate_policy='one capped attempt per canonical board per root, shared by df-pn and native exact; reset per root',
        defaults='residual OFF; omitted attempt cap retains whole-root quota behavior',
        source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        source_hashes={p: sha(ROOT / p) for p in CORE}, solver_sha256=sha(pathlib.Path(solver)),
        compiler=subprocess.check_output(['g++', '--version'], text=True).splitlines()[0], compile_flags='-std=c++20 -O2',
        fixtures_sha256=sha(HERE / 'fixtures.json'), previous_fixtures_sha256=sha(PREVIOUS / 'fixtures.json'),
        roots_sha256={p.name: sha(p) for p in (HERE / 'roots').glob('*.csv')}))

def validate(raw, f, setting, limit):
    rows = parse(raw); assert len(rows) == 1
    r = rows[0]; cap = CAP[setting]
    assert r['seq'] == 1 and r['stones'] == len(f['occupied'])
    assert r['occupied_lo'] == sum(1 << v for v in f['occupied'] if v < 64)
    assert r['occupied_hi'] == sum(1 << (v - 64) for v in f['occupied'] if v >= 64)
    assert r['node_limited'] == 1 and r['node_budget'] == limit and r['exact_nodes'] == 0
    assert r['residual_gate'] == (0 if setting == 'off' else 18) and r['pn_enabled'] == int(setting != 'off')
    assert r['pn_budget'] == 128 and r['pn_attempt_budget'] == cap
    assert r['result'] == f['expected'], 'new deep root verdict needs independent verification'
    assert r['build_ns'] == r['structure_ns'] == r['grundy_ns'] == 0
    if cap:
        assert r['pn_aborts'] <= r['pn_attempted'] == r['residual_calls'] <= r['pn_nodes'] <= r['pn_attempted'] * cap
        assert r['pn_attempt_max'] <= min(cap, 128)
        if r['pn_remaining'] > 0: assert r['pn_aborts'] * cap <= r['pn_nodes']
        else: assert max(0, r['pn_aborts'] - 1) * cap + int(r['pn_aborts'] > 0) <= r['pn_nodes']
    else:
        assert r['pn_attempted'] == r['pn_attempt_skips'] == 0 and r['pn_aborts'] <= 1
    if setting == 'off': assert r['pn_nodes'] == r['residual_calls'] == 0
    assert not any(line.startswith('# residual_gate_profile ') for line in raw.splitlines())
    return r

def run(solver, phase, fixtures, settings, limits, repeats):
    records = []; (HERE / 'raw').mkdir(exist_ok=True)
    for repeat in range(repeats):
        for j, limit in enumerate(limits):
            shift = (repeat + j) % len(settings)
            order = settings[shift:] + settings[:shift]
            for setting in order:
                for f in fixtures:
                    stem = f'{phase}-{f["id"]}-{setting}-n{limit}-r{repeat}'
                    output = HERE / 'raw' / f'{stem}.csv'; assert not output.exists()
                    cmd = [solver, '--n=11', '--memo=18', '--budget=30', '--exact-legal=0',
                        f'--node-budget={limit}', f'--roots-csv={HERE / "roots" / (f["id"] + ".csv")}',
                        f'--csv={output}', f'--log={HERE / "raw" / (stem + ".log")}', '--residual-outcome-budget=128']
                    if setting != 'off': cmd += ['--residual-exact-legal=18', '--residual-evaluator=outcome']
                    if CAP[setting]: cmd += [f'--residual-attempt-budget={CAP[setting]}']
                    subprocess.run(cmd, check=True, timeout=45, stdout=subprocess.DEVNULL)
                    r = validate(output.read_text(), f, setting, limit)
                    records.append(dict(id=f['id'], setting=setting, limit=limit, repeat=repeat,
                        raw=str(output.relative_to(HERE)), **r))
                    print(stem, r['result'], r['expansions'], r['pn_nodes'], r['pn_aborts'], flush=True)
    return records

def aggregate(rows):
    result = {}
    for limit, setting in sorted({(r['limit'], r['setting']) for r in rows}):
        selected = [r for r in rows if r['limit'] == limit and r['setting'] == setting]
        groups = [[r for r in selected if r['id'] == i] for i in sorted({r['id'] for r in selected})]
        for group in groups:
            if not any(r['reason'] == 'TIME_BUDGET' for r in group):
                assert len({tuple(r[k] for k in ('result', 'nodes', 'expansions', 'residual_calls', 'pn_nodes', 'pn_aborts', 'pn_attempt_skips')) for r in group}) == 1
        result[f'n{limit}-{setting}'] = dict(unknown=sum(any(r['result'] == 0 for r in g) for g in groups),
            watchdogs=sum(r['reason'] == 'TIME_BUDGET' for r in selected),
            **{k: sum(statistics.median(r[k] for r in g) for g in groups)
               for k in ('solve_us', 'nodes', 'expansions', 'residual_calls', 'pn_nodes', 'pn_aborts', 'pn_attempt_skips')})
    return result

def select(totals):
    return min(('slice8', 'slice32'), key=lambda s: tuple(totals[f'n20000-{s}'][k] for k in ('unknown', 'expansions', 'solve_us')) + (CAP[s],))

def verify(protocol, data):
    assert data['confirm'] == fresh_roots(data['train'])
    old = json.loads((PREVIOUS / 'fixtures.json').read_text())
    assert data['train'] == [dict(f, id=f'train-{i}') for i, f in enumerate(old['train'] + old['confirm'])]
    assert data['late'] == old['late'] and sha(PREVIOUS / 'fixtures.json') == protocol['previous_fixtures_sha256']
    for name, value in protocol['source_hashes'].items():
        source = subprocess.run(['git', 'show', f'{protocol["source_commit"]}:{name}'], cwd=ROOT, capture_output=True)
        if source.returncode == 0: assert hashlib.sha256(source.stdout).hexdigest() == value
    total = 0
    for name, group, settings, limits, repeats in [('training.json', 'train', SETTINGS, [20000], 3),
            ('confirmation.json', 'confirm', ('off', 'whole', read('selection.json')['setting']), [20000, 100000], 3),
            ('late.json', 'late', ('off', 'whole', read('selection.json')['setting']), [20000], 1)]:
        saved = read(name); rows = saved['records']; fixtures = {f['id']: f for f in data[group]}
        assert len(rows) == len(fixtures) * len(settings) * len(limits) * repeats
        keys = {(r['id'], r['setting'], r['limit'], r['repeat']) for r in rows}
        assert len(keys) == len(rows) and keys == set(itertools.product(fixtures, settings, limits, range(repeats)))
        for r in rows:
            actual = validate((HERE / r['raw']).read_text(), fixtures[r['id']], r['setting'], r['limit'])
            assert actual == {k: v for k, v in r.items() if k in actual}
        assert aggregate(rows) == saved['totals']; total += len(rows)
    selected = read('selection.json')
    assert selected['setting'] == select(read('training.json')['totals'])
    assert selected['training_sha256'] == sha(HERE / 'training.json')
    confirmation = read('confirmation.json')
    assert confirmation['selection_sha256'] == sha(HERE / 'selection.json')
    source = subprocess.run(['git', 'show', f'{confirmation["selection_commit"]}:{(HERE / "selection.json").relative_to(ROOT)}'], cwd=ROOT, capture_output=True)
    if source.returncode == 0: assert source.stdout == (HERE / 'selection.json').read_bytes()
    print(f'VERIFIED {total} archived evaluations, seeded independent geometry, sliced/root budgets, coverage, selection and aggregates')

def main():
    p = argparse.ArgumentParser(); p.add_argument('phase', choices=['freeze', 'train', 'confirm', 'verify'])
    p.add_argument('--solver', default='/tmp/dfpn-attempt'); args = p.parse_args()
    if args.phase == 'freeze': freeze(args.solver); return
    protocol, data = read('protocol.json'), read('fixtures.json')
    assert protocol['settings'] == list(SETTINGS) and protocol['caps'] == CAP and protocol['quota'] == 128 and protocol['gate'] == 18
    assert protocol['repeats'] == 3 and protocol['seed'] == 2026102202 and protocol['train_limit'] == 20000
    assert protocol['confirmation_limits'] == [20000, 100000]
    assert sha(HERE / 'fixtures.json') == protocol['fixtures_sha256']
    assert set(protocol['roots_sha256']) == {f'{f["id"]}.csv' for group in data.values() for f in group}
    for name, value in protocol['roots_sha256'].items(): assert sha(HERE / 'roots' / name) == value
    if args.phase in ('train', 'confirm'):
        committed('protocol.json'); committed('fixtures.json')
        assert sha(pathlib.Path(args.solver)) == protocol['solver_sha256']
    if args.phase == 'train':
        rows = run(args.solver, 'train', data['train'], SETTINGS, [20000], 3); totals = aggregate(rows)
        write('training.json', dict(records=rows, totals=totals))
        write('selection.json', dict(setting=select(totals), training_sha256=sha(HERE / 'training.json'), rule=protocol['selection']))
    elif args.phase == 'confirm':
        committed('selection.json'); committed('training.json')
        settings = ('off', 'whole', read('selection.json')['setting'])
        rows = run(args.solver, 'confirm', data['confirm'], settings, [20000, 100000], 3)
        write('confirmation.json', dict(records=rows, totals=aggregate(rows), selection_sha256=sha(HERE / 'selection.json'),
            selection_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()))
        rows = run(args.solver, 'late', data['late'], settings, [20000], 1)
        write('late.json', dict(records=rows, totals=aggregate(rows)))
    else: verify(protocol, data)

if __name__ == '__main__': main()
