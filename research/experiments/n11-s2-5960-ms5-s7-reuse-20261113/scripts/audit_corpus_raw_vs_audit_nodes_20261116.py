#!/usr/bin/env python3
"""Corpus-wide raw-vs-audit node-sum consistency audit (2026-11-16).

Motivation: the 2026-11-15 concurrent-run race (commit 10b054ef) clobbered
three cost-69h raw batch files on main.  The second independent
verification of the K0863 applicability scan (7c99621f) caught the batch2
bit-set mismatch and the deleted batch3 via its X6 raw/audit bit-set
comparison, but the batch1 clobber was invisible to X6 because the foreign
content kept the same candidate bit set and only the node counts drifted
(+611,900 vs the sweep-audit aggregate).  This audit closes that gap: for
every published sweep-audit JSON it re-derives, from the raw batch files
currently on main, (a) per-batch and total node sums, (b) candidate bit
sets, (c) candidate counts, (d) WIN7 bit sets, and (e) the recorded git
blob sha1s where present, and compares them with the audit's own records.

All five audit schema generations are handled:
  A: .batches[] with file/nodes/candidate_bits           (20 audits)
  B: .batches[] with input_path/candidate_nodes          (69f)
  B': .batches[] with input_path only + .aggregate       (74d/76a/78a)
  C: .batches[] with input_path/git_blob_sha + .sweep_totals  (75e/76d)
  D: .raw_sweep totals + manifest-derived raw file list  (70c)
  E: .raw_batches[] with file/bits + .candidate_nodes_total  (63g/67c)

stdlib only: json, hashlib, sys, os, collections.  Node sums count only
candidate lines (the bit key distinguishes them from pilot control
lines).  Bookkeeping only: REFUTED-D10 is NOT a loss proof and the 11x11
empty board, both two-stone roots, S2 {59,60}, class 1/2/4 remain UNKNOWN.
"""
import json
import hashlib
import os
import sys
from collections import OrderedDict

AUDITS_A = [
    'class2-lane-cost60c-sweep-audit-20261116.json',
    'class2-lane-cost62b-sweep-audit-20261116.json',
    'class2-lane-cost63f-sweep-audit-20261115.json',
    'class2-lane-cost64c-sweep-audit-20261116.json',
    'class2-lane-cost65k-sweep-audit-20261115.json',
    'class2-lane-cost69h-sweep-audit-20261115.json',
    'class2-lane-cost70d-sweep-audit-20261115.json',
    'class2-lane-cost70e-sweep-audit-20261115.json',
    'class2-lane-cost70f-sweep-audit-20261115.json',
    'class2-lane-cost70j-sweep-audit-20261116.json',
    'class2-lane-cost71c-sweep-audit-20261115.json',
    'class2-lane-cost72c-sweep-audit-20261115.json',
    'class2-lane-cost73f-sweep-audit-20261115.json',
    'class2-lane-cost73g-sweep-audit-20261115.json',
    'class2-lane-cost73h-sweep-audit-20261115.json',
    'class2-lane-cost74f-sweep-audit-20261115.json',
    'class2-lane-cost74h-sweep-audit-20261115.json',
    'class4-lane-cost82b-sweep-audit-20261115.json',
    'class4-lane-cost84-sweep-audit-20261115.json',
    'class4-lane-cost87-raw-sweep-audit-20261116.json',
]
AUDIT_B = 'class2-lane-cost69f-sweep-audit-20261115.json'
AUDITS_B2 = [
    'class2-lane-cost74d-sweep-audit-20261115.json',
    'class2-lane-cost76a-sweep-audit-20261115.json',
    'class2-lane-cost78a-sweep-audit-20261115.json',
]
AUDITS_C = [
    'class2-lane-cost75e-sweep-audit-20261116.json',
    'class2-lane-cost76d-sweep-audit-20261116.json',
]
AUDIT_D = 'class2-lane-cost70c-raw-sweep-audit-20261115.json'
D_RAW_PATTERN_PREFIX = 'class2-lane-cost70c-raw-batch'
AUDITS_E = [
    'class2-lane-cost63g-sweep-audit-20261115.json',
    'class2-lane-cost67c-sweep-audit-20261115.json',
]


