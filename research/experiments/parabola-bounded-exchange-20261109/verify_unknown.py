"""Bind an UNKNOWN trial to its exact saved input, without solving it again."""
import argparse
import gzip
import json
from pathlib import Path
from search import build, removal_counter, sha, save, SNAPSHOT

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    raw = (args.saved/'result.json').read_bytes()
    receipt = json.loads(raw)
    initial = json.loads((args.saved/'init.json').read_text())
    assert all(receipt[key] == value for key, value in initial.items())
    assert receipt['status'] == 'UNKNOWN'
    assert receipt['source_sha256'] == sha((HERE/'search.py').read_bytes())
    assert receipt['encoding_snapshot_sha256'] == sha(SNAPSHOT.read_bytes())
    seed_raw = Path(receipt['seed_path']).read_bytes()
    assert sha(seed_raw) == receipt['seed_sha256']
    seed = list(map(int, seed_raw.split()[2:]))
    clauses, nv, prior_top, point_vars = build(seed, receipt['target'], receipt['max_removed'])
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    assert cnf == gzip.decompress((args.saved/'input.cnf.gz').read_bytes())
    assert sha(cnf) == receipt['input_cnf_sha256']
    assert nv == receipt['variables'] and len(clauses) == receipt['clauses']
    extra, top = removal_counter(point_vars, receipt['max_removed'], prior_top)
    assert clauses[-len(extra):] == extra and top == nv
    allowed = set(point_vars)
    assert all(abs(v) in allowed or prior_top < abs(v) <= nv for c in extra for v in c)
    assert all(not (args.saved/name).exists() for name in ('candidate.txt', 'model.json', 'proof.drat.gz'))
    result = dict(status='SAVED_UNKNOWN_VALIDATED', saved_result_sha256=sha(raw), input_cnf_sha256=sha(cnf),
                  variables=nv, clauses=len(clauses), seed_size=len(seed), target=receipt['target'],
                  max_removed=receipt['max_removed'], input_byte_reconstructed=True,
                  auxiliary_reservation_verified=True, no_candidate_model_or_proof=True,
                  source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Input and provenance validation only. UNKNOWN gives no SAT, UNSAT, geometric nonexistence, or global bound.')
    save(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
