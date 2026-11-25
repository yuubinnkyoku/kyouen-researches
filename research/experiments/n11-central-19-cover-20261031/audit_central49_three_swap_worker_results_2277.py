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


def focus_children(owners, witnesses, s4):
    """Resolve a coordinator-selected, unproved S4 to its exact S5 frontier."""
    eligible = {w['s4']: i for i, w in enumerate(witnesses)
                if not w['known_loss4']}
    require(s4 in eligible, 'focus S4 must be a selected unresolved witness')
    index = eligible[s4]
    focus = {k for k, memberships in owners.items() if index in memberships}
    require(len(focus) == witnesses[index]['unknown_s5'],
            'focused S4 dependency mismatch')
    return focus


def choose_priority_focus(owners, witnesses, reported):
    """Select the smallest *remaining* S4 frontier; reports affect scheduling only.

    A fully reported S4 is NOT a proof. Never infer its verdict here.
    """
    candidates = []
    for i, witness in enumerate(witnesses):
        if witness['known_loss4']:
            continue
        keys = {key for key, membership in owners.items() if i in membership}
        require(len(keys) == witness['unknown_s5'],
                'priority S4 dependency mismatch')
        remaining = len(keys - reported.keys())
        if remaining:
            candidates.append((remaining, witness['unknown_s5'], witness['s4']))
    return min(candidates)[2] if candidates else None



def make_focus_plan(owners, witnesses, assignment, shards, ordered, reported,
                    requested_s4=None, existing_sha256=None):
    """Freeze one coordinator decision and all four worklists in one snapshot.

    Each worker must consume its list from this same document, rather than
    independently reselecting a priority against a changing report file.
    """
    require(not any(v == 1 for v in reported.values()),
            'REPLAN_REQUIRED: reported WIN5 must be checked before further work')
    selected = (requested_s4 if requested_s4 is not None
                else choose_priority_focus(owners, witnesses, reported))
    focus = focus_children(owners, witnesses, selected) if selected is not None else set()
    worklists = [[key for key in shard if key in focus and key not in reported]
                 for shard in shards]
    flat = [key for part in worklists for key in part]
    require(len(flat) == len(set(flat)), 'duplicate S5 in frozen focus plan')
    require(set(flat) == focus - reported.keys(),
            'incomplete frozen focus plan')
    require(all(assignment[key] == worker for worker, part in enumerate(worklists)
                for key in part), 'wrong worker in frozen focus plan')
    return {
        'schema': 'n11-central49-2277-focused-snapshot-v1',
        'root': [49, 60], 'root_outcome': 'UNKNOWN',
        'empty_board_outcome': 'UNKNOWN',
        'evidence_level': 'SCHEDULING_ONLY_NOT_A_CERTIFICATE',
        'source_manifest_sha256': previous.prior.digest(ordered),
        'existing_report_sha256': existing_sha256,
        'selected_s4': selected,
        'selected_unknown_s5': len(focus),
        'remaining_s5': len(flat),
        'worker_loads': list(map(len, worklists)),
        'worker_sha256': list(map(previous.prior.digest, worklists)),
        'worklists': worklists,
        'caveat': 'One immutable dispatch snapshot. Worker reports are not independent proofs; empty lists never certify S4 LOSS.'
    }


def remaining_worklist(shards, assignment, existing, worker_id, focus=None):
    """Resume this frontier, optionally restricting work to one S4 witness.

    Focus changes scheduling only, never the assignment or evidence level.
    """
    if focus is not None:
        require(focus <= assignment.keys(), 'focus includes off-frontier S5')
    verdicts, _ = previous.read_reports(assignment, [], existing)
    require(not any(v == 1 for v in verdicts.values()),
            'REPLAN_REQUIRED: reported WIN5 must be checked before further work')
    return [k for k in shards[worker_id]
            if k not in verdicts and (focus is None or k in focus)]



