#!/usr/bin/env python3
"""Generate the fold19 machine (fold_win8_root1009000.py) from the PUBLISHED fold18
machine (fold_win8_root00901010.py, sha256-pinned below), by an exact, asserted
transformation following the adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign
(research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md):

  1. scalar constant replacement (W root env, output path, root hex, cert relpath),
  2. three new SHA-256 pins appended to PIN256 (fold18 record, K1119 audit, K1119 cert),
  3. PREVERIFIED switch + pristine/patched fold18 machine pins inserted,
  4. the seven inherited recursive rerun gate blocks (fold11..fold17 machines) REMOVED
     (their verification content stays: all upstream records remain SHA-pinned and the
     full frontier chain recomputation blocks are kept unchanged),
  5. a fold18 record chaining block inserted (frontier 6,161/488,094 -> 6,157/487,800,
     solved 1,691, incidence 11,721, residual 48 -> 45),
  6. a single rerun gate inserted: one fresh execution of the preverified fold18 copy
     (isolated W copy, FOLD_PREVERIFIED_CHAIN=1), byte-compared to the published fold18
     record; guarded by PREVERIFIED so fold20 can rerun THIS machine in preverified mode,
  7. the K1120 certificate gate block replaced by the K1119 block (all constants sourced
     from the published K1119 audit record), root geometry 44 legal moves,
  8. receipt application against open45 / residualSet45, frontier_after solved 1,695,
     closedAllNew base 67, win16 candidate accounting 8 -> 7 roots / 22 -> 18 rows,
  9. updated result record literals (schema, ordinals, sources, controls, join summary),
  10. closedHistorical additionally unions the fold11/12/13 and fold18 covered rows so
      that rows closed by earlier WIN8 receipts classify as 'closed-before-this-receipt'
      instead of a false 'worklist-but-not-open' (classification robustness fix).

Every replacement asserts its occurrence count is exactly 1 (or the asserted number)
before applying; the output is py_compiled and grep-checked for stale constants.

Usage: python3 build_fold19.py [W_root]   (default /home/user/work/W19)
Input:  <W>/fold_win8_root00901010.py
Output: <W>/fold_win8_root1009000.py
"""
import hashlib, os, sys, py_compile, ast

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W19')
SRC = f'{W}/fold_win8_root00901010.py'
DST = f'{W}/fold_win8_root1009000.py'
PIN_PUB = 'dcdfbf92d62409cc3a92f9f16f319e1328180622660b39751921b5de72800091'
PATCHED_F18_SHA256 = 'd342f1f883d2e22ecca25903ec14ed24f16c77a0895e3ed022ab8832736e7f9e'

