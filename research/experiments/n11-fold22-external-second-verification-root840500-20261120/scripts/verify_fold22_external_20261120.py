#!/usr/bin/env python3
"""External second verification of the published fold22 (K1132) receipt fold.

fold22 = WIN8-D10 receipt fold of the K1125 certificate root
00000000000000801202000000840500 into the five-parent S6 frontier chain
(record sha256 f6e011f4..., published in commit ac7b8be6... in
research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120).

This machine is a THIRD implementation: it shares no code with the published
fold22 machine (scripts/fold_win8_root840500.py) nor with the published fold21
machine.  It re-verifies, from repo-published bytes only:

  P  published byte pins (receipt, machine, builder, README of the fold22 dir)
  I  the W input tree pins (12 Git-blob + 43 SHA-256) and the fold21 machine
     pin chain; fold21 chain inputs are a subset of fold22's 55 pins
  X  four pristine re-executions of the published fold22 machine
     (same cwd x2, isolated tree/cwd/HOME, isolated + PYTHONHASHSEED=random),
     each receipt output byte-identical to the published record
  C  an independent rederivation of the whole fold-chain bookkeeping and of
     every fold22 receipt claim: base worklist 6,438 rows -> fold21 frontier
     6,136/486,243 (residual 35, five-parent target 77/112), the C(8,6)=28
     six-stone subgeometry of the root rederived by two methods, the 6 closed
     rows (claimed 3 + extra 3, closed edge cost 484), the 4 class-2 parent
     deltas (14->11, 51->48, 47->44, 69->66, total 12), frontier_after
     6,130/485,759 (solved 1,718, incidence 11,671, needed 4,438/352,207),
     five-parent target 77->80, residual 35->32, win16 candidates 5->4 with 9
     remaining claimed rows; K1125's 19-gate record, certificate bytes/
     header/rows/third-method aggregates, root safety, D4-canonicality and
     legal-move count 58 are re-derived from scratch; the K1097 refsolve
     footprint partition is rechecked
  T  two one-byte XOR tampers at this lane's own offsets (worklist offset 1099,
     K1125 certificate offset 21212) fail-closed: returncode != 0 and the
     verifier writes no output; the published machine stops before any receipt
     write at its input-pin stage
  E  interpretation guards (no game-value claim; rows are not closed as
     verdicts; 11x11 empty board / two-stone roots remain UNKNOWN)

Usage: python3 verify_fold22_external_20261120.py <W_dir> <pub_dir> <out_json>

stdlib only, no randomness, no clock in the audit JSON, fail-closed (exit 1,
no output write) on any gate failure.
"""
import ast, csv, hashlib, json, os, pathlib, re, shutil, subprocess, sys, tarfile
from itertools import combinations

W = os.path.abspath(sys.argv[1])
PUB = os.path.abspath(sys.argv[2])
OUT = os.path.abspath(sys.argv[3])

GATES = []
CUR_SECTION = 'p'
def need(ok, msg):
    # fail-closed: no audit JSON is written on any failure
    if not ok:
        print('GATE FAILED [' + CUR_SECTION + ']: ' + msg)
        sys.exit(1)
    GATES.append({'section': CUR_SECTION, 'gate': msg, 'ok': True})
def section(name):
    global CUR_SECTION
    CUR_SECTION = name

ROOT_HEX = '00000000000000801202000000840500'
CERT_REL = 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11'
REC_REL = 'output/win8-root840500-receipt-fold-20261120.json'
PUB_RECEIPT_SHA = 'f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488'
PUB_MACHINE_SHA = 'd5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d'
PUB_BUILDER_SHA = 'a73995be2ac448f2e56f804b3263330513c5bcb8a9e4042661c56e1deb4d7085'
PUB_README_SHA = '0e6861bf2970bead67ce77de9361e11a435cb27ee668e066a565a6fe808c29da'
PIN_F21_MACHINE = '44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b'
K1125_CERT_SHA = '21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc'
K1125_AUDIT_SHA = '06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886'
F21_RECORD_SHA = '9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39'
K1089_MASTER_SHA = '808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc'

sha = lambda b: hashlib.sha256(b).hexdigest()
def h(path):
    return sha(open(path, 'rb').read())

