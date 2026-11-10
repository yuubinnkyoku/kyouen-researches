"""Replay adopted compressed CNF/LRAT and semantics without the original DRAT."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from schema import audit as qualify, SEED_SHA
from audit import HERE, ROOT, SOURCE, TRIM, FIXED_SHA, sha, save, run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    manifest = json.loads((args.saved/'manifest.json').read_text())
    schema = json.loads((args.saved/'schema.json').read_text())
    regression = json.loads((HERE/'regression.json').read_text())
    assert sha((HERE/'schema.py').read_bytes()) == manifest['schema_source_sha256'] == regression['schema_source_sha256']
    assert sha((HERE/'audit.py').read_bytes()) == manifest['driver_source_sha256']
    cnf = gzip.decompress((args.saved/'input.cnf.gz').read_bytes())
    packed = (args.saved/'core.lrat.gz').read_bytes()
    proof = gzip.decompress(packed)
    assert sha(cnf) == manifest['input_sha256'] == schema['input_sha256']
    assert sha(packed) == manifest['lrat_gzip_sha256']
    assert sha(proof) == manifest['lrat_raw_sha256'] and proof.count(b'\n') == manifest['lrat_lines']
    seed_path = ROOT/'research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
    seed_raw = seed_path.read_bytes()
    assert sha(seed_raw) == SEED_SHA == manifest['seed_sha256']
    tokens = list(map(int, seed_raw.split()))
    assert tokens[:2] == [2539, 1258] and len(tokens) == 1260
    edges, result = qualify(cnf, tokens[2:])
    for key, value in result.items():
        assert schema[key] == value
    raw_edges = (f'2539 {len(edges)}\n'+''.join(' '.join(map(str, q))+'\n' for q in edges)).encode('ascii')
    assert raw_edges == gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    assert sha(raw_edges) == schema['edge_input_sha256']
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA == manifest['fixed_lrat_source_sha256']
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    geometry = json.loads((args.saved/'geometry.json').read_text())
    assert sha(generic.read_bytes()) == geometry['generic_source_sha256']
    assert sha(wrapper.read_bytes()) == geometry['wrapper_source_sha256']
    with tempfile.TemporaryDirectory(prefix='p2539-local-replay-') as temporary:
        td = Path(temporary)
        cp, pp, ep = td/'input.cnf', td/'core.lrat', td/'edges.txt'
        cp.write_bytes(cnf); pp.write_bytes(proof); ep.write_bytes(raw_edges)
        lr, ge = td/'lrat.exe', td/'geometry.exe'
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(lr)], check=True, timeout=60)
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        geo = run([str(ge), str(ep)], 60)
        assert geo['returncode'] == 0 and geo['stdout'].strip() == f'VERIFIED_EDGES 2539 {len(edges)}'
        replay = run([str(lr), str(cp), str(pp)], 120)
        assert replay['returncode'] == 0 and 'c VERIFIED' in replay['stdout'].splitlines()
    save(args.output, dict(schema_verified=True, geometry=geo, lrat=replay,
         input_sha256=sha(cnf), lrat_raw_sha256=sha(proof), seed_sha256=SEED_SHA,
         schema_source_sha256=manifest['schema_source_sha256'], fixed_lrat_source_sha256=FIXED_SHA,
         replay_source_sha256=sha(Path(__file__).read_bytes()),
         scope='Fresh process replay of adopted compressed proof and independent semantics; no SAT search, original DRAT, edge cache or search builder. Local fixed-origin/pair exclusion only.'))
    print('PASS compressed proof, schema, geometry and seed bindings; original DRAT unused')


if __name__ == '__main__':
    main()
