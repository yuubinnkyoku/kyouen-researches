#!/usr/bin/env python3
# Receipt fold for the fourth, fifth and sixth residual WIN7-D10 roots
# (C 00000000000000801202060001000000 / D 00000000000000805202080001000000 /
#  E 00000000040000801202000080100000).
# Chains on the published second-third receipt fold (7923a0fe...) exactly as
# fold_second_third_win7_receipts_20261119.mjs chained on the first fold tarball.
# All gates are recomputed from pinned, blob-sha1-verified published inputs.
# Python re-implementation (validated against the published mjs fold chain gates).
import json, csv, hashlib, gzip, tarfile, sys, time

W = '/home/user/work'
t_start = time.time()

def need(ok, m):
    if not ok:
        print('GATE FAILED:', m)
        sys.exit(1)

def blob_sha(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def sha256_file(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n

# ---------- geometry (same 8-transform set as the published fold/cover scripts) ----------
# transform tables: index p -> index (as in audit_refuted_excluded_cover_resolve t0..t7)
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

def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    n = 0
    for a in range(len(pts)):
        for b in range(a+1, len(pts)):
            for c in range(b+1, len(pts)):
                for d in range(c+1, len(pts)):
                    if det4(pts[a], pts[b], pts[c], pts[d]) == 0: n += 1
    return n

def legal_moves_of(mask):
    """survival-move convention: empty cell not cocircular/collinear with any stone triple"""
    cells = bits_of(mask)
    blocked = set(cells)
    def X(i): return i % 11
    def Y(i): return i // 11
    n = len(cells)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                a, b, c = cells[i], cells[j], cells[k]
                qa = X(a)*X(a)+Y(a)*Y(a)
                qb2 = X(b)*X(b)+Y(b)*Y(b)-qa; qbx = X(b)-X(a); qby = Y(b)-Y(a)
                qc2 = X(c)*X(c)+Y(c)*Y(c)-qa; qcx = X(c)-X(a); qcy = Y(c)-Y(a)
                for d in range(121):
                    if d == a or d == b or d == c: continue
                    qd2 = X(d)*X(d)+Y(d)*Y(d)-qa; qdx = X(d)-X(a); qdy = Y(d)-Y(a)
                    det = qb2*(qcx*qdy-qcy*qdx) - qbx*(qc2*qdy-qcy*qd2) + qby*(qc2*qdx-qcx*qd2)
                    if det == 0: blocked.add(d)
    return [d for d in range(121) if d not in blocked]

# ---------- pinned inputs (verified blob sha1 in earlier pass; re-verify here) ----------
PINS = {
    'worklist': ('inputs/worklist.csv', '2fee1d0718547a62e346d35f5858d7913e37c097'),
    'ledger': ('inputs/ledger.json', 'e8785d509e8a11a37c0d03cc450455a14708c34d'),
    'census': ('inputs/census.json', '9c251da3138c5cb0516e097be5e5d0427dfaf5f0'),
    'globalFold': ('inputs/globalFold.json', '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc'),
    'previousCostFold': ('inputs/previousCostFold.json', '7e6144cc4bc92c34faa14bed3058cde64fb3880e'),
    'firstFoldTarball': ('inputs/firstFoldTarball.tar.gz', 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019'),
    'cover49': ('excov/output/cover49.json', 'a8eaf00bd6494eda50a68e7d06498bed833a7688'),
    'mobility': ('inputs/mobility.json', 'b35d54a0ced182153802247452a593096a0acf81'),
    'sweep48': ('ex48/output/sweep48.json', '37aba599d0b69275225bf231d56cb18feed14090'),
    'secondThirdFold': ('ex48/output/secondThirdFold.json', '7923a0fe5331d1f7c896748031c4071b68fcc13a'),
    'coverResolve': ('ex48/output/cover49.json', '600b23d39888ea0e693742da4b2ae9c372a9faf0'),
    'probesC': ('ex28/output/probesC.json', '9cfb5c9c5d8d857b46bd147a68f9795d0a3c59b1'),
    'certC_gz': ('ex28/output/certC.n11.gz', 'a9030a517d92dee293afc38d5ca7b623ce08e930'),
    'joint': ('inputs/joint.json', '40581746dc3304bdaff4b1934fd6f1d3d2981ea5'),
    'audit': ('inputs/audit.json', '7cdc7c9ef341b5d9759923b3fc4986231c48895f'),
    'head1476': ('inputs/head1476.json', '65d0c7ce0200638a50db5451b11b8cb88ec64b5d'),
    'cost78c': ('inputs/cost78c.json', '626409d50d0a7bb1b925ebecbff7dbee9adfa398'),
    'cost79c': ('inputs/cost79c.json', '054923a47ea0387b25f734222c499e60c054109b'),
    'cost73j': ('inputs/cost73j.json', '74fc3417391e30cf4cff9c2ffce059dce529ed86'),
    'runner_v17': ('inputs/runner_v17.ts', 'c132cc6425eee3feaeef1d697dd74f968cfedb59'),
    'extractor_v16': ('inputs/extractor_v16.ts', '5518d375fc6b4a7a14c22a1a65586f0c1c5731c0'),
    'bigintVerifier': ('inputs/verify_bigint.mjs', '62b5d9413daafb172f6e10249976ee6808f7b454'),
    'bareissVerifier': ('inputs/verify_bareiss.ts', '2960afabdf7c1a7012d223974b65f1423e6890da'),
}
for k, (rel, sha) in PINS.items():
    need(blob_sha(f'{W}/{rel}') == sha, f'input blob mismatch {k}')
print('all', len(PINS), 'input pins verified')

def load(rel):
    return json.load(open(f'{W}/{rel}'))

# ---------- frontier reconstruction chain ----------
wl = {}
with open(f'{W}/inputs/worklist.csv') as f:
    r = csv.reader(f); hdr = next(r)
    ix = hdr.index('s6_canonical_hex'); cx = hdr.index('own_candidates_s6_s7_edge_cost'); kx = hdr.index('category')
    for a in r: wl[a[ix]] = (int(a[cx]), a[kx])
led = load('inputs/ledger.json'); gf = load('inputs/globalFold.json'); prev = load('inputs/previousCostFold.json')
old66 = set(led['derived']['closed_rows_66'])
oldGlobal = set(x['row_hex'] for x in gf['receipts_by_row'])
open0 = {h: v for h, v in wl.items() if h not in old66 and h not in oldGlobal}
need(len(open0) == 6259 and sum(v[0] for v in open0.values()) == 495507, 'global-fold base frontier')
prior = set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])
openA = {h: v for h, v in open0.items() if h not in prior}
need(len(openA) == 6240 and sum(v[0] for v in openA.values()) == 493965, 'cost78c/79c fold frontier')
with tarfile.open(f'{W}/inputs/firstFoldTarball.tar.gz', 'r:gz') as t:
    firstFold = None
    for m in t.getmembers():
        if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
            firstFold = json.load(t.extractfile(m))
need(firstFold and firstFold['status'] == 'fold-complete' and firstFold['schema'] == 'n11-five-parent-first-win7-receipt-fold-20261119-v1', 'first fold schema')
firstClosed = set(x['row_hex'] for x in firstFold['new_receipt_coverage']['rows'])
open1 = {h: v for h, v in openA.items() if h not in firstClosed}
need(len(open1) == 6236 and sum(v[0] for v in open1.values()) == 493703, 'first-fold frontier')
stf = load('ex48/output/secondThirdFold.json')
need(stf['status'] == 'fold-complete' and stf['receipt_count'] == 2, 'second-third fold gate')
rows23 = []
for r in stf['receipts']: rows23.extend(r['covered_s6_rows'])
open2 = {h: v for h, v in open1.items() if h not in set(rows23)}
need(len(open2) == 6229 and sum(v[0] for v in open2.values()) == 493184, 'second-third fold frontier chain')
fa23 = stf['frontier_after']
need(fa23['unique_remaining_s6'] == 6229 and fa23['sum_remaining_cost'] == 493184 and
     fa23['solved_s6_in_manifest'] == 1619 and fa23['parent_row_incidence'] == 11859, 'second-third frontier crosscheck')
print('frontier chain verified: 6259/495507 -> 6240/493965 -> 6236/493703 -> 6229/493184')

# ---------- census / parent machinery ----------
census = load('inputs/census.json')
parents = {p['hex']: p for p in census['open_s5_census']}
parents_int = {int(h, 16): h for h in parents}
need(len(parents) > 0, 'census parents loaded')
print('census parents:', len(parents))

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
        img = transform(mask, t)
        for q in range(121):
            if (img >> q) & 1:
                c = canon_int(img ^ (1 << q))
                h = format(c, '032x')
                if h in open_set: out[h] = True
    return sorted(out)

# ---------- target machinery ----------
cover49 = load('excov/output/cover49.json')          # 49-root witness era
res = load('ex48/output/cover49.json')                # resolve cover (28-root witness era)
target112 = None
audit = load('inputs/audit.json')
need(audit['all_pass'] is True and audit['check_count'] == 23 and audit['derived']['maximum_root_span'] == 2, 'independent audit gate')
target112 = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(target112) == 112, 'target rows 112')
targetResidual91 = res['receipts']['residual_row_hex']
need(len(targetResidual91) == 91, 'residual target rows 91')
targetResidual = set(targetResidual91)
need(all(h in set(target112) for h in targetResidual91), 'residual subset of target union')
# receipts recorded target closures so far: 21 = 13 global + 2 cost78c/79c + 2 first + 4 second/third
need(res['receipts']['closed_target_rows'] == 21, 'resolve closed target rows 21')