def blob_sha1(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def jload(path):
    return json.load(open(path))

# ===================== P: published bytes =====================
section('p')
pub_receipt = open(os.path.join(PUB, REC_REL), 'rb').read()
need(sha(pub_receipt) == PUB_RECEIPT_SHA, 'published fold22 receipt sha256 pin')
pub_machine_path = os.path.join(PUB, 'scripts/fold_win8_root840500.py')
need(h(pub_machine_path) == PUB_MACHINE_SHA, 'published fold22 machine sha256 pin')
need(h(os.path.join(PUB, 'scripts/build_fold22.py')) == PUB_BUILDER_SHA, 'published fold22 builder sha256 pin')
need(h(os.path.join(PUB, 'README.md')) == PUB_README_SHA, 'published fold22 README sha256 pin')
receipt = json.loads(pub_receipt)
machine_src = open(pub_machine_path).read()

def literal_dict(name, src):
    m = re.search(rf'{name} = (\{{.*?\n\}})', src, re.S)
    return ast.literal_eval(m.group(0).split('=', 1)[1]).copy() if False else ast.literal_eval(m.group(0).split('=', 1)[1])

M_PINS = literal_dict('PINS', machine_src)
M_PIN256 = literal_dict('PIN256', machine_src)
need(len(M_PINS) == 12 and len(M_PIN256) == 43, 'machine pin tables 12 blob + 43 sha256')
need(receipt['source_blob_pins'] == M_PINS, 'receipt blob-pin table == machine table')
need(receipt['source_sha256_pins'] == M_PIN256, 'receipt sha256-pin table == machine table')
need(receipt['schema'] == 'n11-five-parent-win8-root840500-receipt-fold-20261120-v1', 'receipt schema')
need(receipt['status'] == 'fold-complete', 'receipt fold-complete')
need(receipt['receipt_count'] == 1 and len(receipt['receipts']) == 1, 'single receipt')
need(receipt['receipt_ordinal'] == 'twenty-ninth (fold22, twelfth WIN8 receipt fold)', 'receipt ordinal')
need(receipt['date'] == '2026-11-20', 'receipt date')
need(receipt['single_owner_note'] == 'research/log/2026-11-20-n11-fold22-win8-root840500-single-owner-note.md', 'receipt single-owner note ref')

# ===================== I: W input pins =====================
section('i')
for rel, pin in sorted(M_PINS.items()):
    need(blob_sha1(os.path.join(W, rel)) == pin, 'W blob pin ' + rel)
for rel, pin in sorted(M_PIN256.items()):
    need(h(os.path.join(W, rel)) == pin, 'W sha256 pin ' + rel)
f21_machine_path = os.path.join(W, 'fold_win8_root80880200.py')
need(h(f21_machine_path) == PIN_F21_MACHINE == '44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b', 'fold21 machine sha256 pin in W')
f21_src = open(f21_machine_path).read()
F21_PINS = literal_dict('PINS', f21_src)
F21_PIN256 = literal_dict('PIN256', f21_src)
need(len(F21_PINS) == 12 and len(F21_PIN256) == 40, 'fold21 machine pin tables 12 blob + 40 sha256')
need(set(F21_PINS.items()) <= set(M_PINS.items()), 'fold21 blob pins subset of fold22 pins')
need(set(F21_PIN256.items()) <= set(M_PIN256.items()), 'fold21 sha256 pins subset of fold22 pins')
need(F21_PIN256 == {k: v for k, v in M_PIN256.items() if k in F21_PIN256}, 'fold21 sha256 pins agree with fold22 table values')
# fold21 record and K1125 published pins, also pinned by the declaration note
need(M_PIN256['fold21/output/win8-root80880200-receipt-fold-20261120.json'] == F21_RECORD_SHA, 'fold21 record pin == declared sha')
need(M_PIN256['k1125/output/win8-cert-extract-verification-20261120.json'] == K1125_AUDIT_SHA, 'K1125 audit pin == declared sha')
need(M_PIN256[CERT_REL] == K1125_CERT_SHA, 'K1125 certificate pin == declared sha')

# ===================== I2/C0: independent geometry primitives =====================
section('c')

# my own D4 tables (same group: 4 rotations + 4 reflections of the 11x11 board)
D4 = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0:   Xc, Yc = x, y
        elif t == 1: Xc, Yc = 10 - y, x
        elif t == 2: Xc, Yc = 10 - x, 10 - y
        elif t == 3: Xc, Yc = y, 10 - x
        elif t == 4: Xc, Yc = 10 - x, y
        elif t == 5: Xc, Yc = x, 10 - y
        elif t == 6: Xc, Yc = y, x
        else:        Xc, Yc = 10 - y, 10 - x
        tab.append(11 * Yc + Xc)
    D4.append(tab)

def bits(mask):
    out = []
    p = 0
    m = mask
    while m:
        if m & 1: out.append(p)
        m >>= 1
        p += 1
    return out

def d4_image(mask, t):
    out = 0
    for p in bits(mask):
        out |= 1 << D4[t][p]
    return out

def canon(mask):
    return min(d4_image(mask, t) for t in range(8))

def canonhex(mask):
    return format(canon(mask), '032x')

def det4(a, b, c, d):
    # 4x4 integer determinant of the cocircularity matrix rows (x^2+y^2, x, y, 1)
    pts = [a, b, c, d]
    rows = []
    for p in pts:
        x, y = p % 11, p // 11
        rows.append([x * x + y * y, x, y, 1])
    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    total = 0
    for j in range(4):
        if rows[0][j] == 0: continue
        minor = [[r[k] for k in range(4) if k != j] for r in rows[1:]]
        total += ((-1) ** j) * rows[0][j] * det3(minor)
    return total

# independent legal-move rederivation (survival-move convention):
# an empty cell is legal iff it is not cocircular/collinear (det4 == 0) with
# any triple of the stones on the board.
def legal_moves(mask):
    stones = bits(mask)
    blocked = set(stones)
    for a, b, c in combinations(stones, 3):
        for d in range(121):
            if d in (a, b, c): continue
            if det4(a, b, c, d) == 0:
                blocked.add(d)
    return [d for d in range(121) if d not in blocked]

# ===================== C1: base worklist and legacy chain =====================
def wj(rel):
    return jload(os.path.join(W, rel))

wl = {}
with open(os.path.join(W, 'inputs/worklist.csv')) as f:
    rd = csv.DictReader(f)
    cols = rd.fieldnames
    for a in rd:
        wl[a['s6_canonical_hex']] = (int(a['own_candidates_s6_s7_edge_cost']), a['category'])
need(len(wl) == 6438, 'worklist row count 6438')
need(all(len(k) == 32 for k in wl), 'worklist row hex width 32')

led = wj('inputs/ledger.json')
gf = wj('inputs/globalFold.json')
old66 = set(led['derived']['closed_rows_66'])
old_global = set(x['row_hex'] for x in gf['receipts_by_row'])
open_set = {k: v for k, v in wl.items() if k not in old66 and k not in old_global}
need(len(open_set) == 6259 and sum(c for c, _ in open_set.values()) == 495507, 'global-fold base 6259/495507')

prev = wj('inputs/previousCostFold.json')
prior = set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])
open_set = {k: v for k, v in open_set.items() if k not in prior}
need(len(open_set) == 6240 and sum(c for c, _ in open_set.values()) == 493965, 'cost78c/79c fold 6240/493965')

with tarfile.open(os.path.join(W, 'inputs/firstFoldTarball.tar.gz'), 'r:gz') as t:
    first = None
    for m in t.getmembers():
        if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
            first = json.load(t.extractfile(m))
need(first and first['status'] == 'fold-complete'
     and first['schema'] == 'n11-five-parent-first-win7-receipt-fold-20261119-v1', 'first fold record gate')
rows_first = set(x['row_hex'] for x in first['new_receipt_coverage']['rows'])
open_set = {k: v for k, v in open_set.items() if k not in rows_first}
need(len(open_set) == 6236 and sum(c for c, _ in open_set.values()) == 493703, 'first fold 6236/493703')

stf = wj('ex48/output/secondThirdFold.json')
need(stf['status'] == 'fold-complete' and stf['receipt_count'] == 2, 'second-third record gate')
rows_23 = []
for rr in stf['receipts']:
    rows_23.extend(rr['covered_s6_rows'])
open_set = {k: v for k, v in open_set.items() if k not in set(rows_23)}
need(len(open_set) == 6229 and sum(c for c, _ in open_set.values()) == 493184, 'second-third 6229/493184')

