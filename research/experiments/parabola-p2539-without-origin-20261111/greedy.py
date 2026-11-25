"""Delete the origin and extend without reinserting it; certify any best witness."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-p2539-pair-pilot-20261110'
sys.path.insert(0, str(PRIOR))
from augment import blocker, complete_pairs


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    seed_raw = args.seed.read_bytes()
    tokens = list(map(int, seed_raw.split()))
    assert tokens[:2] == [2539, 1258] and len(tokens) == 1260 and len(set(tokens[2:])) == 1258
    assert sha(seed_raw) == '454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'
    seed = set(tokens[2:]); assert 0 in seed
    edge_raw = gzip.decompress(args.edges.read_bytes())
    assert sha(edge_raw) == '30e5d500f658a7a245fdff3e5c7830dc62b376632f2a6c1e75dea08552671dff'
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    incidence = [[] for _ in range(2539)]
    for q in edges:
        for t in q:
            incidence[t].append(q)
    args.output.mkdir(parents=True, exist_ok=False)
    save(args.output/'plan.json', dict(seed_sha256=sha(seed_raw), edge_input_sha256=sha(edge_raw),
         source_sha256=sha(Path(__file__).read_bytes()), helper_source_sha256=sha((PRIOR/'augment.py').read_bytes()),
         scope='Remove parameter0 and greedily add only nonzero parameters. Search edges propose witnesses; full geometry decides safety.'))
    trials = []
    for mode in ('ascending', 'descending', 'blocking-degree'):
        selected = seed-{0}; added = []
        while True:
            legal = [t for t in range(1, 2539) if t not in selected and blocker(t, selected, incidence) is None]
            if not legal:
                break
            if mode == 'ascending':
                t = min(legal)
            elif mode == 'descending':
                t = max(legal)
            else:
                def score(t):
                    disabled = set()
                    for q in incidence[t]:
                        missing = [v for v in q if v not in selected]
                        if len(missing) == 2:
                            disabled.update(v for v in missing if v != t)
                    return len(disabled), t
                t = min(legal, key=score)
            selected.add(t); added.append(t)
            assert 0 not in selected and len(complete_pairs(selected)) <= 1 and len(selected) <= 1270
        raw = (f'2539 {len(selected)}\n'+' '.join(map(str, sorted(selected)))+'\n').encode('ascii')
        (args.output/(mode+'.txt')).write_bytes(raw)
        trials.append(dict(mode=mode, size=len(selected), added=added, candidate_sha256=sha(raw)))
        print(mode, len(selected), 'added', added, flush=True)
    best = max(trials, key=lambda r: (r['size'], r['mode']))
    candidate = (args.output/(best['mode']+'.txt')).read_bytes()
    (args.output/'candidate.txt').write_bytes(candidate)
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-without-origin-') as temporary:
        exe = Path(temporary)/'geometry.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(exe)], check=True, timeout=60)
        r = subprocess.run([str(exe), '--modular-filter'], input=candidate, capture_output=True, timeout=120)
        assert r.returncode == 0 and list(map(int, r.stdout.split()))[:3] == [2539, best['size'], math.comb(best['size'], 4)]
    save(args.output/'summary.json', dict(trials=trials, best=best, independently_safe=True,
         geometry_returncode=r.returncode, geometry_stdout=r.stdout.decode(),
         generic_source_sha256=sha(generic.read_bytes()),
         scope='Only the best saved point set is independently geometrically verified. Neither maximum nor maximality is inferred.'))
    print('GEOMETRY PASS', best['size'], flush=True)


if __name__ == '__main__':
    main()