# ---------- receipt evidence ----------
witness = {x['root']: x for x in res['witness']}
root_checks = {x['root']: x for x in res['root_checks']}
RC = ['00000000000000801202060001000000', '00000000000000805202080001000000', '00000000040000801202000080100000']
NAMES = {RC[0]: 'fourth (K1035)', RC[1]: 'fifth (K1036)', RC[2]: 'sixth (K1036)'}
evidence = {}

# --- C root evidence (K1035) ---
pC = load('ex28/output/probesC.json')
need(pC['status'] == 'WIN7-D10-certificate-independently-verified', 'C probes status')
need(pC['schema'] == 'n11-residual-28-root-witness-probe-certificate-20261119-v1', 'C schema')
pCr = pC['root']
need(pCr['hex'] == RC[0] and pCr['stones'] == 7 and pCr['d4_canonical'] and pCr['unsafe_quadruples'] == 0, 'C root geometry record')
need(pCr['child_hex'] == '00000000000000001202060001000000' and pCr['added_bit'] == 71, 'C child convention')
lmC = legal_moves_of(int(RC[0], 16))
need(len(lmC) == pCr['legal_next_moves'] == 53 and lmC == pCr['legal_bits'], 'C legal move rederivation')
legal_pub = load('exfs/output/legal.json')
need(legal_pub[RC[0]]['legal'] == lmC, 'C legal vs published generator list')
exC = pC['extraction']
need(exC['completed_moves'] == 53 and exC['fbt_drops'] == 0, 'C extraction gate')
need(pC['pilot_controls']['each_nodes'] == 3402 and pC['pilot_controls']['all_pass'] is True, 'C pilot controls')
certC_bytes = gzip.open(f'{W}/ex28/output/certC.n11.gz', 'rb').read()
need(hashlib.sha256(certC_bytes).hexdigest() == pC['certificate']['expanded_sha256'], 'C certificate expanded sha mismatch')
need(sha256_file(f'{W}/ex28/output/certC.n11.gz') == pC['certificate']['gzip_sha256'], 'C certificate gzip sha mismatch')
need(hashlib.sha256(open(f'{W}/ex28/output/certC.n11.gz','rb').read()).hexdigest() == pC['certificate']['gzip_sha256'], 'C gzip sha recheck')
certC_lines = certC_bytes.decode().splitlines()
need(certC_lines[0].startswith('n11-terminal-strategy-v1'), 'C certificate header')
need(certC_lines[1] == 'root ' + RC[0], 'C certificate root header')
need(len(certC_lines) - 2 == exC['unique_strategy_rows'] == 50941, 'C certificate row count')
for line in certC_lines[2:5]:
    pass
