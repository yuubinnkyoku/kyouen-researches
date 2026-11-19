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
residualSet_o = set(residualSet)

def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    n = 0
    for a in range(len(pts)):
        for b in range(a+1, len(pts)):
            for c in range(b+1, len(pts)):
                for d in range(c+1, len(pts)):
                    if det4(pts[a], pts[b], pts[c], pts[d]) == 0: n += 1
    return n


# ================= resolve5: post-twelfth cover re-solve over the 78 residual rows =================
fold9rec = load('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json')
need(fold9rec['status'] == 'fold-complete' and fold9rec['schema'] == 'n11-five-parent-ninth-twelfth-win7-receipt-fold-20261119-v1', 'fold9 record gate')
need(fold9rec['receipt_count'] == 4 and fold9rec['verdict_join_summary']['known_refuted_roots_after_sweep43'] == 379
     and fold9rec['verdict_join_summary']['known_win_roots_after_sweep43'] == 168, 'fold9 verdict universe gate')
need(fold9rec['frontier_after']['unique_remaining_s6'] == 6213 and fold9rec['frontier_after']['sum_remaining_cost'] == 492021
     and fold9rec['frontier_after']['solved_s6_in_manifest'] == 1635, 'fold9 frontier gate')
newTarget = set()
for r in fold9rec['receipts']:
    for h in r['covered_five_parent_target_rows']:
        need(h in residualSet_o, 'fold9 target row not residual-open: ' + h)
        need(h not in closedAll, 'fold9 target row closed twice: ' + h)
        newTarget.add(h)
need(len(newTarget) == 8, 'fold9 new target rows 8')
closedAllNew = closedAll | newTarget
need(len(closedAllNew) == 34, 'closed target rows 34')
targetAfter = [h for h in targetRows112 if h not in closedAllNew]
need(len(targetAfter) == 78, 'residual target rows 78, got %d' % len(targetAfter))
residualRows = targetAfter
residualSet = set(targetAfter)
need(residualSet_o - newTarget == residualSet, 'residual consistency')

# ---------- pool partition with the sweep43 verdicts ----------
poolWinNow = sorted(x for x in pool if x in knownWin)
poolRefutedNow = sorted(x for x in pool if x in knownRefuted)
need(len(poolWinNow) == 8 and len(poolRefutedNow) == 109, 'pool partition 8/109 stable (the 43 witnesses are expansion roots, not pool members)')

# ---------- expansion universe over the 78 residual rows ----------
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

universe = {}
for row in residualRows:
    m = int(row, 16)
    assert popcount(m) == 6 and canon_hex(m) == row, row
    for p in range(121):
        if (m >> p) & 1:
            continue
        root = canon_hex(m | (1 << p))
        if root not in universe:
            pts, unsafe = stones_and_safety(int(root, 16))
            universe[root] = {'covered': coverage_of(int(root, 16), residualSet), 'sources': set(), 'unsafe': unsafe}
        universe[root]['sources'].add(row)
print('universe size (D4-dedup):', len(universe))
in_pool = [r for r in universe if r in pool]
known_ref_exp = [r for r in universe if r in knownRefuted and r not in pool]
known_win_exp = [r for r in universe if r in knownWin and r not in pool]
fresh = [r for r in universe if r not in pool and r not in knownRefuted and r not in knownWin]
for r in in_pool:
    need(r in knownRefuted or r in knownWin, 'pool member without verdict: ' + r)
unsafe_roots = [r for r in universe if universe[r]['unsafe'] > 0]
fresh_safe = sorted(r for r in fresh if universe[r]['unsafe'] == 0)
fresh_unsafe = sorted(r for r in fresh if universe[r]['unsafe'] > 0)
print('in_pool:', len(in_pool), '(refuted', len([r for r in in_pool if r in knownRefuted]), '/ win', len([r for r in in_pool if r in knownWin]), ')',
      'known_refuted:', len(known_ref_exp), 'known_win:', len(known_win_exp),
      'fresh:', len(fresh), '(safe', len(fresh_safe), '/ unsafe', len(fresh_unsafe), ')')
