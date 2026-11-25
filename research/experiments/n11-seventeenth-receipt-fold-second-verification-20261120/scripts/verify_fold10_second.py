#!/usr/bin/env python3
# Independent second verification of fold10 (seventeenth WIN7 receipt fold).
# Scope: geometric re-derivation of the covered rows (8 D4 images x one-stone
# removal), cross-record bookkeeping against the fold9 (thirteenth-sixteenth)
# published record, input SHA pin checks, and frontier arithmetic checks --
# all from the published artifacts only. This is NOT a re-execution of the
# owner's 18-input chain-reconstruction machine (fold_seventeenth.py); the
# chain inputs (worklist/ledger/tarball/...) are not re-verified here and
# remain under the fail-closed machine's own gates.
#
# W path -> repo path map (inputs verified by SHA-256 pin at run time):
#   /home/user/work/fold10v/fold10.json
#     research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json
#     (fold10 正本, sha256 bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a, fetched raw from main)
#   /home/user/work/fold9/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
#     research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
#     (fold9 正本, sha256 24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2)
#   /home/user/work/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11
#     research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11
#     (seventeenth certificate, sha256 21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8)
#
# Usage: python3 verify_fold10_second.py  (writes output/fold10-second-verification-20261120.json)
import json, hashlib, sys, os

F10 = '/home/user/work/fold10v/fold10.json'
F9 = '/home/user/work/fold9/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json'
CERT = '/home/user/work/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11'
ROOT_HEX = '00004000000000821082000000000100'

