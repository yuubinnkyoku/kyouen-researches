#!/usr/bin/env python3
"""Generate the fold20 machine (fold_win8_root08d10000.py) from the PUBLISHED fold19
machine (fold_win8_root1009000.py, sha256-pinned below), by an exact, asserted
transformation continuing the adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign
(research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md):

  1. scalar constant replacement (W root env, output path, root hex, cert relpath),
  2. three new SHA-256 pins appended to PIN256 (fold19 record, K1121 audit, K1121 cert),
  3. the preverified-copy pins of the fold19 machine replaced by the pristine fold19
     machine pin (the fold20 gate re-runs the published fold19 machine as-is; no
     preverified patch is needed because the published fold19 machine already carries
     the FOLD_PREVERIFIED_CHAIN switch of the adopted redesign),
  4. the fold18 preverified rerun gate replaced by (a) a fold19 record chaining block
     (frontier 6,157/487,800 -> 6,152/487,418, solved 1,696, incidence 11,711,
     residual 45 -> 41) and (b) a single rerun gate: one fresh PRISTINE execution of
     the published fold19 machine in an isolated W copy, byte-compared to the
     published fold19 record (the fold18 preverified rerun, its reverse-patch
     preverification and the K1120 gate block re-run transitively inside it);
     guarded by the retained PREVERIFIED switch so fold21 can rerun THIS machine in
     preverified mode,
  5. the K1119 certificate gate block replaced by the K1121 block (all constants
     sourced from the published K1121 audit record), root geometry 50 legal moves,
  6. receipt application against open41 / residualSet41, frontier_after solved base
     1,696, closedAllNew base 71, win16 candidate accounting 7 -> 6 roots / 18 -> 15
     rows,
  7. updated result record literals (schema, ordinal, sources, join summary, controls),
  8. closedHistorical additionally unions the fold19 covered rows so that rows closed
     by the fold19 WIN8 receipt classify as 'closed-before-this-receipt'.

Every replacement asserts its occurrence count is exactly 1 (or the asserted number)
before applying; the output is py_compiled and grep-checked for stale constants.

Usage: python3 build_fold20.py [W_root]   (default /home/user/work/W20)
Input:  <W>/fold_win8_root1009000.py
Output: <W>/fold_win8_root08d10000.py
"""
import hashlib, os, sys, py_compile, ast

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W20')
SRC = f'{W}/fold_win8_root1009000.py'
DST = f'{W}/fold_win8_root08d10000.py'
PIN_PUB = '51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8'
PIN_F19_RECORD = 'c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae'
PIN_K1121_AUDIT = '0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940'
PIN_K1121_CERT = '8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2'

