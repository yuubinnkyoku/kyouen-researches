#!/usr/bin/env python3
"""Generate the fold21 machine (fold_win8_root80880200.py) from the PUBLISHED fold20
machine (fold_win8_root08d10000.py, sha256-pinned below), by an exact, asserted
transformation continuing the adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign:

  1. scalar constant replacement (W root env, output path, root hex, cert relpath,
     predecessor machine pin),
  2. three new SHA-256 pins appended to PIN256 (fold20 record, K1124 audit, K1124 cert),
  3. the fold19 machine rerun gate replaced by (a) a fold20 record chaining block
     (frontier 6,152/487,418 -> 6,144/486,819, solved 1,704, incidence 11,701,
     s6_needed 4,452, cost_needed 353,267, residual 41 -> 38, closed target 74)
     and (b) a single rerun gate: one fresh PRISTINE execution of the published
     fold20 machine in an isolated W copy, byte-compared to the published fold20
     record 76fd255b... (the fold19 machine pristine rerun gate and the K1121 gate
     block re-run transitively inside it); guarded by the retained PREVERIFIED
     switch so fold22 can rerun THIS machine in preverified mode,
  4. the K1121 certificate gate block replaced by the K1124 block (all constants
     sourced from the published K1124 audit record; K1089 replacement16-sweep
     basis: g01 master pin 808fbda1..., g08 probe_reproduction_matches_k1089),
     root geometry 46 legal moves,
  5. receipt application against open38 / residualSet38, frontier_after solved base
     1,704, closedAllNew base 74, win16 candidate accounting 6 -> 5 roots / 15 -> 12
     rows, retired_root_predecessor 08d10000,
  6. updated result record literals (schema, ordinal, sources, join summary, controls),
  7. closedHistorical additionally unions the fold20 covered rows (rows20) so that
     rows closed by the fold20 WIN8 receipt classify as 'closed-before-this-receipt'.

Every replacement asserts its occurrence count before applying; the output is
py_compiled, AST-checked and grep-checked for stale constants.

Usage: python3 build_fold21.py [W_root]   (default /home/user/work/W21)
Input:  <W>/fold_win8_root08d10000.py   (published fold20 machine)
Output: <W>/fold_win8_root80880200.py
"""
import hashlib, os, sys, py_compile, ast

W = os.environ.get('BUILD_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W21')
SRC = f'{W}/fold_win8_root08d10000.py'
DST = f'{W}/fold_win8_root80880200.py'
PIN_PUB = '9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72'
PIN_F20_RECORD = '76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2'
PIN_K1124_AUDIT = '422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172'
PIN_K1124_CERT = 'eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf'

def die(m):
    print('BUILD FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold20 machine sha256 mismatch')
text = src.decode()

def rep(old, new, n=1):
    global text
    c = text.count(old)
    if c != n:
        die('anchor count %d != %d for: %r' % (c, n, old[:90]))
    text = text.replace(old, new)

# ---------- 1. header ----------
hdr_first = '# Receipt fold (fold20, twenty-seventh receipt) of the WIN8-D10 certificate of root'
hdr_last = "# Usage: python3 fold_win8_root08d10000.py  (env FOLD20_W overrides the W root)"
if text.count(hdr_first) != 1 or text.count(hdr_last) != 1:
    die('header anchors')
i = text.index(hdr_first)
j = text.index(hdr_last) + len(hdr_last)
NEW_HDR = """# Receipt fold (fold21, twenty-eighth receipt) of the WIN8-D10 certificate of root
# 00000000000000801202000800880200 (K1124: extraction + triple verification, 19-gate
# record sha256 422e6109...; certificate sha256 eca214f0..., 25,783 rows / 934,278
# bytes; the 46-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with
# uncapped probes 618359/669067; extracted and published by the long lane) into the
# five-parent S6 frontier chain -- the eleventh WIN8 receipt fold, executed under the
# adopted FOLD_PREVERIFIED_CHAIN rerun-gate redesign: this machine re-runs only its
# immediate predecessor (the published fold20 machine, executed PRISTINE in an
# isolated W copy -- no preverified patch is needed, because the published fold20
# machine already carries the PREVERIFIED switch and its default full run internally
# re-runs the published fold19 machine pristine, which in turn re-checks the fold18
# preverified rerun and the K1119/K1120/K1121 gate blocks -- and is verified
# byte-identical to the published fold20 record sha256 76fd255b...), and verifies
# fold10..fold19 upstream by SHA pins plus the full frontier chain recomputation,
# giving the open set 6,144 rows / 486,819 cost, solved S6 1,704, parent incidence
# 11,701 and the residual-38 five-parent target (published fold20 values).  The WIN8
# receipt of root 80880200 is then applied: the covered S6 rows of the root are
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
# published fold20 machine, plus):
#   fold20/output/win8-root08d10000-receipt-fold-20261120.json
#       research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/output/win8-root08d10000-receipt-fold-20261120.json
#   fold_win8_root08d10000.py (published fold20 machine; sha256-pinned)
#       research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/scripts/fold_win8_root08d10000.py
#   k1124/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/output/win8-cert-extract-verification-20261120.json
#   k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11
#       research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/certs/win8-root-00000000000000801202000800880200-20261120.n11
#
# Usage: python3 fold_win8_root80880200.py  (env FOLD21_W overrides the W root)"""
text = text[:i] + NEW_HDR + text[j:]