def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def cand_rows(rows):
    return [r for r in rows if 'bit' in r]


def blob_sha1(path):
    with open(path, 'rb') as f:
        data = f.read()
    h = hashlib.sha1()
    h.update(b'blob %d' % len(data))
    h.update(bytes([0]))
    h.update(data)
    return h.hexdigest()


def check_schema_a(d, report):
    for an in AUDITS_A:
        audit = json.load(open(os.path.join(d, an)))
        entry = {'schema': 'A', 'batches': 0, 'checks': 0}
        for b in audit['batches']:
            fn = b['file']
            rows = cand_rows(load_jsonl(os.path.join(d, fn)))
            got = sum(r['nodes'] for r in rows)
            assert got == b['nodes'], (an, fn, b['nodes'], got)
            got_bits = sorted(r['bit'] for r in rows)
            exp_bits = sorted(b.get('candidate_bits', b.get('bits', [])))
            assert got_bits == exp_bits, (an, fn, 'bit set')
            entry['batches'] += 1
            entry['checks'] += 2
        report[an] = entry


def check_schema_b(d, report):
    audit = json.load(open(os.path.join(d, AUDIT_B)))
    entry = {'schema': 'B', 'batches': 0, 'checks': 0}
    for b in audit['batches']:
        fn = b['input_path'].split('/')[-1]
        rows = cand_rows(load_jsonl(os.path.join(d, fn)))
        got = sum(r['nodes'] for r in rows)
        assert got == b['candidate_nodes'], (AUDIT_B, fn, b['candidate_nodes'], got)
        got_bits = sorted(r['bit'] for r in rows)
        assert got_bits == sorted(b['candidate_bits']), (AUDIT_B, fn, 'bit set')
        entry['batches'] += 1
        entry['checks'] += 2
    agg = audit['aggregate']
    total = sum(b['candidate_nodes'] for b in audit['batches'])
    assert total == agg['candidate_nodes'], (AUDIT_B, 'total')
    entry['checks'] += 1
    report[AUDIT_B] = entry


def check_schema_b2(d, report):
    for an in AUDITS_B2:
        audit = json.load(open(os.path.join(d, an)))
        entry = {'schema': "B'", 'batches': 0, 'checks': 0}
        total = 0
        seen = set()
        for b in audit['batches']:
            fn = b['input_path'].split('/')[-1]
            rows = cand_rows(load_jsonl(os.path.join(d, fn)))
            total += sum(r['nodes'] for r in rows)
            seen.update(r['bit'] for r in rows)
            got_bits = sorted(r['bit'] for r in rows)
            assert got_bits == sorted(b['candidate_bits']), (an, fn, 'bit set')
            entry['batches'] += 1
            entry['checks'] += 1
        agg = audit['aggregate']
        assert total == agg['candidate_nodes'], (an, 'total', agg['candidate_nodes'], total)
        assert len(seen) == agg['candidates'], (an, 'candidates')
        entry['checks'] += 2
        report[an] = entry


def check_schema_c(d, report):
    for an in AUDITS_C:
        audit = json.load(open(os.path.join(d, an)))
        entry = {'schema': 'C', 'batches': 0, 'checks': 0}
        total = 0
        seen = set()
        for b in audit['batches']:
            fn = b['input_path'].split('/')[-1]
            rows = cand_rows(load_jsonl(os.path.join(d, fn)))
            total += sum(r['nodes'] for r in rows)
            seen.update(r['bit'] for r in rows)
            if 'git_blob_sha' in b:
                assert blob_sha1(os.path.join(d, fn)) == b['git_blob_sha'], (an, fn, 'blob sha')
                entry['checks'] += 1
            entry['batches'] += 1
        st = audit['sweep_totals']
        assert total == st['node_sum'], (an, 'node_sum', st['node_sum'], total)
        assert len(seen) == st['candidates'], (an, 'candidates')
        win_got = set()
        for b in audit['batches']:
            fn = b['input_path'].split('/')[-1]
            win_got.update(r['bit'] for r in cand_rows(load_jsonl(os.path.join(d, fn))) if r['loss'] is True)
        assert sorted(win_got) == sorted(st['win7_d10_bits']), (an, 'win bits')
        entry['checks'] += 2 + 1
        report[an] = entry


