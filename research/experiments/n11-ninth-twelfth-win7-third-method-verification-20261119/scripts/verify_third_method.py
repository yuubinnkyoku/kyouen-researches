#!/usr/bin/env python3
# THIRD-environment / THIRD-method independent verifier for n11-terminal-strategy-v1
# WIN7-D10 certificates (9th..12th = K1057-stranded86 expansion artifacts).
#
# Method (distinct from the two published verifiers):
#   published A: BigInt 3x3 cofactor expansion of the lifted matrix [x^2+y^2,x,y,1]
#   published B: Bareiss 4x4 integer elimination
#   THIS: exact Cramer-rule rational solve of the circle equation, cross-multiplied
#   to one exact integer test W*(s_d-s1)+DD*(x_d-x1)+EE*(y_d-y1)==0 for non-collinear
#   triples, and an exact cross-product line test for collinear triples.
#   Python 3 standard library only; no repo code imported.
#
# Replay protocol (identical semantics to the published verifiers):
#   - every legal loser reply at the 7-stone root starts one subroot at depth 0
#   - winner (even depth) must follow the certificate strategy row for its position
#   - loser (odd depth) expands ALL legal replies
#   - a branch ends at a stuck loser (>=13 stones); the winner must never be stuck
#   - all state-flow counters must then match the published BigInt totals and the
#     published Bareiss per-subroot stats EXACTLY.
import sys, json, hashlib, time

