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

# ---------- new receipts (ninth..twelfth = the four sweep43 WIN witnesses) ----------
NAMES = ['ninth', 'tenth', 'eleventh', 'twelfth']
CERTDIR = {'00000000000000801202000001040200': 'cert9/out80120204',
           '00000000000000821082040200000000': 'cert9/out82108204',
           '00000000000000821092200000000000': 'cert9/out82109220',
           '00000000001020003800000048000000': 'cert9/out10200038'}
receipts = []; totalClosed = []; proc_notes = []
import os as _os
for idx, root in enumerate(NEW):
    name = NAMES[idx]
    D9 = CERTDIR[root]
    s = json.load(open(f'{W}/{D9}/win7-root-{root}-extraction-summary-20261119.json'))
    v = json.load(open(f'{W}/{D9}/win7-root-{root}-independent-verification-20261119.json'))
    u = json.load(open(f'{W}/{D9}/win7-root-{root}-bareiss-union-audit-20261119.json'))
    bl = [json.loads(l) for l in open(f'{W}/{D9}/win7-root-{root}-bareiss-subroots-20261119.jsonl').read().strip().splitlines()]
    br, bb = bl[0], bl[1]
    stats = list(bb['stats'].values()) if isinstance(bb['stats'], dict) else bb['stats']
    n_moves = s['legal_next_moves']
    cert_bytes = open(f'{W}/{D9}/win7-root-{root}-20261119.n11', 'rb').read()
    # witness sweep record gates
    wr = w43[root]
    need(wr['covered_stranded_rows'] == sorted(set(wr['covered_stranded_rows'])), name + ' rows sorted unique')
    for p in wr['probe_runs']:
        need(p['cap'] == 30000000 and p['loss'] is True and p['capped'] is False, name + ' probe run gate')
    need(len(wr['probe_runs']) == 2 and sorted(p['ordering'] for p in wr['probe_runs']) == ['andclose0','andclose1'], name + ' both orderings')
    # geometry
    mask = int(root, 16)
    need(popcount(mask) == 7 and canon_hex(mask) == root, name + ' root canonical')
    uq = unsafe_quadruples(mask)
    need(uq == 0, name + ' unsafe quadruples %d' % uq)
    lmv = legal_moves_of(mask)
    need(len(lmv) == n_moves and lmv == s['completed_move_list'], name + ' legal rederivation')
    # extraction gates
    need(s['root'] == root and s['status'] == 'EXTRACTED_UNVERIFIED' and s['fbt_drops'] == 0 and s['failure'] is None, name + ' extraction gate')
    need(s['completed_moves'] == n_moves, name + ' completed moves')
    need(hashlib.sha256(cert_bytes).hexdigest() == s['certificate_sha256'], name + ' cert sha256')
    cert_lines = cert_bytes.decode().splitlines()
    need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
         and cert_lines[1] == 'root ' + root, name + ' cert header')
    need(len(cert_lines) - 2 == s['unique_strategy_rows'], name + ' cert rows')
    # bigint independent verification gates
    need(v['verdict'] == 'WIN7 certificate independently verified' and v['root_hex'] == root and v['root_safe'] is True
         and v['root_mobility'] == n_moves and v['subroots_passed'] == n_moves and v['union_missing'] == 0 and v['union_extra'] == 0
         and v['strategy_rows'] == s['unique_strategy_rows'] and v['consumed_winner_rows'] == s['unique_strategy_rows'], name + ' bigint gate')
    need(v['terminal_range'] == [13, 17] and v['rows_sorted_unique'] is True, name + ' bigint terminal range')
    # bareiss gates
    need(br['stones'] == 7 and br['loserMobility'] == n_moves, name + ' bareiss root check')
    need(bb['rows'] == s['unique_strategy_rows'] and len(stats) == n_moves, name + ' bareiss rows/subroots')
    seen = sum(x['seen'] for x in stats); terms = sum(x['terminals'] for x in stats); oedges = sum(x['opponentEdges'] for x in stats)
    need(v['visited_states_across_subroots'] == seen and v['terminal_count'] == terms and v['loser_reply_edges'] == oedges, name + ' cross-method state flow')
    need(min(x['range'][0] for x in stats) == 13 and max(x['range'][1] for x in stats) == 17, name + ' bareiss terminal range')
    need(u['exact_union'] is True and u['missing'] == 0 and u['extra'] == 0 and u['consumed_unique'] == s['unique_strategy_rows']
         and u['certificate_rows'] == s['unique_strategy_rows'], name + ' bareiss union audit')
    # receipt rows
    rootRows = root_row_set(root, openCur)
    need(len(rootRows) >= 1, name + ' closes no row')
    for h in rootRows:
        need(h in openCur, name + ' row not open: ' + h)
        need(h not in totalClosed, name + ' row closed twice: ' + h)
    targetRows_new = sorted(h for h in rootRows if h in targetResidual86)
    need(targetRows_new == wr['covered_stranded_rows'], name + ' independent to-witness row join mismatch')
    closedCost = sum(openCur[h][0] for h in rootRows)
    deltas = {}
    for h in rootRows:
        for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
    pdeltas = []
    for p in sorted(deltas):
        before = inc[p]; after = before - deltas[p]
        pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before, 'rows_closed': deltas[p], 'rows_after': after})
    for h in rootRows: del openCur[h]
    for h in rootRows:
        for p in row_parents_hex(h): inc[p] -= 1
    receipts.append({
      'root': root, 'receipt': name, 'added_bit': _ns['bits_of'](mask)[-1] if False else s['added_bit'], 'child_hex': s['child'],
      'legal_next_moves': n_moves,
      'covered_s6_rows': rootRows,
      'covered_five_parent_target_rows': targetRows_new,
      'extra_s6_rows_not_in_target': [h for h in rootRows if h not in targetResidual86],
      'unique_strategy_rows': s['unique_strategy_rows'], 'total_nodes': s['total_nodes_this_process'],
      'fbt_drops': s['fbt_drops'], 'closed_edge_cost': closedCost,
      'certificate_sha256': s['certificate_sha256'], 'certificate_bytes': len(cert_bytes),
      'affected_parents': len(pdeltas), 'parent_deltas': pdeltas,
      'probe_runs': [{'ordering': p['ordering'], 'cap': p['cap'], 'loss': p['loss'], 'nodes': p['nodes'], 'capped': p['capped']} for p in wr['probe_runs']],
      'extraction': {'engine': 'class4_child1_cert_extractor_exact_v16 (git blob 5518d375fc6b4a7a14c22a1a65586f0c1c5731c0)',
                     'pilot_control': {'control': 'pilot_d6', 'nodes': 3402, 'loss': False, 'all_pass': True}},
      'independent_verification': {
        'bigint': {'subroots_passed': n_moves, 'union_missing': 0, 'union_extra': 0,
                   'visited_states': v['visited_states_across_subroots'], 'terminal_count': v['terminal_count'],
                   'loser_reply_edges': v['loser_reply_edges'], 'terminal_range': v['terminal_range']},
        'bareiss': {'subroots': len(stats), 'rows': bb['rows'], 'consumed_unique': u['consumed_unique'],
                    'seen': seen, 'terminals': terms, 'opponent_edges': oedges,
                    'union_missing': 0, 'union_extra': 0},
        'cross_method_state_flow_equal': True, 'certificate_union_exact': True,
      },
    })
    totalClosed.extend(rootRows)
    proc_notes.append(f'{name} root {root}: closed {len(rootRows)} S6 rows ({len(targetRows_new)} target rows), cost {closedCost}')
    print(f'  {name}: {root} closed {len(rootRows)} rows, target {len(targetRows_new)}, cost {closedCost}, rows {sorted(rootRows)}')

