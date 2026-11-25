#!/usr/bin/env python3
# Eighth WIN7-D10 receipt fold: chain on the seventh fold (fold_seventh.py re-executed
# with all gates), then fold the eighth receipt root 00000000040000801202000000100001
# (sweep6 WIN among the zero-cover-in-86 candidates; closes a class-2 S6 frontier row).
import json, os, time, hashlib, glob
t_start = time.time()
W = '/home/user/work'
g8 = {'__name__': 'chainbase8', '__file__': os.path.abspath('fold_seventh.py')}
exec(compile(open(os.path.abspath('fold_seventh.py')).read(), 'fold_seventh.py', 'exec'), g8)
need = g8['need']; canon_int = g8['canon_int']; canon_hex = g8['canon_hex']
popcount = g8['popcount']; unsafe_quadruples = g8['unsafe_quadruples']
legal_moves_of = g8['legal_moves_of']; row_parents_hex = g8['row_parents_hex']
demand = g8['demand']; root_row_set = g8['root_row_set']
openCur = g8['openCur']; incidence = g8['incidence']; totalClosed = list(g8['totalClosed'])
parents = g8['parents']; target112 = g8['target112']; targetResidual = g8['targetResidual']
fa23 = g8['fa23']; res = g8['res']; open2 = g8['open2']; receipts = [dict(r) for r in g8['receipts']] + [g8['recG']]
print('chained on the 4/5/6+7 fold state; openCur rows:', len(openCur))

H = '00000000040000801202000000100001'
D8 = f'{W}/cert7/out8'
s = json.load(open(f'{D8}/win7-root-{H}-extraction-summary-20261119.json'))
v = json.load(open(f'{D8}/win7-root-{H}-independent-verification-20261119.json'))
u = json.load(open(f'{D8}/win7-root-{H}-bareiss-union-audit-20261119.json'))
bl = [json.loads(l) for l in open(f'{D8}/win7-root-{H}-bareiss-subroots-20261119.jsonl').read().strip().splitlines()]
br, bb = bl[0], bl[1]
stats = list(bb['stats'].values()) if isinstance(bb['stats'], dict) else bb['stats']
n_moves = s['legal_next_moves']
need(s['root'] == H and s['status'] == 'EXTRACTED_UNVERIFIED' and s['fbt_drops'] == 0 and s['failure'] is None, 'H extraction gate')
need(s['completed_moves'] == n_moves == 58, 'H completed moves 58')
lmv = legal_moves_of(int(H, 16))
need(len(lmv) == n_moves and lmv == s['completed_move_list'], 'H legal move rederivation vs summary')
cert_bytes = open(f'{D8}/win7-root-{H}-20261119.n11', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == s['certificate_sha256'], 'H certificate sha256 mismatch')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0].startswith('n11-terminal-strategy-v1') and cert_lines[1] == 'root ' + H, 'H cert header')
need(len(cert_lines) - 2 == s['unique_strategy_rows'] == 39163, 'H cert row count 39163')
need(v['verdict'] == 'WIN7 certificate independently verified' and v['root_hex'] == H and v['root_safe'] is True
     and v['root_mobility'] == n_moves and v['subroots_passed'] == n_moves and v['union_missing'] == 0 and v['union_extra'] == 0
     and v['strategy_rows'] == s['unique_strategy_rows'] and v['consumed_winner_rows'] == s['unique_strategy_rows'], 'H independent verifier gate')
