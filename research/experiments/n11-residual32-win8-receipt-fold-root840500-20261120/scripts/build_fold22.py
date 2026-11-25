#!/usr/bin/env python3
"""Generate the fold22 machine (fold_win8_root840500.py) from the PUBLISHED fold21
machine (fold_win8_root80880200.py, sha256-pinned below), by an exact, asserted
transformation continuing the adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign:

  1. scalar constant replacement (W root env, output path, root hex, cert relpath,
     predecessor machine pin),
  2. three new SHA-256 pins appended to PIN256 (fold21 record, K1125 audit, K1125 cert),
  3. the fold20 machine rerun gate replaced by (a) a fold21 record chaining block
     (frontier 6,144/486,819 -> 6,136/486,243, solved 1,712, incidence 11,683,
     s6_needed 4,444, cost_needed 352,691, residual 38 -> 35, closed target 77)
     and (b) a single rerun gate: one fresh PRISTINE execution of the published
     fold21 machine in an isolated W copy, byte-compared to the published fold21
     record 9a4da2f6... (the fold20 machine pristine rerun gate and the K1124 gate
     block re-run transitively inside it); guarded by the retained PREVERIFIED
     switch so fold23 can rerun THIS machine in preverified mode,
  4. the K1124 certificate gate block replaced by the K1125 block (all constants
     sourced from the published K1125 audit record; K1089 replacement16-sweep
     basis: g01 master pin 808fbda1..., g08 probe_reproduction_matches_k1089),
     root geometry 58 legal moves,
  5. receipt application against open35 / residualSet35, frontier_after solved base
     1,712, closedAllNew base 77, win16 candidate accounting 5 -> 4 roots / 12 -> 9
     rows, retired_root_predecessor 80880200,
  6. updated result record literals (schema, ordinal, sources, join summary, controls),
  7. closedHistorical additionally unions the fold21 covered rows (rows21) so that
     rows closed by the fold21 WIN8 receipt classify as 'closed-before-this-receipt'.

Every replacement asserts its occurrence count before applying; the output is
py_compiled, AST-checked and grep-checked for stale constants.

Usage: python3 build_fold22.py [W_root]   (default /home/user/work/W22)
Input:  <W>/fold_win8_root80880200.py   (published fold21 machine)
Output: <W>/fold_win8_root840500.py
"""
import hashlib, os, sys, py_compile, ast, re

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W22')
SRC = f'{W}/fold_win8_root80880200.py'
DST = f'{W}/fold_win8_root840500.py'
PIN_PUB = '44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b'
PIN_F21_RECORD = '9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39'
PIN_K1125_AUDIT = '06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886'
PIN_K1125_CERT = '21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc'