# judge status of the 43 swept witnesses within this universe perspective
swept_ref = [r for r in s43['classification']['refuted_d10']['roots'] if r in universe]
swept_win = [r for r in s43['classification']['win7_d10']['roots'] if r in universe]
# The 39 REFUTED witnesses each cover residual rows (their pair rows are all still open), so they must be present.
# The 4 WIN witnesses covered exactly the 8 folded target rows, so they are correctly absent from the 78-row universe.
need(len(swept_ref) == 39, 'all 39 refuted witnesses in universe, got %d' % len(swept_ref))
need(len(swept_win) == 0, 'the 4 WIN witnesses covered only folded rows: %d present' % len(swept_win))

win_cover_hits = {}
for root in sorted(knownWin):
    cov = coverage_of(int(root, 16), residualSet)
    if cov: win_cover_hits[root] = sorted(cov)
rows_covered_by_win = set()
for c in win_cover_hits.values(): rows_covered_by_win |= set(c)
print('known-WIN roots covering the 78 residual rows:', len(win_cover_hits), 'rows coverable:', len(rows_covered_by_win))

pairRoots = {}; singleRoots = {}; multiRoots = {}
for root in fresh_safe:
    rows = sorted(universe[root]['covered'])
    if len(rows) >= 3:
        multiRoots.setdefault(len(rows), []).append((root, rows))
    elif len(rows) == 2:
        pairRoots.setdefault('|'.join(rows), []).append(root)
    elif len(rows) == 1:
        singleRoots.setdefault(rows[0], []).append(root)
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
strandedAfter = [h for h in unmatched if h not in singleRoots and h not in rows_covered_by_win]
singleWithWin = [h for h in unmatchedWithSingleton if h in rows_covered_by_win]
print('pair edges:', len(pairRoots), 'singleton rows:', len(singleRoots), 'multi-cover roots:', {k: len(v) for k, v in sorted(multiRoots.items())})
print('matching:', matching_size, 'matched rows:', len(matchedRows), 'unmatched:', len(unmatched), 'with singleton:', len(unmatchedWithSingleton))
print('stranded after re-solve:', len(strandedAfter), strandedAfter)
witness = []
for i in range(len(residualRows)):
    j = match[i]
    if j is not None and j > i:
        key = '|'.join(sorted([residualRows[i], residualRows[j]]))
        witness.append({'root': sorted(pairRoots[key])[0], 'rows': key.split('|')})
for h in unmatchedWithSingleton:
    witness.append({'root': sorted(singleRoots[h])[0], 'rows': [h]})
witness.sort(key=lambda x: x['root'])
print('witness plan size:', len(witness))
greedy_rows = set(residualRows); greedy_sel = []
cand_map = {r: set(universe[r]['covered']) for r in fresh_safe}
while greedy_rows:
    best = max(sorted(cand_map), key=lambda r: len(cand_map[r] & greedy_rows))
    gained = cand_map[best] & greedy_rows
    if not gained: break
    greedy_sel.append((best, sorted(gained)))
    greedy_rows -= gained
print('greedy set-cover certs:', len(greedy_sel), 'leftover:', len(greedy_rows))

