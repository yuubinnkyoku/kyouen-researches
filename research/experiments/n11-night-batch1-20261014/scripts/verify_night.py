"""Terminal-only independent verification of a batch trace with check_trace.

Same checker binary/source and same criteria as the focus-verified set
(115540 / 144193 / 144311 in n11-native-terminal-checker-20261013 and the
adaptive set 126899 / 144095 / 121263 / 145001): byte-identical check_trace
source, root/verdict bound to the governing manifest row, trace SHA256 bound
to that row, full closure to geometric terminals, pruned roundtrip,
trusted_leaves forced to 0.

Two binding modes:
  --mode frozen   (task A) root/verdict/trace SHA bound to the frozen
                   n11-conflict-closure next10m-manifest row.
  --mode probe    (task B) root/verdict/trace SHA bound to this batch's own
                   probe manifest row (no frozen prior exists).

Raw solver labels stay solver-trusted; only this receipt upgrades a row to
independent terminal-only evidence. UNKNOWN is never upgraded. If the
checker dies (e.g. OOM) the row is recorded solver-trusted only.
"""
import argparse
import hashlib
import json
import resource
import subprocess
import time
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]
FROZEN = ROOT / 'research/experiments/n11-conflict-closure-20261013/output/next10m-manifest.json'
CHECKER_SOURCE = ROOT / 'research/experiments/n11-native-terminal-checker-20261013/scripts/check_trace.cpp'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=int)
    parser.add_argument('--mode', choices=['frozen', 'probe'], required=True)
    parser.add_argument('--probe-manifest', type=Path, required=True,
                        help='this batch probe manifest (night-a or nightb) binding root, verdict and trace hash')
    parser.add_argument('--trace', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--label', required=True, help='artifact label, e.g. night-a or nightb10m')
    args = parser.parse_args()
    for name in ('probe_manifest', 'trace', 'checker'):
        setattr(args, name, getattr(args, name).resolve())
    probe = json.loads(args.probe_manifest.read_text())
    prow = next(r for r in probe['rows'] if r['s5_index'] == args.index)
    assert prow['status'] == 'SOLVED' and prow['verdict'] in (1, 2), 'only completed traces carry propositions'
    assert digest(args.trace) == prow['trace_sha256'], 'trace hash differs from the probe manifest row'
    verdict = prow['verdict']
    root = str(prow['mask'][0] | prow['mask'][1] << 64)
    binding = dict(probe_manifest=str(args.probe_manifest.relative_to(ROOT)),
                   probe_manifest_sha256=digest(args.probe_manifest),
                   probe_search_nodes=prow['nodes'], probe_wall_seconds=prow['wall_seconds'],
                   probe_peak_rss_kib=prow.get('peak_rss_kib'))
    if args.mode == 'frozen':
        frozen = json.loads(FROZEN.read_text())
        frow = next(r for r in frozen['rows'] if r['s5_index'] == args.index)
        assert frow['status'] == 'SOLVED' and frow['verdict'] == verdict
        assert frow['mask'] == prow['mask']
        assert digest(args.trace) == frow['trace_sha256'], 'regenerated trace hash differs from frozen trace'
        binding.update(frozen_manifest=str(FROZEN.relative_to(ROOT)), frozen_manifest_sha256=digest(FROZEN),
                       frozen_trace_sha256=frow['trace_sha256'], frozen_trace_sha256_match=True,
                       frozen_nodes=frow['nodes'], raw_label_trust='solver-trusted completed label from the frozen next10m raw run')
    output = EXP / 'output'
    output.mkdir(exist_ok=True)
    pruned = output / f'{args.label}-{args.index}-pruned.csv.gz'
    dag = output / f'{args.label}-{args.index}-terminal-dag.json.gz'
    receipt_path = output / f'{args.label}-{args.index}-receipt.json'
    assert not pruned.exists() and not dag.exists() and not receipt_path.exists(), 'refusing to overwrite existing artifacts'
    cmd = [str(args.checker), str(args.trace), '--pruned', str(pruned), '--json-dag', str(dag),
           '--expect-root', root, '--expect-verdict', str(verdict)]
    started = time.monotonic()
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        receipt = json.loads(result.stdout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        failure = dict(s5_index=args.index, label=args.label, status='CHECKER_FAILED',
                       evidence_class='solver-trusted-only', verdict=verdict,
                       error=str(exc)[:500], **binding)
        receipt_path.write_text(json.dumps(failure, indent=2, sort_keys=True) + '\n')
        print(json.dumps(failure, indent=2, sort_keys=True))
        return
    assert receipt['trusted_leaves'] == 0, 'terminal-only closure requires zero trusted leaves'
    assert receipt['root_mask'] == root and receipt['verdict'] == verdict
    receipt['wall_seconds'] = time.monotonic() - started
    receipt['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    receipt['trace_sha256'] = digest(args.trace)
    receipt['pruned_sha256'] = digest(pruned)
    receipt['trace_bytes'] = args.trace.stat().st_size
    receipt['pruned_bytes'] = pruned.stat().st_size
    replay_cmd = [str(args.checker), str(pruned), '--expect-root', receipt['root_mask'],
                  '--expect-verdict', str(receipt['verdict'])]
    replay = json.loads(subprocess.run(replay_cmd, text=True, capture_output=True, check=True).stdout)
    assert all(replay[k] == receipt[k] for k in ('root_mask', 'verdict', 'nodes', 'edges', 'terminal_nodes', 'trusted_leaves'))
    assert replay['orphan_nodes'] == 0
    receipt['pruned_roundtrip_verified'] = True
    receipt['pruned_roundtrip_seconds'] = replay['total_seconds']
    receipt['certificate_sha256'] = digest(dag)
    receipt['certificate_bytes'] = dag.stat().st_size
    receipt['checker_source_sha256'] = digest(CHECKER_SOURCE)
    receipt['checker_binary_sha256'] = digest(args.checker)
    receipt['checker_source_path'] = str(CHECKER_SOURCE.relative_to(ROOT))
    receipt['s5_index'] = args.index
    receipt['evidence_class'] = 'independent-terminal-only-verification'
    receipt['trust'] = ('independent terminal-only verification: local geometry, canonical ranking, '
                        'complete universal boundaries, existential witnesses and terminal parity all rechecked; '
                        'zero trusted leaves; raw solver label upgraded solely by this receipt')
    receipt.update(binding)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
