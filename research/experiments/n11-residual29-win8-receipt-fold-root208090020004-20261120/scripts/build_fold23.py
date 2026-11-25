#!/usr/bin/env python3
"""Generate the fold23 machine (fold_win8_root208090020004.py) from the PUBLISHED
fold22 machine (fold_win8_root840500.py, sha256-pinned below), by an exact,
asserted transformation continuing the adopted FOLD_PREVERIFIED_CHAIN
rerun-gate redesign:

  1. scalar constant replacement (W root env, output path, root hex, cert relpath,
     predecessor machine pin),
  2. three new SHA-256 pins appended to PIN256 (fold22 record, K1123 audit, K1123 cert),
  3. the fold21 machine rerun gate replaced by (a) a fold22 record chaining block
     (frontier 6,136/486,243 -> 6,130/485,759, solved 1,718, incidence 11,671,
     s6_needed 4,438, cost_needed 352,207, residual 35 -> 32, closed target 80)
     and (b) a single rerun gate: one fresh PRISTINE execution of the published
     fold22 machine in an isolated W copy, byte-compared to the published fold22
     record f6e011f4... (the fold21 machine pristine rerun gate and the K1125 gate
     block re-run transitively inside it); guarded by the retained PREVERIFIED
     switch so fold24 can rerun THIS machine in preverified mode,
  4. the K1125 certificate gate block replaced by the K1123 block (constants
     sourced from the published K1123 audit record; FRESH-PROBE basis: g01 pins the
     K1119 provenance log (git blob 51bad3..., sha256 4d11ca89...), g02 pins the
     published total 793,616 in that log, g06 pins the fresh probe constants
     442,824/350,792 summing to 793,616 and g08 pins the probe reproduction; gate
     names differ from the K1089-sweep family), root geometry 54 legal moves,
  5. receipt application against open32 / residualSet32, frontier_after solved base
     1,718, closedAllNew base 80, win16 candidate accounting 4 -> 3 roots / 9 -> 6
     rows, retired_root_predecessor 840500,
  6. updated result record literals (schema, ordinal, sources, join summary,
     controls), including the win-candidate note listing fold18/fold22 explicitly,
  7. closedHistorical additionally unions the fold22 covered rows (rows22) so that
     rows closed by the fold22 WIN8 receipt classify as 'closed-before-this-receipt'.

Every replacement asserts its occurrence count before applying; the output is
py_compiled, AST-checked and grep-checked for stale constants.

Usage: python3 build_fold23.py [W_root]   (default /home/user/work/W23)
Input:  <W>/fold_win8_root840500.py   (published fold22 machine)
Output: <W>/fold_win8_root208090020004.py
"""
import hashlib, os, sys, py_compile, ast, re

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W23')
SRC = f'{W}/fold_win8_root840500.py'
DST = f'{W}/fold_win8_root208090020004.py'
PIN_PUB = 'd5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d'
PIN_F22_RECORD = 'f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488'
PIN_K1123_AUDIT = '6ea634c9fdd005626904669e08cb7139e59e78120a0b8c9e1dd48fde0b70ddf0'
PIN_K1123_CERT = 'b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e'