# ---------- 2. scalar constants ----------
rep("PIN_F19_MACHINE_SHA256 = '51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8'",
    "PIN_F20_MACHINE_SHA256 = '" + PIN_PUB + "'")
rep("W = os.environ.get('FOLD20_W', '/home/user/work/W20')",
    "W = os.environ.get('FOLD21_W', '/home/user/work/W21')")
rep("OUT = 'fold20/output/win8-root08d10000-receipt-fold-20261120.json'",
    "OUT = 'fold21/output/win8-root80880200-receipt-fold-20261120.json'")
rep("ROOT_HEX = '00000000000000003800000008d10000'",
    "ROOT_HEX = '00000000000000801202000800880200'")
rep("CERT_RELPATH = 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11'",
    "CERT_RELPATH = 'k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11'")

# ---------- 3. PIN256 additions ----------
rep(" 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11': '8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2',\n}",
    " 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11': '8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2',\n"
    " 'fold20/output/win8-root08d10000-receipt-fold-20261120.json': '" + PIN_F20_RECORD + "',\n"
    " 'k1124/output/win8-cert-extract-verification-20261120.json': '" + PIN_K1124_AUDIT + "',\n"
    " 'k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11': '" + PIN_K1124_CERT + "',\n}")

# ---------- 4. fold19 machine rerun gate -> fold20 chaining + fold20 rerun gate ----------
rg_first = '# ---------- fold19 machine rerun (published machine pristine; single rerun gate) ----------'
rg_last_tail = "else:\n    print('FOLD_PREVERIFIED_CHAIN=1: fold19 machine rerun gate skipped; upstream via SHA pins + chain recomputation')\n"
if text.count(rg_first) != 1 or text.count(rg_last_tail) != 1:
    die('rerun gate anchors')
