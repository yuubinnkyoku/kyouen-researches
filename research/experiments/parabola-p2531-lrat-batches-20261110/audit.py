"""Reusable, case-isolated parallel LRAT audits with immutable prior coverage."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRIM = HERE.parent/'parabola-drat-trim-20261109'
GEN = HERE.parent/'structural-lemmas-2026-10-02/checks/parabola_half_bound.py'
SCHEMA = HERE.parent/'parabola-p2531-lrat-20261110/verify_saved.py'
FIXED_SHA = 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2)+'\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_ds(text):
    values = []
    for group in text.split(','):
        if '-' in group:
            lo, hi = map(int, group.split('-'))
            assert lo <= hi
            values.extend(range(lo,hi+1))
        else:
            values.append(int(group))
    return values


def validate_plan(prior, ds):
    old = set(prior['verified_d_union'])
    assert prior['p'] == 2531 and len(old) == prior['verified_union_count']
    assert all(1 <= d <= 1265 for d in old)
    assert ds and len(ds) == len(set(ds)) and all(1 <= d <= 1265 and d not in old for d in ds)
    return old


def run(command, timeout):
    started = time.monotonic()
    try:
        r = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return dict(returncode=r.returncode, stdout=r.stdout, stderr=r.stderr,
                    seconds=time.monotonic()-started, timed_out=False)
    except subprocess.TimeoutExpired as exc:
        decode = lambda v: v.decode(errors='replace') if isinstance(v,bytes) else v or ''
        return dict(returncode=None, stdout=decode(exc.stdout), stderr=decode(exc.stderr),
                    seconds=time.monotonic()-started, timed_out=True)


def worker(task):
    d, destination, edges, binaries, budget, metadata = task
    out = Path(destination)
    out.mkdir()
    assert sha(Path(__file__).read_bytes()) == metadata['source_sha256']
    sys.path.insert(0,str(GEN.parent))
    generator = load_module('pair_generator',GEN)
    schema = load_module('independent_projection',SCHEMA)
    clauses = sorted({tuple(sorted(c)) for c in generator.clauses_for_pair(2531,edges,d)})
    assert clauses == schema.project(edges,d)
    cnf = schema.dimacs(clauses)
    (out/'input.cnf.gz').write_bytes(gzip.compress(cnf,compresslevel=1,mtime=0))
    record = dict(metadata,p=2531,d=d,variables=1265,clauses=len(clauses),input_sha256=sha(cnf),
                  conflict_budget=budget,verified=False,independent_projection_schema_equal=True,
                  original_drat_distribution='local gzip retained; adopted CNF and LRAT distributed')
    save(out/'init.json',record)
    from pysat.solvers import Cadical195
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(budget)
        answer = solver.solve_limited()
        proof = solver.get_proof() if answer is False else None
        statistics = solver.accum_stats()
    record.update(solver='UNSAT' if answer is False else 'SAT' if answer is True else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started,statistics=statistics)
    if proof:
        original = ('\n'.join(proof)+'\n').encode('ascii')
        (out/'proof.drat.gz').write_bytes(gzip.compress(original,compresslevel=1,mtime=0))
        record.update(proof_sha256=sha(original),proof_lines=len(proof))
        with tempfile.TemporaryDirectory(prefix=f'p2531-case-{d}-') as directory:
            directory = Path(directory)
            cp, pp = directory/'input.cnf', directory/'proof.drat'
            cp.write_bytes(cnf)
            pp.write_bytes(original)
            core = (out/'core.lrat').resolve()
            trimmed = run([binaries['trim'],str(cp),str(pp),'-U','-t','90','-L',str(core)],100)
            trimmed['verified'] = trimmed['returncode']==0 and 's VERIFIED' in trimmed['stdout'].splitlines()
            record['trim'] = trimmed
            if trimmed['verified'] and core.exists():
                raw = core.read_bytes()
                (out/'core.lrat.gz').write_bytes(gzip.compress(raw,compresslevel=1,mtime=0))
                checked = run([binaries['lrat'],str(cp),str(core)],90)
                checked['verified'] = checked['returncode']==0 and 'c VERIFIED' in checked['stdout'].splitlines()
                record.update(lrat=checked,lrat_sha256=sha(raw),lrat_lines=raw.count(b'\n'),
                              lrat_raw_bytes=len(raw),verified=checked['verified'])
    save(out/'result.json',record)
    return record


def collect(output):
    output = Path(output)
    plan = json.loads((output/'plan.json').read_text())
    old = set(plan['prior_verified_d'])
    new, pending, failed = set(), [], []
    for d in plan['requested_d']:
        path = output/f'd{d}/result.json'
        if not path.exists():
            pending.append(d)
            continue
        r = json.loads(path.read_text())
        assert r['d']==d and r['source_sha256']==plan['source_sha256']
        if r['verified'] and r.get('solver')=='UNSAT' and r['lrat']['returncode']==0:
            new.add(d)
        else:
            failed.append(d)
    result = dict(p=2531,h=1265,prior_coverage_path=plan['prior_coverage_path'],
                  prior_coverage_sha256=plan['prior_coverage_sha256'],prior_verified_d=sorted(old),
                  requested_d=plan['requested_d'],new_lrat_verified_d=sorted(new),overlap=sorted(old&new),
                  verified_d_union=sorted(old|new),verified_union_count=len(old|new),remaining=1265-len(old|new),
                  pending_d=pending,failed_or_unknown_d=failed,source_sha256=plan['source_sha256'],
                  scope='Mixed-method coverage chain. Only successful independent LRAT checks enter the union; no all-d completion claim.')
    assert not old&new
    save(output/'coverage.json',result)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prior',type=Path)
    ap.add_argument('--edges',type=Path)
    ap.add_argument('--ds')
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--budget',type=int,default=100000)
    ap.add_argument('--collect-only',action='store_true')
    args = ap.parse_args()
    if args.collect_only:
        print(json.dumps(collect(args.output)),flush=True)
        return
    assert args.prior and args.edges and args.ds and 1<=args.workers<=4 and args.budget>0
    prior_raw = args.prior.read_bytes()
    old = validate_plan(json.loads(prior_raw),parse_ds(args.ds))
    ds = parse_ds(args.ds)
    args.output.mkdir(parents=True,exist_ok=False)
    raw = args.edges.read_bytes()
    edges = [tuple(map(int,row.split())) for row in raw.decode('ascii').splitlines()]
    edge_input = f'2531 {len(edges)}\n'.encode('ascii')+raw
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(edge_input,compresslevel=1,mtime=0))
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    assert all(sha((TRIM/'vendor'/name).read_bytes())==value for name,value in provenance['files'].items())
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes())==FIXED_SHA
    metadata = dict(source_sha256=sha(Path(__file__).read_bytes()),generator_sha256=sha(GEN.read_bytes()),
                    independent_schema_source_sha256=sha(SCHEMA.read_bytes()),edge_input_sha256=sha(edge_input),
                    trim_source_sha256=provenance['files']['drat-trim.c'],fixed_lrat_source_sha256=FIXED_SHA,
                    python_sat=importlib.metadata.version('python-sat'))
    plan = dict(metadata,p=2531,prior_coverage_path=args.prior.resolve().relative_to(ROOT).as_posix(),
                prior_coverage_sha256=sha(prior_raw),prior_verified_d=sorted(old),requested_d=sorted(ds),
                workers=args.workers,conflict_budget=args.budget)
    save(args.output/'plan.json',plan)
    with tempfile.TemporaryDirectory(prefix='p2531-batch-binaries-') as directory:
        directory = Path(directory)
        trim, lr, ge = directory/'trim.exe',directory/'lrat.exe',directory/'geometry.exe'
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(trim)],check=True,timeout=60)
        subprocess.run(['gcc',str(fixed),*provenance['build_flags'],'-DLONGTYPE','-o',str(lr)],check=True,timeout=60)
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(ge)],check=True,timeout=60)
        edge_path = directory/'edges.txt'
        edge_path.write_bytes(edge_input)
        geometry = run([str(ge),str(edge_path)],60)
        assert geometry['returncode']==0 and geometry['stdout'].strip()==f'VERIFIED_EDGES 2531 {len(edges)}'
        geometry.update(input_sha256=sha(edge_input),edge_count=len(edges),wrapper_sha256=sha(wrapper.read_bytes()),
                        generic_sha256=sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes()))
        save(args.output/'geometry.json',geometry)
        metadata.update(trim_binary_sha256=sha(trim.read_bytes()),lrat_binary_sha256=sha(lr.read_bytes()))
        binaries = dict(trim=str(trim),lrat=str(lr))
        tasks = [(d,str(args.output/f'd{d}'),edges,binaries,args.budget,metadata) for d in ds]
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(worker,task):task[0] for task in tasks}
            for future in as_completed(futures):
                d = futures[future]
                try:
                    r = future.result()
                    print(f"d={d} solver={r['solver']} verified={r['verified']}",flush=True)
                except Exception:
                    save(args.output/f'd{d}-failure.json',dict(d=d,traceback=traceback.format_exc()))
                    print(f'd={d} worker failure; raw files retained',flush=True)
    result = collect(args.output)
    print(f"verified_union={result['verified_union_count']} pending={result['pending_d']} failed={result['failed_or_unknown_d']}",flush=True)


if __name__=='__main__':
    multiprocessing.freeze_support()
    main()