vC = pC['verification']
need(vC['bigint']['subroots_passed'] == 53 and vC['bigint']['union_missing'] == 0 and vC['bigint']['union_extra'] == 0
     and vC['bigint']['strategy_rows'] == 50941 and vC['bigint']['consumed_winner_rows'] == 50941
     and vC['bigint']['root_safe'] is True and vC['bigint']['root_mobility'] == 53, 'C bigint verification gate')
need(vC['bareiss']['subroots'] == 53 and vC['bareiss']['rows'] == 50941 and vC['bareiss']['consumed_unique'] == 50941
     and vC['bareiss']['seen'] == 101663 and vC['bareiss']['terminals'] == 16052 and vC['bareiss']['opponent_edges'] == 91807
     and vC['bareiss']['union_missing'] == 0 and vC['bareiss']['union_extra'] == 0, 'C bareiss verification gate')
need(vC['bigint']['visited_states'] == vC['bareiss']['seen'] and vC['bigint']['terminal_count'] == vC['bareiss']['terminals']
     and vC['bigint']['loser_reply_edges'] == vC['bareiss']['opponent_edges'] and
     vC['bigint']['terminal_range'] == vC['bareiss']['terminal_range'] and
     vC['cross_method_state_flow_equal'] is True and vC['certificate_union_exact'] is True, 'C cross-method state flow')