NEW_RERUN = """# ---------- fold20 (twenty-seventh, WIN8 root 08d10000) record chaining ----------
f20 = load('fold20/output/win8-root08d10000-receipt-fold-20261120.json')
need(sha256_of('fold20/output/win8-root08d10000-receipt-fold-20261120.json') == PIN256['fold20/output/win8-root08d10000-receipt-fold-20261120.json'], 'fold20 record sha256')
need(f20['schema'] == 'n11-five-parent-win8-root08d10000-receipt-fold-20261120-v1', 'fold20 schema')
need(f20['status'] == 'fold-complete', 'fold20 fold-complete')
need(f20['receipt_count'] == 1 and len(f20['receipts']) == 1, 'fold20 receipt count')
rc20 = f20['receipts'][0]
rows20 = list(rc20['covered_s6_rows'])
need(len(rows20) == len(set(rows20)) == 8, 'fold20 covered rows unique 8')
for h in rows20:
    need(h in open41, 'fold20 row not open: ' + h)
open38 = {h: v for h, v in open41.items() if h not in set(rows20)}
fa20 = f20['frontier_after']
need(len(open38) == 6144 and sum(v[0] for v in open38.values()) == 486819, 'post-fold20 frontier (must match published 6144/486819)')
need(fa20['unique_remaining_s6'] == 6144 and fa20['sum_remaining_cost'] == 486819
     and fa20['solved_s6_in_manifest'] == 1704 and fa20['parent_row_incidence'] == 11701
     and fa20['s6_needed_by_open_classes'] == 4452 and fa20['cost_needed_by_open_classes'] == 353267, 'fold20 frontier_after published values')
for rec_row in f20['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold20 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows20, 'fold20 coverage row among covered')
need(len(f20['new_receipt_coverage']['rows']) == 8, 'fold20 coverage rows count 8')
need(rc20['closed_edge_cost'] == sum(wl[h][0] for h in rows20), 'fold20 closed edge cost recomputed')
for h in rows20:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11701 == fa20['parent_row_incidence'], 'post-fold20 incidence 11701, got %d' % sum(inc.values()))
targetRows20 = list(rc20['covered_five_parent_target_rows'])
need(set(targetRows20) <= residualSet41 and len(targetRows20) == 3, 'fold20 target rows subset of residual41; exactly 3')
extra20 = [h for h in rows20 if h not in residualSet41]
need(extra20 == rc20['extra_s6_rows_not_in_target'], 'fold20 extra rows recorded')
need(f20['receipt_ordinal'] == 'twenty-seventh (fold20, tenth WIN8 receipt fold)', 'fold20 ordinal')
residual38 = f20['five_parent_target_after']['residual_row_hex_after']
need(len(residual38) == 38 and len(set(residual38)) == 38 and residual38 == sorted(residual38), 'residual 38 sorted unique')
need(sorted(residualSet41 - set(targetRows20)) == residual38, 'residual38 == residual41 minus fold20 target rows')
need(f20['five_parent_target_after']['closed_target_rows_total'] == 74, 'fold20 closed target 74')
residualSet38 = set(residual38)
need(all(h in open38 for h in residual38), 'residual38 rows open in frontier')
print('post-fold20 frontier verified: 6144/486819, solved_s6 1704, incidence 11701, residual 38')

# ---------- fold20 machine rerun (published machine pristine; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold20 machine is executed PRISTINE (no preverified
# patch is needed: the published fold20 machine already carries the PREVERIFIED
# switch of the adopted redesign) in an isolated W copy; it keeps every input
# pin, the full frontier chain recomputation, the fold19 machine pristine rerun
# gate, the K1121 19-gate block, the K1097 crosscheck and the receipt
# application, so its output must be byte-identical to the published fold20 record.
# When THIS machine is the rerun target of fold22, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    import shutil, subprocess
    _pub20 = open(f'{W}/fold_win8_root08d10000.py', 'rb').read()
    need(hashlib.sha256(_pub20).hexdigest() == PIN_F20_MACHINE_SHA256, 'published fold20 machine sha256 pin')
    W20X = W + '-rerun-root-f20'
    if os.path.isdir(W20X): shutil.rmtree(W20X)
    shutil.copytree(W, W20X)
    _env20 = dict(os.environ); _env20['FOLD20_W'] = W20X
    _rr20 = subprocess.run([sys.executable, W20X + '/fold_win8_root08d10000.py'], env=_env20, capture_output=True, text=True)
    need(_rr20.returncode == 0, 'fold20 machine pristine rerun failed: ' + _rr20.stderr[-600:])
    _rerun20_sha = hashlib.sha256(open(W20X + '/fold20/output/win8-root08d10000-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun20_sha == PIN256['fold20/output/win8-root08d10000-receipt-fold-20261120.json'], 'fold20 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W20X)
    print('fold20 machine pristine rerun verified: stdout ends ' + _rr20.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold20 machine rerun gate skipped; upstream via SHA pins + chain recomputation')
"""
i = text.index(rg_first)
j = text.index(rg_last_tail) + len(rg_last_tail)
text = text[:i] + NEW_RERUN + text[j:]

# ---------- 5. K1121 gate block -> K1124 gate block ----------
kb_first = '# ---------- k1121 certificate record (19 gates) ----------'
kb_mid = '# ---------- k1121 geometry independent rederivation ----------'
if text.count(kb_first) != 1 or text.count(kb_mid) != 1:
    die('k-block anchors')
i = text.index(kb_first)
j = text.index(kb_mid) + len(kb_mid)
block = text[i:j]
if block.count('k1121') < 5:
    die('k-block rename sanity')
block = block.replace('k1121', 'k1124').replace('K1121', 'K1124')

def brep(old, new, n=1):
    global block
    c = block.count(old)
    if c != n:
        die('k-block anchor count %d != %d for: %r' % (c, n, old[:90]))
    block = block.replace(old, new)

