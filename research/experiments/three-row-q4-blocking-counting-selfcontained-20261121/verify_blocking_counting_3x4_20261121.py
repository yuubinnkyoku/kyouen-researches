#!/usr/bin/env python3
"""verify_blocking_counting_3x4_20261121.py -- fail-closed machine verifier for
the self-contained blocking-counting class bounds theorem (3 x m slab, q = 4).

Theorem under verification
-------------------------
Board: 3 x m integer slab, rows y in {0,1,2}, cells x in {0..m-1}.
Win sets: 4 points on a common circle or common line. Row capacity q-1 = 3:
no safe configuration has a row with 4 stones (row-line win), so row stone
counts live in {0,1,2,3}^3. def-mode (row-deficient maximal safe) = maximal
safe config with some row holding <= 2 stones, profile (r0,r1,r2) != (3,3,3).

Blocking bookkeeping (every fact re-derived and re-checked by this verifier):
  * An empty cell on a deficient row i (r_i <= 2) cannot be blocked by that
    row's horizontal line (r_i + 1 <= 3 < 4) and cannot be blocked by a
    non-horizontal line (<= 1 slab point per row line => <= 3 slab points on
    a 3-row board, so such a line through the cell carries <= 2 stones).
    (A 3-stone line object from collinear stones automatically never covers a
    deficient-row empty cell: its one point on each row IS the stone.)
  * Hence every empty cell of every deficient row lies on a blocker CIRCLE
    that also contains >= 3 stones of S.
  * A circle meets any horizontal row line in <= 2 points, so a blocker
    circle with u_i stones on row i has <= 2 - u_i non-stone intersections
    with that row line (relevant hits); intersections outside the board only
    weaken it; an intersection at a stone is not an empty cell.
  * Counting blocker circles by their stones: a circle through >= 3 stones of
    S contributes >= 1 stone triple, and a stone triple determines at most
    one object (3 non-collinear points determine a unique circle). Summing
    relevance caps over ALL stone triples T (u_i(T) := stones of T on row i;
    triples with 3 stones of one row reduce to that row's line, which covers
    no deficient-row cell and contributes 0):

        demand = sum_{i def} (m - r_i)
               <= sum_T sum_{i def} max(0, 2 - u_i(T)) =: CAPS(r0,r1,r2)

    (For safe S the per-object count needs no safety input; every blocker
    object's hits are bounded by the cap of any of its triples. Safety is
    used only to bound profiles to r_i <= 3.)
  * Solving for m: m <= floor((CAPS + sum_{i def} r_i) / |def rows|), and the
    value depends only on the sorted class (row positions immaterial: any
    horizontal line behaves identically). CAPS = 0 => impossible for m >= 1.

Gates (all must pass; audit is written only on full pass):
  g_pin      : sha256 pins of input records (byte-identical copies of
               published repo artifacts shipped next to this script).
  g_table    : CAPS re-derived by two independent implementations
               (closed-form multiplicities vs literal stone-combination
               enumeration); class bounds compared to the embedded table;
               floor arithmetic; class maximum must be 68.
  g_curves   : independent exact-integer curve enumeration (3 row lines +
               all circles with >= 4 cells) vs published counts m=4..8.
  g_enum     : independent safety-pruned DFS over all safe sets, m=4..8, vs
               published maximal_by_size / maximal_row_profiles /
               deficient_maximal / P_m_true (geometry re-implemented; the
               published artifacts come from the pinned brute JSONs).
  g_account  : exact per-witness cap-accounting on EVERY def-mode maximal
               safe config found at m=4..8 (integer circle objects through
               every stone triple): blocker-circle coverage of all
               deficient-row empty cells, per-triple relevance caps 2 - u_i,
               demand <= observed relevant sum <= CAPS, m <= B(class),
               plus a no-4-stones-on-one-object safety re-check.
  g_witness23: same exact accounting on the published m=23 SAT witnesses
               (frontier records copy + enumeration-lane m=23 Y=0 family
               witnesses copy): safety, plain-board maximality, and the
               demand <= 66 / m <= 68 consistency for class {2,3,3}.

Usage: python3 verify_blocking_counting_3x4_20261121.py [--tamper]
Exit 0 + output/audit.json written iff ALL gates pass. Exit 1, no audit
write, on any failure. Deterministic: no wall clock, no randomness, sorted
iteration everywhere; audit bytes are environment-independent.
"""
import hashlib
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, 'output')
AUDIT = os.path.join(OUTDIR, 'audit.json')

