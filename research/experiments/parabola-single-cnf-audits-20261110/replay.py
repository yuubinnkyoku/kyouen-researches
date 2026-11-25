"""Replay adopted gzip certificates with all source/schema/geometry bindings."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from check_case import HERE, ROOT, FROZEN, TRIM, FIXED_SHA, CASES, sha, save, run, qualify, edge_bytes, frozen_bindings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    schema = json.loads((args.saved/'schema.json').read_text())
    manifest = json.loads((args.saved/'manifest.json').read_text())
    geometry = json.loads((args.saved/'geometry.json').read_text())
    rup = json.loads((args.saved/'rup.json').read_text())
    lrat = json.loads((args.saved/'lrat.json').read_text())
    p = manifest['p']
    assert p == schema['p'] and manifest['excluded_size'] == CASES[p]['size']
    for key, digest in frozen_bindings().items():
        assert schema[key] == digest
    assert sha((HERE/'check_case.py').read_bytes()) == schema['driver_source_sha256']
    packed_c = (ROOT/manifest['input_path']).read_bytes()
    packed_p = (ROOT/manifest['lrat_path']).read_bytes()
    cnf, proof = gzip.decompress(packed_c), gzip.decompress(packed_p)
    assert sha(packed_c) == manifest['input_gzip_sha256'] and sha(packed_p) == manifest['lrat_gzip_sha256']
    assert sha(cnf) == schema['input_sha256'] == manifest['input_raw_sha256'] == rup['input_sha256'] == lrat['input_sha256']
    assert sha(proof) == manifest['lrat_raw_sha256'] == lrat['lrat_raw_sha256']
    assert len(proof) == manifest['lrat_raw_bytes']
    edges, decoded = qualify(cnf, p)
    raw_edges = edge_bytes(p, edges)
    assert raw_edges == gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    assert sha(raw_edges) == schema['edge_input_sha256'] == geometry['edge_input_sha256']
    assert geometry['returncode'] == 0 and geometry['stdout'].strip() == f'VERIFIED_EDGES {p} {len(edges)}'
    assert sha((HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp').read_bytes()) == geometry['wrapper_source_sha256']
    assert sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes()) == geometry['generic_source_sha256']
    assert rup['verified'] and lrat['verified'] and manifest['schema_geometry_rup_lrat_verified']
    assert rup['returncode'] == lrat['returncode'] == 0
    assert 's VERIFIED' in rup['stdout'].splitlines() and 'c VERIFIED' in lrat['stdout'].splitlines()
    assert schema['original_drat_sha256'] == manifest['original_drat_sha256'] == rup['original_drat_sha256'] == CASES[p]['proof_sha']
    assert sha(gzip.decompress((ROOT/manifest['original_drat_path']).read_bytes())) == CASES[p]['proof_sha']
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    assert sha((TRIM/'vendor/drat-trim.c').read_bytes()) == rup['checker_source_sha256'] == provenance['files']['drat-trim.c']
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == manifest['fixed_lrat_source_sha256'] == lrat['checker_source_sha256'] == FIXED_SHA
    with tempfile.TemporaryDirectory(prefix=f'p{p}-gzip-replay-') as directory:
        directory = Path(directory)
        cp, pp, exe = directory/'input.cnf', directory/'core.lrat', directory/'lrat.exe'
        cp.write_bytes(cnf); pp.write_bytes(proof)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(exe)], check=True, timeout=60)
        result = run([str(exe), str(cp), str(pp)], 180)
        assert result['returncode'] == 0 and 'c VERIFIED' in result['stdout'].splitlines()
        result.update(p=p, independent_upper_bound=manifest['independent_upper_bound'],
                      input_sha256=sha(cnf), lrat_raw_sha256=sha(proof), checker_source_sha256=FIXED_SHA,
                      checker_binary_sha256=sha(exe.read_bytes()), source_sha256=sha(Path(__file__).read_bytes()),
                      schema_geometry_source_proof_bindings=True,
                      scope='Actual replay of distributed gzip CNF/LRAT. No new SAT search, exact maximum or general verifier soundness claim.')
    save(args.output, result)
    print('PASS', p, 'saved gzip replay and all bindings; upper', result['independent_upper_bound'])


if __name__ == '__main__':
    main()