brep("g['gate'] == 'g01_k1091_master_sha256_pin'", "g['gate'] == 'g01_k1089_master_sha256_pin'")
brep("need(gate01['detail'] == 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25', 'k1124 k1091 master sha pin')",
     "need(gate01['detail'] == '808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc', 'k1124 k1089 master sha pin')")
brep("g['gate'] == 'g07_k1091_root_claimed_coverage_3rows']", "g['gate'] == 'g07_k1089_root_claimed_coverage_3rows']")
brep("sorted(k1124['recorded']['k1091_claimed_coverage_rows'])", "sorted(k1124['recorded']['k1089_claimed_coverage_rows'])")
brep("g['gate'] == 'g05_root_mobility_50'][0]", "g['gate'] == 'g05_root_mobility_46'][0]")
brep("gate05['detail'] == 50 and gate05['passed'] is True, 'k1124 mobility 50'",
     "gate05['detail'] == 46 and gate05['passed'] is True, 'k1124 mobility 46'")
brep("g['gate'] == 'g08_probe_reproduction_matches_k1091'][0]", "g['gate'] == 'g08_probe_reproduction_matches_k1089'][0]")
brep("g['gate'] == 'g06_k1091_root_probes_win_uncapped'][0]", "g['gate'] == 'g06_k1089_root_probes_win_uncapped'][0]")
brep("== 564695", "== 618359")
brep("== 673870", "== 669067")
brep("'k1124 uncapped probes 564695/673870 with terminal range [14,18]')",
     "'k1124 uncapped probes 618359/669067 with terminal range [14,18]')")
brep("{'a1_chunk_total_nodes': 2428240, 'b_single_process_nodes': 1748509}",
     "{'a1_chunk_total_nodes': 1670778, 'b_single_process_nodes': 1383269}")
brep("== 1026202", "== 934278")
brep("== 28328", "== 25783", n=2)
brep("tm['root_first_moves'] == 50 and tm['terminal_count'] == 15513 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 83544 and tm['winner_states'] == 53570 and tm['loser_states'] == 14461\n"
     "     and tm['loser_reply_edges'] == 72930, 'k1124 third-method aggregate')",
     "tm['root_first_moves'] == 46 and tm['terminal_count'] == 9204 and tm['terminal_range'] == [14, 18]\n"
     "     and tm['visited_states'] == 57636 and tm['winner_states'] == 37121 and tm['loser_states'] == 11311\n"
     "     and tm['loser_reply_edges'] == 52219, 'k1124 third-method aggregate')")
text = text[:i] + block + text[j:]

# geometry / verification prints
rep("need(len(lmv) == 50, 'root legal move count rederivation 50')",
    "need(len(lmv) == 46, 'root legal move count rederivation 46')")
rep("print('k1121 certificate record verified: 19/19 gates, sha, header, geometry, mobility 50')",
    "print('k1124 certificate record verified: 19/19 gates, sha, header, geometry, mobility 46')")

# ---------- 6. K1097 crosscheck ----------
rep("need(all(h in residualSet41 for h in CLAIM), 'claim rows inside residual41')",
    "need(all(h in residualSet38 for h in CLAIM), 'claim rows inside residual38')")
rep("need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1086/K1113 claim')",
    "need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1089/K1124 claim')")
rep("need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1086/K1113 claim')",
    "need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1089/K1124 claim')")

# ---------- 7. classification + receipt application on open38 / residualSet38 ----------
rep("    if h in open41: row_class[h] = 'open-frontier'",
    "    if h in open38: row_class[h] = 'open-frontier'")
rep("rootRows = sorted(h for h in rootA if h in open41)",
    "rootRows = sorted(h for h in rootA if h in open38)")
rep("targetRows_new = sorted(h for h in rootRows if h in residualSet41)",
    "targetRows_new = sorted(h for h in rootRows if h in residualSet38)")
rep("extra_rows = [h for h in rootRows if h not in residualSet41]",
    "extra_rows = [h for h in rootRows if h not in residualSet38]")
rep("closedCost = sum(open41[h][0] for h in rootRows)",
    "closedCost = sum(open38[h][0] for h in rootRows)")
rep("    del open41[h]", "    del open38[h]")
rep("needed_rows = [h for h in open41 if demand(h)['c1'] == 0]",
    "needed_rows = [h for h in open38 if demand(h)['c1'] == 0]")
