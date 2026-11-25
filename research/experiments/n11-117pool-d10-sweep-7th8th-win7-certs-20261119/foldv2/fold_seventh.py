#!/usr/bin/env python3
# Seventh WIN7-D10 receipt fold: chain on the 4/5/6 fold state (fold_fourth_fifth_sixth.py
# is re-executed with all its gates), then fold the seventh receipt root
# 00000000040080801202000000100000 (sweep35 WIN, dual-verified certificate).
import json, os, sys, time, hashlib
t_start = time.time()
W = '/home/user/work'
g = {'__name__': 'chainbase', '__file__': os.path.abspath('fold_fourth_fifth_sixth.py')}
src = open(os.path.abspath('fold_fourth_fifth_sixth.py')).read()
exec(compile(src, 'fold_fourth_fifth_sixth.py', 'exec'), g)
need = g['need']; canon_int = g['canon_int']; canon_hex = g['canon_hex']
transform = g['transform']; popcount = g['popcount']; bits_of = g['bits_of']
unsafe_quadruples = g['unsafe_quadruples']; legal_moves_of = g['legal_moves_of']
row_parents_hex = g['row_parents_hex']; demand = g['demand']; root_row_set = g['root_row_set']
openCur = g['openCur']; incidence = g['incidence']; totalClosed = list(g['totalClosed'])
parents = g['parents']; target112 = g['target112']; targetResidual = g['targetResidual']
fa23 = g['fa23']; res = g['res']; receipts = [dict(r) for r in g['receipts']]
open2 = g['open2']
print('chained on the 4/5/6 fold state; openCur rows:', len(openCur))

G = '00000000040080801202000000100000'
# ---- seventh receipt evidence gates (mirror the D/E gates of the base machine) ----
D7 = f'{W}/cert7/out7'
s = json.load(open(f'{D7}/win7-root-{G}-extraction-summary-20261119.json'))
v = json.load(open(f'{D7}/win7-root-{G}-independent-verification-20261119.json'))
u = json.load(open(f'{D7}/win7-root-{G}-bareiss-union-audit-20261119.json'))
bl = [json.loads(l) for l in open(f'{D7}/win7-root-{G}-bareiss-subroots-20261119.jsonl').read().strip().splitlines()]
br, bb = bl[0], bl[1]
stats = list(bb['stats'].values()) if isinstance(bb['stats'], dict) else bb['stats']
n_moves = s['legal_next_moves']
need(s['root'] == G and s['status'] == 'EXTRACTED_UNVERIFIED' and s['fbt_drops'] == 0 and s['failure'] is None, 'G extraction gate')
need(s['completed_moves'] == n_moves == 51, 'G completed moves 51')
lmv = legal_moves_of(int(G, 16))
need(len(lmv) == n_moves and lmv == s['completed_move_list'], 'G legal move rederivation vs summary')
cert_bytes = open(f'{D7}/win7-root-{G}-20261119.n11', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == s['certificate_sha256'], 'G certificate sha256 mismatch')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0].startswith('n11-terminal-strategy-v1') and cert_lines[1] == 'root ' + G, 'G cert header')
need(len(cert_lines) - 2 == s['unique_strategy_rows'] == 21829, 'G cert row count 21829')
need(v['verdict'] == 'WIN7 certificate independently verified' and v['root_hex'] == G and v['root_safe'] is True
     and v['root_mobility'] == n_moves and v['subroots_passed'] == n_moves and v['union_missing'] == 0 and v['union_extra'] == 0
     and v['strategy_rows'] == s['unique_strategy_rows'] and v['consumed_winner_rows'] == s['unique_strategy_rows'], 'G independent verifier gate')