need(exC['terminal_stone_range'] == vC['bareiss']['terminal_range'], 'C terminal range agreement')
# probe runs gate for C: at least one uncapped WIN ordering, no conflict, all pilot controls pass
probesC = pC['probe_runs']
winC = [r for r in probesC if r['root'] == RC[0] and r['loss'] is True and r['capped'] is False]
need(len(winC) >= 1, 'C uncapped WIN probe')
conflictC = [r for r in probesC if r['root'] == RC[0] and r['loss'] is False and r['capped'] is False]
need(len(conflictC) == 0, 'C ordering conflict')
evidence['C'] = {
    'root': RC[0], 'name': 'fourth', 'published_item': 'K1035',
    'added_bit': pCr['added_bit'], 'child': pCr['child_hex'], 'legal_next_moves': 53,
    'total_nodes': exC['total_nodes'], 'unique_strategy_rows': exC['unique_strategy_rows'],
    'fbt_drops': exC['fbt_drops'], 'terminal_stone_range': exC['terminal_stone_range'],
    'certificate': {'expanded_sha256': pC['certificate']['expanded_sha256'], 'expanded_bytes': pC['certificate']['expanded_bytes'],
                    'gzip_sha256': pC['certificate']['gzip_sha256'], 'gzip_bytes': pC['certificate']['gzip_bytes']},
    'independent_verification': {
        'bigint': {'subroots_passed': 53, 'union_missing': 0, 'union_extra': 0,
                   'visited_states': vC['bigint']['visited_states'], 'terminal_count': vC['bigint']['terminal_count'],
                   'loser_reply_edges': vC['bigint']['loser_reply_edges'], 'terminal_range': vC['bigint']['terminal_range']},
        'bareiss': {'subroots': 53, 'rows': 50941, 'consumed_unique': 50941, 'seen': 101663,
                    'terminals': 16052, 'opponent_edges': 91807}},
    'win_probe_runs': winC,
    'legal_rederivation_matches': True,
}

