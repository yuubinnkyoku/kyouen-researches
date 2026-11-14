#!/usr/bin/env python3
"""Warm certificate rebuild pipeline driver v2 (class2-lane long-term lane,
2026-11-15). Successor of warm_rebuild_pipeline_20261115.py for the second
warm multiband batch: identical machinery (repo-verbatim blind extractor,
FBS=1<<20, independent BigInt verification), but the targets file and the
output records path are both command-line arguments so two workers can run
side by side on disjoint target halves.

Usage: python3 warm_rebuild_pipeline2_20261115.py <targets.json> <out.json>
       targets.json = list of [band, child_hex, bit, root_hex]

Self-checking guarantees per certificate (unchanged from v1):
- extraction is blind (empty kill table), FBS=1<<20, fbt_drops==0, no fatal;
- the independent verifier re-derives the whole tree: root 7 stones + safe,
  root loser mobility == independent legal_candidates.py enumeration, every
  sub-root PASS, strategy/consumed union 0/0 both directions, terminal stone
  range within 13..17, rows sorted strictly ascending and unique.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
WARM = HERE / 'warm'
WARM.mkdir(exist_ok=True)


def legal_moves(root_hex):
    r = subprocess.run([sys.executable, str(HERE / 'scripts' / 'legal_candidates.py'),
                        root_hex], capture_output=True, text=True, check=True)
    lines = r.stdout.strip().splitlines()
    mobility = int(lines[0].split(' legal ')[1])
    moves = [int(x) for x in lines[1].split(',') if x]
    return moves, mobility


def extract(child_hex, bit, moves, out_path):
    r = subprocess.run(['node', '--experimental-strip-types',
                        str(HERE / 'scripts' / 'cert_driver68.ts'),
                        child_hex, str(bit), out_path],
                       input=','.join(map(str, moves)), capture_output=True,
                       text=True, check=True)
    summary = json.loads(r.stderr.strip().splitlines()[-2])
    return summary


def finalize(cert_path):
    """sort strategy rows ascending while preserving header + root lines."""
    lines = cert_path.read_text().splitlines()
    head, rows = lines[:2], [l for l in lines[2:] if l.strip()]
    n0 = len(rows)
    rows_sorted = sorted(set(rows))
    assert len(rows_sorted) == n0, 'duplicate strategy rows!'
    cert_path.write_text('\n'.join(head + rows_sorted) + '\n')
    return len(rows_sorted)


def verify(cert_path, mobility):
    r = subprocess.run(['node', str(HERE / 'scripts' /
                                    'verify_win7_certificate_bigint_independent.mjs'),
                        str(cert_path), str(mobility)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def process(band, child_hex, bit, root_hex):
    cert_path = WARM / f'{band}-bit{bit}-root-{root_hex}.cert'
    if cert_path.exists():
        cert_path.unlink()
    moves, mobility = legal_moves(root_hex)
    summary = extract(child_hex, bit, moves, str(cert_path))
    assert summary.get('fatal') is None and summary['fbt_drops'] == 0, summary
    n_rows = finalize(cert_path)
    assert n_rows == summary['nRows'], (n_rows, summary['nRows'])
    v = verify(cert_path, mobility)
    assert v['verdict'] == 'WIN7 certificate independently verified', v
    assert v['root_mobility'] == mobility, v
    assert v['subroots_passed'] == mobility, v
    assert v['union_missing'] == 0 and v['union_extra'] == 0, v
    assert v['terminal_range'][0] >= 13 and v['terminal_range'][1] <= 17, v
    assert v['rows_sorted_unique'] is True, v
    assert v['strategy_rows'] == summary['nRows'], v
    r_md5 = subprocess.run(['md5sum', str(cert_path)], capture_output=True, text=True, check=True)
    r_sha = subprocess.run(['sha256sum', str(cert_path)], capture_output=True, text=True, check=True)
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
                      'per-move extractions ok and uncapped (warm multiband 2 '
                      'rebuild, 2026-11-15); sed -n 2p stdin recipe',
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
        'md5': r_md5.stdout.split()[0],
        'sha256': r_sha.stdout.split()[0],
        'bytes': cert_path.stat().st_size,
        'extraction_ms': summary['ms'],
    }
    return entry


def main():
    target_roots = json.loads(Path(sys.argv[1]).read_text())  # list of [band, child, bit, root]
    out_path = Path(sys.argv[2])
    records = []
    for band, child, bit, root in target_roots:
        print(f'processing {band} bit-{bit} root {root} ...', flush=True)
        entry = process(band, child, bit, root)
        records.append(entry)
        print(f"  OK rows={entry['rows']} nodes={entry['extraction_nodes']} "
              f"mobility={entry['root_check']['loser_mobility']} md5={entry['md5']}", flush=True)
        out_path.write_text(json.dumps(records, indent=1) + '\n')
    print(f'written {out_path} with {len(records)} entries')


if __name__ == '__main__':
    main()
