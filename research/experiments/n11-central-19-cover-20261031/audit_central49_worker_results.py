#!/usr/bin/env python3
"""Independent, fail-closed audit of 11x11 {49,60} S5 worker reports.

Reconstruct the fixed cover's legal S5 children and priority-first worker
partition from pinned caches. Worker CSVs are unverified reports, NOT proofs.
No cache is written by this script.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE_SOURCES = (
    ('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
     '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'),
    ('research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache',
     '9887a18c0788d26507be7e8e191c26817634a6b6'),
)
PRIORITY = '00000000000000401002010000000000'
EXPECTED_BASELINE_SHA256 = '18749cc4083357d31c622a8e337cb867bd5700530d0677a9e27dec8197e30e70'
EXPECTED_BASELINE_WORKERS = (
    '287d3771d1d15bafd48ec9fa021ceb2a5256dda0c30eedece8029b80faa0795a',
    '5b05d0af10932ca718c2ed960e350dfda4ae25756f6a96431a25dd92bd74e0fe',
    'cce0a24bce8838f33ffaf5f882216a46ab4b8934224a7258151e91ed8177ab18',
    '086f86af2b117ad5f1a6c7e4e5d7fbcae647c85a313e9e3f3771f37298891845',
)


def require(test, msg):
    if not test:
        raise ValueError(msg)


def pts(key):
    require(len(key) == 32 and all(c in '0123456789abcdef' for c in key), 'invalid hex key')
    bits = int(key, 16)
    require(bits >> 121 == 0, 'out-of-board bits')
    return tuple(i for i in range(121) if bits >> i & 1)


def canonical(points):
    variants = []
    for transform in range(8):
        bits = 0
        for p in points:
            x, y = p % 11, p // 11
            u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                    (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[transform]
            bits |= 1 << (11*v + u)
        variants.append(bits)
    return f'{min(variants):032x}'


def det4(four):
    a = [(p % 11, p // 11) for p in four]
    rows = [(x*x + y*y, x, y) for x, y in a]
    b = [tuple(r[j]-rows[0][j] for j in range(3)) for r in rows[1:]]
    return (b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
            - b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
            + b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]))


def safe(points):
    return all(det4(q) != 0 for q in combinations(points, 4))


def children(s4):
    points = pts(s4)
    require(len(points) == 4 and safe(points) and canonical(points) == s4,
            'invalid S4 witness: '+s4)
    return {canonical((*points, x)) for x in range(121)
            if x not in points and safe((*points, x))}


def digest(keys):
    return hashlib.sha256(('\n'.join(keys)+'\n').encode()).hexdigest()


def load_fixed_cache():
    cache = {}
    for relative, sha in CACHE_SOURCES:
        raw = (ROOT / relative).read_bytes()
        git_sha = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(git_sha == sha, 'pinned S5 cache changed: '+relative)
        local = set()
        for line in raw.decode('utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            cols = line.split(',')
            require(len(cols) == 6 and cols[0] == 's5verdict' and cols[3] == '5',
                    'invalid pinned cache schema')
            lo, hi, verdict, nodes = (int(cols[i]) for i in (1, 2, 4, 5))
            require(0 <= lo < 2**64 and 0 <= hi < 2**57 and verdict in (1, 2)
                    and nodes >= 0, 'invalid pinned S5 evidence')
            key = f'{(hi << 64) | lo:032x}'
            require(key not in local, 'duplicate key in pinned source')
            local.add(key)
            p = pts(key)
            require(len(p) == 5 and safe(p) and canonical(p) == key,
                    'noncanonical or unsafe pinned S5 key')
            require(key not in cache or cache[key] == verdict,
                    'WIN/LOSS CONFLICT in pinned caches: '+key)
            cache[key] = verdict
    require(len(cache) == 5853, 'pinned cache count changed')
    return cache


def build_frontier():
    cert = json.loads((HERE / 'win4-safe-31-loss4-reuse-49.json').read_text())
    frontier = json.loads((HERE / 'central49-frontier-ownership.json').read_text())
    require(cert['root_stones'] == [49, 60] and cert['root_outcome'] == 'UNKNOWN',
            'unexpected S2 root or outcome')
    require(frontier['rootStones'] == [49, 60] and frontier['rootOutcome'] == 'UNKNOWN',
            'unexpected frontier root or outcome')
    witnesses = frontier['witnesses']
    keys = cert['selected_s4_classes']
    require(len(keys) == 31 and keys == [w['s4'] for w in witnesses],
            'S4 witness list changed')
    cache = load_fixed_cache()
    owners = defaultdict(set)
    known_loss4 = set(cert['known_loss4_classes'])
    require(len(known_loss4) == 3, 'known LOSS4 count changed')
    for i, key in enumerate(keys):
        cs = children(key)
        require(len(cs) == witnesses[i]['legalS5Children'],
                'S5 child count mismatch: '+key)
        known = {c for c in cs if c in cache}
        require(all(cache[c] == 2 for c in known), 'known WIN5 child of selected S4: '+key)
        require(len(known) == witnesses[i]['knownLossS5'], 'known S5 count mismatch: '+key)
        require(len(cs)-len(known) == witnesses[i]['unknownS5'],
                'unknown S5 count mismatch: '+key)
        if key in known_loss4:
            require(witnesses[i]['status'] == 'LOSS4_PINNED_S5' and len(known) == len(cs),
                    'incomplete pinned LOSS4')
        else:
            require(witnesses[i]['status'] == 'UNKNOWN', 'unjustified S4 status')
            for c in cs:
                if c not in cache:
                    owners[c].add(i)
    pending = sorted(owners)
    require(len(pending) == 2525 and digest(pending) == EXPECTED_BASELINE_SHA256,
            'S5 frontier or SHA256 changed')
    baseline = [pending[i::4] for i in range(4)]
    require(tuple(map(digest, baseline)) == EXPECTED_BASELINE_WORKERS,
            'baseline worker hashes changed')
    require(PRIORITY in keys, 'priority witness missing')
    priority_index = keys.index(PRIORITY)
    first = [key for key in pending if priority_index in owners[key]]
    require(len(first) == 91 and all(len(owners[key]) == 1 for key in first),
            'priority S4 dependency changed')
    first_set = set(first)
    ordered = first + [key for key in pending if key not in first_set]
    shards = [ordered[i::4] for i in range(4)]
    require(list(map(len, shards)) == [632, 631, 631, 631], 'worker loads changed')
    require([sum(k in first_set for k in s) for s in shards] == [23,23,23,22],
            'priority worker counts changed')
    assignment = {key: i for i, shard in enumerate(shards) for key in shard}
    require(len(assignment) == 2525, 'duplicate S5 assignment')
    return cache, owners, witnesses, assignment, shards, ordered


def parse_rows(path, assignment, expected_worker, verdicts, stats, source_name):
    seen = set()
    with Path(path).open(newline='', encoding='utf-8') as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].strip().startswith('#'):
                continue
            where = f'{source_name}:{line_no}'
            require(len(row) == 6 and row[0] == 's5verdict' and row[3] == '5',
                    'invalid CSV row at '+where)
            require(all(x.isascii() and x.isdecimal() for x in (row[1], row[2], row[4], row[5])),
                    'noninteger or signed S5 field at '+where)
            lo, hi, verdict, nodes = (int(row[i]) for i in (1, 2, 4, 5))
            require(0 <= lo < 2**64 and 0 <= hi < 2**57 and verdict in (0, 1, 2)
                    and nodes >= 0, 'invalid S5 evidence at '+where)
            key = f'{(hi << 64) | lo:032x}'
            require(key in assignment, 'off-frontier S5 key at '+where+': '+key)
            require(expected_worker is None or assignment[key] == expected_worker,
                    'wrong worker for S5 key at '+where+': '+key)
            require(key not in seen, 'duplicate key in one report at '+where)
            seen.add(key)
            stats['rows'] += 1
            if verdict == 0:
                require(expected_worker is not None, 'UNKNOWN in previously merged cache at '+where)
                stats['unknown_rows'] += 1
                continue
            previous = verdicts.get(key)
            require(previous is None or previous == verdict,
                    'WIN/LOSS CONFLICT at '+where+': '+key)
            if previous is not None:
                stats['repeated_verdicts'] += 1
            verdicts[key] = verdict


def audit(worker_reports, existing=None):
    cache, owners, witnesses, assignment, shards, ordered = build_frontier()
    verdicts = {}
    stats = {'rows':0, 'unknown_rows':0, 'repeated_verdicts':0}
    if existing is not None:
        parse_rows(existing, assignment, None, verdicts, stats, str(existing))
    for worker, path in worker_reports:
        parse_rows(path, assignment, worker, verdicts, stats, str(path))
    summary = []
    for i, witness in enumerate(witnesses):
        if witness['status'] != 'UNKNOWN':
            continue
        relevant = [verdicts[k] for k in owners if i in owners[k] and k in verdicts]
        nwin, nloss = relevant.count(1), relevant.count(2)
        summary.append({'s4': witness['s4'], 'worker_reported_win5': nwin,
                        'worker_reported_loss5': nloss,
                        'unreported_s5': witness['unknownS5']-len(relevant),
                        'potential_s4_loss_if_replayed': nwin == 0 and len(relevant) == witness['unknownS5']})
    return {
        'schema':'n11-central49-worker-report-audit-v1',
        'root':[49,60], 'root_outcome':'UNKNOWN',
        'evidence_level':'WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED',
        'pinned_source_cache_classes':len(cache),
        'pending_s5_classes':len(ordered),
        'priority_manifest_sha256':digest(ordered),
        'priority_worker_sha256':list(map(digest, shards)),
        'worker_reports':len(worker_reports), 'input_rows':stats['rows'],
        'unknown_rows_ignored':stats['unknown_rows'],
        'repeated_consistent_verdicts':stats['repeated_verdicts'],
        'distinct_worker_reported_verdicts':len(verdicts),
        'worker_reported_win5':sum(v == 1 for v in verdicts.values()),
        'worker_reported_loss5':sum(v == 2 for v in verdicts.values()),
        'unreported_s5':len(ordered)-len(verdicts),
        's4_dependency_report':summary,
        'caveat':'No S5, S4, S2 or empty-board outcome is certified by worker reports alone. Independently replay every verdict and audit a complete proof before promotion.'
    }


def self_test():
    a, b, c = (f'{n:032x}' for n in (1, 2, 3))
    assignment = {a:0, b:1}
    def row(k, verdict, nodes=5):
        value = int(k, 16)
        return f's5verdict,{value & ((1<<64)-1)},{value>>64},5,{verdict},{nodes}\n'
    def run(content, worker, previous=None):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'worker.csv'
            path.write_text(content)
            verdicts = {} if previous is None else previous.copy()
            stats = {'rows':0,'unknown_rows':0,'repeated_verdicts':0}
            parse_rows(path, assignment, worker, verdicts, stats, 'fixture')
            return verdicts, stats
    require(run(row(a, 2), 0)[0] == {a:2}, 'LOSS row failed')
    require(run(row(a, 0), 0)[0] == {}, 'UNKNOWN incorrectly promoted')
    require(run(row(a, 2), 0, {a:2})[1]['repeated_verdicts'] == 1,
            'same-verdict retry failed')
    bad = ((row(b, 2), 0), (row(c, 2), 0), (row(a, 1), 0),
           (row(a, 2)+row(a, 2), 0), ('s5verdict,1,0,5,3,0\n', 0),
           ('s5verdict,-1,0,5,2,0\n', 0))
    for content, worker in bad:
        try:
            run(content, worker, {a:2} if content == row(a, 1) else None)
        except ValueError:
            continue
        raise AssertionError('negative fixture accepted: '+repr(content))
    print('SELF_TEST_OK')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', nargs=2, action='append', default=[], metavar=('ID','CSV'))
    parser.add_argument('--existing', type=Path, help='Previously merged partial worker cache (must belong to this exact frontier)')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    workers = []
    for ident, filename in args.worker:
        require(ident in ('0','1','2','3'), 'worker ID must be 0..3')
        workers.append((int(ident), Path(filename)))
    print(json.dumps(audit(workers, args.existing), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('WORKER_AUDIT_REFUSED: '+str(exc), file=sys.stderr)
        sys.exit(1)
