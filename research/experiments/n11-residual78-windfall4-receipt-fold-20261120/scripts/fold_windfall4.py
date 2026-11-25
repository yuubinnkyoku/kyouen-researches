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

# ---------- fold9 preamble ----------
ninth_twelfth=True
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

sweep28_add = {'refuted': [], 'win': [], 'capped': [], 'timeout': [], 'missing': []}
if True:
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


# ================= fold9 tail: ninth-twelfth receipt fold =================
need(len(knownRefuted) == 340 and len(knownWin) == 164, 'pre-sweep43 verdict universe 340/164, got %d/%d' % (len(knownRefuted), len(knownWin)))
res4 = load('foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json')
need(res4['receipts']['residual_row_hex'] == residualRows, 'residual rows match resolve4 record')
need(res4['receipts']['closed_target_rows'] == 26 == len(closedAll), 'resolve4 closed target rows 26')
import hashlib
def sha256_of(p):
    return hashlib.sha256(open(f'{W}/{p}','rb').read()).hexdigest()
need(sha256_of('foldv2/output/seventh-win7-receipt-fold-20261119.json') == 'f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737', 'fold7 sha256')
need(sha256_of('foldv2/output/eighth-win7-receipt-fold-20261119.json') == 'afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2', 'fold8 sha256')

# sweep43 verdict ingestion
s43 = load('sweep43/output/witness-43-root-depth10-sweep-20261119.json')
need(s43['status'] == 'sweep-complete' and s43['classification']['counted_roots'] == 43
     and s43['classification']['win7_d10']['count'] == 4 and s43['classification']['refuted_d10']['count'] == 39
     and s43['classification']['capped']['count'] == 0 and s43['classification']['ordering_conflicts']['count'] == 0, 'sweep43 gate')
w43 = {x['root']: x for x in s43['witness_records']}
NEW = sorted(s43['classification']['win7_d10']['roots'])
need(len(NEW) == 4, 'four new WIN receipt roots')
for r in NEW:
    need(r not in knownRefuted, 'WIN/LOSS conflict: ' + r)
    knownWin.add(r)
for r in s43['classification']['refuted_d10']['roots']:
    need(r not in knownWin, 'LOSS/WIN conflict: ' + r)
    knownRefuted.add(r)
need(len(knownRefuted) == 379 and len(knownWin) == 168, 'post-sweep43 verdict universe 379/168, got %d/%d' % (len(knownRefuted), len(knownWin)))

# ---------- worklist / census geometry ----------
import csv as _csv
legal_moves_of_src = open(f'{W}/fold_fourth_fifth_sixth.py').read().split('# ---------- pinned inputs')[0]
_ns = {}; exec(legal_moves_of_src, _ns); legal_moves_of = _ns['legal_moves_of']
census = load('inputs/census.json')
parents = {p['hex']: p for p in census['open_s5_census']}
parents_int = {int(h, 16): h for h in parents}
need(len(parents) > 0, 'census parents loaded')

_rowp_cache = {}
def row_parents_hex(h):
    if h in _rowp_cache: return _rowp_cache[h]
    mask = int(h, 16); ps = set()
    bl = bits_of(mask)
    for q in bl:
        c = canon_int(mask ^ (1 << q))
        if c in parents_int: ps.add(parents_int[c])
    _rowp_cache[h] = ps
    return ps

def demand(h):
    d = {'c1': 0, 'c2': 0, 'c4': 0}
    for p in row_parents_hex(h):
        c = parents[p]['classes']
        if c & 1: d['c1'] += 1
        if c & 2: d['c2'] += 1
        if c & 4: d['c4'] += 1
    return d

def root_row_set(root_hex, open_set):
    mask = int(root_hex, 16); out = {}
    for t in range(8):
        image = transform(mask, t)
        for q in range(121):
            if (image >> q) & 1:
                c = canon_int(image ^ (1 << q))
                h = format(c, '032x')
                if h in open_set: out[h] = True
    return sorted(out)

wl = {}
with open(f'{W}/inputs/worklist.csv') as f:
    rd = _csv.reader(f); hdr = next(rd)
    ix = hdr.index('s6_canonical_hex'); cx = hdr.index('own_candidates_s6_s7_edge_cost'); kx = hdr.index('category')
    for a in rd: wl[a[ix]] = (int(a[cx]), a[kx])
led = load('inputs/ledger.json')
old66 = set(led['derived']['closed_rows_66']); oldGlobal = set(x['row_hex'] for x in globalFold['receipts_by_row'])
open0 = {h: v for h, v in wl.items() if h not in old66 and h not in oldGlobal}
need(len(open0) == 6259 and sum(v[0] for v in open0.values()) == 495507, 'base frontier 6259/495507')
prev = load('inputs/previousCostFold.json')
prior = set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])
openA = {h: v for h, v in open0.items() if h not in prior}
need(len(openA) == 6240 and sum(v[0] for v in openA.values()) == 493965, 'cost78c/79c frontier')
import tarfile
firstFold = None
with tarfile.open(f'{W}/inputs/firstFoldTarball.tar.gz', 'r:gz') as t:
    for m in t.getmembers():
        if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
            firstFold = json.load(t.extractfile(m))