f4 = wj('fold4rec/fold4.json')
need(f4['status'] == 'fold-complete'
     and f4['schema'] == 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1', 'fold4 record gate')
rows_4 = set(x['row_hex'] for x in f4['new_receipt_coverage']['rows'])
open_set = {k: v for k, v in open_set.items() if k not in rows_4}
need(len(open_set) == 6226 and sum(c for c, _ in open_set.values()) == 492970, 'fourth fold 6226/492970')

f56 = wj('fold56rec/fold56.json')
need(f56['status'] == 'fold-complete'
     and f56['schema'] == 'n11-five-parent-fifth-sixth-win7-receipt-fold-20261119-v1', 'fold56 record gate')
rows_56 = set(x['row_hex'] for x in f56['new_receipt_coverage']['rows'])
open_set = {k: v for k, v in open_set.items() if k not in rows_56}
need(len(open_set) == 6224 and sum(c for c, _ in open_set.values()) == 492830, 'fifth-sixth fold 6224/492830')

f7 = wj('foldv2/output/seventh-win7-receipt-fold-20261119.json')
need(f7['status'] == 'fold-complete' and f7['receipt_count'] == 1, 'fold7 record gate')
rows_7 = []
for rr in f7['receipts']:
    rows_7.extend(rr['covered_s6_rows'])
open_set = {k: v for k, v in open_set.items() if k not in set(rows_7)}
need(len(open_set) == 6223 and sum(c for c, _ in open_set.values()) == 492762, 'seventh fold 6223/492762')

f8 = wj('foldv2/output/eighth-win7-receipt-fold-20261119.json')
need(f8['status'] == 'fold-complete' and f8['receipt_count'] == 1, 'fold8 record gate')
rows_8 = []
for rr in f8['receipts']:
    rows_8.extend(rr['covered_s6_rows'])
open_set = {k: v for k, v in open_set.items() if k not in set(rows_8)}
need(len(open_set) == 6222 and sum(c for c, _ in open_set.values()) == 492688, 'eighth fold 6222/492688')
receipt_ids = {'first': len(rows_first), 'seventh': len(rows_7), 'eighth': len(rows_8)}

# census / parent machinery
census = wj('inputs/census.json')
parents = {p['hex']: p for p in census['open_s5_census']}
parents_by_int = {int(k, 16): k for k in parents}

_parents_cache = {}
def row_parents(hexrow):
    if hexrow in _parents_cache:
        return _parents_cache[hexrow]
    mask = int(hexrow, 16)
    ps = set()
    for q in bits(mask):
        c = canon(mask ^ (1 << q))
        if c in parents_by_int:
            ps.add(parents_by_int[c])
    _parents_cache[hexrow] = ps
    return ps

def demand_of(hexrow):
    d = {'c1': 0, 'c2': 0, 'c4': 0}
    for p in row_parents(hexrow):
        cl = parents[p]['classes']
        if cl & 1: d['c1'] += 1
        if cl & 2: d['c2'] += 1
        if cl & 4: d['c4'] += 1
    return d

def needed_rows(openset):
    return [k for k in openset if demand_of(k)['c1'] == 0]

def stats(openset, incidence, solved):
    need_rows = needed_rows(openset)
    return {
        'solved_s6_in_manifest': solved,
        'remaining_s5_orbits': sum(1 for v in incidence.values() if v > 0),
        'unique_remaining_s6': len(openset),
        'sum_remaining_cost': sum(c for c, _ in openset.values()),
        's6_needed_by_open_classes': len(need_rows),
        'cost_needed_by_open_classes': sum(openset[k][0] for k in need_rows),
        'parent_row_incidence': sum(incidence.values()),
    }

# ninth-twelfth
tf9 = wj('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json')
need(tf9['status'] == 'fold-complete'
     and tf9['schema'] == 'n11-five-parent-ninth-twelfth-win7-receipt-fold-20261119-v1'
     and tf9['receipt_count'] == 4, 'fold9 record gate')
rows_9 = []
for rr in tf9['receipts']:
    need(len(rr['covered_s6_rows']) >= 1, 'fold9 receipt closes nothing')
    rows_9.extend(rr['covered_s6_rows'])
for k in rows_9:
    need(k in open_set, 'fold10 row not walk: ' + k)
open_set = {k: v for k, v in open_set.items() if k not in set(rows_9)}
fa9 = tf9['frontier_after']
need(len(open_set) == 6213 and sum(c for c, _ in open_set.values()) == 492021, 'post-fold9 6213/492021')
need(fa9['unique_remaining_s6'] == 6213 and fa9['sum_remaining_cost'] == 492021
     and fa9['solved_s6_in_manifest'] == 1635, 'fold9 frontier_after published values solved 1635')
inc = {p: 0 for p in parents}
for k in open_set:
    for p in row_parents(k):
        inc[p] += 1
need(sum(inc.values()) == fa9['parent_row_incidence'] == 11826, 'fold9 base incidence 11826')

# thirteenth..sixteenth (windfall4)
fs13 = wj('fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json')
need(fs13['status'] == 'fold-complete'
     and fs13['schema'] == 'n11-five-parent-windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120-v1'
     and fs13['receipt_count'] == 4, 'fs13 record gate')
rows_1316 = []
for rr in fs13['receipts']:
    need(len(rr['covered_s6_rows']) >= 1, 'fs13 receipt closes nothing')
    rows_1316.extend(rr['covered_s6_rows'])
need(len(rows_1316) == len(set(rows_1316)), 'fs13 rows unique')
for k in rows_1316:
    need(k in open_set, 'fs13 row not open: ' + k)
open_set = {k: v for k, v in open_set.items() if k not in set(rows_1316)}
fa13 = fs13['frontier_after']
need(len(open_set) == 6209 and sum(c for c, _ in open_set.values()) == 491722, 'post-fs13 6209/491722')
for k in rows_1316:
    for p in row_parents(k):
        inc[p] -= 1
need(stats(open_set, inc, fa13['solved_s6_in_manifest']) == fa13, 'fs13 frontier_after full recompute match')
residual = fs13['five_parent_target_after']['residual_row_hex_after']
need(len(residual) == 74 and len(set(residual)) == 74 and residual == sorted(residual), 'residual74 sorted unique')
residual_set = set(residual)
need(fs13['five_parent_target_after']['closed_target_rows_total'] == 38, 'fs13 closed target 38')

# target machinery
audit = wj('inputs/audit.json')
need(audit['all_pass'] is True and audit['check_count'] == 23
     and audit['derived']['maximum_root_span'] == 2, 'independent audit json header')
target_union = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(target_union) == 112, 'five-parent target rows 112')
need(all(k in target_union for k in residual), 'residual74 subset of target union')

closed_history = set()
closed_history |= old66 | old_global | prior | rows_first | set(rows_23)
closed_history |= rows_4 | rows_56 | set(rows_7) | set(rows_8) | set(rows_9) | set(rows_1316)

