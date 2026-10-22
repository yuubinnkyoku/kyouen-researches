#!/usr/bin/env python3
"""Known outcomes, exact checkpoints, six-word certificates, and rejections."""
from pathlib import Path
import argparse
import json
import subprocess
import tempfile


def run(*args, success=True):
    r = subprocess.run(list(map(str, args)), text=True, capture_output=True)
    assert (r.returncode == 0) == success, (args, r.stdout, r.stderr)
    return r.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument('solver', type=Path)
    p.add_argument('dfpn', type=Path)
    p.add_argument('verifier', type=Path)
    p.add_argument('known_roots', type=Path)
    args = p.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        checkpoint = root/'exact.memo'
        records = [json.loads(s) for s in run(args.dfpn, '--batch', 3, 1000000, 10000,
                                             root/'dfpn', args.known_roots, checkpoint).splitlines()]
        assert len(records) == 20 and all(r['outcome'] == 'P' for r in records)
        for record in records:
            name = 'dfpn'+''.join('-'+str(x) for x in record['root'])+'.cert'
            assert json.loads(run(args.verifier, root/name))['outcome'] == 'P'
        resumed = [json.loads(s) for s in run(args.dfpn, '--batch', 3, 0, 10,
                                             root/'resumed', args.known_roots, checkpoint).splitlines()]
        assert all(r['outcome'] == 'P' and r['nodes'] == 0 for r in resumed)
        # Force repeated geometry cache flushing and independently verify the result.
        cert = root/'eviction.cert'
        record = json.loads(run(args.solver, 3, 1000000, 1, cert, 0, 1))
        assert record['outcome'] == 'P' and json.loads(run(args.verifier, cert))['verified']
        wide = root/'wide.cert'
        run(args.solver, 7, 100, 10, wide, 0, 48, 294, 342)
        assert json.loads(run(args.verifier, wide))['outcome'] == 'P'
        win = root/'win.cert'
        run(args.solver, 7, 100, 1000, win, 24, 171, 318)
        assert json.loads(run(args.verifier, win))['outcome'] == 'N'
        lines = wide.read_text().splitlines()
        row = list(map(int, lines[1].split()))
        bad_label = row.copy(); bad_label[6] = 1
        outside = lines[0].split(); outside[-1] = str(1 << 23)
        cases = {
            'wrong-label': [lines[0], ' '.join(map(str, bad_label))],
            'missing-root': lines[:1],
            'duplicate': [*lines, lines[1]],
            'truncated-row': [lines[0], ' '.join(map(str, row[:-1]))],
            'outside-root': [' '.join(outside), *lines[1:]],
        }
        for name, data in cases.items():
            path = root/(name+'.cert'); path.write_text('\n'.join(data)+'\n')
            run(args.verifier, path, success=False)
        unknown = root/'unknown.cert'
        assert json.loads(run(args.solver, 7, 0, 10, unknown, 0, 5))['outcome'] == 'UNKNOWN'
        assert not unknown.exists()
    print(json.dumps({'known_three_cube_orbits': 20, 'independently_verified': True,
                      'checkpoint_resume_no_expansions': True, 'geometry_eviction_exact': True,
                      'wide_positive_certificates': 2, 'negative_certificates': 5,
                      'zero_budget_unknown': True}, indent=2))


if __name__ == '__main__':
    main()
