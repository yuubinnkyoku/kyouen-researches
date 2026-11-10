"""Check a frozen local-exchange CNF and its saved DRAT, without SAT search."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from schema import audit as qualify, SEED_SHA

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE.parent/'parabola-p2539-exchange-20261110/output/target1259-remove4'
TRIM = HERE.parent/'parabola-drat-trim-20261109'
FIXED_SHA = 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def run(cmd, timeout):
    started = time.monotonic()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return dict(returncode=r.returncode, stdout=r.stdout, stderr=r.stderr,
                    timed_out=False, elapsed_seconds=time.monotonic()-started)
    except subprocess.TimeoutExpired as exc:
        dec = lambda x: x.decode(errors='replace') if isinstance(x, bytes) else x or ''
        return dict(returncode=None, stdout=dec(exc.stdout), stderr=dec(exc.stderr),
                    timed_out=True, elapsed_seconds=time.monotonic()-started)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=int, default=120)
    args = ap.parse_args()
    assert args.timeout > 0
    cnf = gzip.decompress((SOURCE/'input.cnf.gz').read_bytes())
    result = json.loads((SOURCE/'result.json').read_text())
    proof = gzip.decompress((SOURCE/'proof.drat.gz').read_bytes())
    assert sha(cnf) == result['input_sha256']
    assert sha(proof) == result['proof_sha256'] and proof.count(b'\n') == result['proof_lines'] == 228249
    seed_path = ROOT/result['seed_path']
    seed_raw = seed_path.read_bytes()
    assert sha(seed_raw) == SEED_SHA == result['seed_sha256']
    tokens = list(map(int, seed_raw.split()))
    assert tokens[:2] == [2539, 1258] and len(tokens) == 1260
    edges, schema = qualify(cnf, tokens[2:])
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
    raw_edges = (f'2539 {len(edges)}\n'+''.join(' '.join(map(str, q))+'\n' for q in edges)).encode('ascii')
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(raw_edges, mtime=0))
    schema.update(input_sha256=sha(cnf), seed_sha256=SEED_SHA, edge_input_sha256=sha(raw_edges),
                  schema_source_sha256=sha((HERE/'schema.py').read_bytes()), driver_source_sha256=sha(Path(__file__).read_bytes()),
                  original_drat_path=(SOURCE/'proof.drat.gz').relative_to(ROOT).as_posix(),
                  original_drat_sha256=sha(proof), original_drat_lines=proof.count(b'\n'))
    save(args.output/'schema.json', schema)
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    for name, digest in provenance['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == digest
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA
    with tempfile.TemporaryDirectory(prefix='p2539-exchange-proof-') as temporary:
        td = Path(temporary)
        cp, pp, ep = td/'input.cnf', td/'proof.drat', td/'edges.txt'
        cp.write_bytes(cnf); pp.write_bytes(proof); ep.write_bytes(raw_edges)
        ge, trim, lr = td/'geometry.exe', td/'trim.exe', td/'lrat.exe'
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        checked = run([str(ge), str(ep)], 60)
        checked.update(edge_input_sha256=sha(raw_edges), wrapper_source_sha256=sha(wrapper.read_bytes()),
                       generic_source_sha256=sha(generic.read_bytes()))
        save(args.output/'geometry.json', checked)
        assert checked['returncode'] == 0 and checked['stdout'].strip() == f'VERIFIED_EDGES 2539 {len(edges)}'
        subprocess.run(['gcc', str(TRIM/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(trim)], check=True, timeout=60)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(lr)], check=True, timeout=60)
        core = (args.output/'core.lrat').resolve()
        rup = run([str(trim), str(cp), str(pp), '-U', '-t', str(args.timeout), '-L', str(core)], args.timeout+30)
        rup.update(verified=rup['returncode'] == 0 and 's VERIFIED' in rup['stdout'].splitlines(),
                   input_sha256=sha(cnf), original_drat_sha256=sha(proof),
                   checker_source_sha256=provenance['files']['drat-trim.c'])
        save(args.output/'rup.json', rup)
        print('RUP', rup['verified'], flush=True)
        assert rup['verified']
        raw = core.read_bytes()
        (args.output/'core.lrat.gz').write_bytes(gzip.compress(raw, compresslevel=1, mtime=0))
        lrat = run([str(lr), str(cp), str(core)], args.timeout)
        lrat.update(verified=lrat['returncode'] == 0 and 'c VERIFIED' in lrat['stdout'].splitlines(),
                    input_sha256=sha(cnf), lrat_raw_sha256=sha(raw), checker_source_sha256=FIXED_SHA)
        save(args.output/'lrat.json', lrat)
        print('LRAT', lrat['verified'], flush=True)
        assert lrat['verified']
        save(args.output/'manifest.json', dict(p=2539, d=6, excluded_size_at_least=1259, max_removed=4,
             seed_sha256=SEED_SHA, input_sha256=sha(cnf), lrat_raw_sha256=sha(raw),
             lrat_gzip_sha256=sha((args.output/'core.lrat.gz').read_bytes()), lrat_lines=raw.count(b'\n'),
             schema_geometry_rup_lrat_verified=True,
             schema_source_sha256=schema['schema_source_sha256'], driver_source_sha256=sha(Path(__file__).read_bytes()),
             fixed_lrat_source_sha256=FIXED_SHA,
             scope='No safe set of size at least1259 retaining 0,6,2533 can delete at most4 points from the fixed 1258 witness. This is a local exclusion, not a global A(2539) upper bound.'))


if __name__ == '__main__':
    main()
