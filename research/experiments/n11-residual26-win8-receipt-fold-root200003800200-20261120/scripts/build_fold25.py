#!/usr/bin/env python3
"""Build fold25 from the published fold24 machine with asserted substitutions.
The generated machine chains fold24, reruns the fold24 machine pristine in an
isolated W, rechecks K1137's 19-gate certificate audit and applies its two
claimed target rows plus the fail-closed extra open row recorded by geometry.
"""
import ast, hashlib, os, re, sys, py_compile

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/f25/W25')
SRC = f'{W}/fold_win8_root438000000818.py'
DST = f'{W}/fold_win8_root200003800200.py'
PIN_PUB = 'f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8'
PIN_F24_RECORD = 'c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7'
PIN_K1137_AUDIT = 'dafa177bf74fd528c34e9a858a83345df4cf8138c17f33ca0102c28840f28c04'
PIN_K1137_CERT = '7bd64a47bed13c25fe069b0b3563c06081639cd3d2ad09b28a1e6c65a41fa61d'
PIN_K1086_SWEEP = '3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced'
PIN_F23_RECORD = '04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59'
PIN_RUNNER_V17 = 'c132cc6425eee3feaeef1d697dd74f968cfedb59'
ROOT = '00000000000200003800200008180000'
CERT = 'k1137/certs/win8-root-00000000000200003800200008180000-20261120.n11'
EXTRA_ROW = '0000000000000080120a000000008000'

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    raise SystemExit('BUILD FAILED: pristine fold24 machine SHA-256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        raise SystemExit('BUILD FAILED: anchor count %d != %d for %r' % (c, n, old[:100]))
    text = text.replace(old, new)

# Header: retain the complete provenance map and explicit interpretation limits.
hdr_first = '# Receipt fold24 (thirty-first receipt) of the WIN8-D10 certificate of root'
hdr_last = '# Usage: python3 fold_win8_root438000000818.py (env FOLD24_W overrides W)'
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    raise SystemExit('BUILD FAILED: header anchors')
i = text.index(hdr_first); j = text.index(hdr_last) + len(hdr_last)
NEW_HDR = '''# Receipt fold25 (thirty-second receipt) of the WIN8-D10 certificate of root
# 00000000000200003800200008180000 (K1137: 19-gate independent audit; certificate
# SHA-256 7bd64a47..., 19,525 strategy rows / 706,180 bytes; 42-mobility root;
# K1086 uncapped probes 261,294/288,448 and K1097 intrinsic footprint claims
# the two target rows open in the published fold24 residual-26 frontier).
# This machine chains the published fold24 record (SHA-256 c4ab76d3...) and
# re-runs the published fold24 machine pristine in an isolated W copy. The fold24
# run transitively re-runs fold23, fold22, fold21, fold20 and fold19; fold19 checks
# the marker-reversible preverified fold18 copy. Upstream fold10..fold23 are also
# recomputed from SHA-pinned records and the full frontier chain.
#
# The WIN8 receipt coverage is independently rederived by two methods:
# 8 D4 images x C(8,2) removals and C(8,6)=28 six-stone subsets. The resulting
# open rows are checked against K1137's two claimed rows and K1097's footprint.
# The C(8,6) subgeometry additionally contains one open row outside the
# five-parent target; it is closed by the coverage convention and recorded in
# extra_s6_rows_not_in_target (fail-closed). The target bookkeeping advances
# by the two claimed rows only.
# The receipt is a bookkeeping fold only; WIN8-D10 proves only this eight-stone
# root's depth-10 game tree. REFUTED-D10 is not a LOSS proof.
# Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
# and classes 1/2/4 remain UNKNOWN.
#
# W-relative additions -> published repo paths:
#   fold24/output/win8-root438000000818-receipt-fold-20261120.json
#     research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/output/win8-root438000000818-receipt-fold-20261120.json
#   fold_win8_root438000000818.py (published fold24 machine; SHA-256 pinned)
#     research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/fold_win8_root438000000818.py
#   k1137/output/win8-cert-extract-verification-20261120.json and k1137/certs/*
#     research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/
#   k1086/output/addtwo-greedy23-d10-sweep-20261120.json
#     research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/
#   k1137/runner_v17.ts
#     research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/runner_v17.ts
# (the fold24 pristine rerun additionally consumes k1091/output/* and
#  k1136/runner_v17.ts pinned inside the fold24 machine)
#
# Usage: python3 fold_win8_root200003800200.py (env FOLD25_W overrides W)'''
text = text[:i] + NEW_HDR + text[j:]

# Scalar constants.
rep("PIN_F23_MACHINE_SHA256 = 'c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e'\n"
    "PIN_K1091_SWEEP = 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25'\n"
    "PIN_RUNNER_V17 = 'c132cc6425eee3feaeef1d697dd74f968cfedb59'\n"
    "PIN_K1136_CERT = 'dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004'\n"
    "PIN_K1136_AUDIT = 'd065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c'",
    "PIN_F24_MACHINE_SHA256 = '" + PIN_PUB + "'\n"
    "PIN_K1086_SWEEP = '" + PIN_K1086_SWEEP + "'\n"
    "PIN_RUNNER_V17 = '" + PIN_RUNNER_V17 + "'\n"
    "PIN_K1137_CERT = '" + PIN_K1137_CERT + "'\n"
    "PIN_K1137_AUDIT = '" + PIN_K1137_AUDIT + "'")
rep("W = os.environ.get('FOLD24_W', '/home/user/work/W24')",
    "W = os.environ.get('FOLD25_W', '/home/user/work/W25')")
rep("OUT = 'fold24/output/win8-root438000000818-receipt-fold-20261120.json'",
    "OUT = 'fold25/output/win8-root200003800200-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000043800000008180010'", "ROOT_HEX = '" + ROOT + "'")
rep("CERT_RELPATH = 'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11'",
    "CERT_RELPATH = '" + CERT + "'")

# Replace fold24's own K1136 pins (unreferenced by fold25) with the four fold25 pins:
# fold24 record, K1137 audit, K1137 cert, K1086 sweep.
rep(" 'k1136/output/win8-cert-extract-verification-20261120.json': 'd065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c',\n"
    " 'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11': 'dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004',\n}",
    " 'fold24/output/win8-root438000000818-receipt-fold-20261120.json': '" + PIN_F24_RECORD + "',\n"
    " 'k1137/output/win8-cert-extract-verification-20261120.json': '" + PIN_K1137_AUDIT + "',\n"
    " 'k1137/certs/win8-root-00000000000200003800200008180000-20261120.n11': '" + PIN_K1137_CERT + "',\n"
    " 'k1086/output/addtwo-greedy23-d10-sweep-20261120.json': '" + PIN_K1086_SWEEP + "',\n}")

# Replace the predecessor rerun section with fold24 record chaining + pristine rerun.
rg_first = '# ---------- fold23 machine rerun (published machine pristine; single rerun gate) ----------'
rg_last = '# (rerun gate of the fold17 machine removed: adopted single-predecessor rerun design; fold17 record remains SHA-pinned and its chain step recomputed below)'
if text.count(rg_first) != 1 or text.count(rg_last) != 1:
    raise SystemExit('BUILD FAILED: predecessor rerun anchors')
i = text.index(rg_first); j = text.index(rg_last)
NEW_CHAIN_RERUN = '''# ---------- fold24 (thirty-first, WIN8 root 438000000818) record chaining ----------
f24 = load('fold24/output/win8-root438000000818-receipt-fold-20261120.json')
need(sha256_of('fold24/output/win8-root438000000818-receipt-fold-20261120.json') == PIN256['fold24/output/win8-root438000000818-receipt-fold-20261120.json'], 'fold24 record sha256')
need(f24['schema'] == 'n11-five-parent-win8-root438000000818-receipt-fold-20261120-v1', 'fold24 schema')
need(f24['status'] == 'fold-complete', 'fold24 fold-complete')
need(f24['receipt_count'] == 1 and len(f24['receipts']) == 1, 'fold24 receipt count')
rc24 = f24['receipts'][0]
fold24Rows = list(rc24['covered_s6_rows'])
need(len(fold24Rows) == len(set(fold24Rows)) == 3, 'fold24 covered rows unique 3')
for h in fold24Rows:
    need(h in open29, 'fold24 row not open: ' + h)
open26 = {h: v for h, v in open29.items() if h not in set(fold24Rows)}
fa24 = f24['frontier_after']
need(len(open26) == 6123 and sum(v[0] for v in open26.values()) == 485213, 'post-fold24 frontier (must match published 6123/485213)')
need(fa24['unique_remaining_s6'] == 6123 and fa24['sum_remaining_cost'] == 485213
     and fa24['solved_s6_in_manifest'] == 1725 and fa24['parent_row_incidence'] == 11660
     and fa24['s6_needed_by_open_classes'] == 4431 and fa24['cost_needed_by_open_classes'] == 351661, 'fold24 frontier_after published values')
for rec_row in f24['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold24 recorded cost matches worklist')
    need(rec_row['row_hex'] in fold24Rows, 'fold24 coverage row among covered')
need(len(f24['new_receipt_coverage']['rows']) == 3, 'fold24 coverage rows count 3')
need(rc24['closed_edge_cost'] == sum(wl[h][0] for h in fold24Rows), 'fold24 closed edge cost recomputed')
for h in fold24Rows:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11660 == fa24['parent_row_incidence'], 'post-fold24 incidence 11660, got %d' % sum(inc.values()))
targetRows24 = list(rc24['covered_five_parent_target_rows'])
need(set(targetRows24) <= residualSet29 and len(targetRows24) == 3, 'fold24 target rows subset of residual29; exactly 3')
extra24 = [h for h in fold24Rows if h not in residualSet29]
need(extra24 == rc24['extra_s6_rows_not_in_target'], 'fold24 extra rows recorded')
need(f24['receipt_ordinal'] == 'thirty-first (fold24, fourteenth WIN8 receipt fold)', 'fold24 ordinal')
residual26 = f24['five_parent_target_after']['residual_row_hex_after']
need(len(residual26) == 26 and len(set(residual26)) == 26 and residual26 == sorted(residual26), 'residual 26 sorted unique')
need(sorted(residualSet29 - set(targetRows24)) == residual26, 'residual26 == residual29 minus fold24 target rows')
need(f24['five_parent_target_after']['closed_target_rows_total'] == 86, 'fold24 closed target 86')
residualSet26 = set(residual26)
need(all(h in open26 for h in residual26), 'residual26 rows open in frontier')
print('post-fold24 frontier verified: 6123/485213, solved_s6 1725, incidence 11660, residual 26')

# ---------- fold24 machine rerun (published machine pristine; single rerun gate) ----------
# The published fold24 machine is executed PRISTINE in an isolated W copy. Its
# default run rechecks fold23 and the fold22/21/20/19 chain transitively. The result
# must be byte-identical to the published fold24 record.
if not PREVERIFIED:
    import shutil, subprocess
    _pub24 = open(f'{W}/fold_win8_root438000000818.py', 'rb').read()
    need(hashlib.sha256(_pub24).hexdigest() == PIN_F24_MACHINE_SHA256, 'published fold24 machine sha256 pin')
    W24X = W + '-rerun-root-f24'
    if os.path.isdir(W24X): shutil.rmtree(W24X)
    shutil.copytree(W, W24X)
    _env24 = dict(os.environ); _env24['FOLD24_W'] = W24X
    _env24.pop('FOLD_PREVERIFIED_CHAIN', None)
    _rr24 = subprocess.run([sys.executable, W24X + '/fold_win8_root438000000818.py'], env=_env24, capture_output=True, text=True)
    need(_rr24.returncode == 0, 'fold24 machine pristine rerun failed: ' + _rr24.stderr[-800:])
    _rerun24_sha = hashlib.sha256(open(W24X + '/fold24/output/win8-root438000000818-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun24_sha == PIN256['fold24/output/win8-root438000000818-receipt-fold-20261120.json'], 'fold24 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W24X)
    print('fold24 machine pristine rerun verified: stdout ends ' + _rr24.stdout.strip().splitlines()[-1][:100])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold24 machine rerun gate skipped; upstream via SHA pins + chain recomputation')

'''
text = text[:i] + NEW_CHAIN_RERUN + text[j:]

# Replace the K1136 certificate record + geometry section with the K1137 one.
gs_first = '# ---------- k1136 certificate record (19 gates) ----------'
gs_last = '# ---------- K1097 refsolve claim crosscheck ----------'
if text.count(gs_first) != 1 or text.count(gs_last) != 1:
    raise SystemExit('BUILD FAILED: k1136 gates anchors')
i = text.index(gs_first); j = text.index(gs_last)
NEW_GATES = '''# ---------- k1137 certificate record (19 gates) ----------
k1137 = load('k1137/output/win8-cert-extract-verification-20261120.json')
need(k1137['schema'] == 'win8-cert-extract-verification-v1', 'k1137 schema')
need(k1137['all_gates_pass'] is True and k1137['gate_count'] == 19 and len(k1137['gates']) == 19, 'k1137 gate count')
need(all(g['passed'] for g in k1137['gates']), 'k1137 every gate passed')
need(k1137['root'] == ROOT_HEX, 'k1137 root hex')

def gate_of(record, name):
    found = [g for g in record['gates'] if g['gate'] == name]
    need(len(found) == 1, 'missing/duplicate gate ' + name)
    return found[0]

gate01 = gate_of(k1137, 'g01_k1086_master_sha256_pin')
need(gate01['detail'] == PIN_K1086_SWEEP, 'k1137 g01 K1086 sweep sha pin')
need(sha256_of('k1086/output/addtwo-greedy23-d10-sweep-20261120.json') == gate01['detail'], 'K1086 sweep record bytes match g01')
gate02 = gate_of(k1137, 'g02_runner_v17_blob_pin_recorded')
gate03 = gate_of(k1137, 'g03_runner_v17_copy_git_blob')
need(gate02['detail'] == PIN_RUNNER_V17 and gate03['detail'] == PIN_RUNNER_V17, 'k1137 runner v17 blob pin')
need(blob_sha(f'{W}/k1137/runner_v17.ts') == PIN_RUNNER_V17, 'K1137 runner v17 bytes match git blob')
need(gate_of(k1137, 'g04_root_shape_safe')['detail'] == {'quadruple_free': True, 'stones': 8}, 'k1137 root shape')
gate05 = gate_of(k1137, 'g05_root_mobility_42')
need(gate05['detail'] == 42 and gate05['passed'] is True, 'k1137 mobility 42')
gate06 = gate_of(k1137, 'g06_k1086_root_probes_win_uncapped')
need(gate06['detail'] == {
    'andclose0': {'capped': False, 'loss': True, 'nodes': 288448, 'terminalStoneRange': [14, 18]},
    'andclose1': {'capped': False, 'loss': True, 'nodes': 261294, 'terminalStoneRange': [14, 18]},
}, 'k1137 uncapped K1086 probes 261294/288448')
gate07 = gate_of(k1137, 'g07_k1086_root_claimed_coverage_2rows')
CLAIM = sorted(gate07['detail'])
need(len(CLAIM) == 2 and CLAIM == sorted(k1137['recorded']['k1086_claimed_coverage_rows']), 'k1137 claim rows are 2 and consistent')
gate08 = gate_of(k1137, 'g08_probe_reproduction_matches_k1086')
need(gate08['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1137 probe reproduction detail')
need(gate_of(k1137, 'g09_root_move_list_equals_rederivation')['detail'] == {'file': 42, 'rederived': 42}, 'k1137 move list')
need(gate_of(k1137, 'g10_extraction_runs_a1_a2_clean')['detail'] == {'a1_moves': 42, 'a2_moves': 42}, 'k1137 A1/A2 runs')
need(gate_of(k1137, 'g11_a1_a2_per_move_node_exact_repeat')['detail'] == {'identical_moves': 42}, 'k1137 A1/A2 repeat')
need(gate_of(k1137, 'g12_extraction_run_b_single_process_clean')['detail'] == {'b_moves': 42}, 'k1137 B run')
need(gate_of(k1137, 'g13_node_accounting_chunk_vs_single')['detail'] == {'a1_chunk_total_nodes': 1399389, 'b_single_process_nodes': 1057553}, 'k1137 extraction node accounting')
gate14 = gate_of(k1137, 'g14_certificate_format_sorted_unique')
need(gate14['detail'] == {'bytes': 706180, 'rows': 19525, 'sha256': PIN_K1137_CERT}, 'k1137 certificate format gate')
need(gate_of(k1137, 'g15_run_b_rowcount_matches_certificate')['detail'] == {'b_nRows': 19525, 'cert': 19525}, 'k1137 B row count')
gate16 = gate_of(k1137, 'g16_third_method_traversal_pass')
need(gate16['detail'] == {'extra': 0, 'failure': None, 'loser_reply_edges': 39665, 'loser_states': 8556, 'missing': 0,
    'subroot_mobility': 42, 'terminal_count': 6923, 'terminal_range': [14, 18], 'visited_states': 43649, 'winner_states': 28170}, 'k1137 third-method traversal')
need(gate_of(k1137, 'g17_three_method_aggregate_agreement')['detail'] == {'bareiss_subroots': 42, 'bigint_terminal_count': 6923, 'third_method_terminal_count': 6923}, 'k1137 three-method agreement')
need(gate_of(k1137, 'g18_interpretation_guard_present')['detail'] == '5 guard lines', 'k1137 interpretation guard')
gate19 = gate_of(k1137, 'g19_k1097_footprint_and_fold23_residual_open')
need(sorted(gate19['detail']['claimed']) == CLAIM, 'k1137 g19 claimed rows == claim')
need(sorted(gate19['detail']['residual_open_rows']) == CLAIM, 'k1137 g19 residual open rows == claim (fold23 residual-29 era)')
need(gate19['detail']['fold23_sha256'] == PIN256['fold23/output/win8-root208090020004-receipt-fold-20261120.json'], 'k1137 g19 fold23 pin')
need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1137 g19 K1097 pin')
cert_recd = k1137['recorded']['certificate']
cert_bytes = open(f'{W}/{CERT_RELPATH}', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1137 cert sha256')
need(cert_recd['bytes'] == len(cert_bytes) == 706180, 'k1137 cert bytes')
need(cert_recd['rows'] == 19525, 'k1137 cert rows')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1137 cert header')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1137 cert root line')
need(len(cert_lines) - 2 == 19525, 'k1137 cert row count')
data_rows = cert_lines[2:]
need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1137 cert row format')
need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1137 cert rows sorted unique')
tm = k1137['recorded']['third_method']
need(tm['root_first_moves'] == 42 and tm['terminal_count'] == 6923 and tm['terminal_range'] == [14, 18]
     and tm['visited_states'] == 43649 and tm['winner_states'] == 28170 and tm['loser_states'] == 8556
     and tm['loser_reply_edges'] == 39665, 'k1137 third-method aggregate')

# ---------- k1137 geometry independent rederivation ----------
mask = int(ROOT_HEX, 16)
need(popcount(mask) == 8, 'root 8 stones')
need(unsafe_quadruples(mask) == 0, 'root safe')
need(canon_int(mask) == mask, 'root D4 canonical')
lmv = legal_moves_of(mask)
need(len(lmv) == 42, 'root legal move count rederivation 42')
print('k1137 certificate record verified: 19/19 gates, sha, header, geometry, mobility 42')

'''
text = text[:i] + NEW_GATES + text[j:]

# K1097 refsolve crosscheck: claimed rows must now be inside the fold24 residual 26.
rep("need(all(h in residualSet29 for h in CLAIM), 'claim rows inside residual29')",
    "need(all(h in residualSet26 for h in CLAIM), 'claim rows inside residual26')")

# Receipt geometry / fold applications.
rep("closedHistorical |= set(fold23Rows)",
    "closedHistorical |= set(fold23Rows)\nclosedHistorical |= set(fold24Rows)")
rep("    if h in open29: row_class[h] = 'open-frontier'",
    "    if h in open26: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open29)",
    "rootRows = sorted(h for h in rootA if h in open26)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet29)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet26)")
rep("extra_rows = [h for h in rootRows if h not in residualSet29]",
    "extra_rows = [h for h in rootRows if h not in residualSet26]")
rep("    del open29[h]", "    del open26[h]")
rep("closedCost = sum(open29[h][0] for h in rootRows)",
    "closedCost = sum(open26[h][0] for h in rootRows)")
rep("needed_rows = [h for h in open29 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open26 if demand(h)['c1'] == 0]")
rep("  'unique_remaining_s6': len(open29),", "  'unique_remaining_s6': len(open26),")
rep("  'sum_remaining_cost': sum(v[0] for v in open29.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open26.values()),")
rep("  'cost_needed_by_open_classes': sum(open29[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open26[h][0] for h in needed_rows),")
rep("'solved_s6_in_manifest': 1722 + len(rootRows),",
    "'solved_s6_in_manifest': 1725 + len(rootRows),")
rep("need(len(rootRows) == 3 and targetRows_new == CLAIM and extra_rows == [], 'K1136 closes exactly its three claimed open rows')",
    "need(len(rootRows) == 3 and targetRows_new == CLAIM and extra_rows == ['" + EXTRA_ROW + "'], 'K1137 closes its two claimed target rows plus one intrinsic extra open row')")
rep("need(closedCost == 225, 'K1136 closed edge cost 225')",
    "need(closedCost == 216, 'K1137 closed edge cost 216')")
rep("need(sum(deltas.values()) == 6 and len(deltas) == 4 and sum(inc.values()) == 11660, 'K1136 parent incidence decrement 6 across 4 parents')",
    "need(sum(deltas.values()) == 6 and len(deltas) == 4 and sum(inc.values()) == 11654, 'K1137 parent incidence decrement 6 across 4 parents')")
rep("need(frontier_after == {'solved_s6_in_manifest': 1725, 'remaining_s5_orbits': 173, 'unique_remaining_s6': 6123, 'sum_remaining_cost': 485213, 's6_needed_by_open_classes': 4431, 'cost_needed_by_open_classes': 351661, 'parent_row_incidence': 11660}, 'fold24 frontier_after exact values')",
    "need(frontier_after == {'solved_s6_in_manifest': 1728, 'remaining_s5_orbits': 173, 'unique_remaining_s6': 6120, 'sum_remaining_cost': 484997, 's6_needed_by_open_classes': 4428, 'cost_needed_by_open_classes': 351445, 'parent_row_incidence': 11654}, 'fold25 frontier_after exact values')")
rep("closedAllNew = 83 + len(newTargetAll)", "closedAllNew = 86 + len(newTargetAll)")
rep("need(len(residualAfter) == 29 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 26 - len(targetRows_new), 'residual accounting')")
rep("need(closedAllNew == 86 and len(residualAfter) == 26, 'fold24 target accounting 86 closed / 26 residual')",
    "need(closedAllNew == 88 and len(residualAfter) == 24, 'fold25 target accounting 88 closed / 24 residual')")
rep("residualAfter = sorted(residualSet29 - newTargetAll)", "residualAfter = sorted(residualSet26 - newTargetAll)")

# Result dict.
rep("'schema': 'n11-five-parent-win8-root438000000818-receipt-fold-20261120-v1',",
    "'schema': 'n11-five-parent-win8-root200003800200-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'thirty-first (fold24, fourteenth WIN8 receipt fold)'",
    "'receipt_ordinal': 'thirty-second (fold25, fifteenth WIN8 receipt fold)'")
rep("'single_owner_note': 'research/log/2026-11-20-n11-fold24-win8-root438000000818-single-owner-note.md'",
    "'single_owner_note': 'research/log/2026-11-20-n11-fold25-win8-root00000000000200003800200008180000-single-owner-note.md'")
rep("'previous_fold': {'record': 'research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/output/win8-root208090020004-receipt-fold-20261120.json (sha256 04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59)',\n                    'frontier_after': fa23},",
    "'previous_fold': {'record': 'research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/output/win8-root438000000818-receipt-fold-20261120.json (sha256 " + PIN_F24_RECORD + ")',\n                    'frontier_after': fa24},")
rep("    'record': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120 (K1136: WIN8 root certificate extract + independent 19-gate audit; 50-mobility 3-claim WIN8-D10 candidate on the K1091 replacement15 sweep basis)',",
    "    'record': 'research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120 (K1137: WIN8 root certificate extract + independent 19-gate audit; 42-mobility 2-claim WIN8-D10 candidate on the K1086 addtwo-greedy23 sweep basis)',")
rep("'verification_sha256': PIN256['k1136/output/win8-cert-extract-verification-20261120.json'],",
    "'verification_sha256': PIN256['k1137/output/win8-cert-extract-verification-20261120.json'],")
rep("'certificate_path': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/certs/win8-root-00000000000000043800000008180010-20261120.n11',",
    "'certificate_path': 'research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/certs/win8-root-00000000000200003800200008180000-20261120.n11',")
rep("'sweep_basis': 'research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json (K1091; sha256 edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25; uncapped andclose1/andclose0 probes 882327/1054873)',",
    "'sweep_basis': 'research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json (K1086; sha256 " + PIN_K1086_SWEEP + "; uncapped andclose1/andclose0 probes 261294/288448)',")
rep("'claims_record': 'research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json (K1097; sha256 ' + PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'] + '; win16_intrinsic_footprints: intrinsic == claimed == 3 rows)',",
    "'claims_record': 'research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json (K1097; sha256 ' + PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'] + '; win16_intrinsic_footprints: intrinsic == claimed == 2 rows)',")
rep("'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'thirty-first',",
    "'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'thirty-second',")
rep("'legal_next_moves': 50,", "'legal_next_moves': 42,")
rep("'unique_strategy_rows': 34843,", "'unique_strategy_rows': 19525,")
rep("'source_record': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120',",
    "'source_record': 'research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120',")
rep("'frontier_before': fa23,", "'frontier_before': fa24,")

# win16 candidate plan impact.
old_impact_note = "'note': 'Observation only. The K1086 probe classified 7 WIN8-D10 candidates (claims 4+4+4+3+3+3+2 = 23 rows) inside the K1097 plan (16 candidates, 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (3 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows), fold21 retired root 80880200 (3 claimed rows), fold22 retired root 840500 (3 claimed rows), and fold23 retired root 208090020004 (3 claimed rows); this receipt closes the 3 claimed rows of root 438000000818 (a K1097 footprint WIN8-D10 candidate); the remaining 2 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3-3-3 = 3 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',"
new_impact_note = "'note': 'Observation only. The K1086 probe classified 7 WIN8-D10 candidates (claims 4+4+4+3+3+3+2 = 23 rows) inside the K1097 plan (16 candidates, 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (3 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows), fold21 retired root 80880200 (3 claimed rows), fold22 retired root 840500 (3 claimed rows), fold23 retired root 208090020004 (3 claimed rows), and fold24 retired root 438000000818 (3 claimed rows); this receipt closes the 2 claimed rows of root 00000000000200003800200008180000 (a K1097 footprint WIN8-D10 candidate; its C(8,6) subgeometry additionally contains one open row outside the five-parent target, closed and recorded as extra); the remaining 1 WIN8 candidate keeps 49-4-3-3-4-3-4-3-3-4-3-3-3-3-3-2 = 1 claimed row, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',"
rep(old_impact_note, new_impact_note)
rep("'retired_root_predecessor': '00000000000020809002000480100000',",
    "'retired_root_predecessor': '00000000000000043800000008180010',")
rep("'win16_candidates_remaining': 2,", "'win16_candidates_remaining': 1,")
rep("'win16_claimed_rows_remaining': 3,", "'win16_claimed_rows_remaining': 1,")

# verdict join summary.
old_join = "'join_basis': 'published fold23 chain frontier (single fresh rerun gate: the published fold23 machine executed pristine in an isolated W copy, byte-identical to the published fold23 record; fold22 and fold21/20/19 rerun gates rechecked transitively inside it; fold10..fold22 upstream verified by SHA-256 pins and full frontier recomputation) + K1136 independently audited 19-gate WIN8 certificate (K1091 sweep record pin, uncapped probes 882327/1054873, runner v17 blob pin, independent third traversal) + K1097 refsolve footprint claims',"
new_join = "'join_basis': 'published fold24 chain frontier (single fresh rerun gate: the published fold24 machine executed pristine in an isolated W copy, byte-identical to the published fold24 record; fold23 and fold22/21/20/19 rerun gates rechecked transitively inside it; fold10..fold23 upstream verified by SHA-256 pins and full frontier recomputation) + K1137 independently audited 19-gate WIN8 certificate (K1086 sweep record pin, uncapped probes 261294/288448, runner v17 blob pin, independent third traversal) + K1097 refsolve footprint claims',"
rep(old_join, new_join)
rep("'receipt_root_is': 'certificate-backed WIN8-D10 (K1136: extraction self-check + BigInt 3x3 + Bareiss 4x4 + independent Python third-method; 19-gate audit on the K1091 sweep basis)',",
    "'receipt_root_is': 'certificate-backed WIN8-D10 (K1137: extraction self-check + BigInt 3x3 + Bareiss 4x4 + independent Python third-method; 19-gate audit on the K1086 sweep basis)',")

# controls
rep("os.makedirs(f'{W}/fold24/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold25/output', exist_ok=True)")
rep("'post_fold23_incidence_11666_recomputed': True,",
    "'post_fold23_incidence_11666_recomputed': True,\n    'fold24_record_chained_and_published_values_matched': True,\n    'fold24_frontier_6123_485213_recomputed_from_worklist': True,\n    'post_fold24_incidence_11660_recomputed': True,")
rep("'fold23_record_sha256_pin_verified': True,",
    "'fold23_record_sha256_pin_verified': True,\n    'fold24_record_sha256_pin_verified': True,")
rep("'fold23_machine_pristine_rerun_byte_identical': True,",
    "'fold23_machine_pristine_rerun_byte_identical': True,\n    'fold24_machine_pristine_rerun_byte_identical': True,\n    'fold23_machine_pristine_rerun_rechecked_transitively_inside_fold24_rerun': True,")
rep("'k1136_cert_19_gates_rechecked_and_bytes_verified': True,",
    "'k1136_cert_gates_rechecked_inside_fold24_pristine_rerun': True,\n    'k1137_cert_19_gates_rechecked_and_bytes_verified': True,")
rep("'k1091_sweep_record_sha256_rechecked': True,",
    "'k1086_sweep_record_sha256_rechecked': True,")

# Final anchor assertions.
assert text.count("ROOT_HEX = '" + ROOT + "'") == 1
assert text.count("OUT = 'fold25/output/win8-root200003800200-receipt-fold-20261120.json'") == 1
assert text.count("CERT_RELPATH = '" + CERT + "'") == 1
assert text.count("PIN_F24_MACHINE_SHA256 = '" + PIN_PUB + "'") == 1
assert text.count("# ---------- fold24 (thirty-first, WIN8 root 438000000818) record chaining ----------") == 1
assert text.count("# ---------- fold24 machine rerun (published machine pristine; single rerun gate) ----------") == 1
assert text.count("# ---------- k1137 certificate record (19 gates) ----------") == 1
assert text.count("# ---------- k1137 geometry independent rederivation ----------") == 1
assert text.count("'receipt': 'thirty-second',") == 1
assert text.count("'receipt_ordinal': 'thirty-second (fold25, fifteenth WIN8 receipt fold)'") == 1
assert text.count("extra_rows == ['" + EXTRA_ROW + "']") == 1
m = re.search(r'PIN256 = (\{.*?\n\})', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 51, f'PIN256 count {len(d)}'
m = re.search(r'PINS = (\{.*?\n\})', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 12, f'PINS count {len(d)}'
# stale-constant sweep: no K1136/K1091 runtime check remnants outside their
# legitimate roles (PIN256 chain inputs, controls keys describing the chain).
for stale in ["PIN_F23_MACHINE_SHA256", "PIN_K1091_SWEEP", "PIN_K1136_CERT", "PIN_K1136_AUDIT",
              "k1136 certificate record verified", "dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004'",
              "K1091 sweep record bytes match g01", "k1136/output/win8-cert-extract-verification-20261120.json']",
              "c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e"]:
    if stale in text:
        raise SystemExit('BUILD FAILED: stale text remains: ' + stale)
DST_DIR = os.path.dirname(DST)
if DST_DIR:
    os.makedirs(DST_DIR, exist_ok=True)
with open(DST, 'w') as f:
    f.write(text)
ast.parse(text)
py_compile.compile(DST, doraise=True)
print('BUILD OK:', DST)
print('  machine bytes:', len(text.encode()), '/ PINS:', 12, '/ PIN256:', 51)
print('  anchored substitutions: header, scalars, +4 PIN256, fold24 chain+rerun, k1137 gates+geometry, result, controls')