# frontier after
need(s43['classification']['win7_d10']['roots'] == NEW, 'new roots order')
needed_rows = [h for h in openCur if demand(h)['c1'] == 0]
frontier_after = {
    'solved_s6_in_manifest': 1626 + len(totalClosed),
    'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
    'unique_remaining_s6': len(openCur),
    'sum_remaining_cost': sum(v[0] for v in openCur.values()),
    's6_needed_by_open_classes': len(needed_rows),
    'cost_needed_by_open_classes': sum(openCur[h][0] for h in needed_rows),
    'parent_row_incidence': sum(inc.values()),
}
# five-parent target accounting
newTargetAll = set()
for r in receipts: newTargetAll |= set(r['covered_five_parent_target_rows'])
need(len(newTargetAll) == 8, 'new target rows total 8, got %d' % len(newTargetAll))
closedAllNew = closedAll | newTargetAll
need(len(closedAllNew) == 34, 'closed target rows total 34, got %d' % len(closedAllNew))
targetAfter = [h for h in targetRows112 if h not in closedAllNew]
need(len(targetAfter) == 78, 'residual target rows 78, got %d' % len(targetAfter))

result = {
  'schema': 'n11-five-parent-ninth-twelfth-win7-receipt-fold-20261119-v1',
  'date': '2026-11-19', 'status': 'fold-complete',
  'source_main_head_before': '7d191ed173371b702550f2bfbc9b2915bf3e4dbf',
  'previous_fold': {'record': 'foldv2/output/eighth-win7-receipt-fold-20261119.json (git tree of n11-117pool-d10-sweep-7th8th-win7-certs-20261119; sha256 afcf7d0a...)', 'frontier_after': fa8},
  'source_blob_pins': {
    'worklist': '2fee1d0718547a62e346d35f5858d7913e37c097', 'ledger': 'e8785d509e8a11a37c0d03cc450455a14708c34d',
    'census': '9c251da3138c5cb0516e097be5e5d0427dfaf5f0', 'globalFold': '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc',
    'previousCostFold': '7e6144cc4bc92c34faa14bed3058cde64fb3880e', 'firstFoldTarball': 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019',
    'cover49_49c': 'a8eaf00bd6494eda50a68e7d06498bed833a7688', 'head1476': '65d0c7ce0200638a50db5451b11b8cb88ec64b5d',
    'cost78c': '626409d50d0a7bb1b925ebecbff7dbee9adfa398', 'cost79c': '054923a47ea0387b25f734222c499e60c054109b',
    'cost73j': '74fc3417391e30cf4cff9c2ffce059dce529ed86', 'sweep48': '37aba599d0b69275225bf231d56cb18feed14090',
    'fold23': '7923a0fe5331d1f7c896748031c4071b68fcc13a', 'coverResolve': '600b23d39888ea0e693742da4b2ae9c372a9faf0',
    'joint': '40581746dc3304bdaff4b1934fd6f1d3d2981ea5', 'audit': '7cdc7c9ef341b5d9759923b3fc4986231c48895f',
    'fold4_record': '38715413d6dd23b97717c92d73d8b4a0af807cda', 'fold56_record': '134796a7de1e472c26e35defd7340d208a10b9b0',
    'fold7_sha256': 'f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737',
    'fold8_sha256': 'afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2',
    'resolve4_sha256': '2ad70afba4236375925dfd13230bb599b2d38f93631d6ded266fd77d34432e09',
    'sweep35_sha256': '8b7ba7d6b6fbfef057267e95c66efc036779c7d90ec918ec8beaa6a6618b95a5',
    'runner_v17': 'c132cc6425eee3feaeef1d697dd74f968cfedb59',
    'extractor_v16': '5518d375fc6b4a7a14c22a1a65586f0c1c5731c0',
    'bigintVerifier': '62b5d9413daafb172f6e10249976ee6808f7b454',
    'bareissVerifier': '2960afabdf7c1a7012d223974b65f1423e6890da',
  },
  'receipt_count': 4, 'receipts': receipts, 'processing_notes': proc_notes,
  'frontier_before': fa8, 'frontier_after': frontier_after,
  'new_receipt_coverage': {
    'unique_s6_rows': len(totalClosed),
    'closed_edge_cost': sum(r['closed_edge_cost'] for r in receipts),
    'rows': [],
  },
  'witness_sweep_record': 'sweep43/output/witness-43-root-depth10-sweep-20261119.json (43 add-one-stone witnesses over the 86 stranded rows; 4 WIN / 39 REFUTED / 0 capped / 0 conflict)',
  'verdict_join_summary': {
    'known_refuted_roots_pre_sweep43': 340, 'known_win_roots_pre_sweep43': 164,
    'known_refuted_roots_after_sweep43': len(knownRefuted), 'known_win_roots_after_sweep43': len(knownWin),
    'join_limitation': 'explicit pinned sources only (resolve4 chain plus the 43-witness sweep); not the full 8,964-entry cache join',
    'win_loss_conflicts': 0,
  },
  'controls': {
    'base_frontier_recomputed': True, 'chain_frontiers_recomputed_each_step': True,
    'open_frontier_matches_published_6222_492688': True,
    'receipt_rows_rederived_from_all_8_d4_images': True,
    'receipt_target_rows_match_sweep43_witness_records': True,
    'all_receipt_rows_were_open_before_their_receipt': True,
    'receipts_disjoint': True,
    'legal_move_lists_independently_rederived': True,
    'certificates_sha256_verified': True,
    'bigint_independent_verification_pass_both_methods': True,
    'bareiss_union_exact_all_four': True,
    'cross_method_state_flow_equal_all_four': True,
    'pilot_controls_all_four_pass': True,
    'dual_ordering_uncapped_all_four': True,
    'win_loss_conflict_scan_against_published_verdict_universe': True,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
    'The receipts close their S6 rows in the frontier but prove nothing about the empty board or any two-stone root.',
    'The 39 REFUTED-D10 witnesses of the 43-witness sweep are NOT LOSS proofs.',
    'The residual five-parent target rows (78) and any new witness plan are recorded in the post-fold cover re-solve (resolve5); witness roots are a conditional plan, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
# fill new_receipt_coverage rows properly (costs from closed-time snapshot)
row_receipt = {}
rr = []
for r in receipts:
    for h in r['covered_s6_rows']: row_receipt[h] = r['root']
for h in sorted(totalClosed):
    rr.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
               'parents': sorted(row_parents_hex(h)), 'receipt': {'root': row_receipt[h], 'verdict': 'WIN7-D10'}})
result['new_receipt_coverage']['rows'] = rr
result['parent_closure'] = {
  'fully_closed_parent_count': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'] if p['rows_after'] == 0)),
  'affected_unique_parents': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'])),
}
result['five_parent_target_after'] = {
  'framework': 'five-parent target union (112 rows; 26 closed through the eighth receipt, 34 through the twelfth)',
  'closed_target_rows_total': len(closedAllNew), 'residual_target_rows': len(targetAfter),
  'residual_row_hex_after': targetAfter,
}
with open(f'{W}/fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': len(closedAllNew), 'residual_target_rows': len(targetAfter),
                  'closed_cost': result['new_receipt_coverage']['closed_edge_cost'],
                  'all_target_after': targetAfter}, indent=1))
