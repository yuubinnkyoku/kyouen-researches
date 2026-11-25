"""Independent terminal-only verification of a SOLVED adaptive probe row.

Mirrors n11-native-terminal-checker-20261013/scripts/benchmark.py and compare_dag.py:
the standalone check_trace checker (no solver imports) rebuilds a terminal-closed
DAG, replays the pruned trace, and the Python dag_verifier re-checks the exported
certificate. Only completed labels are accepted; trusted_leaves is reported.
"""
import argparse
import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]
CHECKER_EXP = ROOT / 'research/experiments/n11-native-terminal-checker-20261013'
sys.path.insert(0, str(ROOT / 'research/experiments/n11-proof-dag-engine-20261011/scripts'))
from dag_verifier import verify_certificate


class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_uint32), ('PageFaultCount', ctypes.c_uint32),
                ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]


_psapi = ctypes.WinDLL('psapi')


def peak_rss_kib(handle):
    counters = PROCESS_MEMORY_COUNTERS()
    counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    if not _psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
        return None
    return counters.PeakWorkingSetSize // 1024


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=int)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--checker', type=Path, default=CHECKER_EXP / 'output/check_trace.exe')
    args = parser.parse_args()
    args.manifest = args.manifest.resolve()
    manifest = json.loads(args.manifest.read_text())
    row = next(r for r in manifest['rows'] if r['s5_index'] == args.index)
    assert row['verdict'] in (1, 2) and row['status'] == 'SOLVED', 'only completed traces carry propositions'
    source = ROOT / manifest['source']
    assert digest(source) == manifest['source_sha256'], 'manifest source hash mismatch'
    source_row = next(r for r in json.loads(source.read_text())['rows'] if r['s5_index'] == args.index)
    assert source_row['mask'] == row['mask'], 'manifest root differs from frozen source'
    trace = ROOT / row['trace_path']
    assert digest(trace) == row['trace_sha256'], 'manifest trace hash mismatch'
    root = str(row['mask'][0] | row['mask'][1] << 64)
    verdict = row['verdict']

    output = EXP / 'output'
    output.mkdir(exist_ok=True)
    pruned = output / f'adaptive-{args.index}-pruned.csv.gz'
    dag = output / f'adaptive-{args.index}-terminal-dag.json.gz'
    assert not pruned.exists() and not dag.exists(), 'refusing to overwrite existing artifacts'
    cmd = [str(args.checker.resolve()), str(trace), '--pruned', str(pruned), '--json-dag', str(dag),
           '--expect-root', root, '--expect-verdict', str(verdict)]
    started = time.monotonic()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_text, err_text = proc.communicate()
    rss = peak_rss_kib(proc._handle)
    assert proc.returncode == 0, (args.index, err_text)
    receipt = json.loads(out_text)
    receipt['wall_seconds'] = time.monotonic() - started
    receipt['peak_rss_kib'] = rss
    receipt['trace_sha256'] = digest(trace)
    receipt['pruned_sha256'] = digest(pruned)
    receipt['trace_bytes'] = trace.stat().st_size
    receipt['pruned_bytes'] = pruned.stat().st_size

    replay_cmd = [str(args.checker.resolve()), str(pruned), '--expect-root', receipt['root_mask'],
                  '--expect-verdict', str(receipt['verdict'])]
    replay = json.loads(subprocess.run(replay_cmd, text=True, capture_output=True, check=True).stdout)
    assert all(replay[k] == receipt[k] for k in ('root_mask', 'verdict', 'nodes', 'edges', 'terminal_nodes', 'trusted_leaves'))
    assert replay['orphan_nodes'] == 0
    receipt['pruned_roundtrip_verified'] = True
    receipt['pruned_roundtrip_seconds'] = replay['total_seconds']
    receipt['certificate_sha256'] = digest(dag)
    receipt['certificate_bytes'] = dag.stat().st_size
    receipt['checker_source_sha256'] = digest(ROOT / 'research/experiments/n11-native-terminal-checker-20261013/scripts/check_trace.cpp')
    receipt['manifest'] = str(args.manifest.relative_to(ROOT))
    receipt['manifest_sha256'] = digest(args.manifest)
    receipt['manifest_source_sha256'] = manifest['source_sha256']
    receipt['manifest_trace_sha256_match'] = receipt['trace_sha256'] == row['trace_sha256']
    receipt['s5_index'] = args.index

    with gzip.open(dag, 'rt') as stream:
        cert = json.load(stream)
    checked = verify_certificate(cert)
    assert all(checked[k] == receipt[k] for k in checked), (checked, receipt)
    comparison = dict(s5_index=args.index, fresh_python_verification=checked,
                      matches_native_receipt=True, trusted_leaves=receipt['trusted_leaves'])
    (output / f'adaptive-{args.index}-python-comparison.json').write_text(json.dumps(comparison, indent=2, sort_keys=True) + '\n')
    (output / f'adaptive-{args.index}-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
