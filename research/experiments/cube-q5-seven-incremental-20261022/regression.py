#!/usr/bin/env python3
"""Check incremental legality, independent proofs and checkpoint interoperability."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def run(*args):
    result = subprocess.run(list(map(str, args)), text=True, capture_output=True)
    assert result.returncode == 0, (args, result.stdout, result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('engine', type=Path)
    parser.add_argument('legacy', type=Path)
    parser.add_argument('verifier', type=Path)
    parser.add_argument('--direct', action='store_true')
    args = parser.parse_args()
    flags = ['--direct'] if args.direct else []
    known = Path(__file__).resolve().parent.parent/'cube-q5-seven-frontier-20261022/known-roots3.txt'
    audits = {str(side): json.loads(run(args.engine, '--audit', side, histories, *flags))
              for side, histories in [(3, 30), (7, 12)]}
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        checkpoint = root/'exact.memo'
        records = [json.loads(line) for line in run(
            args.engine, '--batch', 3, 1000000, 10000, root/'new', known,
            checkpoint, '--validate', *flags).splitlines()]
        assert len(records) == 20 and all(r['outcome'] == 'P' for r in records)
        proofs = []
        for record in records:
            name = 'new'+''.join('-'+str(p) for p in record['root'])+'.cert'
            proof = json.loads(run(args.verifier, root/name))
            assert proof['verified'] and proof['outcome'] == 'P'
            proofs.append(proof)
        # Old reader accepts bulk-written files; old writer is then read by new.
        resumed = [json.loads(line) for line in run(
            args.legacy, '--batch', 3, 0, 10000, root/'old', known,
            checkpoint).splitlines()]
        returned = [json.loads(line) for line in run(
            args.engine, '--batch', 3, 0, 10000, root/'returned', known,
            checkpoint, '--validate', *flags).splitlines()]
        assert len(resumed) == len(returned) == 20
        assert all(r['outcome'] == 'P' and r['nodes'] == 0 for r in resumed+returned)
        # Eviction on every new quad must not alter an exact proof.
        one = root/'one.txt'; one.write_text('0 1\n')
        evicted = json.loads(run(args.engine, '--batch', 3, 1000000, 1,
                                 root/'evict', one, root/'evict.memo', '--validate', *flags))
        assert evicted['outcome'] == 'P'
        assert json.loads(run(args.verifier, root/'evict-0-1.cert'))['verified']
        # Six-word masks and a terminal beyond bit 128.
        wide = root/'wide.txt'; wide.write_text('0 48 294 342\n')
        record = json.loads(run(args.engine, '--batch', 7, 10, 10,
                                root/'wide', wide, root/'wide.memo', '--validate', *flags))
        assert record['outcome'] == 'P'
        assert json.loads(run(args.verifier, root/'wide-0-48-294-342.cert'))['verified']
        unknown = root/'unknown.txt'; unknown.write_text('0 5\n')
        record = json.loads(run(args.engine, '--batch', 7, 0, 10000,
                                root/'unknown', unknown, root/'unknown.memo', *flags))
        assert record['outcome'] == 'UNKNOWN'
        assert not (root/'unknown-0-5.cert').exists()
        dfs_records = [json.loads(line) for line in run(
            args.engine, '--batch', 3, 1000000, 10000, root/'dfs', known,
            root/'dfs.memo', '--validate', '--dfs', *flags).splitlines()]
        assert len(dfs_records) == 20 and all(r['outcome'] == 'P' for r in dfs_records)
        for record in dfs_records:
            name = 'dfs'+''.join('-'+str(p) for p in record['root'])+'.cert'
            assert json.loads(run(args.verifier, root/name))['verified']
    print(json.dumps({'direct': args.direct, 'audits': audits, 'known_three_cube_orbits': 20,
                      'all_proofs_independently_verified': True,
                      'bidirectional_checkpoint_compatibility': True,
                      'geometry_eviction_exact': True, 'wide_terminal_verified': True,
                      'mobility_dfs_independent_three_cube_proofs': 20,
                      'zero_budget_unknown': True, 'proofs': proofs}, indent=2))


if __name__ == '__main__':
    main()
