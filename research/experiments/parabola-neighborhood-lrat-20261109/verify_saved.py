"""Bind the accepted LRAT and controls to the exact saved neighborhood input."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-bounded-exchange-20261109'
TRIM = HERE.parent/'parabola-drat-trim-20261109'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    accepted = HERE/'output/target1303-remove3'
    receipt_raw = (accepted/'result.json').read_bytes()
    receipt = json.loads(receipt_raw)
    assert receipt['source_sha256'] == sha((HERE/'audit.py').read_bytes())
    assert receipt['trim']['verified'] and receipt['lrat_verified'] and receipt['lrat']['verified']
    assert receipt['trim']['returncode'] == receipt['lrat']['returncode'] == 0
    assert 's VERIFIED' in receipt['trim']['stdout'].splitlines()
    assert 'c VERIFIED' in receipt['lrat']['stdout'].splitlines()
    core = accepted/'core.lrat'
    digest, size, count = hashlib.sha256(), 0, 0
    with core.open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            digest.update(block)
            size += len(block)
            count += block.count(b'\n')
    assert [digest.hexdigest(), size, count] == [receipt['core_sha256'], receipt['core_bytes'], receipt['core_lines']]
    for name, expected in receipt['upstream']['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == expected
    assert sha((TRIM/'lrat-check-empty-fixed.c').read_bytes()) == receipt['fixed_lrat_source_sha256']
    saved = PRIOR/'output/target1303-remove3-budget100000'
    original = json.loads((saved/'result.json').read_text())
    assert original['source_sha256'] == sha((PRIOR/'search.py').read_bytes())
    seed_raw = Path(original['seed_path']).read_bytes()
    assert sha(seed_raw) == original['seed_sha256']
    seed = list(map(int, seed_raw.split()[2:]))
    assert len(seed) == 1302 and original['target'] == 1303 and original['max_removed'] == 3
    spec = importlib.util.spec_from_file_location('saved_bounded_search', PRIOR/'search.py')
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)
    assert sha(worker.SNAPSHOT.read_bytes()) == original['encoding_snapshot_sha256']
    clauses, nv, prior_top, point_vars = worker.build(seed, 1303, 3)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    assert cnf == gzip.decompress((saved/'input.cnf.gz').read_bytes())
    assert sha(cnf) == original['input_cnf_sha256'] == receipt['input_cnf_sha256']
    proof = gzip.decompress((saved/'proof.drat.gz').read_bytes())
    assert sha(proof) == original['proof_sha256'] == receipt['original_drat_sha256']
    extra, top = worker.removal_counter(point_vars, 3, prior_top)
    assert clauses[-len(extra):] == extra and top == nv
    assert len(point_vars) == 1299 and prior_top == 32569 and nv == 36457
    allowed = set(point_vars)
    assert all(abs(v) in allowed or prior_top < abs(v) <= nv for c in extra for v in c)
    trim_controls = json.loads((HERE/'output/trim-controls.json').read_text())
    assert trim_controls['source_sha256'] == receipt['upstream']['files']['drat-trim.c']
    assert len(trim_controls['cases']) == 6
    assert all(c['accepted'] == (c['name'] == 'resolution-unsat') for c in trim_controls['cases'])
    lrat_controls = json.loads((HERE/'output/lrat-controls.json').read_text())
    assert lrat_controls['source_sha256']['empty-fixed'] == receipt['fixed_lrat_source_sha256']
    assert len(lrat_controls['cases']) == 5
    assert all(c['results']['empty-fixed']['accepted'] == c['expected'] for c in lrat_controls['cases'])
    result = dict(input_cnf_byte_reconstructed=True, auxiliary_reservation_verified=True,
                  source_and_proof_hashes_match=True, accepted_lrat_receipt_sha256=sha(receipt_raw),
                  lrat_raw_sha256=digest.hexdigest(), lrat_raw_bytes=size, lrat_lines=count,
                  trim_controls=6, fixed_lrat_controls=5, variables=nv, clauses=len(clauses),
                  source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Saved input reconstruction, proof/control/source binding. LRAT itself was replayed by audit.py; no new SAT search or global geometric upper bound.')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