def die(m):
    print('BUILD FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold18 machine sha256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        die('anchor count %d != %d for: %r' % (c, n, old[:90]))
    text = text.replace(old, new)

# ---------- 1. header ----------
hdr_first = '# Receipt fold (fold18, twenty-fifth receipt) of the WIN8-D10 certificate of root'
hdr_last = "# Usage: python3 fold_win8_root00901010.py  (env FOLD18_W overrides the W root)"
i = text.index(hdr_first)
j = text.index(hdr_last) + len(hdr_last)
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    die('header anchors')
NEW_HDR = """# Receipt fold (fold19, twenty-sixth receipt) of the WIN8-D10 certificate of root
# 00000000000000801212000001009000 (K1119: extraction + triple verification, 19-gate
# record sha256 4696ce14...; certificate sha256 b4dd1e06..., 16,262 rows / 587,989
# bytes; the 44-mobility 4-claim WIN8 candidate of the K1091 sweep with uncapped
# probes 192365/229502; extracted and published by the parallel lane) into the five-parent
# S6 frontier chain -- the ninth WIN8 receipt fold, executed under the adopted
# FOLD_PREVERIFIED_CHAIN rerun-gate redesign (adoption note
# research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md): this machine
# re-runs only its immediate predecessor (the published fold18 machine, executed as
# the marker-reversible preverified copy fold_win8_root00901010_preverified.py with
# FOLD_PREVERIFIED_CHAIN=1, verified byte-identical to the published fold18 record
# sha256 18b543c4...), and verifies fold11..fold17 upstream by SHA pins plus the full
# frontier chain recomputation, giving the open set 6,157 rows / 487,800 cost,
# solved S6 1,691, parent incidence 11,721 and the residual-45 five-parent target
# (published fold18 values).  The WIN8 receipt of root 1009000 is then applied:
# the covered S6 rows of the root are rederived geometrically by two independent
# methods -- (A) the fold-chain convention of 8 D4 images with C(8,2) two-stone
# removals (224 operations) and (B) the refsolve coverage_of82 convention of the
# C(8,6)=28 six-stone subsets of the root -- whose canonical row sets must be equal
# (D4-equivariance) and whose intersection with the open frontier is the receipt
# closure.
#
# All chain and certificate inputs are fail-closed SHA-pinned.  Bookkeeping
# only: WIN8-D10 proves only the game tree of the eight-stone root; REFUTED-D10
# is not a LOSS proof; no game value near the empty board is asserted.
# 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map (identical chain inputs as the
# published fold18 machine, plus):
#   fold18/output/win8-root00901010-receipt-fold-20261120.json
#       research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/output/win8-root00901010-receipt-fold-20261120.json
#   fold_win8_root00901010.py (published fold18 machine; sha256-pinned)
#       research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/scripts/fold_win8_root00901010.py
#   fold_win8_root00901010_preverified.py (marker-reversible preverified copy; sha256-pinned)
#       research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root00901010_preverified.py
#   k1119/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/output/win8-cert-extract-verification-20261120.json
#   k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11
#       research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/certs/win8-root-00000000000000801212000001009000-20261120.n11
#
# Usage: python3 fold_win8_root1009000.py  (env FOLD19_W overrides the W root)"""
text = text[:i] + NEW_HDR + text[j:]

# ---------- 2. scalars ----------
rep("W = os.environ.get('FOLD18_W', '/home/user/work/W18')",
    "W = os.environ.get('FOLD19_W', '/home/user/work/W19')")
rep("OUT = 'fold18/output/win8-root00901010-receipt-fold-20261120.json'",
    "OUT = 'fold19/output/win8-root1009000-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000801202000000901010'",
    "ROOT_HEX = '00000000000000801212000001009000'")
rep("CERT_RELPATH = 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11'",
    "CERT_RELPATH = 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11'")

# ---------- 3. PIN256 additions ----------
rep(" 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11': 'd6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1',\n}",
    " 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11': 'd6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1',\n"
    " 'fold18/output/win8-root00901010-receipt-fold-20261120.json': '18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026',\n"
    " 'k1119/output/win8-cert-extract-verification-20261120.json': '4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100',\n"
    " 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11': 'b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c',\n}")

# ---------- 4. PREVERIFIED switch + machine pins after imports ----------
rep("import json, sys, os, hashlib, tarfile, csv\nfrom itertools import combinations\n",
    "import json, sys, os, hashlib, tarfile, csv\nfrom itertools import combinations\n\n"
    "PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'\n"
    "PATCHED_F18_REL = 'fold_win8_root00901010_preverified.py'\n"
    "PIN_F18_MACHINE_SHA256 = 'dcdfbf92d62409cc3a92f9f16f319e1328180622660b39751921b5de72800091'\n"
    "PATCHED_F18_SHA256 = '%s'\n" % PATCHED_F18_SHA256)

# ---------- 5. remove the seven inherited rerun gate blocks ----------
RERUNS = [
    ("# ---------- fold11 machine byte-identical rerun (published scripts source) ----------",
     "print('fold11 machine rerun verified: stdout ends ' + _rr.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold12 machine byte-identical rerun (published scripts source) ----------",
     "print('fold12 machine rerun verified: stdout ends ' + _rr12.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold13 machine byte-identical rerun (published scripts source) ----------",
     "print('fold13 machine rerun verified: stdout ends ' + _rr13.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold14 machine byte-identical rerun (published scripts source) ----------",
     "print('fold14 machine rerun verified: stdout ends ' + _rr14.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold15 machine byte-identical rerun (published scripts source) ----------",
     "print('fold15 machine rerun verified: stdout ends ' + _rr15.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold16 machine byte-identical rerun (published scripts source) ----------",
     "print('fold16 machine rerun verified: stdout ends ' + _rr16.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold17 machine byte-identical rerun (published scripts source) ----------",
     "print('fold17 machine rerun verified: stdout ends ' + _rr17.stdout.strip().splitlines()[-1][:80])"),
]
for header, last in RERUNS:
    if text.count(header) != 1: die('rerun block header count != 1: ' + header)
    if text.count(last) != 1: die('rerun block end count != 1: ' + last)
    i = text.index(header)
    j = text.index(last) + len(last)
    name = header.split()[2]
    text = text[:i] + ('# (rerun gate of the %s machine removed: adopted single-predecessor rerun design; %s record remains SHA-pinned and its chain step recomputed below)' % (name, name)) + text[j:]

# ---------- 6. insert fold18 chaining + fold18 rerun gate after the fold17 chaining print ----------
anchor17 = "print('post-fold17 frontier verified: 6161/488094, solved_s6 1687, incidence 11729, residual 48')"
if text.count(anchor17) != 1: die('fold17 chain print anchor')
INSERT = """

# ---------- fold18 (twenty-fifth, WIN8 root 00901010) record chaining ----------
f18 = load('fold18/output/win8-root00901010-receipt-fold-20261120.json')
need(sha256_of('fold18/output/win8-root00901010-receipt-fold-20261120.json') == PIN256['fold18/output/win8-root00901010-receipt-fold-20261120.json'], 'fold18 record sha256')
need(f18['schema'] == 'n11-five-parent-win8-root00901010-receipt-fold-20261120-v1', 'fold18 schema')
need(f18['status'] == 'fold-complete', 'fold18 fold-complete')
need(f18['receipt_count'] == 1 and len(f18['receipts']) == 1, 'fold18 receipt count')
rc18 = f18['receipts'][0]
rows18 = list(rc18['covered_s6_rows'])
need(len(rows18) == len(set(rows18)) == 4, 'fold18 covered rows unique 4')
for h in rows18:
    need(h in open48, 'fold18 row not open: ' + h)
open45 = {h: v for h, v in open48.items() if h not in set(rows18)}
fa18 = f18['frontier_after']
need(len(open45) == 6157 and sum(v[0] for v in open45.values()) == 487800, 'post-fold18 frontier (must match published 6157/487800)')
need(fa18['unique_remaining_s6'] == 6157 and fa18['sum_remaining_cost'] == 487800
     and fa18['solved_s6_in_manifest'] == 1691 and fa18['parent_row_incidence'] == 11721
     and fa18['s6_needed_by_open_classes'] == 4465 and fa18['cost_needed_by_open_classes'] == 354248, 'fold18 frontier_after published values')
for rec_row in f18['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold18 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows18, 'fold18 coverage row among covered')
need(rc18['closed_edge_cost'] == sum(wl[h][0] for h in rows18), 'fold18 closed edge cost recomputed')
for h in rows18:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11721 == fa18['parent_row_incidence'], 'post-fold18 incidence 11721, got %d' % sum(inc.values()))
targetRows18 = list(rc18['covered_five_parent_target_rows'])
need(set(targetRows18) <= residualSet48 and len(targetRows18) == 3, 'fold18 target rows subset of residual48; exactly 3')
extra18 = [h for h in rows18 if h not in residualSet48]
need(extra18 == rc18['extra_s6_rows_not_in_target'], 'fold18 extra rows recorded')
residual45 = f18['five_parent_target_after']['residual_row_hex_after']
need(len(residual45) == 45 and len(set(residual45)) == 45 and residual45 == sorted(residual45), 'residual 45 sorted unique')
need(sorted(residualSet48 - set(targetRows18)) == residual45, 'residual45 == residual48 minus fold18 target rows')
need(f18['five_parent_target_after']['closed_target_rows_total'] == 67, 'fold18 closed target 67')
residualSet45 = set(residual45)
need(all(h in open45 for h in residual45), 'residual45 rows open in frontier')
print('post-fold18 frontier verified: 6157/487800, solved_s6 1691, incidence 11721, residual 45')

# ---------- fold18 machine rerun (published machine as preverified copy; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold18 machine is executed as the marker-reversible
# preverified copy (PATCHED_F18_REL) with FOLD_PREVERIFIED_CHAIN=1, in an isolated W
# copy; it skips only its seven recursive rerun gates and keeps every input pin, the
# full frontier chain recomputation, the K1120 19-gate block, the K1097 crosscheck and
# the receipt application, so its output must be byte-identical to the published fold18
# record.  When THIS machine is the rerun target of fold20, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    _pub = open(f'{W}/fold_win8_root00901010.py', 'rb').read()
    need(hashlib.sha256(_pub).hexdigest() == PIN_F18_MACHINE_SHA256, 'published fold18 machine sha256 pin')
    _pf = open(f'{W}/{PATCHED_F18_REL}', 'r').read()
    need(hashlib.sha256(_pf.encode()).hexdigest() == PATCHED_F18_SHA256, 'preverified fold18 copy sha256 pin')
    _rev = []
    _ib = False
    _note = "PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'  # FOLD_PREVERIFIED_CHAIN_GUARD NOTE"
    for _l in _pf.split('\\n'):
        if 'FOLD_PREVERIFIED_CHAIN_GUARD' in _l:
            if _l.strip() == 'if not PREVERIFIED:  # FOLD_PREVERIFIED_CHAIN_GUARD BEGIN':
                _ib = True
            elif _l.strip() == '# FOLD_PREVERIFIED_CHAIN_GUARD END':
                _ib = False
            elif _l.strip() != _note:
                need(False, 'unexpected guard marker: ' + _l)
            continue
        if _ib and _l:
            need(_l.startswith('    '), 'guard indent marker')
            _rev.append(_l[4:])
        else:
            _rev.append(_l)
    need(hashlib.sha256('\\n'.join(_rev).encode()).hexdigest() == PIN_F18_MACHINE_SHA256, 'reverse patch of preverified copy != published fold18 machine')
    import shutil, subprocess
    W18X = W + '-rerun-root-f18'
    if os.path.isdir(W18X): shutil.rmtree(W18X)
    shutil.copytree(W, W18X)
    _env18 = dict(os.environ); _env18['FOLD18_W'] = W18X; _env18['FOLD_PREVERIFIED_CHAIN'] = '1'
    _rr18 = subprocess.run([sys.executable, W18X + '/' + PATCHED_F18_REL], env=_env18, capture_output=True, text=True)
    need(_rr18.returncode == 0, 'fold18 machine preverified rerun failed: ' + _rr18.stderr[-600:])
    _rerun18_sha = hashlib.sha256(open(W18X + '/fold18/output/win8-root00901010-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun18_sha == PIN256['fold18/output/win8-root00901010-receipt-fold-20261120.json'], 'fold18 preverified rerun byte mismatch vs published record')
    shutil.rmtree(W18X)
    print('fold18 machine preverified rerun verified: stdout ends ' + _rr18.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold18 machine rerun gate skipped; upstream via SHA pins + chain recomputation')
"""
text = text.replace(anchor17, anchor17 + INSERT)

# ---------- 7. K1120 -> K1119 gate block ----------
rep("# ---------- k1120 certificate record (19 gates) ----------",
    "# ---------- k1119 certificate record (19 gates) ----------")
rep("# ---------- k1120 geometry independent rederivation ----------",
    "# ---------- k1119 geometry independent rederivation ----------")
rep("k1120 = load('k1120/output/win8-cert-extract-verification-20261120.json')",
    "k1119 = load('k1119/output/win8-cert-extract-verification-20261120.json')")
rep("need(k1120['schema'] == 'win8-cert-extract-verification-v1', 'k1120 schema')",
    "need(k1119['schema'] == 'win8-cert-extract-verification-v1', 'k1119 schema')")
rep("need(k1120['all_gates_pass'] is True and k1120['gate_count'] == 19 and len(k1120['gates']) == 19, 'k1120 gate count')",
    "need(k1119['all_gates_pass'] is True and k1119['gate_count'] == 19 and len(k1119['gates']) == 19, 'k1119 gate count')")
rep("need(all(g['passed'] for g in k1120['gates']), 'k1120 every gate passed')",
    "need(all(g['passed'] for g in k1119['gates']), 'k1119 every gate passed')")
rep("need(k1120['root'] == ROOT_HEX, 'k1120 root hex')",
    "need(k1119['root'] == ROOT_HEX, 'k1119 root hex')")
rep("gate01 = [g for g in k1120['gates'] if g['gate'] == 'g01_k1095_master_sha256_pin'][0]",
    "gate01 = [g for g in k1119['gates'] if g['gate'] == 'g01_k1091_master_sha256_pin'][0]")
rep("need(gate01['detail'] == '335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707', 'k1120 k1095 master sha pin')",
    "need(gate01['detail'] == 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25', 'k1119 k1091 master sha pin')")
rep("gate07 = [g for g in k1120['gates'] if g['gate'] == 'g07_k1095_root_claimed_coverage_3rows']",
    "gate07 = [g for g in k1119['gates'] if g['gate'] == 'g07_k1091_root_claimed_coverage_4rows']")
rep("need(len(CLAIM) == 3, 'k1120 claim rows are 3')",
    "need(len(CLAIM) == 4, 'k1119 claim rows are 4')")
rep("need(CLAIM == sorted(k1120['recorded']['k1095_claimed_coverage_rows']), 'k1120 claim rows consistent')",
    "need(CLAIM == sorted(k1119['recorded']['k1091_claimed_coverage_rows']), 'k1119 claim rows consistent')")
rep("gate05 = [g for g in k1120['gates'] if g['gate'] == 'g05_root_mobility_45'][0]",
    "gate05 = [g for g in k1119['gates'] if g['gate'] == 'g05_root_mobility_44'][0]")
rep("need(gate05['detail'] == 45 and gate05['passed'] is True, 'k1120 mobility 45')",
    "need(gate05['detail'] == 44 and gate05['passed'] is True, 'k1119 mobility 44')")
rep("gate08 = [g for g in k1120['gates'] if g['gate'] == 'g08_probe_reproduction_matches_k1095'][0]",
    "gate08 = [g for g in k1119['gates'] if g['gate'] == 'g08_probe_reproduction_matches_k1091'][0]")
rep("'k1120 probe reproduction detail')", "'k1119 probe reproduction detail')")
rep("gate06 = [g for g in k1120['gates'] if g['gate'] == 'g06_k1095_root_probes_win_uncapped'][0]",
    "gate06 = [g for g in k1119['gates'] if g['gate'] == 'g06_k1091_root_probes_win_uncapped'][0]")
rep("need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 198622\n"
    "     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 240848\n"
    "     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],\n"
    "     'k1120 uncapped probes 198622/240848 with terminal range [14,18]')",
    "need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 192365\n"
    "     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 229502\n"
    "     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],\n"
    "     'k1119 uncapped probes 192365/229502 with terminal range [14,18]')")
rep("need(gate13['detail'] == {'a1_chunk_total_nodes': 631539, 'b_single_process_nodes': 524342}, 'k1120 extraction node accounting')",
    "need(gate13['detail'] == {'a1_chunk_total_nodes': 865602, 'b_single_process_nodes': 712106}, 'k1119 extraction node accounting')")
rep("gate13 = [g for g in k1120['gates'] if g['gate'] == 'g13_node_accounting_chunk_vs_single'][0]",
    "gate13 = [g for g in k1119['gates'] if g['gate'] == 'g13_node_accounting_chunk_vs_single'][0]")
rep("'k1120 third-method zero miss/extra')", "'k1119 third-method zero miss/extra')")
rep("gate16 = [g for g in k1120['gates'] if g['gate'] == 'g16_third_method_traversal_pass'][0]",
    "gate16 = [g for g in k1119['gates'] if g['gate'] == 'g16_third_method_traversal_pass'][0]")
rep("gate19 = [g for g in k1120['gates'] if g['gate'] == 'g19_k1097_refsolve_footprint_match'][0]",
    "gate19 = [g for g in k1119['gates'] if g['gate'] == 'g19_k1097_refsolve_footprint_match'][0]")
rep("need(len(gate19['detail']['claimed']) == 3 and sorted(gate19['detail']['claimed']) == CLAIM, 'k1120 g19 footprint claimed == CLAIM (3 rows)')",
    "need(len(gate19['detail']['claimed']) == 4 and sorted(gate19['detail']['claimed']) == CLAIM, 'k1119 g19 footprint claimed == CLAIM (4 rows)')")
rep("need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1120 g19 k1097 sha pin')",
    "need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1119 g19 k1097 sha pin')")
rep("cert_recd = k1120['recorded']['certificate']",
    "cert_recd = k1119['recorded']['certificate']")
rep("need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1120 cert sha256')",
    "need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1119 cert sha256')")
rep("need(cert_recd['bytes'] == len(cert_bytes) == 484892, 'k1120 cert bytes')",
    "need(cert_recd['bytes'] == len(cert_bytes) == 587989, 'k1119 cert bytes')")
rep("need(cert_recd['rows'] == 13422, 'k1120 cert rows')",
    "need(cert_recd['rows'] == 16262, 'k1119 cert rows')")
rep("need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1120 cert header')",
    "need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1119 cert header')")
rep("need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1120 cert root line')",
    "need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1119 cert root line')")
rep("need(len(cert_lines) - 2 == 13422, 'k1120 cert row count')",
    "need(len(cert_lines) - 2 == 16262, 'k1119 cert row count')")
rep("'k1120 cert row format')", "'k1119 cert row format')")
rep("'k1120 cert rows sorted unique')", "'k1119 cert rows sorted unique')")
rep("tm = k1120['recorded']['third_method']",
    "tm = k1119['recorded']['third_method']")
rep("need(tm['root_first_moves'] == 45 and tm['terminal_count'] == 4336 and tm['terminal_range'] == [14, 18]\n"
    "     and tm['visited_states'] == 30999 and tm['winner_states'] == 20028 and tm['loser_states'] == 6635\n"
    "     and tm['loser_reply_edges'] == 28516, 'k1120 third-method aggregate')",
    "need(tm['root_first_moves'] == 44 and tm['terminal_count'] == 5783 and tm['terminal_range'] == [14, 18]\n"
    "     and tm['visited_states'] == 37696 and tm['winner_states'] == 24352 and tm['loser_states'] == 7561\n"
    "     and tm['loser_reply_edges'] == 34261, 'k1119 third-method aggregate')")
rep("need(len(lmv) == 45, 'root legal move count rederivation 45')",
    "need(len(lmv) == 44, 'root legal move count rederivation 44')")
rep("print('k1120 certificate record verified: 19/19 gates, sha, header, geometry, mobility 45')",
    "print('k1119 certificate record verified: 19/19 gates, sha, header, geometry, mobility 44')")

# ---------- 8. K1097 crosscheck / receipt application constant updates ----------
rep("need(all(h in residualSet48 for h in CLAIM), 'claim rows inside residual48')",
    "need(all(h in residualSet45 for h in CLAIM), 'claim rows inside residual45')")
rep("    if h in open48: row_class[h] = 'open-frontier'",
    "    if h in open45: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open48)",
    "rootRows = sorted(h for h in rootA if h in open45)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet48)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet45)")
rep("extra_rows = [h for h in rootRows if h not in residualSet48]",
    "extra_rows = [h for h in rootRows if h not in residualSet45]")
rep("closedCost = sum(open48[h][0] for h in rootRows)",
    "closedCost = sum(open45[h][0] for h in rootRows)")
rep("    del open48[h]", "    del open45[h]")
rep("needed_rows = [h for h in open48 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open45 if demand(h)['c1'] == 0]")
rep("  'solved_s6_in_manifest': 1687 + len(rootRows),",
    "  'solved_s6_in_manifest': 1691 + len(rootRows),")
rep("  'unique_remaining_s6': len(open48),", "  'unique_remaining_s6': len(open45),")
rep("  'sum_remaining_cost': sum(v[0] for v in open48.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open45.values()),")
rep("  'cost_needed_by_open_classes': sum(open48[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open45[h][0] for h in needed_rows),")
rep("closedAllNew = 64 + len(newTargetAll)", "closedAllNew = 67 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet48 - newTargetAll)",
    "residualAfter = sorted(residualSet45 - newTargetAll)")
rep("need(len(residualAfter) == 48 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 45 - len(targetRows_new), 'residual accounting')")

# ---------- 9. classification closedHistorical extension ----------
rep("closedHistorical |= set(rows7) | set(rows8) | set(rows9) | set(rows13_16) | set(rows10)\nclosedHistorical |= set(rows14)",
    "closedHistorical |= set(rows7) | set(rows8) | set(rows9) | set(rows13_16) | set(rows10)\n"
    "closedHistorical |= set(rows11) | set(rows12) | set(rows13)\nclosedHistorical |= set(rows14)")
rep("closedHistorical |= set(rows17)",
    "closedHistorical |= set(rows17)\nclosedHistorical |= set(rows18)")

# ---------- 10. result record literals ----------
rep("  'schema': 'n11-five-parent-win8-root00901010-receipt-fold-20261120-v1',",
    "  'schema': 'n11-five-parent-win8-root1009000-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'twenty-fifth (fold18, eighth WIN8 receipt fold)',",
    "'receipt_ordinal': 'twenty-sixth (fold19, ninth WIN8 receipt fold)',")
rep("  'single_owner_note': 'research/log/2026-11-20-n11-fold18-win8-root00901010-single-owner-note.md',",
    "  'single_owner_note': 'research/log/2026-11-20-n11-fold19-win8-root1009000-single-owner-note.md',")
rep("  'previous_fold': {'record': 'research/experiments/n11-residual51-win8-receipt-fold-root22081000-20261120/output/win8-root22081000-receipt-fold-20261120.json (sha256 1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674)',\n"
    "                    'frontier_after': fa17},",
    "  'previous_fold': {'record': 'research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/output/win8-root00901010-receipt-fold-20261120.json (sha256 18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026)',\n"
    "                    'frontier_after': fa18},")
rep("  'frontier_before': fa17,", "  'frontier_before': fa18,")
rep("    'record': 'research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120 (K1120: WIN8 root certificate extract + triple verification, 19 gates; 45-mobility 3-claim WIN8 candidate of the K1095 sweep with uncapped probes 240848/198622; published by this lane)',",
    "    'record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120 (K1119: WIN8 root certificate extract + triple verification, 19 gates; 44-mobility 4-claim WIN8 candidate of the K1091 sweep with uncapped probes 192365/229502; published by the parallel lane)',")
rep("    'verification_sha256': PIN256['k1120/output/win8-cert-extract-verification-20261120.json'],",
    "    'verification_sha256': PIN256['k1119/output/win8-cert-extract-verification-20261120.json'],")
rep("    'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/certs/win8-root-00000000000000801202000000901010-20261120.n11',",
    "    'certificate_path': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/certs/win8-root-00000000000000801212000001009000-20261120.n11',")
rep("    'k1095_probes_record': 'research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/output/.input-k1095.json (K1095 replace-12 d10 sweep record; sha256 335eca5e...; claimed coverage 3 rows, pinned by K1120 g01/g07)',",
    "    'k1091_probes_record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/output/.input-k1091.json (K1091 alternate-15-roots d10 sweep record; sha256 edd7ac84...; claimed coverage 4 rows, pinned by K1119 g01/g07)',")
# claims_record descriptive string: for root 1009000 the K1097 footprint is
# intrinsic == claimed == 4 rows (machine-verified below); the fold18 source string
# says 3 rows (correct for root 00901010).  Transcription fix before publication.
rep("; win16_intrinsic_footprints: intrinsic == claimed == 3 rows)',",
    "; win16_intrinsic_footprints: intrinsic == claimed == 4 rows)',")
rep("      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'twenty-fifth',",
    "      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'twenty-sixth',")
rep("      'legal_next_moves': 45,", "      'legal_next_moves': 44,")
rep("      'unique_strategy_rows': 13422,", "      'unique_strategy_rows': 16262,")
rep("        'source_record': 'research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120',",
    "        'source_record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120',")

# win_candidate_plan_impact block (span replace)
wc_start = "  'win_candidate_plan_impact': {"
wc_end = "  'verdict_join_summary': {"
i = text.index(wc_start); j = text.index(wc_end)
NEW_WC = """  'win_candidate_plan_impact': {
    'note': 'Observation only. The K1086 probe classified 7 WIN8-D10 candidates (claims 4+4+4+3+3+3+2 = 23 rows) inside the K1097 plan (16 candidates, 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (4 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows) and fold18 retired root 00901010 (3 claimed rows); this receipt closes the 4 claimed rows of root 1009000 (a K1091-sweep WIN candidate inside the same K1097 footprint plan); the remaining 7 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4 = 18 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',
    'retired_win_candidate_root': ROOT_HEX,
    'rows_of_retired_root': CLAIM,
    'retired_root_predecessor': '00000000000000801202000000901010',
    'win16_candidates_remaining': 7,
    'win16_claimed_rows_remaining': 18,
    'residual23_untouched': True,
  },
"""
text = text[:i] + NEW_WC + text[j:]

# verdict_join_summary block (span replace)
vj_end = "  'controls': {"
i = text.index(wc_end); j = text.index(vj_end)
NEW_VJ = """  'verdict_join_summary': {
    'join_basis': 'published fold18 chain frontier (single fresh rerun gate: the published fold18 machine executed as the marker-reversible preverified copy in an isolated W copy with FOLD_PREVERIFIED_CHAIN=1, byte-identical to the published fold18 record; fold11..fold17 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1119 triple-verified WIN8 certificate + K1091 claims and K1097 refsolve coverage footprints',
    'receipt_root_is': 'certificate-backed WIN8-D10 (K1119: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',
  },
"""
text = text[:i] + NEW_VJ + text[j:]

# controls block (span replace)
ct_end = "  'interpretation_guard': ["
i = text.index(vj_end); j = text.index(ct_end)
NEW_CT = """  'controls': {
    'base_frontier_recomputed': True,
    'chain_frontiers_recomputed_each_step': True,
    'fold10_record_chained_and_published_values_matched': True,
    'fold10_frontier_6206_491497_recomputed_from_worklist': True,
    'post_fold10_incidence_11810_recomputed': True,
    'fold11_record_chained_and_published_values_matched': True,
    'fold11_frontier_6201_491110_recomputed_from_worklist': True,
    'post_fold11_incidence_11803_recomputed': True,
    'fold12_record_chained_and_published_values_matched': True,
    'fold12_frontier_6193_490526_recomputed_from_worklist': True,
    'post_fold12_incidence_11790_recomputed': True,
    'fold13_record_chained_and_published_values_matched': True,
    'fold13_frontier_6184_489813_recomputed_from_worklist': True,
    'post_fold13_incidence_11775_recomputed': True,
    'fold14_record_chained_and_published_values_matched': True,
    'fold14_frontier_6179_489440_recomputed_from_worklist': True,
    'post_fold14_incidence_11765_recomputed': True,
    'fold15_record_chained_and_published_values_matched': True,
    'fold15_frontier_6173_488954_recomputed_from_worklist': True,
    'post_fold15_incidence_11753_recomputed': True,
    'fold16_record_chained_and_published_values_matched': True,
    'fold16_frontier_6168_488575_recomputed_from_worklist': True,
    'post_fold16_incidence_11743_recomputed': True,
    'fold17_record_chained_and_published_values_matched': True,
    'fold17_frontier_6161_488094_recomputed_from_worklist': True,
    'post_fold17_incidence_11729_recomputed': True,
    'fold18_record_chained_and_published_values_matched': True,
    'fold18_frontier_6157_487800_recomputed_from_worklist': True,
    'post_fold18_incidence_11721_recomputed': True,
    'fold10_record_sha256_pin_verified': True,
    'fold11_record_sha256_pin_verified': True,
    'fold12_record_sha256_pin_verified': True,
    'fold13_record_sha256_pin_verified': True,
    'fold14_record_sha256_pin_verified': True,
    'fold15_record_sha256_pin_verified': True,
    'fold16_record_sha256_pin_verified': True,
    'fold17_record_sha256_pin_verified': True,
    'fold18_record_sha256_pin_verified': True,
    'rerun_gate_redesign_adopted_single_predecessor_rerun': True,
    'fold11_through_fold17_machine_recursive_reruns_replaced_by_sha_pins_and_chain_recomputation': True,
    'fold18_machine_preverified_rerun_byte_identical': True,
    'preverified_copy_reverse_patch_equals_published_machine': True,
    'all_chain_input_pins_verified_upfront': True,
    'k1119_cert_19_gates_rechecked_and_bytes_verified': True,
    'k1120_cert_gates_rechecked_inside_preverified_fold18_rerun': True,
    'k1097_refsolve_27_gates_rechecked': True,
    'coverage_rederived_from_d4_images_and_subsets_two_methods': True,
    'rederived_target_rows_match_published_claim': True,
    'all_receipt_rows_were_open_before': True,
    'coverage_of_historical_closed_set_empty': True,
    'win16_claim_partition_exactly_once_rechecked': True,
    'legal_move_count_independently_rederived': True,
    'certificates_sha256_verified': True,
  },
"""
text = text[:i] + NEW_CT + text[j:]

rep("os.makedirs(f'{W}/fold18/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold19/output', exist_ok=True)")

# ---------- 11. final hygiene checks ----------
for stale in ["'FOLD11_W'", "'-rerun-root-f12'", "'-rerun-root-f13'", "'-rerun-root-f14'",
              "'-rerun-root-f15'", "'-rerun-root-f16'", "'-rerun-root-f17'",
              "fold_win8_root8003180.py", "fold_win8_root8005021.py", "fold_win8_root9840004.py",
              "fold_win8_root9090022.py", "fold_win8_root120000038.py", "fold_win8_root8890020.py",
              "fold_win8_root22081000.py", "k1095"]:
    if stale in text:
        die('stale constant remains: ' + stale)
import re as _re
allowed_k1120 = {
    " 'k1120/output/win8-cert-extract-verification-20261120.json': 'ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516',",
    " 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11': 'd6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1',",
    "    'k1120_cert_gates_rechecked_inside_preverified_fold18_rerun': True,",
}
for m in _re.findall(r".*k1120.*", text):
    if m not in allowed_k1120:
        die('unexpected k1120 line: ' + m)

open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
print('fold19 machine built:', DST)
print('sha256:', hashlib.sha256(text.encode()).hexdigest())
print('lines:', text.count('\n') + 1)