W, Q = 3, 4

# ---------------------------------------------------------------------------
# pinned inputs: byte-identical copies of published repo artifacts.
# sha256 pins (not the historical md5s: this verifier pins its own copies).
# ---------------------------------------------------------------------------
PIN_WITNESS_SOURCE = 'frontier_records_m23_copy.jsonl'
PIN_M23_FAMILY = 'm23_Y0_witnesses_copy.jsonl'

PIN_ME = {
    'brute_3x4_4.json': '914069e135b4b40f23caa6f2095633948769af80b837378f6b25bbe60801e7bb',
    'brute_3x5_4.json': '5618bb61ce0fb878cb9f349660c238165e57cdabbec71334270e6a7d6808bdfd',
    'brute_3x6_4.json': '847afbed5ad61541de458c34b39c9c1b70e7cfff12d52114c4b3c9292b63ede1',
    'brute_3x7_4.json': '38ce7156a38a22508533b3d3a12dc735804159bc6d0228297d5790bcbf153c71',
    'brute_3x8_4.json': '70fa1727c045ace08261a454c81aa8b88d979b1672ff27c9ed5e0f4c5ad6773b',
    # byte-copy of research/experiments/three-row-q4-frontier-20261121/output/
    # records.jsonl at repo commit 13098121 (2026-11-21T10:47Z)
    PIN_WITNESS_SOURCE: '5d908d40a6e5bf235f6cacc220f487ca1f8c7cd39517b989faa1774076662b90',
    # byte-copy of the enumeration-lane published m=23 family Y=0 witnesses
    PIN_M23_FAMILY: '4448d0d85de01333391f95b40920153a0dffc8ae75fbe188c111ca0743c90731',
}

# embedded expected aggregates, machine-extracted from the pinned published
# JSONs (compared at run time against a live parse of the same pins AND
# against the independent recomputation below).
EXPECTED_BRUTE = {
    4: {'curves': 29, 'deficient_maximal': 182, 'maximal_by_size': {'5': 104, '6': 78}},
    5: {'curves': 50, 'deficient_maximal': 674, 'maximal_by_size': {'5': 64, '6': 530, '7': 80}},
    6: {'curves': 86, 'deficient_maximal': 1724,
        'maximal_by_size': {'5': 4, '6': 648, '7': 964, '8': 108}},
    7: {'curves': 141, 'deficient_maximal': 4607,
        'maximal_by_size': {'5': 1, '6': 240, '7': 2982, '8': 1384, '9': 64}},
    8: {'curves': 221, 'deficient_maximal': 11542,
        'maximal_by_size': {'5': 2, '6': 56, '7': 3768, '8': 7716, '9': 976}},
}

# expected class-bound table, sorted class -> bound (0 = impossible).
EXPECTED_TABLE = {
    (0, 0, 0): 0, (0, 0, 1): 0, (0, 0, 2): 0, (0, 0, 3): 0, (0, 1, 1): 0,
    (0, 1, 2): 2, (1, 1, 1): 2,
    (0, 1, 3): 5, (0, 2, 2): 5, (1, 1, 2): 5,
    (0, 2, 3): 13, (1, 1, 3): 13,
    (1, 2, 2): 11,
    (1, 2, 3): 24,
    (2, 2, 2): 22,
    (0, 3, 3): 36,
    (2, 2, 3): 40,
    (1, 3, 3): 52,
    (2, 3, 3): 68,
}

TAMPER = '--tamper' in sys.argv

gates = []


def gate(name, ok, detail=''):
    if not ok:
        print(f'GATE FAILED g_{name}: {detail}')
        print(f'STOPPED after {len(gates) + 1} gate(s); {len(gates)} passed '
              f'before failure. No audit written.')
        sys.exit(1)
    gates.append((name, detail))
    print(f'  g_{name} PASS  ({detail})')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def die(msg):
    print(f'FATAL: {msg}')
    sys.exit(1)


# ===========================================================================
# g_pin
# ===========================================================================
def run_pins():
    for fn, want in sorted(PIN_ME.items()):
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            die(f'missing pinned input {fn}')
        got = sha(p)
        if got != want:
            gate('pin', False, f'{fn}: sha256 {got[:12]}... != pinned {want[:12]}...')
    gate('pin', True, f'{len(PIN_ME)} pinned records sha-verified')