rep("  'unique_remaining_s6': len(open41),",
    "  'unique_remaining_s6': len(open38),")
rep("  'sum_remaining_cost': sum(v[0] for v in open41.values()),",
    "  'sum_remaining_cost': sum(v[0] for v in open38.values()),")
rep("  'cost_needed_by_open_classes': sum(open41[h][0] for h in needed_rows),",
    "  'cost_needed_by_open_classes': sum(open38[h][0] for h in needed_rows),")
rep("closedHistorical |= set(rows19)", "closedHistorical |= set(rows19)\nclosedHistorical |= set(rows20)")
rep("'solved_s6_in_manifest': 1696 + len(rootRows),",
    "'solved_s6_in_manifest': 1704 + len(rootRows),")
rep("closedAllNew = 71 + len(newTargetAll)",
    "closedAllNew = 74 + len(newTargetAll)")
rep("residualAfter = sorted(residualSet41 - newTargetAll)",
    "residualAfter = sorted(residualSet38 - newTargetAll)")
rep("need(len(residualAfter) == 41 - len(targetRows_new), 'residual accounting')",
    "need(len(residualAfter) == 38 - len(targetRows_new), 'residual accounting')")

# ---------- 8. result record ----------
rep("'schema': 'n11-five-parent-win8-root08d10000-receipt-fold-20261120-v1',",
    "'schema': 'n11-five-parent-win8-root80880200-receipt-fold-20261120-v1',")
rep("'receipt_ordinal': 'twenty-seventh (fold20, tenth WIN8 receipt fold)',",
    "'receipt_ordinal': 'twenty-eighth (fold21, eleventh WIN8 receipt fold)',")
rep("'single_owner_note': 'research/log/2026-11-20-n11-fold20-win8-root08d10000-single-owner-note.md',",
    "'single_owner_note': 'research/log/2026-11-20-n11-fold21-win8-root80880200-single-owner-note.md',")
rep("'record': 'research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json (sha256 c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae)',\n"
    "                    'frontier_after': fa19},",
    "'record': 'research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/output/win8-root08d10000-receipt-fold-20261120.json (sha256 " + PIN_F20_RECORD + ")',\n"
    "                    'frontier_after': fa20},")
rep("'record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120 (K1121: WIN8 root certificate extract + triple verification, 19 gates; 50-mobility 3-claim WIN8 candidate of the K1091 sweep with uncapped probes 564695/673870; published by the parallel lane)',",
    "'record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120 (K1124: WIN8 root certificate extract + triple verification, 19 gates; 46-mobility 3-claim WIN8 candidate of the K1089 replacement16 sweep with uncapped probes 618359/669067; published by the long lane)',")
rep("'verification_sha256': PIN256['k1121/output/win8-cert-extract-verification-20261120.json'],",
    "'verification_sha256': PIN256['k1124/output/win8-cert-extract-verification-20261120.json'],")
rep("'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11',",
    "'certificate_path': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/certs/win8-root-00000000000000801202000800880200-20261120.n11',")
rep("'k1091_probes_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/.input-k1091.json (K1091 alternate-15-roots d10 sweep record; sha256 edd7ac84...; claimed coverage 3 rows, pinned by K1121 g01/g07)',",
    "'k1089_sweep_record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/output/.input-k1089.json (K1089 replacement16 sweep record; sha256 808fbda1...; claimed coverage 3 rows, pinned by K1124 g01/g07)',")
rep("'receipt': 'twenty-seventh',", "'receipt': 'twenty-eighth',")
rep("'legal_next_moves': 50,", "'legal_next_moves': 46,")
rep("'unique_strategy_rows': 28328,", "'unique_strategy_rows': 25783,")
rep("'source_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120',",
    "'source_record': 'research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120',")
rep("'frontier_before': fa19,", "'frontier_before': fa20,")

# win candidate plan impact
rep("fold18 retired root 00901010 (3 claimed rows) and fold19 retired root 1009000 (4 claimed rows); this receipt closes the 3 claimed rows of root 08d10000 (a K1091-sweep WIN candidate inside the same K1097 footprint plan); the remaining 6 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3 = 15 claimed rows",
    "fold18 retired root 00901010 (3 claimed rows), fold19 retired root 1009000 (4 claimed rows) and fold20 retired root 08d10000 (3 claimed rows); this receipt closes the 3 claimed rows of root 80880200 (a K1089 replacement16-sweep WIN candidate inside the same K1097 footprint plan); the remaining 5 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3-3 = 12 claimed rows")
