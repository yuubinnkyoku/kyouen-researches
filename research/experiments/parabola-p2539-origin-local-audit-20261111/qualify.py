"""Bind the old fixed-pair proof and the two new adopted proofs to one seed."""
import argparse
import gzip
import json
from pathlib import Path
from audit import HERE, sha, save


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    old = HERE.parent/'parabola-p2539-exchange-audit-20261110'
    prior = json.loads((old/'output/manifest.json').read_text())
    prior_replay = json.loads((old/'replay.json').read_text())
    seed = '454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'
    assert prior['seed_sha256'] == prior_replay['seed_sha256'] == seed
    assert prior['schema_geometry_rup_lrat_verified']
    assert (prior['p'], prior['d'], prior['excluded_size_at_least'], prior['max_removed']) == (2539, 6, 1259, 4)
    assert prior_replay['schema_verified'] and prior_replay['geometry']['returncode'] == 0
    assert prior_replay['lrat']['returncode'] == 0 and 'c VERIFIED' in prior_replay['lrat']['stdout'].splitlines()
    assert sha(gzip.decompress((old/'output/input.cnf.gz').read_bytes())) == prior['input_sha256']
    packed = (old/'output/core.lrat.gz').read_bytes()
    assert sha(packed) == prior['lrat_gzip_sha256']
    assert sha(gzip.decompress(packed)) == prior['lrat_raw_sha256'] == prior_replay['lrat_raw_sha256']
    replay = json.loads((HERE/'replay.json').read_text())
    assert replay['both_verified'] and replay['seed_sha256'] == seed
    assert sha((HERE/'schema.py').read_bytes()) == replay['schema_source_sha256']
    assert sha((HERE/'replay.py').read_bytes()) == replay['replay_source_sha256']
    rows = []
    assert {r['case'] for r in replay['cases']} == {'changed-pair', 'no-pair'} and len(replay['cases']) == 2
    for row in replay['cases']:
        folder = HERE/'output'/row['case']
        manifest = json.loads((folder/'manifest.json').read_text())
        assert manifest['seed_sha256'] == seed and manifest['schema_geometry_rup_lrat_verified']
        assert manifest['target_size'] == 1259 and manifest['max_removed'] == 4
        assert row['schema_verified'] and row['geometry']['returncode'] == 0
        assert row['rup']['returncode'] == 0 and 's VERIFIED' in row['rup']['stdout'].splitlines()
        assert sha(gzip.decompress((folder/'input.cnf.gz').read_bytes())) == manifest['input_sha256'] == row['input_sha256']
        packed = (folder/'verified-proof.drat.gz').read_bytes()
        assert sha(packed) == manifest['adopted_drat_gzip_sha256']
        assert sha(gzip.decompress(packed)) == manifest['adopted_drat_raw_sha256'] == row['drat_raw_sha256']
        rows.append(dict(case=row['case'], manifest_sha256=sha((folder/'manifest.json').read_bytes()),
                         input_sha256=row['input_sha256'], proof_sha256=row['drat_raw_sha256']))
    save(args.output, dict(seed_sha256=seed, origin_retained=True, excluded_size_at_least=1259, max_removed=4,
         old_fixed_pair_manifest_sha256=sha((old/'output/manifest.json').read_bytes()),
         old_fixed_pair_replay_sha256=sha((old/'replay.json').read_bytes()), new_cases=rows,
         replay_sha256=sha((HERE/'replay.json').read_bytes()),
         subset_argument_sha256=sha((HERE/'README.md').read_bytes()), source_sha256=sha(Path(__file__).read_bytes()),
         all_three_classes_bound=True,
         scope='Finite independent CNF proof checks plus the separately stated subset argument exclude every origin-retaining improvement deleting at most4 seed points. No unrestricted local optimality or global maximum.'))
    print('PASS all three classes bound to one seed; origin-retaining four-deletion exclusion')


if __name__ == '__main__':
    main()