# ===========================================================================
# cap table: two independent implementations
# ===========================================================================
def caps_closed_form(r, defrows):
    caps = 0
    comps = {}
    for u in itertools.product(range(r[0] + 1), range(r[1] + 1), range(r[2] + 1)):
        if sum(u) != 3 or max(u) > 2:
            continue
        mult = math.comb(r[0], u[0]) * math.comb(r[1], u[1]) * math.comb(r[2], u[2])
        if mult == 0:
            continue
        cap = sum(max(0, 2 - u[i]) for i in defrows)
        comps[u] = (mult, cap)
        caps += mult * cap
    return caps, comps


def caps_literal(r, defrows):
    stones = []
    for i in range(3):
        stones += [i] * r[i]
    caps = 0
    for T in itertools.combinations(range(len(stones)), 3):
        u = [0, 0, 0]
        for t in T:
            u[stones[t]] += 1
        if max(u) > 2:
            continue
        caps += sum(max(0, 2 - u[i]) for i in defrows)
    return caps


def class_bound(r):
    """r: profile (not class). Returns (bound, caps, d, sum_r)."""
    defrows = [i for i in range(3) if r[i] <= Q - 2]
    d = len(defrows)
    if d == 0:
        return None, 0, 0, 0      # not a def profile
    caps, comps = caps_closed_form(r, defrows)
    sum_r = sum(r[i] for i in defrows)
    if caps == 0:
        return 0, caps, d, sum_r   # impossible for m >= 1
    return (caps + sum_r) // d, caps, d, sum_r