def die(m):
    print('BUILD FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold22 machine sha256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        die('anchor count %d != %d for: %r' % (c, n, old[:90]))
    text = text.replace(old, new)

# ---------- 1. header ----------
hdr_first = '# Receipt fold (fold22, twenty-ninth receipt) of the WIN8-D10 certificate of root'
hdr_last = "# Usage: python3 fold_win8_root840500.py  (env FOLD22_W overrides the W root)"
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    die('header anchors')
i = text.index(hdr_first)
j = text.index(hdr_last) + len(hdr_last)
NEW_HDR = """# Receipt fold (fold23, thirtieth receipt) of the WIN8-D10 certificate of root
# 00000000000020809002000480100000 (K1123: extraction + triple verification, 19-gate
# record sha256 6ea634c9...; certificate sha256 b8145352..., 23,621 rows / 855,258
# bytes; the 54-mobility 3-claim WIN8-D10 candidate on the FRESH-PROBE basis --
# fresh probes 350792/442824 summing to the published K1119 fresh-probe total
# 793616, provenance log pinned by g01/g02) into the five-parent S6 frontier chain
# -- the thirteenth WIN8 receipt fold, executed under the adopted
# FOLD_PREVERIFIED_CHAIN rerun-gate redesign: this machine re-runs only its
# immediate predecessor (the published fold22 machine, executed PRISTINE in an
# isolated W copy -- no preverified patch is needed, because the published fold22
# machine already carries the PREVERIFIED switch and its default full run internally
# re-runs the published fold21 machine pristine, which in turn re-checks the fold20
# pristine rerun and the K1124 gate blocks -- and the K1125 19-gate block itself
# re-runs inside the fold22 machine -- and is verified byte-identical to the
# published fold22 record sha256 f6e011f4...), and verifies fold10..fold21 upstream
# by SHA pins plus the full frontier chain recomputation, giving the open set
# 6,130 rows / 485,759 cost, solved S6 1,718, parent incidence 11,671 and the
# residual-32 five-parent target (published fold22 values).  The WIN8 receipt of
# root 208090020004 is then applied: the covered S6 rows of the root are
# rederived geometrically by two independent methods -- (A) the fold-chain convention
# of 8 D4 images with C(8,2) two-stone removals (224 operations) and (B) the refsolve
# coverage_of82 convention of the C(8,6)=28 six-stone subsets of the root -- whose
# canonical row sets must be equal (D4-equivariance) and whose intersection with the
# open frontier is the receipt closure.
#
# All chain and certificate inputs are fail-closed SHA-pinned.  Bookkeeping
# only: WIN8-D10 proves only the game tree of the eight-stone root; REFUTED-D10
# is not a LOSS proof; no game value near the empty board is asserted.
# 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map (identical chain inputs as the
# published fold22 machine, plus):
#   fold22/output/win8-root840500-receipt-fold-20261120.json
#       research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/output/win8-root840500-receipt-fold-20261120.json
#   fold_win8_root840500.py (published fold22 machine; sha256-pinned)
#       research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/scripts/fold_win8_root840500.py
#   k1123/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/output/win8-cert-extract-verification-20261120.json
#   k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11
#       research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/certs/win8-root-00000000000020809002000480100000-20261120.n11
#
# Usage: python3 fold_win8_root208090020004.py  (env FOLD23_W overrides the W root)"""
text = text[:i] + NEW_HDR + text[j:]

# ---------- 2. scalar constants ----------
rep("PIN_F21_MACHINE_SHA256 = '44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b'",
    "PIN_F22_MACHINE_SHA256 = '" + PIN_PUB + "'")
rep("W = os.environ.get('FOLD22_W', '/home/user/work/W22')",
    "W = os.environ.get('FOLD23_W', '/home/user/work/W23')")
rep("OUT = 'fold22/output/win8-root840500-receipt-fold-20261120.json'",
    "OUT = 'fold23/output/win8-root208090020004-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000801202000000840500'",
    "ROOT_HEX = '00000000000020809002000480100000'")
rep("CERT_RELPATH = 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11'",
    "CERT_RELPATH = 'k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11'")

# ---------- 3. PIN256 additions ----------
rep(" 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11': '21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc',\n}",
    " 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11': '21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc',\n"
    " 'fold22/output/win8-root840500-receipt-fold-20261120.json': '" + PIN_F22_RECORD + "',\n"
    " 'k1123/output/win8-cert-extract-verification-20261120.json': '" + PIN_K1123_AUDIT + "',\n"
    " 'k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11': '" + PIN_K1123_CERT + "',\n}")

# ---------- 4. fold21 machine rerun gate -> fold22 chaining + fold22 rerun gate ----------
rg_first = '# ---------- fold21 machine rerun (published machine pristine; single rerun gate) ----------'
rg_last_tail = "else:\n    print('FOLD_PREVERIFIED_CHAIN=1: fold21 machine rerun gate skipped; upstream via SHA pins + chain recomputation')\n"
if text.count(rg_first) != 1 or text.count(rg_last_tail) != 1:
    die('rerun gate anchors')
NEW_RERUN = """# ---------- fold22 (twenty-ninth, WIN8 root 840500) record chaining ----------
f22 = load('fold22/output/win8-root840500-receipt-fold-20261120.json')
need(sha256_of('fold22/output/win8-root840500-receipt-fold-20261120.json') == PIN256['fold22/output/win8-root840500-receipt-fold-20261120.json'], 'fold22 record sha256')
need(f22['schema'] == 'n11-five-parent-win8-root840500-receipt-fold-20261120-v1', 'fold22 schema')
need(f22['status'] == 'fold-complete', 'fold22 fold-complete')
need(f22['receipt_count'] == 1 and len(f22['receipts']) == 1, 'fold22 receipt count')
rc22 = f22['receipts'][0]
rows22 = list(rc22['covered_s6_rows'])
need(len(rows22) == len(set(rows22)) == 6, 'fold22 covered rows unique 6')
for h in rows22:
    need(h in open35, 'fold22 row not open: ' + h)
open32 = {h: v for h, v in open35.items() if h not in set(rows22)}
fa22 = f22['frontier_after']
need(len(open32) == 6130 and sum(v[0] for v in open32.values()) == 485759, 'post-fold22 frontier (must match published 6130/485759)')
need(fa22['unique_remaining_s6'] == 6130 and fa22['sum_remaining_cost'] == 485759
     and fa22['solved_s6_in_manifest'] == 1718 and fa22['parent_row_incidence'] == 11671
     and fa22['s6_needed_by_open_classes'] == 4438 and fa22['cost_needed_by_open_classes'] == 352207, 'fold22 frontier_after published values')
for rec_row in f22['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold22 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows22, 'fold22 coverage row among covered')
need(len(f22['new_receipt_coverage']['rows']) == 6, 'fold22 coverage rows count 6')
need(rc22['closed_edge_cost'] == sum(wl[h][0] for h in rows22), 'fold22 closed edge cost recomputed')
for h in rows22:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11671 == fa22['parent_row_incidence'], 'post-fold22 incidence 11671, got %d' % sum(inc.values()))
targetRows22 = list(rc22['covered_five_parent_target_rows'])
need(set(targetRows22) <= residualSet35 and len(targetRows22) == 3, 'fold22 target rows subset of residual35; exactly 3')
extra22 = [h for h in rows22 if h not in residualSet35]
need(extra22 == rc22['extra_s6_rows_not_in_target'], 'fold22 extra rows recorded')
need(f22['receipt_ordinal'] == 'twenty-ninth (fold22, twelfth WIN8 receipt fold)', 'fold22 ordinal')
residual32 = f22['five_parent_target_after']['residual_row_hex_after']
need(len(residual32) == 32 and len(set(residual32)) == 32 and residual32 == sorted(residual32), 'residual 32 sorted unique')
need(sorted(residualSet35 - set(targetRows22)) == residual32, 'residual32 == residual35 minus fold22 target rows')
need(f22['five_parent_target_after']['closed_target_rows_total'] == 80, 'fold22 closed target 80')
residualSet32 = set(residual32)
need(all(h in open32 for h in residual32), 'residual32 rows open in frontier')
print('post-fold22 frontier verified: 6130/485759, solved_s6 1718, incidence 11671, residual 32')

# ---------- fold22 machine rerun (published machine pristine; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold22 machine is executed PRISTINE (no preverified
# patch is needed: the published fold22 machine already carries the PREVERIFIED
# switch of the adopted redesign) in an isolated W copy; it keeps every input
# pin, the full frontier chain recomputation, the fold21 machine pristine rerun
# gate, the K1125 19-gate block, the K1097 crosscheck and the receipt
# application, so its output must be byte-identical to the published fold22 record.
# When THIS machine is the rerun target of fold24, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    import shutil, subprocess
    _pub22 = open(f'{W}/fold_win8_root840500.py', 'rb').read()
    need(hashlib.sha256(_pub22).hexdigest() == PIN_F22_MACHINE_SHA256, 'published fold22 machine sha256 pin')
    W22X = W + '-rerun-root-f22'
    if os.path.isdir(W22X): shutil.rmtree(W22X)
    shutil.copytree(W, W22X)
    _env22 = dict(os.environ); _env22['FOLD22_W'] = W22X
    _rr22 = subprocess.run([sys.executable, W22X + '/fold_win8_root840500.py'], env=_env22, capture_output=True, text=True)
    need(_rr22.returncode == 0, 'fold22 machine pristine rerun failed: ' + _rr22.stderr[-600:])
    _rerun22_sha = hashlib.sha256(open(W22X + '/fold22/output/win8-root840500-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun22_sha == PIN256['fold22/output/win8-root840500-receipt-fold-20261120.json'], 'fold22 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W22X)
    print('fold22 machine pristine rerun verified: stdout ends ' + _rr22.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold22 machine rerun gate skipped; upstream via SHA pins + chain recomputation')
"""
i = text.index(rg_first)
j = text.index(rg_last_tail) + len(rg_last_tail)
text = text[:i] + NEW_RERUN + text[j:]

# ---------- 5. K1125 gate block -> K1123 gate block (fresh-probe family) ----------
kb_first = '# ---------- k1125 certificate record (19 gates) ----------'
kb_mid = '# ---------- k1125 geometry independent rederivation ----------'
if text.count(kb_first) != 1 or text.count(kb_mid) != 1:
    die('k-block anchors')
i = text.index(kb_first)
j = text.index(kb_mid) + len(kb_mid)
block = text[i:j]
if block.count('k1125') < 5:
    die('k-block rename sanity')
block = block.replace('k1125', 'k1123').replace('K1125', 'K1123')

def brep(old, new, n=1):
    global block
    c = block.count(old)
    if c != n:
        die('k-block anchor count %d != %d for: %r' % (c, n, old[:90]))
    block = block.replace(old, new)

# g01: K1089 master pin -> K1119 provenance log pin (fresh-probe basis), and add g02
brep("gate01['detail'] == '808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc', 'k1123 k1089 master sha pin'",
     "gate01['detail'] == {'git_blob': '51bad3fac4c36fcd1cbf6aeec01b7e153d9adb89', 'sha256': '4d11ca896815b73e4e0616a07c81f7abc582d4f5401174462d63e3abd27a4472'}, 'k1123 fresh-probe basis: K1119 provenance log pin')\n"
     "gate02 = [g for g in k1123['gates'] if g['gate'] == 'g02_k1119_log_root_probe_total_published'][0]\n"
     "need(gate02['detail'] == {'published_total': 793616, 'root_hex_in_log': True, 'uncapped_loss_true_statement_in_log': True}, 'k1123 g02 published probe total 793616 in the K1119 log'")
brep("'g01_k1089_master_sha256_pin'", "'g01_k1119_log_sha256_pin'")
brep("'g07_k1089_root_claimed_coverage_3rows'", "'g07_k1097_root_claimed_coverage_3rows'")
brep("k1123['recorded']['k1089_claimed_coverage_rows']", "k1123['recorded']['k1097_claimed_coverage_rows']")
brep("'g05_root_mobility_58'", "'g05_root_mobility_54'")
brep("gate05['detail'] == 58 and gate05['passed'] is True, 'k1123 mobility 58'",
     "gate05['detail'] == 54 and gate05['passed'] is True, 'k1123 mobility 54'")
brep("'g08_probe_reproduction_matches_k1089'", "'g08_probe_reproduction_matches_k1119_total'")
brep("'g06_k1089_root_probes_win_uncapped'", "'g06_fresh_probe_constants_match_k1119_total'")
brep("need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 736409\n"
     "     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 878391\n"
     "     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],\n"
     "     'k1123 uncapped probes 736409/878391 with terminal range [14,18]')",
     "need(gate06['detail'] == {'andclose0': 442824, 'andclose1': 350792, 'sum': 793616},\n"
     "     'k1123 fresh probes 442824/350792 summing to the K1119 published total 793616')")
brep("{'a1_chunk_total_nodes': 2310103, 'b_single_process_nodes': 1984636}",
     "{'a1_chunk_total_nodes': 3009765, 'b_single_process_nodes': 3009765}")
brep("'g19_k1097_refsolve_footprint_match'", "'g19_k1097_footprint_and_fold18_residual_open'")
brep("need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1123 g19 k1097 sha pin')",
     "need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1123 g19 k1097 sha pin')\n"
     "need(gate19['detail']['fold18_sha256'] == PIN256['fold18/output/win8-root00901010-receipt-fold-20261120.json'], 'k1123 g19 fold18 record sha pin')")
brep("== 1067425", "== 855258")
brep("== 29468", "== 23621", n=2)
brep("tm['root_first_moves'] == 58 and tm['terminal_count'] == 9810 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 59990 and tm['winner_states'] == 38458 and tm['loser_states'] == 11722\n"
     "     and tm['loser_reply_edges'] == 52360, 'k1123 third-method aggregate'",
     "tm['root_first_moves'] == 54 and tm['terminal_count'] == 7516 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 49094 and tm['winner_states'] == 31623 and tm['loser_states'] == 9955\n"
     "     and tm['loser_reply_edges'] == 43650, 'k1123 third-method aggregate'")
text = text[:i] + block + text[j:]

# geometry / verification prints
rep("need(len(lmv) == 58, 'root legal move count rederivation 58')",
    "need(len(lmv) == 54, 'root legal move count rederivation 54')")
rep("print('k1125 certificate record verified: 19/19 gates, sha, header, geometry, mobility 58')",
    "print('k1123 certificate record verified: 19/19 gates, sha, header, geometry, mobility 54')")

# ---------- 6. K1097 crosscheck ----------
rep("need(all(h in residualSet35 for h in CLAIM), 'claim rows inside residual35')",
    "need(all(h in residualSet32 for h in CLAIM), 'claim rows inside residual32')")
rep("need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1089/K1125 claim')",
    "need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1123 claim (K1097 record)')")
rep("need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1089/K1125 claim')",
    "need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1123 claim (K1097 record)')")

# ---------- 7. classification + receipt application on open32 / residualSet32 ----------
rep("    if h in open35: row_class[h] = 'open-frontier'",
    "    if h in open32: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open35)",
    "rootRows = sorted(h for h in rootA if h in open32)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet35)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet32)")
rep("extra_rows = [h for h in rootRows if h not in residualSet35]",
    "extra_rows = [h for h in rootRows if h not in residualSet32]")
rep("closedCost = sum(open35[h][0] for h in rootRows)",
    "closedCost = sum(open32[h][0] for h in rootRows)")
rep("    del open35[h]", "    del open32[h]")
rep("needed_rows = [h for h in open35 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open32 if demand(h)['c1'] == 0]")
rep("  'unique_remaining_s6': len(open35),",
    "  'unique_remaining_s6': len(open32),")
rep("  'sum_remaining_cost': sum(v[0] for v in open35.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open32.values()),")
rep("  'cost_needed_by_open_classes': sum(open35[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open32[h][0] for h in needed_rows),")
rep("closedHistorical |= set(rows20)\nclosedHistorical |= set(rows21)",
    "closedHistorical |= set(rows20)\nclosedHistorical |= set(rows21)\nclosedHistorical |= set(rows22)")
rep("'solved_s6_in_manifest': 1712 + len(rootRows),",
    "'solved_s6_in_manifest': 1718 + len(rootRows),")
rep("closedAllNew = 77 + len(newTargetAll)", "closedAllNew = 80 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet35 - newTargetAll)",
    "residualAfter = sorted(residualSet32 - newTargetAll)")
rep("need(len(residualAfter) == 35 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 32 - len(targetRows_new), 'residual accounting')")

# ---------- 8. result record ----------
rep("'schema': 'n11-five-parent-win8-root840500-receipt-fold-20261120-v1',",
    "'schema': 'n11-five-parent-win8-root208090020004-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'twenty-ninth (fold22, twelfth WIN8 receipt fold)',",
    "'receipt_ordinal': 'thirtieth (fold23, thirteenth WIN8 receipt fold)',")
rep("'single_owner_note': 'research/log/2026-11-20-n11-fold22-win8-root840500-single-owner-note.md',",
    "'single_owner_note': 'research/log/2026-11-20-n11-fold23-win8-root208090020004-single-owner-note.md',")
rep("'record': 'research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/output/win8-root80880200-receipt-fold-20261120.json (sha256 9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39)',\n"
    "                    'frontier_after': fa21},",
    "'record': 'research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/output/win8-root840500-receipt-fold-20261120.json (sha256 " + PIN_F22_RECORD + ")',\n"
    "                    'frontier_after': fa22},")
rep("'record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120 (K1125: WIN8 root certificate extract + triple verification, 19 gates; 58-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with uncapped probes 736409/878391; published by the long lane)',",
    "'record': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120 (K1123: WIN8 root certificate extract + triple verification, 19 gates; 54-mobility 3-claim WIN8-D10 candidate on the fresh-probe basis, fresh probes 350792/442824 matching the published K1119 total 793616)',")
rep("'verification_sha256': PIN256['k1125/output/win8-cert-extract-verification-20261120.json'],",
    "'verification_sha256': PIN256['k1123/output/win8-cert-extract-verification-20261120.json'],")
rep("'certificate_path': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/certs/win8-root-00000000000000801202000000840500-20261120.n11',",
    "'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/certs/win8-root-00000000000020809002000480100000-20261120.n11',")
rep("'k1089_sweep_record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/output/.input-k1089.json (K1089 replacement16 sweep record; sha256 808fbda1...; claimed coverage 3 rows, pinned by K1125 g01/g07)',",
    "'fresh_probe_basis': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/output/.input-k1119-log.md (published K1119 fresh-probe log; git blob 51bad3fac..., sha256 4d11ca89...; probe total 793616, pinned by K1123 g01/g02/g06/g08)',")
rep("'receipt': 'twenty-ninth',", "'receipt': 'thirtieth',")
rep("'legal_next_moves': 58,", "'legal_next_moves': 54,")
rep("'unique_strategy_rows': 29468,", "'unique_strategy_rows': 23621,")
rep("'source_record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120',",
    "'source_record': 'research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120',")
rep("'frontier_before': fa21,", "'frontier_before': fa22,")

# win candidate plan impact
rep("fold17 retired root 22081000 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows) and fold21 retired root 80880200 (3 claimed rows); this receipt closes the 3 claimed rows of root 840500 (a K1089 replacement16-sweep WIN candidate inside the same K1097 footprint plan); the remaining 4 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3 = 9 claimed rows",
    "fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows), fold21 retired root 80880200 (3 claimed rows) and fold22 retired root 840500 (3 claimed rows); this receipt closes the 3 claimed rows of root 208090020004 (the last published WIN8-D10 candidate inside the same K1097 footprint win16 plan); the remaining 3 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3-3 = 6 claimed rows")
rep("'retired_root_predecessor': '00000000000000801202000800880200',",
    "'retired_root_predecessor': '00000000000000801202000000840500',")
rep("'win16_candidates_remaining': 4,", "'win16_candidates_remaining': 3,")
rep("'win16_claimed_rows_remaining': 9,", "'win16_claimed_rows_remaining': 6,")

# verdict join summary
rep("'join_basis': 'published fold21 chain frontier (single fresh rerun gate: the published fold21 machine executed pristine in an isolated W copy, byte-identical to the published fold21 record; the fold20 machine pristine rerun gate and the K1124 gate block re-run transitively inside it; fold10..fold20 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1125 triple-verified WIN8 certificate + K1089 replacement16-sweep claims and K1097 refsolve coverage footprints',",
    "'join_basis': 'published fold22 chain frontier (single fresh rerun gate: the published fold22 machine executed pristine in an isolated W copy, byte-identical to the published fold22 record; the fold21 machine pristine rerun gate and the K1125 gate block re-run transitively inside it; fold10..fold21 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1123 triple-verified WIN8 certificate on the fresh-probe basis (probes match the published K1119 total 793616) + K1097 refsolve coverage footprints',")
rep("'receipt_root_is': 'certificate-backed WIN8-D10 (K1125: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',",
    "'receipt_root_is': 'certificate-backed WIN8-D10 (K1123: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate fresh-probe record)',")

# controls
rep("    'post_fold21_incidence_11683_recomputed': True,",
    "    'post_fold21_incidence_11683_recomputed': True,\n"
    "    'fold22_record_chained_and_published_values_matched': True,\n"
    "    'fold22_frontier_6130_485759_recomputed_from_worklist': True,\n"
    "    'post_fold22_incidence_11671_recomputed': True,")
rep("    'fold21_record_sha256_pin_verified': True,",
    "    'fold21_record_sha256_pin_verified': True,\n    'fold22_record_sha256_pin_verified': True,")
rep("    'fold21_machine_pristine_rerun_byte_identical': True,",
    "    'fold21_machine_pristine_rerun_byte_identical': True,\n    'fold22_machine_pristine_rerun_byte_identical': True,")
rep("    'fold20_machine_pristine_rerun_rechecked_transitively_inside_fold21_rerun': True,",
    "    'fold20_machine_pristine_rerun_rechecked_transitively_inside_fold21_rerun': True,\n    'fold21_machine_pristine_rerun_rechecked_transitively_inside_fold22_rerun': True,")
rep("    'k1125_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1124_cert_gates_rechecked_inside_fold21_pristine_rerun': True,",
    "    'k1123_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1125_cert_gates_rechecked_inside_fold22_pristine_rerun': True,\n    'k1124_cert_gates_rechecked_inside_fold21_pristine_rerun': True,")
rep("os.makedirs(f'{W}/fold22/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold23/output', exist_ok=True)")

# ---------- 9. write + machine checks ----------
open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
for stale in ['PIN_F21_MACHINE_SHA256', '_pub21', 'W21X = ', '_rr21', 'fold21 machine rerun',
              "'g01_k1089_master_sha256_pin'", "'g06_k1089_root_probes_win_uncapped'",
              "'g08_probe_reproduction_matches_k1089'", "'g07_k1089_root_claimed_coverage_3rows'",
              "'g19_k1097_refsolve_footprint_match'", '808fbda1', 'mobility 58',
              '== 736409', '== 878391', '2310103', '1984636', '== 1067425', '29468',
              '9810', '59990', '38458', '11722', '52360', 'del open35', 'open35[h]',
              'for h in rootA if h in open35', 'in residualSet35 -', "if h in open35",
              'k1125 certificate record verified', 'k1089_sweep_record',
              "'frontier_after': fa21", "'frontier_before': fa21",
              'residualSet35 - newTargetAll', 'len(open35),', '== 35 - len(targetRows_new)']:
    if stale in text:
        die('stale constant remains: ' + stale)
# positive sanity
assert text.count("ROOT_HEX = '00000000000020809002000480100000'") == 1
assert text.count("OUT = 'fold23/output/win8-root208090020004-receipt-fold-20261120.json'") == 1
assert text.count("os.environ.get('FOLD23_W'") == 1
assert text.count('# ---------- fold22 (twenty-ninth, WIN8 root 840500) record chaining ----------') == 1
assert text.count('# ---------- fold22 machine rerun (published machine pristine; single rerun gate) ----------') == 1
assert text.count('closedHistorical |= set(rows22)') == 1
assert text.count('need(len(residualAfter) == 32 - len(targetRows_new)') == 1
assert text.count("'receipt': 'thirtieth',") == 1
assert text.count('k1123 fresh probes 442824/350792 summing to the K1119 published total 793616') == 1
assert text.count('# ---------- k1123 certificate record (19 gates) ----------') == 1
assert text.count('# ---------- k1123 geometry independent rederivation ----------') == 1
assert text.count("'g01_k1119_log_sha256_pin'") == 1
assert text.count("'g02_k1119_log_root_probe_total_published'") == 1
assert text.count("WIN8-D10 candidate on the fresh-probe basis") >= 1
m = re.search(r'PIN256 = \{(.*?)\n\}', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 46, 'PIN256 count %d' % len(d)
m = re.search(r'PINS = \{(.*?)\n\}', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 12, 'PINS count %d' % len(d)
print('BUILD OK:', DST, len(text), 'chars')
print('machine lines:', text.count(chr(10)) + 1)