need(br['stones'] == 7 and br['loserMobility'] == n_moves and bb['rows'] == s['unique_strategy_rows'] and len(stats) == n_moves, 'G bareiss root/subroots')
seen = sum(x['seen'] for x in stats); terms = sum(x['terminals'] for x in stats); oedg = sum(x['opponentEdges'] for x in stats)
tmin = min(x['range'][0] for x in stats); tmax = max(x['range'][1] for x in stats)
need(v['visited_states_across_subroots'] == seen and v['terminal_count'] == terms and v['loser_reply_edges'] == oedg, 'G cross-method state flow')
need(tmin == s['terminal_stone_range'][0] and tmax == s['terminal_stone_range'][1] and v['terminal_range'][0] == tmin and v['terminal_range'][1] == tmax, 'G terminal range agreement')
need(u['exact_union'] is True and u['missing'] == 0 and u['extra'] == 0 and u['certificate_rows'] == s['unique_strategy_rows'] and u['consumed_unique'] == s['unique_strategy_rows'], 'G bareiss consumed-union audit')
# sweep35 WIN probe runs (both orderings)
s35 = json.load(open(f'{W}/sweep35/output/eligible-29-candidate-root-depth10-sweep-20261119.json'))
need(G in s35['classification']['win7_d10']['roots'] and s35['classification']['win7_d10']['count'] == 1, 'G sweep35 WIN gate')
pr35 = []
import glob
for f in glob.glob(f'{W}/sweep35/output/probe-recordsfix-w*.jsonl') + glob.glob(f'{W}/sweep35/output/round1-quarantine/probe-records-w*.jsonl'):
    for line in open(f):
        d = json.loads(line)
        if d['root'] == G and d.get('result'):
            pr35.append({'ordering': d['ordering'], 'nodes': d['result']['nodes'], 'loss': d['result']['loss'], 'capped': d['result']['capped'], 'pilot_nodes': d['control']['nodes']})
need(len(pr35) == 2 and all(p['loss'] is True and not p['capped'] and p['pilot_nodes'] == 3402 for p in pr35), 'G win probe both orderings')
evidenceG = {
  'root': G, 'name': 'seventh', 'published_item': 'this run (sweep35 WIN; certificate publication pending)',
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
  'win_probe_runs': {'source': 'sweep35 (this run)', 'orderings': pr35,
                     'note': 'both AND orderings uncapped loss=true; this run also holds the round-1 quarantined records'},
  'legal_rederivation_matches': True,
}
print('seventh receipt evidence gates passed')

# ---- fold the seventh receipt ----
mask = int(G, 16)
need(popcount(mask) == 7 and int(canon_hex(mask), 16) == mask and format(canon_int(mask), '032x') == G, 'G root canonical')
need(unsafe_quadruples(mask) == 0, 'G unsafe quadruples')
rootRows = root_row_set(G, {**openCur})
for h in rootRows: need(h in openCur, 'G row not open ' + h)
witness2 = {x['root']: x for x in json.load(open(f'{W}/foldv2/output/post-sixth-receipt-cover-resolve2-with-sweep-20261119.json'))['witness']}
wt = witness2.get(G)
need(wt is not None, 'G witness entry missing in resolve2 record')
targetRowsG = sorted(h for h in rootRows if h in targetResidual)
need(targetRowsG == sorted(wt['rows']), 'G independent root-to-target-row join mismatch (resolve2 witness)')
need(len(targetRowsG) == 1, 'G single target row')
for h in rootRows:
    need(h not in totalClosed, 'G row closed twice ' + h)
closedCost = sum(openCur[h][0] for h in rootRows)
deltas = {}
for h in rootRows:
    for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
pdeltas = []
for p in sorted(deltas):
    before = incidence[p]
    after = before - deltas[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before,
                    'rows_closed': deltas[p], 'rows_after': after})
for h in rootRows:
    del openCur[h]
for h in rootRows:
    for p in row_parents_hex(h): incidence[p] -= 1
recG = {
  'root': G, 'receipt': 'seventh', 'published_item': evidenceG['published_item'],
  'added_bit': evidenceG['added_bit'], 'child_hex': evidenceG['child'],
  'legal_next_moves': evidenceG['legal_next_moves'],
  'covered_s6_rows': rootRows,
  'covered_five_parent_target_rows': targetRowsG,
  'extra_s6_rows_not_in_target': [h for h in rootRows if h not in targetResidual],
  'unique_strategy_rows': evidenceG['unique_strategy_rows'],
  'total_nodes': evidenceG['total_nodes'],
  'closed_edge_cost': closedCost,
  'affected_parents': len(pdeltas),
  'parent_deltas': pdeltas,
  'evidence': evidenceG,
}
totalClosed.extend(rootRows)
print('G folded: rows', rootRows, 'cost', closedCost)

# ---- frontier after 4/5/6/7 ----
need(len(openCur) == 6223, 'frontier rows 6223, got %d' % len(openCur))
need(g['fa23']['solved_s6_in_manifest'] + len(totalClosed) == 1625, 'solved S6 1625')
sumcost = sum(v[0] for v in openCur.values())
needed_rows = [h for h in openCur if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1625,
  'remaining_s5_orbits': sum(1 for p in incidence.values() if p > 0),
  'unique_remaining_s6': len(openCur),
  'sum_remaining_cost': sumcost,
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(openCur[h][0] for h in needed_rows),
  'parent_row_incidence': sum(incidence.values()),
}
need(frontier_after['sum_remaining_cost'] == 492830 - closedCost, 'sum cost after G fold')
need(frontier_after['parent_row_incidence'] == 11852 - sum(len(row_parents_hex(h)) for h in rootRows), 'incidence delta (post-4/5/6 base is 11852)')