need(br['stones'] == 7 and br['loserMobility'] == n_moves and bb['rows'] == s['unique_strategy_rows'] and len(stats) == n_moves, 'H bareiss root/subroots')
seen = sum(x['seen'] for x in stats); terms = sum(x['terminals'] for x in stats); oedg = sum(x['opponentEdges'] for x in stats)
tmin = min(x['range'][0] for x in stats); tmax = max(x['range'][1] for x in stats)
need(v['visited_states_across_subroots'] == seen and v['terminal_count'] == terms and v['loser_reply_edges'] == oedg, 'H cross-method state flow')
need(tmin == 13 and tmax == 17, 'H terminal range agreement')
need(u['exact_union'] is True and u['missing'] == 0 and u['extra'] == 0 and u['certificate_rows'] == s['unique_strategy_rows'] and u['consumed_unique'] == s['unique_strategy_rows'], 'H bareiss consumed-union audit')
pr6 = []
for f in glob.glob(f'{W}/sweep6/output/probe-records-w*.jsonl'):
    for line in open(f):
        d = json.loads(line)
        if d['root'] == H and d.get('result'):
            pr6.append({'ordering': d['ordering'], 'nodes': d['result']['nodes'], 'loss': d['result']['loss'], 'capped': d['result']['capped'], 'pilot_nodes': d['control']['nodes']})
need(len(pr6) == 2 and all(p['loss'] is True and not p['capped'] and p['pilot_nodes'] == 3402 for p in pr6), 'H win probe both orderings')
evidenceH = {
  'root': H, 'name': 'eighth', 'published_item': 'this run (sweep6 WIN among zero-cover-in-86 candidates)',
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
  'win_probe_runs': {'source': 'sweep6 (this run)', 'orderings': pr6,
                     'note': 'both AND orderings uncapped loss=true; candidate covered zero rows of the residual 86 five-parent targets, but closes one open class-2 frontier S6 row'},
  'legal_rederivation_matches': True,
}
print('eighth receipt evidence gates passed')

mask = int(H, 16)
need(popcount(mask) == 7 and format(canon_int(mask), '032x') == H, 'H root canonical')
need(unsafe_quadruples(mask) == 0, 'H unsafe quadruples')
rootRows = root_row_set(H, {**openCur})
for h in rootRows: need(h in openCur, 'H row not open ' + h)
need(rootRows == ['00000000000000801202000000100001'], 'H single class-2 frontier row')
for h in rootRows: need(h not in totalClosed, 'H row closed twice ' + h)
closedCost = sum(openCur[h][0] for h in rootRows)
need(closedCost == 74, 'H closed cost 74')
targetRowsH = sorted(h for h in rootRows if h in targetResidual)
need(targetRowsH == [], 'H closes no five-parent target row (class-2 frontier row only)')
deltas = {}
for h in rootRows:
    for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
pdeltas = []
for p in sorted(deltas):
    before = incidence[p]
    after = before - deltas[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before,
                    'rows_closed': deltas[p], 'rows_after': after})
for h in rootRows: del openCur[h]
for h in rootRows:
    for p in row_parents_hex(h): incidence[p] -= 1
recH = {
  'root': H, 'receipt': 'eighth', 'published_item': evidenceH['published_item'],
  'added_bit': evidenceH['added_bit'], 'child_hex': evidenceH['child'],
  'legal_next_moves': evidenceH['legal_next_moves'],
  'covered_s6_rows': rootRows,
  'covered_five_parent_target_rows': targetRowsH,
  'extra_s6_rows_not_in_target': [h for h in rootRows if h not in targetResidual],
  'unique_strategy_rows': evidenceH['unique_strategy_rows'],
  'total_nodes': evidenceH['total_nodes'],
  'closed_edge_cost': closedCost,
  'affected_parents': len(pdeltas),
  'parent_deltas': pdeltas,
  'evidence': evidenceH,
}
totalClosed.extend(rootRows)

need(len(openCur) == 6222, 'frontier rows 6222, got %d' % len(openCur))
need(fa23['solved_s6_in_manifest'] + len(totalClosed) == 1626, 'solved S6 1626')
needed_rows = [h for h in openCur if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1626,
  'remaining_s5_orbits': sum(1 for p in incidence.values() if p > 0),
  'unique_remaining_s6': len(openCur),
  'sum_remaining_cost': sum(v[0] for v in openCur.values()),
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(openCur[h][0] for h in needed_rows),
  'parent_row_incidence': sum(incidence.values()),
}
need(frontier_after['sum_remaining_cost'] == 492762 - 74, 'sum cost after H fold')
need(frontier_after['parent_row_incidence'] == 11848, 'incidence 11848')

