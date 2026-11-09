"""Produce blockers as proposals, then check explicit quads without any CNF."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000'
BASE = HERE.parent/'parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf'
spec = importlib.util.spec_from_file_location('integer_geometry', HERE.parent/'parabola-local-repair-20261109/verify.py')
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    raw = (SOURCE/'candidate.txt').read_bytes()
    values = list(map(int, raw.split()))
    p, n = values[:2]
    selected = set(values[2:])
    assert p == 2647 and n == len(selected) == 1302 and sorted(selected) == values[2:]
    safe = json.loads((SOURCE/'geometry.json').read_text())
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert safe['returncode'] == 0 and safe['candidate_input_sha256'] == sha(raw)
    assert safe['verifier_source_sha256'] == sha(generic.read_bytes())
    base = BASE.read_bytes()
    assert sha(base) == '0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3'
    proposals = defaultdict(list)
    for row in base.decode('ascii').splitlines():
        if not row or row[0] in 'cp':
            continue
        required = {lit if lit > 0 else p+lit for lit in map(int, row.split()[:-1])}
        missing = required-selected
        if len(missing) == 1:
            proposals[next(iter(missing))].append(required)
    fixed = {0, 1323, 1324}
    entries = []
    for t in sorted(set(range(p))-selected):
        quad = None
        if p-t in selected:
            quad = sorted({t, p-t, 1323, 1324})
            assert len(quad) == 4
        else:
            for required in proposals[t]:
                pool = (required | fixed)-{t}
                assert pool <= selected
                for triple in combinations(sorted(pool), 3):
                    candidate = sorted((t, *triple))
                    coords = [(v, v*v % p) for v in candidate]
                    if geometry.determinant(coords) == 0:
                        quad = candidate
                        break
                if quad is not None:
                    break
        assert quad is not None, f'no explicit blocker found for {t}'
        assert geometry.determinant([(v, v*v % p) for v in quad]) == 0
        entries.append([t, *quad])
    text = f'{p} {len(entries)}\n'+''.join(' '.join(map(str, row))+'\n' for row in entries)
    certificate = args.output/'blockers.txt'
    certificate.write_text(text, encoding='ascii', newline='\n')
    controls = []
    with tempfile.TemporaryDirectory(prefix='blocker-check-') as td:
        td = Path(td)
        exe = td/'verify.exe'
        subprocess.run(['g++', '-std=c++17', '-O2', str(HERE.parent/'parabola-maximal-1300-20261109/verify_blockers.cpp'), '-o', str(exe)], check=True, timeout=60)
        checked = subprocess.run([str(exe), str(SOURCE/'candidate.txt'), str(certificate)], capture_output=True, text=True, timeout=15)
        assert checked.returncode == 0 and checked.stdout.strip() == 'VERIFIED_BLOCKERS 2647 1302 1345'
        bad_rows = [list(r) for r in entries]
        bad_rows[1] = list(bad_rows[0])
        malformed = [('missing-row', text.rsplit('\n', 2)[0]+'\n'),
                     ('trailing-data', text+'1\n'),
                     ('wrong-prime', text.replace('2647 ', '2649 ', 1)),
                     ('duplicate-added', f'{p} {len(entries)}\n'+''.join(' '.join(map(str, r))+'\n' for r in bad_rows))]
        changed = [list(r) for r in entries]
        changed[0][0] = min(selected)
        malformed.append(('selected-added', f'{p} {len(entries)}\n'+''.join(' '.join(map(str, r))+'\n' for r in changed)))
        changed = [list(r) for r in entries]
        changed[0][1:] = changed[0][1:][::-1]
        malformed.append(('unsorted-quad', f'{p} {len(entries)}\n'+''.join(' '.join(map(str, r))+'\n' for r in changed)))
        t = entries[0][0]
        nonedge = next(sorted((t, *triple)) for triple in combinations(sorted(selected)[:8], 3)
                       if geometry.determinant([(v, v*v % p) for v in (t, *triple)]) != 0)
        changed = [list(r) for r in entries]
        changed[0][1:] = nonedge
        malformed.append(('nonedge', f'{p} {len(entries)}\n'+''.join(' '.join(map(str, r))+'\n' for r in changed)))
        for name, content in malformed:
            path = td/'invalid.txt'
            path.write_text(content, encoding='ascii', newline='\n')
            run = subprocess.run([str(exe), str(SOURCE/'candidate.txt'), str(path)], capture_output=True, text=True, timeout=15)
            assert run.returncode != 0, name
            controls.append(dict(name=name, returncode=run.returncode))
        result = dict(worker_source_sha256=sha(Path(__file__).read_bytes()), p=p, size=n, outside_points=p-n, explicit_blockers=len(entries),
                      candidate_input_sha256=sha(raw), certificate_sha256=sha(certificate.read_bytes()),
                      base_geometry_receipt_sha256=sha((SOURCE/'geometry.json').read_bytes()),
                      checker_source_sha256=sha((HERE.parent/'parabola-maximal-1300-20261109/verify_blockers.cpp').read_bytes()),
                      included_geometry_sha256=sha(generic.read_bytes()), checker_binary_sha256=sha(exe.read_bytes()),
                      returncode=checked.returncode, stdout=checked.stdout, rejected_controls=controls,
                      inclusion_maximal=True,
                      scope='Specific saved 1302-point safe set is inclusion-maximal, not a maximum-size claim. Checker reads no CNF.')
    (args.output/'audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