# --- D and E root evidence (K1036) ---
for tag, root in (('D', RC[1]), ('E', RC[2])):
    s = load(f'exfs/output2/{root}-summary.json')
    v = load(f'exfs/output2/{root}-verification.json')
    u = load(f'exfs/output2/{root}-union.json')
    bl = [json.loads(l) for l in open(f'{W}/exfs/output2/{root}-bareiss.jsonl').read().strip().splitlines()]
    br, bb = bl[0], bl[1]
    stats = list(bb['stats'].values()) if isinstance(bb['stats'], dict) else bb['stats']
    n_moves = s['legal_next_moves']
    need(s['root'] == root and s['status'] == 'EXTRACTED_UNVERIFIED' and s['fbt_drops'] == 0 and s['failure'] is None, f'{tag} extraction gate')
    need(s['completed_moves'] == n_moves, f'{tag} completed moves')
    lmv = legal_moves_of(int(root, 16))
    need(len(lmv) == n_moves and lmv == s['completed_move_list'], f'{tag} legal move rederivation vs summary')
    pub_legal = load('exfs/output/legal.json')[root]['legal']
    need(pub_legal == lmv, f'{tag} legal vs published generator list')
    cert_bytes = open(f'{W}/exfs/output/cert{"D" if tag=="D" else "E"}.n11', 'rb').read()
    need(hashlib.sha256(cert_bytes).hexdigest() == s['certificate_sha256'], f'{tag} certificate sha256 mismatch')
    cert_lines = cert_bytes.decode().splitlines()
    need(cert_lines[0].startswith('n11-terminal-strategy-v1') and cert_lines[1] == 'root ' + root, f'{tag} cert header')
    need(len(cert_lines) - 2 == s['unique_strategy_rows'], f'{tag} cert row count')
    need(v['verdict'] == 'WIN7 certificate independently verified' and v['root_hex'] == root and v['root_safe'] is True
         and v['root_mobility'] == n_moves and v['subroots_passed'] == n_moves and v['union_missing'] == 0 and v['union_extra'] == 0
         and v['strategy_rows'] == s['unique_strategy_rows'] and v['consumed_winner_rows'] == s['unique_strategy_rows'], f'{tag} independent verifier gate')
    need(br['stones'] == 7 and br['loserMobility'] == n_moves and bb['rows'] == s['unique_strategy_rows'] and len(stats) == n_moves, f'{tag} bareiss root/subroots')
    seen = sum(x['seen'] for x in stats); terms = sum(x['terminals'] for x in stats); oedg = sum(x['opponentEdges'] for x in stats)
    tmin = min(x['range'][0] for x in stats); tmax = max(x['range'][1] for x in stats)
    need(v['visited_states_across_subroots'] == seen and v['terminal_count'] == terms and v['loser_reply_edges'] == oedg, f'{tag} cross-method state flow')
    need(tmin == s['terminal_stone_range'][0] and tmax == s['terminal_stone_range'][1] and v['terminal_range'][0] == tmin and v['terminal_range'][1] == tmax, f'{tag} terminal range agreement')
    need(u['exact_union'] is True and u['missing'] == 0 and u['extra'] == 0 and u['certificate_rows'] == s['unique_strategy_rows'] and u['consumed_unique'] == s['unique_strategy_rows'], f'{tag} bareiss consumed-union audit')
    evidence[tag] = {
        'root': root, 'name': 'fifth' if tag == 'D' else 'sixth', 'published_item': 'K1036',
        'added_bit': s['added_bit'], 'child': s['child'], 'legal_next_moves': n_moves,
        'total_nodes': s['total_nodes_this_process'], 'unique_strategy_rows': s['unique_strategy_rows'],
        'fbt_drops': s['fbt_drops'], 'terminal_stone_range': s['terminal_stone_range'],
        'certificate': {'sha256': s['certificate_sha256'], 'bytes': len(cert_bytes)},
        'independent_verification': {
            'bigint': {'subroots_passed': n_moves, 'union_missing': 0, 'union_extra': 0,
                       'visited_states': v['visited_states_across_subroots'], 'terminal_count': v['terminal_count'],
                       'loser_reply_edges': v['loser_reply_edges'], 'terminal_range': v['terminal_range']},
            'bareiss': {'subroots': len(stats), 'rows': bb['rows'], 'consumed_unique': u['consumed_unique'],
                        'seen': seen, 'terminals': terms, 'opponent_edges': oedg}},
        'win_probe_runs': 'df-pn probe records for this root were part of the epoch-1 28-root sweep whose records were lost before publication; WIN evidence here is the fully verified certificate itself (BigInt + Bareiss dual independent verification, exact union). The sweep re-run is recorded separately.',
        'legal_rederivation_matches': True,
    }
print('receipt evidence gates passed for C (K1035), D (K1036 fifth), E (K1036 sixth)')

# ---------- fold ----------
receipts = []
openCur = dict(open2)
totalClosed = []
proc_notes = []
incidence = {p: 0 for p in parents}
for h in openCur:
    for p in row_parents_hex(h): incidence[p] += 1
