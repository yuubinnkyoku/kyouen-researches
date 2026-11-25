"""Convert a saved neighborhood DRAT to LRAT and check hints independently."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
TRIM = HERE.parent/'parabola-drat-trim-20261109'
FIXED_SHA = 'ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def bounded(command, timeout):
    started = time.monotonic()
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return dict(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr,
                    seconds=time.monotonic()-started, timed_out=False)
    except subprocess.TimeoutExpired as exc:
        decode = lambda value: value.decode(errors='replace') if isinstance(value, bytes) else value or ''
        return dict(returncode=None, stdout=decode(exc.stdout), stderr=decode(exc.stderr),
                    seconds=time.monotonic()-started, timed_out=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    original = json.loads((args.saved/'result.json').read_text())
    cnf = gzip.decompress((args.saved/'input.cnf.gz').read_bytes())
    proof = gzip.decompress((args.saved/'proof.drat.gz').read_bytes())
    assert sha(cnf) == original['input_cnf_sha256'] and sha(proof) == original['proof_sha256']
    provenance = json.loads((TRIM/'vendor/provenance.json').read_text())
    for name, expected in provenance['files'].items():
        assert sha((TRIM/'vendor'/name).read_bytes()) == expected
    fixed = TRIM/'lrat-check-empty-fixed.c'
    assert sha(fixed.read_bytes()) == FIXED_SHA
    report = dict(input_cnf_sha256=sha(cnf), original_drat_sha256=sha(proof),
                  original_drat_lines=original['proof_lines'], input_variables=original['variables'],
                  input_clauses=original['clauses'], source_sha256=sha(Path(__file__).read_bytes()),
                  upstream=provenance, fixed_lrat_source_sha256=FIXED_SHA,
                  scope='Independent LRAT replay of one saved bounded-neighborhood CNF; no global geometric upper bound.')
    save(args.output/'preflight.json', report)
    with tempfile.TemporaryDirectory(prefix='neighborhood-lrat-') as directory:
        directory = Path(directory)
        cp, pp = directory/'input.cnf', directory/'proof.drat'
        cp.write_bytes(cnf)
        pp.write_bytes(proof)
        trim_exe, fixed_exe = directory/'drat-trim.exe', directory/'fixed-lrat.exe'
        subprocess.run(['gcc', str(TRIM/'vendor/drat-trim.c'), *provenance['build_flags'], '-o', str(trim_exe)], check=True, timeout=60)
        subprocess.run(['gcc', str(fixed), *provenance['build_flags'], '-DLONGTYPE', '-o', str(fixed_exe)], check=True, timeout=60)
        report.update(trim_binary_sha256=sha(trim_exe.read_bytes()), fixed_lrat_binary_sha256=sha(fixed_exe.read_bytes()))
        core = (args.output/'core.lrat').resolve()
        trim = bounded([str(trim_exe), str(cp), str(pp), '-U', '-t', str(args.timeout), '-L', str(core)], args.timeout+15)
        trim['verified'] = trim['returncode'] == 0 and 's VERIFIED' in trim['stdout'].splitlines()
        report['trim'] = trim
        save(args.output/'trim.json', report)
        print(f"trim_verified={trim['verified']} seconds={trim['seconds']:.2f}", flush=True)
        report['lrat_verified'] = False
        if core.exists():
            digest, count, size = hashlib.sha256(), 0, 0
            with core.open('rb') as stream:
                for block in iter(lambda: stream.read(8*1024*1024), b''):
                    digest.update(block)
                    count += block.count(b'\n')
                    size += len(block)
            report.update(core_sha256=digest.hexdigest(), core_bytes=size, core_lines=count)
            if size <= 32*1024*1024:
                with core.open('rb') as src, (args.output/'core.lrat.gz').open('wb') as dst:
                    with gzip.GzipFile(filename='', mode='wb', fileobj=dst, compresslevel=1, mtime=0) as packed:
                        for block in iter(lambda: src.read(8*1024*1024), b''):
                            packed.write(block)
                report['core_git_distribution'] = 'gzip included'
            else:
                report['core_git_distribution'] = 'raw local only; manifest and deterministic conversion retained'
                report['core_local_path'] = str(core)
            if trim['verified']:
                lrat = bounded([str(fixed_exe), str(cp), str(core)], args.timeout)
                lrat['verified'] = lrat['returncode'] == 0 and 'c VERIFIED' in lrat['stdout'].splitlines()
                report['lrat'] = lrat
                report['lrat_verified'] = lrat['verified']
        save(args.output/'result.json', report)
        print(json.dumps({k:report[k] for k in ('lrat_verified', 'core_bytes', 'core_lines') if k in report}), flush=True)
    if not report['lrat_verified']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