def audit_frozen_plan(plan_path, existing, workers, merged_out):
    """Rebuild and audit one frozen coordinator dispatch before merging receipts.

    Unlike the generic frontier audit, this rejects worker rows outside the
    *selected* S4's frozen worklists, even when they belong to the 2277 pool.
    All verdicts remain unverified worker reports.
    """
    import os
    import tempfile

    _, owners, witnesses, assignment, shards, ordered, _ = build()
    raw = plan_path.read_bytes()
    plan = json.loads(raw)
    require(isinstance(plan, dict), 'invalid frozen plan document')
    before = (hashlib.sha256(existing.read_bytes()).hexdigest()
              if existing is not None else None)
    require(plan.get('existing_report_sha256') == before,
            'frozen plan belongs to a different existing report')
    old, _ = previous.read_reports(assignment, [], existing)
    after = (hashlib.sha256(existing.read_bytes()).hexdigest()
             if existing is not None else None)
    require(before == after, 'existing report changed during snapshot audit')
    expected = make_focus_plan(owners, witnesses, assignment, shards, ordered,
                               old, plan.get('selected_s4'), before)
    require(plan == expected, 'frozen plan differs from reconstructed frontier')
    focused_assignment = {
        key: worker
        for worker, keys in enumerate(expected['worklists'])
        for key in keys
    }
    require(len(focused_assignment) == expected['remaining_s5'],
            'duplicate frozen worker assignment')
    verdicts = dict(old)
    stats = {'rows': 0, 'unknown_rows': 0, 'repeated_verdicts': 0}
    hashes = [(path, hashlib.sha256(path.read_bytes()).hexdigest())
              for _, path in workers]
    for worker, path in workers:
        previous.prior.parse_rows(path, focused_assignment, worker,
                                  verdicts, stats, str(path))
    require(not any(v == 1 for v in verdicts.values()),
            'REPLAN_REQUIRED: reported WIN5; independently verify before continuing')
    require(all(hashlib.sha256(path.read_bytes()).hexdigest() == digest
                for path, digest in hashes),
            'worker report changed during merge')
    require(before == (hashlib.sha256(existing.read_bytes()).hexdigest()
                       if existing is not None else None),
            'existing report changed during merge')
    new_keys = set(verdicts) - set(old)
    require(new_keys <= focused_assignment.keys(),
            'merged a verdict outside frozen worklists')
    if merged_out is not None:
        inputs = [plan_path] + [path for _, path in workers]
        if existing is not None:
            inputs.append(existing)
        require(all(merged_out.resolve() != path.resolve() for path in inputs),
                'merged output must not overwrite an input')
        require(not merged_out.exists(), 'merged output already exists')
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode='w', encoding='utf-8', newline='', dir=merged_out.parent,
                    prefix='.focus-merge-', delete=False) as stream:
                temporary = Path(stream.name)
                for key in sorted(verdicts):
                    bits = int(key, 16)
                    stream.write(
                        f's5verdict,{bits & ((1 << 64)-1)},{bits >> 64},'
                        f'5,{verdicts[key]},0\n')  # node count unavailable after merge
                stream.flush()
                os.fsync(stream.fileno())
            os.link(temporary, merged_out)  # atomic, refuses overwrite
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return {
        'schema': 'n11-central49-2277-frozen-receipt-audit-v1',
        'root_outcome': 'UNKNOWN', 'empty_board_outcome': 'UNKNOWN',
        'evidence_level': 'WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED',
        'snapshot_sha256': hashlib.sha256(raw).hexdigest(),
        'selected_s4': plan['selected_s4'],
        'frozen_focus_s5': plan['remaining_s5'],
        'new_reported_verdicts': len(new_keys),
        'total_reported_verdicts': len(verdicts),
        'remaining_focused_s5': plan['remaining_s5'] - len(new_keys),
        'unknown_rows_ignored': stats['unknown_rows'],
        'repeated_consistent_verdicts': stats['repeated_verdicts'],
        'merged_output': str(merged_out) if merged_out is not None else None,
        'caveat': 'Worker reports are not certificates. Independently replay every verdict.'
    }