need(firstFold and firstFold['status'] == 'fold-complete', 'first fold')
firstClosed = set(x['row_hex'] for x in firstFold['new_receipt_coverage']['rows'])
open1 = {h: v for h, v in openA.items() if h not in firstClosed}
need(len(open1) == 6236 and sum(v[0] for v in open1.values()) == 493703, 'first-fold frontier')
stf = load('ex48/output/secondThirdFold.json')
rows23 = []
for r in stf['receipts']: rows23.extend(r['covered_s6_rows'])
open2 = {h: v for h, v in open1.items() if h not in set(rows23)}
need(len(open2) == 6229 and sum(v[0] for v in open2.values()) == 493184, 'second-third frontier')

def frontier_stats(openSet, solved):
    inc = {p: 0 for p in parents}
    for h in openSet:
        for p in row_parents_hex(h): inc[p] += 1
    needed_rows = [h for h in openSet if demand(h)['c1'] == 0]
    return {
      'solved_s6_in_manifest': solved,
      'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
      'unique_remaining_s6': len(openSet),
      'sum_remaining_cost': sum(v[0] for v in openSet.values()),
      's6_needed_by_open_classes': len(needed_rows),
      'cost_needed_by_open_classes': sum(openSet[h][0] for h in needed_rows),
      'parent_row_incidence': sum(inc.values()), '_inc': inc,
    }