result5 = {
  'schema': 'n11-five-parent-post-twelfth-receipt-cover-resolve5-20261119-v1',
  'date': '2026-11-19',
  'status': 'exact-residual-candidate-cover' if (len(strandedAfter) == 0 and len(witness) > 0) else 'partial-candidate-cover-with-stranded-rows',
  'base_state': {
    'residual_rows': len(residualRows),
    'known_refuted_total': len(knownRefuted), 'known_win_total': len(knownWin),
    'source_records': ['post-eighth-receipt-cover-resolve4 (chain reproduced, 340/164)',
                       'witness-43-root-depth10-sweep-20261119 (39 REFUTED + 4 WIN ingested -> 379/168)',
                       'ninth-twelfth-win7-receipt-fold-20261119 (S6 frontier 6222/492688 -> 6213/492021; target 34/112)'],
    'residual_row_hex': residualRows,
  },
  'target': {'parents': 5, 'rows': 112, 'closed_target_rows_total': 34, 'residual_target_rows': len(residualRows)},
  'verdict_pool': {
    'known_refuted_roots': len(knownRefuted), 'known_win_roots': len(knownWin),
    'pool_roots': len(pool), 'pool_refuted': len(poolRefutedNow), 'pool_win': len(poolWinNow),
    'sweep43_refuted_witnesses_in_universe': len(swept_ref),
    'sweep43_win_witnesses_absent_folded_rows': len(swept_win),
    'limitation': 'explicit pinned sources only (the resolve4 chain plus the 43-witness sweep); not the full 8,964-entry cache join',
  },
  'expansion': {
    'universe_roots': len(universe), 'in_pool_117': len(in_pool),
    'known_refuted_expansion': len(known_ref_exp), 'known_win_expansion': len(known_win_exp),
    'fresh_all': len(fresh), 'fresh_safe': len(fresh_safe), 'fresh_unsafe': len(fresh_unsafe),
    'unsafe_roots_total': len(unsafe_roots),
    'known_win_cover_hits': win_cover_hits,
    'rows_covered_by_known_win': sorted(rows_covered_by_win),
  },
  'resolve': {
    'pair_edges': len(pairRoots), 'singleton_eligible_rows': len(singleRoots),
    'multi_cover_roots': {str(k): len(v) for k, v in multiRoots.items()},
    'maximum_matching': matching_size, 'matched_rows': len(matchedRows),
    'unmatched_rows': len(unmatched), 'unmatched_with_singleton': len(unmatchedWithSingleton),
    'stranded_rows': len(strandedAfter), 'stranded_row_hex': sorted(strandedAfter),
    'stranded_scope_note': 'stranded at THIS scope means: no remaining unjudged fresh-safe add-one-stone candidate covers the row (pair or singleton) and no known-WIN receipt covers it. It is NOT a mathematical unclosability proof; deeper expansions (two added stones), other closure mechanisms, or candidates beyond this scope may still close it.',
    'witness_size': len(witness),
  },
  'witness': witness,
  'witness_full': [{'root': w['root'], 'rows': w['rows'], 'covered': sorted(universe[w['root']]['covered']),
                    'sources': sorted(universe[w['root']]['sources']),
                    'rule': 'each witness root is unjudged at depth 10 (the previous 43-witness plan was fully consumed: 4 WIN folded, 39 REFUTED struck)'} for w in witness],
  'controls': {
    'residual_consistent_with_fold9_record': True,
    'all_39_refuted_swept_witnesses_in_universe': True,
    'win_witnesses_only_covered_folded_rows': True,
    'pool_partition_stable_109_8': True,
    'witness_rows_are_open_residual_rows': True,
    'rows_6stones_canonical': True,
  },
  'interpretation_guard': [
    'Witness roots here are a conditional plan for the next depth-10 sweep, not certificates.',
    'A WIN7-D10 verdict requires both AND orderings uncapped with passing pilot controls; a fold additionally requires extraction and dual independent verification of the certificate.',
    'REFUTED-D10 is not a LOSS proof.',
    'Stranded rows at this scope do not preclude closure by out-of-scope mechanisms.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
with open(f'{W}/fold9/output/post-twelfth-receipt-cover-resolve5-20261119.json', 'w') as f:
    json.dump(result5, f, indent=1); f.write('\n')
print(json.dumps({'status': result5['status'], 'residual': len(residualRows), 'fresh_safe': len(fresh_safe),
                  'matching': matching_size, 'witness': len(witness), 'stranded': len(strandedAfter)}, indent=1))
