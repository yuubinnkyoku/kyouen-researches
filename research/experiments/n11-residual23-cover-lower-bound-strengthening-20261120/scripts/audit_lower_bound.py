#!/usr/bin/env python3
"""Strengthen the residual-23 provider-cover lower bound from pinned K1097/K1102 outputs.
This is arithmetic over independently published exact provider histograms; it does not
rebuild the 120,424-root pool, run probes, or close any game-theoretic row.
"""
import argparse, hashlib, json, math

COMMIT = '259e4019db88395a1b8ca48fda9d0b842665653a'
BASE = f'https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/{COMMIT}/'
SOURCES = {
 'k1097': ('research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json', '2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40'),
 'k1102': ('research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/output/refuted50-refsolve-second-verification-20261120.json', 'd0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b'),
}
EXPECTED_HIST = {'1': 40065, '2': 4857, '3': 297}

def need(ok, msg):
    if not ok: raise RuntimeError(msg)

def sha(b): return hashlib.sha256(b).hexdigest()

def load(path, pin, label):
    raw = open(path, 'rb').read()
    need(sha(raw) == pin, f'{label} SHA-256 mismatch: {sha(raw)}')
    return json.loads(raw)

ap = argparse.ArgumentParser()
ap.add_argument('--k1097', required=True)
ap.add_argument('--k1102', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
k1 = load(a.k1097, SOURCES['k1097'][1], 'K1097')
k2 = load(a.k1102, SOURCES['k1102'][1], 'K1102')

# K1097's histogram is emitted by the exact P''' scan; K1102 independently
# rebuilds all 120,474 safe roots and rederives the same filtered-pool histogram.
g1 = next(g for g in k1['gates'] if g['name'] == 'residual23-demand-on-P-triple-prime')
h1 = {str(k): int(v) for k,v in g1['detail']['provider_coverage_hist_over_23rows'].items()}
v2 = k2['second_verification_results']
h2 = {str(k): int(v) for k,v in v2['provider_hist'].items()}
need(h1 == EXPECTED_HIST, 'K1097 provider histogram mismatch')
need(h2 == EXPECTED_HIST, 'K1102 provider histogram mismatch')
need(h1 == h2, 'independent provider histograms disagree')
rows = len(k1['exclusion']['residual23_rows'])
need(rows == v2['residual23'] == 23, 'residual row count mismatch')
pool = k1['exclusion']['pool_P_triple_prime_size']
need(pool == v2['pool_P_triple_prime'] == 120424, 'filtered pool size mismatch')
providers = sum(h1.values())
need(providers == v2['providers_touching_23rows'] == 45219, 'provider count mismatch')
hist_counts = {int(k): int(v) for k,v in h1.items()}
need(hist_counts == {1:40065, 2:4857, 3:297}, 'provider size histogram mismatch')
max_cover = max(hist_counts)
need(max_cover == 3, 'filtered pool has a provider covering more than 3 rows')
new_lb = (rows + max_cover - 1) // max_cover
need(new_lb == 8, 'derived lower bound mismatch')
eligible_roots = hist_counts[2] + hist_counts[3]
pair_patterns_upper = math.comb(rows, 2)
triple_patterns_upper = min(hist_counts[3], math.comb(rows, 3))
pattern_vars_upper = pair_patterns_upper + triple_patterns_upper
need(eligible_roots == 5154 and pair_patterns_upper == 253
     and triple_patterns_upper == 297 and pattern_vars_upper == 550,
     '8-cover pattern compression arithmetic mismatch')

s1 = k1['scope1_refsolve_residual23']
s2 = k1['scope2_refsolve_need_new_providers']
need(s1['greedy_size'] == s2['greedy_size'] == 9, 'greedy size mismatch')
need(s1['greedy_selection'] == s2['greedy_selection'], 'scope1/scope2 greedy selections differ')
need(s1['leftover_rows'] == s2['leftover_rows'] == [], 'greedy cover leaves rows open')
need(v2['greedy_scope1']['size'] == v2['greedy_scope2']['size'] == 9, 'K1102 greedy size mismatch')
need(s1['gains_hist'] == s2['gains_hist'] == {'1':1,'2':2,'3':6}, 'K1097 gains mismatch')
need(v2['greedy_scope1']['gains_hist'] == v2['greedy_scope2']['gains_hist'] == {'1':1,'2':2,'3':6}, 'K1102 gains mismatch')
gwin = next(g for g in k1['gates'] if g['name'] == 'win16-intrinsic-footprints')
need(gwin['detail']['residual23_covered_by_win_intrinsic'] == 0, 'K1097 WIN16 intrinsic hit')
need(v2['residual23_win_intrinsic_hits'] == [], 'K1102 WIN16 intrinsic hit')
need(v2['matching']['size'] == s1['max_matching'] == 23, 'matching mismatch')
need(s1['lower_bound_rows'] == s2['lower_bound_rows'] == 6, 'legacy lower bound mismatch')

# An 8-root cover can only be (8 triples with exactly one duplicate row) or
# (7 triples + 1 pair, pairwise disjoint); any singleton or two pairs give <=22.
result = {
 'schema':'n11-residual23-cover-lower-bound-strengthening-20261120-v1',
 'source_commit':COMMIT,
 'inputs':{k:{'path':v[0],'sha256':v[1]} for k,v in SOURCES.items()},
 'independent_source_agreement':True,
 'residual_rows':rows,
 'pool_P_triple_prime':pool,
 'providers_touching_residual23':providers,
 'provider_coverage_histogram':h1,
 'eligible_provider_roots_for_8cover':eligible_roots,
 'eight_cover_pattern_variables_upper_bound':pattern_vars_upper,
 'pair_patterns_upper_bound':pair_patterns_upper,
 'triple_patterns_upper_bound':triple_patterns_upper,
 'pattern_compression_factor_at_least':providers // pattern_vars_upper,
 'max_rows_covered_by_one_provider':max_cover,
 'previous_recorded_lower_bound':6,
 'strengthened_lower_bound':new_lb,
 'greedy_cover_size':9,
 'minimum_cover_size_interval':[new_lb,9],
 'scope2_same_bound_reason':'All 16 WIN8 intrinsic footprints have zero intersection with the residual-23 rows; removing those roots does not change the provider histogram.',
 'eight_root_cover_shapes':['8 triples with exactly one duplicated row', '7 triples plus 1 pair with no overlap'],
 'eight_cover_ilp':'At most 550 binary coverage-pattern variables and 23 row constraints; the 40,065 singleton providers cannot occur in an 8-cover.',
 'checks':[
  'K1097 exact filtered-pool provider histogram matches the pinned expected histogram',
  'K1102 independent full-pool verification reports the same filtered-pool histogram',
  'provider histogram totals 45,219 roots and has maximum coverage 3',
  'any 8-cover excludes singletons and at least two pairs; only 8 triples or 7 triples plus 1 pair remain',
  'coverage-pattern compression gives at most 253 pair patterns + 297 triple patterns = 550 variables',
  'both scopes have 23 rows, 9-root greedy cover, and identical gains histogram',
  'WIN16 intrinsic coverage of residual23 is empty in both records',
  'Kuhn/Hopcroft-Karp matching size is 23 in both records',
  'legacy ceil(23/4)=6 is retained as a valid but weaker bound; ceil(23/3)=8 is stronger'
 ],
 'interpretation_guard':[
  'This is a geometric candidate-cover bound, not a game-theoretic verdict.',
  'The audit reads two pinned published summaries; it does not regenerate the 120,424-root pool or rerun any depth-10 probe.',
  'No certificate is extracted and no S6 row is closed.',
  'The 9-root greedy cover is a plan, not a proof that 8 roots are impossible.'
 ]
}
txt = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
with open(a.out, 'w', encoding='utf-8', newline='\n') as f: f.write(txt)
print('WROTE', a.out)
print('sha256', sha(txt.encode()))
print('rows', rows, 'providers', providers, 'max_cover', max_cover, 'lower_bound', new_lb, 'greedy', 9)