rep("'retired_root_predecessor': '00000000000000801212000001009000',",
    "'retired_root_predecessor': '00000000000000003800000008d10000',")
rep("'win16_candidates_remaining': 6,", "'win16_candidates_remaining': 5,")
rep("'win16_claimed_rows_remaining': 15,", "'win16_claimed_rows_remaining': 12,")

# verdict join summary
rep("'join_basis': 'published fold19 chain frontier (single fresh rerun gate: the published fold19 machine executed pristine in an isolated W copy, byte-identical to the published fold19 record; the fold18 preverified rerun, its reverse-patch preverification and the K1120 gate block re-run transitively inside it; fold10..fold18 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1121 triple-verified WIN8 certificate + K1091 claims and K1097 refsolve coverage footprints',",
    "'join_basis': 'published fold20 chain frontier (single fresh rerun gate: the published fold20 machine executed pristine in an isolated W copy, byte-identical to the published fold20 record; the fold19 machine pristine rerun gate and the K1121 gate block re-run transitively inside it; fold10..fold19 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1124 triple-verified WIN8 certificate + K1089 replacement16-sweep claims and K1097 refsolve coverage footprints',")
rep("'receipt_root_is': 'certificate-backed WIN8-D10 (K1121: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',",
    "'receipt_root_is': 'certificate-backed WIN8-D10 (K1124: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',")

# controls
rep("    'post_fold19_incidence_11711_recomputed': True,",
    "    'post_fold19_incidence_11711_recomputed': True,\n"
    "    'fold20_record_chained_and_published_values_matched': True,\n"
    "    'fold20_frontier_6144_486819_recomputed_from_worklist': True,\n"
    "    'post_fold20_incidence_11701_recomputed': True,")
rep("    'fold19_record_sha256_pin_verified': True,",
    "    'fold19_record_sha256_pin_verified': True,\n    'fold20_record_sha256_pin_verified': True,")
rep("    'fold19_machine_pristine_rerun_byte_identical': True,",
    "    'fold20_machine_pristine_rerun_byte_identical': True,")
rep("    'fold18_preverified_rerun_and_reverse_patch_rechecked_transitively_inside_fold19_rerun': True,",
    "    'fold19_machine_pristine_rerun_rechecked_transitively_inside_fold20_rerun': True,")
rep("    'k1121_cert_19_gates_rechecked_and_bytes_verified': True,",
    "    'k1124_cert_19_gates_rechecked_and_bytes_verified': True,\n    'k1121_cert_gates_rechecked_inside_fold20_pristine_rerun': True,")
rep("os.makedirs(f'{W}/fold20/output', exist_ok=True)",
    "os.makedirs(f'{W}/fold21/output', exist_ok=True)")

# ---------- 9. write + machine checks ----------
open(DST, 'w').write(text)
py_compile.compile(DST, doraise=True)
ast.parse(text)
for stale in ["'g01_k1091_master_sha256_pin'", 'k1091_claimed_coverage_rows', 'edd7ac84', '_pub19', 'W19X',
              'PIN_F19_MACHINE_SHA256', '== 564695', '== 673870', '564695/673870', '2428240', '1748509',
              '1026202', '28328', '15513', '83544', '53570', '14461', '72930', 'FOLD20_W,',
              "'g08_probe_reproduction_matches_k1091'", "'g06_k1091'", "'g07_k1091'", 'mobility 50', 'k1091_probes_record']:
    if stale in text:
        die('stale constant remains: ' + stale)
# positive sanity
assert text.count("ROOT_HEX = '00000000000000801202000800880200'") == 1
assert text.count("OUT = 'fold21/output/win8-root80880200-receipt-fold-20261120.json'") == 1
assert text.count('fold20/output/win8-root08d10000-receipt-fold-20261120.json') == 7
assert text.count('# ---------- fold20 (twenty-seventh, WIN8 root 08d10000) record chaining ----------') == 1
assert text.count('# ---------- fold20 machine rerun (published machine pristine; single rerun gate) ----------') == 1
assert text.count('closedHistorical |= set(rows20)') == 1
print('BUILD OK:', DST, len(text), 'chars')
print('machine lines:', text.count(chr(10)) + 1)
