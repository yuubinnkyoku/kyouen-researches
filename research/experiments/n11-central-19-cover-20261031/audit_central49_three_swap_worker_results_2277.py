#!/usr/bin/env python3
"""Independent fail-closed 2277-class central49 worker frontier.

Worker verdicts are reports, NOT independent proof. Older worklists are historical.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import audit_central49_post_three_two_swap_worker_results_2345 as previous

HERE = Path(__file__).resolve().parent
CERT = HERE / 'central49-three-swap-2277.json'
CERT_BLOB = '2f5a19a9f91f911cba1e83cdfb0f6bca1e2f69c1'
EXPECTED = 2277


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build():
    check = subprocess.run(
        ['node', str(HERE / 'verify_central49_three_swap_2277.js')],
        capture_output=True, text=True)
    require(check.returncode == 0,
            'three-swap verifier failed: ' + (check.stderr or check.stdout)[-1600:])
    raw = CERT.read_bytes()
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(sha == CERT_BLOB, 'three-swap certificate changed; explicit re-audit required')
    doc = json.loads(raw)
    require(doc['schema'] == 'n11-central49-terminal-safe-three-swap-2277-v1'
            and doc['root_stones'] == [49, 60]
            and doc['root_outcome'] == 'UNKNOWN'
            and doc['empty_board_outcome'] == 'UNKNOWN',
            'invalid three-swap certificate identity')
    keys = doc['selected_s4_classes']
    require(len(keys) == 31 and keys == sorted(set(keys))
            and not set(keys).intersection(previous.prior.REFUTED_S4),
            'invalid S4 witness list')
    loss4 = set(doc['known_loss4_classes'])
    require(len(loss4) == 3 and loss4 <= set(keys), 'known LOSS4 changed')
    cache = previous.prior.load_fixed_cache()
    owners = defaultdict(set)
    witnesses = []
    all_children, known_children = set(), set()
    for i, key in enumerate(keys):
        children = previous.prior.children(key)
        known = children.intersection(cache)
        require(all(cache[c] == 2 for c in known),
                'cached WIN5 child under candidate LOSS4: ' + key)
        if key in loss4:
            require(known == children, 'incomplete pinned LOSS4: ' + key)
        else:
            for child in children - known:
                owners[child].add(i)
        all_children.update(children)
        known_children.update(known)
        witnesses.append({'s4': key, 'known_loss4': key in loss4,
                          'unknown_s5': len(children - known)})
    pending = sorted(owners)
    require(len(all_children) == 2591 and len(known_children) == 314
            and len(pending) == EXPECTED
            and set(pending).isdisjoint(known_children)
            and set(pending).union(known_children) == all_children,
            'three-swap frontier mismatch')
    unresolved = [i for i, w in enumerate(witnesses) if not w['known_loss4']]
    require(len(unresolved) == 28, 'unproved S4 count changed')
    priority = min(unresolved, key=lambda i: (witnesses[i]['unknown_s5'], keys[i]))
    first = [k for k in pending if priority in owners[k]]
    require(len(first) == witnesses[priority]['unknown_s5'] == 94,
            'priority witness changed')
    first_set = set(first)
    ordered = first + [k for k in pending if k not in first_set]
    shards = [ordered[i::4] for i in range(4)]
    require(list(map(len, shards)) == [570, 569, 569, 569],
            'unbalanced worker schedule')
    assignment = {k: i for i, shard in enumerate(shards) for k in shard}
    require(len(assignment) == EXPECTED, 'duplicate S5 work')
    return cache, owners, witnesses, assignment, shards, ordered, priority


def audit(workers, existing):
    cache, owners, witnesses, assignment, shards, ordered, priority = build()
    verdicts, stats = previous.read_reports(assignment, workers, existing)
    per_s4 = []
    for i, witness in enumerate(witnesses):
        if witness['known_loss4']:
            continue
        relevant = [verdicts[k] for k in owners if i in owners[k] and k in verdicts]
        per_s4.append({
            's4': witness['s4'],
            'reported_win5': relevant.count(1),
            'reported_loss5': relevant.count(2),
            'unreported_s5': witness['unknown_s5'] - len(relevant),
            'potential_loss4_only_after_independent_replay':
                len(relevant) == witness['unknown_s5'] and 1 not in relevant
        })
    return {
        'schema': 'n11-central49-three-swap-2277-worker-audit-v1',
        'root': [49, 60], 'root_outcome': 'UNKNOWN',
        'empty_board_outcome': 'UNKNOWN',
        'evidence_level': 'WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED',
        'pinned_cache_classes': len(cache),
        'pending_s5_classes': EXPECTED,
        'priority_s4': witnesses[priority]['s4'],
        'priority_unknown_s5': witnesses[priority]['unknown_s5'],
        'manifest_sha256': previous.prior.digest(ordered),
        'worker_sha256': list(map(previous.prior.digest, shards)),
        'worker_loads': list(map(len, shards)),
        'report_rows': stats['rows'],
        'unknown_rows_ignored': stats['unknown_rows'],
        'repeated_consistent_verdicts': stats['repeated_verdicts'],
        'reported_win5': sum(v == 1 for v in verdicts.values()),
        'reported_loss5': sum(v == 2 for v in verdicts.values()),
        'unreported_s5': EXPECTED - len(verdicts),
        'plan_invalidated_if_reported_win5_verified':
            any(v == 1 for v in verdicts.values()),
        's4_dependency_report': per_s4,
        'caveat': 'Worker reports are not certificates. Verify all reported verdicts independently before proof promotion.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', nargs=2, action='append', default=[],
                        metavar=('ID', 'CSV'))
    parser.add_argument('--existing', type=Path)
    parser.add_argument('--worklist', choices=('0', '1', '2', '3'))
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        previous.prior.self_test()
        return
    workers = []
    for ident, filename in args.worker:
        require(ident in ('0', '1', '2', '3'), 'worker ID must be 0..3')
        workers.append((int(ident), Path(filename)))
    if args.worklist is not None:
        require(not workers and args.existing is None,
                'cannot export worklist while accepting unverified reports')
        _, _, _, _, shards, _, _ = build()
        keys = shards[int(args.worklist)]
        if keys:
            sys.stdout.write('\n'.join(keys) + '\n')
        return
    print(json.dumps(audit(workers, args.existing), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('WORKER_AUDIT_REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
