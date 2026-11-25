"""Check the reduced edge input, coverage chain, and distributed LRAT archives."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIOR = HERE.parent/'parabola-p2531-lrat-20261109/output/batch82-85-v2'
FIXED = HERE.parent/'parabola-drat-trim-20261109/lrat-check-empty-fixed.c'
FIXED_SHA = 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def project(edges, d):
    out = set()
    for edge in edges:
        values = {t if t <= 1265 else t-2531 for t in edge if t not in (0,d,2531-d)}
        if not any(-v in values for v in values):
            out.add(tuple(sorted(values)))
    return sorted(out)


def dimacs(clauses):
    return (f'p cnf 1265 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def write_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2)+'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--manifest', type=Path)
    ap.add_argument('--replay', action='store_true')
    args = ap.parse_args()
    assert not args.output.exists() and (args.manifest is None or not args.manifest.exists())
    coverage = json.loads((args.saved/'coverage.json').read_text())
    prior_raw = (PRIOR/'coverage.json').read_bytes()
    prior = json.loads(prior_raw)
    assert coverage['prior_coverage_sha256'] == sha(prior_raw)
    old = set(prior['verified_d_union'])
    assert len(old) == 147 and coverage['prior_verified_d'] == sorted(old)
    source = sha((HERE/'audit.py').read_bytes())
    assert source == coverage['source_sha256']
    raw = gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    lines = raw.decode('ascii').splitlines()
    assert lines[0] == '2531 38160'
    edges = [tuple(map(int,row.split())) for row in lines[1:]]
    assert len(edges) == 38160
    full = gzip.decompress((PRIOR/'edges.txt.gz').read_bytes()).decode('ascii').splitlines()
    assert full[0] == '2531 837640'
    all_edges = [tuple(map(int,row.split())) for row in full[1:]]
    kept = [q for q in all_edges if not(q[0]+q[3]==2531 and q[1]+q[2]==2531)]
    assert kept == edges and len(all_edges)-len(kept) == 799480
    for d in (82,83,84,85):
        assert dimacs(project(edges,d)) == gzip.decompress((PRIOR/f'd{d}/input.cnf.gz').read_bytes())
    geometric = json.loads((args.saved/'geometry.json').read_text())
    assert geometric['returncode'] == 0 and geometric['input_sha256'] == sha(raw)
    assert geometric['stdout'].strip() == 'VERIFIED_EDGES 2531 38160'
    assert geometric['wrapper_sha256'] == sha((HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp').read_bytes())
    assert geometric['generic_sha256'] == sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
    assert sha(FIXED.read_bytes()) == FIXED_SHA
    records, original_checks = [], 0
    with tempfile.TemporaryDirectory(prefix='p2531-archive-replay-') as directory:
        directory = Path(directory)
        exe = directory/'lrat.exe'
        if args.replay:
            subprocess.run(['gcc', str(FIXED), '-std=c99', '-O2', '-DLONGTYPE', '-Dgetc_unlocked=getc', '-o', str(exe)], check=True, timeout=60)
        for d in coverage['new_lrat_verified_d']:
            folder = args.saved/f'd{d}'
            receipt = json.loads((folder/'result.json').read_text())
            assert receipt['verified'] and receipt['solver'] == 'UNSAT' and receipt['source_sha256'] == source
            cnf_raw = gzip.decompress((folder/'input.cnf.gz').read_bytes())
            lrat_gzip = (folder/'core.lrat.gz').read_bytes()
            lrat_raw = gzip.decompress(lrat_gzip)
            assert dimacs(project(edges,d)) == cnf_raw and sha(cnf_raw) == receipt['input_sha256']
            assert sha(lrat_raw) == receipt['lrat_sha256'] and len(lrat_raw) == receipt['lrat_raw_bytes']
            original = folder/'proof.drat.gz'
            if original.exists():
                assert sha(gzip.decompress(original.read_bytes())) == receipt['proof_sha256']
                original_checks += 1
            assert receipt['fixed_lrat_source_sha256'] == FIXED_SHA
            assert receipt['trim']['returncode'] == receipt['lrat']['returncode'] == 0
            assert 's VERIFIED' in receipt['trim']['stdout'].splitlines() and 'c VERIFIED' in receipt['lrat']['stdout'].splitlines()
            record = dict(d=d, input_path=(folder/'input.cnf.gz').resolve().relative_to(ROOT).as_posix(),
                          input_sha256=sha(cnf_raw), lrat_path=(folder/'core.lrat.gz').resolve().relative_to(ROOT).as_posix(),
                          lrat_raw_sha256=sha(lrat_raw), lrat_gzip_sha256=sha(lrat_gzip),
                          original_drat_sha256=receipt['proof_sha256'], original_drat_distribution='local gzip retained',
                          verified=True)
            if args.replay:
                cp, pp = directory/'input.cnf', directory/'core.lrat'
                cp.write_bytes(cnf_raw)
                pp.write_bytes(lrat_raw)
                started = time.monotonic()
                run = subprocess.run([str(exe), str(cp), str(pp)], capture_output=True, text=True, timeout=60)
                assert run.returncode == 0 and 'c VERIFIED' in run.stdout.splitlines()
                record['archive_replay'] = dict(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr,
                                                seconds=time.monotonic()-started, binary_sha256=sha(exe.read_bytes()))
            records.append(record)
    new = {r['d'] for r in records}
    assert new == set(range(86,101)) and not old & new
    assert coverage['verified_d_union'] == sorted(old|new) and coverage['verified_union_count'] == 162
    assert coverage['remaining'] == 1103
    result = dict(filtered_edges=38160, omitted_two_pair_edges=799480, pilot_inputs_byte_equal=4,
                  independent_projection_schemas=15, new_lrat_d=sorted(new), prior_verified_count=147,
                  verified_union_count=162, remaining=1103, original_drat_local_checks=original_checks,
                  compressed_certificate_replays=len(records) if args.replay else 0,
                  fixed_lrat_source_sha256=FIXED_SHA, records=records,
                  source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Independent input projection and optional replay of distributed CNF/LRAT archives, with mixed-method coverage chain. Not a completed all-d audit.')
    write_new(args.output, result)
    if args.manifest:
        write_new(args.manifest, dict(records=records, verification_receipt_sha256=sha(args.output.read_bytes())))
    print(json.dumps({k:v for k,v in result.items() if k!='records'}, indent=2))


if __name__ == '__main__':
    main()