# chain: published fold records 4, 5/6, 7, 8
fold4rec = load('fold4rec/fold4.json')
need(fold4rec['status'] == 'fold-complete' and fold4rec['schema'] == 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1', 'fold4 record gate')
rows4 = [x['row_hex'] for x in fold4rec['new_receipt_coverage']['rows']]
open3 = {h: v for h, v in open2.items() if h not in set(rows4)}
fa4 = fold4rec['frontier_after']
need(len(open3) == 6226 and sum(v[0] for v in open3.values()) == 492970, 'fourth-fold frontier')
need(fa4['solved_s6_in_manifest'] == 1622 and fa4['parent_row_incidence'] == 11855 and fa4['remaining_s5_orbits'] == 173, 'fold4 frontier_after gate')
fold56rec = load('fold56rec/fold56.json')
need(fold56rec['status'] == 'fold-complete' and fold56rec['schema'] == 'n11-five-parent-fifth-sixth-win7-receipt-fold-20261119-v1', 'fold56 record gate')
rows56 = [x['row_hex'] for x in fold56rec['new_receipt_coverage']['rows']]
open4 = {h: v for h, v in open3.items() if h not in set(rows56)}
need(len(open4) == 6224 and sum(v[0] for v in open4.values()) == 492830, 'fifth-sixth-fold frontier')
fa56 = fold56rec['frontier_after']
need(fa56['solved_s6_in_manifest'] == 1624 and fa56['parent_row_incidence'] == 11852, 'fold56 frontier_after gate')
rows7 = []
for r in fold7['receipts']: rows7.extend(r['covered_s6_rows'])
open5set = {h: v for h, v in open4.items() if h not in set(rows7)}
need(len(open5set) == 6223 and sum(v[0] for v in open5set.values()) == 492762, 'seventh-fold frontier')
need(fold7['frontier_after']['solved_s6_in_manifest'] == 1625 and fold7['frontier_after']['parent_row_incidence'] == 11850, 'fold7 frontier_after gate')
rows8 = []
for r in fold8['receipts']: rows8.extend(r['covered_s6_rows'])
openCur = {h: v for h, v in open5set.items() if h not in set(rows8)}
need(len(openCur) == 6222 and sum(v[0] for v in openCur.values()) == 492688, 'eighth-fold frontier (must match published 6222/492688)')
fa8 = fold8['frontier_after']
need(fa8['solved_s6_in_manifest'] == 1626 and fa8['parent_row_incidence'] == 11848 and fa8['s6_needed_by_open_classes'] == 4517
     and fa8['cost_needed_by_open_classes'] == 358189, 'fold8 frontier_after gate')
inc = {p: 0 for p in parents}
for h in openCur:
    for p in row_parents_hex(h): inc[p] += 1
need(sum(inc.values()) == 11848, 'open frontier incidence 11848')

# ---------- target machinery ----------
targetRows112 = targetRows  # from join head (audit witness pairs union)
need(len(targetRows112) == 112, 'target 112')
cover = load('excov/output/cover49.json')
targetResidual97 = set(cover['receipts']['residual_row_hex'])
need(len(targetResidual97) == 97, 'target residual 97')
targetResidual86 = residualSet
need(targetResidual86 <= targetResidual97, 'residual86 subset of 97')

def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    n = 0
    for a in range(len(pts)):
        for b in range(a+1, len(pts)):
            for c in range(b+1, len(pts)):
                for d in range(c+1, len(pts)):
                    if det4(pts[a], pts[b], pts[c], pts[d]) == 0: n += 1
    return n


# ================= ingest the published ninth-twelfth receipt fold record =================
# The four sweep43 WIN receipts were folded by the published fail-closed fold machine
# (fold_ninth_twelfth.py, published with its 9-12 receipts).  This machine rebuilds the
# entire chain from the same pinned inputs (all gates above) and re-derives the ninth
# through twelfth receipt coverage by geometry, then gates the result against the
# published record byte-for-byte on every row list and frontier statistic.
import hashlib
def sha256_of(p):
    return hashlib.sha256(open(f'{W}/{p}', 'rb').read()).hexdigest()

fold9rec = load('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json')
need(sha256_of('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json') ==
     'ee002d792345cf3e2f90fda43a0d6a3d4bf6ed29d3280653491b3dd83f42e67a', 'fold9 record sha256 pin')
need(fold9rec['schema'] == 'n11-five-parent-ninth-twelfth-win7-receipt-fold-20261119-v1', 'fold9 schema')
need(fold9rec['status'] == 'fold-complete' and fold9rec['receipt_count'] == 4, 'fold9 record gate')

NAMES9 = ['ninth', 'tenth', 'eleventh', 'twelfth']
open9 = dict(openCur)               # published post-eighth frontier (6222 / 492688, gated above)
totalClosed9 = []
newTargetAll9 = set()
proc_notes9 = []
for idx, r in enumerate(fold9rec['receipts']):
    need(r['receipt'] == NAMES9[idx], 'fold9 receipt order')
    need(r['root'] == NEW[idx], 'fold9 receipt roots == sweep43 WIN roots')
    mask = int(r['root'], 16)
    need(popcount(mask) == 7 and canon_hex(mask) == r['root'], 'fold9 root canonical')
    rows = root_row_set(r['root'], open9)
    need(rows == r['covered_s6_rows'], 'fold9 row re-derivation mismatch: ' + r['root'])
    for h in rows:
        need(h in open9, 'fold9 row not open: ' + h)
        need(h not in totalClosed9, 'fold9 row closed twice: ' + h)
    tgt = sorted(h for h in rows if h in targetResidual86)
    need(tgt == r['covered_five_parent_target_rows'], 'fold9 target rows mismatch')
    for h in rows: del open9[h]
    for h in rows:
        for p in row_parents_hex(h): inc[p] -= 1
    totalClosed9.extend(rows); newTargetAll9 |= set(tgt)
    proc_notes9.append(f"{NAMES9[idx]} root {r['root']}: re-derived {len(rows)} S6 rows ({len(tgt)} target rows)")
need(len(totalClosed9) == 9 and len(set(totalClosed9)) == 9, 'fold9 closed 9 unique S6 rows')
need(len(newTargetAll9) == 8, 'fold9 new target rows 8')
fa9 = fold9rec['frontier_after']
need(fa9['unique_remaining_s6'] == len(open9) == 6213, 'post-twelfth frontier rows')
need(fa9['sum_remaining_cost'] == sum(v[0] for v in open9.values()) == 492021, 'post-twelfth frontier cost')
need(fa9['solved_s6_in_manifest'] == 1635, 'post-twelfth solved count')
need(fa9['parent_row_incidence'] == sum(inc.values()) == 11826, 'post-twelfth incidence')
need(fa9['remaining_s5_orbits'] == sum(1 for v in inc.values() if v > 0), 'post-twelfth remaining orbits')
need(fa9['s6_needed_by_open_classes'] == len([h for h in open9 if demand(h)['c1'] == 0]) == 4513, 'post-twelfth needed rows')
need(fa9['cost_needed_by_open_classes'] == sum(open9[h][0] for h in open9 if demand(h)['c1'] == 0) == 357882, 'post-twelfth needed cost')
need([x['row_hex'] for x in fold9rec['new_receipt_coverage']['rows']] == sorted(totalClosed9), 'fold9 coverage rows list')
closedAllNew9 = closedAll | newTargetAll9
need(len(closedAllNew9) == 34, 'closed target rows total 34 after twelfth')
residualAfter9 = [h for h in targetRows112 if h not in closedAllNew9]
need(len(residualAfter9) == 78, 'residual 78 after twelfth')
need(residualAfter9 == fold9rec['five_parent_target_after']['residual_row_hex_after'], 'fold9 residual list')
need(sha256_of('fold9/output/post-twelfth-receipt-cover-resolve5-20261119.json') ==
     '5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e', 'resolve5 record sha256 pin')
res5 = load('fold9/output/post-twelfth-receipt-cover-resolve5-20261119.json')
need(res5['status'] == 'exact-residual-candidate-cover', 'resolve5 status')
need(res5['base_state']['residual_row_hex'] == residualAfter9, 'resolve5 base residual row list')

# ================= windfall receipts (thirteenth..sixteenth) =================
# The four cost65h-lane windfall WIN7-D10 roots (K1063; certificates extracted and
# triple-verified in K1066) close their covered residual rows here.  Every receipt
# is gated against ALL of: the published resolve6 verdict-join record (raw bit_line
# provenance, sha256-pinned), the K1066 fail-closed triple-verification record (its
# own sha256 pinned, all 50 gates re-asserted pass), the raw K1066 per-bit artifacts
# (extraction run/rerun summaries, TS Bareiss subroot stats + union audit, exact
# python Bareiss replay, BigInt independent verification, runner v16 node-exact
# crosscheck jsonl), and fresh geometry + legal-move rederivation in this process.
K1066 = '/home/user/work/repo/research/experiments/n11-residual78-windfall4-cert-extract-20261120'
verify = json.load(open(f'{K1066}/output/windfall4-cert-triple-verification-20261120.json'))
need(hashlib.sha256(open(f'{K1066}/output/windfall4-cert-triple-verification-20261120.json','rb').read()).hexdigest() ==
     'a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb', 'K1066 verify record sha256 pin')
need(verify['status'] == 'windfall-4-WIN7-roots-certificate-backed-pending-fold', 'K1066 status')
need(verify['schema'].startswith('n11-windfall4-win7-cert-extract-triple-verify-v1'), 'K1066 schema')
need(len(verify['checks']) == 50 and all(c['pass'] is True for c in verify['checks']), 'K1066 fifty gates all pass')

resolve6 = load('windfall/output/post-saturation-full-cache-join-resolve6-20261120.json')
need(sha256_of('windfall/output/post-saturation-full-cache-join-resolve6-20261120.json') ==
     'e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a', 'resolve6 record sha256 pin')
need(resolve6['status'] == 'exact-live-candidate-cover', 'resolve6 status')
need(resolve6['base_state']['residual_row_hex'] == residualAfter9, 'resolve6 base residual == post-twelfth residual')
wcheck = [c for c in resolve6['checks'] if c['name'] == 'win-coverage-of-residual'][0]
need(wcheck['pass'] is True and wcheck['detail']['win_cover_hits'] == 4, 'windfall coverage check pass')
ev = sorted(wcheck['detail']['evidence'], key=lambda e: e['engine_entries'][0]['bit'])
need([e['engine_entries'][0]['bit'] for e in ev] == [40, 43, 99, 118], 'windfall bits 40/43/99/118')
CHILD_HEX = verify['inputs']['child_hex']
child_mask = int(CHILD_HEX, 16)
need(all(e['engine_entries'][0]['child_hex'] == CHILD_HEX for e in ev), 'windfall child hex')
need(CHILD_HEX == '00000000000000803202000000001000', 'cost65h child hex')

openW = dict(open9)                  # 6213 open rows after the twelfth receipt
receipts = []; totalClosed = []; proc_notes = []
NAMESW = ['thirteenth', 'fourteenth', 'fifteenth', 'sixteenth']
for idx, e in enumerate(ev):
    bit = e['engine_entries'][0]['bit']
    name = NAMESW[idx]
    rt = [x for x in verify['roots'] if x['bit'] == bit]
    need(len(rt) == 1, 'K1066 root entry for bit %d' % bit)
    rt = rt[0]
    raw_mask = child_mask | (1 << bit)
    raw_hex = format(raw_mask, '032x')
    need(rt['raw_root_hex'] == raw_hex, 'raw root hex for bit %d' % bit)
    canon_root = e['root']
    need(rt['canonical_root_hex'] == canon_root and canon_hex(raw_mask) == canon_root, 'canonical mapping bit %d' % bit)
    need(e['popcount'] == 7 and e['unsafe_quadruples'] == 0 and e['d4_canonical'] is True, 'root safety bit %d' % bit)
    uq = unsafe_quadruples(raw_mask)
    need(uq == 0, name + ' unsafe quadruples %d' % uq)
    # --- certificate + extraction gates ---
    cert_path = f"{K1066}/{rt['certificate']['file']}"
    cert_bytes = open(cert_path, 'rb').read()
    need(len(cert_bytes) == rt['certificate']['bytes'], name + ' cert bytes')
    need(hashlib.sha256(cert_bytes).hexdigest() == rt['certificate']['sha256'], name + ' certificate sha256')
    cert_lines = cert_bytes.decode().splitlines()
    need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', name + ' cert header')
    need(cert_lines[1] == 'root ' + raw_hex, name + ' cert root line (raw maxbit child convention)')
    n_rows = rt['extraction']['rows']; n_moves = rt['extraction']['moves']
    need(len(cert_lines) - 2 == n_rows, name + ' cert rows')
    need(rt['extraction']['fbt_drops'] == 0 and rt['extraction']['fatal'] is None, name + ' extraction clean')
    need(rt['extraction']['kill_table'].startswith('empty'), name + ' blind extraction (empty kill table)')
    need(rt['extraction']['rerun_byte_identical'] is True, name + ' rerun byte-identical')
    s1 = json.load(open(f'{K1066}/output/extraction-run1-summary-bit{bit}-20261120.json'))
    s2 = json.load(open(f'{K1066}/output/extraction-rerun-summary-bit{bit}-20261120.json'))
    need(s1['child'] == CHILD_HEX and s1['bit'] == bit and s1['moves'] == n_moves
         and s1['nRows'] == n_rows and s1['fbt_drops'] == 0, name + ' run1 summary')
    need(s2['moves'] == n_moves and s2['sum'] == s1['sum'] == rt['extraction']['nodes_run1'] == rt['extraction']['nodes_rerun']
         and s2['nRows'] == s1['nRows'] == n_rows and s2['fbt_drops'] == 0, name + ' rerun determinism summary')
    need(all(v['ok'] is True and v['capped'] is False for v in s1['perMove'].values())
         and len(s1['perMove']) == n_moves, name + ' per-move extraction ok/uncapped')
    # --- independent legal-move rederivation (geometry, this process) ---
    lmv = legal_moves_of(raw_mask)
    need(len(lmv) == n_moves, name + ' legal move rederivation %d vs %d' % (len(lmv), n_moves))
    # --- TS Bareiss subroot decomposition gates ---
    rc = json.load(open(f'{K1066}/output/ts-root-check-bit{bit}-20261120.json'))
    need(rc['stones'] == 7 and rc['loserMobility'] == n_moves, name + ' ts root check')
    stats_all = []
    for line in open(f'{K1066}/output/ts-subroot-stats-bit{bit}-20261120.jsonl').read().strip().splitlines():
        d = json.loads(line)
        need(d['rows'] == n_rows, name + ' ts subroot rows')
        stats_all.extend(d['stats'].values())
    need(len(stats_all) == n_moves, name + ' ts subroot count')
    seen = sum(x['seen'] for x in stats_all); terms = sum(x['terminals'] for x in stats_all)
    oedges = sum(x['opponentEdges'] for x in stats_all)
    need(min(x['range'][0] for x in stats_all) == 13 and max(x['range'][1] for x in stats_all) == 17, name + ' ts terminal range')
    ua = json.load(open(f'{K1066}/output/ts-union-audit-bit{bit}-20261120.json'))
    need(ua['bit'] == bit and ua['exact_union'] is True and ua['missing'] == 0 and ua['extra'] == 0
         and ua['consumed_unique'] == n_rows and ua['certificate_rows'] == n_rows, name + ' ts union audit')
    # --- exact python Bareiss replay gates ---
    pr = json.load(open(f'{K1066}/output/python-bareiss-replay-bit{bit}-20261120.json'))
    need(pr['root_hex'] == raw_hex and pr['root_stones'] == 7 and pr['root_loser_mobility'] == n_moves
         and pr['subroots_passed'] == n_moves and pr['strategy_rows'] == n_rows and pr['consumed_rows'] == n_rows
         and pr['union_missing'] == 0 and pr['union_extra'] == 0
         and pr['terminal_stone_range'] == [13, 15, 17], name + ' python bareiss replay')
    # --- BigInt independent verification gates ---
    bi = json.load(open(f'{K1066}/output/bigint-independent-verification-bit{bit}-20261120.json'))
    need(bi['root_hex'] == raw_hex and bi['root_safe'] is True and bi['root_stones'] == 7
         and bi['root_mobility'] == n_moves and bi['subroots_passed'] == n_moves
         and bi['strategy_rows'] == n_rows and bi['consumed_winner_rows'] == n_rows
         and bi['union_missing'] == 0 and bi['union_extra'] == 0 and bi['rows_sorted_unique'] is True
         and bi['terminal_range'] == [13, 17] and bi['verdict'] == 'WIN7 certificate independently verified', name + ' bigint gate')
    need(bi['visited_states_across_subroots'] == seen and bi['terminal_count'] == terms
         and bi['loser_reply_edges'] == oedges, name + ' cross-method state flow (bigint == ts bareiss)')
    # --- published raw bit_line provenance (resolve6 record) ---
    rawprov = e['engine_entries'][0]['raw_provenance'][0]
    bitline = rawprov['bit_line']
    need(bitline['bit'] == bit and bitline['loss'] is True and bitline['capped'] is False
         and bitline['andclose'] is True and bitline['terminalStoneRange'] == [13, 17], name + ' raw bit_line verdict')
    need(rawprov['pilot_control_line']['control'] == 'pilot_d6' and rawprov['pilot_control_line']['loss'] is False
         and rawprov['pilot_control_line']['nodes'] == 3402 and rawprov['pilot_control_line']['capped'] is False, name + ' pilot control line')
    need(rt['runner_v16_fresh_crosscheck']['bit'] == bit
         and rt['runner_v16_fresh_crosscheck']['loss'] is True
         and rt['runner_v16_fresh_crosscheck']['capped'] is False
         and rt['runner_v16_fresh_crosscheck']['nodes'] == bitline['nodes'], name + ' K1066 runner crosscheck == raw bit_line nodes')
    need(rt['raw_batch_provenance']['file'] == rawprov['file'], name + ' raw batch file provenance')
    need(rt['resolve6_evidence_root'] == canon_root, name + ' K1066 resolve6 evidence root')
    # --- runner v16 node-exact crosscheck artifact ---
    ccmap = {}
    for line in open(f'{K1066}/output/runner-v16-node-exact-crosscheck-20261120.jsonl'):
        d = json.loads(line)
        if 'bit' in d: ccmap[d['bit']] = d
    need(bit in ccmap and ccmap[bit]['loss'] is True and ccmap[bit]['capped'] is False
         and ccmap[bit]['nodes'] == bitline['nodes'], name + ' runner v16 fresh nodes == published raw bit_line')
    # --- WIN/LOSS conflict scan against the published verdict universe ---
    need(canon_root not in knownRefuted, name + ' WIN/LOSS conflict vs published refuted universe')
    knownWin.add(canon_root)
    # --- coverage (geometry over all 8 D4 images of the raw root) ---
    rows = root_row_set(raw_hex, openW)
    need(len(rows) >= 1, name + ' closes no open row')
    for h in rows:
        need(h in openW, name + ' row not open: ' + h)
        need(h not in totalClosed and h not in totalClosed9, name + ' row closed twice: ' + h)
    tgt = sorted(h for h in rows if h in set(residualAfter9))
    need(tgt == e['covered_residual_rows'], name + ' covered residual rows == resolve6/K1066 record')
    need(tgt == rt['covered_residual_rows'], name + ' covered rows == K1066 root entry')
    closedCost = sum(openW[h][0] for h in rows)
    deltas = {}
    for h in rows:
        for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
    pdeltas = []
    for p in sorted(deltas):
        pb = inc[p]; pa = pb - deltas[p]
        pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': pb, 'rows_closed': deltas[p], 'rows_after': pa})
    for h in rows: del openW[h]
    for h in rows:
        for p in row_parents_hex(h): inc[p] -= 1
    receipts.append({
      'root': raw_hex, 'canonical_root_hex': canon_root, 'bit': bit, 'receipt': name,
      'child_hex': CHILD_HEX, 'added_bit': bit, 'legal_next_moves': n_moves,
      'covered_s6_rows': rows,
      'covered_five_parent_target_rows': tgt,
      'extra_s6_rows_not_in_target': [h for h in rows if h not in set(residualAfter9)],
      'unique_strategy_rows': n_rows,
      'extraction_nodes_run1_rerun': s1['sum'],
      'fbt_drops': 0, 'closed_edge_cost': closedCost,
      'certificate': {'file': rt['certificate']['file'], 'bytes': rt['certificate']['bytes'],
                      'sha256': rt['certificate']['sha256'], 'published_at': 'research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/' + rt['certificate']['file']},
      'verdict_basis': {
        'kind': 'single-order depth-10 engine verdict (andclose=1, uncapped loss=true) with triple-independent certificate verification',
        'raw_bit_line': {'file': rawprov['file'], 'nodes': bitline['nodes']},
        'runner_v16_fresh_nodes': ccmap[bit]['nodes'],
        'determinism_rerun_note': e['engine_entries'][0]['lane_context'][0]['determinism_rerun_note'],
        'lane_sweep_record': e['engine_entries'][0]['lane_context'][0]['file'],
      },
      'independent_verification': {
        'ts_bareiss': {'subroots': len(stats_all), 'seen': seen, 'terminals': terms,
                       'opponent_edges': oedges, 'union_missing': 0, 'union_extra': 0},
        'python_bareiss_replay': {'subroots_passed': pr['subroots_passed'], 'terminal_stone_range': pr['terminal_stone_range'],
                                  'visited_winner_states': pr['visited_winner_states'], 'union_missing': 0, 'union_extra': 0},
        'bigint': {'subroots_passed': bi['subroots_passed'], 'visited_states': bi['visited_states_across_subroots'],
                   'terminal_count': bi['terminal_count'], 'loser_reply_edges': bi['loser_reply_edges'],
                   'terminal_range': bi['terminal_range'], 'union_missing': 0, 'union_extra': 0},
        'cross_method_state_flow_equal': True, 'certificate_union_exact': True,
        'k1066_record': 'research/experiments/n11-residual78-windfall4-cert-extract-20261120/output/windfall4-cert-triple-verification-20261120.json (sha256 a3ca1b3df...; 50 gates pass)',
        'pilot_control': {'control': 'pilot_d6', 'nodes': 3402, 'loss': False, 'capped': False},
      },
      'affected_parents': len(pdeltas), 'parent_deltas': pdeltas,
    })
    totalClosed.extend(rows)
    proc_notes.append(f'{name} bit {bit} raw root {raw_hex} (canonical {canon_root}): closed {len(rows)} S6 rows ({len(tgt)} target rows), cost {closedCost}')
    print(f'  {name}: bit {bit} {raw_hex} closed {len(rows)} rows, target {len(tgt)}, cost {closedCost}')
need([e['engine_entries'][0]['bit'] for e in ev] == [r['bit'] for r in receipts], 'windfall receipt order')
need(len(set(residualAfter9) - set(h for r in receipts for h in r['covered_five_parent_target_rows'])) == 74, 'windfall closes exactly 4 target rows')

# ---------- frontier after ----------
needed_rows = [h for h in openW if demand(h)['c1'] == 0]
frontier_after = {
    'solved_s6_in_manifest': 1635 + len(totalClosed),
    'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
    'unique_remaining_s6': len(openW),
    'sum_remaining_cost': sum(v[0] for v in openW.values()),
    's6_needed_by_open_classes': len(needed_rows),
    'cost_needed_by_open_classes': sum(openW[h][0] for h in needed_rows),
    'parent_row_incidence': sum(inc.values()),
}
# ---------- five-parent target accounting ----------
newTargetAll = set()
for r in receipts: newTargetAll |= set(r['covered_five_parent_target_rows'])
need(len(newTargetAll) == 4, 'new windfall target rows total 4, got %d' % len(newTargetAll))
closedAllNew = closedAllNew9 | newTargetAll
need(len(closedAllNew) == 38, 'closed target rows total 38, got %d' % len(closedAllNew))
targetAfter = [h for h in targetRows112 if h not in closedAllNew]
need(len(targetAfter) == 74, 'residual target rows 74, got %d' % len(targetAfter))
row_receipt = {}
rr = []
for r in receipts:
    for h in r['covered_s6_rows']: row_receipt[h] = r['root']
for h in sorted(totalClosed):
    rr.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
               'parents': sorted(row_parents_hex(h)),
               'receipt': {'root': row_receipt[h], 'verdict': 'WIN7-D10 (certificate-backed)'}})

