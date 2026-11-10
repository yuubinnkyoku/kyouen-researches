"""Greedily extend repaired subsets and certify one maximal safe witness."""
import argparse
import gzip
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time
from pilot import HERE, save, sha

P = 2539


def complete_pairs(selected):
    return [i for i in range(1, (P+1)//2) if i in selected and P-i in selected]


def blocker(t, selected, incidence):
    pairs = complete_pairs(selected)
    assert len(pairs) <= 1
    if t and P-t in selected and pairs:
        a = pairs[0]
        return tuple(sorted([a, P-a, t, P-t]))
    return next((q for q in incidence[t] if all(v == t or v in selected for v in q)), None)


def extend(points, incidence, mode):
    selected = set(points)
    added = []
    while True:
        legal = [t for t in range(P) if t not in selected and blocker(t, selected, incidence) is None]
        if not legal:
            break
        empty = [t for t in legal if not t or P-t not in selected]
        choices = empty or legal
        if mode == 'ascending':
            t = min(choices)
        elif mode == 'descending':
            t = max(choices)
        else:
            def score(t):
                newly_blocked = set()
                for q in incidence[t]:
                    missing = [v for v in q if v not in selected]
                    if len(missing) == 2:
                        newly_blocked.update(v for v in missing if v != t)
                return len(newly_blocked), t
            t = min(choices, key=score)
        selected.add(t)
        added.append(t)
        assert len(selected) <= 1271 and len(complete_pairs(selected)) <= 1
    return sorted(selected), added


def validate_blockers(points, rows):
    selected = set(points)
    missing = set(range(P))-selected
    assert len(rows) == len(missing) and {t for t, q in rows} == missing
    for t, q in rows:
        assert len(q) == len(set(q)) == 4 and tuple(sorted(q)) == tuple(q)
        assert 0 <= q[0] < q[-1] < P and t in q
        assert set(q)-{t} <= selected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--repaired', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    plan = json.loads((args.saved/'plan.json').read_text())
    assert sha(raw) == plan['edge_input_sha256']
    edges = [tuple(map(int, line.split())) for line in raw.decode('ascii').splitlines()[1:]]
    incidence = [[] for _ in range(P)]
    for q in edges:
        for t in q:
            incidence[t].append(q)
    args.output.mkdir(parents=True, exist_ok=False)
    trials = []
    for model in sorted(args.repaired.glob('d*/candidate.txt')):
        tokens = list(map(int, model.read_bytes().split()))
        assert tokens[0] == P and len(tokens) == tokens[1]+2
        for mode in ('ascending', 'descending', 'blocking-degree'):
            points, added = extend(tokens[2:], incidence, mode)
            name = model.parent.name+'-'+mode
            candidate = (f'{P} {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii')
            (args.output/(name+'.txt')).write_bytes(candidate)
            trials.append(dict(name=name, size=len(points), added=added,
                               start_sha256=sha(model.read_bytes()), candidate_sha256=sha(candidate)))
            print(name, len(points), flush=True)
    best = max(trials, key=lambda r: (r['size'], r['name']))
    candidate = (args.output/(best['name']+'.txt')).read_bytes()
    (args.output/'candidate.txt').write_bytes(candidate)
    points = list(map(int, candidate.split()))[2:]
    selected = set(points)
    rows = [(t, blocker(t, selected, incidence)) for t in range(P) if t not in selected]
    assert all(q is not None for t, q in rows)
    validate_blockers(points, rows)
    blockers = (f'{P} {len(points)} {len(rows)}\n'+''.join(str(t)+' '+' '.join(map(str, q))+'\n' for t, q in rows)).encode('ascii')
    (args.output/'blockers.txt').write_bytes(blockers)
    edge_input = (f'{P} {len(rows)}\n'+''.join(' '.join(map(str, q))+'\n' for t, q in rows)).encode('ascii')
    (args.output/'blocker-edges.txt.gz').write_bytes(gzip.compress(edge_input, mtime=0))
    with tempfile.TemporaryDirectory(prefix='p2539-maximal-audit-') as directory:
        directory = Path(directory)
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        subset, ge = directory/'subset.exe', directory/'edges.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(subset)], check=True, timeout=60)
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        started = time.monotonic()
        r = subprocess.run([str(subset), '--modular-filter'], input=candidate, capture_output=True, timeout=120)
        assert r.returncode == 0, r.stdout+r.stderr
        values = list(map(int, r.stdout.split()))
        assert len(values) == 4 and values[:3] == [P, len(points), math.comb(len(points), 4)]
        ep = directory/'blockers.txt'; ep.write_bytes(edge_input)
        b = subprocess.run([str(ge), str(ep)], capture_output=True, text=True, timeout=60)
        assert b.returncode == 0 and b.stdout.strip() == f'VERIFIED_EDGES {P} {len(rows)}'
        report = dict(p=P, size=len(points), verified_safe=True, verified_inclusion_maximal=True,
             returncode=r.returncode, stdout=r.stdout.decode(), geometry_elapsed_seconds=time.monotonic()-started,
             blocker_returncode=b.returncode, blocker_stdout=b.stdout, missing_points=len(rows),
             candidate_sha256=sha(candidate), blockers_sha256=sha(blockers),
             generic_source_sha256=sha(generic.read_bytes()), wrapper_source_sha256=sha(wrapper.read_bytes()),
             source_sha256=sha(Path(__file__).read_bytes()),
             scope='A fixed safe subset and one genuine forbidden quadruple for every possible added point. Inclusion maximality is not maximum cardinality.')
    save(args.output/'verification.json', report)
    save(args.output/'trials.json', dict(trials=trials, best=best, lower_bound=len(points), upper_bound=1271,
         scope='Greedy extension trials against provided edges; only the final candidate and its complete blocker list are independently geometrically certified.'))
    print('PASS lower', len(points), 'upper 1271; maximal blockers', len(rows), flush=True)


if __name__ == '__main__':
    main()
