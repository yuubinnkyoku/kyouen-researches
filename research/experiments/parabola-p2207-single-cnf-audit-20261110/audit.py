"""Audit a saved p2207 upper-bound CNF and DRAT via geometry, RUP and LRAT."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from schema import audit as audit_schema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SAVED = HERE.parent/'parabola-p2207-no-equality-witness-20261107/output/cert-2207-1105'
TRIM = HERE.parent/'parabola-drat-trim-20261109'
FIXED_SHA = 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'
PROOF_SHA = 'f0ce140db899e4c9009fced1bc38aa753315d71bd8eb9f1498db0c74ad77a7ea'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2)+'\n')


def run(command, timeout):
    started = time.monotonic()
    try:
        r = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return dict(returncode=r.returncode, stdout=r.stdout, stderr=r.stderr,
                    elapsed_seconds=time.monotonic()-started, timed_out=False)
    except subprocess.TimeoutExpired as exc:
        decode = lambda v: v.decode(errors='replace') if isinstance(v, bytes) else v or ''
        return dict(returncode=None, stdout=decode(exc.stdout), stderr=decode(exc.stderr),
                    elapsed_seconds=time.monotonic()-started, timed_out=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()
    assert args.timeout > 0
    cnf = (SAVED/'a2207_1105.cnf').read_bytes()
    edges, schema = audit_schema(cnf)
    assert (schema['variables'], schema['clauses'], len(edges)) == (7720, 50616, 31868)
    original = gzip.decompress((SAVED/'a2207_1105.drat.gz').read_bytes())
    assert sha(original) == PROOF_SHA and original.count(b'\n') == 497179
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    for name, digest in provenance['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == digest
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA
    args.output.mkdir(parents=True, exist_ok=False)
    packed = gzip.compress(cnf, mtime=0)
    (args.output/'input.cnf.gz').write_bytes(packed)
    edge_input = (f'2207 {len(edges)}\n'+''.join(' '.join(map(str, q))+'\n' for q in edges)).encode('ascii')
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(edge_input, mtime=0))
    schema.update(input_sha256=sha(cnf), source_cnf_path=(SAVED/'a2207_1105.cnf').relative_to(ROOT).as_posix(),
                  original_drat_sha256=sha(original), original_drat_lines=original.count(b'\n'),
                  original_drat_path=(SAVED/'a2207_1105.drat.gz').relative_to(ROOT).as_posix(),
                  edge_input_sha256=sha(edge_input), driver_source_sha256=sha(Path(__file__).read_bytes()),
                  schema_source_sha256=sha((HERE/'schema.py').read_bytes()),
                  scope='Every safe 1105-set extends to these structural clauses; residual clauses must additionally pass integer geometry. No completeness of the supplied edge set is required for UNSAT exclusion.')
    save(args.output/'schema.json', schema)
    with tempfile.TemporaryDirectory(prefix='p2207-single-cnf-') as directory:
        directory = Path(directory)
        cp, pp, ep = directory/'input.cnf', directory/'proof.drat', directory/'edges.txt'
        cp.write_bytes(cnf); pp.write_bytes(original); ep.write_bytes(edge_input)
        ge, trim, lrat = directory/'geometry.exe', directory/'trim.exe', directory/'lrat.exe'
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        geometry = run([str(ge), str(ep)], 60)
        geometry.update(wrapper_source_sha256=sha(wrapper.read_bytes()), generic_source_sha256=sha(generic.read_bytes()),
                        edge_input_sha256=sha(edge_input), binary_sha256=sha(ge.read_bytes()))
        save(args.output/'geometry.json', geometry)
        assert geometry['returncode'] == 0 and geometry['stdout'].strip() == 'VERIFIED_EDGES 2207 31868'
        subprocess.run(['gcc', str(TRIM/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(trim)], check=True, timeout=60)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(lrat)], check=True, timeout=60)
        core = (args.output/'core.lrat').resolve()
        result = run([str(trim), str(cp), str(pp), '-U', '-t', str(args.timeout), '-L', str(core)], args.timeout+30)
        result.update(input_sha256=sha(cnf), original_drat_sha256=sha(original),
                      checker_source_sha256=provenance['files']['drat-trim.c'],
                      checker_binary_sha256=sha(trim.read_bytes()), method='Pinned DRAT-trim -U; RUP-only backward check',
                      verified=result['returncode'] == 0 and 's VERIFIED' in result['stdout'].splitlines())
        save(args.output/'rup.json', result)
        print('RUP', result['verified'], flush=True)
        if not result['verified']:
            raise SystemExit(1)
        raw = core.read_bytes()
        (args.output/'core.lrat.gz').write_bytes(gzip.compress(raw, mtime=0))
        checked = run([str(lrat), str(cp), str(core)], args.timeout)
        checked.update(input_sha256=sha(cnf), lrat_raw_sha256=sha(raw),
                       checker_source_sha256=FIXED_SHA, checker_binary_sha256=sha(lrat.read_bytes()),
                       verified=checked['returncode'] == 0 and 'c VERIFIED' in checked['stdout'].splitlines())
        save(args.output/'lrat.json', checked)
        manifest = dict(input_path=(args.output/'input.cnf.gz').resolve().relative_to(ROOT).as_posix(),
                        input_raw_sha256=sha(cnf), input_gzip_sha256=sha(packed),
                        lrat_path=(args.output/'core.lrat.gz').resolve().relative_to(ROOT).as_posix(),
                        lrat_raw_sha256=sha(raw), lrat_gzip_sha256=sha((args.output/'core.lrat.gz').read_bytes()),
                        lrat_raw_bytes=len(raw), lrat_lines=raw.count(b'\n'), original_drat_sha256=PROOF_SHA,
                        original_drat_path=schema['original_drat_path'], fixed_lrat_source_sha256=FIXED_SHA,
                        schema_geometry_rup_lrat_verified=checked['verified'],
                        scope='Finite upper bound 1104 from faithful class (1,1,0), sound provided edges and two separate proof checkers; no new SAT search or general verifier soundness theorem.')
        save(args.output/'manifest.json', manifest)
        print('LRAT', checked['verified'], 'bytes', len(raw), flush=True)
        if not checked['verified']:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
