#!/usr/bin/env python3
"""Rebuild the warm multiband certificate records from already-extracted certs.

Re-runs the independent BigInt verifier (no solver/cache import) for every
pushed warm certificate and merges the verifier output with the extraction
summary written by warm_rebuild_pipeline_20261115.py, producing one record
entry per certificate in the same schema as warm_records.json.

Usage: python3 rebuild_warm_records_20261115.py <targets.json> <out.json>
       targets.json = list of [band, child_hex, bit, root_hex] (greedy order)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
WARM = HERE / 'warm'
SCRIPTS = HERE / 'scripts'


def legal_moves(root_hex):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'legal_candidates.py'),
                        root_hex], capture_output=True, text=True, check=True)
    lines = r.stdout.strip().splitlines()
    mobility = int(lines[0].split(' legal ')[1])
    return mobility


def verify(cert_path, mobility):
    r = subprocess.run(['node', str(SCRIPTS /
                                    'verify_win7_certificate_bigint_independent.mjs'),
                        str(cert_path), str(mobility)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    targets = json.loads(Path(sys.argv[1]).read_text())
    records = []
    for band, child_hex, bit, root_hex in targets:
        cert_path = WARM / f'{band}-bit{bit}-root-{root_hex}.cert'
        summary = json.loads(
            Path(str(cert_path) + '.summary.json').read_text())
        assert summary['bit'] == bit and summary['child'] == child_hex, summary
        mobility = legal_moves(root_hex)
        v = verify(cert_path, mobility)
        assert v['verdict'] == 'WIN7 certificate independently verified', v
        assert v['root_mobility'] == mobility, v
        assert v['subroots_passed'] == mobility, v
        assert v['union_missing'] == 0 and v['union_extra'] == 0, v
        assert v['terminal_range'][0] >= 13 and v['terminal_range'][1] <= 17, v
        assert v['rows_sorted_unique'] is True, v
        assert v['strategy_rows'] == summary['nRows'], v
        data = cert_path.read_bytes()
        entry = {
            'band': band,
            'child_hex': child_hex,
            'bit': bit,
            'root_hex': root_hex,
            'verdict': 'WIN7',
            'rows': summary['nRows'],
            'extraction_nodes': summary['sum'],
            'extraction': 'class4_child1_cert_extractor_exact.ts (repo-verbatim), '
                          'blind (empty kill table, FBS=1<<20): fbt_drops=0, all '
                          'per-move extractions ok and uncapped (warm rebuild, '
                          '2026-11-15); sed -n 2p stdin recipe',
            'rows_sorted_unique': True,
            'root_check': {
                'stones': v['root_stones'],
                'loser_mobility': mobility,
                'independent_enumeration_legal': mobility,
                'match': v['root_mobility'] == mobility,
            },
            'sub_roots_verified': v['subroots_passed'],
            'sub_roots_pass': v['subroots_passed'],
            'union_missing': v['union_missing'],
            'union_extra': v['union_extra'],
            'terminal_range': v['terminal_range'],
            'visited_states_across_subroots': v['visited_states_across_subroots'],
            'winner_states': v['winner_states'],
            'loser_states': v['loser_states'],
            'loser_reply_edges': v['loser_reply_edges'],
            'terminal_count': v['terminal_count'],
            'md5': hashlib.md5(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data),
            'extraction_ms': summary['ms'],
        }
        records.append(entry)
        print(f"OK {band} bit-{bit} root {root_hex} rows={entry['rows']} "
              f"mobility={mobility} md5={entry['md5']}", flush=True)
    Path(sys.argv[2]).write_text(json.dumps(records, indent=1) + '\n')
    print(f'written {sys.argv[2]} with {len(records)} entries')


if __name__ == '__main__':
    main()