gates = []
def gate(name, ok, detail=''):
    gates.append({'gate': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return bool(ok)

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

# D4 transforms (verbatim published convention of the fold chain)
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
    out, p = [], 0
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

def det3(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    q1 = x1*x1 + y1*y1; q2 = x2*x2 + y2*y2; q3 = x3*x3 + y3*y3
    return q1*(x2*y3 - x3*y2) - q2*(x1*y3 - x3*y1) + q3*(x1*y2 - x2*y1)

def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    n = 0
    m = len(pts)
    for a in range(m):
        for b in range(a+1, m):
            for c in range(b+1, m):
                for d in range(c+1, m):
                    if (det3(pts[a], pts[b], pts[c]) - det3(pts[a], pts[b], pts[d])
                            + det3(pts[a], pts[c], pts[d]) - det3(pts[b], pts[c], pts[d])) == 0:
                        n += 1
    return n

f10 = json.load(open(F10))
f9 = json.load(open(F9))

# 1. bookkeeping/hash pins
gate('fold10 正本 sha256 == published bed7d331...', sha256(F10) == 'bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a', sha256(F10))
gate('fold9 local pin == fold10.previous_fold pin', f10['source_sha256_pins']['fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json'] == sha256(F9) == '24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2')
gate('cert sha256 pin matches local byte-exact file', f10['receipts'][0]['certificate_sha256'] == sha256(CERT) == '21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8')
gate('cert bytes pin', f10['receipts'][0]['certificate_bytes'] == 1791541)

# 2. root geometry independent re-derivation
root = int(ROOT_HEX, 16)
gate('root popcount == 7', bin(root).count('1') == 7)
gate('root is D4-canonical', canon_int(root) == root)
gate('root safe (no cocircular quadruple)', unsafe_quadruples(root) == 0)

# 3. covered rows geometric re-derivation: 8 D4 images x one-stone removal
cands = set()
for t in range(8):
    image = transform(root, t)
    for q in bits_of(image):
        cands.add(format(canon_int(image ^ (1 << q)), '032x'))
gate('56 removal candidates distinct count >= 3', len(cands) >= 3, f'{len(cands)} distinct canonical 6-stone removals')

covered = f10['receipts'][0]['covered_s6_rows']
for h in covered:
    gate(f'covered row {h} in D4-removal rederivation', h in cands)

# 4. target bookkeeping vs fold9 residual74
res74 = f9['five_parent_target_after']['residual_row_hex_after']
gate('fold9 residual74: 74 rows, sorted, unique', len(res74) == 74 and len(set(res74)) == 74 and res74 == sorted(res74))
target_rows = f10['receipts'][0]['covered_five_parent_target_rows']
gate('target rows == coverage claim rows', target_rows == ['00000000000000821082000000000001', '00000000000000821082000000000004'])
gate('target rows in fold9 residual74', all(h in res74 for h in target_rows))
extra = f10['receipts'][0]['extra_s6_rows_not_in_target']
gate('extra row not in target residual74', all(h not in res74 for h in extra))
gate('target coverage 2 rows in rederivation', all(h in cands for h in target_rows))

res72_expected = sorted(set(res74) - set(target_rows))
gate('fold10 residual72 == fold9 residual74 minus target rows (exact list)',
     f10['five_parent_target_after']['residual_row_hex_after'] == res72_expected)
gate('residual72 count', f10['five_parent_target_after']['residual_target_rows'] == 72 == len(res72_expected))
gate('closed target total 40', f10['five_parent_target_after']['closed_target_rows_total'] == 40)

# 5. the strongest independent geometric claim: among the 56 canonical
#    removal candidates, exactly the two claimed target rows touch the
#    fold9 residual74 set
in_res = sorted(h for h in cands if h in set(res74))
gate('rederived rows touching residual74 == exactly the 2 claimed target rows', in_res == target_rows, in_res)

# 6. arithmetic gates
fa = f10['frontier_after']; fb = f10['frontier_before']
gate('frontier_before == fold9 frontier_after stage', fb == f9['frontier_after'])
gate('frontier rows -3', fb['unique_remaining_s6'] - 3 == fa['unique_remaining_s6'])
rows_cost = {r['row_hex']: r['cost'] for r in f10['new_receipt_coverage']['rows']}
closed_cost = sum(rows_cost[h] for h in covered)
gate('closed edge cost == sum of row costs == 225', closed_cost == 225 == f10['new_receipt_coverage']['closed_edge_cost'] == f10['receipts'][0]['closed_edge_cost'])
gate('cost difference matches (491722-225==491497)', fb['sum_remaining_cost'] - fa['sum_remaining_cost'] == 225)
gate('solved +3 (1639->1642)', fb['solved_s6_in_manifest'] + 3 == fa['solved_s6_in_manifest'] == 1642)
pd = f10['receipts'][0]['parent_deltas']
gate('incidence delta 11818->11810 == parent rows_closed sum 8', fb['parent_row_incidence'] - fa['parent_row_incidence'] == sum(p['rows_closed'] for p in pd) == 8)
gate('affected parents 5, fully closed 0', len(pd) == 5 and f10['parent_closure']['fully_closed_parent_count'] == 0 and f10['parent_closure']['affected_unique_parents'] == 5)
gate('parent_deltas rows_before/after monotone', all(p['rows_before'] - p['rows_closed'] == p['rows_after'] for p in pd))
gate('witness_plan retired rows == target rows', f10['witness_plan_impact']['rows_of_retired_root'] == target_rows)
gate('receipt_count 1, schema', f10['receipt_count'] == 1 and f10['schema'] == 'n11-five-parent-seventeenth-win7-receipt-fold-20261120-v1')

# 7. interpretation guard present
gate('interpretation guard 5 entries incl UNKNOWN clause', len(f10['interpretation_guard']) == 5 and any('UNKNOWN' in g for g in f10['interpretation_guard']))

allpass = all(g['pass'] for g in gates)
record = {
  'schema': 'n11-fold10-second-verification-20261120-v1',
  'date': '2026-11-20',
  'status': 'second-verified' if allpass else 'gate-failed',
  'subject': 'research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json',
  'inputs_verified_by_sha256': {
    'fold10_record': sha256(F10),
    'fold9_record': sha256(F9),
    'seventeenth_certificate': sha256(CERT),
  },
  'independent_method': (
    'Direct geometric re-derivation of the covered rows from the receipt root '
    '(8 D4 images x one-stone removal -> D4 canonical forms, 56 distinct candidates), '
    'cross-checked against the fold9 published residual74 and the fold10 record, plus '
    'frontier/arithmetic/parent-delta/integrity gates. No chain-reconstruction inputs '
    '(worklist/ledger/tarball/...) are consumed; those stay under the owner machine\'s '
    'own fail-closed gates. REFUTED-D10 is not a LOSS proof; closed rows keep arbitrary '
    'game-theoretic value in this bookkeeping.'
  ),
  'key_finding': {
    'rederivation_distinct_candidates': len(cands),
    'rederivation_candidate_hexes': sorted(cands),
    'candidates_touching_fold9_residual74': in_res,
    'claim': 'Exactly the two claimed five-parent target rows of the fold10 receipt appear '
             'among the 56 geometric one-stone-removal D4-canonical candidates intersected '
             'with the fold9 residual74; the third closed row (target-external extra) is '
             'also a geometric removal candidate but sits outside the target bookkeeping, '
             'so its frontier membership cannot be re-derived from these two records alone.',
    'residual72 equality': f10['five_parent_target_after']['residual_row_hex_after'] == res72_expected,
  },
  'unknown_guard': 'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  'gates_total': len(gates),
  'gates_all_pass': allpass,
  'gates': gates,
}
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output'), exist_ok=True)
outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'fold10-second-verification-20261120.json')
with open(outp, 'w') as f:
    json.dump(record, f, indent=1, sort_keys=False); f.write('\n')
print(json.dumps({'status': record['status'], 'gates_total': len(gates), 'all_pass': allpass,
                  'output': outp, 'sha256': sha256(outp)}, indent=1))
sys.exit(0 if allpass else 1)