X = [b % 11 for b in range(121)]
Y = [b // 11 for b in range(121)]
S = [X[b]*X[b] + Y[b]*Y[b] for b in range(121)]
FULL = (1 << 121) - 1

_triple_cache = {}

def tmask(a, b, c):
    # banned cells d (!= a,b,c) lying on the unique circle-or-line through a,b,c
    if not (a < b < c):
        s = sorted((a, b, c)); a, b, c = s
    key = (a, b, c)
    r = _triple_cache.get(key)
    if r is not None:
        return r
    x1, y1, s1 = X[a], Y[a], S[a]
    x2, y2, s2 = X[b], Y[b], S[b]
    x3, y3, s3 = X[c], Y[c], S[c]
    A1, B1 = x2 - x1, y2 - y1
    A2, B2 = x3 - x1, y3 - y1
    W = A1 * B2 - A2 * B1
    m = 0
    if W == 0:
        dx, dy = x2 - x1, y2 - y1
        for d in range(121):
            if d == a or d == b or d == c:
                continue
            if dx * (Y[d] - y1) - dy * (X[d] - x1) == 0:
                m |= 1 << d
    else:
        C1, C2 = -(s2 - s1), -(s3 - s1)
        DD = C1 * B2 - C2 * B1   # W*D (circle equation coefficient, cross-multiplied)
        EE = A1 * C2 - A2 * C1   # W*E
        for d in range(121):
            if d == a or d == b or d == c:
                continue
            if W * (S[d] - s1) + DD * (X[d] - x1) + EE * (Y[d] - y1) == 0:
                m |= 1 << d
    _triple_cache[key] = m
    return m

def bits_of(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out

def options_of(points):
    # points: sorted list of bit indices
    banned = 0
    for p in points:
        banned |= 1 << p
    n = len(points)
    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            pj = points[j]
            for k in range(j + 1, n):
                banned |= tmask(pi, pj, points[k])
    return FULL & ~banned

def is_safe(points):
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                tm = tmask(points[i], points[j], points[k])
                for l in range(k + 1, n):
                    if (tm >> points[l]) & 1:
                        return False
    return True

def verify(cert_path, summary_path, bigint_path, bareiss_path, out_path, crosscheck_sample=512):
    import os
    t0 = time.time()
    res = {'schema': 'n11-win7-d10-third-method-verification-20261119-v1',
           'method': 'exact rational circle solve, cross-multiplied; exact line test for collinear triples; python3 stdlib only',
           # record the basename (the published .n11 name) so outputs are
           # reproducible regardless of scratch-directory location
           'cert_path': os.path.basename(cert_path)}

    cert_bytes = open(cert_path, 'rb').read()
    cert_sha = hashlib.sha256(cert_bytes).hexdigest()
    text = cert_bytes.decode('utf-8')
    summary = json.load(open(summary_path))
    bigint = json.load(open(bigint_path))
    blines = [json.loads(l) for l in open(bareiss_path) if l.strip()]
    root_check, bareiss_stats = blines[0], blines[1]

    FAIL = []
    def gate(ok, name, detail=''):
        res.setdefault('gates', []).append({'name': name, 'pass': bool(ok), 'detail': str(detail)})
        if not ok:
            FAIL.append(name)

    gate(cert_sha == summary['certificate_sha256'], 'sha256(cert)==extraction.certificate_sha256', cert_sha)
    gate(cert_sha == bigint.get('certificate_sha256', cert_sha) or 'certificate_sha256' not in bigint, 'bigint record cert sha compat')

    lines = text.split('\n')
    while lines and lines[-1].strip() == '':
        lines.pop()
    gate(lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'header', lines[0][:70])
    rf = lines[1].split()
    gate(len(rf) == 2 and rf[0] == 'root' and len(rf[1]) == 32, 'root line')
    root_hex = rf[1]
    gate(root_hex == summary['root'], 'root==extraction.root')
    root = int(root_hex, 16)

    strategy = {}
    prev = -1
    rows_sorted = True
    for line in lines[2:]:
        parts = line.split()
        if len(parts) != 2:
            gate(False, 'row shape', repr(line)); break
        hexs, mv = parts
        if len(hexs) != 32 or any(c not in '0123456789abcdef' for c in hexs):
            gate(False, 'row hex', line); break
        move = int(mv)
        if not (0 <= move < 121):
            gate(False, 'move range', line); break
        b = int(hexs, 16)
        if b in strategy:
            gate(False, 'duplicate strategy row', line); break
        if b < prev:
            rows_sorted = False
        prev = b
        strategy[b] = move
    n_rows = len(strategy)
    gate(n_rows == len(lines) - 2, 'row count==lines-2')
    gate(n_rows == summary['unique_strategy_rows'], 'rows==extraction.unique_strategy_rows', n_rows)
    gate(n_rows == bigint['strategy_rows'], 'rows==bigint.strategy_rows')
    gate(n_rows == bareiss_stats['rows'], 'rows==bareiss.rows')
    gate(rows_sorted and n_rows == len(lines) - 2, 'rows sorted+unique')

    # ---- method equivalence self-test against BOTH published algebraic routes ----
    # (a) lifted-determinant route (published A formulation, recomputed here independently)
    def det3_lifted(a, b, c, col):
        rows = []
        for p in (a, b, c):
            v = [S[p], X[p], Y[p], 1]
            rows.append([v[i] for i in range(4) if i != col])
        (p, q, r), (s, t, u), (v, w, z) = rows
        return p * (t * z - u * w) - q * (s * z - u * v) + r * (s * w - t * v)
    def forbidden_lifted(a, b, c):
        # cell d banned iff lifted 4x4 det of [S,X,Y,1] rows (a,b,c,d) == 0,
        # expanded along row d: coefficients = signed 3x3 minors of rows a,b,c.
        coeffs = []
        for col in range(4):
            cf = det3_lifted(a, b, c, col)
            coeffs.append(-cf if col % 2 == 0 else cf)
        m = 0
        for d in range(121):
            if d == a or d == b or d == c:
                continue
            if coeffs[0] * S[d] + coeffs[1] * X[d] + coeffs[2] * Y[d] + coeffs[3] == 0:
                m |= 1 << d
        return m
    import random
    rng = random.Random(20261119 + n_rows)
    test_triples = set()
    # deterministic corner cases first: collinear triples both axis-aligned and diagonal
    collinear_sets = [(0, 1, 2), (0, 11, 22), (0, 12, 24), (5, 16, 27), (9, 19, 29), (10, 21, 32), (13, 24, 35), (110, 115, 120), (2, 13, 24), (66, 77, 88)]
    for t in collinear_sets:
        test_triples.add(tuple(sorted(t)))
    while len(test_triples) < crosscheck_sample:
        test_triples.add(tuple(sorted(rng.sample(range(121), 3))))
    mismatches = 0
    for (a, b, c) in sorted(test_triples):
        m1 = tmask(a, b, c)
        m2 = forbidden_lifted(a, b, c)
        if m1 != m2:
            mismatches += 1
    gate(mismatches == 0, 'third-method vs lifted-cofactor method equivalence (%d sampled triples)' % len(test_triples), 'mismatches=%d' % mismatches)

    # ---- root checks ----
    root_points = bits_of(root)
    gate(len(root_points) == 7, 'root has seven stones', len(root_points))
    gate(len(root_points) == root_check['stones'], 'root stones==bareiss root check')
    gate(is_safe(root_points), 'root is safe')
    gate(len(root_points) == bigint['root_stones'], 'root stones==bigint.root_stones')
    root_opts = options_of(root_points)
    root_moves = bits_of(root_opts)
    gate(len(root_moves) == summary['legal_next_moves'], 'root mobility==extraction.legal_next_moves', len(root_moves))
    gate(len(root_moves) == bigint['root_mobility'], 'root mobility==bigint.root_mobility')
    gate(len(root_moves) == root_check['loserMobility'], 'root mobility==bareiss.loserMobility')
    gate(sorted(root_moves) == summary['completed_move_list'], 'mobility bits==completed_move_list')
    gate(len(root_moves) == summary['completed_moves'], 'completed moves==legal moves')

    # ---- replay ----
    opt_cache = {}
    visited_total = 0
    winner_states = 0
    loser_states = 0
    loser_reply_edges = 0
    terminal_count = 0
    min_terminal, max_terminal = 999, 0
    consumed = set()
    per_subroot = {}
    winner_stuck = []
    missing_row = []
    terminal_with_row = []
    illegal_strategy_move = []
    parity_bad = []
    tcache = opt_cache
    for rm in root_moves:
        b0 = root | (1 << rm)
        p0 = sorted(root_points + [rm])
        o0 = options_of(p0)
        opt_cache[b0] = o0
        stack = [(b0, 0, o0, p0)]
        seen = set()
        s_seen = 0; s_terms = 0; s_edges = 0; s_min = 999; s_max = 0
        while stack:
            board, depth, opts, points = stack.pop()
            if board in seen:
                continue
            seen.add(board)
            s_seen += 1
            visited_total += 1
            if opts == 0:
                if depth % 2 != 1:
                    winner_stuck.append('%032x' % board)
                    continue
                if board in strategy:
                    terminal_with_row.append('%032x' % board)
                terminal_count += 1
                s_terms += 1
                nst = len(points)
                s_min = min(s_min, nst); s_max = max(s_max, nst)
                min_terminal = min(min_terminal, nst); max_terminal = max(max_terminal, nst)
                if nst % 2 != 1:
                    parity_bad.append(nst)
                continue
            if depth % 2 == 0:
                winner_states += 1
                mv = strategy.get(board)
                if mv is None:
                    missing_row.append('%032x' % board)
                    continue
                if not ((opts >> mv) & 1):
                    illegal_strategy_move.append(('%032x' % board, mv))
                    continue
                consumed.add(board)
                nb = board | (1 << mv)
                nopts = tcache.get(nb)
                if nopts is None:
                    np_ = points.copy()
                    np_.append(mv); np_.sort()
                    nopts = options_of(np_)
                    tcache[nb] = nopts
                else:
                    np_ = sorted(points + [mv])
                stack.append((nb, depth + 1, nopts, np_))
            else:
                loser_states += 1
                replies = bits_of(opts)
                loser_reply_edges += len(replies)
                s_edges += len(replies)
                for m in replies:
                    nb = board | (1 << m)
                    nopts = tcache.get(nb)
                    if nopts is None:
                        np_ = points.copy()
                        np_.append(m); np_.sort()
                        nopts = options_of(np_)
                        tcache[nb] = nopts
                    else:
                        np_ = sorted(points + [m])
                    stack.append((nb, depth + 1, nopts, np_))
        per_subroot['m%d' % rm] = {'seen': s_seen, 'terminals': s_terms,
                                   'opponentEdges': s_edges, 'range': [s_min, s_max]}

    # ---- union ----
    missing = sorted('%032x' % k for k in strategy.keys() - consumed)
    extra = sorted('%032x' % k for k in consumed - strategy.keys())

    gate(len(winner_stuck) == 0, 'winner never stuck', len(winner_stuck))
    gate(len(missing_row) == 0, 'no missing winner row', len(missing_row))
    gate(len(terminal_with_row) == 0, 'no terminal with strategy row', len(terminal_with_row))
    gate(len(illegal_strategy_move) == 0, 'no illegal strategy move', len(illegal_strategy_move))
    gate(len(parity_bad) == 0, 'terminal stone counts are odd', parity_bad[:5])
    gate(len(missing) == 0, 'strategy/consumed union missing==0', len(missing))
    gate(len(extra) == 0, 'strategy/consumed union extra==0', len(extra))

    # ---- cross-method exact value comparison ----
    gate(visited_total == bigint['visited_states_across_subroots'], 'visited==bigint', visited_total)
    gate(winner_states == bigint['winner_states'], 'winner_states==bigint', winner_states)
    gate(loser_states == bigint['loser_states'], 'loser_states==bigint', loser_states)
    gate(loser_reply_edges == bigint['loser_reply_edges'], 'loser_reply_edges==bigint', loser_reply_edges)
    gate(terminal_count == bigint['terminal_count'], 'terminal_count==bigint', terminal_count)
    gate([min_terminal, max_terminal] == list(bigint['terminal_range']), 'terminal_range==bigint', [min_terminal, max_terminal])
    gate([min_terminal, max_terminal] == list(summary['terminal_stone_range']), 'terminal_range==extraction', [min_terminal, max_terminal])
    gate(13 <= min_terminal and max_terminal <= 17, 'terminal range within depth-10 window 13..17')
    gate(consumed and len(consumed) == bigint['consumed_winner_rows'], 'consumed_winner_rows==bigint', len(consumed))

    bs = bareiss_stats['stats']
    gate(len(bs) == len(per_subroot), 'subroot count==bareiss', len(per_subroot))
    sub_mism = []
    for k, v in per_subroot.items():
        w = bs.get(k)
        if w is None or w['seen'] != v['seen'] or w['terminals'] != v['terminals'] or \
           w['opponentEdges'] != v['opponentEdges'] or list(w['range']) != v['range']:
            sub_mism.append(k)
    gate(len(sub_mism) == 0, 'per-subroot stats==bareiss (all %d subroots)' % len(per_subroot), sub_mism[:10])
    tot_seen = sum(v['seen'] for v in bs.values()); tot_terms = sum(v['terminals'] for v in bs.values())
    tot_edges = sum(v['opponentEdges'] for v in bs.values())
    gate(tot_seen == visited_total and tot_terms == terminal_count and tot_edges == loser_reply_edges,
         'bareiss totals==third replay', (tot_seen, tot_terms, tot_edges))

    res.update({
        'root_hex': root_hex,
        'certificate_sha256': cert_sha,
        'root_stones': len(root_points),
        'root_mobility': len(root_moves),
        'strategy_rows': n_rows,
        'rows_sorted_unique': rows_sorted,
        'subroots_verified': len(per_subroot),
        'visited_states_across_subroots': visited_total,
        'winner_states': winner_states,
        'loser_states': loser_states,
        'loser_reply_edges': loser_reply_edges,
        'terminal_count': terminal_count,
        'terminal_range': [min_terminal, max_terminal],
        'consumed_winner_rows': len(consumed),
        'union_missing': len(missing),
        'union_extra': len(extra),
        'triple_mask_cache_entries': len(_triple_cache),
        'options_cache_entries': len(opt_cache),
        'method_equivalence_sample': len(test_triples),
        'method_equivalence_mismatches': mismatches,
        'bigint_record_matches_exactly': (visited_total == bigint['visited_states_across_subroots'] and
                                          winner_states == bigint['winner_states'] and
                                          loser_states == bigint['loser_states'] and
                                          loser_reply_edges == bigint['loser_reply_edges'] and
                                          terminal_count == bigint['terminal_count'] and
                                          [min_terminal, max_terminal] == list(bigint['terminal_range'])),
        'bareiss_per_subroot_matches_exactly': len(sub_mism) == 0,
        'all_gates_pass': len(FAIL) == 0,
        'failed_gates': FAIL,
        'wall_s': round(time.time() - t0, 1),
    })
    json.dump(res, open(out_path, 'w'), indent=1)
    open(out_path, 'a').write('\n')
    print(json.dumps(res, indent=1))
    return res

if __name__ == '__main__':
    verify(*sys.argv[1:6])