def die(m):
    print('BUILD FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold19 machine sha256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        die('anchor count %d != %d for: %r' % (c, n, old[:90]))
    text = text.replace(old, new)

# ---------- 1. header ----------
hdr_first = '# Receipt fold (fold19, twenty-sixth receipt) of the WIN8-D10 certificate of root'
hdr_last = "# Usage: python3 fold_win8_root1009000.py  (env FOLD19_W overrides the W root)"
i = text.index(hdr_first)
j = text.index(hdr_last) + len(hdr_last)
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    die('header anchors')
NEW_HDR = """# Receipt fold (fold20, twenty-seventh receipt) of the WIN8-D10 certificate of root
# 00000000000000003800000008d10000 (K1121: extraction + triple verification, 19-gate
# record sha256 0088ebab...; certificate sha256 8513e366..., 28,328 rows / 1,026,202
# bytes; the 50-mobility 3-claim WIN8 candidate of the K1091 sweep with uncapped
# probes 564695/673870; extracted and published by the parallel lane) into the five-parent
# S6 frontier chain -- the tenth WIN8 receipt fold, executed under the adopted
# FOLD_PREVERIFIED_CHAIN rerun-gate redesign (adoption note
# research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md): this machine
# re-runs only its immediate predecessor (the published fold19 machine, executed
# PRISTINE in an isolated W copy -- no preverified patch is needed, because the
# published fold19 machine already carries the PREVERIFIED switch and its default
# full run internally re-runs the published fold18 machine as the marker-reversible
# preverified copy -- and is verified byte-identical to the published fold19 record
# sha256 c02d9a54...), and verifies fold10..fold18 upstream by SHA pins plus the full
# frontier chain recomputation, giving the open set 6,152 rows / 487,418 cost,
# solved S6 1,696, parent incidence 11,711 and the residual-41 five-parent target
# (published fold19 values).  The WIN8 receipt of root 08d10000 is then applied:
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
# published fold19 machine, plus):
#   fold19/output/win8-root1009000-receipt-fold-20261120.json
#       research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json
#   fold_win8_root1009000.py (published fold19 machine; sha256-pinned)
#       research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root1009000.py
#   k1121/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/win8-cert-extract-verification-20261120.json
#   k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11
#       research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11
#
# Usage: python3 fold_win8_root08d10000.py  (env FOLD20_W overrides the W root)"""
text = text[:i] + NEW_HDR + text[j:]

# ---------- 2. scalars ----------
rep("PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'\n"
    "PATCHED_F18_REL = 'fold_win8_root00901010_preverified.py'\n"
    "PIN_F18_MACHINE_SHA256 = 'dcdfbf92d62409cc3a92f9f16f319e1328180622660b39751921b5de72800091'\n"
    "PATCHED_F18_SHA256 = 'd342f1f883d2e22ecca25903ec14ed24f16c77a0895e3ed022ab8832736e7f9e'",
    "PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'\n"
    "PIN_F19_MACHINE_SHA256 = '%s'" % PIN_PUB)
rep("W = os.environ.get('FOLD19_W', '/home/user/work/W19')",
    "W = os.environ.get('FOLD20_W', '/home/user/work/W20')")
rep("OUT = 'fold19/output/win8-root1009000-receipt-fold-20261120.json'",
    "OUT = 'fold20/output/win8-root08d10000-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000801212000001009000'",
    "ROOT_HEX = '00000000000000003800000008d10000'")
rep("CERT_RELPATH = 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11'",
    "CERT_RELPATH = 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11'")

# ---------- 3. PIN256 additions ----------
rep(" 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11': 'b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c',\n}",
    " 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11': 'b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c',\n"
    " 'fold19/output/win8-root1009000-receipt-fold-20261120.json': '%s',\n" % PIN_F19_RECORD +
    " 'k1121/output/win8-cert-extract-verification-20261120.json': '%s',\n" % PIN_K1121_AUDIT +
    " 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11': '%s',\n}" % PIN_K1121_CERT)

# ---------- 4. replace the fold18 preverified rerun gate: fold19 chaining + fold19 pristine rerun gate ----------
gate_first = '# ---------- fold18 machine rerun (published machine as preverified copy; single rerun gate) ----------'
gate_last = "    print('FOLD_PREVERIFIED_CHAIN=1: fold18 machine rerun gate skipped; upstream via SHA pins + chain recomputation')"
if text.count(gate_first) != 1 or text.count(gate_last) != 1:
    die('fold18 gate span anchors')
i = text.index(gate_first)
j = text.index(gate_last) + len(gate_last)
INSERT = """
# ---------- fold19 (twenty-sixth, WIN8 root 1009000) record chaining ----------
f19 = load('fold19/output/win8-root1009000-receipt-fold-20261120.json')
need(sha256_of('fold19/output/win8-root1009000-receipt-fold-20261120.json') == PIN256['fold19/output/win8-root1009000-receipt-fold-20261120.json'], 'fold19 record sha256')
need(f19['schema'] == 'n11-five-parent-win8-root1009000-receipt-fold-20261120-v1', 'fold19 schema')
need(f19['status'] == 'fold-complete', 'fold19 fold-complete')
need(f19['receipt_count'] == 1 and len(f19['receipts']) == 1, 'fold19 receipt count')
rc19 = f19['receipts'][0]
rows19 = list(rc19['covered_s6_rows'])
need(len(rows19) == len(set(rows19)) == 5, 'fold19 covered rows unique 5')
for h in rows19:
    need(h in open45, 'fold19 row not open: ' + h)
open41 = {h: v for h, v in open45.items() if h not in set(rows19)}
fa19 = f19['frontier_after']
need(len(open41) == 6152 and sum(v[0] for v in open41.values()) == 487418, 'post-fold19 frontier (must match published 6152/487418)')
need(fa19['unique_remaining_s6'] == 6152 and fa19['sum_remaining_cost'] == 487418
     and fa19['solved_s6_in_manifest'] == 1696 and fa19['parent_row_incidence'] == 11711
     and fa19['s6_needed_by_open_classes'] == 4460 and fa19['cost_needed_by_open_classes'] == 353866, 'fold19 frontier_after published values')
for rec_row in f19['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold19 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows19, 'fold19 coverage row among covered')
need(rc19['closed_edge_cost'] == sum(wl[h][0] for h in rows19), 'fold19 closed edge cost recomputed')
for h in rows19:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11711 == fa19['parent_row_incidence'], 'post-fold19 incidence 11711, got %d' % sum(inc.values()))
targetRows19 = list(rc19['covered_five_parent_target_rows'])
need(set(targetRows19) <= residualSet45 and len(targetRows19) == 4, 'fold19 target rows subset of residual45; exactly 4')
extra19 = [h for h in rows19 if h not in residualSet45]
need(extra19 == rc19['extra_s6_rows_not_in_target'], 'fold19 extra rows recorded')
residual41 = f19['five_parent_target_after']['residual_row_hex_after']
need(len(residual41) == 41 and len(set(residual41)) == 41 and residual41 == sorted(residual41), 'residual 41 sorted unique')
need(sorted(residualSet45 - set(targetRows19)) == residual41, 'residual41 == residual45 minus fold19 target rows')
need(f19['five_parent_target_after']['closed_target_rows_total'] == 71, 'fold19 closed target 71')
residualSet41 = set(residual41)
need(all(h in open41 for h in residual41), 'residual41 rows open in frontier')
print('post-fold19 frontier verified: 6152/487418, solved_s6 1696, incidence 11711, residual 41')

# ---------- fold19 machine rerun (published machine pristine; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold19 machine is executed PRISTINE (no preverified
# patch is needed: the published fold19 machine already carries the PREVERIFIED
# switch of the adopted redesign, and its default full run is a short gate that
# internally re-runs the published fold18 machine as the marker-reversible
# preverified copy, re-verifying the reverse patch) in an isolated W copy; it keeps
# every input pin, the full frontier chain recomputation, the fold18 preverified
# rerun gate, the K1119 19-gate block, the K1097 crosscheck and the receipt
# application, so its output must be byte-identical to the published fold19 record.
# When THIS machine is the rerun target of fold21, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    import shutil, subprocess
    _pub19 = open(f'{W}/fold_win8_root1009000.py', 'rb').read()
    need(hashlib.sha256(_pub19).hexdigest() == PIN_F19_MACHINE_SHA256, 'published fold19 machine sha256 pin')
    W19X = W + '-rerun-root-f19'
    if os.path.isdir(W19X): shutil.rmtree(W19X)
    shutil.copytree(W, W19X)
    _env19 = dict(os.environ); _env19['FOLD19_W'] = W19X
    _rr19 = subprocess.run([sys.executable, W19X + '/fold_win8_root1009000.py'], env=_env19, capture_output=True, text=True)
    need(_rr19.returncode == 0, 'fold19 machine pristine rerun failed: ' + _rr19.stderr[-600:])
    _rerun19_sha = hashlib.sha256(open(W19X + '/fold19/output/win8-root1009000-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun19_sha == PIN256['fold19/output/win8-root1009000-receipt-fold-20261120.json'], 'fold19 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W19X)
    print('fold19 machine pristine rerun verified: stdout ends ' + _rr19.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold19 machine rerun gate skipped; upstream via SHA pins + chain recomputation')"""
text = text[:i] + INSERT + text[j:]

# ---------- 5. K1119 -> K1121 gate block ----------
rep("# ---------- k1119 certificate record (19 gates) ----------",
    "# ---------- k1121 certificate record (19 gates) ----------")
rep("# ---------- k1119 geometry independent rederivation ----------",
    "# ---------- k1121 geometry independent rederivation ----------")
rep("k1119 = load('k1119/output/win8-cert-extract-verification-20261120.json')",
    "k1121 = load('k1121/output/win8-cert-extract-verification-20261120.json')")
rep("need(k1119['schema'] == 'win8-cert-extract-verification-v1', 'k1119 schema')",
    "need(k1121['schema'] == 'win8-cert-extract-verification-v1', 'k1121 schema')")
rep("need(k1119['all_gates_pass'] is True and k1119['gate_count'] == 19 and len(k1119['gates']) == 19, 'k1119 gate count')",
    "need(k1121['all_gates_pass'] is True and k1121['gate_count'] == 19 and len(k1121['gates']) == 19, 'k1121 gate count')")
rep("need(all(g['passed'] for g in k1119['gates']), 'k1119 every gate passed')",
    "need(all(g['passed'] for g in k1121['gates']), 'k1121 every gate passed')")
rep("need(k1119['root'] == ROOT_HEX, 'k1119 root hex')",
    "need(k1121['root'] == ROOT_HEX, 'k1121 root hex')")
rep("gate01 = [g for g in k1119['gates'] if g['gate'] == 'g01_k1091_master_sha256_pin'][0]",
    "gate01 = [g for g in k1121['gates'] if g['gate'] == 'g01_k1091_master_sha256_pin'][0]")
rep("need(gate01['detail'] == 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25', 'k1119 k1091 master sha pin')",
    "need(gate01['detail'] == 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25', 'k1121 k1091 master sha pin')")
rep("gate07 = [g for g in k1119['gates'] if g['gate'] == 'g07_k1091_root_claimed_coverage_4rows']",
    "gate07 = [g for g in k1121['gates'] if g['gate'] == 'g07_k1091_root_claimed_coverage_3rows']")
rep("need(len(CLAIM) == 4, 'k1119 claim rows are 4')",
    "need(len(CLAIM) == 3, 'k1121 claim rows are 3')")
rep("need(CLAIM == sorted(k1119['recorded']['k1091_claimed_coverage_rows']), 'k1119 claim rows consistent')",
    "need(CLAIM == sorted(k1121['recorded']['k1091_claimed_coverage_rows']), 'k1121 claim rows consistent')")
rep("gate05 = [g for g in k1119['gates'] if g['gate'] == 'g05_root_mobility_44'][0]",
    "gate05 = [g for g in k1121['gates'] if g['gate'] == 'g05_root_mobility_50'][0]")
rep("need(gate05['detail'] == 44 and gate05['passed'] is True, 'k1119 mobility 44')",
    "need(gate05['detail'] == 50 and gate05['passed'] is True, 'k1121 mobility 50')")
rep("gate08 = [g for g in k1119['gates'] if g['gate'] == 'g08_probe_reproduction_matches_k1091'][0]",
    "gate08 = [g for g in k1121['gates'] if g['gate'] == 'g08_probe_reproduction_matches_k1091'][0]")
rep("need(gate08['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1119 probe reproduction detail')",
    "need(gate08['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1121 probe reproduction detail')")
rep("gate06 = [g for g in k1119['gates'] if g['gate'] == 'g06_k1091_root_probes_win_uncapped'][0]",
    "gate06 = [g for g in k1121['gates'] if g['gate'] == 'g06_k1091_root_probes_win_uncapped'][0]")
rep("need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 192365\n"
    "     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 229502\n"
    "     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],\n"
    "     'k1119 uncapped probes 192365/229502 with terminal range [14,18]')",
    "need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 564695\n"
    "     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 673870\n"
    "     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],\n"
    "     'k1121 uncapped probes 564695/673870 with terminal range [14,18]')")
rep("gate13 = [g for g in k1119['gates'] if g['gate'] == 'g13_node_accounting_chunk_vs_single'][0]",
    "gate13 = [g for g in k1121['gates'] if g['gate'] == 'g13_node_accounting_chunk_vs_single'][0]")
rep("need(gate13['detail'] == {'a1_chunk_total_nodes': 865602, 'b_single_process_nodes': 712106}, 'k1119 extraction node accounting')",
    "need(gate13['detail'] == {'a1_chunk_total_nodes': 2428240, 'b_single_process_nodes': 1748509}, 'k1121 extraction node accounting')")
rep("gate16 = [g for g in k1119['gates'] if g['gate'] == 'g16_third_method_traversal_pass'][0]",
    "gate16 = [g for g in k1121['gates'] if g['gate'] == 'g16_third_method_traversal_pass'][0]")
rep("need(gate16['detail']['missing'] == 0 and gate16['detail']['extra'] == 0 and gate16['detail']['failure'] is None, 'k1119 third-method zero miss/extra')",
    "need(gate16['detail']['missing'] == 0 and gate16['detail']['extra'] == 0 and gate16['detail']['failure'] is None, 'k1121 third-method zero miss/extra')")
rep("gate19 = [g for g in k1119['gates'] if g['gate'] == 'g19_k1097_refsolve_footprint_match'][0]",
    "gate19 = [g for g in k1121['gates'] if g['gate'] == 'g19_k1097_refsolve_footprint_match'][0]")
rep("need(len(gate19['detail']['claimed']) == 4 and sorted(gate19['detail']['claimed']) == CLAIM, 'k1119 g19 footprint claimed == CLAIM (4 rows)')",
    "need(len(gate19['detail']['claimed']) == 3 and sorted(gate19['detail']['claimed']) == CLAIM, 'k1121 g19 footprint claimed == CLAIM (3 rows)')")
rep("need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1119 g19 k1097 sha pin')",
    "need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1121 g19 k1097 sha pin')")
rep("cert_recd = k1119['recorded']['certificate']",
    "cert_recd = k1121['recorded']['certificate']")
rep("need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1119 cert sha256')",
    "need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1121 cert sha256')")
rep("need(cert_recd['bytes'] == len(cert_bytes) == 587989, 'k1119 cert bytes')",
    "need(cert_recd['bytes'] == len(cert_bytes) == 1026202, 'k1121 cert bytes')")
rep("need(cert_recd['rows'] == 16262, 'k1119 cert rows')",
    "need(cert_recd['rows'] == 28328, 'k1121 cert rows')")
rep("need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1119 cert header')",
    "need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1121 cert header')")
rep("need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1119 cert root line')",
    "need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1121 cert root line')")
rep("need(len(cert_lines) - 2 == 16262, 'k1119 cert row count')",
    "need(len(cert_lines) - 2 == 28328, 'k1121 cert row count')")
rep("need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1119 cert row format')",
    "need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1121 cert row format')")
rep("need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1119 cert rows sorted unique')",
    "need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1121 cert rows sorted unique')")
rep("tm = k1119['recorded']['third_method']",
    "tm = k1121['recorded']['third_method']")
rep("need(tm['root_first_moves'] == 44 and tm['terminal_count'] == 5783 and tm['terminal_range'] == [14, 18]\n"
    "     and tm['visited_states'] == 37696 and tm['winner_states'] == 24352 and tm['loser_states'] == 7561\n"
    "     and tm['loser_reply_edges'] == 34261, 'k1119 third-method aggregate')",
    "need(tm['root_first_moves'] == 50 and tm['terminal_count'] == 15513 and tm['terminal_range'] == [14, 18]\n"
    "     and tm['visited_states'] == 83544 and tm['winner_states'] == 53570 and tm['loser_states'] == 14461\n"
    "     and tm['loser_reply_edges'] == 72930, 'k1121 third-method aggregate')")
rep("need(len(lmv) == 44, 'root legal move count rederivation 44')",
    "need(len(lmv) == 50, 'root legal move count rederivation 50')")
rep("print('k1119 certificate record verified: 19/19 gates, sha, header, geometry, mobility 44')",
    "print('k1121 certificate record verified: 19/19 gates, sha, header, geometry, mobility 50')")

# ---------- 6. K1097 crosscheck / receipt application constant updates ----------
rep("need(all(h in residualSet45 for h in CLAIM), 'claim rows inside residual45')",
    "need(all(h in residualSet41 for h in CLAIM), 'claim rows inside residual41')")
rep("    if h in open45: row_class[h] = 'open-frontier'",
    "    if h in open41: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open45)",
    "rootRows = sorted(h for h in rootA if h in open41)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet45)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet41)")
rep("extra_rows = [h for h in rootRows if h not in residualSet45]",
    "extra_rows = [h for h in rootRows if h not in residualSet41]")
rep("closedCost = sum(open45[h][0] for h in rootRows)",
    "closedCost = sum(open41[h][0] for h in rootRows)")
rep("    del open45[h]", "    del open41[h]")
rep("needed_rows = [h for h in open45 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open41 if demand(h)['c1'] == 0]")
rep("  'solved_s6_in_manifest': 1691 + len(rootRows),",
    "  'solved_s6_in_manifest': 1696 + len(rootRows),")
rep("  'unique_remaining_s6': len(open45),", "  'unique_remaining_s6': len(open41),")
rep("  'sum_remaining_cost': sum(v[0] for v in open45.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open41.values()),")
rep("  'cost_needed_by_open_classes': sum(open45[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open41[h][0] for h in needed_rows),")
rep("closedAllNew = 67 + len(newTargetAll)", "closedAllNew = 71 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet45 - newTargetAll)",
    "residualAfter = sorted(residualSet41 - newTargetAll)")
rep("need(len(residualAfter) == 45 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 41 - len(targetRows_new), 'residual accounting')")

# ---------- 7. classification closedHistorical extension ----------
rep("closedHistorical |= set(rows18)",
    "closedHistorical |= set(rows18)\nclosedHistorical |= set(rows19)")

# ---------- 8. result record literals ----------
rep("  'schema': 'n11-five-parent-win8-root1009000-receipt-fold-20261120-v1',",
    "  'schema': 'n11-five-parent-win8-root08d10000-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'twenty-sixth (fold19, ninth WIN8 receipt fold)',",
    "'receipt_ordinal': 'twenty-seventh (fold20, tenth WIN8 receipt fold)',")
rep("  'single_owner_note': 'research/log/2026-11-20-n11-fold19-win8-root1009000-single-owner-note.md',",
    "  'single_owner_note': 'research/log/2026-11-20-n11-fold20-win8-root08d10000-single-owner-note.md',")
rep("  'previous_fold': {'record': 'research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/output/win8-root00901010-receipt-fold-20261120.json (sha256 18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026)',",
    "  'previous_fold': {'record': 'research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json (sha256 c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae)',")
rep("                    'frontier_after': fa18},",
    "                    'frontier_after': fa19},")
rep("  'frontier_before': fa18,", "  'frontier_before': fa19,")
rep("    'record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120 (K1119: WIN8 root certificate extract + triple verification, 19 gates; 44-mobility 4-claim WIN8 candidate of the K1091 sweep with uncapped probes 192365/229502; published by the parallel lane)',",
    "    'record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120 (K1121: WIN8 root certificate extract + triple verification, 19 gates; 50-mobility 3-claim WIN8 candidate of the K1091 sweep with uncapped probes 564695/673870; published by the parallel lane)',")
rep("    'verification_sha256': PIN256['k1119/output/win8-cert-extract-verification-20261120.json'],",
    "    'verification_sha256': PIN256['k1121/output/win8-cert-extract-verification-20261120.json'],")
rep("    'certificate_path': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/certs/win8-root-00000000000000801212000001009000-20261120.n11',",
    "    'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11',")
rep("    'k1091_probes_record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/output/.input-k1091.json (K1091 alternate-15-roots d10 sweep record; sha256 edd7ac84...; claimed coverage 4 rows, pinned by K1119 g01/g07)',",
    "    'k1091_probes_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/.input-k1091.json (K1091 alternate-15-roots d10 sweep record; sha256 edd7ac84...; claimed coverage 3 rows, pinned by K1121 g01/g07)',")
# claims_record descriptive string: for root 08d10000 the K1097 footprint is
# intrinsic == claimed == 3 rows (machine-verified below); this is the 3-row version
# and, unlike the fold19 machine's source string, needs no transcription fix.
rep("; win16_intrinsic_footprints: intrinsic == claimed == 4 rows)',",
    "; win16_intrinsic_footprints: intrinsic == claimed == 3 rows)',")
rep("      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'twenty-sixth',",
    "      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'twenty-seventh',")
rep("      'legal_next_moves': 44,", "      'legal_next_moves': 50,")
rep("      'unique_strategy_rows': 16262,", "      'unique_strategy_rows': 28328,")
rep("        'source_record': 'research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120',",
    "        'source_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120',")

# win_candidate_plan_impact block (span replace)
wc_start = "  'win_candidate_plan_impact': {"
wc_end = "  'verdict_join_summary': {"
i = text.index(wc_start); j = text.index(wc_end)
NEW_WC = """  'win_candidate_plan_impact': {
    'note': 'Observation only. The K1086 probe classified 7 WIN8-D10 candidates (claims 4+4+4+3+3+3+2 = 23 rows) inside the K1097 plan (16 candidates, 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (4 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows) and fold19 retired root 1009000 (4 claimed rows); this receipt closes the 3 claimed rows of root 08d10000 (a K1091-sweep WIN candidate inside the same K1097 footprint plan); the remaining 6 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3 = 15 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',
    'retired_win_candidate_root': ROOT_HEX,
    'rows_of_retired_root': CLAIM,
    'retired_root_predecessor': '00000000000000801212000001009000',
    'win16_candidates_remaining': 6,
    'win16_claimed_rows_remaining': 15,
    'residual23_untouched': True,
  },
"""
text = text[:i] + NEW_WC + text[j:]

# verdict_join_summary block (span replace)
vj_end = "  'controls': {"
i = text.index(wc_end); j = text.index(vj_end)
NEW_VJ = """  'verdict_join_summary': {
    'join_basis': 'published fold19 chain frontier (single fresh rerun gate: the published fold19 machine executed pristine in an isolated W copy, byte-identical to the published fold19 record; the fold18 preverified rerun, its reverse-patch preverification and the K1120 gate block re-run transitively inside it; fold10..fold18 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1121 triple-verified WIN8 certificate + K1091 claims and K1097 refsolve coverage footprints',
    'receipt_root_is': 'certificate-backed WIN8-D10 (K1121: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',
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
    'fold19_record_chained_and_published_values_matched': True,
    'fold19_frontier_6152_487418_recomputed_from_worklist': True,
    'post_fold19_incidence_11711_recomputed': True,
    'fold10_record_sha256_pin_verified': True,
    'fold11_record_sha256_pin_verified': True,
    'fold12_record_sha256_pin_verified': True,
    'fold13_record_sha256_pin_verified': True,
    'fold14_record_sha256_pin_verified': True,
    'fold15_record_sha256_pin_verified': True,
    'fold16_record_sha256_pin_verified': True,
    'fold17_record_sha256_pin_verified': True,
    'fold18_record_sha256_pin_verified': True,
    'fold19_record_sha256_pin_verified': True,
    'rerun_gate_redesign_adopted_single_predecessor_rerun': True,
    'fold11_through_fold17_machine_recursive_reruns_replaced_by_sha_pins_and_chain_recomputation': True,
    'fold19_machine_pristine_rerun_byte_identical': True,
    'fold18_preverified_rerun_and_reverse_patch_rechecked_transitively_inside_fold19_rerun': True,
    'all_chain_input_pins_verified_upfront': True,
    'k1121_cert_19_gates_rechecked_and_bytes_verified': True,
    'k1120_cert_gates_rechecked_inside_preverified_fold18_rerun': True,
    'k1119_cert_gates_rechecked_inside_fold19_pristine_rerun': True,
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

rep("os.makedirs(f'{W}/fold19/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold20/output', exist_ok=True)")

# ---------- 9. final hygiene checks ----------
for stale in ["PATCHED_F18", "PIN_F18", "'FOLD18_W'", "W18X", "'-rerun-root-f18'",
              "fold_win8_root00901010", "g07_k1091_root_claimed_coverage_4rows",
              "k1095", "mobility 44", "587989", "16262", "865602", "712106",
              "192365", "229502", "5783", "37696", "24352", "7561", "34261",
              "1691 + len(rootRows)", "45 - len(targetRows_new)"]:
    if stale in text:
        die('stale constant remains: ' + stale)
import re as _re
allowed_k1119 = {
    " 'k1119/output/win8-cert-extract-verification-20261120.json': '4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100',",
    " 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11': 'b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c',",
    "    'k1119_cert_gates_rechecked_inside_fold19_pristine_rerun': True,",
}
allowed_k1120 = {
    " 'k1120/output/win8-cert-extract-verification-20261120.json': 'ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516',",
    " 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11': 'd6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1',",
    "    'k1120_cert_gates_rechecked_inside_preverified_fold18_rerun': True,",
}
for m in _re.findall(r".*[k]1119.*", text):
    if m not in allowed_k1119:
        die('unexpected k1119 line: ' + m)
for m in _re.findall(r".*[k]1120.*", text):
    if m not in allowed_k1120:
        die('unexpected k1120 line: ' + m)

open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
print('fold20 machine built:', DST)
print('sha256:', hashlib.sha256(text.encode()).hexdigest())
print('lines:', text.count('\n') + 1)