# ---- five-parent residual cover after ----
closedAll = set()
closedAll |= set(res['receipts']['first_win7_target_rows'])
closedAll |= set(res['receipts']['second_third_win7_target_rows'])
gHits = [h for h in target112 if h in set(x['row_hex'] for x in g['gf']['receipts_by_row'])]
lHits = [h for h in target112 if h in set(x['row_hex'] for x in g['prev']['new_receipt_coverage']['receipts_by_row'])]
closedAll |= set(gHits) | set(lHits) | set(gHits)
newTarget = [h for r in receipts + [recG] for h in r['covered_five_parent_target_rows']]
closedAll |= set(newTarget)
need(len(closedAll) == 26, 'closed target rows 26, got %d' % len(closedAll))
targetAfter = [h for h in target112 if h not in closedAll]
need(len(targetAfter) == 86, 'residual target rows 86')
record = {
  'schema': 'n11-five-parent-seventh-win7-receipt-fold-20261119-v1',
  'date': '2026-11-19',
  'status': 'fold-complete',
  'implementation_note': 'chains on fold_fourth_fifth_sixth.py (re-executed with all gates; its own record is the 4/5/6 fold) and folds the seventh receipt root discovered by the 29-candidate sweep35 of this run.',
  'environment_note': 'composed in the Vibe sandbox 2026-11-19; this run had no GitHub push transport, so the record is held in the lane Knowledge with exact values for publication by a later run.',
  'receipt_count': 1,
  'receipts': [recG],
  'frontier_before': {'unique_remaining_s6': 6224, 'sum_remaining_cost': 492830, 'solved_s6_in_manifest': 1624, 'source': 'fourth-fifth-sixth-win7-receipt-fold-20261119.json (this run, epoch-1 crosschecked)'},
  'new_receipt_coverage': {
    'unique_s6_rows': len(rootRows),
    'closed_edge_cost': closedCost,
    'rows': [{'row_hex': h, 'cost': open2[h][0], 'category': open2[h][1], 'demand': demand(h),
              'parents': sorted(row_parents_hex(h)), 'receipt': {'root': G, 'verdict': 'WIN7-D10'}} for h in sorted(rootRows)]
  },
  'parent_closure': {
    'fully_closed_parent_count': sum(1 for p in pdeltas if p['rows_after'] == 0),
    'affected_unique_parents': len(set(p['parent_hex'] for p in pdeltas))
  },
  'frontier_after': frontier_after,
  'five_parent_residual_cover_after': {
    'rows': len(targetAfter),
    'closed_target_rows_total': len(closedAll),
    'seventh_target_rows': sorted(targetRowsG),
    'remaining_book': 'post-sweep35 re-solve recorded separately (resolve3): all 28 other covering candidates are REFUTED-D10, so the residual 86 rows are stranded within the 117-root pool at depth 10.',
  },
  'controls': {
    'base_state_reexecuted_all_gates_pass': True,
    'receipt_rows_rederived_from_all_8_d4_images': True,
    'receipt_target_rows_match_resolve2_witness_join': True,
    'receipt_rows_were_open_before_fold': True,
    'receipts_disjoint_from_first_six': True,
    'certificates_sha256_verified': True,
    'dual_independent_verification_gates_pass': True,
    'win_probe_both_orderings_uncapped': True,
    'legal_move_list_independently_rederived': True,
    'win_loss_conflicts': 0,
    'frontier_after_6223_rows': len(openCur) == 6223,
    'solved_s6_1625': frontier_after['solved_s6_in_manifest'] == 1625,
    'target_26_of_112': len(closedAll) == 26,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone root of this receipt.',
    'This fold closes S6 rows in the frontier; it does not prove a win from the empty board or any two-stone root.',
    'REFUTED-D10 is NOT a LOSS proof.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
}
outp = f'{W}/foldv2/output/seventh-win7-receipt-fold-20261119.json'
with open(outp, 'w') as f:
    json.dump(record, f, indent=1)
    f.write('\n')
print(json.dumps({'status': record['status'], 'folded_rows': rootRows, 'cost': closedCost,
                  'frontier_after': frontier_after, 'closed_target_total': len(closedAll), 'residual': len(targetAfter),
                  'cert_sha256': s['certificate_sha256'], 'sha256_record': hashlib.sha256(open(outp,'rb').read()).hexdigest(),
                  'wall_seconds': round(time.time()-t_start,1)}, indent=1))
