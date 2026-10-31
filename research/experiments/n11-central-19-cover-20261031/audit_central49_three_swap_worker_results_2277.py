#!/usr/bin/env python3
"""Independent fail-closed 2277-class central49 worker frontier.

Worker verdicts are reports, NOT independent proof. Older worklists are historical.
"""
import argparse
import hashlib
import json
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
    # The expensive exhaustive 3-for-3 optimality audit runs once in CI.
    # Worklist export independently checks geometry, WIN exclusions and S5 children.
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
    # Independently reconstruct WIN4 parents from the pinned S5 cache and
    # the six separately terminal-proved WIN5 witnesses.
    blocked = set()
    for key, verdict in cache.items():
        if verdict == 1:
            points = previous.prior.pts(key)
            for x in points:
                blocked.add(previous.prior.canonical(
                    tuple(y for y in points if y != x)))
    terminal_win5 = (
        (5, 45, 49, 53, 60), (1, 49, 59, 60, 61),
        (37, 49, 59, 60, 61), (49, 51, 59, 60, 71),
        (2, 49, 59, 60, 61), (14, 49, 59, 60, 61),
    )
    for points in terminal_win5:
        for x in points:
            blocked.add(previous.prior.canonical(
                tuple(y for y in points if y != x)))
    require(len(blocked) == 573 and not blocked.intersection(keys),
            'WIN4 exclusion failed')

    # The 119 third moves must all be covered by selected canonical S4
    # classes, considering all eight D4 images containing the fixed root.
    covered = set()
    for key in keys:
        points = previous.prior.pts(key)
        for t in range(8):
            image = []
            for p in points:
                x, y = p % 11, p // 11
                u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                        (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
                image.append(11*v + u)
            if 49 in image and 60 in image:
                covered.update(p for p in image if p not in (49, 60))
    require(covered == set(range(121)) - {49, 60},
            'incomplete third-move coverage')
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


def remaining_worklist(shards, assignment, existing, worker_id):
    """Resume only this exact frontier; never treat a report as a certificate."""
    verdicts, _ = previous.read_reports(assignment, [], existing)
    require(not any(v == 1 for v in verdicts.values()),
            'REPLAN_REQUIRED: reported WIN5 must be checked before further work')
    return [k for k in shards[worker_id] if k not in verdicts]


def self_test():
    import tempfile
    previous.prior.self_test()
    a, b, c = (f'{i:032x}' for i in (1, 2, 3))
    shards = [[a], [b], [], []]
    assignment = {a: 0, b: 1}

    def row(key, verdict):
        value = int(key, 16)
        return f's5verdict,{value & ((1 << 64) - 1)},{value >> 64},5,{verdict},1\\n'

    with tempfile.TemporaryDirectory() as directory:
        report = Path(directory) / 'merged.csv'
        require(remaining_worklist(shards, assignment, None, 0) == [a],
                'empty resume changed full worklist')
        report.write_text(row(a, 2), encoding='utf-8')
        require(remaining_worklist(shards, assignment, report, 0) == [],
                'reported LOSS was scheduled twice')
        require(remaining_worklist(shards, assignment, report, 1) == [b],
                'other worker lost its assignment')
        for bad in (row(a, 1), row(a, 0), row(c, 2),
                    row(a, 2) + row(a, 1)):
            report.write_text(bad, encoding='utf-8')
            try:
                remaining_worklist(shards, assignment, report, 0)
            except ValueError:
                continue
            raise AssertionError('unsafe resume accepted: ' + repr(bad))
    print('RESUME_SELF_TEST_OK')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', nargs=2, action='append', default=[],
                        metavar=('ID', 'CSV'))
    parser.add_argument('--existing', type=Path)
    parser.add_argument('--worklist', choices=('0', '1', '2', '3'))
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    workers = []
    for ident, filename in args.worker:
        require(ident in ('0', '1', '2', '3'), 'worker ID must be 0..3')
        workers.append((int(ident), Path(filename)))
    if args.worklist is not None:
        require(not workers, 'cannot export worklist with worker reports')
        _, _, _, assignment, shards, _, _ = build()
        keys = remaining_worklist(shards, assignment, args.existing,
                                  int(args.worklist))
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