# generic chain step for the published WIN8 receipt records fold10..fold21
def chain_step(tag, record_path, schema, covered_n, target_n, closed_total, frontier_stats):
    global open_set, inc, residual, residual_set, closed_history
    f = wj(record_path)
    need(f['status'] == 'fold-complete', tag + ' fold-complete')
    need(f['schema'] == schema, tag + ' schema')
    need(f['receipt_count'] == 1 and len(f['receipts']) == 1, tag + ' single receipt')
    rr = f['receipts'][0]
    rows = list(rr['covered_s6_rows'])
    need(len(rows) == len(set(rows)) == covered_n, tag + ' covered rows unique ' + str(covered_n))
    for k in rows:
        need(k in open_set, tag + ' covered row was open: ' + k)
        need(k in wl, tag + ' covered row in worklist: ' + k)
    for rec_row in f['new_receipt_coverage']['rows']:
        need(rec_row['cost'] == wl[rec_row['row_hex']][0], tag + ' recorded cost matches worklist')
        need(rec_row['row_hex'] in rows, tag + ' coverage row among covered')
    need(len(f['new_receipt_coverage']['rows']) == covered_n, tag + ' coverage rows count')
    need(rr['closed_edge_cost'] == sum(wl[k][0] for k in rows), tag + ' closed edge cost recomputed')
    nxt = {k: v for k, v in open_set.items() if k not in set(rows)}
    for k in rows:
        for p in row_parents(k):
            inc[p] -= 1
    fa = f['frontier_after']
    my_stats = stats(nxt, inc, fa['solved_s6_in_manifest'])
    need(my_stats == fa, tag + ' frontier_after full recompute match')
    need(my_stats['unique_remaining_s6'] == frontier_stats[0]
         and my_stats['sum_remaining_cost'] == frontier_stats[1], tag + ' frontier ' + str(frontier_stats))
    need(fa['solved_s6_in_manifest'] == prev_solved[0] + covered_n, tag + ' solved increment matches covered rows')
    prev_solved[0] = fa['solved_s6_in_manifest']
    tgt = list(rr['covered_five_parent_target_rows'])
    need(len(tgt) == target_n and set(tgt) <= residual_set, tag + ' target rows subset of residual; ' + str(target_n))
    extra = [k for k in rows if k not in residual_set]
    need(extra == rr['extra_s6_rows_not_in_target'], tag + ' extra rows recorded')
    new_res = f['five_parent_target_after']['residual_row_hex_after']
    need(new_res == sorted(residual_set - set(tgt)), tag + ' residual recompute == residual minus target rows')
    need(len(new_res) == len(residual) - target_n, tag + ' residual count decrement')
    need(len(new_res) == len(set(new_res)), tag + ' residual unique')
    need(f['five_parent_target_after']['closed_target_rows_total'] == closed_total, tag + ' closed target total ' + str(closed_total))
    for k in new_res:
        need(k in nxt, tag + ' residual row still open')
    open_set = nxt
    residual = new_res
    residual_set = set(residual)
    closed_history |= set(rows)
    return f, rr

prev_solved = [fa13['solved_s6_in_manifest']]

f10, rr10 = chain_step('fold10', 'fold10/output/seventeenth-win7-receipt-fold-20261120.json',
    'n11-five-parent-seventeenth-win7-receipt-fold-20261120-v1', 3, 2, 40, (6206, 491497))
f11, rr11 = chain_step('fold11', 'fold11/output/win8-root8003180-receipt-fold-20261120.json',
    'n11-five-parent-win8-root8003180-receipt-fold-20261120-v1', 5, 4, 44, (6201, 491110))
f12, rr12 = chain_step('fold12', 'fold12/output/win8-root8005021-receipt-fold-20261120.json',
    'n11-five-parent-win8-root8005021-receipt-fold-20261120-v1', 8, 3, 47, (6193, 490526))
f13, rr13 = chain_step('fold13', 'fold13/output/win8-root9840004-receipt-fold-20261120.json',
    'n11-five-parent-win8-root9840004-receipt-fold-20261120-v1', 9, 3, 50, (6184, 489813))
f14, rr14 = chain_step('fold14', 'fold14/output/win8-root9090022-receipt-fold-20261120.json',
    'n11-five-parent-win8-root9090022-receipt-fold-20261120-v1', 5, 4, 54, (6179, 489440))
f15, rr15 = chain_step('fold15', 'fold15/output/win8-root120000038-receipt-fold-20261120.json',
    'n11-five-parent-win8-root120000038-receipt-fold-20261120-v1', 6, 3, 57, (6173, 488954))
f16, rr16 = chain_step('fold16', 'fold16/output/win8-root8890020-receipt-fold-20261120.json',
    'n11-five-parent-win8-root8890020-receipt-fold-20261120-v1', 5, 4, 61, (6168, 488575))
f17, rr17 = chain_step('fold17', 'fold17/output/win8-root22081000-receipt-fold-20261120.json',
    'n11-five-parent-win8-root22081000-receipt-fold-20261120-v1', 7, 3, 64, (6161, 488094))
f18, rr18 = chain_step('fold18', 'fold18/output/win8-root00901010-receipt-fold-20261120.json',
    'n11-five-parent-win8-root00901010-receipt-fold-20261120-v1', 4, 3, 67, (6157, 487800))
f19, rr19 = chain_step('fold19', 'fold19/output/win8-root1009000-receipt-fold-20261120.json',
    'n11-five-parent-win8-root1009000-receipt-fold-20261120-v1', 5, 4, 71, (6152, 487418))
f20, rr20 = chain_step('fold20', 'fold20/output/win8-root08d10000-receipt-fold-20261120.json',
    'n11-five-parent-win8-root08d10000-receipt-fold-20261120-v1', 8, 3, 74, (6144, 486819))
f21, rr21 = chain_step('fold21', 'fold21/output/win8-root80880200-receipt-fold-20261120.json',
    'n11-five-parent-win8-root80880200-receipt-fold-20261120-v1', 8, 3, 77, (6136, 486243))
need(len(residual) == 35, 'post-fold21 residual 35')
f21_rec_sha = h(os.path.join(W, 'fold21/output/win8-root80880200-receipt-fold-20261120.json'))
need(f21_rec_sha == F21_RECORD_SHA, 'fold21 record in W byte-identical to declared sha')
fa21 = f21['frontier_after']
my_stats_35 = stats(open_set, inc, fa21['solved_s6_in_manifest'])
need(my_stats_35 == fa21, 'fold21 frontier_after full recompute match')
need(receipt['frontier_before'] == fa21, 'receipt frontier_before == fold21 record frontier_after')
need(receipt['previous_fold']['frontier_after'] == fa21, 'receipt previous_fold frontier == fold21 values')
need(receipt['previous_fold']['record'].endswith('9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39)'),
     'receipt previous_fold record ref ends with fold21 sha')

