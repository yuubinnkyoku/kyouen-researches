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

# ---------- coverage over residual rows ----------
pairRoots = {}; singleRoots = {}; zeroCover = []
for root in candidates:
    mask = int(root, 16)
    covered = set()
    for t in range(8):
        image = transform(mask, t)
        for bit in bits_of(image):
            row = canon_hex(image ^ (1 << bit))
            if row in residualSet: covered.add(row)
    rows = sorted(covered)
    if len(rows) == 2:
        key = '|'.join(rows)
        pairRoots.setdefault(key, []).append(root)
    elif len(rows) == 1:
        singleRoots.setdefault(rows[0], []).append(root)
    else:
        zeroCover.append({'root': root, 'residual_covered': rows})
rowIndex = {h: i for i, h in enumerate(residualRows)}
graph = [[] for _ in residualRows]
for key in pairRoots:
    a, b = key.split('|')
    i, j = rowIndex[a], rowIndex[b]
    graph[i].append(j); graph[j].append(i)
for edges in graph: edges.sort()
matching_size, match = maximum_matching(graph)
matchedRows = [h for i, h in enumerate(residualRows) if match[i] != -1]
unmatched = [h for i, h in enumerate(residualRows) if match[i] == -1]
unmatchedWithSingleton = [h for h in unmatched if h in singleRoots]
strandedRows = [h for h in unmatched if h not in singleRoots]
witness = []
for i in range(len(residualRows)):
    j = match[i]
    if j is not None and j > i:
        key = '|'.join(sorted([residualRows[i], residualRows[j]]))
        witness.append({'root': sorted(pairRoots[key])[0], 'rows': key.split('|')})
for h in unmatchedWithSingleton:
    witness.append({'root': sorted(singleRoots[h])[0], 'rows': [h]})
witness.sort(key=lambda x: x['root'])
coveredByWitness = set(h for w in witness for h in w['rows'])
witnessCoversAll = len(coveredByWitness) == len(residualRows) and all(h in residualSet for w in witness for h in w['rows'])
rootChecks = []
for item in witness:
    mask = int(item['root'], 16)
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    unsafe = sum(1 for a in range(7) for b in range(a+1, 7) for c in range(b+1, 7) for d in range(c+1, 7)
                 if det4(pts[a], pts[b], pts[c], pts[d]) == 0)
    covered = set()
    for t in range(8):
        image = transform(mask, t)
        for bit in bits_of(image):
            row = canon_hex(image ^ (1 << bit))
            if row in residualSet: covered.add(row)
    need(popcount(mask) == 7 and canon_hex(mask) == item['root'] and unsafe == 0, 'unsafe/noncanonical root ' + item['root'])
    need(sorted(covered) == sorted(item['rows']), 'coverage mismatch ' + item['root'])
    rootChecks.append({'root': item['root'], 'stones': 7, 'd4_canonical': True, 'unsafe_quadruples': unsafe,
                       'covered_residual_rows': item['rows']})
fullyCovered = witnessCoversAll and len(strandedRows) == 0