def die(m):
    print('BUILD FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold21 machine sha256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        die('anchor count %d != %d for: %r' % (c, n, old[:90]))
    text = text.replace(old, new)

# ---------- 1. header ----------
hdr_first = '# Receipt fold (fold21, twenty-eighth receipt) of the WIN8-D10 certificate of root'
hdr_last = "# Usage: python3 fold_win8_root80880200.py  (env FOLD21_W overrides the W root)"
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    die('header anchors')
i = text.index(hdr_first)
j = text.index(hdr_last) + len(hdr_last)
NEW_HDR = """# Receipt fold (fold22, twenty-ninth receipt) of the WIN8-D10 certificate of root
# 00000000000000801202000000840500 (K1125: extraction + triple verification, 19-gate
# record sha256 06c65f76...; certificate sha256 21ad6195..., 29,468 rows / 1,067,425
# bytes; the 58-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with
# uncapped probes 736409/878391; extracted and published by the long lane) into the
# five-parent S6 frontier chain -- the twelfth WIN8 receipt fold, executed under the
# adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign: this machine re-runs only its
# immediate predecessor (the published fold21 machine, executed PRISTINE in an
# isolated W copy -- no preverified patch is needed, because the published fold21
# machine already carries the PREVERIFIED switch and its default full run internally
# re-runs the published fold20 machine pristine, which in turn re-checks the fold19
# pristine rerun and the K1121/K1124 gate blocks -- and is verified
# byte-identical to the published fold21 record sha256 9a4da2f6...), and verifies
# fold10..fold20 upstream by SHA pins plus the full frontier chain recomputation,
# giving the open set 6,136 rows / 486,243 cost, solved S6 1,712, parent incidence
# 11,683 and the residual-35 five-parent target (published fold21 values).  The WIN8
# receipt of root 840500 is then applied: the covered S6 rows of the root are
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
# published fold21 machine, plus):
#   fold21/output/win8-root80880200-receipt-fold-20261120.json
#       research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/output/win8-root80880200-receipt-fold-20261120.json
#   fold_win8_root80880200.py (published fold21 machine; sha256-pinned)
#       research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/scripts/fold_win8_root80880200.py
#   k1125/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/output/win8-cert-extract-verification-20261120.json
#   k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11
#       research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/certs/win8-root-00000000000000801202000000840500-20261120.n11
#
# Usage: python3 fold_win8_root840500.py  (env FOLD22_W overrides the W root)"""
text = text[:i] + NEW_HDR + text[j:]

# ---------- 2. scalar constants ----------
rep("PIN_F20_MACHINE_SHA256 = '9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72'",
    "PIN_F21_MACHINE_SHA256 = '" + PIN_PUB + "'")
rep("W = os.environ.get('FOLD21_W', '/home/user/work/W21')",
    "W = os.environ.get('FOLD22_W', '/home/user/work/W22')")
rep("OUT = 'fold21/output/win8-root80880200-receipt-fold-20261120.json'",
    "OUT = 'fold22/output/win8-root840500-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000801202000800880200'",
    "ROOT_HEX = '00000000000000801202000000840500'")
rep("CERT_RELPATH = 'k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11'",
    "CERT_RELPATH = 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11'")

# ---------- 3. PIN256 additions ----------
rep(" 'k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11': 'eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf',\n}",
    " 'k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11': 'eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf',\n"
    " 'fold21/output/win8-root80880200-receipt-fold-20261120.json': '" + PIN_F21_RECORD + "',\n"
    " 'k1125/output/win8-cert-extract-verification-20261120.json': '" + PIN_K1125_AUDIT + "',\n"
    " 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11': '" + PIN_K1125_CERT + "',\n}")

# ---------- 4. fold20 machine rerun gate -> fold21 chaining + fold21 rerun gate ----------
rg_first = '# ---------- fold20 machine rerun (published machine pristine; single rerun gate) ----------'
rg_last_tail = "else:\n    print('FOLD_PREVERIFIED_CHAIN=1: fold20 machine rerun gate skipped; upstream via SHA pins + chain recomputation')\n"
if text.count(rg_first) != 1 or text.count(rg_last_tail) != 1:
    die('rerun gate anchors')
NEW_RERUN = """# ---------- fold21 (twenty-eighth, WIN8 root 80880200) record chaining ----------
f21 = load('fold21/output/win8-root80880200-receipt-fold-20261120.json')
need(sha256_of('fold21/output/win8-root80880200-receipt-fold-20261120.json') == PIN256['fold21/output/win8-root80880200-receipt-fold-20261120.json'], 'fold21 record sha256')
need(f21['schema'] == 'n11-five-parent-win8-root80880200-receipt-fold-20261120-v1', 'fold21 schema')
need(f21['status'] == 'fold-complete', 'fold21 fold-complete')
need(f21['receipt_count'] == 1 and len(f21['receipts']) == 1, 'fold21 receipt count')
rc21 = f21['receipts'][0]
rows21 = list(rc21['covered_s6_rows'])
need(len(rows21) == len(set(rows21)) == 8, 'fold21 covered rows unique 8')
for h in rows21:
    need(h in open38, 'fold21 row not open: ' + h)
open35 = {h: v for h, v in open38.items() if h not in set(rows21)}
fa21 = f21['frontier_after']
need(len(open35) == 6136 and sum(v[0] for v in open35.values()) == 486243, 'post-fold21 frontier (must match published 6136/486243)')
need(fa21['unique_remaining_s6'] == 6136 and fa21['sum_remaining_cost'] == 486243
     and fa21['solved_s6_in_manifest'] == 1712 and fa21['parent_row_incidence'] == 11683
     and fa21['s6_needed_by_open_classes'] == 4444 and fa21['cost_needed_by_open_classes'] == 352691, 'fold21 frontier_after published values')
for rec_row in f21['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold21 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows21, 'fold21 coverage row among covered')
need(len(f21['new_receipt_coverage']['rows']) == 8, 'fold21 coverage rows count 8')
need(rc21['closed_edge_cost'] == sum(wl[h][0] for h in rows21), 'fold21 closed edge cost recomputed')
for h in rows21:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11683 == fa21['parent_row_incidence'], 'post-fold21 incidence 11683, got %d' % sum(inc.values()))
targetRows21 = list(rc21['covered_five_parent_target_rows'])
need(set(targetRows21) <= residualSet38 and len(targetRows21) == 3, 'fold21 target rows subset of residual38; exactly 3')
extra21 = [h for h in rows21 if h not in residualSet38]
need(extra21 == rc21['extra_s6_rows_not_in_target'], 'fold21 extra rows recorded')
need(f21['receipt_ordinal'] == 'twenty-eighth (fold21, eleventh WIN8 receipt fold)', 'fold21 ordinal')
residual35 = f21['five_parent_target_after']['residual_row_hex_after']
need(len(residual35) == 35 and len(set(residual35)) == 35 and residual35 == sorted(residual35), 'residual 35 sorted unique')
need(sorted(residualSet38 - set(targetRows21)) == residual35, 'residual35 == residual38 minus fold21 target rows')
need(f21['five_parent_target_after']['closed_target_rows_total'] == 77, 'fold21 closed target 77')
residualSet35 = set(residual35)
need(all(h in open35 for h in residual35), 'residual35 rows open in frontier')
print('post-fold21 frontier verified: 6136/486243, solved_s6 1712, incidence 11683, residual 35')

# ---------- fold21 machine rerun (published machine pristine; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold21 machine is executed PRISTINE (no preverified
# patch is needed: the published fold21 machine already carries the PREVERIFIED
# switch of the adopted redesign) in an isolated W copy; it keeps every input
# pin, the full frontier chain recomputation, the fold20 machine pristine rerun
# gate, the K1124 19-gate block, the K1097 crosscheck and the receipt
# application, so its output must be byte-identical to the published fold21 record.
# When THIS machine is the rerun target of fold23, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    import shutil, subprocess
    _pub21 = open(f'{W}/fold_win8_root80880200.py', 'rb').read()
    need(hashlib.sha256(_pub21).hexdigest() == PIN_F21_MACHINE_SHA256, 'published fold21 machine sha256 pin')
    W21X = W + '-rerun-root-f21'
    if os.path.isdir(W21X): shutil.rmtree(W21X)
    shutil.copytree(W, W21X)
    _env21 = dict(os.environ); _env21['FOLD21_W'] = W21X
    _rr21 = subprocess.run([sys.executable, W21X + '/fold_win8_root80880200.py'], env=_env21, capture_output=True, text=True)
    need(_rr21.returncode == 0, 'fold21 machine pristine rerun failed: ' + _rr21.stderr[-600:])
    _rerun21_sha = hashlib.sha256(open(W21X + '/fold21/output/win8-root80880200-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun21_sha == PIN256['fold21/output/win8-root80880200-receipt-fold-20261120.json'], 'fold21 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W21X)
    print('fold21 machine pristine rerun verified: stdout ends ' + _rr21.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold21 machine rerun gate skipped; upstream via SHA pins + chain recomputation')
"""
i = text.index(rg_first)
j = text.index(rg_last_tail) + len(rg_last_tail)
text = text[:i] + NEW_RERUN + text[j:]

# ---------- 5. K1124 gate block -> K1125 gate block ----------
kb_first = '# ---------- k1124 certificate record (19 gates) ----------'
kb_mid = '# ---------- k1124 geometry independent rederivation ----------'
if text.count(kb_first) != 1 or text.count(kb_mid) != 1:
    die('k-block anchors')
i = text.index(kb_first)
j = text.index(kb_mid) + len(kb_mid)
block = text[i:j]
if block.count('k1124') < 5:
    die('k-block rename sanity')
block = block.replace('k1124', 'k1125').replace('K1124', 'K1125')

def brep(old, new, n=1):
    global block
    c = block.count(old)
    if c != n:
        die('k-block anchor count %d != %d for: %r' % (c, n, old[:90]))
    block = block.replace(old, new)

brep("g['gate'] == 'g05_root_mobility_46'][0]", "g['gate'] == 'g05_root_mobility_58'][0]")
brep("gate05['detail'] == 46 and gate05['passed'] is True, 'k1125 mobility 46'",
     "gate05['detail'] == 58 and gate05['passed'] is True, 'k1125 mobility 58'")
brep("== 618359", "== 736409")
brep("== 669067", "== 878391")
brep("'k1125 uncapped probes 618359/669067 with terminal range [14,18]')",
     "'k1125 uncapped probes 736409/878391 with terminal range [14,18]')")
brep("{'a1_chunk_total_nodes': 1670778, 'b_single_process_nodes': 1383269}",
     "{'a1_chunk_total_nodes': 2310103, 'b_single_process_nodes': 1984636}")
brep("== 934278", "== 1067425")
brep("== 25783", "== 29468", n=2)
brep("tm['root_first_moves'] == 46 and tm['terminal_count'] == 9204 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 57636 and tm['winner_states'] == 37121 and tm['loser_states'] == 11311\n"
     "     and tm['loser_reply_edges'] == 52219, 'k1125 third-method aggregate')",
     "tm['root_first_moves'] == 58 and tm['terminal_count'] == 9810 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 59990 and tm['winner_states'] == 38458 and tm['loser_states'] == 11722\n"
     "     and tm['loser_reply_edges'] == 52360, 'k1125 third-method aggregate')")
text = text[:i] + block + text[j:]

# geometry / verification prints
rep("need(len(lmv) == 46, 'root legal move count rederivation 46')",
    "need(len(lmv) == 58, 'root legal move count rederivation 58')")
rep("print('k1124 certificate record verified: 19/19 gates, sha, header, geometry, mobility 46')",
    "print('k1125 certificate record verified: 19/19 gates, sha, header, geometry, mobility 58')")

# ---------- 6. K1097 crosscheck ----------
rep("need(all(h in residualSet38 for h in CLAIM), 'claim rows inside residual38')",
    "need(all(h in residualSet35 for h in CLAIM), 'claim rows inside residual35')")
rep("need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1089/K1124 claim')",
    "need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1089/K1125 claim')")
rep("need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1089/K1124 claim')",
    "need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1089/K1125 claim')")

# ---------- 7. classification + receipt application on open35 / residualSet35 ----------
rep("    if h in open38: row_class[h] = 'open-frontier'",
    "    if h in open35: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open38)",
    "rootRows = sorted(h for h in rootA if h in open35)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet38)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet35)")
rep("extra_rows = [h for h in rootRows if h not in residualSet38]",
    "extra_rows = [h for h in rootRows if h not in residualSet35]")
rep("closedCost = sum(open38[h][0] for h in rootRows)",
    "closedCost = sum(open35[h][0] for h in rootRows)")
rep("    del open38[h]", "    del open35[h]")
rep("needed_rows = [h for h in open38 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open35 if demand(h)['c1'] == 0]")
rep("  'unique_remaining_s6': len(open38),",
    "  'unique_remaining_s6': len(open35),")
rep("  'sum_remaining_cost': sum(v[0] for v in open38.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open35.values()),")
rep("  'cost_needed_by_open_classes': sum(open38[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open35[h][0] for h in needed_rows),")
rep("closedHistorical |= set(rows20)", "closedHistorical |= set(rows20)\nclosedHistorical |= set(rows21)")
rep("'solved_s6_in_manifest': 1704 + len(rootRows),",
    "'solved_s6_in_manifest': 1712 + len(rootRows),")
rep("closedAllNew = 74 + len(newTargetAll)",
    "closedAllNew = 77 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet38 - newTargetAll)",
    "residualAfter = sorted(residualSet35 - newTargetAll)")
rep("need(len(residualAfter) == 38 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 35 - len(targetRows_new), 'residual accounting')")

# ---------- 8. result record ----------
rep("'schema': 'n11-five-parent-win8-root80880200-receipt-fold-20261120-v1',",
    "'schema': 'n11-five-parent-win8-root840500-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'twenty-eighth (fold21, eleventh WIN8 receipt fold)',",
    "'receipt_ordinal': 'twenty-ninth (fold22, twelfth WIN8 receipt fold)',")
rep("'single_owner_note': 'research/log/2026-11-20-n11-fold21-win8-root80880200-single-owner-note.md',",
    "'single_owner_note': 'research/log/2026-11-20-n11-fold22-win8-root840500-single-owner-note.md',")
rep("'record': 'research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/output/win8-root08d10000-receipt-fold-20261120.json (sha256 76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2)',\n"
    "                    'frontier_after': fa20},",
    "'record': 'research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/output/win8-root80880200-receipt-fold-20261120.json (sha256 " + PIN_F21_RECORD + ")',\n"
    "                    'frontier_after': fa21},")
rep("'record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120 (K1124: WIN8 root certificate extract + triple verification, 19 gates; 46-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with uncapped probes 618359/669067; published by the long lane)',",
    "'record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120 (K1125: WIN8 root certificate extract + triple verification, 19 gates; 58-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with uncapped probes 736409/878391; published by the long lane)',")
rep("'verification_sha256': PIN256['k1124/output/win8-cert-extract-verification-20261120.json'],",
    "'verification_sha256': PIN256['k1125/output/win8-cert-extract-verification-20261120.json'],")
rep("'certificate_path': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/certs/win8-root-00000000000000801202000800880200-20261120.n11',",
    "'certificate_path': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/certs/win8-root-00000000000000801202000000840500-20261120.n11',")
rep("'k1089_sweep_record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/output/.input-k1089.json (K1089 replacement16 sweep record; sha256 808fbda1...; claimed coverage 3 rows, pinned by K1124 g01/g07)',",
    "'k1089_sweep_record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/output/.input-k1089.json (K1089 replacement16 sweep record; sha256 808fbda1...; claimed coverage 3 rows, pinned by K1125 g01/g07)',")
rep("'receipt': 'twenty-eighth',", "'receipt': 'twenty-ninth',")
rep("'legal_next_moves': 46,", "'legal_next_moves': 58,")
rep("'unique_strategy_rows': 25783,", "'unique_strategy_rows': 29468,")
rep("'source_record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120',",
    "'source_record': 'research/experiments/n11-residual45-win8-cert-extract-root840500-20261120',")
rep("'frontier_before': fa20,", "'frontier_before': fa21,")

# win candidate plan impact
rep("fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows) and fold20 retired root 08d10000 (3 claimed rows); this receipt closes the 3 claimed rows of root 80880200 (a K1089 replacement16-sweep WIN candidate inside the same K1097 footprint plan); the remaining 5 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3 = 12 claimed rows",
    "fold19 retired root 1009000 (4 claimed rows), fold20 retired root 08d10000 (3 claimed rows) and fold21 retired root 80880200 (3 claimed rows); this receipt closes the 3 claimed rows of root 840500 (a K1089 replacement16-sweep WIN candidate inside the same K1097 footprint plan); the remaining 4 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3-3 = 9 claimed rows")
rep("'retired_root_predecessor': '00000000000000003800000008d10000',",
    "'retired_root_predecessor': '00000000000000801202000800880200',")
rep("'win16_candidates_remaining': 5,", "'win16_candidates_remaining': 4,")
rep("'win16_claimed_rows_remaining': 12,", "'win16_claimed_rows_remaining': 9,")

# verdict join summary
rep("'join_basis': 'published fold20 chain frontier (single fresh rerun gate: the published fold20 machine executed pristine in an isolated W copy, byte-identical to the published fold20 record; the fold19 machine pristine rerun gate and the K1121 gate block re-run transitively inside it; fold10..fold19 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1124 triple-verified WIN8 certificate + K1089 replacement16-sweep claims and K1097 refsolve coverage footprints',",
    "'join_basis': 'published fold21 chain frontier (single fresh rerun gate: the published fold21 machine executed pristine in an isolated W copy, byte-identical to the published fold21 record; the fold20 machine pristine rerun gate and the K1124 gate block re-run transitively inside it; fold10..fold20 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1125 triple-verified WIN8 certificate + K1089 replacement16-sweep claims and K1097 refsolve coverage footprints',")
rep("'receipt_root_is': 'certificate-backed WIN8-D10 (K1124: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',",
    "'receipt_root_is': 'certificate-backed WIN8-D10 (K1125: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',")

# controls
rep("    'post_fold20_incidence_11701_recomputed': True,",
    "    'post_fold20_incidence_11701_recomputed': True,\n"
    "    'fold21_record_chained_and_published_values_matched': True,\n"
    "    'fold21_frontier_6136_486243_recomputed_from_worklist': True,\n"
    "    'post_fold21_incidence_11683_recomputed': True,")
rep("    'fold20_record_sha256_pin_verified': True,",
    "    'fold20_record_sha256_pin_verified': True,\n    'fold21_record_sha256_pin_verified': True,")
rep("    'fold20_machine_pristine_rerun_byte_identical': True,",
    "    'fold20_machine_pristine_rerun_byte_identical': True,\n    'fold21_machine_pristine_rerun_byte_identical': True,")
rep("    'fold19_machine_pristine_rerun_rechecked_transitively_inside_fold20_rerun': True,",
    "    'fold19_machine_pristine_rerun_rechecked_transitively_inside_fold20_rerun': True,\n    'fold20_machine_pristine_rerun_rechecked_transitively_inside_fold21_rerun': True,")
rep("    'k1124_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1121_cert_gates_rechecked_inside_fold20_pristine_rerun': True,",
    "    'k1125_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1124_cert_gates_rechecked_inside_fold21_pristine_rerun': True,\n    'k1121_cert_gates_rechecked_inside_fold20_pristine_rerun': True,")
rep("os.makedirs(f'{W}/fold21/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold22/output', exist_ok=True)")

# ---------- 9. write + machine checks ----------
open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
for stale in ['PIN_F20_MACHINE_SHA256', '_pub20', 'W20X', '_rr20', "'g05_root_mobility_46'", 'mobility 46',
              '== 618359', '== 669067', '618359/669067', '1670778', '1383269', '934278', '25783',
              '9204', '57636', '37121', '11311', '52219']:
    if stale in text:
        die('stale constant remains: ' + stale)
# positive sanity
assert text.count("ROOT_HEX = '00000000000000801202000000840500'") == 1
assert text.count("OUT = 'fold22/output/win8-root840500-receipt-fold-20261120.json'") == 1
assert text.count("os.environ.get('FOLD22_W'") == 1
assert text.count('# ---------- fold21 (twenty-eighth, WIN8 root 80880200) record chaining ----------') == 1
assert text.count('# ---------- fold21 machine rerun (published machine pristine; single rerun gate) ----------') == 1
assert text.count('closedHistorical |= set(rows21)') == 1
assert text.count('need(len(residualAfter) == 35 - len(targetRows_new)') == 1
assert text.count("'receipt': 'twenty-ninth',") == 1
assert text.count('k1125 uncapped probes 736409/878391') == 1
m = re.search(r'PIN256 = \{(.*?)\n\}', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 43, 'PIN256 count %d' % len(d)
m = re.search(r'PINS = \{(.*?)\n\}', text, re.S)
d = ast.literal_eval(m.group(0).split('=', 1)[1])
assert len(d) == 12, 'PINS count %d' % len(d)
print('BUILD OK:', DST, len(text), 'chars')
print('machine lines:', text.count(chr(10)) + 1)