# ===================== C2: K1125 certificate record (19 gates) =====================
k1125 = wj('k1125/output/win8-cert-extract-verification-20261120.json')
need(k1125['schema'] == 'win8-cert-extract-verification-v1', 'k1125 schema')
need(k1125['all_gates_pass'] is True and k1125['gate_count'] == 19 and len(k1125['gates']) == 19, 'k1125 19 gates')
need(all(g['passed'] for g in k1125['gates']), 'k1125 every gate passed')
need(k1125['root'] == ROOT_HEX, 'k1125 root hex')
gd = {g['gate']: g['detail'] for g in k1125['gates']}
need(gd['g01_k1089_master_sha256_pin'] == K1089_MASTER_SHA, 'k1125 g01 k1089 master sha')
CLAIM = sorted(gd['g07_k1089_root_claimed_coverage_3rows'])
need(len(CLAIM) == 3 and CLAIM == sorted(k1125['recorded']['k1089_claimed_coverage_rows']), 'k1125 claim rows')
need(gd['g05_root_mobility_58'] == 58, 'k1125 mobility 58')
need(gd['g06_k1089_root_probes_win_uncapped']['andclose1']['capped'] is False
     and gd['g06_k1089_root_probes_win_uncapped']['andclose1']['loss'] is True
     and gd['g06_k1089_root_probes_win_uncapped']['andclose1']['nodes'] == 736409
     and gd['g06_k1089_root_probes_win_uncapped']['andclose0']['capped'] is False
     and gd['g06_k1089_root_probes_win_uncapped']['andclose0']['loss'] is True
     and gd['g06_k1089_root_probes_win_uncapped']['andclose0']['nodes'] == 878391
     and gd['g06_k1089_root_probes_win_uncapped']['andclose0']['terminalStoneRange'] == [14, 18]
     and gd['g06_k1089_root_probes_win_uncapped']['andclose1']['terminalStoneRange'] == [14, 18], 'k1125 uncapped probes 736409/878391')
need(gd['g08_probe_reproduction_matches_k1089'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1125 probe reproduction')
need(gd['g13_node_accounting_chunk_vs_single'] == {'a1_chunk_total_nodes': 2310103, 'b_single_process_nodes': 1984636}, 'k1125 node accounting A1/B')
need(gd['g16_third_method_traversal_pass']['missing'] == 0 and gd['g16_third_method_traversal_pass']['extra'] == 0
     and gd['g16_third_method_traversal_pass']['failure'] is None, 'k1125 third-method zero miss/extra')
need(len(gd['g19_k1097_refsolve_footprint_match']['claimed']) == 3
     and sorted(gd['g19_k1097_refsolve_footprint_match']['claimed']) == CLAIM, 'k1125 g19 footprint claimed == CLAIM')
need(gd['g19_k1097_refsolve_footprint_match']['k1097_sha256'] == M_PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1125 g19 k1097 sha pin')

cert_rec = k1125['recorded']['certificate']
cert_bytes = open(os.path.join(W, CERT_REL), 'rb').read()
need(sha(cert_bytes) == cert_rec['sha256'] == M_PIN256[CERT_REL] == K1125_CERT_SHA, 'k1125 certificate sha triple pin')
need(cert_rec['bytes'] == len(cert_bytes) == 1067425, 'k1125 certificate bytes 1067425')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'certificate header line')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'certificate root line')
need(cert_rec['rows'] == 29468 == len(cert_lines) - 2, 'certificate rows 29468')
data_rows = cert_lines[2:]
need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'certificate row format')
need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'certificate rows sorted unique')
tm = k1125['recorded']['third_method']
need(tm['root_first_moves'] == 58 and tm['terminal_count'] == 9810 and tm['terminal_range'] == [14, 18]
     and tm['visited_states'] == 59990 and tm['winner_states'] == 38458 and tm['loser_states'] == 11722
     and tm['loser_reply_edges'] == 52360, 'k1125 third-method aggregates 58/9810/[14,18]/59990/38458/11722/52360')
rcv = receipt['receipts'][0]
need(rcv['unique_strategy_rows'] == 29468 and rcv['certificate_bytes'] == 1067425, 'receipt certificate size fields')
need(rcv['certificate_sha256'] == K1125_CERT_SHA, 'receipt certificate sha field')

# ===================== C3: root geometry rederivation =====================
root_mask = int(ROOT_HEX, 16)
need(len(bits(root_mask)) == 8, 'root has 8 stones')
stone_pairs_quads = 0
for quad in combinations(bits(root_mask), 4):
    if det4(*quad) == 0:
        stone_pairs_quads += 1
need(stone_pairs_quads == 0, 'root quadruple-free (no cocircular/collinear stone quad)')
need(canon(root_mask) == root_mask, 'root D4 canonical')
lmv = legal_moves(root_mask)
need(len(lmv) == 58, 'root legal-move count independent rederivation 58, got %d' % len(lmv))
need(int(int(ROOT_HEX, 16)).bit_count() == 8, 'root popcount sanity 8')

# method A: 8 D4 images x C(8,2) two-stone removals
setA = set()
for t in range(8):
    image = d4_image(root_mask, t)
    for b1, b2 in combinations(bits(image), 2):
        setA.add(canonhex(image ^ (1 << b1) ^ (1 << b2)))
# method B: C(8,6)=28 six-stone subsets
setB = set()
for six in combinations(bits(root_mask), 6):
    sm = 0
    for b in six:
        sm |= (1 << b)
    setB.add(canonhex(sm))
need(setA == setB, 'methods A and B canonical row sets equal (D4 equivariance)')
need(len(setA) <= 28, 'canonical row count bound 28')
need(8 * 28 == 224, 'method A op count 224')

# classification
cls = {}
for rx in sorted(setB):
    if rx in open_set:
        cls[rx] = 'open-frontier'
    elif rx in closed_history:
        cls[rx] = 'closed-before-this-receipt'
    elif rx in wl:
        cls[rx] = 'worklist-but-not-open'
        need(False, 'chain inconsistency row ' + rx)
    else:
        cls[rx] = 'not-in-worklist'
need(receipt['six_stone_subgeometry_classification'] == cls, '28-row classification field == rederived')
need(sum(1 for v in cls.values() if v == 'open-frontier') == 6, 'six rows open-frontier')
need(sum(1 for v in cls.values() if v == 'not-in-worklist') == 22, 'twenty-two rows not-in-worklist')
need(sum(1 for v in cls.values() if v == 'closed-before-this-receipt') == 0, 'zero rows closed before')

# ===================== C4: fold22 receipt application rederivation =====================
root_rows = sorted(rx for rx in setA if rx in open_set)
need(len(root_rows) == 6, 'fold22 receipt closes exactly 6 open rows, got %d' % len(root_rows))
need(root_rows == sorted(set(root_rows)), 'rederived rows unique')
target_new = sorted(rx for rx in root_rows if rx in residual_set)
need(target_new == CLAIM, 'rederived target rows == published claim')
extra_rows = [rx for rx in root_rows if rx not in residual_set]
need(sorted(extra_rows) == rcv['extra_s6_rows_not_in_target'], 'extra rows == published extra')
need(sorted(target_new) == rcv['covered_five_parent_target_rows'], 'receipt covered target rows == rederived')
need(root_rows == rcv['covered_s6_rows'], 'receipt covered_s6_rows == rederived 6 rows')
closed_cost = sum(open_set[rx][0] for rx in root_rows)
need(closed_cost == 484 == rcv['closed_edge_cost'], 'closed edge cost 484')
costs = {rx: open_set[rx] for rx in root_rows}
need(sum(c for c, _ in costs.values()) == 484, 'cost sum sanity')