def run_table():
    table = {}   # class -> bound
    rows = []
    for r in itertools.product(range(4), repeat=3):
        if r == (3, 3, 3):
            continue
        b, caps, d, sum_r, = class_bound(r)
        defrows = [i for i in range(3) if r[i] <= Q - 2]
        _, comps = caps_closed_form(r, defrows)
        lit = caps_literal(r, defrows)
        if lit != caps:
            gate('table', False, f'profile {r}: closed-form CAPS {caps} != literal {lit}')
        if d and (caps + sum_r) % d:
            if ((caps + sum_r) // d) * d + ((caps + sum_r) % d) != caps + sum_r:
                gate('table', False, f'floor arithmetic broke for {r}')
        cls = tuple(sorted(r))
        table.setdefault(cls, set()).add(b)
        rows.append({'profile': list(r), 'class': list(cls), 'caps': caps,
                     'def_rows': d, 'sum_def_r': sum_r, 'bound': b})
    for cls, v in table.items():
        if len(v) != 1:
            gate('table', False, f'bound not position-independent for {cls}: {v}')
    final = {cls: list(v)[0] for cls, v in table.items()}
    if final != EXPECTED_TABLE:
        diff = {k: (final.get(k), EXPECTED_TABLE.get(k)) for k in
                set(final) | set(EXPECTED_TABLE) if final.get(k) != EXPECTED_TABLE.get(k)}
        gate('table', False, f'class table mismatch: {diff}')
    assert len(final) == 19   # 20 multisets of size 3 over {0..3} minus (3,3,3)
    # spot re-derivations for the six dominant classes (caps recomputed from
    # the printed compositions in the README table):
    for r, want_caps in (((2, 3, 3), 66), ((1, 3, 3), 51), ((0, 3, 3), 36),
                         ((3, 2, 2), 76), ((1, 2, 3), 46), ((2, 2, 2), 60)):
        b, caps, d, sum_r = class_bound(r)
        if caps != want_caps:
            gate('table', False, f'CAPS spot-check {r}: {caps} != {want_caps}')
    classmax = max(final.values())
    impossible = sorted(cls for cls, b in final.items() if b == 0)
    gate('table', True, f'19 classes; CAPS x-checked closed-form/literal; '
                        f'max bound {classmax}; impossible: '
                        f'{[list(c) for c in impossible]}')
    return final


# ===========================================================================
# exact integer geometry (independent third implementation)
# ===========================================================================
def circle_or_line(p1, p2, p3):
    """Object through 3 distinct integer points.
    ('circle', (K, A, B, C)): K*(x^2+y^2)+A*x+B*y+C = 0, K > 0, gcd-normalized.
    ('line', (a, b, c)): a*x+b*y+c = 0, gcd- and sign-normalized.
    None for degenerate input."""
    if p1 == p2 or p1 == p3 or p2 == p3:
        return None
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    dx12, dy12 = x2 - x1, y2 - y1
    dx13, dy13 = x3 - x1, y3 - y1
    if dx12 * dy13 - dy12 * dx13 == 0:
        a, b, c = dy12, x1 - x2, (x2 - x1) * y1 - (y2 - y1) * x1
        # a*x + b*y + c = 0; check both anchor points:
        assert a * x1 + b * y1 + c == 0 and a * x2 + b * y2 + c == 0 and a * x3 + b * y3 + c == 0
        g = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
        a, b, c = a // g, b // g, c // g
        if a < 0 or (a == 0 and b < 0):
            a, b, c = -a, -b, -c
        return ('line', (a, b, c))
    # circle x^2+y^2+D*x+E*Y+F = 0; solve linear system via Cramer.
    m = ((x1, y1, 1), (x2, y2, 1), (x3, y3, 1))
    rhs = (-(x1 * x1 + y1 * y1), -(x2 * x2 + y2 * y2), -(x3 * x3 + y3 * y3))
    def det3(m_):
        return (m_[0][0] * (m_[1][1] * m_[2][2] - m_[1][2] * m_[2][1])
                - m_[0][1] * (m_[1][0] * m_[2][2] - m_[1][2] * m_[2][0])
                + m_[0][2] * (m_[1][0] * m_[2][1] - m_[1][1] * m_[2][0]))
    mD = ((rhs[0], y1, 1), (rhs[1], y2, 1), (rhs[2], y3, 1))
    mE = ((x1, rhs[0], 1), (x2, rhs[1], 1), (x3, rhs[2], 1))
    mF = ((x1, y1, rhs[0]), (x2, y2, rhs[1]), (x3, y3, rhs[2]))
    det = det3(m)
    K = -det
    A, B, C = -det3(mD), -det3(mE), -det3(mF)
    assert K != 0
    g = math.gcd(math.gcd(math.gcd(abs(K) or 1, abs(A)), abs(B)), abs(C)) or 1
    K, A, B, C = K // g, A // g, B // g, C // g
    if K < 0:
        K, A, B, C = -K, -A, -B, -C
    # verify anchors:
    for (x, y) in (p1, p2, p3):
        assert K * (x * x + y * y) + A * x + B * y + C == 0
    return ('circle', (K, A, B, C))


def obj_cells(obj, m):
    """All board cells on the object, sorted."""
    kind, co = obj
    cells = []
    if kind == 'line':
        a, b, c = co
        for y in range(W):
            for x in range(m):
                if a * x + b * y + c == 0:
                    cells.append((x, y))
        return sorted(cells)
    K, A, B, C = co
    # K*x^2 + A*x + (K*y^2 + B*y + C) = 0
    for y in range(W):
        c1 = K * y * y + B * y + C
        disc = A * A - 4 * K * c1
        if disc < 0:
            continue
        s = math.isqrt(disc)
        if s * s != disc:
            continue
        for num in ({-A + s} | ({-A - s} if s else set())):
            if num % (2 * K) == 0:
                x = num // (2 * K)
                if 0 <= x < m:
                    cells.append((x, y))
    return sorted(cells)


def enumerate_curves(m):
    """Every >=4-cell win object: 3 row lines + all circles with >= 4 cells.
    Returns sorted list of ('row'/'circle', key, cells-tuple)."""
    curves = []
    seen = {}
    circles = {}
    for y in range(W):
        curves.append(('row', (0, y), tuple((x, y) for x in range(m))))
    pts = [(x, y) for y in range(W) for x in range(m)]
    for tri in itertools.combinations(pts, 3):
        obj = circle_or_line(*tri)
        if obj is None or obj[0] != 'circle':
            continue
        co = obj[1]
        if co in circles:
            continue
        cells = tuple(obj_cells(obj, m))
        if len(cells) >= Q:
            circles[co] = cells
    for co, cells in circles.items():
        curves.append(('circle', co, cells))
    curves.sort(key=lambda c: (c[0], repr(c[1])))
    return curves


# ===========================================================================
# g_curves + g_enum: independent DFS search, m = 4..8
# ===========================================================================
CAPS_LOOKUP = {}   # profile -> (bound, caps) filled at start


def run_curves_and_enum():
    results = {}
    for m in (4, 5, 6, 7, 8):
        curves = enumerate_curves(m)
        pts = [(x, y) for y in range(W) for x in range(m)]
        index_of = {p: i for i, p in enumerate(pts)}
        cover = [[] for _ in range(len(pts))]
        for ci, cu in enumerate(curves):
            for cell in cu[2]:
                cover[index_of[cell]].append(ci)

        with open(os.path.join(HERE, f'brute_3x{m}_4.json')) as f:
            pub = json.load(f)
        exp = EXPECTED_BRUTE[m]
        if pub['curves'] != exp['curves']:
            gate('curves', False, f'm={m}: embedded expected curves inconsistent '
                                  f'with pinned file')
        if pub['deficient_maximal'] != exp['deficient_maximal']:
            gate('curves', False, f'm={m}: embedded expected def total inconsistent '
                                  f'with pinned file')
        if pub['maximal_by_size'] != exp['maximal_by_size']:
            gate('curves', False, f'm={m}: embedded expected maximal_by_size '
                                  f'inconsistent with pinned file')
        if len(curves) != pub['curves']:
            gate('curves', False, f'm={m}: curve count {len(curves)} != '
                                  f'published {pub["curves"]}')

        max_by_size = {}
        max_by_profile = {}
        def_total = 0
        def_witnesses = []
        n = len(pts)
        rows_of = [p[1] for p in pts]
        count_curves = [0] * len(curves)
        sel = []
        sel_set = set()
        n_safe = 0
        n_scanned = 0

        def classify():
            nonlocal def_total, n_safe, n_scanned
            n_safe += 1
            # cheap necessary condition from the counting theorem itself:
            # demand <= CAPS(profile). Sound pruning only (a false prune
            # would break the match against the published independent
            # enumeration).
            rc = [0] * W
            for i in sel:
                rc[rows_of[i]] += 1
            key = (rc[0], rc[1], rc[2])
            capsrec = CAPS_LOOKUP.get(key)
            if capsrec is None:
                return                      # (3,3,3): rare, fall through below
            bound, caps, d, sum_r = capsrec
            if d and (d * m - sum_r) > caps:
                return
            if d == 0 and min(rc) <= Q - 2:
                die('CAPS_LOOKUP inconsistent')
            n_scanned += 1
            # maximality: every non-stone cell covered by some curve with
            # >= q-1 stones
            for i in range(n):
                if i in sel_set:
                    continue
                blocked = False
                for ci in cover[i]:
                    if count_curves[ci] >= Q - 1:
                        blocked = True
                        break
                if not blocked:
                    return
            pr = tuple(rc)
            max_by_profile[pr] = max_by_profile.get(pr, 0) + 1
            max_by_size[len(sel)] = max_by_size.get(len(sel), 0) + 1
            if min(rc) <= Q - 2:
                def_total += 1
                def_witnesses.append(sorted(pts[i] for i in sel))

        def dfs(start):
            for i in range(start, n):
                ok = True
                for ci in cover[i]:
                    if count_curves[ci] == Q - 1:
                        ok = False
                        break
                if not ok:
                    continue
                for ci in cover[i]:
                    count_curves[ci] += 1
                sel.append(i)
                sel_set.add(i)
                classify()
                dfs(i + 1)
                sel.pop()
                sel_set.remove(i)
                for ci in cover[i]:
                    count_curves[ci] -= 1

        # empty set is itself a safe set (never maximal for m >= 1: no
        # blockers), consistent with brute34 which counts it in safe_sets but
        # never as maximal; we do not need safe_sets matching, so skip.
        dfs(0)

        got_size = {str(k): v for k, v in sorted(max_by_size.items())}
        if got_size != pub['maximal_by_size']:
            gate('enum', False, f'm={m}: maximal_by_size {got_size} != '
                                f'published {pub["maximal_by_size"]}')
        pub_prof = {_parse_profile_key(k): v for k, v in
                    pub['maximal_row_profiles'].items()}
        if max_by_profile != pub_prof:
            diff = {k: (max_by_profile.get(k), pub_prof.get(k)) for k in
                    set(max_by_profile) | set(pub_prof)
                    if max_by_profile.get(k) != pub_prof.get(k)}
            gate('enum', False, f'm={m}: maximal_row_profiles mismatch: {diff}')
        if def_total != pub['deficient_maximal']:
            gate('enum', False, f'm={m}: deficient_maximal {def_total} != '
                                f'{pub["deficient_maximal"]}')
        if (def_total == 0) != pub['P_m_true']:
            gate('enum', False, f'm={m}: P(m) mismatch')
        results[m] = {'curves': len(curves), 'def_total': def_total,
                      'safe_sets': n_safe, 'scanned': n_scanned,
                      'profiles': len(max_by_profile),
                      'witnesses': def_witnesses}
    gate('curves', True, 'm=4..8 curve counts 29/50/86/141/221 match published')
    tot = sum(r['def_total'] for r in results.values())
    gate('enum', True, f'm=4..8: deficient totals 182/674/1724/4607/11542 = '
                      f'{tot} match published; profiles and P(m) match')
    return results


def _parse_profile_key(k):
    return tuple(int(t) for t in k.strip('()').split(','))   # int() tolerates spaces


# ===========================================================================
# g_account: exact per-witness cap accounting
# ===========================================================================
def account_witness(stones, m):
    """Exact blocking-bookkeeping check of one def-mode maximal safe config.
    Returns (ok, info-or-error)."""
    stones = sorted(tuple(s) for s in stones)
    sset = set(stones)
    if len(sset) != len(stones):
        return False, 'duplicate stones'
    off = [p for p in stones if not (0 <= p[0] < m and 0 <= p[1] < W)]
    if off:
        return False, f'off-board stones {off}'
    rc = [0] * W
    for (x, y) in stones:
        rc[y] += 1
    if max(rc) > Q - 1 or min(rc) > Q - 2:
        return False, f'row counts {rc} not a def profile'
    prof = (rc[0], rc[1], rc[2])
    bound, caps, d, sum_r = CAPS_LOOKUP[prof]
    if bound == 0:
        return False, f'impossible class {sorted(prof)}'
    if m > bound:
        return False, f'm={m} exceeds class bound {bound} ({sorted(prof)})'
    defrows = [i for i in range(W) if rc[i] <= Q - 2]
    # demand cells: empty cells of deficient rows
    demand_cells = set()
    for i in defrows:
        for x in range(m):
            if (x, i) not in sset:
                demand_cells.add((x, i))
    demand = len(demand_cells)
    if demand != sum(m - rc[i] for i in defrows):
        return False, 'demand bookkeeping'
    covered = set()
    relevant_total = 0
    nobjects = 0
    for tri in itertools.combinations(stones, 3):
        u = [0, 0, 0]
        for p in tri:
            u[p[1]] += 1
        obj = circle_or_line(*tri)
        if obj is None:
            return False, f'degenerate triple {tri}'
        cells = obj_cells(obj, m)
        # safety re-check: no object may hold >= 4 stones
        nons = 0
        for c in cells:
            if c in sset:
                nons += 1
        if nons >= Q:
            return False, f'object through {tri} holds {nons} stones (win set)'
        # relevance caps per deficient row
        for i in defrows:
            rel = 0
            for c in cells:
                if c[1] == i and c not in sset:
                    rel += 1
            if rel > 2 - u[i]:
                return False, (f'object {tri} row {i}: {rel} relevant hits '
                              f'> cap {2 - u[i]}')
        relall = 0
        for c in cells:
            if c in demand_cells:
                relall += 1
                covered.add(c)
        relevant_total += relall
        nobjects += 1
    if covered != demand_cells:
        missing = sorted(demand_cells - covered)
        return False, f'{len(missing)} uncovered deficient-row cells, ' \
                      f'e.g. {missing[:3]}'
    if demand > relevant_total:
        return False, f'demand {demand} > observed relevant {relevant_total}'
    if relevant_total > caps:
        return False, f'observed relevant {relevant_total} > CAPS {caps}'
    info = {'profile': list(prof), 'class': sorted(prof), 'bound': bound,
            'caps': caps, 'demand': demand, 'relevant_observed': relevant_total,
            'objects': nobjects}
    return True, info


def run_account(enum_results):
    checked = 0
    by_class = {}
    for m in sorted(enum_results):
        for stones in enum_results[m]['witnesses']:
            ok, info = account_witness(stones, m)
            if not ok:
                gate('account', False, f'm={m} witness {stones}: {info}')
            checked += 1
            key = tuple(info['class'])
            rec = by_class.setdefault(key, {'checked': 0, 'max_relevant': 0,
                                             'max_demand': 0, 'caps': info['caps']})
            rec['checked'] += 1
            rec['max_relevant'] = max(rec['max_relevant'], info['relevant_observed'])
            rec['max_demand'] = max(rec['max_demand'], info['demand'])
    gate('account', True, f'{checked} def witnesses (m=4..8) pass exact '
                          f'cap accounting; {len(by_class)} classes exercised')
    return checked, by_class


# ===========================================================================
# g_witness23
# ===========================================================================
def coord_to_stones(s):
    return sorted(tuple(int(v) for v in pair.split(':')) for pair in s.split(','))


def run_witness23():
    wit = set()
    with open(os.path.join(HERE, PIN_WITNESS_SOURCE)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get('m') == 23 and d.get('verdict') == 'SAT' and 'witness_coord' in d:
                wit.add(tuple(coord_to_stones(d['witness_coord'])))
    with open(os.path.join(HERE, PIN_M23_FAMILY)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if 'witness' in d:
                wit.add(tuple(sorted(tuple(p) for p in d['witness'])))
            elif 'stones' in d:
                wit.add(tuple(sorted(tuple(p) for p in d['stones'])))
    checked = 0
    for stones in sorted(wit):
        ok, info = account_witness(stones, 23)
        if not ok:
            gate('witness23', False, f'm=23 witness {stones}: {info}')
        checked += 1
        if tuple(info['class']) != (2, 3, 3):
            gate('witness23', False,
                 f'witness {stones}: class {info["class"]} != (2,3,3)')
        if info['caps'] != 66:
            gate('witness23', False, f'caps {info["caps"]} != 66')
        if info['demand'] != 21:
            gate('witness23', False, f'demand {info["demand"]} != 21')
    if checked < 4:
        gate('witness23', False, f'only {checked} distinct published m=23 '
                                 f'witnesses found (need >= 4)')
    gate('witness23', True, f'{checked} published m=23 witnesses: safety, '
                            f'plain-board maximality, coverage, 21 <= '
                            f'relevant <= 66, m=23 <= 68')


# ===========================================================================
def main():
    print('verify_blocking_counting_3x4_20261121 starting')
    print(f'input dir: {HERE}')
    if TAMPER:
        print('TAMPER MODE: negative control (expected table falsified)')
    run_pins()
    for r in itertools.product(range(4), repeat=3):
        CAPS_LOOKUP[r] = class_bound(r)
    if TAMPER:
        EXPECTED_TABLE[(2, 3, 3)] = 67      # unsound over-tightening
    table = run_table()
    if TAMPER:
        die('tamper handler unreachable (table gate must fail first)')
    enum_results = run_curves_and_enum()
    checked, by_class = run_account(enum_results)
    run_witness23()

    audit = {
        'theorem': '3xm q=4 blocking-counting class bounds (self-contained)',
        'board': 'rows y in {0,1,2}, cells x in {0..m-1}; '
                 'win = 4 points on a common circle or line',
        'class_bounds': {str(list(k)): v for k, v in sorted(table.items())},
        'class_max': max(table.values()),
        'corollary': 'any def-mode maximal safe config on 3xm has m <= 68; '
                     'to decide P(m) for 32 <= m <= 68 only classes '
                     '{0,3,3}<=36, {1,3,3}<=52, {2,3,3}<=68 and {2,2,3}<=40 '
                     'can host witnesses',
        'gates': [{'name': n, 'detail': d} for n, d in gates],
        'n_gates': len(gates),
        'enum': {str(m): {'curves': r['curves'], 'def_total': r['def_total'],
                         'safe_sets_visited': r['safe_sets'],
                         'maximality_scans': r['scanned'],
                         'maximal_profiles': r['profiles']}
                 for m, r in sorted(enum_results.items())},
        'account': {'witnesses_checked': checked,
                    'by_class': {str(list(k)): v for k, v in sorted(by_class.items())}},
        'pins': dict(sorted(PIN_ME.items())),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(AUDIT, 'w') as f:
        json.dump(audit, f, sort_keys=True, indent=1, ensure_ascii=False)
        f.write('\n')
    print(f'ALL {len(gates)} GATES PASS')
    print(f'audit written: {AUDIT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