def self_test():
    import tempfile
    previous.prior.self_test()
    a, b, c = (f'{i:032x}' for i in (1, 2, 3))
    shards = [[a], [b], [], []]
    assignment = {a: 0, b: 1}
    example_witnesses = [
        {'s4': 'candidate', 'known_loss4': False, 'unknown_s5': 1},
        {'s4': 'proved', 'known_loss4': True, 'unknown_s5': 0},
    ]
    example_owners = {a: {0}, b: {0}}
    try:
        focus_children(example_owners, example_witnesses, 'candidate')
    except ValueError:
        pass
    else:
        raise AssertionError('inconsistent focused S4 count accepted')
    example_owners[b] = set()
    require(choose_priority_focus(example_owners, example_witnesses, {}) == 'candidate',
            'priority focus did not select the unresolved witness')
    require(choose_priority_focus(example_owners, example_witnesses, {a: 2}) is None,
            'fully reported S4 was rescheduled')
    require(focus_children(example_owners, example_witnesses, 'candidate') == {a},
            'coordinator focus omitted a child')
    frozen = make_focus_plan(example_owners, example_witnesses, assignment,
                             shards, [a, b], {})
    require(frozen['selected_s4'] == 'candidate'
            and frozen['worker_loads'] == [1, 0, 0, 0]
            and frozen['worklists'] == [[a], [], [], []]
            and frozen['remaining_s5'] == 1,
            'frozen focus snapshot is inconsistent')
    finished = make_focus_plan(example_owners, example_witnesses, assignment,
                               shards, [a, b], {a: 2})
    require(finished['selected_s4'] is None and finished['remaining_s5'] == 0
            and finished['evidence_level'] == 'SCHEDULING_ONLY_NOT_A_CERTIFICATE',
            'fully reported work was promoted to proof')
    for bad_report, bad_s4 in (({a: 1}, None), ({}, 'proved'),
                               ({}, 'unselected')):
        try:
            make_focus_plan(example_owners, example_witnesses, assignment,
                            shards, [a, b], bad_report, bad_s4)
        except ValueError:
            pass
        else:
            raise AssertionError('unsafe frozen focus plan accepted')
    for bad in ('proved', 'unselected'):
        try:
            focus_children(example_owners, example_witnesses, bad)
        except ValueError:
            continue
        raise AssertionError('invalid S4 focus accepted: ' + bad)

    def row(key, verdict):
        value = int(key, 16)
        return f's5verdict,{value & ((1 << 64) - 1)},{value >> 64},5,{verdict},1\n'

    two_witnesses = [
        {'s4': 'large', 'known_loss4': False, 'unknown_s5': 2},
        {'s4': 'small', 'known_loss4': False, 'unknown_s5': 1},
    ]
    two_owners = {a: {0, 1}, b: {0}}
    require(choose_priority_focus(two_owners, two_witnesses, {}) == 'small',
            'priority did not choose smaller S4')
    require(choose_priority_focus(two_owners, two_witnesses, {a: 2}) == 'large',
            'priority did not update after a report')
    require(choose_priority_focus(two_owners, two_witnesses, {a: 2, b: 2}) is None,
            'fully reported witnesses were mistaken for pending work')
    with tempfile.TemporaryDirectory() as directory:
        report = Path(directory) / 'merged.csv'
        require(remaining_worklist(shards, assignment, None, 0) == [a],
                'empty resume changed full worklist')
        report.write_text(row(a, 2), encoding='utf-8')
        require(remaining_worklist(shards, assignment, report, 0) == [],
                'reported LOSS was scheduled twice')
        require(remaining_worklist(shards, assignment, report, 1) == [b],
                'other worker lost its assignment')
        require(remaining_worklist(shards, assignment, None, 0, {a}) == [a],
                'focused worklist lost its S5 child')
        require(remaining_worklist(shards, assignment, None, 1, {a}) == [],
                'focused worklist leaked another S4 child')
        require(remaining_worklist(shards, assignment, report, 0, {a}) == [],
                'focused resume repeated a reported S5')
        try:
            remaining_worklist(shards, assignment, None, 0, {c})
        except ValueError:
            pass
        else:
            raise AssertionError('off-frontier focus was accepted')
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
    parser.add_argument('--focus-s4', metavar='HEX32',
                        help='Export only unknown S5 children of this selected, unresolved S4')
    parser.add_argument('--focus-priority', action='store_true',
                        help='Automatically focus the unresolved S4 with fewest unreported S5 children')
    parser.add_argument('--focus-plan', action='store_true',
                        help='Emit one immutable JSON snapshot with all four focused worker lists')
    parser.add_argument('--audit-focus-plan', type=Path,
                        help='Audit receipts against one frozen --focus-plan JSON')
    parser.add_argument('--merged-out', type=Path,
                        help='Publish a NEW merged CSV only after fail-closed audit')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    workers = []
    for ident, filename in args.worker:
        require(ident in ('0', '1', '2', '3'), 'worker ID must be 0..3')
        workers.append((int(ident), Path(filename)))
    if args.audit_focus_plan is not None:
        require(args.worklist is None and not args.focus_plan
                and not args.focus_priority and args.focus_s4 is None,
                'frozen receipt audit cannot export a new worklist')
        print(json.dumps(audit_frozen_plan(args.audit_focus_plan, args.existing,
                                          workers, args.merged_out),
                         indent=2, ensure_ascii=False))
        return
    require(args.merged_out is None,
            '--merged-out requires --audit-focus-plan')
    require(not (args.focus_s4 and args.focus_priority),
            '--focus-s4 and --focus-priority are mutually exclusive')
    require(not (args.focus_plan and args.worklist is not None),
            '--focus-plan and --worklist are mutually exclusive')
    if args.focus_plan:
        require(not workers, 'cannot export a focus plan with worker reports')
        _, owners, witnesses, assignment, shards, ordered, _ = build()
        before = (hashlib.sha256(args.existing.read_bytes()).hexdigest()
                  if args.existing is not None else None)
        reported, _ = previous.read_reports(assignment, [], args.existing)
        after = (hashlib.sha256(args.existing.read_bytes()).hexdigest()
                 if args.existing is not None else None)
        require(before == after, 'existing report changed during focus snapshot')
        plan = make_focus_plan(owners, witnesses, assignment, shards, ordered,
                               reported, args.focus_s4, before)
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return
    if args.worklist is not None:
        require(not workers, 'cannot export worklist with worker reports')
        _, owners, witnesses, assignment, shards, _, _ = build()
        if args.focus_priority:
            reported, _ = previous.read_reports(assignment, [], args.existing)
            require(not any(v == 1 for v in reported.values()),
                    'REPLAN_REQUIRED: reported WIN5 must be checked before further work')
            selected = choose_priority_focus(owners, witnesses, reported)
            focus = (focus_children(owners, witnesses, selected)
                     if selected is not None else set())
        else:
            focus = (focus_children(owners, witnesses, args.focus_s4)
                     if args.focus_s4 is not None else None)
        keys = remaining_worklist(shards, assignment, args.existing,
                                  int(args.worklist), focus)
        if keys:
            sys.stdout.write('\n'.join(keys) + '\n')
        return
    require(args.focus_s4 is None and not args.focus_priority,
            '--focus-s4 and --focus-priority require --worklist')
    print(json.dumps(audit(workers, args.existing), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('WORKER_AUDIT_REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