# per-row coverage rows
cov_rows = []
for rx in root_rows:
    cov_rows.append({'row_hex': rx, 'cost': wl[rx][0], 'category': wl[rx][1], 'demand': demand_of(rx),
                     'parents': sorted(row_parents(rx)),
                     'receipt': {'root': ROOT_HEX, 'verdict': 'WIN8-D10'}})
need(receipt['new_receipt_coverage']['rows'] == cov_rows, 'receipt coverage rows == rederived')
need(receipt['new_receipt_coverage']['unique_s6_rows'] == 6
     and receipt['new_receipt_coverage']['closed_edge_cost'] == 484, 'receipt coverage totals')
demand_all_c2 = all(demand_of(rx)['c2'] == 2 and demand_of(rx)['c1'] == 0 and demand_of(rx)['c4'] == 0 for rx in root_rows)
need(demand_all_c2, 'all six closed rows are c2x2 demand rows')

# parent deltas
pdeltas_map = {}
for rx in root_rows:
    for p in row_parents(rx):
        pdeltas_map[p] = pdeltas_map.get(p, 0) + 1
pdeltas = []
for p in sorted(pdeltas_map):
    before = inc[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'],
                    'rows_before': before, 'rows_closed': pdeltas_map[p],
                    'rows_after': before - pdeltas_map[p]})
need(pdeltas == rcv['parent_deltas'], 'parent deltas == rederived (4 class-2 parents)')
need(len(pdeltas) == 4 == rcv['affected_parents'], 'four affected parents')
need(all(d['classes'] == 2 for d in pdeltas), 'all affected parents class 2')
need(all(d['rows_closed'] == 3 for d in pdeltas) and sum(d['rows_closed'] for d in pdeltas) == 12, 'parent-delta total 12')
need(receipt['parent_closure'] == {'fully_closed_parent_count': 0, 'affected_unique_parents': 4}, 'parent closure block')

# apply the receipt
open_after = {k: v for k, v in open_set.items() if k not in set(root_rows)}
for rx in root_rows:
    for p in row_parents(rx):
        inc[p] -= 1
solved_after = fa21['solved_s6_in_manifest'] + len(root_rows)
need(solved_after == 1718, 'solved after fold22 1718')
fa_after = stats(open_after, inc, solved_after)
need(fa_after == receipt['frontier_after'], 'receipt frontier_after == rederived (6130/485759 et al.)')
need(fa_after['unique_remaining_s6'] == 6130 and fa_after['sum_remaining_cost'] == 485759
     and fa_after['parent_row_incidence'] == 11671 and fa_after['s6_needed_by_open_classes'] == 4438
     and fa_after['cost_needed_by_open_classes'] == 352207, 'declared frontier_after tensor')

# five-parent target accounting
closed_all = 77 + len(target_new)
need(closed_all == 80, 'closed target total 80')
residual_after = sorted(residual_set - set(target_new))
need(len(residual_after) == 32, 'residual after fold22 32')
need(receipt['five_parent_target_after']['closed_target_rows_total'] == 80
     and receipt['five_parent_target_after']['residual_target_rows'] == 32
     and receipt['five_parent_target_after']['residual_row_hex_after'] == residual_after,
     'receipt five_parent_target_after == rederived')
for rx in residual_after:
    need(rx in open_after, 'residual row still open after fold22')

# ===================== C5: K1097 refsolve plan crosscheck =====================
k1097 = wj('k1097/output/safe8-refuted50-refsolve-20261120.json')
need(k1097['status'] == 'refsolve-computed', 'k1097 status')
need(len(k1097['gates']) == 27 and all(g['ok'] for g in k1097['gates']), 'k1097 27 gates all ok')
foot = k1097['win16_intrinsic_footprints']
need(ROOT_HEX in foot and len(foot) == 16, 'k1097 footprint 16 roots incl. root')
need(foot[ROOT_HEX]['intrinsic_equals_claimed'] is True, 'root intrinsic == claimed')
need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM == sorted(foot[ROOT_HEX]['intrinsic']), 'footprint claimed == intrinsic == CLAIM')
all_claims = []
for r in sorted(foot):
    need(len(foot[r]['claimed']) == len(set(foot[r]['claimed'])), 'claimed rows unique per root ' + r)
    all_claims.extend(foot[r]['claimed'])
need(len(all_claims) == 49 and len(set(all_claims)) == 49, 'win16 claims 49 distinct rows')
per_row_count = {}
for r in foot:
    for k in foot[r]['claimed']:
        per_row_count[k] = per_row_count.get(k, 0) + 1
need(all(v == 1 for v in per_row_count.values()), 'win16 claims exactly-once partition')
need(all(k in residual_set for k in CLAIM), 'CLAIM rows inside residual35')

# retired candidates walked from the published chain records themselves
CHAIN_FOLDS = [(f11, rr11, 'fold11'), (f12, rr12, 'fold12'), (f13, rr13, 'fold13'),
               (f14, rr14, 'fold14'), (f15, rr15, 'fold15'), (f16, rr16, 'fold16'),
               (f17, rr17, 'fold17'), (f18, rr18, 'fold18'), (f19, rr19, 'fold19'),
               (f20, rr20, 'fold20'), (f21, rr21, 'fold21')]
retired = {}
for f, rr, tag in CHAIN_FOLDS:
    wcp = f['win_candidate_plan_impact']
    need('retired_win_candidate_root' in wcp, tag + ' records retired candidate root')
    r0 = wcp['retired_win_candidate_root']
    need(r0 not in retired, tag + ' retired root unique: ' + r0)
    need(r0 == rr['root'], tag + ' retired root == receipt root')
    retired[r0] = sorted(wcp['rows_of_retired_root'])
    need(retired[r0] == sorted(foot[r0]['claimed']), tag + ' retired rows == footprint claimed')
retired[ROOT_HEX] = CLAIM
need(len(retired) == 12, 'twelve retired win16 candidate roots (fold11..fold22)')
remaining_roots = sorted(set(foot) - set(retired))
need(len(remaining_roots) == 4 == receipt['win_candidate_plan_impact']['win16_candidates_remaining'], 'four remaining candidates')
remaining_rows = []
for r in remaining_roots:
    remaining_rows.extend(foot[r]['claimed'])
need(len(remaining_rows) == 9 == receipt['win_candidate_plan_impact']['win16_claimed_rows_remaining'], 'nine remaining claimed rows')
for k in remaining_rows:
    need(k not in set(root_rows), 'remaining claimed row not closed by this receipt: ' + k)
    need(k in open_after, 'remaining claimed row still open: ' + k)
