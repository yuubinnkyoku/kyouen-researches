"""Verify prior-ledger hashes, current schemas, and compressed LRAT replay."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
import time
from audit import ROOT, HERE, TRIM, GEN, SCHEMA, FIXED_SHA, sha, save, load_module

BASE = HERE.parent/'parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531_34249932790a9e9d.json'


def repo_path(value):
    normalized = str(value).replace('\\','/')
    assert 'research/' in normalized
    path = (ROOT/normalized[normalized.index('research/'):]).resolve()
    assert path.is_relative_to(ROOT)
    return path


def check_chain(path, seen=None):
    seen = set() if seen is None else seen
    path = Path(path).resolve()
    assert path not in seen
    seen.add(path)
    data = json.loads(path.read_text())
    assert data['p']==2531
    if 'prior_coverage_path' in data:
        previous = repo_path(data['prior_coverage_path'])
        assert sha(previous.read_bytes())==data['prior_coverage_sha256']
        old = check_chain(previous,seen)
        assert data['prior_verified_d']==sorted(old)
    else:
        raw = BASE.read_bytes()
        baseline = json.loads(raw)
        assert baseline['checker_source_sha256']=='34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b'
        old = {r['d'] for r in baseline['records'] if r['verified'] and r['checker_rc']==0 and r['solver']=='UNSAT'}
        assert len(old)==143 and sha(raw)==data['baseline_sha256']
        assert data['baseline_fixed_d']==sorted(old)
    new = set(data['new_lrat_verified_d'])
    assert not old&new and data['verified_d_union']==sorted(old|new)
    assert data['verified_union_count']==len(old|new) and data['remaining']==1265-len(old|new)
    return old|new


def replay(task):
    record, exe = task
    with tempfile.TemporaryDirectory(prefix=f"p2531-replay-{record['d']}-") as directory:
        directory = Path(directory)
        cp, pp = directory/'input.cnf', directory/'core.lrat'
        cp.write_bytes(gzip.decompress(repo_path(record['input_path']).read_bytes()))
        pp.write_bytes(gzip.decompress(repo_path(record['lrat_path']).read_bytes()))
        started = time.monotonic()
        r = subprocess.run([exe,str(cp),str(pp)],capture_output=True,text=True,timeout=90)
        assert r.returncode==0 and 'c VERIFIED' in r.stdout.splitlines()
        return dict(d=record['d'],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,
                    seconds=time.monotonic()-started)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--workers',type=int,default=4)
    args = ap.parse_args()
    assert not args.output.exists() and not args.manifest.exists() and 1<=args.workers<=4
    coverage = json.loads((args.saved/'coverage.json').read_text())
    plan = json.loads((args.saved/'plan.json').read_text())
    union = check_chain(args.saved/'coverage.json')
    assert coverage['prior_verified_d']==plan['prior_verified_d']
    assert coverage['prior_coverage_sha256']==plan['prior_coverage_sha256']
    assert plan['source_sha256']==sha((HERE/'audit.py').read_bytes())==coverage['source_sha256']
    raw = gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    lines = raw.decode('ascii').splitlines()
    assert lines[0]=='2531 38160'
    edges = [tuple(map(int,line.split())) for line in lines[1:]]
    assert len(edges)==38160 and sha(raw)==plan['edge_input_sha256']
    geometry = json.loads((args.saved/'geometry.json').read_text())
    assert geometry['returncode']==0 and geometry['input_sha256']==sha(raw)
    assert geometry['stdout'].strip()=='VERIFIED_EDGES 2531 38160'
    assert geometry['wrapper_sha256']==sha((HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp').read_bytes())
    assert geometry['generic_sha256']==sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
    assert plan['generator_sha256']==sha(GEN.read_bytes()) and plan['independent_schema_source_sha256']==sha(SCHEMA.read_bytes())
    schema = load_module('frozen_independent_schema',SCHEMA)
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes())==FIXED_SHA
    records, local_drat_count = [], 0
    for d in coverage['new_lrat_verified_d']:
        folder = args.saved/f'd{d}'
        receipt = json.loads((folder/'result.json').read_text())
        assert receipt['verified'] and receipt['solver']=='UNSAT' and receipt['d']==d
        assert receipt['source_sha256']==plan['source_sha256'] and receipt['fixed_lrat_source_sha256']==FIXED_SHA
        assert receipt['generator_sha256']==plan['generator_sha256'] and receipt['edge_input_sha256']==sha(raw)
        cnf = gzip.decompress((folder/'input.cnf.gz').read_bytes())
        packed = (folder/'core.lrat.gz').read_bytes()
        lrat = gzip.decompress(packed)
        assert schema.dimacs(schema.project(edges,d))==cnf and sha(cnf)==receipt['input_sha256']
        assert sha(lrat)==receipt['lrat_sha256'] and len(lrat)==receipt['lrat_raw_bytes']
        assert receipt['trim']['returncode']==receipt['lrat']['returncode']==0
        assert 's VERIFIED' in receipt['trim']['stdout'].splitlines() and 'c VERIFIED' in receipt['lrat']['stdout'].splitlines()
        original = folder/'proof.drat.gz'
        if original.exists():
            assert sha(gzip.decompress(original.read_bytes()))==receipt['proof_sha256']
            local_drat_count += 1
        records.append(dict(d=d,input_path=(folder/'input.cnf.gz').resolve().relative_to(ROOT).as_posix(),
             input_sha256=sha(cnf),lrat_path=(folder/'core.lrat.gz').resolve().relative_to(ROOT).as_posix(),
             lrat_raw_sha256=sha(lrat),lrat_gzip_sha256=sha(packed),
             original_drat_path=original.resolve().relative_to(ROOT).as_posix(),original_drat_sha256=receipt['proof_sha256'],
             original_drat_distribution='local gzip retained'))
    with tempfile.TemporaryDirectory(prefix='p2531-replay-binary-') as directory:
        exe = Path(directory)/'lrat.exe'
        subprocess.run(['gcc',str(fixed),'-std=c99','-O2','-DLONGTYPE','-Dgetc_unlocked=getc','-o',str(exe)],check=True,timeout=60)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            replayed = list(pool.map(replay,[(record,str(exe)) for record in records]))
        binary_sha = sha(exe.read_bytes())
    assert {r['d'] for r in replayed}==set(coverage['new_lrat_verified_d'])
    result = dict(prior_verified_count=len(plan['prior_verified_d']),new_verified_d=coverage['new_lrat_verified_d'],
                  verified_union_count=len(union),remaining=1265-len(union),prior_chain_hashes_verified=True,
                  independent_projection_cases=len(records),compressed_certificate_replays=replayed,
                  original_drat_local_checks=local_drat_count,fixed_lrat_source_sha256=FIXED_SHA,
                  replay_binary_sha256=binary_sha,source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Prior coverage hash chain, current input schemas and actual replay of distributed CNF/LRAT gzip. No all-d completion or general verifier soundness claim.')
    save(args.output,result)
    save(args.manifest,dict(records=records,verification_receipt_sha256=sha(args.output.read_bytes())))
    print(f"PASS new={len(records)} prior={len(plan['prior_verified_d'])} union={len(union)} remaining={1265-len(union)}",flush=True)


if __name__=='__main__':
    main()