def check_schema_d(d, report):
    audit = json.load(open(os.path.join(d, AUDIT_D)))
    entry = {'schema': 'D', 'batches': 0, 'checks': 0}
    raws = sorted(fn for fn in os.listdir(d) if fn.startswith(D_RAW_PATTERN_PREFIX) and fn.endswith('.jsonl'))
    total = 0
    seen = set()
    win_got = set()
    for fn in raws:
        rows = cand_rows(load_jsonl(os.path.join(d, fn)))
        total += sum(r['nodes'] for r in rows)
        seen.update(r['bit'] for r in rows)
        win_got.update(r['bit'] for r in rows if r['loss'] is True)
        entry['batches'] += 1
    rs = audit['raw_sweep']
    assert total == rs['total_search_nodes'], (AUDIT_D, 'total', rs['total_search_nodes'], total)
    assert len(seen) == rs['unique_candidate_bits'], (AUDIT_D, 'unique bits')
    assert sorted(win_got) == sorted(rs['win7_bits']), (AUDIT_D, 'win bits')
    entry['checks'] += 3
    report[AUDIT_D] = entry


def check_schema_e(d, report):
    for an in AUDITS_E:
        audit = json.load(open(os.path.join(d, an)))
        entry = {'schema': 'E', 'batches': 0, 'checks': 0}
        total = 0
        seen = set()
        for b in audit['raw_batches']:
            fn = b['file']
            rows = cand_rows(load_jsonl(os.path.join(d, fn)))
            total += sum(r['nodes'] for r in rows)
            seen.update(r['bit'] for r in rows)
            got_bits = sorted(r['bit'] for r in rows)
            assert got_bits == sorted(b['bits']), (an, fn, 'bit set')
            entry['batches'] += 1
            entry['checks'] += 1
        assert total == audit['candidate_nodes_total'], (an, 'total', audit['candidate_nodes_total'], total)
        assert len(seen) == audit['candidates'], (an, 'candidates')
        entry['checks'] += 2
        report[an] = entry


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    report = OrderedDict()
    check_schema_a(d, report)
    check_schema_b(d, report)
    check_schema_b2(d, report)
    check_schema_c(d, report)
    check_schema_d(d, report)
    check_schema_e(d, report)
    total_batches = sum(v['batches'] for v in report.values())
    total_checks = sum(v['checks'] for v in report.values())
    out = OrderedDict([
        ('schema', 'n11-corpus-raw-vs-audit-node-sum-audit-20261116-v1'),
        ('date', '2026-11-16'),
        ('method', 'independent stdlib re-derivation from the raw batch jsonl files on current main: per-batch and total node sums, candidate bit sets, candidate counts, WIN7 bit sets, and recorded git blob sha1s, compared against every published sweep-audit JSON (5 schema generations)'),
        ('audits_checked', len(report)),
        ('raw_batches_checked', total_batches),
        ('checks_passed', total_checks),
        ('mismatches', 0),
        ('motivation', 'the 2026-11-15 concurrent-run race (10b054ef) drifted cost-69h batch1 node totals by +611,900 while keeping the bit set, which the X6 bit-set comparison of the second independent verification could not see; this node-sum audit closes that detection gap corpus-wide'),
        ('per_audit', report),
        ('unknown_status', 'bookkeeping only; REFUTED-D10 is NOT a loss proof; the 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1/2/4 all remain UNKNOWN'),
    ])
    outp = os.path.join(d, 'corpus-raw-vs-audit-node-sum-audit-20261116.json')
    with open(outp, 'w') as f:
        json.dump(out, f, indent=1)
        f.write(chr(10))
    print('audits:', len(report), 'batches:', total_batches, 'checks:', total_checks, 'mismatches: 0')
    print('written', outp)


if __name__ == '__main__':
    main()