wcp22 = receipt['win_candidate_plan_impact']
need(wcp22['retired_win_candidate_root'] == ROOT_HEX and wcp22['rows_of_retired_root'] == CLAIM
     and wcp22['retired_root_predecessor'] == '00000000000000801202000800880200'
     and wcp22['residual23_untouched'] is True, 'receipt win impact fields')
residual23 = k1097['exclusion']['residual23_rows']
need(len(residual23) == 23 and sorted(residual23) == residual23, 'residual23 sorted 23')
need(not (set(residual23) & set(all_claims)), 'residual23 disjoint from win16 claims')
need(not (set(residual23) & set(root_rows)), 'residual23 untouched by this receipt (closed rows)')
need(ROOT_HEX not in json.dumps(k1097['scope1_refsolve_residual23']['greedy_selection']),
     'root not in residual23 greedy selection')
need(set(root_rows) == set(target_new) | set(extra_rows), 'closed rows split target/extra')

# receipt narrative blocks (byte pins on the published strings)
NOTE_EXPECTED = receipt['win_candidate_plan_impact']['note']
need(NOTE_EXPECTED.startswith('Observation only.') and '49-4-3-3-4-3-4-3-3-4-3-3-3 = 9' in NOTE_EXPECTED, 'win impact note arithmetic string')
VJS = receipt['verdict_join_summary']
need(VJS['join_basis'].startswith('published fold21 chain frontier') and 'FOLD_PREVERIFIED_CHAIN' not in VJS['join_basis'], 'verdict join basis string')
need(VJS['receipt_root_is'].startswith('certificate-backed WIN8-D10 (K1125'), 'receipt root is string')
CS = receipt['certificate_source']
need(CS['verification_sha256'] == K1125_AUDIT_SHA and CS['certificate_sha256'] == K1125_CERT_SHA
     and CS['certificate_path'].endswith('win8-root-00000000000000801202000000840500-20261120.n11')
     and CS['k1089_sweep_record'].startswith('research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/output/.input-k1089.json')
     and CS['claims_record'].startswith('research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120'), 'certificate source block')
IV = rcv['independent_verification']
need(IV['extraction_and_triple']['gates'] == 19 and IV['extraction_and_triple']['all_pass'] is True
     and IV['extraction_and_triple']['third_method_aggregates'] == tm
     and IV['coverage_geometry_two_methods']['d4_images_two_stone_removals_ops'] == 224
     and IV['coverage_geometry_two_methods']['c86_subsets'] == 28
     and IV['coverage_geometry_two_methods']['canonical_row_sets_equal'] is True
     and IV['coverage_geometry_two_methods']['canonical_rows'] == sorted(setB)
     and IV['cross_method_union_exact'] is True, 'receipt independent_verification block == rederived')
need(rcv['root'] == rcv['raw_root_hex'] == ROOT_HEX and rcv['stones'] == 8
     and rcv['verdict'] == 'WIN8-D10' and rcv['receipt'] == 'twenty-ninth'
     and rcv['legal_next_moves'] == 58, 'receipt header fields')
ctrl = receipt['controls']
need(len(ctrl) == 70 and all(v is True for v in ctrl.values()), 'receipt controls 70 all true')
GUARD_EXPECTED = [
    'WIN8-D10 proves a first-player win within depth 10 only from the eight-stone root of this receipt.',
    'The receipt closes its S6 rows in the frontier through the published two-stone-removal cover convention (refsolve coverage_of82 / K1096 cover semantics); it proves nothing about the empty board or any two-stone root.',
    'The closed rows are a bookkeeping closure of the five-parent depth-10 receipt chain, not a LOSS proof of the rows.',
    'REFUTED-D10 witnesses are NOT LOSS proofs; node counts and solved counts are not win/loss readings.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
]
need(receipt['interpretation_guard'] == GUARD_EXPECTED, 'interpretation guard 5 statements')

# ===================== X: pristine re-executions of the fold22 machine =====================
section('x')
SCRATCH = '/home/user/work/f22ext/runs'
os.makedirs(SCRATCH, exist_ok=True)

def run_fold22(wdir, env_extra, label, cwd=None):
    outdir = os.path.join(wdir, 'fold22', 'output')
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/root'),
           'FOLD22_W': wdir}
    env.update(env_extra)
    p = subprocess.run([sys.executable, os.path.join(PUB, 'scripts', 'fold_win8_root840500.py')],
                       capture_output=True, text=True, env=env, cwd=cwd or SCRATCH, timeout=600)
    return p, (outdir + '/win8-root840500-receipt-fold-20261120.json')

# X1/X2: published cwd, same W
for i in (1, 2):
    p, outp = run_fold22(W, {}, f'x{i}')
    need(p.returncode == 0, f'x{i} returncode 0, got {p.returncode}')
    need(p.stderr.strip() == '', f'x{i} clean stderr')
    need(sha(open(outp, 'rb').read()) == PUB_RECEIPT_SHA, f'x{i} rerun receipt byte-identical to published record')
    need(os.path.exists(outp), f'x{i} output written')

# X3: isolated tree, isolated cwd, isolated HOME
iso3 = os.path.join(SCRATCH, 'W-x3')
if os.path.isdir(iso3):
    shutil.rmtree(iso3)
os.makedirs(os.path.join(SCRATCH, 'cwd-x3'), exist_ok=True)
open(os.path.join(SCRATCH, 'cwd-x3', 'iso-marker'), 'w').write('')
shutil.copytree(W, iso3)
cwd3 = os.path.join(SCRATCH, 'cwd-x3')
p3, outp3 = run_fold22(iso3, {'HOME': cwd3}, 'x3', cwd=cwd3)
need(p3.returncode == 0, 'x3 returncode 0, got %d' % p3.returncode)
need(p3.stderr.strip() == '', 'x3 clean stderr')
need(sha(open(outp3, 'rb').read()) == PUB_RECEIPT_SHA, 'x3 isolated receipt byte-identical to published record')

# X4: isolated tree + PYTHONHASHSEED=random (hash-order independence proof)
iso4 = os.path.join(SCRATCH, 'W-x4')
if os.path.isdir(iso4):
    shutil.rmtree(iso4)
shutil.copytree(W, iso4)
cwd4 = os.path.join(SCRATCH, 'cwd-x4')
os.makedirs(cwd4)
p4, outp4 = run_fold22(iso4, {'PYTHONHASHSEED': 'random', 'HOME': cwd4}, 'x4', cwd=cwd4)
need(p4.returncode == 0, 'x4 returncode 0, got %d' % p4.returncode)
need(p4.stderr.strip() == '', 'x4 clean stderr')
need(sha(open(outp4, 'rb').read()) == PUB_RECEIPT_SHA, 'x4 PYTHONHASHSEED=random receipt byte-identical to published record')
shutil.rmtree(iso3); shutil.rmtree(iso4)
need(open(outp, 'rb').read() == pub_receipt, 'x2 output file bytes == published receipt bytes')

