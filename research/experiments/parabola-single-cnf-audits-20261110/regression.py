"""Controls for prime routing and schema corruption using both saved cases."""
import argparse
from pathlib import Path
from check_case import HERE, CASES, source_directory, qualify, parse, save, sha, frozen_bindings


def dimacs(nv, clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    records = []
    for p, config in CASES.items():
        raw = (source_directory(p)/f'a{p}_{config["size"]}.cnf').read_bytes()
        _, schema = qualify(raw, p)
        nv, clauses = parse(raw)
        base = schema['point_base']
        altered = list(clauses)
        i = next(i for i, c in enumerate(clauses) if base+1 in c and -1 in c)
        altered[i] = tuple(4*((p-1)//2) if v == base+1 else v for v in altered[i])
        mutants = [('missing-structure', dimacs(nv, clauses[1:]), p),
                   ('extra-positive-unit', dimacs(nv, clauses+[(nv,)]), p),
                   ('selector-geometry', dimacs(nv, clauses[:-1]+[(-1, -2, -3)]), p),
                   ('point-selector-alias', dimacs(nv, altered), p),
                   ('wrong-prime-route', raw, next(q for q in CASES if q != p))]
        rejected = []
        for name, candidate, selected_p in mutants:
            try:
                qualify(candidate, selected_p)
            except (AssertionError, ValueError):
                rejected.append(name)
            else:
                raise AssertionError((p, name))
        records.append(dict(p=p, input_sha256=sha(raw), rejected=rejected))
    save(args.output, dict(cases=records, frozen_bindings=frozen_bindings(),
                          source_sha256=sha(Path(__file__).read_bytes()),
                          scope='Two real inputs, ten schema/routing corruptions. Frozen prior schema also has exhaustive small semantic controls.'))
    print('PASS both inputs and ten schema/routing negatives')


if __name__ == '__main__':
    main()
