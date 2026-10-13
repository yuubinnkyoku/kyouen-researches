#!/usr/bin/env python3
"""Bounded minimum-union refinement of the repaired optimistic joint plan.

No game verdict is inferred by this script.  Tracked historical inputs are
read-only.  The output is independently checked against Board geometry and
the explicit old exact-S5 cache plus terminal-verified additions.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / 'research/experiments/n11-joint-s5-proof-planning-20261012/output'
REPAIRED = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output/repaired-joint-plan.json'
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
sys.path.insert(0, str(ROOT / 'research/experiments/n11-central-reply-frontier-20261012/scripts'))
from independent import Board
from analyze_central_reply_frontier import load_exact_s5_cache, CACHE


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log(message):
    print(message, flush=True)


class Instance:
    def __init__(self, graph, verdicts):
        self.graph = graph
        self.verdicts = verdicts
        losses = {i for i, value in verdicts.items() if value == 2}
        wins = {i for i, value in verdicts.items() if value == 1}
        self.cost = [set(row) - losses for row in graph['s4_cost']]
        self.excluded = {s for s, row in enumerate(graph['s4_cost']) if wins.intersection(row)}
        self.groups, self.labels, index = [], [], {}
        self.pairs = {}
        for root in graph['roots']:
            if root['role'] == 'known-loss-baseline':
                continue
            pair = (root['origin_first'], root['origin_reply'])
            self.pairs[pair] = root['pair_mask'][0] | root['pair_mask'][1] << 64
            for row in root['thirds']:
                opts = tuple(s for s in row['options'] if s not in self.excluded)
                assert opts, (pair, row['third'])
                key = frozenset(opts)
                if key not in index:
                    index[key] = len(self.groups)
                    self.groups.append(opts)
                    self.labels.append([])
                self.labels[index[key]].append((*pair, row['third']))
        self.free = [i for i, opts in enumerate(self.groups) if any(not self.cost[s] for s in opts)]
        self.paid = [i for i in range(len(self.groups)) if i not in set(self.free)]
        self.cover = defaultdict(set)
        for i in self.paid:
            for s in self.groups[i]:
                self.cover[s].add(i)
        self.in_play = sorted(self.cover)

    def union(self, assign):
        result = set()
        for s in set(assign[i] for i in self.paid):
            result.update(self.cost[s])
        return result

    def initial(self, entries):
        old = {(e['first'], e['reply'], e['third']): e['s4_class_index'] for e in entries}
        assign = [None] * len(self.groups)
        existing_union = set().union(*(self.cost[s] for s in set(old.values()) if s not in self.excluded))
        missing = []
        for i, labels in enumerate(self.labels):
            candidates = {old[label] for label in labels} - self.excluded
            assert candidates <= set(self.groups[i])
            if i in self.free:
                assign[i] = min(s for s in self.groups[i] if not self.cost[s])
            elif candidates:
                assign[i] = min(candidates, key=lambda s: (len(self.cost[s]), s))
            else:
                missing.append(i)
        if missing:
            assign, union = repair_groups(self, assign, existing_union, missing)
            log(f'overlay repair: {len(missing)} distinct groups -> union {len(union)}')
        else:
            union = self.union(assign)
            assert union <= existing_union
        return assign, union


def refine(inst, assign, union, history, label, passes=6, seed=0):
    rng = random.Random(seed)
    for iteration in range(passes):
        order = list(inst.paid)
        if iteration:
            rng.shuffle(order)
        extra = {s: len(inst.cost[s] - union) for s in inst.in_play}
        out = list(assign)
        accum = set()
        for i in order:
            s = min(inst.groups[i], key=lambda s: (extra[s], len(inst.cost[s] - accum), len(inst.cost[s]), s))
            out[i] = s
            accum.update(inst.cost[s])
        # Retain only nonincreasing steps; equality can expose another choice.
        if len(accum) > len(union):
            break
        changed = out != assign
        before = len(union)
        assign, union = out, accum
        history.append({'phase': label, 'iteration': iteration, 'before': before, 'after': len(union)})
        log(f'{label} pass {iteration}: {before} -> {len(union)}')
        if not changed:
            break
    return assign, union


def greedy(inst, exponent=1.0, seed=0, jitter=0.0):
    """A single reproducible marginal/coverage start, without LP or pool storage."""
    rng = random.Random(seed)
    elem_opts = defaultdict(list)
    for s in inst.in_play:
        for e in inst.cost[s]:
            elem_opts[e].append(s)
    outside = {s: len(inst.cost[s]) for s in inst.in_play}
    live = {s: len(inst.cover[s]) for s in inst.in_play}
    active = set(inst.in_play)
    uncovered = set(inst.paid)
    assign = [None] * len(inst.groups)
    for i in inst.free:
        assign[i] = min(s for s in inst.groups[i] if not inst.cost[s])
    union = set()
    while uncovered:
        s = min(active, key=lambda s: ((outside[s] + jitter * rng.random()) / live[s] ** exponent,
                                      outside[s], -live[s], s))
        fresh = inst.cost[s] - union
        union.update(fresh)
        for e in fresh:
            for other in elem_opts[e]:
                outside[other] -= 1
        for i in inst.cover[s] & uncovered:
            uncovered.remove(i)
            assign[i] = s
            for other in inst.groups[i]:
                live[other] -= 1
                if not live[other]:
                    active.discard(other)
    assert inst.union(assign) == union
    return assign, union


def repair_groups(inst, assign, candidate, missing):
    """Greedy re-cover only groups that are not yet feasible in candidate."""
    out = list(assign)
    todo = set(missing)
    options = {s for i in todo for s in inst.groups[i]}
    while todo:
        best = None
        for s in options:
            covered = inst.cover[s] & todo
            if not covered:
                continue
            fresh = len(inst.cost[s] - candidate)
            key = (fresh / len(covered), fresh, -len(covered), len(inst.cost[s]), s)
            if best is None or key < best[0]:
                best = (key, s, covered)
        assert best is not None
        _, s, covered = best
        candidate.update(inst.cost[s])
        for i in covered:
            out[i] = s
        todo.difference_update(covered)
    assert all(inst.cost[out[i]] <= candidate for i in inst.paid)
    actual = inst.union(out)
    assert actual <= candidate
    return out, actual


def forced_shrink(inst, assign, union, history, passes=3):
    """Keep forced intersections, then repair and explicitly recheck feasibility."""
    for iteration in range(passes):
        forced = set()
        for i in inst.paid:
            options = [inst.cost[s] for s in inst.groups[i] if inst.cost[s] <= union]
            assert options
            inter = set(options[0])
            for option in options[1:]:
                inter.intersection_update(option)
            forced.update(inter)
        out = list(assign)
        missing = []
        forced_size = len(forced)
        for i in inst.paid:
            candidates = [s for s in inst.groups[i] if inst.cost[s] <= forced]
            if candidates:
                out[i] = min(candidates, key=lambda s: (len(inst.cost[s]), s))
            else:
                missing.append(i)
        out, candidate = repair_groups(inst, out, forced, missing)
        before = len(union)
        accepted = len(candidate) < len(union)
        history.append({'phase': 'forced_shrink', 'iteration': iteration, 'before': before,
                        'forced': forced_size, 'repair_groups': len(missing),
                        'candidate': len(candidate), 'accepted': accepted})
        log(f'forced shrink {iteration}: forced {forced_size}, repaired {len(missing)}, candidate {len(candidate)}')
        if not accepted:
            break
        assign, union = out, candidate
    return assign, union


def block_descent(inst, assign, union, history, rounds=3, seed=0):
    """Replace all groups using a selected S4 together, admitting new S5 elements.

    Counting costs by distinct selected S4 makes elements removable only when
    no surviving response needs them.  Every affected group is greedily
    re-covered and the complete union is reconstructed before accepting.
    """
    rng = random.Random(seed)
    for iteration in range(rounds):
        block_groups = defaultdict(set)
        for i in inst.paid:
            block_groups[assign[i]].add(i)
        counts = Counter(e for s in block_groups for e in inst.cost[s])
        order = sorted(block_groups, key=lambda s: (-sum(counts[e] == 1 for e in inst.cost[s]), s))
        if iteration:
            rng.shuffle(order)
        accepted = 0
        for pos, old_s in enumerate(order):
            affected = [i for i in inst.paid if assign[i] == old_s]
            if not affected:
                continue
            selected = set(assign[i] for i in inst.paid)
            counts = Counter(e for s in selected for e in inst.cost[s])
            unique = {e for e in inst.cost[old_s] if counts[e] == 1}
            if not unique:
                continue
            candidate = union - unique
            out, candidate = repair_groups(inst, assign, candidate, affected)
            if len(candidate) < len(union):
                before = len(union)
                history.append({'phase': 'block_descent', 'iteration': iteration, 's4_removed': old_s,
                                'groups_repaired': len(affected), 'exclusive_elements': len(unique),
                                'before': before, 'after': len(candidate)})
                assign, union = out, candidate
                accepted += 1
                log(f'block {iteration}/{pos}: S4 {old_s}, groups {len(affected)}: {before} -> {len(union)}')
        log(f'block round {iteration}: accepted {accepted}, union {len(union)}')
        if not accepted:
            break
    return assign, union


def verify_and_save(inst, assign, union, sources, history, output):
    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, value in inst.verdicts.items():
        key = tuple(inst.graph['s5_masks'][i])
        if key in cache:
            assert cache[key]['verdict'] == value
        cache[key] = {'verdict': value}
    choices = {label: assign[i] for i, labels in enumerate(inst.labels) for label in labels}
    checked = {}
    for pair, mask in inst.pairs.items():
        actual = {label[2] for label in choices if label[:2] == pair}
        expected = set(board.points(board.legal(mask)))
        assert actual == expected and len(actual) == 119
    entries = []
    for label, s in sorted(choices.items()):
        mask = inst.graph['s4_masks'][s][0] | inst.graph['s4_masks'][s][1] << 64
        s3 = inst.pairs[label[:2]] | 1 << label[2]
        witness = next((p for p in board.points(board.legal(s3)) if board.canonical(s3 | 1 << p) == mask), None)
        assert witness is not None, (label, s)
        if s not in checked:
            children = board.children(mask)
            assert all(cache.get((c & ((1 << 64) - 1), c >> 64), {}).get('verdict') != 1 for c in children)
            unknown = {c for c in children if (c & ((1 << 64) - 1), c >> 64) not in cache}
            expected = {inst.graph['s5_masks'][i][0] | inst.graph['s5_masks'][i][1] << 64 for i in inst.cost[s]}
            assert unknown == expected, (s, 'incomplete S5 boundary')
            checked[s] = len(children)
        entries.append({'first': label[0], 'reply': label[1], 'third': label[2], 'fourth': witness,
                        's4_class_index': s, 's4_mask': inst.graph['s4_masks'][s],
                        'unknown_s5_children': len(inst.cost[s])})
    assert set().union(*(inst.cost[e['s4_class_index']] for e in entries)) == union
    out = {'schema': 'n11-refined-joint-plan-v1', 'source_sha256': sources,
           'input_union_size': json.loads(REPAIRED.read_text())['union_size'],
           'union_size': len(union), 'roots': len(inst.pairs), 'third_moves_covered': len(entries),
           'distinct_groups': len(inst.groups), 'free_groups': len(inst.free), 'paid_groups': len(inst.paid),
           'free_thirds': sum(not inst.cost[s] for s in choices.values()),
           'excluded_s4_classes': sorted(inst.excluded), 'resolved_s5_verdicts': inst.verdicts,
           'groups': entries, 'required_new_s5': sorted(union), 'optimization_history': history,
           'verification': {'passed': True, 'checked_selected_s4': len(checked),
                            'complete_third_boundaries': len(inst.pairs), 'complete_s5_boundaries': len(checked),
                            'known_win_selected': 0},
           'trust': 'Optimistic plan only. Old exact-S5 leaves remain solver-trusted; additions are explicit overlay inputs whose source hashes are retained. Remaining required S5 verdicts UNKNOWN. No root proof or optimality claim.'}
    output.write_text(json.dumps(out, sort_keys=True, indent=2) + '\n')
    log(json.dumps({k: out[k] for k in ('union_size', 'roots', 'third_moves_covered', 'verification')}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--block-rounds', type=int, default=3)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--input', type=Path, default=REPAIRED)
    parser.add_argument('--output', type=Path, default=EXP / 'output/refined-joint-plan.json')
    parser.add_argument('--greedy-starts', type=int, default=0,
                        help='bounded fresh greedy starts (0..4), after local refinement')
    parser.add_argument('--overlay', type=Path,
                        help='JSON additions: {resolved_s5_verdicts: {index: verdict}, source_sha256: {path: hash}}')
    args = parser.parse_args()
    started = time.time()
    with gzip.open(OLD / 'dependency-graph.json.gz', 'rt') as stream:
        graph = json.load(stream)
    plan = json.loads(args.input.read_text())
    verdicts = {int(i): v for i, v in plan['resolved_s5_verdicts'].items()}
    sources = {str(p.relative_to(ROOT)): sha(p) for p in (OLD / 'dependency-graph.json.gz', args.input, CACHE)}
    for relative, digest in plan['source_sha256'].items():
        assert sha(ROOT / relative) == digest
        sources[relative] = digest
    if args.overlay:
        overlay = json.loads(args.overlay.read_text())
        for i, value in overlay['resolved_s5_verdicts'].items():
            index = int(i)
            assert value in (1, 2) and 0 <= index < len(graph['s5_masks'])
            assert index not in verdicts or verdicts[index] == value
            verdicts[index] = value
        for relative, digest in overlay['source_sha256'].items():
            assert sha(ROOT / relative) == digest
            sources[relative] = digest
        sources[str(args.overlay.relative_to(ROOT))] = sha(args.overlay)
    inst = Instance(graph, verdicts)
    assign, union = inst.initial(plan['groups'])
    history = [{'phase': 'initial', 'union_size': len(union)}]
    log(f'initial {len(union)}, {len(inst.groups)} groups, {len(inst.paid)} paid')
    assign, union = refine(inst, assign, union, history, 'refine', seed=args.seed)
    assign, union = forced_shrink(inst, assign, union, history)
    assign, union = block_descent(inst, assign, union, history, rounds=args.block_rounds, seed=args.seed)
    starts = [(1.0, 0.0), (0.75, 0.0), (1.25, 0.0), (1.0, 2.0)]
    assert 0 <= args.greedy_starts <= len(starts)
    for pos, (exponent, jitter) in enumerate(starts[:args.greedy_starts]):
        start_assign, start_union = greedy(inst, exponent, args.seed + pos, jitter)
        log(f'greedy {pos}: exponent {exponent}, jitter {jitter}, union {len(start_union)}')
        start_assign, start_union = refine(inst, start_assign, start_union, history, f'greedy_{pos}_refine', seed=args.seed + pos)
        start_assign, start_union = forced_shrink(inst, start_assign, start_union, history, passes=1)
        history.append({'phase': 'greedy', 'start': pos, 'exponent': exponent, 'jitter': jitter,
                        'candidate': len(start_union), 'accepted': len(start_union) < len(union)})
        if len(start_union) < len(union):
            assign, union = start_assign, start_union
            assign, union = block_descent(inst, assign, union, history, rounds=1, seed=args.seed)
    assign, union = refine(inst, assign, union, history, 'final_refine', seed=args.seed)
    history.append({'phase': 'total', 'seconds_before_verification': round(time.time() - started, 3)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    verify_and_save(inst, assign, union, sources, history, args.output)


if __name__ == '__main__':
    main()