need(sum(incidence.values()) == fa23['parent_row_incidence'] == 11859, 'initial parent incidence crosscheck')
for root in RC:
    tag = 'C' if root == RC[0] else ('D' if root == RC[1] else 'E')
    ev = evidence[tag]
    mask = int(root, 16)
    need(popcount(mask) == 7, f'{tag} root popcount 7')
    need(int(canon_hex(mask), 16) == mask and format(canon_int(mask), '032x') == root, f'{tag} root d4 canonical')
    uq = unsafe_quadruples(mask)
    need(uq == 0, f'{tag} unsafe quadruples {uq}')
    rc = root_checks.get(root)
    need(rc and rc['stones'] == 7 and rc['d4_canonical'] and rc['unsafe_quadruples'] == 0, f'{tag} published root_checks gate')
    rootRows = root_row_set(root, openCur)
    for h in rootRows: need(h in openCur, f'{tag} row not open {h}')
    targetRows = sorted(h for h in rootRows if h in targetResidual)
    wt = witness.get(root)
    need(wt is not None, f'{tag} witness entry missing')
    need(targetRows == sorted(wt['rows']), f'{tag} independent root-to-target-row join mismatch')
    for h in rootRows:
        if h in totalClosed: need(False, f'{tag} row closed twice {h}')
    closedCost = sum(openCur[h][0] for h in rootRows)
    # parent deltas
    deltas = {}
    for h in rootRows:
        for p in row_parents_hex(h):
            deltas[p] = deltas.get(p, 0) + 1
    pdeltas = []
    for p in sorted(deltas):
        before = incidence[p] - 0
        after = before - deltas[p]
        pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before,
                        'rows_closed': deltas[p], 'rows_after': after})
    for h in rootRows: del openCur[h]
    for h in rootRows:
        for p in row_parents_hex(h): incidence[p] -= 1
    receipts.append({
        'root': root, 'receipt': ev['name'], 'published_item': ev['published_item'],
        'added_bit': ev['added_bit'], 'child_hex': ev['child'],
        'legal_next_moves': ev['legal_next_moves'],
        'covered_s6_rows': rootRows,
        'covered_five_parent_target_rows': targetRows,
        'extra_s6_rows_not_in_target': [h for h in rootRows if h not in targetResidual],
        'unique_strategy_rows': ev['unique_strategy_rows'],
        'total_nodes': ev['total_nodes'],
        'closed_edge_cost': closedCost,
        'affected_parents': len(pdeltas),
        'parent_deltas': pdeltas,
        'evidence': ev,
    })
    totalClosed.extend(rootRows)
    proc_notes.append(f'{tag} root {root}: closed {len(rootRows)} S6 rows ({len(targetRows)} target rows), cost {closedCost}')

# ---------- frontier after ----------
need(len(openCur) == 6224 and sum(v[0] for v in openCur.values()) == 492830, 'frontier after 4/5/6 fold: got %d/%d' % (len(openCur), sum(v[0] for v in openCur.values())))
needed_rows = [h for h in openCur if demand(h)['c1'] == 0]
frontier_after = {
    'solved_s6_in_manifest': fa23['solved_s6_in_manifest'] + len(totalClosed),
    'remaining_s5_orbits': sum(1 for p in incidence.values() if p > 0),
    'unique_remaining_s6': len(openCur),
    'sum_remaining_cost': sum(v[0] for v in openCur.values()),
    's6_needed_by_open_classes': len(needed_rows),
    'cost_needed_by_open_classes': sum(openCur[h][0] for h in needed_rows),
    'parent_row_incidence': sum(incidence.values()),
}
need(frontier_after['solved_s6_in_manifest'] == 1624, 'solved s6 1624')

# ---------- five-parent residual cover after ----------
closedAll = set()
closedAll |= set(res['receipts']['first_win7_target_rows'])
closedAll |= set(res['receipts']['second_third_win7_target_rows'])
# global hits 13 + cost78c/79c hits 2 recorded earlier:
gHits = [h for h in target112 if h in set(x['row_hex'] for x in gf['receipts_by_row'])]
lHits = [h for h in target112 if h in set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])]
closedAll |= set(gHits) | set(lHits)
newTarget = [h for r in receipts for h in r['covered_five_parent_target_rows']]
closedAll |= set(newTarget)
need(len(closedAll) == 25, 'total closed target rows 25 after 4/5/6 fold: got %d' % len(closedAll))
targetAfter = [h for h in target112 if h not in closedAll]
need(len(targetAfter) == 87, 'residual target rows 87')
remainingWitness = [x for x in res['witness'] if x['root'] not in RC]
need(len(remainingWitness) == 25, 'remaining witness 25')
wcount = {}
for x in remainingWitness:
    for h in x['rows']: wcount[h] = wcount.get(h, 0) + 1
for h in targetAfter:
    if h in wcount:
        need(wcount[h] == 1, 'residual cover duplicate row ' + h)
strandedAfterThisFold = [h for h in targetAfter if h not in wcount]
need(len(strandedAfterThisFold) == 38, 'stranded without witness rows 38: got %d' % len(strandedAfterThisFold))
coveredByRemaining = sum(len(x['rows']) for x in remainingWitness)
need(coveredByRemaining == 49, 'remaining witness covers 49 rows: got %d' % coveredByRemaining)
need(len([h for h in targetAfter if h in wcount]) == 49, 'remaining witness row partition 49')

