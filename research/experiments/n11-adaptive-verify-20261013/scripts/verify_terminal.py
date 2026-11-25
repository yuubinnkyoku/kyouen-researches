"""Terminal-only independent verification of a regenerated next10m trace.

Same checker and same criteria as the focus-verified set
(115540 / 144193 / 144311 in n11-native-terminal-checker-20261013):
byte-identical check_trace source, root/verdict bound to the frozen
next10m-manifest row, trace SHA256 bound to that row, full closure to
geometric terminals, pruned roundtrip, trusted_leaves forced to 0.

Raw solver labels stay solver-trusted; only this receipt upgrades a row to
independent terminal-only evidence. UNKNOWN is never upgraded.
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


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=int)
    parser.add_argument('--manifest', type=Path, required=True,
                        help='frozen next10m-manifest.json binding root, verdict and trace hash')
    parser.add_argument('--probe-manifest', type=Path, required=True,
                        help='fresh adaptive probe manifest for this run')
    parser.add_argument('--trace', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    args = parser.parse_args()
    for name in ('manifest', 'probe_manifest', 'trace', 'checker'):
        setattr(args, name, getattr(args, name).resolve())
    manifest = json.loads(args.manifest.read_text())
    row = next(r for r in manifest['rows'] if r['s5_index'] == args.index)
    assert row['verdict'] in (1, 2) and row['status'] == 'SOLVED', 'only completed traces carry propositions'
    source = ROOT / manifest['source']
    assert digest(source) == manifest['source_sha256'], 'manifest source hash mismatch'
    source_row = next(r for r in json.loads(source.read_text())['rows'] if r['s5_index'] == args.index)
    assert source_row['mask'] == row['mask'], 'manifest root differs from frozen source'
    root = str(row['mask'][0] | row['mask'][1] << 64)
    verdict = row['verdict']
    assert digest(args.trace) == row['trace_sha256'], 'regenerated trace hash differs from frozen next10m trace'
    probe = json.loads(args.probe_manifest.read_text())
    prow = next(r for r in probe['rows'] if r['s5_index'] == args.index)
    assert prow['status'] == 'SOLVED' and prow['verdict'] == verdict
    assert prow['trace_sha256'] == row['trace_sha256'] and prow['mask'] == row['mask']
    output = EXP / 'output'
    output.mkdir(exist_ok=True)
    pruned = output / f'pilot-{args.index}-pruned.csv.gz'
    dag = output / f'pilot-{args.index}-terminal-dag.json.gz'
    assert not pruned.exists() and not dag.exists(), 'refusing to overwrite existing artifacts'
    cmd = [str(args.checker), str(args.trace), '--pruned', str(pruned), '--json-dag', str(dag),
           '--expect-root', root, '--expect-verdict', str(verdict)]
    started = time.monotonic()
    result = subprocess.run(cmd, text=True, capture_output=True, check=True)
    receipt = json.loads(result.stdout)
    assert receipt['trusted_leaves'] == 0, 'terminal-only closure requires zero trusted leaves'
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
    receipt['checker_source_sha256'] = digest(EXP / 'scripts' / 'check_trace.cpp')
    receipt['checker_binary_sha256'] = digest(args.checker)
    receipt['manifest'] = str(args.manifest.relative_to(ROOT))
    receipt['manifest_sha256'] = digest(args.manifest)
    receipt['manifest_source_sha256'] = manifest['source_sha256']
    receipt['manifest_trace_sha256_match'] = True
    receipt['probe_manifest'] = str(args.probe_manifest.relative_to(ROOT))
    receipt['probe_manifest_sha256'] = digest(args.probe_manifest)
    receipt['probe_search_nodes'] = prow['nodes']
    receipt['probe_wall_seconds'] = prow['wall_seconds']
    receipt['probe_peak_rss_kib'] = prow['peak_rss_kib']
    receipt['s5_index'] = args.index
    receipt['evidence_class'] = 'independent-terminal-only-verification'
    receipt['raw_label_trust'] = 'solver-trusted completed label from the frozen next10m raw run'
    receipt['trust'] = ('independent terminal-only verification: local geometry, canonical ranking, '
                        'complete universal boundaries, existential witnesses and terminal parity all rechecked; '
                        'zero trusted leaves; raw solver label upgraded solely by this receipt')
    (output / f'pilot-{args.index}-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
