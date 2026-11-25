"""Test the new independent prefix meanings, corrupt schemas and geometric boundary."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from pysat.card import CardEnc, EncType
from schema import audit, counter, parse
from audit import HERE, SOURCE, ROOT, save, sha


def encode(nv, clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    cases = []
    for n in range(3, 8):
        for k in range(1, n-1):
            for signed in (False, True):
                inputs = [-i if signed and i % 2 else i for i in range(1, n+1)]
                top = n+7
                card = CardEnc.atmost(inputs, bound=k, top_id=top, encoding=EncType.seqcounter)
                labels, counts = counter(card.clauses, inputs, k, top, card.nv)
                for mask in range(1 << n):
                    bits = [bool(mask & (1 << i)) for i in range(n)]
                    values = {abs(v): bits[i] if v > 0 else not bits[i] for i, v in enumerate(inputs)}
                    values.update({v: sum(bits[:i+1]) >= j for v, (i, j) in labels.items()})
                    actual = all(any((lit > 0) == values[abs(lit)] for lit in c) for c in card.clauses)
                    assert actual == (sum(bits) <= k)
                cases.append(dict(inputs=n, bound=k, signed=signed, assignments=1 << n, rules=counts))
    raw = gzip.decompress((SOURCE/'input.cnf.gz').read_bytes())
    init = json.loads((SOURCE/'init.json').read_text())
    seed = list(map(int, (ROOT/init['seed_path']).read_bytes().split()))[2:]
    nv, clauses = parse(raw)
    edges, qualified = audit(raw, seed)
    first = qualified['geometric_clauses']+qualified['onehot_clauses']
    second = first+qualified['empty_counter_clauses']
    variants = {}
    clone = lambda: [c[:] for c in clauses]
    bad = clone(); bad[first-1] = bad[first-2][:]; variants['broken-onehot'] = bad
    bad = clone(); bad[first][0] = -bad[first][0]; variants['wrong-empty-input-polarity'] = bad
    bad = clone(); bad[second][0] = -bad[second][0]; variants['wrong-removal-polarity'] = bad
    bad = clone(); bad[first][-1] = 3807; variants['aux-selection-alias'] = bad
    overflow = next(i for i in range(first, second) if len(clauses[i]) == 2 and all(v < 0 for v in clauses[i]))
    bad = clone(); bad[overflow][-1] += 1; variants['wrong-overflow-threshold'] = bad
    bad = clone(); bad[0][0] = -bad[0][0]; variants['positive-geometric-clause'] = bad
    rejected = []
    for name, value in variants.items():
        try:
            audit(encode(nv, value), seed)
        except (AssertionError, KeyError, StopIteration):
            rejected.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    # A zero modular sum is NOT a geometric acceptance test.
    false_q = (1, 2, 4, 2532)
    assert sum(false_q) % 2539 == 0
    bad = clone()
    bad[0] = [-(t if t <= 1269 else 1269+2539-t) for t in false_q]
    false_edges, _ = audit(encode(nv, bad), seed)
    assert false_edges[0] == false_q
    wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    geometry_controls = []
    with tempfile.TemporaryDirectory(prefix='exchange-schema-controls-') as temporary:
        td = Path(temporary); exe = td/'geometry.exe'; ep = td/'edges.txt'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(exe)], check=True, timeout=60)
        for name, p, q, code in [('true-edge', 5, (1, 2, 3, 4), 0), ('modular-nonedge', 2539, false_q, 4)]:
            ep.write_text(f'{p} 1\n'+' '.join(map(str, q))+'\n', encoding='ascii')
            run = subprocess.run([str(exe), str(ep)], capture_output=True, text=True, timeout=10)
            assert run.returncode == code, (name, run)
            geometry_controls.append(dict(name=name, actual=run.returncode, expected=code))
    save(args.output, dict(counter_cases=cases, total_assignments=sum(c['assignments'] for c in cases),
                          rejected_schema_controls=rejected, geometry_controls=geometry_controls,
                          schema_source_sha256=sha((HERE/'schema.py').read_bytes()),
                          regression_source_sha256=sha(Path(__file__).read_bytes()),
                          scope='Exhaustive small prefix interpretations and corrupt-schema controls, including a modular-sum-zero nonedge. No general checker soundness proof.'))
    print('PASS', sum(c['assignments'] for c in cases), 'prefix assignments;', len(rejected), 'schema rejections; true/false geometry', flush=True)


if __name__ == '__main__':
    main()