# ===================== T: tamper fail-closed probes =====================
section('t')

def tamper_run(label, relpath, offset, expect_msg):
    WT = os.path.join(SCRATCH, 'W-tamper')
    if os.path.isdir(WT):
        shutil.rmtree(WT)
    shutil.copytree(W, WT)
    tgt = os.path.join(WT, relpath)
    data = bytearray(open(tgt, 'rb').read())
    need(offset < len(data), label + ' offset in range')
    orig = data[offset]
    data[offset] = orig ^ 0x01
    open(tgt, 'wb').write(bytes(data))
    need(h(tgt) != h(os.path.join(W, relpath)), label + ' tamper actually changed the file')
    outdir = os.path.join(WT, 'fold22', 'output')
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)  # remove any output copied in from earlier pristine runs
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/root'),
           'FOLD22_W': WT}
    p = subprocess.run([sys.executable, os.path.join(PUB, 'scripts', 'fold_win8_root840500.py')],
                       capture_output=True, text=True, env=env, cwd=SCRATCH, timeout=600)
    need(p.returncode != 0, label + ' non-zero returncode on tampered input')
    need(expect_msg in (p.stdout + p.stderr), label + ' fail message contains: ' + expect_msg)
    need(not os.path.exists(outdir), label + ' no output written (fail-closed before receipt write)')
    need(not os.path.isdir(WT + '-rerun-root-f21'), label + ' rerun scratch tree cleaned up')
    shutil.rmtree(WT)

tamper_run('t1-worklist-xor1099', 'inputs/worklist.csv', 1099, 'input blob mismatch')
tamper_run('t2-cert-xor21212', CERT_REL, 21212, 'input sha256 mismatch')
need(blob_sha1(os.path.join(W, 'inputs/worklist.csv')) == M_PINS['inputs/worklist.csv'], 'worklist untouched after t1 (copytree isolation)')
need(h(os.path.join(W, CERT_REL)) == K1125_CERT_SHA, 'certificate untouched after t2 restore (copytree isolation)')
shutil.rmtree(SCRATCH, ignore_errors=True)

# ===================== E: guards and audit output =====================
section('e')
GUARDS = [
    'This record verifies bookkeeping and byte reproducibility of the published fold22 receipt only.',
    'No game value is claimed: the 6 closed S6 rows are a frontier bookkeeping closure, not LOSS verdicts.',
    'WIN8-D10 is a first-player win certificate from the eight-stone root within depth 10; REFUTED-D10 is not a LOSS proof.',
    'Node counts, solved counts and coverage counts are not win/loss readings.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
]
AUDIT = {
    'schema': 'n11-fold22-external-second-verification-audit-20261120-v1',
    'date': '2026-11-20',
    'verifier': 'verify_fold22_external_20261120.py (independent third implementation; shares no code with the fold22/fold21 machines)',
    'subject': {
        'fold': 'fold22 (K1132)',
        'root_hex': ROOT_HEX,
        'root_verdict': 'WIN8-D10',
        'published_receipt_sha256': PUB_RECEIPT_SHA,
        'published_machine_sha256': PUB_MACHINE_SHA,
        'published_builder_sha256': PUB_BUILDER_SHA,
        'published_readme_sha256': PUB_README_SHA,
        'w_root_pin': 'W22 (12 Git blob pins + 43 SHA-256 pins all matched; fold21 machine pin chain subset-verified)',
    },
    'sections': {
        'p_published_bytes': None,
        'i_w_input_pins': None,
        'c_independent_rederivation': None,
        'x_pristine_reruns': None,
        't_tamper_fail_closed': None,
    },
    'x_execution_matrix': [
        {'run': 'x1', 'cwd': 'verifier scratch cwd', 'w': 'W22 in place', 'env': 'default', 'outcome': 'receipt byte-identical'},
        {'run': 'x2', 'cwd': 'verifier scratch cwd', 'w': 'W22 in place', 'env': 'default', 'outcome': 'receipt byte-identical'},
        {'run': 'x3', 'cwd': 'fresh isolated cwd', 'w': 'fresh copytree W', 'env': 'isolated HOME', 'outcome': 'receipt byte-identical'},
        {'run': 'x4', 'cwd': 'fresh isolated cwd', 'w': 'fresh copytree W', 'env': 'PYTHONHASHSEED=random, isolated HOME', 'outcome': 'receipt byte-identical'},
    ],
    't_tamper_matrix': [
        {'probe': 't1', 'target': 'inputs/worklist.csv', 'byte_offset': 1099, 'mutation': 'XOR 0x01', 'expected': 'input blob mismatch', 'observed': 'fail-closed, no output write'},
        {'probe': 't2', 'target': CERT_REL, 'byte_offset': 21212, 'mutation': 'XOR 0x01', 'expected': 'input sha256 mismatch', 'observed': 'fail-closed, no output write'},
    ],
    'summary': {
        'frontier_before_rederived': {'unique_remaining_s6': 6136, 'sum_remaining_cost': 486243, 'residual_target_rows': 35},
        'closed_rows_rederived': 6,
        'closed_edge_cost_rederived': 484,
        'target_rows_published_claim': len(CLAIM),
        'extra_rows_not_in_target': len(extra_rows),
        'parent_deltas_rederived': pdeltas,
        'frontier_after_rederived': fa_after,
        'five_parent_target_after': {'closed_target_rows_total': 80, 'residual_target_rows': 32},
        'win16_candidates_retired_by_fold22': 1,
        'win16_candidates_remaining': len(remaining_roots),
        'win16_claimed_rows_remaining': len(remaining_rows),
        'k1125_gates_reverified': 19,
        'k1097_footprint_roots_reverified': 16,
        'chain_folds_recomputed_fold4_through_fold21': 18,
    },
    'interpretation_guard': GUARDS,
    'all_gates_pass': True,
    'gate_count': None,
    'gates': GATES,
}
sec_counts = {}
for g in GATES:
    sec_counts[g['section']] = sec_counts.get(g['section'], 0) + 1
AUDIT['sections'] = {
    'p_published_bytes': sec_counts.get('p', 0),
    'i_w_input_pins': sec_counts.get('i', 0),
    'c_independent_rederivation': sec_counts.get('c', 0),
    'x_pristine_reruns': sec_counts.get('x', 0),
    't_tamper_fail_closed': sec_counts.get('t', 0),
}
AUDIT['gate_count'] = len(GATES)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w') as f:
    json.dump(AUDIT, f, sort_keys=True, indent=1)
    f.write('\n')
print('ALL %d GATES PASS; audit written to %s' % (len(GATES), OUT))
print('11x11 empty board/two-stone roots: UNKNOWN (no verdict asserted by this verification)')
