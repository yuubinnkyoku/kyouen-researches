#!/usr/bin/env python3
"""Independent exact finite audits; standard library only, no random sampling.

The all-graph audit enumerates point-vertex deletion sets. A separate audit
enumerates the actual forbidden-hyperedge game, without domination formulas.
Large-family tables use floating point and are explicitly diagnostic only.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
import math
from pathlib import Path


def graph_data(n, edges):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj, [a.bit_count() for a in adj]


def deletion_records(n, edges):
    adj, deg = graph_data(n, edges)
    full = (1 << n) - 1
    records = []
    for x in range(1 << n):
        if any(x >> v & 1 and not adj[v] & (full ^ x) for v in range(n)):
            continue
        internal = sum(bool(x >> a & 1 and x >> b & 1) for a, b in edges)
        lost = sum(bool(x >> a & 1 or x >> b & 1) for a, b in edges)
        defect = lost - x.bit_count()
        assert defect == sum(deg[v] - 1 for v in range(n) if x >> v & 1) - internal
        unseen, sizes = x, []
        while unseen:
            todo = unseen & -unseen
            component = 0
            while todo:
                bit = todo & -todo
                todo ^= bit
                if component & bit:
                    continue
                component |= bit
                todo |= adj[bit.bit_length() - 1] & x & ~component
            unseen &= ~component
            sizes.append(component.bit_count())
        records.append((x, lost, defect, internal > 0, sizes))
    return records


def exact_audit(n, edges, records, r):
    adj, deg = graph_data(n, edges)
    delta, upper, e = min(deg), max(deg), len(edges)
    powers = [r ** k for k in range(max(sum(deg), e) + 1)]
    center_weights = {x: powers[e - lost] for x, lost, _, _, _ in records}
    center_total = sum(center_weights.values())
    bern_den = math.prod(1 + powers[d] for d in deg)
    bern_weights = {
        x: powers[sum(deg[v] for v in range(n) if not x >> v & 1)]
        for x in range(1 << n)
    }
    assert sum(bern_weights.values()) == bern_den
    tv = Fraction(sum(abs(center_weights.get(x, 0) * bern_den - w * center_total)
                      for x, w in bern_weights.items()), 2 * center_total * bern_den)
    bad = sum(center_weights[x] for x, _, _, is_bad, _ in records if is_bad)
    component_weight = sum(center_weights[x] for x, _, _, _, sizes in records
                           if len(sizes) == 1 and sizes[0] >= 2)
    # Component removal injection and the sharpened activity exponent.
    assert bad * powers[e] <= component_weight * center_total
    for _, lost, _, _, sizes in records:
        if len(sizes) == 1 and sizes[0] >= 2:
            assert lost >= 2 * delta + sizes[0] - 3
    activity_bound = Fraction(n * upper ** 2, powers[2 * delta - 1]) / (1 - Fraction(upper ** 2, r))
    assert Fraction(component_weight, powers[e]) <= activity_bound
    edge_error = sum(Fraction(1, (1 + powers[deg[a]]) * (1 + powers[deg[b]])) for a, b in edges)
    assert tv <= activity_bound + edge_error
    # Push forward by terminal excess, including the one center-free terminal.
    terminal = Counter({e - 1: 1})
    for x, _, defect, _, _ in records:
        terminal[defect] += center_weights[x]
    independent = Counter()
    for x, w in bern_weights.items():
        independent[sum(deg[v] - 1 for v in range(n) if x >> v & 1)] += w
    total = center_total + 1
    terminal_tv = Fraction(sum(abs(terminal[k] * bern_den - independent[k] * total)
                              for k in terminal.keys() | independent.keys()), 2 * total * bern_den)
    assert terminal_tv <= activity_bound + edge_error + Fraction(1, powers[e])
    assert terminal[0] == powers[e]  # no nonempty deletion gives defect zero
    return float(tv), float(terminal_tv), float(activity_bound + edge_error)


def graph_terminal(n, edges, r):
    out = Counter({len(edges) - 1: 1})
    for _, lost, defect, _, _ in deletion_records(n, edges):
        out[defect] += r ** (len(edges) - lost)
    return out


def edge_corrected_audit(n, edges, records, r):
    _, deg = graph_data(n, edges)
    delta, upper, e = min(deg), max(deg), len(edges)
    # Independent Bernoulli variables indexed by vertices AND edges.
    # Factor r**cost + u**jump has probability 1/(1+r**cost) of inclusion.
    polymers = [(1 << v, deg[v], deg[v] - 1) for v in range(n)]
    polymers += [((1 << a) | (1 << b), deg[a] + deg[b] - 1, deg[a] + deg[b] - 3)
                 for a, b in edges]
    independent = Counter({0: 1})
    for _, cost, jump in polymers:
        new = Counter()
        factor = r ** cost
        for k, w in independent.items():
            new[k] += w * factor
            new[k + jump] += w
        independent = new
    denominator = sum(independent.values())
    terminal = Counter({e - 1: 1})
    center_total = big_component_weight = bad = 0
    for _, lost, defect, _, sizes in records:
        weight = r ** (e - lost)
        terminal[defect] += weight
        center_total += weight
        if any(m >= 3 for m in sizes):
            bad += weight
        if len(sizes) == 1 and sizes[0] >= 3:
            assert lost >= 2 * delta + sizes[0] - 3
            big_component_weight += weight
    assert bad * r ** e <= big_component_weight * center_total
    activity_bound = Fraction(n * upper ** 4, r ** (2 * delta)) / (1 - Fraction(upper ** 2, r))
    assert Fraction(big_component_weight, r ** e) <= activity_bound
    incompatibility_bound = Fraction((n + e) * (upper + 1) ** 2, r ** (2 * delta))
    total = center_total + 1
    tv = Fraction(sum(abs(terminal[k] * denominator - independent[k] * total)
                      for k in terminal.keys() | independent.keys()), 2 * total * denominator)
    assert tv <= activity_bound + incompatibility_bound + Fraction(1, r ** e)
    return float(tv)


def direct_hyperedges(n, edges, r):
    """Only forbidden-edge inclusion and maximality; no graph formula."""
    size = 1 + n + r * len(edges)
    forbidden = []
    for j, (a, b) in enumerate(edges):
        h = 1 | (1 << (1 + a)) | (1 << (1 + b))
        for k in range(r):
            h |= 1 << (1 + n + r * j + k)
        forbidden.append(h)
    result = Counter()
    shortest = size - len(edges)
    for s in range(1 << size):
        if any(s & h == h for h in forbidden):
            continue
        if all(s >> v & 1 or any((s | (1 << v)) & h == h for h in forbidden) for v in range(size)):
            result[s.bit_count() - shortest] += 1
    return result, 1 << size


def cycle_transfer(n, r, cutoff, normalized):
    """Trace of a 4-state transfer, checked against direct sets at small n."""
    coeff = [0.0 if normalized else 0] * (cutoff + 1)
    total = 0.0 if normalized else 0
    for start in range(4):
        polynomials = {start: [1] + [0] * cutoff}
        totals = {start: 1}
        for _ in range(n):
            newp, newt = {}, {}
            for state, poly in polynomials.items():
                a, b = state >> 1, state & 1
                for c in (0, 1):
                    if a and b and c:
                        continue
                    nxt = (b << 1) | c
                    w = (1 / r if b or c else 1.0) if normalized else (1 if b or c else r)
                    shift = c * (1 - b)
                    arr = newp.setdefault(nxt, [0] * (cutoff + 1))
                    for k in range(cutoff + 1 - shift):
                        arr[k + shift] += poly[k] * w
                    newt[nxt] = newt.get(nxt, 0) + totals[state] * w
            polynomials, totals = newp, newt
        for k, v in enumerate(polynomials.get(start, [])):
            coeff[k] += v
        total += totals.get(start, 0)
    return coeff, total


def main():
    graphs = rational_checks = hyper_checks = hyper_states = cost_checks = 0
    maximum_tv = maximum_edge_tv = 0.0
    edge_corrected_checks = 0
    for n in range(3, 7):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [ab for j, ab in enumerate(possible) if mask >> j & 1]
            _, deg = graph_data(n, edges)
            if min(deg) < 2:
                continue
            graphs += 1
            records = deletion_records(n, edges)
            cost_checks += sum(len(sizes) == 1 and sizes[0] >= 2 for *_, sizes in records)
            for r in (max(deg) ** 2 + 1, 2 * max(deg) ** 2 + 1):
                tv, _, _ = exact_audit(n, edges, records, r)
                maximum_tv = max(maximum_tv, tv)
                rational_checks += 1
            maximum_edge_tv = max(maximum_edge_tv, edge_corrected_audit(
                n, edges, records, max(deg) ** 2 + 1))
            edge_corrected_checks += 1
            if n <= 4:
                for r in (1, 2):
                    if 1 + n + r * len(edges) <= 17:
                        actual, states = direct_hyperedges(n, edges, r)
                        assert actual == graph_terminal(n, edges, r)
                        hyper_checks += 1
                        hyper_states += states
    transfer_checks = 0
    for n in range(3, 13):
        edges = [(j, (j + 1) % n) for j in range(n)]
        for r in (1, 2, 5):
            coeff, total = cycle_transfer(n, r, n, False)
            direct = graph_terminal(n, edges, r)
            direct[n - 1] -= 1  # transfer counts center-containing only
            assert all(coeff[k] == direct[k] for k in range(n + 1))
            assert total == sum(direct.values())
            transfer_checks += 1
    tables = []
    for r in (5, 10, 20, 40, 80):
        n = r * r
        coeff, total = cycle_transfer(n, r, 20, True)
        center_free = r ** (-n)
        probs = [a / (total + center_free) for a in coeff]
        lam = n / (1 + r * r)
        pois = [math.exp(-lam)]
        for k in range(1, 21):
            pois.append(pois[-1] * lam / k)
        partial = sum(abs(a - b) for a, b in zip(probs, pois)) / 2
        tail = max(0, 1 - sum(probs)) + max(0, 1 - sum(pois))
        bound = n * 4 / (r ** 3 * (1 - 4 / r)) + 2 * n / r ** 4 + center_free
        corrected_lam = lam + n / (1 + r ** 3)
        corrected_pois = [math.exp(-corrected_lam)]
        for k in range(1, 21):
            corrected_pois.append(corrected_pois[-1] * corrected_lam / k)
        corrected_partial = sum(abs(a - b) for a, b in zip(probs, corrected_pois)) / 2
        corrected_tail = max(0, 1 - sum(probs)) + max(0, 1 - sum(corrected_pois))
        corrected_bound = n * 16 / (r ** 4 * (1 - 4 / r)) + (2 * n) * 10 / r ** 4 + center_free
        tables.append(dict(family="cycle", n=n, r=r, q=r + 3, poisson_mean=lam,
                           shortest_probability=probs[0], limit_shortest=math.exp(-1),
                           poisson_tv_interval=[partial, partial + tail / 2],
                           theorem_tv_bound=bound,
                           edge_corrected_poisson_mean=corrected_lam,
                           edge_corrected_tv_interval=[corrected_partial, corrected_partial + corrected_tail / 2],
                           edge_corrected_theorem_bound=corrected_bound))
    for r in (4, 8, 16, 32, 64):
        copies = r ** 3 // 4
        singleton = 4 / r ** 3
        nonsingleton = (6 * r + 4) / r ** 6
        log_z = copies * math.log1p(singleton + nonsingleton)
        # All nontrivial deletions in K4 have defect 3, hence odd.
        odd_probability = -math.expm1(copies * math.log1p(-2 * nonsingleton / (1 + singleton + nonsingleton))) / 2
        tables.append(dict(family="disjoint_K4", n=4 * copies, r=r, q=r + 3,
                           shortest_probability=math.exp(-log_z), limit_shortest=math.exp(-1),
                           odd_excess_probability=odd_probability,
                           edge_corrected_odd_probability=-math.expm1(-2 * (6 * copies) / (1 + r ** 5)) / 2,
                           center_free_probability_upper_bound_log10=-6 * copies * math.log10(r)))
    output = dict(audit="PASS", all_labeled_graphs_min_degree_two_n3_through_n6=graphs,
                  exact_rational_distribution_checks=rational_checks,
                  exact_edge_corrected_distribution_checks=edge_corrected_checks,
                  connected_deletion_cost_checks=cost_checks,
                  direct_hyperedge_checks=hyper_checks, direct_hyperedge_states=hyper_states,
                  independent_integer_cycle_transfer_checks=transfer_checks,
                  largest_exact_deletion_tv=maximum_tv,
                  largest_exact_edge_corrected_bernoulli_tv=maximum_edge_tv,
                  diagnostics_only_floating_point_tables=tables)
    path = Path(__file__).with_name("output") / "audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if not isinstance(v, list)}, indent=2))


if __name__ == "__main__":
    main()
