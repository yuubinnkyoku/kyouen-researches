"""Qualify saved h+2 CNFs with the frozen independent schema and two checkers."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FROZEN = HERE.parent/'parabola-p2207-single-cnf-audit-20261110'
sys.path.insert(0, str(FROZEN))
from audit import sha, save, run, TRIM, FIXED_SHA
from schema import audit as audit_schema, parse

CASES = {
    2531: dict(size=1267, variables=8854, clauses=59662, edges=38160, lines=190979,
               proof_sha='4cfc01c9297c19857042b92ec7b0a55331041c9101bf1174c0fc3c27aed17b4e'),
    3251: dict(size=1627, variables=11374, clauses=87888, edges=60266, lines=229866,
               proof_sha='34106047c97238641a1d57487a78a36f1c7b403a1a2f8d14f9abba0408eb4f13'),
}


def source_directory(p):
    return HERE.parent/'parabola-p2207-no-equality-witness-20261107/output'/f'cert-{p}-{CASES[p]["size"]}'


def qualify(raw, p):
    expected = CASES[p]
    edges, schema = audit_schema(raw, p)
    assert (schema['variables'], schema['clauses'], len(edges)) == (
        expected['variables'], expected['clauses'], expected['edges'])
    return edges, schema


def edge_bytes(p, edges):
    return (f'{p} {len(edges)}\n'+''.join(' '.join(map(str, q))+'\n' for q in edges)).encode('ascii')


def frozen_bindings():
    prior = json.loads((FROZEN/'output/schema.json').read_text())
    regression = json.loads((FROZEN/'output/regression.json').read_text())
    digest = sha((FROZEN/'schema.py').read_bytes())
    assert digest == prior['schema_source_sha256'] == regression['schema_source_sha256']
    assert sha((FROZEN/'audit.py').read_bytes()) == prior['driver_source_sha256']
    return dict(schema_source_sha256=digest, helper_source_sha256=prior['driver_source_sha256'],
                prior_semantics_regression_sha256=sha((FROZEN/'output/regression.json').read_bytes()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--p', type=int, choices=CASES, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()
    assert args.timeout > 0
    config = CASES[args.p]
    source = source_directory(args.p)
    stem = f'a{args.p}_{config["size"]}'
    cnf = (source/(stem+'.cnf')).read_bytes()
    original = gzip.decompress((source/(stem+'.drat.gz')).read_bytes())
    receipt = json.loads((source/'receipt.json').read_text())
    assert receipt['p'] == args.p and receipt['size'] == config['size']
    assert sha(original) == config['proof_sha'] == receipt['proof_sha256']
    assert original.count(b'\n') == config['lines'] == receipt['proof_lines']
    edges, schema = qualify(cnf, args.p)
    bindings = frozen_bindings()
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    for name, digest in provenance['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == digest
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA
    args.output.mkdir(parents=True, exist_ok=False)
    packed = gzip.compress(cnf, mtime=0)
    (args.output/'input.cnf.gz').write_bytes(packed)
    edge_input = edge_bytes(args.p, edges)
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(edge_input, mtime=0))
    schema.update(bindings, target_size=config['size'], input_sha256=sha(cnf),
                  source_cnf_path=(source/(stem+'.cnf')).relative_to(ROOT).as_posix(),
                  original_drat_path=(source/(stem+'.drat.gz')).relative_to(ROOT).as_posix(),
                  original_drat_sha256=sha(original), original_drat_lines=config['lines'],
                  original_receipt_sha256=sha((source/'receipt.json').read_bytes()),
                  edge_input_sha256=sha(edge_input), driver_source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Every safe h+2 set extends to this class CNF; all residual clauses separately checked by integer geometry. No SAT search or reliance on original checker status.')
    save(args.output/'schema.json', schema)
    with tempfile.TemporaryDirectory(prefix=f'p{args.p}-single-proof-') as directory:
        directory = Path(directory)
        cp, pp, ep = directory/'input.cnf', directory/'proof.drat', directory/'edges.txt'
        cp.write_bytes(cnf); pp.write_bytes(original); ep.write_bytes(edge_input)
        ge, trim, lr = directory/'geometry.exe', directory/'trim.exe', directory/'lrat.exe'
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        geometry = run([str(ge), str(ep)], 60)
        geometry.update(wrapper_source_sha256=sha(wrapper.read_bytes()), generic_source_sha256=sha(generic.read_bytes()),
                        edge_input_sha256=sha(edge_input), binary_sha256=sha(ge.read_bytes()))
        save(args.output/'geometry.json', geometry)
        assert geometry['returncode'] == 0 and geometry['stdout'].strip() == f'VERIFIED_EDGES {args.p} {len(edges)}'
        subprocess.run(['gcc', str(TRIM/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(trim)], check=True, timeout=60)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(lr)], check=True, timeout=60)
        core = (args.output/'core.lrat').resolve()
        result = run([str(trim), str(cp), str(pp), '-U', '-t', str(args.timeout), '-L', str(core)], args.timeout+30)
        result.update(input_sha256=sha(cnf), original_drat_sha256=sha(original),
                      checker_source_sha256=provenance['files']['drat-trim.c'], checker_binary_sha256=sha(trim.read_bytes()),
                      method='Pinned DRAT-trim -U, RUP-only',
                      verified=result['returncode'] == 0 and 's VERIFIED' in result['stdout'].splitlines())
        save(args.output/'rup.json', result)
        print(args.p, 'RUP', result['verified'], flush=True)
        if not result['verified']:
            raise SystemExit(1)
        raw = core.read_bytes()
        (args.output/'core.lrat.gz').write_bytes(gzip.compress(raw, mtime=0))
        checked = run([str(lr), str(cp), str(core)], args.timeout)
        checked.update(input_sha256=sha(cnf), lrat_raw_sha256=sha(raw), checker_source_sha256=FIXED_SHA,
                       checker_binary_sha256=sha(lr.read_bytes()),
                       verified=checked['returncode'] == 0 and 'c VERIFIED' in checked['stdout'].splitlines())
        save(args.output/'lrat.json', checked)
        manifest = dict(p=args.p, excluded_size=config['size'], independent_upper_bound=config['size']-1,
                        input_path=(args.output/'input.cnf.gz').resolve().relative_to(ROOT).as_posix(),
                        input_raw_sha256=sha(cnf), input_gzip_sha256=sha(packed),
                        lrat_path=(args.output/'core.lrat.gz').resolve().relative_to(ROOT).as_posix(),
                        lrat_raw_sha256=sha(raw), lrat_gzip_sha256=sha((args.output/'core.lrat.gz').read_bytes()),
                        lrat_raw_bytes=len(raw), lrat_lines=raw.count(b'\n'),
                        original_drat_path=schema['original_drat_path'], original_drat_sha256=sha(original),
                        fixed_lrat_source_sha256=FIXED_SHA, schema_geometry_rup_lrat_verified=checked['verified'],
                        scope='Finite single-CNF upper bound from faithful independent schema, sound provided geometry and RUP/fixed-LRAT checks. Original per-d coverage counts unchanged.')
        save(args.output/'manifest.json', manifest)
        print(args.p, 'LRAT', checked['verified'], 'upper', config['size']-1, flush=True)
        if not checked['verified']:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