result = {
  'schema': 'n11-five-parent-windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120-v1',
  'date': '2026-11-20', 'status': 'fold-complete',
  'source_main_head_before': '68b04984f22fe907120ded2deaf5b03182108fd7',
  'previous_fold': {'record': 'fold/output/ninth-twelfth-win7-receipt-fold-20261119.json of n11-stranded86-add-one-stone-expansion-d10-sweep-20261119 (sha256 ee002d792345cf3e2f90fda43a0d6a3d4bf6ed29d3280653491b3dd83f42e67a)',
                    'frontier_after': fa9,
                    'closed_target_rows_total': 34, 'residual_target_rows': 78,
                    'coverage_rederived_in_this_run_by_geometry': proc_notes9},
  'windfall_source': {
    'verdict_join_record': 'research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json (sha256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a; K1063)',
    'certificate_record': 'research/experiments/n11-residual78-windfall4-cert-extract-20261120/output/windfall4-cert-triple-verification-20261120.json (sha256 a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb; K1066)',
    'lane_sweep_record': 'class2-lane-cost65h-sweep-20261114.json (cost65h lane; raw bit_line provenance through the K0863 cache corpus join)',
  },
  'source_blob_pins': {
    'worklist': '2fee1d0718547a62e346d35f5858d7913e37c097', 'ledger': 'e8785d509e8a11a37c0d03cc450455a14708c34d',
    'census': '9c251da3138c5cb0516e097be5e5d0427dfaf5f0', 'globalFold': '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc',
    'previousCostFold': '7e6144cc4bc92c34faa14bed3058cde64fb3880e', 'firstFoldTarball': 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019',
    'cover49_49c': 'a8eaf00bd6494eda50a68e7d06498bed833a7688', 'head1476': '65d0c7ce0200638a50db5451b11b8cb88ec64b5d',
    'cost78c': '626409d50d0a7bb1b925ebecbff7dbee9adfa398', 'cost79c': '054923a47ea0387b25f734222c499e60c054109b',
    'cost73j': '74fc3417391e30cf4cff9c2ffce059dce529ed86', 'sweep48': '37aba599d0b69275225bf231d56cb18feed14090',
    'fold23': '7923a0fe5331d1f7c896748031c4071b68fcc13a', 'coverResolve1': '600b23d339888ea0e693742da2b2ae9c372a9faf0',
    'joint': '40581746dc3304bdaff4b1934fd6f1d3d2981ea5', 'audit': '7cdc7c9ef341b5d9759923b3fc4986231c48895f',
    'fold4_record': '38715413d6dd23b97717c92d73d8b4a0af807cda', 'fold56_record': '134796a7de1e472c26e35defd7340d208a10b9b0',
    'fold7_sha256': 'f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737',
    'fold8_sha256': 'afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2',
    'resolve4_sha256': '2ad70afba4236375925dfd13230bb599b2d38f93631d6ded266fd77d34432e09',
    'resolve5_sha256': '5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e',
    'fold9_sha256': 'ee002d792345cf3e2f90fda43a0d6a3d4bf6ed29d3280653491b3dd83f42e67a',
    'sweep35_sha256': '8b7ba7d6b6fbfef057267e95c66efc036779c7d90ec918ec8beaa6a6618b95a5',
    'resolve6_sha256': 'e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a',
    'k1066_verify_sha256': 'a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb',
    'cert_bit40_sha256': '02778cf535bb3a269496f8b1cf0064fbadeb3b302bc4476d6b2d1c391bc37a34',
    'cert_bit43_sha256': '27e60fdca5eeed3fb1c188edd35a2d6ba...',
  },
  'receipt_count': 4, 'receipts': receipts, 'processing_notes': proc_notes,
  'frontier_before': fa9, 'frontier_after': frontier_after,
  'new_receipt_coverage': {
    'unique_s6_rows': len(totalClosed),
    'closed_edge_cost': sum(r['closed_edge_cost'] for r in receipts),
    'rows': rr,
  },
  'verdict_basis_note': (
    'Each windfall receipt is a depth-10 single-order (andclose=1) engine WIN verdict '
    'whose certificate was extracted blind from the raw maxbit-child root and triple-verified '
    '(TS Bareiss 4x4 subroot decomposition, exact python Bareiss replay, BigInt 3x3 cofactor), '
    'with the fresh runner v16 solve reproducing the published raw bit_line nodes node-exact. '
    'The dual-ordering requirement of the sweep-43 receipts does not apply to this variant: '
    'the receipt here is the certificate itself, not an order-duality verdict.'),
  'controls': {
    'base_frontier_recomputed': True, 'chain_frontiers_recomputed_each_step': True,
    'open_frontier_matches_published_6222_492688': True,
    'post_twelfth_frontier_matches_published_6213_492021': True,
    'fold9_record_sha256_pinned': True,
    'fold9_ninth_twelfth_coverage_rederived_by_geometry_from_sweep43_win_roots': True,
    'receipt_rows_rederived_from_all_8_d4_images': True,
    'receipt_target_rows_match_resolve6_and_k1066_records': True,
    'all_receipt_rows_were_open_before_their_receipt': True,
    'receipts_disjoint_from_all_previous_folds': True,
    'raw_root_maxbit_child_convention_gated': True,
    'canonical_mapping_gated_for_noncanonical_raw_roots': True,
    'legal_move_lists_independently_rederived': True,
    'certificates_sha256_verified_against_published_k1066': True,
    'extraction_determinism_run1_rerun_gated': True,
    'triple_independent_verification_gates_repassed': True,
    'cross_method_state_flow_equal_all_four': True,
    'runner_v16_fresh_nodes_node_exact_vs_published_bit_line': True,
    'k1066_fifty_gates_all_pass': True,
    'resolve6_record_sha256_pinned': True,
    'win_loss_conflict_scan_against_published_verdict_universe': True,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
    'The receipts close their S6 rows in the frontier but prove nothing about the empty board or any two-stone root.',
    'REFUTED-D10 verdicts are NOT LOSS proofs; pn/dn counts and solved counts are not game outcomes.',
    'A fold is row-coverage bookkeeping under the depth-10 receipt framework; the residual 74 target rows are covered by the (still conditional) resolve5 witness plan until their own receipts are published.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
result['source_blob_pins']['cert_bit43_sha256'] = receipts[1]['certificate']['sha256']
result['source_blob_pins']['cert_bit99_sha256'] = receipts[2]['certificate']['sha256']
result['source_blob_pins']['cert_bit118_sha256'] = receipts[3]['certificate']['sha256']
result['parent_closure'] = {
  'fully_closed_parent_count': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'] if p['rows_after'] == 0)),
  'affected_unique_parents': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'])),
}
result['five_parent_target_after'] = {
  'framework': 'five-parent target union (112 rows; 26 closed through the eighth receipt, 34 through the twelfth, 38 through the sixteenth)',
  'closed_target_rows_total': len(closedAllNew), 'residual_target_rows': len(targetAfter),
  'residual_row_hex_after': targetAfter,
}
with open(f'{W}/foldwf/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': len(closedAllNew), 'residual_target_rows': len(targetAfter),
                  'closed_cost': result['new_receipt_coverage']['closed_edge_cost'],
                  'rows_closed': sorted(totalClosed)}, indent=1))