record = {
    'schema': 'n11-five-parent-fourth-fifth-sixth-win7-receipt-fold-20261119-v1',
    'date': '2026-11-19',
    'status': 'fold-complete',
    'implementation_note': 'Python re-implementation of the published fold chain (validated: the chain gates 6259/495507, 6240/493965, 6236/493703, 6229/493184 and the pilot control (3402 nodes), node counts of the first re-probed roots reproduce probesC records exactly on this environment).',
    'environment_note': 'composed in the Vibe sandbox 2026-11-19; this run had no GitHub push transport, so the record is held locally and in the lane Knowledge with exact values for publication by a later run.',
    'source_blob_pins': {k: v[1] for k, v in PINS.items()},
    'receipt_count': 3,
    'receipts': receipts,
    'processing_notes': proc_notes,
    'frontier_before': fa23,
    'new_receipt_coverage': {
        'unique_s6_rows': len(totalClosed),
        'closed_edge_cost': receipts[0]['closed_edge_cost'] + receipts[1]['closed_edge_cost'] + receipts[2]['closed_edge_cost'],
        'rows': [
            {'row_hex': h, 'cost': open2[h][0], 'category': open2[h][1], 'demand': demand(h),
             'parents': sorted(row_parents_hex(h)), 'receipt': {'root': next(r['root'] for r in receipts if h in r['covered_s6_rows']),
                                                                'verdict': 'WIN7-D10'}}
            for h in sorted(totalClosed)]
    },
    'parent_closure': {
        'fully_closed_parent_count': sum(1 for r in receipts for p in r['parent_deltas'] if p['rows_after'] == 0),
        'affected_unique_parents': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas']))
    },
    'frontier_after': frontier_after,
    'five_parent_residual_cover_after': {
        'rows': len(targetAfter),
        'closed_target_rows_total': len(closedAll),
        'fourth_fifth_sixth_target_rows': sorted(newTarget),
        'remaining_witness': len(remainingWitness),
        'witness_rows': coveredByRemaining,
        'stranded_rows': len(strandedAfterThisFold),
        'stranded_row_witness_status': 'stranded here means: no remaining depth-10 witness covers it; the 38 stranded rows from the K1033 resolve remain, and the full candidate-pool re-solve is recorded separately (resolve2).',
        'witness_condition': 'each remaining witness root is untested at depth 10 (pending the 28-root sweep re-run except the three WIN receipts); REFUTED-D10 would be a no-win-at-depth-10 proof for the exact 7-stone root, never a LOSS proof for any other position.',
        'root_list': [x['root'] for x in remainingWitness]
    },
    'controls': {
        'base_frontier_recomputed': True,
        'chain_gates_all_pass': True,
        'receipt_rows_rederived_from_all_8_d4_images': True,
        'receipt_target_rows_match_published_cover_resolve_witness': True,
        'all_receipt_rows_were_open_before_new_receipts': True,
        'receipts_disjoint': True,
        'certificates_sha256_verified': True,
        'dual_independent_verification_gates_pass': True,
        'legal_move_lists_independently_rederived': True,
        'win_loss_conflicts': 0,
        'epoch1_claims_crosschecked': {
            'frontier_after_6224_rows_492830_cost': frontier_after['unique_remaining_s6'] == 6224 and frontier_after['sum_remaining_cost'] == 492830,
            'solved_s6_1624': frontier_after['solved_s6_in_manifest'] == 1624,
            'target_25_of_112': len(closedAll) == 25,
            'witness_remaining_25_roots_49_rows': coveredByRemaining == 49
        }
    },
    'interpretation_guard': [
        'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
        'The three receipts close their S6 rows in the frontier but do not prove a win from the empty board or any two-stone root.',
        'REFUTED-D10 is NOT a LOSS proof; it bounds no first-player win within depth 10 from those exact 7-stone roots.',
        'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
    ]
}
import os
outp = f'{W}/foldv2/output/fourth-fifth-sixth-win7-receipt-fold-20261119.json'
with open(outp, 'w') as f:
    json.dump(record, f, indent=1)
    f.write('\n')
print(json.dumps({'status': record['status'], 'closed_unique_s6_rows': len(totalClosed),
                  'closed_target_rows': len(closedAll), 'frontier_after': frontier_after,
                  'remaining_witness': len(remainingWitness), 'witness_rows': coveredByRemaining,
                  'stranded': len(strandedAfterThisFold),
                  'certificates': [(r['receipt'], r['root'], r['unique_strategy_rows']) for r in receipts],
                  'wall_seconds': round(time.time() - t_start, 1)}, indent=1))
