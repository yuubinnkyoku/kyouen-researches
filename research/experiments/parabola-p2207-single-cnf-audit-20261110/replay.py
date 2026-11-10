"""Replay the distributed gzip CNF/LRAT with full source and schema bindings."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from audit import HERE, ROOT, TRIM, FIXED_SHA, PROOF_SHA, save, sha, run
from schema import audit as audit_schema


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    manifest = json.loads((args.saved/'manifest.json').read_text())
    schema = json.loads((args.saved/'schema.json').read_text())
    geometry = json.loads((args.saved/'geometry.json').read_text())
    rup = json.loads((args.saved/'rup.json').read_text())
    lrat = json.loads((args.saved/'lrat.json').read_text())
    cp = (ROOT/manifest['input_path']).read_bytes()
    pp = (ROOT/manifest['lrat_path']).read_bytes()
    cnf, proof = gzip.decompress(cp), gzip.decompress(pp)
    assert sha(cp) == manifest['input_gzip_sha256']
    assert sha(pp) == manifest['lrat_gzip_sha256']
    assert sha(cnf) == manifest['input_raw_sha256'] == schema['input_sha256'] == rup['input_sha256'] == lrat['input_sha256']
    assert sha(proof) == manifest['lrat_raw_sha256'] == lrat['lrat_raw_sha256']
    assert len(proof) == manifest['lrat_raw_bytes']
    assert sha((HERE/'schema.py').read_bytes()) == schema['schema_source_sha256']
    assert sha((HERE/'audit.py').read_bytes()) == schema['driver_source_sha256']
    edges, decoded = audit_schema(cnf)
    assert decoded['structural_clauses'] == 18748 and len(edges) == 31868
    raw_edges = (f'2207 {len(edges)}\n'+''.join(' '.join(map(str, e))+'\n' for e in edges)).encode('ascii')
    assert raw_edges == gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    assert sha(raw_edges) == geometry['edge_input_sha256'] == schema['edge_input_sha256']
    assert geometry['returncode'] == 0 and geometry['stdout'].strip() == 'VERIFIED_EDGES 2207 31868'
    wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert sha(wrapper.read_bytes()) == geometry['wrapper_source_sha256']
    assert sha(generic.read_bytes()) == geometry['generic_source_sha256']
    assert rup['verified'] and lrat['verified'] and manifest['schema_geometry_rup_lrat_verified']
    assert rup['returncode'] == lrat['returncode'] == 0
    assert 's VERIFIED' in rup['stdout'].splitlines() and 'c VERIFIED' in lrat['stdout'].splitlines()
    assert manifest['original_drat_sha256'] == schema['original_drat_sha256'] == rup['original_drat_sha256'] == PROOF_SHA
    assert sha(gzip.decompress((ROOT/manifest['original_drat_path']).read_bytes())) == PROOF_SHA
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA == manifest['fixed_lrat_source_sha256'] == lrat['checker_source_sha256']
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    assert sha((TRIM/'vendor/drat-trim.c').read_bytes()) == rup['checker_source_sha256'] == provenance['files']['drat-trim.c']
    lower = HERE.parent/'parabola-p2207-1104-witness-20261110/output'
    lower_receipt = json.loads((lower/'geometry.json').read_text())
    assert lower_receipt['verified'] and lower_receipt['returncode'] == 0
    assert sha((lower/'candidate.txt').read_bytes()) == lower_receipt['candidate_input_sha256']
    assert lower_receipt['p'] == 2207 and lower_receipt['size'] == 1104
    assert sha(generic.read_bytes()) == lower_receipt['verifier_source_sha256']
    with tempfile.TemporaryDirectory(prefix='p2207-saved-replay-') as directory:
        directory = Path(directory)
        c, p, exe = directory/'input.cnf', directory/'core.lrat', directory/'lrat.exe'
        c.write_bytes(cnf); p.write_bytes(proof)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(exe)], check=True, timeout=60)
        result = run([str(exe), str(c), str(p)], 180)
        assert result['returncode'] == 0 and 'c VERIFIED' in result['stdout'].splitlines()
        result.update(input_sha256=sha(cnf), lrat_raw_sha256=sha(proof),
                      source_sha256=sha(Path(__file__).read_bytes()), checker_source_sha256=FIXED_SHA,
                      checker_binary_sha256=sha(exe.read_bytes()), schema_geometry_proof_bindings=True,
                      lower_1104_receipt_binding=True, independent_upper_bound=1104,
                      scope='Actual replay of distributed CNF/LRAT gzip, all schema/geometry/source/hash bindings and prior independently checked lower witness. Finite computational A(2207)=1104; not Lean formalization.')
    save(args.output, result)
    print('PASS saved gzip replay, schema/geometry/source bindings, lower 1104 upper 1104')


if __name__ == '__main__':
    main()
