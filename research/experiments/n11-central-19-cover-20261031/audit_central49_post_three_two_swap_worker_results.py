#!/usr/bin/env python3
"""Fail-closed worker frontier for the 2450-class central49 post-three-two-swap cover.

The 2542-, 2584-, 2627- and 2525-class manifests remain historical and are NOT accepted.
Worker CSV verdicts are unverified reports, never promoted to proof.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import audit_central49_repaired_worker_results as prior

HERE = Path(__file__).resolve().parent
CERT = HERE / 'central49-post-three-two-swap-2450.json'
CERT_BLOB = '77ce6a7e2b1f4fd3d35143acede17da9f0595439'
EXPECTED = 2450


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build():
    check = subprocess.run(
        ['node', str(HERE / 'verify_central49_post_three_two_swap_2450.js')],
        capture_output=True, text=True)
    require(check.returncode == 0,
            'post-three-two-swap verifier failed: ' + (check.stderr or check.stdout)[-1400:])
    raw = CERT.read_bytes()
    git_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(git_sha == CERT_BLOB, 'post-three-two-swap certificate changed; explicit re-audit required')
    doc = json.loads(raw)
    require(doc['schema'] == 'n11-central49-terminal-safe-post-three-two-swap-v1'
            and doc['root_stones'] == [49, 60]
            and doc['root_outcome'] == 'UNKNOWN'
            and doc['empty_board_outcome'] == 'UNKNOWN',
            'invalid post-three-two-swap certificate identity')
    keys = doc['selected_s4_classes']
    require(len(keys) == 31 and keys == sorted(set(keys))
            and not set(keys).intersection(prior.REFUTED_S4),
            'invalid selected S4 keys')
    loss4 = set(doc['known_loss4_classes'])
    require(len(loss4) == 3 and loss4 <= set(keys), 'known LOSS4 changed')
    cache = prior.load_fixed_cache()
    owners = defaultdict(set)
    witnesses = []
    all_children, known_children = set(), set()
    for i, key in enumerate(keys):
        cs = prior.children(key)
        known = cs.intersection(cache)
        require(all(cache[c] == 2 for c in known),
                'cached WIN5 child under candidate LOSS4: ' + key)
        if key in loss4:
            require(known == cs, 'incomplete pinned LOSS4: ' + key)
        else:
            for c in cs - known:
                owners[c].add(i)
        all_children.update(cs)
        known_children.update(known)
        witnesses.append({'s4': key, 'known_loss4': key in loss4,
                          'unknown_s5': len(cs - known)})
    pending = sorted(owners)
    require(len(all_children) == 2765 and len(known_children) == 315
            and len(pending) == EXPECTED
            and set(pending).isdisjoint(known_children)
            and set(pending).union(known_children) == all_children,
            'post-three-two-swap frontier count/coverage mismatch')
    unresolved = [i for i, w in enumerate(witnesses) if not w['known_loss4']]
    require(len(unresolved) == 28, 'unproved S4 count changed')
    priority = min(unresolved, key=lambda i: (witnesses[i]['unknown_s5'], keys[i]))
    first = [key for key in pending if priority in owners[key]]
    require(len(first) == witnesses[priority]['unknown_s5'],
            'priority S4 children inconsistent')
    first_set = set(first)
    ordered = first + [key for key in pending if key not in first_set]
    shards = [ordered[i::4] for i in range(4)]
    require(list(map(len, shards)) == [613, 613, 612, 612],
            'unbalanced post-three-two-swap worklist')
    assignment = {key: i for i, shard in enumerate(shards) for key in shard}
    require(len(assignment) == EXPECTED, 'duplicate or missing S5 work')
    return cache, owners, witnesses, assignment, shards, ordered, priority


def read_reports(assignment, workers, existing):
    verdicts = {}
    stats = {'rows': 0, 'unknown_rows': 0, 'repeated_verdicts': 0}
    if existing:
        prior.parse_rows(existing, assignment, None, verdicts, stats, str(existing))
    for worker, filename in workers:
        prior.parse_rows(filename, assignment, worker, verdicts, stats, str(filename))
    return verdicts, stats


def audit(workers, existing):
    cache, owners, witnesses, assignment, shards, ordered, priority = build()
    verdicts, stats = read_reports(assignment, workers, existing)
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
        'schema': 'n11-central49-post-three-two-swap-worker-audit-v1',
        'root': [49, 60], 'root_outcome': 'UNKNOWN',
        'empty_board_outcome': 'UNKNOWN',
        'evidence_level': 'WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED',
        'pinned_cache_classes': len(cache),
        'pending_s5_classes': EXPECTED,
        'priority_s4': witnesses[priority]['s4'],
        'priority_unknown_s5': witnesses[priority]['unknown_s5'],
        'manifest_sha256': prior.digest(ordered),
        'worker_sha256': list(map(prior.digest, shards)),
        'worker_loads': list(map(len, shards)),
        'report_rows': stats['rows'],
        'unknown_rows_ignored': stats['unknown_rows'],
        'repeated_consistent_verdicts': stats['repeated_verdicts'],
        'reported_win5': sum(v == 1 for v in verdicts.values()),
        'reported_loss5': sum(v == 2 for v in verdicts.values()),
        'unreported_s5': EXPECTED - len(verdicts),
        'plan_invalidated_if_reported_win5_verified': any(v == 1 for v in verdicts.values()),
        's4_dependency_report': per_s4,
        'caveat': 'Worker reports are not certificates. Any verified WIN5 refutes the affected S4 LOSS candidate. Never infer an S2 or empty-board outcome from these counts.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', nargs=2, action='append', default=[], metavar=('ID', 'CSV'))
    parser.add_argument('--existing', type=Path)
    parser.add_argument('--worklist', choices=('0', '1', '2', '3'))
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        prior.self_test()
        return
    workers = []
    for ident, filename in args.worker:
        require(ident in ('0', '1', '2', '3'), 'worker ID must be 0..3')
        workers.append((int(ident), Path(filename)))
    if args.worklist is not None:
        require(not workers, 'cannot export worklist with worker reports')
        _, _, _, assignment, shards, _, _ = build()
        verdicts, _ = read_reports(assignment, [], args.existing)
        require(not any(v == 1 for v in verdicts.values()),
                'REPLAN_REQUIRED: reported WIN5 invalidates candidate if verified')
        remaining = [k for k in shards[int(args.worklist)] if k not in verdicts]
        if remaining:
            sys.stdout.write('\n'.join(remaining) + '\n')
        return
    print(json.dumps(audit(workers, args.existing), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('WORKER_AUDIT_REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
