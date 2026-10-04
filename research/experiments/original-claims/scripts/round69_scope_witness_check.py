"""Recheck original B262/B267/B270/B271 and B291-B300 conditions on n=4.

No legacy verdict is imported. Uses the shared integer geometry engine;
all safe sets, maximal supersets, and actual d(p) are retained.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/research'))
from kyouen_core import board_square, det4


def bits(mask):
    return [p for p in range(16) if mask >> p & 1]


def main():
    b = board_square(4)
    g = b.solve_grundy()
    assert len(g) == 5811 and g[0] == 0 and len(b.quads) == 194
    legal = {s: b.legal_moves(s) for s in g}
    lm = {s: sum(1 << p for p in moves) for s, moves in legal.items()}
    maximal = sorted(s for s in g if not legal[s])
    maxima = [s for s in maximal if s.bit_count() == 7]
    assert len(maximal) == 928 and len(maxima) == 64
    degree = [len(qs) for qs in b.quads_by_pt]
    height = {}
    for s in sorted(g, key=int.bit_count, reverse=True):
        height[s] = max((1 + height[s | (1 << p)] for p in legal[s]), default=0)

    def state(s):
        return {'S': bits(s), 'g': g[s], 'L': legal[s], 'h': height[s]}

    def gain(s, p):
        return lm[s] & ~(1 << p) & ~lm[s | (1 << p)]

    found = {}
    groups = {f'B{i}': {} for i in range(291, 297)}
    group298 = {}
    gain_strata = {}
    permutations = []
    for swap in [False, True]:
        for flipx in [False, True]:
            for flipy in [False, True]:
                perm = []
                for x, y in b.points:
                    if swap:
                        x, y = y, x
                    perm.append((3-x if flipx else x) + 4*(3-y if flipy else y))
                permutations.append(perm)

    def stabilizer(s):
        return sum(sum(1 << perm[p] for p in bits(s)) == s for perm in permutations)

    for s in sorted(g):
        ids, moves, k = bits(s), legal[s], s.bit_count()
        win = [p for p in moves if not g[s | (1 << p)]]
        u = {p: gain(s, p).bit_count() for p in moves}
        if k in [4, 5] and moves:
            key = (k, len(moves), sum(u.values()))
            variance_key = sum(v*v for v in u.values())
            cell = gain_strata.setdefault(key, {}).setdefault(variance_key, [0, 0])
            cell[0] += not bool(g[s])
            cell[1] += 1
        if len(win) == 1 and 'B265' not in found:
            p = win[0]
            smaller = sum(v < u[p] for v in u.values())
            bigger = sum(v > u[p] for v in u.values())
            if smaller >= 2 and bigger >= 2:
                found['B265'] = {**state(s), 'p': p, 'u': u[p], 'smaller': smaller, 'bigger': bigger}
        if g[s] and 'B268' not in found:
            for extra in moves:
                t = s | (1 << extra)
                common = set(moves) & set(legal[t])
                wt = {p for p in common if not g[t | (1 << p)]}
                ws = set(win) & common
                if g[t] and len(common) >= 4 and ws and wt and not ws & wt:
                    found['B268'] = {'S': state(s), 'T': state(t), 'extra': extra, 'common_L': sorted(common), 'winning_common_S': sorted(ws), 'winning_common_T': sorted(wt)}
                    break
        if 'B262' not in found:
            for p, q in combinations(moves, 2):
                t = s | (1 << p)
                if q in legal[t] and u[p] >= 3 and u[q] >= 3 and gain(t, q) == 0:
                    found['B262'] = {**state(s), 'p': p, 'q': q, 'u_p': u[p], 'u_q': u[q], 'u_q_after_p': 0}
                    break
        if height[s] <= 3 and 'B267' not in found:
            for p, q in combinations(moves, 2):
                if gain(s, p) == gain(s, q) and g[s | (1 << p)] != g[s | (1 << q)]:
                    found['B267'] = {**state(s), 'p': p, 'q': q, 'newly_blocked': bits(gain(s, p)), 'g_p': g[s | (1 << p)], 'g_q': g[s | (1 << q)]}
                    break
        if g[s] and 'B270' not in found:
            for p in win:
                for q in moves:
                    if q in legal[s | (1 << p)] and g[s | (1 << q)]:
                        found['B270'] = {**state(s), 'p': p, 'q': q, 'g_p': 0, 'g_q': g[s | (1 << q)], 'g_pq': g[s | (1 << p) | (1 << q)]}
                        break
                if 'B270' in found:
                    break
        if len(win) == 1 and 'B297' not in found:
            p = win[0]
            ds = [degree[q] for q in moves]
            us = list(u.values())
            stabs = {q: stabilizer(s | (1 << q)) for q in moves}
            if min(ds) < degree[p] < max(ds) and min(us) < u[p] < max(us) and min(stabs.values()) < stabs[p] < max(stabs.values()):
                found['B297'] = {**state(s), 'p': p, 'degree': degree[p], 'degree_range': [min(ds), max(ds)], 'u': u[p], 'u_range': [min(us), max(us)], 'stabilizers': stabs}
        if k < 3:
            continue
        ds = tuple(sorted((b.points[p][0]-b.points[q][0])**2 + (b.points[p][1]-b.points[q][1])**2 for p, q in combinations(ids, 2)))
        boundary = tuple(sorted(min(p % 4, 3-p % 4, p // 4, 3-p // 4) for p in ids))
        comp = tuple(sorted(sum(all(q >> p & 1 for p in tri) for q in b.quads) for tri in combinations(ids, 3)))
        dets = [abs(det4(*(b.rows[p] for p in c))) for c in combinations(ids, 4)]
        profile = tuple(sorted(Counter(m.bit_count() for m in maximal if s & m == s).items()))
        subpn = tuple(sum(not g[sum(1 << p for p in c)] for c in combinations(ids, j)) for j in range(1, 4))
        keys = {
            'B292': (k, ds, boundary), 'B293': (k, comp),
            'B294': (k, len(moves), tuple(sorted(len(legal[s | (1 << p)]) for p in moves))),
            'B295': (k, profile), 'B296': (k, subpn),
        }
        if dets:
            assert min(dets) > 0
            keys['B291'] = (k, min(dets), len(moves), sum(degree[p] for p in ids))
        for bid, key in keys.items():
            if bid in found:
                continue
            prev = groups[bid].get(key)
            if prev is not None and bool(g[prev]) != bool(g[s]):
                found[bid] = {'P': state(s if not g[s] else prev), 'N': state(s if g[s] else prev), 'equal_features': key}
            groups[bid].setdefault(key, s)
        key = (k, len(moves))
        mc = sum(s & m == s for m in maxima)
        group298.setdefault(key, []).append((s, mc))

    for pairs in group298.values():
        if 'B298' in found:
            break
        for s, count in pairs:
            if g[s]:
                continue
            for t, count_t in pairs:
                if g[t] and count > count_t and height[s] >= height[t]:
                    found['B298'] = {'P': state(s), 'N': state(t), 'maximum_extensions_P': count, 'maximum_extensions_N': count_t}
                    break
            if 'B298' in found:
                break

    for key, cells in gain_strata.items():
        if 'B269' in found:
            break
        for low, high in combinations(sorted(cells), 2):
            lp, ln = cells[low]
            hp, hn = cells[high]
            if ln >= 10 and hn >= 10 and lp*hn > hp*ln:
                found['B269'] = {'fixed_k_L_sum_u': key, 'lower_sum_u_squared': low, 'higher_sum_u_squared': high, 'lower_variance_P_total': cells[low], 'higher_variance_P_total': cells[high]}
                break

    blocked = 10
    s = sum(1 << p for p in [3, 4, 15])
    @lru_cache(None)
    def blocked_g(t):
        values = {blocked_g(t | (1 << p)) for p in legal[t] if p != blocked}
        value = 0
        while value in values:
            value += 1
        return value
    old = [p for p in legal[s] if not g[s | (1 << p)]]
    new = [p for p in legal[s] if p != blocked and not blocked_g(s | (1 << p))]
    assert blocked in old and g[s] > 0 and blocked_g(s) > 0 and set(new)-set(old)
    found['B299'] = {**state(s), 'blocked': blocked, 'g_after': blocked_g(s), 'old_wins': old, 'new_wins': new, 'reborn': sorted(set(new)-set(old))}

    # Actual depth-d unlabeled legal trees: depth 0 has no additional leaf label.
    sig = {s: 0 for s in g}
    depths = []
    for depth in range(1, 5):
        intern, next_sig, signs, first = {}, {}, {}, {}
        witness = None
        for s in sorted(g):
            key = tuple(sorted(sig[s | (1 << p)] for p in legal[s]))
            code = intern.setdefault(key, len(intern))
            next_sig[s] = code
            if code in signs and signs[code] != bool(g[s]) and witness is None:
                witness = [state(first[code]), state(s)]
            signs.setdefault(code, bool(g[s]))
            first.setdefault(code, s)
        depths.append({'depth': depth, 'classes': len(intern), 'opposite_outcome_witness': witness})
        sig = next_sig
    found['B300_finite_depths'] = depths

    cov = []
    for p, q in combinations(range(16), 2):
        nums = []
        for lam in [1, 64]:
            z = sum(lam**s.bit_count() for s in g)
            wp = sum(lam**s.bit_count() for s in g if s >> p & 1)
            wq = sum(lam**s.bit_count() for s in g if s >> q & 1)
            wpq = sum(lam**s.bit_count() for s in g if s >> p & 1 and s >> q & 1)
            nums.append(wpq*z-wp*wq)
        if nums[0]*nums[1] < 0:
            cov.append({'p': p, 'q': q, 'lambda_values': [1, 64], 'covariance_numerators': nums, 'in_common_quad': any(e >> p & 1 and e >> q & 1 for e in b.quads)})
    found['B271_B272'] = cov[:1]
    assert cov
    output = {'n': 4, 'safe_sets': len(g), 'maximal_sets': len(maximal), 'maximum_sets': len(maxima), 'witnesses': found, 'B297_n4_found': 'B297' in found}
    target = Path(__file__).resolve().parents[1] / 'output/round69_scope_witness_check.json'
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS original conditions rechecked:', ', '.join(found), flush=True)


if __name__ == '__main__':
    main()
