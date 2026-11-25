"""Audit previously uncovered equality parameters using explicit LRAT hints."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRIM = HERE.parent/'parabola-drat-trim-20261109'
GEN = HERE.parent/'structural-lemmas-2026-10-02/checks/parabola_half_bound.py'
BASELINE = HERE.parent/'parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531_34249932790a9e9d.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def run(command, timeout):
    start = time.monotonic()
    try:
        value = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return dict(returncode=value.returncode, stdout=value.stdout, stderr=value.stderr,
                    seconds=time.monotonic()-start, timed_out=False)
    except subprocess.TimeoutExpired as exc:
        decode = lambda v: v.decode(errors='replace') if isinstance(v, bytes) else v or ''
        return dict(returncode=None, stdout=decode(exc.stdout), stderr=decode(exc.stderr),
                    seconds=time.monotonic()-start, timed_out=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--ds', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--budget', type=int, default=100000)
    args = ap.parse_args()
    p, h = 2531, 1265
    ds = list(map(int, args.ds.split(',')))
    baseline_raw = BASELINE.read_bytes()
    baseline = json.loads(baseline_raw)
    assert baseline['checker_source_sha256'] == '34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b'
    old = {r['d'] for r in baseline['records'] if r['verified'] and r['checker_rc'] == 0 and r['solver'] == 'UNSAT'}
    assert len(old) == 143 and len(set(ds)) == len(ds) and all(1 <= d <= h and d not in old for d in ds)
    args.output.mkdir(parents=True, exist_ok=False)
    edge_raw = args.edges.read_bytes()
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()]
    assert all(len(q) == 4 and tuple(sorted(set(q))) == q for q in edges)
    edge_input = f'{p} {len(edges)}\n'.encode('ascii')+edge_raw
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(edge_input, compresslevel=1, mtime=0))
    spec = importlib.util.spec_from_file_location('clause_generator', GEN)
    sys.path.insert(0, str(GEN.parent))
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    for name, expected in provenance['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == expected
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'
    records = []
    with tempfile.TemporaryDirectory(prefix='p2531-lrat-') as directory:
        directory = Path(directory)
        edge_path = directory/'edges.txt'
        edge_path.write_bytes(edge_input)
        geometric = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        ge, trim, lr = directory/'edges.exe', directory/'trim.exe', directory/'lrat.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(geometric), '-o', str(ge)], check=True, timeout=60)
        geometry = run([str(ge), str(edge_path)], 60)
        assert geometry['returncode'] == 0 and geometry['stdout'].strip() == f'VERIFIED_EDGES {p} {len(edges)}'
        geometry.update(input_sha256=sha(edge_input), edge_count=len(edges), wrapper_sha256=sha(geometric.read_bytes()),
                        generic_sha256=sha(generic.read_bytes()), binary_sha256=sha(ge.read_bytes()))
        save(args.output/'geometry.json', geometry)
        subprocess.run(['gcc', str(TRIM/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(trim)], check=True, timeout=60)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(lr)], check=True, timeout=60)
        for d in ds:
            out = args.output/f'd{d}'
            out.mkdir()
            clauses = sorted({tuple(sorted(c)) for c in generator.clauses_for_pair(p, edges, d)})
            # Separately project each forbidden conjunction: low is variable false,
            # high true; the fixed origin/complete pair are always selected.
            manual = set()
            for q in edges:
                literals = {(-min(t,p-t) if t > h else min(t,p-t))
                            for t in q if t and min(t,p-t) != d}
                if any(-v in literals for v in literals):
                    continue
                manual.add(tuple(sorted(literals)))
            assert set(clauses) == manual
            cnf = (f'p cnf {h} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
            (out/'input.cnf.gz').write_bytes(gzip.compress(cnf, compresslevel=1, mtime=0))
            record = dict(p=p, d=d, variables=h, clauses=len(clauses), input_sha256=sha(cnf),
                          edge_input_sha256=sha(edge_input), generator_sha256=sha(GEN.read_bytes()),
                          source_sha256=sha(Path(__file__).read_bytes()), independent_projection_schema_equal=True,
                          conflict_budget=args.budget, python_sat=importlib.metadata.version('python-sat'),
                          verified=False)
            save(out/'init.json', record)
            started = time.monotonic()
            with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
                solver.conf_budget(args.budget)
                answer = solver.solve_limited()
                proof = solver.get_proof() if answer is False else None
                stats = solver.accum_stats()
            record.update(solver='UNSAT' if answer is False else 'SAT' if answer is True else 'UNKNOWN',
                          solve_seconds=time.monotonic()-started, statistics=stats)
            if proof:
                proof_raw = ('\n'.join(proof)+'\n').encode('ascii')
                (out/'proof.drat.gz').write_bytes(gzip.compress(proof_raw, compresslevel=1, mtime=0))
                record.update(proof_sha256=sha(proof_raw), proof_lines=len(proof))
                cp, pp = directory/'input.cnf', directory/'proof.drat'
                cp.write_bytes(cnf)
                pp.write_bytes(proof_raw)
                core = (out/'core.lrat').resolve()
                trimmed = run([str(trim), str(cp), str(pp), '-U', '-t', '45', '-L', str(core)], 55)
                trimmed['verified'] = trimmed['returncode'] == 0 and 's VERIFIED' in trimmed['stdout'].splitlines()
                record['trim'] = trimmed
                if trimmed['verified'] and core.exists():
                    raw = core.read_bytes()
                    (out/'core.lrat.gz').write_bytes(gzip.compress(raw, compresslevel=1, mtime=0))
                    checked = run([str(lr), str(cp), str(core)], 45)
                    checked['verified'] = checked['returncode'] == 0 and 'c VERIFIED' in checked['stdout'].splitlines()
                    record.update(lrat=checked, lrat_sha256=sha(raw), lrat_lines=raw.count(b'\n'),
                                  lrat_raw_bytes=len(raw), verified=checked['verified'])
            record.update(trim_source_sha256=provenance['files']['drat-trim.c'],
                          fixed_lrat_source_sha256=sha(fixed.read_bytes()), trim_binary_sha256=sha(trim.read_bytes()),
                          lrat_binary_sha256=sha(lr.read_bytes()))
            save(out/'result.json', record)
            records.append(record)
            print(f"d={d} solver={record['solver']} verified={record['verified']}", flush=True)
        new = {r['d'] for r in records if r['verified']}
        coverage = dict(p=p, h=h, baseline_sha256=sha(baseline_raw), baseline_fixed_d=sorted(old),
                        new_lrat_verified_d=sorted(new), overlap=sorted(old & new), verified_d_union=sorted(old|new),
                        verified_union_count=len(old|new), remaining=h-len(old|new),
                        source_sha256=sha(Path(__file__).read_bytes()),
                        scope='Mixed-method union of fixed K0707-checker receipts and new independent LRAT checks. Not a completed all-d audit.')
        save(args.output/'coverage.json', coverage)


if __name__ == '__main__':
    main()
