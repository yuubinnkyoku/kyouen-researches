#!/usr/bin/env python3
"""Build fold24 from the published fold23 machine with asserted substitutions.
The generated machine chains fold23, reruns fold23 pristine in an isolated W,
rechecks K1136's 19-gate certificate audit and applies its three claimed rows.
"""
import ast, hashlib, os, re, sys, py_compile

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/tmp/kyouen-fold24/W')
SRC = f'{W}/fold_win8_root208090020004.py'
DST = f'{W}/fold_win8_root438000000818.py'
PIN_PUB = 'c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e'
PIN_F23_RECORD = '04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59'
PIN_K1136_AUDIT = 'd065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c'
PIN_K1136_CERT = 'dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004'
PIN_K1091_SWEEP = 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25'
PIN_RUNNER_V17 = 'c132cc6425eee3feaeef1d697dd74f968cfedb59'
ROOT = '00000000000000043800000008180010'
CERT = 'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11'

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    raise SystemExit('BUILD FAILED: pristine fold23 machine SHA-256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        raise SystemExit('BUILD FAILED: anchor count %d != %d for %r' % (c, n, old[:100]))
    text = text.replace(old, new)

# Header: retain the complete provenance map and explicit interpretation limits.
hdr_first = '# Receipt fold (fold23, thirtieth receipt)'
hdr_last = "# Usage: python3 fold_win8_root208090020004.py  (env FOLD23_W overrides the W root)"
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    raise SystemExit('BUILD FAILED: header anchors')
i = text.index(hdr_first); j = text.index(hdr_last) + len(hdr_last)
NEW_HDR = '''# Receipt fold24 (thirty-first receipt) of the WIN8-D10 certificate of root
# 00000000000000043800000008180010 (K1136: 19-gate independent audit; certificate
# SHA-256 dbcb0bae..., 34,843 strategy rows / 1,260,393 bytes; 50-mobility root;
# K1091 uncapped probes 882,327/1,054,873 and K1097 intrinsic footprint claims
# exactly the three rows open in the published fold23 residual-29 frontier).
# This machine chains the published fold23 record (SHA-256 04f334ff...) and
# re-runs the published fold23 machine pristine in an isolated W copy. The fold23
# run transitively re-runs fold22, fold21, fold20 and fold19; fold19 checks the
# marker-reversible preverified fold18 copy. Upstream fold10..fold22 are also
# recomputed from SHA-pinned records and the full frontier chain.
#
# The WIN8 receipt coverage is independently rederived by two methods:
# 8 D4 images x C(8,2) removals and C(8,6)=28 six-stone subsets. The resulting
# open rows are checked against K1136's three claimed rows and K1097's footprint.
# The receipt is a bookkeeping fold only; WIN8-D10 proves only this eight-stone
# root's depth-10 game tree. REFUTED-D10 is not a LOSS proof.
# Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
# and classes 1/2/4 remain UNKNOWN.
#
# W-relative additions -> published repo paths:
#   fold23/output/win8-root208090020004-receipt-fold-20261120.json
#     research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/output/win8-root208090020004-receipt-fold-20261120.json
#   fold_win8_root208090020004.py (published fold23 machine; SHA-256 pinned)
#     research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/scripts/fold_win8_root208090020004.py
#   k1136/output/win8-cert-extract-verification-20261120.json and k1136/certs/*
#     research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/
#   k1091/output/replace15-d10-sweep-20261120.json
#     research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/
#   k1136/runner_v17.ts
#     research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/runner_v17.ts
#
# Usage: python3 fold_win8_root438000000818.py (env FOLD24_W overrides W)'''
text = text[:i] + NEW_HDR + text[j:]

# Scalar constants.
rep("PIN_F22_MACHINE_SHA256 = 'd5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d'",
    "PIN_F23_MACHINE_SHA256 = '" + PIN_PUB + "'\nPIN_K1091_SWEEP = '" + PIN_K1091_SWEEP + "'\nPIN_RUNNER_V17 = '" + PIN_RUNNER_V17 + "'\nPIN_K1136_CERT = '" + PIN_K1136_CERT + "'\nPIN_K1136_AUDIT = '" + PIN_K1136_AUDIT + "'")
rep("W = os.environ.get('FOLD23_W', '/home/user/work/W23')",
    "W = os.environ.get('FOLD24_W', '/home/user/work/W24')")
rep("OUT = 'fold23/output/win8-root208090020004-receipt-fold-20261120.json'",
    "OUT = 'fold24/output/win8-root438000000818-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000020809002000480100000'", "ROOT_HEX = '" + ROOT + "'")
rep("CERT_RELPATH = 'k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11'",
    "CERT_RELPATH = '" + CERT + "'")

# Append exactly three new SHA-256 pins: fold23 record, K1136 audit, K1136 cert.
rep(" 'k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11': 'b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e',\n}",
    " 'k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11': 'b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e',\n"
    " 'fold23/output/win8-root208090020004-receipt-fold-20261120.json': '" + PIN_F23_RECORD + "',\n"
    " 'k1136/output/win8-cert-extract-verification-20261120.json': '" + PIN_K1136_AUDIT + "',\n"
    " 'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11': '" + PIN_K1136_CERT + "',\n}")

# Replace the predecessor rerun section with fold23 record chaining + pristine rerun.
rg_first = '# ---------- fold22 machine rerun (published machine pristine; single rerun gate) ----------'
rg_last = "# (rerun gate of the fold17 machine removed: adopted single-predecessor rerun design; fold17 record remains SHA-pinned and its chain step recomputed below)"
if text.count(rg_first) != 1 or text.count(rg_last) != 1:
    raise SystemExit('BUILD FAILED: predecessor rerun anchors')
i = text.index(rg_first); j = text.index(rg_last)
NEW_CHAIN_RERUN = '''# ---------- fold23 (thirtieth, WIN8 root 208090020004) record chaining ----------
f23 = load('fold23/output/win8-root208090020004-receipt-fold-20261120.json')
need(sha256_of('fold23/output/win8-root208090020004-receipt-fold-20261120.json') == PIN256['fold23/output/win8-root208090020004-receipt-fold-20261120.json'], 'fold23 record sha256')
need(f23['schema'] == 'n11-five-parent-win8-root208090020004-receipt-fold-20261120-v1', 'fold23 schema')
need(f23['status'] == 'fold-complete', 'fold23 fold-complete')
need(f23['receipt_count'] == 1 and len(f23['receipts']) == 1, 'fold23 receipt count')
rc23 = f23['receipts'][0]
fold23Rows = list(rc23['covered_s6_rows'])
need(len(fold23Rows) == len(set(fold23Rows)) == 4, 'fold23 covered rows unique 4')
for h in fold23Rows:
    need(h in open32, 'fold23 row not open: ' + h)
open29 = {h: v for h, v in open32.items() if h not in set(fold23Rows)}
fa23 = f23['frontier_after']
need(len(open29) == 6126 and sum(v[0] for v in open29.values()) == 485438, 'post-fold23 frontier (must match published 6126/485438)')
need(fa23['unique_remaining_s6'] == 6126 and fa23['sum_remaining_cost'] == 485438
     and fa23['solved_s6_in_manifest'] == 1722 and fa23['parent_row_incidence'] == 11666
     and fa23['s6_needed_by_open_classes'] == 4434 and fa23['cost_needed_by_open_classes'] == 351886, 'fold23 frontier_after published values')
for rec_row in f23['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold23 recorded cost matches worklist')
    need(rec_row['row_hex'] in fold23Rows, 'fold23 coverage row among covered')
need(len(f23['new_receipt_coverage']['rows']) == 4, 'fold23 coverage rows count 4')
need(rc23['closed_edge_cost'] == sum(wl[h][0] for h in fold23Rows), 'fold23 closed edge cost recomputed')
for h in fold23Rows:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11666 == fa23['parent_row_incidence'], 'post-fold23 incidence 11666, got %d' % sum(inc.values()))
targetRows23 = list(rc23['covered_five_parent_target_rows'])
need(set(targetRows23) <= residualSet32 and len(targetRows23) == 3, 'fold23 target rows subset of residual32; exactly 3')
extra23 = [h for h in fold23Rows if h not in residualSet32]
need(extra23 == rc23['extra_s6_rows_not_in_target'], 'fold23 extra rows recorded')
need(f23['receipt_ordinal'] == 'thirtieth (fold23, thirteenth WIN8 receipt fold)', 'fold23 ordinal')
residual29 = f23['five_parent_target_after']['residual_row_hex_after']
need(len(residual29) == 29 and len(set(residual29)) == 29 and residual29 == sorted(residual29), 'residual 29 sorted unique')
need(sorted(residualSet32 - set(targetRows23)) == residual29, 'residual29 == residual32 minus fold23 target rows')
need(f23['five_parent_target_after']['closed_target_rows_total'] == 83, 'fold23 closed target 83')
residualSet29 = set(residual29)
need(all(h in open29 for h in residual29), 'residual29 rows open in frontier')
print('post-fold23 frontier verified: 6126/485438, solved_s6 1722, incidence 11666, residual 29')

# ---------- fold23 machine rerun (published machine pristine; single rerun gate) ----------
# The published fold23 machine is executed PRISTINE in an isolated W copy. Its
# default run rechecks fold22 and the fold21/20/19 chain transitively. The result
# must be byte-identical to the published fold23 record.
if not PREVERIFIED:
    import shutil, subprocess
    _pub23 = open(f'{W}/fold_win8_root208090020004.py', 'rb').read()
    need(hashlib.sha256(_pub23).hexdigest() == PIN_F23_MACHINE_SHA256, 'published fold23 machine sha256 pin')
    W23X = W + '-rerun-root-f23'
    if os.path.isdir(W23X): shutil.rmtree(W23X)
    shutil.copytree(W, W23X)
    _env23 = dict(os.environ); _env23['FOLD23_W'] = W23X
    _env23.pop('FOLD_PREVERIFIED_CHAIN', None)
    _rr23 = subprocess.run([sys.executable, W23X + '/fold_win8_root208090020004.py'], env=_env23, capture_output=True, text=True)
    need(_rr23.returncode == 0, 'fold23 machine pristine rerun failed: ' + _rr23.stderr[-800:])
    _rerun23_sha = hashlib.sha256(open(W23X + '/fold23/output/win8-root208090020004-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun23_sha == PIN256['fold23/output/win8-root208090020004-receipt-fold-20261120.json'], 'fold23 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W23X)
    print('fold23 machine pristine rerun verified: stdout ends ' + _rr23.stdout.strip().splitlines()[-1][:100])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold23 machine rerun gate skipped; upstream via SHA pins + chain recomputation')

'''
text = text[:i] + NEW_CHAIN_RERUN + text[j:]

# Replace K1123's fresh-probe gate block with K1136's K1091 sweep-backed gate block.
kb_first = '# ---------- k1123 certificate record (19 gates) ----------'
kb_mid = '# ---------- k1123 geometry independent rederivation ----------'
if text.count(kb_first) != 1 or text.count(kb_mid) != 1:
    raise SystemExit('BUILD FAILED: K1123 block anchors')
i = text.index(kb_first); j = text.index(kb_mid) + len(kb_mid)
NEW_K1136 = '''# ---------- k1136 certificate record (19 gates) ----------
k1136 = load('k1136/output/win8-cert-extract-verification-20261120.json')
need(k1136['schema'] == 'win8-cert-extract-verification-v1', 'k1136 schema')
need(k1136['all_gates_pass'] is True and k1136['gate_count'] == 19 and len(k1136['gates']) == 19, 'k1136 gate count')
need(all(g['passed'] for g in k1136['gates']), 'k1136 every gate passed')
need(k1136['root'] == ROOT_HEX, 'k1136 root hex')

def gate_of(record, name):
    found = [g for g in record['gates'] if g['gate'] == name]
    need(len(found) == 1, 'missing/duplicate gate ' + name)
    return found[0]

gate01 = gate_of(k1136, 'g01_k1091_master_sha256_pin')
need(gate01['detail'] == PIN_K1091_SWEEP, 'k1136 g01 K1091 sweep sha pin')
need(sha256_of('k1091/output/replace15-d10-sweep-20261120.json') == gate01['detail'], 'K1091 sweep record bytes match g01')
gate02 = gate_of(k1136, 'g02_runner_v17_blob_pin_recorded')
gate03 = gate_of(k1136, 'g03_runner_v17_copy_git_blob')
need(gate02['detail'] == PIN_RUNNER_V17 and gate03['detail'] == PIN_RUNNER_V17, 'k1136 runner v17 blob pin')
need(blob_sha(f'{W}/k1136/runner_v17.ts') == PIN_RUNNER_V17, 'K1136 runner v17 bytes match git blob')
need(gate_of(k1136, 'g04_root_shape_safe')['detail'] == {'quadruple_free': True, 'stones': 8}, 'k1136 root shape')
gate05 = gate_of(k1136, 'g05_root_mobility_50')
need(gate05['detail'] == 50 and gate05['passed'] is True, 'k1136 mobility 50')
gate06 = gate_of(k1136, 'g06_k1091_root_probes_win_uncapped')
need(gate06['detail'] == {
    'andclose0': {'capped': False, 'loss': True, 'nodes': 1054873, 'terminalStoneRange': [14, 18]},
    'andclose1': {'capped': False, 'loss': True, 'nodes': 882327, 'terminalStoneRange': [14, 18]},
}, 'k1136 uncapped K1091 probes 882327/1054873')
gate07 = gate_of(k1136, 'g07_k1091_root_claimed_coverage_3rows')
CLAIM = sorted(gate07['detail'])
need(len(CLAIM) == 3 and CLAIM == sorted(k1136['recorded']['k1091_claimed_coverage_rows']), 'k1136 claim rows are 3 and consistent')
gate08 = gate_of(k1136, 'g08_probe_reproduction_matches_k1091')
need(gate08['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1136 probe reproduction detail')
need(gate_of(k1136, 'g09_root_move_list_equals_rederivation')['detail'] == {'file': 50, 'rederived': 50}, 'k1136 move list')
need(gate_of(k1136, 'g10_extraction_runs_a1_a2_clean')['detail'] == {'a1_moves': 50, 'a2_moves': 50}, 'k1136 A1/A2 runs')
need(gate_of(k1136, 'g11_a1_a2_per_move_node_exact_repeat')['detail'] == {'identical_moves': 50}, 'k1136 A1/A2 repeat')
need(gate_of(k1136, 'g12_extraction_run_b_single_process_clean')['detail'] == {'b_moves': 50}, 'k1136 B run')
need(gate_of(k1136, 'g13_node_accounting_chunk_vs_single')['detail'] == {'a1_chunk_total_nodes': 3539166, 'b_single_process_nodes': 2564865}, 'k1136 extraction node accounting')
gate14 = gate_of(k1136, 'g14_certificate_format_sorted_unique')
need(gate14['detail'] == {'bytes': 1260393, 'rows': 34843, 'sha256': PIN_K1136_CERT}, 'k1136 certificate format gate')
need(gate_of(k1136, 'g15_run_b_rowcount_matches_certificate')['detail'] == {'b_nRows': 34843, 'cert': 34843}, 'k1136 B row count')
gate16 = gate_of(k1136, 'g16_third_method_traversal_pass')
need(gate16['detail'] == {'extra': 0, 'failure': None, 'loser_reply_edges': 67581, 'loser_states': 14382, 'missing': 0,
    'subroot_mobility': 50, 'terminal_count': 13173, 'terminal_range': [14, 18], 'visited_states': 77154, 'winner_states': 49599}, 'k1136 third-method traversal')
need(gate_of(k1136, 'g17_three_method_aggregate_agreement')['detail'] == {'bareiss_subroots': 50, 'bigint_terminal_count': 13173, 'third_method_terminal_count': 13173}, 'k1136 three-method agreement')
need(gate_of(k1136, 'g18_interpretation_guard_present')['detail'] == '5 guard lines', 'k1136 interpretation guard')
gate19 = gate_of(k1136, 'g19_k1097_footprint_and_fold23_residual_open')
need(sorted(gate19['detail']['claimed']) == CLAIM and gate19['detail']['claimed_rows_open_in_residual29'] == 3
     and gate19['detail']['residual29_rows'] == 29, 'k1136 g19 claimed rows open in residual29')
need(gate19['detail']['fold23_sha256'] == PIN256['fold23/output/win8-root208090020004-receipt-fold-20261120.json'], 'k1136 g19 fold23 pin')
need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1136 g19 K1097 pin')
cert_recd = k1136['recorded']['certificate']
cert_bytes = open(f'{W}/{CERT_RELPATH}', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1136 cert sha256')
need(cert_recd['bytes'] == len(cert_bytes) == 1260393, 'k1136 cert bytes')
need(cert_recd['rows'] == 34843, 'k1136 cert rows')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1136 cert header')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1136 cert root line')
need(len(cert_lines) - 2 == 34843, 'k1136 cert row count')
data_rows = cert_lines[2:]
need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1136 cert row format')
need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1136 cert rows sorted unique')
tm = k1136['recorded']['third_method']
need(tm['root_first_moves'] == 50 and tm['terminal_count'] == 13173 and tm['terminal_range'] == [14, 18]
     and tm['visited_states'] == 77154 and tm['winner_states'] == 49599 and tm['loser_states'] == 14382
     and tm['loser_reply_edges'] == 67581, 'k1136 third-method aggregate')

# ---------- k1136 geometry independent rederivation ----------
mask = int(ROOT_HEX, 16)
need(popcount(mask) == 8, 'root 8 stones')
need(unsafe_quadruples(mask) == 0, 'root safe')
need(canon_int(mask) == mask, 'root D4 canonical')
lmv = legal_moves_of(mask)
need(len(lmv) == 50, 'root legal move count rederivation 50')
print('k1136 certificate record verified: 19/19 gates, sha, header, geometry, mobility 50')
'''
text = text[:i] + NEW_K1136 + text[j:]
# The new K1136 block already performs the independent root-geometry check;
# remove the old K1123 geometry block that followed the replaced marker.
dup_start = text.index("mask = int(ROOT_HEX, 16)", text.index("print('k1136 certificate record verified"))
dup_end = text.index("# ---------- K1097 refsolve claim crosscheck ----------", dup_start)
text = text[:dup_start] + text[dup_end:]

# K1097 footprint must agree with K1136 and the fold23 residual.
rep("'footprint claimed == K1123 claim (K1097 record)'", "'footprint claimed == K1136 claim (K1097 record)'")
rep("'footprint intrinsic == K1123 claim (K1097 record)'", "'footprint intrinsic == K1136 claim (K1097 record)'")
rep("need(all(h in residualSet32 for h in CLAIM), 'claim rows inside residual32')",
    "need(all(h in residualSet29 for h in CLAIM), 'claim rows inside residual29')")

# Apply K1136 against the fold23-derived open29 / residual29 state.
rep("closedHistorical |= set(rows22)\nrow_class = {}",
    "closedHistorical |= set(rows22)\nclosedHistorical |= set(fold23Rows)\nrow_class = {}")
rep("if h in open32: row_class[h] = 'open-frontier'", "if h in open29: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open32)", "rootRows = sorted(h for h in rootA if h in open29)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet32)", "targetRows_new = sorted(h for h in rootRows if h in residualSet29)")
rep("extra_rows = [h for h in rootRows if h not in residualSet32]", "extra_rows = [h for h in rootRows if h not in residualSet29]")
rep("closedCost = sum(open32[h][0] for h in rootRows)", "closedCost = sum(open29[h][0] for h in rootRows)")
rep("    del open32[h]", "    del open29[h]")
rep("needed_rows = [h for h in open32 if demand(h)['c1'] == 0]", "needed_rows = [h for h in open29 if demand(h)['c1'] == 0]")
rep("'solved_s6_in_manifest': 1718 + len(rootRows)", "'solved_s6_in_manifest': 1722 + len(rootRows)")
rep("'unique_remaining_s6': len(open32)", "'unique_remaining_s6': len(open29)")
rep("'sum_remaining_cost': sum(v[0] for v in open32.values())", "'sum_remaining_cost': sum(v[0] for v in open29.values())")
rep("'cost_needed_by_open_classes': sum(open32[h][0] for h in needed_rows)", "'cost_needed_by_open_classes': sum(open29[h][0] for h in needed_rows)")
rep("closedAllNew = 80 + len(newTargetAll)", "closedAllNew = 83 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet32 - newTargetAll)", "residualAfter = sorted(residualSet29 - newTargetAll)")
rep("need(len(residualAfter) == 32 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 29 - len(targetRows_new), 'residual accounting')\nneed(closedAllNew == 86 and len(residualAfter) == 26, 'fold24 target accounting 86 closed / 26 residual')")

# Fail-closed expected fold24 result; no inferred victory for the frontier rows.
rep("# five-parent target accounting\nnewTargetAll = set(targetRows_new)",
    "need(len(rootRows) == 3 and targetRows_new == CLAIM and extra_rows == [], 'K1136 closes exactly its three claimed open rows')\nneed(closedCost == 225, 'K1136 closed edge cost 225')\nneed(sum(deltas.values()) == 6 and len(deltas) == 4 and sum(inc.values()) == 11660, 'K1136 parent incidence decrement 6 across 4 parents')\nneed(frontier_after == {'solved_s6_in_manifest': 1725, 'remaining_s5_orbits': 173, 'unique_remaining_s6': 6123, 'sum_remaining_cost': 485213, 's6_needed_by_open_classes': 4431, 'cost_needed_by_open_classes': 351661, 'parent_row_incidence': 11660}, 'fold24 frontier_after exact values')\n# five-parent target accounting\nnewTargetAll = set(targetRows_new)")

# Result record: identities, predecessor, source, frontier, and receipt ordinal.
rep("'schema': 'n11-five-parent-win8-root208090020004-receipt-fold-20261120-v1',",
    "'schema': 'n11-five-parent-win8-root438000000818-receipt-fold-20261120-v1',")
rep("'date': '2026-11-20', 'status': 'fold-complete', 'receipt_ordinal': 'thirtieth (fold23, thirteenth WIN8 receipt fold)',",
    "'date': '2026-11-20', 'status': 'fold-complete', 'receipt_ordinal': 'thirty-first (fold24, fourteenth WIN8 receipt fold)',")
rep("'single_owner_note': 'research/log/2026-11-20-n11-fold23-win8-root208090020004-single-owner-note.md',",
    "'single_owner_note': 'research/log/2026-11-20-n11-fold24-win8-root438000000818-single-owner-note.md',")
rep("'previous_fold': {'record': 'research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/output/win8-root840500-receipt-fold-20261120.json (sha256 f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488)',\n                    'frontier_after': fa22},",
    "'previous_fold': {'record': 'research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/output/win8-root208090020004-receipt-fold-20261120.json (sha256 " + PIN_F23_RECORD + ")',\n                    'frontier_after': fa23},")
rep("'record': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120 (K1123: WIN8 root certificate extract + triple verification, 19 gates; 54-mobility 3-claim WIN8-D10 candidate on the fresh-probe basis, fresh probes 350792/442824 matching the published K1119 total 793616)',",
    "'record': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120 (K1136: WIN8 root certificate extract + independent 19-gate audit; 50-mobility 3-claim WIN8-D10 candidate on the K1091 replacement15 sweep basis)',")
rep("'verification_sha256': PIN256['k1123/output/win8-cert-extract-verification-20261120.json'],",
    "'verification_sha256': PIN256['k1136/output/win8-cert-extract-verification-20261120.json'],")
rep("'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/certs/win8-root-00000000000020809002000480100000-20261120.n11',",
    "'certificate_path': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/certs/win8-root-00000000000000043800000008180010-20261120.n11',")
rep("'fresh_probe_basis': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/output/.input-k1119-log.md (published K1119 fresh-probe log; git blob 51bad3fac..., sha256 4d11ca89...; probe total 793616, pinned by K1123 g01/g02/g06/g08)',",
    "'sweep_basis': 'research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json (K1091; sha256 " + PIN_K1091_SWEEP + "; uncapped andclose1/andclose0 probes 882327/1054873)',")
rep("'receipt': 'thirtieth',", "'receipt': 'thirty-first',")
rep("'legal_next_moves': 54,", "'legal_next_moves': 50,")
rep("'unique_strategy_rows': 23621,", "'unique_strategy_rows': 34843,")
rep("'source_record': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120',",
    "'source_record': 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120',")
rep("'frontier_before': fa22,", "'frontier_before': fa23,")

# Candidate plan accounting: K1136 is the next retired root in K1097's exact 16-root partition.
old_note = "Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (4 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows), fold21 retired root 80880200 (3 claimed rows) and fold22 retired root 840500 (3 claimed rows); this receipt closes the 3 claimed rows of root 208090020004 (the last published WIN8-D10 candidate inside the same K1097 footprint win16 plan); the remaining 3 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3-3 = 6 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked."
new_note = "Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (3 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows), fold21 retired root 80880200 (3 claimed rows), fold22 retired root 840500 (3 claimed rows), and fold23 retired root 208090020004 (3 claimed rows); this receipt closes the 3 claimed rows of root 438000000818 (a K1097 footprint WIN8-D10 candidate); the remaining 2 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3-3-3 = 3 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked."
rep(old_note, new_note)
rep("'retired_root_predecessor': '00000000000000801202000000840500',", "'retired_root_predecessor': '00000000000020809002000480100000',")
rep("'win16_candidates_remaining': 3,", "'win16_candidates_remaining': 2,")
rep("'win16_claimed_rows_remaining': 6,", "'win16_claimed_rows_remaining': 3,")

# Join summary and controls.
rep("'join_basis': 'published fold22 chain frontier (single fresh rerun gate: the published fold22 machine executed pristine in an isolated W copy, byte-identical to the published fold22 record; the fold21 machine pristine rerun gate and the K1125 gate block re-run transitively inside it; fold10..fold21 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1123 triple-verified WIN8 certificate on the fresh-probe basis (probes match the published K1119 total 793616) + K1097 refsolve coverage footprints',",
    "'join_basis': 'published fold23 chain frontier (single fresh rerun gate: the published fold23 machine executed pristine in an isolated W copy, byte-identical to the published fold23 record; fold22 and fold21/20/19 rerun gates rechecked transitively inside it; fold10..fold22 upstream verified by SHA-256 pins and full frontier recomputation) + K1136 independently audited 19-gate WIN8 certificate (K1091 sweep record pin, uncapped probes 882327/1054873, runner v17 blob pin, independent third traversal) + K1097 refsolve footprint claims',")
rep("'receipt_root_is': 'certificate-backed WIN8-D10 (K1123: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate fresh-probe record)',",
    "'receipt_root_is': 'certificate-backed WIN8-D10 (K1136: extraction self-check + BigInt 3x3 + Bareiss 4x4 + independent Python third-method; 19-gate audit on the K1091 sweep basis)',")
rep("    'fold22_record_chained_and_published_values_matched': True,\n    'fold22_frontier_6130_485759_recomputed_from_worklist': True,\n    'post_fold22_incidence_11671_recomputed': True,",
    "    'fold22_record_chained_and_published_values_matched': True,\n    'fold22_frontier_6130_485759_recomputed_from_worklist': True,\n    'post_fold22_incidence_11671_recomputed': True,\n    'fold23_record_chained_and_published_values_matched': True,\n    'fold23_frontier_6126_485438_recomputed_from_worklist': True,\n    'post_fold23_incidence_11666_recomputed': True,")
rep("    'fold22_record_sha256_pin_verified': True,",
    "    'fold22_record_sha256_pin_verified': True,\n    'fold23_record_sha256_pin_verified': True,")
rep("    'fold22_machine_pristine_rerun_byte_identical': True,",
    "    'fold22_machine_pristine_rerun_byte_identical': True,\n    'fold23_machine_pristine_rerun_byte_identical': True,")
rep("    'fold21_machine_pristine_rerun_rechecked_transitively_inside_fold22_rerun': True,",
    "    'fold21_machine_pristine_rerun_rechecked_transitively_inside_fold22_rerun': True,\n    'fold22_machine_pristine_rerun_rechecked_transitively_inside_fold23_rerun': True,")
rep("    'k1123_cert_19_gates_rechecked_and_bytes_verified': True,",
    "    'k1123_cert_gates_rechecked_inside_fold23_pristine_rerun': True,\n    'k1136_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1091_sweep_record_sha256_rechecked': True,\n    'runner_v17_blob_pin_rechecked': True,")
rep("os.makedirs(f'{W}/fold23/output', exist_ok=True)", "os.makedirs(f'{W}/fold24/output', exist_ok=True)")

# Static checks before publication.
for stale in [
    "PIN_F22_MACHINE_SHA256", "FOLD23_W', '/home/user/work/W23",
    "ROOT_HEX = '00000000000020809002000480100000'", "fold23/output/win8-root208090020004-receipt-fold-20261120.json'\nwith open",
    "residualSet32 for h in CLAIM", "residualSet32 - newTargetAll", "32 - len(targetRows_new)",
    "'legal_next_moves': 54", "'unique_strategy_rows': 23621", "'receipt': 'thirtieth'",
]:
    if stale in text:
        raise SystemExit('BUILD FAILED: stale text remains: ' + stale)
assert text.count("ROOT_HEX = '" + ROOT + "'") == 1
assert text.count("OUT = 'fold24/output/win8-root438000000818-receipt-fold-20261120.json'") == 1
assert text.count("CERT_RELPATH = '" + CERT + "'") == 1
assert text.count("PIN_F23_MACHINE_SHA256 = '" + PIN_PUB + "'") == 1
assert text.count("# ---------- fold23 (thirtieth, WIN8 root 208090020004) record chaining ----------") == 1
assert text.count("# ---------- fold23 machine rerun (published machine pristine; single rerun gate) ----------") == 1
assert text.count("# ---------- k1136 certificate record (19 gates) ----------") == 1
assert text.count("# ---------- k1136 geometry independent rederivation ----------") == 1
assert text.count("'receipt': 'thirty-first',") == 1
m = re.search(r'PIN256 = (\{.*?\n\})', text, re.S)
d = ast.literal_eval(m.group(1))
assert len(d) == 49, f'PIN256 count {len(d)}'
m = re.search(r'PINS = (\{.*?\n\})', text, re.S)
d = ast.literal_eval(m.group(1))
assert len(d) == 12, f'PINS count {len(d)}'
open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
print('BUILD OK:', DST, len(text), 'chars', text.count(chr(10))+1, 'lines')
print('PINS=12 PIN256=49')
