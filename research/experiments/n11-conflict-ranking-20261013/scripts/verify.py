#!/usr/bin/env python3
"""Check ranking with direct D4 containment and explicit replacement plans.

This checker imports no Board, solver, or ranking code. Candidate child widths
are separately checked by the existing translated-determinant C++ executable.
WIN coverage uses D4 images containing each four-stone set, rather than the
ranking producer's canonical-predecessor/Board.children algorithm.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / 'research/experiments/n11-joint-s5-proof-planning-20261012/output'
WIN = ROOT / 'research/experiments/n11-proof-cost-comparison-20261012/output'
QUOT = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output'


def mask(pair):
    return pair[0] | pair[1] << 64


def pair(value):
    return [value & ((1 << 64)-1), value >> 64]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(None)
def images(value):
    result = []
    for reflection in range(2):
        for rotation in range(4):
            out = 0
            for p in range(121):
                if not value >> p & 1:
                    continue
                x, y = p % 11, p // 11
                if reflection:
                    x = 10-x
                for _ in range(rotation):
                    x, y = 10-y, x
                out |= 1 << (y*11+x)
            result.append(out)
    return tuple(result)


def canonical(value):
    return min(images(value))


def legal(value):
    occupied = [p for p in range(121) if value >> p & 1]
    blocked = value
    for a, b, c in combinations(occupied, 3):
        u = (b % 11-a % 11, b // 11-a // 11)
        v = (c % 11-a % 11, c // 11-a // 11)
        uq, vq = u[0]**2+u[1]**2, v[0]**2+v[1]**2
        curve = 0
        for p in range(121):
            w = (p % 11-a % 11, p // 11-a // 11)
            wq = w[0]**2+w[1]**2
            determinant = u[0]*(v[1]*wq-vq*w[1])-u[1]*(v[0]*wq-vq*w[0])+uq*(v[0]*w[1]-v[1]*w[0])
            if determinant == 0:
                curve |= 1 << p
        assert not curve & (value ^ ((1 << a) | (1 << b) | (1 << c)))
        blocked |= curve
    return [p for p in range(121) if not blocked >> p & 1]


def child_contains(s4, s5):
    return any(image & s4 == s4 for image in images(s5))


def ident(entry):
    return entry['first'], entry['reply'], entry['third']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ranking', type=Path, default=EXP / 'output/ranking.json')
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=EXP / 'output/verification.json')
    args = parser.parse_args()
    data = json.loads(args.ranking.read_text())
    for path, expected in data['source_sha256'].items():
        assert sha(ROOT/path) == expected
    assert data['implementation_sha256'] == sha(EXP / 'scripts' / 'rank.py')
    with gzip.open(OLD / 'dependency-graph.json.gz', 'rt') as stream:
        graph = json.load(stream)
    plan = json.loads((QUOT / 'repaired-joint-plan.json').read_text())
    analysis = json.loads((WIN / 'win-side-analysis.json').read_text())
    replies = next(row for row in analysis['firsts'] if row['first'] == 49)['replies']
    cache = {}
    for line in (ROOT / 'research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache').read_text().splitlines():
        if line.startswith('#') or not line.strip():
            continue
        fields = line.split(',')
        value = int(fields[1]) | int(fields[2]) << 64
        cache[value] = int(fields[4])
    for i, verdict in plan['resolved_s5_verdicts'].items():
        cache[mask(graph['s5_masks'][int(i)])] = verdict
    free_s4 = {canonical(value ^ (1 << p)) for value, verdict in cache.items() if verdict == 1
               for p in range(121) if value >> p & 1}
    candidate_masks = {r['s5_index']: mask(r['mask']) for r in data['rows']}
    candidate_usage = defaultdict(list)
    candidate_critical = defaultdict(list)
    candidate_free = defaultdict(list)
    relevant = []
    for reply in replies:
        stored = sorted(mask(m) for m in reply['witness_masks'])
        s3 = (1 << 49) | (1 << reply['reply']) | (1 << reply['chosen_third'])
        fourths = legal(s3)
        assert len(fourths) == reply['chosen_fourths']
        for fourth in fourths:
            s4 = canonical(s3 | 1 << fourth)
            incident = {i for i, value in candidate_masks.items() if child_contains(s4, value)}
            if not incident:
                continue
            covers = [m for m in stored if child_contains(s4, m)]
            already_free = s4 in free_s4
            node = dict(reply=reply['reply'], third=reply['chosen_third'], fourth=fourth,
                        s4_mask=pair(s4), stored_witness_masks=[pair(m) for m in covers],
                        already_known_win=already_free)
            relevant.append(node)
            for i in incident:
                if candidate_masks[i] in covers:
                    candidate_usage[i].append(node)
                    if covers == [candidate_masks[i]] and not already_free:
                        candidate_critical[i].append(node)
                if not already_free:
                    candidate_free[i].append(node)
    # Geometry-first ranking can be checked by C++ without any producer imports.
    lines = [' '.join(map(str, [r['s5_index'], *r['mask'], r['legal'], r['stabilizer_order'],
                               r['canonical_children'], r['canonical_children']])) for r in data['rows']]
    proc = subprocess.run([str(args.binary.resolve())], input='\n'.join(lines)+'\n',
                          text=True, capture_output=True, check=True)
    cpp = json.loads(proc.stdout)
    assert cpp['passed'] and cpp['parents'] == data['candidates'] == 28
    bad = lines[0].split()
    bad[3] = str(int(bad[3])+1)
    rejected = subprocess.run([str(args.binary.resolve())], input=' '.join(bad)+'\n',
                              text=True, capture_output=True)
    assert rejected.returncode != 0 and 'mismatch parent=' in rejected.stderr
    costs = [set(c)-{558600} for c in graph['s4_cost']]
    selected = {ident(e): e['s4_class_index'] for e in plan['groups']}
    options = {(root['origin_first'], root['origin_reply'], row['third']): set(row['options'])
               for root in graph['roots'] if root['role'] != 'known-loss-baseline' for row in root['thirds']}
    pairs = {(root['origin_first'], root['origin_reply']): mask(root['pair_mask']) for root in graph['roots']}
    checks = 0
    for row in data['rows']:
        i = row['s5_index']
        assert row['mask'] == graph['s5_masks'][i]
        l, w = row['loss_plan'], row['fixed_win_cover']
        assert w['witnessed_branches'] == candidate_usage[i]
        assert w['if_loss_uncovered_branches'] == candidate_critical[i]
        assert w['if_win_newly_free_branches'] == candidate_free[i]
        assert w['if_loss_uncovered_replies'] == sorted({r['reply'] for r in candidate_critical[i]})
        assert w['if_win_newly_free_replies'] == sorted({r['reply'] for r in candidate_free[i]})
        assert w['stored_reply_occurrences'] == sorted(r['reply'] for r in replies if row['mask'] in r['witness_masks'])
        invalidated = {s for s, c in enumerate(costs) if i in c}
        affected = sorted(k for k, s in selected.items() if s in invalidated)
        assert l['if_win_invalidated_s4_options'] == sorted(invalidated)
        assert l['if_win_affected_choices'] == [list(k) for k in affected]
        assert l['if_win_invalidated_selected_s4'] == sorted({selected[k] for k in affected})
        assert l['if_win_affected_roots'] == sorted({k[0] for k in affected})
        assert l['if_loss_union_size'] == len(plan['required_new_s5'])-1 == 31635
        replacements = {ident(e): e for e in l['if_win_greedy_replacements']}
        assert set(replacements) == set(affected) and not l['if_win_unrepairable_choices']
        choices = selected.copy()
        for k, entry in replacements.items():
            s = entry['new_s4']
            assert s in options[k] and s not in invalidated and s not in plan['excluded_s4_classes']
            s3 = pairs[k[:2]] | 1 << k[2]
            assert entry['fourth'] in legal(s3)
            assert canonical(s3 | 1 << entry['fourth']) == mask(graph['s4_masks'][s])
            choices[k] = s
            checks += 1
        union = set().union(*(costs[s] for s in choices.values()))
        assert i not in union and len(union) == l['if_win_greedy_repaired_union_size']
        assert len(union)-31636 == l['if_win_greedy_delta']
        score = Fraction(len(affected)+len(candidate_critical[i]), row['canonical_children'])
        assert score == Fraction(**row['impact_score'])
    expected_geometry = sorted(data['rows'], key=lambda r: (r['canonical_children'],
                         -len(r['loss_plan']['if_win_affected_choices']),
                         -len(r['fixed_win_cover']['if_loss_uncovered_branches']), r['s5_index']))
    expected_impact = sorted(data['rows'], key=lambda r: (-Fraction(**r['impact_score']), r['canonical_children'], r['s5_index']))
    assert [r['s5_index'] for r in expected_geometry] == data['geometry_first_order']
    assert [r['s5_index'] for r in expected_impact] == data['impact_per_child_order']
    assert cpp['canonical_child_incidence'] == data['canonical_child_incidence']
    assert cpp['distinct_children'] == data['distinct_s6_children']
    assert cpp['child_parent_multiplicity'] == data['child_parent_multiplicity']
    def damage(row):
        return len(row['loss_plan']['if_win_affected_choices']) + len(row['fixed_win_cover']['if_loss_uncovered_branches'])
    pareto = [r['s5_index'] for r in expected_geometry if not any(
        q['canonical_children'] <= r['canonical_children'] and damage(q) >= damage(r)
        and (q['canonical_children'] < r['canonical_children'] or damage(q) > damage(r))
        for q in data['rows'])]
    assert pareto == data['pareto_children_vs_total_affected']
    out = dict(passed=True, ranking_sha256=sha(args.ranking), verifier_sha256=sha(Path(__file__)),
               cpp_source_sha256=sha(QUOT.parent / 'scripts' / 'verify.cpp'), cpp_binary_sha256=sha(args.binary),
               candidate_count=28, concrete_win_branch_count=sum(r['chosen_fourths'] for r in replies),
               separately_verified_replacement_choices=checks,
               geometry='translated integer determinant C++; direct D4-image containment Python; no Board or solver imports',
               changed_legal_count_rejected=True, cpp_census=cpp)
    args.output.write_text(json.dumps(out, sort_keys=True, indent=2)+'\n')
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