result = {
    'schema': 'n11-five-parent-post-eighth-receipt-cover-resolve-20261119-v1',
    'date': '2026-11-19',
    'status': 'exact-residual-candidate-cover' if fullyCovered else 'residual-rows-uncoverable-by-remaining-candidates',
    'with_sweep28_verdicts': with_sweep,
    'sweep28_ingest': {k: sorted(v) for k, v in sweep28_add.items()} if with_sweep else None,
    'sweep28_note': ('sweep verdict ingestion: remaining untested witness roots that completed both AND orderings uncapped with passing pilot controls were ingested as REFUTED-D10/WIN7-D10; capped, conflicting, timed-out or incomplete roots are excluded from the eligible pool here only if their verdicts landed'
                     if with_sweep else 'pre-sweep scope: the remaining 25 witness roots are still untested; they remain eligible candidates'),
    'target': {'parents': 5, 'rows': 112, 'maximum_candidate_root_span': 2},
    'receipts': {
        'global_fold_rows': len(globalRows), 'global_hits': len(globalHits),
        'cost78c_79c_rows': len(laterRows),
        'first_win7_rows': firstFold['new_receipt_coverage']['unique_s6_rows'],
        'closed_target_rows': len(closedAll),
        'first_win7_target_rows': firstTarget,
        'second_third_win7_target_rows': myTarget,
        'fourth_fifth_sixth_win7_target_rows': newTarget,
        'residual_rows': len(residualRows), 'residual_row_hex': residualRows
    },
    'verdict_pool': {
        'known_refuted_roots': len(knownRefuted), 'known_win_roots': len(knownWin),
        'refuted_before_sweep': ext_refuted_before, 'win_before_sweep': ext_win_before,
        'pool_roots': len(pool), 'pool_refuted': len(poolRefutedNow), 'pool_win': len(poolWinNow),
        'pool_fully_depth10_judged': True,
        'sweep6_ingest': {k: sorted(v) for k, v in sweep6_add.items()},
        'eighth_receipt_root': fold8['receipts'][0]['root'],
        'eligible_candidates': len(candidates), 'zero_residual_cover_in_pool': len(zeroCover),
        'fold_receipt_roots': NEW_RECEIPTS,
        'limitation': 'the known-verdict join uses the explicitly pinned sweep/receipt sources (originals plus the 2026-11-19 48-root depth-10 sweep, the six published WIN7-D10 receipts, and where enabled the 2026-11-19 28-root witness sweep records); it is not the full 8,964-entry cache join'
    },
    'resolve': {
        'pair_edges': len(pairRoots), 'singleton_eligible_rows': len(singleRoots),
        'maximum_matching': matching_size, 'matched_rows': len(matchedRows),
        'unmatched_rows': len(unmatched), 'unmatched_with_singleton': len(unmatchedWithSingleton),
        'stranded_rows': len(strandedRows), 'stranded_row_hex': strandedRows,
        'witness_size': len(witness), 'lower_bound': (len(residualRows) + 1) // 2,
        'covered_rows': len(coveredByWitness)
    },
    'witness': witness, 'root_checks': rootChecks,
    'controls': {
        'enumerated_totals_reproduce_236_156': True,
        'eight_receipt_roots_are_the_only_pool_wins': len(poolWinNow) == 8,
        'pool_fully_judged_depth10_109_refuted_8_win': len(poolRefutedNow) == 109 and len(poolWinNow) == 8 and len(candidates) == 0,
        'closed_target_rows_25': len(closedAll) == 25,
        'residual_rows_87': len(residualRows) == 87,
        'witness_rows_are_open_residual_rows': True
    },
    'interpretation_guard': [
        'This re-solve strikes any swept REFUTED-D10 roots from the candidate pool and recomputes a candidate cover; witness roots still require sweeps and independently verified certificates.',
        'A stranded row cannot be closed by ANY remaining depth-10 WIN7 candidate in the 117-root pool at this scope; it then needs a candidate beyond this pool, a deeper search, or a different closure mechanism. It is NOT a mathematical unclosability proof.',
        'Witness roots here are a conditional plan, not certificates.',
        'REFUTED-D10 is not a LOSS proof.',
        'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
    ]
}
tail = sys.argv[1] if len(sys.argv) > 1 else ''
out = f'{W}/foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json'
with open(out, 'w') as f:
    json.dump(result, f, indent=1)
    f.write('\n')
print(json.dumps({'status': result['status'], 'with_sweep': with_sweep,
                  'known_refuted': len(knownRefuted), 'known_win': len(knownWin),
                  'pool': len(pool), 'pool_refuted': len(poolRefutedNow), 'pool_win': len(poolWinNow),
                  'eligible_candidates': len(candidates),
                  'residual_rows': len(residualRows),
                  'resolve': {k: v for k, v in result['resolve'].items() if k != 'stranded_row_hex'}}, indent=1))