closedAll = set()
closedAll |= set(res['receipts']['first_win7_target_rows'])
closedAll |= set(res['receipts']['second_third_win7_target_rows'])
gHits = [h for h in target112 if h in set(x['row_hex'] for x in g8['g']['gf']['receipts_by_row'])]
lHits = [h for h in target112 if h in set(x['row_hex'] for x in g8['g']['prev']['new_receipt_coverage']['receipts_by_row'])]
closedAll |= set(gHits) | set(lHits)
newTarget = [h for r in receipts + [recH] for h in r['covered_five_parent_target_rows']]
closedAll |= set(newTarget)
need(len(closedAll) == 26, 'closed target rows still 26 (H closes none)')
targetAfter = [h for h in target112 if h not in closedAll]
need(len(targetAfter) == 86, 'residual target rows still 86')
record = {
  'schema': 'n11-five-parent-eighth-win7-receipt-fold-20261119-v1',
  'date': '2026-11-19',
  'status': 'fold-complete',
  'implementation_note': 'chains on fold_seventh.py (re-executed with all gates: base 4/5/6 + seventh fold) and folds the eighth receipt root discovered by the 6-root zero-cover sweep of this run.',
  'environment_note': 'composed in the Vibe sandbox 2026-11-19; no GitHub push transport this run; record held in lane Knowledge for publication by a later run.',
  'receipt_count': 1,
  'receipts': [recH],
  'frontier_before': {'unique_remaining_s6': 6223, 'sum_remaining_cost': 492762, 'solved_s6_in_manifest': 1625, 'source': 'seventh-win7-receipt-fold-20261119.json'},
  'new_receipt_coverage': {
    'unique_s6_rows': len(rootRows),
    'closed_edge_cost': closedCost,
    'rows': [{'row_hex': h, 'cost': open2[h][0], 'category': open2[h][1], 'demand': demand(h),
              'parents': sorted(row_parents_hex(h)), 'receipt': {'root': H, 'verdict': 'WIN7-D10'}} for h in sorted(rootRows)]
  },
  'parent_closure': {
    'fully_closed_parent_count': sum(1 for p in pdeltas if p['rows_after'] == 0),
    'affected_unique_parents': len(set(p['parent_hex'] for p in pdeltas))
  },
  'frontier_after': frontier_after,
  'five_parent_residual_cover_after': {
    'rows': len(targetAfter),
    'closed_target_rows_total': len(closedAll),
    'eighth_target_rows': targetRowsH,
    'remaining_book': 'unchanged by the eighth fold: the residual 86 five-parent target rows remain stranded within the 117-root pool at depth 10 (resolve3 record).',
  },
  'controls': {
    'base_state_reexecuted_all_gates_pass': True,
    'receipt_rows_rederived_from_all_8_d4_images': True,
    'receipt_rows_were_open_before_fold': True,
    'receipts_disjoint_from_first_seven': True,
    'certificates_sha256_verified': True,
    'dual_independent_verification_gates_pass': True,
    'win_probe_both_orderings_uncapped': True,
    'legal_move_list_independently_rederived': True,
    'win_loss_conflicts': 0,
    'frontier_after_6222_rows': len(openCur) == 6222,
    'solved_s6_1626': frontier_after['solved_s6_in_manifest'] == 1626,
    'target_unchanged_26_of_112': len(closedAll) == 26,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from this individual seven-stone root.',
    'This fold closes one open class-2 frontier S6 row; it does not touch the five-parent target book and proves nothing about the empty board or two-stone roots.',
    'REFUTED-D10 is NOT a LOSS proof.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
}
outp = f'{W}/foldv2/output/eighth-win7-receipt-fold-20261119.json'
with open(outp, 'w') as f:
    json.dump(record, f, indent=1)
    f.write('\n')
print(json.dumps({'status': record['status'], 'folded_rows': rootRows, 'cost': closedCost,
                  'frontier_after': frontier_after, 'cert_sha256': s['certificate_sha256'],
                  'sha256_record': hashlib.sha256(open(outp,'rb').read()).hexdigest(), 'wall_seconds': round(time.time()-t_start,1)}, indent=1))
