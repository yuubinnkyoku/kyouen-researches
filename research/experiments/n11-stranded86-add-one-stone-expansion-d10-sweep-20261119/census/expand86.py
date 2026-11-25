#!/usr/bin/env python3
# Receipt-aware exact cover re-SOLVE (resolve2) for the five-parent head-1410 target
# union after the 4th/5th/6th WIN7-D10 receipt folds (C/D/E): the three published
# receipt roots become known-WIN, their closed target rows leave the residual, and a
# fresh minimum candidate cover is recomputed over the 87 residual target rows.
# Mirrors audit_refuted_excluded_cover_resolve_20261119.mjs (resolve1); additionally
# ingests the 28-root witness sweep verdict records (when present) so the remaining
# untested witness roots leave the eligible pool as REFUTED-D10.
# Usage: python3 resolve2.py [--with-sweep]
import json, sys, hashlib, time

W = '/home/user/work'

def need(ok, m):
    if not ok:
        print('GATE FAILED:', m)
        sys.exit(1)

def blob_sha(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n

TF = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10 - y, x
        elif t == 2: X, Y = 10 - x, 10 - y
        elif t == 3: X, Y = y, 10 - x
        elif t == 4: X, Y = 10 - x, y
        elif t == 5: X, Y = x, 10 - y
        elif t == 6: X, Y = y, x
        else: X, Y = 10 - y, 10 - x
        tab.append(11 * Y + X)
    TF.append(tab)

def bits_of(mask):
    out = []
    p = 0
    while mask:
        if mask & 1: out.append(p)
        mask >>= 1
        p += 1
    return out

def transform(mask, t):
    out = 0
    for p in bits_of(mask):
        out |= 1 << TF[t][p]
    return out

def canon_int(mask):
    best = None
    for t in range(8):
        z = transform(mask, t)
        if best is None or z < best: best = z
    return best

def canon_hex(mask):
    return format(canon_int(mask), '032x')

def det3(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    q1 = x1*x1 + y1*y1; q2 = x2*x2 + y2*y2; q3 = x3*x3 + y3*y3
    return q1*(x2*y3 - x3*y2) - q2*(x1*y3 - x3*y1) + q3*(x1*y2 - x2*y1)

def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)

# ---------- blossom maximum matching (port of the published mjs) ----------
def maximum_matching(g):
    n = len(g)
    match = [-1]*n
    p = [0]*n; base = [0]*n; used = [False]*n; blossom = [False]*n
    def lca(a, b):
        seen = [False]*n
        while True:
            a = base[a]; seen[a] = True
            if match[a] == -1: break
            a = p[match[a]]
        while True:
            b = base[b]
            if seen[b]: return b
            b = p[match[b]]
    def mark_path(v, b, child):
        while base[v] != b:
            blossom[base[v]] = True
            blossom[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]
    def find_path(root):
        for i in range(n): used[i] = False; p[i] = -1; base[i] = i
        q = [root]; used[root] = True
        qi = 0
        while qi < len(q):
            v = q[qi]; qi += 1
            for u in g[v]:
                if base[v] == base[u] or match[v] == u: continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    b = lca(v, u)
                    for i in range(n): blossom[i] = False
                    mark_path(v, b, u); mark_path(u, b, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = b
                            if not used[i]:
                                used[i] = True; q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1: return u
                    m = match[u]; used[m] = True; q.append(m)
        return -1
    for i in range(n):
        if match[i] == -1:
            v = find_path(i)
            while v != -1:
                pv = p[v]
                nv = match[pv] if pv != -1 else -1
                match[v] = pv
                if pv != -1: match[pv] = v
                v = nv
    return sum(1 for x in match if x != -1) // 2, match

def load(rel):
    return json.load(open(f'{W}/{rel}'))

# ---------- original verdict join (verbatim gates, from resolve1) ----------
joint = load('inputs/joint.json')
audit = load('inputs/audit.json')
head = load('inputs/head1476.json')
globalFold = load('inputs/globalFold.json')
fold78 = load('inputs/previousCostFold.json')
c78 = load('inputs/cost78c.json'); c79 = load('inputs/cost79c.json'); c73 = load('inputs/cost73j.json')
need(audit['all_pass'] is True and audit['check_count'] == 23 and audit['derived']['maximum_root_span'] == 2, 'independent audit gate')
need(len(joint['derived']['joint_results']) == 31 and joint['all_pass'] is True, 'joint gate')
targetRows = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(targetRows) == 112, 'target rows 112')
globalRows = set(x['row_hex'] for x in globalFold['receipts_by_row'])
laterRows = set(x['row_hex'] for x in fold78['new_receipt_coverage']['receipts_by_row'])
globalHits = [h for h in targetRows if h in globalRows]
laterHits = [h for h in targetRows if h in laterRows]
need(len(globalHits) == 13 and len(laterHits) == 2, 'previous receipt overlap 13+2')
knownRefuted, knownWin = set(), set()
for x in head['candidate_root_universe']['matched_roots']:
    if x['verdict'] == 'REFUTED-D10': knownRefuted.add(x['d4_canon_root'])
    elif x['verdict'] == 'WIN7-D10': knownWin.add(x['d4_canon_root'])
for c in (c78, c79):
    for x in (c.get('transfers') or {}).values():
        if x['verdict'] == 'REFUTED-D10': knownRefuted.add(x['root_canon'])
        elif x['verdict'] == 'WIN7-D10': knownWin.add(x['root_canon'])
    for bit in (c.get('actual_execution', {}).get('refuted_d10_bits') or []):
        knownRefuted.add(canon_hex(int(c['s6_child'], 16) | (1 << bit)))
    for bit in (c.get('actual_execution', {}).get('win7_d10_bits') or []):
        knownWin.add(canon_hex(int(c['s6_child'], 16) | (1 << bit)))
for x in (c73.get('transfers') or {}).values():
    if x['verdict'] == 'REFUTED-D10': knownRefuted.add(x['root_canon'])
    elif x['verdict'] == 'WIN7-D10': knownWin.add(x['root_canon'])
c73Wins = set(c73['actual_execution']['results']['win7_d10_bits'])
for bit in c73['engine_candidate_bits']['open_bits']:
    root = canon_hex(int(c73['s6_child'], 16) | (1 << bit))
    if bit in c73Wins: knownWin.add(root)
    else: knownRefuted.add(root)
for row in globalFold['receipts_by_row']:
    for x in row['receipts']: knownWin.add(canon_hex(int(x['root'], 16)))
for row in fold78['new_receipt_coverage']['receipts_by_row']:
    for x in row['receipts']: knownWin.add(canon_hex(int(x['root'], 16)))
for x in fold78['new_receipt_coverage']['marginal_by_root']:
    knownWin.add(canon_hex(int(x['root'], 16)))
ext_refuted_before = len(knownRefuted); ext_win_before = len(knownWin)
need(ext_refuted_before == 236 and ext_win_before == 156, f'enumerated verdict-source totals {ext_refuted_before}/{ext_win_before}')
# sweep48 verdicts (46 refuted + 2 win) and receipts
sweep = load('ex48/output/sweep48.json')
need(sweep['status'] == 'sweep-complete' and sweep['classification']['counted_roots'] == 48, 'sweep json gate')
need(len(sweep['classification']['ordering_conflicts']) == 0, 'sweep conflicts')
for r in sweep['classification']['refuted_d10']['roots']: knownRefuted.add(r)
for r in sweep['classification']['win7_d10']['roots']: knownWin.add(r)
# first + second/third receipts folded as known WIN (resolve1 chain) — plus C/D/E
# (the second/third receipts are exactly the sweep48 WIN roots and were just added)
import tarfile
firstFold = None
with tarfile.open(f'{W}/inputs/firstFoldTarball.tar.gz', 'r:gz') as t:
    for m in t.getmembers():
        if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
            firstFold = json.load(t.extractfile(m))
knownWin.add(canon_hex(int(firstFold['root']['hex'], 16)))
foldv2 = load('foldv2/output/fourth-fifth-sixth-win7-receipt-fold-20261119.json')
need(foldv2['status'] == 'fold-complete' and foldv2['receipt_count'] == 3, 'fold v2 gate')
NEW_RECEIPTS = [r['root'] for r in foldv2['receipts']]
for root in NEW_RECEIPTS:
    knownWin.add(canon_hex(int(root, 16)))
# seventh receipt fold (G) and the sweep35 verdict ingestion (resolve3 additions)
fold7 = load('foldv2/output/seventh-win7-receipt-fold-20261119.json')
need(fold7['status'] == 'fold-complete' and fold7['receipt_count'] == 1, 'fold7 gate')
for r in fold7['receipts']:
    knownWin.add(canon_hex(int(r['root'], 16)))
# eighth receipt fold (H) and the sweep6 verdict ingestion (resolve4 additions)
fold8 = load('foldv2/output/eighth-win7-receipt-fold-20261119.json')
need(fold8['status'] == 'fold-complete' and fold8['receipt_count'] == 1, 'fold8 gate')
for r in fold8['receipts']:
    knownWin.add(canon_hex(int(r['root'], 16)))
s35 = load('sweep35/output/eligible-29-candidate-root-depth10-sweep-20261119.json')
need(s35['status'] == 'sweep-complete' and s35['classification']['counted_roots'] == 29
     and s35['classification']['win7_d10']['count'] == 1 and s35['classification']['refuted_d10']['count'] == 28
     and s35['classification']['capped']['count'] == 0 and len(s35['classification']['ordering_conflicts']) == 0, 'sweep35 gate')
for r in s35['classification']['refuted_d10']['roots']: knownRefuted.add(r)
for r in s35['classification']['win7_d10']['roots']: knownWin.add(r)
KNOWN_G = s35['classification']['win7_d10']['roots'][0]
need(KNOWN_G == '00000000040080801202000000100000' and
     fold7['receipts'][0]['root'] == KNOWN_G, 'sweep35 WIN must be the folded seventh root')
# sweep6: the six zero-cover eligible candidates judged at depth 10 (this run)
roots6 = json.load(open(f'{W}/sweep6/roots.json'))
recs6 = []
import glob as _glob
for f in sorted(_glob.glob(f'{W}/sweep6/output/probe-records-w*.jsonl')):
    for line in open(f):
        recs6.append(json.loads(line))
by_root6 = {}
for x in recs6:
    by_root6.setdefault(x['root'], []).append(x)
need(len(by_root6) == 6, 'sweep6 must cover exactly the 6 candidates')
sweep6_add = {'refuted': [], 'win': [], 'capped': [], 'timeout': [], 'missing': []}
for item in roots6:
    root = item['root']
    rs = by_root6.get(root, [])
    probes = [x for x in rs if 'result' in x and x.get('error') is None]
    need(len(probes) == 2, 'sweep6 root needs both orderings: ' + root)
    ctrl_ok = all(x.get('control', {}).get('nodes') == 3402 and x['control']['loss'] is False for x in rs)
    need(ctrl_ok, 'sweep6 pilot control gate: ' + root)
    uncapped = [x for x in probes if not x['result']['capped']]
    need(len(uncapped) == 2, 'sweep6 root must complete uncapped: ' + root)
    any_win = any(x['result']['loss'] is True for x in uncapped)
    any_ref = any(x['result']['loss'] is False for x in uncapped)
    need(not (any_win and any_ref), 'sweep6 win/refuted conflict: ' + root)
    if any_win:
        knownWin.add(root); sweep6_add['win'].append(root)
    else:
        need(any_ref, 'sweep6 verdict undefined: ' + root)
        knownRefuted.add(root); sweep6_add['refuted'].append(root)
need(len(sweep6_add['win']) == 1 and len(sweep6_add['refuted']) == 5, 'sweep6 verdict 1 WIN / 5 REFUTED')
KNOWN_H = sweep6_add['win'][0]
need(KNOWN_H == '00000000040000801202000000100001' and
     fold8['receipts'][0]['root'] == KNOWN_H, 'sweep6 WIN must be the folded eighth root')

# ---------- optional: ingest the 28-root witness sweep verdicts ----------
with_sweep = '--with-sweep' in sys.argv
sweep28_add = {'refuted': [], 'win': [], 'capped': [], 'timeout': [], 'missing': []}
if with_sweep:
    roots28 = json.load(open(f'{W}/sweep28/roots.json'))
    recs = []
    import glob
    for f in sorted(glob.glob(f'{W}/sweep28/output/probe-records-w*.jsonl')):
        for line in open(f):
            recs.append(json.loads(line))
    by_root = {}
    for x in recs:
        by_root.setdefault(x['root'], []).append(x)
    for item in roots28:
        root = item['root']
        if root in NEW_RECEIPTS: continue
        rs = by_root.get(root, [])
        probes = [x for x in rs if 'result' in x and x.get('error') is None]
        if len(probes) < 2:
            sweep28_add['missing'].append(root); continue
        ctrl_ok = all(x.get('control', {}).get('nodes') == 3402 and x['control']['loss'] is False for x in rs)
        if not ctrl_ok:
            sweep28_add['timeout'].append(root); continue
        res_by_ord = {}
        capped = {}
        for x in rs:
            if 'result' not in x:
                continue
            key = ('uncapped' if not x['result']['capped'] else 'capped', x['result']['loss'])
            res_by_ord.setdefault(x['ordering'], []).append(key)
        # official rule (sweep48 classification_rule): WIN7-D10 = uncapped loss=true in >=1 ordering;
        # REFUTED-D10 = uncapped loss=false in >=1 ordering and no uncapped WIN.
        any_uncapped_win = any(k[0] == 'uncapped' and k[1] is True for v in res_by_ord.values() for k in v)
        any_uncapped_nowin = any(k[0] == 'uncapped' and k[1] is False for v in res_by_ord.values() for k in v)
        conflict = any(k[0] == 'uncapped' and k[1] is False for v in res_by_ord.values() for k in v if k[1] is True) and False
        # WIN/REFUTED conflict is impossible per-run (loss is boolean per ordering); cross-order conflict
        # would mean one ordering uncapped-win and the other uncapped-refuted:
        has_unc_win_in_ord = {o: any(k[0] == 'uncapped' and k[1] for k in v) for o, v in res_by_ord.items()}
        has_unc_ref_in_ord = {o: any(k[0] == 'uncapped' and not k[1] for k in v) for o, v in res_by_ord.items()}
        if any(has_unc_win_in_ord.get(o, False) and has_unc_ref_in_ord.get(o, False) for o in res_by_ord):
            sweep28_add['timeout'].append(root); continue
        if any_uncapped_win:
            verdict = 'WIN7-D10'
        elif any_uncapped_nowin:
            verdict = 'REFUTED-D10'
        else:
            verdict = 'CAPPED'
        if verdict == 'WIN7-D10':
            knownWin.add(root); sweep28_add['win'].append(root)
        elif verdict == 'REFUTED-D10':
            knownRefuted.add(root); sweep28_add['refuted'].append(root)
        else:
            sweep28_add['capped'].append(root)

# ---------- residual after all six receipts ----------
closedAll = set(globalHits) | set(laterHits)
firstTarget = firstFold['root']['covered_five_parent_target_rows']
need(len(firstTarget) == 2, 'first fold target rows')
stf = load('ex48/output/secondThirdFold.json')
myTarget = []
for r in stf['receipts']: myTarget.extend(r['covered_five_parent_target_rows'])
need(len(myTarget) == 4, 'second/third fold target rows 4')
newTarget = foldv2['five_parent_residual_cover_after']['fourth_fifth_sixth_target_rows']
need(len(newTarget) == 4, 'fold v2 target rows 4')
for h in firstTarget + myTarget + newTarget:
    need(h in set(targetRows), 'fold target row not in target union: ' + h)
closedAll |= set(firstTarget) | set(myTarget) | set(newTarget)
for r in fold7['receipts']:
    for h in r['covered_five_parent_target_rows']:
        need(h in set(targetRows), 'fold7 target row not in target union: ' + h)
        need(h not in closedAll, 'fold7 target row closed twice: ' + h)
        closedAll.add(h)
for r in fold8['receipts']:
    for h in r['covered_five_parent_target_rows']:
        need(h in set(targetRows), 'fold8 target row not in target union: ' + h)
        need(h not in closedAll, 'fold8 target row closed twice: ' + h)
        closedAll.add(h)
need(len(closedAll) == 26, 'total closed target rows 26 (6+7+8 receipts), got %d' % len(closedAll))
residualRows = [h for h in targetRows if h not in closedAll]
need(len(residualRows) == 86, 'residual rows after eight receipts: %d' % len(residualRows))
residualSet = set(residualRows)

# ---------- pool: original 117 candidates minus known verdicts ----------
pool = set(canon_hex(int(x['root'], 16)) for x in audit['derived']['witness_pairs'])
for subset in joint['derived']['joint_results']:
    for root in subset['witness_roots']: pool.add(canon_hex(int(root, 16)))
need(len(pool) == 117, 'pool size 117')
res1 = load('ex48/output/cover49.json')
publishedWitness = set(x['root'] for x in res1['witness'])
for r in publishedWitness: need(r in pool, 'witness root not in pool: ' + r)
poolWinNow = sorted(x for x in pool if x in knownWin)
need(len(poolWinNow) == 8, 'eight WIN receipt roots in pool, got %d' % len(poolWinNow))
poolRefutedNow = sorted(x for x in pool if x in knownRefuted)
candidates = sorted(x for x in pool if x not in knownRefuted and x not in knownWin)
need(len(poolRefutedNow) == 109, 'pool REFUTED-D10 count 109, got %d' % len(poolRefutedNow))
need(len(candidates) == 0, 'pool must be fully depth-10 judged, got %d untested' % len(candidates))
need(117 == len(poolRefutedNow) + len(poolWinNow), 'pool partition 109+8')


# ================= add-one-stone expansion for the 86 stranded rows =================
residualSet = set(residualRows)
need(len(residualRows) == 86, 'residual rows 86')

def stones_and_safety(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    if len(pts) != 7:
        return pts, None
    unsafe = 0
    for a in range(7):
        for b in range(a+1, 7):
            for c in range(b+1, 7):
                for d in range(c+1, 7):
                    if det4(pts[a], pts[b], pts[c], pts[d]) == 0:
                        unsafe += 1
    return pts, unsafe

def coverage_of(mask, universal=None):
    covered = set()
    for t in range(8):
        image = transform(mask, t)
        for bit in bits_of(image):
            row = canon_hex(image ^ (1 << bit))
            if universal is None or row in universal:
                covered.add(row)
    return covered

# (1) expansion universe: for every residual row r and every empty cell p, root = canon(r | 1<<p)
universe = {}   # root -> {'covered': set(rows), 'sources': set(rows), 'unsafe': ...}
row_ok = 0
for row in residualRows:
    m = int(row, 16)
    assert popcount(m) == 6 and canon_hex(m) == row, row
    row_ok += 1
    for p in range(121):
        if (m >> p) & 1:
            continue
        root = canon_hex(m | (1 << p))
        if root not in universe:
            pts, unsafe = stones_and_safety(int(root, 16))
            assert unsafe is not None
            assert canon_hex(int(root, 16)) == root
            universe[root] = {'covered': coverage_of(int(root, 16), residualSet),
                              'sources': set(), 'unsafe': unsafe}
        universe[root]['sources'].add(row)
need(row_ok == 86, 'rows iterated')
print('universe size (D4-dedup, not yet safety-filtered):', len(universe))

# (2) classification
in_pool = [r for r in universe if r in pool]
known_ref_exp = [r for r in universe if r in knownRefuted and r not in pool]
known_win_exp = [r for r in universe if r in knownWin and r not in pool]
fresh = [r for r in universe if r not in pool and r not in knownRefuted and r not in knownWin]
# every pool member is depth-10 judged (109 REFUTED + 8 WIN); cross-check:
for r in in_pool:
    need(r in knownRefuted or r in knownWin, 'pool member without verdict: ' + r)
unsafe_roots = [r for r in universe if universe[r]['unsafe'] > 0]
safe_universe = [r for r in universe if universe[r]['unsafe'] == 0]
need(len(in_pool) + len(known_ref_exp) + len(known_win_exp) + len(fresh) == len(set(in_pool) | set(known_ref_exp) | set(known_win_exp) | set(fresh)), 'partition disjoint')
fresh_safe = sorted(r for r in fresh if universe[r]['unsafe'] == 0)
fresh_unsafe = sorted(r for r in fresh if universe[r]['unsafe'] > 0)
print('in_pool:', len(in_pool), 'known_refuted:', len(known_ref_exp), 'known_win:', len(known_win_exp),
      'fresh:', len(fresh), '(fresh safe:', len(fresh_safe), 'unsafe:', len(fresh_unsafe), ')')
print('unsafe total in universe:', len(unsafe_roots))

# (3) known-WIN coverage over residual rows (potential immediate fold, pool or not)
win_cover_hits = {}
for root in sorted(knownWin):
    cov = coverage_of(int(root, 16), residualSet)
    if cov:
        win_cover_hits[root] = sorted(cov)
print('known-WIN roots covering residual rows:', len(win_cover_hits))
for r, c in sorted(win_cover_hits.items()):
    print('  WIN', r, '->', len(c), 'residual rows')
# dedupe which residual rows are coverable by a known WIN
rows_covered_by_win = set()
for c in win_cover_hits.values():
    rows_covered_by_win |= set(c)
print('residual rows coverable by known WINs:', len(rows_covered_by_win))

# (4) structure over the safe fresh candidates
pairRoots = {}; singleRoots = {}; multiRoots = {}
for root in fresh_safe:
    rows = sorted(universe[root]['covered'])
    if len(rows) >= 3:
        multiRoots.setdefault(len(rows), []).append((root, rows))
    elif len(rows) == 2:
        key = '|'.join(rows)
        pairRoots.setdefault(key, []).append(root)
    elif len(rows) == 1:
        singleRoots.setdefault(rows[0], []).append(root)
freshable_roots = set(fresh_safe)
covered_by_fresh = set()
for root in fresh_safe:
    covered_by_fresh |= universe[root]['covered']
rowIndex = {h: i for i, h in enumerate(residualRows)}
graph = [[] for _ in residualRows]
for key in pairRoots:
    a, b = key.split('|')
    i, j = rowIndex[a], rowIndex[b]
    graph[i].append(j); graph[j].append(i)
for edges in graph:
    edges.sort()
matching_size, match = maximum_matching(graph)
matchedRows = [h for i, h in enumerate(residualRows) if match[i] != -1]
unmatched = [h for i, h in enumerate(residualRows) if match[i] == -1]
unmatchedWithSingleton = [h for h in unmatched if h in singleRoots]
strandedAfter = [h for h in unmatched if h not in singleRoots and h not in rows_covered_by_win]
print('pair pairRoots(edges):', len(pairRoots), 'single eligible rows:', len(singleRoots))
print('multi-cover roots (>=3 residual rows):', {k: len(v) for k, v in sorted(multiRoots.items())})
print('maximum matching:', matching_size, 'matched rows:', len(matchedRows))
print('unmatched:', len(unmatched), 'unmatched with singleton:', len(unmatchedWithSingleton))
print('stranded after add-one-stone expansion (no fresh single/pair, no known-win cover):', len(strandedAfter))
witness = []
for i in range(len(residualRows)):
    j = match[i]
    if j is not None and j > i:
        key = '|'.join(sorted([residualRows[i], residualRows[j]]))
        witness.append({'root': sorted(pairRoots[key])[0], 'rows': key.split('|')})
for h in unmatchedWithSingleton:
    witness.append({'root': sorted(singleRoots[h])[0], 'rows': [h]})
witness.sort(key=lambda x: x['root'])
print('witness size (matching + singletons):', len(witness))

# (5) greedy set-cover to gauge certificate count including singles/multis
import math
greedy_rows = set(residualRows)
greedy_sel = []
cand_map = {r: set(universe[r]['covered']) for r in fresh_safe}
while greedy_rows:
    best = max(sorted(cand_map), key=lambda r: len(cand_map[r] & greedy_rows))
    gained = cand_map[best] & greedy_rows
    if not gained:
        break
    greedy_sel.append((best, sorted(gained)))
    greedy_rows -= gained
print('greedy set-cover over fresh safe (incl. singles/multis):', len(greedy_sel), 'certificates;',
      'leftover rows:', len(greedy_rows))

result = {
  'schema': 'n11-add-one-stone-expansion-86-rows-20261119-v1',
  'date': '2026-11-19',
  'base_state': {
    'residual_rows': len(residualRows),
    'known_refuted_total': len(knownRefuted),
    'known_win_total': len(knownWin),
    'pool': len(pool), 'pool_refuted': len(poolRefutedNow), 'pool_win': len(poolWinNow),
    'residual_rows_hex': residualRows,
    'source_records': ['post-seventh-receipt-cover-resolve3 (byte-identical repro)',
                        'post-eighth-receipt-cover-resolve4 (byte-identical repro)'],
  },
  'expansion': {
    'universe_roots': len(universe),
    'in_pool_117': len(in_pool),
    'known_refuted': sorted(known_ref_exp),
    'known_win_covered': {r: sorted(universe[r]['covered']) for r in sorted(known_win_exp)},
    'fresh_all': len(fresh),
    'fresh_safe': len(fresh_safe),
    'fresh_unsafe': len(fresh_unsafe),
    'unsafe_roots_total': len(unsafe_roots),
    'coverage_hist': {str(k): sum(1 for r in fresh_safe if len(universe[r]['covered']) == k)
                      for k in range(0, 1 + max((len(universe[r]['covered']) for r in fresh_safe), default=0))},
  },
  'known_win_hits': win_cover_hits,
  'rows_covered_by_known_win': sorted(rows_covered_by_win),
  'resolve_after_expansion': {
    'paired_rows_via_fresh': len(matchedRows),
    'matching_size': matching_size,
    'unmatched_rows': len(unmatched),
    'unmatched_with_singleton': len(unmatchedWithSingleton),
    'stranded_after_expansion': strandedAfter,
    'multi_cover_roots': {str(k): v for k, v in multiRoots.items()},
    'greedy_cover_certs': len(greedy_sel),
    'greedy_leftover': len(greedy_rows),
  },
  'witness': witness,
  'witness_full': [{'root': w['root'], 'rows': w['rows'], 'covered': sorted(universe[w['root']]['covered']),
                    'sources': sorted(universe[w['root']]['sources'])} for w in witness],
  'controls': {
    'rows_6stones_canonical': row_ok == 86,
    'known_win_total_164': len(knownWin) == 164,
    'known_refuted_total_340': len(knownRefuted) == 340,
    'pool_partition_109_8': len(poolRefutedNow) == 109 and len(poolWinNow) == 8,
  },
  'interpretation_guard': [
    'Add-one-stone expansion universe = canon(row + 1 stone) for the 86 open five-parent target rows; a universe member is any safe D4-canonical 7-stone position.',
    'Coverage rule is the same 8-D4-image-minus-one-stone relation used by the published resolve/fold machinery.',
    'fresh safe candidates have no verdict in the explicit pinned-source join (340 REFUTED / 164 WIN at this scope); they still require depth-10 probes (runner v17, both orderings, cap 30M, pilot_d6) and independently verified certificates before any fold.',
    'A known-WIN hit on a stranded row is NOT a fold by itself: only an independently verified WIN7-D10 certificate can close the row; row closure needs receipt extraction.',
    'REFUTED-D10 is not a LOSS proof. Witness roots here are a conditional plan, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
import json as _json
with open(f'{W}/foldv2/output/add-one-stone-expansion-86-rows-20261119.json', 'w') as f:
    _json.dump(result, f, indent=1)
    f.write('\n')
print('written add-one-stone-expansion-86-rows-20261119.json')
